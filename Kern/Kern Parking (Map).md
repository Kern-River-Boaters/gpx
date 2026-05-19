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

# --- CENTERING (Explicit coordinates for reliability) ---
lat: 35.780805
long: -118.640779
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

# --- DISABLE BROKEN CONTROLS ---
# "Show all markers" button zooms to (0,0) - disable it
showAllMarkers: false

geojson: [[Kern Parking.json]]
```
