# Tagging Strategy - KRB Whitewater Guidebook

## Purpose
This document defines the tagging standards for the KRB repository. All markdown files (river guides, maps, tutorials) should use hierarchical tags for easy filtering and navigation.

## Core Principle
**Every tag must belong to a root hierarchy.** Never create loose tags like `#kern` or `#rapid` - always use the structured form: `#river/kern`, `#feature/rapid`.

---

## Tag Hierarchies

### 1. `type/` - Content Category
**Purpose**: Classify what kind of file this is.

**Common Values**:
- `type/gpx` - GPX waypoint files
- `type/map` - Markdown files with embedded maps
- `type/river_guide` - Comprehensive river guides
- `type/tutorial` - How-to guides and documentation
- `type/script` - Python scripts for processing
- `type/data` - JSON data files

**Rule**: Every file should have at least one `type/` tag.

---

### 2. `river/` - Specific River
**Purpose**: Identify which river system the content covers.

**Common Values**:
- `river/kern` - Kern River (general)
- `river/kern/upper` - Upper Kern (Forks of Kern to Johnsondale)
- `river/kern/lower` - Lower Kern (Kernville to Lake Isabella)
- `river/kern/north_fork` - North Fork of Kern
- `river/san_joaquin` - San Joaquin River
- `river/rogue` - Rogue River (Oregon)

**Rule**: Use underscores for multi-word river names. Add sub-hierarchies for major sections.

**Examples**:
```yaml
tags:
  - river/kern/upper
  - river/san_joaquin
```

---

### 3. `difficulty/` - Whitewater Classification
**Purpose**: Indicate the difficulty/class of rapids covered.

**Common Values**:
- `difficulty/class_i` - Class I (beginner)
- `difficulty/class_ii` - Class II
- `difficulty/class_iii` - Class III
- `difficulty/class_iv` - Class IV (advanced)
- `difficulty/class_v` - Class V (expert)
- `difficulty/class_ii_iii` - Class II-III range
- `difficulty/class_iii_iv` - Class III-IV range
- `difficulty/class_iv_v` - Class IV-V range

**Rule**: For content covering a range, use combined tags (e.g., `difficulty/class_ii_iii`).

---

### 4. `feature/` - River Features
**Purpose**: Categorize what type of waypoints or features are included.

**Common Values**:
- `feature/rapid` - Rapids and drops
- `feature/campground` - Camping areas
- `feature/access` - Put-ins and take-outs
- `feature/parking` - Parking areas and trailheads
- `feature/hazard` - Portages, sieves, dangerous features
- `feature/poi` - Points of interest (waterfalls, hot springs, landmarks)
- `feature/milestone` - River miles, gauges, confluences

**Rule**: Use multiple feature tags if the file contains multiple types.

**Example**:
```yaml
tags:
  - feature/rapid
  - feature/campground
  - feature/access
```

---

### 5. `season/` - Paddling Season
**Purpose**: Indicate when the river is typically run.

**Common Values**:
- `season/spring_runoff` - Spring snowmelt (high flows)
- `season/summer` - Summer flows
- `season/fall` - Fall flows
- `season/winter` - Winter flows
- `season/year_round` - Runnable year-round

**Rule**: Use for content that's season-specific. Many rivers are `season/year_round`.

---

### 6. `region/` - Geographic Region
**Purpose**: Organize by geography for discovery.

**Common Values**:
- `region/california` - California
- `region/sierra_nevada` - Sierra Nevada mountains
- `region/southern_california` - Southern California
- `region/oregon` - Oregon

**Rule**: Use multiple region tags to nest (e.g., Kern River gets both `region/california` and `region/sierra_nevada`).

---

### 7. `flow/` - Flow Conditions
**Purpose**: Tag content specific to flow levels.

**Common Values**:
- `flow/low` - Low flow conditions
- `flow/medium` - Medium/optimal flows
- `flow/high` - High flow conditions
- `flow/flood` - Flood stage (dangerous)

**Rule**: Optional - use when content is flow-specific (e.g., "high flow beta").

---

### 8. `status/` - Data Verification Status
**Purpose**: Track data accuracy and currency.

**Common Values**:
- `status/verified` - Field-verified, accurate
- `status/needs_verification` - Untested, needs field check
- `status/outdated` - Old data needing updates
- `status/draft` - Work in progress

**Rule**: Tag new/untested data with `status/needs_verification` until field-verified.

---

## Tagging Patterns by Content Type

### GPX Collection (with Map)
```yaml
---
tags:
  - type/gpx
  - type/map
  - river/kern/upper
  - feature/rapid
  - difficulty/class_iii_iv
  - region/california
  - region/sierra_nevada
  - season/year_round
  - status/verified
---
```

### River Access Points
```yaml
---
tags:
  - type/map
  - river/kern
  - feature/access
  - feature/parking
  - region/california
---
```

### Tutorial/Documentation
```yaml
---
tags:
  - type/tutorial
  - type/documentation
---
```

### Python Script
```yaml
---
tags:
  - type/script
---
```

---

## Frontmatter Standards

**Minimal frontmatter**:
```yaml
---
tags:
  - type/[type]
  - river/[river]
  - feature/[feature]
---
```

**Extended frontmatter** (for GPX collections):
```yaml
---
tags:
  - type/gpx
  - type/map
  - river/kern/upper
  - feature/rapid
  - difficulty/class_iii_iv
  - region/california
  - season/year_round
  - status/verified
river_section: "Upper Kern"
difficulty_range: "Class III-IV"
waypoint_count: 42
last_verified: 2026-05-15
---
```

---

## AI Assistant Instructions

> **Superseded.** Full AI/LLM guidance for tagging, auditing, and content standards is now in `_Meta/VAULT_CONTEXT.md`. That file is the single source of truth for LLM context in this vault.

For quick reference: load `_Meta/VAULT_CONTEXT.md` (Section 4 for tag hierarchy, Section 6 for inference heuristics, Section 7 for audit rules) before tagging any KRB content.

---

## Tag Maintenance

### Adding New Rivers
1. Add river mapping to schema: `"#NewRiver": "river/new_river"`
2. Document in this SOP under river hierarchy
3. Tag all related files consistently

### Adding New Regions
1. Add region to schema
2. Update existing river files with regional tags
3. Use multiple region tags for geographic nesting

---

## Anti-Patterns (What NOT to Do)

❌ **Don't**: Create flat tags like `#kern`, `#rapid`, `#class-iv`  
✅ **Do**: Use `#river/kern`, `#feature/rapid`, `#difficulty/class_iv`

❌ **Don't**: Mix plurals/singulars (`#rapids` vs `#rapid`)  
✅ **Do**: Always use singular: `#feature/rapid`

❌ **Don't**: Create personal/work tags (`#keysight`, `#personal`)  
✅ **Do**: Keep tags relevant to whitewater navigation only

❌ **Don't**: Tag with inconsistent river names  
✅ **Do**: Follow schema exactly: `river/kern` not `river/kern_river`

---

## Dataview Query Examples

**All Kern River content**:
```dataview
LIST
FROM #river/kern
SORT file.name ASC
```

**Class IV rapids on any river**:
```dataview
TABLE river_section, difficulty_range
FROM #difficulty/class_iv
SORT file.name ASC
```

**Verified campground data**:
```dataview
LIST
FROM #feature/campground AND #status/verified
```

---

**Last Updated**: 2026-05-19  
**Maintainer**: Jose Luis Pino  
**Repository**: Public GitHub (Kern River Boaters)  
**Schema Location**: `_Meta/Schemas/tag_schema.json`
