#!/usr/bin/env python3
"""
Test for ACTUAL horizontal scroll (not just element positioning)
This checks if the DOCUMENT actually has horizontal scroll, not individual elements
"""

from playwright.sync_api import sync_playwright
import sys

def test_actual_horizontal_scroll(url):
    """Test if page actually has horizontal scrollbar"""
    print("=" * 70)
    print("TESTING ACTUAL HORIZONTAL SCROLL")
    print("=" * 70)
    print()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)

        # Test on multiple devices
        devices = [
            {'name': 'iPhone SE', 'width': 375, 'height': 667},
            {'name': 'iPhone 12 Pro', 'width': 390, 'height': 844},
            {'name': 'Samsung Galaxy S21', 'width': 360, 'height': 800},
            {'name': 'iPhone 14 Pro Max', 'width': 430, 'height': 932},
            {'name': 'iPad Mini', 'width': 768, 'height': 1024},
            {'name': 'iPad Air', 'width': 820, 'height': 1180},
            {'name': 'iPad Pro', 'width': 1024, 'height': 1366},
            {'name': 'Laptop', 'width': 1366, 'height': 768},
            {'name': 'Desktop HD', 'width': 1920, 'height': 1080},
            {'name': 'Desktop 4K', 'width': 2560, 'height': 1440},
        ]

        all_pass = True
        failed_devices = []

        for device in devices:
            print(f"\n{'=' * 70}")
            print(f"TESTING: {device['name']} ({device['width']}x{device['height']})")
            print(f"{'=' * 70}\n")

            context = browser.new_context(viewport={'width': device['width'], 'height': device['height']})
            page = context.new_page()
            page.goto(url)

            # Wait for page to load and AOS to initialize
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(2000)  # Wait for AOS animations

            # Check DOCUMENT scroll width vs viewport
            scroll_info = page.evaluate('''
                () => {
                    return {
                        documentScrollWidth: document.documentElement.scrollWidth,
                        documentClientWidth: document.documentElement.clientWidth,
                        bodyScrollWidth: document.body.scrollWidth,
                        bodyClientWidth: document.body.clientWidth,
                        windowInnerWidth: window.innerWidth
                    };
                }
            ''')

            doc_overflow = scroll_info['documentScrollWidth'] - scroll_info['windowInnerWidth']
            body_overflow = scroll_info['bodyScrollWidth'] - scroll_info['windowInnerWidth']

            # Check if there's ACTUAL horizontal scrollbar
            has_horizontal_scroll = doc_overflow > 0 or body_overflow > 0

            print(f"  Document ScrollWidth:  {scroll_info['documentScrollWidth']}px")
            print(f"  Window InnerWidth:     {scroll_info['windowInnerWidth']}px")
            print(f"  Document Overflow:     {doc_overflow}px")
            print()
            print(f"  Body ScrollWidth:      {scroll_info['bodyScrollWidth']}px")
            print(f"  Body ClientWidth:      {scroll_info['bodyClientWidth']}px")
            print(f"  Body Overflow:         {body_overflow}px")
            print()

            if has_horizontal_scroll:
                print(f"  [FAIL] Horizontal scroll detected!")
                all_pass = False
                failed_devices.append({
                    'name': device['name'],
                    'doc_overflow': doc_overflow,
                    'body_overflow': body_overflow
                })
            else:
                print(f"  [PASS] No horizontal scroll")

            # Try to actually scroll horizontally to confirm
            page.evaluate("window.scrollTo(1000, 0)")
            actual_scroll_x = page.evaluate("window.scrollX")

            if actual_scroll_x > 0:
                print(f"  [FAIL] Page actually scrolled horizontally by {actual_scroll_x}px!")
                if not has_horizontal_scroll:
                    all_pass = False
                    failed_devices.append({
                        'name': device['name'],
                        'actual_scroll': actual_scroll_x
                    })
            else:
                print(f"  [PASS] Cannot scroll horizontally (locked)")

            # Take screenshot
            screenshot_name = f"scroll_test_{device['name'].lower().replace(' ', '_')}_{device['width']}x{device['height']}.png"
            page.screenshot(path=screenshot_name, full_page=True)
            print(f"\n  [SAVED] {screenshot_name}")

            context.close()

        browser.close()

        # Summary
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)

        if all_pass:
            print("\n[SUCCESS] No horizontal scroll on any device!")
            print("All devices passed the scroll test.")
        else:
            print(f"\n[FAILED] Found horizontal scroll on {len(failed_devices)} device(s):\n")
            for device in failed_devices:
                print(f"  - {device['name']}")
                if 'doc_overflow' in device:
                    print(f"    Document overflow: {device['doc_overflow']}px")
                if 'body_overflow' in device:
                    print(f"    Body overflow: {device['body_overflow']}px")
                if 'actual_scroll' in device:
                    print(f"    Actual scroll: {device['actual_scroll']}px")
                print()

        print("=" * 70)

        return 0 if all_pass else 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test-actual-scroll.py <html_file_path>")
        sys.exit(1)

    html_file = sys.argv[1]

    # Convert to file:// URL
    import os
    from pathlib import Path

    full_path = Path(html_file).resolve()
    url = f"file:///{full_path}".replace("\\", "/")

    exit_code = test_actual_horizontal_scroll(url)
    sys.exit(exit_code)