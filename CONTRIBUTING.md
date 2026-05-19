# Contributing to KRB River Boater GPX Collections

Thank you for your interest in contributing! This repository serves two distinct purposes:

1. **Curated GPX Collections** for rivers not covered by commercial guidebooks (Kern, etc.)
2. **Obsidian Vault** with interactive maps for desktop and mobile viewing

## Quick Start

### Prerequisites
- **Git** for version control
- **Python 3.7+** for GPX processing scripts
- **Obsidian** (desktop or mobile) for viewing/editing maps

### Setup
```bash
# Clone repository
git clone https://github.com/Kern-River-Boaters/gpx.git
cd gpx

# Install Python dependencies
pip install -r requirements.txt

# Open in Obsidian
# File → Open Folder as Vault → Select this directory
# Settings → Community Plugins → Enable: Leaflet, Dataview
```

## Types of Contributions

### 1. Adding New River Data

**Acceptable Sources:**
- Your own GPS tracks from personal trips
- Data from boaters who have explicitly granted permission
- Public domain datasets with proper attribution
- Files you've legally obtained and processed using our scripts

**Not Acceptable:**
- Copyrighted commercial guidebook data (RiverMaps, etc.) without permission
- GPS tracks from other boaters without explicit consent
- Data scraped from websites without permission

**Process:**
1. Create subdirectory: `River Name/`
2. Add GPX files with descriptive names (e.g., `Lower Kern Rapids.gpx`)
3. Run map generator: `python _Meta/Scripts/refresh_gpx_maps.py`
4. Add hierarchical tags to markdown files (see `_Meta/00_SOPs/Tagging_Strategy.md`)
5. Test on desktop and mobile Obsidian
6. Submit pull request with source attribution

### 2. Improving Scripts

**`RiverMaps/parseRiverMaps.py`** (Garmin Instinct formatting):
- Must maintain 15-character waypoint name limit
- Must split collections at 99 waypoints
- Cannot modify without testing on actual Garmin Instinct hardware

**`_Meta/Scripts/refresh_gpx_maps.py`** (Obsidian map generation):
- Must preserve single-file architecture (no separate `(Map).md` files)
- Must maintain auto-generated block markers for user content protection
- Must test on Windows desktop + Android mobile before submitting

**Testing Checklist:**
- [ ] Script runs without errors on sample data
- [ ] Generated files render correctly in Obsidian desktop
- [ ] Maps work on Android mobile (after app restart)
- [ ] User notes preserved (not overwritten by script)
- [ ] All existing tests still pass

### 3. Fixing Bugs

**Before submitting a fix:**
1. Check `_Meta/00_SOPs/` for documented limitations (may not be fixable)
2. Test on actual devices (not just your local environment)
3. Verify fix doesn't break existing functionality
4. Document any new limitations discovered

**Known Limitations (don't submit bugs for these):**
- Android touch gestures unreliable (Obsidian app issue, not our code)
- No layer toggle UI in Leaflet plugin (plugin limitation)
- "Show all markers" button doesn't work with GeoJSON-only maps

### 4. Improving Documentation

**Documentation Structure:**
- `README.md` - User-facing project overview and quick start
- `CLAUDE.md` - AI assistant instructions (architectural decisions, constraints)
- `_Meta/00_SOPs/` - Detailed troubleshooting and setup guides
- `_Meta/Tests/` - Reproducible test cases for plugin behavior

**When to add new SOP:**
- Discovered plugin limitation or workaround
- Mobile rendering issue and solution
- Setup steps not covered in existing docs

## Commit Message Guidelines

Use clear, descriptive commit messages:

```
Single-line summary starting with verb (Add, Fix, Update, Remove)

Optional body with:
- Why this change was needed
- What alternatives were considered
- Testing performed

Closes #123 (if applicable)
```

**Good Examples:**
```
Add Rogue River rapids with satellite imagery

Fix Android pinch zoom by adding explicit touchZoom parameter
Tested on Pixel 8 Pro - gestures now work after app restart

Document OpenTopoMap tile server failure
Added to tile server tests - returns 404 errors consistently
```

**Bad Examples:**
```
Fixed stuff
Updated files
WIP
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>  # Never include AI co-authorship
```

## Code Style

### Python
- Follow PEP 8 style guide
- Use 4 spaces for indentation
- Include module-level docstrings with design goals and dependencies
- Add inline comments only when logic is non-obvious
- Use type hints for function signatures

### Markdown
- Use 2 spaces for indentation
- Max line length: 120 characters (soft limit for readability)
- Use relative links to other files: `[Setup Guide](_Meta/00_SOPs/Setup_Guide.md)`
- Include code block language specifiers: ` ```python `, ` ```bash `

### GPX/GeoJSON
- Maintain coordinate precision: 6 decimal places (±0.11m accuracy)
- Use proper GeoJSON coordinate order: `[longitude, latitude]`
- Include descriptive names and descriptions for all waypoints

## Testing Requirements

### For Script Changes
```bash
# Test GPX to GeoJSON conversion
python _Meta/Scripts/refresh_gpx_maps.py

# Verify generated files
cat "Kern/Lower Kern Rapids.json"  # Check GeoJSON structure
cat "Kern/Lower Kern Rapids.md"   # Check Leaflet syntax
```

### For Map Rendering Changes
1. Open vault in Obsidian desktop
2. Verify maps render with all waypoints visible
3. Test on Android mobile (restart Obsidian app first)
4. Check touch gestures (pinch zoom, drag)
5. Verify both street and satellite maps work

### For Garmin Instinct Changes
1. Process test GPX with `parseRiverMaps.py`
2. Import to Garmin Explore app
3. Sync to actual Garmin Instinct watch
4. Verify waypoint names visible (<=15 chars)
5. Check rapid classifications displayed correctly

## Pull Request Process

1. **Fork the repository** and create a feature branch
2. **Make your changes** following the guidelines above
3. **Test thoroughly** on relevant devices
4. **Update documentation** if you changed behavior or added features
5. **Submit pull request** with clear description of changes
6. **Respond to feedback** from maintainers

**PR Description Template:**
```markdown
## What This Changes
Brief description of the change and why it's needed

## Type of Change
- [ ] New river data
- [ ] Bug fix
- [ ] Script improvement
- [ ] Documentation update
- [ ] Test addition

## Testing Performed
- [ ] Desktop Obsidian (Windows/Mac/Linux)
- [ ] Android mobile Obsidian
- [ ] iOS mobile Obsidian
- [ ] Garmin Instinct sync (if applicable)

## Screenshots
If UI/map changes, include before/after screenshots

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests pass
- [ ] Commit messages clear and descriptive
```

## Questions or Issues?

- **Bug reports:** Open an issue with reproduction steps and device info
- **Feature requests:** Open an issue describing use case and proposed solution
- **Questions:** Check `_Meta/00_SOPs/` first, then open a discussion

## License and Safety

By contributing, you agree that:
- Your contributions will be licensed under the same terms as this repository
- You have the legal right to contribute the data/code
- You've read and understand the liability disclaimers in `LICENSE`
- Whitewater boating is inherently dangerous; GPS data is for reference only

**Safety First:** This tool is for trip planning and beta reference. Always scout rapids in person, carry proper safety gear, and don't rely solely on GPS coordinates in narrow canyons where signal accuracy degrades.

---

Thank you for helping make this resource better for the whitewater community!
