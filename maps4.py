import os
import hashlib
import gpxpy # pip install gpxpy

# --- CONFIGURATION ---
STATIC_SUFFIX = " (Map)"
MD_EXT = ".md"
TICKS = "`" * 3

def get_mtime(path):
    if not os.path.exists(path): return 0
    return os.path.getmtime(path)

def process_gpx(gpx_path):
    try:
        with open(gpx_path, 'r', encoding='utf-8') as f:
            gpx = gpxpy.parse(f)

        if not gpx.waypoints:
            return None, None

        # 1. GENERATE MARKER LIST (Inline)
        # This creates the exact text format that worked in your manual test
        markers = []
        lats = []
        lons = []

        for wpt in gpx.waypoints:
            if wpt.latitude is None or wpt.longitude is None: continue
            
            # Clean Name
            name = wpt.name.strip().replace('"', '') if wpt.name else "Unnamed"
            
            # Append to list:  - [Lat, Lon, "Name"]
            markers.append(f"  - [{wpt.latitude}, {wpt.longitude}, \"{name}\"]")
            
            lats.append(wpt.latitude)
            lons.append(wpt.longitude)

        if not markers: return None, None

        # 2. CALCULATE CENTER
        # Simple average is safest for initial view
        center_lat = sum(lats) / len(lats)
        center_lon = sum(lons) / len(lons)

        # Join markers into a single string
        markers_str = "\n".join(markers)

        return markers_str, (center_lat, center_lon)

    except Exception as e:
        print(f"Error parsing {gpx_path}: {e}")
        return None, None

def write_map_note(base_name, dir_path, markers_str, center):
    map_filename = f"{base_name}{STATIC_SUFFIX}{MD_EXT}"
    map_path = os.path.join(dir_path, map_filename)
    
    # Unique Map ID
    map_id = hashlib.md5(base_name.encode()).hexdigest()[:8]
    
    # THE WORKING CONFIGURATION
    # We use the exact settings that worked in your sanity check.
    content = f"""---
related: "[[{base_name}]]"
tags:
  - auto-generated
---
> [!WARNING] DO NOT EDIT
> Auto-generated from GPX.

{TICKS}leaflet
id: map_{map_id}
# Center the map on the river
lat: {center[0]:.6f}
long: {center[1]:.6f}
zoom: 12

# Visuals
height: 600px
minZoom: 5
maxZoom: 18
osmLayer: true

# Mobile Controls (Unlocked)
lock: false
gestureHandling: false
dragging: true
scrollWheelZoom: true

# INLINE MARKERS (No external files to fail loading)
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
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            if fname.lower().endswith('.gpx'):
                base_name = os.path.splitext(fname)[0]
                gpx_path = os.path.join(dirpath, fname)
                
                # Always process to ensure fix
                print(f"Processing: {fname}")
                markers_str, center = process_gpx(gpx_path)
                
                if markers_str:
                    write_map_note(base_name, dirpath, markers_str, center)
                    count += 1
                    
                    # Create Parent Note if missing
                    parent_path = os.path.join(dirpath, f"{base_name}{MD_EXT}")
                    if not os.path.exists(parent_path):
                        with open(parent_path, 'w', encoding='utf-8') as f:
                            f.write(f"---\nrelated: \"[[{base_name}{STATIC_SUFFIX}]]\"\n---\n# {base_name}\n\nNotes...")

    print(f"Done. Generated {count} inline maps.")

if __name__ == "__main__":
    main()
    