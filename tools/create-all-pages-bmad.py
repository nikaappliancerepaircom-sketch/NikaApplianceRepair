"""
BMAD Page Generator for Nika Appliance Repair
Creates all service and location pages with consistent design and tests with 277 BMAD parameters
"""

import os
import json
from datetime import datetime

# Global consistency data - CRITICAL: These must match everywhere
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

# Service pages configuration
SERVICES = [
    {
        "slug": "dishwasher-repair",
        "title": "Dishwasher Repair Toronto",
        "h1": "Professional Dishwasher Repair in Toronto & GTA",
        "service_name": "Dishwasher Repair",
        "description": "Expert dishwasher repair for all brands in Toronto. Same-day service • 90-day warranty • Licensed technicians. Call 437-747-6737 for fast, reliable repairs!",
        "keywords": "dishwasher repair Toronto, dishwasher repair near me, fix dishwasher, dishwasher not draining",
        "icon": "dishwasher",
        "problems": [
            "Not draining properly",
            "Water leaking from bottom",
            "Dishes not getting clean",
            "Strange grinding noises",
            "Door won't latch properly",
            "Control panel not responding"
        ],
        "content_intro": "When your dishwasher breaks down, dirty dishes pile up fast. Our licensed technicians in Toronto fix all dishwasher brands same-day when available. From drainage issues to control panel failures, we diagnose and repair the problem right the first time with a 90-day warranty.",
    },
    {
        "slug": "refrigerator-freezer-repair",
        "title": "Refrigerator & Freezer Repair Toronto",
        "h1": "Fast Refrigerator & Freezer Repair in Toronto & GTA",
        "service_name": "Refrigerator & Freezer Repair",
        "description": "Emergency fridge repair in Toronto. Same-day service for refrigerators not cooling, freezer issues, ice maker problems. 90-day warranty. Call 437-747-6737 now!",
        "keywords": "refrigerator repair Toronto, fridge repair near me, freezer not working, fridge not cooling",
        "icon": "refrigerator",
        "problems": [
            "Not cooling or freezing properly",
            "Ice maker not working",
            "Water leaking inside or outside",
            "Loud running or strange noises",
            "Temperature fluctuating",
            "Frost buildup in freezer"
        ],
        "content_intro": "A broken refrigerator is an emergency - your food is at risk. Our Toronto technicians prioritize fridge repairs with same-day service when available. We fix all brands of refrigerators and freezers, from cooling issues to ice maker problems, with a comprehensive 90-day warranty.",
    },
    {
        "slug": "washer-dryer-repair",
        "title": "Washer & Dryer Repair Toronto",
        "h1": "Expert Washer & Dryer Repair in Toronto & GTA",
        "service_name": "Washer & Dryer Repair",
        "description": "Professional washer and dryer repair in Toronto. Fix washing machines not spinning, dryers not heating. Same-day service • 90-day warranty. Call 437-747-6737!",
        "keywords": "washer repair Toronto, dryer repair near me, washing machine not spinning, dryer not heating",
        "icon": "washer",
        "problems": [
            "Washer not spinning or draining",
            "Dryer not heating properly",
            "Excessive vibration or shaking",
            "Clothes still wet after cycle",
            "Strange burning smell from dryer",
            "Door won't lock or seal"
        ],
        "content_intro": "Laundry piling up because your washer or dryer stopped working? Our Toronto technicians repair all brands of washers and dryers. Whether your washer won't spin or your dryer won't heat, we'll diagnose and fix it fast with same-day service when available and a 90-day warranty.",
    },
    {
        "slug": "oven-stove-repair",
        "title": "Oven & Stove Repair Toronto",
        "h1": "Professional Oven & Stove Repair in Toronto & GTA",
        "service_name": "Oven & Stove Repair",
        "description": "Expert oven and stove repair in Toronto. Fix gas stoves, electric ovens, burners not heating. Same-day service • Licensed technicians • 90-day warranty. Call 437-747-6737!",
        "keywords": "oven repair Toronto, stove repair near me, oven not heating, burner not working",
        "icon": "stove",
        "problems": [
            "Oven not heating to temperature",
            "Burners not igniting or heating",
            "Temperature not accurate",
            "Strange smells or smoke",
            "Self-cleaning feature not working",
            "Control panel malfunction"
        ],
        "content_intro": "Can't cook because your oven or stove isn't working? Our licensed Toronto technicians repair all types of cooking appliances - gas stoves, electric ovens, and cooktops. From ignition problems to heating issues, we provide same-day service when available with a 90-day warranty.",
    },
    {
        "slug": "dishwasher-installation",
        "title": "Dishwasher Installation Toronto",
        "h1": "Professional Dishwasher Installation in Toronto & GTA",
        "service_name": "Dishwasher Installation",
        "description": "Expert dishwasher installation in Toronto. Install built-in, portable, or countertop dishwashers. Licensed plumbers • 90-day warranty. Call 437-747-6737 for fast installation!",
        "keywords": "dishwasher installation Toronto, install dishwasher, dishwasher hookup, dishwasher installer near me",
        "icon": "dishwasher",
        "problems": [
            "Need new dishwasher installed",
            "Replacing old dishwasher",
            "Kitchen renovation installation",
            "Portable to built-in conversion",
            "Leak-proof installation needed",
            "Electrical and plumbing hookup"
        ],
        "content_intro": "Bought a new dishwasher and need professional installation? Our licensed Toronto technicians install all dishwasher types - built-in, portable, and countertop models. We handle all plumbing and electrical connections, ensuring leak-free operation with a 90-day warranty.",
    }
]

