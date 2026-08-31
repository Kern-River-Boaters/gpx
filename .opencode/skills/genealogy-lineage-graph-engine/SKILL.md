---
name: "genealogy-lineage-graph-engine"
description: "genealogy-lineage-graph-engine skill for OpenCode"
---

# genealogy-lineage-graph-engine

> Parent Skill Definition: [genealogy-lineage-graph-engine](file:///home/jpino/Obsidian/Genealogy/_Meta/Skills/genealogy-lineage-graph-engine/SKILL.md)

---
name: genealogy-lineage-graph-engine
description: Governs the universal Bases-native dynamic family tree graph engine, dual-hemisphere radial fan charts, bidirectional lineage pointer symmetry, hemisphere typography rules, and global citizenship flag registries across Obsidian and Kern Publisher Web.
---

# 🌳 Genealogy Lineage Graph & Fan Chart Engine

## 1. Overview & Architectural Standards
This skill governs the generation, maintenance, and verification of dynamic family tree graphs and dual-hemisphere radial fan charts across the Genealogy vault and Kern Publisher Web.

### Key References:
- **ADR-016**: Bases-Native Dynamic N-Generation Genealogy Graph Architecture.
- **ADR-017**: Bidirectional Lineage Pointer Symmetry, Dual-Hemisphere Radial Lineage Visualizers, and Publisher Pre-Flight Test Harness.
- **ADR-019**: Generalized Lineage Path Tracing, In-Place Navigation, and Universal Accessibility Standard for Open-Source Family Tree Visualizers.
- **ADR-045**: High-Performance Publisher Architecture, In-Memory Vault Indexing, and Zero-Latency Client SPA Routing.
- **SOP-GEN-006**: Dynamic Family Tree Graph Governance and Record Provisioning.
- **Engine Implementation**: [[`_Meta/Scripts/genealogy_graph_engine.js`]] (Universal Base Engine) & [[`Common/_Meta/Scripts/kern_publisher.py`]] (FastAPI Publisher).

---

## 2. Mandatory Profile Structure

Every person profile created or enriched in `People/` MUST include the dynamic family tree code block immediately below `## 📌 Executive Summary`:

````markdown
## 🌳 Family Tree & Dynamic Lineage Graph

```family-tree
depth: 2
spouses: true
dates: true
direction: TD
```
````

### Supported Codeblock Options:
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `depth` | Integer (1–5) | `2` | Traversal depth for both ancestors and descendants. |
| `view` | String | `'fan'` | Default view mode: `'fan'` (radial fan chart), `'pedigree'` (compact bracket), or `'hourglass'` (mermaid flow). |
| `highlight` | String | `null` | Path trace: `'patrilineal'` (Y-DNA), `'matrilineal'` (mtDNA), target ancestor WikiLink, or property predicate (`'citizenship_anchor:true'`). |
| `palette` | String | `'classic'` | Color scheme: `'classic'`, `'viridis'` (colorblind-safe), `'contrast'`, or `'monochrome'`. |
| `print` | String | `'letter'` | Print/Export preset: `'letter'`, `'tabloid'`, or `'poster'`. |
| `spouses` | Boolean | `true` | Lateral marriage partners (`-.-|m.|`). |
| `dates` | Boolean | `true` | Display birth and death years. |
| `direction` | String | `'TD'` | Top-Down (`TD`) or Left-Right (`LR`). |

---

## 3. Universal Dual-Hemisphere Fan Chart Standard

All radial visualizers generate responsive SVG charts with:
- **Upper Hemisphere ($0^\circ \to 180^\circ$ - Ancestors)**: **Full Legal Names** across all ancestral rings (Parents, Grandparents, Great-Grandparents).
- **Lower Hemisphere ($180^\circ \to 360^\circ$ - Descendants)**: **Given Names Only** across all descendant rings (Children, Grandchildren, Great-Grandchildren), avoiding surname collisions in tight angular slices.
- **Compound Given Name Engine**: Validated whitelist (`luis`, `andres`, `ignacio`, `antonio`, `manuel`, `maria`, `ramon`, `luisa`, `isabel`, `esther`, `teresa`, `concepcion`, `carmen`, `pilar`, `elena`, `dolores`, `jose`, `belen`, `jude`, `carlos`, `pablo`, `francisco`) preserves authentic compound given names (*José Luis*, *María Luisa*, *Elena María*, *Alister Jude*) while accurately isolating and stripping surnames (*Gutiérrez*, *Jiménez*, *Pino*, *Rexach*).
- **Center Hub**: Subject displays full legal name, vital dates, legal citizenship flags, and spouse badges.

---

## 4. Strict Legal Citizenship Flag Registry

Flags represent strictly **legal nationality**, not physical location of residence:
1. **Priority 1 (Declared Legal Nationality)**: `citizenship_status` or `citizenship` takes absolute precedence (e.g. `spanish_citizen` $\to$ 🇪🇸, `us_citizen` $\to$ 🇺🇸, `canadian_citizen` $\to$ 🇨🇦, `peruvian_citizen` $\to$ 🇵🇪, `cuban_citizen` $\to$ 🇨🇺, `british` $\to$ 🇬🇧).
2. **Priority 2 (Birth Place Fallback)**: For historical ancestors without explicit citizenship tags, `birth_place` is matched against the declarative `COUNTRY_REGISTRY` covering 50 US states, Canadian provinces, Spanish provinces, UK counties, and over 40 global nations.
3. **Strict Exclusion**: `locations_lived`, career employment, and expat residences (e.g. living in Texas or Canada) are strictly excluded from conferring nationality flags.

---

## 5. Pre-Flight Quality Gate & Definition of Done

Before declaring completion of any lineage edits, profile creations, or publisher service changes:
1. **Pre-Flight Test Suite**:
   ```bash
   python3 [[test_kern_publisher.py]]
   ```
   *Must pass all 11 unit tests with 100% OK.*
2. **Vault DAG & Symmetry Sentinel**:
   ```bash
   python3 [[audit_and_enforce_source_links.py]]
   ```
   *Must report 0 orphaned sources, 0 missing tree blocks, and 100% bidirectional pointer symmetry.*
3. **Publisher Service Reload**:
   ```bash
   systemctl --user restart kern-publisher.service
   ```

