# genealogy-source-ingestion

> Parent Skill Definition: [genealogy-source-ingestion](file:///home/jpino/Obsidian/Genealogy/_Meta/Skills/genealogy-source-ingestion/SKILL.md)

---
name: genealogy-source-ingestion
description: Ingests raw genealogical source documents (PDFs, census images, birth/baptismal certificates, military registers) from Sources/_Inbox/ and online repositories, applies ADR-011 filename sanitization, performs visual statistical variance verification, integrates archival-vision-engine restoration, extracts general vital facts (occupations, religion, places lived, immigration), enforces universal bidirectional atomic linking, formats canonical companion source Markdown notes with doc_type: source, and strictly enforces table WikiLink pipe escaping per ADR-023 and SOP-GEN-010.
---

# 🏛️ Genealogical Source Ingestion & Epistemic Provenance Standard

Governed under **ADR-002 (Zero-Cruft)**, **ADR-020/021 (Tri-Asset Archival Vision)**, **ADR-023 (Standardized Source Frontmatter & Table Pipe Escaping)**, and **SOP-GEN-010**.

---

## 🔬 1. The 4-Tier Epistemic Provenance Taxonomy

| Epistemic Tier | Confidence Weight | Source Definition & Traceability Anchor |
| :--- | :---: | :--- |
| **Tier 1: Primary Archival Facsimile** | **1.00** | Direct, contemporaneous official record scan present in `Sources/` with verified physical bytes and visual embed. |
| **Tier 2: Human / Legacy GEDCOM Entry** | **0.80** | Pre-existing vault frontmatter/markdown entered by human researcher, pending primary record binding. |
| **Tier 3: Hermes Inferred Fact** | **0.60 – 0.90** | Machine-extracted biographical fact derived from OCR/HTR with explicit document coordinates. |
| **Tier 4: Quarantined Discrepancy** | **< 0.50** | Unresolved evidentiary conflict between sources; routed to staging for human review. |

---

## 📄 2. Canonical Companion Note Frontmatter (`doc_type: source`)

Every archival asset holding in `Sources/` is defined by a canonical `.md` note with 84 typed properties registered in `.obsidian/types.json`:

```yaml
---
doc_type: source
id: SRC-CENS-1900-1900_CENSUS_CALAIS
title: 1900 US Federal Census - Calais ME
description: Primary genealogical holding for 1900 US Federal Census documenting John Warren Whalen family in Calais, Maine.
tags:
  - topic/genealogy
  - topic/census
  - provenance/primary_facsimile
created: '2026-08-30'
updated: '2026-08-30'
status: verified
version: '1.0'
source_type: census
people:
  - '[[People/W/Whalen/Whalen, John Warren 1860-08-12|John Warren Whalen]]'
  - '[[People/W/Whalen/Whalen, Hollis Vernon 1898-12-14|Hollis Vernon Whalen]]'
event_date: '1900-06-01'
year: 1900
location: Calais, Washington County, Maine, USA
repository: National Archives and Records Administration (NARA)
portfolio:
  - canadian_citizenship_chain_a
quay: 3
epistemic_tier: 'Tier 1: Primary Archival Facsimile'
verification_status: verified_empirical
media_file: '[[Sources/Census/1900-Census-CalaisME-JohnWWhalenFamily-Page1-Display.jpg]]'
master_asset: '[[Sources/Census/1900-Census-CalaisME-JohnWWhalenFamily-Page1-Master.jpg]]'
display_asset: '[[Sources/Census/1900-Census-CalaisME-JohnWWhalenFamily-Page1-Display.jpg]]'
inference_asset: '[[Sources/Census/1900-Census-CalaisME-JohnWWhalenFamily-Page1-Inference.png]]'
pdf_asset: '[[Sources/Census/1900-Census-CalaisME-JohnWWhalenFamily.pdf]]'
sha256: 33223ae53240f98e7a7c95269007e8d56402f9d98fd642a63aca03e95018938a
audit_tag: verified_empirical
audit_date: '2026-08-30'
audit_status: passed
---
```

---

## 🧹 3. Strict Markdown Table WikiLink Pipe Escaping Standard

* **Root Cause Invariant**: In Markdown table syntax, `|` is the cell delimiter. Embedding `[[Target|Alias]]` into a table cell splits the cell and creates phantom columns.
* **Mandatory Table Syntax**: Inside any Markdown table row, ALL WikiLink alias pipes MUST be escaped as `[[Target\|Alias]]`.
* **Frontmatter Invariant**: In YAML frontmatter, pipes MUST NEVER be backslash-escaped (`'[[Target|Alias]]'`).
* **Automated Sentinel**: `_Meta/Scripts/sanitize_markdown_tables.py` audits and enforces 0 unescaped table pipes vault-wide.

---

## 🌳 4. Obsidian Bases Dynamic Evidence Dashboards

Every person profile (`People/`) queries corroborating evidence dynamically using Bases-native syntax:
```markdown
## 📄 Source Documents & Archival Evidence

```base
filters:
  and:
    - doc_type == "source"
    - file.hasLink("Whalen, Hollis Vernon 1898-12-14.md")
views:
  - type: table
    name: Corroborating Evidence
    order:
      - year
      - source_type
      - file.name
      - repository
```
```

---

## 🏛️ 5. 3-Tier Archival Images, Tripartite Dates & Audit Tags

* **3-Tier Image Lineage**: Every scan maintains `-Master.jpg` (pristine bitstream), `-Display.jpg` (Markdown embed), and `-Inference.jpg` (Sauvola-binarized machine vision input).
* **Tripartite Date Hierarchy**: `event_date` > `registration_date` > `issue_date`. Certificate issuance dates never override event dates.
* **4-Tier Hierarchical Geocoding**: Requires `city_town`, `county_parish`, `state_province`, `country_sovereignty`.
* **Zero Synthetic Evidence Prohibition**: Agents are strictly forbidden from generating artificial canvas/PIL mock certificates. All evidence must be genuine empirical archival scans.

