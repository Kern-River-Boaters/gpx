---
tags:
  - feature/access
  - region/california
  - region/sierra_nevada
  - river/kern
  - season/year_round
  - status/verified
  - type/map
---

> [!WARNING] DO NOT EDIT
> Data Source: [[Kern Access.json]]

```leaflet
id: map_5e23a4b4

# --- CENTERING ---
# bounds: used by "reset zoom" button
bounds: [[35.416246, -118.843782], [36.143662, -118.414322]]
# lat/long/zoom: initial view on map load
lat: 35.779954
long: -118.629052
zoom: 11

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

geojson: [[Kern Access.json]]
```
