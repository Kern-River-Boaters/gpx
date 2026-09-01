# Workspace Agent Rules

## Ergonomics & Hands-Free Autonomous Mode
- **Zero-Friction Execution**: The user is recovering from rotator cuff surgery and needs to minimize mousing and clicking.
- **Auto-Accept & Proceed**: Execute commands, tool calls, fixes, and workflow steps completely autonomously without waiting for manual confirmation or prompting for simple approvals whenever possible.
- **Direct Execution**: Perform code modifications, system service management, and verification commands directly.

## Basename WikiLink Invariant & Markdown Table Pipe Escaping
- **Basename WikiLinks Only**: ALL internal Obsidian links across all vaults MUST use clean file basenames (`[[Whalen, Patrick 1811-09-01|Patrick Whalen]]` and `[[1840 Marriage Whalen Patrick Leslie Eliza.pdf]]`). Hardcoded folder path prefixes (`People/...`, `Sources/...`) are strictly forbidden.
- **Mandatory Table Pipe Escaping**: In Markdown table rows, ALL WikiLinks containing alias pipes MUST be escaped as ``Alias`` to prevent table column splitting. Run `sanitize_markdown_tables.py` to enforce.

## Canonical Space-Free Source Naming & 2-Tier Archival Taxonomy (ADR-GEN-026)
- **Deterministic Space-Free Naming**: All source notes and binary media assets across all vaults MUST follow the space-free grammar (`YYYY-MM-DD_[Category]_[Surname-Given]_[Detail]_[Repo]_[Tier].[ext]`). Spaces in source filenames are strictly prohibited.
- **Two-Tier Archival Folder Structure (9 Top-Level Categories)**:
  1. `Sources/Vital_Statistics/` (`Births/`, `Marriages/`, `Deaths/`, `Baptisms/`)
  2. `Sources/Census/` (`US/`, `Canada/`)
  3. `Sources/Military/`: Service rolls, draft cards, pensions, discharge records.
  4. `Sources/Land_and_Probate/`: Deeds, wills, probate inventories, land settlements.
  5. `Sources/Immigration_and_Passports/`: Visas, passports, passenger manifests, border crossings.
  6. `Sources/Microfilms/`: Authentic dual-asset archival film stitches (PANB, LAC, NARA).
  7. `Sources/Published_Histories/` (`Directories/`, `Town_Reports/`)
  8. `Sources/Personal_Papers_and_Artifacts/` (`Education/`, `Awards_and_Honors/`, `Correspondence/`, `Memorabilia/`)
  9. `Sources/Newspapers_and_Periodicals/` (`Obituaries/`, `Articles/`, `Clippings/`)

## Strict Family Vault Boundary & Client Isolation
- **Family SSoT Mandate**: The master `Genealogy` vault is exclusively reserved for the family bloodlines (Pino, Whalen, Leslie, Dudley, Dunklee, Rexach, Serra).
- **Client Data Separation**: Commercial/friend client data (`Kamas`, `Nary`) is 100% excluded from `Genealogy` and maintained in standalone independent vaults.
- **Deliverable Projection**: `sync_client_deliverables.py` projects exclusively into `Canadian-Citizenship` for Lisa Michelle Phillips (Chain A Whalen lineage).
- **Client Vault Definition of Done (DoD)**: Client deliverable vaults must maintain 100% client-friendly canonical naming, zero broken links, zero AI engine tokens, and zero internal scaffolding directories.

## Tri-Tier Image Asset Lifecycle & Master Invariant (ADR-GEN-020 / ADR-GEN-026)
- **WE ALWAYS KEEP THE MASTER**: The pristine, unaltered, highest-resolution original facsimile (`_Master.jpg` or `.pdf`) is permanently preserved in the archive as the legal golden copy. Inferior cropped screenshots are replaced by the authentic Master scan.
- **Single Markdown Note Binding**: All asset tiers (`_Master.jpg`, `_Display.jpg`, `_Inference.png`, `_PageN.jpg`) are bound to **ONE single companion note** (`[BaseName].md`).
- **Multi-Page Single Note Consolidation**: Consecutive folios/sheets of the same household or instrument are consolidated into a single master companion note with sequential Page 1 / Page 2 OCR streams.
- **Absolute Prohibition on Synthetic Evidence**: AI agents are STRICTLY FORBIDDEN from generating synthetic images, mock certificates, artificial census sheets, or fake validation seals using PIL, ImageDraw, SVG, canvas, or AI image generators.
- **Anti-SERP & Anti-Bot Block Mandate**: NEVER capture, ingest, or embed search engine result pages (SERPs), search query lists, unauthenticated login screens ("Sign In"), or anti-bot block pages (`Error 15`, `Access Denied`).
- **Atomic Linking Mandatory**: Every ingested document or microfilm facsimile MUST be atomically linked to its target profile (`People/`) in both frontmatter `sources:` and markdown body `## 📄 Source Documents`.
- **Definition of Done**: Run `python3 _Meta/Tests/run_all_tests.py` to assert 0 orphaned sources, 0 uncanonical names, and 0 broken links before declaring completion.

