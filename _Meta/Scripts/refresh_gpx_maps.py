#!/usr/bin/env python3
"""
Unified GPX-to-Markdown converter for KRB whitewater guidebook.
Converts GPX waypoints to GeoJSON + embedded Obsidian Leaflet maps.

DESIGN GOALS:
1. Single file per GPX (no separate map files)
2. Auto-generated map block with preserved user content
3. Robust mobile rendering (iOS/Android Obsidian)
4. Bounds-based centering to fix viewport issues

DEPENDENCIES:
  pip install gpxpy geojson
"""

import os
import re
import json
import hashlib
import gpxpy
import geojson

# --- CONFIGURATION ---
MD_EXT = ".md"
JSON_EXT = ".json"
TICKS = "`" * 3

# Markers for auto-generated content block
MAP_START_MARKER = "<!-- BEGIN AUTO-GENERATED MAP -->"
MAP_END_MARKER = "<!-- END AUTO-GENERATED MAP -->"

# Bounding box buffer (degrees) - prevents waypoints from being cut off at edges
BBOX_BUFFER = 0.003  # ~300m padding (tighter fit)

def get_mtime(path):
    """Returns file modification time, or 0 if file doesn't exist."""
    return os.path.getmtime(path) if os.path.exists(path) else 0

def parse_gpx_to_geojson(gpx_path):
    """
    Parse GPX file and return:
      - GeoJSON FeatureCollection (for .json data file)
      - Bounding box [[minLat, minLon], [maxLat, maxLon]]
      - Center point [lat, lon]

    Returns (None, None, None) on error.
    """
    try:
        with open(gpx_path, 'r', encoding='utf-8') as f:
            gpx = gpxpy.parse(f)

        if not gpx.waypoints:
            print(f"  ⚠️  No waypoints found in {os.path.basename(gpx_path)}")
            return None, None, None

        # Build GeoJSON features
        features = []
        lats = []
        lons = []

        for wpt in gpx.waypoints:
            if wpt.latitude is None or wpt.longitude is None:
                continue

            # GeoJSON spec: coordinates are [longitude, latitude]
            point = geojson.Point((wpt.longitude, wpt.latitude))

            name = (wpt.name or "Unnamed").strip().replace('"', '')
            desc = (wpt.description or name).strip().replace('"', '')

            features.append(geojson.Feature(
                geometry=point,
                properties={"name": name, "desc": desc}
            ))

            lats.append(wpt.latitude)
            lons.append(wpt.longitude)

        if not features:
            return None, None, None

        # Calculate bounds with buffer
        min_lat = min(lats) - BBOX_BUFFER
        max_lat = max(lats) + BBOX_BUFFER
        min_lon = min(lons) - BBOX_BUFFER
        max_lon = max(lons) + BBOX_BUFFER

        # Leaflet bounds format: [[southWest], [northEast]]
        bounds = [[min_lat, min_lon], [max_lat, max_lon]]

        # Center point (fallback if bounds don't work on mobile)
        center = [(min_lat + max_lat) / 2, (min_lon + max_lon) / 2]

        return geojson.FeatureCollection(features), bounds, center

    except Exception as e:
        print(f"  ❌ Error parsing {os.path.basename(gpx_path)}: {e}")
        return None, None, None

def generate_map_block(base_name, json_filename, bounds, center):
    """
    Generate the auto-generated map block with markers.
    This block will be inserted/updated in the markdown file.
    """
    map_id = hashlib.md5(base_name.encode()).hexdigest()[:8]
    bounds_json = json.dumps(bounds)

    # Calculate zoom level based on bounding box size
    lat_range = bounds[1][0] - bounds[0][0]
    lon_range = bounds[1][1] - bounds[0][1]
    max_range = max(lat_range, lon_range)

    if max_range > 0.5:
        zoom = 11
    elif max_range > 0.2:
        zoom = 13
    elif max_range > 0.1:
        zoom = 14
    else:
        zoom = 15

    return f"""{MAP_START_MARKER}
## Street Map

{TICKS}leaflet
id: map_{map_id}_street
bounds: {bounds_json}
lat: {center[0]:.6f}
long: {center[1]:.6f}
zoom: {zoom}
height: 600px
minZoom: 5
maxZoom: 20
osmLayer: true
darkMode: false
lock: false
dragging: true
gestureHandling: false
scrollWheelZoom: true
touchZoom: true
doubleClickZoom: true
showAllMarkers: false

geojson: [[{json_filename}]]
{TICKS}

## Satellite Map

{TICKS}leaflet
id: map_{map_id}_satellite
bounds: {bounds_json}
lat: {center[0]:.6f}
long: {center[1]:.6f}
zoom: {zoom}
height: 600px
minZoom: 5
maxZoom: 20
osmLayer: false
tileServer: https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}
darkMode: false
lock: false
dragging: true
gestureHandling: false
scrollWheelZoom: true
touchZoom: true
doubleClickZoom: true
showAllMarkers: false

geojson: [[{json_filename}]]
{TICKS}
{MAP_END_MARKER}"""

