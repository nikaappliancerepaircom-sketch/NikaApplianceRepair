#!/usr/bin/env python3
"""
Blog Post Generator for Keyword Gap Opportunities
Part of BMAD v2 Auto-Posting System

Generates SEO-optimized blog posts targeting keyword gaps identified via DataForSEO
"""

import os
from pathlib import Path
from datetime import datetime, timedelta

# Blog post topics based on keyword gap analysis
# Format: (slug, title, category, target_keyword, search_volume)
KEYWORD_GAP_POSTS = [
    # High priority - 800+ search volume
    ("lg-dishwasher-troubleshooting-codes", "LG Dishwasher Error Codes: Complete Troubleshooting Guide Toronto", "troubleshooting", "lg dishwasher troubleshooting codes", 880),
    ("fix-gas-oven-not-heating", "How to Fix a Gas Oven Not Heating: Toronto Repair Guide", "troubleshooting", "fix gas oven", 880),

    # Medium-high priority - 500+ search volume
    ("dishwasher-leaking-from-bottom", "Dishwasher Leaking From Bottom: Causes & Fixes Toronto", "troubleshooting", "dishwasher leaking", 590),
    ("lg-appliance-repair-toronto", "LG Appliance Repair Toronto: Complete Service Guide", "guides", "lg appliance repair", 590),
    ("samsung-ice-maker-not-making-ice", "Samsung Ice Maker Not Making Ice: Troubleshooting Guide", "troubleshooting", "samsung ice maker not making ice", 590),

    # Medium priority - 300+ search volume
    ("whirlpool-dishwasher-not-cleaning", "Whirlpool Dishwasher Not Cleaning Dishes Properly: Solutions", "troubleshooting", "whirlpool dishwasher not cleaning", 320),
    ("kenmore-refrigerator-repair-guide", "Kenmore Refrigerator Repair: Common Issues & Solutions Toronto", "guides", "kenmore refrigerator repair", 260),
    ("dryer-not-heating-troubleshooting", "Dryer Not Heating? Complete Troubleshooting Guide Toronto", "troubleshooting", "dryer not heating", 240),
    ("washing-machine-not-spinning", "Washing Machine Not Spinning: Causes & DIY Fixes", "troubleshooting", "washing machine not spinning", 220),
    ("refrigerator-not-cooling-properly", "Refrigerator Not Cooling: Emergency Repair Guide Toronto", "troubleshooting", "refrigerator not cooling", 200),

    # Standard priority - branded/specific keywords
    ("oven-not-heating-evenly", "Oven Not Heating Evenly: Calibration & Repair Tips", "troubleshooting", "oven not heating evenly", 180),
    ("dishwasher-not-draining-completely", "Dishwasher Not Draining: Quick Fixes & When to Call Pro", "troubleshooting", "dishwasher not draining", 170),
    ("freezer-making-loud-noise", "Freezer Making Loud Noise: Diagnosis & Repair Toronto", "troubleshooting", "freezer making noise", 160),
    ("washer-leaking-from-bottom", "Washer Leaking From Bottom: Common Causes & Solutions", "troubleshooting", "washer leaking from bottom", 150),
    ("gas-stove-burner-not-igniting", "Gas Stove Burner Not Igniting: Safety & Repair Guide", "troubleshooting", "stove burner not igniting", 140),
    ("ice-maker-troubleshooting-guide", "Ice Maker Troubleshooting: Complete Repair Guide Toronto", "troubleshooting", "ice maker troubleshooting", 130),
    ("dryer-making-squeaking-noise", "Dryer Making Squeaking Noise: Causes & Fixes", "troubleshooting", "dryer squeaking noise", 120),
    ("refrigerator-compressor-problems", "Refrigerator Compressor Problems: Signs & Repair Options", "troubleshooting", "refrigerator compressor problems", 110),
    ("dishwasher-soap-dispenser-not-opening", "Dishwasher Soap Dispenser Not Opening: Easy Fixes", "troubleshooting", "dishwasher soap dispenser not opening", 100),
    ("washing-machine-error-codes-guide", "Washing Machine Error Codes: Complete Brand Guide Toronto", "guides", "washing machine error codes", 200),
]

