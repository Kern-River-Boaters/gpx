# chezmoi-secret-ops

> Parent Skill Definition: [chezmoi-secret-ops](file:///home/jpino/Obsidian/Common/_Meta/Skills/chezmoi-secret-ops/SKILL.md)

---
name: chezmoi-secret-ops
description: "Operational skill and procedural runbook for managing, auditing, hydrating, and backing up declarative host secrets and dotfiles via Chezmoi, age, and KeePass under SYS-SEC-004."
version: 1.0
trigger: "Trigger whenever managing credentials, rotating API keys, debugging secret permissions, or updating Chezmoi templates."
---

# Chezmoi Secret Operations & Zero-Trust Hydration Skill

This skill governs the declarative management of host secrets, configuration templates, KeePass extraction, and multi-node bootstrap across the **Kern Workstation**, **Overlook MacBook**, and **Android mobile devices** under **SYS-SEC-004 (ADR-038)**.

---

## 1. Architecture & Multi-Node Topology

```
~/.local/share/chezmoi/ (Git Repo: joseluispino/dotfiles-chezmoi)
 ├── dot_bashrc.tmpl
 ├── dot_zshrc.tmpl
 ├── dot_gitconfig.tmpl
 ├── dot_ssh/
 │    └── config.tmpl
 ├── .chezmoiignore.tmpl
 └── dot_config/
      ├── open-webui/
      │    └── encrypted_private_webui.env.age       [Kern only]
      ├── sso/
      │    ├── encrypted_private_oauth2-proxy.env.age [Kern only]
      │    └── authenticated_emails.txt              [Kern only]
      ├── kern-notifications/
      │    └── encrypted_private_notifications.env.age [Kern only]
      └── vertex/
           └── encrypted_private_credentials.json.age [Kern & Overlook]
```

### Node Matrix & Secret Scoping (`.chezmoiignore`)
| Node | Hostname / OS | Dotfiles Applied | Secrets Hydrated |
|---|---|---|---|
| **Kern** | `kern` (Ubuntu Linux x86_64) | `.bashrc`, `.gitconfig`, `~/.ssh/config` | Open WebUI, SSO, Notifications, Vertex AI |
| **Overlook** | `overlook` (macOS / Ubuntu) | `.bashrc`, `.zshrc`, `.gitconfig`, `~/.ssh/config` | Vertex AI (`credentials.json`) |
| **Pixel 8 Pro** | `localhost` (Termux / Debian VM) | `.bashrc`, `.gitconfig`, `~/.ssh/config` | **Zero server secrets** (Blocked by `.chezmoiignore`) |
| **Pixel Tablet**| `localhost` (Termux / Debian VM) | `.bashrc`, `.gitconfig`, `~/.ssh/config` | **Zero server secrets** (Blocked by `.chezmoiignore`) |

---

## 2. Canonical Secret & Key Placements

1. **SSH Private Key**:
   * Master GitHub ed25519 key: `~/.ssh/id_ed25519` (`chmod 0600`).
   * Master public key: `~/.ssh/id_ed25519.pub` (`chmod 0644`).
   * Legacy RSA keys: Archived to `~/.ssh/archive/` (`0700` dir, `0600` files).
2. **Git-Crypt Master Unlock Key**:
   * **Canonical Location**: `~/.config/git-crypt/notes-vault-production.key` (`chmod 0600`).
   * *Never store plaintext key stubs in `~` or `~/Downloads/`.*
3. **Chezmoi Master Decryption Key**:
   * `~/.config/chezmoi/key.txt` (`chmod 0600`).
4. **KeePass Keystore Backup (`Jose Database.kdbx`)**:
   * Master age key (`chezmoi_age_key.txt`) and GCP Vertex key (`vertex_service_account.json`) attached to **`Kern Ubuntu Gmail`**.
   * Master Git-Crypt key (`notes-vault-production.key`) attached to **`Personal Obsidian Git Crypt`** (or `Notes Vault Git-Crypt (PRODUCTION)`).
   * Master GitHub SSH keys (`id_ed25519`, `id_ed25519.pub`) attached to **`SSH Keys github`**.

---

## 3. New Node Bootstrap Runbooks

### Method A: One-Liner via Tailscale Mesh (Recommended)
On any new machine that has joined the Tailscale mesh:
```bash
curl -fsSL https://kern.tailb08dba.ts.net/bootstrap.sh | bash
```

### Method B: Standalone Setup via Common Repo
```bash
# 1. Clone Common
git clone git@github.com:joseluispino/Common.git ~/Obsidian/Common

# 2. Run automated secret extraction from KeePass
python3 ~/Obsidian/Common/_Meta/Scripts/setup_chezmoi_secrets.py

# 3. Clone & unlock all 5 Obsidian vaults
bash ~/Obsidian/Common/_Meta/Scripts/setup_obsidian.sh
```

---

## 4. Android 17 Linux Terminal (Debian VM) Setup

When switching SSH and agent workloads from Termux to the native Android 17 Linux Terminal:
```bash
# 1. In Termux: Stop Termux SSH
pkill sshd

# 2. In Android 17 Linux Terminal app:
sudo apt update && sudo apt install -y openssh-server
mkdir -p ~/.ssh && chmod 700 ~/.ssh
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIA14L7tB7BW6/WP1n7gJiJVgpW4peUgE/PkNqy/9Tj9D joseluispino@gmail.com" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
sudo service ssh start
```

---

## 5. Strict Security Guardrails (Non-Negotiable)

1. **Zero Plaintext in Git Working Trees**: Never commit `.env` or credential files into Obsidian git repos.
2. **Strict File Permissions**: All hydrated secret files must possess `0600` permissions (`-rw-------`).
3. **IaC Synchronization**: Never modify host configuration in `/etc/` or `~/.config/` without simultaneously updating `setup_kern_https.sh`, `deploy_kern.py`, and `dotfiles-chezmoi`.
4. **Zero Blast-Radius Client Isolation**: Mobile and client nodes must never receive server secrets (Open WebUI database credentials, SSO secrets, notification webhooks).


