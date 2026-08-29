# genealogy-source-ingestion

> Parent Skill Definition: [genealogy-source-ingestion](file:///home/jpino/Obsidian/Genealogy/_Meta/Skills/genealogy-source-ingestion/SKILL.md)

---
name: genealogy-source-ingestion
description: Ingests raw genealogical source documents (PDFs, census images, birth/baptismal certificates, military registers) from Sources/_Inbox/ and online repositories, applies ADR-011 filename sanitization, performs visual statistical variance verification, integrates archival-vision-engine restoration, links sources to verified profiles, and updates frontmatter facts per SOP-GEN-002, ADR-013, ADR-021, and SOP-GEN-008.
---

# 📜 Genealogy Source Ingestion & Evidence Ingestion Standard

## 📌 Executive Summary
High-integrity genealogy vaults require deterministic evidence ingestion, strict file naming standards, visual quality validation, DIEM-v2 paleographic scoring, and companion metadata notes for every primary document.

---

## 🛡️ Ingestion Governance & Standards

### 1. ADR-011 Filename Standard
All ingested documents must adhere to deterministic, date-anchored filenames:
* **Vital Statistics:** `Sources/Vital_Statistics/{YYYY}-{EventType}-{PersonName}-{Location}.png`
* **Microfilm Master & Enhanced Scans:** `Sources/Microfilms/{YYYY}-{DocType}-{Location}-{Subject}-Master.jpg` and `-Enhanced.jpg`
* **Censuses:** `Sources/Census/{YYYY}-Census-{Location}-{FamilyName}.png`
* **Military / Legal:** `Sources/Military/{YYYY}-{RecordType}-{PersonName}.png`
* **Newspaper Clippings:** `Sources/Newspaper_Clippings/{YYYY-MM-DD}-Clipping-{URN}-{Publication}.png`

### 2. Autonomous Visual Quality & Golden Master Restoration Engine (ADR-021 & SOP-GEN-008)
Every ingested primary microfilm must be processed and verified through `archival-vision-engine`:
* **Reel Statefulness & Fast-Fail Sentinel:** Bypasses spacer frames in $<5\text{ms}$ and inherits baseline hyperparameters across sequential frames.
* **Edge-Preserving Bilateral Background Normalization:** Eliminates illumination gradients, binding shadows, and tape splices without halo ringing using downsampled bilateral filtering ($d=15, \sigma=75$) and continuous division.
* **Global Gamma Shift ($\gamma=0.85$):** Restores mid-tone contrast for faint cursive script and vertical table delimiters without highlight blowout.
* **Natural Delimiter & Intersection Matrix:** Detects genuine grid boundaries ($\text{Intersections} = \text{h\_lines} \land \text{v\_lines}$) with organic charcoal overlay `#6E6964`.
* **2x Super-Resolution Upscaling:** Lanczos-4 upscaling to $\ge 4000\text{px}$ width.
* **DIEM-v2 Scorecard Gate:** Enforces $\text{Score} \ge 85.0/100$, $\text{Continuity} \ge 80\%$, $\text{Noise} \le 4\%$, $\text{FPD} \le 15\%$, and $\text{Median Comp Area} \le 350\text{px}$.

### 3. Structured Companion Markdown Standard
Every primary image file MUST have a corresponding companion Markdown note (`.md`) containing:
1. Complete YAML frontmatter (`doc_type`, `id`, `name`, `target_person`, `archive_ref`, `diem_v2_score`).
2. Visual preview embeds for both Enhanced and Master facsimiles.
3. Certified Markdown statutory transcription table.
4. Mathematical column checksum balance.
5. Evidentiary weight analysis for citizenship or lineage proof.

### 4. Strict Anti-SERP, Anti-Fabrication & Verified Facsimile Mandate (ADR-013 / SOP-GEN-002)
* **Absolute Ban on Synthetic / Mock Documents**: NEVER generate artificial, synthetic, mock, or simulated historical records, census returns, certificates, newspaper clippings, microfilms, or stamps/seals using PIL, ImageDraw, SVG canvas, or AI text-to-image tools. Manufacturing artificial proof documents is strictly prohibited.
* **Zero-SERP Policy**: NEVER capture, ingest, or embed search engine result pages (SERPs), search query lists, unauthenticated login screens ("Sign In"), or anti-bot block pages (`Error 15`, `Access Denied`).
* **Facsimile Requirement**: Only authentic primary document scans, certified civil certificates, genuine high-resolution microfilm facsimiles, census enumeration sheets, and parish register images obtained from real archival holdings or user uploads may be ingested into `Sources/` and linked to `People/` profiles.


