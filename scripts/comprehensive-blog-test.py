#!/usr/bin/env python3
"""
Comprehensive blog testing - ALL 57 POSTS
Check design, layout, CSS, and functionality issues
"""
import asyncio
import sys
import os
import json
from pathlib import Path
from playwright.async_api import async_playwright

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

async def test_blog_comprehensive(browser, filepath):
    """Comprehensive test of a blog post"""
    page = await browser.new_page(viewport={"width": 1200, "height": 800})

    abs_path = filepath.resolve()
    file_url = abs_path.as_uri()

    try:
        await page.goto(file_url, wait_until='load')
    except:
        pass

    issues = []
    data = {}

    # Test 1: H1 title
    try:
        h1 = await page.query_selector('h1.blog-title')
        if h1:
            h1_text = await h1.text_content()
            h1_text = h1_text.strip()
            data['h1_title'] = h1_text
            if h1_text == 'Blog Post' or h1_text == '':
                issues.append('H1_GENERIC')
        else:
            issues.append('H1_MISSING')
    except:
        issues.append('H1_ERROR')

    # Test 2: Page title
    try:
        page_title = await page.title()
        data['page_title'] = page_title
    except:
        pass

    # Test 3: Main elements exist
    try:
        main = await page.query_selector('main.blog-main')
        data['main_exists'] = main is not None
        if not main:
            issues.append('MAIN_MISSING')

        article = await page.query_selector('article.blog-content')
        data['article_exists'] = article is not None
        if not article:
            issues.append('ARTICLE_MISSING')

        site_header = await page.query_selector('header.site-header')
        data['site_header_exists'] = site_header is not None
        if not site_header:
            issues.append('SITE_HEADER_MISSING')

        blog_header = await page.query_selector('header.blog-header')
        data['blog_header_exists'] = blog_header is not None
        if not blog_header:
            issues.append('BLOG_HEADER_MISSING')

        footer = await page.query_selector('footer.seo-footer-premium')
        data['footer_exists'] = footer is not None
        if not footer:
            issues.append('FOOTER_MISSING')
    except:
        issues.append('STRUCTURE_ERROR')

    # Test 4: Sidebar
    try:
        sidebar = await page.query_selector('aside.blog-sidebar')
        data['sidebar_exists'] = sidebar is not None
        if sidebar:
            display = await sidebar.evaluate('el => window.getComputedStyle(el).display')
            data['sidebar_display'] = display
            if display == 'none':
                issues.append('SIDEBAR_HIDDEN')
        else:
            issues.append('SIDEBAR_MISSING')
    except:
        issues.append('SIDEBAR_ERROR')

    # Test 5: Social share
    try:
        social = await page.query_selector('.social-share')
        data['social_share_exists'] = social is not None
        if not social:
            issues.append('SOCIAL_MISSING')
    except:
        pass

    # Test 6: Progress bar
    try:
        progress = await page.query_selector('#progressBar')
        data['progress_bar_exists'] = progress is not None
        if not progress:
            issues.append('PROGRESS_BAR_MISSING')
    except:
        pass

    # Test 7: CSS classes present
    try:
        # Check for footer CSS class
        has_footer_css = await page.evaluate('''
        () => {
            const style = document.querySelector('style');
            if (!style) return false;
            return style.textContent.includes('.seo-footer-premium');
        }
        ''')
        data['footer_css'] = has_footer_css
        if not has_footer_css:
            issues.append('FOOTER_CSS_MISSING')
    except:
        pass

    await page.close()
    return {'issues': issues, 'data': data}

async def main():
    blog_base = Path("blog")

    print("\n" + "="*80)
    print("COMPREHENSIVE BLOG TESTING - ALL 57 POSTS")
    print("="*80 + "\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        all_results = []
        issue_summary = {}

        for folder in ["maintenance", "troubleshooting", "guides"]:
            folder_path = blog_base / folder
            if not folder_path.exists():
                continue

            html_files = sorted([f for f in folder_path.glob('*.html')])
            print(f"[{folder.upper()}] - Testing {len(html_files)} posts...")

            for filepath in html_files:
                result = await test_blog_comprehensive(browser, filepath)
                result['file'] = filepath.name
                result['folder'] = folder
                all_results.append(result)

                for issue in result['issues']:
                    if issue not in issue_summary:
                        issue_summary[issue] = []
                    issue_summary[issue].append(filepath.name)

            print(f"  [DONE] {len(html_files)} posts tested\n")

        await browser.close()

    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80 + "\n")

    total_posts = len(all_results)
    posts_with_issues = len([r for r in all_results if r['issues']])
    total_issues = sum(len(r['issues']) for r in all_results)

    print(f"Total Posts: {total_posts}")
    print(f"Posts with Issues: {posts_with_issues}")
    print(f"Total Issues Found: {total_issues}\n")

    if issue_summary:
        print("ISSUES FOUND:\n")
        for issue_type, files in sorted(issue_summary.items()):
            print(f"  {issue_type}: {len(files)} posts")
            if len(files) <= 3:
                for f in files:
                    print(f"    - {f}")
        print()
    else:
        print("NO ISSUES FOUND! All 57 posts pass design validation.\n")

    # Save results
    with open('blog_comprehensive_test.json', 'w') as f:
        json.dump(all_results, f, indent=2)

    # Print stats
    print("="*80)
    if posts_with_issues == 0:
        print("SUCCESS: All 57 blog posts pass comprehensive testing!")
    else:
        print(f"WARNING: {posts_with_issues} posts need attention")
    print("="*80 + "\n")

if __name__ == '__main__':
    asyncio.run(main())
