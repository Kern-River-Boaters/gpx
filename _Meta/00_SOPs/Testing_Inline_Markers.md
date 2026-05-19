# Testing Inline Markers vs. GeoJSON

## Background

We're testing two approaches for embedding GPX waypoints in Obsidian Leaflet maps:

### Approach 1: External GeoJSON (Current)
- **Script**: `_Meta/Scripts/refresh_gpx_maps.py`
- **Architecture**: GPX → GeoJSON file → Referenced in Leaflet
- **Files per river**: 3 (`.gpx`, `.json`, `.md`)
- **Pros**: 
  - Single source of truth (JSON file)
  - Cleaner markdown files
  - Easier to inspect/debug waypoint data
- **Cons**: 
  - Extra `.json` files to manage
  - "Show all markers" button broken (zooms to Ivory Coast)

### Approach 2: Inline Markers (Test)
- **Script**: `_Meta/Scripts/refresh_gpx_maps_inline.py`
- **Architecture**: GPX → Inline markers in Leaflet code block
- **Files per river**: 2 (`.gpx`, `.md`)
- **Pros**: 
  - Fewer files (no JSON)
  - "Show all markers" button works correctly
  - All data in one place
- **Cons**: 
  - Potential Android performance issues (historically reported)
  - Larger markdown files
  - Harder to inspect waypoint data

## Testing Protocol

### Step 1: Test on Desktop
1. Open `Kern/Lower Kern Rapids.md` in Obsidian (already converted to inline)
2. Verify map renders correctly
3. Test controls:
   - ✅ Pan (mouse drag)
   - ✅ Zoom (mouse wheel)
   - ✅ Reset zoom button
   - ✅ Show all markers button (should work now!)

### Step 2: Test on Android
**Critical tests** (this is where inline markers historically failed):

1. **Initial load time**
   - Open note with inline markers
   - Time how long map takes to render
   - Compare with GeoJSON version (e.g., `North Fork Kern Rapids.md`)

2. **Responsiveness**
   - Pan around map (single-finger drag)
   - Pinch to zoom in/out
   - Note any lag or stuttering

3. **Memory usage**
   - Open multiple inline-marker maps
   - Check if app becomes sluggish or crashes
   - Test with 40+ waypoints (Lower Kern Rapids has 41)

4. **Show all markers button**
   - Does it work correctly now?
   - Does it zoom to the river instead of Ivory Coast?

### Step 3: Compare Results

| Feature | GeoJSON (Current) | Inline Markers (Test) |
|---------|-------------------|----------------------|
| Desktop performance | ✅ Fast | ⏳ Test |
| Android performance | ✅ Fast | ⏳ Test |
| Show all markers | ❌ Broken | ⏳ Test |
| File count | 3 per river | 2 per river |
| Markdown size | Small (~1-2KB) | Medium (~4KB) |
| JSON size | Medium (~12KB) | N/A |

## Testing Commands

### Convert ONE file to inline markers (test):
```bash
cd /path/to/KRB
python _Meta/Scripts/refresh_gpx_maps_inline.py "Kern/Lower Kern Rapids.gpx"
```

### Revert to GeoJSON (if inline fails):
```bash
cd /path/to/KRB
# Force regeneration with GeoJSON
rm "Kern/Lower Kern Rapids.json"
python _Meta/Scripts/refresh_gpx_maps.py
```

### Convert ALL files to inline (if test succeeds):
```bash
cd /path/to/KRB
# Backup first!
git add -A && git commit -m "Backup before inline marker conversion"

# Convert all
for gpx in Kern/*.gpx "San Joaquin"/*.gpx "Rouge River"/*.gpx; do
  python _Meta/Scripts/refresh_gpx_maps_inline.py "$gpx"
done

# Remove JSON files
rm Kern/*.json "San Joaquin"/*.json "Rouge River"/*.json
```

## Decision Criteria

**Use inline markers IF**:
- ✅ Android performance is acceptable (no lag/crashes)
- ✅ "Show all markers" button working is important
- ✅ Fewer files outweighs larger markdown size

**Keep GeoJSON IF**:
- ❌ Android shows performance issues with 40+ inline markers
- ✅ Separation of concerns (data vs. presentation) is valuable
- ✅ Current architecture is working well

## Known Android Issues (Historical)

From user reports on Obsidian forums:
- Inline markers can cause severe lag on Android with 50+ waypoints
- Leaflet plugin may crash or freeze during pan/zoom
- Performance varies by Android device (older devices worse)
- GeoJSON typically performs better on mobile

**Our test**: Lower Kern Rapids has 41 waypoints - right at the threshold where issues might appear.

---

## ❌ Test Results - FAILED

**Date**: 2026-05-19  
**Status**: Inline markers approach **not viable**

### Issue: Leaflet Plugin Parsing Error

Inline markers fail to render (grey box) when combined with YAML comments in the code block.

**Root Cause**:
```leaflet
# --- CENTERING ---    ← These comments cause parsing errors
marker:
  - [lat, lon, "name"]
```

The Obsidian Leaflet plugin v6.0.5 doesn't support YAML-style comments (`#`) when using inline `marker:` arrays. Comments work fine with `geojson:` references, but break with inline markers.

**Attempted Fix**: Removing all comments makes the inline markers work, but loses documentation value for debugging.

**Workaround Tested**: None - would need to sacrifice code readability.

### Conclusion

**Sticking with GeoJSON approach** because:
- ✅ Works reliably on desktop and mobile
- ✅ Supports comments for maintainability
- ✅ Better separation of data (JSON) and presentation (MD)
- ✅ Easier to debug waypoint coordinates
- ❌ "Show all markers" button broken (acceptable tradeoff)

**Inline markers rejected** because:
- ❌ Breaks rendering when comments present
- ❌ Removing comments hurts maintainability
- ❌ No clear advantage over GeoJSON
- ❌ Historical Android performance concerns

---

**Final Decision**: Keep current GeoJSON architecture  
**Test File**: Reverted to GeoJSON (`Kern/Lower Kern Rapids.md`)
