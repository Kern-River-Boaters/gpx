---
tags:
  - difficulty/class_ii_iii
  - feature/rapid
  - region/california
  - region/sierra_nevada
  - river/kern
  - season/year_round
  - status/verified
  - type/map
---

> [!WARNING] DO NOT EDIT
> Data Source: [[Lower Kern Rapids.json]]

```leaflet
id: map_947ece13

# --- CENTERING ---
# bounds: used by "reset zoom" button
bounds: [[35.414764000000005, -118.841555], [35.646254, -118.475566]]
# lat/long/zoom: initial view on map load
lat: 35.530509
long: -118.658560
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

geojson: [[Lower Kern Rapids.json]]
```
