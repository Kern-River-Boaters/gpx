# System Instructions for Claude / AI Coding Assistants

Welcome to the **River Boater GPX Collections for Garmin Instinct** development workspace. When assisting with maintenance, refactoring, or feature additions in this repository, you must adhere strictly to the constraints, architectural decisions, and hardware-specific requirements outlined below.

---

## 1. Core Project Philosophy & Backstory
This repository exists to bridge the gap between technical, high-speed whitewater kayaking and physical navigation limitations. Rafters on multi-day expeditions can freely consult physical guidebooks (like RiverMaps) to scan upcoming rapids and check beta. Kayakers need their hands on paddles and eyes on the river.

This tool solves that problem by formatting raw GPX data into glanceable, high-contrast wrist beta optimized for the **Garmin Instinct** series (Instinct 1, 2, 2X, 3). It converts long, truncated descriptive tags into a dense, 15-character identifier that explicitly provides the rapid name and its classification rating.

---

## 2. Technical Code Guidelines

### `parseRiverMaps.py` (Garmin Instinct Formatting)

#### Data Purpose & Local Execution
* **Strict Separation of Data & Tools:** We **do not host or redistribute** proprietary or copyrighted data belonging to commercial publishers (e.g., RiverMaps). The script is purely a local utility for end-users to format files they have legally obtained themselves.
* **Personal Use Configuration:** Because this tool is executed locally for personal device synchronization, there is no technical requirement to strip or scrub description metadata (`waypoint.description`) or original data during the parsing process. Users may fully preserve text fields for their own devices.

#### Naming Logic, Beta Extraction & Space-Stripping
* **Prefix Markers:** The original RiverMaps GPX data uses 2-character category markers at the front of waypoint names (`R-`, `C-`, `P-`, `M-`). The script **must completely slice off** this two-character prefix (`waypoint.name[2:]`) to save screen space.
* **Beta Extraction:** For Rapids (`R-`), parse the `waypoint.description` field using a strict regex pattern `r"(\(\w*)([0-9]+)(\w*\))"` to find the numerical classification rating. This becomes the `suffix` (appended with no spaces).
* **Smart Abbreviation (PascalCase & Vowel Stripping):** To enforce the 15-character hardware limit without losing readability, the script uses aggressive space-saving techniques:
  1. Capitalize each word and remove all spaces (e.g., `Lava Falls Rapid` -> `LavaFallsRapid`).
  2. Calculate available space: `15 - len(suffix)`.
  3. If the base name exceeds this space, strip vowels (`[aeiouAEIOU]`), but **always preserve the first letter** of the name.
  4. If still too long, apply a hard truncate to the remaining characters.
  5. Append the `suffix`.
  * *Example Output Tracing:* `R-Granite Gorge Rapid` with `(Class 5)` -> `GraniteGorgeRapid` is too long (17 chars). Vowels stripped (except first letter) -> `GrntGrgRpd`. Append suffix -> **`GrntGrgRpd5`**.

### `refresh_gpx_maps.py` (Obsidian Leaflet Maps)

#### Architecture Decisions
* **Single-File Design:** Each river has ONE markdown file with embedded maps. No separate `(Map).md` files.
* **Auto-Generated Block Protection:** Maps are enclosed in HTML comment markers (`<!-- BEGIN AUTO-GENERATED MAP -->` / `<!-- END AUTO-GENERATED MAP -->`). Script regenerates only this block, preserving user notes above/below.
* **Dual Map Strategy:** Each file contains BOTH street (OpenStreetMap) and satellite (Esri World Imagery) maps. No layer toggle UI exists in Leaflet plugin—users scroll to their preferred view.
* **GeoJSON External Files:** Waypoints stored as separate `.json` files, referenced via `geojson: [[filename.json]]` parameter. This avoids inline marker parsing issues with HTML comments.

