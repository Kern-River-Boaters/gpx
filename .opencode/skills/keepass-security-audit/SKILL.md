---
name: "keepass-security-audit"
description: "keepass-security-audit skill for OpenCode"
---

# keepass-security-audit

> Parent Skill Definition: [keepass-security-audit](file:///home/jpino/Obsidian/Common/_Meta/Skills/keepass-security-audit/SKILL.md)

---
name: keepass-security-audit
description: "Operational skill for executing, dry-running, auditing, and remediating KeePass (.kdbx) password databases and 2FA coverage across federated Obsidian vaults under SYS-AGN-006 and ADR-036 Level 4 Maturity."
doc_type: skill
tags:
  - type/skill
  - topic/security
  - topic/keepass
  - topic/2fa
governing_adr: "[[SYS-AGN-006]]"
---

# KeePass & 2FA Security Audit Pipeline Skill

This skill guides AI interactive environments (**Google Antigravity**, **Claude Code**, **GitHub Copilot**, **Cursor**, **OpenCode**) through inspecting, executing, and supervising the **KeePass & 2FA Security Audit Pipeline** and **Supervised Remediation Assist** across federated vaults.

---

## 📜 Architectural Overview & Governance

The pipeline is cataloged in **[[SCRIPTS-INDEX.md]]** and governed by **[[SYS-AGN-006]]** and **[[ADR-036]]** (Level 4 Autonomous Maturity):
1. **Phase 1 (Deterministic Extraction)**: Uses `pykeepass` to extract credentials, computes password ages (`now - entry.mtime`), tallies username reuse frequency, matches domains against the `2fa.directory` v3 API, and masks sensitive secrets before touching AI models.
2. **Phase 2 (Semantic Clustering)**: Uses **Gemini 3.7 Flash** (via `google-genai` and `~/.config/open-webui/gemini_api_key`) or local **Ollama** GPU inference to categorize sanitized domains into 11 standard industry buckets with Pydantic structured output.
3. **Phase 3 (Obsidian Re-hydration)**: Generates markdown checklist sections (`Audit_Part_XX.md`), an **Obsidian Core Base (`00_KeePass_Security_Audit.base`)** view, and appends run telemetry to `Common/_Meta/Telemetry/KeePass_Audit_Ledger.jsonl`.
4. **Phase 4 (Supervised Playwright Assist)**: Launches visible browser sessions, navigates to target services, pre-fills credentials, and pauses for human verification and 2FA configuration.

---

## 🛠️ CLI Execution Commands

### 1. Master Security Audit Pipeline

* **Standard Execution (Gemini 3.7 Flash)**:
  ```bash
  python3 Common/_Meta/Scripts/keepass_audit_pipeline.py --kdbx /path/to/database.kdbx
  ```

* **Dry-Run Mode (Extraction & Categorization Preview)**:
  ```bash
  python3 Common/_Meta/Scripts/keepass_audit_pipeline.py --kdbx /path/to/database.kdbx --dry-run
  ```

* **Air-Gapped / Offline Local GPU Execution (Ollama)**:
  ```bash
  python3 Common/_Meta/Scripts/keepass_audit_pipeline.py --kdbx /path/to/database.kdbx --provider ollama --model qwen2.5-coder:32b
  ```

* **Custom Output Directory & Refresh 2FA Cache**:
  ```bash
  python3 Common/_Meta/Scripts/keepass_audit_pipeline.py --kdbx /path/to/database.kdbx --output-dir Notes/Estate/Technology/KeePass_Audit --refresh-cache
  ```

---

### 2. Supervised Playwright Remediation Assist

* **Launch Remediation for Top 50 Duplicate / Missing 2FA Accounts**:
  ```bash
  python3 Common/_Meta/Scripts/keepass_remediation_assist.py --kdbx /path/to/database.kdbx --limit 50
  ```

* **Dry-Run Remediation Sequence**:
  ```bash
  python3 Common/_Meta/Scripts/keepass_remediation_assist.py --kdbx /path/to/database.kdbx --dry-run
  ```

* **Resume Previous Remediation Session**:
  ```bash
  python3 Common/_Meta/Scripts/keepass_remediation_assist.py --kdbx /path/to/database.kdbx --resume
  ```

---

## 🛡️ Operational Safeguards & Level 4 Constraints

1. **Zero Credential Exposure**: Passwords, OTP secrets, usernames, and notes are never passed to LLMs. Only sanitized `[UUID, Domain/Title]` pairs are passed to classification engines.
2. **Read-Only Database Access**: `.kdbx` files are opened in strict read-only mode.
3. **Core Base Standard (No Dataview)**: All views use official Obsidian Core Base syntax with string expression filters and summary aggregations.