## Dynamic Family Tree Graph Standard
- **Mandatory Family Tree Block**: Every newly created, enriched, or modified person profile (`People/`) MUST contain the dynamic ````family-tree` codeblock section directly beneath the Executive Summary:
  ```markdown
  ## 🌳 Family Tree & Dynamic Lineage Graph

  ```family-tree
  depth: 2
  spouses: true
  dates: true
  direction: TD
  ```
  ```
- **Universal Cross-Platform Compliance**: Traversal must use the universal Bases-native engine (`genealogy_graph_engine.js`), maintaining 100% compatibility across Obsidian and Kern Publisher Web without Dataview dependencies.
- **Automated Sentinel**: `audit_and_enforce_source_links.py` automatically asserts and repairs any missing family tree blocks across all vault profiles.

## Bidirectional Lineage Pointer Symmetry Standard
- **Reciprocal Pointer Invariance**: Every genealogical relationship in frontmatter MUST be bidirectionally symmetric:
  - **Child $\leftr→ Parent**: If Person A lists Person B in `parents:`, Person B MUST list Person A in `children:`, and vice versa.
  - **Spouse $\leftr→ Spouse**: If Person A lists Person B in `spouse:`, Person B MUST list Person A in `spouse:`.
  - **Sibling $\leftr→ Sibling**: All individuals sharing parents MUST symmetrically list each other in `siblings:`.
- **Automated Enforcement**: `audit_and_enforce_source_links.py` and `reconcile_bidirectional_lineage_pointers.py` automatically audit and repair any asymmetric links across the vault on every run.

## Universal Dual-Hemisphere Fan Chart Typography & Legal Citizenship Standard
- **Upper Hemisphere (Ancestors)**: **Full Legal Names** across all ancestral rings (Parents, Grandparents, Great-Grandparents).
- **Lower Hemisphere (Descendants)**: **Given Names Only** across all descendant rings (Children, Grandchildren, Great-Grandchildren), preserving authentic compound given names (*José Luis*, *María Luisa*, *Elena María*, *Alister Jude*) while omitting surnames to prevent text collision.
- **Center Hub**: Subject displays full legal name, vital dates, legal citizenship flags, and spouse badges.
- **Strict Legal Citizenship**: Flags infer strictly from `citizenship_status` / `citizenship` (or birth place as legacy fallback). Residence history (`locations_lived`) is strictly prohibited from generating nationality flags.
- **Pre-Flight Quality Gate**: Run `python3 Common/_Meta/Tests/test_kern_publisher.py` (31 unit tests) and `python3 _Meta/Tests/run_all_tests.py` (32 unit tests) prior to reloading Kern Publisher Web or completing tasks.

## Person Profile Definition of Done (Level 4 Empirical Standard)
Every profile in `People/` is declared **Done** if and only if:
1. **Frontmatter Integrity**: Standard YAML properties (`id: URN-*`, `name`, `birth_date`, `birth_place`, `parents`, `spouse`, `children`, `siblings`, `citizenship_status`, `data_origin: certified_vital_records`, `audit_tag: verified_empirical`, `audit_status: passed`).
2. **100% Reciprocal Lineage Symmetry**: Symmetric bidirectional pointers across parents, spouses, and siblings.
3. **Clean Basename WikiLinks**: Clean basenames only (``Alias`` with escaped pipes in tables).
4. **Dynamic Family Tree Codeblock**: Embedded ````family-tree```` section directly under Executive Summary.
5. **Dynamic Obsidian Base Table**: `## 📄 Source Documents & Archival Evidence` Base block querying `file.hasLink("<Person Profile>.md")`.
6. **Canonical 6-Section Layout**: Follows `.obsidian/templates/Person_Profile_Template.md`.

## Source Document 3-Layer Definition of Done (DoD)
Every source companion note in `Sources/` is declared **Done** if and only if:
1. **7-Category Taxonomy Locus**: Resides strictly in one of the 7 archival folders.
2. **Multi-Generational Kinship Linking**: Frontmatter `people:` array links all 3 attested generations (Subject G0, Parents G1, Grandparents G2, Spouses, Witnesses).
3. **Layer 1 Frontmatter**: Complete metadata (`doc_type: source`, `quay: 3`, `epistemic_tier`, `sha256`, `media_file:`).
4. **Layer 2 Fact Table**: Clean Markdown table with escaped table pipes (``Alias``).
5. **Layer 3 Verbatim OCR Block**: Full verbatim text stream (Apple Vision / RapidOCR / Hermes Consensus), with bilingual Spanish/English for Latin American/Spanish holdings.

## Self-Healing Dual-Tier Compute & Wake-on-LAN (WoL) Standby Standard
- **Primary Compute Node (Kern)**: High-speed local single-pass OCR via `rapidocr-onnxruntime` (AMD Ryzen AI 9 HX 370, 24 threads, 50 TOPS NPU) provides 100% independent processing without external dependencies.
- **Mac Node Booster (`pino-family-imac`)**: Apple Vision Neural Engine acts as opportunistic cluster booster.
- **Standby & WoL Management**: `wake_mac_node.py` broadcasts UDP magic packets to wake the Mac from 2W standby on demand. If the Mac is offline, Kern seamlessly executes 100% of OCR locally.
- **Tri-Engine Forensic Consensus**: For degraded/faded cursive records, `forensic_tri_engine_ocr.py` triangulates Apple Vision, RapidOCR, and Hermes LLM for high-accuracy consensus.

## Cross-Corpus Kinship Discovery Standard
- **Full-Text OCR Searchability**: Use `discover_kinship_across_transcriptions.py` to search Layer 3 text across all source holdings.
- **Automatic Back-Annotation**: When an ancestor's mention is verified as a witness, godparent (*padrino*), or neighbor in a document, back-annotate their WikiLink into `people:` and Layer 2 tables, instantly updating their Obsidian Base table.

