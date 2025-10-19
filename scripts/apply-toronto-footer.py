#!/usr/bin/env python3
"""
Apply Toronto-style footer to all pages

Changes:
1. Extract footer from richmond-hill.html (toronto-style footer)
2. Fix review count 520+ → 5,200+
3. Apply correct paths for each page type (index vs subdirectories)
4. Replace JavaScript footer loader on book.html with inline footer
5. Apply to all 48 pages
"""

import re
from pathlib import Path

# Toronto-style footer template (from richmond-hill.html)
FOOTER_TEMPLATE = """    <footer class="seo-footer-premium">
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
                        <li><a href="{path_prefix}services/refrigerator-repair">Refrigerator Repair</a></li>
                        <li><a href="{path_prefix}services/dishwasher-repair">Dishwasher Repair</a></li>
                        <li><a href="{path_prefix}services/washer-repair">Washer Repair</a></li>
                        <li><a href="{path_prefix}services/dryer-repair">Dryer Repair</a></li>
                        <li><a href="{path_prefix}services/oven-repair">Oven Repair</a></li>
                        <li><a href="{path_prefix}services/stove-repair">Stove Repair</a></li>
                        <li><a href="{path_prefix}services/range-repair">Range Repair</a></li>
                        <li><a href="{path_prefix}services/microwave-repair">Microwave Repair</a></li>
                        <li><a href="{path_prefix}services/freezer-repair">Freezer Repair</a></li>
                    </ul>
                </div>

                <!-- Column 2: Top Service Areas -->
                <div class="footer-column">
                    <h4 class="footer-heading">Top Service Areas</h4>
                    <ul class="footer-links">
                        <li><a href="{path_prefix}locations/mississauga">Mississauga</a></li>
                        <li><a href="{path_prefix}locations/brampton">Brampton</a></li>
                        <li><a href="{path_prefix}locations/markham">Markham</a></li>
                        <li><a href="{path_prefix}locations/vaughan">Vaughan</a></li>
                        <li><a href="{path_prefix}locations/richmond-hill">Richmond Hill</a></li>
                        <li><a href="{path_prefix}locations/oakville">Oakville</a></li>
                        <li><a href="{path_prefix}locations/burlington">Burlington</a></li>
                        <li><a href="{path_prefix}locations/oshawa">Oshawa</a></li>
                        <li><a href="{path_prefix}locations/ajax">Ajax</a></li>
                        <li><a href="{path_prefix}locations/pickering">Pickering</a></li>
                        <li><a href="{path_prefix}locations/milton">Milton</a></li>
                        <li><a href="{path_prefix}locations/whitby">Whitby</a></li>
                    </ul>
                </div>

                <!-- Column 3: Company -->
                <div class="footer-column">
                    <h4 class="footer-heading">Company</h4>
                    <ul class="footer-links">
                        <li><a href="{path_prefix}about">About Us</a></li>
                        <li><a href="{path_prefix}#testimonials">Customer Reviews</a></li>
                        <li><a href="{path_prefix}#faq">FAQ</a></li>
                        <li><a href="{path_prefix}book">Book Online</a></li>
                        <li><a href="{path_prefix}#areas">Service Areas</a></li>
                        <li><a href="{path_prefix}privacy">Privacy Policy</a></li>
                        <li><a href="{path_prefix}terms">Terms of Service</a></li>
                        <li><a href="{path_prefix}sitemap.xml">Sitemap</a></li>
                    </ul>
                </div>

                <!-- Column 4: Contact -->
                <div class="footer-column footer-column-contact">
                    <h4 class="footer-heading">Contact Us</h4>
                    <div class="footer-contact-box">
                        <p class="contact-item">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" style="vertical-align: middle; margin-right: 8px;">
                                <path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>
                            </svg>
                            <a href="tel:4377476737" class="contact-link">(437) 747-6737</a>
                        </p>
                        <p class="contact-item">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" style="vertical-align: middle; margin-right: 8px;">
                                <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
                            </svg>
                            <a href="mailto:care@niappliancerepair.ca" class="contact-link">care@niappliancerepair.ca</a>
                        </p>
                        <p class="contact-item">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" style="vertical-align: middle; margin-right: 8px;">
                                <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                            </svg>
                            <span>60 Walter Tunny Cresent<br>East Gwillimbury, ON L9N 0R3</span>
                        </p>
                        <p class="contact-item">
                            <strong>📅 Service Hours:</strong><br>
                            Mon-Fri: 8 AM - 8 PM<br>
                            Sat: 9 AM - 6 PM<br>
                            Sun: 10 AM - 5 PM
                        </p>
                    </div>

                    <!-- Call to Action Button -->
                    <a href="tel:4377476737" class="footer-cta-button">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>
                        </svg>
                        Call Now for Same-Day Service
                    </a>
                </div>
            </div>

            <!-- Footer Bottom -->
            <div class="footer-bottom">
                <div class="footer-bottom-content">
                    <p class="copyright">
                        © <span id="current-year-footer">2025</span> Nika Appliance Repair. All Rights Reserved.
                        <span class="separator">|</span>
                        Licensed & Insured Appliance Repair Company Serving Toronto & GTA
                    </p>
                    <div class="footer-social-links">
                        <span class="footer-tagline">Trusted by 5,200+ Happy Customers</span>
                    </div>
                </div>
            </div>
        </div>
    </footer>

    <style>
    /* ========== SEO-OPTIMIZED FOOTER STYLES ========== */

    .seo-footer-premium {
        position: relative;
        background: linear-gradient(135deg, #1976D2 0%, #2196F3 50%, #1565C0 100%);
        color: #ffffff;
        padding: 4rem 0 2rem;
        overflow: hidden;
    }

    .seo-footer-premium::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background:
            radial-gradient(circle at 20% 50%, rgba(255,255,255,0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255,255,255,0.1) 0%, transparent 50%);
        pointer-events: none;
    }

    .seo-footer-premium .container {
        position: relative;
        z-index: 2;
    }

    /* Trust Badges Row */
    .footer-trust-badges {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin-bottom: 4rem;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .trust-badge-item {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .badge-icon {
        font-size: 2.5rem;
        line-height: 1;
    }

    .badge-text {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }

    .badge-text strong {
        font-size: 1rem;
        font-weight: 700;
        color: #ffffff;
    }

    .badge-text span {
        font-size: 0.875rem;
        color: rgba(255, 255, 255, 0.9);
    }

    /* Main Footer Content */
    .footer-main-content {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 3rem;
        margin-bottom: 3rem;
    }

    .footer-column {
        display: flex;
        flex-direction: column;
    }

    .footer-heading {
        font-size: 1.25rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid rgba(255, 255, 255, 0.3);
    }

    .footer-links {
        list-style: none;
        padding: 0;
        margin: 0;
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .footer-links li {
        line-height: 1.6;
    }

    .footer-links a {
        color: rgba(255, 255, 255, 0.9);
        text-decoration: none;
        font-size: 0.95rem;
        transition: all 0.2s ease;
        display: inline-block;
    }

    .footer-links a:hover {
        color: #ffffff;
        transform: translateX(4px);
    }

    /* Contact Column */
    .footer-column-contact {
        background: rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .footer-contact-box {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }

    .contact-item {
        font-size: 0.95rem;
        line-height: 1.6;
        color: rgba(255, 255, 255, 0.9);
        margin: 0;
    }

    .contact-link {
        color: #ffffff;
        text-decoration: none;
        font-weight: 600;
        transition: opacity 0.2s ease;
    }

    .contact-link:hover {
        opacity: 0.8;
    }

    /* CTA Button */
    .footer-cta-button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        background: #27AE60;
        color: #ffffff;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s ease;
        border: 2px solid #27AE60;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }

    .footer-cta-button:hover {
        background: #229954;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(39, 174, 96, 0.4);
    }

    /* Footer Bottom */
    .footer-bottom {
        padding-top: 2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.2);
    }

    .footer-bottom-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
    }

    .copyright {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.9);
        margin: 0;
    }

    .separator {
        margin: 0 0.5rem;
        opacity: 0.5;
    }

    .footer-social-links {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .footer-tagline {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 600;
    }

    /* Responsive Design */
    @media (max-width: 968px) {
        .seo-footer-premium {
            padding: 3rem 0 1.5rem;
        }

        .footer-trust-badges {
            grid-template-columns: repeat(2, 1fr);
            gap: 1.5rem;
            padding: 1.5rem;
            margin-bottom: 3rem;
        }

        .footer-main-content {
            grid-template-columns: repeat(2, 1fr);
            gap: 2rem;
        }

        .footer-column-contact {
            grid-column: 1 / -1;
        }

        .footer-bottom-content {
            flex-direction: column;
            text-align: center;
        }

        .separator {
            display: none;
        }
    }

    @media (max-width: 768px) {
        .footer-trust-badges {
            grid-template-columns: 1fr;
            gap: 1rem;
        }

        .footer-main-content {
            grid-template-columns: 1fr;
            gap: 2rem;
        }

        .footer-heading {
            font-size: 1.1rem;
        }

        .badge-text strong {
            font-size: 0.95rem;
        }

        .badge-text span {
            font-size: 0.8rem;
        }

        .footer-cta-button {
            width: 100%;
            padding: 0.875rem 1.25rem;
            font-size: 0.95rem;
        }
    }

    @media (max-width: 480px) {
        .seo-footer-premium {
            padding: 2rem 0 1rem;
        }

        .footer-trust-badges {
            margin-bottom: 2rem;
        }

        .badge-icon {
            font-size: 2rem;
        }

        .footer-links a {
            font-size: 0.9rem;
        }

        .contact-item {
            font-size: 0.875rem;
        }
    }

    /* Accessibility */
    @media (prefers-reduced-motion: reduce) {
        .footer-links a,
        .footer-cta-button {
            transition: none;
        }
    }
    </style>

    <script>
    // Set current year in footer
    document.getElementById('current-year-footer').textContent = new Date().getFullYear();
    </script>"""


