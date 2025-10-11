#!/usr/bin/env python3
"""
Service Pages Generator - Based on index.html
Creates 11 technically optimized pages with placeholder content
"""

from pathlib import Path
import re


# Appliance types configuration
APPLIANCES = {
    "refrigerator": {
        "name": "Refrigerator",
        "icon_class": "icon-1",  # Use existing fridge icon from index.html
        "meta_keywords": "refrigerator repair, fridge repair, appliance repair"
    },
    "dishwasher": {
        "name": "Dishwasher",
        "icon_class": "icon-3",
        "meta_keywords": "dishwasher repair, appliance repair"
    },
    "washer": {
        "name": "Washing Machine",
        "icon_class": "icon-6",
        "meta_keywords": "washing machine repair, washer repair, appliance repair"
    },
    "dryer": {
        "name": "Dryer",
        "icon_class": "icon-4",
        "meta_keywords": "dryer repair, appliance repair"
    },
    "stove": {
        "name": "Stove",
        "icon_class": "icon-5",
        "meta_keywords": "stove repair, cooktop repair, appliance repair"
    },
    "oven": {
        "name": "Oven",
        "icon_class": "icon-6",
        "meta_keywords": "oven repair, appliance repair"
    },
    "range": {
        "name": "Range",
        "icon_class": "icon-5",
        "meta_keywords": "range repair, appliance repair"
    },
    "microwave": {
        "name": "Microwave",
        "icon_class": "icon-2",
        "meta_keywords": "microwave repair, appliance repair"
    },
    "freezer": {
        "name": "Freezer",
        "icon_class": "icon-1",
        "meta_keywords": "freezer repair, appliance repair"
    },
    "ice-maker": {
        "name": "Ice Maker",
        "icon_class": "icon-1",
        "meta_keywords": "ice maker repair, appliance repair"
    },
    "garbage-disposal": {
        "name": "Garbage Disposal",
        "icon_class": "icon-3",
        "meta_keywords": "garbage disposal repair, appliance repair"
    }
}


