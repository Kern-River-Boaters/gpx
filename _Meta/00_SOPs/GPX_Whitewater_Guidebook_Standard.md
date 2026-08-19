---
doc_type: sop
sop_id: SOP-KRB-001
status: approved
created: 2026-08-19
authors:
  - "[[Jose Luis Pino]]"
tags:
  - type/sop
  - topic/recreation/whitewater
  - topic/maps
---

# SOP-KRB-001: GPX Single Source of Truth & Section-Level Whitewater Guidebooks

> [!INFO] Purpose & Scope
> Standardizes the mapping architecture and information hierarchy across the **KRB (Kern River Basin)** vault. Establishes native GPX (`.gpx`) files as the sole authoritative geometry and waypoint single source of truth (SSOT), deprecates intermediate `.json` GeoJSON files, and organizes notes into rich **River Section Guidebooks**.

---

## 1. GPX Single Source of Truth Architecture

1. **Native GPS Ingestion**:
   * All river geometry, waypoints (`<wpt>`), and continuous track polylines (`<trk>`) originate directly from Garmin, Gaia GPS, or field survey devices as `.gpx` files in `KRB/Kern/`.
2. **Zero Intermediate GeoJSON Files**:
   * Redundant intermediate `.json` GeoJSON files are prohibited and removed.
   * Direct XML parsing is performed on the fly by `kern_publisher.py` and native `obsidian-leaflet-plugin`.
3. **Cross-Platform Compatibility**:
   * **Obsidian Desktop & Mobile**: Loaded via `gpx: [[FileName.gpx]]` in ````leaflet` blocks.
   * **Kern Publisher**: Preprocessed via `preprocess_leaflet_blocks` with sub-millisecond parsing and dual tile rendering.

---

## 2. River Section Guidebooks Hierarchy (Anti-Stub Rule)

Whitewater paddlers and river runners think in **Runs and River Sections**, not isolated 3-line stub files.

* **Mandatory Standard**:
  * Authoritative notes in `KRB/Kern/` represent complete river runs (e.g., `North Fork Kern Rapids.md`, `Lower Kern Rapids.md`, `Brush Creek.md`).
  * Each section guidebook embeds both **Street Map** (OpenStreetMap) and **Satellite Map** (Esri ArcGIS World Imagery) containers.
* **Prohibited**:
  * Auto-generating hundreds of individual rapid stubs that only contain a single coordinate and no beta. Major Class V signature drops (*Carson Falls*, *Vortex*, *Coffin Drop*) may receive dedicated profile notes only when rich scouting photography, hazard diagrams, and portage beta exist.

---

## 3. Map Block Configuration Standard

Each river section note MUST provide dual tile views with touch-isolated Leaflet markup:

````markdown
### Street Map
```leaflet
id: map_section_street
lat: 35.930665
long: -118.454626
zoom: 13
height: 600px
osmLayer: true
gpx: [[North Fork Kern Rapids.gpx]]
```

### Satellite Map
```leaflet
id: map_section_satellite
lat: 35.930665
long: -118.454626
zoom: 13
height: 600px
tileServer: https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}
gpx: [[North Fork Kern Rapids.gpx]]
```
````

---

## 4. Mobile Gesture Isolation

To prevent mobile scroll-trapping when scrolling long guidebooks on touchscreens (iOS / Android), map containers enforce:
* `scrollWheelZoom: false` (desktop)
* `touchZoom: true` (two-finger mobile pinch)
* Touch gesture containment allowing normal single-finger page scrolling.
