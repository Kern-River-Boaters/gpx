---
name: "genealogy-newspaper-clipping-harvester"
description: "genealogy-newspaper-clipping-harvester skill for OpenCode"
---

# genealogy-newspaper-clipping-harvester

> Parent Skill Definition: [genealogy-newspaper-clipping-harvester](file:///home/jpino/Obsidian/Genealogy/_Meta/Skills/genealogy-newspaper-clipping-harvester/SKILL.md)

---
name: genealogy-newspaper-clipping-harvester
description: "Governs automated discovery, extraction, OCR text indexing, and back-annotation of historical newspaper clippings from Newspapers.com, Ancestry.com Publisher Extra, and regional gazettes into Obsidian vault profiles under SYS-SCH-002."
---

# Genealogy Newspaper Clipping Harvester Skill

## Overview
This skill governs the automated harvesting, optical processing, metadata indexing, and biographical back-annotation of historical news clippings from **Newspapers.com (Publisher Extra)**, **Ancestry.com**, and local town reports into the Obsidian Genealogy vault.

## Core Procedures

### 1. Ingestion & Staging
- All newspaper clippings and town reports must be staged in `Sources/Published_Histories/` using ADR-011 naming standards:
  - Example: `John_W_Whalen_died_Tuesday_June_9_1936.jpg`
  - Example: `Eastport Alms House Master John Whalen.jpg`
  - Example: `John_W_Warren_won_shooting_match.jpg`

### 2. Auto-Cataloging & Indexing
- Run the harvester script to scan for newly added clippings and regenerate the central catalog:
  ```bash
  python3 _Meta/Scripts/harvest_newspaper_clippings.py
  ```
- Generates/updates **`00_Projects_and_Dashboards/Historical_Newspaper_Clippings_Index.md`** with artifact links, publication metadata, and related ancestors.

### 3. Biographical Back-Annotation (`SYS-SCH-002`)
- Every harvested clipping must be back-annotated into the subject's profile note (`People/...`):
  1. Embedded preview in `### 🖼️ Primary Archival Document Previews (Embedded)`:
     ```markdown
     #### 📰 1883 Kennebec Journal Marksmanship Report
     ![[Sources/Published_Histories/John_W_Warren_won_shooting_match.jpg|600]]
     ```
  2. Narrative integration in `## 📖 Biographical Narrative & Historical Context`.
  3. Clickable link in `## 📚 Complete Archival Evidence & Document Library on File`.