def update_markdown_file(md_path, base_name, json_filename, bounds, center):
    """
    Update or create markdown file with embedded map block.
    Preserves user content outside the auto-generated markers.
    """
    map_block = generate_map_block(base_name, json_filename, bounds, center)

    if os.path.exists(md_path):
        # Read existing file
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if it has the markers
        if MAP_START_MARKER in content and MAP_END_MARKER in content:
            # Replace existing map block
            pattern = re.compile(
                re.escape(MAP_START_MARKER) + r'.*?' + re.escape(MAP_END_MARKER),
                re.DOTALL
            )
            new_content = pattern.sub(map_block, content)
        else:
            # Append map block at end
            new_content = content.rstrip() + "\n\n" + map_block + "\n"
    else:
        # Create new file with basic structure
        new_content = f"""---
tags:
  - type/map
---

# {base_name}

{map_block}
"""

    # Write updated content
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

def process_gpx_file(gpx_path):
    """
    Process a single GPX file:
    1. Parse to GeoJSON
    2. Write .json data file
    3. Update .md file with embedded map (preserving user content)

    Returns True if processing succeeded.
    """
    dirpath = os.path.dirname(gpx_path)
    base_name = os.path.splitext(os.path.basename(gpx_path))[0]

    json_filename = f"{base_name}{JSON_EXT}"
    md_filename = f"{base_name}{MD_EXT}"

    json_path = os.path.join(dirpath, json_filename)
    md_path = os.path.join(dirpath, md_filename)

    # Parse GPX
    geo_data, bounds, center = parse_gpx_to_geojson(gpx_path)

    if not geo_data:
        return False

    # Write GeoJSON data file
    with open(json_path, 'w', encoding='utf-8') as f:
        geojson.dump(geo_data, f, indent=2)

    # Update markdown with embedded map
    update_markdown_file(md_path, base_name, json_filename, bounds, center)

    print(f"  ✅ {base_name} -> GeoJSON + embedded map")
    return True

def scan_and_process(root_dir):
    """
    Recursively scan for .gpx files and process them.
    Only regenerates if GPX is newer than existing JSON.
    """
    print(f"Scanning for GPX files in: {root_dir}")
    print()

    processed = 0
    skipped = 0

    for dirpath, _, filenames in os.walk(root_dir):
        # Skip hidden directories and _Meta
        if '\\.' in dirpath or '_Meta' in dirpath:
            continue

        for filename in filenames:
            if not filename.lower().endswith('.gpx'):
                continue

            gpx_path = os.path.join(dirpath, filename)
            base_name = os.path.splitext(filename)[0]
            json_path = os.path.join(dirpath, f"{base_name}{JSON_EXT}")

            # Check if regeneration needed
            if get_mtime(json_path) >= get_mtime(gpx_path):
                skipped += 1
                continue

            print(f"Processing: {filename}")
            if process_gpx_file(gpx_path):
                processed += 1

    print()
    print(f"✅ Complete. Processed: {processed}, Skipped (up-to-date): {skipped}")

def main():
    # Ensure required packages are installed
    try:
        import gpxpy
        import geojson
    except ImportError as e:
        print("❌ Missing required package!")
        print("Run: pip install gpxpy geojson")
        return

    root = os.getcwd()
    scan_and_process(root)

    print()
    print("Next steps:")
    print("1. Review files - user content preserved, map blocks updated")
    print("2. Delete old *' (Map).md' files if any exist")
    print("3. Test in Obsidian mobile")

if __name__ == "__main__":
    main()
