---
name: "genealogy-gramps-exporter"
description: "genealogy-gramps-exporter skill for OpenCode"
---

# genealogy-gramps-exporter

> Parent Skill Definition: [genealogy-gramps-exporter](file:///home/jpino/Obsidian/Genealogy/_Meta/Skills/genealogy-gramps-exporter/SKILL.md)

---
name: genealogy-gramps-exporter
description: Standardizes vault-to-GEDCOM export using obsidian-gramps-provenance-sync, guaranteeing 100% bidirectional family pointer symmetry, strict GEDCOM 5.5.1 header compliance, and private export placement per GEN-ADR-007 and SOP-GEN-003.
---

# Genealogy Gramps Exporter Skill

## Purpose
Export Markdown profiles from the vault into strict GEDCOM 5.5.1 format (`.ged`) using the `obsidian-gramps-provenance-sync` engine, ensuring 100% bidirectional pointer symmetry (`FAMS`/`FAMC` <-> `HUSB`/`WIFE`/`CHIL`) and routing outputs strictly to the private `Sources/Exports/` vault directory per **GEN-ADR-007** and **SOP-GEN-003**.

## Rules & Safety Controls
1. **Private Export Target**: All production exports MUST land in `Sources/Exports/Vault_Export_Latest.ged`.
2. **Package Isolation**: Never output vault exports to package test directories (e.g. `obsidian-gramps-provenance-sync/tests/`).
3. **Reciprocal Pointer Symmetry**: Every family record (`FAM`) with husband, wife, or children must have matching reciprocal `FAMS` or `FAMC` pointers on individual records (`INDI`).
4. **Execution Command**:
   ```bash
   python3 obsidian-gramps-provenance-sync/src/exporter.py
   ```

