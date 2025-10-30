#!/usr/bin/env python3
"""
Clean and standardize all blog posts to use ONLY the premium template structure
Removes all old/duplicate code and rewrites posts correctly
"""
import os
import re
from pathlib import Path

def extract_post_content(filepath):
    """
    Extract just the content from a post (everything inside <article> or after <h1/h2)
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract everything inside article tags if they exist
    article_match = re.search(r'<article[^>]*>(.*?)</article>', content, re.DOTALL)
    if article_match:
        body_content = article_match.group(1).strip()
    else:
        # Otherwise, try to get content after first h1 or h2
        h_match = re.search(r'<h[12][^>]*>.*?</h[12]>(.*)', content, re.DOTALL)
        if h_match:
            # Extract from h tag to footer or end
            temp = h_match.group(0)
            footer_match = re.search(r'<footer', temp)
            if footer_match:
                body_content = temp[:footer_match.start()].strip()
            else:
                body_content = temp.strip()
        else:
            # Last resort: get everything between body tags
            body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
            if body_match:
                body_content = body_match.group(1).strip()
            else:
                body_content = ""

    # Clean up the body content
    # Remove container divs, old headers, etc
    body_content = re.sub(r'<div class="container">|</div>\s*$', '', body_content)
    body_content = re.sub(r'<div class="reading-progress"[^>]*></div>', '', body_content)
    body_content = re.sub(r'<!-- Reading Progress.*?-->', '', body_content, flags=re.DOTALL)
    body_content = re.sub(r'<!-- Header Navigation.*?</header>', '', body_content, flags=re.DOTALL)
    body_content = re.sub(r'<!-- Main Content.*?<main[^>]*>', '', body_content, flags=re.DOTALL)

    return body_content.strip()

def extract_head_content(filepath):
    """
    Extract head section (meta, schema, CSS)
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    head_match = re.search(r'<head>(.*?)</head>', content, re.DOTALL)
    if head_match:
        head_content = head_match.group(1)
        # Keep only meta tags and schema, remove old style/script tags
        # Keep: meta, schema.org scripts, canonical, og tags
        # Remove: old style blocks
        head_content = re.sub(r'<style>.*?</style>', '', head_content, flags=re.DOTALL)
        return head_content.strip()
    return ""

def get_standard_header():
    """Get the standardized site header"""
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
    </header>'''

def rebuild_post(filepath, head_content, body_content):
    """
    Rebuild a post with standard structure
    """
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
'''

    html += head_content + '\n'

    # Add CSS links if not present
    if '../../css/blog-premium.css' not in head_content:
        html += '''
    <!-- Premium Blog Styles -->
    <link rel="stylesheet" href="../../css/blog-premium.css">

    <!-- Header Styles -->
    <link rel="stylesheet" href="../../css/header-optimized.css">
'''

    html += '''
</head>
<body>
    <!-- Reading Progress Bar -->
    <div class="reading-progress" id="progressBar"></div>

    ''' + get_standard_header() + '''

    <!-- Main Blog Content -->
    <div class="blog-wrapper">
        <main class="blog-main">
            <article class="blog-content">
'''

    html += body_content

    html += '''
            </article>
        </main>
    </div>
</body>
</html>
'''

    return html

def main():
    blog_dir = Path("blog/troubleshooting")

    if not blog_dir.exists():
        print("[ERROR] Blog directory not found")
        return

    html_files = sorted([f for f in blog_dir.glob('*.html')])

    print("\n" + "="*80)
    print("DEEP CLEANING AND STANDARDIZING BLOG POSTS")
    print("="*80 + "\n")

    updated_count = 0
    error_count = 0

    for filepath in html_files:
        filename = filepath.name

        try:
            # Extract components
            head_content = extract_head_content(filepath)
            body_content = extract_post_content(filepath)

            if body_content:
                # Rebuild with standard structure
                html = rebuild_post(filepath, head_content, body_content)

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html)

                print(f"[OK] {filename} - Cleaned and standardized")
                updated_count += 1
            else:
                print(f"[SKIP] {filename} - Could not extract content")

        except Exception as e:
            print(f"[ERROR] {filename} - {str(e)}")
            error_count += 1

    print("\n" + "="*80)
    print(f"Cleaned: {updated_count} posts")
    print(f"Errors: {error_count} posts")
    print(f"Total: {len(html_files)} posts processed")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
