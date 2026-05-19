# KRB Vault Setup Guide

## Purpose
Instructions for setting up the KRB (Kern River Boater) vault for first-time users on desktop and mobile.

---

## Required Obsidian Plugins

This vault requires the following community plugins to render maps correctly:

### 1. **Leaflet** (obsidian-leaflet-plugin)
**Version**: 6.0.5+  
**Author**: Jeremy Valentine  
**Repository**: [valentine195/obsidian-leaflet-plugin](https://github.com/valentine195/obsidian-leaflet-plugin)

**Purpose**: Renders interactive GPX waypoint maps in markdown notes.

**Installation**:
1. Settings → Community Plugins → Browse
2. Search "Leaflet"
3. Install and Enable

**Settings** (already configured in `.obsidian/plugins/obsidian-leaflet-plugin/data.json`):
- Default tile server: CartoDB Voyager (high contrast for outdoor use)
- Dark mode: Disabled (prevents black maps on mobile)
- Mobile gestures: Single-finger panning enabled

### 2. **Dataview** (dataview)
**Version**: 0.5.68+  
**Author**: Michael Brenan  
**Repository**: [blacksmithgu/obsidian-dataview](https://github.com/blacksmithgu/obsidian-dataview)

**Purpose**: Powers dynamic queries and dashboards for filtering river content by tags.

**Installation**:
1. Settings → Community Plugins → Browse
2. Search "Dataview"
3. Install and Enable

---

## Plugin Settings Are Tracked in Git

The `.obsidian/plugins/` directory is **checked into git** so settings sync across devices:

- **Tracked**: Plugin manifests, settings (`data.json`), enabled plugin list
- **Not Tracked**: Workspace state, cache files (see `.gitignore`)

After cloning this repository:
1. Open the vault in Obsidian
2. Go to Settings → Community Plugins
3. Click "Enable" for Leaflet and Dataview
4. Settings will automatically load from git

---

## Mobile Setup (Android/iOS)

### Step 1: Install Obsidian Mobile
- Android: [Google Play Store](https://play.google.com/store/apps/details?id=md.obsidian)
- iOS: [App Store](https://apps.apple.com/us/app/obsidian-connected-notes/id1557175442)

### Step 2: Sync Vault to Mobile Device
Choose one of:

**Option A: Obsidian Sync** (Paid, $10/month)
- Best cross-platform experience
- Settings → Sync → Connect to vault

**Option B: Git-based sync** (Free, Technical)
- Use [Working Copy](https://workingcopy.app/) (iOS) or [Termux + git](https://wiki.termux.com/wiki/Main_Page) (Android)
- Clone this repository to Obsidian's vault folder

**Option C: Local folder sync** (Free, Desktop Required)
- Use iCloud Drive (iOS) or Google Drive (Android)
- Sync the vault folder from desktop
- Open in Obsidian Mobile

### Step 3: Enable Community Plugins on Mobile
1. Settings → Community Plugins → Enable Community Plugins
2. Leaflet and Dataview should appear in the list
3. Enable both plugins

### Step 4: Verify Map Rendering
1. Open `Kern/Lower Kern Rapids (Map).md`
2. Map should render with all waypoints visible
3. Test single-finger panning (no "use two fingers" prompt)
4. Test pinch-to-zoom

---

## Troubleshooting Mobile Maps

### Issue: Maps show "use two fingers to move the map"
**Fix**: The Leaflet plugin settings didn't sync. Manually disable gesture handling:
1. Settings → Leaflet → Gesture Handling: OFF
2. Close and reopen the map note

### Issue: Map is blank or black
**Cause**: Dark mode conflict with tile server  
**Fix**: Toggle Obsidian's appearance (Settings → Appearance → Dark Mode)

### Issue: Map is centered incorrectly (bounding box off)
**Cause**: Leaflet plugin version mismatch  
**Fix**: 
1. Ensure Leaflet plugin >= 6.0.5
2. If issue persists, regenerate maps:
   ```bash
   cd /path/to/KRB
   python _Meta/Scripts/refresh_gpx_maps.py
   ```

### Issue: No waypoints visible
**Cause**: GeoJSON file not loading  
**Fix**: Check that `San_Joaquin_Horseshoe_Bend.json` exists in same folder as map

---

## Updating Maps from GPX Files

If you add new `.gpx` files or modify existing ones:

### Automatic Regeneration
```bash
cd /path/to/KRB
python _Meta/Scripts/refresh_gpx_maps.py
```

This script:
1. Scans for all `.gpx` files in the vault
2. Converts waypoints to GeoJSON (`.json` data files)
3. Generates Leaflet map markdown (`(Map).md` files)
4. Only regenerates if GPX is newer than existing JSON

### Manual Workflow
If you prefer to manually parse RiverMaps GPX files:
```bash
cd /path/to/KRB/RiverMaps
python parseRiverMaps.py path/to/file.gpx
```
See `RiverMaps/README.md` for details on RiverMaps-specific processing.

---

## File Organization

```
KRB/
├── Kern/                           # Kern River waypoints
│   ├── Lower Kern Rapids.gpx      # Source GPX file
│   ├── Lower Kern Rapids.json     # Auto-generated GeoJSON
│   ├── Lower Kern Rapids (Map).md # Auto-generated Leaflet map
│   └── Lower Kern Rapids.md       # User notes (manual)
├── San Joaquin/                    # San Joaquin River waypoints
├── Rouge River/                    # Rogue River waypoints
├── RiverMaps/                      # RiverMaps GPX parser
│   ├── parseRiverMaps.py          # Garmin Instinct formatting
│   └── README.md                  # Parser documentation
├── _Meta/
│   ├── Scripts/
│   │   ├── refresh_gpx_maps.py    # GPX → GeoJSON + Leaflet
│   │   └── add_tags_to_markdown.py # Bulk tagging utility
│   ├── Schemas/
│   │   └── tag_schema.json        # Tag hierarchy definitions
│   └── 00_SOPs/
│       ├── Tagging_Strategy.md    # Tag usage guide
│       └── Setup_Guide.md         # This file
└── .obsidian/
    ├── plugins/
    │   ├── obsidian-leaflet-plugin/
    │   │   ├── manifest.json      # Plugin version
    │   │   └── data.json          # Settings (tracked in git)
    │   └── dataview/
    └── community-plugins.json     # Enabled plugins list
```

---

## Development Workflow

### Adding a New River Section

1. **Collect GPX data** (from Garmin device, RiverMaps, or field recording)

2. **Place GPX file** in appropriate folder:
   ```
   Kern/New_Section.gpx
   ```

3. **Generate maps**:
   ```bash
   python _Meta/Scripts/refresh_gpx_maps.py
   ```

4. **Review generated files**:
   - `New_Section.json` (GeoJSON data)
   - `New_Section (Map).md` (Leaflet visualization)

5. **Add tags** to `New_Section (Map).md` frontmatter:
   ```yaml
   ---
   tags:
     - type/map
     - river/kern/new_section
     - feature/rapid
     - difficulty/class_iii
     - region/california
     - status/needs_verification
   related: "[[New_Section.json]]"
   ---
   ```

6. **Test on mobile** before committing

7. **Commit to git**:
   ```bash
   git add Kern/New_Section.*
   git commit -m "Add New Section waypoints"
   ```

---

## License and Usage

This repository is **public** and intended for the whitewater paddling community.

- **GPX Data**: Field-verified waypoints are freely redistributable
- **RiverMaps Parser**: Local utility for personal Garmin device formatting (see `RiverMaps/README.md` for usage restrictions)
- **Scripts**: MIT License (see `LICENSE`)

⚠️ **Safety Disclaimer**: Whitewater navigation is inherently hazardous. GPS data may be inaccurate in canyons. Always scout rapids and use proper safety equipment.

---

**Last Updated**: 2026-05-19  
**Maintainer**: Jose Luis Pino  
**Repository**: [GitHub - Kern River Boaters](https://github.com/user/KRB)
