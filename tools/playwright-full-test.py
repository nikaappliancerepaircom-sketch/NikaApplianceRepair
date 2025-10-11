#!/usr/bin/env python3
"""
Full Playwright test for all 62 pages
Tests header/footer links, dropdowns, responsive design
"""

import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright
from datetime import datetime

class PlaywrightTester:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.results = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_pages': 0,
            'passed': 0,
            'failed': 0,
            'details': {}
        }

    async def test_page(self, page, file_path, url):
        """Test a single page"""
        print(f"\n[TESTING] {file_path.name}")

        result = {
            'url': url,
            'path': str(file_path),
            'tests': {},
            'issues': [],
            'passed': True
        }

        try:
            # Navigate to page
            await page.goto(url, wait_until='networkidle', timeout=10000)
            await page.wait_for_load_state('domcontentloaded')

            # Test 1: Header dropdown exists
            dropdown = await page.query_selector('.has-dropdown')
            result['tests']['header_dropdown_exists'] = dropdown is not None
            if not dropdown:
                result['issues'].append('Header dropdown not found')
                result['passed'] = False

            # Test 2: Hover over dropdown and check if menu appears
            if dropdown:
                await dropdown.hover()
                await page.wait_for_timeout(500)  # Wait for CSS transition

                menu = await page.query_selector('.dropdown-menu')
                is_visible = await menu.is_visible() if menu else False
                result['tests']['dropdown_menu_visible'] = is_visible

                if not is_visible:
                    result['issues'].append('Dropdown menu not visible on hover')
                    result['passed'] = False

            # Test 3: Check dropdown links
            dropdown_links = await page.query_selector_all('.dropdown-menu a')
            result['tests']['dropdown_links_count'] = len(dropdown_links)

            if len(dropdown_links) < 8:
                result['issues'].append(f'Only {len(dropdown_links)} dropdown links found, expected 8')
                result['passed'] = False

            # Test 4: Footer Service Areas section exists
            footer_areas = await page.query_selector('footer .footer-column:has(h4:text("Service Areas"))')
            result['tests']['footer_service_areas'] = footer_areas is not None

            if not footer_areas:
                result['issues'].append('Footer Service Areas section not found')
                result['passed'] = False

            # Test 5: Count footer location links
            if footer_areas:
                footer_links = await footer_areas.query_selector_all('a')
                result['tests']['footer_links_count'] = len(footer_links)

                if len(footer_links) < 8:
                    result['issues'].append(f'Only {len(footer_links)} footer links found, expected 8')
                    result['passed'] = False

            # Test 6: Test one dropdown link click (without navigation)
            if dropdown_links and len(dropdown_links) > 0:
                first_link = dropdown_links[0]
                href = await first_link.get_attribute('href')
                result['tests']['sample_dropdown_href'] = href

                # Check if href is valid
                if not href or href == '#':
                    result['issues'].append('Dropdown link has invalid href')
                    result['passed'] = False

            # Test 7: Check responsive typography CSS is loaded
            responsive_css = await page.query_selector('link[href*="responsive-typography.css"]')
            result['tests']['responsive_typography_loaded'] = responsive_css is not None

            # Test 8: Check if h1 uses CSS clamp
            h1 = await page.query_selector('h1')
            if h1:
                font_size = await h1.evaluate('el => window.getComputedStyle(el).fontSize')
                result['tests']['h1_font_size'] = font_size

            # Test 9: Mobile viewport test
            await page.set_viewport_size({'width': 375, 'height': 667})
            await page.wait_for_timeout(500)

            mobile_menu = await page.query_selector('.mobile-menu-toggle')
            result['tests']['mobile_menu_exists'] = mobile_menu is not None

            # Test 10: Check for console errors
            console_errors = []
            page.on('console', lambda msg: console_errors.append(msg.text) if msg.type == 'error' else None)

            result['tests']['console_errors'] = len(console_errors)
            if len(console_errors) > 0:
                result['issues'].append(f'{len(console_errors)} console errors found')

            # Screenshot
            screenshot_path = self.base_dir / 'screenshots' / f'{file_path.stem}.png'
            screenshot_path.parent.mkdir(exist_ok=True)
            await page.screenshot(path=str(screenshot_path), full_page=True)
            result['screenshot'] = str(screenshot_path)

            print(f"  [{'PASS' if result['passed'] else 'FAIL'}] {file_path.name}")
            if result['issues']:
                for issue in result['issues']:
                    print(f"    - {issue}")

        except Exception as e:
            result['passed'] = False
            result['issues'].append(f'Error: {str(e)}')
            print(f"  [ERROR] {file_path.name}: {e}")

        return result

    async def run_all_tests(self):
        """Run tests on all pages"""
        print("=" * 60)
        print("PLAYWRIGHT FULL PAGE TESTING")
        print("=" * 60)

        # Get all HTML files
        all_files = []
        all_files.append(self.base_dir / 'index.html')

        for subdir in ['services', 'locations', 'blog']:
            dir_path = self.base_dir / subdir
            all_files.extend([f for f in dir_path.glob('*.html') if f.name != 'index.html'])

        self.results['total_pages'] = len(all_files)

        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080}
            )
            page = await context.new_page()

            # Start local server (using Python's http.server)
            import subprocess
            import threading
            import time

            def run_server():
                subprocess.run([
                    'python', '-m', 'http.server', '8080',
                    '--directory', str(self.base_dir)
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            server_thread = threading.Thread(target=run_server, daemon=True)
            server_thread.start()
            time.sleep(2)  # Wait for server to start

            # Test all pages
            for file_path in all_files:
                relative_path = file_path.relative_to(self.base_dir)
                url = f'http://localhost:8080/{relative_path.as_posix()}'

                result = await self.test_page(page, file_path, url)
                self.results['details'][str(relative_path)] = result

                if result['passed']:
                    self.results['passed'] += 1
                else:
                    self.results['failed'] += 1

            await browser.close()

        # Save results
        results_file = self.base_dir / f'playwright_test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2)

        print("\n" + "=" * 60)
        print(f"TOTAL: {self.results['total_pages']} pages")
        print(f"PASSED: {self.results['passed']}")
        print(f"FAILED: {self.results['failed']}")
        print(f"\nResults saved to: {results_file}")
        print("=" * 60)

        return self.results

async def main():
    tester = PlaywrightTester()
    await tester.run_all_tests()

if __name__ == '__main__':
    asyncio.run(main())
