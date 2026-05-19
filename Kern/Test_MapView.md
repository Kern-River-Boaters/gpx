# Test: Map View with GeoJSON

Testing if Map View plugin can render GeoJSON inline with embedded map.

## Test 1: Embedded Map with mapZoom

```mapview
{"type":"FeatureCollection","features":[{"type":"Feature","geometry":{"type":"Point","coordinates":[-118.556407,35.577993]},"properties":{"name":"White Maiden's (4)"}},{"type":"Feature","geometry":{"type":"Point","coordinates":[-118.640497,35.535047]},"properties":{"name":"Upper Bailmore (2+)"}},{"type":"Feature","geometry":{"type":"Point","coordinates":[-118.658560,35.530509]},"properties":{"name":"Center Point"}}]}
```

## Test 2: Standard GeoJSON with Auto-fit

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
autofit

## Test 3: Reference External GeoJSON

```mapview
geojson: [[Lower Kern Rapids.json]]
```

---

**If none work, Map View likely doesn't support inline embedded maps like Leaflet does.**
