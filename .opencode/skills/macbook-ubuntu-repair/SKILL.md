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
- **Cause**: The Linux kernel's block cache retains stale partition boundaries.
- **Fix**: Do **not** assume hardware failure. Forcefully unmount the partition, run `fsck.ext4 -y -f` to stitch inodes, and carefully remount. The kernel will read the correct boundaries.

### 3. Bypassing Live USB Firewalls (Localtunnel)
Debian-based Live USBs (like GParted) employ strict TCP wrappers (`hosts.deny`) or missing SSH keys that reject incoming SSH connections (`Connection reset by peer`).
- **Fix**: Instead of fighting SSH, start a local HTTP server on the agent's host workstation and expose it using `localtunnel` (`npx -y localtunnel --port <PORT>`). Have the user run `wget -qO- https://<localtunnel-url>/script.sh | sudo bash` on the laptop to seamlessly stream and execute agentic recovery scripts.

## Scripts
Reference the `.sh` scripts in the `scripts/` directory for ready-to-use recovery payloads.

