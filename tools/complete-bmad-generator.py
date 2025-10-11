"""
Complete BMAD Page Generator with ALL 13 Sections from index.html
Creates service and location pages with full design and all sections
"""

import os
import sys

# Import extracted sections
script_dir = os.path.dirname(os.path.abspath(__file__))
extracted_sections_path = os.path.join(script_dir, 'extracted-sections.py')
exec(open(extracted_sections_path, 'r', encoding='utf-8').read())

GLOBAL_DATA = {
    "phone": "437-747-6737",
    "phone_href": "tel:4377476737",
    "warranty": "90-day",
    "diagnostic_fee": "$119",
    "diagnostic_note": "(waived with repair)",
    "repair_range": "$120-240",
    "service_hours": "Monday-Friday 8AM-6PM, Saturday 9AM-5PM",
    "rating": "4.9★",
    "review_count": "127",
    "years_experience": "5+",
    "completion_count": "5,200+"
}

# Service configurations
SERVICES = {
    "dishwasher-repair": {
        "name": "Dishwasher Repair",
        "keyword": "dishwasher repair",
        "description": "Professional dishwasher repair service"
    },
    "refrigerator-freezer-repair": {
        "name": "Refrigerator & Freezer Repair",
        "keyword": "refrigerator repair",
        "description": "Expert refrigerator and freezer repair"
    },
    "washer-dryer-repair": {
        "name": "Washer & Dryer Repair",
        "keyword": "washer repair",
        "description": "Professional washer and dryer repair"
    },
    "oven-stove-repair": {
        "name": "Oven & Stove Repair",
        "keyword": "oven repair",
        "description": "Expert oven and stove repair service"
    },
    "dishwasher-installation": {
        "name": "Dishwasher Installation",
        "keyword": "dishwasher installation",
        "description": "Professional dishwasher installation service"
    }
}

# All CSS files from index.html
CSS_FILES = [
    "css/style.css",
    "css/video-custom.css",
    "css/video-modern.css",
    "css/how-it-works-modern.css",
    "css/about-redesign.css",
    "css/mobile-responsive.css",
    "css/floating-icons-fix.css",
    "css/centering-fixes.css",
    "css/section-centering-override.css",
    "css/countdown-horizontal.css",
    "css/mobile-fixes-priority.css",
    "css/mobile-layout-critical.css",
    "css/correct-button-colors.css"
]


def create_service_page_header(service_name, keyword):
    """Create HTML head with all CSS and meta tags"""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Expert {keyword} in Toronto GTA - Same-day service, 90-day warranty, all brands. Call 437-747-6737 for fast reliable {keyword} from licensed technicians.">
    <meta name="keywords" content="{keyword}, {keyword} Toronto, appliance repair, Toronto appliance repair, GTA {keyword}">
    <title>{service_name} Toronto GTA | Same Day | 90-Day Warranty - Nika</title>

    <!-- Google Fonts - EXACT same as index.html -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;500;600;700&family=Rubik:wght@300;400;500;600;700&display=swap" rel="stylesheet">

    <!-- ALL CSS FILES from index.html -->
    {''.join([f'<link rel="stylesheet" href="../{css_file}">' for css_file in CSS_FILES])}

    <!-- Schema Markup -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Service",
        "name": "{service_name}",
        "provider": {{
            "@type": "LocalBusiness",
            "name": "Nika Appliance Repair",
            "telephone": "{GLOBAL_DATA['phone']}",
            "address": {{
                "@type": "PostalAddress",
                "addressRegion": "ON",
                "addressCountry": "CA"
            }},
            "priceRange": "$$",
            "aggregateRating": {{
                "@type": "AggregateRating",
                "ratingValue": "4.9",
                "reviewCount": "127"
            }}
        }},
        "areaServed": ["Toronto", "Mississauga", "Brampton", "Vaughan", "Markham", "Richmond Hill", "Etobicoke", "Scarborough", "North York"]
    }}
    </script>

    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {{
                "@type": "Question",
                "name": "How quickly can you come for {keyword}?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "We offer same-day {keyword} service when our schedule permits. Call {GLOBAL_DATA['phone']} for our earliest available time slot in the GTA."
                }}
            }},
            {{
                "@type": "Question",
                "name": "How much does {keyword} cost?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "We charge {GLOBAL_DATA['diagnostic_fee']} for diagnosis {GLOBAL_DATA['diagnostic_note']}. Most {keyword} repairs cost {GLOBAL_DATA['repair_range']} plus parts with upfront pricing."
                }}
            }},
            {{
                "@type": "Question",
                "name": "Do you offer a warranty on {keyword} repairs?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "Yes! All {keyword} repairs come with our comprehensive {GLOBAL_DATA['warranty']} warranty covering both parts and labor."
                }}
            }}
        ]
    }}
    </script>
