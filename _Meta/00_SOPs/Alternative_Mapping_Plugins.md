# Alternative Mapping Plugins for Obsidian

## Currently Tested

### 1. Obsidian Leaflet (Current - Partial Success)
**Repository**: valentine195/obsidian-leaflet-plugin  
**Version**: 6.0.5  
**Status**: ✅ Works with GeoJSON, ❌ "Show all markers" broken

### 2. Map View (Tested - Doesn't Work for Us)
**Repository**: esm7/obsidian-map-view  
**Version**: 6.1.4  
**Status**: ❌ Separate pane only, not inline embedded maps

## Other Popular Map Plugins to Try

### 3. Obsidian Leaflet Extended
**Repository**: Check if exists  
**Features**: May have additional GeoJSON support  
**Worth trying?**: Unknown

### 4. Mapbox (Custom Solution)
**Approach**: Create custom HTML iframes with Mapbox GL JS  
**Pros**: Full control, modern rendering engine  
**Cons**: Requires API key, more complex setup  
**Example**:
```html
<iframe src="mapbox-embed-url" width="100%" height="600px"></iframe>
```

### 5. Google Maps Embed (Simple Alternative)
**Approach**: Use Google Maps embed API  
**Pros**: Simple, reliable, works everywhere  
**Cons**: No waypoint support (would need to generate URLs)  
**Example**:
```html
<iframe src="https://www.google.com/maps/embed?pb=..." width="100%" height="600px"></iframe>
```

### 6. OpenLayers (Custom)
**Approach**: Build custom OpenLayers implementation  
**Pros**: Open source, powerful  
**Cons**: Requires custom development

### 7. Static Map Images (Fallback)
**Approach**: Generate PNG/JPG maps from GPX data  
**Tools**: 
- staticmap.py (Python library)
- Mapbox Static API
- Google Static Maps API
**Pros**: Always works, no JavaScript issues  
**Cons**: Not interactive, need regeneration on data change

## Community Plugin Search

### Recommended Search Terms
Try searching Obsidian Community Plugins for:
- "map"
- "geo"
- "gps"
- "location"
- "leaflet"
- "geojson"

### How to Search
1. Settings → Community Plugins → Browse
2. Search each term
3. Sort by "Downloads" to find popular ones

## Current Best Option

**Stick with Obsidian Leaflet** unless one of these proves better:

**Why Leaflet still wins**:
- ✅ Most popular map plugin (battle-tested)
- ✅ Works with our GeoJSON architecture
- ✅ Good mobile performance
- ✅ Inline embedded maps
- ❌ "Show all markers" button issue (acceptable)

**Only switch if new plugin has**:
- ✅ Inline embedded maps (not separate pane)
- ✅ GeoJSON support for 40+ waypoints
- ✅ Good Android performance
- ✅ "Show all markers" or equivalent that works

---

**Action Items**:
1. Search Obsidian Community Plugins for "geojson"
2. Check if any newer plugins exist
3. Read reviews/issues on GitHub for alternatives
4. If nothing better, accept current Leaflet limitation

**Date**: 2026-05-19
