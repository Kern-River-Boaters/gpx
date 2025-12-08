import os
import json
import hashlib
import gpxpy # pip install gpxpy
import geojson # pip install geojson

# --- CONFIGURATION ---
STATIC_SUFFIX = " (Map)"
MD_EXT = ".md"
JSON_EXT = ".json"
TICKS = "`" * 3

def process_gpx(gpx_path):
    try:
        with open(gpx_path, 'r', encoding='utf-8') as f:
            gpx = gpxpy.parse(f)

        if not gpx.waypoints:
            return None, None

        # 1. GENERATE GEOJSON FEATURES
        # We use GeoJSON because it is robust and supported by Leaflet
        features = []
        lats = []
        lons = []

        for wpt in gpx.waypoints:
            if wpt.latitude is None or wpt.longitude is None: continue
            
            # GeoJSON requires [Longitude, Latitude]
            point = geojson.Point((wpt.longitude, wpt.latitude))
            
            # Clean Name
            name = wpt.name.strip().replace('"', '') if wpt.name else "Unnamed"
            
            # Create Feature
            feat = geojson.Feature(geometry=point, properties={"name": name, "desc": name})
            features.append(feat)
            
            lats.append(wpt.latitude)
            lons.append(wpt.longitude)

        if not features: return None, None

        fc = geojson.FeatureCollection(features)

        # 2. CALCULATE CENTER (For Initial View)
        # We use a simple average to ensure the camera points at the river
        center_lat = sum(lats) / len(lats)
        center_lon = sum(lons) / len(lons)

        return fc, (center_lat, center_lon)

    except Exception as e:
        print(f"Error parsing {gpx_path}: {e}")
        return None, None

def write_files(base_name, dir_path, geo_data, center):
    json_name = f"{base_name}{JSON_EXT}"
    map_name = f"{base_name}{STATIC_SUFFIX}{MD_EXT}"
    
    # 1. Write JSON File
    json_full_path = os.path.join(dir_path, json_name)
    with open(json_full_path, 'w', encoding='utf-8') as f:
        geojson.dump(geo_data, f, indent=2)

    # 2. Write Markdown Map
    map_full_path = os.path.join(dir_path, map_name)
    map_id = hashlib.md5(base_name.encode()).hexdigest()[:8]
    
    content = f"""---
related: "[[{base_name}]]"
tags:
  - auto-generated
---
> [!WARNING] DO NOT EDIT
> Data Source: [[{json_name}]]

{TICKS}leaflet
id: map_{map_id}

# --- CENTERING (Fixed) ---
# We explicitly tell Leaflet where to look.
# We do NOT use 'bounds' (which breaks easily).
lat: {center[0]:.6f}
long: {center[1]:.6f}
zoom: 13

# --- VISUALS ---
height: 600px
minZoom: 5
maxZoom: 18
osmLayer: true
# Prevents "Black Map" on mobile dark mode
darkMode: false

# --- MOBILE CONTROLS (Unlocked) ---
# 'lock: false' -> Enables One-Finger Panning
lock: false
# 'gestureHandling: false' -> Removes "Two finger" warning
gestureHandling: false
# 'scrollWheelZoom: true' -> Enables zoom
scrollWheelZoom: true

geojson: [[{json_name}]]
{TICKS}
"""
    with open(map_full_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    root = os.getcwd()
    print(f"Scanning {root}...")
    
    count = 0
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            if fname.lower().endswith('.gpx'):
                base_name = os.path.splitext(fname)[0]
                gpx_path = os.path.join(dirpath, fname)
                
                print(f"Processing: {fname}")
                geo_data, center = process_gpx(gpx_path)
                
                if geo_data:
                    # Verify coordinates in console
                    print(f"  > Center: {center[0]:.4f}, {center[1]:.4f}")
                    write_files(base_name, dirpath, geo_data, center)
                    count += 1
                    
                    # Ensure parent note
                    parent_path = os.path.join(dirpath, f"{base_name}{MD_EXT}")
                    if not os.path.exists(parent_path):
                        with open(parent_path, 'w', encoding='utf-8') as f:
                            f.write(f"---\nrelated: \"[[{base_name}{STATIC_SUFFIX}]]\"\n---\n# {base_name}\n\nNotes...")

    print(f"Done. Generated {count} robust maps.")

if __name__ == "__main__":
    main()
    