#!/usr/bin/env python3
"""
Standardize all blog posts to use the premium-blog-example.html structure
Converts all posts to use:
- <header class="site-header"> for main navigation
- <div class="blog-wrapper"> > <main class="blog-main"> structure
"""
import os
import re
from pathlib import Path

def get_premium_header():
    """Get the standard site header from premium example"""
    return '''<!-- Header -->
    <header class="site-header">
        <div class="header-container">
            <div class="header-logo">
                <a href="/">Nika Appliance Repair</a>
            </div>

            <nav class="header-nav" id="mainNav">
                <ul class="nav-list">
                    <li><a href="/" class="nav-link">Home</a></li>
                    <li><a href="/services" class="nav-link">Services</a></li>
                    <li><a href="/locations" class="nav-link">Locations</a></li>
                    <li><a href="/about" class="nav-link">About</a></li>
                    <li><a href="/blog" class="nav-link">Blog</a></li>
                </ul>
            </nav>

            <div class="header-cta">
                <a href="tel:4377476737" class="cta-phone">
                    <i class="fas fa-phone"></i> (437) 747-6737
                </a>
            </div>

            <button class="mobile-menu-btn" aria-label="Menu" aria-expanded="false">
                <span class="menu-bar"></span>
                <span class="menu-bar"></span>
                <span class="menu-bar"></span>
            </button>
        </div>
    </header>

    <!-- Main Blog Content -->
    <div class="blog-wrapper">
        <main class="blog-main">'''

def standardize_post(filepath):
    """
    Standardize a single post to use premium blog template structure
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Step 1: Remove reading progress bar if it exists (will add in header)
    content = re.sub(r'<div class="reading-progress"[^>]*></div>\s*', '', content)

    # Step 2: Remove existing site-header if any
    content = re.sub(r'<header class="site-header">.*?</header>\s*', '', content, flags=re.DOTALL)

    # Step 3: Remove existing header navigation sections
    content = re.sub(r'<header[^>]*>.*?<div class="header-content">.*?</nav>.*?</div>\s*</header>\s*', '', content, flags=re.DOTALL)

    # Step 4: Remove content-wrapper divs
    content = re.sub(r'<main class="content-wrapper">\.', '<main class="blog-main">', content)

    # Step 5: Find body tag and inject standard header
    body_match = re.search(r'(<body[^>]*>)\s*', content)
    if body_match:
        body_tag = body_match.group(1)
        header_html = f'{body_tag}\n    <!-- Reading Progress Bar -->\n    <div class="reading-progress" id="progressBar"></div>\n\n    '
        header_html += get_premium_header()

        content = content[:body_match.start()] + header_html + content[body_match.end():]

    # Step 6: Ensure blog-wrapper exists (if not present, add it)
    if '<div class="blog-wrapper">' not in content:
        # Find first main or article tag and wrap it
        main_match = re.search(r'(<main[^>]*>)', content)
        if main_match:
            content = content[:main_match.start()] + '<div class="blog-wrapper">\n        ' + content[main_match.start():]
            content = content.replace('</main>', '        </main>\n    </div>', 1)

    # Step 7: Ensure article tag exists
    if '<article' not in content:
        # Wrap main content in article
        content = re.sub(r'(<main[^>]*>)', r'\1\n            <article class="blog-content">', content)
        content = re.sub(r'(</main>)', r'            </article>\n        \1', content, count=1)

    # Step 8: Close blog-wrapper before </body>
    if '<div class="blog-wrapper">' in content and '</div>\n    </div>\n</body>' not in content:
        content = content.replace('</main>', '</main>\n        </div>\n    </div>', 1)

    return content, original_content != content

def main():
    blog_dir = Path("blog/troubleshooting")

    if not blog_dir.exists():
        print("[ERROR] Blog directory not found")
        return

    html_files = sorted([f for f in blog_dir.glob('*.html')])

    print("\n" + "="*80)
    print("STANDARDIZING BLOG POST DESIGNS")
    print("="*80 + "\n")

    updated_count = 0
    error_count = 0
    skipped_count = 0

    for filepath in html_files:
        filename = filepath.name

        try:
            new_content, was_modified = standardize_post(filepath)

            if was_modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"[OK] {filename} - Standardized")
                updated_count += 1
            else:
                print(f"[SKIP] {filename} - Already standard")
                skipped_count += 1

        except Exception as e:
            print(f"[ERROR] {filename} - {str(e)}")
            error_count += 1

    print("\n" + "="*80)
    print(f"Updated: {updated_count} posts")
    print(f"Skipped: {skipped_count} posts")
    print(f"Errors: {error_count} posts")
    print(f"Total: {len(html_files)} posts processed")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
