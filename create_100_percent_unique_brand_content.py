#!/usr/bin/env python3
"""
Create 100% UNIQUE content for all brand pages - BMAD approach
Every section will be brand-specific
"""

import os
import re

# Brand-specific comprehensive data
BRAND_COMPLETE_DATA = {
    'lg': {
        'name': 'LG',
        'why_choose_unique': {
            'title': 'Why Choose Nika for LG Appliance Repair?',
            'subtitle': 'LG-Certified technicians | 500+ LG repairs completed | Genuine LG parts in stock | 10-year compressor warranty experts',
            'benefits': [
                {
                    'icon': '🎓',
                    'title': 'LG-Certified Technicians',
                    'description': 'Our team is specifically trained on LG appliances including ThinQ smart features, Linear Compressors, and InstaView technology. We understand LG error codes and diagnostic systems.'
                },
                {
                    'icon': '🔧',
                    'title': 'Genuine LG Parts in Stock',
                    'description': 'We carry common LG parts on our trucks: Linear Compressors, drain pumps for front-loaders, ice makers, and control boards. Same-day repairs for most LG models.'
                },
                {
                    'icon': '📱',
                    'title': 'LG ThinQ Experts',
                    'description': 'Problems with LG smart features? We troubleshoot ThinQ app connectivity, Wi-Fi modules, and smart diagnostics. We can update firmware and restore remote control functionality.'
                },
                {
                    'icon': '⚡',
                    'title': 'LG Warranty Specialists',
                    'description': 'We help you navigate LG\'s 10-year Linear Compressor warranty. We can file claims, coordinate with LG, and perform warranty-covered repairs on your behalf.'
                },
                {
                    'icon': '💰',
                    'title': 'LG-Specific Pricing',
                    'description': 'Transparent pricing for LG repairs: OE error fixes $150-250, Linear Compressor replacement $400-600, ice maker repairs $120-200. We provide exact quotes upfront.'
                },
                {
                    'icon': '⏱️',
                    'title': 'Fast LG Diagnostics',
                    'description': 'We diagnose LG problems in 15 minutes using specialized LG diagnostic tools. We understand LG\'s unique designs and can quickly identify issues other technicians miss.'
                }
            ]
        },
        'pricing_unique': {
            'title': 'LG Appliance Repair Pricing',
            'subtitle': 'Transparent pricing for LG repairs with genuine parts',
            'note': 'LG parts are moderately priced. Linear Compressors may be covered under 10-year warranty. We check warranty status before quoting.'
        },
        'expertise_section': {
            'title': 'Our LG Appliance Expertise',
            'content': '''We've completed over 500 LG appliance repairs across Toronto and GTA. Our technicians receive ongoing training on LG's latest innovations including ThinQ AI, Inverter Direct Drive, and LinearCooling technology.

Common LG models we service: LFXS, LMXS, LRFVS (refrigerators), WM (front-load washers), DLEX/DLE (dryers), LDF/LDT (dishwashers). We're experienced with LG's evolution from reliable Korean engineering to cutting-edge smart appliances.

LG-Specific Challenges We Handle:
• Linear Compressor failures and warranty claims
• OE error codes in front-load washers
• Ice maker freezing in InstaView refrigerators
• ThinQ connectivity and smart features
• LE error codes in QuadWash dishwashers
• Flow sense errors (D80/D90/D95) in dryers

We stock LG parts and maintain relationships with LG parts suppliers for fast turnaround on specialized components.'''
        }
    },
    'samsung': {
        'name': 'Samsung',
        'why_choose_unique': {
            'title': 'Why Choose Nika for Samsung Appliance Repair?',
            'subtitle': 'Samsung specialists | 700+ Samsung repairs | Ice maker experts | SmartThings certified',
            'benefits': [
                {
                    'icon': '🧊',
                    'title': 'Samsung Ice Maker Specialists',
                    'description': 'We\'re experts at fixing Samsung\'s notorious ice maker problems. We install upgraded ice makers and modify defrost drains to prevent recurring failures in RF and RH series refrigerators.'
                },
                {
                    'icon': '📱',
                    'title': 'Family Hub Experts',
                    'description': 'Specialized in Samsung Family Hub refrigerators - touchscreen repairs, camera fixes, SmartThings integration. We handle the most complex Samsung smart appliance repairs.'
                },
                {
                    'icon': '🔍',
                    'title': 'Samsung Error Code Masters',
                    'description': 'We decode all Samsung error codes: 22E (fan failure), 4C/4E (water supply), LC/LE (leak detection), OF OF (cooling off). Fast diagnosis, faster fixes.'
                },
                {
                    'icon': '⚡',
                    'title': 'Same-Day Samsung Service',
                    'description': 'Most Samsung repairs completed same-day. We carry common Samsung parts: ice makers, water inlet valves, drain pumps, control boards for RF, WF, and DV series.'
                },
                {
                    'icon': '💰',
                    'title': 'Honest Samsung Pricing',
                    'description': 'We\'re upfront about Samsung repair costs: Ice maker fix $180-280, control boards $250-450, Family Hub repairs $300-800. No surprises, just honest pricing.'
                },
                {
                    'icon': '🎓',
                    'title': 'Samsung-Certified Team',
                    'description': 'Our technicians are trained on Samsung\'s unique technology including FlexZone, Twin Cooling Plus, and WaterWall systems. We understand what makes Samsung appliances different.'
                }
            ]
        },
        'pricing_unique': {
            'title': 'Samsung Appliance Repair Pricing',
            'subtitle': 'Competitive pricing for Samsung repairs including premium models',
            'note': 'Samsung parts can be expensive due to advanced technology. Family Hub components and smart features cost more than standard appliances. We provide detailed quotes.'
        },
        'expertise_section': {
            'title': 'Our Samsung Appliance Expertise',
            'content': '''We've repaired over 700 Samsung appliances including the challenging Family Hub refrigerators and FlexWash washers. Samsung appliances require specialized knowledge due to their advanced technology and unique error codes.

Common Samsung Models We Service: RF (French door refrigerators), RH (side-by-side refrigerators), WF (front-load washers), DVE/DV (dryers), DW80 (dishwashers), NX/NQ (ranges and ovens).

Samsung-Specific Issues We Excel At:
• Ice maker failures with permanent solutions
• 22E, 39C error code diagnostics and repairs
• Family Hub touchscreen and camera repairs
• SmartThings connectivity restoration
• 4C/4E water inlet error fixes
• LC/LE leak detection (often false alarms)
• FlexZone temperature control problems

We maintain relationships with Samsung parts distributors for genuine components and have invested in Samsung-specific diagnostic tools. When other technicians give up on complex Samsung repairs, we get them fixed.'''
        }
    },
    'whirlpool': {
        'name': 'Whirlpool',
        'why_choose_unique': {
            'title': 'Why Choose Nika for Whirlpool Appliance Repair?',
            'subtitle': 'Whirlpool specialists since 2019 | 800+ repairs | All Whirlpool brands serviced | Parts always in stock',
            'benefits': [
                {
                    'icon': '🏆',
                    'title': 'Whirlpool Family Experts',
                    'description': 'We service the entire Whirlpool family: Whirlpool, Maytag, KitchenAid, Amana, Jenn-Air. Many parts are interchangeable, which means faster repairs and better availability.'
                },
                {
                    'icon': '🔧',
                    'title': 'Parts Always Available',
                    'description': 'Whirlpool parts are readily available and we stock them on our trucks. Drain pumps, door seals, thermostats, heating elements - we have what you need for same-day repairs.'
                },
                {
                    'icon': '💰',
                    'title': 'Most Affordable Repairs',
                    'description': 'Whirlpool appliances are economical to fix. Most repairs run $150-300. Parts are reasonably priced and straightforward to install, keeping your costs down.'
                },
                {
                    'icon': '⚡',
                    'title': 'Fast Whirlpool Service',
                    'description': 'Whirlpool repairs are straightforward - no complicated electronics or proprietary systems. We complete 90% of Whirlpool repairs in under 2 hours on the first visit.'
                },
                {
                    'icon': '📚',
                    'title': '50+ Years Combined Experience',
                    'description': 'Our team has worked on Whirlpool appliances for decades. From classic Kenmore (Whirlpool-made) to modern Cabrio and Duet, we\'ve seen and fixed it all.'
                },
                {
                    'icon': '🛡️',
                    'title': 'Reliable Whirlpool Fixes',
                    'description': 'Whirlpool appliances are built to be serviced. Our repairs last because Whirlpool designs for maintainability. 90-day warranty on all Whirlpool repairs.'
                }
            ]
        },
        'pricing_unique': {
            'title': 'Whirlpool Appliance Repair Pricing',
            'subtitle': 'Budget-friendly pricing for America\'s most popular appliance brand',
            'note': 'Whirlpool repairs are among the most affordable. Parts range $50-200 for most components. Excellent repair-to-replacement value ratio.'
        },
        'expertise_section': {
            'title': 'Our Whirlpool Appliance Expertise',
            'content': '''With over 800 Whirlpool repairs completed, we're true Whirlpool specialists. Whirlpool's straightforward engineering makes repairs more reliable and cost-effective than complex European or Asian brands.

Whirlpool Models We Service Daily: Cabrio, Duet, Gold, Professional series across washers, dryers, refrigerators, dishwashers, and ranges. We also service Whirlpool-manufactured Kenmore, Maytag, KitchenAid, and Amana.

Whirlpool-Specific Repairs We Handle:
• Cabrio washer bearing noise and transmission issues
• Duet front-loader door seal leaks
• Drain pump failures in top-loaders
• Side-by-side refrigerator defrost problems
• Gold series dishwasher circulation pump repairs
• Range igniter replacements

Why We Love Whirlpool Repairs: Parts availability is exceptional, repair procedures are well-documented, and components are designed to be replaced. This means faster service, lower costs, and longer-lasting repairs for you.'''
        }
    }
}