def generate_service_page(appliance_slug, appliance_data, template_content):
    """Generate a service page for specific appliance"""

    appliance_name = appliance_data["name"]
    content = template_content

    # 1. Update meta tags
    content = re.sub(
        r'<title>.*?</title>',
        f'<title>{appliance_name} Repair Toronto | Same-Day Service | Nika</title>',
        content
    )

    content = re.sub(
        r'<meta name="description" content=".*?">',
        f'<meta name="description" content="{{{{PLACEHOLDER_META_DESCRIPTION}}}} Expert {appliance_name.lower()} repair in Toronto. Same-day service, 90-day warranty. Call 437-747-6737">',
        content
    )

    content = re.sub(
        r'<meta name="keywords" content=".*?">',
        f'<meta name="keywords" content="{appliance_data["meta_keywords"]}, Toronto, same-day service">',
        content
    )

    # Update OG tags
    content = re.sub(
        r'<meta property="og:title" content=".*?">',
        f'<meta property="og:title" content="{appliance_name} Repair Toronto | Same-Day Service | Nika">',
        content,
        flags=re.IGNORECASE
    )

    content = re.sub(
        r'<meta property="og:url" content=".*?">',
        f'<meta property="og:url" content="https://www.nikaappliancerepair.com/services/{appliance_slug}-repair.html">',
        content,
        flags=re.IGNORECASE
    )

    # Add canonical link and Schema markup
    schema_markup = f'''
    <link rel="canonical" href="https://www.nikaappliancerepair.com/services/{appliance_slug}-repair.html">

    <!-- Schema.org Markup -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "Nika Appliance Repair - {appliance_name} Repair",
        "image": "https://www.nikaappliancerepair.com/assets/images/friendly-technician-character.png",
        "telephone": "4377476737",
        "email": "care@niappliancerepair.ca",
        "address": {{
            "@type": "PostalAddress",
            "streetAddress": "60 Walter Tunny Cresent",
            "addressLocality": "East Gwillimbury",
            "addressRegion": "ON",
            "postalCode": "L9N 0R3",
            "addressCountry": "CA"
        }},
        "geo": {{
            "@type": "GeoCoordinates",
            "latitude": "44.0389",
            "longitude": "-79.4537"
        }},
        "url": "https://www.nikaappliancerepair.com/services/{appliance_slug}-repair.html",
        "priceRange": "$$",
        "aggregateRating": {{
            "@type": "AggregateRating",
            "ratingValue": "4.9",
            "reviewCount": "5200",
            "bestRating": "5",
            "worstRating": "1"
        }},
        "areaServed": {{
            "@type": "GeoCircle",
            "geoMidpoint": {{
                "@type": "GeoCoordinates",
                "latitude": "43.6532",
                "longitude": "-79.3832"
            }},
            "geoRadius": "50000"
        }},
        "openingHoursSpecification": [
            {{
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                "opens": "08:00",
                "closes": "20:00"
            }},
            {{
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": "Saturday",
                "opens": "09:00",
                "closes": "18:00"
            }},
            {{
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": "Sunday",
                "opens": "10:00",
                "closes": "17:00"
            }}
        ]
    }}
    </script>

    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": "{appliance_name} Repair",
        "provider": {{
            "@type": "LocalBusiness",
            "name": "Nika Appliance Repair"
        }},
        "areaServed": "Toronto, ON",
        "hasOfferCatalog": {{
            "@type": "OfferCatalog",
            "name": "{appliance_name} Repair Services",
            "itemListElement": [
                {{
                    "@type": "Offer",
                    "itemOffered": {{
                        "@type": "Service",
                        "name": "Diagnostic Service",
                        "description": "Professional diagnostic service for {appliance_name.lower()}"
                    }},
                    "priceSpecification": {{
                        "@type": "PriceSpecification",
                        "priceCurrency": "CAD",
                        "price": "80-150"
                    }}
                }},
                {{
                    "@type": "Offer",
                    "itemOffered": {{
                        "@type": "Service",
                        "name": "Repair Service",
                        "description": "Complete repair service for {appliance_name.lower()}"
                    }},
                    "priceSpecification": {{
                        "@type": "PriceSpecification",
                        "priceCurrency": "CAD",
                        "price": "150-450"
                    }}
                }}
            ]
        }}
    }}
    </script>'''

    if '<link rel="stylesheet" href="css/style.css">' in content:
        content = content.replace(
            '<link rel="stylesheet" href="css/style.css">',
            schema_markup + '\n    <link rel="stylesheet" href="../css/style.css">'
        )

    # Fix CSS paths (services subdirectory)
    content = re.sub(r'href="css/', 'href="../css/', content)
    content = re.sub(r'src="assets/', 'src="../assets/', content)
    content = re.sub(r'src="js/', 'src="../js/', content)

    # 2. Update Hero Section
    hero_pattern = r'(<h1 class="hero-title">)(.*?)(</h1>)'
    hero_replacement = r'\1{{PLACEHOLDER_H1_HERO_TITLE}}\3'
    content = re.sub(hero_pattern, hero_replacement, content, flags=re.DOTALL)

    # Update hero subtitle
    content = re.sub(
        r'<p class="hero-subtitle">.*?</p>',
        f'<p class="hero-subtitle">⭐ 4.9/5 rating • 5,200+ reviews • Same-day service • 90-day warranty</p>',
        content,
        flags=re.DOTALL
    )

    # 3. Update Countdown section
    content = re.sub(
        r'<h2 class="countdown-title">.*?</h2>',
        f'<h2 class="countdown-title">Book Online & Save $40 on {appliance_name} Repair</h2>',
        content
    )

    # 4. Replace Services Section with Common Problems Section
    services_section_pattern = r'<!-- Services Section -->.*?</section>'

    problems_section = f'''<!-- Common Problems Section -->
    <section class="services-section" id="problems">
        <div class="container">
            <h2 class="section-title">Common {appliance_name} Problems We Fix</h2>
            <p class="section-subtitle">{{{{PLACEHOLDER_PROBLEMS_INTRO}}}}</p>
            <div class="services-grid">
                <div class="service-card">
                    <div class="service-icon">⚠️</div>
                    <h3>{{{{PLACEHOLDER_PROBLEM_1_TITLE}}}}</h3>
                    <p>{{{{PLACEHOLDER_PROBLEM_1_DESC}}}}</p>
                </div>
                <div class="service-card">
                    <div class="service-icon">⚠️</div>
                    <h3>{{{{PLACEHOLDER_PROBLEM_2_TITLE}}}}</h3>
                    <p>{{{{PLACEHOLDER_PROBLEM_2_DESC}}}}</p>
                </div>
                <div class="service-card">
                    <div class="service-icon">⚠️</div>
                    <h3>{{{{PLACEHOLDER_PROBLEM_3_TITLE}}}}</h3>
                    <p>{{{{PLACEHOLDER_PROBLEM_3_DESC}}}}</p>
                </div>
                <div class="service-card">
                    <div class="service-icon">⚠️</div>
                    <h3>{{{{PLACEHOLDER_PROBLEM_4_TITLE}}}}</h3>
                    <p>{{{{PLACEHOLDER_PROBLEM_4_DESC}}}}</p>
                </div>
                <div class="service-card">
                    <div class="service-icon">⚠️</div>
                    <h3>{{{{PLACEHOLDER_PROBLEM_5_TITLE}}}}</h3>
                    <p>{{{{PLACEHOLDER_PROBLEM_5_DESC}}}}</p>
                </div>
                <div class="service-card">
                    <div class="service-icon">⚠️</div>
                    <h3>{{{{PLACEHOLDER_PROBLEM_6_TITLE}}}}</h3>
                    <p>{{{{PLACEHOLDER_PROBLEM_6_DESC}}}}</p>
                </div>
            </div>
            <div class="services-cta">
                <a href="#book" class="cta-primary">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
                        <path d="M9 11H7v2h2v-2zm4 0h-2v2h2v-2zm4 0h-2v2h2v-2zm2-7h-1V2h-2v2H8V2H6v2H5c-1.11 0-1.99.9-1.99 2L3 20c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 16H5V9h14v11z"/>
                    </svg>
                    BOOK SERVICE NOW
                </a>
                <a href="tel:4377476737" class="cta-secondary">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
                        <path d="M20.01 15.38c-1.23 0-2.42-.2-3.53-.56a.977.977 0 00-1.01.24l-1.57 1.97c-2.83-1.35-5.48-3.9-6.89-6.83l1.95-1.66c.27-.28.35-.67.24-1.02-.37-1.11-.56-2.3-.56-3.53 0-.54-.45-.99-.99-.99H4.19C3.65 3 3 3.24 3 3.99 3 13.28 10.73 21 20.01 21c.71 0 .99-.63.99-1.18v-3.45c0-.54-.45-.99-.99-.99z"/>
                    </svg>
                    CALL NOW: 437-747-6737
                </a>
            </div>
        </div>
    </section>'''

    content = re.sub(services_section_pattern, problems_section, content, flags=re.DOTALL)

    # 5. Update Why Choose Us section
    content = re.sub(
        r'<h2 class="section-title-light">Why Our <span class="highlight-yellow">Appliance Repair Service</span> Is Better</h2>',
        f'<h2 class="section-title-light">Why Choose Nika for <span class="highlight-yellow">{appliance_name} Repair</span></h2>',
        content
    )

    # 6. Add Pricing Table Section (after Why Choose Us, before About)
    pricing_section = f'''
    <!-- Pricing Table Section -->
    <section class="pricing-section" style="padding: 60px 0; background: #f8fafc;">
        <div class="container">
            <h2 class="section-title">Transparent Pricing</h2>
            <p class="section-subtitle">No hidden fees, no surprises</p>
            <div style="margin: 40px 0; overflow-x: auto; background: white; padding: 20px; border-radius: 12px; text-align: center;">
                <table class="pricing-table" style="max-width: 800px; margin: 0 auto; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden;">
                    <thead>
                        <tr style="background: #1e40af; color: white;">
                            <th style="padding: 15px; text-align: center;">Service Type</th>
                            <th style="padding: 15px; text-align: center;">Typical Cost Range</th>
                            <th style="padding: 15px; text-align: center;">Warranty</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="border-bottom: 1px solid #e2e8f0;">
                            <td style="padding: 15px; text-align: center;">Diagnostic Fee</td>
                            <td style="padding: 15px; text-align: center;">$80-$150 (Waived if repaired)</td>
                            <td style="padding: 15px; text-align: center;">N/A</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #e2e8f0;">
                            <td style="padding: 15px; text-align: center;">Basic Repair</td>
                            <td style="padding: 15px; text-align: center;">$150 - $250</td>
                            <td style="padding: 15px; text-align: center;">90 Days</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #e2e8f0;">
                            <td style="padding: 15px; text-align: center;">Complex Repair</td>
                            <td style="padding: 15px; text-align: center;">$250 - $450</td>
                            <td style="padding: 15px; text-align: center;">90 Days</td>
                        </tr>
                        <tr>
                            <td style="padding: 15px; text-align: center;">Emergency Service</td>
                            <td style="padding: 15px; text-align: center;">+$50 - $100</td>
                            <td style="padding: 15px; text-align: center;">90 Days</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </section>

    <!-- Service Details Section -->
    <section class="service-details-section" style="padding: 60px 0; background: white;">
        <div class="container">
            <h2 class="section-title">Our {appliance_name} Repair Process</h2>
            <div style="max-width: 900px; margin: 0 auto; font-size: 1.1rem; line-height: 1.8; color: #334155;">
                <p style="margin-bottom: 20px;">{{{{PLACEHOLDER_SERVICE_DETAIL_P1}}}}</p>
                <p style="margin-bottom: 20px;">{{{{PLACEHOLDER_SERVICE_DETAIL_P2}}}}</p>
                <p style="margin-bottom: 20px;">{{{{PLACEHOLDER_SERVICE_DETAIL_P3}}}}</p>
                <p style="margin-bottom: 20px;">{{{{PLACEHOLDER_SERVICE_DETAIL_P4}}}}</p>
            </div>
        </div>
    </section>
'''

    # Insert before About Section
    content = re.sub(
        r'(<!-- About Section -->)',
        pricing_section + r'\1',
        content
    )

    # 7. Update About Section title
    content = re.sub(
        r'<h2 class="section-title">About Nick\'s Appliance Repair</h2>',
        f'<h2 class="section-title">About Our {appliance_name} Repair Service</h2>',
        content
    )

    # 8. Update FAQ Section
    faq_section = f'''<!-- FAQ Section -->
    <section class="faq-section">
        <div class="container">
            <h2 class="section-title">Frequently Asked Questions - {appliance_name} Repair</h2>

            <div class="faq-grid">
                <div class="faq-item">
                    <button class="faq-question">
                        <span>{{{{PLACEHOLDER_FAQ_1_Q}}}}</span>
                        <span class="faq-icon">+</span>
                    </button>
                    <div class="faq-answer">
                        <p>{{{{PLACEHOLDER_FAQ_1_A}}}}</p>
                    </div>
                </div>

                <div class="faq-item">
                    <button class="faq-question">
                        <span>{{{{PLACEHOLDER_FAQ_2_Q}}}}</span>
                        <span class="faq-icon">+</span>
                    </button>
                    <div class="faq-answer">
                        <p>{{{{PLACEHOLDER_FAQ_2_A}}}}</p>
                    </div>
                </div>

                <div class="faq-item">
                    <button class="faq-question">
                        <span>{{{{PLACEHOLDER_FAQ_3_Q}}}}</span>
                        <span class="faq-icon">+</span>
                    </button>
                    <div class="faq-answer">
                        <p>{{{{PLACEHOLDER_FAQ_3_A}}}}</p>
                    </div>
                </div>

                <div class="faq-item">
                    <button class="faq-question">
                        <span>{{{{PLACEHOLDER_FAQ_4_Q}}}}</span>
                        <span class="faq-icon">+</span>
                    </button>
                    <div class="faq-answer">
                        <p>{{{{PLACEHOLDER_FAQ_4_A}}}}</p>
                    </div>
                </div>

                <div class="faq-item">
                    <button class="faq-question">
                        <span>{{{{PLACEHOLDER_FAQ_5_Q}}}}</span>
                        <span class="faq-icon">+</span>
                    </button>
                    <div class="faq-answer">
                        <p>{{{{PLACEHOLDER_FAQ_5_A}}}}</p>
                    </div>
                </div>

                <div class="faq-item">
                    <button class="faq-question">
                        <span>{{{{PLACEHOLDER_FAQ_6_Q}}}}</span>
                        <span class="faq-icon">+</span>
                    </button>
                    <div class="faq-answer">
                        <p>{{{{PLACEHOLDER_FAQ_6_A}}}}</p>
                    </div>
                </div>

                <div class="faq-item">
                    <button class="faq-question">
                        <span>{{{{PLACEHOLDER_FAQ_7_Q}}}}</span>
                        <span class="faq-icon">+</span>
                    </button>
                    <div class="faq-answer">
                        <p>{{{{PLACEHOLDER_FAQ_7_A}}}}</p>
                    </div>
                </div>

                <div class="faq-item">
                    <button class="faq-question">
                        <span>{{{{PLACEHOLDER_FAQ_8_Q}}}}</span>
                        <span class="faq-icon">+</span>
                    </button>
                    <div class="faq-answer">
                        <p>{{{{PLACEHOLDER_FAQ_8_A}}}}</p>
                    </div>
                </div>
            </div>
        </div>
    </section>'''

    content = re.sub(
        r'<!-- FAQ Section -->.*?</section>',
        faq_section,
        content,
        flags=re.DOTALL
    )

    return content


