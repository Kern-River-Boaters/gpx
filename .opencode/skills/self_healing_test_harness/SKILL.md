---
name: "self_healing_test_harness"
description: "self_healing_test_harness skill for OpenCode"
---

# self_healing_test_harness

> Parent Skill Definition: [self_healing_test_harness](file:///home/jpino/Obsidian/Common/_Meta/Skills/self_healing_test_harness/SKILL.md)

---
name: "self_healing_test_harness"
description: "Self-healing E2E Playwright test harness, Ollama local model heartbeat testing, and least-privilege sudoers infrastructure recovery."
---

# Self-Healing Test Harness & Infrastructure Recovery Skill

## Overview
This skill defines the autonomous self-healing pattern for the Kern platform test harness (`test_portal_playwright.py`) and least-privilege sudoers recovery rules (`kern-healing`).

## Core Principles
1. **Zero SPA Collisions:** E2E test suites must verify that static assets (`/_app/`, `/static/`) bypass FastCGI/ForwardAuth `auth_request` wrappers to prevent MIME-type loading failures (`text/html` instead of JavaScript).
2. **Subpath Alignment:** Environment variables (`WEBUI_URL`, `GOOGLE_REDIRECT_URI`) must precisely mirror Nginx root routing paths without extraneous subpaths (e.g., `/chat`), ensuring Google OAuth callbacks resolve correctly.
3. **Automated Auto-Correction:** When route status checks or local model inference heartbeats fail, the test harness automatically executes pre-approved least-privilege recovery commands (`sudo nginx -t && sudo systemctl reload nginx`, `sudo docker restart open-webui`).
4. **Multi-Tool Skill Synchronization:** Run `deploy_agent_skills.py` to distribute canonical `SKILL.md` definitions across `.opencode/`, `.claude/`, and `.cursor/`.

