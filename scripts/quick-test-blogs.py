#!/usr/bin/env python3
"""
Quick blog testing - check first few posts from each category for bugs
"""
import asyncio
import sys
import os
from pathlib import Path
from playwright.async_api import async_playwright

# Fix encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

async def test_blog_post(browser, filepath):
    """Test a single blog post and return results"""
    page = await browser.new_page()

    abs_path = filepath.resolve()
    file_url = abs_path.as_uri()

    try:
        await page.goto(file_url, wait_until='networkidle')
    except:
        await page.goto(file_url, wait_until='load')

    issues = []

    # Test 1: H1 title
    try:
        h1 = await page.query_selector('h1.blog-title')
        if h1:
            h1_text = await h1.text_content()
            if 'Blog Post' in h1_text:
                issues.append('[H1 BUG] Title shows "Blog Post" instead of actual title')
        else:
            issues.append('[ERROR] H1.blog-title not found')
    except Exception as e:
        issues.append(f'[H1 ERROR] {str(e)}')

    # Test 2: Sidebar visibility
    try:
        sidebar = await page.query_selector('aside.blog-sidebar')
        if sidebar:
            is_visible = await sidebar.is_visible()
            if not is_visible:
                issues.append('[SIDEBAR BUG] Sidebar not visible (CSS issue)')
            else:
                # Check if it's on the right
                bbox = await sidebar.bounding_box()
                if bbox:
                    # Get viewport width
                    viewport = page.viewportSize
                    if viewport:
                        right_edge = bbox['x'] + bbox['width']
                        viewport_width = viewport['width']
                        if right_edge < viewport_width - 50:  # Allow 50px margin
                            issues.append('[SIDEBAR POSITION] Sidebar not on right side')
        else:
            issues.append('[ERROR] Sidebar not found')
    except Exception as e:
        issues.append(f'[SIDEBAR ERROR] {str(e)}')

    # Test 3: Footer visibility
    try:
        footer = await page.query_selector('footer.seo-footer-premium')
        if footer:
            is_visible = await footer.is_visible()
            if not is_visible:
                issues.append('[FOOTER BUG] Footer not visible')
        else:
            issues.append('[ERROR] Footer not found')
    except Exception as e:
        issues.append(f'[FOOTER ERROR] {str(e)}')

    # Test 4: Blog header
    try:
        blog_header = await page.query_selector('header.blog-header')
        if blog_header:
            is_visible = await blog_header.is_visible()
            if not is_visible:
                issues.append('[BLOG-HEADER BUG] Not visible')
        else:
            issues.append('[ERROR] Blog header not found')
    except Exception as e:
        issues.append(f'[BLOG-HEADER ERROR] {str(e)}')

    # Test 5: Site header
    try:
        site_header = await page.query_selector('header.site-header')
        if site_header:
            is_visible = await site_header.is_visible()
            if not is_visible:
                issues.append('[SITE-HEADER BUG] Not visible')
        else:
            issues.append('[ERROR] Site header not found')
    except Exception as e:
        issues.append(f'[SITE-HEADER ERROR] {str(e)}')

    # Test 6: Article content
    try:
        article = await page.query_selector('article.blog-content')
        if article:
            is_visible = await article.is_visible()
            if not is_visible:
                issues.append('[ARTICLE BUG] Not visible')
        else:
            issues.append('[ERROR] Article not found')
    except Exception as e:
        issues.append(f'[ARTICLE ERROR] {str(e)}')

    await page.close()
    return issues

async def main():
    blog_base = Path("blog")

    print("\n" + "="*80)
    print("QUICK BLOG TEST - CHECKING FIRST 3 POSTS FROM EACH CATEGORY")
    print("="*80 + "\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch()

        total_issues = 0

        for folder in ["maintenance", "troubleshooting", "guides"]:
            folder_path = blog_base / folder
            if not folder_path.exists():
                continue

            html_files = sorted([f for f in folder_path.glob('*.html')])[:3]  # Only first 3
            print(f"[{folder.upper()}] - Testing {len(html_files)} posts\n")

            for filepath in html_files:
                issues = await test_blog_post(browser, filepath)
                total_issues += len(issues)

                if issues:
                    print(f"  [ISSUES] {filepath.name}")
                    for issue in issues:
                        print(f"    - {issue}")
                else:
                    print(f"  [OK] {filepath.name}")

            print()

        await browser.close()

    print("="*80)
    print(f"Total Issues Found: {total_issues}")
    print("="*80 + "\n")

if __name__ == '__main__':
    asyncio.run(main())
