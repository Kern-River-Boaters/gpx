---
name: "The Talent Agent"
description: "The Talent Agent skill for OpenCode"
---

# The Talent Agent

> Parent Skill Definition: [The Talent Agent](file:///home/jpino/Obsidian/Notes/_Meta/Skills/The Talent Agent/SKILL.md)

---
name: "The Talent Agent Content & Innovation Drafting Skill"
description: "Governs automated concept triage, obsolescence auditing, idea consolidation, multi-channel drafting, LLM-as-a-Judge critique loops, and hardware-agnostic patent relevance mapping across federated vaults."
---

# ✍️ The Talent Agent Skill & Architectural SOP

## 1. Core Principles
- **Federated Vault Awareness**: Sweeps all federated vaults (`Notes`, `KRB`, `Common`, `Genealogy`, `Cookbook`) for emerging ideas, PRDs, patents, commercialization proposals, and technical drafts.
- **Intelligent Triage & Obsolescence Lifecycle**:
  - Automatically assesses non-processed ideas for obsolescence against active codebase implementations.
  - Detects duplicate/overlapping concepts across vaults and suggests consolidation/merges.
  - Scores commercial viability (TAM, monetization vectors, competitive moat) on a 0.0–10.0 scale.
  - Updates Obsidian YAML frontmatter in place following `obsidian-frontmatter-standard`.
- **100% Full-Text Preservation**: Never truncate source concept notes. Preserves full architectural specifications, patent claims, and RAG context.
- **Frontmatter Sanitization**: Always strip source YAML frontmatter (`strip_frontmatter()`) before rendering post bodies to prevent double YAML blocks.
- **Multi-Persona Venue Contracts**:
  - **LinkedIn Persona**: High-impact narrative hook, 3-4 bulleted takeaways, hashtags, 350-500 words.
  - **Substack Persona**: Deep narrative background, system architecture breakdown, code/schema snippets, 600-1200 words.
  - **Patent Counsel Persona**: Hardware-agnostic functional abstractions, Claims 1/15/25 outlines, multi-embodiment architectures, prior art distinction table.
  - **Market Analyst Persona**: Commercial viability score, TAM ($42.5B), monetization vectors, competitive moat.
  - **YouTube Persona**: High-energy opening hook, timestamped chapters, visual B-roll cues, monologue script.

## 2. LLM-as-a-Judge Critique & Jargon Translation Loop
- All generated drafts MUST pass through `judge_and_refine_draft()`.
- Strips raw human triage badges (`status: pending_review`).
- Translates internal vault codenames (`host kern`, `Aegis`, `Obsidian Bases`, `git-crypt`) into industry-standard terms via `_Meta/Skills/The Talent Agent/style_guide.json`.

## 3. Persistent Caching & Nightly Execution
- Caches triage and synthesis results by content hash in `_Meta/Cache/innovation_triage_cache.json` to prevent unnecessary token consumption.
- Runs nightly on host `kern` at 03:30 AM via `kern-weekly-content-drafting.timer` / `kern-nightly-innovation-agent.timer`.

