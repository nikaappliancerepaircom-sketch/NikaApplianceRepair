"""
Optimized SEO Page Generator - Target 85+/100
Fixes:
1. Keyword density 1.5-2.5% (was 0.86%)
2. 15+ internal links (was 0)
3. Toronto mentions 15-40 (was 49)
4. Voice search phrases
5. More lists/tables for snippets
"""

import os

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

# Service configurations with optimized keywords
SERVICES = {
    "dishwasher-repair": {
        "name": "Dishwasher Repair",
        "keyword": "dishwasher repair",
        "common_issues": ["Not draining properly", "Not cleaning dishes", "Making loud noises", "Leaking water", "Won't start or complete cycle"],
        "brands": ["Bosch", "KitchenAid", "Whirlpool", "GE", "Samsung", "LG", "Miele", "Frigidaire"],
        "parts": ["spray arms", "drain pumps", "door latches", "control boards", "heating elements"]
    },
    "refrigerator-freezer-repair": {
        "name": "Refrigerator & Freezer Repair",
        "keyword": "refrigerator repair",
        "common_issues": ["Not cooling properly", "Ice maker not working", "Water leaking", "Making strange noises", "Freezer too cold or warm"],
        "brands": ["LG", "Samsung", "Whirlpool", "GE", "Frigidaire", "KitchenAid", "Maytag", "Sub-Zero"],
        "parts": ["compressors", "evaporator fans", "defrost timers", "thermostats", "ice makers"]
    },
    "washer-dryer-repair": {
        "name": "Washer & Dryer Repair",
        "keyword": "washer repair",
        "common_issues": ["Won't spin or drain", "Excessive vibration", "Not heating properly", "Door won't lock", "Making loud noises"],
        "brands": ["LG", "Samsung", "Whirlpool", "Maytag", "GE", "Bosch", "Electrolux", "Speed Queen"],
        "parts": ["drum bearings", "belts", "motors", "pumps", "heating elements"]
    },
    "oven-stove-repair": {
        "name": "Oven & Stove Repair",
        "keyword": "oven repair",
        "common_issues": ["Not heating evenly", "Burners not igniting", "Oven door won't close", "Temperature inaccurate", "Control panel errors"],
        "brands": ["GE", "Whirlpool", "Frigidaire", "Samsung", "LG", "Bosch", "KitchenAid", "Thermador"],
        "parts": ["heating elements", "igniters", "thermostats", "control boards", "door hinges"]
    },
    "dishwasher-installation": {
        "name": "Dishwasher Installation",
        "keyword": "dishwasher installation",
        "common_issues": ["New dishwasher setup", "Replacement installation", "Connection to plumbing", "Electrical hookup", "Cabinet modifications"],
        "brands": ["Bosch", "KitchenAid", "Whirlpool", "GE", "Samsung", "LG", "Miele", "Frigidaire"],
        "parts": ["water lines", "drain hoses", "mounting brackets", "electrical connections", "soundproofing"]
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

# Floating icons HTML from index.html
FLOATING_ICONS_HTML = '''
    <!-- Floating Icons Animation Background -->
    <div class="hero-bg-animation">
        <!-- Refrigerator Icon -->
        <div class="floating-icon icon-1">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="white" xmlns="http://www.w3.org/2000/svg">
                <path d="M7 2C5.9 2 5 2.9 5 4V19C5 20.1 5.9 21 7 21H17C18.1 21 19 20.1 19 19V4C19 2.9 18.1 2 17 2H7ZM7 4H17V10H7V4ZM7 12H17V19H7V12ZM8 5V8H10V5H8ZM8 13V16H10V13H8Z"/>
            </svg>
        </div>

        <!-- Dishwasher Icon -->
        <div class="floating-icon icon-2">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="white" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 2H6C4.9 2 4 2.9 4 4V20C4 21.1 4.9 22 6 22H18C19.1 22 20 21.1 20 20V4C20 2.9 19.1 2 18 2ZM18 4V8H6V4H18ZM6 20V10H18V20H6ZM8 5C7.45 5 7 5.45 7 6C7 6.55 7.45 7 8 7C8.55 7 9 6.55 9 6C9 5.45 8.55 5 8 5ZM10 5C9.45 5 9 5.45 9 6C9 6.55 9.45 7 10 7C10.55 7 11 6.55 11 6C11 5.45 10.55 5 10 5Z"/>
            </svg>
        </div>

        <!-- Dryer Icon -->
        <div class="floating-icon icon-3">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="white" xmlns="http://www.w3.org/2000/svg">
                <path d="M6 2H18C19.11 2 20 2.89 20 4V20C20 21.11 19.11 22 18 22H6C4.89 22 4 21.11 4 20V4C4 2.89 4.89 2 6 2ZM6 4V7H18V4H6ZM6 9V20H18V9H6ZM8 5C8.55 5 9 5.45 9 6C9 6.55 8.55 7 8 7C7.45 7 7 6.55 7 6C7 5.45 7.45 5 8 5ZM10 5C10.55 5 11 5.45 11 6C11 6.55 10.55 7 10 7C9.45 7 9 6.55 9 6C9 5.45 9.45 5 10 5ZM12 11.5C14.21 11.5 16 13.29 16 15.5S14.21 19.5 12 19.5 8 17.71 8 15.5 9.79 11.5 12 11.5ZM12 13.5C10.9 13.5 10 14.4 10 15.5S10.9 17.5 12 17.5 14 16.6 14 15.5 13.1 13.5 12 13.5Z"/>
            </svg>
        </div>

        <!-- Stove Icon -->
        <div class="floating-icon icon-4">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="white" xmlns="http://www.w3.org/2000/svg">
                <path d="M4 8H20V5H4V8ZM6 2C6.55 2 7 2.45 7 3S6.55 4 6 4 5 3.55 5 3 5.45 2 6 2ZM9 2C9.55 2 10 2.45 10 3S9.55 4 9 4 8 3.55 8 3 8.45 2 9 2ZM15 2C15.55 2 16 2.45 16 3S15.55 4 15 4 14 3.55 14 3 14.45 2 15 2ZM18 2C18.55 2 19 2.45 19 3S18.55 4 18 4 17 3.55 17 3 17.45 2 18 2ZM4 10V19C4 20.1 4.9 21 6 21H18C19.1 21 20 20.1 20 19V10H4ZM8 18C6.9 18 6 17.1 6 16C6 14.9 6.9 14 8 14S10 14.9 10 16C10 17.1 9.1 18 8 18ZM16 18C14.9 18 14 17.1 14 16C14 14.9 14.9 14 16 14S18 14.9 18 16C18 17.1 17.1 18 16 18Z"/>
            </svg>
        </div>

        <!-- Oven Icon -->
        <div class="floating-icon icon-5">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="white" xmlns="http://www.w3.org/2000/svg">
                <path d="M4 3C2.9 3 2 3.9 2 5V19C2 20.1 2.9 21 4 21H20C21.1 21 22 20.1 22 19V5C22 3.9 21.1 3 20 3H4ZM4 5H20V9H4V5ZM4 11H20V19H4V11ZM5 6V8H7V6H5ZM8 6V8H10V6H8ZM19 6C18.45 6 18 6.45 18 7C18 7.55 18.45 8 19 8C19.55 8 20 7.55 20 7C20 6.45 19.55 6 19 6ZM6 13V17H18V13H6Z"/>
            </svg>
        </div>

        <!-- Washing Machine Icon -->
        <div class="floating-icon icon-6">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="white" xmlns="http://www.w3.org/2000/svg">
                <path d="M6 2H18C19.11 2 20 2.89 20 4V20C20 21.11 19.11 22 18 22H6C4.89 22 4 21.11 4 20V4C4 2.89 4.89 2 6 2ZM6 4V20H18V4H6ZM12 7C14.76 7 17 9.24 17 12S14.76 17 12 17 7 14.76 7 12 9.24 7 12 7ZM12 9C10.34 9 9 10.34 9 12S10.34 15 12 15 15 13.66 15 12 13.66 9 12 9ZM8 5C8.55 5 9 5.45 9 6S8.55 7 8 7 7 6.55 7 6 7.45 5 8 5ZM10 5C10.55 5 11 5.45 11 6S10.55 7 10 7 9 6.55 9 6 9.45 5 10 5Z"/>
            </svg>
        </div>
    </div>
'''

# Floating icons CSS from index.html
FLOATING_ICONS_CSS = '''
<style>
    /* Floating Icons Animation from index.html */
    .hero-bg-animation {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        z-index: 1;
        pointer-events: none;
    }

    .floating-icon {
        position: absolute;
        opacity: 0.7;
        transition: all 0.3s ease;
    }

    .floating-icon:hover {
        transform: scale(1.1);
        opacity: 0.9;
    }

    .floating-icon svg {
        display: block;
        transform-style: preserve-3d;
        filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
    }

    /* Icon positions */
    .icon-1 {
        top: 20%;
        left: 5%;
        animation: floatDiagonal 25s infinite ease-in-out;
    }

    .icon-2 {
        top: 20%;
        right: 8%;
        animation: floatCircular 30s infinite ease-in-out;
        animation-delay: 2s;
    }

    .icon-3 {
        top: 50%;
        left: 5%;
        animation: floatDiagonal 28s infinite ease-in-out reverse;
        animation-delay: 4s;
    }

    .icon-4 {
        top: 50%;
        right: 8%;
        animation: floatWave 32s infinite ease-in-out;
        animation-delay: 1s;
    }

    .icon-5 {
        top: 80%;
        left: 5%;
        animation: floatCircular 27s infinite ease-in-out reverse;
        animation-delay: 6s;
    }

    .icon-6 {
        top: 80%;
        right: 8%;
        animation: floatDiagonal 29s infinite ease-in-out;
        animation-delay: 3s;
    }

    /* Keyframes for smooth floating animations */
    @keyframes floatDiagonal {
        0%, 100% {
            transform: translate(0, 0) rotate(0deg);
        }
        25% {
            transform: translate(30px, -20px) rotate(5deg);
        }
        50% {
            transform: translate(15px, -40px) rotate(-3deg);
        }
        75% {
            transform: translate(-20px, -25px) rotate(7deg);
        }
    }

    @keyframes floatCircular {
        0%, 100% {
            transform: translate(0, 0) scale(1);
        }
        25% {
            transform: translate(25px, -15px) scale(1.05);
        }
        50% {
            transform: translate(40px, 10px) scale(0.95);
        }
        75% {
            transform: translate(15px, 20px) scale(1.03);
        }
    }

    @keyframes floatWave {
        0%, 100% {
            transform: translateY(0) rotate(0deg);
        }
        25% {
            transform: translateY(-30px) rotate(3deg);
        }
        50% {
            transform: translateY(-10px) rotate(-3deg);
        }
        75% {
            transform: translateY(-25px) rotate(2deg);
        }
    }

    /* Hide some icons on smaller screens */
    @media (max-width: 768px) {
        .icon-3, .icon-4, .icon-5, .icon-6 {
            display: none;
        }

        .icon-1, .icon-2 {
            opacity: 0.4;
        }

        .floating-icon svg {
            width: 32px;
            height: 32px;
        }
    }
</style>
'''


def create_optimized_service_page(slug):
    """Create service page with 85+/100 SEO optimization"""

    config = SERVICES[slug]
    service_name = config["name"]
    keyword = config["keyword"]

    # Location links for internal linking (15+ links needed)
    location_links = f"""<a href="../locations/toronto.html">Toronto</a>,
<a href="../locations/mississauga.html">Mississauga</a>,
<a href="../locations/brampton.html">Brampton</a>,
<a href="../locations/vaughan.html">Vaughan</a>,
<a href="../locations/markham.html">Markham</a>,
<a href="../locations/richmond-hill.html">Richmond Hill</a>,
<a href="../locations/etobicoke.html">Etobicoke</a>,
<a href="../locations/scarborough.html">Scarborough</a>,
<a href="../locations/north-york.html">North York</a>"""

    # Service links for internal linking
    service_links = ""
    for other_slug in SERVICES.keys():
        if other_slug != slug:
            service_links += f'<a href="../services/{other_slug}.html">{SERVICES[other_slug]["name"]}</a>, '
    service_links = service_links.rstrip(', ')

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

    {FLOATING_ICONS_CSS}

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
            }},
            {{
                "@type": "Question",
                "name": "What brands do you service for {keyword}?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "We service all major brands including {', '.join(config['brands'][:5])} and many more."
                }}
            }},
            {{
                "@type": "Question",
                "name": "What areas do you serve for {keyword}?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "We serve Toronto, Mississauga, Brampton, Vaughan, Markham, Richmond Hill, Etobicoke, Scarborough, North York and all GTA areas."
                }}
            }}
        ]
    }}
    </script>
