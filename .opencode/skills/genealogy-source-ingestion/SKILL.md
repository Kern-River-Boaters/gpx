---
name: "genealogy-source-ingestion"
description: "genealogy-source-ingestion skill for OpenCode"
---

# genealogy-source-ingestion

> Parent Skill Definition: [genealogy-source-ingestion](file:///home/jpino/Obsidian/Genealogy/_Meta/Skills/genealogy-source-ingestion/SKILL.md)

---
name: genealogy-source-ingestion
description: Ingests raw genealogical source documents (PDFs, census images, birth/baptismal certificates, military registers) from Sources/_Inbox/ and online repositories, applies ADR-011 filename sanitization, performs visual statistical variance verification, integrates archival-vision-engine restoration, extracts general vital facts (occupations, religion, places lived, immigration), and enforces universal bidirectional atomic linking per SOP-GEN-002, ADR-013, ADR-020, ADR-021, and SOP-GEN-008.
---

# 🏛️ Genealogical Source Ingestion & Epistemic Provenance Standard

Governed under **ADR-002 (Zero-Cruft)**, **ADR-020/021 (Tri-Asset Archival Vision)**, and **ADR-036 (Level 4 Provenance)**.

---

## 🔬 1. The 4-Tier Epistemic Provenance Taxonomy

| Epistemic Tier | Confidence Weight | Source Definition & Traceability Anchor |
| :--- | :---: | :--- |
| **Tier 1: Primary Archival Facsimile** | **1.00** | Direct, contemporaneous official record scan present in `Sources/` with verified physical bytes and visual embed. |
| **Tier 2: Human / Legacy GEDCOM Entry** | **0.80** | Pre-existing vault frontmatter/markdown entered by human researcher, pending primary record binding. |
| **Tier 3: Hermes Inferred Fact** | **0.60 – 0.90** | Machine-extracted biographical fact derived from OCR/HTR with explicit document coordinates. |
| **Tier 4: Quarantined Discrepancy** | **< 0.50** | Unresolved evidentiary conflict between sources; routed to staging for human review. |

---

## 📋 2. Universal Fact & Signal Extraction Taxonomy

Every ingested primary document extracts:
* **Honorific Signals**: Isolate `titles_and_honorifics` (`Capt.`, `Rev.`, `Esq.`, `Hon.`, `Deacon`, `Col.`, `Judge`, `Dr.`).
* **Occupational Tripwires**: Check professions requiring citizenship (Homesteaders under 1862 Act, Sheriffs, Tavern Licensees, Elected Officials).
* **Socioeconomic Wealth Tracking**: Extract Real Estate Value, Personal Estate Value (1850-1870 Censuses), and 1930 Radio Ownership (`R`).
* **Inter-Censal Gap Bridging**: Extract City Directory annual residence and `"widow of [Name]"` entries.
* **Geopolitical Normalization**: Map archaic jurisdictions (`Canada East` $\rightarrow$ Quebec, `Canada West` $\rightarrow$ Ontario).

---

## 🛡️ 3. Non-Destructive Conflict Resolution (Zero Silent Overwrites)
* When primary evidence conflicts with legacy human-entered properties, inject an epistemic discrepancy audit table:
```markdown
## 🔍 Epistemic Discrepancy & Verification Audit
| Field | Human-Curated Value | Primary Source Value | Ground-Truth Document | Resolution & Confidence |
| :--- | :--- | :--- | :--- | :--- |
```
* Telemetry emitted to `_Meta/Telemetry/Genealogy_Provenance_Ledger.jsonl`.

---

## 🏛️ 4. 3-Tier Archival Images, Tripartite Dates & Audit Tags
* **3-Tier Image Lineage**: Every scan maintains `-Master.jpg` (pristine bitstream), `-Display.jpg` (Markdown embed), and `-Inference.jpg` (Sauvola-binarized machine vision input).
* **Tripartite Date Hierarchy**: `event_date` > `registration_date` > `issue_date`. Certificate issuance dates never override event dates.
* **4-Tier Hierarchical Geocoding**: Requires `city_town`, `county_parish`, `state_province`, `country_sovereignty`.
* **Mandatory Post-Processing Audit Tags**: Every ingested profile is stamped with `audit_tag: verified_empirical`, `audit_date: YYYY-MM-DD`, `audit_status: passed`, and discrepancy resolutions.

