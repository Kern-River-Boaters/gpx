# KRB Vault — Claude Code / Developer Guide

## Vault Identity
- **Purpose**: Whitewater kayaking GPS tools and river guides for Garmin Instinct devices
- **Repository**: Public GitHub (`Kern-River-Boaters/gpx`)
- **Scope**: Open-source community resource — everything is public, no confidential data
- **Architecture**: Public spoke in maintainer's federated Obsidian system

## AI / LLM Context
> For all LLM content work (tagging, auditing, generating river guide content), use `_Meta/VAULT_CONTEXT.md`.
> CLAUDE.md is for Claude Code / developer use only.

---

## Federation Map

| Vault | Purpose | Repo |
|---|---|---|
| **Common** (hub) | Governance & shared standards | Public GitHub |
| **KNotes** | Keysight work — CONFIDENTIAL | Keysight Bitbucket |
| **Cookbook** | Culinary recipes | Public GitHub |
| **Notes** | Personal life management | Private GitHub |
| **KRB** | Whitewater recreation — YOU ARE HERE | Public GitHub |

---

## Directory Structure

```
KRB/
├── Kern/                    # Kern River waypoints (.gpx, .json, .md triplets)
├── San Joaquin/             # San Joaquin River waypoints
├── Rouge River/             # Rogue River (Oregon) waypoints
├── RiverMaps/               # parseRiverMaps.py — Garmin Instinct formatter
├── _Meta/
│   ├── Schemas/             # obsidian_tag_refactor.json
│   ├── Scripts/             # refresh_gpx_maps.py, add_tags_to_markdown.py
│   ├── 00_SOPs/             # Plugin limitations, tagging guide, setup guide
│   ├── Tests/               # Leaflet plugin test cases
│   ├── Attachments/         # Images and media
│   └── VAULT_CONTEXT.md     # LLM/AI content context (authoritative)
├── CLAUDE.md                # This file
├── README.md                # Public-facing documentation
└── CONTRIBUTING.md          # Community contribution guidelines
```

---

## Technical Code Guidelines

### `parseRiverMaps.py` (Garmin Instinct Formatting)

- **No proprietary data in this repo.** Script is a local formatter; users supply their own legally obtained RiverMaps GPX files.
- **Cross-vault processing:** Maintainer's private RiverMaps data lives in Notes vault, not here. Scripts process external paths:
  ```bash
  python _Meta/Scripts/parseRiverMaps.py \
    --input "/c/Obsidian/Notes/Recreation/Kayaking/Private_RiverMaps/[file].gpx" \
    --output "/c/Obsidian/Notes/Recreation/Kayaking/Private_RiverMaps/Garmin_Formatted/"
  ```
- **15-character limit:** Names use PascalCase + vowel stripping + hard truncate to stay ≤15 chars.
- **99-waypoint split:** Collections capped at 99 to stay under Garmin Explore's "large collection" threshold.
- **Prefix stripping:** 2-char category prefixes (`R-`, `C-`, `P-`, `M-`) are sliced off. Beta extracted from description via regex `r"(\(\w*)([0-9]+)(\w*\))"`.

### `refresh_gpx_maps.py` (Obsidian Leaflet Maps)

- **Single-file architecture:** Each river section has one `.md` file — no separate `(Map).md` files.
- **Auto-generated block:** Maps enclosed in `<!-- BEGIN AUTO-GENERATED MAP -->` / `<!-- END AUTO-GENERATED MAP -->`. Script regenerates only this block; user notes above/below are preserved.
- **Dual maps:** Each file has both OpenStreetMap (street) and Esri World Imagery (satellite). No layer toggle — plugin doesn't support it.
- **GeoJSON external files:** Waypoints in `.json` files, referenced via `geojson: [[filename.json]]`. Inline markers break with HTML comment markers.
- **Bounding box:** `BBOX_BUFFER = 0.003` (~300m padding).
- **Required touch parameters (Android):**
  ```yaml
  dragging: true
  gestureHandling: false
  scrollWheelZoom: true
  touchZoom: true
  doubleClickZoom: true
  ```
