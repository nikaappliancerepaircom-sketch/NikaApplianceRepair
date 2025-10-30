#!/usr/bin/env python3
"""
CORRECTLY rebuild ONLY maintenance posts with COMPLETE footer styles
"""
import re
from pathlib import Path

def extract_post_content(filepath):
    """Extract just the article body text"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    article_match = re.search(r'<article[^>]*>(.*?)</article>', content, re.DOTALL)
    if article_match:
        return article_match.group(1).strip()
    return ""

def extract_head_meta(filepath):
    """Extract meta tags and title from head"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    title_match = re.search(r'<title[^>]*>([^<]+)</title>', content)
    title = title_match.group(1) if title_match else "Blog Post"

    desc_match = re.search(r'<meta name="description" content="([^"]+)"', content)
    description = desc_match.group(1) if desc_match else ""

    kw_match = re.search(r'<meta name="keywords" content="([^"]+)"', content)
    keywords = kw_match.group(1) if kw_match else ""

    return {
        'title': title,
        'description': description,
        'keywords': keywords,
    }

def get_footer_styles():
    """Return the complete inline CSS for footer from premium template"""
    return '''    <!-- Footer Styles -->
    <style>
        /* Footer Premium Styles */
        .seo-footer-premium {
            background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
            color: white;
            padding: 3rem 0 1.5rem;
            margin-top: 4rem;
        }

        .seo-footer-premium .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 2rem;
        }

        .footer-trust-badges {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
            padding-bottom: 2rem;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }

        .trust-badge-item {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .badge-icon {
            font-size: 2rem;
        }

        .badge-text strong {
            display: block;
            font-size: 1rem;
            margin-bottom: 0.25rem;
        }

        .badge-text span {
            font-size: 0.875rem;
            opacity: 0.8;
        }

        .footer-main-content {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }

        .footer-heading {
            font-size: 1.125rem;
            margin-bottom: 1rem;
            font-weight: 600;
        }

        .footer-links {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .footer-links li {
            margin-bottom: 0.5rem;
        }

        .footer-links a {
            color: rgba(255,255,255,0.8);
            text-decoration: none;
            font-size: 0.95rem;
            transition: color 0.2s;
        }

        .footer-links a:hover {
            color: white;
        }

        .footer-contact-box {
            margin-bottom: 1.5rem;
        }

        .contact-item {
            margin-bottom: 1rem;
            font-size: 0.95rem;
            line-height: 1.6;
        }

        .contact-link {
            color: #93c5fd;
            text-decoration: none;
        }

        .contact-link:hover {
            color: #60a5fa;
            text-decoration: underline;
        }

        .footer-cta-button {
            display: inline-flex;
            align-items: center;
            gap: 0.75rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem 2rem;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            transition: transform 0.2s;
        }

        .footer-cta-button:hover {
            transform: translateY(-2px);
        }

        .footer-bottom {
            margin-top: 2rem;
            padding-top: 1.5rem;
            border-top: 1px solid rgba(255,255,255,0.1);
        }

        .footer-bottom-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }

        .copyright {
            font-size: 0.875rem;
            opacity: 0.8;
            margin: 0;
        }

        .separator {
            margin: 0 0.5rem;
        }

        .footer-tagline {
            font-size: 0.875rem;
            opacity: 0.8;
        }

        @media (max-width: 768px) {
            .footer-trust-badges {
                grid-template-columns: 1fr;
            }

            .footer-main-content {
                grid-template-columns: 1fr;
            }

            .footer-bottom-content {
                flex-direction: column;
                text-align: center;
            }
        }
    </style>'''

def get_blog_header():
    """Return the blog header section"""
    return '''            <!-- Blog Header -->
            <header class="blog-header">
                <div class="blog-meta-top">
                    <span class="blog-category">
                        <i class="fas fa-wrench"></i> Appliance Tips
                    </span>
                    <span class="reading-time">
                        <i class="far fa-clock"></i> 10 min read
                    </span>
                </div>

                <h1 class="blog-title">Blog Post</h1>

                <div class="blog-meta">
                    <span class="meta-item">
                        <i class="far fa-calendar"></i> October 30, 2025
                    </span>
                    <span class="meta-item">
                        <i class="far fa-user"></i> Expert Team
                    </span>
                </div>
            </header>

            <!-- Social Share -->
            <div class="social-share">
                <a href="#" class="share-btn facebook" aria-label="Share on Facebook">
                    <i class="fab fa-facebook-f"></i>
                </a>
                <a href="#" class="share-btn twitter" aria-label="Share on Twitter">
                    <i class="fab fa-twitter"></i>
                </a>
                <a href="#" class="share-btn linkedin" aria-label="Share on LinkedIn">
                    <i class="fab fa-linkedin-in"></i>
                </a>
                <a href="#" class="share-btn email" aria-label="Share via Email">
                    <i class="far fa-envelope"></i>
                </a>
            </div>'''

