# culinary-recipe-architect

> Parent Skill Definition: [culinary-recipe-architect](file:///home/jpino/Obsidian/Cookbook/_Meta/Skills/culinary-recipe-architect/SKILL.md)

---
name: culinary-recipe-architect
description: "Governs multimodal recipe ingestion (NYT Cooking, YouTube, cookbook scans), physical cookbook indexing, 'Kenji Food Lab' culinary physics synthesis, dynamic ratio scaling, clean printable PDF generation, and production log lifecycle across the Cookbook vault."
---

# Culinary Recipe Architect & Ingestion Skill

## Overview
This skill governs the ingestion, synthesis, validation, printable PDF generation, and lifecycle management of culinary recipes, physical cookbook indices, and production logs in the **Cookbook** vault under **CBK-ADR-001** and **Level 4 Autonomous Agent Governance (ADR-036)**.

---

## Core Invariants & Governance Rules

### 1. Naming Standard & Suffix Conventions
* Recipes must use standard parenthetical suffixes for dietary modifications or major variants:
  * `(LG)` — Low-Glycemic optimization (e.g., `No-Knead Sourdough Bread (LG).md`, `Coffee Ice Cream (LG).md`)
  * `(GF)` — Gluten-Free optimization for celiac safety (e.g., `Caputo Pizza Dough (GF).md`, `Sourdough Pizza Crust (GF).md`)
  * `(LG, GF)` — Dual optimization (e.g., `Korean Beef Jerky (Yukpo) (LG, GF).md`)
  * `(SVQ)` — Sous-Vide-Que hybrid methods (e.g., `SVQ Pork Loin.md`)
* Do not use long descriptive title prefixes like `"Low-Glycemic Korean Beef Jerky"`. Use clean title + suffix.

### 2. Frontmatter Compliance (`obsidian-frontmatter-standard`)
* Every recipe must start on line 1 with isolated `---` delimiters and contain valid YAML.
* Standard properties:
  * `doc_type: recipe` (or `technique`, `log`, `cookbook`)
  * `status: active` | `draft`
  * `course`: `[main, snack, appetizer, side, dessert, breakfast, various]`
  * `method`: `[smoking, low_slow, grilling, high_heat, dehydrating, curing, baking, sous_vide, braising, stir_fry, various]`
  * `cuisine`: Capitalized string (e.g. `Korean`, `American`, `Spanish`, `Chinese`, `Italian`)
  * `region`: Capitalized string (e.g. `Texan`, `Californian`, `Cantonese`, `Andalusian`)
  * `diet`: `[low_glycemic, gluten_free]` (**Critical:** Keep lean; do NOT track medical conditions like hypertension or over-tag).
  * `main_ingredient`: Normalized string (e.g. `beef`, `pork`, `chicken`, `seafood`, `pizza`, `pasta`)
  * `hardware`: `[weber_searwood, weber_summit, camp_chef, deli_meat_slicer, cambro_container, stainless_meat_hooks, pizza_steel, anova_precision_cooker, bosch_induction, wok, dutch_oven]`
  * `source`: If from NYT, `source: NYT Cooking`. If from a physical book, quoted wikilink: `"[[Cookbook Title]]"`. If web, site/creator name.
  * `author`: Author or chef name (e.g. `J. Kenji López-Alt`, `Melissa Clark`).
  * `pages`: Integer or string (e.g. `163` or `240-241`) for physical cookbook page references.
  * `url`: Quoted HTTPS URL for online, YouTube, or NYT Cooking sources.
  * `aliases`: List of short names and search terms.

### 3. Multi-Modal Ingestion & NYT Cooking Protocol
* **NYT Cooking**:
  * Ingests via authenticated session cookies (`rss_cookies.json`).
  * Extracts JSON-LD schema (ingredients, step-by-step instructions, author, yield, high-res photo).
  * Automatically sets `source: NYT Cooking`, `url: '<URL>'`, and optimizes cover image to WebP.
* **YouTube Ingestion**:
  * Extracts transcript captions and harvests max-res cover thumbnail.
* **Physical Cookbook Scans**:
  * Automatically creates `Cookbook/Cookbooks/<Book Title>.md` if missing, embedding an Obsidian Base / Dataview query block.
* **Zero-Bloat Media Pipeline**:
  * Auto-converts all incoming user photos, scans, and attachments (JPEG/PNG/HEIC) to **WebP (quality 85, max 1600px)** in `Cookbook/_Meta/Attachments/media/<slug>_<timestamp>.webp`.

### 4. Ingredients Formatting Duality (Tables vs. Bulleted Lists)
* **Ratio Scaling Tables** (`| Ingredient | Per 1 lb Base Ratio | Current Cook (<Weight>) | Purpose / Function |`):
  * **Strictly reserved for mass-based recipes** (charcuterie, jerky, bacon cures, large primal BBQ cuts, bread percentages).
* **Hierarchical Bulleted Lists** (`- 2 cups flour`, `- 1 tbsp olive oil`):
  * **Mandatory standard for all standard, volumetric, and everyday recipes**.

### 5. Single-Column Dynamic Re-Scaling Protocol
* When requested to scale an existing mass-based recipe to a new batch weight:
  * Parse `Per 1 lb Base Ratio` column.
  * Update **only** the `Current Cook (<Weight>)` column and the `Batch Size` line in `## Specs`.
  * Leave all story, food lab science, execution protocols, and notes completely intact.

### 6. Clean Printable PDF Export Engine (`--pdf-export`)
* Generates an elegant, print-ready PDF via Playwright Chromium in `Cookbook/_Meta/Attachments/exports/<Title>.pdf`.
* **Sanitization Layer**:
  * Removes ephemeral `Current Cook (...)` columns from tables, preserving the clean base ratio and culinary purpose for guests.
  * Strips internal Obsidian Base query blocks and frontmatter YAML.
* **Attribution Layer**:
  * Prominently formats **Source**, **Author**, and active clickable **URL**.

### 7. Production Log Frontmatter & Core Base Invariant
* Production logs are stored in: `Cookbook/Daily Notes/YYYY-MM-DD <Description> Log.md`.
* Alias: `[YYYY-MM-DD <Short Name> Log]`.
* **Required Properties for Base Query Binding**:
  * `tags: [type/log, status/active]`
  * `doc_type: log`
  * `status: active`
  * `start_date: YYYY-MM-DD`
  * `related_recipes: ["[[Exact Canonical Recipe Name]]"]`

### 8. Dual-Link Instant Access Engine & URL Percent-Encoding
* **Native Obsidian URI**: `obsidian://open?vault=Cookbook&file=<Fully_Percent_Encoded_Path>`
  * **Critical:** Must encode parentheses `(` as `%28` and `)` as `%29` so Markdown link syntax `[Link](URL)` does not truncate at the first closing parenthesis.
* **Kern Web Publisher**: `https://kern.tailb08dba.ts.net/obsidian/view/Cookbook/<Path>.md`

