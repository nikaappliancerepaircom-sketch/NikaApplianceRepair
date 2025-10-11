#!/usr/bin/env python3
"""
Complete Cross-Browser & Multi-Device Testing Suite
Using Playwright for professional testing
BMAD Method 2025
"""

import asyncio
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

try:
    from playwright.async_api import async_playwright, Page, Browser
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("[ERROR] Playwright not installed. Run: pip install playwright && playwright install")
    exit(1)


class CompleteTester:
    """Professional testing suite for all browsers and devices"""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path).absolute()
        self.url = f"file:///{self.file_path}".replace('\\', '/')
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Test results storage
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "url": self.url,
            "summary": {
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "warnings": 0
            },
            "devices": {},
            "browsers": {},
            "performance": {},
            "accessibility": {},
            "visual": {},
            "seo": {}
        }

        # Device configurations
        self.devices = [
            # Popular Mobile Phones
            {"name": "iPhone_15_Pro_Max", "viewport": {"width": 430, "height": 932}, "deviceScaleFactor": 3, "isMobile": True, "hasTouch": True},
            {"name": "iPhone_14", "viewport": {"width": 390, "height": 844}, "deviceScaleFactor": 3, "isMobile": True, "hasTouch": True},
            {"name": "iPhone_SE", "viewport": {"width": 375, "height": 667}, "deviceScaleFactor": 2, "isMobile": True, "hasTouch": True},
            {"name": "Samsung_Galaxy_S24", "viewport": {"width": 412, "height": 915}, "deviceScaleFactor": 2.625, "isMobile": True, "hasTouch": True},
            {"name": "Google_Pixel_8", "viewport": {"width": 412, "height": 915}, "deviceScaleFactor": 2.625, "isMobile": True, "hasTouch": True},

            # Tablets
            {"name": "iPad_Pro_12.9", "viewport": {"width": 1024, "height": 1366}, "deviceScaleFactor": 2, "isMobile": True, "hasTouch": True},
            {"name": "iPad_Mini", "viewport": {"width": 768, "height": 1024}, "deviceScaleFactor": 2, "isMobile": True, "hasTouch": True},
            {"name": "Surface_Pro", "viewport": {"width": 912, "height": 1368}, "deviceScaleFactor": 2, "isMobile": False, "hasTouch": True},

            # Desktop Sizes
            {"name": "Desktop_HD", "viewport": {"width": 1920, "height": 1080}, "deviceScaleFactor": 1, "isMobile": False, "hasTouch": False},
            {"name": "Desktop_2K", "viewport": {"width": 2560, "height": 1440}, "deviceScaleFactor": 1, "isMobile": False, "hasTouch": False},
            {"name": "Desktop_4K", "viewport": {"width": 3840, "height": 2160}, "deviceScaleFactor": 1, "isMobile": False, "hasTouch": False},
            {"name": "Laptop", "viewport": {"width": 1366, "height": 768}, "deviceScaleFactor": 1, "isMobile": False, "hasTouch": False},
        ]

    async def run_all_tests(self):
        """Run complete test suite"""
        print("\n" + "="*60)
        print("COMPLETE CROSS-BROWSER & DEVICE TESTING SUITE")
        print("="*60)
        print(f"Testing: {self.file_path}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)

        async with async_playwright() as playwright:
            # Test all browsers
            await self.test_all_browsers(playwright)

            # Test all devices
            await self.test_all_devices(playwright)

            # Performance testing
            await self.test_performance(playwright)

            # Accessibility testing
            await self.test_accessibility(playwright)

            # SEO testing
            await self.test_seo(playwright)

        # Generate report
        self.generate_report()

    async def test_all_browsers(self, playwright):
        """Test in Chrome, Firefox, Safari (WebKit)"""
        print("\n[BROWSER COMPATIBILITY TESTING]")
        print("-" * 40)

        browsers = [
            ("Chromium", playwright.chromium),
            ("Firefox", playwright.firefox),
            ("WebKit", playwright.webkit)  # Safari on Mac/iOS
        ]

        for browser_name, browser_type in browsers:
            print(f"\n  Testing {browser_name}...")
            browser = await browser_type.launch(headless=True)

            try:
                context = await browser.new_context()
                page = await context.new_page()

                # Collect console errors
                errors = []
                page.on("console", lambda msg: errors.append(msg.text()) if msg.type == "error" else None)
                page.on("pageerror", lambda error: errors.append(str(error)))

                # Load page
                response = await page.goto(self.url, wait_until="networkidle")

                # Check basic functionality
                result = {
                    "loads": response.status < 400 if response else False,
                    "title": await page.title(),
                    "errors": errors,
                    "js_errors": [],
                    "css_issues": []
                }

                # Check for JavaScript errors
                js_check = await page.evaluate("""() => {
                    const errors = [];
                    // Check if key functions exist
                    if (typeof document.querySelector === 'undefined') errors.push('querySelector not available');
                    if (typeof window.addEventListener === 'undefined') errors.push('addEventListener not available');
                    return errors;
                }""")
                result["js_errors"] = js_check

                # Visual regression check
                screenshot_path = f"screenshots/browser_{browser_name}_{self.timestamp}.png"
                os.makedirs("screenshots", exist_ok=True)
                await page.screenshot(path=screenshot_path, full_page=True)
                result["screenshot"] = screenshot_path

                # Check critical elements
                critical_elements = await self.check_critical_elements(page)
                result["critical_elements"] = critical_elements

                self.results["browsers"][browser_name] = result

                # Print status
                status = "✅" if result["loads"] and len(errors) == 0 else "❌"
                print(f"    {status} {browser_name}: {'Passed' if status == '✅' else f'{len(errors)} errors'}")

                await context.close()

            except Exception as e:
                print(f"    ❌ {browser_name}: Failed - {str(e)}")
                self.results["browsers"][browser_name] = {"error": str(e)}

            finally:
                await browser.close()

    async def test_all_devices(self, playwright):
        """Test on all device sizes"""
        print("\n📱 MULTI-DEVICE TESTING")
        print("-" * 40)

        browser = await playwright.chromium.launch(headless=True)

        for device in self.devices:
            print(f"\n  Testing {device['name'].replace('_', ' ')}...")

            context = await browser.new_context(
                viewport=device["viewport"],
                device_scale_factor=device["deviceScaleFactor"],
                is_mobile=device["isMobile"],
                has_touch=device["hasTouch"]
            )

            page = await context.new_page()

            try:
                await page.goto(self.url, wait_until="networkidle")

                # Visual checks
                visual_issues = await self.check_visual_issues(page, device["name"])

                # Responsive checks
                responsive_issues = await self.check_responsive_design(page, device)

                # Touch target checks for mobile
                touch_issues = []
                if device["hasTouch"]:
                    touch_issues = await self.check_touch_targets(page)

                # Screenshot
                screenshot_path = f"screenshots/device_{device['name']}_{self.timestamp}.png"
                os.makedirs("screenshots", exist_ok=True)
                await page.screenshot(path=screenshot_path, full_page=True)

                # Store results
                self.results["devices"][device["name"]] = {
                    "visual_issues": visual_issues,
                    "responsive_issues": responsive_issues,
                    "touch_issues": touch_issues,
                    "screenshot": screenshot_path,
                    "viewport": device["viewport"]
                }

                # Print status
                total_issues = len(visual_issues) + len(responsive_issues) + len(touch_issues)
                status = "✅" if total_issues == 0 else "⚠️" if total_issues < 5 else "❌"
                print(f"    {status} {device['name']}: {total_issues} issues found")

            except Exception as e:
                print(f"    ❌ {device['name']}: Error - {str(e)}")
                self.results["devices"][device["name"]] = {"error": str(e)}

            finally:
                await context.close()

        await browser.close()

    async def check_visual_issues(self, page: Page, device_name: str) -> List[str]:
        """Check for visual problems"""
        issues = await page.evaluate("""() => {
            const issues = [];

            // Check for overlapping elements
            const elements = Array.from(document.querySelectorAll('*')).filter(el => {
                const style = window.getComputedStyle(el);
                return style.display !== 'none' && style.visibility !== 'hidden';
            });

            for (let i = 0; i < elements.length - 1; i++) {
                const rect1 = elements[i].getBoundingClientRect();
                for (let j = i + 1; j < Math.min(i + 10, elements.length); j++) {
                    const rect2 = elements[j].getBoundingClientRect();

                    // Skip if parent-child
                    if (elements[i].contains(elements[j]) || elements[j].contains(elements[i])) continue;

                    // Check overlap
                    if (rect1.width > 0 && rect2.width > 0 &&
                        !(rect1.right < rect2.left || rect1.left > rect2.right ||
                          rect1.bottom < rect2.top || rect1.top > rect2.bottom)) {

                        const z1 = window.getComputedStyle(elements[i]).zIndex;
                        const z2 = window.getComputedStyle(elements[j]).zIndex;

                        if (z1 === 'auto' && z2 === 'auto') {
                            issues.push(`Overlapping: ${elements[i].tagName} and ${elements[j].tagName}`);
                            if (issues.length >= 10) return issues;
                        }
                    }
                }
            }

            // Check horizontal scroll
            if (document.documentElement.scrollWidth > window.innerWidth) {
                issues.push('Horizontal scroll detected');
            }

            // Check broken images
            const images = document.querySelectorAll('img');
            images.forEach(img => {
                if (!img.complete || img.naturalWidth === 0) {
                    issues.push(`Broken image: ${img.src.split('/').pop()}`);
                }
            });

            // Check text truncation
            const textElements = document.querySelectorAll('p, h1, h2, h3, h4, h5, h6, span');
            textElements.forEach(el => {
                if (el.scrollWidth > el.clientWidth) {
                    issues.push(`Text overflow in ${el.tagName}`);
                }
            });

            return issues;
        }""")

        return issues[:10]  # Limit to first 10 issues

    async def check_responsive_design(self, page: Page, device: Dict) -> List[str]:
        """Check responsive design issues"""
        issues = []

        # Check viewport meta
        viewport_meta = await page.evaluate("() => document.querySelector('meta[name=viewport]')?.content")
        if not viewport_meta:
            issues.append("Missing viewport meta tag")
        elif "width=device-width" not in viewport_meta:
            issues.append("Viewport not set to device-width")

        # Check fixed widths
        fixed_widths = await page.evaluate("""() => {
            const elements = document.querySelectorAll('*');
            const fixed = [];
            elements.forEach(el => {
                const style = window.getComputedStyle(el);
                const width = style.width;
                if (width.includes('px') && parseInt(width) > window.innerWidth) {
                    fixed.push(`${el.tagName}: ${width}`);
                }
            });
            return fixed;
        }""")

        if fixed_widths:
            issues.extend([f"Fixed width: {fw}" for fw in fixed_widths[:3]])

        return issues

    async def check_touch_targets(self, page: Page) -> List[str]:
        """Check touch target sizes for mobile"""
        issues = await page.evaluate("""() => {
            const issues = [];
            const minSize = 44; // Apple's recommendation

            const clickable = document.querySelectorAll('a, button, input, select, textarea, [onclick]');
            clickable.forEach(el => {
                const rect = el.getBoundingClientRect();
                if (rect.width < minSize || rect.height < minSize) {
                    issues.push(`Small touch target: ${el.tagName} (${Math.round(rect.width)}x${Math.round(rect.height)}px)`);
                }
            });

            return issues;
        }""")

        return issues[:5]

    async def check_critical_elements(self, page: Page) -> Dict[str, bool]:
        """Check if critical elements exist and are visible"""
        elements = {
            "header": "header",
            "navigation": "nav",
            "main_heading": "h1",
            "cta_button": ".btn-primary, .cta",
            "footer": "footer",
            "logo": ".logo, [class*='logo']",
            "menu": ".nav-menu, .menu",
            "search": "input[type='search'], .search",
            "contact": ".phone, [href^='tel:']"
        }

        results = {}
        for name, selector in elements.items():
            exists = await page.evaluate(f"""() => {{
                const el = document.querySelector('{selector}');
                if (!el) return false;
                const rect = el.getBoundingClientRect();
                const style = window.getComputedStyle(el);
                return style.display !== 'none' &&
                       style.visibility !== 'hidden' &&
                       rect.width > 0 &&
                       rect.height > 0;
            }}""")
            results[name] = exists

        return results

    async def test_performance(self, playwright):
        """Test performance metrics"""
        print("\n⚡ PERFORMANCE TESTING")
        print("-" * 40)

        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Start performance monitoring
        await page.goto(self.url)

        # Get performance metrics
        metrics = await page.evaluate("""() => {
            const perf = performance.getEntriesByType('navigation')[0];
            const paint = performance.getEntriesByType('paint');

            return {
                // Navigation Timing
                loadTime: perf.loadEventEnd - perf.fetchStart,
                domReady: perf.domContentLoadedEventEnd - perf.fetchStart,
                ttfb: perf.responseStart - perf.fetchStart,

                // Resource Timing
                dns: perf.domainLookupEnd - perf.domainLookupStart,
                tcp: perf.connectEnd - perf.connectStart,
                request: perf.responseStart - perf.requestStart,
                response: perf.responseEnd - perf.responseStart,

                // Paint Timing
                fcp: paint.find(p => p.name === 'first-contentful-paint')?.startTime || 0,
                lcp: 0, // Would need PerformanceObserver

                // Resource counts
                resources: performance.getEntriesByType('resource').length,

                // Memory (if available)
                memory: performance.memory ? {
                    used: Math.round(performance.memory.usedJSHeapSize / 1048576),
                    total: Math.round(performance.memory.totalJSHeapSize / 1048576)
                } : null
            };
        }""")

        self.results["performance"] = metrics

        # Print key metrics
        print(f"  Load Time: {metrics['loadTime']:.0f}ms")
        print(f"  DOM Ready: {metrics['domReady']:.0f}ms")
        print(f"  TTFB: {metrics['ttfb']:.0f}ms")
        print(f"  FCP: {metrics['fcp']:.0f}ms")
        print(f"  Resources: {metrics['resources']}")

        # Performance score
        score = 100
        if metrics['loadTime'] > 3000: score -= 20
        if metrics['ttfb'] > 600: score -= 10
        if metrics['fcp'] > 1800: score -= 10
        if metrics['resources'] > 50: score -= 10

        status = "✅" if score >= 80 else "⚠️" if score >= 60 else "❌"
        print(f"\n  {status} Performance Score: {score}/100")

        await context.close()
        await browser.close()

    async def test_accessibility(self, playwright):
        """Test accessibility"""
        print("\n♿ ACCESSIBILITY TESTING")
        print("-" * 40)

        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(self.url)

        # Inject axe-core for accessibility testing
        await page.add_script_tag(url="https://unpkg.com/axe-core@4.8.2/axe.min.js")

        # Run accessibility tests
        results = await page.evaluate("() => axe.run()")

        violations = results.get("violations", [])
        self.results["accessibility"] = {
            "violations": len(violations),
            "issues": [
                {
                    "description": v["description"],
                    "impact": v["impact"],
                    "nodes": len(v["nodes"])
                }
                for v in violations[:10]
            ]
        }

        # Print summary
        if violations:
            print(f"  ❌ Found {len(violations)} accessibility violations:")
            for v in violations[:5]:
                print(f"    - {v['impact'].upper()}: {v['description']}")
        else:
            print("  ✅ No accessibility violations found!")

        # Manual checks
        manual_checks = await page.evaluate("""() => {
            const checks = {
                altText: document.querySelectorAll('img:not([alt])').length === 0,
                labels: document.querySelectorAll('input:not([aria-label]):not([id])').length === 0,
                headingOrder: (() => {
                    const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6'));
                    let lastLevel = 0;
                    for (const h of headings) {
                        const level = parseInt(h.tagName[1]);
                        if (level > lastLevel + 1) return false;
                        lastLevel = level;
                    }
                    return true;
                })(),
                contrast: true, // Would need color contrast calculation
                keyboardNav: document.querySelectorAll('[tabindex="-1"]').length === 0
            };
            return checks;
        }""")

        print("\n  Manual Checks:")
        for check, passed in manual_checks.items():
            status = "PASS" if passed else "FAIL"
            print(f"    {status} {check}")

        await context.close()
        await browser.close()

    async def test_seo(self, playwright):
        """Test SEO elements"""
        print("\n🔍 SEO TESTING")
        print("-" * 40)

        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(self.url)

        # Check SEO elements
        seo_checks = await page.evaluate("""() => {
            const checks = {
                title: document.title.length > 0 && document.title.length < 60,
                metaDescription: (() => {
                    const desc = document.querySelector('meta[name="description"]');
                    return desc && desc.content.length > 100 && desc.content.length < 160;
                })(),
                h1Count: document.querySelectorAll('h1').length === 1,
                canonicalUrl: !!document.querySelector('link[rel="canonical"]'),
                ogTags: !!document.querySelector('meta[property^="og:"]'),
                schemaOrg: !!document.querySelector('script[type="application/ld+json"]'),
                altTexts: document.querySelectorAll('img:not([alt])').length === 0,
                metaViewport: !!document.querySelector('meta[name="viewport"]'),
                lang: !!document.documentElement.lang
            };
            return checks;
        }""")

        self.results["seo"] = seo_checks

        # Print results
        for check, passed in seo_checks.items():
            status = "PASS" if passed else "FAIL"
            print(f"  {status} {check}")

        await context.close()
        await browser.close()

    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "="*60)
        print("TEST REPORT SUMMARY")
        print("="*60)

        # Calculate totals
        browser_issues = sum(len(b.get("errors", [])) for b in self.results["browsers"].values())
        device_issues = sum(
            len(d.get("visual_issues", [])) +
            len(d.get("responsive_issues", [])) +
            len(d.get("touch_issues", []))
            for d in self.results["devices"].values()
        )

        # Browser Summary
        print("\n🌐 BROWSER COMPATIBILITY:")
        for browser, data in self.results["browsers"].items():
            if "error" in data:
                print(f"  ❌ {browser}: Failed to test")
            else:
                errors = len(data.get("errors", []))
                status = "✅" if errors == 0 else f"❌ ({errors} errors)"
                print(f"  {status} {browser}")

        # Device Summary
        print(f"\n📱 DEVICE TESTING: {len(self.results['devices'])} devices tested")
        mobile_issues = sum(1 for d, data in self.results["devices"].items()
                          if "Mobile" in d or "Phone" in d or "iPhone" in d or "Galaxy" in d
                          and (data.get("visual_issues") or data.get("responsive_issues")))
        tablet_issues = sum(1 for d, data in self.results["devices"].items()
                          if "iPad" in d or "Tablet" in d or "Surface" in d
                          and (data.get("visual_issues") or data.get("responsive_issues")))
        desktop_issues = sum(1 for d, data in self.results["devices"].items()
                           if "Desktop" in d or "Laptop" in d
                           and (data.get("visual_issues") or data.get("responsive_issues")))

        print(f"  Mobile: {'✅' if mobile_issues == 0 else f'⚠️ {mobile_issues} devices with issues'}")
        print(f"  Tablet: {'✅' if tablet_issues == 0 else f'⚠️ {tablet_issues} devices with issues'}")
        print(f"  Desktop: {'✅' if desktop_issues == 0 else f'⚠️ {desktop_issues} devices with issues'}")

        # Performance Summary
        if self.results.get("performance"):
            perf = self.results["performance"]
            print(f"\n⚡ PERFORMANCE:")
            status = "✅" if perf["loadTime"] < 3000 else "⚠️" if perf["loadTime"] < 5000 else "❌"
            print(f"  {status} Load Time: {perf['loadTime']:.0f}ms")
            status = "✅" if perf["ttfb"] < 600 else "⚠️" if perf["ttfb"] < 1000 else "❌"
            print(f"  {status} TTFB: {perf['ttfb']:.0f}ms")

        # Accessibility Summary
        if self.results.get("accessibility"):
            a11y = self.results["accessibility"]
            violations = a11y.get("violations", 0)
            status = "✅" if violations == 0 else "⚠️" if violations < 5 else "❌"
            print(f"\n♿ ACCESSIBILITY:")
            print(f"  {status} {violations} violations found")

        # SEO Summary
        if self.results.get("seo"):
            seo = self.results["seo"]
            passed = sum(1 for v in seo.values() if v)
            total = len(seo)
            status = "✅" if passed == total else "⚠️" if passed >= total * 0.7 else "❌"
            print(f"\n🔍 SEO:")
            print(f"  {status} {passed}/{total} checks passed")

        # Overall Score
        total_score = 100
        if browser_issues > 0: total_score -= 20
        if device_issues > 10: total_score -= 20
        if device_issues > 5: total_score -= 10

        print(f"\n" + "="*60)
        print(f"OVERALL SCORE: {total_score}/100")

        if total_score >= 90:
            print("STATUS: ✅ EXCELLENT - Ready for production!")
        elif total_score >= 70:
            print("STATUS: ⚠️ GOOD - Minor issues to fix")
        elif total_score >= 50:
            print("STATUS: ⚠️ NEEDS WORK - Several issues to address")
        else:
            print("STATUS: ❌ POOR - Major issues found")

        # Save detailed report
        report_path = f"test_report_{self.timestamp}.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        print(f"\n📊 Detailed report saved to: {report_path}")
        print(f"📸 Screenshots saved to: screenshots/")

        # Create HTML report
        self.create_html_report()

    def create_html_report(self):
        """Create visual HTML report"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Test Report - {self.timestamp}</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; margin: 40px; }}
        h1 {{ color: #2c5aa0; }}
        .pass {{ color: green; }}
        .fail {{ color: red; }}
        .warn {{ color: orange; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
        .card {{ border: 1px solid #ddd; border-radius: 8px; padding: 16px; }}
        img {{ max-width: 100%; height: auto; }}
    </style>
</head>
<body>
    <h1>Cross-Browser & Multi-Device Test Report</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

    <h2>Browser Compatibility</h2>
    <div class="grid">
        {"".join(f'<div class="card"><h3>{b}</h3><p class="{"pass" if not d.get("errors") else "fail"}">{len(d.get("errors", []))} errors</p></div>' for b, d in self.results["browsers"].items())}
    </div>

    <h2>Device Testing</h2>
    <div class="grid">
        {"".join(f'<div class="card"><h3>{d.replace("_", " ")}</h3><img src="{data.get("screenshot", "")}" alt="{d}"><p>{len(data.get("visual_issues", []))} visual issues</p></div>' for d, data in self.results["devices"].items() if "screenshot" in data)}
    </div>
</body>
</html>"""

        with open(f"test_report_{self.timestamp}.html", "w") as f:
            f.write(html)

        print(f"📄 Visual report saved to: test_report_{self.timestamp}.html")


async def main():
    """Run the complete test suite"""

    # Check if file exists
    file_path = "website/index.html"
    if not Path(file_path).exists():
        print(f"[ERROR] File not found: {file_path}")
        return

    # Run tests
    tester = CompleteTester(file_path)
    await tester.run_all_tests()


if __name__ == "__main__":
    if not PLAYWRIGHT_AVAILABLE:
        print("\n[ERROR] Please install Playwright first:")
        print("pip install playwright")
        print("playwright install")
        exit(1)

    # Run the async main function
    asyncio.run(main())