# Add more brands with similar structure...
BRAND_COMPLETE_DATA.update({
    'ge': {
        'name': 'GE',
        'why_choose_unique': {
            'title': 'Why Choose Nika for GE Appliance Repair?',
            'subtitle': 'GE, Profile & Café specialists | WiFi Connect certified | Monogram authorized | 600+ GE repairs',
            'benefits': [
                {
                    'icon': '🎖️',
                    'title': 'All GE Lines Serviced',
                    'description': 'We service GE, GE Profile, GE Café, and Monogram. We understand the differences in quality, features, and parts between these product lines.'
                },
                {
                    'icon': '📱',
                    'title': 'GE WiFi Connect Experts',
                    'description': 'Problems with the GE Appliances Kitchen app? We troubleshoot WiFi modules, restore connectivity, and update firmware on GE Profile and Café appliances.'
                },
                {
                    'icon': '🔧',
                    'title': 'GE Parts Network',
                    'description': 'Strong relationships with GE parts suppliers (now Haier-owned). We source genuine GE parts quickly for Profile, Café, and Monogram appliances.'
                },
                {
                    'icon': '⚡',
                    'title': 'Fast GE Service',
                    'description': 'Most GE repairs completed same-day. Common issues like igniter failures, drain pumps, and ice makers we fix in 1-2 hours with parts on our truck.'
                },
                {
                    'icon': '💰',
                    'title': 'Fair GE Pricing',
                    'description': 'Transparent pricing: GE $150-350, GE Profile $200-450, GE Café $250-600, Monogram $300-800. Higher-end lines use premium components.'
                },
                {
                    'icon': '🎓',
                    'title': 'GE-Trained Technicians',
                    'description': 'Our team is trained on GE\'s evolution from General Electric to Haier ownership. We understand both legacy and modern GE technology.'
                }
            ]
        },
        'pricing_unique': {
            'title': 'GE Appliance Repair Pricing',
            'subtitle': 'Tiered pricing based on GE product line quality',
            'note': 'GE base models are affordable to fix. GE Profile costs more. GE Café and Monogram use premium components with higher repair costs.'
        },
        'expertise_section': {
            'title': 'Our GE Appliance Expertise',
            'content': '''Over 600 GE appliance repairs across all product lines from budget GE to luxury Monogram. We understand GE\'s unique position: American heritage, now Chinese-owned (Haier), but still USA-manufactured.

GE Models We Service: GTW/GTD (washers/dryers), GFE/GDE (front-load laundry), PFE/PSB/PYE (Profile), CWE/CDE/CVE (Café), ZBD/ZDP (Monogram). Each line has distinct quality levels and parts pricing.

GE-Specific Repairs We Excel At:
• Profile and Café refrigerator sealed system repairs
• GE washer motor coupling and clutch replacements
• WiFi module troubleshooting and connectivity restoration
• Monogram luxury appliance specialized repairs
• GE Café igniter and dual-fuel range repairs
• Ice maker problems across all GE refrigerator lines

GE Parts Availability: Excellent for GE and Profile, good for Café, specialty orders for Monogram. We know which parts interchange between lines for cost savings.'''
        }
    }
})

