#!/usr/bin/env python3
"""
Generate sitemap.xml for all blog posts and pages
Includes blog posts from all categories
"""
import os
from pathlib import Path
from datetime import datetime
import re

def extract_metadata_from_html(filepath):
    """Extract metadata from HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title
    title = ''
    if '<title>' in content:
        start = content.find('<title>') + 7
        end = content.find('</title>')
        title = content[start:end]

    # Get last modified date from file
    modified_timestamp = os.path.getmtime(filepath)
    lastmod = datetime.fromtimestamp(modified_timestamp).strftime('%Y-%m-%d')

    return {
        'title': title,
        'lastmod': lastmod
    }

def generate_sitemap(base_url='https://nikaappliancerepair.com'):
    """Generate complete sitemap.xml"""
    base_dir = Path(__file__).parent.parent

    urls = []

    print("=" * 70)
    print("GENERATING SITEMAP.XML")
    print("=" * 70)
    print()

    # 1. Add homepage
    print("[+] Adding homepage...")
    urls.append({
        'loc': base_url,
        'lastmod': datetime.now().strftime('%Y-%m-%d'),
        'changefreq': 'weekly',
        'priority': '1.0'
    })

    # 2. Add main pages
    print("[+] Adding main pages...")
    main_pages = ['services.html', 'locations.html', 'brands.html', 'about.html', 'blog.html']
    for page in main_pages:
        page_path = base_dir / page
        if page_path.exists():
            metadata = extract_metadata_from_html(page_path)
            urls.append({
                'loc': f"{base_url}/{page.replace('.html', '')}",
                'lastmod': metadata['lastmod'],
                'changefreq': 'weekly',
                'priority': '0.9'
            })
            print(f"    + {page}")

    # 3. Add location pages
    print("\n[+] Adding location pages...")
    locations_dir = base_dir / 'locations'
    if locations_dir.exists():
        location_count = 0
        for location_file in sorted(locations_dir.glob('*.html')):
            metadata = extract_metadata_from_html(location_file)
            urls.append({
                'loc': f"{base_url}/locations/{location_file.stem}",
                'lastmod': metadata['lastmod'],
                'changefreq': 'monthly',
                'priority': '0.8'
            })
            location_count += 1
        print(f"    + {location_count} location pages added")

    # 4. Add service pages
    print("\n[+] Adding service pages...")
    services_dir = base_dir / 'services'
    if services_dir.exists():
        service_count = 0
        for service_file in sorted(services_dir.glob('*.html')):
            metadata = extract_metadata_from_html(service_file)
            urls.append({
                'loc': f"{base_url}/services/{service_file.stem}",
                'lastmod': metadata['lastmod'],
                'changefreq': 'monthly',
                'priority': '0.8'
            })
            service_count += 1
        print(f"    + {service_count} service pages added")

    # 5. Add brand pages
    print("\n[+] Adding brand pages...")
    brands_dir = base_dir / 'brands'
    if brands_dir.exists():
        brand_count = 0
        for brand_file in sorted(brands_dir.glob('*.html')):
            metadata = extract_metadata_from_html(brand_file)
            urls.append({
                'loc': f"{base_url}/brands/{brand_file.stem}",
                'lastmod': metadata['lastmod'],
                'changefreq': 'monthly',
                'priority': '0.7'
            })
            brand_count += 1
        print(f"    + {brand_count} brand pages added")

    # 6. Add blog posts from all categories
    print("\n[+] Adding blog posts...")
    blog_dir = base_dir / 'blog'
    blog_categories = ['posts', 'troubleshooting', 'maintenance', 'guides', 'seasonal', 'brands', 'locations']

    total_blog_posts = 0
    for category in blog_categories:
        category_dir = blog_dir / category
        if category_dir.exists():
            category_count = 0
            for post_file in sorted(category_dir.glob('*.html')):
                metadata = extract_metadata_from_html(post_file)
                urls.append({
                    'loc': f"{base_url}/blog/{category}/{post_file.stem}",
                    'lastmod': metadata['lastmod'],
                    'changefreq': 'monthly',
                    'priority': '0.7'
                })
                category_count += 1
            if category_count > 0:
                print(f"    + {category_count} posts from {category}")
                total_blog_posts += category_count

    print(f"\n[TOTAL] {total_blog_posts} blog posts added to sitemap")

    # Generate XML
    print("\n[+] Generating XML...")
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for url_data in urls:
        xml += '  <url>\n'
        xml += f'    <loc>{url_data["loc"]}</loc>\n'
        xml += f'    <lastmod>{url_data["lastmod"]}</lastmod>\n'
        xml += f'    <changefreq>{url_data["changefreq"]}</changefreq>\n'
        xml += f'    <priority>{url_data["priority"]}</priority>\n'
        xml += '  </url>\n'

    xml += '</urlset>'

    # Write sitemap.xml
    sitemap_path = base_dir / 'sitemap.xml'
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(xml)

    print(f"\n[OK] Sitemap generated successfully!")
    print(f"     Location: {sitemap_path}")
    print(f"     Total URLs: {len(urls)}")
    print("=" * 70)

    return sitemap_path, len(urls)

def main():
    """Main function"""
    generate_sitemap()

if __name__ == '__main__':
    main()
