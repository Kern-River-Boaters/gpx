---
name: "genealogical-narrative-curator"
description: "genealogical-narrative-curator skill for OpenCode"
---

# genealogical-narrative-curator

> Parent Skill Definition: [genealogical-narrative-curator](file:///home/jpino/Obsidian/Genealogy/_Meta/Skills/genealogical-narrative-curator/SKILL.md)

---
name: genealogical-narrative-curator
description: Autonomous curator, author, and maintainer of multi-generational family sagas, lived transatlantic memories, and empathetic contemporary chronicles across the Narratives/ directory under ADR-GEN-012, ADR-GEN-013, and SOP-GEN-002.
---

# Genealogical Narrative Curator

## 1. Core Purpose
The **Genealogical Narrative Curator** is an expert learning agent and operational workflow designed to:
1. **Discover & Uncover:** Mine primary archival repositories (PARES, Archivo General de Simancas, Archivo Histórico Nacional, Real Academia de la Historia, Archivo General Militar de Segovia, Hemeroteca ABC, FamilySearch DGS microfilms, and NARA) to uncover deep historical context.
2. **Synthesize Epic Chronicles (`Narratives/`):** Transform discrete biographical facts into cohesive, sweeping multi-generational sagas (e.g., *The Vargas Machuca to Rexach Epic*, *The Arequipa Jurists & Medical Pioneers*, *The Rexach Civil War Fracture*).
3. **Calibrate Contemporary Empathy & Living Oral Memory:** Write and maintain contemporary family chronicles and living oral histories under **SOP-GEN-002** and **SOP-GEN-005**—capturing formative transatlantic memories (such as altar serving and bilingual translating for visiting family clergy in Maryland) with warmth, dignity, and generational perspective.
4. **Maintain Narrative-to-Graph Integrity:** Ensure every person mentioned in a narrative links to an active, valid profile in `People/`.

## 2. Mandatory Curatorial Workflow
```mermaid
graph TD
    A["🔍 1. Ingest Archival Facts & Living Oral History (SOP-GEN-005)"] --> B["📜 2. Draft Multi-Generational Chronology"]
    B --> C["⚖️ 3. Apply Generational Span Bounds (ADR-GEN-012)"]
    C --> D["🌿 4. Calibrate Tone & Humble Intergenerational Voice (SOP-GEN-002)"]
    D --> E["🔗 5. Weave Bidirectional WikiLinks into People/"]
    E --> F["🧪 6. Run Automated Narrative Linter & Master Unit Tests"]
```

## 3. Guiding Rules & Principles
* **Living Oral Memory Integration (SOP-GEN-005):** Personal testimonies and authentic family memories (e.g. assisting Father Enrique Rexach during Maryland Masses) form primary qualitative provenance and must be woven seamlessly into the narrative tapestry.
* **Anti-Hagiography / Humble Framing:** Do not place any living individual in an exaggerated heroic role. Frame contemporary challenges through observational, generational wisdom.
* **Deep Lineage Integrity (SOP-GEN-001):** When connecting medieval or early modern figures (e.g. 13th-century knights) to 16th/17th-century descendants, always insert a generational transmission node to prevent chronological compression.
* **Interactive WikiLinks:** Every major figure mentioned must be hyperlinked with Obsidian ``WikiLink`` syntax pointing to their canonical note in `People/`.

## 4. Execution Tools
Run the narrative curation engine to audit and validate all narratives:
```bash
python3 _Meta/Scripts/narrative_curator_engine.py
```

