# River Boater GPX Collections for Garmin Instinct

[![License](https://img.shields.io/badge/license-Copyrighted%20/%20Free%20Use-blue.svg)](LICENSE)
*Please read the full [LICENSE](LICENSE) for liability shields, whitewater safety warnings, and canyon GPS accuracy limitations before using these files.*

This repository contains a curated library of pre-processed GPX collections for rivers like the **Kern and others** that are not covered by commercial guidebooks. I have collected these files from local boaters and sources who have granted permission, and they are fully cleared for public redistribution here. 

All curated files in this repo are pre-optimized specifically for the Garmin Instinct series to ensure critical information remains visible on the water.

## Why This Tool Exists

On multi-day river trips, rafters often have the luxury of flipping through a physical RiverMaps guidebook to track upcoming rapids, monitor progress, and read beta. As a kayaker, you don't have that freedom—you need your hands on the paddle and your eyes on the line. 

This project was born out of the need to know exactly where you are and what is coming up next without fumbling with wet paper maps. It leverages the Garmin Instinct’s high-visibility, high-contrast screen and wrist-based waypoint navigation feature. By processing raw data into shortened, descriptive tags, you can drop your eyes to your wrist mid-river and instantly see the classification and distance of the upcoming rapid.

## Garmin Instinct & Explore Limitations

The `parseRiverMaps.py` script included in this repo specifically designs around the unique hardware constraints of the Garmin Instinct series (including the Instinct 1, 2, 2X, and 3) and the quirks of the Garmin Explore platform:

* **15-Character Name Limit & Smart Abbreviation:** The Garmin Instinct display aggressively truncates waypoint names on its map data fields and navigation lists. If a waypoint name is too long, the watch cuts it off, often hiding the vital rapid classification. To fix this, the script derives a highly readable, shortened name directly from the original long name:
    * **Category Sorting:** The script reads the prepended two-character prefix in the original name (`R-` for Rapids, `C-` for Campgrounds, `P-` for Points of Interest, and `M-` for Mile Markers) to sort them into clean, separate files. This allows you to easily assign distinct custom icons for each category in Garmin Explore.
    * **Space/Vowel-Stripping & Beta Extraction:** It then completely slices *off* that two-character prefix, removes all spaces by capitalizing the first letter of each word, and extracts the numerical rapid rating from the description text. To guarantee everything fits perfectly within the strict 15-character constraint without losing readability, the script calculates the remaining space. If the name is too long, it dynamically strips out the vowels (while keeping the very first letter intact so the word shapes remain recognizable) and appends the rapid class directly to the end. For example, a long waypoint originally named `R-Granite Gorge Rapid` with a `(Class 5)` description is elegantly compressed into **`GrntGrgRpd5`**. 
* **The 99-Waypoint Sync Threshold:** Garmin Explore explicitly flags any collection with over 100 waypoints as a "large collection," which can trigger app warnings or cause the sync pipeline to fail entirely. The script splits data into clean, manageable collections capped at exactly 99 waypoints each, sitting safely under the limit.

---

## Instructions for Our Curated Collections
To import the pre-built, curated collections provided in this repo, follow these steps:

1. On your Garmin watch, add the map view for your kayak activity profile.
2. Import each file as a new collection using the **Garmin Explore** app or web portal. Note that you can import the waypoint files as either Tracks or Routes.
3. **Manually Bulk-Assign Icons:** Because the standard GPX schema does not reliably map proprietary Garmin icons during an import, Garmin Explore will often default your waypoints to generic pins. To fix this, tap "Select All" within your newly imported collection inside the Garmin Explore app, and manually set the proper high-visibility icon (e.g., a tent for camps, a rapid symbol for rapids). Icons that render beautifully on the Instinct's dual-window display include:

![Garmin Icons](_Meta/Attachments/garmin-icons.png)

---

## Processing Your Own RiverMaps GPX Data 

For rivers that have an official RiverMaps guidebook (such as the Salt, Grand Canyon, Green, etc.), I do not host or curate those files here because RiverMaps already does an excellent job maintaining them. You can download their official GPS waypoint files for public download at no charge directly from their site:
**[RiverMaps GPS Waypoints Download](https://rivermaps.net/pages/gps-waypoints)**

To assist with your own preprocessing of those files, I’ve included the `parseRiverMaps.py` script in this repository. 

**Note:** *This script was built and tested specifically for formatting RiverMaps GPX files only.* It automates breaking apart their specific GPX structure, extracting the rapid class from the descriptions, and compressing the names for Garmin compatibility.

### ⚠️ Legal Disclaimer for `parseRiverMaps.py`
> This repository does not host or distribute proprietary data from commercial publishers like RiverMaps. To use the `parseRiverMaps.py` tool on external RiverMaps files, you must acquire your own raw files directly from the link above and accept their Terms and Conditions, which prohibit copying or distributing their files. The script is provided strictly for your personal use to format coordinate data and generic waypoint names for physical device limitations; it is not meant to bypass copyright on creative descriptions, proprietary notes, or subjective hazard warnings.

---

## Using This Vault in Obsidian

This repository is also structured as an **Obsidian vault** with interactive GPX waypoint maps that work on desktop and mobile.

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/user/KRB.git
   cd KRB
   ```

2. **Open in Obsidian**:
   - File → Open Folder as Vault → Select `KRB/`

3. **Install required plugins**:
   - Settings → Community Plugins → Browse
   - Install and enable: **Leaflet** and **Dataview**

4. **View interactive maps**:
   - Open any river markdown file (e.g., `Kern/Lower Kern Rapids.md`)
   - Each file contains both street and satellite map views
   - Maps render with all waypoints and support zooming and panning

For detailed setup instructions (including mobile configuration), see [`_Meta/00_SOPs/Setup_Guide.md`](_Meta/00_SOPs/Setup_Guide.md).

### ⚠️ Android Mobile Touch Controls
Touch gestures on Android can be unreliable due to conflicts between Obsidian's mobile gesture handlers and the Leaflet map webview. **Workaround:** Completely close and restart the Obsidian app before viewing maps. This clears the gesture cache and restores proper touch controls for that session.

See [`_Meta/00_SOPs/Android_Touch_Controls_Known_Issues.md`](_Meta/00_SOPs/Android_Touch_Controls_Known_Issues.md) for detailed troubleshooting.

### Updating Maps from GPX Files

If you add new `.gpx` files or modify existing ones:

```bash
# Install Python dependencies (first time only)
pip install -r requirements.txt

# Regenerate all maps
python _Meta/Scripts/refresh_gpx_maps.py
```

This automatically:
- Converts GPX waypoints to GeoJSON (`.json` data files)
- Generates Leaflet map markdown (`(Map).md` files)
- Only updates maps if GPX source is newer than existing JSON

---

## Repository Structure

```
KRB/
├── Kern/                           # Kern River waypoints
│   ├── Lower Kern Rapids.gpx      # Source GPX file
│   ├── Lower Kern Rapids.json     # Auto-generated GeoJSON
│   └── Lower Kern Rapids.md       # User notes + embedded street/satellite maps
├── San Joaquin/                    # San Joaquin River waypoints
├── Rouge River/                    # Rogue River waypoints
├── RiverMaps/                      # RiverMaps GPX parser (Garmin Instinct)
│   └── parseRiverMaps.py          # 15-char name compression, 99-waypoint splitting
├── _Meta/                          # Vault infrastructure
│   ├── Scripts/
│   │   ├── refresh_gpx_maps.py    # GPX → GeoJSON + Leaflet converter
│   │   └── add_tags_to_markdown.py # Bulk tagging utility
│   ├── Schemas/
│   │   └── tag_schema.json        # Hierarchical tag definitions
│   ├── Tests/                      # Leaflet plugin capability tests
│   │   ├── Test_LayerControl.md   # Layer switching tests
│   │   ├── Test_MapView.md        # Map View plugin tests
│   │   └── Test_TileLayers.md     # Tile server tests
│   └── 00_SOPs/
│       ├── Setup_Guide.md                      # Plugin installation, mobile setup
│       ├── Android_Touch_Controls_Known_Issues.md  # Android gesture troubleshooting
│       └── Tagging_Strategy.md                 # Tag usage guide
├── .obsidian/                      # Obsidian configuration (tracked in git)
│   ├── plugins/                   # Leaflet and Dataview settings
│   └── community-plugins.json     # Enabled plugins list
├── requirements.txt                # Python dependencies
├── KRB.code-workspace             # VS Code workspace configuration
├── CLAUDE.md                       # AI assistant context
├── LICENSE                         # Liability disclaimers
└── README.md                       # This file
```

---

