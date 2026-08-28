# script-execution-harness

> Parent Skill Definition: [script-execution-harness](file:///home/jpino/Obsidian/Common/_Meta/Skills/script-execution-harness/SKILL.md)

---
name: script-execution-harness
description: "Standard operational skill for discovering, dry-running, auditing, and executing vault scripts in _Meta/Scripts/ under SYS-AGN-006."
doc_type: skill
tags:
  - type/skill
  - topic/scripts
  - topic/governance
governing_adr: "[[SYS-AGN-006]]"
---

# Script Execution Harness Skill

This skill provides standardized directives for AI interactive environments (**Google Antigravity**, **GitHub Copilot**, **Claude Code**, **Cursor**, **OpenCode**) to inspect, dry-run, and execute operational scripts across federated vaults (`Common`, `Genealogy`, `Notes`, `Cookbook`, `KRB`).

---

## 📜 Master Script Registry & Governance

All operational scripts are cataloged in **[[SCRIPTS-INDEX.md]]** and governed by **[[SYS-AGN-006]]**.

### Core Script Execution Rules

1. **Always Check Available Flags**: Run `python3 <script_path> --help` to inspect CLI arguments before calling any script.
2. **Safety & Dry-Run First**: If a script supports `--dry-run` or `--check-freshness`, run it in dry-run mode first to preview potential changes.
3. **Environment Dynamic Paths**: Scripts calculate `OBSIDIAN_ROOT` dynamically from environment variables or relative parent directories. Never pass hardcoded system paths.
4. **Structured Error Handling**: Monitor return codes. Successful runs return exit code `0`; non-zero exit codes signal a failure that must be inspected via logs.

---

## 🛠️ Frequently Used Operational Commands

* **Multi-Tool Skill Adapter Deployment**:
  ```bash
  python3 Common/_Meta/Scripts/deploy_agent_skills.py
  ```
* **Federated ADR & Agent Verification Audit**:
  ```bash
  python3 Common/_Meta/Scripts/verify_adr_index.py
  ```
* **Local Git Cache Upstream Synchronization**:
  ```bash
  python3 Common/_Meta/Scripts/sync_git_cache_upstream.py
  ```

