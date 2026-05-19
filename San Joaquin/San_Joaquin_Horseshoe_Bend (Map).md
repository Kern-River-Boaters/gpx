---
tags:
  - region/california
  - region/sierra_nevada
  - river/san_joaquin
  - season/year_round
  - status/verified
  - type/map
---

> [!WARNING] DO NOT EDIT
> Data Source: [[San_Joaquin_Horseshoe_Bend.json]]

```leaflet
id: map_bfde0138

# --- CENTERING ---
# bounds: used by "reset zoom" button
bounds: [[37.099737000000005, -119.52294900000001], [37.159211, -119.445]]
# lat/long/zoom: initial view on map load
lat: 37.129474
long: -119.483975
zoom: 14

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

geojson: [[San_Joaquin_Horseshoe_Bend.json]]
```
