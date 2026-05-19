#!/usr/bin/env python3
"""
Unified GPX-to-Markdown converter for KRB whitewater guidebook.
Converts GPX waypoints to GeoJSON + Obsidian Leaflet maps.

DESIGN GOALS:
1. Robust mobile rendering (iOS/Android Obsidian)
2. Single source of truth (GPX -> GeoJSON -> Leaflet)
3. Clean separation: auto-generated map files vs. user notes
4. Bounds-based centering to fix viewport issues

DEPENDENCIES:
  pip install gpxpy geojson
"""

import os
import json
import hashlib
import gpxpy
import geojson

# --- CONFIGURATION ---
MAP_SUFFIX = " (Map)"
MD_EXT = ".md"
JSON_EXT = ".json"
TICKS = "`" * 3

# Bounding box buffer (degrees) - prevents waypoints from being cut off at edges
BBOX_BUFFER = 0.01  # ~1km padding

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

def generate_map_markdown(base_name, json_filename, bounds, center):
    """
    Generate Obsidian-compatible Leaflet map markdown.

    MOBILE FIX STRATEGY:
    - Use fitBounds via bounds parameter (primary)
    - Provide lat/long/zoom as fallback
    - Disable gestureHandling (removes "use two fingers" overlay)
    - Enable lock: false for single-finger panning
    - Enable zoomFeatures to auto-zoom GeoJSON on "Show all markers"
    """
    map_id = hashlib.md5(base_name.encode()).hexdigest()[:8]

    # Format bounds as JSON for Leaflet plugin
    bounds_json = json.dumps(bounds)

    return f"""---
tags:
  - type/map
related: "[[{json_filename}]]"
---

> [!WARNING] DO NOT EDIT
> Data Source: [[{json_filename}]]

{TICKS}leaflet
id: map_{map_id}

# --- CENTERING (Bounds-based for mobile compatibility) ---
# Primary: fitBounds uses the bounding box
bounds: {bounds_json}
# Fallback: explicit center if bounds fail
lat: {center[0]:.6f}
long: {center[1]:.6f}
zoom: 13

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

# --- FIX "SHOW ALL MARKERS" BUTTON ---
# Auto-zoom to GeoJSON extent instead of (0,0)
zoomFeatures: true

geojson: [[{json_filename}]]
{TICKS}
"""

def process_gpx_file(gpx_path):
    """
    Process a single GPX file:
    1. Parse to GeoJSON
    2. Write .json data file
    3. Write " (Map).md" Leaflet visualization

    Returns True if processing succeeded.
    """
    dirpath = os.path.dirname(gpx_path)
    base_name = os.path.splitext(os.path.basename(gpx_path))[0]

    json_filename = f"{base_name}{JSON_EXT}"
    map_filename = f"{base_name}{MAP_SUFFIX}{MD_EXT}"

    json_path = os.path.join(dirpath, json_filename)
    map_path = os.path.join(dirpath, map_filename)

    # Parse GPX
    geo_data, bounds, center = parse_gpx_to_geojson(gpx_path)

    if not geo_data:
        return False

    # Write GeoJSON data file
    with open(json_path, 'w', encoding='utf-8') as f:
        geojson.dump(geo_data, f, indent=2)

    # Write Leaflet map markdown
    map_content = generate_map_markdown(base_name, json_filename, bounds, center)
    with open(map_path, 'w', encoding='utf-8') as f:
        f.write(map_content)

    print(f"  ✅ {base_name} -> GeoJSON + Map")
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
    print("1. Open vault in Obsidian mobile to test rendering")
    print("2. Verify maps are centered correctly and allow single-finger pan")
    print("3. If issues persist, check Obsidian Leaflet plugin version")

if __name__ == "__main__":
    main()