#### Map Configuration Requirements
* **Bounding Box:** Always calculate from waypoint coordinates with `BBOX_BUFFER = 0.003` (approximately 300m padding) for tight viewport fit.
* **Touch Controls (Android):** Always include explicit touch parameters:
  ```yaml
  dragging: true
  gestureHandling: false
  scrollWheelZoom: true
  touchZoom: true
  doubleClickZoom: true
  ```
* **Zoom Levels:** `minZoom: 5`, `maxZoom: 20`, with calculated default zoom 11-15 based on bounding box size.
* **Show All Markers:** Set `showAllMarkers: false` (button doesn't work with GeoJSON-only maps, zooms to 0,0).

#### Known Limitations (Documented)
* **Android Touch Controls:** Obsidian mobile gesture handlers conflict with Leaflet. Workaround: Restart Obsidian app before viewing maps. See `_Meta/00_SOPs/Android_Touch_Controls_Known_Issues.md`.
* **No Layer Toggle UI:** Leaflet plugin doesn't support `baseMaps` or layer control buttons. Solution: Generate both street and satellite maps in same file.
* **Inline Markers Break with Comments:** Cannot mix `marker:` arrays with HTML comment markers—causes grey box rendering failure. Must use external GeoJSON files.

---

## 3. Strict Hardware & Ecosystem Constraints

### Garmin Instinct Limitations

#### The 15-Character Constraint
* Garmin Instinct watches aggressively truncate text inside active navigation menus, map data fields, and the signature circular secondary window. 
* Final waypoint names generated by any parsing mechanism **must remain strictly <= 15 characters**. The script achieves this via the dynamic space-and-vowel-stripping logic outlined above.

#### The 99-Waypoint Sync Threshold
* The Garmin Explore ecosystem marks any collection exceeding 100 items as a "large collection" and frequently fails to sync.
* The processing class enforces a split threshold at exactly **99 waypoints**. Ensure waypoint arrays are populated *before* evaluating if the file is full to prevent off-by-one errors.

#### GPX Schema & Icon Incompatibility
* The standard GPX `<sym>` tag does not natively map to Garmin's proprietary high-visibility Instinct icons during automated synchronization.
* **Do not hardcode custom symbols inside the GPX XML.** Users are explicitly instructed to import files into Garmin Explore as isolated collections and bulk-assign icons manually.

### Obsidian Leaflet Plugin Constraints
* **No Layer Control:** Plugin does not support `baseMaps` array, `image` parameter for layer switching, or `layers` array. Confirmed via testing in `_Meta/Tests/Test_LayerControl.md`.
* **Tile Server Format:** Use single string, not array: `tileServer: https://server.arcgisonline.com/.../tile/{z}/{y}/{x}` (note `{z}/{y}/{x}` not `{{z}}/{{y}}/{{x}}`).
* **GeoJSON Only for Protected Content:** Inline `marker:` arrays cannot coexist with HTML comment markers. See `_Meta/00_SOPs/Testing_Inline_Markers.md` for failure documentation.

---

## 4. Documentation Continuity

### README.md
* **Local Linking Conventions:** Always use clean, local relative links (e.g., `[LICENSE](LICENSE)`, `[Setup Guide](_Meta/00_SOPs/Setup_Guide.md)`).
* **Curated Datasets:** The repository directly hosts curated, cleared-for-redistribution GPX libraries for rivers not covered by commercial guidebooks (e.g., the **Kern**). Keep this independent of the script instructions.
* **Safety & Disclaimers:** Every refactor must preserve the prominent liability shield, canyon GPS signal interference warnings, and the safety notice indicating that whitewater boating is inherently hazardous.
* **Repository Structure:** Keep the directory tree diagram up-to-date when files/folders are added or moved.

### LICENSE
* Dual-purpose: Copyright protection for curated data + liability disclaimers for whitewater hazards and GPS accuracy in canyons.
* **Never modify safety warnings or liability shields** without explicit user approval.

### _Meta/00_SOPs/ (Standard Operating Procedures)
* **Purpose:** Document plugin limitations, workarounds, testing results, and setup instructions for future maintainers.
* **When to Add:** After discovering plugin behavior that contradicts documentation, testing workarounds, or resolving mobile rendering issues.
* **Current Files:**
  - `Setup_Guide.md` - Plugin installation and mobile configuration
  - `Android_Touch_Controls_Known_Issues.md` - Touch gesture workarounds with test results
  - `Testing_Inline_Markers.md` - Why inline markers + comments don't work
  - `Alternative_Map_View_Plugin.md` - Why Map View plugin isn't suitable
  - `Tagging_Strategy.md` - Hierarchical tag system for river metadata

### _Meta/Tests/
* **Purpose:** Reproducible test cases for plugin behavior verification.
* **Format:** Self-contained markdown files with multiple test configurations and results documented inline.
* **Current Files:**
  - `Test_LayerControl.md` - Layer switching syntax tests (all failed)
  - `Test_MapView.md` - Map View plugin capability tests
  - `Test_TileLayers.md` - Tile server compatibility tests (OSM, Esri, OpenTopo)

---

## 5. Python Script Development Guidelines

### Code Style
* **Docstrings:** Top-level module docstring with design goals, dependencies, and usage examples.
* **Configuration Section:** Group all constants at top (file extensions, markers, buffer values, zoom levels).
* **Type Hints:** Use for function signatures when beneficial for maintainability.
* **Error Handling:** Graceful degradation—log warnings but don't crash on missing files or malformed GPX.

### Dependencies
* **Minimal & Documented:** Only add dependencies that solve real problems. Document in `requirements.txt` with version constraints and purpose comments.
* **Current Stack:** `gpxpy` (GPX parsing), `geojson` (GeoJSON generation). No other dependencies needed.

### File Naming Conventions
* **Scripts:** Lowercase with underscores: `refresh_gpx_maps.py`, `add_tags_to_markdown.py`
* **Data Files:** Match GPX source name: `Lower Kern Rapids.gpx` → `Lower Kern Rapids.json` + `Lower Kern Rapids.md`
* **Test Files:** Prefix with `Test_`, PascalCase: `Test_LayerControl.md`

---

## 6. Git Workflow & Commit Messages

### Commit Message Format
* **Single-line summary:** Start with verb (Add, Fix, Update, Remove, Document), max 72 chars
* **Body (optional):** Separate with blank line, explain WHY not WHAT, use bullet points for multi-part changes
* **Footer (optional):** Reference issues, breaking changes, testing notes
* **Never include:** `Co-Authored-By: Claude` or similar AI co-authorship lines (user explicitly requested removal)

### Example Good Commit
```
Fix Android mobile zoom and tighten bounding box

- Reduced BBOX_BUFFER from 0.01° to 0.003° (300m vs 1km padding)
- Added explicit touchZoom: true for Android gesture support
- Increased default zoom levels by 1-2 across all ranges

Tested on Android Obsidian app - pinch zoom now works reliably.
```

### Branch Strategy
* **Main Branch:** `master` (this repository uses `master`, not `main`)
* **Remote:** `origin` = `git@github.com:Kern-River-Boaters/gpx.git`
* **Force Push Policy:** Only when rewriting history for commit message cleanup or squashing experimental work. Always warn user before force pushing.

---

## 7. Future Refactoring Guidance

### When Adding New Rivers
1. Create subdirectory: `River Name/`
2. Add source GPX files
3. Run `python _Meta/Scripts/refresh_gpx_maps.py`
4. Add hierarchical tags to generated markdown (see `_Meta/00_SOPs/Tagging_Strategy.md`)
5. Test on mobile before committing

### When Modifying Map Generation
1. **Test on actual devices** (Windows desktop + Android mobile minimum)
2. **Document limitations** in `_Meta/00_SOPs/` if workarounds needed
3. **Preserve auto-generated block markers** - don't change HTML comment syntax
4. **Update CLAUDE.md** with new constraints or configuration requirements

### When Plugin Behavior Changes
1. Create test file in `_Meta/Tests/` with multiple syntax variations
2. Document results inline (which tests passed/failed)
3. Update relevant SOP with findings
4. Update `CLAUDE.md` if architectural decisions change

### Don't Do This
* ❌ Add dependencies without updating `requirements.txt` and documenting purpose
* ❌ Create separate `(Map).md` files (single-file architecture is intentional)
* ❌ Try to implement layer toggle UI (plugin doesn't support it, tested exhaustively)
* ❌ Use inline `marker:` arrays with auto-generated blocks (parsing fails with HTML comments)
* ❌ Modify LICENSE safety warnings without explicit user approval
* ❌ Add `Co-Authored-By: Claude` or similar lines to commits

---

## 8. Key Architectural Trade-offs (Don't Revisit Without User Input)

These decisions were made after extensive testing and user feedback. Don't propose alternatives without strong justification:

1. **Dual maps instead of layer toggle:** Plugin doesn't support layer control UI. Users prefer scrolling between two maps over not having satellite option.
2. **GeoJSON external files instead of inline markers:** Inline markers break when used with HTML comment protection markers. GeoJSON is more robust.
3. **Single-file architecture:** Users want notes and maps together. Separate `(Map).md` files were confusing and harder to maintain.
4. **Tight bounding box (300m buffer):** User feedback: 1km buffer was too loose, made maps less useful for whitewater navigation.
5. **Disable "Show all markers" button:** Button doesn't work with GeoJSON-only maps (zooms to 0,0). Better to hide broken feature than leave it.
6. **Document Android touch issues instead of "fixing":** Issue is in Obsidian's mobile gesture handlers, not our code. Restart workaround is reliable.

---

## 9. Testing Checklist for Map Changes

Before committing changes to map generation or configuration:

- [ ] Maps render on Windows desktop Obsidian
- [ ] Maps render on Android mobile Obsidian (test after app restart)
- [ ] Waypoints appear at correct locations
- [ ] Bounding box centers on waypoints (not world map)
- [ ] Touch zoom works on mobile (two-finger pinch)
- [ ] Dragging works on mobile (one-finger pan)
- [ ] Reset zoom button returns to proper bounding box
- [ ] Both street and satellite maps functional
- [ ] Auto-generated block preserved after re-running script
- [ ] User notes above/below auto-generated block untouched

---

## 10. Quick Reference: Common Tasks

### Regenerate all maps after GPX changes
```bash
python _Meta/Scripts/refresh_gpx_maps.py
```

### Add new river with maps
```bash
mkdir "River Name"
# Add GPX files to River Name/
python _Meta/Scripts/refresh_gpx_maps.py
# Add tags using _Meta/Scripts/add_tags_to_markdown.py
```

### Test Leaflet plugin behavior
1. Create test file in `_Meta/Tests/Test_NewFeature.md`
2. Add multiple test cases with different syntax
3. Document results inline
4. Update relevant SOP if limitation found

### Clean up experimental test files
Move to `_Meta/Tests/` instead of deleting (preserves test history for future reference)

---

## 11. Resources for Future Maintainers

* **Leaflet Plugin Docs:** https://github.com/javalent/obsidian-leaflet (community plugin)
* **Obsidian Mobile Gesture Issues:** `_Meta/00_SOPs/Android_Touch_Controls_Known_Issues.md` (with forum/Reddit links)
* **Garmin Instinct Constraints:** RiverMaps GPX processing script header comments in `RiverMaps/parseRiverMaps.py`
* **GeoJSON Spec:** https://geojson.org/ (coordinate order: [longitude, latitude])
* **Tile Servers:** Esri World Imagery (satellite), CartoDB Voyager (street) - both tested and working

---

**Last Updated:** 2026-05-19
