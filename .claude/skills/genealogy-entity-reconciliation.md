# genealogy-entity-reconciliation

> Parent Skill Definition: [genealogy-entity-reconciliation](file:///home/jpino/Obsidian/Genealogy/_Meta/Skills/genealogy-entity-reconciliation/SKILL.md)

---
name: genealogy-entity-reconciliation
description: "Audits duplicate profiles, executes 3-tier triangulated matching, performs non-destructive entity merging, and repoints WikiLink array links (parents, spouse, children) across vault records per GEN-ADR-004 and GEN-ADR-005."
---

# Genealogy Entity Reconciliation Skill

## Purpose
Detect duplicate individual profile nodes across `People/Verified/` and `People/Extended_Family/`, evaluate 3-tier triangulated matching, execute non-destructive entity reconciliation, and repoint WikiLinks system-wide per **GEN-ADR-004** and **GEN-ADR-005**.

## Reconciliation Protocol
1. **Triangulated Matching**:
   - **Tier 1**: Deterministic URN match (`id: URN-GEN-...`).
   - **Tier 2**: High-confidence match (Normalized name match + identical birth/death year overlap + location match).
   - **Tier 3**: Probabilistic match (Name similarity + location overlap).
2. **Non-Destructive Archiving**:
   - Primary profile (`People/Verified/` if available) is retained.
   - Secondary profile content is merged into primary notes under `## 📜 Archived Records & Provenance`.
   - Secondary file is moved to `People/Archived/` or marked with `status: merged`.
3. **WikiLink Repointing**:
   - Repoint all `parents:`, `spouse:`, and `children:` array references across the entire vault to point to the primary node.
4. **Execution Commands**:
   ```bash
   python3 _Meta/Scripts/detect_safe_duplicates.py --vault . --report 00_Projects_and_Dashboards/Duplicate_Audit_Report.md
   ```

