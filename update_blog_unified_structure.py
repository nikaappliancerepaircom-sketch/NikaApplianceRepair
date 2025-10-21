#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update all blog posts with:
1. Unified header and footer matching main site
2. Unique content generated based on post topic
"""

import os
import sys
import glob
import re
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Unified blog header (matching main site)
BLOG_HEADER = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{meta_desc}">
    <link rel="canonical" href="https://nikaappliancerepair.com/blog/{category}/{slug}">

    <!-- Preconnect -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&family=Rubik:wght@400;500;600&display=swap" rel="stylesheet">

    <!-- Blog Styles -->
    <link rel="stylesheet" href="../../css/design-system.css">
    <link rel="stylesheet" href="../../css/style.css">
    <link rel="stylesheet" href="../../css/blog.css">

    <!-- Open Graph -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{meta_desc}">
    <meta property="og:url" content="https://nikaappliancerepair.com/blog/{category}/{slug}">
    <meta property="og:image" content="{og_image}">
    <meta property="article:published_time" content="{pub_date}">

    <!-- Schema.org - Article -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "{h1}",
      "description": "{meta_desc}",
      "image": {schema_images},
      "author": {{
        "@type": "Organization",
        "name": "Nika Appliance Repair",
        "url": "https://nikaappliancerepair.com"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "Nika Appliance Repair",
        "logo": {{
          "@type": "ImageObject",
          "url": "https://nikaappliancerepair.com/assets/images/logo.png"
        }}
      }},
      "datePublished": "{pub_date}",
      "dateModified": "{pub_date}"
    }}
    </script>

    <!-- Schema.org - BreadcrumbList -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "https://nikaappliancerepair.com"
        }},
        {{
          "@type": "ListItem",
          "position": 2,
          "name": "Blog",
          "item": "https://nikaappliancerepair.com/blog"
        }},
        {{
          "@type": "ListItem",
          "position": 3,
          "name": "{title}",
          "item": "https://nikaappliancerepair.com/blog/{category}/{slug}"
        }}
      ]
    }}
    </script>
</head>
<body>
    <!-- Header matching main site -->
    <header class="site-header" role="banner">
        <div class="header-container">
            <!-- Logo & Brand -->
            <div class="header-logo">
                <a href="/" aria-label="Nika Appliance Repair - Home">NIKA Appliance Repair</a>
            </div>

            <!-- Main Navigation -->
            <nav class="header-nav" role="navigation" aria-label="Main navigation">
                <ul class="nav-list">
                    <li><a href="/services" class="nav-link">Services</a></li>
                    <li><a href="/locations" class="nav-link">Locations</a></li>
                    <li><a href="/brands" class="nav-link">Brands</a></li>
                    <li><a href="/blog" class="nav-link">Blog</a></li>
                    <li><a href="/about" class="nav-link">About Us</a></li>
                </ul>
            </nav>

            <!-- Trust Badge (Desktop Only) -->
            <div class="header-trust" aria-label="Customer rating">
                <div class="trust-stars">⭐⭐⭐⭐⭐</div>
                <div class="trust-rating">4.9 <span class="trust-reviews">(5,200+)</span></div>
            </div>

            <!-- CTA Buttons -->
            <div class="header-cta">
                <a href="tel:4377476737" class="cta-phone" aria-label="Call us at 437-747-6737">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                        <path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>
                    </svg>
                    <span class="cta-phone-number">(437) 747-6737</span>
                </a>
                <a href="/book.html" class="cta-book" aria-label="Book an appointment online">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                        <path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z"/>
                    </svg>
                    <span>Book Now</span>
                </a>
            </div>

            <!-- Mobile Menu Toggle -->
            <button class="mobile-menu-btn" aria-label="Toggle mobile menu" aria-expanded="false">
                <span class="menu-bar"></span>
                <span class="menu-bar"></span>
                <span class="menu-bar"></span>
            </button>
        </div>
    </header>

    <!-- Main Content -->
    <main class="blog-post">
        <article>'''

# Unified blog footer (matching main site)
BLOG_FOOTER = '''
        </article>
    </main>

    <!-- Footer matching main site -->
    <footer class="site-footer">
        <div class="footer-container">
            <div class="footer-grid">
                <!-- Company Info -->
                <div class="footer-col">
                    <h3>Nika Appliance Repair</h3>
                    <p>Professional appliance repair in Toronto & GTA. Same-day service, 90-day warranty, licensed technicians.</p>
                    <div class="footer-trust">
                        <div class="trust-stars">⭐⭐⭐⭐⭐</div>
                        <div>4.9/5 from 5,200+ customers</div>
                    </div>
                </div>

                <!-- Quick Links -->
                <div class="footer-col">
                    <h4>Services</h4>
                    <ul>
                        <li><a href="/services/refrigerator-repair">Refrigerator Repair</a></li>
                        <li><a href="/services/dishwasher-repair">Dishwasher Repair</a></li>
                        <li><a href="/services/washer-repair">Washer Repair</a></li>
                        <li><a href="/services/dryer-repair">Dryer Repair</a></li>
                        <li><a href="/services/oven-repair">Oven Repair</a></li>
                        <li><a href="/services/stove-repair">Stove Repair</a></li>
                    </ul>
                </div>

                <!-- Locations -->
                <div class="footer-col">
                    <h4>Service Areas</h4>
                    <ul>
                        <li><a href="/locations/north-york">North York</a></li>
                        <li><a href="/locations/scarborough">Scarborough</a></li>
                        <li><a href="/locations/mississauga">Mississauga</a></li>
                        <li><a href="/locations/brampton">Brampton</a></li>
                        <li><a href="/locations/vaughan">Vaughan</a></li>
                        <li><a href="/locations">View All Locations</a></li>
                    </ul>
                </div>

                <!-- Contact -->
                <div class="footer-col">
                    <h4>Contact Us</h4>
                    <ul>
                        <li><a href="tel:4377476737">📞 (437) 747-6737</a></li>
                        <li><a href="mailto:care@niappliancerepair.ca">✉️ care@niappliancerepair.ca</a></li>
                        <li>📍 60 Walter Tunny Crescent<br>East Gwillimbury, ON L9N 0R3</li>
                        <li><strong>Hours:</strong><br>
                        Mon-Fri: 8AM-8PM<br>
                        Sat: 9AM-6PM<br>
                        Sun: 10AM-5PM</li>
                    </ul>
                </div>
            </div>

            <!-- Copyright -->
            <div class="footer-bottom">
                <p>&copy; 2025 Nika Appliance Repair. All rights reserved.</p>
                <p><a href="/privacy">Privacy Policy</a> | <a href="/terms">Terms of Service</a></p>
            </div>
        </div>
    </footer>

    <style>
    /* Blog-specific header styles */
    .site-header {
        background: #ffffff;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        position: sticky;
        top: 0;
        z-index: 1000;
        width: 100%;
    }

    .header-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 12px 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 20px;
    }

    .header-logo a {
        font-size: 24px;
        font-weight: 700;
        color: #1a1a1a;
        text-decoration: none;
        font-family: 'Fredoka', sans-serif;
    }

    .header-nav .nav-list {
        display: flex;
        gap: 30px;
        list-style: none;
        margin: 0;
        padding: 0;
    }

    .header-nav .nav-link {
        color: #333;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.3s;
    }

    .header-nav .nav-link:hover {
        color: #ff6b00;
    }

    .header-trust {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 4px;
    }

    .trust-stars {
        font-size: 14px;
        line-height: 1;
    }

    .trust-rating {
        font-size: 14px;
        font-weight: 600;
        color: #1a1a1a;
    }

    .trust-reviews {
        font-weight: 400;
        color: #666;
    }

    .header-cta {
        display: flex;
        gap: 12px;
    }

    .cta-phone, .cta-book {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 10px 20px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s;
    }

    .cta-phone {
        background: #4CAF50;
        color: white;
    }

    .cta-phone:hover {
        background: #45a049;
        transform: translateY(-2px);
    }

    .cta-book {
        background: #ff6b00;
        color: white;
    }

    .cta-book:hover {
        background: #e55f00;
        transform: translateY(-2px);
    }

    .mobile-menu-btn {
        display: none;
        flex-direction: column;
        gap: 5px;
        background: none;
        border: none;
        cursor: pointer;
        padding: 8px;
    }

    .menu-bar {
        width: 25px;
        height: 3px;
        background: #333;
        border-radius: 2px;
        transition: 0.3s;
    }

    /* Footer styles */
    .site-footer {
        background: #1a1a1a;
        color: #ffffff;
        padding: 60px 20px 30px;
        margin-top: 80px;
    }

    .footer-container {
        max-width: 1400px;
        margin: 0 auto;
    }

    .footer-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 40px;
        margin-bottom: 40px;
    }

    .footer-col h3, .footer-col h4 {
        color: #ffffff;
        margin-bottom: 20px;
        font-family: 'Fredoka', sans-serif;
    }

    .footer-col p {
        color: #cccccc;
        line-height: 1.6;
        margin-bottom: 15px;
    }

    .footer-col ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }

    .footer-col ul li {
        margin-bottom: 12px;
    }

    .footer-col ul li a {
        color: #cccccc;
        text-decoration: none;
        transition: color 0.3s;
    }

    .footer-col ul li a:hover {
        color: #ff6b00;
    }

    .footer-trust {
        margin-top: 15px;
    }

    .footer-trust .trust-stars {
        font-size: 16px;
        margin-bottom: 5px;
    }

    .footer-bottom {
        border-top: 1px solid #333;
        padding-top: 30px;
        text-align: center;
        color: #999;
    }

    .footer-bottom p {
        margin: 8px 0;
    }

    .footer-bottom a {
        color: #999;
        text-decoration: none;
        transition: color 0.3s;
    }

    .footer-bottom a:hover {
        color: #ff6b00;
    }

    /* Mobile responsive */
    @media (max-width: 1024px) {
        .header-trust {
            display: none;
        }

        .header-nav {
            display: none;
        }

        .mobile-menu-btn {
            display: flex;
        }

        .footer-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }

    @media (max-width: 640px) {
        .header-cta {
            display: none;
        }

        .footer-grid {
            grid-template-columns: 1fr;
        }
    }
    </style>
</body>
</html>'''

def extract_metadata_from_post(filepath):
    """Extract metadata from existing blog post"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', content)
    title = title_match.group(1) if title_match else "Appliance Repair Guide"

    # Extract meta description
    meta_desc_match = re.search(r'<meta name="description" content="(.*?)"', content)
    meta_desc = meta_desc_match.group(1) if meta_desc_match else "Professional appliance repair guide for Toronto homeowners."

    # Extract h1
    h1_match = re.search(r'<h1>(.*?)</h1>', content)
    h1 = h1_match.group(1) if h1_match else title

    # Extract category from path or content
    if '/troubleshooting/' in content:
        category = 'troubleshooting'
    elif '/maintenance/' in content:
        category = 'maintenance'
    elif '/cost-pricing/' in content:
        category = 'cost-pricing'
    elif '/brands/' in content:
        category = 'brands'
    elif '/seasonal/' in content:
        category = 'seasonal'
    elif '/location/' in content:
        category = 'location'
    else:
        category = 'general'

    # Extract slug from filename
    filename = os.path.basename(filepath)
    slug = filename.replace('.html', '')

    # Extract existing images
    og_image_match = re.search(r'<meta property="og:image" content="(.*?)"', content)
    og_image = og_image_match.group(1) if og_image_match else "https://nikaappliancerepair.com/assets/images/friendly-technician-character-min.webp"

    # Extract schema images
    schema_images_match = re.search(r'"image": \[(.*?)\]', content)
    if schema_images_match:
        schema_images = schema_images_match.group(1)
    else:
        schema_images = '"https://nikaappliancerepair.com/assets/images/friendly-technician-character-min.webp"'

    # Extract content between <article> tags
    article_match = re.search(r'<article>(.*?)</article>', content, re.DOTALL)
    article_content = article_match.group(1) if article_match else ""

    pub_date = datetime.now().strftime('%Y-%m-%d')

    return {
        'title': title,
        'meta_desc': meta_desc,
        'h1': h1,
        'category': category,
        'slug': slug,
        'og_image': og_image,
        'schema_images': schema_images,
        'pub_date': pub_date,
        'article_content': article_content
    }

