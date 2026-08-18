---
name: "macbook-ubuntu-repair"
description: "macbook-ubuntu-repair skill for OpenCode"
---

# macbook-ubuntu-repair

> Parent Skill Definition: [macbook-ubuntu-repair](file:///home/jpino/Obsidian/Common/_Meta/Skills/macbook-ubuntu-repair/SKILL.md)

---
name: macbook-ubuntu-repair
description: Operational skill for repairing Mid-2015 Retina MacBook Pro Ubuntu EFI bootloaders, mitigating dual-graphics handover crashes, resolving false ext4 I/O errors after partition resizing, and bypassing Live USB firewall blocks using localtunnel.
---

# MacBook Pro Ubuntu Repair Skill

## Context
When maintaining Ubuntu on older dual-GPU MacBooks (like the Mid-2015 Retina), agents will encounter several hardware-specific constraints that cause standard Linux recovery techniques to fail. Use this skill when troubleshooting black screens on boot, EFI/GRUB issues, or missing bootloaders on Macs.

## Key Architectures & Solutions

### 1. NVRAM Wipe & EFI Fallback Bug
When a user performs an NVRAM reset (`Command + Option + P + R`), the Mac deletes all custom OS boot entries.
- **Symptom**: The Mac boot picker only shows a generic "EFI Boot" icon. Clicking it causes an instant black screen without showing the GRUB menu.
- **Cause**: The Mac firmware strictly powers down the Intel Iris GPU and leaves the AMD GPU uninitialized when loading from the generic fallback path (`/EFI/BOOT/BOOTX64.EFI`). GRUB crashes trying to output text.
- **Fix**: 
  1. Boot from a FAT32 GPT Live USB (Macs ignore `isohybrid` `dd` images).
  2. Modify `/etc/default/grub` in a `chroot` to include `GRUB_TERMINAL=console` and `nomodeset`.
  3. Run `grub-install --removable` to explicitly populate the Mac fallback path.
  4. **CRITICAL**: Mount `efivars` and explicitly inject the OS into the NVRAM using `efibootmgr -c -d /dev/sda -p 1 -L "Ubuntu" -l '\EFI\ubuntu\grubx64.efi'`.

### 2. Ext4 Block Cache Desync (False I/O Errors)
If a user uses GParted to move the left edge of an `ext4` partition, they are physically shifting the filesystem data. 
- **Symptom**: Running `grub-install` throws `input/output error` when copying files, making it appear as though the SSD is failing.
- **Symptom**: Antigravity IDE and Electron apps freeze or show a white screen on boot.
- **Root Cause**: The Apple OEM Samsung SSUBX PCIe AHCI SSD triggers Intel DMAR page table translation faults on Linux if Intel IOMMU is enabled. This causes `ata1.00 frozen` link errors and emergency ext4 `remount-ro` lockups. Furthermore, leaving `nomodeset` active disables the GPU drivers needed for Wayland/Electron.
- **Fix (Already integrated in `fix_final.sh`)**: Ensure `intel_iommu=off` is safely appended to `GRUB_CMDLINE_LINUX_DEFAULT`, and explicitly remove `nomodeset` from the configuration to restore hardware acceleration.

### 3. Bypassing Live USB Firewalls (Localtunnel)
Debian-based Live USBs (like GParted) employ strict TCP wrappers (`hosts.deny`) or missing SSH keys that reject incoming SSH connections (`Connection reset by peer`).
- **Fix**: Instead of fighting SSH, start a local HTTP server on the agent's host workstation and expose it using `localtunnel` (`npx -y localtunnel --port <PORT>`). Have the user run `wget -qO- https://<localtunnel-url>/script.sh | sudo bash` on the laptop to seamlessly stream and execute agentic recovery scripts.

## Scripts
Reference the `.sh` scripts in the `scripts/` directory for ready-to-use recovery payloads.

