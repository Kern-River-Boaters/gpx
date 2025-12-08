import os
import time
import xml.etree.ElementTree as ET
import hashlib

# --- CONFIGURATION ---
STATIC_SUFFIX = " (Map)"
MD_EXT = ".md"
TICKS = "`" * 3

def get_file_mtime(path):
    return os.path.getmtime(path)

def parse_gpx(filepath):
    """Parses GPX to extract waypoints."""
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        waypoints = []
        lats = []
        lons = []
        
        # Find all waypoints regardless of namespace
        for wpt in root.findall(".//{*}wpt"):
            lat_str = wpt.get('lat')
            lon_str = wpt.get('lon')
            if lat_str and lon_str:
                lat = float(lat_str)
                lon = float(lon_str)
                name_tag = wpt.find(".//{*}name")
                raw_name = name_tag.text if name_tag is not None else "Unnamed"
                safe_name = raw_name.replace('"', '').strip() # Removed quotes for safety
                
                # Format: - [lat, lon, "name"]
                waypoints.append(f"  - [{lat}, {lon}, \"{safe_name}\"]")
                lats.append(lat)
                lons.append(lon)
            
        if not waypoints:
            return [], (0, 0)
            
        avg_lat = sum(lats) / len(lats)
        avg_lon = sum(lons) / len(lons)
        return waypoints, (avg_lat, avg_lon)
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        return [], (0, 0)

def generate_static_content(base_name, waypoints, center_coords):
    """Generates the content for the STATIC map file."""
    avg_lat, avg_lon = center_coords
    markers_str = "\n".join(waypoints)
    map_hash = hashlib.md5(base_name.encode()).hexdigest()[:8]
    
    # UPDATED: Uses Esri Satellite provider and disables Dark Mode
    content = f"""---
related: "[[{base_name}]]"
tags:
  - auto-generated
---
> [!WARNING] DO NOT EDIT
> This file is automatically regenerated.

{TICKS}leaflet
id: map_{map_hash}
lat: {avg_lat:.6f}
long: {avg_lon:.6f}
zoom: 11
height: 600px
minZoom: 5
maxZoom: 18
osmLayer: false
tileServer: https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}
darkMode: false
marker:
{markers_str}
{TICKS}
"""
    return content

def generate_main_content(static_filename_base):
    return f"""---
related: "[[{static_filename_base}]]"
---
# {static_filename_base.replace(STATIC_SUFFIX, "")}

Your notes here.
"""

def scan_and_refresh(root_dir):
    print(f"Scanning: {root_dir}")
    count_updated = 0
    
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(".gpx"):
                base_name = os.path.splitext(filename)[0]
                gpx_path = os.path.join(dirpath, filename)
                static_path = os.path.join(dirpath, f"{base_name}{STATIC_SUFFIX}{MD_EXT}")
                main_path = os.path.join(dirpath, f"{base_name}{MD_EXT}")
                
                # Logic: Update if GPX is newer OR if static file doesn't exist
                should_update = True
                if not os.path.exists(static_path):
                    should_update = True
                elif get_file_mtime(gpx_path) > get_file_mtime(static_path):
                    should_update = True
                
                if should_update:
                    print(f"Regenerating map for: {filename}")
                    markers, center = parse_gpx(gpx_path)
                    if markers:
                        content = generate_static_content(base_name, markers, center)
                        with open(static_path, "w", encoding="utf-8") as f:
                            f.write(content)
                        count_updated += 1

                # Ensure main note exists
                if not os.path.exists(main_path):
                    content = generate_main_content(f"{base_name}{STATIC_SUFFIX}")
                    with open(main_path, "w", encoding="utf-8") as f:
                        f.write(content)

    print(f"Done. Updated {count_updated} maps.")

if __name__ == "__main__":
    scan_and_refresh(os.getcwd())
    