---
name: "mobile-termux-node"
description: "mobile-termux-node skill for OpenCode"
---

# mobile-termux-node

> Parent Skill Definition: [mobile-termux-node](file:///home/jpino/Obsidian/Common/_Meta/Skills/mobile-termux-node/SKILL.md)

---
name: mobile-termux-node
description: Operational skill for connecting to, diagnosing, synchronizing, and auditing the Android mobile workstation (Google Pixel 8 Pro running Termux on port 8022). Enforces passwordless Tailscale SSH, Android FUSE filemode safeguards, mobile Obsidian Properties integrity, and gesture handling standards.
---

# Skill: Mobile Termux Workstation Operations

## Overview
This skill governs remote management, zero-friction synchronization, and troubleshooting for the mobile workstation (`joss-pixel-8-pro`) over Tailscale SSH into Termux on port `8022`.

## Core Invariants & Rules

1. **Authentication & Remote Execution**:
   - Device: Google Pixel 8 Pro (`joss-pixel-8-pro`)
   - Address: `100.107.175.38` (Port `8022`)
   - Authenticate via `ssh -p 8022 -o StrictHostKeyChecking=no 100.107.175.38 "<command>"` using Kern's authorized ed25519 key.

2. **Android FUSE Storage Safeguards**:
   - Vault Path: `/sdcard/Documents/Obsidian/{Common,Notes,Cookbook,KRB,Genealogy}`
   - Before executing git status/pull operations, idempotently ensure:
     ```bash
     git config core.filemode false
     ```
   - Never force-kill storage writes; Android FUSE sync operations for large repositories (13,000+ files) require patience.

3. **Mobile Obsidian Standards**:
   - Frontmatter properties must strictly follow ADR-022 (quoted wikilinks, no unquoted markdown links).
   - Maps must use `gestureHandling: true` to prevent touch-trapping on mobile.
   - Base tables must use `formula.log_date` to prevent accidental Daily Note generation on tap.

