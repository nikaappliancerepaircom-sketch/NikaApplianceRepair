#!/usr/bin/env python3
"""
Auto-update sitemap.xml lastmod dates

Use this script when you:
1. Update content on existing pages
2. Want to tell Google to re-crawl specific pages

You DON'T need this script when:
- Just checking the site
- Google will auto-discover changes anyway
"""

import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

def update_sitemap_dates():
    """Update lastmod dates in sitemap.xml to today"""

    sitemap_path = Path('C:/NikaApplianceRepair/sitemap.xml')

    # Parse XML
    tree = ET.parse(sitemap_path)
    root = tree.getroot()

    # Get namespace
    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

    # Get today's date
    today = datetime.now().strftime('%Y-%m-%d')

    # Update all lastmod dates
    urls = root.findall('ns:url', namespace)
    updated_count = 0

    for url in urls:
        lastmod = url.find('ns:lastmod', namespace)
        if lastmod is not None:
            old_date = lastmod.text
            lastmod.text = today
            updated_count += 1

    # Write back (preserve formatting)
    tree.write(
        sitemap_path,
        encoding='UTF-8',
        xml_declaration=True,
        method='xml'
    )

    print(f'Sitemap Updated!')
    print(f'Updated {updated_count} URLs to date: {today}')
    print(f'\nNext step: Google will auto-discover changes within 1-3 days.')
    print(f'Optional: Force re-index via Google Search Console.')

if __name__ == '__main__':
    update_sitemap_dates()
