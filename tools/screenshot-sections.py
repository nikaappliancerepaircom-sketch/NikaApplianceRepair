#!/usr/bin/env python3
"""
Take screenshots of specific sections
"""

from playwright.sync_api import sync_playwright
from pathlib import Path
import time

def screenshot_sections(html_file):
    """Take screenshots of specific sections"""

    html_path = Path(html_file).absolute()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})

        # Load local HTML file
        page.goto(f'file:///{html_path}')
        time.sleep(2)

        screenshots_dir = Path('screenshots')
        screenshots_dir.mkdir(exist_ok=True)

        # 1. Hero section
        hero = page.locator('section.hero-section').first
        if hero.count() > 0:
            hero.screenshot(path=str(screenshots_dir / 'hero-section.png'))
            print("[OK] Hero section")

        # 2. Pricing table
        pricing = page.locator('h3:has-text("Transparent Pricing")').first
        if pricing.count() > 0:
            parent = pricing.locator('xpath=ancestor::div[1]')
            parent.screenshot(path=str(screenshots_dir / 'pricing-table.png'))
            print("[OK] Pricing table")

        # 3. Blue FAQ section
        blue_section = page.locator('.voice-search-content').first
        if blue_section.count() > 0:
            blue_section.screenshot(path=str(screenshots_dir / 'blue-faq.png'))
            print("[OK] Blue FAQ section")

        # 4. Service features
        features = page.locator('.service-feature-icons').first
        if features.count() > 0:
            features.screenshot(path=str(screenshots_dir / 'service-features.png'))
            print("[OK] Service features")

        browser.close()

def main():
    base_dir = Path(__file__).parent.parent
    page_path = base_dir / 'services' / 'refrigerator-repair.html'

    print("Taking section screenshots...\n")

    if page_path.exists():
        screenshot_sections(page_path)
        print("\nAll screenshots saved to screenshots/")
    else:
        print(f"File not found: {page_path}")

if __name__ == '__main__':
    main()
