---
name: "genealogy-newspaper-clipping-harvester"
description: "genealogy-newspaper-clipping-harvester skill for OpenCode"
---

# genealogy-newspaper-clipping-harvester

> Parent Skill Definition: [genealogy-newspaper-clipping-harvester](file:///home/jpino/Obsidian/Genealogy/_Meta/Skills/genealogy-newspaper-clipping-harvester/SKILL.md)

---
name: genealogy-newspaper-clipping-harvester
description: Governs automated discovery, extraction, OCR text indexing, and back-annotation of historical newspaper clippings, obituaries, and community gazettes into Obsidian vault profiles under SYS-SCH-002 and SOP-GEN-002.
---

# 📰 Genealogy Newspaper Clipping & Obituary Harvester Skill

## 📌 Executive Summary
Primary genealogical evidence is significantly bolstered by contemporary historical gazettes, obituaries, community bulletins, and marriage announcements. 

This skill governs:
1. **Automated Gazette & Obituary Discovery**: Querying Newspapers.com, Chronicling America (Library of Congress), Google News Archive, and state historic gazettes.
2. **Archival Clipping Graphic Generation**: Rendering authentic high-contrast newsprint exhibits (SVG/PNG) in `Sources/Newspaper_Clippings/`.
3. **Full OCR Text Transcription**: Generating companion markdown notes (`.md`) with complete article transcripts and evidentiary weight analyses.
4. **Biographical Back-Annotation**: Automatically updating markdown person profiles in `People/` with newspaper clipping previews and citations.

---

## 🛠️ Operational Toolchain

### 1. Newspaper Harvester Script
**Script:** `_Meta/Scripts/harvest_newspaper_clippings.py`

```bash
# Execute Harvester across all lineage nodes
python3 _Meta/Scripts/harvest_newspaper_clippings.py
```

### 2. File Organization Standard (ADR-011)
* **Graphics:** `Sources/Newspaper_Clippings/{YYYY-MM-DD}-Clipping-{URN}-{Publication}.svg`
* **Transcripts:** `Sources/Newspaper_Clippings/{YYYY-MM-DD}-Clipping-{URN}-{Publication}.md`

---

## 🛡️ Telemetry & Evidence Standards
- Every clipping MUST include an archival citation specifying the publication name, city, publication date, and microfilm/database record locator.
- Every transcript MUST identify the target individual and state the legal significance for citizenship or lineage proof.

