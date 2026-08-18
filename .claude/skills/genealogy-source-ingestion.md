# genealogy-source-ingestion

> Parent Skill Definition: [genealogy-source-ingestion](file:///home/jpino/Obsidian/Genealogy/_Meta/Skills/genealogy-source-ingestion/SKILL.md)

---
name: genealogy-source-ingestion
description: Ingests raw genealogical source documents (PDFs, census images, birth/baptismal certificates) from Sources/_Inbox/, applies ADR-011 filename sanitization, links sources to verified profiles, embeds visual document previews, and updates frontmatter facts per SOP-GEN-002 and ADR-013.
---

# Genealogy Source Ingestion Skill

## Purpose
Automate processing of new source documents added to `Sources/_Inbox/`, enforcing strict **ADR-011 filename sanitization**, organizing files into permanent person directories under `Sources/`, linking files in `People/` profile notes, embedding visual image previews (`![[...|600]]`), and updating vital frontmatter facts and citizenship trackers per **SOP-GEN-002** and **ADR-013**.

## Ingestion Workflow
1. **Inbox Scanning**: Scan `Sources/_Inbox/` for incoming `.pdf`, `.jpg`, `.png`, `.jpeg`, `.webp` files.
2. **Filename Normalization (ADR-011)**:
   - Format: `[YYYY]-[EventType]-[LastnameFirstname]-[Location].[ext]`
   - Strip all non-ASCII characters, emojis, quotes, parentheses, and shell characters.
   - Replace spaces with hyphens.
3. **Permanent Organization**:
   - Relocate sanitized files from `Sources/_Inbox/` to dedicated person directories (e.g. `Sources/<Gen>-<PersonName>/` or `Sources/Vital_Statistics/`).
4. **Visual Embedding & Metadata Update (ADR-013)**:
   - Append clean unquoted WikiLinks to YAML frontmatter `sources:`.
   - Embed high-resolution document previews (`![[Sources/...|600]]`) under `### 🖼️ Primary Archival Document Previews (Embedded)`.
   - Maintain the complete clickable library under `### 📚 Complete Archival Evidence & Document Library on File`.
   - Provide direct 1-click live online database links and exact archival microfilm ordering locators.
5. **Citizenship Tracker Alignment**:
   - Update `00_Projects_and_Dashboards/Citizenship_Chains/` and `00_Projects_and_Dashboards/Project - Canadian Citizenship Document Acquisition.md`.

