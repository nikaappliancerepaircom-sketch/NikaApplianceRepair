"""
Full Design Page Generator - Using EXACT index.html design
All CSS files, floating icons, gradients, colors, images from index.html
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

# Floating icons SVG (6 icons from index.html)
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
        animation-delay: 3s;
    }

    .icon-6 {
        top: 80%;
        right: 8%;
        animation: floatWave 29s infinite ease-in-out reverse;
        animation-delay: 5s;
    }

    @keyframes floatDiagonal {
        0%, 100% {
            transform: translate(0, 0) rotate(0deg) scale(1);
        }
        25% {
            transform: translate(20px, -20px) rotate(15deg) scale(1.1);
        }
        50% {
            transform: translate(-15px, -25px) rotate(-10deg) scale(1.05);
        }
        75% {
            transform: translate(-20px, 15px) rotate(20deg) scale(1.15);
        }
    }

    @keyframes floatCircular {
        0%, 100% {
            transform: translate(0, 0) rotate(0deg) scale(1);
        }
        25% {
            transform: translate(25px, -10px) rotate(90deg) scale(1.1);
        }
        50% {
            transform: translate(15px, 20px) rotate(180deg) scale(1.05);
        }
        75% {
            transform: translate(-20px, 15px) rotate(270deg) scale(1.08);
        }
    }

    @keyframes floatWave {
        0%, 100% {
            transform: translate(0, 0) scale(1);
        }
        33% {
            transform: translate(15px, -15px) scale(1.1);
        }
        66% {
            transform: translate(-15px, 15px) scale(0.95);
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


def create_service_page(service_name, slug):
    """Create service page with FULL index.html design"""

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Expert {service_name.lower()} in Toronto • Same-day service • 90-day warranty • Licensed technicians • Call {GLOBAL_DATA['phone']} for fast reliable service!">
    <meta name="keywords" content="{service_name.lower()} Toronto, {service_name.lower()} near me, appliance repair Toronto">
    <title>{service_name} Toronto | Same Day | Save $40 - Nika</title>

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
                "addressLocality": "Toronto",
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
        "areaServed": "Toronto, ON"
    }}
    </script>

    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {{
                "@type": "Question",
                "name": "How quickly can you come for {service_name.lower()}?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "We offer same-day {service_name.lower()} service when our schedule permits. Call {GLOBAL_DATA['phone']} for our earliest available time slot in Toronto and the GTA."
                }}
            }},
            {{
                "@type": "Question",
                "name": "How much does {service_name.lower()} cost in Toronto?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "We charge {GLOBAL_DATA['diagnostic_fee']} for diagnosis {GLOBAL_DATA['diagnostic_note']}. Most {service_name.lower()} repairs cost {GLOBAL_DATA['repair_range']} plus parts with upfront pricing."
                }}
            }},
            {{
                "@type": "Question",
                "name": "Do you offer a warranty on {service_name.lower()} repairs?",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "Yes! All {service_name.lower()} repairs come with our comprehensive {GLOBAL_DATA['warranty']} warranty covering both parts and labor for complete peace of mind."
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

    <!-- Hero Section with Floating Icons Background - EXACTLY like index.html -->
    <section class="hero-section">
        {FLOATING_ICONS_HTML}
        <div class="container">
            <div class="hero-content">
                <div class="hero-text">
                    <h1 class="hero-title">
                        Professional <span class="highlight-yellow">{service_name}</span> in Toronto & GTA
                    </h1>
                    <p class="hero-subtitle">Same-day service • {GLOBAL_DATA['warranty']} warranty • All brands</p>
                    <p class="hero-trust-text">✅ No Hidden Fees - Ever! • Licensed & Insured • {GLOBAL_DATA['years_experience']} Years Experience</p>
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

    <!-- AI Summary Box Section - Light gray background -->
    <section class="section bg-light-gray">
        <div class="container">
            <div class="ai-summary-box" style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border-left: 4px solid #0ea5e9; padding: 2rem; border-radius: 8px; margin: 2rem 0;">
                <h3 style="color: #0ea5e9; margin-top: 0;">Quick Summary - AI-Optimized</h3>
                <p style="font-size: 1.1rem; line-height: 1.7;">Need {service_name.lower()} in <a href="../locations/toronto.html">Toronto</a>? Nika Appliance Repair provides same-day {service_name.lower()} service with a {GLOBAL_DATA['warranty']} warranty. Licensed technicians fix all major brands. Call {GLOBAL_DATA['phone']} for {GLOBAL_DATA['diagnostic_fee']} diagnosis {GLOBAL_DATA['diagnostic_note']}. Most repairs cost {GLOBAL_DATA['repair_range']} plus parts with upfront pricing. We serve <a href="../locations/mississauga.html">Mississauga</a>, <a href="../locations/brampton.html">Brampton</a>, <a href="../locations/vaughan.html">Vaughan</a>, and all GTA.</p>
            </div>
        </div>
    </section>

    <!-- Main Content Section - White background -->
    <section class="section bg-white">
        <div class="container" style="max-width: 900px;">
            <img src="../assets/images/friendly-technician-character.png" alt="{service_name} Service Professional" style="width: 100%; max-width: 600px; margin: 2rem auto; display: block; border-radius: 8px;" />

            <h2>Why Choose Nika for {service_name} in Toronto?</h2>
            <p>When you need {service_name.lower()} in <a href="../locations/toronto.html">Toronto</a>, <a href="../locations/north-york.html">North York</a>, <a href="../locations/scarborough.html">Scarborough</a>, <a href="../locations/etobicoke.html">Etobicoke</a>, or anywhere in the GTA, you need fast reliable service from licensed professionals. Nika Appliance Repair has been serving the Greater Toronto Area for over {GLOBAL_DATA['years_experience']} years with a perfect track record of {GLOBAL_DATA['completion_count']} successful repairs. Our expert technicians specialize in {service_name.lower()} for all major brands including LG, Samsung, Whirlpool, GE, Maytag, Frigidaire, KitchenAid, and Bosch appliances. We understand that appliance breakdowns disrupt your daily routine which is why we offer same-day {service_name.lower()} service when our schedule permits in <a href="../locations/mississauga.html">Mississauga</a>, <a href="../locations/brampton.html">Brampton</a>, <a href="../locations/vaughan.html">Vaughan</a>, <a href="../locations/markham.html">Markham</a>, and <a href="../locations/richmond-hill.html">Richmond Hill</a>.</p>

            <img src="../assets/images/friendly-technician-character.png" alt="Common {service_name} Problems" style="width: 100%; max-width: 600px; margin: 2rem auto; display: block; border-radius: 8px;" />

            <h2>Common {service_name} Problems We Fix in Toronto</h2>
            <p>Our experienced {service_name.lower()} technicians have seen and fixed thousands of appliance issues across Toronto and the GTA. Here are the most common problems we encounter with {service_name.lower()} that require professional diagnosis and repair from our licensed insured technicians who carry comprehensive liability insurance for your protection and peace of mind during every service call in your Toronto or GTA home or business location.</p>

            <h3>Appliances Not Operating Properly</h3>
            <p>When your appliance isn't working as it should for {service_name.lower()}, it could be due to electrical issues mechanical failures or control board problems that require expert diagnosis. Our technicians use advanced diagnostic tools to quickly identify the root cause of your {service_name.lower()} problem. We carry most common parts in our service vehicles allowing us to complete {service_name.lower()} repairs on the first visit in most cases across Toronto Mississauga Brampton Vaughan Markham Richmond Hill Etobicoke Scarborough and North York. This saves you time and gets your appliance back to working condition faster with our {GLOBAL_DATA['warranty']} warranty.</p>

            <h3>Strange Noises and Unusual Sounds</h3>
            <p>Grinding squeaking banging or humming noises from your appliance often indicate worn bearings loose components or motor issues that need {service_name.lower()} attention. These sounds shouldn't be ignored as they can lead to more serious damage if left unaddressed in your Toronto or GTA home. Our {service_name.lower()} technicians can identify the source of the noise and recommend the most cost-effective solution whether it's a simple adjustment or a component replacement with our {GLOBAL_DATA['warranty']} parts and labor warranty for complete peace of mind.</p>

            <img src="../assets/images/friendly-technician-character.png" alt="{service_name} Repair Process" style="width: 100%; max-width: 600px; margin: 2rem auto; display: block; border-radius: 8px;" />

            <h3>Leaking Water or Moisture Issues</h3>
            <p>Water leaks from your appliance can cause significant damage to your floors and cabinetry if not addressed quickly with professional {service_name.lower()} service. Common causes include worn seals clogged drain lines or damaged hoses that our technicians can diagnose and repair. We'll locate the source of the leak explain the problem clearly and provide an upfront quote for the {service_name.lower()} repair in your Toronto Mississauga Brampton or other GTA location. Our {GLOBAL_DATA['warranty']} warranty gives you confidence that the repair will last and you won't face the same problem again within {GLOBAL_DATA['warranty']} period.</p>

            <h3>Not Heating or Cooling Correctly</h3>
            <p>Temperature issues with your appliance can stem from faulty thermostats heating elements compressors or control systems that require expert {service_name.lower()} diagnosis. These problems require professional evaluation to avoid replacing expensive components unnecessarily which is why our Toronto and GTA customers trust Nika Appliance Repair for honest transparent {service_name.lower()} service. Our technicians test all related systems to pinpoint the exact issue ensuring you only pay for the {service_name.lower()} repairs you actually need with no hidden fees or surprise charges ever.</p>

            <h2>Our {service_name} Process in Toronto & GTA</h2>
            <p>We've perfected our {service_name.lower()} repair process over {GLOBAL_DATA['years_experience']} years to provide the best possible service to our Toronto Mississauga Brampton Vaughan Markham Richmond Hill Etobicoke Scarborough and North York customers who trust us for professional {service_name.lower()} service.</p>

            <div class="ai-summary-box" style="background: linear-gradient(135deg, #fff5e1 0%, #ffe4b5 100%); border-left: 4px solid #ff9800; padding: 2rem; border-radius: 8px; margin: 2rem 0;">
                <h3 style="color: #ff9800; margin-top: 0;">Step-by-Step {service_name} Repair Process</h3>
                <p><strong>Step 1 - Call or Book Online for {service_name}:</strong> Contact us at {GLOBAL_DATA['phone']} or use our online booking form below for {service_name.lower()} service. We'll schedule a convenient time offering same-day {service_name.lower()} service when available in your Toronto or GTA location.</p>
                <p><strong>Step 2 - Diagnostic Visit:</strong> Our licensed {service_name.lower()} technician arrives with a fully stocked service vehicle. We diagnose the issue using professional-grade tools and provide a detailed explanation of the problem with your appliance.</p>
                <p><strong>Step 3 - Upfront Quote:</strong> Before any {service_name.lower()} work begins you'll receive a clear written quote. We charge {GLOBAL_DATA['diagnostic_fee']} for the diagnosis which is waived when you proceed with the {service_name.lower()} repair.</p>
                <p><strong>Step 4 - Expert Repair:</strong> Once approved we complete the {service_name.lower()} repair using high-quality OEM or equivalent parts. Most {service_name.lower()} repairs are completed during the first visit in Toronto and the GTA.</p>
                <p><strong>Step 5 - Testing & Warranty:</strong> We thoroughly test the appliance to ensure it's working perfectly after {service_name.lower()} service. All repairs come with our {GLOBAL_DATA['warranty']} parts and labor warranty.</p>
            </div>

            <img src="../assets/images/friendly-technician-character.png" alt="{service_name} Pricing Toronto" style="width: 100%; max-width: 600px; margin: 2rem auto; display: block; border-radius: 8px;" />

            <h2>Transparent {service_name} Pricing in Toronto</h2>
            <p>We believe in transparent upfront pricing with no hidden fees for our {service_name.lower()} service in Toronto and the GTA. Here's exactly what you can expect when you choose Nika Appliance Repair for professional {service_name.lower()} service in your home or business location across the Greater Toronto Area including all major neighborhoods and suburbs.</p>

            <h3>Diagnostic Fee for {service_name}: {GLOBAL_DATA['diagnostic_fee']}</h3>
            <p>Our {service_name.lower()} diagnostic visit includes a thorough inspection of your appliance identification of all issues and a detailed explanation of what's wrong with clear communication. If you decide to proceed with the {service_name.lower()} repair we waive this fee entirely. This means you only pay for the {service_name.lower()} repair itself not for us to tell you what's wrong with your appliance in your Toronto Mississauga Brampton Vaughan or other GTA home.</p>

            <h3>{service_name} Repair Costs: {GLOBAL_DATA['repair_range']} Plus Parts</h3>
            <p>Most {service_name.lower()} jobs in Toronto and the GTA fall within the {GLOBAL_DATA['repair_range']} range for labor plus the cost of any necessary parts for your specific appliance brand and model. Complex {service_name.lower()} repairs may cost more but we'll always provide a complete quote before starting work. We source high-quality parts at competitive prices and pass those savings on to you for affordable {service_name.lower()} service across Toronto and the GTA with our {GLOBAL_DATA['warranty']} warranty.</p>

            <h3>No Hidden Fees or Surprises with {service_name}</h3>
            <p>What we quote for {service_name.lower()} is what you pay. There are no trip charges no weekend surcharges and no surprise fees for {service_name.lower()} service in Toronto or the GTA. If we discover additional issues during the {service_name.lower()} repair we'll discuss them with you and get your approval before proceeding. You're always in control of the {service_name.lower()} repair process and costs with complete transparency from Nika Appliance Repair.</p>

            <img src="../assets/images/friendly-technician-character.png" alt="{service_name} Service Areas GTA" style="width: 100%; max-width: 600px; margin: 2rem auto; display: block; border-radius: 8px;" />

            <h2>{service_name} Service Areas Across Toronto & GTA</h2>
            <p>We proudly serve all of Toronto and the Greater Toronto Area with professional {service_name.lower()} service. Our central location allows us to reach customers quickly across the region for same-day {service_name.lower()} service when our schedule permits.</p>

            <p><strong><a href="../locations/toronto.html">Toronto</a> {service_name}:</strong> From downtown Entertainment District to the Beaches we serve all Toronto neighborhoods with fast {service_name.lower()} response times and our {GLOBAL_DATA['warranty']} warranty.</p>

            <p><strong><a href="../locations/north-york.html">North York</a> & <a href="../locations/scarborough.html">Scarborough</a> {service_name}:</strong> Complete {service_name.lower()} coverage of Toronto's northern and eastern areas with licensed insured technicians.</p>

            <p><strong><a href="../locations/etobicoke.html">Etobicoke</a> {service_name}:</strong> Serving western Toronto with the same quality {service_name.lower()} service and {GLOBAL_DATA['warranty']} warranty we're known for.</p>

            <p><strong><a href="../locations/mississauga.html">Mississauga</a> <a href="../locations/brampton.html">Brampton</a> <a href="../locations/vaughan.html">Vaughan</a> {service_name}:</strong> Full {service_name.lower()} service coverage throughout Peel and York regions.</p>

            <p><strong><a href="../locations/markham.html">Markham</a> & <a href="../locations/richmond-hill.html">Richmond Hill</a> {service_name}:</strong> Expert {service_name.lower()} service for all of York Region's eastern communities.</p>

            <img src="../assets/images/friendly-technician-character.png" alt="Why Choose Nika for {service_name}" style="width: 100%; max-width: 600px; margin: 2rem auto; display: block; border-radius: 8px;" />

            <h2>What Makes Our {service_name} Service Different?</h2>
            <p>There are many appliance repair companies offering {service_name.lower()} in Toronto but Nika Appliance Repair stands out for several important reasons that our {GLOBAL_DATA['completion_count']} satisfied customers across the GTA have experienced firsthand with our professional {service_name.lower()} service.</p>

            <h3>Licensed and Insured {service_name} Technicians</h3>
            <p>All our {service_name.lower()} technicians are fully licensed and carry comprehensive liability insurance for your protection during every service call. This protects you and your property during every {service_name.lower()} visit. We invest heavily in ongoing training to keep our {service_name.lower()} team current with the latest appliance technologies and repair techniques for all major brands in Toronto and the GTA.</p>

            <h3>Same-Day {service_name} Service When Available</h3>
            <p>We understand that appliance breakdowns requiring {service_name.lower()} are urgent and disruptive. That's why we maintain a flexible schedule and offer same-day {service_name.lower()} service whenever possible in Toronto and the GTA. For emergency situations like refrigerators not cooling or water leaks we prioritize your {service_name.lower()} call and get to you as quickly as possible.</p>

            <h3>{GLOBAL_DATA['warranty']} Parts and Labor Warranty on {service_name}</h3>
            <p>Our comprehensive {GLOBAL_DATA['warranty']} warranty on {service_name.lower()} covers both parts and labor. If the same issue occurs again within {GLOBAL_DATA['warranty']} after your {service_name.lower()} repair we'll return and fix it at no additional cost. This {service_name.lower()} warranty demonstrates our confidence in the quality of our work across Toronto and the GTA.</p>

            <h3>Upfront {service_name} Pricing and Transparent Communication</h3>
            <p>We provide detailed quotes before starting any {service_name.lower()} work in your Toronto or GTA home. You'll know exactly what the {service_name.lower()} repair will cost with no hidden fees or surprise charges. If we discover additional issues during {service_name.lower()} service we'll discuss them with you and get your approval before proceeding with complete honesty.</p>

            <h3>Rated {GLOBAL_DATA['rating']} by {GLOBAL_DATA['review_count']} Customers for {service_name}</h3>
            <p>Our {GLOBAL_DATA['rating']} rating from {GLOBAL_DATA['review_count']} verified customers speaks to our commitment to quality {service_name.lower()} service in Toronto and the GTA. We've completed over {GLOBAL_DATA['completion_count']} successful repairs across the GTA building a reputation for reliability and expertise in {service_name.lower()} that our customers trust and recommend to their friends and family.</p>

            <h2>Book Your {service_name} Appointment in Toronto</h2>
            <p>Ready to get your appliance fixed with professional {service_name.lower()} service? Call us at {GLOBAL_DATA['phone']} or fill out the form below to schedule your {service_name.lower()} service appointment in Toronto or anywhere in the GTA. We'll respond quickly and provide you with our earliest available time slot for same-day {service_name.lower()} service when our schedule permits.</p>

            <!-- Contact Form -->
            <div style="background: #f8fafc; padding: 2rem; border-radius: 8px; margin: 2rem 0;" id="book">
                <h3>Quick {service_name} Service Request Form</h3>
                <form style="max-width: 600px; margin: 0 auto;">
                    <div style="margin-bottom: 1rem;">
                        <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Your Name *</label>
                        <input type="text" required style="width: 100%; padding: 0.75rem; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 1rem;" />
                    </div>
                    <div style="margin-bottom: 1rem;">
                        <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Phone Number *</label>
                        <input type="tel" required style="width: 100%; padding: 0.75rem; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 1rem;" />
                    </div>
                    <div style="margin-bottom: 1rem;">
                        <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Email Address</label>
                        <input type="email" style="width: 100%; padding: 0.75rem; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 1rem;" />
                    </div>
                    <div style="margin-bottom: 1rem;">
                        <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Service Needed</label>
                        <select style="width: 100%; padding: 0.75rem; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 1rem;">
                            <option>{service_name}</option>
                            <option>Other Service</option>
                        </select>
                    </div>
                    <div style="margin-bottom: 1rem;">
                        <label style="display: block; margin-bottom: 0.5rem; font-weight: 500;">What's the problem?</label>
                        <textarea rows="4" style="width: 100%; padding: 0.75rem; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 1rem;"></textarea>
                    </div>
                    <button type="submit" class="cta-primary" style="width: 100%;">Request {service_name} Service Call</button>
                </form>
            </div>
        </div>
    </section>

    <!-- FAQ Section - Light gray background -->
    <section class="section bg-light-gray">
        <div class="container" style="max-width: 900px;">
            <h2 style="text-align: center;">Frequently Asked Questions About {service_name}</h2>

            <div style="max-width: 800px; margin: 2rem auto;">
                <h3>How quickly can you come for {service_name.lower()} in Toronto?</h3>
                <p>We offer same-day {service_name.lower()} service when our schedule permits in Toronto and the GTA. For emergencies like refrigerators not cooling or water leaks we prioritize urgent situations. Call {GLOBAL_DATA['phone']} and we'll give you our earliest available time slot. Most of our customers in Toronto Mississauga Brampton Vaughan and the GTA can expect {service_name.lower()} service within 24-48 hours with our {GLOBAL_DATA['warranty']} warranty.</p>

                <h3>How much does {service_name.lower()} cost in Toronto?</h3>
                <p>We charge {GLOBAL_DATA['diagnostic_fee']} for diagnosis {GLOBAL_DATA['diagnostic_note']}. Most {service_name.lower()} repairs cost {GLOBAL_DATA['repair_range']} plus parts. We provide upfront pricing before starting work - no hidden fees! The final cost depends on the specific issue and required parts but we'll always give you a complete quote before proceeding with {service_name.lower()} service.</p>

                <h3>Do you offer a warranty on {service_name.lower()} repairs?</h3>
                <p>Yes! All {service_name.lower()} repairs come with our comprehensive {GLOBAL_DATA['warranty']} warranty covering both parts and labor. If the same issue occurs within {GLOBAL_DATA['warranty']} we'll fix it at no additional charge. This {service_name.lower()} warranty gives you peace of mind that your repair will last.</p>

                <h3>What appliance brands do you repair for {service_name.lower()}?</h3>
                <p>We repair all major appliance brands for {service_name.lower()} including LG Samsung Whirlpool GE Maytag Frigidaire KitchenAid Bosch Electrolux Kenmore and many others. Our {service_name.lower()} technicians are trained on the latest models and technologies from all manufacturers.</p>

                <h3>Are you licensed and insured for {service_name.lower()}?</h3>
                <p>Absolutely! All our {service_name.lower()} technicians are fully licensed and we carry comprehensive liability insurance for your protection and peace of mind. We also conduct background checks on all our {service_name.lower()} technicians for your safety.</p>

                <h3>What areas do you service for {service_name.lower()}?</h3>
                <p>We service all of Toronto and the Greater Toronto Area for {service_name.lower()} including Toronto Mississauga Brampton Vaughan Markham Richmond Hill Etobicoke Scarborough and North York. Call us to confirm we serve your specific location for {service_name.lower()} service.</p>

                <h3>Do you charge extra for evenings or weekends for {service_name.lower()}?</h3>
                <p>Our standard rates apply during our regular {service_name.lower()} service hours {GLOBAL_DATA['service_hours']}. We don't add surprise surcharges for {service_name.lower()} - what we quote is what you pay.</p>

                <h3>How do I prepare for your {service_name.lower()} visit?</h3>
                <p>Simply clear access to the appliance and have any relevant information ready for {service_name.lower()} (model number age symptoms). Our {service_name.lower()} technicians bring all necessary tools and common parts so you don't need to do anything special to prepare.</p>
            </div>
        </div>
    </section>

    <!-- CTA Section - Blue gradient -->
    <section class="section bg-blue-gradient" style="text-align: center; padding: 4rem 0;">
        <div class="container">
            <h2 style="color: white;">Need {service_name} in Toronto?</h2>
            <p style="color: white; font-size: 1.2rem; margin-bottom: 2rem;">Call now for same-day service when available!</p>
            <a href="{GLOBAL_DATA['phone_href']}" class="cta-primary">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
                    <path d="M20.01 15.38c-1.23 0-2.42-.2-3.53-.56a.977.977 0 00-1.01.24l-1.57 1.97c-2.83-1.35-5.48-3.9-6.89-6.83l1.95-1.66c.27-.28.35-.67.24-1.02-.37-1.11-.56-2.3-.56-3.53 0-.54-.45-.99-.99-.99H4.19C3.65 3 3 3.24 3 3.99 3 13.28 10.73 21 20.01 21c.71 0 .99-.63.99-1.18v-3.45c0-.54-.45-.99-.99-.99z"/>
                </svg>
                Call {GLOBAL_DATA['phone']}
            </a>
        </div>
    </section>

    <!-- Footer - Dark blue -->
    <footer class="main-footer bg-dark-blue">
        <div class="container">
            <div class="footer-content" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; padding: 3rem 0;">
                <div>
                    <h3>Nika Appliance Repair</h3>
                    <p>Phone: <a href="{GLOBAL_DATA['phone_href']}">{GLOBAL_DATA['phone']}</a></p>
                    <p>Hours: {GLOBAL_DATA['service_hours']}</p>
                    <p>Serving Toronto & GTA</p>
                </div>
                <div>
                    <h4>Our Services</h4>
                    <ul style="list-style: none; padding: 0;">
                        <li><a href="dishwasher-repair.html">Dishwasher Repair</a></li>
                        <li><a href="refrigerator-freezer-repair.html">Refrigerator Repair</a></li>
                        <li><a href="washer-dryer-repair.html">Washer & Dryer Repair</a></li>
                        <li><a href="oven-stove-repair.html">Oven & Stove Repair</a></li>
                        <li><a href="dishwasher-installation.html">Dishwasher Installation</a></li>
                    </ul>
                </div>
                <div>
                    <h4>Service Areas</h4>
                    <ul style="list-style: none; padding: 0;">
                        <li><a href="../locations/toronto.html">Toronto</a></li>
                        <li><a href="../locations/mississauga.html">Mississauga</a></li>
                        <li><a href="../locations/brampton.html">Brampton</a></li>
                        <li><a href="../locations/vaughan.html">Vaughan</a></li>
                        <li><a href="../locations/markham.html">Markham</a></li>
                    </ul>
                </div>
            </div>
            <div style="text-align: center; padding: 2rem 0; border-top: 1px solid rgba(255,255,255,0.1);">
                <p>&copy; 2025 Nika Appliance Repair. Licensed & Insured | {GLOBAL_DATA['warranty']} Warranty</p>
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


SERVICES = [
    ("Dishwasher Repair", "dishwasher-repair"),
    ("Refrigerator & Freezer Repair", "refrigerator-freezer-repair"),
    ("Washer & Dryer Repair", "washer-dryer-repair"),
    ("Oven & Stove Repair", "oven-stove-repair"),
    ("Dishwasher Installation", "dishwasher-installation")
]


def main():
    print("="*60)
    print("FULL DESIGN GENERATOR - Using index.html design")
    print("="*60)

    services_dir = "services"
    os.makedirs(services_dir, exist_ok=True)

    for service_name, slug in SERVICES:
        filename = f"{services_dir}/{slug}.html"
        html = create_service_page(service_name, slug)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"[OK] {filename}")

    print(f"\n[SUCCESS] Generated {len(SERVICES)} pages with FULL index.html design")
    print("- All CSS files from index.html")
    print("- Floating SVG icons with animations")
    print("- Exact gradients and colors")
    print("- Same header/footer design")
    print("- Real images from assets/images")
    print("- 1800+ words per page")
    print("- AI summary boxes")
    print("- FAQ schema")
    print("- 15+ internal links")
    print("- Contact forms")
    print("\nReady for BMAD testing!")

if __name__ == "__main__":
    main()
