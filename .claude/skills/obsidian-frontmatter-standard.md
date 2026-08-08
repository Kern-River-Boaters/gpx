# obsidian-frontmatter-standard

> Parent Skill Definition: [obsidian-frontmatter-standard](file:///home/jpino/Obsidian/Common/_Meta/Skills/obsidian-frontmatter-standard/SKILL.md)

# Obsidian Frontmatter & Properties Standard Skill

## Overview
This skill governs all YAML frontmatter creation and modification across federated Obsidian vaults, strictly grounded in official Obsidian documentation (`Properties.md`).

## Core Rules
1. **Isolated Delimiters**: The opening `---` and closing `---` delimiters must always sit completely isolated on their own lines, with no trailing or leading characters (e.g., never `---doc_type`).
2. **List Property Formatting**: All list properties (such as `parents`, `spouse`, `children`, `occupations`, `tags`, `aliases`, `locations_lived`) must be formatted either as a clean indented block list with hyphens (`- item`) or as a valid inline empty array (`[]`) strictly on the same line (e.g. `spouse: []`), never orphaned on a newline beneath the key.
3. **Property Types**:
   - **Text**: Single line of text. Internal links (`[[Link]]`) must be surrounded by quotes.
   - **List**: Multiple values, each preceded by a hyphen and a space (`- value`).
   - **Number**: Literal numeric values.
   - **Checkbox**: `true` or `false` boolean values.
   - **Date**: Formatted as `YYYY-MM-DD`.
4. **Mandatory Guardrail Module**: All automated scripts *must* import and utilize `_Meta/Scripts/frontmatter_guardrail.py` (`parse_and_save_frontmatter`) to handle YAML serialization, preventing manual string concatenation errors.

