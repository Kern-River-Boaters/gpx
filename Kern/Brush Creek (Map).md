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
> Data Source: [[Brush Creek.json]]

```leaflet
id: map_09aa3f74

# --- CENTERING ---
# bounds: used by "reset zoom" button
bounds: [[35.956166, -118.48791200000001], [35.981331, -118.45523999999999]]
# lat/long/zoom: initial view on map load
lat: 35.968749
long: -118.471576
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

geojson: [[Brush Creek.json]]
```