def get_path_prefix(file_path):
    """Determine path prefix based on file location"""
    # Homepage and listing pages at root
    if file_path.name in ['index.html', 'services.html', 'locations.html', 'book.html']:
        return ''
    # Subdirectory pages (services/, locations/, brands/)
    else:
        return '../'


def replace_footer(file_path):
    """Replace existing footer with Toronto-style footer"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Determine path prefix
    path_prefix = get_path_prefix(file_path)

    # Generate footer with correct paths using str.replace (not .format to avoid CSS {} issues)
    footer_with_paths = FOOTER_TEMPLATE.replace('{path_prefix}', path_prefix)

    # Pattern 1: Match existing inline footer (most pages)
    # Find from <footer to </script> that contains current-year-footer
    footer_pattern = r"<footer class=\"seo-footer-premium\">.*?document\.getElementById\('current-year-footer'\).*?</script>"

    if re.search(footer_pattern, content, re.DOTALL):
        content = re.sub(footer_pattern, footer_with_paths.strip(), content, flags=re.DOTALL)
        changed = True
    else:
        # Pattern 2: For book.html - replace JavaScript footer loader
        # Match: <div id="footer-placeholder"></div> ... fetch footer script
        book_footer_pattern = r'<!-- Footer Placeholder -->.*?<div id="footer-placeholder"></div>.*?fetch\(\'/includes/footer\.html\'\).*?\.catch\(error => console\.error\(\'Error loading footer:\', error\)\);'

        if re.search(book_footer_pattern, content, re.DOTALL):
            # Insert footer before closing body tag
            # First remove the placeholder and loader
            content = re.sub(book_footer_pattern, '', content, flags=re.DOTALL)

            # Insert footer before closing body tag
            body_close_pattern = r'(</body>)'
            footer_insertion = f'\n{footer_with_paths}\n\\1'
            content = re.sub(body_close_pattern, footer_insertion, content)
            changed = True
        else:
            changed = False

    if content != original and changed:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    return False


def main():
    base_dir = Path('C:/NikaApplianceRepair')

    pages = []

    # Homepage
    pages.append(base_dir / 'index.html')

    # Book page (special case - has JavaScript loader)
    pages.append(base_dir / 'book.html')

    # Service pages (9)
    services = ['refrigerator-repair', 'dishwasher-repair', 'washer-repair', 'dryer-repair',
                'oven-repair', 'stove-repair', 'range-repair', 'microwave-repair', 'freezer-repair']
    for service in services:
        pages.append(base_dir / 'services' / f'{service}.html')

    # Location pages (20)
    locations = ['richmond-hill', 'mississauga', 'brampton', 'markham', 'vaughan',
                 'oakville', 'milton', 'burlington', 'ajax', 'pickering',
                 'whitby', 'oshawa', 'aurora', 'newmarket', 'etobicoke',
                 'north-york', 'scarborough', 'caledon', 'east-gwillimbury', 'halton-hills']
    for location in locations:
        pages.append(base_dir / 'locations' / f'{location}.html')

    # Brand pages (15)
    brands = ['samsung', 'lg', 'whirlpool', 'ge', 'bosch',
              'kitchenaid', 'maytag', 'frigidaire', 'electrolux', 'kenmore',
              'miele', 'fisher-paykel', 'amana', 'hotpoint', 'danby']
    for brand in brands:
        pages.append(base_dir / 'brands' / f'{brand}-appliance-repair-toronto.html')

    # Listing pages
    pages.append(base_dir / 'services.html')
    pages.append(base_dir / 'locations.html')

    print('='*70)
    print('APPLYING TORONTO-STYLE FOOTER TO ALL PAGES')
    print('='*70)
    print()
    print('Changes:')
    print('  1. Toronto-style footer structure')
    print('  2. Review count: 5,200+ (fixed from 520+)')
    print('  3. Correct paths for each page type')
    print('  4. Fix book.html (inline footer instead of JS loader)')
    print()
    print('='*70)
    print()

    updated = 0
    skipped = 0

    for page in pages:
        if page.exists():
            print(f'Processing: {page.name}...', end=' ')
            if replace_footer(page):
                print('[UPDATED]')
                updated += 1
            else:
                print('[SKIP - no footer found]')
                skipped += 1
        else:
            print(f'[WARN] Not found: {page}')

    print()
    print('='*70)
    print(f'COMPLETE!')
    print(f'  Updated: {updated} pages')
    print(f'  Skipped: {skipped} pages')
    print('='*70)


if __name__ == '__main__':
    main()
