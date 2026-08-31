# overlook-client-node

> Parent Skill Definition: [overlook-client-node](file:///home/jpino/Obsidian/Common/_Meta/Skills/overlook-client-node/SKILL.md)

---
name: overlook-client-node
description: "Operational skill for provisioning, diagnosing, auditing, and managing the Overlook mobile workstation (Apple MacBook Pro Retina 15-inch Mid 2015 / MacBookPro11,5), Broadcom FaceTime HD PCIe camera (bcwc_pcie), mbpfan thermals, lid close safeguards, amdgpu SI driver assignment, external monitor support, and federated MCP routing to Kern. Use whenever modifying Overlook drivers, power profiles, GPU config, or client configs."
---

# Overlook Mobile Client Node Standard

## Operational Context
`overlook` (Apple MacBook Pro Retina 15-inch Mid 2015, `MacBookPro11,5`) serves as the primary mobile client workstation and note graph hub for the federated Obsidian vault system. All host-level configurations, Apple hardware drivers, and compute mesh integrations are managed as Infrastructure-as-Code via `_Meta/Scripts/deploy_overlook.py` under **[[ADR-032 - Mobile Client Workstation Infrastructure-as-Code, Apple Hardware Driver Orchestration, and Remote Compute Integration (deploy_overlook.py)|SYS-INF-010]]**.

---

## 1. Hardware & Driver Provisioning Reference

| Component | Hardware Identifier | Linux Driver / Daemon | Configuration File / Target | Key Verification Command |
| :--- | :--- | :--- | :--- | :--- |
| **FaceTime HD Webcam** | `14e4:1570` (PCIe) | `facetimehd` (DKMS 0.7.0.1) | `/etc/modules-load.d/facetimehd.conf` | `ls -la /dev/video0 && lsmod \| grep facetimehd` |
| **Primary Bluetooth Controller** | `2357:0604` (TP-Link UB500 / RTL8761BU) | `btusb` / `btrtl` (BT 5.4) | Primary default adapter (`hci1`) for dual BLE peripherals (K860 + SlimBlade Pro) | `bluetoothctl list && bluetoothctl info` |
| **Internal Bluetooth (Fallback)** | `05ac:8290` (Apple Broadcom) | `btusb` / `btbcm` | `/lib/firmware/brcm/BCM-05ac-8290.hcd` (Powered OFF when UB500 active) | `bluetoothctl show AC:BC:32:8F:41:9C` |
| **Firmware Payload** | Broadcom BCM15700A2 | Extracted from OSX | `/usr/lib/firmware/facetimehd/firmware.bin` | `stat /usr/lib/firmware/facetimehd/firmware.bin` |
| **Thermals & Fans** | Dual Fan Assembly | `mbpfan` | `/etc/mbpfan.conf` (`55°C` / `78°C` / `92°C`) | `systemctl status mbpfan.service` |
| **Trackpad** | Apple Multitouch | `libinput` | `/etc/X11/xorg.conf.d/40-touchpad.conf` | `gsettings get org.gnome.desktop.peripherals.touchpad natural-scroll` |
| **Magic Mouse** | Apple Magic Mouse | `hid-magicmouse` (DKMS) | Custom scroll acceleration & 3-finger middle click | `lsmod \| grep magicmouse` |
| **Retina Display** | 2880 × 1800 (16:10) | GNOME HiDPI | `text-scaling-factor 1.25` | `gsettings get org.gnome.desktop.interface text-scaling-factor` |
| **Lid Safeguards** | Haswell + AMD dGPU | `systemd-logind` | `/etc/systemd/logind.conf.d/lid-switch.conf` | `gsettings get org.gnome.settings-daemon.plugins.power lid-close-ac-action` |
| **AMD dGPU Driver Assignment** | Venus XT SI `0x6821` (`01:00.0`) | `amdgpu` (explicit SI) | `/etc/modprobe.d/overlook-gpu.conf` | `cat /sys/module/amdgpu/parameters/si_support` (expect `1`) |
| **External Monitor (HDMI/MiniDP)** | card2-HDMI-A-3 / card2-DP-3,4 | `amdgpu` HPD | Requires `si_support=1` in overlook-gpu.conf | `cat /sys/class/drm/card2/card2-HDMI-A-3/status` |
| **SSD Storage Controller** | Samsung `S4LN058A01 [SSUBX]` (PCI `02:00.0`) | `ahci` / IOMMU Bypass | `/etc/default/grub` (`intel_iommu=off`) | `cat /proc/cmdline \| grep intel_iommu=off` |
| **SSH Server & Compute Mesh** | Inbound SSH from Kern | `openssh-server` | `/etc/ssh/sshd_config`, `~/.ssh/authorized_keys` | `systemctl status ssh && ufw status` |

---

## 2. Mandatory Hardware & Sleep Rules

1. **Prevent Dual-GPU Sleep Lockup:** The Haswell CPU + AMD Radeon R9 M370X dGPU suffers from unrecoverable PCIe VM context loss (`amdgpu_vm_validate failed`) when entering S3 sleep on lid close. Zero-sleep policy MUST be enforced: `HandleLidSwitch=ignore` and `LidSwitchIgnoreInhibited=yes` in `/etc/systemd/logind.conf.d/lid-switch.conf`, GNOME power schemas (`lid-close-*-action='nothing'`), system-wide sleep disable in `/etc/systemd/sleep.conf.d/no-suspend.conf` (`AllowSuspend=no`), and masked systemd targets (`sleep.target`, `suspend.target`, `hibernate.target`, `hybrid-sleep.target`).
2. **DKMS Module Maintenance:** Broadcom FaceTime HD webcam (`facetimehd`) and Magic Mouse drivers MUST be registered under DKMS so that kernel updates automatically recompile the binary modules.
3. **Module Conflict Avoidance:** `bdc_pci` MUST remain blacklisted in `/etc/modprobe.d/facetimehd.conf` to avoid conflicting with `facetimehd`.
4. **Identity & Bi-Directional SSH Mesh:** The primary OS user on Overlook is `pino` (`/home/pino`), whereas on the Kern compute brain it is `jpino` (`/home/jpino`). Overlook runs `openssh-server` (`systemctl enable --now ssh`, UFW allow 22) with Kern's public key (`jpino@keysight.com`) in `~/.ssh/authorized_keys` to enable inbound SSH from Kern. Outbound SSH configurations to Kern map `User jpino` in `~/.ssh/config`.
5. **MacBook Keyboard Shortcuts (Print Screen Mapping):** Because MacBook keyboards lack a physical `PrtScn` key, GNOME media-key bindings route `InteractiveScreenshot` via:
   * `Cmd (⌘) + Shift + 4` / `Cmd + Shift + 3` / `Cmd + Shift + 5` *(macOS muscle memory)*
   * `Cmd (⌘) + Shift + S` *(Windows/Linux snip)*
   * `Ctrl + Shift + S` *(Fallback)*
   * Pinned 1-click **Take a Screenshot** app icon in Ubuntu left dock.
6. **Strict Prohibition on Forced dGPU Powerdown / Module Reloads:** On `MacBookPro11,5` (Mid 2015 dual-GPU), the internal Retina display multiplexer is managed by Apple GMUX (v4.0.20). Attempting to force runtime powerdown (`options radeon runpm=1`, `echo auto > power/control`) or reloading the `radeon` driver live drops the GMUX panel pixel clock, blanks the internal display, and breaks Mutter compositing. The discrete GPU MUST remain under standard kernel defaults with `power/control = on`.
7. **Broadcom Bluetooth Firmware & USB Power Management:** The Apple Bluetooth Host Controller (`05ac:8290` / `BCM20703A1`) requires `BCM-05ac-8290.hcd` (and `.zst`) in `/lib/firmware/brcm/`. **Crucially, native kernel defaults MUST be used for USB power.** Attempting to force USB autosuspend off via `options btusb enable_autosuspend=n` or udev `power/control="on"` causes unrecoverable `SET_CONFIGURATION` timeouts (`BCM: Reset failed (-110)`) during the Broadcom firmware initialization sequence, resulting in a permanent hardware crash requiring an SMC Reset.
8. **Apple Samsung SSUBX SSD IOMMU Bypass (Prevent Read-Only Remounts):** The Apple OEM Samsung PCIe AHCI SSD controller (`02:00.0`) triggers Intel DMAR page table translation faults (`non-zero reserved fields in PTE`) if Intel IOMMU is enabled. `intel_iommu=off` MUST be set in `/etc/default/grub` to prevent ATA host bus errors, link freezes (`ata1.00 frozen`), and ext4 emergency `remount-ro` lockups.
9. **Explicit amdgpu SI Driver Assignment (HDMI / External Monitor):** The AMD Venus XT GPU (device `0x6821`, SI/Southern Islands family) is claimed by both `radeon` and `amdgpu`. Without explicit configuration, `amdgpu` wins the PCI bind but runs with `si_support=-1` (ambiguous default), causing HPD to never fire — HDMI and MiniDP ports report `disconnected` and no EDID is read. `/etc/modprobe.d/overlook-gpu.conf` MUST set `options amdgpu si_support=1 cik_support=0` and `options radeon si_support=0 cik_support=1`, baked into initramfs via `sudo update-initramfs -u`. This is enforced by `deploy_overlook.py --step display_power`. **All external ports (HDMI right-side, Thunderbolt/MiniDP left-side) are physically wired to the AMD card2 — the Intel iGPU has no physical output connectors on this hardware.**
10. **Apple-GMUX Screen & Keyboard Backlight Nativism:** The internal screen backlight (`gmux_backlight`) and keyboard backlight (`smc::kbd_backlight`) are handled perfectly by the modern Linux kernel (`7.x`) and GNOME Wayland out of the box. Do **NOT** apply legacy kernel parameters (e.g., `acpi_backlight=vendor`) or udev input integration hacks. F1/F2 correctly control the screen, and F5/F6 control the keyboard LEDs.
11. **Mandatory SMC Reset for Hardware Freezes:** When recovering from a GPU compositor freeze or Bluetooth controller hang, the NVRAM reset (`Cmd + Opt + P + R`) is generally ineffective. The **SMC Reset** (holding `Shift + Control + Option + Power` for 10 seconds while powered down) is definitively required to flush the Apple GMUX (Graphics Multiplexer) and USB/Bluetooth firmware states.
12. **Electron SUID Sandbox Extraction Bug:** When agents or users manually extract `.tar.gz` archives of Electron applications (like Antigravity IDE), the `chrome-sandbox` executable loses its `root` ownership and `4755` SUID permission, causing the app to instantly abort launch. The agent MUST NOT hallucinate a disk or GPU lockup in this scenario; it MUST run `sudo chown root:root chrome-sandbox && sudo chmod 4755 chrome-sandbox`.
13. **Battery Longevity & Power Telemetry Baseline (`battery_guard.py` / SYS-INF-010):** Overlook operates an iFixit high-capacity battery pack (105.02 Wh, ~108.5% health). The absolute minimal hardware power floor (with AMD dGPU Cape Verde active in `power/control = on`, USB peripherals pulled, and Wi-Fi disabled) is **`18.3313 W`** (~5.73 hours theoretical runtime). Standard development load (Wi-Fi + BT 5.4 LE) draws ~22–28 W (~3.75–4.75 hours). AccuBattery Guardian enforces an 80% charge ceiling (~84 Wh usable, ~4.5 hours light dev) to protect cell chemistry.


---

## 3. Operational Command Matrix (`deploy_overlook.py`)

```bash
# 1. Audit live host configuration drift (Read-only, zero sudo)
python3 _Meta/Scripts/deploy_overlook.py --diff

# 2. Dry-run provisioning (Simulate all operations)
python3 _Meta/Scripts/deploy_overlook.py --dry-run

# 3. Apply full client stack (Requires root)
sudo python3 _Meta/Scripts/deploy_overlook.py

# 4. Rebuild / activate specific hardware subsystem
sudo python3 _Meta/Scripts/deploy_overlook.py --step hardware_storage_grub
sudo python3 _Meta/Scripts/deploy_overlook.py --step hardware_camera
sudo python3 _Meta/Scripts/deploy_overlook.py --step hardware_bluetooth
sudo python3 _Meta/Scripts/deploy_overlook.py --step hardware_thermals_fan
sudo python3 _Meta/Scripts/deploy_overlook.py --step display_power

# 5. Quick Bluetooth restore runner
sudo bash _Meta/Scripts/fix_overlook_bluetooth.sh

# 6. Check partition reclamation geometry for macOS APFS removal
python3 _Meta/Scripts/deploy_overlook.py --partition-check

# 7. Battery Longevity & AccuBattery Guardian controls
python3 _Meta/Scripts/battery_guard.py --status           # View live % & wattage draw
python3 _Meta/Scripts/battery_guard.py --override 100    # Charge to 100% (Travel mode)
python3 _Meta/Scripts/battery_guard.py --reset-override  # Reset target to 80%
python3 _Meta/Scripts/battery_guard.py --snooze 30       # Snooze alerts for 30m

# 8. Rollback host configuration to pre-apply snapshot
sudo python3 _Meta/Scripts/deploy_overlook.py --revert latest
```

---

## 4. Associated Governance & SOPs
* **Architecture Standard:** [[ADR-032 - Mobile Client Workstation Infrastructure-as-Code, Apple Hardware Driver Orchestration, and Remote Compute Integration (deploy_overlook.py)]]
* **Gitea Mesh Architecture:** [[ADR-041 - Gitea Local Mesh Git Platform, ForwardAuth SSO, Decrypted Visual Diffs, and Dual-Mode Asynchronous Cloud Mirroring]]
* **SOP Guide:** [[Overlook Client Configuration.md]]
* **Hardware Inventory:** [[MacBook Pro Retina 2015.md]]
* **Companion Workstation:** [[Kern Workstation Configuration.md]]

---

## 5. Dual-Mode Smart Mesh Synchronization (ADR-041)

When running `sync_vaults` on Overlook:
- **Mesh Mode (Home WiFi / Tailscale)**: Synchronizes with **Kern Gitea** (`https://kern.tailb08dba.ts.net/git/`) at Gigabit speeds, with sub-second push returns and background GitHub cloud mirroring.
- **Cloud Fallback (Traveling / Offline)**: Automatically falls back to **GitHub cloud** if Kern is unreachable.
- **Commands**:
  - `sync_vaults` (Sync default vaults: `Cookbook`, `Notes`, `Common`)
  - `sync_vaults --status` (Check uncommitted/unpushed status)
  - `sync_vaults --diff` (Inspect decrypted plaintext diffs and Gitea web links)


