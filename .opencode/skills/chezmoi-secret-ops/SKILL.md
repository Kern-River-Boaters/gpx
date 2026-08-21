---
name: "chezmoi-secret-ops"
description: "chezmoi-secret-ops skill for OpenCode"
---

# chezmoi-secret-ops

> Parent Skill Definition: [chezmoi-secret-ops](file:///home/jpino/Obsidian/Common/_Meta/Skills/chezmoi-secret-ops/SKILL.md)

---
name: chezmoi-secret-ops
description: "Operational skill and procedural runbook for managing, auditing, hydrating, and backing up declarative host secrets and dotfiles via Chezmoi, age, and KeePass under SYS-SEC-004."
version: 1.0
trigger: "Trigger whenever managing credentials, rotating API keys, debugging secret permissions, or updating Chezmoi templates."
---

# Chezmoi Secret Operations & Zero-Trust Hydration Skill

This skill governs the declarative management of host secrets, configuration templates, and KeePass backups across the **Kern Workstation** and federated compute nodes under **SYS-SEC-004 (ADR-038)**.

---

## 1. Architecture & Single Source of Truth

```
~/.local/share/chezmoi/ (Git Repo)
 ├── dot_config/
 │    ├── open-webui/
 │    │    └── encrypted_private_webui.env.age
 │    ├── sso/
 │    │    ├── encrypted_private_oauth2-proxy.env.age
 │    │    └── authenticated_emails.txt
 │    ├── kern-notifications/
 │    │    └── encrypted_private_notifications.env.age
 │    └── vertex/
 │         └── encrypted_private_credentials.json.age
```

* **Master age Key**: `~/.config/chezmoi/key.txt` (`chmod 0600`).
* **KeePass Backup**: Master `age` key and `vertex_service_account.json` are attached to entry **`Kern Ubuntu Gmail`** in `Jose Database.kdbx`.
* **Host Hydration Targets**:
  * `~/.config/open-webui/webui.env` (`0600`)
  * `~/.config/sso/oauth2-proxy.env` (`0600`)
  * `~/.config/kern-notifications/notifications.env` (`0600`)
  * `~/.config/vertex/credentials.json` (`0600`)

---

## 2. Common Operational Commands

### A. Idempotent Hydration & Verification (Hands-Free)
```bash
# Verify and apply existing encrypted state idempotently
python3 _Meta/Scripts/setup_chezmoi_secrets.py
```

### B. KeePass Extraction & Key Refresh (Interactive)
```bash
# Prompt for KeePass master password, extract/attach secrets, and regenerate templates
python3 _Meta/Scripts/setup_chezmoi_secrets.py --keepass
```

### C. Manual Chezmoi Diff & Status
```bash
# Inspect uncommitted changes or template drift
chezmoi diff
chezmoi status
```

### D. Verify Host Endpoint Health
```bash
# Run the 12-suite zero-trust and secret permission audit
python3 _Meta/Scripts/test_kern_endpoints.py
```

---

## 3. Strict Security Guardrails (Non-Negotiable)

1. **Zero Plaintext in Git Working Trees**: Never commit `.env` or credential files into Obsidian git repos.
2. **Strict File Permissions**: All hydrated secret files must possess `0600` permissions (`-rw-------`).
3. **IaC Docker Compose Flags**: Always invoke Docker Compose with `--env-file ~/.config/open-webui/webui.env` to prevent credential exposure in `ps aux` process tables.
4. **Zero Blast-Radius Machine Identity**: Use `kernworkstation@gmail.com` for machine operations and keep personal accounts strictly as authorized end-user subjects in `authenticated_emails.txt`.

