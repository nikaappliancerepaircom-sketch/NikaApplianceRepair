#!/usr/bin/env python3
"""
Quick test of key pages
"""

from playwright.sync_api import sync_playwright
from pathlib import Path
import time

def test_and_screenshot(html_file, name):
    """Test page and screenshot"""

    html_path = Path(html_file).absolute()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})

        page.goto(f'file:///{html_path}')
        time.sleep(2)

        # Full page screenshot
        screenshots_dir = Path('final-test')
        screenshots_dir.mkdir(exist_ok=True)
        page.screenshot(path=str(screenshots_dir / f'{name}-full.png'), full_page=True)

        print(f"[OK] {name}")

        browser.close()

def main():
    base_dir = Path(__file__).parent.parent

    print("Quick testing key pages...\n")

    # Test 3 different pages
    pages = [
        (base_dir / 'services' / 'dishwasher-repair.html', 'dishwasher'),
        (base_dir / 'services' / 'dryer-repair.html', 'dryer'),
        (base_dir / 'locations' / 'toronto.html', 'toronto'),
    ]

    for file_path, name in pages:
        if file_path.exists():
            test_and_screenshot(file_path, name)

    print("\nScreenshots saved to final-test/")

if __name__ == '__main__':
    main()
