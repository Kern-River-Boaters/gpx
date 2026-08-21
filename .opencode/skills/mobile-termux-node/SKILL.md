---
name: "mobile-termux-node"
description: "mobile-termux-node skill for OpenCode"
---

# mobile-termux-node

> Parent Skill Definition: [mobile-termux-node](file:///home/jpino/Obsidian/Common/_Meta/Skills/mobile-termux-node/SKILL.md)

---
name: mobile-termux-node
description: Operational skill for connecting to, diagnosing, synchronizing, and auditing the Android mobile workstation (Google Pixel 8 Pro and Pixel Tablet running native Debian VM on port 22 or Termux on port 8022). Enforces passwordless Tailscale SSH, virtio-fs and Android FUSE filemode safeguards, mobile Obsidian Properties integrity, and gesture handling standards.
---

# Skill: Mobile Android Workstation Operations (Debian VM & Termux)

## Overview
This skill governs remote management, synchronization, and troubleshooting for Android mobile workstations (**Google Pixel 8 Pro** and **Google Pixel Tablet**) across two complementary execution tiers:
1. **Tier 1 (Primary Compute & Agents): Native Android 17 Linux Terminal (Debian VM via AVF/crosvm)**
2. **Tier 2 (OS Integrations & Quick CLI): Termux Userland Environment**

---

## 1. Multi-Tier Android Architecture Matrix

| Capability | Tier 1: Android 17 Linux Terminal (Debian VM) | Tier 2: Termux Environment |
|---|---|---|
| **Underlying Tech** | Real KVM / AVF Virtual Machine (`crosvm`) | Android Application Userland (Bionic libc) |
| **Linux Distro** | Debian GNU/Linux 13 (trixie) aarch64 | Termux rolling packages (`pkg`) |
| **Kernel** | Real Linux 6.12 guest kernel | Android host kernel |
| **SSH Port** | **Port 22** (`droid@<tailscale-ip>`) | **Port 8022** (`<user>@<tailscale-ip>`) |
| **Storage Engine** | **virtio-fs** (`/mnt/shared/Documents/Obsidian/`) | **Android FUSE** (`/sdcard/Documents/Obsidian/`) |
| **Private Keys & Dotfiles**| True ext4 (`/home/droid/` supports `0600`) | Userland private dir (`/data/data/com.termux/`) |
| **KeePass Path** | `/mnt/shared/Autosync/Keepass/Jose Database.kdbx` | `/sdcard/Autosync/Keepass/Jose Database.kdbx` |
| **Process Stability** | **High** (Protected by Android Virtualization Service) | Medium (Subject to Android background killer) |
| **Android OS Hooks** | None (Isolated VM container) | Full (`termux-api`: notifications, battery, clipboard) |

---

## 2. Storage & FUSE vs virtio-fs Reliability Standard

### Is virtio-fs (Debian VM) More Reliable than Termux FUSE?
* **Yes, significantly.**
  * **No False Git Modifications**: virtio-fs handles POSIX timestamp and inode transitions cleanly.
  * **True Linux POSIX Permissions**: `~/.ssh/` and `~/.config/` reside on the VM's native virtual ext4 disk, allowing strict `chmod 0600` without Android FUSE permission stripping.
  * **Memory Isolation**: Large Git decrypt operations (e.g. 16,000 files in `Genealogy`) run in dedicated VM memory without triggering Android MediaProvider crashes.

### Canonical Vault Storage Invariant (Zero Disk Waste)
Both runtimes MUST target the **exact same physical storage**:
* **Physical Location**: `/sdcard/Documents/Obsidian/{Common,Notes,Cookbook,KRB,Genealogy}`
* **Debian VM Symlink**: `/home/droid/Obsidian` $\longrightarrow$ `/mnt/shared/Documents/Obsidian`
* **Termux Path**: `/sdcard/Documents/Obsidian` (or `~/storage/shared/Documents/Obsidian`)

---

## 3. Remote SSH Commands & Authentication

### A. Debian VM (Port 22)
```bash
# Connect to Tablet Debian VM
ssh -i ~/.ssh/id_ed25519 droid@100.113.126.115 "<command>"

# Run sync inside VM
ssh -i ~/.ssh/id_ed25519 droid@100.113.126.115 "cd ~/Obsidian/Common && git pull"
```

### B. Termux (Port 8022)
```bash
# Connect to Phone Termux
ssh -p 8022 -i ~/.ssh/id_ed25519 100.107.175.38 "<command>"

# Connect to Tablet Termux
ssh -p 8022 -i ~/.ssh/id_ed25519 100.120.222.84 "<command>"
```

---

## 4. Mobile Obsidian Standards (ADR-022)

1. **Frontmatter**: Quoted wikilinks, strict YAML quoting, no unquoted markdown links.
2. **Maps & Leaflet**: `gestureHandling: true` to prevent touch-trapping on mobile touchscreens.
3. **Core Base Tables**: `formula.log_date` mapping to prevent accidental Daily Note note creation on mobile taps.


