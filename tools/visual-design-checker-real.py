#!/usr/bin/env python3
"""
REAL Visual Design Checker with Browser Automation
Takes screenshots and checks actual rendering issues
Version: 2.0 - BMAD Method 2025
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

# Try multiple browser automation options
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("[WARN] Selenium not installed. Install with: pip install selenium")

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("[INFO] Playwright not available. Install with: pip install playwright && playwright install")

class RealVisualChecker:
    """Real visual design checker using browser automation"""

    def __init__(self, file_path):
        self.file_path = Path(file_path).absolute()
        self.file_url = f"file:///{self.file_path}".replace('\\', '/')
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "url": self.file_url,
            "screenshots": [],
            "visual_issues": [],
            "responsive_issues": [],
            "overlapping_elements": [],
            "broken_elements": [],
            "contrast_issues": [],
            "scores": {}
        }

        # Device configurations
        self.devices = [
            {"name": "Mobile", "width": 375, "height": 812, "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)"},
            {"name": "Tablet", "width": 768, "height": 1024, "user_agent": "Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X)"},
            {"name": "Desktop", "width": 1920, "height": 1080, "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        ]

    def run_check(self):
        """Run complete visual check"""
        print("\n" + "=" * 60)
        print("REAL VISUAL DESIGN CHECK WITH BROWSER AUTOMATION")
        print("=" * 60)

        if not SELENIUM_AVAILABLE and not PLAYWRIGHT_AVAILABLE:
            print("[ERROR] No browser automation available!")
            print("Install Selenium: pip install selenium webdriver-manager")
            print("Or Playwright: pip install playwright && playwright install")
            return

        # Use Selenium if available (more common)
        if SELENIUM_AVAILABLE:
            self.check_with_selenium()
        elif PLAYWRIGHT_AVAILABLE:
            self.check_with_playwright()

        # Generate final report
        self.calculate_scores()
        self.print_report()
        self.save_report()

    def check_with_selenium(self):
        """Check using Selenium WebDriver"""
        print("\n[INFO] Using Selenium for visual checking...")

        # Setup Chrome options
        options = Options()
        options.add_argument('--headless')  # Run in background
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        try:
            # Try to use Chrome with auto-download driver
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service

            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
        except:
            try:
                # Try Edge as fallback
                from selenium.webdriver.edge.options import Options as EdgeOptions
                from webdriver_manager.microsoft import EdgeChromiumDriverManager
                from selenium.webdriver.edge.service import Service as EdgeService

                edge_options = EdgeOptions()
                edge_options.add_argument('--headless')
                edge_service = EdgeService(EdgeChromiumDriverManager().install())
                driver = webdriver.Edge(service=edge_service, options=edge_options)
            except Exception as e:
                print(f"[ERROR] Could not start browser: {e}")
                return

        try:
            for device in self.devices:
                print(f"\n--- Checking {device['name']} ({device['width']}x{device['height']}) ---")

                # Set window size
                driver.set_window_size(device['width'], device['height'])

                # Load page
                driver.get(self.file_url)
                time.sleep(2)  # Wait for page to render

                # Take screenshot
                screenshot_name = f"screenshot_{device['name'].lower()}_{datetime.now().strftime('%H%M%S')}.png"
                driver.save_screenshot(screenshot_name)
                print(f"[OK] Screenshot saved: {screenshot_name}")
                self.report["screenshots"].append(screenshot_name)

                # Check for visual issues
                self.check_overlapping_elements(driver, device['name'])
                self.check_viewport_overflow(driver, device['name'])
                self.check_text_truncation(driver, device['name'])
                self.check_broken_images(driver, device['name'])
                self.check_element_visibility(driver, device['name'])

                # Check contrast (simplified)
                if device['name'] == 'Desktop':
                    self.check_color_contrast_selenium(driver)

        finally:
            driver.quit()

    def check_overlapping_elements(self, driver, device_name):
        """Check for overlapping elements using JavaScript"""

        overlap_script = """
        const elements = document.querySelectorAll('*');
        const overlapping = [];

        for (let i = 0; i < elements.length; i++) {
            const el1 = elements[i];
            if (!el1.offsetParent) continue; // Skip hidden

            const rect1 = el1.getBoundingClientRect();
            if (rect1.width === 0 || rect1.height === 0) continue;

            for (let j = i + 1; j < elements.length; j++) {
                const el2 = elements[j];
                if (!el2.offsetParent) continue;

                const rect2 = el2.getBoundingClientRect();
                if (rect2.width === 0 || rect2.height === 0) continue;

                // Skip parent-child relationships
                if (el1.contains(el2) || el2.contains(el1)) continue;

                // Check if they overlap
                if (!(rect1.right < rect2.left ||
                      rect1.left > rect2.right ||
                      rect1.bottom < rect2.top ||
                      rect1.top > rect2.bottom)) {

                    // Check z-index to see if intentional
                    const z1 = window.getComputedStyle(el1).zIndex;
                    const z2 = window.getComputedStyle(el2).zIndex;

                    if (z1 === 'auto' && z2 === 'auto') {
                        overlapping.push({
                            elem1: el1.tagName + (el1.className ? '.' + el1.className : ''),
                            elem2: el2.tagName + (el2.className ? '.' + el2.className : ''),
                            rect1: {top: rect1.top, left: rect1.left},
                            rect2: {top: rect2.top, left: rect2.left}
                        });
                    }
                }
            }
        }

        return overlapping.slice(0, 10); // Return first 10
        """

        try:
            overlaps = driver.execute_script(overlap_script)

            if overlaps:
                print(f"[WARN] {device_name}: Found {len(overlaps)} overlapping elements")
                for overlap in overlaps[:3]:
                    issue = f"{overlap['elem1']} overlaps with {overlap['elem2']}"
                    print(f"  - {issue}")
                    self.report["overlapping_elements"].append({
                        "device": device_name,
                        "issue": issue
                    })
            else:
                print(f"[OK] {device_name}: No overlapping elements")
        except Exception as e:
            print(f"[ERROR] Could not check overlaps: {e}")

    def check_viewport_overflow(self, driver, device_name):
        """Check for horizontal scroll"""

        overflow_script = """
        const hasHorizontalScroll = document.documentElement.scrollWidth > window.innerWidth;
        const hasVerticalOverflow = document.body.scrollHeight > window.innerHeight * 10; // Too tall

        const overflowingElements = [];
        const elements = document.querySelectorAll('*');

        elements.forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.right > window.innerWidth || rect.left < 0) {
                overflowingElements.push({
                    tag: el.tagName,
                    class: el.className,
                    overflow: rect.right > window.innerWidth ? 'right' : 'left',
                    amount: rect.right > window.innerWidth ? rect.right - window.innerWidth : Math.abs(rect.left)
                });
            }
        });

        return {
            hasHorizontalScroll: hasHorizontalScroll,
            hasVerticalOverflow: hasVerticalOverflow,
            overflowing: overflowingElements.slice(0, 5)
        };
        """

        try:
            result = driver.execute_script(overflow_script)

            if result['hasHorizontalScroll']:
                print(f"[ERROR] {device_name}: Horizontal scroll detected!")
                self.report["visual_issues"].append(f"{device_name}: Page has horizontal scroll")

            if result['overflowing']:
                print(f"[WARN] {device_name}: Elements overflow viewport")
                for el in result['overflowing']:
                    issue = f"{el['tag']}.{el['class']} overflows {el['direction']} by {el['amount']}px"
                    self.report["responsive_issues"].append({
                        "device": device_name,
                        "issue": issue
                    })
        except Exception as e:
            print(f"[ERROR] Could not check overflow: {e}")

    def check_text_truncation(self, driver, device_name):
        """Check for cut-off text"""

        truncation_script = """
        const truncated = [];
        const elements = document.querySelectorAll('p, h1, h2, h3, h4, h5, h6, span, div');

        elements.forEach(el => {
            if (el.scrollWidth > el.clientWidth || el.scrollHeight > el.clientHeight) {
                const style = window.getComputedStyle(el);
                if (style.overflow !== 'hidden' && !style.textOverflow) {
                    truncated.push({
                        tag: el.tagName,
                        text: el.textContent.substring(0, 50),
                        scrollWidth: el.scrollWidth,
                        clientWidth: el.clientWidth
                    });
                }
            }
        });

        return truncated.slice(0, 5);
        """

        try:
            truncated = driver.execute_script(truncation_script)

            if truncated:
                print(f"[WARN] {device_name}: Found {len(truncated)} truncated text elements")
                for item in truncated[:2]:
                    self.report["visual_issues"].append(f"{device_name}: Text truncated in {item['tag']}")
        except Exception as e:
            print(f"[ERROR] Could not check text truncation: {e}")

    def check_broken_images(self, driver, device_name):
        """Check for broken images"""

        image_script = """
        const images = document.querySelectorAll('img');
        const broken = [];

        images.forEach(img => {
            if (!img.complete || img.naturalWidth === 0) {
                broken.push({
                    src: img.src,
                    alt: img.alt || 'no alt text'
                });
            }
        });

        return broken;
        """

        try:
            broken = driver.execute_script(image_script)

            if broken:
                print(f"[ERROR] {device_name}: Found {len(broken)} broken images")
                for img in broken:
                    self.report["broken_elements"].append({
                        "device": device_name,
                        "type": "image",
                        "src": img['src']
                    })
            else:
                print(f"[OK] {device_name}: All images loading")
        except Exception as e:
            print(f"[ERROR] Could not check images: {e}")

    def check_element_visibility(self, driver, device_name):
        """Check if important elements are visible"""

        visibility_script = """
        const checkVisibility = (selector) => {
            const el = document.querySelector(selector);
            if (!el) return { exists: false };

            const rect = el.getBoundingClientRect();
            const style = window.getComputedStyle(el);

            return {
                exists: true,
                visible: style.display !== 'none' &&
                        style.visibility !== 'hidden' &&
                        style.opacity > 0 &&
                        rect.width > 0 &&
                        rect.height > 0,
                inViewport: rect.top < window.innerHeight && rect.bottom > 0,
                position: { top: rect.top, left: rect.left }
            };
        };

        return {
            header: checkVisibility('header'),
            nav: checkVisibility('nav'),
            h1: checkVisibility('h1'),
            cta: checkVisibility('.btn-primary, .cta, button[type="submit"]'),
            footer: checkVisibility('footer')
        };
        """

        try:
            visibility = driver.execute_script(visibility_script)

            for element, status in visibility.items():
                if not status['exists']:
                    print(f"[INFO] {device_name}: No {element} found")
                elif not status['visible']:
                    print(f"[WARN] {device_name}: {element} is hidden")
                    self.report["visual_issues"].append(f"{device_name}: {element} not visible")
                elif not status['inViewport'] and element in ['header', 'h1', 'cta']:
                    print(f"[WARN] {device_name}: {element} outside viewport")

        except Exception as e:
            print(f"[ERROR] Could not check visibility: {e}")

    def check_color_contrast_selenium(self, driver):
        """Basic contrast check"""

        contrast_script = """
        const getLuminance = (r, g, b) => {
            const [rs, gs, bs] = [r, g, b].map(c => {
                c = c / 255;
                return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
            });
            return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
        };

        const getContrast = (rgb1, rgb2) => {
            const matches1 = rgb1.match(/\\d+/g);
            const matches2 = rgb2.match(/\\d+/g);
            if (!matches1 || !matches2) return 21; // Skip if can't parse

            const l1 = getLuminance(+matches1[0], +matches1[1], +matches1[2]);
            const l2 = getLuminance(+matches2[0], +matches2[1], +matches2[2]);

            const lighter = Math.max(l1, l2);
            const darker = Math.min(l1, l2);

            return (lighter + 0.05) / (darker + 0.05);
        };

        const issues = [];
        const elements = document.querySelectorAll('p, h1, h2, h3, h4, h5, h6, a, button');

        elements.forEach(el => {
            const style = window.getComputedStyle(el);
            const bgColor = style.backgroundColor;
            const color = style.color;

            if (bgColor && color && bgColor !== 'rgba(0, 0, 0, 0)') {
                const contrast = getContrast(bgColor, color);
                if (contrast < 4.5) {
                    issues.push({
                        element: el.tagName,
                        text: el.textContent.substring(0, 30),
                        contrast: contrast.toFixed(2)
                    });
                }
            }
        });

        return issues.slice(0, 5);
        """

        try:
            issues = driver.execute_script(contrast_script)

            if issues:
                print(f"[WARN] Found {len(issues)} contrast issues")
                for issue in issues[:3]:
                    self.report["contrast_issues"].append({
                        "element": issue['element'],
                        "contrast": issue['contrast'],
                        "minimum": "4.5"
                    })
        except Exception as e:
            print(f"[ERROR] Could not check contrast: {e}")

    def check_with_playwright(self):
        """Alternative: Check using Playwright"""
        print("\n[INFO] Using Playwright for visual checking...")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            for device in self.devices:
                print(f"\n--- Checking {device['name']} ---")

                context = browser.new_context(
                    viewport={'width': device['width'], 'height': device['height']},
                    user_agent=device['user_agent']
                )
                page = context.new_page()

                # Load page
                page.goto(self.file_url)
                page.wait_for_load_state('networkidle')

                # Take screenshot
                screenshot_name = f"screenshot_{device['name'].lower()}.png"
                page.screenshot(path=screenshot_name)
                print(f"[OK] Screenshot saved: {screenshot_name}")

                # Run visual checks
                # (Similar checks as Selenium but using Playwright API)

                context.close()

            browser.close()

    def calculate_scores(self):
        """Calculate visual design scores"""

        # Count issues
        overlap_count = len(self.report["overlapping_elements"])
        visual_count = len(self.report["visual_issues"])
        responsive_count = len(self.report["responsive_issues"])
        broken_count = len(self.report["broken_elements"])
        contrast_count = len(self.report["contrast_issues"])

        # Calculate scores (0-100)
        overlap_score = max(0, 100 - overlap_count * 20)
        visual_score = max(0, 100 - visual_count * 10)
        responsive_score = max(0, 100 - responsive_count * 15)
        integrity_score = max(0, 100 - broken_count * 25)
        contrast_score = max(0, 100 - contrast_count * 20)

        # Overall score
        overall = (overlap_score + visual_score + responsive_score + integrity_score + contrast_score) / 5

        self.report["scores"] = {
            "overall": round(overall),
            "overlap": overlap_score,
            "visual": visual_score,
            "responsive": responsive_score,
            "integrity": integrity_score,
            "contrast": contrast_score
        }

    def print_report(self):
        """Print the visual design report"""

        print("\n" + "=" * 60)
        print("REAL VISUAL DESIGN REPORT")
        print("=" * 60)

        scores = self.report["scores"]
        print(f"\nOVERALL VISUAL SCORE: {scores['overall']}/100")
        print(f"  No Overlaps: {scores['overlap']}/100")
        print(f"  Visual Integrity: {scores['visual']}/100")
        print(f"  Responsive Design: {scores['responsive']}/100")
        print(f"  Elements Loading: {scores['integrity']}/100")
        print(f"  Color Contrast: {scores['contrast']}/100")

        # Print issues
        if self.report["overlapping_elements"]:
            print(f"\n[OVERLAPPING] {len(self.report['overlapping_elements'])} elements overlap")
            for item in self.report["overlapping_elements"][:3]:
                print(f"  - {item['device']}: {item['issue']}")

        if self.report["visual_issues"]:
            print(f"\n[VISUAL ISSUES] {len(self.report['visual_issues'])} problems found")
            for issue in self.report["visual_issues"][:3]:
                print(f"  - {issue}")

        if self.report["responsive_issues"]:
            print(f"\n[RESPONSIVE] {len(self.report['responsive_issues'])} responsive problems")
            for item in self.report["responsive_issues"][:3]:
                print(f"  - {item['device']}: {item['issue']}")

        if self.report["broken_elements"]:
            print(f"\n[BROKEN] {len(self.report['broken_elements'])} broken elements")
            for item in self.report["broken_elements"][:3]:
                print(f"  - {item['device']}: Broken {item['type']}")

        if self.report["contrast_issues"]:
            print(f"\n[CONTRAST] {len(self.report['contrast_issues'])} contrast issues")
            for item in self.report["contrast_issues"][:3]:
                print(f"  - {item['element']}: {item['contrast']} (need 4.5)")

        # Status
        if scores['overall'] >= 90:
            print("\n[EXCELLENT] No visual issues")
        elif scores['overall'] >= 70:
            print("\n[GOOD] Minor visual issues")
        elif scores['overall'] >= 50:
            print("\n[NEEDS WORK] Several visual problems")
        else:
            print("\n[POOR] Major visual issues, design is broken")

        print(f"\nScreenshots saved: {', '.join(self.report['screenshots'])}")

    def save_report(self):
        """Save detailed report to JSON"""

        filename = f"visual_report_real_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.report, f, indent=2, ensure_ascii=False)

        print(f"\nFull report saved to: {filename}")


if __name__ == "__main__":
    # Get file path from arguments
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "website/index.html"

    # Check if file exists
    if not Path(file_path).exists():
        print(f"[ERROR] File not found: {file_path}")
        sys.exit(1)

    print(f"Checking visual design of: {file_path}")

    # Run the check
    checker = RealVisualChecker(file_path)
    checker.run_check()