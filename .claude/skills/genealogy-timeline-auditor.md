# genealogy-timeline-auditor

> Parent Skill Definition: [genealogy-timeline-auditor](file:///home/jpino/Obsidian/Genealogy/_Meta/Skills/genealogy-timeline-auditor/SKILL.md)

---
name: genealogy-timeline-auditor
description: Audits genealogical profiles across the vault for timeline gaps, missing vital statistics, unlinked ancestors, broken WikiLinks, and chronological anomalies (e.g. parent born after child).
---

# Genealogy Timeline Auditor Skill

## Purpose
Perform systematic quality checks across all profiles in `People/` to detect chronological anomalies, missing vital statistics, unlinked relatives, broken WikiLinks, and timeline gaps.

## Audit Checks
1. **Chronological Sanity**: Parent birth date must precede child birth date by at least 12 years.
2. **Lifespan Sanity**: Birth date must precede death date; lifespan should not exceed 115 years without explicit proof note.
3. **Missing Vital Statistics**: Flag profiles lacking both birth and death dates/places.
4. **Unlinked Relatives**: Detect named relatives in text/frontmatter without valid `[[WikiLinks]]`.
5. **WikiLink Resolution**: Detect broken WikiLinks targeting non-existent note titles.

## Execution Command
```bash
python3 _Meta/Scripts/audit_timeline_gaps.py --vault . --report 00_Projects_and_Dashboards/Timeline_Gap_Audit_Report.md
```

