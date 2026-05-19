# Comprehensive Map Rendering Tests

Testing different plugins and syntaxes to find the best mapping solution.

---

## Test 1: Leaflet with GeoJSON (Current Working Method)

```leaflet
id: test_leaflet_geojson
lat: 35.530509
long: -118.658560
zoom: 12
height: 400px
osmLayer: true
darkMode: false

geojson: [[Lower Kern Rapids.json]]
```

**Expected**: ✅ Should render inline with all 41 waypoints from JSON file

---

## Test 2: Map View with Inline GeoJSON

```geojson
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [-118.556407, 35.577993]
      },
      "properties": {
        "name": "White Maiden's (4)"
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [-118.640497, 35.535047]
      },
      "properties": {
        "name": "Upper Bailmore (2+)"
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [-118.658560, 35.530509]
      },
      "properties": {
        "name": "Center Point"
      }
    }
  ]
}
```

**Expected**: 
- ✅ If Map View works inline: Interactive map with 3 points
- ❌ If Map View doesn't work inline: World map or code block only

---

## Test 3: Leaflet with Inline Markers (No GeoJSON)

```leaflet
id: test_leaflet_inline
lat: 35.530509
long: -118.658560
zoom: 12
height: 400px
osmLayer: true
darkMode: false

marker:
  - [35.577993, -118.556407, "White Maiden's (4)"]
  - [35.535047, -118.640497, "Upper Bailmore (2+)"]
  - [35.530509, -118.658560, "Center Point"]
```

**Expected**: 
- ✅ Should render if Leaflet supports inline markers without comments
- ❌ Grey box if syntax error

---

## Test 4: Leaflet with Hybrid (Marker + GeoJSON)

```leaflet
id: test_leaflet_hybrid
lat: 35.530509
long: -118.658560
zoom: 12
height: 400px
osmLayer: true
darkMode: false

marker:
  - [35.530509, -118.658560, "Center"]

geojson: [[Lower Kern Rapids.json]]
```

**Expected**: 
- ✅ Should render if Leaflet supports mixing marker and geojson
- ❌ Grey box if incompatible syntax

---

## Test 5: Map View with mapview Block

```mapview
{"type":"FeatureCollection","features":[{"type":"Feature","geometry":{"type":"Point","coordinates":[-118.556407,35.577993]},"properties":{"name":"Test Point"}}]}
```

**Expected**: 
- ✅ If Map View supports mapview blocks inline
- ❌ Code block or world map if not supported

---

## Results Summary

| Test | Plugin | Method | Result | Notes |
|------|--------|--------|--------|-------|
| 1 | Leaflet | GeoJSON file | ⏳ | Current working method |
| 2 | Map View | Inline GeoJSON | ⏳ | Test for inline rendering |
| 3 | Leaflet | Inline markers | ⏳ | Test without comments |
| 4 | Leaflet | Hybrid | ⏳ | Test marker+geojson mix |
| 5 | Map View | mapview block | ⏳ | Alternative syntax |

---

## Instructions

1. **View this note in Obsidian** (not editor mode, but reading mode)
2. **Check each test section** - does it render an interactive map?
3. **Fill in Results**:
   - ✅ = Renders correctly with points visible
   - ❌ = Grey box, world map with no points, or code block only
4. **Report findings** so we can choose the best approach

---

**Goal**: Find a method that:
- ✅ Renders inline (not separate pane)
- ✅ Shows all waypoints correctly
- ✅ Works on desktop AND mobile
- ✅ Has working zoom controls (including "Show all markers" if possible)
