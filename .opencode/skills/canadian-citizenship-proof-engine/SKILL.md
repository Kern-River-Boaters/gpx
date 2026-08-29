---
name: "canadian-citizenship-proof-engine"
description: "canadian-citizenship-proof-engine skill for OpenCode"
---

# canadian-citizenship-proof-engine

> Parent Skill Definition: [canadian-citizenship-proof-engine](file:///home/jpino/Obsidian/Genealogy/_Meta/Skills/canadian-citizenship-proof-engine/SKILL.md)

---
name: canadian-citizenship-proof-engine
description: Governs proof verification, dual-anchor lineage triangulation, archival order generation, and IRCC dossier compilation under Bill C-3 / Senate Bill S-245, ADR-013, ADR-021, and SOP-GEN-008 across federated genealogy vaults.
---

# Canadian Citizenship Proof Engine Skill (Bill C-3 / S-245)

## 🛡️ Anti-Hallucination & Provenance Integrity Mandate (CRITICAL)

### 1. Absolute Prohibition on Fabricated Citations & Synthetic Facsimiles
- **NEVER Fabricate Archival Hold Citations**: Agents must NEVER invent specific reel numbers, register numbers, folio/page numbers, or Latin register transcription text (e.g. *Actus Baptismi*) unless the exact scan or certified transcript has been physically inspected or retrieved from a verified digital database.
- **NEVER Disguise Hypotheses as Verified Documents**: Generated image cards must NEVER pretend to be authentic camera scans or proven holdings. 
- **Full Transparency**: If an agent hypothesizes where a record is located based on surrounding vital clues, it must be explicitly tagged as `doc_type: research_hypothesis` and titled `🔍 Archival Search Hypothesis: [Description]`.

### 2. Dual-Asset Archival Ingestion & Golden Master Standard (ADR-021 / SOP-GEN-008)
- Every archival microfilm from Library and Archives Canada (LAC) or Provincial Archives of New Brunswick (PANB) must be processed via the **Archival Vision Engine (`archival-vision-engine`)**:
  - **Blank Page Fast-Fail & Reel Warm-Start:** Bypasses spacer frames in $<5\text{ms}$ and caches baseline hyperparameters across reel frames.
  - **Edge-Preserving Bilateral Background Normalization:** Uses downsampled bilateral filtering ($d=15, \sigma=75$) and continuous division to flatten illumination gradients without halo ringing.
  - **Global Gamma Contrast Shift ($\gamma=0.85$):** Restores mid-tone contrast for faint iron gall ink strokes and column delimiters without highlight blowout.
  - **2x Super-Resolution Enhanced Copy:** Staged alongside the master scan (`-Enhanced.jpg` + `-Master.jpg`).
  - **DIEM-v2 Evidentiary Scorecard:** Requires $\text{Score} \ge 85.0/100$, positive field gain ($\Delta\text{Fields} \ge 0$), and mathematical checksum verification to validate 100% enumeration completeness.

### 3. The Three-Tier Evidence Classification
1. 🟢 **Tier 1: Verified Empirical Evidence**:
   - Documents and indices directly searched, fetched, and verified (e.g., US Federal Censuses from NARA, State Department of Health birth/death certificates, LAC/PANB microfilm facsimiles).
2. 🟡 **Tier 2: Archival Search Hypotheses**:
   - Explicitly formulated research targets ("Based on the 1898 Maine birth certificate stating father was born in New Brunswick in Aug 1860, we hypothesize a baptism exists in PANB Charlotte County Catholic/Anglican registers").
3. 🔴 **Tier 3: Unverified / Negative Leads**:
   - Repositories or collections searched where no matching record was found.

---

## 🏛️ Core Statutory Principles (Bill C-3 / S-245)

### 1. Repeal of First-Generation Limit (FGL)
- Bill C-3 repeals the First-Generation Limit for all individuals born abroad prior to December 15, 2025 who are direct lineal descendants of a Canadian-born parent or ancestor.

### 2. Substantial Connection Exemption
- All individuals born abroad prior to December 15, 2025 are **100% exempt** from the 1,095-day physical presence requirement in Canada.

### 3. Maternal Parity Doctrine
- Descent through maternal lines (mothers, grandmothers, great-grandmothers) holds 100% legal parity with paternal lines under Section 3 of the amended Citizenship Act.

## 📁 Deliverable Topology & Clean 3+1 Standard Model (ADR-009)

When generating or updating client deliverable repositories (`00_Projects_and_Dashboards/`), the agent MUST enforce the **3+1 Clean Suite Standard**:

```
00_Projects_and_Dashboards/
├── 00_Master_Dashboard.md                                # Single interactive landing portal (Overview, KPIs, Quick Links)
├── 1_Canadian_Citizenship_Executive_Evidence_Summary.md  # Formal statutory brief for IRCC / Legal Counsel (Bill C-3 / S-245)
├── 2_Canadian_Citizenship_Archival_Request_Packet.md     # Actionable pre-filled email orders for archives (PANB, LAC)
├── 3_Archival_Research_Strategy.md                       # (Optional) Specialized parish guide and repository search plan
└── Family_Citizenship_Descent_Tree.canvas                # Visual interactive generational canvas (G-1 -> G4)
```

### Critical Rules:
1. **Zero Scraper / Diagnostic Residue**: Internal crawler logs, visual variance scores ($\sigma$), and raw API traces are transient and MUST NOT be saved into `00_Projects_and_Dashboards/`.
2. **Standardized Deliverable Prefixes**: Executive Briefs and Archival Order Packets must use numeric prefixes (`1_`, `2_`, `3_`) so clients and counsel have unambiguous sequence priority.
3. **Visual Canvas Generation**: Every citizenship portfolio MUST include `Family_Citizenship_Descent_Tree.canvas` linking applicant cards directly to verified evidence scans.

## 🎨 Mermaid Diagram Governance Standard
When generating Mermaid diagrams for archival search hypotheses, lineage evidence matrices, or descent trees:
1. **Explicit Subgraph ID and Quoted Title**: Always use `subgraph ID ["Quoted Human Title"]` (e.g. `subgraph PANB_TARGET ["Archival Order Target (PANB)"]`). Never use unquoted spaces or parentheses in subgraph declarations.
2. **Safe Arrow Syntax**: Use `-->` or `-.->|"Label"|` with quoted link labels.
3. **HTML Label Sanitization**: Ensure nodes use HTML-safe escape characters when embedding line breaks (`<br/>`) or formatting.

