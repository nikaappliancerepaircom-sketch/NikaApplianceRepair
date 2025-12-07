#!/usr/bin/env python3
"""
Generate RSS feed from published blog posts
Scans blog folders and creates feed.xml for automation integrations
"""
import os
import re
from pathlib import Path
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

def get_post_data(filepath):
    """Extract metadata from blog post HTML"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    data = {
        'filepath': str(filepath),
        'filename': filepath.name,
        'title': '',
        'description': '',
        'date': '',
        'url': '',
        'image': ''
    }

    # Parse title
    title_match = re.search(r'<title>([^<]+)</title>', content)
    if title_match:
        data['title'] = title_match.group(1).replace(' | Nika Appliance Repair', '').strip()

    # Parse meta description
    desc_match = re.search(r'<meta name="description" content="([^"]+)"', content)
    if desc_match:
        data['description'] = desc_match.group(1)

    # Parse date from multiple sources
    date_match = re.search(r'<meta property="article:published_time" content="(\d{4}-\d{2}-\d{2})"', content)
    if not date_match:
        date_match = re.search(r'^date:\s*["\']?(\d{4}-\d{2}-\d{2})["\']?', content, re.MULTILINE)
    if not date_match:
        date_match = re.search(r'"datePublished":\s*"(\d{4}-\d{2}-\d{2})"', content)

    if date_match:
        data['date'] = date_match.group(1)

    # Parse canonical URL
    canonical_match = re.search(r'<link rel="canonical" href="([^"]+)"', content)
    if canonical_match:
        data['url'] = canonical_match.group(1)

    # Parse OG image
    image_match = re.search(r'<meta property="og:image" content="([^"]+)"', content)
    if image_match:
        data['image'] = image_match.group(1)

    return data

def generate_rss(base_dir, output_file='feed.xml', limit=20):
    """Generate RSS feed from blog posts"""

    blog_folders = [
        'blog/posts',
        'blog/troubleshooting',
        'blog/maintenance',
        'blog/guides',
        'blog/seasonal',
        'blog/brands'
    ]

    all_posts = []

    for folder in blog_folders:
        folder_path = base_dir / folder
        if folder_path.exists():
            for html_file in folder_path.glob('*.html'):
                if html_file.name != 'index.html':
                    post_data = get_post_data(html_file)
                    if post_data['title'] and post_data['date']:
                        all_posts.append(post_data)

    # Sort by date (newest first)
    all_posts.sort(key=lambda x: x['date'], reverse=True)

    # Limit posts
    all_posts = all_posts[:limit]

    # Create RSS XML
    rss = Element('rss', version='2.0')
    rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')
    rss.set('xmlns:media', 'http://search.yahoo.com/mrss/')

    channel = SubElement(rss, 'channel')

    # Channel metadata
    SubElement(channel, 'title').text = "Nika Appliance Repair Blog"
    SubElement(channel, 'link').text = "https://nikaappliancerepair.com/blog"
    SubElement(channel, 'description').text = "Expert appliance repair tips, troubleshooting guides, and maintenance advice for Toronto homeowners"
    SubElement(channel, 'language').text = "en-ca"
    SubElement(channel, 'lastBuildDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')

    atom_link = SubElement(channel, 'atom:link')
    atom_link.set('href', 'https://nikaappliancerepair.com/feed.xml')
    atom_link.set('rel', 'self')
    atom_link.set('type', 'application/rss+xml')

    # Add items
    for post in all_posts:
        item = SubElement(channel, 'item')
        SubElement(item, 'title').text = post['title']
        SubElement(item, 'link').text = post['url']
        SubElement(item, 'description').text = post['description']

        # Format date for RSS
        try:
            pub_date = datetime.strptime(post['date'], '%Y-%m-%d')
            SubElement(item, 'pubDate').text = pub_date.strftime('%a, %d %b %Y 09:00:00 +0000')
        except:
            pass

        SubElement(item, 'guid', isPermaLink='true').text = post['url']

        if post['image']:
            enclosure = SubElement(item, 'enclosure')
            enclosure.set('url', post['image'])
            enclosure.set('type', 'image/webp')

    # Pretty print XML
    xml_str = minidom.parseString(tostring(rss)).toprettyxml(indent='  ')
    # Remove extra blank lines
    xml_str = '\n'.join([line for line in xml_str.split('\n') if line.strip()])

    # Write to file
    output_path = base_dir / output_file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(xml_str)

    print(f"[OK] Generated RSS feed with {len(all_posts)} posts")
    print(f"[OK] Saved to: {output_path}")

    return all_posts

def main():
    base_dir = Path(__file__).parent.parent
    posts = generate_rss(base_dir)

    print(f"\nLatest posts in feed:")
    for i, post in enumerate(posts[:5], 1):
        print(f"  {i}. {post['title'][:50]}... ({post['date']})")

if __name__ == '__main__':
    main()
