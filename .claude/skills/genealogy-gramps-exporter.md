# genealogy-gramps-exporter

> Parent Skill Definition: [genealogy-gramps-exporter](file:///home/jpino/Obsidian/Genealogy/_Meta/Skills/genealogy-gramps-exporter/SKILL.md)

---
name: genealogy-gramps-exporter
description: "Standardizes vault-to-GEDCOM export using obsidian-gramps-provenance-sync, guaranteeing 100% bidirectional family pointer symmetry, native SOUR/REPO/QUAY/EXID/OBJE serialization, dual GEDCOM 7.0 and 5.5.1 header compliance, and private export placement per ADR-GEN-007, ADR-GEN-023, and SOP-GEN-010."
---

# Genealogy Gramps Exporter Skill

## Purpose
Export Markdown profiles and source records from the vault into strict GEDCOM 5.5.1 and next-generation GEDCOM 7.0 formats (`.ged`) using the `obsidian-gramps-provenance-sync` engine, ensuring 100% bidirectional pointer symmetry (`FAMS`/`FAMC` <-> `HUSB`/`WIFE`/`CHIL`), native source/repository records (`0 @S...@ SOUR`, `0 @R...@ REPO`, `QUAY 0-3`, `PAGE`, `OBJE`), GEDCOM 7.0 schemas (`HEAD.SCHMA`, `EXID`, `NO NATU`), and routing outputs strictly to the private `Sources/Exports/` vault directory per **ADR-GEN-007**, **ADR-GEN-023**, and **SOP-GEN-010**.

## Rules & Safety Controls
1. **Private Export Target**: All production exports MUST land in `Sources/Exports/Vault_Export_5.5.1.ged` and `Sources/Exports/Vault_Export_7.0.ged`.
2. **Native Source & Repository Linking**:
   - Every `doc_type: source` companion note in `Sources/` exports as a top-level `0 @S...@ SOUR` record with `TITL`, `AUTH`, `PUBL`, `REPO`, `OBJE`.
   - Every unique repository exports as a `0 @R...@ REPO` record.
   - Individual citations link via `1 SOUR @S...@` with `2 QUAY` (0–3) and `2 PAGE`.
3. **GEDCOM 7.0 Features**:
   - `HEAD.GEDC.VERS 7.0` with `HEAD.SCHMA` extension schema blocks.
   - `EXID` external identifier tags mapping URNs and persistent entity IDs.
   - `NO NATU` negative evidence assertions for proven alienage retention.
4. **Reciprocal Pointer Symmetry**: Every family record (`FAM`) with husband, wife, or children must have matching reciprocal `FAMS` or `FAMC` pointers on individual records (`INDI`).
5. **Performance SLA**: Graph resolution operates at $O(1)$ dictionary complexity via tokenized name indexes, exporting 13,000+ individuals and 700+ sources in under 5 seconds.
6. **Execution Commands**:
   ```bash
   # Export GEDCOM 5.5.1
   python3 obsidian-gramps-provenance-sync/src/exporter.py --version 5.5.1

   # Export GEDCOM 7.0
   python3 obsidian-gramps-provenance-sync/src/exporter.py --version 7.0

   # Export Both Formats Simultaneously
   python3 obsidian-gramps-provenance-sync/src/exporter.py --version both
   ```

