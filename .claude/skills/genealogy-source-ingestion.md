# genealogy-source-ingestion

> Parent Skill Definition: [genealogy-source-ingestion](file:///home/jpino/Obsidian/Genealogy/_Meta/Skills/genealogy-source-ingestion/SKILL.md)

---
name: genealogy-source-ingestion
description: Ingests raw genealogical source documents (PDFs, census images, birth/baptismal certificates) from Sources/_Inbox/, applies ADR-011 filename sanitization, links sources to verified profiles, and updates frontmatter facts per SOP-GEN-002.
---

# Genealogy Source Ingestion Skill

## Purpose
Automate processing of new source documents added to `Sources/_Inbox/`, enforcing strict **ADR-011 filename sanitization**, linking files to `People/Verified/` profile notes, and updating vital frontmatter facts and citizenship trackers per **SOP-GEN-002**.

## Workflow
1. **Inbox Scanning**: Scan `Sources/_Inbox/` for incoming `.pdf`, `.jpg`, `.png`, `.jpeg`, `.webp` files.
2. **Filename Normalization (ADR-011)**:
   - Format: `[YYYY]-[EventType]-[LastnameFirstname]-[Location].[ext]`
   - Strip all non-ASCII characters, emojis, quotes, parentheses, and shell characters.
   - Replace spaces with hyphens.
3. **Target Profile Resolution**:
   - Match `LastnameFirstname` against existing profiles in `People/Verified/` or `People/Extended_Family/`.
4. **Source Linking & Metadata Update**:
   - Move sanitized file to `Sources/`.
   - Append markdown link under `## 📄 Source Documents` in target profile note.
   - Update frontmatter fields (`birth_date`, `birth_place`, `death_date`, `death_place`) if new facts are discovered.
5. **Execution Command**:
   ```bash
   python3 _Meta/Scripts/ingest_inbox_sources.py --inbox Sources/_Inbox/ --sources Sources/
   ```

