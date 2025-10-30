#!/usr/bin/env python3
"""
Comprehensive SEO optimization check for all 57 blog posts
Runs in parallel for speed
"""
import re
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_seo(filepath):
    """Check SEO parameters for a single post"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    result = {
        'file': filepath.name,
        'issues': [],
        'seo_data': {}
    }

    # 1. H1 Count - Should be exactly 1
    h1_count = len(re.findall(r'<h1', content))
    result['seo_data']['h1_count'] = h1_count
    if h1_count != 1:
        result['issues'].append(f'H1_COUNT:{h1_count}')

    # 2. Meta title
    title_match = re.search(r'<title[^>]*>([^<]+)</title>', content)
    if title_match:
        title = title_match.group(1)
        result['seo_data']['title_length'] = len(title)
        result['seo_data']['title'] = title
        if len(title) < 30 or len(title) > 60:
            result['issues'].append(f'TITLE_LENGTH:{len(title)}')
    else:
        result['issues'].append('TITLE_MISSING')

    # 3. Meta description
    desc_match = re.search(r'<meta name="description" content="([^"]+)"', content)
    if desc_match:
        desc = desc_match.group(1)
        result['seo_data']['desc_length'] = len(desc)
        if len(desc) < 120 or len(desc) > 160:
            result['issues'].append(f'DESC_LENGTH:{len(desc)}')
    else:
        result['issues'].append('DESC_MISSING')

    # 4. Meta keywords
    kw_match = re.search(r'<meta name="keywords" content="([^"]+)"', content)
    if kw_match:
        keywords = kw_match.group(1)
        kw_count = len(keywords.split(','))
        result['seo_data']['keyword_count'] = kw_count
        if kw_count < 3 or kw_count > 10:
            result['issues'].append(f'KEYWORDS:{kw_count}')
    else:
        result['issues'].append('KEYWORDS_MISSING')

    # 5. H2 tags (should have at least 2)
    h2_count = len(re.findall(r'<h2', content))
    result['seo_data']['h2_count'] = h2_count
    if h2_count < 2:
        result['issues'].append(f'H2_LOW:{h2_count}')

    # 6. Images with alt tags
    img_tags = re.findall(r'<img[^>]*>', content)
    result['seo_data']['img_count'] = len(img_tags)
    if img_tags:
        imgs_with_alt = len(re.findall(r'<img[^>]*\salt[^>]*>', content))
        result['seo_data']['imgs_with_alt'] = imgs_with_alt
        if imgs_with_alt < len(img_tags):
            result['issues'].append(f'IMG_ALT:{len(img_tags)-imgs_with_alt}')

    # 7. Internal links
    internal_links = len(re.findall(r'href="/', content))
    result['seo_data']['internal_links'] = internal_links
    if internal_links < 3:
        result['issues'].append(f'LINKS_LOW:{internal_links}')

    # 8. Canonical tag
    canonical = '<link rel="canonical"' in content
    result['seo_data']['canonical'] = canonical
    if not canonical:
        result['issues'].append('CANONICAL_MISSING')

    # 9. OpenGraph tags
    og_tags = len(re.findall(r'<meta property="og:', content))
    result['seo_data']['og_tags'] = og_tags
    if og_tags < 3:
        result['issues'].append(f'OG_TAGS:{og_tags}')

    # 10. Content length (word count estimate)
    # Count words in article content
    article_match = re.search(r'<article[^>]*>(.*?)</article>', content, re.DOTALL)
    if article_match:
        article_text = article_match.group(1)
        # Remove HTML tags
        text_only = re.sub(r'<[^>]+>', '', article_text)
        word_count = len(text_only.split())
        result['seo_data']['word_count'] = word_count
        if word_count < 800:
            result['issues'].append(f'CONTENT_SHORT:{word_count}')
    else:
        result['issues'].append('ARTICLE_MISSING')

    return result

def main():
    blog_base = Path("blog")
    folders = ["maintenance", "troubleshooting", "guides"]

    print("\n" + "="*80)
    print("SEO OPTIMIZATION CHECK - ALL 57 POSTS (PARALLEL)")
    print("="*80 + "\n")

    all_files = []
    for folder in folders:
        folder_path = blog_base / folder
        if folder_path.exists():
            all_files.extend(sorted([f for f in folder_path.glob('*.html')]))

    # Run in parallel
    results = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(check_seo, f): f for f in all_files}

        for future in as_completed(futures):
            result = future.result()
            results.append(result)

    # Sort by filename for consistent output
    results.sort(key=lambda x: x['file'])

    # Summary
    total_issues = {}
    for result in results:
        for issue in result['issues']:
            issue_type = issue.split(':')[0]
            if issue_type not in total_issues:
                total_issues[issue_type] = []
            total_issues[issue_type].append(result['file'])

    print(f"SEO RESULTS FOR {len(results)} POSTS:\n")

    if not total_issues:
        print("All posts pass SEO checks!\n")
    else:
        print("SEO ISSUES FOUND:\n")
        for issue_type, files in sorted(total_issues.items()):
            print(f"  {issue_type}: {len(files)} posts")
            if len(files) <= 3:
                for f in files:
                    print(f"    - {f}")

    # Statistics
    print("\n" + "="*80)
    print("SEO METRICS SUMMARY")
    print("="*80 + "\n")

    avg_word_count = sum(r['seo_data'].get('word_count', 0) for r in results) / len(results)
    avg_title_length = sum(r['seo_data'].get('title_length', 0) for r in results) / len(results)
    avg_desc_length = sum(r['seo_data'].get('desc_length', 0) for r in results) / len(results)
    h1_issues = len([r for r in results if r['seo_data']['h1_count'] != 1])
    h2_avg = sum(r['seo_data'].get('h2_count', 0) for r in results) / len(results)

    print(f"Average Word Count: {avg_word_count:.0f}")
    print(f"Average Title Length: {avg_title_length:.0f}")
    print(f"Average Description Length: {avg_desc_length:.0f}")
    print(f"Average H2 Tags: {h2_avg:.1f}")
    print(f"Posts with H1 issues: {h1_issues}")
    print(f"Total Issues: {sum(len(files) for files in total_issues.values())}\n")

    # Save detailed report
    report = {
        'total_posts': len(results),
        'total_issues': sum(len(files) for files in total_issues.values()),
        'issue_types': total_issues,
        'detailed_results': results
    }

    with open('seo_check_results.json', 'w') as f:
        json.dump(report, f, indent=2)

    print("="*80)
    print("Detailed report saved to seo_check_results.json")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
