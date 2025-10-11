#!/usr/bin/env python3
"""
Test all pages and take screenshots
"""

from playwright.sync_api import sync_playwright
from pathlib import Path
import time

def test_page(html_file, output_name):
    """Test page and take screenshots"""

    html_path = Path(html_file).absolute()
    issues = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})

        page.goto(f'file:///{html_path}')
        time.sleep(1)

        # Test 1: Check pricing table has $119
        pricing = page.locator('td:has-text("$119")').first
        if pricing.count() == 0:
            issues.append("Missing $119 in pricing table")

        # Test 2: Check hero image visible
        hero_img = page.locator('section.hero-section img').first
        if hero_img.count() == 0:
            issues.append("Missing hero image")

        # Test 3: Check 4.9 star rating
        rating = page.locator('text=/4\\.9.*from 5,200/i').first
        if rating.count() == 0:
            issues.append("Missing 4.9 rating")

        # Test 4: Check no duplicate Transparent Pricing
        pricing_headers = page.locator('h3:has-text("Transparent Pricing")')
        if pricing_headers.count() > 1:
            issues.append(f"Duplicate pricing tables ({pricing_headers.count()})")

        # Take screenshot only if issues found
        if issues:
            screenshots_dir = Path('test-screenshots')
            screenshots_dir.mkdir(exist_ok=True)
            page.screenshot(path=str(screenshots_dir / f'{output_name}.png'))

        browser.close()

    return issues

def main():
    base_dir = Path(__file__).parent.parent

    print("=" * 70)
    print("TESTING ALL PAGES")
    print("=" * 70)

    all_files = []

    # Service pages
    services_dir = base_dir / 'services'
    if services_dir.exists():
        all_files.extend([('service', f) for f in services_dir.glob('*.html') if f.name != 'index.html'])

    # Location pages
    locations_dir = base_dir / 'locations'
    if locations_dir.exists():
        all_files.extend([('location', f) for f in locations_dir.glob('*.html') if f.name != 'index.html'])

    print(f"\nTesting {len(all_files)} pages...\n")

    passed = 0
    failed = 0
    all_issues = {}

    for page_type, file_path in all_files:
        issues = test_page(file_path, file_path.stem)

        if issues:
            failed += 1
            all_issues[file_path.name] = issues
            print(f"[FAIL] {file_path.name}: {', '.join(issues)}")
        else:
            passed += 1
            print(f"[PASS] {file_path.name}")

    print("\n" + "=" * 70)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 70)

    if all_issues:
        print("\nFailed pages:")
        for page, issues in all_issues.items():
            print(f"  - {page}: {', '.join(issues)}")

if __name__ == '__main__':
    main()
