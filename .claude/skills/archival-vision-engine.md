# archival-vision-engine

> Parent Skill Definition: [archival-vision-engine](file:///home/jpino/Obsidian/Genealogy/_Meta/Skills/archival-vision-engine/SKILL.md)

---
name: archival-vision-engine
description: Governs edge-preserving bilateral background normalization, global gamma contrast restoration, reel statefulness, blank-frame fast-failing, 4-gate deterministic DIEM verification, Spencerian top-hat cursive loop clearance, and table lattice slicing across historical microfilms under ADR-020, ADR-021, and SOP-GEN-008.
---

# Archival Vision Engine (`archival-vision`)

Governs deterministic image restoration, paleographical transcription, table lattice slicing, and closed-loop visual quality gates for degraded 19th-century census schedules, parish registers, and civil microfilms under **ADR-020**, **ADR-021**, and **SOP-GEN-008**.

---

## 🏛️ Golden Master 4-Gate Reasoning Architecture

```mermaid
graph TD
    classDef raw fill:#37474f,stroke:#263238,color:#fff;
    classDef check fill:#f57c00,stroke:#e65100,color:#fff;
    classDef gate fill:#1565c0,stroke:#0d47a1,color:#fff;
    classDef pass fill:#2e7d32,stroke:#1b5e20,color:#fff;
    classDef out fill:#4a148c,stroke:#311b92,color:#fff;

    RAW["<b>Raw Archival Scan (LAC / PANB Microfilm)</b>"]:::raw --> FF{"<b>Step 0: Fast-Fail Check</b><br/>check_blank_frame (<5ms)"}:::check
    
    FF -->|Blank Target| SKIP["<b>Fast-Exit: SKIPPED_BLANK_PAGE</b>"]:::check
    FF -->|Valid Ledger| G0["<b>Gate 0: Edge-Preserving Background Normalization</b><br/>• 25% Downsample<br/>• Heavy Bilateral Filter (d=15, &sigma;=75)<br/>• Continuous Division: raw / bg_map * 255<br/>• Global Gamma Shift (&gamma;=0.85)"]:::gate

    G0 --> J0{"<b>Gate 0 Checkpoint</b><br/><i>Substrate Variance &le; 150.0?<br/>Embossed halos eradicated?</i>"}:::check
    J0 -->|PASS| G1["<b>Gate 1: Natural Delimiter & Lattice Intersections</b><br/>• 35x1 / 1x35 Line Extraction + Bridging<br/>• Intersections = h_lines &and; v_lines &ge; min_cells<br/>• X-Projection Peaks &ge; baseline_columns"]:::gate:::pass

    G1 --> J1{"<b>Gate 1 Checkpoint</b><br/><i>Lattice density met? Columns preserved?</i>"}:::check
    J1 -->|PASS| G2["<b>Gate 2: Super-Resolution Upscaling</b><br/>• 2x Lanczos-4 Super-Resolution<br/>• Smooth anti-aliased interpolation"]:::gate:::pass

    G2 --> J2{"<b>Gate 2 Checkpoint</b><br/><i>Variance ratio &isin; [0.5, 3.5]?</i>"}:::check
    J2 -->|PASS| G3["<b>Gate 3: Anti-Smear & Ink Health (DIEM-v2)</b><br/>• Top-Hat Loop Clearance (9x9, strength=0.6)<br/>• FPD &le; 15% (No black blobs)<br/>• Median Comp Area &le; 350px (No stroke fusing)<br/>• Continuity &gt; 80% | Noise &lt; 4%"]:::gate:::pass

    G3 --> J3{"<b>Gate 3 Checkpoint</b><br/><i>DIEM Score = 100%?</i>"}:::check
    J3 -->|PASS| OUT["<b>2x Certified Golden Master Facsimile</b><br/>(4902 x 4096 px)"]:::out
    OUT --> MEM["<b>Persistent Skill Memory</b><br/>~/.hermes/skills/historical_census_1861.json"]:::out
    OUT --> SLICE["<b>Downstream Table Slicing & HTR</b><br/>Lattice Slicer &rarr; Transcribe &rarr; Math Checksum"]:::pass
```

---

## 🔬 Core Architectural Principles

### 1. Reel Statefulness & Warm-Start Baseline Caching
* **Reel Drift Protection**: Lighting and contrast drift slowly across sequential microfilm frames. When processing a reel (e.g. LAC C-1001), `ReelContext` inherits winning parameters from the preceding frame, triggering the full optimization search loop only when DIEM scores drop below baseline thresholds.
* **Blank Frame Fast-Fail**: Target cards, spacer frames, and black leader segments are identified in $<5\text{ms}$ via `check_blank_frame`, bypassing heavy filters immediately.

### 2. Gate 0: Edge-Preserving Bilateral Background Normalization & Global Gamma Shift
* **Root Problem**: Massive Gaussian blurring across hard tape splices or binding shadows creates a sloped gradient, causing severe edge-ringing (embossed halos) and highlight blowout during division.
* **Edge-Preserving Formulation**:
  1. **Downsample**: Scale working copy to $25\%$ for sub-$15\text{ms}$ processing.
  2. **Bilateral Estimation Map**: Apply `cv2.bilateralFilter(small_gray, d=15, sigmaColor=75.0, sigmaSpace=75.0)` to smooth substrate texture while strictly preserving the sharp geometric step-edges of tape splices and shadow borders.
  3. **Linear Upsampling**: Interpolate back to full resolution using `INTER_LINEAR` (preventing cubic overshoot and ringing).
  4. **Constrained Division**: $\text{flat\_raw} = \frac{\text{raw\_gray}}{\text{bg\_map}} \times 255$.
  5. **Global Gamma Shift ($\gamma=0.85$)**: Corrects highlight blowout and deepens faint cursive entries, ditto marks, and column dividers across the whole canvas.

### 3. Gate 1: Delimiter Lattice & Intersection Density Gate
* **Deterministic Line Intersection Formula**:
  $$\text{Intersections} = \text{h\_lines} \land \text{v\_lines}$$
* **Mathematical Constraints**:
  1. $\text{Intersection Centroids} \ge \text{min\_expected\_intersections}$
  2. $\text{len}(X\text{-peaks}) \ge \text{baseline\_columns}$
* **Organic Charcoal Overlay**: Rendered with `#6E6964` (`[100, 105, 110]` BGR) at $65\%$ opacity with $3\times 3$ Gaussian blur to match historical optical focus.

### 4. Gate 3: Ink Health, Top-Hat Loop Clearance & Anti-Bloat Standard
* **Spencerian Top-Hat Clearing**: Morphological white top-hat filter (`kernel_size=(9, 9)`, `strength=0.6`) clears bleed-through ink trapped inside tight cursive loops ('e', 'o', 'a', 'g') without severing thin pen strokes.
* **Foreground Pixel Density (FPD $\le 15.0\%$)**: Rejects over-binarized blobs and blotches.
* **Component Area Bloat ($\text{Median Area} \le 350\text{px}$)**: Prevents cursive pen strokes from fusing into solid blocks.
* **Hard Circuit Breaker**: Auto-tunes `sauvola_k`, `min_component_area`, and `text_opacity` autonomously upon DIEM violation.

---

## 💻 CLI & Python Usage

```python
from archival_vision.goal_loop import run_multi_gate_goal_loop
from archival_vision.lattice import slice_document_cells
from archival_vision.transcribe import resolve_ledger_transcriptions
from archival_vision.checksum import validate_ledger_math

# 1. Execute Multi-Gate Goal Loop with Edge-Preserving Normalization
result = run_multi_gate_goal_loop(
    input_path="Sources/Microfilms/1861-Census-WestIsles-CharlotteNB-PatrickWhalinFamily-LAC-C1001-Master.jpg",
    output_path="Sources/Microfilms/1861-Census-WestIsles-CharlotteNB-PatrickWhalinFamily-LAC-C1001-Enhanced.jpg",
    skill_profile_path="~/.hermes/skills/historical_census_1861.json",
    use_llm_judge=False
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

## 🔬 Multi-Gate Verification DIEM Scorecard Baseline

```json
{
  "dataset": "1861-Census-WestIsles-CharlotteNB-PatrickWhalinFamily-LAC-C1001-Master",
  "diem_scorecard": {
    "human_readability": 99.83,
    "machine_readability": 100.0,
    "mean_luminance": 236.35,
    "contrast_std": 54.81,
    "laplacian_variance": 3753.79,
    "stroke_continuity_index": 88.35,
    "background_noise_ratio": 1.32,
    "faint_ink_density": 2.51,
    "substrate_variance": 123.51,
    "foreground_pixel_density": 8.0,
    "median_component_area": 93.0
  },
  "winning_parameters": {
    "downsample_scale": 0.25,
    "bg_bilateral_d": 15,
    "bg_bilateral_sigma_color": 75.0,
    "bg_bilateral_sigma_space": 75.0,
    "morph_close_ksize": [5, 5],
    "global_gamma": 0.85,
    "h_kernel_len": 25,
    "v_kernel_len": 135,
    "h_bridge_len": 400,
    "upscale_factor": 2,
    "tophat_kernel_size": [9, 9],
    "text_opacity": 0.75,
    "clahe_clip_limit": 2.0,
    "sauvola_k": 0.12,
    "min_component_area": 12,
    "bilateral_sigma": 25.0,
    "header_gamma": 0.75,
    "grid_color_bgr": [100, 105, 110],
    "grid_opacity": 0.65
  }
}
```

