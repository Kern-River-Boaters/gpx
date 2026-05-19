#!/usr/bin/env python3
"""
TEST VERSION: GPX-to-Markdown with INLINE markers (no JSON files).
Testing if this resolves Android issues or creates new ones.

This embeds waypoints directly in the Leaflet code block instead of
using external GeoJSON files.
"""

import os
import re
import hashlib
import gpxpy

# --- CONFIGURATION ---
MD_EXT = ".md"
TICKS = "`" * 3

# Markers for auto-generated content block
MAP_START_MARKER = "<!-- BEGIN AUTO-GENERATED MAP -->"
MAP_END_MARKER = "<!-- END AUTO-GENERATED MAP -->"

# Bounding box buffer (degrees)
BBOX_BUFFER = 0.003  # ~300m padding

def get_mtime(path):
    """Returns file modification time, or 0 if file doesn't exist."""
    return os.path.getmtime(path) if os.path.exists(path) else 0

def parse_gpx_to_markers(gpx_path):
    """
    Parse GPX file and return:
      - List of marker strings for inline embedding
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

        # Build marker list
        markers = []
        lats = []
        lons = []

        for wpt in gpx.waypoints:
            if wpt.latitude is None or wpt.longitude is None:
                continue

            name = (wpt.name or "Unnamed").strip().replace('"', '\\"')

            # Leaflet marker format: [lat, lon, "name"]
            markers.append(f'  - [{wpt.latitude}, {wpt.longitude}, "{name}"]')

            lats.append(wpt.latitude)
            lons.append(wpt.longitude)

        if not markers:
            return None, None, None

        # Calculate bounds with buffer
        min_lat = min(lats) - BBOX_BUFFER
        max_lat = max(lats) + BBOX_BUFFER
        min_lon = min(lons) - BBOX_BUFFER
        max_lon = max(lons) + BBOX_BUFFER

        # Leaflet bounds format: [[southWest], [northEast]]
        bounds = [[min_lat, min_lon], [max_lat, max_lon]]

        # Center point
        center = [(min_lat + max_lat) / 2, (min_lon + max_lon) / 2]

        return markers, bounds, center

    except Exception as e:
        print(f"  ❌ Error parsing {os.path.basename(gpx_path)}: {e}")
        return None, None, None

def generate_map_block(base_name, markers, bounds, center):
    """
    Generate the auto-generated map block with INLINE markers.
    """
    map_id = hashlib.md5(base_name.encode()).hexdigest()[:8]
    bounds_json = str(bounds).replace("'", "")

    # Calculate zoom level based on bounding box size
    lat_range = bounds[1][0] - bounds[0][0]
    lon_range = bounds[1][1] - bounds[0][1]
    max_range = max(lat_range, lon_range)

    if max_range > 0.5:
        zoom = 11
    elif max_range > 0.2:
        zoom = 12
    elif max_range > 0.1:
        zoom = 13
    else:
        zoom = 14

    # Build marker block
    markers_block = "\n".join(markers)

    return f"""{MAP_START_MARKER}
{TICKS}leaflet
id: map_{map_id}

# --- CENTERING ---
bounds: {bounds_json}
lat: {center[0]:.6f}
long: {center[1]:.6f}
zoom: {zoom}

# --- VISUALS ---
height: 600px
minZoom: 5
maxZoom: 18
osmLayer: true
darkMode: false

# --- MOBILE CONTROLS ---
lock: false
dragging: true
gestureHandling: false
scrollWheelZoom: true
touchZoom: true
doubleClickZoom: true

# --- INLINE MARKERS (no external JSON) ---
marker:
{markers_block}
{TICKS}
{MAP_END_MARKER}"""

def update_markdown_file(md_path, base_name, markers, bounds, center):
    """
    Update or create markdown file with embedded map block.
    Preserves user content outside the auto-generated markers.
    """
    map_block = generate_map_block(base_name, markers, bounds, center)

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
    Process a single GPX file with INLINE markers.
    """
    dirpath = os.path.dirname(gpx_path)
    base_name = os.path.splitext(os.path.basename(gpx_path))[0]
    md_filename = f"{base_name}{MD_EXT}"
    md_path = os.path.join(dirpath, md_filename)

    # Parse GPX
    markers, bounds, center = parse_gpx_to_markers(gpx_path)

    if not markers:
        return False

    # Update markdown with embedded map
    update_markdown_file(md_path, base_name, markers, bounds, center)

    print(f"  ✅ {base_name} -> inline markers ({len(markers)} waypoints)")
    return True

def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python refresh_gpx_maps_inline.py <path_to_gpx_file>")
        print("Example: python refresh_gpx_maps_inline.py 'Kern/Lower Kern Rapids.gpx'")
        return

    gpx_path = sys.argv[1]

    if not os.path.exists(gpx_path):
        print(f"❌ File not found: {gpx_path}")
        return

    print(f"Testing inline markers for: {os.path.basename(gpx_path)}")
    print()

    if process_gpx_file(gpx_path):
        print()
        print("✅ Test file generated with inline markers")
        print()
        print("Next steps:")
        print("1. Test on Android - check rendering speed and responsiveness")
        print("2. Compare with GeoJSON version")
        print("3. If Android issues appear, revert with refresh_gpx_maps.py")
    else:
        print("❌ Failed to process file")

if __name__ == "__main__":
    main()
