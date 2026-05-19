#!/usr/bin/env python3
"""
Add hierarchical tags to markdown files in KRB repository.
Infers tags from directory structure and filenames.
"""

import os
import re
from pathlib import Path

# Paths
KRB_ROOT = Path(r"C:\Obsidian\KRB")

# Directory to river mappings
RIVER_MAPPINGS = {
    "Kern": "river/kern",
    "San Joaquin": "river/san_joaquin",
    "Rouge River": "river/rogue",  # Note: "Rouge" is a typo, should be "Rogue"
}

# Feature mappings from filename patterns
FEATURE_PATTERNS = {
    r'Rapids?': "feature/rapid",
    r'Campgrounds?': "feature/campground",
    r'Access': "feature/access",
    r'Parking': "feature/parking",
    r'Hazards?': "feature/hazard",
    r'Other': "feature/poi",
    r'Picnic': "feature/campground",
    r'Brush Creek': "feature/poi",  # Specific creek/tributary
}

# Difficulty inference from filenames
DIFFICULTY_PATTERNS = {
    r'Upper.*Kern.*Rapids': "difficulty/class_iii_iv",
    r'Lower.*Kern.*Rapids': "difficulty/class_ii_iii",
    r'North.*Fork.*Rapids': "difficulty/class_iv_v",
}

def infer_tags_from_file(file_path: Path) -> set:
    """Infer tags based on file location and name."""
    tags = set()

    filename = file_path.stem  # Without extension
    parent_dir = file_path.parent.name

    # Determine river from parent directory
    for river_name, river_tag in RIVER_MAPPINGS.items():
        if river_name in str(file_path.parent):
            tags.add(river_tag)

            # Add regional tags for California rivers
            if river_name in ["Kern", "San Joaquin"]:
                tags.add("region/california")
                tags.add("region/sierra_nevada")
            elif river_name == "Rouge River":  # Rogue is in Oregon
                tags.add("region/oregon")

    # Determine feature type from filename
    for pattern, feature_tag in FEATURE_PATTERNS.items():
        if re.search(pattern, filename, re.IGNORECASE):
            tags.add(feature_tag)

    # Determine difficulty from filename
    for pattern, difficulty_tag in DIFFICULTY_PATTERNS.items():
        if re.search(pattern, filename, re.IGNORECASE):
            tags.add(difficulty_tag)

    # Determine content type
    if "(Map)" in filename or ".json" in file_path.name:
        tags.add("type/map")
    elif "Tutorial" in filename:
        tags.add("type/tutorial")
    elif file_path.suffix == ".md" and "(Map)" not in filename:
        tags.add("type/river_guide")

    # Add verified status (assuming existing data is verified)
    if tags:  # Only add status if we have other tags
        tags.add("status/verified")

    # Add year-round season for established rivers
    if any(tag.startswith("river/") for tag in tags):
        tags.add("season/year_round")

    return tags

def has_frontmatter(content: str) -> bool:
    """Check if file already has frontmatter."""
    return content.startswith("---\n") or content.startswith("---\r\n")

def extract_existing_tags(content: str) -> set:
    """Extract existing tags from frontmatter."""
    tags = set()
    if not has_frontmatter(content):
        return tags

    frontmatter_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        tags_match = re.search(r'tags:\s*\n((?:  - .*\n)*)', frontmatter)
        if tags_match:
            tags_text = tags_match.group(1)
            for line in tags_text.split('\n'):
                match = re.match(r'\s*-\s*(.+)', line)
                if match:
                    tags.add(match.group(1).strip())

    return tags

def add_frontmatter_to_file(file_path: Path, tags: set) -> bool:
    """Add or update frontmatter with tags."""
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"  ❌ {file_path.name} - Error reading: {e}")
        return False

    # Get existing tags
    existing_tags = extract_existing_tags(content)

    # Merge with new tags
    all_tags = existing_tags | tags

    if not all_tags:
        print(f"  ⏭️  {file_path.name} - no tags to add")
        return False

    # Sort tags hierarchically
    sorted_tags = sorted(all_tags)

    # Build frontmatter
    frontmatter_lines = ["---", "tags:"]
    for tag in sorted_tags:
        frontmatter_lines.append(f"  - {tag}")
    frontmatter_lines.append("---")
    frontmatter = "\n".join(frontmatter_lines) + "\n\n"

    # Remove existing frontmatter if present
    if has_frontmatter(content):
        content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, count=1, flags=re.DOTALL)

    # Add new frontmatter
    new_content = frontmatter + content.lstrip()

    # Write back
    try:
        file_path.write_text(new_content, encoding='utf-8')
        print(f"  ✅ {file_path.name} - added {len(all_tags)} tags")
        return True
    except Exception as e:
        print(f"  ❌ {file_path.name} - Error writing: {e}")
        return False

def process_directory(directory: Path):
    """Process all markdown files in directory."""
    md_files = list(directory.rglob("*.md"))

    # Exclude _Meta directory and root-level files
    md_files = [
        f for f in md_files
        if "_Meta" not in str(f)
        and f.parent != KRB_ROOT  # Skip README.md, CLAUDE.md at root
    ]

    if not md_files:
        return

    print(f"Processing {len(md_files)} markdown files...")
    print()

    updated_count = 0
    for file_path in sorted(md_files):
        tags = infer_tags_from_file(file_path)
        if tags and add_frontmatter_to_file(file_path, tags):
            updated_count += 1

    print()
    print(f"✅ Updated {updated_count} markdown files")

def main():
    print("Adding tags to KRB markdown files...")
    print()

    process_directory(KRB_ROOT)

    print()
    print("✅ Tag migration complete!")
    print()
    print("Next steps:")
    print("1. Review tagged files in Obsidian")
    print("2. Manually adjust any incorrect inferences")
    print("3. Add difficulty tags to rapids where known")
    print("4. Commit changes to git")

if __name__ == '__main__':
    main()
