---
name: "obsidian-frontmatter-standard"
description: "obsidian-frontmatter-standard skill for OpenCode"
---

# obsidian-frontmatter-standard

> Parent Skill Definition: [obsidian-frontmatter-standard](file:///home/jpino/Obsidian/Common/_Meta/Skills/obsidian-frontmatter-standard/SKILL.md)

---
name: obsidian-frontmatter-standard
description: "Comprehensive governance and validation standard for YAML frontmatter and Obsidian Properties across federated vaults. Enforces official Obsidian Help specifications, strict quoting rules, and prohibits brittle string concatenations."
---

# Obsidian Frontmatter & Properties Standard Skill

## Overview
This skill governs all YAML frontmatter creation, manipulation, and validation across federated Obsidian vaults, grounded directly in official Obsidian documentation (`references/obsidian-help/en/Editing and formatting/Properties.md`).

## Core Rules & Invariants

1. **Isolated Delimiters**:
   - The opening `---` and closing `---` delimiters must sit completely isolated on their own lines (no trailing spaces, never `---doc_type`).
2. **Prohibition of Unquoted Markdown Links**:
   - Markdown links like `receipts: [Receipt.pdf](../../Sources/Receipt.pdf)` are **STRICTLY FORBIDDEN** in YAML frontmatter because `[` and `]` are reserved YAML sequence tokens.
   - All internal links must use quoted wikilinks: `receipts: "[[Receipt.pdf]]"` or list items `- "[[Receipt.pdf]]"`.
3. **Scalar Quoting Rules**:
   - All scalar strings containing `*` (e.g. `*bold*` or `*`), `&` (e.g. URLs with query params `url: "https://example.com?a=1&b=2"`), `:` (colons followed by spaces), or single quotes `'` **MUST be enclosed in double quotes (`"..."`)**.
   - Note descriptions must be single-line strings. Never embed multiline string fragments containing `type: note` or `tags:` in frontmatter.
4. **List Property Formatting**:
   - List properties must be formatted either as a clean block sequence with hyphens (`- "item"`) or as a valid inline empty array (`[]`) on the same line (e.g. `aliases: []`).
   - Never place `[]` on a key if child list items follow on subsequent lines.
5. **Obsidian Property Types**:
   - **Text**: Single line. Internal links (`"[[Link]]"`) and URLs with `&` must be surrounded by quotes.
   - **List / Multitext**: Multiple values, each preceded by `- ` and indented uniformly.
   - **Number**: Literal numeric values (integers or decimals, no arithmetic expressions).
   - **Checkbox**: `true` or `false` boolean values.
   - **Date**: Formatted strictly as `YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SS`.
6. **Automated Verification**:
   - Run `_Meta/Scripts/test_frontmatter_standards.py` to audit all 15,000+ notes across the federation.
   - Every note must parse cleanly with `yaml.safe_load`.

---

## 🛡️ 7. Strict Prohibition on Naive String Concatenation & Ingestion Safeguards (ADR-021)

### The Anti-Pattern
Agents and automated scripts must **NEVER** use naive string replacement or string concatenation (e.g. `ptxt.replace("sources:\n", f"sources:\n  - \"{link}\"\n")`) to mutate frontmatter. 

### Why This Fails
Vault notes may have mixed indentation conventions (0-space vs. 2-space lists). Injecting an indented list item at the head of a 0-space block breaks YAML 1.2 block mapping parsing, producing fatal YAML syntax exceptions (`expected <block end>, but found '-'`) that cascade across the graph engine and publish pipelines.

### Mandatory Safe Ingestion Protocol
All automated scripts mutating YAML frontmatter MUST use `safe_frontmatter_injector.py`:
1. Parse the existing YAML block into a Python dictionary with `yaml.safe_load()`.
2. Manipulate the native data structure (appending to list, deduplicating).
3. Serialize back cleanly with `yaml.dump(sort_keys=False, allow_unicode=True)`.
4. Run a pre-write parse test `yaml.safe_load(new_yaml)` before saving to disk.
5. All CI/test gates must execute `test_frontmatter_schema.py` across all vault markdown files.

