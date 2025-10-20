#!/usr/bin/env python3
"""
Standardize all internal link formats to use consistent relative paths.

This script converts absolute paths to relative paths for:
- /services/* → services/* (or ../services/* for subdirectory pages)
- /locations/* → locations/* (or ../locations/* for subdirectory pages)
- /brands/* → brands/* (or ../brands/* for subdirectory pages)
- /book → book (or ../book for subdirectory pages)
- /about → about (or ../about for subdirectory pages)

Exceptions:
- Keeps /blog links as-is (for clean URLs)
- Preserves external links (https://...)
- Preserves anchor links (#...)
- Preserves CSS/JS file references
"""

import os
import re
import glob
from pathlib import Path

# Define the root directory
ROOT_DIR = Path(r"C:\NikaApplianceRepair")

# Define patterns for different file locations
PATTERNS = {
    # Root level files (index.html, services.html, locations.html, brands.html, about.html, book.html, blog.html)
    "root": {
        "input_dir": ROOT_DIR,
        "glob_pattern": "*.html",
        "path_prefix": "",  # No prefix needed, same directory
    },
    # Service pages (services/*.html)
    "services": {
        "input_dir": ROOT_DIR / "services",
        "glob_pattern": "*.html",
        "path_prefix": "../",  # Go up one level
    },
    # Location pages (locations/*.html)
    "locations": {
        "input_dir": ROOT_DIR / "locations",
        "glob_pattern": "*.html",
        "path_prefix": "../",  # Go up one level
    },
    # Brand pages (brands/*.html)
    "brands": {
        "input_dir": ROOT_DIR / "brands",
        "glob_pattern": "*.html",
        "path_prefix": "../",  # Go up one level
    },
}

# Define replacement patterns
# These will be applied based on the file's location
def get_replacements(path_prefix):
    """
    Generate replacement patterns based on the file's location.

    Args:
        path_prefix: The prefix to add to paths (e.g., "" for root, "../" for subdirs)

    Returns:
        List of (pattern, replacement) tuples
    """
    replacements = [
        # Services links
        (r'href="/services/([^"]*)"', rf'href="{path_prefix}services/\1"'),
        (r'href="/services"', rf'href="{path_prefix}services"'),

        # Locations links
        (r'href="/locations/([^"]*)"', rf'href="{path_prefix}locations/\1"'),
        (r'href="/locations"', rf'href="{path_prefix}locations"'),

        # Brands links
        (r'href="/brands/([^"]*)"', rf'href="{path_prefix}brands/\1"'),
        (r'href="/brands"', rf'href="{path_prefix}brands"'),

        # Book link
        (r'href="/book"', rf'href="{path_prefix}book"'),

        # About link
        (r'href="/about"', rf'href="{path_prefix}about"'),
    ]

    return replacements


def should_skip_file(filepath):
    """Check if file should be skipped."""
    filepath_str = str(filepath)

    # Skip backup files
    if "backup" in filepath_str.lower():
        return True

    # Skip template files
    if "template" in filepath_str.lower():
        return True

    # Skip test files
    if "test" in filepath_str.lower():
        return True

    # Skip optimization files
    if "optimization" in filepath_str.lower():
        return True

    return False


def process_file(filepath, path_prefix):
    """
    Process a single HTML file and convert absolute paths to relative paths.

    Args:
        filepath: Path to the HTML file
        path_prefix: The prefix to add to relative paths

    Returns:
        Tuple of (changes_made, num_replacements)
    """
    if should_skip_file(filepath):
        return False, 0

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        replacements = get_replacements(path_prefix)
        total_replacements = 0

        # Apply each replacement pattern
        for pattern, replacement in replacements:
            # Count matches before replacement
            matches = re.findall(pattern, content)
            if matches:
                content = re.sub(pattern, replacement, content)
                num_replacements = len(matches)
                total_replacements += num_replacements
                print(f"    - Replaced {num_replacements} instances of pattern: {pattern[:50]}...")

        # Only write if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, total_replacements

        return False, 0

    except Exception as e:
        print(f"  ERROR processing {filepath}: {e}")
        return False, 0


def main():
    """Main function to process all HTML files."""
    print("=" * 80)
    print("Standardizing Internal Link Formats")
    print("=" * 80)
    print("\nConverting absolute paths to relative paths...")
    print("Exception: Keeping /blog links as-is for clean URLs\n")

    total_files_processed = 0
    total_files_changed = 0
    total_replacements = 0

    # Process each category of files
    for category, config in PATTERNS.items():
        input_dir = config["input_dir"]
        glob_pattern = config["glob_pattern"]
        path_prefix = config["path_prefix"]

        print(f"\n{'=' * 80}")
        print(f"Processing {category.upper()} files")
        print(f"Directory: {input_dir}")
        print(f"Path prefix: '{path_prefix}'")
        print(f"{'=' * 80}\n")

        # Find all matching HTML files
        pattern_path = input_dir / glob_pattern
        files = glob.glob(str(pattern_path))

        if not files:
            print(f"  No files found matching pattern: {pattern_path}")
            continue

        print(f"Found {len(files)} files to process\n")

        for filepath in sorted(files):
            filepath = Path(filepath)
            rel_path = filepath.relative_to(ROOT_DIR)

            print(f"Processing: {rel_path}")
            changed, num_replacements = process_file(filepath, path_prefix)

            total_files_processed += 1
            if changed:
                total_files_changed += 1
                total_replacements += num_replacements
                print(f"  [OK] Changed: {num_replacements} replacements made")
            else:
                print(f"  - No changes needed")
            print()

    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total files processed: {total_files_processed}")
    print(f"Total files changed: {total_files_changed}")
    print(f"Total replacements made: {total_replacements}")
    print("\n[SUCCESS] Internal link standardization complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
