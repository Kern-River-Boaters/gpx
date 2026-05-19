# Complete Obsidian Map Plugin Research

## Tested Plugins

### 1. ✅ Obsidian Leaflet (Works - Current)
- **Repository**: valentine195/obsidian-leaflet-plugin
- **Downloads**: 100K+
- **Status**: Works with GeoJSON inline embedding
- **Issue**: "Show all markers" zooms to world view

### 2. ❌ Map View (Doesn't Work for Our Use Case)
- **Repository**: esm7/obsidian-map-view
- **Downloads**: 50K+
- **Status**: Separate pane only, not inline

## Other Known Map Plugins

### 3. Obsidian Overleaf (Map Overlay)
- **Use Case**: Overlays maps on notes
- **Type**: Not for embedded interactive maps
- **Verdict**: Not suitable

### 4. Obsidian Geo (Location Tagging)
- **Use Case**: Adds geolocation metadata
- **Type**: Not for map rendering
- **Verdict**: Not suitable

### 5. Custom iFrame Solutions

#### Option A: Leaflet.js in iFrame
Create custom HTML with Leaflet.js directly:
```html
<iframe srcdoc="<html>...</html>" width="100%" height="600px"></iframe>
```
**Pros**: Full control
**Cons**: Complex to maintain, doesn't work in mobile app

#### Option B: OpenStreetMap iFrame
Embed OSM directly:
```html
<iframe src="https://www.openstreetmap.org/export/embed.html?bbox=..." width="100%" height="600px"></iframe>
```
**Pros**: Simple, always works
**Cons**: Static bounds, no waypoint support

## Conclusion

**Obsidian Leaflet is THE standard** for embedded interactive maps in Obsidian. It's:
- Most mature (years of development)
- Most popular (100K+ downloads)
- Best documented
- Only viable option for inline GeoJSON rendering

**No better alternative exists** unless we build custom HTML/JavaScript solutions.

---

**Recommendation**: Enhance our current Leaflet setup with:
1. Multiple tile layer options (satellite, terrain, etc.)
2. Better documentation of workarounds
3. Accept "Show all markers" limitation

**Date**: 2026-05-19
