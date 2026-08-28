# gedcom-export-standard

> Parent Skill Definition: [gedcom-export-standard](file:///home/jpino/Obsidian/Genealogy/obsidian-gramps-provenance-sync/skills/gedcom-export-standard/SKILL.md)

---
name: gedcom-gramps-export
description: "Standards and execution rules for exporting Obsidian genealogy vaults to strict GEDCOM 5.5.1 format with 100% bidirectional pointer symmetry for Gramps import."
---

# GEDCOM Export & Gramps Integration Standard

> [!INFO] Official Standard Specification
> Authoritative GEDCOM specification document: [GEDCOM 5.5.1 Specification PDF](references/ged551.pdf)

## Core Rules
1. **Bidirectional Symmetry:** Never write a `FAM` record without ensuring all referenced `HUSB`, `WIFE`, and `CHIL` records contain matching `FAMS` or `FAMC` tags.
2. **Strict Uppercase Tags:** GEDCOM tags must follow uppercase level hierarchy (`0 HEAD`, `1 INDI`, `1 FAM`, etc.).
3. **Provenance Preservation:** Retain provenance metadata in `NOTE` / `2 CONC` tags for auditability.

