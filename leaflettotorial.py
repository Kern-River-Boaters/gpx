import os
import hashlib
import gpxpy # pip install gpxpy

# --- CONFIGURATION ---
STATIC_SUFFIX = " (Map)"
MD_EXT = ".md"
TICKS = "`" * 3

def process_gpx(gpx_path):
    """
    Parses GPX and returns:
    1. A YAML-formatted string of markers.
    2. The center point (Lat, Lon).
    """
    try:
        with open(gpx_path, 'r', encoding='utf-8') as f:
            gpx = gpxpy.parse(f)

        if not gpx.waypoints:
            return None, None

        markers = []
        lats = []
        lons = []

        for wpt in gpx.waypoints:
            if wpt.latitude is None or wpt.longitude is None:
                continue
            
            # Sanitize Name:
            # 1. Strip whitespace
            # 2. Remove double quotes (breaks YAML)
            # 3. Remove single quotes (breaks YAML)
            name = "Unnamed"
            if wpt.name:
                name = wpt.name.strip().replace('"', '').replace("'", "")
            
            # FORMAT: Strict YAML list item
            # - [35.12345, -118.12345, "Name"]
            marker_line = f"  - [{wpt.latitude:.6f}, {wpt.longitude:.6f}, \"{name}\"]"
            markers.append(marker_line)
            
            lats.append(wpt.latitude)
            lons.append(wpt.longitude)

        if not markers:
            return None, None

        # Calculate Center (Average)
        center_lat = sum(lats) / len(lats)
        center_lon = sum(lons) / len(lons)

        # Join markers with newlines
        markers_str = "\n".join(markers)

        return markers_str, (center_lat, center_lon)

    except Exception as e:
        print(f"Error parsing {gpx_path}: {e}")
        return None, None

def write_map_note(base_name, dir_path, markers_str, center):
    map_filename = f"{base_name}{STATIC_SUFFIX}{MD_EXT}"
    map_path = os.path.join(dir_path, map_filename)
    
    # Generate unique ID based on filename to prevent caching collisions
    map_id = hashlib.md5(base_name.encode()).hexdigest()[:8]
    
    # --- THE TUTORIAL CONFIGURATION ---
    # This block is tuned to match standard Leaflet JS behavior.
    content = f"""---
related: "[[{base_name}]]"
tags:
  - auto-generated
---
> [!WARNING] DO NOT EDIT
> Auto-generated from GPX.

{TICKS}leaflet
id: map_{map_id}

# --- LOCATION ---
# Hardcoded center prevents "Africa" bug
lat: {center[0]:.6f}
long: {center[1]:.6f}
# Start zoomed in (Standard map view)
zoom: 13

# --- VISUALS ---
height: 600px
minZoom: 5
maxZoom: 18
osmLayer: true
# Fixes "Black Map" on Android Dark Mode
darkMode: false

# --- TUTORIAL BEHAVIOR (Standard Web Map) ---
# 1. lock: false 
#    Disables the "Note Scroll Protection". 
#    Allows one-finger interaction immediately.
lock: false

# 2. gestureHandling: false
#    Removes the "Use Ctrl + Scroll to zoom" or "Use two fingers" overlay.
gestureHandling: false

# 3. dragging: true
#    Explicitly enables panning.
dragging: true

# 4. scrollWheelZoom: true
#    Enables pinch-to-zoom on mobile.
scrollWheelZoom: true

# --- DATA ---
marker:
{markers_str}
{TICKS}
"""
    with open(map_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    root = os.getcwd()
    print(f"Scanning {root}...")
    
    count = 0
    # Walk through all subdirectories
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            if fname.lower().endswith('.gpx'):
                base_name = os.path.splitext(fname)[0]
                gpx_path = os.path.join(dirpath, fname)
                
                print(f"Processing: {fname}")
                markers_str, center = process_gpx(gpx_path)
                
                if markers_str:
                    # Write the map note in the SAME directory as the GPX
                    write_map_note(base_name, dirpath, markers_str, center)
                    count += 1
                    
                    # Ensure parent note exists
                    parent_path = os.path.join(dirpath, f"{base_name}{MD_EXT}")
                    if not os.path.exists(parent_path):
                         with open(parent_path, 'w', encoding='utf-8') as f:
                            f.write(f"---\nrelated: \"[[{base_name}{STATIC_SUFFIX}]]\"\n---\n# {base_name}\n\nNotes...")

    print(f"Done. Generated {count} standard maps.")

if __name__ == "__main__":
    main()
    