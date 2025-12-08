---
related: "[[Kern Access]]"
tags:
  - auto-generated
---
> [!WARNING] DO NOT EDIT
> Data Source: [[Kern Access.json]]

```leaflet
id: map_5e23a4b4

# --- CENTERING (Fixed) ---
# We explicitly tell Leaflet where to look.
# We do NOT use 'bounds' (which breaks easily).
lat: 35.753618
long: -118.538692
zoom: 13

# --- VISUALS ---
height: 600px
minZoom: 5
maxZoom: 18
osmLayer: true
# Prevents "Black Map" on #mobile dark mode
#darkMode: false

# --- MOBILE CONTROLS (Unlocked) ---
# 'lock: false' -> Enables #One-Finger Panning
lock: false
# 'gestureHandling: false' -> Removes "Two finger" warning
gestureHandling: false
# 'scrollWheelZoom: true' -> Enables zoom
#scrollWheelZoom: true

geojson: [[Kern Access.json]]
```

GPX
```leaflet
id: map_5e23a4b42
gpx: [[Kern Access.gpx]]
gpxMarkers:
  start: start_marker_type
  waypoint: waypoint_marker_type
```