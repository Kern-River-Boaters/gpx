# Testing Layer Control Button

## Test 1: Simple image Parameter (String)

```leaflet
id: test_image_string
lat: 35.530509
long: -118.658560
zoom: 13
height: 600px
minZoom: 5
maxZoom: 20
darkMode: false
image: osm

geojson: [[Lower Kern Rapids.json]]
```

---

## Test 2: Baseline OSM (Should Work)

```leaflet
id: test_baseline_osm
lat: 35.530509
long: -118.658560
zoom: 13
height: 600px
osmLayer: true

geojson: [[Lower Kern Rapids.json]]
```

---

## Test 3: Just Satellite (Should Work)

```leaflet
id: test_satellite_only
lat: 35.530509
long: -118.658560
zoom: 13
height: 600px
osmLayer: false
tileServer: https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}

geojson: [[Lower Kern Rapids.json]]
```

---

## Conclusion

**Reality Check**: The Obsidian Leaflet plugin may not support layer control buttons at all.

If none of these show a toggle button, our options are:

### Option A: Dual Maps (Two Blocks Per File)
Include BOTH street and satellite maps in each file:

```markdown
## Street Map
[leaflet block with OSM]

## Satellite Map  
[leaflet block with Satellite]
```

Users scroll to whichever they want.

### Option B: Manual Switch (Current)
Users edit the file to toggle between layers (what we have now).

### Option C: Separate Files
Create `Lower Kern Rapids - Satellite.md` versions for key rivers.

**Test these 3 above first, then let me know if any work or if we should pivot to Option A/B/C.**
