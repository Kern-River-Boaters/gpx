---
doc_type: dashboard
tags:
  - topic/recreation/whitewater
  - river/kern
created: 2026-08-19
status: active
---

# 🗺️ Kern River Basin Master Corridor Dashboard

> [!info] 🌊 Interactive River Corridor Map & Rapids Catalog
> This master dashboard dynamically displays all rapids, put-ins, take-outs, and campgrounds along the North Fork and Lower Kern River corridors using native **Obsidian Core Bases** with mobile gesture isolation.

---

## 🗺️ 1. Interactive River Corridor Map

```base
filters:
  and:
    - 'file.hasTag("river/kern")'
views:
  - type: map
    name: "Kern River Corridor Map"
    coordinates: coordinates
    icon: icon
    color: color
```

---

## 🌊 2. Rapids Catalog

```base
filters:
  and:
    - 'file.hasTag("feature/rapid")'
views:
  - type: table
    name: "Rapids Inventory"
    order:
      - file.name
      - section
      - coordinates
```

---

## ⛺ 3. Campgrounds & Access Points

```base
filters:
  or:
    - 'file.hasTag("feature/campground")'
    - 'file.hasTag("feature/access")'
views:
  - type: cards
    name: "Campgrounds & Access Points"
    order:
      - file.name
      - doc_type
```
