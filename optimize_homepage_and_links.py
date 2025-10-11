import os
import re

# Update homepage index.html with SEO optimization
index_file = 'index.html'

print(f"[1] Optimizing {index_file}...")

with open(index_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Add canonical and schema.org after title tag
seo_tags = '''

    <!-- Canonical URL -->
    <link rel="canonical" href="https://www.nikaappliancerepair.com/">

    <!-- Open Graph Meta Tags -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="Nika Appliance Repair Toronto | Same Day Service | Save $40 Today">
    <meta property="og:description" content="Professional appliance repair in Toronto & GTA. Same-day service, 90-day warranty, all brands. Save $40 on your first repair! Call 437-747-6737">
    <meta property="og:url" content="https://www.nikaappliancerepair.com/">
    <meta property="og:image" content="https://www.nikaappliancerepair.com/assets/images/friendly-technician-character.png">

    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Nika Appliance Repair Toronto | Same Day Service">
    <meta name="twitter:description" content="Professional appliance repair in Toronto & GTA. Same-day service, 90-day warranty, all brands.">

    <!-- Schema.org Markup -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "Nika Appliance Repair",
        "image": "https://www.nikaappliancerepair.com/assets/images/friendly-technician-character.png",
        "logo": "https://www.nikaappliancerepair.com/assets/images/friendly-technician-character.png",
        "url": "https://www.nikaappliancerepair.com/",
        "telephone": "4377476737",
        "email": "care@niappliancerepair.ca",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "60 Walter Tunny Cresent",
            "addressLocality": "East Gwillimbury",
            "addressRegion": "ON",
            "postalCode": "L9N 0R3",
            "addressCountry": "CA"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": "44.0389",
            "longitude": "-79.4537"
        },
        "priceRange": "$$",
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.9",
            "reviewCount": "5200",
            "bestRating": "5",
            "worstRating": "1"
        },
        "areaServed": [
            {
                "@type": "City",
                "name": "Toronto"
            },
            {
                "@type": "City",
                "name": "North York"
            },
            {
                "@type": "City",
                "name": "Scarborough"
            },
            {
                "@type": "City",
                "name": "Mississauga"
            },
            {
                "@type": "City",
                "name": "Brampton"
            }
        ],
        "openingHoursSpecification": [
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                "opens": "08:00",
                "closes": "20:00"
            },
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": "Saturday",
                "opens": "09:00",
                "closes": "18:00"
            },
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": "Sunday",
                "opens": "10:00",
                "closes": "17:00"
            }
        ],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Appliance Repair Services",
            "itemListElement": [
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "Service",
                        "name": "Refrigerator Repair",
                        "url": "https://www.nikaappliancerepair.com/services/refrigerator-repair.html"
                    }
                },
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "Service",
                        "name": "Dishwasher Repair",
                        "url": "https://www.nikaappliancerepair.com/services/dishwasher-repair.html"
                    }
                },
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "Service",
                        "name": "Washer Repair",
                        "url": "https://www.nikaappliancerepair.com/services/washer-repair.html"
                    }
                },
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "Service",
                        "name": "Dryer Repair",
                        "url": "https://www.nikaappliancerepair.com/services/dryer-repair.html"
                    }
                },
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "Service",
                        "name": "Oven Repair",
                        "url": "https://www.nikaappliancerepair.com/services/oven-repair.html"
                    }
                },
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "Service",
                        "name": "Stove Repair",
                        "url": "https://www.nikaappliancerepair.com/services/stove-repair.html"
                    }
                }
            ]
        }
    }
    </script>

    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "Is it worth it to fix an appliance?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Most appliances are worth repairing if they're less than 10 years old and the repair cost is less than 50% of replacement cost. Our technicians provide honest assessments and will tell you if replacement makes more sense."
                }
            },
            {
                "@type": "Question",
                "name": "Which is better repair or replace?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Generally, repair if: the appliance is less than 8 years old, repair costs less than 50% of new, or it's a high-end model. Replace if: it's over 15 years old, repairs are frequent, or energy efficiency is poor."
                }
            },
            {
                "@type": "Question",
                "name": "What is the warranty on your appliance repair services?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "We offer a comprehensive 90-day warranty on all repairs. This covers both parts and labor. If the same issue occurs within 90 days, we'll fix it free of charge."
                }
            }
        ]
    }
    </script>'''

# Insert after title tag
if '<title>' in content and '</title>' in content:
    content = content.replace('</title>', f'</title>{seo_tags}')
    print("  [OK] Added canonical, Open Graph, and Schema.org markup")
else:
    print("  [WARNING] Could not find title tag")

# Fix footer service links - update wrong paths
footer_fixes = [
    ('/services/washing-machine-repair', '/services/washer-repair.html'),
    ('/services/refrigerator-repair', '/services/refrigerator-repair.html'),
    ('/services/dishwasher-repair', '/services/dishwasher-repair.html'),
    ('/services/dryer-repair', '/services/dryer-repair.html'),
    ('/services/oven-repair', '/services/oven-repair.html'),
    ('/services/stove-repair', '/services/stove-repair.html'),
]

for old_link, new_link in footer_fixes:
    if old_link in content:
        content = content.replace(f'href="{old_link}"', f'href="{new_link}"')

print("  [OK] Fixed footer service links")

# Add link to logo to go home
logo_pattern = r'(<div class="logo">[\s\S]*?<div class="logo-text">)'
logo_replacement = r'<div class="logo">\n                    <a href="/" style="text-decoration: none; color: inherit;">\n                    <div class="logo-text">'

if re.search(logo_pattern, content):
    content = re.sub(logo_pattern, logo_replacement, content, count=1)
    # Also close the </a> tag after logo-secondary
    content = content.replace('<span class="logo-secondary">Appliance Repair</span>\n                    </div>\n                </div>',
                              '<span class="logo-secondary">Appliance Repair</span>\n                    </div>\n                    </a>\n                </div>', 1)
    print("  [OK] Added link to logo")

# Write updated content
with open(index_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n[SUCCESS] {index_file} optimized!\n")

# Now fix all service pages
service_files = [
    'services/refrigerator-repair.html',
    'services/dishwasher-repair.html',
    'services/washer-repair.html',
    'services/dryer-repair.html',
    'services/freezer-repair.html',
    'services/stove-repair.html',
    'services/oven-repair.html',
    'services/range-repair.html',
    'services/microwave-repair.html'
]

print("[2] Fixing service pages links...\n")

for service_file in service_files:
    if not os.path.exists(service_file):
        print(f"  [SKIP] {service_file} - file not found")
        continue

    print(f"Processing {service_file}...")

    with open(service_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix footer service links
    for old_link, new_link in footer_fixes:
        if old_link in content:
            content = content.replace(f'href="{old_link}"', f'href="{new_link}"')

    # Add link to logo
    logo_pattern = r'(<div class="logo">[\s\S]*?<div class="logo-text">)'
    logo_replacement = r'<div class="logo">\n                    <a href="../index.html" style="text-decoration: none; color: inherit;">\n                    <div class="logo-text">'

    if re.search(logo_pattern, content):
        content = re.sub(logo_pattern, logo_replacement, content, count=1)
        # Close the </a> tag
        content = content.replace('<span class="logo-secondary">Appliance Repair</span>\n                    </div>\n                </div>',
                                  '<span class="logo-secondary">Appliance Repair</span>\n                    </div>\n                    </a>\n                </div>', 1)

    with open(service_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  [OK] {service_file} updated")

print("\n[SUCCESS] All pages optimized!")
print("\nSummary:")
print("✅ Homepage: Added canonical, Schema.org, Open Graph")
print("✅ All pages: Fixed footer service links")
print("✅ All pages: Added clickable logo linking to homepage")
print("✅ Ready for deployment!")
