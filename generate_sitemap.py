#!/usr/bin/env python3
"""
Generate Sitemap with Clean URLs (no .html extensions)
Creates SEO-optimized sitemap for Google Search Console
"""

import os
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom

def generate_sitemap():
    """Generate sitemap.xml with clean URLs only"""

    base_url = "https://nikaappliancerepair.com"
    today = datetime.now().strftime("%Y-%m-%d")

    # Create XML structure
    urlset = ET.Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    # Static pages (high priority)
    static_pages = [
        ('/', '1.0', 'weekly', today),
        ('/about', '1.0', 'weekly', today),
        ('/services', '1.0', 'weekly', today),
        ('/locations', '0.9', 'weekly', today),
        ('/brands', '0.9', 'weekly', today),
        ('/book', '0.95', 'weekly', today),
        ('/team', '0.85', 'monthly', today),
        ('/optimizations', '0.7', 'monthly', today),
        ('/blog/', '0.95', 'daily', today),
    ]

    for path, priority, changefreq, lastmod in static_pages:
        url = ET.SubElement(urlset, 'url')
        ET.SubElement(url, 'loc').text = base_url + path
        ET.SubElement(url, 'lastmod').text = lastmod
        ET.SubElement(url, 'changefreq').text = changefreq
        ET.SubElement(url, 'priority').text = priority

    # Blog posts (clean URLs without .html)
    blog_dir = Path("C:\\NikaApplianceRepair\\blog")
    html_files = []

    # Find all blog HTML files
    for category in ['guides', 'troubleshooting', 'maintenance']:
        category_path = blog_dir / category
        if category_path.exists():
            html_files.extend(list(category_path.glob("*.html")))

    print(f"Found {len(html_files)} blog posts")

    # Add blog posts to sitemap
    for html_file in html_files:
        # Get relative path from blog directory
        relative_path = html_file.relative_to(blog_dir)

        # Convert to clean URL
        # Example: guides/bosch-dishwasher-repair.html -> /blog/guides/bosch-dishwasher-repair
        path_parts = list(relative_path.parts)

        # Remove .html extension
        if path_parts[-1].endswith('.html'):
            path_parts[-1] = path_parts[-1][:-5]

        # Build clean URL path
        clean_path = "/blog/" + "/".join(path_parts)
        full_url = base_url + clean_path

        # Get file modification time
        mtime = datetime.fromtimestamp(html_file.stat().st_mtime)
        lastmod = mtime.strftime("%Y-%m-%d")

        # Determine priority based on category
        if 'guides' in str(relative_path):
            priority = '0.9'
        elif 'troubleshooting' in str(relative_path):
            priority = '0.85'
        else:  # maintenance
            priority = '0.8'

        # Add to sitemap
        url = ET.SubElement(urlset, 'url')
        ET.SubElement(url, 'loc').text = full_url
        ET.SubElement(url, 'lastmod').text = lastmod
        ET.SubElement(url, 'changefreq').text = 'weekly'
        ET.SubElement(url, 'priority').text = priority

        print(f"Added: {clean_path}")

    # Pretty print XML
    xml_str = minidom.parseString(ET.tostring(urlset)).toprettyxml(indent="  ")

    # Remove empty lines
    xml_str = "\n".join([line for line in xml_str.split("\n") if line.strip()])

    # Write to file
    sitemap_path = Path("C:\\NikaApplianceRepair\\sitemap.xml")
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(xml_str)

    print(f"\n{'='*60}")
    print(f"Sitemap generated successfully!")
    print(f"  Location: {sitemap_path}")
    print(f"  Total URLs: {len(urlset)}")
    print(f"  Static pages: {len(static_pages)}")
    print(f"  Blog posts: {len(html_files)}")
    print(f"{'='*60}")
    print(f"\nAll URLs use clean format (no .html extension)")
    print(f"Submit to Google Search Console: https://search.google.com/search-console")

if __name__ == "__main__":
    generate_sitemap()