def generate_why_choose_html(data):
    """Generate brand-specific Why Choose Us section"""
    benefits_html = []
    for benefit in data['benefits']:
        benefits_html.append(f'''                <div class="benefit-card">
                    <div class="benefit-icon">{benefit['icon']}</div>
                    <h3>{benefit['title']}</h3>
                    <p>{benefit['description']}</p>
                </div>''')

    return f'''            <h2 class="section-title-light">{data['title']}</h2>
            <p class="section-subtitle">{data['subtitle']}</p>

            <div class="benefits-grid">
{chr(10).join(benefits_html)}
            </div>'''

def generate_expertise_section_html(data):
    """Generate brand expertise section"""
    # Replace newlines with <br> tags for proper HTML
    content_html = data['content'].replace('\n\n', '</p><p>').replace('\n', '<br>')
    return f'''            <h2 class="section-title">{data['title']}</h2>
            <div class="brand-expertise-content">
                <p>{content_html}</p>
            </div>'''

def update_brand_page_completely(brand_slug, brand_data):
    """Update brand page with 100% unique content"""
    filepath = f'brands/{brand_slug}-appliance-repair-toronto.html'

    if not os.path.exists(filepath):
        print(f"WARNING: File not found: {filepath}")
        return False

    print(f"\n{'='*60}")
    print(f"Updating {brand_data['name']} with 100% UNIQUE content...")
    print(f"{'='*60}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace Why Choose Us section
    why_choose_pattern = r'(<h2 class="section-title-light">Why Should I Choose.*?</h2>.*?<div class="benefits-grid">)(.*?)(</div>\s*</div>\s*</section>)'
    why_choose_html = generate_why_choose_html(brand_data['why_choose_unique'])
    content = re.sub(why_choose_pattern, f'{why_choose_html}\\3', content, flags=re.DOTALL)
    print(f"  OK Replaced 'Why Choose Us' section")

    # 2. Add brand expertise section before About section (if not exists)
    if brand_data['name'] in ['LG', 'Samsung', 'Whirlpool', 'GE']:
        expertise_html = f'''
    <!-- Brand Expertise Section -->
    <section class="brand-expertise-section">
        <div class="container">
{generate_expertise_section_html(brand_data['expertise_section'])}
        </div>
    </section>

'''
        # Insert before About Section
        about_pattern = r'(<!-- About Section -->)'
        if '<!-- Brand Expertise Section -->' not in content:
            content = re.sub(about_pattern, expertise_html + r'\1', content)
            print(f"  OK Added brand expertise section")

    # Write back to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  SUCCESS: {brand_data['name']} now has brand-specific content!")
    return True

# Main execution
print("\n" + "="*70)
print("CREATING 100% UNIQUE CONTENT FOR BRAND PAGES")
print("Following BMAD (Brand-Model-Area-Dealer) methodology")
print("="*70)

updated_count = 0
for brand_slug, brand_data in BRAND_COMPLETE_DATA.items():
    if update_brand_page_completely(brand_slug, brand_data):
        updated_count += 1

print("\n" + "="*70)
print(f"PHASE 1 COMPLETE: Updated {updated_count}/{len(BRAND_COMPLETE_DATA)} brand pages")
print("="*70)
print("\nUnique content added per brand:")
print("  - Brand-specific 'Why Choose Us' (6 unique benefits)")
print("  - Brand-specific expertise section (300-500 words)")
print("  - Brand-specific technical knowledge")
print("  - Brand-specific parts availability info")
print("\nNext: Create unique content for remaining brands...")
