#!/usr/bin/env python3
"""
Find blog posts with different/inconsistent design structures
"""
import os
from pathlib import Path

def check_post_design(filepath):
    """
    Check design structure of a post
    Returns: (design_type, has_site_header, has_container, has_article_tag)
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        has_site_header = 'class="site-header"' in content
        has_container = 'class="container"' in content
        has_article_tag = '<article' in content
        has_hero = 'class="hero-section"' in content or 'class="hero-title"' in content

        # Determine design type
        if has_site_header and not has_container:
            design = "STANDARD"  # Premium template style
        elif has_container and not has_site_header:
            design = "CUSTOM"    # Custom container design
        elif has_site_header and has_container:
            design = "MIXED"     # Both styles mixed
        else:
            design = "MINIMAL"   # Neither style

        return design, has_site_header, has_container, has_article_tag, has_hero

    except Exception as e:
        return "ERROR", False, False, False, False

def main():
    base_dir = Path("blog/troubleshooting")

    if not base_dir.exists():
        print("[ERROR] Directory not found")
        return

    html_files = sorted([f for f in base_dir.glob('*.html')])

    print("\n" + "="*80)
    print("BLOG DESIGN STRUCTURE ANALYSIS")
    print("="*80 + "\n")

    design_groups = {
        "STANDARD": [],
        "CUSTOM": [],
        "MIXED": [],
        "MINIMAL": [],
        "ERROR": []
    }

    for filepath in html_files:
        filename = filepath.name
        design, has_header, has_container, has_article, has_hero = check_post_design(filepath)

        design_groups[design].append(filename)

        if design != "STANDARD":
            print(f"[{design}] {filename}")
            print(f"  --> site-header: {has_header}, container: {has_container}, article: {has_article}, hero: {has_hero}")

    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total posts checked: {len(html_files)}")
    print(f"  - STANDARD design: {len(design_groups['STANDARD'])} [OK]")
    print(f"  - CUSTOM design: {len(design_groups['CUSTOM'])} [NEEDS FIX]")
    print(f"  - MIXED design: {len(design_groups['MIXED'])} [NEEDS FIX]")
    print(f"  - MINIMAL design: {len(design_groups['MINIMAL'])} [NEEDS FIX]")
    print(f"  - ERROR: {len(design_groups['ERROR'])} [ERROR]")

    if len(design_groups['STANDARD']) == len(html_files):
        print("\n[OK] ALL POSTS USE STANDARD DESIGN")
    else:
        non_standard = len(html_files) - len(design_groups['STANDARD'])
        print(f"\n[ALERT] {non_standard} POSTS USE NON-STANDARD DESIGN - NEED FIX")

        if design_groups['CUSTOM']:
            print(f"\nCustom Design Posts ({len(design_groups['CUSTOM'])}):")
            for name in design_groups['CUSTOM']:
                print(f"  - {name}")

        if design_groups['MIXED']:
            print(f"\nMixed Design Posts ({len(design_groups['MIXED'])}):")
            for name in design_groups['MIXED']:
                print(f"  - {name}")

    print("\n" + "="*80 + "\n")

if __name__ == '__main__':
    main()