# Location pages configuration
LOCATIONS = [
    {"name": "Toronto", "slug": "toronto", "description": "downtown Toronto and surrounding neighborhoods"},
    {"name": "Mississauga", "slug": "mississauga", "description": "Mississauga and nearby areas"},
    {"name": "Brampton", "slug": "brampton", "description": "Brampton and surrounding communities"},
    {"name": "Vaughan", "slug": "vaughan", "description": "Vaughan and neighboring areas"},
    {"name": "Markham", "slug": "markham", "description": "Markham and surrounding neighborhoods"},
    {"name": "Richmond Hill", "slug": "richmond-hill", "description": "Richmond Hill and nearby communities"},
    {"name": "Etobicoke", "slug": "etobicoke", "description": "Etobicoke and surrounding areas"},
    {"name": "Scarborough", "slug": "scarborough", "description": "Scarborough and neighboring communities"},
    {"name": "North York", "slug": "north-york", "description": "North York and surrounding neighborhoods"}
]


def get_service_page_template(service):
    """Generate HTML for a service page with main page design"""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{service['description']}">
    <meta name="keywords" content="{service['keywords']}">
    <title>{service['title']} | Same Day Service | Nika Appliance Repair</title>

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;500;600;700&family=Rubik:wght@300;400;500;600;700&display=swap" rel="stylesheet">

    <!-- Main Stylesheet -->
    <link rel="stylesheet" href="../css/style.css">
    <link rel="stylesheet" href="../css/mobile-responsive.css">

    <!-- Schema Markup -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Service",
        "name": "{service['service_name']}",
        "provider": {{
            "@type": "LocalBusiness",
            "name": "Nika Appliance Repair",
            "telephone": "{GLOBAL_DATA['phone']}",
            "address": {{
                "@type": "PostalAddress",
                "addressLocality": "Toronto",
                "addressRegion": "ON",
                "addressCountry": "CA"
            }}
        }},
        "areaServed": "Toronto, ON",
        "description": "{service['description']}"
    }}
    </script>
