---
name: "archival-vision-engine"
description: "archival-vision-engine skill for OpenCode"
---

# archival-vision-engine

> Parent Skill Definition: [archival-vision-engine](file:///home/jpino/Obsidian/Genealogy/_Meta/Skills/archival-vision-engine/SKILL.md)

---
name: archival-vision-engine
description: Governs decoupled document restoration, synthetic occlusion neutralization, 4-gate reasoning vision judge validation, Spencerian top-hat cursive loop clearance, and ghost-cell dropping table lattice slicing across historical microfilms under ADR-020 and ADR-021.
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

    RAW["<b>Raw Archival Scan (Grayscale / BGR)</b>"]:::raw --> G0["<b>Gate 0: Occlusion Neutralization</b><br/>Gaussian absdiff variance map (&lt;6) + inRange(165,220)<br/>MORPH_OPEN (25x25) + Dilate (open_k + 2*dilate_px) -> 255 White"]:::gate
    
    G0 --> J0{"Vision Judge: Gate 0<br/><i>Grey block erased? Seam invisible?</i>"}:::judge
    J0 -->|PASS| G1["<b>Gate 1: Grid & Segmentation</b><br/>Directional Line Kernels (35x1, 1x35) + 1x25 Line Healing"]:::gate:::pass

    G1 --> J1{"Vision Judge: Gate 1<br/><i>Masking text? Continuous lines?</i>"}:::judge
    J1 -->|PASS| G2["<b>Gate 2: Upscaling & Artifacts</b><br/>2x Super-Resolution + Unsharp Edge Enhancement"]:::gate:::pass

    G2 --> J2{"Vision Judge: Gate 2<br/><i>Checkerboards? Synthetic distortion?</i>"}:::judge
    J2 -->|PASS| G3["<b>Gate 3: Top-Hat Ink Integrity</b><br/>RETR_CCOMP Cavity Detection + Bottom-Hat (9x9)"]:::gate:::pass

    G3 --> J3{"Vision Judge: Gate 3<br/><i>Trapped ink cleared? Strokes connected?</i>"}:::judge
    J3 -->|PASS| SLICE["<b>Downstream Protection: Lattice Slicer</b><br/>Drop zero-variance pure white ghost cells"]:::pass
```

---

## 🔬 Core Architectural Principles

### 1. Gate 0: Synthetic Microfilm Occlusion Neutralization
* **Root Problem:** Synthetic grey scanning blocks/tape trap JPEG compression noise that layout segmenters misinterpret as columns and OCR models hallucinate into ghost text.
* **Mathematical Isolation:**
  1. **Variance Map:** $21 \times 21$ Gaussian blur + `cv2.absdiff` targets zero-texture flatness ($\text{Variance} < 6$).
  2. **Intensity Intersection:** `cv2.inRange(gray, 165, 220)` avoids touching clean white paper.
  3. **Macro-Geometry Filter:** `cv2.MORPH_OPEN` with $25 \times 25$ rectangular kernel drops out natural paper smudges.
  4. **Seam-Swallowing Infill:** Dilation kernel $(k_w + 2\cdot\text{dilate\_px}, k_h + 2\cdot\text{dilate\_px})$ completely swallows the dark boundary seam, overwriting the entire region with pure white ($255$).

### 2. Gate 1 & 2: Structural Grid & 2x Super-Resolution
* **Tall Line Healing ($1 \times 25$):** Reconstructs fragmented column dividers across degraded ledger pages without thickening cursive text strokes.
* **Zonal Header Gamma Boost ($\gamma = 0.75$):** Elevates faded metadata script in the top 12% bounding box.
* **Lanczos + Unsharp Sharpening ($2\times$):** Generates $4902 \times 4096\text{ px}$ delivery assets with anti-aliased edge crispness.

### 3. Gate 3: Morphological Top-Hat Loop Clearance
* **Hierarchical Contour Cavity Isolation (`cv2.RETR_CCOMP`):** Discovers enclosed internal cavities inside Spencerian loops (`e`, `a`, `o`, `d`, `b`, `g`) and brightens trapped bleed-through noise to median background luminance without altering outer stroke trajectories.
* **Bottom-Hat Attenuation:** Clears residual noise in semi-open cursive loops.

### 4. Downstream Layout Segmentation & Ghost Cell Protection (`lattice.py`)
* **Ghost Cell Dropping:** Drops inferred cell bounding boxes where internal variance is near-zero ($\text{Variance} < 0.1$, $\text{Mean} \ge 254.0$), eliminating false OCR processing on neutralized occlusion voids.

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

