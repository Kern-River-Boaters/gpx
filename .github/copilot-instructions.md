# GitHub Copilot Instructions — Federated Obsidian Vault

This workspace follows the governance standards defined in the Master ADR Index:
👉 **[Master ADR Index](file:///home/jpino/Obsidian/Common/_Meta/ADR/ADR-INDEX.md)**

## Active Agent Skills
- **The Talent Agent** (Notes): [The Talent Agent](file:///home/jpino/Obsidian/Notes/_Meta/Skills/The Talent Agent/SKILL.md)
- **gedcom-export-standard** (Genealogy): [gedcom-export-standard](file:///home/jpino/Obsidian/Genealogy/obsidian-gramps-provenance-sync/skills/gedcom-export-standard/SKILL.md)
- **genealogical-biography-synthesizer** (Genealogy): [genealogical-biography-synthesizer](file:///home/jpino/Obsidian/Genealogy/_Meta/Skills/genealogical-biography-synthesizer/SKILL.md)
- **genealogy-entity-reconciliation** (Genealogy): [genealogy-entity-reconciliation](file:///home/jpino/Obsidian/Genealogy/_Meta/Skills/genealogy-entity-reconciliation/SKILL.md)
- **genealogy-gramps-exporter** (Genealogy): [genealogy-gramps-exporter](file:///home/jpino/Obsidian/Genealogy/_Meta/Skills/genealogy-gramps-exporter/SKILL.md)
- **genealogy-source-ingestion** (Genealogy): [genealogy-source-ingestion](file:///home/jpino/Obsidian/Genealogy/_Meta/Skills/genealogy-source-ingestion/SKILL.md)
- **genealogy-timeline-auditor** (Genealogy): [genealogy-timeline-auditor](file:///home/jpino/Obsidian/Genealogy/_Meta/Skills/genealogy-timeline-auditor/SKILL.md)
- **git-crypt-vault-safety** (Common): [git-crypt-vault-safety](file:///home/jpino/Obsidian/Common/_Meta/Skills/git-crypt-vault-safety/SKILL.md)
- **hardware-routing-constraints** (Common): [hardware-routing-constraints](file:///home/jpino/Obsidian/Common/_Meta/Skills/hardware-routing-constraints/SKILL.md)
- **keepass-security-audit** (Common): [keepass-security-audit](file:///home/jpino/Obsidian/Common/_Meta/Skills/keepass-security-audit/SKILL.md)
- **kern-reverse-proxy-sso** (Common): [kern-reverse-proxy-sso](file:///home/jpino/Obsidian/Common/_Meta/Skills/kern-reverse-proxy-sso/SKILL.md)
- **macbook-ubuntu-repair** (Common): [macbook-ubuntu-repair](file:///home/jpino/Obsidian/Common/_Meta/Skills/macbook-ubuntu-repair/SKILL.md)
- **markdown-transport-sanitizer** (Common): [markdown-transport-sanitizer](file:///home/jpino/Obsidian/Common/_Meta/Skills/markdown-transport-sanitizer/SKILL.md)
- **mobile-termux-node** (Common): [mobile-termux-node](file:///home/jpino/Obsidian/Common/_Meta/Skills/mobile-termux-node/SKILL.md)
- **obsidian-bases** (Common): [obsidian-bases](file:///home/jpino/Obsidian/Common/_Meta/Skills/obsidian-bases/SKILL.md)
- **obsidian-frontmatter-standard** (Common): [obsidian-frontmatter-standard](file:///home/jpino/Obsidian/Common/_Meta/Skills/obsidian-frontmatter-standard/SKILL.md)
- **open-webui-iac** (Common): [open-webui-iac](file:///home/jpino/Obsidian/Common/_Meta/Skills/open-webui-iac/SKILL.md)
- **overlook-client-node** (Common): [overlook-client-node](file:///home/jpino/Obsidian/Common/_Meta/Skills/overlook-client-node/SKILL.md)
- **script-execution-harness** (Common): [script-execution-harness](file:///home/jpino/Obsidian/Common/_Meta/Skills/script-execution-harness/SKILL.md)
- **self_healing_test_harness** (Common): [self_healing_test_harness](file:///home/jpino/Obsidian/Common/_Meta/Skills/self_healing_test_harness/SKILL.md)
- **voice-control-npu** (Common): [voice-control-npu](file:///home/jpino/Obsidian/Common/_Meta/Skills/voice-control-npu/SKILL.md)

## Key Directives
1. **Frontmatter Guardrails (ADR-022)**: Ensure YAML frontmatter uses isolated `---` delimiters and inline arrays (`[]`).
2. **Epistemic Provenance (SYS-SCH-003)**: Explicitly separate certified facts (`proven_...`) from AI hypotheses (`ai_inferred_...`).
3. **Local Git Cache (ADR-024)**: Commit sub-second to local bare cache repos (`git-cache/*.git`).
