---
tags:
  - feature/parking
  - region/california
  - region/sierra_nevada
  - river/kern
  - season/year_round
  - status/verified
  - type/map
---

> [!WARNING] DO NOT EDIT
> Data Source: [[Kern Parking.json]]

```leaflet
id: map_ee71bcd3

# --- CENTERING (Bounds-based for mobile compatibility) ---
# Primary: fitBounds uses the bounding box
bounds: [[35.41421097867191, -118.8409470191598], [36.14739803433418, -118.44061003230512]]
# Fallback: explicit center if bounds fail
lat: 35.780805
long: -118.640779
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

geojson: [[Kern Parking.json]]
```
