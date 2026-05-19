# Map View Plugin - GeoJSON Support Test

## Discovery
Map View plugin has a setting: `"handleGeoJsonCodeBlocks": true` (line 158 in data.json)

This suggests it CAN render GeoJSON code blocks, not just single frontmatter locations!

## Test Syntax

Map View might support this syntax:

````markdown
```geojson
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [-118.556407, 35.577993]
      },
      "properties": {
        "name": "White Maiden's (4)"
      }
    }
  ]
}
```
````

## Test Plan

1. Create a test note with inline GeoJSON code block
2. See if Map View renders it inline or in separate pane
3. Compare with Leaflet rendering
4. Test on Android

## Quick Test

Let's test with Lower Kern Rapids:

### Option A: Inline GeoJSON Code Block
Embed the JSON directly in a ```geojson block instead of referencing external file.

### Option B: Reference External GeoJSON
Check if Map View can reference `[[Lower Kern Rapids.json]]` somehow.

## Questions
1. Does Map View render GeoJSON inline in the note?
2. Or does it only show in the separate Map View pane?
3. Can it handle 40+ waypoints performantly?
4. Does it work on Android?

---

**Status**: 🧪 Needs testing  
**Date**: 2026-05-19
