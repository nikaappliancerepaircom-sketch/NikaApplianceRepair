#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update sitemap.xml with all blog posts
"""

import os
import sys
import glob
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Get all blog HTML files
blog_files = []

# Search in all blog directories
blog_dirs = [
    'blog/troubleshooting',
    'blog/maintenance',
    'blog/cost-pricing',
    'blog/brands',
    'blog/seasonal',
    'blog/location'
]

for blog_dir in blog_dirs:
    if os.path.exists(blog_dir):
        files = glob.glob(f'{blog_dir}/*.html')
        for file in files:
            # Convert to URL path
            url_path = file.replace('\\', '/').replace('.html', '')
            blog_files.append(url_path)

# Sort alphabetically
blog_files.sort()

print(f"Found {len(blog_files)} blog posts")

# Read existing sitemap
with open('sitemap.xml', 'r', encoding='utf-8') as f:
    sitemap_content = f.read()

# Find where to insert blog posts (before closing </urlset>)
insert_position = sitemap_content.rfind('</urlset>')

# Generate blog post URLs
today = datetime.now().strftime('%Y-%m-%d')
blog_urls = []

for blog_file in blog_files:
    url_entry = f'''  <url>
    <loc>https://nikaappliancerepair.com/{blog_file}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
'''
    blog_urls.append(url_entry)

# Combine all blog URLs
all_blog_urls = '\n'.join(blog_urls)

# Insert into sitemap
new_sitemap = sitemap_content[:insert_position] + all_blog_urls + sitemap_content[insert_position:]

# Write updated sitemap
with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(new_sitemap)

print(f"✅ Updated sitemap.xml with {len(blog_files)} blog posts")
print(f"📅 Last modified: {today}")
