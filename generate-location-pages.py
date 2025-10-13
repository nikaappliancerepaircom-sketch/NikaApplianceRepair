#!/usr/bin/env python3
"""
Location Pages Generator for Nika Appliance Repair
Generates individual SEO-optimized pages for each service area
"""

import os
import re
from pathlib import Path

# All 61 GTA locations from index.html
LOCATIONS = [
    {"slug": "ajax", "name": "Ajax"},
    {"slug": "aurora", "name": "Aurora"},
    {"slug": "agincourt", "name": "Agincourt"},
    {"slug": "bayview-glen", "name": "Bayview Glen"},
    {"slug": "berczy-village", "name": "Berczy Village"},
    {"slug": "beverley-glen", "name": "Beverley Glen"},
    {"slug": "bradford", "name": "Bradford"},
    {"slug": "beverley-acres", "name": "Beverley Acres"},
    {"slug": "brampton", "name": "Brampton"},
    {"slug": "cachet", "name": "Cachet"},
    {"slug": "cathedraltown", "name": "Cathedraltown"},
    {"slug": "calgary", "name": "Calgary"},
    {"slug": "concord", "name": "Concord"},
    {"slug": "don-valley-village", "name": "Don Valley Village"},
    {"slug": "elgin-mills", "name": "Elgin Mills"},
    {"slug": "east-gwillimbury", "name": "East Gwillimbury"},
    {"slug": "east-york", "name": "East York"},
    {"slug": "edmonton", "name": "Edmonton"},
    {"slug": "etobicoke", "name": "Etobicoke"},
    {"slug": "greensborough", "name": "Greensborough"},
    {"slug": "gta", "name": "GTA"},
    {"slug": "gormley", "name": "Gormley"},
    {"slug": "hillcrest-village", "name": "Hillcrest village"},
    {"slug": "innisfil", "name": "Innisfil"},
    {"slug": "king-city", "name": "King City"},
    {"slug": "kleinburg", "name": "Kleinburg"},
    {"slug": "holland-landing", "name": "Holland Landing"},
    {"slug": "langstaff", "name": "Langstaff"},
    {"slug": "lamoreaux", "name": "Lamoreaux"},
    {"slug": "maple", "name": "Maple"},
    {"slug": "markham", "name": "Markham"},
    {"slug": "mount-albert", "name": "Mount Albert"},
    {"slug": "milliken", "name": "Milliken"},
    {"slug": "mississauga", "name": "Mississauga"},
    {"slug": "newmarket", "name": "Newmarket"},
    {"slug": "north-york", "name": "North York"},
    {"slug": "oak-ridges", "name": "Oak-Ridges"},
    {"slug": "oakville", "name": "Oakville"},
    {"slug": "oshawa", "name": "Oshawa"},
    {"slug": "pickering", "name": "Pickering"},
    {"slug": "richmond-hill", "name": "Richmond Hill"},
    {"slug": "richvale", "name": "Richvale"},
    {"slug": "raymerville-markville-east", "name": "Raymerville Markville East"},
    {"slug": "steeles", "name": "Steeles"},
    {"slug": "scarborough", "name": "Scarborough"},
    {"slug": "schomberg", "name": "Schomberg"},
    {"slug": "stouffville", "name": "Stouffville"},
    {"slug": "thornhill", "name": "Thornhill"},
    {"slug": "toronto", "name": "Toronto"},
    {"slug": "unionville", "name": "Unionville"},
    {"slug": "uxbridge", "name": "Uxbridge"},
    {"slug": "vaughan", "name": "Vaughan"},
    {"slug": "whitby", "name": "Whitby"},
    {"slug": "woodbridge", "name": "Woodbridge"},
    {"slug": "wismer-commons", "name": "Wismer Commons"},
    {"slug": "yongehurst", "name": "Yongehurst"},
    {"slug": "burlington", "name": "Burlington"},
    {"slug": "milton", "name": "Milton"},
    {"slug": "georgetown", "name": "Georgetown"},
    {"slug": "halton-hills", "name": "Halton Hills"},
]

def read_template():
    """Read the main index.html as template"""
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

