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
> Data Source: [[Kern Other.json]]

```leaflet
id: map_a4672552

# --- CENTERING (Explicit coordinates for reliability) ---
lat: 35.757380
long: -118.623154
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

geojson: [[Kern Other.json]]
```
