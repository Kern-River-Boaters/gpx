import os
import time
import json
import xml.etree.ElementTree as ET
import hashlib

# --- CONFIGURATION ---
STATIC_SUFFIX = " (Map)"
MD_EXT = ".md"
JSON_EXT = ".json"
TICKS = "`" * 3

def get_file_mtime(path):
    return os.path.getmtime(path)

def parse_gpx_to_features(filepath):
    """Parses GPX and returns a list of GeoJSON features and the center point."""
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        features = []
        lats = []
        lons = []
        
        for wpt in root.findall(".//{*}wpt"):
            lat_str = wpt.get('lat')
            lon_str = wpt.get('lon')
            if lat_str and lon_str:
                lat = float(lat_str)
                lon = float(lon_str)
                name_tag = wpt.find(".//{*}name")
                raw_name = name_tag.text if name_tag is not None else "Unnamed"
                safe_name = raw_name.replace('"', '').strip()
                
                # GeoJSON Structure for a single point
                feature = {
                    "type": "Feature",
                    "properties": {
                        "name": safe_name,
                        "desc": safe_name # Shows in tooltip
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lon, lat] # GeoJSON uses [Lon, Lat] order!
                    }
                }
                features.append(feature)
                lats.append(lat)
                lons.append(lon)
            
        if not features:
            return [], (0, 0)
            
        avg_lat = sum(lats) / len(lats)
        avg_lon = sum(lons) / len(lons)
        return features, (avg_lat, avg_lon)
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        return [], (0, 0)

def generate_static_map(base_name, json_filename, center_coords):
    """Generates the Markdown file that LOADS the JSON file."""
    avg_lat, avg_lon = center_coords
    map_hash = hashlib.md5(base_name.encode()).hexdigest()[:8]
    
    # We simply link to the JSON file. 
    # Note: We use osmLayer: true because that was the one that worked for you.
    content = f"""---
related: "[[{base_name}]]"
tags:
  - auto-generated
---
> [!WARNING] DO NOT EDIT
> This file reads data from [[{json_filename}]]. 

{TICKS}leaflet
id: map_{map_hash}
lat: {avg_lat:.6f}
long: {avg_lon:.6f}
zoom: 11
height: 600px
osmLayer: true
geojson: [[{json_filename}]]
{TICKS}
"""
    return content

def generate_main_note(static_filename_base):
    return f"""---
related: "[[{static_filename_base}]]"
---
# {static_filename_base.replace(STATIC_SUFFIX, "")}

Your manual notes go here.
"""

def scan_and_refresh(root_dir):
    print(f"Scanning: {root_dir}")
    count_updated = 0
    
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(".gpx"):
                base_name = os.path.splitext(filename)[0]
                gpx_path = os.path.join(dirpath, filename)
                
                # Define filenames
                json_filename = f"{base_name}{JSON_EXT}"
                static_md_name = f"{base_name}{STATIC_SUFFIX}{MD_EXT}"
                main_md_name = f"{base_name}{MD_EXT}"
                
                json_path = os.path.join(dirpath, json_filename)
                static_path = os.path.join(dirpath, static_md_name)
                main_path = os.path.join(dirpath, main_md_name)
                
                # Logic: Refresh if GPX is newer than JSON file
                should_update = True 
                if not os.path.exists(json_path) or not os.path.exists(static_path):
                    should_update = True
                elif get_file_mtime(gpx_path) > get_file_mtime(json_path):
                    should_update = True
                
                if should_update:
                    print(f"Processing: {filename}")
                    features, center = parse_gpx_to_features(gpx_path)
                    
                    if features:
                        # 1. Create JSON Data File
                        geojson_data = {
                            "type": "FeatureCollection",
                            "features": features
                        }
                        with open(json_path, "w", encoding="utf-8") as f:
                            json.dump(geojson_data, f, indent=2)
                        
                        # 2. Create Static Map Markdown
                        content = generate_static_map(base_name, json_filename, center)
                        with open(static_path, "w", encoding="utf-8") as f:
                            f.write(content)
                            
                        count_updated += 1

                # 3. Create Main Note if missing
                if not os.path.exists(main_path):
                    content = generate_main_note(f"{base_name}{STATIC_SUFFIX}")
                    with open(main_path, "w", encoding="utf-8") as f:
                        f.write(content)

    print(f"Done. Updated {count_updated} sets.")

if __name__ == "__main__":
    scan_and_refresh(os.getcwd())
    