---
tags:
  - feature/poi
  - region/california
  - region/sierra_nevada
  - river/kern
  - season/year_round
  - status/verified
  - type/map
---

> [!WARNING] DO NOT EDIT
> Data Source: [[Kern Other.json]]

```leaflet
id: map_a4672552

# --- CENTERING (Bounds-based for mobile compatibility) ---
# Primary: fitBounds uses the bounding box
bounds: [[35.414562012776734, -118.83647803984583], [36.10019702300429, -118.40982900165021]]
# Fallback: explicit center if bounds fail
lat: 35.757380
long: -118.623154
zoom: 13

# --- VISUALS ---
height: 600px
minZoom: 5
maxZoom: 18
osmLayer: true
# Prevent black map on mobile dark mode
darkMode: false

# --- MOBILE CONTROLS ---
# Enable single-finger panning
lock: false
# Remove "use two fingers" overlay
gestureHandling: false
# Explicitly enable touch interactions
scrollWheelZoom: true

# --- FIX "SHOW ALL MARKERS" BUTTON ---
# Auto-zoom to GeoJSON extent instead of (0,0)
zoomFeatures: true

geojson: [[Kern Other.json]]
```
