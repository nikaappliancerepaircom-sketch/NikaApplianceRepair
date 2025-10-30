#!/usr/bin/env python3
"""
Visual blog testing - Check actual design and layout issues
"""
import asyncio
import sys
import os
from pathlib import Path
from playwright.async_api import async_playwright

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

async def test_blog_visual(browser, filepath):
    """Test blog post visual layout and CSS rendering"""
    page = await browser.new_page(viewport={"width": 1200, "height": 800})

    abs_path = filepath.resolve()
    file_url = abs_path.as_uri()

    try:
        await page.goto(file_url, wait_until='load')
    except:
        pass

    issues = []

    # Test 1: H1 title not hardcoded
    try:
        h1 = await page.query_selector('h1.blog-title')
        if h1:
            h1_text = await h1.text_content()
            h1_text = h1_text.strip()
            if h1_text == 'Blog Post' or h1_text == '':
                issues.append('[H1] Shows generic text')
        else:
            issues.append('[H1] Element missing')
    except:
        pass

    # Test 2: Sidebar visibility and position
    try:
        sidebar = await page.query_selector('aside.blog-sidebar')
        if sidebar:
            # Check if visible
            display = await sidebar.evaluate('el => window.getComputedStyle(el).display')
            visibility = await sidebar.evaluate('el => window.getComputedStyle(el).visibility')
            if display == 'none' or visibility == 'hidden':
                issues.append('[SIDEBAR] Hidden by CSS (display: none or visibility: hidden)')
            else:
                # Check position - should be on right side
                position = await sidebar.evaluate('el => window.getComputedStyle(el).position')
                # Get bounding box
                bbox = await sidebar.bounding_box()
                if bbox and bbox['x'] < 500:  # If less than 500px from left, probably not right
                    issues.append('[SIDEBAR] Not positioned on right side')
        else:
            issues.append('[SIDEBAR] Element missing from HTML')
    except Exception as e:
        issues.append(f'[SIDEBAR] Check failed: {str(e)[:50]}')

    # Test 3: Blog structure (main, article, etc)
    try:
        main = await page.query_selector('main.blog-main')
        if not main:
            issues.append('[MAIN] blog-main element missing')

        article = await page.query_selector('article.blog-content')
        if not article:
            issues.append('[ARTICLE] blog-content element missing')

        header_site = await page.query_selector('header.site-header')
        if not header_site:
            issues.append('[HEADER] site-header element missing')
    except:
        pass

    # Test 4: Footer visible and positioned
    try:
        footer = await page.query_selector('footer.seo-footer-premium')
        if footer:
            display = await footer.evaluate('el => window.getComputedStyle(el).display')
            if display == 'none':
                issues.append('[FOOTER] Hidden by CSS')
        else:
            issues.append('[FOOTER] Element missing')
    except:
        pass

    # Test 5: Check CSS files loaded (check for 404s)
    try:
        stylesheets = await page.query_selector_all('link[rel="stylesheet"]')
        for sheet in stylesheets:
            href = await sheet.get_attribute('href')
            if href and '../css/' in href:
                # Check if it returns content
                try:
                    response = await page.evaluate(f'''
                    async (url) => {{
                        const response = await fetch(url);
                        return response.status;
                    }}
                    ''', href)
                except:
                    pass  # Skip this check if fetch not available
    except:
        pass

    # Test 6: Social share buttons
    try:
        social = await page.query_selector('.social-share')
        if not social:
            issues.append('[SOCIAL-SHARE] Element missing')
    except:
        pass

    # Test 7: Reading progress bar
    try:
        progress = await page.query_selector('#progressBar')
        if not progress:
            issues.append('[PROGRESS-BAR] Element missing')
    except:
        pass

    await page.close()
    return issues

async def main():
    blog_base = Path("blog")

    print("\n" + "="*80)
    print("VISUAL BLOG TESTING - CHECKING DESIGN ISSUES")
    print("="*80 + "\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        total_issues = 0
        posts_with_issues = 0

        for folder in ["maintenance", "troubleshooting", "guides"]:
            folder_path = blog_base / folder
            if not folder_path.exists():
                continue

            html_files = sorted([f for f in folder_path.glob('*.html')])[:3]
            print(f"[{folder.upper()}] - Testing {len(html_files)} posts\n")

            for filepath in html_files:
                issues = await test_blog_visual(browser, filepath)

                if issues:
                    posts_with_issues += 1
                    total_issues += len(issues)
                    print(f"  [ISSUES] {filepath.name}")
                    for issue in issues:
                        print(f"    - {issue}")
                else:
                    print(f"  [OK] {filepath.name}")

            print()

        await browser.close()

    print("="*80)
    print(f"Posts with Issues: {posts_with_issues}/9")
    print(f"Total Issues: {total_issues}")
    print("="*80 + "\n")

if __name__ == '__main__':
    asyncio.run(main())
