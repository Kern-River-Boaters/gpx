---
name: "voice-control-npu"
description: "voice-control-npu skill for OpenCode"
---

# voice-control-npu

> Parent Skill Definition: [voice-control-npu](file:///home/jpino/Obsidian/Common/_Meta/Skills/voice-control-npu/SKILL.md)

---
name: voice-control-npu
description: Local NPU-accelerated voice control and dictation skill for VS Code and code-server on the Kern workstation via FastFlowLM.
---

# Voice Control & NPU Transcription Skill

## Overview
This skill provides instructions and validation rules for operating local speech-to-text (ASR) dictation and voice control on the `kern` workstation, leveraging the AMD Ryzen AI XDNA 2 NPU (`FastFlowLM` on port `11435`) at <2W power consumption.

## Key Guidelines
1. **Endpoint Routing:** Always route streaming dictation and ASR requests to `http://localhost:11435/v1` (or Tailscale mesh `http://100.107.8.107:11435/v1`).
2. **Dictation Instructions:** Reference `.github/dictation.md` for project terminology (`pipecleaner`, `FastFlowLM`, `kern`) and Obsidian shortcut syntax (`[[WikiLink]]`, `📅 Date`).
3. **Dual GUI Support:** Ensure microphone capture is active and HTTPS WebSocket headers are correctly proxied when operating via browser-based `code-server` (`https://kern.tailb08dba.ts.net/code/`).
4. **Health Auditing:** Run `python3 _Meta/Scripts/test_voice_control_health.py` before deployments.

