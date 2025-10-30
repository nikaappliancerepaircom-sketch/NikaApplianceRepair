#!/usr/bin/env python3
"""
Generate proper Table of Contents for each blog post
Extract H2 and H3 headings from article content and create TOC
"""
import re
from pathlib import Path

def extract_headings(filepath):
    """Extract H2 and H3 headings from article content"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract article content
    article_match = re.search(r'<article[^>]*>(.*?)</article>', content, re.DOTALL)
    if not article_match:
        return []

    article_content = article_match.group(1)

    # Find all H2 and H3 tags with their text and IDs
    headings = []
    h2_pattern = r'<h2[^>]*id="([^"]*)"[^>]*>([^<]+)</h2>'
    h3_pattern = r'<h3[^>]*(?:id="([^"]*)")?[^>]*>([^<]+)</h3>'

    # Extract H2 headings
    for match in re.finditer(h2_pattern, article_content):
        heading_id = match.group(1) or "section-" + str(len(headings))
        heading_text = match.group(2).strip()
        headings.append({
            'level': 2,
            'id': heading_id,
            'text': heading_text
        })

    # Extract H3 headings (group by parent H2)
    h3_list = []
    for match in re.finditer(h3_pattern, article_content):
        heading_id = match.group(1) or "subsection-" + str(len(h3_list))
        heading_text = match.group(2).strip()
        h3_list.append({
            'level': 3,
            'id': heading_id,
            'text': heading_text
        })

    # Interleave H3s with H2s
    final_headings = []
    h3_idx = 0
    for h2 in headings:
        final_headings.append(h2)
        # Add H3s that belong to this H2 (simple heuristic: until next H2)
        # For now, add next 5 H3s as children
        count = 0
        while h3_idx < len(h3_list) and count < 10:
            final_headings.append(h3_list[h3_idx])
            h3_idx += 1
            count += 1

    # Add remaining H3s
    while h3_idx < len(h3_list):
        final_headings.append(h3_list[h3_idx])
        h3_idx += 1

    return final_headings

def generate_toc_html(headings):
    """Generate HTML for Table of Contents"""
    if not headings:
        return None

    html = '<ul class="toc-list">'
    current_level = 2

    for heading in headings:
        level = heading['level']

        # Handle nesting
        if level > current_level:
            # Open nested lists
            for _ in range(level - current_level):
                html += '<li><ul class="toc-sublist">'
        elif level < current_level:
            # Close nested lists
            for _ in range(current_level - level):
                html += '</ul></li>'

        current_level = level

        # Add the item
        html += f'<li><a href="#{heading["id"]}">{heading["text"]}</a></li>'

    # Close remaining lists
    for _ in range(current_level - 2):
        html += '</ul></li>'
    html += '</ul>'

    return html

def update_toc_in_post(filepath, toc_html):
    """Replace the placeholder TOC with real one"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find and replace the TOC widget content
    # Pattern: <div class="toc-widget">...<ul class="toc-list">..content..</ul>...</div>
    toc_pattern = r'(<div class="toc-widget">\s*<h3>[^<]*</h3>)\s*<ul class="toc-list">.*?</ul>'

    if re.search(toc_pattern, content, re.DOTALL):
        new_toc = r'\1\n' + toc_html
        content = re.sub(toc_pattern, new_toc, content, flags=re.DOTALL)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    blog_base = Path("blog")
    folders = ["maintenance", "troubleshooting", "guides"]

    print("\n" + "="*80)
    print("GENERATING TABLE OF CONTENTS FOR ALL 57 POSTS")
    print("="*80 + "\n")

    total_updated = 0
    total_failed = 0

    for folder in folders:
        folder_path = blog_base / folder
        if not folder_path.exists():
            continue

        html_files = sorted([f for f in folder_path.glob('*.html')])
        print(f"[{folder.upper()}] - {len(html_files)} posts\n")

        for filepath in html_files:
            try:
                headings = extract_headings(filepath)

                if not headings:
                    print(f"  SKIP {filepath.name} (no headings found)")
                    continue

                toc_html = generate_toc_html(headings)

                if update_toc_in_post(filepath, toc_html):
                    print(f"  OK {filepath.name} ({len(headings)} items)")
                    total_updated += 1
                else:
                    print(f"  ERROR {filepath.name} (could not find TOC widget)")
                    total_failed += 1

            except Exception as e:
                print(f"  ERROR {filepath.name}: {str(e)[:60]}")
                total_failed += 1

        print()

    print("="*80)
    print(f"Total Updated: {total_updated}")
    print(f"Total Failed: {total_failed}")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
