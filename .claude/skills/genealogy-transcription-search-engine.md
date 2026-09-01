# genealogy-transcription-search-engine

> Parent Skill Definition: [genealogy-transcription-search-engine](file:///home/jpino/Obsidian/Genealogy/_Meta/Skills/genealogy-transcription-search-engine/SKILL.md)

---
name: genealogy-transcription-search-engine
description: "Governs full-text regex and fuzzy discovery across Layer 3 OCR transcriptions of all source holdings in Sources/, enabling serendipitous kinship discovery, multi-generational witness triangulation, godparent (padrino) linkage, and automated Base query back-annotation across federated vaults."
---

# 🔍 Genealogical Cross-Corpus Transcription & Kinship Discovery Engine

Governed under **ADR-GEN-022 (Hermes Document Extraction Ontology & Level 4 Provenance)** and **SOP-GEN-010**.

---

## 🎯 1. Overview & Operational Purpose

Because all 743+ source holdings in `Sources/` feature **Layer 3 Verbatim Archival Document Transcriptions (OCR)**, the vault supports full-text semantic and regex querying across the entire archival corpus:
* **Serendipitous Kinship Discovery**: Locate unlinked family members mentioned as witnesses, godparents (*padrinos*), declarantes, executors, and neighbors.
* **Maiden Name & Alias Triangulation**: Trace maiden surnames (*Romani*, *Dunham*, *Dudley*, *Lesley / Leslie*, *Gutiérrez*, *Rexach*) across unrelated municipal and census files.
* **Automated Back-Annotation**: When an ancestor's presence is verified in a previously disconnected document, the engine back-annotates their WikiLink into frontmatter `people:` and Layer 2 tables, instantly updating their Obsidian Base table.

---

## 🛠️ 2. Discovery Execution Standard

To search and discover unlinked connections across all source notes:

```bash
# Search for specific surname or person across all Layer 3 OCR text
python3 _Meta/Scripts/discover_kinship_across_transcriptions.py --query "Oscar Torres"

# Search with automatic back-annotation to link discovered files to ancestor Base tables
python3 _Meta/Scripts/discover_kinship_across_transcriptions.py --query "Romani" --apply
```

---

## 🛡️ 3. Kinship Triangulation Invariants

1. **Epistemic Provenance Rule**: Back-annotation must only occur if the extracted person unambiguously matches a vault profile or establishes a new corroborated candidate.
2. **Table Pipe Escaping Invariant**: When adding newly discovered individuals to Layer 2 tables, table WikiLinks must escape pipes as `[[Target\|Alias]]`.
3. **Reciprocal Pointer Invariance**: Ensure newly discovered family connections are reflected in bidirectional frontmatter pointers.