def get_sidebar():
    """Return sidebar"""
    return '''        <!-- Sidebar -->
        <aside class="blog-sidebar">
            <div class="toc-widget">
                <h3>Table of Contents</h3>
                <ul class="toc-list">
                    <li><a href="#section1">Main Topics</a></li>
                </ul>
            </div>

            <div class="related-widget">
                <h3>Related Posts</h3>
                <div class="related-post">
                    <a href="#">Top 10 Appliance Maintenance Tips</a>
                    <div class="related-post-meta">
                        <i class="far fa-calendar"></i> Oct 15, 2025
                    </div>
                </div>
                <div class="related-post">
                    <a href="#">When to Repair vs Replace Your Appliances</a>
                    <div class="related-post-meta">
                        <i class="far fa-calendar"></i> Oct 10, 2025
                    </div>
                </div>
            </div>
        </aside>'''

def get_footer():
    """Return the complete premium footer"""
    footer = '''    <!-- Footer -->
    <footer class="seo-footer-premium">
        <div class="container">
            <!-- Trust Badges Row -->
            <div class="footer-trust-badges">
                <div class="trust-badge-item">
                    <div class="badge-icon">⭐</div>
                    <div class="badge-text">
                        <strong>4.9/5 Rating</strong>
                        <span>5,200+ Reviews</span>
                    </div>
                </div>
                <div class="trust-badge-item">
                    <div class="badge-icon">🏆</div>
                    <div class="badge-text">
                        <strong>Licensed & Insured</strong>
                        <span>Since 2017</span>
                    </div>
                </div>
                <div class="trust-badge-item">
                    <div class="badge-icon">🛡️</div>
                    <div class="badge-text">
                        <strong>90-Day Warranty</strong>
                        <span>Parts & Labor</span>
                    </div>
                </div>
                <div class="trust-badge-item">
                    <div class="badge-icon">⚡</div>
                    <div class="badge-text">
                        <strong>Same-Day Service</strong>
                        <span>7 Days a Week</span>
                    </div>
                </div>
            </div>

            <!-- Main Footer Content -->
            <div class="footer-main-content">
                <!-- Column 1: Services -->
                <div class="footer-column">
                    <h4 class="footer-heading">Our Services</h4>
                    <ul class="footer-links">
                        <li><a href="/services/refrigerator-repair">Refrigerator Repair</a></li>
                        <li><a href="/services/dishwasher-repair">Dishwasher Repair</a></li>
                        <li><a href="/services/washer-repair">Washer Repair</a></li>
                        <li><a href="/services/dryer-repair">Dryer Repair</a></li>
                        <li><a href="/services/oven-repair">Oven Repair</a></li>
                    </ul>
                </div>

                <!-- Column 2: Locations -->
                <div class="footer-column">
                    <h4 class="footer-heading">Service Areas</h4>
                    <ul class="footer-links">
                        <li><a href="/locations/mississauga">Mississauga</a></li>
                        <li><a href="/locations/brampton">Brampton</a></li>
                        <li><a href="/locations/markham">Markham</a></li>
                        <li><a href="/locations/vaughan">Vaughan</a></li>
                        <li><a href="/locations/oakville">Oakville</a></li>
                    </ul>
                </div>

                <!-- Column 3: Company -->
                <div class="footer-column">
                    <h4 class="footer-heading">Company</h4>
                    <ul class="footer-links">
                        <li><a href="/about">About Us</a></li>
                        <li><a href="/reviews">Customer Reviews</a></li>
                        <li><a href="/faq">FAQ</a></li>
                        <li><a href="/book">Book Online</a></li>
                        <li><a href="/privacy">Privacy Policy</a></li>
                    </ul>
                </div>

                <!-- Column 4: Contact -->
                <div class="footer-column footer-column-contact">
                    <h4 class="footer-heading">Contact Us</h4>
                    <div class="footer-contact-box">
                        <p class="contact-item">
                            <i class="fas fa-phone"></i>
                            <a href="tel:4377476737" class="contact-link">(437) 747-6737</a>
                        </p>
                        <p class="contact-item">
                            <i class="far fa-envelope"></i>
                            <a href="mailto:care@niappliancerepair.ca" class="contact-link">care@niappliancerepair.ca</a>
                        </p>
                        <p class="contact-item">
                            <i class="fas fa-map-marker-alt"></i>
                            <span>Serving Toronto & GTA</span>
                        </p>
                    </div>

                    <a href="tel:4377476737" class="footer-cta-button">
                        <i class="fas fa-phone"></i>
                        Call for Same-Day Service
                    </a>
                </div>
            </div>

            <!-- Footer Bottom -->
            <div class="footer-bottom">
                <div class="footer-bottom-content">
                    <p class="copyright">
                        © 2025 Nika Appliance Repair. All Rights Reserved.
                        <span class="separator">|</span>
                        Licensed & Insured
                    </p>
                    <div class="footer-social-links">
                        <span class="footer-tagline">Trusted by 5,200+ Happy Customers</span>
                    </div>
                </div>
            </div>
        </div>
    </footer>'''
    return footer

