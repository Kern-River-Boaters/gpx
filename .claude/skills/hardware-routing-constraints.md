# hardware-routing-constraints

> Parent Skill Definition: [hardware-routing-constraints](file:///home/jpino/Obsidian/Common/_Meta/Skills/hardware-routing-constraints/SKILL.md)

---
name: hardware_routing_constraints
description: "Baseline constraints for dynamic model routing across the dual-runtime topology on the Kern workstation."
version: 1.0
trigger: "Evaluated before every model API call when dynamic routing is enabled."
---

# Hardware Routing Constraints
 
You are operating on the `kern` workstation node, which features a tri-tier runtime topology: **Google Cloud Vertex AI (`[Cloud]`)**, **Local Radeon 890M iGPU (`[GPU]`)**, and **Local Ryzen AI XDNA 2 NPU (`[NPU]`)**. You must strictly adhere to the following hardware constraints.

## The Rule of Delegation
Before executing any tool, subagent, or prompt, evaluate computational complexity and select the appropriate backend.

### 1. The Cloud Frontier Tier (`[Cloud]`)
* **Target:** Google Cloud Vertex AI via Service Account (`gemini-2.5-flash`, `gemini-2.5-pro`).
* **Criteria:** Large codebase planning, massive document synthesis (1M+ context window), cross-vault lineage resolution, or when local GPU is busy.
* **Billing:** Powered by the dedicated $300 Google Cloud credit on `project-bdf647f6-7b79-4a34-bfb`.

### 2. The GPU Tier (`[GPU]` — Heavy-Duty & SOTA Local)
* **Target:** `llama-server` (`muse-glimmer` on Port 11436) and Ollama (`qwen2.5-coder:32b`, `llama3.1:70b` on Port 11434).
* **Criteria:** Private offline reasoning, complex file modifications, code building, and local 65k context orchestration.
* **Constraint:** Utilizes 96GB unified memory pool (~25W - 50W). Run sequentially to prevent memory bandwidth saturation.

### 3. The NPU Tier (`[NPU]` — Efficiency)
* **Target:** FastFlowLM on the XDNA 2 NPU (Port 11435).
* **Criteria:** Background triage, rapid parsing, Whisper V3 audio transcription, and lightweight chat.
* **Constraint:** Ultra-low power profile (< 2W). Maximum context limit: 16,384 tokens.

## Learning Loop Feedback
If a task routed to the NPU Tier times out or fails context constraints (> 16k), automatically elevate to the GPU or Cloud Frontier Tier and record the telemetry in post-task reviews.

