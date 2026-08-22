---
name: "moab-windows-node"
description: "moab-windows-node skill for OpenCode"
---

# moab-windows-node

> Parent Skill Definition: [moab-windows-node](file:///home/jpino/Obsidian/Common/_Meta/Skills/moab-windows-node/SKILL.md)

---
name: moab-windows-node
description: "Operational skill for provisioning, diagnosing, auditing, and managing the Moab Windows development workstation (Windows 11 Pro 24H2), Windows OpenSSH Server daemon (sshd), ACL hardening, Chezmoi dotfiles deployment, Tailscale mesh routing, and Git Bash /c/Obsidian path normalization. Use whenever modifying Windows host services, SSH mesh routing, or Windows-specific tool configurations."
---

# Moab Windows Workstation Node Standard

## Operational Context
`moab` (Windows 11 Pro 24H2, `100.77.112.7` / `moab.tailb08dba.ts.net`) serves as the primary desktop development workstation, high-throughput terminal node, and federated Obsidian vault storage hub. All host configuration, OpenSSH server automation, and declarative dotfiles are governed by **[[ADR-039 - Windows Workstation Client Node Architecture, OpenSSH Inbound Automation, and Cross-Platform Chezmoi Mesh Standard|SYS-INF-014]]** and **[[Windows Workstation Configuration]]**.

---

## 1. System & Service Architecture Reference

| Component | Target / Path | Service / Tool | Verification Command | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **OpenSSH Server** | `C:\ProgramData\ssh\` | `sshd` Windows Service | `Get-Service sshd` | Startup set to `Automatic` |
| **Inbound Firewall** | TCP Port 22 | Windows Defender Firewall | `Get-NetFirewallRule -Name "OpenSSH-Server-In-TCP"` | Direction: Inbound, Action: Allow |
| **User Authorized Keys** | `C:\Users\Jose\.ssh\authorized_keys` | File ACL (`0600`) | `Get-Acl C:\Users\Jose\.ssh\authorized_keys` | SYSTEM, Administrators, Jose FullControl |
| **Admin Authorized Keys** | `C:\ProgramData\ssh\administrators_authorized_keys` | File ACL | `Get-Acl C:\ProgramData\ssh\administrators_authorized_keys` | Mandatory for `BUILTIN\Administrators` |
| **Dotfiles Repository** | `C:\Users\Jose\.local\share\chezmoi` | `chezmoi` (v2.72.0+) | `chezmoi status && chezmoi diff` | Git: `joseluispino/dotfiles-chezmoi.git` |
| **SSH Client Config** | `C:\Users\Jose\.ssh\config` | OpenSSH Client | `ssh kern "hostname && whoami"` | Templated via `dot_ssh/config.tmpl` |
| **Vault Storage Root** | `C:\Obsidian\` (`/c/Obsidian`) | Local NVMe | `Get-ChildItem C:\Obsidian` | Multi-layer LF line ending enforcement |

---

## 2. Operational Rules & Guardrails

1. **Dual-Key Mirroring for Windows Administrators:** Because user `Jose` is a member of `BUILTIN\Administrators`, Windows OpenSSH Server bypasses `%USERPROFILE%\.ssh\authorized_keys` by default and enforces `C:\ProgramData\ssh\administrators_authorized_keys`. Whenever keys are updated or rotated, both files MUST be synchronized and secured with strict ACLs (`NT AUTHORITY\SYSTEM:(F)` and `BUILTIN\Administrators:(F)`).
2. **Self-Elevating Execution:** Windows service modifications (`Start-Service sshd`, `Set-Service`) require Administrator privileges. Automated scripts MUST implement self-elevation (`setup_windows_sshd.ps1`) using `Start-Process powershell.exe -Verb RunAs` to prevent silent access denied failures.
3. **Dynamic Path Detection in Shell Configs:** `dot_bashrc.tmpl` MUST NEVER evaluate `.chezmoi.username` literally on Windows, as it resolves to domain-prefixed strings (e.g. `MOAB\Jose`). Path resolution MUST check `/c/Obsidian` and `$HOME/Obsidian` dynamically.
4. **Git Safe Directory Enforcement:** `dot_gitconfig.tmpl` MUST inject `[safe] directory = *` on Windows to prevent dubious ownership fatal errors when switching between native PowerShell, Git Bash, and WSL.
5. **CRLF vs LF Line Ending Hygiene:** All git repositories on Windows MUST enforce LF line endings (`git config --global core.autocrlf false` and `git config --global core.eol lf`) to protect Git-Crypt transport encryption.

---

## 3. Operational Command Matrix

```powershell
# 1. Verify and start OpenSSH Server (Self-Elevating)
& "C:\Obsidian\Common\_Meta\Scripts\setup_windows_sshd.ps1"

# 2. Check OpenSSH service status
Get-Service sshd

# 3. Test outbound SSH to Kern
ssh kern "hostname && whoami"

# 4. Test inbound SSH from Kern to Moab
ssh kern "ssh moab 'hostname && whoami'"

# 5. Audit Chezmoi state and template drift
chezmoi status
chezmoi diff

# 6. Pull and apply latest dotfiles
chezmoi update
```

