#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update blog.html to show only published posts
"""

import os
import sys
import glob
import re

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def get_published_posts():
    """Get all published blog posts"""
    published = []

    categories = ['brands', 'maintenance', 'cost-pricing', 'location', 'seasonal', 'troubleshooting']

    for category in categories:
        category_dir = f'blog/{category}'
        if os.path.exists(category_dir):
            posts = glob.glob(f'{category_dir}/*.html')
            for post in posts:
                filename = os.path.basename(post)
                slug = filename.replace('.html', '')

                # Read post to get metadata
                with open(post, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract title
                h1_match = re.search(r'<h1>(.*?)</h1>', content)
                title = h1_match.group(1) if h1_match else slug.replace('-', ' ').title()

                # Extract meta description
                meta_match = re.search(r'<meta name="description" content="(.*?)"', content)
                description = meta_match.group(1) if meta_match else ""

                published.append({
                    'category': category,
                    'slug': slug,
                    'title': title,
                    'description': description[:150] + '...' if len(description) > 150 else description,
                    'url': f'/blog/{category}/{slug}'
                })

    return published

def generate_blog_html(posts):
    """Generate blog.html with published posts"""

    # Category icons
    category_icons = {
        'troubleshooting': '🔧',
        'maintenance': '🛠️',
        'brands': '🏷️',
        'cost-pricing': '💰',
        'seasonal': '🌤️',
        'location': '📍'
    }

    # Category names
    category_names = {
        'troubleshooting': 'Troubleshooting',
        'maintenance': 'Maintenance',
        'brands': 'Brands',
        'cost-pricing': 'Cost & Pricing',
        'seasonal': 'Seasonal',
        'location': 'Location'
    }

    # Featured post (first one)
    featured = posts[0] if posts else None

    # Generate HTML
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Appliance Repair Blog | Toronto Expert Tips & Guides | Nika</title>
    <meta name="description" content="Expert appliance repair tips, troubleshooting guides, and maintenance advice for Toronto homeowners. Learn DIY fixes, repair costs, and when to call a pro.">
    <link rel="canonical" href="https://nikaappliancerepair.com/blog">

    <!-- Preconnect -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&family=Rubik:wght@400;500;600&display=swap" rel="stylesheet">

    <!-- Styles -->
    <link rel="stylesheet" href="css/design-system.css">
    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="css/header-optimized.css">

    <!-- Schema.org - Blog -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Blog",
      "name": "Nika Appliance Repair Blog",
      "description": "Expert appliance repair tips, troubleshooting guides, and maintenance advice for Toronto homeowners",
      "url": "https://nikaappliancerepair.com/blog",
      "publisher": {
        "@type": "Organization",
        "name": "Nika Appliance Repair",
        "logo": {
          "@type": "ImageObject",
          "url": "https://nikaappliancerepair.com/assets/images/logo.png"
        }
      }
    }
    </script>

    <style>
        /* Blog Index Specific Styles */
        .blog-hero {
            background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
            color: white;
            padding: 4rem 2rem;
            text-align: center;
        }

        .blog-hero h1 {
            font-family: 'Fredoka', sans-serif;
            font-size: clamp(2rem, 5vw, 3rem);
            font-weight: 700;
            margin-bottom: 1rem;
        }

        .blog-hero p {
            font-size: 1.25rem;
            opacity: 0.95;
            max-width: 700px;
            margin: 0 auto;
        }

        .blog-main {
            max-width: 1200px;
            margin: 0 auto;
            padding: 3rem 1.5rem;
        }

        /* Categories */
        .blog-categories {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            justify-content: center;
            margin: 2rem 0 3rem;
        }

        .category-filter {
            padding: 0.75rem 1.5rem;
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 30px;
            text-decoration: none;
            color: #333;
            font-weight: 600;
            transition: all 0.3s;
            cursor: pointer;
        }

        .category-filter:hover,
        .category-filter.active {
            background: #2196F3;
            color: white;
            border-color: #2196F3;
            transform: translateY(-2px);
        }

        /* Featured Post */
        .featured-post {
            background: white;
            border-radius: 16px;
            padding: 2.5rem;
            margin-bottom: 3rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            display: grid;
            grid-template-columns: 120px 1fr;
            gap: 2rem;
            align-items: center;
        }

        .featured-image {
            font-size: 5rem;
            text-align: center;
        }

        .featured-badge {
            display: inline-block;
            background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
            color: white;
            padding: 0.4rem 1rem;
            border-radius: 20px;
            font-weight: 700;
            font-size: 0.85rem;
            margin-bottom: 1rem;
        }

        .featured-content h2 {
            font-family: 'Fredoka', sans-serif;
            font-size: 1.75rem;
            margin-bottom: 0.75rem;
            color: #1a1a1a;
        }

        .featured-meta {
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }

        .featured-content p {
            color: #555;
            line-height: 1.7;
            margin-bottom: 1.5rem;
        }

        .read-more {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            color: #2196F3;
            font-weight: 700;
            text-decoration: none;
            transition: gap 0.3s;
        }

        .read-more:hover {
            gap: 0.75rem;
        }

        /* Posts Grid */
        .posts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 2rem;
        }

        .post-card {
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            text-decoration: none;
            color: inherit;
            transition: all 0.3s;
            display: flex;
            flex-direction: column;
        }

        .post-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        }

        .post-image {
            background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
            height: 140px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 4rem;
        }

        .post-content {
            padding: 1.5rem;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
        }

        .post-category {
            display: inline-block;
            background: #E3F2FD;
            color: #1976D2;
            padding: 0.3rem 0.8rem;
            border-radius: 15px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            margin-bottom: 0.75rem;
        }

        .post-content h3 {
            font-family: 'Fredoka', sans-serif;
            font-size: 1.15rem;
            margin-bottom: 0.75rem;
            color: #1a1a1a;
            line-height: 1.4;
        }

        .post-content p {
            color: #666;
            font-size: 0.9rem;
            line-height: 1.6;
            margin-bottom: 1rem;
            flex-grow: 1;
        }

        .post-meta {
            display: flex;
            gap: 1rem;
            color: #999;
            font-size: 0.8rem;
        }

        /* Mobile */
        @media (max-width: 768px) {
            .featured-post {
                grid-template-columns: 1fr;
                text-align: center;
            }

            .featured-image {
                font-size: 4rem;
            }

            .posts-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <!-- Hero -->
    <section class="blog-hero">
        <h1>Appliance Repair Blog</h1>
        <p>Expert tips, troubleshooting guides, and maintenance advice for Toronto homeowners</p>
    </section>

    <!-- Main Content -->
    <main class="blog-main">
        <!-- Categories -->
        <nav class="blog-categories">
            <button class="category-filter active" data-category="all">📚 All Posts</button>'''

    # Add category buttons
    categories_used = set(post['category'] for post in posts)
    for cat in ['troubleshooting', 'maintenance', 'cost-pricing', 'brands', 'seasonal', 'location']:
        if cat in categories_used:
            icon = category_icons.get(cat, '📄')
            name = category_names.get(cat, cat.title())
            html += f'\n            <button class="category-filter" data-category="{cat}">{icon} {name}</button>'

    html += '\n        </nav>\n\n'

    # Featured post
    if featured:
        icon = category_icons.get(featured['category'], '📄')
        html += f'''        <!-- Featured Post -->
        <article class="featured-post">
            <div class="featured-image">{icon}</div>
            <div class="featured-content">
                <span class="featured-badge">⚡ Featured</span>
                <h2>{featured['title']}</h2>
                <div class="featured-meta">
                    <span>January 21, 2025</span>
                    <span>•</span>
                    <span>7 min read</span>
                </div>
                <p>{featured['description']}</p>
                <a href="{featured['url']}" class="read-more">Read Full Guide →</a>
            </div>
        </article>

'''

    # Posts grid
    html += '        <!-- Posts Grid -->\n'
    html += '        <div class="posts-grid">\n\n'

    for post in posts:
        icon = category_icons.get(post['category'], '📄')
        cat_name = category_names.get(post['category'], post['category'].title())

        html += f'''            <a href="{post['url']}" class="post-card" data-category="{post['category']}">
                <div class="post-image">{icon}</div>
                <div class="post-content">
                    <span class="post-category">{cat_name}</span>
                    <h3>{post['title']}</h3>
                    <p>{post['description']}</p>
                    <div class="post-meta">
                        <span>Jan 21, 2025</span>
                        <span>7 min read</span>
                    </div>
                </div>
            </a>

'''

    html += '''        </div>
    </main>

    <script>
        // Category filtering
        const filters = document.querySelectorAll('.category-filter');
        const posts = document.querySelectorAll('.post-card');

        filters.forEach(filter => {
            filter.addEventListener('click', () => {
                const category = filter.dataset.category;

                // Update active state
                filters.forEach(f => f.classList.remove('active'));
                filter.classList.add('active');

                // Filter posts
                posts.forEach(post => {
                    if (category === 'all' || post.dataset.category === category) {
                        post.style.display = 'flex';
                    } else {
                        post.style.display = 'none';
                    }
                });
            });
        });
    </script>
</body>
</html>'''

    return html

def main():
    print("=" * 70)
    print("📝 UPDATING BLOG.HTML WITH PUBLISHED POSTS")
    print("=" * 70)
    print()

    # Get published posts
    posts = get_published_posts()
    print(f"✅ Found {len(posts)} published posts")
    print()

    if not posts:
        print("❌ No published posts found!")
        return

    # Show posts by category
    categories = {}
    for post in posts:
        if post['category'] not in categories:
            categories[post['category']] = []
        categories[post['category']].append(post['title'][:50] + '...')

    for cat, titles in sorted(categories.items()):
        print(f"{cat.upper()}: {len(titles)} posts")
        for title in titles:
            print(f"  • {title}")

    print()

    # Generate HTML
    html = generate_blog_html(posts)

    # Write file
    with open('blog.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("=" * 70)
    print(f"✅ Updated blog.html with {len(posts)} published posts")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Review blog.html in browser")
    print("2. git add blog.html")
    print("3. git commit -m 'Update blog.html to show only published posts'")
    print("4. git push")

if __name__ == "__main__":
    main()
