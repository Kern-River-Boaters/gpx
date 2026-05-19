---
tags:
  - region/oregon
  - river/rogue
  - season/year_round
  - status/verified
  - type/map
---

> [!WARNING] DO NOT EDIT
> Data Source: [[Rogue_Cadillac.json]]

```leaflet
id: map_8e9bd414

# --- CENTERING ---
# bounds: used by "reset zoom" button
bounds: [[42.622800000000005, -124.0588], [42.7288, -123.5756]]
# lat/long/zoom: initial view on map load
lat: 42.675800
long: -123.817200
zoom: 12

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

# --- HIDE BROKEN CONTROLS ---
# "Show all markers" button is broken (zooms to 0,0 Ivory Coast)
showAllMarkers: false

geojson: [[Rogue_Cadillac.json]]
```