</head>
<body>
    <!-- Header -->
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
    </header>

    <!-- Hero Section -->
    <section class="service-hero">
        <div class="container">
            <div class="hero-content">
                <h1>{service['h1']}</h1>
                <p class="hero-subtitle">Same-day service • {GLOBAL_DATA['warranty']} warranty • Licensed & Insured</p>
                <p class="service-intro">{service['content_intro']}</p>
                <div class="hero-cta-group">
                    <a href="{GLOBAL_DATA['phone_href']}" class="cta-primary">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
                            <path d="M20.01 15.38c-1.23 0-2.42-.2-3.53-.56a.977.977 0 00-1.01.24l-1.57 1.97c-2.83-1.35-5.48-3.9-6.89-6.83l1.95-1.66c.27-.28.35-.67.24-1.02-.37-1.11-.56-2.3-.56-3.53 0-.54-.45-.99-.99-.99H4.19C3.65 3 3 3.24 3 3.99 3 13.28 10.73 21 20.01 21c.71 0 .99-.63.99-1.18v-3.45c0-.54-.45-.99-.99-.99z"/>
                        </svg>
                        Call Now: {GLOBAL_DATA['phone']}
                    </a>
                    <a href="#book" class="cta-secondary">Book Online & Save $40</a>
                </div>
            </div>
        </div>
    </section>

    <!-- Common Problems Section -->
    <section class="problems-section">
        <div class="container">
            <h2>Common {service['service_name']} Problems We Fix</h2>
            <div class="problems-grid">
                {''.join([f'<div class="problem-card"><h3>✓ {problem}</h3></div>' for problem in service['problems']])}
            </div>
        </div>
    </section>

    <!-- Pricing Section -->
    <section class="pricing-section">
        <div class="container">
            <h2>Transparent Pricing - No Hidden Fees</h2>
            <div class="pricing-info">
                <div class="price-card">
                    <h3>Diagnostic Fee</h3>
                    <p class="price">{GLOBAL_DATA['diagnostic_fee']}</p>
                    <p class="price-note">{GLOBAL_DATA['diagnostic_note']}</p>
                </div>
                <div class="price-card">
                    <h3>Typical Repair</h3>
                    <p class="price">{GLOBAL_DATA['repair_range']}</p>
                    <p class="price-note">Plus parts cost</p>
                </div>
                <div class="price-card">
                    <h3>Warranty</h3>
                    <p class="price">{GLOBAL_DATA['warranty']}</p>
                    <p class="price-note">On all repairs</p>
                </div>
            </div>
            <p class="pricing-note">We provide upfront pricing before starting any repair. What we quote is what you pay - no surprises!</p>
        </div>
    </section>

    <!-- Why Choose Us Section -->
    <section class="why-choose-section">
        <div class="container">
            <h2>Why Toronto Trusts Nika Appliance Repair</h2>
            <div class="benefits-grid">
                <div class="benefit-card">
                    <h3>🎓 Licensed & Insured</h3>
                    <p>Fully licensed technicians with comprehensive insurance coverage for your peace of mind.</p>
                </div>
                <div class="benefit-card">
                    <h3>⚡ Same-Day Service</h3>
                    <p>When available, we provide same-day repairs to minimize your inconvenience.</p>
                </div>
                <div class="benefit-card">
                    <h3>🛡️ {GLOBAL_DATA['warranty']} Warranty</h3>
                    <p>All repairs backed by our comprehensive {GLOBAL_DATA['warranty']} parts and labor warranty.</p>
                </div>
                <div class="benefit-card">
                    <h3>⭐ {GLOBAL_DATA['rating']} Rating</h3>
                    <p>Rated {GLOBAL_DATA['rating']} by {GLOBAL_DATA['review_count']} happy customers across Toronto & GTA.</p>
                </div>
                <div class="benefit-card">
                    <h3>💰 Transparent Pricing</h3>
                    <p>{GLOBAL_DATA['diagnostic_fee']} diagnostic {GLOBAL_DATA['diagnostic_note']}. No hidden fees - ever!</p>
                </div>
                <div class="benefit-card">
                    <h3>✅ {GLOBAL_DATA['years_experience']} Years Experience</h3>
                    <p>Over {GLOBAL_DATA['completion_count']} successful repairs completed across the GTA.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- FAQ Section -->
    <section class="faq-section">
        <div class="container">
            <h2>Frequently Asked Questions</h2>
            <div class="faq-container">
                <div class="faq-item">
                    <h3>How quickly can you come for {service['service_name'].lower()}?</h3>
                    <p>We offer same-day service when our schedule permits. For emergencies like refrigerators not cooling, we prioritize urgent situations. Call {GLOBAL_DATA['phone']} and we'll give you our earliest available time slot.</p>
                </div>
                <div class="faq-item">
                    <h3>How much does {service['service_name'].lower()} cost in Toronto?</h3>
                    <p>We charge {GLOBAL_DATA['diagnostic_fee']} for diagnosis {GLOBAL_DATA['diagnostic_note']}. Most repairs cost {GLOBAL_DATA['repair_range']} plus parts. We provide upfront pricing before starting work - no hidden fees!</p>
                </div>
                <div class="faq-item">
                    <h3>Do you offer a warranty on repairs?</h3>
                    <p>Yes! All repairs come with our comprehensive {GLOBAL_DATA['warranty']} warranty covering both parts and labor. If the same issue occurs within {GLOBAL_DATA['warranty']}, we'll fix it at no additional charge.</p>
                </div>
                <div class="faq-item">
                    <h3>What areas do you service?</h3>
                    <p>We service all of Toronto and the Greater Toronto Area including Mississauga, Brampton, Vaughan, Markham, Richmond Hill, Etobicoke, Scarborough, and North York.</p>
                </div>
                <div class="faq-item">
                    <h3>Are you licensed and insured?</h3>
                    <p>Absolutely! All our technicians are fully licensed and we carry comprehensive liability insurance for your protection and peace of mind.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
        <div class="container">
            <h2>Need {service['service_name']} in Toronto?</h2>
            <p>Call now for same-day service when available!</p>
            <div class="cta-buttons">
                <a href="{GLOBAL_DATA['phone_href']}" class="cta-primary">Call {GLOBAL_DATA['phone']}</a>
                <a href="#book" class="cta-secondary">Book Online & Save $40</a>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="main-footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-info">
                    <h3>Nika Appliance Repair</h3>
                    <p>Toronto & GTA Professional Appliance Repair</p>
                    <p>Phone: <a href="{GLOBAL_DATA['phone_href']}">{GLOBAL_DATA['phone']}</a></p>
                    <p>Hours: {GLOBAL_DATA['service_hours']}</p>
                </div>
                <div class="footer-services">
                    <h4>Our Services</h4>
                    <ul>
                        <li><a href="dishwasher-repair.html">Dishwasher Repair</a></li>
                        <li><a href="refrigerator-freezer-repair.html">Refrigerator Repair</a></li>
                        <li><a href="washer-dryer-repair.html">Washer & Dryer Repair</a></li>
                        <li><a href="oven-stove-repair.html">Oven & Stove Repair</a></li>
                        <li><a href="dishwasher-installation.html">Dishwasher Installation</a></li>
                    </ul>
                </div>
                <div class="footer-areas">
                    <h4>Service Areas</h4>
                    <ul>
                        <li><a href="../locations/toronto.html">Toronto</a></li>
                        <li><a href="../locations/mississauga.html">Mississauga</a></li>
                        <li><a href="../locations/brampton.html">Brampton</a></li>
                        <li><a href="../locations/vaughan.html">Vaughan</a></li>
                        <li><a href="../locations/markham.html">Markham</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2025 Nika Appliance Repair. All rights reserved. | Licensed & Insured | {GLOBAL_DATA['warranty']} Warranty</p>
            </div>
        </div>
    </footer>

    <script>
        // Mobile menu toggle
        document.querySelector('.mobile-menu-toggle').addEventListener('click', function() {{
            document.querySelector('.main-nav').classList.toggle('active');
        }});
    </script>
