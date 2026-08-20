# hardware-routing-constraints

> Parent Skill Definition: [hardware-routing-constraints](file:///home/jpino/Obsidian/Common/_Meta/Skills/hardware-routing-constraints/SKILL.md)

---
name: hardware_routing_constraints
description: "Baseline constraints for dynamic model routing across the dual-runtime topology on the Kern workstation."
version: 1.0
trigger: "Evaluated before every model API call when dynamic routing is enabled."
---

# Hardware Routing Constraints

You are operating on the `kern` workstation node, which features a highly asymmetric dual-runtime topology. You have the authority to dynamically route tasks, but you MUST strictly adhere to the following hardware constraints to prevent system crashes and power spikes.

## The Rule of Delegation
Before executing any tool, subagent, or prompt, you must evaluate the computational complexity of the task and select the appropriate backend port.

### 1. The NPU Tier (Efficiency)
*   **Target:** FastFlowLM on the XDNA 2 NPU (Port 11435).
*   **Criteria:** The task involves simple text formatting, basic data extraction, reading RSS feeds, or lightweight chat.
*   **Constraint:** You must route these tasks to the FastFlowLM NPU port. This ensures the node maintains its < 2W ultra-low power profile for background triage.

### 2. The GPU Tier (Heavy-Duty)
*   **Target:** Ollama on the Radeon 890M iGPU (Port 11434).
*   **Criteria:** The task involves deep logic reasoning, complex system architecture drafting, writing code in Python or Rust, or extensive multi-vault RAG extraction.
*   **Constraint:** You must route these tasks to the Ollama GPU port. This allows the task to utilize the 96GB unified memory pool and up to 50W of power.

## Learning Loop Feedback
If a task routed to the NPU Tier fails, times out, or produces malformed JSON, you must log the failure. You will automatically route the retry to the GPU Tier and record this edge case in your post-task review to refine your future routing decisions.

