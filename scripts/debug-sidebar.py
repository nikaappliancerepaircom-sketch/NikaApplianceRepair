#!/usr/bin/env python3
"""
Debug sidebar positioning - check what's happening with TOC and Related Posts
"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def debug_sidebar():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Show browser
        page = await browser.new_page(viewport={"width": 1400, "height": 900})

        # Test a post
        test_file = Path("blog/maintenance/dishwasher-maintenance-hard-water.html")
        file_url = test_file.resolve().as_uri()

        print(f"Testing: {test_file}")
        print(f"URL: {file_url}\n")

        await page.goto(file_url, wait_until='load')

        # Check sidebar structure
        print("="*80)
        print("SIDEBAR STRUCTURE DEBUG")
        print("="*80 + "\n")

        # Get HTML of wrapper
        wrapper = await page.query_selector('.blog-wrapper')
        if wrapper:
            wrapper_html = await wrapper.evaluate('el => el.outerHTML')
            print("Blog-wrapper HTML (first 500 chars):")
            print(wrapper_html[:500])
            print("\n...")

        # Check sidebar element
        sidebar = await page.query_selector('aside.blog-sidebar')
        if sidebar:
            print("\nSidebar found!")

            # Get CSS properties
            display = await sidebar.evaluate('el => window.getComputedStyle(el).display')
            position = await sidebar.evaluate('el => window.getComputedStyle(el).position')
            visibility = await sidebar.evaluate('el => window.getComputedStyle(el).visibility')

            print(f"  - display: {display}")
            print(f"  - position: {position}")
            print(f"  - visibility: {visibility}")

            # Check parent grid
            parent = await sidebar.evaluate('''el => {
                const p = el.parentElement;
                if (!p) return null;
                const style = window.getComputedStyle(p);
                return {
                    display: style.display,
                    gridTemplateColumns: style.gridTemplateColumns,
                    gap: style.gap,
                    children: p.children.length
                };
            }''')
            print(f"\nParent element properties:")
            print(f"  - display: {parent['display']}")
            print(f"  - gridTemplateColumns: {parent['gridTemplateColumns']}")
            print(f"  - gap: {parent['gap']}")
            print(f"  - children count: {parent['children']}")

            # Check children order
            children_info = await sidebar.evaluate('''el => {
                const p = el.parentElement;
                const children = Array.from(p.children).map((child, idx) => ({
                    index: idx,
                    class: child.className,
                    tag: child.tagName
                }));
                return children;
            }''')
            print(f"\nChildren order in grid:")
            for child in children_info:
                print(f"  [{child['index']}] <{child['tag'].lower()} class=\"{child['class']}\">")

            # Check TOC widget
            toc = await sidebar.query_selector('.toc-widget')
            if toc:
                print(f"\nTable of Contents widget: FOUND")
                toc_display = await toc.evaluate('el => window.getComputedStyle(el).display')
                print(f"  - display: {toc_display}")
            else:
                print(f"\nTable of Contents widget: NOT FOUND")

            # Check Related widget
            related = await sidebar.query_selector('.related-widget')
            if related:
                print(f"\nRelated Posts widget: FOUND")
                related_display = await related.evaluate('el => window.getComputedStyle(el).display')
                print(f"  - display: {related_display}")
            else:
                print(f"\nRelated Posts widget: NOT FOUND")

        else:
            print("\nSidebar element NOT FOUND in HTML!")

        print("\n" + "="*80)
        print("Browser window open. Check the layout visually.")
        print("Press Enter to close...")
        print("="*80 + "\n")

        input()
        await browser.close()

if __name__ == '__main__':
    asyncio.run(debug_sidebar())
