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

# Safety buffer (in degrees) to ensure points aren't on the exact edge of screen
# 0.005 degrees is roughly 500 meters
BUFFER = 0.005 

def get_mtime(path):
    """Returns file modification time or 0 if missing."""
    if not os.path.exists(path):
        return 0
    return os.path.getmtime(path)

def process_gpx(gpx_path):
    """
    Parses GPX and returns:
    1. A GeoJSON FeatureCollection (for the .json file)
    2. A Leaflet-formatted Bounds List [[Lat, Lon], [Lat, Lon]] (for the .md file)
    3. A Center Point [Lat, Lon] (for the .md file)
    """
    try:
        with open(gpx_path, 'r', encoding='utf-8') as f:
            gpx = gpxpy.parse(f)

        if not gpx.waypoints and not gpx.tracks:
            return None, None, None

        # --- 1. BUILD GEOJSON FEATURES ---
        features = []
        
        # Process Waypoints
        for wpt in gpx.waypoints:
            if wpt.latitude is None or wpt.longitude is None:
                continue
            
            # GeoJSON geometry is ALWAYS [Longitude, Latitude]
            point = geojson.Point((wpt.longitude, wpt.latitude))
            
            name = wpt.name.strip() if wpt.name else "Unnamed"
            # Clean up name for display
            clean_name = name.replace('"', '')
            
            feat = geojson.Feature(geometry=point, properties={"name": clean_name, "desc": clean_name})
            features.append(feat)

        # (Optional) Process Tracks if you have them, treated as lines
        for track in gpx.tracks:
            for seg in track.segments:
                coords = [(p.longitude, p.latitude) for p in seg.points]
                if coords:
                    line = geojson.LineString(coords)
                    features.append(geojson.Feature(geometry=line, properties={"color": "blue"}))

        if not features:
            return None, None, None

        fc = geojson.FeatureCollection(features)

        # --- 2. CALCULATE BOUNDS ---
        # We use gpxpy's native bounding box calculator
        bounds = gpx.get_bounds()
        
        if bounds:
            # Apply Buffer
            min_lat = bounds.min_latitude - BUFFER
            max_lat = bounds.max_latitude + BUFFER
            min_lon = bounds.min_longitude - BUFFER
            max_lon = bounds.max_longitude + BUFFER
            
            # Leaflet expects [[SouthWestLat, SouthWestLon], [NorthEastLat, NorthEastLon]]
            leaflet_bounds = [[min_lat, min_lon], [max_lat, max_lon]]
            
            # Calculate Center
            center_lat = (min_lat + max_lat) / 2
            center_lon = (min_lon + max_lon) / 2
            leaflet_center = [center_lat, center_lon]
        else:
            # Fallback for single point (gpxpy sometimes returns None for bounds on single points)
            # We just take the first waypoint
            first_pt = gpx.waypoints[0]
            leaflet_center = [first_pt.latitude, first_pt.longitude]
            # Create a tiny box around it
            leaflet_bounds = [
                [first_pt.latitude - 0.01, first_pt.longitude - 0.01],
                [first_pt.latitude + 0.01, first_pt.longitude + 0.01]
            ]

        return fc, leaflet_bounds, leaflet_center

    except Exception as e:
        print(f"CRITICAL ERROR parsing {gpx_path}: {e}")
        return None, None, None

def write_files(base_name, dir_path, geo_data, bounds, center):
    """Writes the JSON data and the Markdown Map note."""
    
    # Filenames
    json_name = f"{base_name}{JSON_EXT}"
    map_name = f"{base_name}{STATIC_SUFFIX}{MD_EXT}"
    
    json_path = os.path.join(dir_path, json_name)
    map_path = os.path.join(dir_path, map_name)
    
    # 1. Write GeoJSON
    with open(json_path, 'w', encoding='utf-8') as f:
        geojson.dump(geo_data, f, indent=2)

    # 2. Write Markdown Map
    # Unique ID based on name to prevent caching collisions
    map_id = hashlib.md5(base_name.encode()).hexdigest()[:8]
    
    # Convert lists to JSON strings for injection into Markdown
    bounds_str = json.dumps(bounds)
    
    content = f"""---
related: "[[{base_name}]]"
tags:
  - auto-generated
---
> [!WARNING] DO NOT EDIT
> Data Source: [[{json_name}]]

{TICKS}leaflet
id: map_{map_id}

# --- CRITICAL LOCATION FIXES ---
# We force the map to these exact coordinates.
# If 'bounds' fails, 'lat/long' catches it.
bounds: {bounds_str}
lat: {center[0]:.6f}
long: {center[1]:.6f}

# --- VISUALS ---
height: 600px
minZoom: 5
maxZoom: 18
osmLayer: true

# --- MOBILE UNLOCK ---
# 'lock: false' is the master switch for panning
lock: false
# 'gestureHandling: false' removes the two-finger requirement
gestureHandling: false
# 'dragging: true' ensures touch events work
dragging: true
# 'scrollWheelZoom: true' allows pinch-zoom
scrollWheelZoom: true

geojson: [[{json_name}]]
{TICKS}
"""
    with open(map_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    root = os.getcwd()
    print(f"Scanning {root}...")
    
    processed = 0
    
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            if fname.lower().endswith('.gpx'):
                gpx_path = os.path.join(dirpath, fname)
                base_name = os.path.splitext(fname)[0]
                
                # Check for existing outputs
                json_path = os.path.join(dirpath, f"{base_name}{JSON_EXT}")
                
                # Update logic: If GPX is newer than JSON, or JSON is missing
                if get_mtime(gpx_path) > get_mtime(json_path):
                    print(f"Processing: {fname}")
                    
                    geo_data, bounds, center = process_gpx(gpx_path)
                    
                    if geo_data:
                        print(f"  > Valid Data found. Center: {center}")
                        write_files(base_name, dirpath, geo_data, bounds, center)
                        processed += 1
                        
                        # Create Main Note link if missing
                        main_note = os.path.join(dirpath, f"{base_name}{MD_EXT}")
                        if not os.path.exists(main_note):
                            with open(main_note, 'w', encoding='utf-8') as f:
                                f.write(f"---\nrelated: \"[[{base_name}{STATIC_SUFFIX}]]\"\n---\n# {base_name}\n\nNotes...")
                    else:
                        print(f"  > Warning: No waypoints found in {fname}")

    print(f"Done. Processed {processed} maps.")

if __name__ == "__main__":
    main()
    