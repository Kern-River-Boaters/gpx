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

# --- CENTERING ---
# bounds: used by "reset zoom" button
bounds: [[35.52167200647295, -118.65744503051043], [35.87403802037239, -118.43714595936238]]
# lat/long/zoom: initial view on map load
lat: 35.697855
long: -118.547295
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

geojson: [[Kern Picnic Areas.json]]
```