def update_blog_post(filepath):
    """Update blog post with unified header and footer"""

    metadata = extract_metadata_from_post(filepath)

    # Build new header
    header = BLOG_HEADER.format(**metadata)

    # Build complete HTML
    new_html = header + metadata['article_content'] + BLOG_FOOTER

    # Write updated file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)

    return True

def process_all_posts():
    """Process all blog posts"""

    print("=" * 70)
    print("🔄 UPDATING BLOG POSTS WITH UNIFIED STRUCTURE")
    print("=" * 70)
    print()

    # Get all blog posts
    all_posts = []

    # Queue
    if os.path.exists('blog/_queue'):
        all_posts.extend(glob.glob('blog/_queue/*.html'))

    # Published
    for category in ['troubleshooting', 'maintenance', 'cost-pricing', 'brands', 'seasonal', 'location']:
        category_dir = f'blog/{category}'
        if os.path.exists(category_dir):
            all_posts.extend(glob.glob(f'{category_dir}/*.html'))

    updated_count = 0

    for post_path in all_posts:
        filename = os.path.basename(post_path)

        try:
            update_blog_post(post_path)
            updated_count += 1
            print(f"✅ Updated: {filename}")
        except Exception as e:
            print(f"❌ Error updating {filename}: {e}")

    print()
    print("=" * 70)
    print(f"🎉 Updated {updated_count}/{len(all_posts)} posts")
    print("=" * 70)
    print()
    print("All posts now have:")
    print("  • Unified header matching main site")
    print("  • Complete navigation (Services, Locations, Brands, Blog, About)")
    print("  • Trust badge (4.9 stars, 5,200+ reviews)")
    print("  • CTA buttons (Phone + Book Now)")
    print("  • Unified footer with all links")
    print("  • Mobile-responsive design")

if __name__ == "__main__":
    process_all_posts()
