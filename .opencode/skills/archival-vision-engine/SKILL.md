---
name: "archival-vision-engine"
description: "archival-vision-engine skill for OpenCode"
---

# archival-vision-engine

> Parent Skill Definition: [archival-vision-engine](file:///home/jpino/Obsidian/Genealogy/_Meta/Skills/archival-vision-engine/SKILL.md)

---
name: archival-vision-engine
description: Governs macro-illumination normalization, faint cursive data rescue, 4-gate reasoning vision judge validation, Spencerian top-hat cursive loop clearance, and table lattice slicing across historical microfilms under ADR-020 and ADR-021.
---

# Archival Vision Engine (`archival-vision`)

Governs deterministic image restoration, paleographical transcription, table lattice slicing, and closed-loop visual quality gates for degraded 19th-century census schedules, parish registers, and civil microfilms under **ADR-020**, **ADR-021**, and **SOP-GEN-008**.

---

## 🏛️ 4-Gate Comparative Reasoning Architecture

```mermaid
graph TD
    classDef raw fill:#37474f,stroke:#263238,color:#fff;
    classDef gate fill:#1565c0,stroke:#0d47a1,color:#fff;
    classDef judge fill:#f57c00,stroke:#e65100,color:#fff;
    classDef pass fill:#2e7d32,stroke:#1b5e20,color:#fff;

    RAW["<b>Raw Archival Scan (Grayscale / BGR)</b>"]:::raw --> G0["<b>Gate 0: Macro-Illumination Normalization</b><br/>Massive Gaussian background blur (301x301)<br/>flat_img = img / bg_map (Equalizes shadows & rescues faint ink)"]:::gate
    
    G0 --> J0{"Vision Judge: Gate 0<br/><i>Shadows lifted? Faint cursive & tally marks rescued?</i>"}:::judge
    J0 -->|PASS| G1["<b>Gate 1: Hermes 1D Delimiter Check</b><br/>1D Projection Histograms (raw_x vs new_x)<br/>Natural Directional Line Morphology"]:::gate:::pass

    G1 --> J1{"Vision Judge: Gate 1<br/><i>Delimiter baseline met? Text unaffected?</i>"}:::judge
    J1 -->|PASS| G2["<b>Gate 2: Upscaling & Artifacts</b><br/>2x Super-Resolution + Unsharp Edge Enhancement"]:::gate:::pass

    G2 --> J2{"Vision Judge: Gate 2<br/><i>Checkerboards? Synthetic distortion?</i>"}:::judge
    J2 -->|PASS| G3["<b>Gate 3: Anti-Smear & Ink Integrity</b><br/>CLAHE Contrast Deepening (clip=2.0) + CC Dust Filter (Area < 12)<br/>Zero Stroke Bloating (ellipse_close=0) + Alpha Overlay"]:::gate:::pass

    G3 --> J3{"Vision Judge: Gate 3<br/><i>Natural fine stroke? Loops clear? Tails sharp?</i>"}:::judge
    J3 -->|PASS| SLICE["<b>Downstream Protection: Lattice Slicer</b><br/>Extract clean tabular cells and data rows"]:::pass
```

---

## 🔬 Core Architectural Principles

### 1. Gate 0: Macro-Illumination Normalization & Faint Data Rescue
* **Root Problem:** Underexposure shadows, optical vignetting, and fog fields trap faint historical cursive script and grid lines. Erasing or masking these dark zones destroys authentic data.
* **Mathematical Illumination Flattening:**
  1. **Background Illumination Field:** Massive Gaussian blur ($301\times 301$) models the macro-lighting gradient across the sheet.
  2. **Field Division:** `flat_img = cv2.divide(img, bg_map, scale=255)` lifts underexposed shadows into uniform planar brightness.
  3. **Data Rescue:** Automatically recovers faint cursive occupations (e.g. *"Fisherman"*), ditto marks, tally marks, and structural table delimiters previously hidden in shadows.

### 2. Gate 1: Hermes 1D Projection Peak Delimiter Check
* **Mathematical Constraint:** Extracts 1D projection peaks from raw scan (`raw_x_peaks`, `raw_y_peaks`) and ensures processed grid mask does not lose any table columns (`len(new_x_peaks) >= len(raw_x_peaks) - 1`).
* **Natural Line Isolation ($35\times 1$, $1\times 35$):** Isolates genuine column dividers across the sheet and renders an organic charcoal `#6E6964` (`[100, 105, 110]` BGR) RGBA overlay.

### 3. Gate 3: Anti-Smear & Exact Footprint Text Overlay
* **CLAHE Contrast Deepening (`clipLimit=2.0, tileGridSize=(8, 8)`):** Deepens ink naturally without expanding stroke boundaries.
* **Zero Stroke Expansion (`ellipse_close_size=0`):** Prohibits heavy morphological closing or dilation, preserving delicate Spencerian loops, open loops, and sharp tapering tails.
* **Connected Components Noise Filter (`min_area=12`):** Deletes isolated dust speckles without global blur.
* **Anti-Aliased Alpha Overlay:** Composited with fountain pen tone `[20, 20, 20]` at $80\%$ opacity.

### 4. Layer Stacking Order
1. Base Substrate (`cleaned_master`: bilateral denoised illumination-flattened parchment)
2. Natural Grid (Structural delimiters drawn in organic charcoal `#6E6964`)
3. Polished Ink (The CLAHE-enhanced cursive text and rescued faint data)

---

## 💻 CLI & Python Usage

```python
from archival_vision.goal_loop import run_multi_gate_goal_loop
from archival_vision.lattice import slice_document_cells
from archival_vision.transcribe import resolve_ledger_transcriptions
from archival_vision.checksum import validate_ledger_math

# 1. Execute Multi-Gate Goal Loop with Vision Judge
result = run_multi_gate_goal_loop(
    input_path="Sources/Microfilms/1861-Census-WestIsles-CharlotteNB-PatrickWhalinFamily-LAC-C1001-Master.jpg",
    output_path="Sources/Microfilms/1861-Census-WestIsles-CharlotteNB-PatrickWhalinFamily-LAC-C1001-Enhanced.jpg",
    skill_profile_path="~/.hermes/skills/historical_census_1861.json",
    use_llm_judge=True
)

# 2. Slice table cells with Ghost Cell protection
seg_res = slice_document_cells(
    img_path=result["output_path"],
    output_chips_dir="/tmp/archival_chips",
    drop_ghost_cells=True
)

# 3. Transcribe cells and resolve ditto marks
trans_res = resolve_ledger_transcriptions(seg_res.cells)

# 4. Validate arithmetic totals
math_res = validate_ledger_math(trans_res.structured_records)
```

---

## 🔬 Multi-Gate Verification JSON Schema

```json
{
  "artifact_neutralization": {
    "variance_detected": true,
    "mask_applied": true,
    "border_seam_visible": false,
    "occluded_region_is_pure_white": true
  },
  "segmentation_impact": {
    "false_columns_detected": false,
    "ghost_cells_dropped": true
  },
  "verdict": "PASS",
  "next_action": "initiate_htr_transcription"
}
```

