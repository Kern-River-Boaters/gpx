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
> Data Source: [[Kern Campgrounds.json]]

```leaflet
id: map_c96ef2b5

# --- CENTERING ---
# bounds: used by "reset zoom" button
bounds: [[35.46908696345985, -118.74294899240137], [35.972817994877694, -118.41144897207617]]
# lat/long/zoom: initial view on map load
lat: 35.720952
long: -118.577199
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

geojson: [[Kern Campgrounds.json]]
```
