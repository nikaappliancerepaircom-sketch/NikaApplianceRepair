#!/usr/bin/env python3
"""
Comprehensive blog testing script using Playwright
Tests all 57 blog posts for design and functionality issues
"""
import asyncio
import json
import sys
import os
from pathlib import Path
from playwright.async_api import async_playwright

# Fix encoding for Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8')

async def test_blog_post(browser, filepath):
    """Test a single blog post and return results"""
    page = await browser.new_page()

    # Convert file path to URL - use absolute path
    abs_path = filepath.resolve()
    file_url = abs_path.as_uri()

    await page.goto(file_url, wait_until='networkidle')

    results = {
        'file': filepath.name,
        'url': file_url,
        'issues': [],
        'elements': {}
    }

    try:
        # Test 1: Check blog title (H1)
        h1_element = await page.query_selector('h1.blog-title')
        if h1_element:
            h1_text = await h1_element.text_content()
            results['elements']['h1_title'] = h1_text.strip()
            if h1_text.strip() == 'Blog Post':
                results['issues'].append('BUG: H1 title shows generic "Blog Post" instead of actual post title')
        else:
            results['issues'].append('ERROR: H1.blog-title element not found')

        # Test 2: Check page title (meta/title tag)
        page_title = await page.title()
        results['elements']['page_title'] = page_title

        # Test 3: Check sidebar visibility
        sidebar = await page.query_selector('aside.blog-sidebar')
        if sidebar:
            is_visible = await sidebar.is_visible()
            results['elements']['sidebar_visible'] = is_visible
            if not is_visible:
                results['issues'].append('BUG: Sidebar exists but is not visible (CSS display issue)')
            else:
                # Check sidebar content
                toc = await sidebar.query_selector('.toc-widget')
                related = await sidebar.query_selector('.related-widget')
                results['elements']['toc_present'] = toc is not None
                results['elements']['related_present'] = related is not None
        else:
            results['issues'].append('ERROR: Sidebar element not found')

        # Test 4: Check footer
        footer = await page.query_selector('footer.seo-footer-premium')
        if footer:
            is_visible = await footer.is_visible()
            results['elements']['footer_visible'] = is_visible
            if not is_visible:
                results['issues'].append('BUG: Footer exists but is not visible')
            else:
                # Check footer content
                trust_badges = await footer.query_selector('.footer-trust-badges')
                results['elements']['trust_badges'] = trust_badges is not None
        else:
            results['issues'].append('ERROR: Footer.seo-footer-premium not found')

        # Test 5: Check blog header
        blog_header = await page.query_selector('header.blog-header')
        if blog_header:
            is_visible = await blog_header.is_visible()
            results['elements']['blog_header_visible'] = is_visible
            if not is_visible:
                results['issues'].append('BUG: Blog header not visible')
        else:
            results['issues'].append('ERROR: Blog header not found')

        # Test 6: Check social share buttons
        social_share = await page.query_selector('.social-share')
        if social_share:
            is_visible = await social_share.is_visible()
            results['elements']['social_share_visible'] = is_visible
            if not is_visible:
                results['issues'].append('BUG: Social share buttons not visible')
            else:
                share_buttons = await social_share.query_selector_all('a.share-btn')
                results['elements']['share_buttons_count'] = len(share_buttons)
        else:
            results['issues'].append('ERROR: Social share section not found')

        # Test 7: Check article content
        article = await page.query_selector('article.blog-content')
        if article:
            is_visible = await article.is_visible()
            results['elements']['article_visible'] = is_visible
            if not is_visible:
                results['issues'].append('BUG: Article content not visible')
        else:
            results['issues'].append('ERROR: Article element not found')

        # Test 8: Check CSS files are loaded
        stylesheets = await page.query_selector_all('link[rel="stylesheet"]')
        css_files = []
        for sheet in stylesheets:
            href = await sheet.get_attribute('href')
            if href:
                css_files.append(href)
        results['elements']['css_files'] = css_files

        # Test 9: Check reading progress bar
        progress_bar = await page.query_selector('#progressBar')
        if progress_bar:
            results['elements']['progress_bar_present'] = True
        else:
            results['issues'].append('ERROR: Reading progress bar not found')

        # Test 10: Check site header
        site_header = await page.query_selector('header.site-header')
        if site_header:
            is_visible = await site_header.is_visible()
            results['elements']['site_header_visible'] = is_visible
        else:
            results['issues'].append('ERROR: Site header not found')

        # Test 11: Check viewport dimensions to test responsiveness
        viewport = page.viewportSize
        results['elements']['viewport'] = viewport

    except Exception as e:
        results['issues'].append(f'EXCEPTION: {str(e)}')

    await page.close()
    return results

async def main():
    blog_base = Path("blog")
    folders = ["troubleshooting", "guides", "maintenance"]
    all_results = []

    print("\n" + "="*100)
    print("COMPREHENSIVE BLOG TESTING - ALL 57 POSTS")
    print("="*100 + "\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch()

        for folder in folders:
            folder_path = blog_base / folder
            if not folder_path.exists():
                continue

            html_files = sorted([f for f in folder_path.glob('*.html')])
            print(f"\n[{folder.upper()}] - Testing {len(html_files)} posts\n")

            for filepath in html_files:
                results = await test_blog_post(browser, filepath)
                all_results.append(results)

                # Print result for each post
                status = "✓ OK" if not results['issues'] else f"✗ {len(results['issues'])} ISSUES"
                print(f"  {status} - {filepath.name}")

                # Print issues for this post
                if results['issues']:
                    for issue in results['issues']:
                        print(f"      • {issue}")

        await browser.close()

    # Summary
    print("\n" + "="*100)
    print("TEST SUMMARY")
    print("="*100 + "\n")

    total_posts = len(all_results)
    posts_with_issues = len([r for r in all_results if r['issues']])
    total_issues = sum(len(r['issues']) for r in all_results)

    print(f"Total Posts Tested: {total_posts}")
    print(f"Posts with Issues: {posts_with_issues}")
    print(f"Total Issues Found: {total_issues}\n")

    # Group issues by type
    issue_types = {}
    for result in all_results:
        for issue in result['issues']:
            issue_type = issue.split(':')[0]
            if issue_type not in issue_types:
                issue_types[issue_type] = []
            issue_types[issue_type].append((result['file'], issue))

    print("ISSUES BY TYPE:\n")
    for issue_type, issues in sorted(issue_types.items()):
        print(f"{issue_type} ({len(issues)} occurrences):")
        # Group by specific issue
        specific_issues = {}
        for filename, issue in issues:
            if issue not in specific_issues:
                specific_issues[issue] = []
            specific_issues[issue].append(filename)

        for issue, files in sorted(specific_issues.items()):
            print(f"  • {issue}")
            if len(files) <= 5:
                for f in files:
                    print(f"    - {f}")
            else:
                print(f"    - Affects {len(files)} files")
        print()

    # Save detailed results to JSON
    with open('blog_test_results.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    print("Detailed results saved to blog_test_results.json\n")

if __name__ == '__main__':
    asyncio.run(main())
