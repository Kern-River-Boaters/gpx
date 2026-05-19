---
tags:
  - difficulty/class_iv_v
  - feature/rapid
  - region/california
  - region/sierra_nevada
  - river/kern
  - season/year_round
  - status/verified
  - type/map
---

> [!WARNING] DO NOT EDIT
> Data Source: [[North Fork Kern Rapids.json]]

```leaflet
id: map_b1dde91e

# --- CENTERING (Bounds-based for mobile compatibility) ---
# Primary: fitBounds uses the bounding box
bounds: [[35.743743, -118.49805400000001], [36.117587, -118.411198]]
# Fallback: explicit center if bounds fail
lat: 35.930665
long: -118.454626
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

geojson: [[North Fork Kern Rapids.json]]
```