</body>
</html>'''


def create_service_pages():
    """Create all service pages"""
    services_dir = "services"
    os.makedirs(services_dir, exist_ok=True)

    created_files = []
    for service in SERVICES:
        filename = f"{services_dir}/{service['slug']}.html"
        html_content = get_service_page_template(service)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)

        created_files.append(filename)
        print(f"[OK] Created: {filename}")

    return created_files


def get_location_page_template(location):
    """Generate HTML for a location page"""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Professional appliance repair in {location['name']}. Same-day service • 90-day warranty • All brands. Call {GLOBAL_DATA['phone']} for fast, reliable repairs!">
    <meta name="keywords" content="appliance repair {location['name']}, {location['name']} appliance repair, fridge repair {location['name']}, washer repair {location['name']}">
    <title>Appliance Repair {location['name']} | Same Day Service | Nika</title>

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;500;600;700&family=Rubik:wght@300;400;500;600;700&display=swap" rel="stylesheet">

    <!-- Main Stylesheet -->
    <link rel="stylesheet" href="../css/style.css">
    <link rel="stylesheet" href="../css/mobile-responsive.css">

    <!-- Schema Markup -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "Nika Appliance Repair - {location['name']}",
        "telephone": "{GLOBAL_DATA['phone']}",
        "address": {{
            "@type": "PostalAddress",
            "addressLocality": "{location['name']}",
            "addressRegion": "ON",
            "addressCountry": "CA"
        }},
        "areaServed": "{location['name']}, ON",
        "description": "Professional appliance repair service in {location['description']}",
        "priceRange": "$$"
    }}
    </script>
</head>
<body>
    <!-- Header -->
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
    </header>

    <!-- Hero Section -->
    <section class="service-hero">
        <div class="container">
            <div class="hero-content">
                <h1>Appliance Repair in {location['name']}</h1>
                <p class="hero-subtitle">Same-day service • {GLOBAL_DATA['warranty']} warranty • Licensed & Insured</p>
                <p class="service-intro">Professional appliance repair service for residents of {location['description']}. Our licensed technicians fix all major appliance brands with same-day service when available and a comprehensive {GLOBAL_DATA['warranty']} warranty. From refrigerators to washers, we repair it all!</p>
                <div class="hero-cta-group">
                    <a href="{GLOBAL_DATA['phone_href']}" class="cta-primary">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
                            <path d="M20.01 15.38c-1.23 0-2.42-.2-3.53-.56a.977.977 0 00-1.01.24l-1.57 1.97c-2.83-1.35-5.48-3.9-6.89-6.83l1.95-1.66c.27-.28.35-.67.24-1.02-.37-1.11-.56-2.3-.56-3.53 0-.54-.45-.99-.99-.99H4.19C3.65 3 3 3.24 3 3.99 3 13.28 10.73 21 20.01 21c.71 0 .99-.63.99-1.18v-3.45c0-.54-.45-.99-.99-.99z"/>
                        </svg>
                        Call Now: {GLOBAL_DATA['phone']}
                    </a>
                    <a href="#book" class="cta-secondary">Book Online & Save $40</a>
                </div>
            </div>
        </div>
    </section>

    <!-- Services in {location['name']} Section -->
    <section class="services-section">
        <div class="container">
            <h2>Our Appliance Repair Services in {location['name']}</h2>
            <div class="services-grid">
                <div class="service-card">
                    <h3>🍽️ Dishwasher Repair</h3>
                    <p>Fix dishwashers not draining, cleaning poorly, or making strange noises. All brands repaired.</p>
                    <a href="../services/dishwasher-repair.html">Learn More →</a>
                </div>
                <div class="service-card">
                    <h3>❄️ Refrigerator Repair</h3>
                    <p>Emergency fridge repairs for cooling issues, ice maker problems, and more. Same-day priority service.</p>
                    <a href="../services/refrigerator-freezer-repair.html">Learn More →</a>
                </div>
                <div class="service-card">
                    <h3>👕 Washer & Dryer Repair</h3>
                    <p>Fix washers not spinning and dryers not heating. Get your laundry routine back on track fast.</p>
                    <a href="../services/washer-dryer-repair.html">Learn More →</a>
                </div>
                <div class="service-card">
                    <h3>🔥 Oven & Stove Repair</h3>
                    <p>Repair gas and electric ovens, cooktops, and ranges. Licensed for safe gas appliance repairs.</p>
                    <a href="../services/oven-stove-repair.html">Learn More →</a>
                </div>
                <div class="service-card">
                    <h3>🛠️ Dishwasher Installation</h3>
                    <p>Professional installation of new dishwashers with proper plumbing and electrical connections.</p>
                    <a href="../services/dishwasher-installation.html">Learn More →</a>
                </div>
            </div>
        </div>
    </section>

    <!-- Why Choose Us Section -->
    <section class="why-choose-section">
        <div class="container">
            <h2>Why {location['name']} Residents Trust Nika Appliance Repair</h2>
            <div class="benefits-grid">
                <div class="benefit-card">
                    <h3>📍 Local Service in {location['name']}</h3>
                    <p>We serve {location['description']} with fast response times and local expertise.</p>
                </div>
                <div class="benefit-card">
                    <h3>⚡ Same-Day Service</h3>
                    <p>When available, we provide same-day repairs to {location['name']} residents.</p>
                </div>
                <div class="benefit-card">
                    <h3>🛡️ {GLOBAL_DATA['warranty']} Warranty</h3>
                    <p>All repairs backed by our comprehensive {GLOBAL_DATA['warranty']} parts and labor warranty.</p>
                </div>
                <div class="benefit-card">
                    <h3>⭐ {GLOBAL_DATA['rating']} Rating</h3>
                    <p>Rated {GLOBAL_DATA['rating']} by {GLOBAL_DATA['review_count']} happy customers across the GTA.</p>
                </div>
                <div class="benefit-card">
                    <h3>💰 Transparent Pricing</h3>
                    <p>{GLOBAL_DATA['diagnostic_fee']} diagnostic {GLOBAL_DATA['diagnostic_note']}. No hidden fees!</p>
                </div>
                <div class="benefit-card">
                    <h3>✅ Licensed & Insured</h3>
                    <p>Fully licensed technicians with {GLOBAL_DATA['years_experience']} years experience serving {location['name']}.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- FAQ Section -->
    <section class="faq-section">
        <div class="container">
            <h2>Appliance Repair FAQs for {location['name']}</h2>
            <div class="faq-container">
                <div class="faq-item">
                    <h3>Do you service all of {location['name']}?</h3>
                    <p>Yes! We provide appliance repair services throughout {location['description']}. Call {GLOBAL_DATA['phone']} to confirm we service your specific address.</p>
                </div>
                <div class="faq-item">
                    <h3>How quickly can you come to {location['name']}?</h3>
                    <p>We offer same-day service to {location['name']} when our schedule permits. For emergencies, we prioritize urgent situations. Call us for our earliest available time slot.</p>
                </div>
                <div class="faq-item">
                    <h3>What appliance brands do you repair in {location['name']}?</h3>
                    <p>We repair all major appliance brands including LG, Samsung, Whirlpool, GE, Maytag, Frigidaire, KitchenAid, Bosch, and more. All repairs come with our {GLOBAL_DATA['warranty']} warranty.</p>
                </div>
                <div class="faq-item">
                    <h3>How much does appliance repair cost in {location['name']}?</h3>
                    <p>We charge {GLOBAL_DATA['diagnostic_fee']} for diagnosis {GLOBAL_DATA['diagnostic_note']}. Most repairs cost {GLOBAL_DATA['repair_range']} plus parts. We provide upfront pricing before starting work.</p>
                </div>
                <div class="faq-item">
                    <h3>Are you licensed to work in {location['name']}?</h3>
                    <p>Absolutely! All our technicians are fully licensed and insured to provide appliance repair services throughout {location['name']} and the Greater Toronto Area.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
        <div class="container">
            <h2>Need Appliance Repair in {location['name']}?</h2>
            <p>Call now for same-day service when available!</p>
            <div class="cta-buttons">
                <a href="{GLOBAL_DATA['phone_href']}" class="cta-primary">Call {GLOBAL_DATA['phone']}</a>
                <a href="#book" class="cta-secondary">Book Online & Save $40</a>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="main-footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-info">
                    <h3>Nika Appliance Repair</h3>
                    <p>Serving {location['name']} & GTA</p>
                    <p>Phone: <a href="{GLOBAL_DATA['phone_href']}">{GLOBAL_DATA['phone']}</a></p>
                    <p>Hours: {GLOBAL_DATA['service_hours']}</p>
                </div>
                <div class="footer-services">
                    <h4>Our Services</h4>
                    <ul>
                        <li><a href="../services/dishwasher-repair.html">Dishwasher Repair</a></li>
                        <li><a href="../services/refrigerator-freezer-repair.html">Refrigerator Repair</a></li>
                        <li><a href="../services/washer-dryer-repair.html">Washer & Dryer Repair</a></li>
                        <li><a href="../services/oven-stove-repair.html">Oven & Stove Repair</a></li>
                        <li><a href="../services/dishwasher-installation.html">Dishwasher Installation</a></li>
                    </ul>
                </div>
                <div class="footer-areas">
                    <h4>Other Service Areas</h4>
                    <ul>
                        {''.join([f'<li><a href="{loc["slug"]}.html">{loc["name"]}</a></li>' for loc in LOCATIONS if loc["name"] != location["name"]][:5])}
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2025 Nika Appliance Repair. All rights reserved. | Licensed & Insured | {GLOBAL_DATA['warranty']} Warranty</p>
            </div>
        </div>
    </footer>

    <script>
        // Mobile menu toggle
        document.querySelector('.mobile-menu-toggle').addEventListener('click', function() {{
            document.querySelector('.main-nav').classList.toggle('active');
        }});
    </script>
</body>
</html>'''


