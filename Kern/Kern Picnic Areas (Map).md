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

# --- CENTERING (Fixed) ---
# We explicitly tell Leaflet where to look.
# We do NOT use 'bounds' (which breaks easily).
lat: 35.753561
long: -118.500863
zoom: 13

# --- VISUALS ---
height: 600px
minZoom: 5
maxZoom: 18
osmLayer: true
# Prevents "Black Map" on mobile dark mode
darkMode: false

# --- MOBILE CONTROLS (Unlocked) ---
# 'lock: false' -> Enables One-Finger Panning
lock: false
# 'gestureHandling: false' -> Removes "Two finger" warning
gestureHandling: false
# 'scrollWheelZoom: true' -> Enables zoom
scrollWheelZoom: true

geojson: [[Kern Picnic Areas.json]]
```
