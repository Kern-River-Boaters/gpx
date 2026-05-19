# Testing Tile Layer Syntax for Leaflet Plugin

## Test 1: Single Satellite Tile Server (String)

```leaflet
id: test_satellite_string
lat: 35.530509
long: -118.658560
zoom: 12
height: 400px
osmLayer: false
tileServer: https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}

geojson: [[Lower Kern Rapids.json]]
```

**Expected**: Satellite imagery as base layer

---

## Test 2: OpenStreetMap + Satellite (Multiple Layers)

```leaflet
id: test_multiple_layers
lat: 35.530509
long: -118.658560
zoom: 12
height: 400px
osmLayer: true
layer: https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}

geojson: [[Lower Kern Rapids.json]]
```

**Expected**: OSM base + Satellite overlay (or layer control)

---

## Test 3: Default OSM (Baseline - Should Work)

```leaflet
id: test_osm_baseline
lat: 35.530509
long: -118.658560
zoom: 12
height: 400px
osmLayer: true

geojson: [[Lower Kern Rapids.json]]
```

**Expected**: ✅ Standard OpenStreetMap with all waypoints visible

---

## Test 4: Terrain/Topo Map

```leaflet
id: test_terrain
lat: 35.530509
long: -118.658560
zoom: 12
height: 400px
osmLayer: false
tileServer: https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png

geojson: [[Lower Kern Rapids.json]]
```

**Expected**: Topographic map with contour lines

---

**Instructions**: Check which tests render correctly, then report back which syntax works!