</head>
<body>
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
    </header>

    <!-- Hero Section with Floating Icons Background -->
    <section class="hero-section">
        {FLOATING_ICONS_HTML}
        <div class="container">
            <div class="hero-content">
                <div class="hero-text">
                    <h1 class="hero-title">
                        Professional <span class="highlight-yellow">{service_name}</span> in GTA
                    </h1>
                    <p class="hero-subtitle">Same-day service • {GLOBAL_DATA['warranty']} warranty • All brands</p>
                    <p class="hero-trust-text">No Hidden Fees - Ever! • Licensed & Insured • {GLOBAL_DATA['years_experience']} Years Experience</p>
                    <div class="hero-cta-group">
                        <a href="#book" class="cta-primary">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
                                <path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z"/>
                            </svg>
                            Book Service Now
                        </a>
                        <a href="{GLOBAL_DATA['phone_href']}" class="cta-secondary">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
                                <path d="M20.01 15.38c-1.23 0-2.42-.2-3.53-.56a.977.977 0 00-1.01.24l-1.57 1.97c-2.83-1.35-5.48-3.9-6.89-6.83l1.95-1.66c.27-.28.35-.67.24-1.02-.37-1.11-.56-2.3-.56-3.53 0-.54-.45-.99-.99-.99H4.19C3.65 3 3 3.24 3 3.99 3 13.28 10.73 21 20.01 21c.71 0 .99-.63.99-1.18v-3.45c0-.54-.45-.99-.99-.99z"/>
                            </svg>
                            CLICK TO CALL US TODAY
                        </a>
                    </div>
                </div>
                <div class="hero-image">
                    <img src="../assets/images/friendly-technician-character.png" alt="Professional {service_name} Technician" />
                </div>
            </div>
        </div>
    </section>

    <!-- AI Summary Box Section -->
    <section class="section bg-light-gray">
        <div class="container">
            <div class="ai-summary-box" style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border-left: 4px solid #0ea5e9; padding: 2rem; border-radius: 8px; margin: 2rem 0;">
                <h3 style="color: #0ea5e9; margin-top: 0;">Quick Summary - AI-Optimized</h3>
                <p style="font-size: 1.1rem; line-height: 1.7;">Need professional {keyword} in the GTA? Nika Appliance Repair provides same-day {keyword} service with a {GLOBAL_DATA['warranty']} warranty. Licensed technicians fix all major brands. Call {GLOBAL_DATA['phone']} for {GLOBAL_DATA['diagnostic_fee']} diagnosis {GLOBAL_DATA['diagnostic_note']}. Most {keyword} repairs cost {GLOBAL_DATA['repair_range']} plus parts with upfront pricing. We serve {location_links} and all GTA areas.</p>
            </div>
        </div>
    </section>

    <!-- Main Content Section -->
    <section class="section bg-white">
        <div class="container" style="max-width: 900px;">
            <img src="../assets/images/friendly-technician-character.png" alt="{service_name} Service Professional" style="width: 100%; max-width: 600px; margin: 2rem auto; display: block; border-radius: 8px;" />

            <h2>Why Choose Our {service_name} Service</h2>
            <p>When you need reliable {keyword} in the GTA, choosing the right service provider makes all the difference. Our expert {keyword} technicians bring {GLOBAL_DATA['years_experience']} years of experience to every service call. We understand how important your appliances are to your daily routine, which is why we prioritize same-day {keyword} service whenever possible.</p>

            <p>Our {keyword} service stands out because we focus on transparency and quality. Every {keyword} job starts with a thorough diagnostic assessment for {GLOBAL_DATA['diagnostic_fee']}, which is waived when you proceed with repairs. This approach ensures you understand exactly what {keyword} work is needed before we begin, with no surprises or hidden fees.</p>

            <h2>Common {service_name} Issues We Fix</h2>
            <p>Our experienced technicians handle all types of {keyword} challenges. Here are the most common {keyword} problems we solve:</p>

            <table style="width: 100%; border-collapse: collapse; margin: 1.5rem 0; border: 1px solid #e2e8f0;">
                <thead>
                    <tr style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                        <th style="padding: 1rem; text-align: left; border: 1px solid #e2e8f0;">Issue</th>
                        <th style="padding: 1rem; text-align: left; border: 1px solid #e2e8f0;">Description</th>
                    </tr>
                </thead>
                <tbody>
                    {"".join([f'<tr style="background: {"#f8fafc" if i % 2 == 0 else "white"};"><td style="padding: 0.75rem; border: 1px solid #e2e8f0;">{issue}</td><td style="padding: 0.75rem; border: 1px solid #e2e8f0;">Professional {keyword} diagnosis and repair</td></tr>' for i, issue in enumerate(config['common_issues'])])}
                </tbody>
            </table>

            <p>No matter what {keyword} issue you're facing, our skilled technicians have the expertise to diagnose and fix it properly. Each {keyword} repair comes with our {GLOBAL_DATA['warranty']} warranty for your peace of mind.</p>

            <h2>Brands We Service for {service_name}</h2>
            <p>Our {keyword} expertise covers all major appliance manufacturers. Whether you need {keyword} for a brand-new model or an older appliance, our technicians have the knowledge and parts to get your appliance working perfectly again.</p>

            <ul style="column-count: 2; column-gap: 2rem; list-style-type: none; padding: 0;">
                {"".join([f'<li style="padding: 0.5rem 0; border-bottom: 1px solid #e2e8f0;"><strong>{brand}</strong> {keyword}</li>' for brand in config['brands']])}
            </ul>

            <p>Each brand has unique characteristics and common {keyword} needs. Our technicians receive ongoing training to stay current with the latest {keyword} techniques and technologies across all brands.</p>

            <h2>Our {service_name} Process</h2>
            <p>We've refined our {keyword} process to be efficient, transparent, and customer-focused. Here's what you can expect when you call us for {keyword}:</p>

            <ol style="line-height: 2;">
                <li><strong>Initial Contact:</strong> Call {GLOBAL_DATA['phone']} to schedule your {keyword} appointment - often same-day service is available</li>
                <li><strong>Diagnostic Assessment:</strong> Our technician performs a comprehensive {keyword} diagnostic for {GLOBAL_DATA['diagnostic_fee']}</li>
                <li><strong>Transparent Quote:</strong> You receive upfront pricing for the {keyword} work needed before any repairs begin</li>
                <li><strong>Professional Repair:</strong> If you approve, we complete the {keyword} work with quality parts and expert techniques</li>
                <li><strong>Quality Testing:</strong> Every {keyword} repair is thoroughly tested to ensure proper operation</li>
                <li><strong>Warranty Coverage:</strong> Your {keyword} repair is backed by our {GLOBAL_DATA['warranty']} warranty</li>
            </ol>

            <h3>How much does {keyword} cost?</h3>
            <p>The cost of {keyword} depends on the specific issue and required parts. Most {keyword} repairs fall within the {GLOBAL_DATA['repair_range']} range plus parts. The diagnostic fee of {GLOBAL_DATA['diagnostic_fee']} is waived when you proceed with {keyword} repairs, making the process more affordable.</p>

            <h3>How long does {keyword} take?</h3>
            <p>Most {keyword} jobs are completed during a single service visit lasting 1-2 hours. Complex {keyword} repairs requiring special parts may need a return visit, but we stock common parts on our service vehicles to complete most {keyword} work immediately.</p>

            <h3>What warranty do you offer on {keyword}?</h3>
            <p>Every {keyword} repair comes with our comprehensive {GLOBAL_DATA['warranty']} warranty covering both parts and labor. This warranty demonstrates our confidence in the quality of our {keyword} work and protects your investment.</p>

            <h2>Areas We Serve for {service_name}</h2>
            <p>Our {keyword} service covers the entire GTA including {location_links}. No matter where you're located in the Greater area, our mobile {keyword} service brings expert repairs directly to your home.</p>

            <p>Each area has unique characteristics, but our {keyword} service remains consistently excellent wherever you're located. We maintain the same high standards, transparent pricing, and quality workmanship for every {keyword} job across all service areas.</p>

            <h3>Why is professional {keyword} important?</h3>
            <p>Professional {keyword} is crucial because modern appliances contain complex systems requiring specialized knowledge. Attempting DIY {keyword} can void warranties, create safety hazards, or cause additional damage requiring more expensive repairs. Our licensed technicians have the training, tools, and experience to perform {keyword} safely and effectively.</p>

            <h3>Can I prevent future {keyword} needs?</h3>
            <p>Regular maintenance can reduce the frequency of {keyword} needs. Our technicians provide specific maintenance recommendations during each {keyword} visit. Simple steps like regular cleaning and proper usage can extend appliance life and reduce {keyword} requirements.</p>

            <h2>Additional Services</h2>
            <p>Beyond {keyword}, we offer comprehensive appliance repair services including {service_links}. Our technicians can handle all your appliance needs during a single visit, saving you time and money.</p>

            <h3>What makes your {keyword} service different?</h3>
            <p>Our {keyword} service combines technical expertise with customer-focused practices. We prioritize transparent communication, upfront pricing, and quality workmanship. Every {keyword} technician is licensed, insured, and committed to your satisfaction. Our {GLOBAL_DATA['warranty']} warranty and {GLOBAL_DATA['rating']} rating from {GLOBAL_DATA['review_count']} reviews demonstrate our commitment to excellence in {keyword} service.</p>

            <h3>How do I schedule {keyword} service?</h3>
            <p>Scheduling {keyword} service is simple. Call {GLOBAL_DATA['phone']} to speak with our friendly staff. We'll discuss your {keyword} needs, schedule a convenient appointment, and often provide same-day {keyword} service. You can also use our online booking form below for {keyword} scheduling.</p>

            <h2>Emergency {service_name} Service</h2>
            <p>Some {keyword} situations require immediate attention. When you have an urgent {keyword} need, our team responds quickly to minimize disruption to your daily routine. Call {GLOBAL_DATA['phone']} for emergency {keyword} service in the GTA.</p>

            <p>Our emergency {keyword} service operates on the same principles as scheduled repairs - transparent pricing, quality workmanship, and {GLOBAL_DATA['warranty']} warranty coverage. You never pay more just because you need urgent {keyword} service.</p>

            <img src="../assets/images/friendly-technician-character.png" alt="{service_name} Expert Technician" style="width: 100%; max-width: 600px; margin: 2rem auto; display: block; border-radius: 8px;" />

            <h2>Customer Satisfaction Guarantee</h2>
            <p>Your satisfaction with our {keyword} service is our top priority. We maintain a {GLOBAL_DATA['rating']} rating based on {GLOBAL_DATA['review_count']} customer reviews because we focus on doing {keyword} work right the first time. If you're not completely satisfied with your {keyword} repair, we'll make it right.</p>

            <h3>What customers say about our {keyword} service</h3>
            <p>Our {keyword} customers consistently praise our professionalism, transparency, and technical expertise. Many customers note that our {keyword} technicians take time to explain issues clearly and provide helpful maintenance tips. The {GLOBAL_DATA['warranty']} warranty gives customers confidence in choosing our {keyword} service.</p>

            <h2>Ready for Expert {service_name}?</h2>
            <p>Don't let appliance problems disrupt your routine. Our professional {keyword} service combines technical expertise, transparent pricing, and customer-focused care to deliver results you can trust. With same-day service availability, comprehensive warranties, and competitive pricing, we make {keyword} simple and stress-free.</p>

            <p>Call {GLOBAL_DATA['phone']} now to schedule your {keyword} appointment. Our friendly team is ready to help you get your appliance back to perfect working condition with quality {keyword} service you can rely on.</p>
        </div>
    </section>

    <!-- Contact Form Section -->
    <section id="book" class="section bg-light-gray">
        <div class="container" style="max-width: 600px;">
            <h2 style="text-align: center; margin-bottom: 2rem;">Book Your {service_name} Service</h2>
            <form class="contact-form" style="background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <div class="form-group">
                    <label for="name">Name *</label>
                    <input type="text" id="name" name="name" required style="width: 100%; padding: 0.75rem; border: 1px solid #e2e8f0; border-radius: 4px; font-size: 1rem;">
                </div>
                <div class="form-group" style="margin-top: 1rem;">
                    <label for="phone">Phone *</label>
                    <input type="tel" id="phone" name="phone" required style="width: 100%; padding: 0.75rem; border: 1px solid #e2e8f0; border-radius: 4px; font-size: 1rem;">
                </div>
                <div class="form-group" style="margin-top: 1rem;">
                    <label for="service">Service Needed</label>
                    <input type="text" id="service" name="service" value="{service_name}" readonly style="width: 100%; padding: 0.75rem; border: 1px solid #e2e8f0; border-radius: 4px; font-size: 1rem; background: #f8fafc;">
                </div>
                <div class="form-group" style="margin-top: 1rem;">
                    <label for="message">Describe the Issue</label>
                    <textarea id="message" name="message" rows="4" style="width: 100%; padding: 0.75rem; border: 1px solid #e2e8f0; border-radius: 4px; font-size: 1rem;"></textarea>
                </div>
                <button type="submit" style="width: 100%; margin-top: 1.5rem; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 4px; font-size: 1.1rem; font-weight: 600; cursor: pointer;">
                    Book Service Now
                </button>
            </form>
            <p style="text-align: center; margin-top: 1.5rem; color: #64748b;">Or call us directly: <a href="{GLOBAL_DATA['phone_href']}" style="color: #667eea; font-weight: 600;">{GLOBAL_DATA['phone']}</a></p>
        </div>
    </section>

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
</html>
'''


def main():
    """Generate all optimized service pages"""
    print("=" * 60)
    print("OPTIMIZED SEO GENERATOR - Target 85+/100")
    print("=" * 60)

    # Get absolute path to services directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    services_dir = os.path.join(project_root, "services")

    if not os.path.exists(services_dir):
        os.makedirs(services_dir)

    for slug in SERVICES.keys():
        html = create_optimized_service_page(slug)
        filepath = os.path.join(services_dir, f"{slug}.html")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"[OK] {filepath}")

    print()
    print(f"[SUCCESS] Generated {len(SERVICES)} optimized pages")
    print()
    print("OPTIMIZATIONS:")
    print("- Keyword density increased to 1.5-2.5% target")
    print("- 15+ internal links per page (locations + services)")
    print("- Reduced location mentions (15-35 range)")
    print("- Added voice search phrases (questions)")
    print("- Added comparison tables for snippets")
    print("- Full index.html design with all CSS and animations")
    print()
    print("Ready for BMAD testing - Target 85+/100!")


if __name__ == "__main__":
    main()
