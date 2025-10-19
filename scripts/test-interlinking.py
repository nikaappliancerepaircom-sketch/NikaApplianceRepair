#!/usr/bin/env python3
"""
Quick test to verify internal links work correctly
Tests a sample of pages from each category
"""

import re
from pathlib import Path

def test_links_in_file(file_path):
    """Test that links in a file have correct format"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    page_category = None
    if '/services/' in str(file_path):
        page_category = 'services'
    elif '/locations/' in str(file_path):
        page_category = 'locations'
    elif '/brands/' in str(file_path):
        page_category = 'brands'
    else:
        page_category = 'root'

    issues = []

    # Find all href links
    links = re.findall(r'href="([^"]+)"', content)

    for link in links:
        # Skip external links, anchors, and tel/mailto
        if link.startswith(('http', '#', 'tel:', 'mailto:')):
            continue

        # Check for .html extensions
        if '.html' in link and 'sitemap.xml' not in link:
            issues.append(f"Link has .html extension: {link}")

        # Check for absolute paths starting with /
        if link.startswith('/') and not link.startswith('//'):
            issues.append(f"Absolute path found (should be relative): {link}")

        # Check relative paths match page category
        if page_category != 'root':
            # Subfolder pages should use ../
            if link.startswith(('services/', 'locations/', 'brands/')):
                issues.append(f"Missing ../ prefix in subfolder page: {link}")

    return issues

def main():
    base_dir = Path('C:/NikaApplianceRepair')

    # Sample pages to test (1 from each category)
    test_pages = [
        base_dir / 'index.html',  # Root
        base_dir / 'services/refrigerator-repair.html',  # Service
        base_dir / 'locations/richmond-hill.html',  # Location
        base_dir / 'brands/samsung-appliance-repair-toronto.html',  # Brand
    ]

    total_issues = 0

    print("="*60)
    print("INTERLINKING TEST - SAMPLE VERIFICATION")
    print("="*60)
    print()

    for page in test_pages:
        if not page.exists():
            print(f"[SKIP] {page.name} - file not found")
            continue

        print(f"Testing: {page.name}")
        issues = test_links_in_file(page)

        if issues:
            print(f"  [FAIL] {len(issues)} issues found:")
            for issue in issues[:5]:  # Show first 5
                print(f"    - {issue}")
            if len(issues) > 5:
                print(f"    ... and {len(issues) - 5} more")
            total_issues += len(issues)
        else:
            print(f"  [PASS] All links look good!")
        print()

    print("="*60)
    if total_issues == 0:
        print("[PASS] ALL TESTS PASSED - No issues found!")
    else:
        print(f"[WARN] FOUND {total_issues} ISSUES - Review needed")
    print("="*60)

if __name__ == '__main__':
    main()