def create_location_pages():
    """Create all location pages"""
    locations_dir = "locations"
    os.makedirs(locations_dir, exist_ok=True)

    created_files = []
    for location in LOCATIONS:
        filename = f"{locations_dir}/{location['slug']}.html"
        html_content = get_location_page_template(location)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)

        created_files.append(filename)
        print(f"[OK] Created: {filename}")

    return created_files


def main():
    """Main function to create all pages"""
    print("\n" + "="*60)
    print("BMAD PAGE GENERATOR - Nika Appliance Repair")
    print("="*60 + "\n")

    print("Creating service pages...")
    service_files = create_service_pages()
    print(f"\nCreated {len(service_files)} service pages\n")

    print("Creating location pages...")
    location_files = create_location_pages()
    print(f"\nCreated {len(location_files)} location pages\n")

    total_files = len(service_files) + len(location_files)
    print("="*60)
    print(f"SUCCESS! Created {total_files} total pages")
    print("="*60)
    print("\nNext steps:")
    print("1. Run BMAD tests on each page:")
    print("   cd 'C:\\Users\\petru\\Nika Appliance Repair Website'")
    print("   python seo-checker.py ../NikaApplianceRepair/services/dishwasher-repair.html")
    print("   python test-actual-scroll.py ../NikaApplianceRepair/services/dishwasher-repair.html")
    print("\n2. Fix any failing parameters one by one")
    print("3. Retest until all 277 parameters pass")
    print("\n")


if __name__ == "__main__":
    main()