</head>
<body>'''


def create_header():
    """Create header navigation - EXACT from index.html"""
    return f'''
    <!-- Header - EXACT SAME AS INDEX.HTML -->
    <header class="main-header">
        <div class="container">
            <div class="header-content">
                <div class="logo">
                    <a href="../index.html">
                        <div class="logo-text">
                            <span class="logo-primary">NIKA</span>
                            <span class="logo-secondary">Appliance Repair</span>
                        </div>
                    </a>
                </div>
                <nav class="main-nav">
                    <ul>
                        <li><a href="../index.html#services">Services</a></li>
                        <li><a href="../index.html#about">About</a></li>
                        <li><a href="../index.html#areas">Areas</a></li>
                        <li class="has-dropdown">
                            <a href="#brands">Brands</a>
                            <ul class="dropdown-menu">
                                <li><a href="../brands/lg-appliance-repair-toronto.html">LG</a></li>
                                <li><a href="../brands/samsung-appliance-repair.html">Samsung</a></li>
                                <li><a href="../brands/whirlpool-appliance-repair.html">Whirlpool</a></li>
                                <li><a href="../brands/ge-appliance-repair.html">GE</a></li>
                            </ul>
                        </li>
                        <li><a href="../index.html#contact">Contact</a></li>
                    </ul>
                </nav>
                <div class="header-cta">
                    <a href="{GLOBAL_DATA['phone_href']}" class="call-btn">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
                            <path d="M20.01 15.38c-1.23 0-2.42-.2-3.53-.56a.977.977 0 00-1.01.24l-1.57 1.97c-2.83-1.35-5.48-3.9-6.89-6.83l1.95-1.66c.27-.28.35-.67.24-1.02-.37-1.11-.56-2.3-.56-3.53 0-.54-.45-.99-.99-.99H4.19C3.65 3 3 3.24 3 3.99 3 13.28 10.73 21 20.01 21c.71 0 .99-.63.99-1.18v-3.45c0-.54-.45-.99-.99-.99z"/>
                        </svg>
                        {GLOBAL_DATA['phone']}
                    </a>
                    <a href="#book" class="book-btn">Book Service</a>
                </div>
                <button class="mobile-menu-toggle">
                    <span></span>
                    <span></span>
                    <span></span>
                </button>
            </div>
        </div>
    </header>'''


def create_footer():
    """Create footer - EXACT from index.html"""
    return f'''
    <!-- Footer - EXACT SAME AS INDEX.HTML -->
    <footer class="main-footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-column">
                    <h4>Services</h4>
                    <ul>
                        <li><a href="../services/dishwasher-repair.html">Dishwasher Repair</a></li>
                        <li><a href="../services/refrigerator-freezer-repair.html">Refrigerator Repair</a></li>
                        <li><a href="../services/washer-dryer-repair.html">Washer & Dryer Repair</a></li>
                        <li><a href="../services/oven-stove-repair.html">Oven & Stove Repair</a></li>
                        <li><a href="../services/dishwasher-installation.html">Dishwasher Installation</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h4>Areas Served</h4>
                    <ul>
                        <li><a href="../locations/toronto.html">Toronto</a></li>
                        <li><a href="../locations/mississauga.html">Mississauga</a></li>
                        <li><a href="../locations/brampton.html">Brampton</a></li>
                        <li><a href="../locations/vaughan.html">Vaughan</a></li>
                        <li><a href="../locations/markham.html">Markham</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h4>Contact</h4>
                    <ul>
                        <li>Phone: {GLOBAL_DATA['phone']}</li>
                        <li>Hours: {GLOBAL_DATA['service_hours']}</li>
                        <li>Rating: {GLOBAL_DATA['rating']} ({GLOBAL_DATA['review_count']} reviews)</li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 Nika Appliance Repair. All rights reserved. Licensed & Insured.</p>
            </div>
        </div>
    </footer>

    <!-- Mobile Menu Toggle Script -->
    <script>
        document.querySelector('.mobile-menu-toggle').addEventListener('click', function() {{
            document.querySelector('.main-nav').classList.toggle('active');
        }});
    </script>
</body>
</html>'''


def adapt_hero_for_service(service_name):
    """Adapt hero section for service page"""
    hero = SECTION_1.replace(
        "<h1>",
        f'<h1>Professional <span class="highlight-yellow">{service_name}</span> in GTA - '
    )
    return hero


def create_service_page(slug):
    """Create complete service page with ALL 13 sections"""
    config = SERVICES[slug]
    service_name = config["name"]
    keyword = config["keyword"]

    # Build complete page
    html = create_service_page_header(service_name, keyword)
    html += create_header()

    # Add all 13 sections (using extracted sections from index.html)
    # Section 1: Hero
    html += adapt_hero_for_service(service_name)

    # Section 2: Countdown (first)
    html += SECTION_2

    # Section 3: Services
    html += SECTION_3

    # Section 4: Why Choose
    html += SECTION_4

    # Section 5: About
    html += SECTION_5

    # Section 6: Countdown (second)
    html += SECTION_6

    # Section 7: Brands
    html += SECTION_7

    # Section 8: Testimonials
    html += SECTION_8

    # Section 9: Areas
    html += SECTION_9

    # Section 10: Property Managers
    html += SECTION_10

    # Section 11: Booking
    html += SECTION_11

    # Section 12: How It Works
    html += SECTION_12

    # Section 13: FAQ
    html += SECTION_13

    html += create_footer()

    return html


def main():
    """Generate all service pages with complete design"""
    print("=" * 60)
    print("COMPLETE BMAD GENERATOR - ALL 13 SECTIONS")
    print("=" * 60)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    services_dir = os.path.join(project_root, "services")

    if not os.path.exists(services_dir):
        os.makedirs(services_dir)

    for slug in SERVICES.keys():
        html = create_service_page(slug)
        filepath = os.path.join(services_dir, f"{slug}.html")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"[OK] {filepath}")

    print()
    print(f"[SUCCESS] Generated {len(SERVICES)} pages with ALL 13 sections")
    print()
    print("SECTIONS INCLUDED:")
    print("1. Hero Section (with floating icons)")
    print("2. Countdown Section (first)")
    print("3. Services Grid")
    print("4. Why Choose Us")
    print("5. About Section")
    print("6. Countdown Section (second)")
    print("7. Brands Section")
    print("8. Testimonials")
    print("9. Service Areas")
    print("10. Property Managers")
    print("11. Booking Form")
    print("12. How It Works")
    print("13. FAQ Section")
    print()
    print("Ready for complete BMAD testing!")


if __name__ == "__main__":
    main()
