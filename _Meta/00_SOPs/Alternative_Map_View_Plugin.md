# Alternative: Map View Plugin

## Background

You have **two** map plugins installed:
1. **Leaflet** (obsidian-leaflet-plugin) - Currently used
2. **Map View** (obsidian-map-view) - Alternative option

## Comparison

### Leaflet Plugin (Current)
**Repository**: [valentine195/obsidian-leaflet-plugin](https://github.com/valentine195/obsidian-leaflet-plugin)  
**Version**: 6.0.5

**Pros**:
- ✅ Embeds maps directly in notes (inline)
- ✅ Works with GeoJSON files
- ✅ Highly customizable (bounds, controls, styling)
- ✅ Good mobile performance with GeoJSON
- ✅ Code block syntax (portable across notes)

**Cons**:
- ❌ "Show all markers" button broken with GeoJSON-only maps
- ❌ Can't mix inline markers + GeoJSON without breaking
- ❌ Comments break inline marker syntax

### Map View Plugin (Alternative)
**Repository**: [esm7/obsidian-map-view](https://github.com/esm7/obsidian-map-view)  
**Version**: 6.1.4

**How it works**:
- Uses frontmatter properties instead of code blocks
- Opens maps in a separate view pane (like graph view)
- Can display multiple notes with location data on one map

**Example frontmatter**:
```yaml
---
location: [35.530509, -118.658560]
---
```

**Pros**:
- ✅ Simpler syntax (frontmatter only)
- ✅ Can aggregate multiple notes on one map
- ✅ Good for vault-wide geographic visualization
- ✅ Mobile-friendly

**Cons**:
- ❌ Doesn't embed maps inline in notes
- ❌ Opens in separate pane (not inline viewing)
- ❌ Designed for single locations per note (not 40+ waypoints)
- ❌ Not ideal for our use case (river sections with many waypoints)

## Conclusion

**Map View is NOT suitable** for our use case because:
1. It's designed for notes with ONE location each (e.g., travel journal, meeting places)
2. We need to display 40+ waypoints per river section
3. We want inline embedded maps, not a separate view pane
4. Our GeoJSON architecture works well for bulk waypoint data

**Stick with Leaflet plugin** and accept the "Show all markers" button limitation.

## Other Map Plugins to Consider

If Leaflet continues to have issues, here are alternatives:

### 1. Mapbox (Custom iframe)
- Use Mapbox GL JS or Leaflet.js in an iframe
- Full control over rendering
- Requires API key (free tier available)
- More complex setup

### 2. Custom Web Component
- Build a custom web component for Obsidian
- Use Leaflet.js directly
- Full control, but requires development

### 3. Static Map Images
- Generate static map images from GPX
- Embed as images in markdown
- No interactivity, but always works
- Good fallback for mobile if performance issues

## Test: Map View with Single Location

If you want to test Map View for comparison, add this to a note's frontmatter:

```yaml
---
location: [35.530509, -118.658560]
mapZoom: 12
---
```

Then open Command Palette (Ctrl+P) → "Map View: Open map view"

The note will appear as a pin on the map. But this only shows ONE location per note, not our 40+ waypoints.

---

**Recommendation**: Continue with Leaflet + GeoJSON architecture. The "Show all markers" button issue is acceptable since:
1. "Reset zoom" button works correctly
2. Initial view is already centered properly
3. No better alternative for inline maps with bulk waypoints
4. Android performance is good with current approach

**Date**: 2026-05-19
