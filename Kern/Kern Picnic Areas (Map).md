---
tags:
  - feature/campground
  - region/california
  - region/sierra_nevada
  - river/kern
  - season/year_round
  - status/verified
  - type/map
---

> [!WARNING] DO NOT EDIT
> Data Source: [[Kern Picnic Areas.json]]

```leaflet
id: map_529532ed

# --- CENTERING (Bounds-based for mobile compatibility) ---
# Primary: fitBounds uses the bounding box
bounds: [[35.52167200647295, -118.65744503051043], [35.87403802037239, -118.43714595936238]]
# Fallback: explicit center if bounds fail
lat: 35.697855
long: -118.547295
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

geojson: [[Kern Picnic Areas.json]]
```
