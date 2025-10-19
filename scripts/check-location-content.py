#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check 10 location pages for duplicate content and wrong city names."""

import os
import sys
import re

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def check_page_content(file_path):
    """Check if page has correct city name or duplicate Ajax content."""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    page_name = os.path.basename(file_path).replace('.html', '')
    city_name = page_name.replace('-', ' ').title()

    print(f"\n{'='*70}")
    print(f"CHECKING: {page_name}.html")
    print(f"Expected city: {city_name}")
    print(f"{'='*70}")

    # Extract H1
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL | re.IGNORECASE)
    h1_text = h1_match.group(1).strip() if h1_match else "NO H1"
    h1_text = re.sub(r'<[^>]+>', '', h1_text)  # Remove HTML tags
    print(f"\nH1: {h1_text}")

    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', content)
    title_text = title_match.group(1) if title_match else "NO TITLE"
    print(f"Title: {title_text}")

    # Check for city mentions
    city_mentions = len(re.findall(rf'\b{city_name}\b', content, re.IGNORECASE))
    ajax_mentions = len(re.findall(r'\bAjax\b', content, re.IGNORECASE))

    print(f"\n'{city_name}' mentions: {city_mentions}")
    print(f"'Ajax' mentions: {ajax_mentions}")

    # Check first paragraph
    hero_text_match = re.search(r'<h1[^>]*>.*?</h1>.*?<p[^>]*>(.*?)</p>', content, re.DOTALL | re.IGNORECASE)
    if hero_text_match:
        first_para = hero_text_match.group(1).strip()
        first_para = re.sub(r'<[^>]+>', '', first_para)[:200]
        print(f"\nFirst paragraph:")
        print(f"  {first_para}...")

    # Check canonical URL
    canonical_match = re.search(r'<link rel="canonical" href="([^"]+)">', content)
    if canonical_match:
        canonical = canonical_match.group(1)
        print(f"\nCanonical URL: {canonical}")
        if page_name.lower() in canonical.lower():
            print("  ✓ Canonical matches page")
        else:
            print(f"  ✗ WARNING: Canonical doesn't match page name")

    # Diagnosis
    print(f"\n{'='*70}")
    if ajax_mentions > city_mentions and page_name.lower() != 'ajax':
        print("⚠️ ISSUE: More 'Ajax' mentions than city name - likely duplicate content")
        print("  This page probably was copied from Ajax without proper replacement")
    elif city_mentions == 0:
        print("⚠️ ISSUE: City name not found in content - wrong content")
    elif city_name.lower() in h1_text.lower() or page_name.lower() in h1_text.lower():
        print("✓ GOOD: Page has correct city-specific content")
    else:
        print("⚠️ UNCERTAIN: Check manually")

    return {
        'page': page_name,
        'h1': h1_text,
        'city_mentions': city_mentions,
        'ajax_mentions': ajax_mentions,
        'has_issue': ajax_mentions > city_mentions and page_name.lower() != 'ajax'
    }

def main():
    """Check 10 sample location pages."""

    print("="*70)
    print("LOCATION CONTENT ANALYSIS - 10 SAMPLE PAGES")
    print("="*70)

    # Sample 10 pages
    pages = [
        'locations/ajax.html',
        'locations/toronto.html',
        'locations/brampton.html',
        'locations/mississauga.html',
        'locations/markham.html',
        'locations/vaughan.html',
        'locations/richmond-hill.html',
        'locations/whitby.html',
        'locations/aurora.html',
        'locations/stouffville.html',
    ]

    results = []
    for file_path in pages:
        if os.path.exists(file_path):
            result = check_page_content(file_path)
            results.append(result)
        else:
            print(f"\n✗ ERROR: {file_path} not found")

    # Summary
    print(f"\n\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}\n")

    issues_found = [r for r in results if r['has_issue']]

    print(f"Pages checked: {len(results)}")
    print(f"Pages with duplicate Ajax content: {len(issues_found)}\n")

    if issues_found:
        print("⚠️ PAGES WITH ISSUES:")
        for r in issues_found:
            print(f"  - {r['page']}.html (Ajax mentions: {r['ajax_mentions']}, City mentions: {r['city_mentions']})")
    else:
        print("✓ All checked pages have correct content")

    print(f"\n{'='*70}")

if __name__ == '__main__':
    main()