- **`showAllMarkers: false`:** Button is broken with GeoJSON-only maps (zooms to 0,0).
- **Zoom levels:** `minZoom: 5`, `maxZoom: 20`, calculated default 11–15.

---

## Obsidian Leaflet Plugin Constraints

Confirmed through exhaustive testing — do not revisit without strong justification:

- **No layer control:** Plugin does not support `baseMaps`, `image` parameter, or `layers` array.
- **Tile server format:** Single string, `{z}/{y}/{x}` not `{{z}}/{{y}}/{{x}}`.
- **GeoJSON only with protected blocks:** Inline `marker:` arrays cannot coexist with HTML comment markers.
- **Android touch issues:** Conflict with Obsidian mobile gesture handlers. Workaround: restart Obsidian app. See `_Meta/00_SOPs/Android_Touch_Controls_Known_Issues.md`.

---

## Git Workflow

- **Branch:** `master` (not `main`)
- **Remote:** `origin` = `git@github.com:Kern-River-Boaters/gpx.git`
- **Commit format:** Single-line summary starting with verb (Add, Fix, Update, Remove, Document), max 72 chars. Body optional.
- **Do NOT add** `Co-Authored-By: Claude` or similar AI co-authorship lines to commits.
- **Force push:** Only for history rewriting/squash cleanup. Always warn before force pushing.

---

## Community Contribution Guidelines

See `CONTRIBUTING.md` for full details. Summary:

- GPX data submitted must be field-verified with GPS coordinates confirmed on the river
- New rivers follow the folder + triplet pattern: `[River Name]/[Section].gpx/.json/.md`
- Run `python _Meta/Scripts/refresh_gpx_maps.py` after adding or modifying GPX files
- Test maps on both desktop Obsidian and Android mobile before committing
- Never commit private RiverMaps data — redistribute only community-sourced or free waypoints
- Always preserve safety disclaimers in README and LICENSE

---

## Python Script Development

- **Style:** Module docstring, constants at top, type hints for function signatures, graceful error handling.
- **Dependencies:** Minimal. Current stack: `gpxpy`, `geojson`. Document additions in `requirements.txt`.
- **File naming:** `lowercase_with_underscores.py`.

---

## Testing Checklist for Map Changes

Before committing changes to map generation:

- [ ] Maps render on Windows desktop Obsidian
- [ ] Maps render on Android mobile (after app restart)
- [ ] Waypoints appear at correct locations
- [ ] Bounding box centers on waypoints (not world map)
- [ ] Touch zoom works on mobile (two-finger pinch)
- [ ] Dragging works on mobile (one-finger pan)
- [ ] Both street and satellite maps functional
- [ ] Auto-generated block preserved after re-running script
- [ ] User notes above/below auto-generated block untouched

---

## Common Tasks

### Regenerate all maps after GPX changes
```bash
python _Meta/Scripts/refresh_gpx_maps.py
```

### Add a new river section
```bash
mkdir "River Name"
# Add GPX files to River Name/
python _Meta/Scripts/refresh_gpx_maps.py
# Add tags using _Meta/Scripts/add_tags_to_markdown.py
```

### Test Leaflet plugin behavior
1. Create test file in `_Meta/Tests/Test_NewFeature.md`
2. Add multiple test cases with different syntax
3. Document results inline
4. Update relevant SOP if limitation confirmed

---

## Resources

- **Leaflet Plugin:** https://github.com/javalent/obsidian-leaflet
- **GeoJSON spec:** https://geojson.org/ (coordinate order: `[longitude, latitude]`)
- **Tile servers:** Esri World Imagery (satellite), CartoDB Voyager (street) — both tested and working
- **Garmin Instinct constraints:** Script header in `RiverMaps/parseRiverMaps.py`
- **Android touch issues:** `_Meta/00_SOPs/Android_Touch_Controls_Known_Issues.md`

---

**Last Updated:** 2026-06-13