def generate_post_content(slug, title, category, keyword, volume):
    """Generate full blog post HTML content"""

    # Generate meta description
    meta_desc = f"Expert {keyword} repair in Toronto. Professional troubleshooting guide with step-by-step solutions. Same-day service available. Call (437) 747-1010."

    # Determine appliance type from slug
    appliance = "appliance"
    if "dishwasher" in slug:
        appliance = "dishwasher"
    elif "refrigerator" in slug or "freezer" in slug:
        appliance = "refrigerator"
    elif "dryer" in slug:
        appliance = "dryer"
    elif "washer" in slug or "washing" in slug:
        appliance = "washing machine"
    elif "oven" in slug or "stove" in slug:
        appliance = "oven"
    elif "ice-maker" in slug:
        appliance = "ice maker"

    # Generate common issues based on appliance type
    issues_content = generate_issues_section(appliance, keyword)

    # Generate DIY tips
    diy_content = generate_diy_section(appliance, keyword)

    # Generate when to call pro section
    pro_content = generate_pro_section(appliance)

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Nika Appliance Repair</title>
    <meta name="description" content="{meta_desc[:160]}">
    <meta name="keywords" content="{keyword}, toronto {appliance} repair, {appliance} troubleshooting, appliance repair toronto">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;500;600;700&family=Rubik:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="/css/blog-premium.css">
    <link rel="canonical" href="https://nikaappliancerepair.com/blog/{category}/{slug}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{meta_desc[:160]}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://nikaappliancerepair.com/blog/{category}/{slug}">
    <meta property="article:published_time" content="{datetime.now().strftime('%Y-%m-%d')}">

    <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title}",
  "author": {{
    "@type": "Organization",
    "name": "Nika Appliance Repair",
    "url": "https://nikaappliancerepair.com"
  }},
  "publisher": {{
    "@type": "LocalBusiness",
    "name": "Nika Appliance Repair",
    "telephone": "+1-437-747-1010",
    "address": {{
      "@type": "PostalAddress",
      "addressLocality": "Toronto",
      "addressRegion": "ON",
      "addressCountry": "CA"
    }}
  }},
  "datePublished": "{datetime.now().strftime('%Y-%m-%d')}",
  "dateModified": "{datetime.now().strftime('%Y-%m-%d')}",
  "mainEntityOfPage": {{
    "@type": "WebPage",
    "@id": "https://nikaappliancerepair.com/blog/{category}/{slug}"
  }}
}}
    </script>

    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        :root {{
            --cool-blue-primary: #2193b0;
            --cool-blue-secondary: #6dd5ed;
            --cool-blue-dark: #1a7a91;
            --charcoal: #2C3E50;
            --pure-white: #FFFFFF;
            --off-white: #F8FAFB;
            --light-gray: #F5F7FA;
        }}
        body {{
            font-family: 'Rubik', sans-serif;
            background: var(--light-gray);
            color: var(--charcoal);
            line-height: 1.7;
        }}
        .header {{
            background: linear-gradient(135deg, var(--cool-blue-primary), var(--cool-blue-secondary));
            padding: 1rem 2rem;
            position: sticky;
            top: 0;
            z-index: 1000;
        }}
        .header-content {{
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .logo {{
            font-family: 'Fredoka', sans-serif;
            font-size: 1.5rem;
            font-weight: 700;
            color: white;
            text-decoration: none;
        }}
        .header-cta {{
            background: white;
            color: var(--cool-blue-primary);
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            transition: transform 0.2s;
        }}
        .header-cta:hover {{ transform: translateY(-2px); }}

        .hero-section {{
            background: linear-gradient(135deg, var(--cool-blue-primary), var(--cool-blue-secondary));
            padding: 4rem 2rem;
            text-align: center;
            color: white;
        }}
        .hero-content {{ max-width: 900px; margin: 0 auto; }}
        .hero-badge {{
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }}
        .hero-title {{
            font-family: 'Fredoka', sans-serif;
            font-size: clamp(2rem, 5vw, 3rem);
            margin-bottom: 1rem;
        }}
        .hero-meta {{
            display: flex;
            justify-content: center;
            gap: 2rem;
            flex-wrap: wrap;
            opacity: 0.9;
        }}

        .breadcrumb {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 1rem 2rem;
            font-size: 0.9rem;
        }}
        .breadcrumb a {{ color: var(--cool-blue-primary); text-decoration: none; }}
        .breadcrumb a:hover {{ text-decoration: underline; }}

        .main-content {{
            max-width: 900px;
            margin: 2rem auto;
            padding: 0 2rem;
        }}
        .content-card {{
            background: white;
            border-radius: 16px;
            padding: 3rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            margin-bottom: 2rem;
        }}
        h2 {{
            font-family: 'Fredoka', sans-serif;
            font-size: 1.75rem;
            color: var(--charcoal);
            margin: 2rem 0 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid var(--cool-blue-secondary);
        }}
        h3 {{
            font-size: 1.25rem;
            color: var(--cool-blue-dark);
            margin: 1.5rem 0 0.75rem;
        }}
        p {{ margin-bottom: 1rem; }}
        ul, ol {{
            margin: 1rem 0;
            padding-left: 2rem;
        }}
        li {{ margin-bottom: 0.5rem; }}

        .tip-box {{
            background: linear-gradient(135deg, #e8f4f8 0%, #d1ecf1 100%);
            border-left: 4px solid var(--cool-blue-primary);
            padding: 1.5rem;
            border-radius: 0 12px 12px 0;
            margin: 1.5rem 0;
        }}
        .tip-box h4 {{
            color: var(--cool-blue-dark);
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .warning-box {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 1.5rem;
            border-radius: 0 12px 12px 0;
            margin: 1.5rem 0;
        }}
        .warning-box h4 {{
            color: #856404;
            margin-bottom: 0.5rem;
        }}

        .cta-section {{
            background: linear-gradient(135deg, var(--cool-blue-primary), var(--cool-blue-dark));
            color: white;
            padding: 3rem;
            border-radius: 16px;
            text-align: center;
            margin: 2rem 0;
        }}
        .cta-section h3 {{
            font-family: 'Fredoka', sans-serif;
            font-size: 1.75rem;
            color: white;
            margin-bottom: 1rem;
        }}
        .cta-button {{
            display: inline-block;
            background: white;
            color: var(--cool-blue-primary);
            padding: 1rem 2rem;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 700;
            font-size: 1.1rem;
            margin-top: 1rem;
            transition: transform 0.2s;
        }}
        .cta-button:hover {{ transform: translateY(-3px); }}

        .footer {{
            background: #1a202c;
            color: white;
            padding: 3rem 2rem;
            text-align: center;
        }}
        .footer a {{ color: #93c5fd; }}

        @media (max-width: 768px) {{
            .content-card {{ padding: 1.5rem; }}
            .hero-section {{ padding: 2rem 1rem; }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <a href="/" class="logo">Nika Appliance Repair</a>
            <a href="tel:+14377471010" class="header-cta">
                <i class="fas fa-phone"></i> (437) 747-1010
            </a>
        </div>
    </header>

    <section class="hero-section">
        <div class="hero-content">
            <span class="hero-badge"><i class="fas fa-tools"></i> {category.title()} Guide</span>
            <h1 class="hero-title">{title}</h1>
            <div class="hero-meta">
                <span><i class="fas fa-calendar"></i> {datetime.now().strftime('%B %d, %Y')}</span>
                <span><i class="fas fa-clock"></i> 8 min read</span>
                <span><i class="fas fa-map-marker-alt"></i> Toronto, ON</span>
            </div>
        </div>
    </section>

    <nav class="breadcrumb">
        <a href="/">Home</a> &gt;
        <a href="/blog-nika-appliance-repair.html">Blog</a> &gt;
        <a href="/blog-nika-appliance-repair.html?category={category}">{category.title()}</a> &gt;
        <span>{title[:50]}...</span>
    </nav>

    <main class="main-content">
        <article class="content-card">
            <p>Is your <strong>{appliance}</strong> giving you trouble? You're not alone. As Toronto's trusted appliance repair experts, we see <strong>{keyword}</strong> issues every day. This comprehensive guide will help you diagnose the problem and decide whether it's a DIY fix or time to call a professional.</p>

            <div class="tip-box">
                <h4><i class="fas fa-lightbulb"></i> Quick Tip</h4>
                <p>Before attempting any repairs, always unplug your {appliance} and turn off relevant utilities. Safety first!</p>
            </div>

            {issues_content}

            {diy_content}

            {pro_content}

            <div class="cta-section">
                <h3>Need Professional Help?</h3>
                <p>Our certified technicians are available for same-day service across Toronto and the GTA.</p>
                <a href="tel:+14377471010" class="cta-button">
                    <i class="fas fa-phone"></i> Call (437) 747-1010
                </a>
            </div>

            <h2>Why Choose Nika Appliance Repair?</h2>
            <ul>
                <li><strong>Same-Day Service</strong> - We understand emergencies can't wait</li>
                <li><strong>Certified Technicians</strong> - Factory-trained on all major brands</li>
                <li><strong>Transparent Pricing</strong> - No hidden fees, upfront quotes</li>
                <li><strong>90-Day Warranty</strong> - All repairs backed by our guarantee</li>
                <li><strong>Serving All Toronto</strong> - From Downtown to North York, Scarborough to Etobicoke</li>
            </ul>

            <h2>Areas We Serve</h2>
            <p>We provide <strong>{keyword}</strong> services throughout the Greater Toronto Area including:</p>
            <ul>
                <li>Downtown Toronto</li>
                <li>North York</li>
                <li>Scarborough</li>
                <li>Etobicoke</li>
                <li>Mississauga</li>
                <li>Vaughan</li>
                <li>Richmond Hill</li>
                <li>Markham</li>
            </ul>
        </article>
    </main>

    <footer class="footer">
        <p>&copy; {datetime.now().year} Nika Appliance Repair Toronto. All rights reserved.</p>
        <p>Licensed & Insured | <a href="/services.html">Services</a> | <a href="/locations.html">Service Areas</a> | <a href="/blog-nika-appliance-repair.html">Blog</a></p>
    </footer>

    <script src="/js/header.js"></script>
</body>
</html>'''

    return html_content


def generate_issues_section(appliance, keyword):
    """Generate common issues section based on appliance type"""

    issues_map = {
        "dishwasher": '''
            <h2>Common Dishwasher Problems</h2>
            <h3>1. Dishes Not Getting Clean</h3>
            <p>If your dishwasher isn't cleaning properly, check:</p>
            <ul>
                <li>Spray arms for clogs or debris</li>
                <li>Water temperature (should be 120°F minimum)</li>
                <li>Detergent dispenser functionality</li>
                <li>Filter cleanliness</li>
            </ul>

            <h3>2. Water Drainage Issues</h3>
            <p>Standing water after a cycle often indicates:</p>
            <ul>
                <li>Clogged drain hose</li>
                <li>Faulty drain pump</li>
                <li>Garbage disposal connection blocked</li>
                <li>Check valve problems</li>
            </ul>

            <h3>3. Error Code Display</h3>
            <p>Modern dishwashers display error codes to help diagnose issues. Common codes indicate problems with water inlet, drainage, heating, or door latch.</p>
        ''',
        "refrigerator": '''
            <h2>Common Refrigerator Problems</h2>
            <h3>1. Not Cooling Properly</h3>
            <p>When your fridge isn't maintaining temperature:</p>
            <ul>
                <li>Check condenser coils for dust buildup</li>
                <li>Verify door seals are intact</li>
                <li>Ensure vents aren't blocked</li>
                <li>Listen for compressor operation</li>
            </ul>

            <h3>2. Ice Maker Issues</h3>
            <p>Ice maker problems often stem from:</p>
            <ul>
                <li>Water supply line frozen or kinked</li>
                <li>Faulty water inlet valve</li>
                <li>Ice maker assembly failure</li>
                <li>Freezer temperature too warm</li>
            </ul>

            <h3>3. Strange Noises</h3>
            <p>Unusual sounds may indicate compressor issues, fan problems, or ice buildup in the freezer section.</p>
        ''',
        "dryer": '''
            <h2>Common Dryer Problems</h2>
            <h3>1. Not Heating</h3>
            <p>A dryer that tumbles but doesn't heat usually has:</p>
            <ul>
                <li>Faulty heating element</li>
                <li>Broken thermal fuse</li>
                <li>Defective gas igniter (gas dryers)</li>
                <li>Clogged lint screen or vent</li>
            </ul>

            <h3>2. Takes Too Long to Dry</h3>
            <p>Extended drying times often result from:</p>
            <ul>
                <li>Restricted airflow in the vent system</li>
                <li>Overloading the dryer</li>
                <li>Moisture sensor malfunction</li>
                <li>Failing heating components</li>
            </ul>

            <h3>3. Unusual Noises</h3>
            <p>Squeaking, thumping, or grinding sounds may indicate worn drum rollers, damaged belt, or failing motor bearings.</p>
        ''',
        "washing machine": '''
            <h2>Common Washing Machine Problems</h2>
            <h3>1. Won't Spin</h3>
            <p>A washer that fills but won't spin may have:</p>
            <ul>
                <li>Unbalanced load</li>
                <li>Worn drive belt</li>
                <li>Faulty lid switch (top-load)</li>
                <li>Door latch issues (front-load)</li>
            </ul>

            <h3>2. Leaking Water</h3>
            <p>Water leaks commonly originate from:</p>
            <ul>
                <li>Damaged door boot seal (front-load)</li>
                <li>Loose hose connections</li>
                <li>Cracked tub or pump</li>
                <li>Detergent overflow</li>
            </ul>

            <h3>3. Error Codes</h3>
            <p>Modern washers display codes for drainage issues, water fill problems, motor errors, and sensor failures.</p>
        ''',
        "oven": '''
            <h2>Common Oven Problems</h2>
            <h3>1. Not Heating Properly</h3>
            <p>When your oven won't reach temperature:</p>
            <ul>
                <li>Faulty bake or broil element</li>
                <li>Defective temperature sensor</li>
                <li>Control board malfunction</li>
                <li>Gas igniter issues (gas ovens)</li>
            </ul>

            <h3>2. Uneven Heating</h3>
            <p>Hot spots or uneven baking often indicate:</p>
            <ul>
                <li>Convection fan problems</li>
                <li>Temperature calibration needed</li>
                <li>Damaged heating element</li>
                <li>Door seal issues</li>
            </ul>

            <h3>3. Ignition Problems (Gas)</h3>
            <p>If your gas oven won't ignite, check the igniter glow, gas supply, and safety valve operation.</p>
        ''',
        "ice maker": '''
            <h2>Common Ice Maker Problems</h2>
            <h3>1. Not Making Ice</h3>
            <p>When ice production stops completely:</p>
            <ul>
                <li>Water supply line frozen or disconnected</li>
                <li>Faulty water inlet valve</li>
                <li>Ice maker control arm stuck</li>
                <li>Freezer temperature too high</li>
            </ul>

            <h3>2. Small or Hollow Ice Cubes</h3>
            <p>Undersized cubes often indicate:</p>
            <ul>
                <li>Low water pressure</li>
                <li>Clogged water filter</li>
                <li>Partially blocked inlet valve</li>
            </ul>

            <h3>3. Ice Tastes Bad</h3>
            <p>Off-tasting ice usually means the water filter needs replacement or the ice storage bin needs cleaning.</p>
        ''',
    }

    return issues_map.get(appliance, '''
            <h2>Common Issues</h2>
            <p>Every appliance can develop problems over time. Our technicians are trained to diagnose and repair a wide range of issues efficiently.</p>
            <ul>
                <li>Performance problems</li>
                <li>Unusual noises</li>
                <li>Error codes</li>
                <li>Electrical issues</li>
                <li>Mechanical failures</li>
            </ul>
        ''')


def generate_diy_section(appliance, keyword):
    """Generate DIY troubleshooting tips"""
    return f'''
            <h2>DIY Troubleshooting Steps</h2>
            <p>Before calling for professional help, try these safe troubleshooting steps:</p>

            <h3>Step 1: Power Check</h3>
            <p>Ensure your {appliance} is properly plugged in and the circuit breaker hasn't tripped. Sometimes the simplest solution is the right one.</p>

            <h3>Step 2: Visual Inspection</h3>
            <p>Look for obvious issues like loose connections, visible damage, or obstructions that might be affecting operation.</p>

            <h3>Step 3: Clean and Clear</h3>
            <p>Many {appliance} problems stem from buildup or blockages. Clean filters, vents, and accessible components.</p>

            <h3>Step 4: Reset the Appliance</h3>
            <p>Unplug your {appliance} for 5 minutes, then plug it back in. This can clear error codes and reset electronic controls.</p>

            <div class="warning-box">
                <h4><i class="fas fa-exclamation-triangle"></i> Safety Warning</h4>
                <p>Never attempt repairs involving gas lines, high voltage components, or sealed refrigerant systems. These require licensed professionals and can be dangerous.</p>
            </div>
    '''


def generate_pro_section(appliance):
    """Generate when to call professional section"""
    return f'''
            <h2>When to Call a Professional</h2>
            <p>While some {appliance} issues can be resolved with DIY troubleshooting, certain situations require expert help:</p>

            <ul>
                <li><strong>Gas-related issues</strong> - Always call a licensed technician for gas leaks or ignition problems</li>
                <li><strong>Electrical problems</strong> - Sparking, burning smells, or tripping breakers need professional attention</li>
                <li><strong>Refrigerant leaks</strong> - Sealed system repairs require EPA certification</li>
                <li><strong>Repeated failures</strong> - If the same problem keeps recurring, there may be an underlying issue</li>
                <li><strong>Under warranty</strong> - DIY repairs may void your manufacturer warranty</li>
                <li><strong>Complex error codes</strong> - Professional diagnostic tools can pinpoint exact failures</li>
            </ul>

            <div class="tip-box">
                <h4><i class="fas fa-clock"></i> Same-Day Service Available</h4>
                <p>Nika Appliance Repair offers same-day service for urgent repairs throughout Toronto. Call us at (437) 747-1010 and we'll dispatch a technician as soon as possible.</p>
            </div>
    '''


def main():
    """Generate all blog posts from keyword gap list"""
    base_dir = Path(__file__).parent.parent.parent.parent
    drafts_dir = base_dir / "blog" / "_drafts"

    # Create drafts directory if it doesn't exist
    drafts_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("GENERATING KEYWORD GAP BLOG POSTS")
    print("=" * 70)
    print(f"\nOutput directory: {drafts_dir}")
    print(f"Total posts to generate: {len(KEYWORD_GAP_POSTS)}\n")

    for i, (slug, title, category, keyword, volume) in enumerate(KEYWORD_GAP_POSTS, 1):
        filename = f"{slug}.html"
        filepath = drafts_dir / filename

        content = generate_post_content(slug, title, category, keyword, volume)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"[{i:02d}/{len(KEYWORD_GAP_POSTS)}] Created: {filename}")
        print(f"         Keyword: {keyword} (vol: {volume})")

    print(f"\n{'=' * 70}")
    print(f"[SUCCESS] Generated {len(KEYWORD_GAP_POSTS)} blog posts")
    print(f"Location: {drafts_dir}")
    print("=" * 70)


if __name__ == "__main__":
    main()
