#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Analyze which location pages have unique content vs template duplicates."""

import os
import sys
import glob
import re
from collections import defaultdict

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def extract_unique_phrases(file_path):
    """Extract location-specific phrases from a page."""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    page_name = os.path.basename(file_path).replace('.html', '')

    # Location-specific keywords that shouldn't be on other pages
    keywords = {
        'oak_ridges': len(re.findall(r'Oak Ridges', content, re.IGNORECASE)),
        'well_water': len(re.findall(r'well water', content, re.IGNORECASE)),
        'lake_humidity': len(re.findall(r'lake humidity', content, re.IGNORECASE)),
        'horse_farm': len(re.findall(r'horse farm', content, re.IGNORECASE)),
        'persian_chinese': len(re.findall(r'Persian & Chinese', content, re.IGNORECASE)),
        'upscale_brand': len(re.findall(r'Upscale brand', content, re.IGNORECASE)),
        'legacy_ballantrae': len(re.findall(r'Legacy.*Ballantrae', content, re.IGNORECASE)),
        'growing_family': len(re.findall(r'growing family', content, re.IGNORECASE)),
    }

    # Extract first 2 paragraphs
    paras = re.findall(r'<p[^>]*>(.*?)</p>', content, re.DOTALL | re.IGNORECASE)
    first_para = re.sub(r'<[^>]+>', '', paras[0])[:150] if paras else ""
    second_para = re.sub(r'<[^>]+>', '', paras[1])[:150] if len(paras) > 1 else ""

    return {
        'page': page_name,
        'keywords': keywords,
        'first_para': first_para,
        'second_para': second_para,
    }

def main():
    """Analyze all location pages."""

    print("="*80)
    print("LOCATION PAGES UNIQUENESS ANALYSIS")
    print("="*80)
    print()

    location_files = sorted(glob.glob('locations/*.html'))

    if not location_files:
        print("ERROR: No location pages found")
        return

    print(f"Analyzing {len(location_files)} location pages...\n")

    results = []
    for file_path in location_files:
        result = extract_unique_phrases(file_path)
        results.append(result)

    # Group by first paragraph (to find duplicates)
    para_groups = defaultdict(list)
    for r in results:
        para_key = r['first_para'][:100]  # First 100 chars
        para_groups[para_key].append(r['page'])

    # Find duplicate content
    print("="*80)
    print("DUPLICATE CONTENT DETECTION")
    print("="*80)
    print()

    duplicate_groups = {k: v for k, v in para_groups.items() if len(v) > 1}

    if duplicate_groups:
        print(f"Found {len(duplicate_groups)} groups of pages with duplicate content:\n")
        for i, (para, pages) in enumerate(duplicate_groups.items(), 1):
            print(f"Group {i}: {len(pages)} pages")
            print(f"First paragraph: \"{para}...\"")
            print(f"Pages:")
            for page in pages:
                print(f"  - {page}.html")
            print()
    else:
        print("✓ No duplicate content found - all pages unique\n")

    # Check for misplaced location-specific content
    print("="*80)
    print("MISPLACED LOCATION-SPECIFIC CONTENT")
    print("="*80)
    print()

    issues = []

    for r in results:
        page = r['page']
        kw = r['keywords']

        # Oak Ridges should only be in Ajax/Aurora area pages
        if kw['oak_ridges'] > 0 and page not in ['ajax', 'aurora', 'richmond-hill']:
            issues.append(f"{page}.html has 'Oak Ridges' ({kw['oak_ridges']}x) - should only be in Ajax/Aurora")

        # Horse farm should only be in Stouffville
        if kw['horse_farm'] > 0 and page != 'stouffville':
            issues.append(f"{page}.html has 'horse farm' - should only be in Stouffville")

        # Lake humidity should only be in waterfront cities (Whitby, Pickering, Oshawa)
        if kw['lake_humidity'] > 0 and page not in ['whitby', 'pickering', 'oshawa']:
            issues.append(f"{page}.html has 'lake humidity' - should only be in waterfront cities")

    if issues:
        print(f"⚠️ Found {len(issues)} misplaced content issues:\n")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✓ No misplaced location-specific content")

    # Summary by template type
    print(f"\n{'='*80}")
    print("CONTENT TEMPLATE ANALYSIS")
    print(f"{'='*80}\n")

    # Count how many use each template
    template_counts = defaultdict(int)
    for pages in para_groups.values():
        template_counts[len(pages)] += 1

    unique_pages = sum(1 for v in para_groups.values() if len(v) == 1)
    templated_pages = len(location_files) - unique_pages

    print(f"Unique content pages: {unique_pages}")
    print(f"Template-based pages: {templated_pages}")
    print(f"Total pages: {len(location_files)}")

    print(f"\n{'='*80}")
    print("RECOMMENDATION")
    print(f"{'='*80}\n")

    if templated_pages > 0:
        print(f"⚠️ {templated_pages} pages are using duplicate templates!")
        print("\nThese pages need unique, location-specific content:")
        print("- Replace generic text with city-specific details")
        print("- Add neighborhood names")
        print("- Add local landmarks")
        print("- Add city-specific appliance issues")
        print("- Remove location-specific content from other cities")
    else:
        print("✓ All pages have unique content!")

    print(f"\n{'='*80}")

if __name__ == '__main__':
    main()
