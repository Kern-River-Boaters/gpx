# obsidian-bases

> Parent Skill Definition: [obsidian-bases](file:///home/jpino/Obsidian/Common/_Meta/Skills/obsidian-bases/SKILL.md)

---
name: obsidian-bases
description: "Use ONLY when writing, editing, or validating Obsidian Core Base (.base) files, embedded base code blocks, or vault property types (.obsidian/types.json). Enforces official obsidian-help corpus syntax standards: expression-based filters, property configuration maps, formula link transformations, and internal multitext property type definitions."
---

# Skill: Obsidian Core Bases Syntax & Vault Property Standard (Official Corpus Reference)

> [!INFO] Live Corpus Documentation
> Official Obsidian documentation reference: [Obsidian Core Bases Specification](references/obsidian-help/en/Bases)

When creating or editing Obsidian Core Base files (`.base`), embedded base code blocks (` ```base `), or vault property configurations (`.obsidian/types.json`), follow these first principles derived directly from the official `obsidian-help` corpus and vault runtime verification:

---

## 1. Core Base Syntax Rules (`.base` files)

1. **No `from` or `source` Clause**:
   - Bases automatically scan the entire vault by default. Never include SQL-style `from` or `source` clauses.

2. **Expression-Based Filters (`filters:`)**:
   - Filters evaluate as string expressions (e.g., `- "reconciliation_status == 'merged_pending_review'"`).
   - **Prohibited**: Verbose dictionary objects like `field: ..., operator: equals, value: ...`.

3. **Property Configuration Maps (`properties:`)**:
   - The `properties:` block is a dictionary/object mapping property keys to configuration maps (such as assigning display names: `displayName: "Display Title"`).
   - **Strict Rule**: Only `displayName` is allowed under `properties:`. Do NOT put `type:` or `options:` inside `.base` files (doing so causes YAML syntax errors and displays as orange in Obsidian).

4. **Formula Link Transformations (`formulas:`)**:
   - Use Base formulas to strip raw YAML brackets/quotes and map array values into native clickable link objects:
     ```yaml
     formulas:
       clean_duplicates: 'if(archived_duplicates, archived_duplicates.toString().replace(/[\[\]"]/g, "").split(",").map(link(value.trim())))'
       clean_gedcom_ids: 'if(gedcom_ids, gedcom_ids.toString().replace(/[\[\]"]/g, "").split(",").map(value.trim()))'
     ```
   - Reference formula properties in views using `formula.clean_duplicates`.

5. **View Layout Types (`views:` -> `type:`)**:
   - `type: table`: Tabular data grid with custom `order:`, column `displayName:`, row formulas, and `summaries:` footers.
   - `type: cards`: Responsive gallery grid displaying cover images (`image: "[[cover.jpg]]"`), tags, and metadata pills.
   - `type: list`: Compact, formatted bullet/item feed.
   - `type: map`: Interactive OpenFreeMap / Leaflet map displaying markers extracted from `coordinates: [lat, lng]` or `"lat, lng"` with customizable `icon:` (from Lucide) and `color:`.

6. **Column Summaries & Aggregations (`views:` -> `summaries:`)**:
   - Built-in aggregations replace legacy DataviewJS reduce loops:
     ```yaml
     summaries:
       cost: Sum
       labor: Sum
       formula.total_basis: Sum
       rating: Average
       status: Count
     ```
   - Supported summary functions: `Sum`, `Average`, `Count`, `Min`, `Max`, `Range`, `Median`, `Stddev`, `Earliest`, `Latest`.

---

## 2. Vault Property Types Registry (`.obsidian/types.json`)

Obsidian tracks property UI types (List, Text, Date, Checkbox) globally per vault inside `.obsidian/types.json`.

> [!IMPORTANT]
> **Internal Type String Names**:
> Obsidian uses exact internal type string names. Never use unrecognized strings like `"multiselect"`, which causes Obsidian to display question mark `[?]` icons next to properties!

| Property UI Type | Internal `types.json` String | Example Usage |
| :--- | :--- | :--- |
| **List (Multi-Select)** | **`"multitext"`** | `parents`, `spouse`, `children`, `archived_duplicates`, `gedcom_ids`, `sources` |
| **Text (Single Value)** | **`"text"`** | `doc_type`, `name`, `birth_place`, `reconciliation_status`, `document_status` |
| **Date** | **`"date"`** | `reconciliation_date`, `created` |
| **Checkbox (Boolean)** | **`"checkbox"`** | `historical_significance`, `merge_approved` |
| **Number** | **`"number"`** | `sequence`, `age` |

### Standard `.obsidian/types.json` Example:
```json
{
  "types": {
    "parents": "multitext",
    "spouse": "multitext",
    "children": "multitext",
    "archived_duplicates": "multitext",
    "potential_duplicates": "multitext",
    "reconciliation_status": "text",
    "document_status": "text",
    "reconciliation_date": "date",
    "historical_significance": "checkbox"
  }
}
```

---

## 3. YAML Frontmatter WikiLink Formatting (`.md` files)

To ensure Obsidian's visual Properties UI renders WikiLinks as **clickable purple/blue link pills**:

* **List Properties**: Use double-quoted WikiLink list items:
  ```yaml
  spouse:
    - "[[Belva Bertha Anna Burleson Penland - URN-GEN-GED-I342596405423]]"
  children:
    - "[[Lela Penland - URN-GEN-GED-I342596405524]]"
  ```
* **Scalar Properties**: Use double-quoted scalar WikiLinks:
  ```yaml
  subject: "[[Lisa Pino]]"
  merged_into:
    - "[[Primary Profile Stem]]"
  ```

---

## 4. Complete Core Base Example Schema

```yaml
filters:
  and:
    - "reconciliation_status == 'merged_pending_review' || reconciliation_status == 'merged'"

formulas:
  clean_duplicates: 'if(archived_duplicates, archived_duplicates.toString().replace(/[\[\]"]/g, "").split(",").map(link(value.trim())))'
  clean_gedcom_ids: 'if(gedcom_ids, gedcom_ids.toString().replace(/[\[\]"]/g, "").split(",").map(value.trim()))'

properties:
  name:
    displayName: Name
  birth_date:
    displayName: Birth Date
  death_date:
    displayName: Death Date
  reconciliation_date:
    displayName: Reconciled Date
  formula.clean_duplicates:
    displayName: Archived Duplicates
  relationship_annotation:
    displayName: Relationship Note
  formula.clean_gedcom_ids:
    displayName: GEDCOM IDs
  reconciliation_status:
    displayName: Reconciliation Status
  merge_approved:
    displayName: Approved
  document_status:
    displayName: Document Status

views:
  - type: table
    name: "Duplicate Entity Merge Review Table"
    order:
      - file.name
      - name
      - birth_date
      - death_date
      - reconciliation_date
      - formula.clean_duplicates
      - relationship_annotation
      - formula.clean_gedcom_ids
      - reconciliation_status
      - merge_approved
      - document_status
```