def customize_for_location(template, location):
    """Customize template for specific location"""
    slug = location['slug']
    name = location['name']

    html = template

    # 1. Update meta description
    html = re.sub(
        r'<meta name="description" content="[^"]*"',
        f'<meta name="description" content="Appliance repair in {name}, Ontario. Same-day service, 90-day warranty, all major brands. Save $40 on your first repair! Call 437-747-6737 for fast service"',
        html
    )

    # 2. Update title
    html = re.sub(
        r'<title>[^<]*</title>',
        f'<title>Appliance Repair {name} | Same Day Service | Save $40 | Nika</title>',
        html
    )

    # 3. Update canonical URL
    html = re.sub(
        r'<link rel="canonical" href="[^"]*"',
        f'<link rel="canonical" href="https://nikaappliancerepair.com/locations/{slug}"',
        html
    )

    # 4. Update Open Graph
    html = re.sub(
        r'<meta property="og:title" content="[^"]*"',
        f'<meta property="og:title" content="Nika Appliance Repair {name} | Same Day Service"',
        html
    )
    html = re.sub(
        r'<meta property="og:description" content="[^"]*"',
        f'<meta property="og:description" content="Professional appliance repair in {name}. Same-day service, 90-day warranty, all brands. Call 437-747-6737"',
        html
    )
    html = re.sub(
        r'<meta property="og:url" content="[^"]*"',
        f'<meta property="og:url" content="https://nikaappliancerepair.com/locations/{slug}"',
        html
    )

    # 5. Update Twitter Card
    html = re.sub(
        r'<meta name="twitter:title" content="[^"]*"',
        f'<meta name="twitter:title" content="Nika Appliance Repair {name} | Same Day Service"',
        html
    )
    html = re.sub(
        r'<meta name="twitter:description" content="[^"]*"',
        f'<meta name="twitter:description" content="Professional appliance repair in {name}. Same-day service, 90-day warranty, all brands."',
        html
    )

    # 6. Update Schema.org - add addressLocality
    html = re.sub(
        r'"addressLocality":\s*"[^"]*"',
        f'"addressLocality": "{name}"',
        html
    )

    # 7. Update Hero H1 - make it location-specific
    html = re.sub(
        r'We\'re the <span class="highlight-yellow">appliance</span><br>\s*repair company that<br>\s*will <span class="highlight-yellow">make</span> you say\.\.\.<br>\s*<span class="wow-text">WOW!</span>',
        f'Professional <span class="highlight-yellow">Appliance</span><br>Repair in <span class="highlight-yellow">{name}</span><br>Same Day Service<br><span class="wow-text">Save $40!</span>',
        html
    )

    # 8. Update AI Summary Box with location
    html = re.sub(
        r'<h2 class="text-blue text-2xl font-semibold mb-4" style="margin-bottom: 1\.5rem;">Quick Answer: Appliance Repair Toronto</h2>',
        f'<h2 class="text-blue text-2xl font-semibold mb-4" style="margin-bottom: 1.5rem;">Quick Answer: Appliance Repair {name}</h2>',
        html
    )

    html = re.sub(
        r'<strong>Need appliance repair in Toronto\?</strong>',
        f'<strong>Need appliance repair in {name}?</strong>',
        html
    )

    html = re.sub(
        r'We serve Toronto, Mississauga, Brampton, and 60\+ GTA areas',
        f'We serve {name} and surrounding areas in GTA',
        html
    )

    # 9. Update "Near Me" section
    html = re.sub(
        r'<h2 style="text-align: center; font-size: 1\.6rem; color: #212529; margin-bottom: 1\.5rem;">Looking for "Appliance Repair Near Me"\?</h2>',
        f'<h2 style="text-align: center; font-size: 1.6rem; color: #212529; margin-bottom: 1.5rem;">Appliance Repair Services in {name}</h2>',
        html
    )

    # 10. Update location-specific keywords in "Near Me" cards
    html = re.sub(
        r'refrigerator repair Toronto today',
        f'refrigerator repair {name} today',
        html
    )
    html = re.sub(
        r'washing machine repair near me Toronto',
        f'washing machine repair near me {name}',
        html
    )
    html = re.sub(
        r'dishwasher repair service Toronto',
        f'dishwasher repair service {name}',
        html
    )
    html = re.sub(
        r'dryer repair Toronto same day',
        f'dryer repair {name} same day',
        html
    )
    html = re.sub(
        r'oven repair Toronto fast service',
        f'oven repair {name} fast service',
        html
    )
    html = re.sub(
        r'appliance repair service open now Toronto',
        f'appliance repair service open now {name}',
        html
    )

    # 11. Update CSS/JS paths to go up one level (we're in /locations/)
    html = re.sub(r'href="css/', 'href="../css/', html)
    html = re.sub(r'src="js/', 'src="../js/', html)
    html = re.sub(r'src="assets/', 'src="../assets/', html)

    # 12. Update navigation links to go back to root
    html = re.sub(r'href="#', 'href="../#', html)
    html = re.sub(r'href="/', 'href="../', html)
    # Fix double slashes
    html = re.sub(r'href="\.\./\.\.\/', 'href="../', html)

    # 13. Add location-specific breadcrumb schema
    breadcrumb_schema = f'''
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {{
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": "https://nikaappliancerepair.com/"
            }},
            {{
                "@type": "ListItem",
                "position": 2,
                "name": "Service Areas",
                "item": "https://nikaappliancerepair.com/#areas"
            }},
            {{
                "@type": "ListItem",
                "position": 3,
                "name": "{name}",
                "item": "https://nikaappliancerepair.com/locations/{slug}"
            }}
        ]
    }}
    </script>'''

    # Insert breadcrumb before </head>
    html = html.replace('</head>', f'{breadcrumb_schema}\n</head>')

    return html

def generate_all_pages():
    """Generate all location pages"""
    print("Starting location pages generation...")
    print(f"Total locations: {len(LOCATIONS)}")

    # Create locations directory
    locations_dir = Path('locations')
    locations_dir.mkdir(exist_ok=True)
    print(f"Created directory: {locations_dir}")

    # Read template
    print("Reading template from index.html...")
    template = read_template()

    # Generate each location page
    for i, location in enumerate(LOCATIONS, 1):
        slug = location['slug']
        name = location['name']

        print(f"[{i}/{len(LOCATIONS)}] Generating: {name} ({slug})...")

        # Customize template
        html = customize_for_location(template, location)

        # Write file
        output_file = locations_dir / f'{slug}.html'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"    Created: {output_file}")

    print("\n" + "="*60)
    print(f"SUCCESS! Generated {len(LOCATIONS)} location pages!")
    print("="*60)
    print(f"\nLocation: {locations_dir.absolute()}")
    print(f"Example URLs:")
    print(f"   - https://nikaappliancerepair.com/locations/toronto")
    print(f"   - https://nikaappliancerepair.com/locations/mississauga")
    print(f"   - https://nikaappliancerepair.com/locations/brampton")

if __name__ == '__main__':
    generate_all_pages()
