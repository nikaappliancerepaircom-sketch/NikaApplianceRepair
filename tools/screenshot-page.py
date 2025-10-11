#!/usr/bin/env python3
"""
Take screenshots of pages using Playwright
"""

from playwright.sync_api import sync_playwright
from pathlib import Path
import time

def screenshot_page(html_file, output_name):
    """Take full page screenshot"""

    html_path = Path(html_file).absolute()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})

        # Load local HTML file
        page.goto(f'file:///{html_path}')

        # Wait for page to load
        time.sleep(2)

        # Take screenshot
        screenshot_path = Path('screenshots') / f'{output_name}.png'
        screenshot_path.parent.mkdir(exist_ok=True)

        page.screenshot(path=str(screenshot_path), full_page=True)

        browser.close()

        print(f"Screenshot saved: {screenshot_path}")
        return screenshot_path

def main():
    base_dir = Path(__file__).parent.parent

    print("Taking screenshots...")

    # Screenshot refrigerator-repair page
    page_path = base_dir / 'services' / 'refrigerator-repair.html'

    if page_path.exists():
        screenshot_page(page_path, 'refrigerator-repair-full')
        print(f"\nScreenshot complete!")
    else:
        print(f"File not found: {page_path}")

if __name__ == '__main__':
    main()
