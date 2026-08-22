# open-webui-iac

> Parent Skill Definition: [open-webui-iac](file:///home/jpino/Obsidian/Common/_Meta/Skills/open-webui-iac/SKILL.md)

---
name: open-webui-iac
description: "Operational skill for provisioning Open WebUI via SQLite, enforcing Infrastructure-as-Code (IaC), managing cache invalidation, and avoiding global persona prompt bloat."
---

# Open WebUI IaC Drift Management

## 1. Context and The "Invisible Payload" Problem
Open WebUI is highly stateful. It stores configurations like custom tools, models, and fallback globals in a local SQLite database (`webui.db`) and aggressively caches this database in its FastAPI backend memory.
If a custom agent persona (e.g., `kern-vault-assistant` / Hermes) is mistakenly registered as an Open WebUI "Model," its base context (often >6,000 tokens) becomes stored in the `model` table. 

Due to Open WebUI's inheritance mechanics, these massive prompts can be globally applied to other naive models (like `muse-glimmer`) leading to **invisible configuration drift and severe latency (45+ seconds per query)**.

## OpenCode Planner & Context Architecture

When pairing Open WebUI and OpenCode AI architecture:
- `muse-glimmer` (30B) running on `llama-server` is configured natively with a **32k context window** to absorb massive OpenCode codebase RAG payloads.
- **The Prefill Penalty:** While 32k context avoids crashes, injecting 23,000+ tokens of codebase context incurs a significant hardware math penalty. The Ryzen AI 9 iGPU evaluates prompt prefill at **~75 tokens per second**. A 23k token payload will take **~5 minutes** to process before generating the first reasoning trace.
- **Workflow Optimization:**
  1. For interactive, zero-latency triage: use NPU (`fastflowlm` on `:11435`).
  2. For instant Chat/Reasoning: use Open WebUI (which avoids the 23k workspace dump).
  3. For heavy codebase coding: use `qwen2.5-coder` on Ollama (`:11434`).
  4. For background agentic planning: use `muse-glimmer` on `llama-server` (`:11436`), knowing the 5-minute prefill is an acceptable asynchronous delay.

## 2. Safe Provisioning Standards

When making changes to Open WebUI configurations (e.g., registering new tools, removing rogue system prompts, updating base URLs):

1. **Use `provision_owui.py`:** Always modify the database via direct `docker exec` SQLite queries using `Common/_Meta/Scripts/provision_owui.py`. Do not rely on the Open WebUI web interface.
2. **Never Inject Personas as Global Models:** ECC personas (like Hermes) should be run natively or via specific external APIs, never stored as a persistent model in `webui.db` where its `VAULT_CONTEXT_BASE.md` might bleed into other chats.

## 3. The Mandatory Restart Rule
Because Open WebUI's Python backend reads `webui.db` into memory at startup, any native modifications you perform on the `.db` file using `sqlite3` will **NOT** be reflected in the user's browser, and the backend will continue to serve stale, bloated payloads.

**CRITICAL:** Every automated modification to `webui.db` must be followed by a container restart to flush the memory cache:
```bash
docker restart open-webui
```
Failure to restart the container will leave the frontend and backend unsynced, causing persistent ghost latency issues.

## 4. UI Default Models Type Safety (SvelteKit Split Bug)
In Open WebUI v0.11.0, the SvelteKit frontend evaluates `(ft=i())!=null&&ft.default_models ? it.default_models.split(",") : []`. 
If `ui.default_models` is stored as `'[]'` (a JSON array) in `webui.db`, the FastAPI backend returns `default_models: []` (a list). Because `[]` is truthy in JavaScript, the frontend attempts to call `[].split(",")`, which throws `TypeError: default_models.split is not a function` during component mount, completely crashing SvelteKit initialization and freezing the UI on an infinite loading spinner.

**Rule:** `ui.default_models` in `webui.db` MUST always be set to `null` (or a comma-separated string like `"gemini-2.5-flash"`), never a JSON array `'[]'`. `provision_owui.py` enforces this automatically via `sanitize_ui_config()`.

## 5. Multi-User OAuth Provisioning & Auto-Redirect Standard
- **Default User Role (`DEFAULT_USER_ROLE=user`):** Enforced across `docker-compose.webui.yml`, `setup_kern_https.sh`, and `deploy_kern.py` so whitelisted Google OAuth users receive active `user` roles immediately upon first login rather than hanging in `pending`.
- **Auto-Redirect Isolation (`OAUTH_AUTO_REDIRECT=False`):** Enforced to prevent client-side redirect loops and race conditions on mobile/desktop browsers with pre-existing session tokens.
- **SvelteKit `/chat/` Route Patch:** `provision_owui.py` patches `/app/build/_app/immutable/entry/app.WPjxzi0v.js` on startup to ensure subpath `/chat/` requests reroute cleanly to root `/` without 404s.


