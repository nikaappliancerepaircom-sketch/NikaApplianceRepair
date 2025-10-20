#!/usr/bin/env python3
"""
Add mobile-icon-centering-fix.css to all HTML pages
This script adds the CSS link to pages that don't already have it.
"""

import os
import re
from pathlib import Path

# CSS link to add
CSS_LINK = '    <link rel="stylesheet" href="../css/mobile-icon-centering-fix.css">'
CSS_LINK_ROOT = '    <link rel="stylesheet" href="css/mobile-icon-centering-fix.css">'

def should_process_file(file_path):
    """Check if file should be processed."""
    path_str = str(file_path).lower()

    # Skip backup directories
    if 'backup' in path_str or 'old-files' in path_str:
        return False

    # Skip blog posts (we'll handle blog separately if needed)
    if 'blog' in path_str and file_path.name != 'blog.html':
        return False

    # Skip context engineering and tools
    if 'context-engineering' in path_str or 'tools' in path_str:
        return False

    # Skip placeholder files
    if 'placeholder' in path_str:
        return False

    return True

def add_css_to_file(file_path, is_root=False):
    """Add CSS link to a file if it doesn't already exist."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if already has the CSS link
        if 'mobile-icon-centering-fix.css' in content:
            print(f"[OK] Already has CSS: {file_path}")
            return False

        # Choose the correct CSS link based on location
        css_link = CSS_LINK_ROOT if is_root else CSS_LINK

        # Find the last CSS link and add after it
        # Look for common patterns of CSS links
        patterns = [
            r'(<link rel="stylesheet" href="[^"]*\.css">)',
            r'(<link rel="stylesheet" href="[^"]*\.css" \/>)',
        ]

        last_css_match = None
        last_position = -1

        for pattern in patterns:
            matches = list(re.finditer(pattern, content))
            if matches:
                last_match = matches[-1]
                if last_match.end() > last_position:
                    last_position = last_match.end()
                    last_css_match = last_match

        if last_css_match:
            # Insert after the last CSS link
            insert_pos = last_css_match.end()
            new_content = content[:insert_pos] + '\n' + css_link + content[insert_pos:]

            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"[OK] Added CSS to: {file_path}")
            return True
        else:
            print(f"[ERROR] Could not find CSS section in: {file_path}")
            return False

    except Exception as e:
        print(f"[ERROR] Error processing {file_path}: {e}")
        return False

def main():
    """Main function to process all HTML files."""
    base_dir = Path(__file__).parent

    print("=" * 60)
    print("Adding mobile-icon-centering-fix.css to all pages")
    print("=" * 60)

    counts = {
        'processed': 0,
        'skipped': 0,
        'already_had': 0,
        'added': 0
    }

    # Process root index.html
    index_path = base_dir / 'index.html'
    if index_path.exists():
        print("\n--- Processing Root Page ---")
        if 'mobile-icon-centering-fix.css' in index_path.read_text(encoding='utf-8'):
            print(f"[OK] Already has CSS: {index_path}")
            counts['already_had'] += 1
        elif add_css_to_file(index_path, is_root=True):
            counts['added'] += 1
        counts['processed'] += 1

    # Process about.html
    about_path = base_dir / 'about.html'
    if about_path.exists():
        print("\n--- Processing About Page ---")
        if 'mobile-icon-centering-fix.css' in about_path.read_text(encoding='utf-8'):
            print(f"[OK] Already has CSS: {about_path}")
            counts['already_had'] += 1
        elif add_css_to_file(about_path, is_root=True):
            counts['added'] += 1
        counts['processed'] += 1

    # Process services pages
    services_dir = base_dir / 'services'
    if services_dir.exists():
        print("\n--- Processing Service Pages ---")
        for html_file in services_dir.glob('*.html'):
            if should_process_file(html_file):
                if 'mobile-icon-centering-fix.css' in html_file.read_text(encoding='utf-8'):
                    print(f"[OK] Already has CSS: {html_file}")
                    counts['already_had'] += 1
                elif add_css_to_file(html_file, is_root=False):
                    counts['added'] += 1
                counts['processed'] += 1

    # Process location pages
    locations_dir = base_dir / 'locations'
    if locations_dir.exists():
        print("\n--- Processing Location Pages ---")
        for html_file in locations_dir.glob('*.html'):
            if should_process_file(html_file):
                if 'mobile-icon-centering-fix.css' in html_file.read_text(encoding='utf-8'):
                    print(f"[OK] Already has CSS: {html_file}")
                    counts['already_had'] += 1
                elif add_css_to_file(html_file, is_root=False):
                    counts['added'] += 1
                counts['processed'] += 1

    # Process brand pages
    brands_dir = base_dir / 'brands'
    if brands_dir.exists():
        print("\n--- Processing Brand Pages ---")
        for html_file in brands_dir.glob('*.html'):
            if should_process_file(html_file):
                if 'mobile-icon-centering-fix.css' in html_file.read_text(encoding='utf-8'):
                    print(f"[OK] Already has CSS: {html_file}")
                    counts['already_had'] += 1
                elif add_css_to_file(html_file, is_root=False):
                    counts['added'] += 1
                counts['processed'] += 1

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total files processed: {counts['processed']}")
    print(f"Files that already had CSS: {counts['already_had']}")
    print(f"Files with CSS added: {counts['added']}")
    print(f"Files skipped: {counts['skipped']}")
    print("=" * 60)

    if counts['added'] > 0:
        print(f"\n[SUCCESS] Successfully added CSS to {counts['added']} files!")
    else:
        print("\n[SUCCESS] All files already have the CSS link!")

if __name__ == '__main__':
    main()