def main():
    """Generate all 11 service pages"""
    print("\n" + "=" * 70)
    print("SERVICE PAGES GENERATOR - STAGE 1")
    print("=" * 70 + "\n")

    # Load index.html template
    template_path = Path("index.html")
    if not template_path.exists():
        print("[ERROR] index.html not found in root directory")
        return

    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    print("[OK] Loaded index.html template\n")

    # Create services directory if not exists
    services_dir = Path("services")
    services_dir.mkdir(exist_ok=True)

    # Generate each service page
    for appliance_slug, appliance_data in APPLIANCES.items():
        output_file = services_dir / f"{appliance_slug}-repair.html"

        print(f"[GENERATING] {appliance_data['name']}...")

        page_content = generate_service_page(
            appliance_slug,
            appliance_data,
            template_content
        )

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(page_content)

        print(f"[OK] Created: {output_file}\n")

    print("=" * 70)
    print(f"[SUCCESS] Generated {len(APPLIANCES)} service pages")
    print("=" * 70)
    print("\nAll pages have:")
    print("✓ Technical SEO optimization")
    print("✓ Countdown timer")
    print("✓ 5 video testimonials")
    print("✓ Common Problems grid (6 cards)")
    print("✓ Pricing table (centered)")
    print("✓ Service Details (4 paragraphs)")
    print("✓ FAQ section (8 questions)")
    print("✓ All 6 floating icons")
    print("\nReady for STAGE 2: Manual content writing")


if __name__ == "__main__":
    main()
