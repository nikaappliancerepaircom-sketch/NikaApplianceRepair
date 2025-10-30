#!/usr/bin/env python3
"""
Check design structure of ALL blog posts across all folders
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
    blog_base = Path("blog")
    folders = ["troubleshooting", "maintenance", "guides"]

    print("\n" + "="*80)
    print("COMPLETE BLOG DESIGN STRUCTURE ANALYSIS")
    print("="*80 + "\n")

    total_designs = {
        "STANDARD": 0,
        "CUSTOM": 0,
        "MIXED": 0,
        "MINIMAL": 0,
        "ERROR": 0
    }
    
    all_files = []

    for folder in folders:
        folder_path = blog_base / folder
        if not folder_path.exists():
            continue
            
        html_files = sorted([f for f in folder_path.glob('*.html')])
        
        print(f"\n[{folder.upper()}] - {len(html_files)} posts")
        print("-" * 80)
        
        folder_designs = {
            "STANDARD": [],
            "CUSTOM": [],
            "MIXED": [],
            "MINIMAL": [],
            "ERROR": []
        }

        for filepath in html_files:
            filename = filepath.name
            design, has_header, has_container, has_article, has_hero = check_post_design(filepath)

            folder_designs[design].append(filename)
            total_designs[design] += 1
            all_files.append((folder, filename, design))

            if design != "STANDARD":
                print(f"[{design}] {filename}")
                print(f"  --> site-header: {has_header}, container: {has_container}, article: {has_article}, hero: {has_hero}")

        print(f"\nFolder Summary:")
        print(f"  STANDARD: {len(folder_designs['STANDARD'])} [OK]")
        if folder_designs['CUSTOM']:
            print(f"  CUSTOM: {len(folder_designs['CUSTOM'])} [NEEDS FIX]")
        if folder_designs['MIXED']:
            print(f"  MIXED: {len(folder_designs['MIXED'])} [NEEDS FIX]")
        if folder_designs['MINIMAL']:
            print(f"  MINIMAL: {len(folder_designs['MINIMAL'])} [NEEDS FIX]")
        if folder_designs['ERROR']:
            print(f"  ERROR: {len(folder_designs['ERROR'])} [ERROR]")

    print("\n" + "="*80)
    print("OVERALL SUMMARY")
    print("="*80)
    total_posts = sum(total_designs.values())
    print(f"Total posts across all folders: {total_posts}")
    print(f"  - STANDARD design: {total_designs['STANDARD']} [OK]")
    print(f"  - CUSTOM design: {total_designs['CUSTOM']} [NEEDS FIX]")
    print(f"  - MIXED design: {total_designs['MIXED']} [NEEDS FIX]")
    print(f"  - MINIMAL design: {total_designs['MINIMAL']} [NEEDS FIX]")
    print(f"  - ERROR: {total_designs['ERROR']} [ERROR]")

    if total_designs['STANDARD'] == total_posts:
        print("\n[OK] ALL POSTS USE STANDARD DESIGN")
    else:
        non_standard = total_posts - total_designs['STANDARD']
        print(f"\n[ALERT] {non_standard} POSTS USE NON-STANDARD DESIGN - NEED FIX")

    print("\n" + "="*80 + "\n")

if __name__ == '__main__':
    main()
