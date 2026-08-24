---
name: "kern-reverse-proxy-sso"
description: "kern-reverse-proxy-sso skill for OpenCode"
---

# kern-reverse-proxy-sso

> Parent Skill Definition: [kern-reverse-proxy-sso](file:///home/jpino/Obsidian/Common/_Meta/Skills/kern-reverse-proxy-sso/SKILL.md)

---
name: kern-reverse-proxy-sso
description: "Operational skill for configuring, deploying, auditing, and debugging NGINX HTTPS Reverse Proxy, ForwardAuth SSO gateway (oauth2-proxy), zero-trust loopback isolation (127.0.0.1), and Open WebUI root SPA alignment on kern. Use whenever modifying NGINX, oauth2-proxy, Open WebUI, or service routing."
---

# Kern Reverse-Proxy, SSO & Zero-Trust Isolation Standard

## Operational Context
The `kern` workstation operates multiple microservices protected by a single unified HTTPS reverse proxy and Google OAuth Single Sign-On gateway. All microservices MUST bind exclusively to `127.0.0.1` (loopback) to prevent unauthenticated direct port access over public network interfaces.

---

## 1. Path-Based Reverse Proxy Matrix

| HTTPS Location | Upstream Target | Application | Key Configuration Requirements |
|---|---|---|---|
| `/` | `http://127.0.0.1:3000` | Open WebUI AI Assistant | Root domain application (SvelteKit + FastAPI) |
| `/chat/` | `http://127.0.0.1:3000` | Open WebUI Alias | 301 Redirects to `/` |
| `/obsidian/` | `http://127.0.0.1:8095/` | Kern Obsidian Web Publisher | Vault reader & search dashboard |
| `/ingestion/` | `http://127.0.0.1:8096/` | Kern Ingestion Studio | Audio note & document triage engine |
| `/code/` | `http://127.0.0.1:8080/` | code-server IDE | Web IDE (`auth: none` — protected by SSO) |
| `/grafana/` | `http://127.0.0.1:3001/grafana/` | Grafana Dashboards | `GF_SERVER_SERVE_FROM_SUB_PATH=true` |
| `/git/` | `http://127.0.0.1:3002/` | Gitea Local Mesh Git Platform | Local Git remote, automated GitHub mirror, ForwardAuth SSO |
| `/terminal/` | `http://127.0.0.1:7681/` | ttyd Web SSH Terminal | Terminal daemon (`-i 127.0.0.1`) |
| `/dicom/` | `http://127.0.0.1:8300/` | OHIF DICOM Viewer | Medical imaging viewer |
| `/pacs/` | `http://127.0.0.1:8042/` | Orthanc PACS | DICOM PACS server (loopback only — was `100.107.8.107`, fixed Aug 12) |
| `/podcast/` | `http://127.0.0.1:8090/` | Private Podcast RSS | Audio feed server |
| `/metrics/` | `http://127.0.0.1:9090/metrics/` | Prometheus Metrics | System metrics daemon |
| `/cadvisor/` | `http://127.0.0.1:8081/` | cAdvisor Container Monitor | Container stats (`sub_filter` asset rewriting for root-only upstream) |
| `/bootstrap.sh` | Static `/var/www/html/bootstrap.sh` | Node Bootstrap Harness | Direct shell script serving (Tailscale network layer isolated, no OAuth cookie required) |

### Internal Model Serving Ports (loopback only — NOT proxied through nginx)

| Port | Service | Models / Optimization Config |
|---|---|---|
| `:11434` | Ollama (Docker, `--network host`) | GPU models: qwen2.5:32b, llama3.1:70b, mistral-nemo, nomic-embed-text |
| `:11435` | FastFlowLM (systemd --user) | NPU XDNA2: 35 models (deepseek-r1, gemma4, medgemma, qwen3.6-moe…) |
| `:11436` | llama-server (systemd) | Muse Glimmer 30B GGUF bridge with DFlash speculative decoding (`dflash-kquant.gguf`), `--ctx-size 16384`, `--reasoning-format none` |
| `:3343–3348` | RAG MCP Servers (5 vaults) | Obsidian RAG/SQL: Notes, Common, Cookbook, KRB, Genealogy |
---

## 2. Mandatory Zero-Trust Binding Rules (SYS-SEC-001 / SYS-SEC-002)

1. **Loopback Only:** All microservice ports (`:3001`, `:7681`, `:8300`, `:8042`, `:8095`, `:8096`, `:8080`, `:9090`, `:8090`) MUST bind to `127.0.0.1`.
2. **No Host IP Binds:** Never bind services to `100.107.8.107` or `0.0.0.0`. **CRITICAL**: Because NGINX and Docker configs are dynamically generated, you MUST NOT directly edit `/etc/nginx/sites-available/kern-https` to fix these without ALSO updating `setup_kern_https.sh` and `deploy_kern.py`.
3. **ForwardAuth SSO Scope Isolation:** All subpath nginx `location` blocks (except public oauth callbacks and root Open WebUI) MUST include:
   ```nginx
   auth_request       /oauth2/auth;
   error_page 401     = @error401;
   auth_request_set   $user  $upstream_http_x_auth_request_user;
   auth_request_set   $email $upstream_http_x_auth_request_email;
   proxy_set_header   X-User  $user;
   proxy_set_header   X-Email $email;
   ```
4. **No Global 401 Interception:** NEVER define `error_page 401` at server scope or under `location /`. Open WebUI returns HTTP 401 when unauthenticated; intercepting 401 server-wide forces NGINX to capture Open WebUI's 401 status and redirect users to `oauth2-proxy` / Obsidian.
5. **Strict `Clear-Site-Data` Header Scoping:** NEVER send `Clear-Site-Data: "cache", "storage"` on `location /` or API routes. Wiping browser storage on general responses clears LocalStorage/SessionStorage on every fetch request, evicting the client application's JWT session token and causing an infinite loading IO logo loop. Restrict `Clear-Site-Data` strictly to sign-out routes (`/oauth2/sign_out`) and `@error401` redirects.
6. **OAuth Auto-Redirect Isolation:** Open WebUI must run with `OAUTH_AUTO_REDIRECT=False` to prevent automated redirect collisions and infinite loading loops on devices with valid pre-existing sessions.
7. **Open WebUI Persistent DB Precedence (SYS-INF-011):** Open WebUI's SQLite database (`/app/backend/data/webui.db` in the Docker volume) **permanently overrides** env vars for `model_filter.list`, `openai.api_base_urls`, `ollama.base_urls`, and `webui.url`. Any env-var-only approach will silently revert to stale DB values after container restart. After every `docker run` or `docker restart`, the `deploy_kern.py` step_4_gpu_ollama_webui() DB patch step MUST run to enforce canonical config. Verify with `test_kern_endpoints.py` Suite 8.
8. **PWA Service Worker Isolation & URL Scoping:** Services running under subpaths (e.g. `/obsidian/`) MUST explicitly scope all internal navigation links, wikilinks, browse, view, and search URLs under `/obsidian/` (e.g. `/obsidian/browse/...`, `/obsidian/view/...`) and inject an inline SW unregistration script in `<head>` to prevent the root PWA Service Worker (Open WebUI) from intercepting subpath requests and rendering `404: Not Found`.

---

## 3. TDD Verification Checklist

Whenever modifying configuration or deploying updates:

1. **Security & Endpoint Suite**:
   ```bash
   python3 [[test_kern_endpoints.py]]
   ```
   * Verifies no microservice port is exposed on `100.107.8.107`.
   * Verifies all loopback upstreams return HTTP 200 on `127.0.0.1`.
   * Verifies all NGINX locations enforce 302 SSO redirects and 301 canonical trailing slashes.

2. **Browser Static Asset & Chunk Suite**:
   ```bash
   python3 [[test_browser_assets.py]]
   ```
   * Inspects `index.html` and entry JS bundles to verify all 100+ SvelteKit chunks, static files, and API endpoints load with HTTP 200 OK.

3. **Headless Chrome Log & DOM Trace**:
   ```bash
   node [[capture_console_errors.js]]
   ```
   * Launches Puppeteer headless Chromium to capture JS console errors, unhandled exceptions, and DOM splash screen state.

4. **Open WebUI Database Alignment**:
    ```bash
    docker exec open-webui python3 -c "import sqlite3; conn = sqlite3.connect('/app/backend/data/webui.db'); conn.execute('UPDATE config SET value = \'\"https://kern.tailb08dba.ts.net\"\' WHERE key = \'webui.url\''); conn.commit()"
    ```
    * Ensures Open WebUI's persistent SQLite database matches `https://kern.tailb08dba.ts.net`.

5. **Playwright E2E Browser Validation Suite**:
    ```bash
    python3 [[test_portal_playwright.py]]
    ```
    * Runs headless Chromium E2E tests across all portal routes, following redirects and asserting against actual DOM content and titles to guarantee zero SPA router collisions (preventing Open WebUI 404 / IO logo intercept errors).

---

## 4. Local LLM Performance & Speculative Decoding Guidelines

When serving large local reasoning models (such as Muse Glimmer 30B GGUF) on unified-memory workstations:

1. **Vulkan Memory Bandwidth Decode Ceiling (~4.25 t/s):**
   * The AMD Ryzen AI 9 HX 370 iGPU LPDDR5X memory bandwidth physically limits 30B GGUF matrix math decode throughput. Even with full GPU layer offloading (`--n-gpu-layers 99`), decode speed will natively cap at ~4 t/s.

2. **DFlash Speculative Decoding Acceleration:**
   * Speculative decoding (using the 1.63GB `dflash-kquant.gguf` drafter model) must be enabled via `llama-server` command-line parameters:
     `--model-draft /home/jpino/.local/share/models/dflash-kquant.gguf --spec-type draft-dflash --spec-draft-n-max 15 --spec-draft-n-min 3`
   * This leverages the workstation's faster prompt ingestion (prefill) speed (~75 t/s) to draft blocks of tokens, raising net decode throughput by **50% to 100%** (up to ~6–10 t/s).

3. **Reasoning Stream Alignment for Open WebUI:**
   * **The Problem:** Reasoning models output internal thinking traces into `delta.reasoning_content` in OpenAI compatible SSE streams. Open WebUI expects text in `delta.content`. While the model is thinking, the UI receives zero text and appears completely frozen.
   * **The Standard:** Serve reasoning models with `--reasoning-format none`. This forces the server to output all tokens directly into `delta.content`, allowing token-by-token text to stream immediately to Open WebUI in **< 1.0 second**.

4. **Prompt Ingestion Latency & Context Sizing:**
   * **Prefill Speed:** Prefill speed on Vulkan is ~75 tokens per second. If Open WebUI passes a large context window (e.g. 6,000 tokens of chat history/RAG context), prompt ingestion alone takes **~80 seconds** before the first token of the response can generate.
   * **The Standard:** Always configure a minimum of `--ctx-size 16384` to prevent prompt overflow errors, and encourage starting **New Chat** threads when local inference latency increases (which resets prompt ingestion time to < 2 seconds).