def rebuild_post(filepath, meta):
    """Rebuild post with premium template structure"""
    body_content = extract_post_content(filepath)

    if not body_content:
        return None

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{meta['title']}</title>
    <meta name="description" content="{meta['description']}">
    <meta name="keywords" content="{meta['keywords']}">

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;500;600;700&family=Rubik:wght@300;400;500;600;700&display=swap" rel="stylesheet">

    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

    <!-- Premium Blog Styles -->
    <link rel="stylesheet" href="../css/blog-premium.css">

    <!-- Header Styles -->
    <link rel="stylesheet" href="../css/header-optimized.css">

{get_footer_styles()}
</head>
<body>
    <!-- Reading Progress Bar -->
    <div class="reading-progress" id="progressBar"></div>

    <!-- Header -->
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

            <div class="header-trust">
                <div class="trust-stars">⭐⭐⭐⭐⭐</div>
                <div class="trust-rating">4.9/5</div>
                <div class="trust-reviews">5,200+ Reviews</div>
            </div>

            <div class="header-cta">
                <a href="tel:4377476737" class="cta-phone">
                    <i class="fas fa-phone"></i> (437) 747-6737
                </a>
                <a href="/book" class="cta-book">
                    <i class="fas fa-calendar-check"></i> Book Now
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
        <main class="blog-main">
{get_blog_header()}

            <!-- Blog Content -->
            <article class="blog-content">
{body_content}
            </article>
        </main>

{get_sidebar()}
    </div>

{get_footer()}

    <!-- Scripts -->
    <script>
        window.addEventListener('scroll', function() {{
            const progressBar = document.getElementById('progressBar');
            const windowHeight = window.innerHeight;
            const documentHeight = document.documentElement.scrollHeight - windowHeight;
            const scrolled = (window.scrollY / documentHeight) * 100;
            progressBar.style.width = scrolled + '%';
        }});

        const menuBtn = document.querySelector('.mobile-menu-btn');
        const mainNav = document.getElementById('mainNav');

        if (menuBtn) {{
            menuBtn.addEventListener('click', function() {{
                const isOpen = this.getAttribute('aria-expanded') === 'true';
                this.setAttribute('aria-expanded', !isOpen);
                mainNav.classList.toggle('menu-open');
            }});
        }}
    </script>
</body>
</html>
'''
    return html

def main():
    blog_base = Path("blog")
    folder = "maintenance"
    folder_path = blog_base / folder

    if not folder_path.exists():
        print(f"[ERROR] {folder} folder not found")
        return

    html_files = sorted([f for f in folder_path.glob('*.html')])

    print("\n" + "="*80)
    print(f"CORRECTLY REBUILDING {folder.upper()} POSTS WITH COMPLETE FOOTER STYLES")
    print("="*80 + "\n")

    updated = 0
    errors = 0

    for filepath in html_files:
        filename = filepath.name
        try:
            meta = extract_head_meta(filepath)
            html = rebuild_post(filepath, meta)

            if html:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html)
                print(f"  OK {filename}")
                updated += 1
            else:
                print(f"  SKIP {filename}")
                errors += 1
        except Exception as e:
            print(f"  ERROR {filename}: {str(e)[:50]}")
            errors += 1

    print("\n" + "="*80)
    print(f"Updated: {updated}")
    print(f"Errors: {errors}")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
