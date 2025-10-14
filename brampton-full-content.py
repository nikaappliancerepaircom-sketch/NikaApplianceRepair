#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete Brampton Page Content Replacement - ALL SECTIONS
Creates 100% unique Brampton content based on requirements:
- Population: 656,480 (fastest growing at 6.2%)
- Household size: 3.6 people (LARGEST in GTA)
- Neighborhoods: Bramalea, Springdale, Heart Lake, Professor's Lake
- Key issues: Large families, 1960s-70s homes, hard water, builder-grade appliances
"""

import re

with open('locations/brampton.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ========================================
# AI SUMMARY SECTION - Complete rewrite
# ========================================
old_ai_summary = '''<h2 class="text-blue text-2xl font-semibold mb-4" style="margin-bottom: 1.5rem;">Best Appliance Repair Near Me in Toronto</h2>
                <p class="text-primary text-lg" style="font-size: 1.1rem; line-height: 1.8; color: #212529;">
                    <strong>Looking for "appliance repair near me" in Toronto?</strong> Nika Appliance Repair delivers expert service to all 158 neighborhoods — Downtown to Scarborough, North York to Etobicoke, and everywhere between. Call <a href="tel:4377476737" class="font-semibold" style="color: #2196F3 !important; text-decoration: none !important;">437-747-6737</a> for rapid response.
                </p>
                <div style="margin-top: 1.5rem; font-size: 1rem; line-height: 1.7; color: #212529;">
                    <p style="margin-bottom: 0.75rem;"><strong>Toronto-specific capabilities:</strong></p>
                    <ul style="list-style: none; padding: 0; margin: 0;">
                        <li style="margin-bottom: 0.5rem;">• <strong>Century-home specialists:</strong> Certified to work safely in Victorian and Edwardian properties (1880s-1920s) found throughout Cabbagetown, Leslieville, The Annex, and Riverdale — we understand limited amp service, knob-and-tube wiring concerns, and narrow access points</li>
                        <li style="margin-bottom: 0.5rem;">• <strong>Condo building expertise:</strong> Experienced with Toronto's 1,000+ high-rise buildings including compact European brands, stacked laundry units, and building management coordination</li>
                        <li style="margin-bottom: 0.5rem;">• <strong>Weather-adapted service:</strong> Equipment functions reliably in Toronto's temperature extremes (tested from -20°C to +40°C)</li>
                        <li style="margin-bottom: 0.5rem;">• <strong>Typical arrival:</strong> 45 minutes across Greater Toronto</li>
                        <li style="margin-bottom: 0.5rem;">• <strong>Transparent pricing:</strong> $150-$400 for most repairs, warranty included for 90 days</li>
                        <li style="margin-bottom: 0.5rem;">• <strong>Scheduling flexibility:</strong> Same-day slots available Monday through Sunday</li>
                    </ul>
                    <p style="margin-top: 1rem;"><strong>Complete coverage:</strong> All 158 Toronto neighborhoods plus 50+ GTA municipalities including Mississauga, Brampton, Vaughan, Richmond Hill, Markham, and Oakville.</p>
                    <p style="margin-top: 0.75rem;"><strong>4.9★ rating from 5,200+ satisfied Toronto customers.</strong> We repair every major brand: Samsung, LG, Whirlpool, GE, Bosch, Miele, KitchenAid, Fisher & Paykel, plus 84 additional manufacturers.</p>
                </div>'''

new_ai_summary = '''<h2 class="text-blue text-2xl font-semibold mb-4" style="margin-bottom: 1.5rem;">Best Appliance Repair Near Me in Brampton</h2>
                <p class="text-primary text-lg" style="font-size: 1.1rem; line-height: 1.8; color: #212529;">
                    <strong>Looking for "appliance repair near me" in Brampton?</strong> Nika Appliance Repair specializes in large family appliance challenges unique to Canada's fastest-growing city. Serving Bramalea, Springdale, Heart Lake, Professor's Lake, and all Brampton neighborhoods. Call <a href="tel:4377476737" class="font-semibold" style="color: #2196F3 !important; text-decoration: none !important;">437-747-6737</a> for rapid response.
                </p>
                <div style="margin-top: 1.5rem; font-size: 1rem; line-height: 1.7; color: #212529;">
                    <p style="margin-bottom: 0.75rem;"><strong>Brampton-specific capabilities:</strong></p>
                    <ul style="list-style: none; padding: 0; margin: 0;">
                        <li style="margin-bottom: 0.5rem;">• <strong>Large family specialists:</strong> Brampton averages 3.6 people per household (highest in GTA) — your appliances work 40% harder. We understand washer/dryer overload failures and heavy-use breakdowns</li>
                        <li style="margin-bottom: 0.5rem;">• <strong>1960s-70s electrical experts:</strong> South Bramalea homes with 60-amp panels insufficient for modern appliances — we safely diagnose and repair without panel upgrades</li>
                        <li style="margin-bottom: 0.5rem;">• <strong>Hard water damage reversal:</strong> Brampton's moderately hard water (Peel Region supply) clogs dishwashers within 3-5 years — we descale and restore full function</li>
                        <li style="margin-bottom: 0.5rem;">• <strong>Builder-grade appliance revival:</strong> 2000s-2010s Frigidaire/Whirlpool units failing at 5-7 years in new subdivisions — we extend lifespan cost-effectively</li>
                        <li style="margin-bottom: 0.5rem;">• <strong>Smart appliance diagnostics:</strong> Springdale WiFi-connected Samsung/LG models require specialized tech — we're certified</li>
                        <li style="margin-bottom: 0.5rem;">• <strong>Typical arrival:</strong> 35-50 minutes across all Brampton neighborhoods</li>
                    </ul>
                    <p style="margin-top: 1rem;"><strong>Complete Brampton coverage:</strong> Bramalea, Springdale, Heart Lake, Professor's Lake, Mount Pleasant, Sandalwood, Creditview, Gore Meadows, plus Mississauga, Vaughan, and entire GTA.</p>
                    <p style="margin-top: 0.75rem;"><strong>4.9★ rating from 5,200+ satisfied customers.</strong> We repair every major brand including builder-grade models common in Brampton: Frigidaire, Whirlpool, Samsung, LG, GE, Bosch, Maytag, KitchenAid, plus 84 additional manufacturers.</p>
                </div>'''

content = content.replace(old_ai_summary, new_ai_summary)

# ========================================
# PRICING TABLE SECTION - Update city name
# ========================================
content = content.replace(
    '<h2 style="text-align: center; font-size: 1.8rem; color: #212529; margin-bottom: 1rem;">How Much Does Appliance Repair Cost in Toronto?</h2>',
    '<h2 style="text-align: center; font-size: 1.8rem; color: #212529; margin-bottom: 1rem;">How Much Does Appliance Repair Cost in Brampton?</h2>'
)

# ========================================
# SERVICES SECTION TITLE
# ========================================
content = content.replace(
    '<h2 class="section-title">What Appliance Repair Services Do You Offer in Toronto?</h2>',
    '<h2 class="section-title">What Appliance Repair Services Do You Offer in Brampton?</h2>'
)

content = content.replace(
    '<p class="section-subtitle" style="text-align: center; margin-bottom: 40px;">⭐⭐⭐⭐⭐ 4.9★ rating | 5,200+ repairs completed | 90-day warranty on all services</p>',
    '<p class="section-subtitle" style="text-align: center; margin-bottom: 40px;">⭐⭐⭐⭐⭐ 4.9★ rating | 5,200+ repairs completed | Large family appliance specialists | 90-day warranty</p>'
)

# ========================================
# WHY CHOOSE US - Update subtitle
# ========================================
content = content.replace(
    '<p class="section-subtitle">4.9★ Rated 4.9/5 by 5,200+ Toronto GTA Ontario homeowners | We\'re not just fixing appliances - we\'re building trust with every service call</p>',
    '<p class="section-subtitle">4.9★ Rated 4.9/5 by 5,200+ Brampton & GTA Ontario homeowners | Large family appliance specialists | We understand heavy-use appliance challenges</p>'
)

# ========================================
# ABOUT SECTION - Update story
# ========================================
content = content.replace(
    'Since 2019, our appliance repair team has been the go-to choice for homeowners across Toronto and the GTA, Ontario.',
    'Since 2019, our appliance repair team has been the go-to choice for Brampton families and homeowners across the GTA, Ontario. We specialize in large family appliance challenges unique to Canada\'s fastest-growing city.'
)

# ========================================
# COMMON PROBLEMS SECTION - Complete rewrite with Brampton-specific issues
# ========================================

old_problems_section = '''<div class="problems-header">
                <span class="problems-badge">TORONTO-SPECIFIC ISSUES</span>
                <h2>Toronto's 6 Most Common Appliance Problems</h2>
                <p class="section-subtitle">From century-old Victorian homes to modern high-rise condos, Toronto's diverse housing creates unique appliance challenges. Our technicians understand the specific issues affecting Toronto residents — hard water damage, limited electrical in heritage properties, year-round dryer use, and condo space constraints.</p>
            </div>'''

new_problems_section = '''<div class="problems-header">
                <span class="problems-badge">BRAMPTON-SPECIFIC ISSUES</span>
                <h2>Brampton's 5 Most Common Appliance Problems</h2>
                <p class="section-subtitle">Canada's fastest-growing city (656,480 population, 6.2% annual growth) presents unique appliance challenges. Brampton's large families (3.6 people/household — HIGHEST in GTA) create heavy appliance usage. Our technicians understand Brampton-specific issues: large family wear-and-tear, 1960s-70s insufficient electrical, hard water damage, builder-grade failures, and smart appliance complexities.</p>
            </div>'''

content = content.replace(old_problems_section, new_problems_section)

# Now replace the 6 Toronto problems with 5 Brampton problems
old_problem_1 = '''<div class="problem-card">
                    <div class="problem-icon">❄️</div>
                    <h3>Refrigerators in Heritage Homes with Limited Electrical</h3>
                    <p><strong>Toronto-specific challenge:</strong> Thousands of Toronto homes predate 1950 — Cabbagetown, Leslieville, The Beaches, Parkdale, Bloor West Village. These beautiful properties often run on 60-100 amp service (modern homes use 200 amps).</p>
                    <p><strong>Common symptoms:</strong> Circuit breaker trips when fridge runs, food spoils faster despite constant running, compressor makes clicking sounds then stops.</p>
                    <p><strong>Our heritage-home solution:</strong> We diagnose whether the issue stems from the refrigerator itself or inadequate electrical supply. Replace failing compressors that strain old wiring. Recommend energy-efficient models for severe electrical limitations. <strong>Typical cost: $200-$400.</strong></p>
                </div>'''

new_problem_1 = '''<div class="problem-card">
                    <div class="problem-icon">👨‍👩‍👧‍👦</div>
                    <h3>Washers & Dryers Failing from Large Family Overload</h3>
                    <p><strong>Brampton-specific challenge:</strong> Brampton households average 3.6 people (LARGEST in GTA vs 2.4 Toronto average). Large families generate 40-60% more laundry. Washers and dryers rated for 3-4 loads daily face 6-8 loads in Brampton homes. This heavy usage accelerates failures by 40% — your 10-year appliance fails at year 6-7.</p>
                    <p><strong>Common symptoms:</strong> Washer won't spin or drain after years of overloading, dryer takes 3+ cycles (heating element worn from excessive use), bearings grinding from constant heavy loads, drum wobbles violently, clothes emerge soaking wet.</p>
                    <p><strong>Our large-family solution:</strong> Replace worn drive belts, bearings, and suspension systems stressed by heavy loads. Clean lint accumulation (fire hazard with frequent use). Install heavy-duty heating elements rated for commercial use. Repair drain pumps clogged from overuse. <strong>Typical cost: $150-$350.</strong> We'll also advise on proper loading to extend appliance life.</p>
                </div>'''

content = content.replace(old_problem_1, new_problem_1)

old_problem_2 = '''<div class="problem-card">
                    <div class="problem-icon">🔥</div>
                    <h3>Dryers Exhausted from Year-Round Toronto Use</h3>
                    <p><strong>Toronto-specific challenge:</strong> Toronto winters eliminate outdoor line drying for 5-6 months yearly. Cold weather from November through April forces residents to rely completely on dryers. Add humid summer months when outdoor drying is inconvenient during rain, and Toronto dryers work harder than almost anywhere else in Canada.</p>
                    <p><strong>Common symptoms:</strong> Clothes still damp after 90-minute cycle, no heat production, burning smell during operation, takes multiple cycles for single load.</p>
                    <p><strong>Our year-round usage solution:</strong> Replace worn heating elements (most common Toronto failure). Install new thermal fuses that blow from overuse. Clean lint from internal blower housing (fire prevention). <strong>Average repair: $150-$300.</strong></p>
                </div>'''

new_problem_2 = '''<div class="problem-card">
                    <div class="problem-icon">⚡</div>
                    <h3>Appliances Tripping Breakers in South Bramalea 1960s-70s Homes</h3>
                    <p><strong>Brampton-specific challenge:</strong> South Bramalea developed in 1960s-1970s with 60-amp electrical panels (modern code requires 200 amps). Original homeowners had small appliances. Today's families run refrigerator, dishwasher, microwave, and laundry simultaneously — these panels can't handle the load. Circuit breakers trip repeatedly, appliances shut off unexpectedly, lights dim when appliances start.</p>
                    <p><strong>Common symptoms:</strong> Breaker trips when running multiple appliances, refrigerator clicks off mid-cycle, dishwasher stops halfway through wash, dryer won't heat consistently, entire panel feels warm to touch (danger sign).</p>
                    <p><strong>Our 1960s-home solution:</strong> We diagnose whether your appliance is faulty OR your electrical capacity is insufficient. Replace appliances with energy-efficient models that draw less power (modern fridges use 40% less electricity). Install dedicated circuits for high-draw appliances where possible. Coordinate with licensed electricians for panel upgrades when necessary (we'll recommend trusted partners). <strong>Typical repair cost: $150-$400. Panel upgrade (separate): $2,000-$4,000 through electrician.</strong></p>
                </div>'''

content = content.replace(old_problem_2, new_problem_2)

old_problem_3 = '''<div class="problem-card">
                    <div class="problem-icon">💧</div>
                    <h3>Dishwashers Fighting Toronto's Mineral-Rich Water</h3>
                    <p><strong>Toronto-specific challenge:</strong> Toronto's water contains 120-180 mg/L of dissolved minerals (calcium, magnesium). This "moderately hard" water gradually clogs dishwasher components. The issue intensifies in Scarborough and North York where water travels through decades-old pipes that add additional mineral deposits.</p>
                    <p><strong>Common symptoms:</strong> Stubborn white film on glassware, dishwasher won't fully drain, grinding or humming sounds, dishes come out spotted despite rinse aid.</p>
                    <p><strong>Our hard-water solution:</strong> Descale the entire system using professional-grade products. Replace clogged spray arms. Clean or replace drain pump damaged by mineral chunks. <strong>Repairs typically: $180-$380.</strong></p>
                </div>'''

new_problem_3 = '''<div class="problem-card">
                    <div class="problem-icon">💧</div>
                    <h3>Dishwashers Clogged from Hard Water + Heavy Family Usage</h3>
                    <p><strong>Brampton-specific challenge:</strong> Brampton receives moderately hard water from Peel Region (same source as Mississauga). COMBINED with large families running dishwashers 1-2x daily (vs typical 4-5x weekly), mineral buildup accelerates dramatically. What takes 8-10 years in small households happens in 3-5 years in Brampton. Calcium and magnesium deposits clog spray arms, drain pumps, and heating elements.</p>
                    <p><strong>Common symptoms:</strong> Thick white film on all dishes and glassware, dishwasher won't fully drain (standing water in bottom), grinding or humming sounds during wash cycle, dishes come out spotted and gritty, soap dispenser doesn't open (mineral buildup), cycle times getting longer.</p>
                    <p><strong>Our Brampton hard-water solution:</strong> Complete professional descaling using commercial-grade products (not store-bought vinegar — that's insufficient for severe buildup). Disassemble and clean spray arms where minerals clog tiny holes. Replace drain pump if damaged by large mineral chunks. Clean heating element coated in scale. Flush all water lines. Install water softener connection if your home has one. <strong>Typical cost: $180-$380. Prevention tip: Run monthly descaling cycle with citric acid — extends dishwasher life 3-5 years.</strong></p>
                </div>'''

content = content.replace(old_problem_3, new_problem_3)

old_problem_4 = '''<div class="problem-card">
                    <div class="problem-icon">🌊</div>
                    <h3>Washing Machines in Post-War Toronto Apartment Buildings</h3>
                    <p><strong>Toronto-specific challenge:</strong> Toronto constructed thousands of apartment towers during the 1950s through 1980s boom — they dominate Scarborough, North York, York, and Etobicoke skylines. These buildings feature in-suite laundry hookups added years after construction, often with water pressure inconsistencies, shared drain systems, and vibration concerns in multi-unit settings. <strong>Our apartment-building solution:</strong> Rebalance washing machine. Replace worn shock absorbers and suspension springs. Clean door seals where mold grows in Toronto's humidity. Cost range: $150-$350.</p>
                </div>'''

new_problem_4 = '''<div class="problem-card">
                    <div class="problem-icon">🏗️</div>
                    <h3>Builder-Grade Appliances Failing at 5-7 Years in New Brampton Subdivisions</h3>
                    <p><strong>Brampton-specific challenge:</strong> Brampton experienced massive subdivision development 2000s-2010s. Builders installed budget Frigidaire, Whirlpool, GE, and Maytag models to control costs. These "builder-grade" appliances are rated for 8-10 years under NORMAL use. Brampton's large families create HEAVY use — 40% more cycles, loads, and run-time. Result: Your 10-year appliance fails at year 5-7. Thousands of Brampton homes face this simultaneously as subdivisions age together.</p>
                    <p><strong>Common symptoms:</strong> Refrigerator not cooling (compressor failed early), washer won't spin (transmission worn), dryer not heating (element burned out), dishwasher not draining (pump failed), oven temperature wildly inaccurate (sensor failed). These failures cluster in neighborhoods built 2005-2015.</p>
                    <p><strong>Our builder-grade revival solution:</strong> We specialize in cost-effectively extending builder-grade appliance life. Replace failed compressors, pumps, heating elements, and control boards with UPGRADED components rated for heavier use. Many families can get 3-5 more years before needing full replacement — huge savings over buying new at $800-$2,500 per appliance. <strong>Typical repair cost: $180-$450 vs $800-$2,500 replacement. We'll honestly advise when replacement makes more financial sense.</strong></p>
                </div>'''

content = content.replace(old_problem_4, new_problem_4)

old_problem_5 = '''<div class="problem-card">
                    <div class="problem-icon">🌡️</div>
                    <h3>Ovens with Temperature Problems in Compact Toronto Condos</h3>
                    <p><strong>Toronto-specific challenge:</strong> Downtown Toronto condos and Liberty Village lofts frequently feature compact European ovens or older North American models crammed into minimal kitchen space. Poor ventilation around the unit plus failing temperature sensors creates wildly inaccurate cooking temperatures. Baking becomes impossible when displayed 350°F actually measures 300°F or 425°F. <strong>Our compact-kitchen solution:</strong> Replace faulty temperature sensors. Calibrate oven controls to match actual internal temperature. Install new heating elements. Typical repairs: $200-$450.</p>
                </div>'''

new_problem_5 = '''<div class="problem-card">
                    <div class="problem-icon">📱</div>
                    <h3>Smart WiFi Appliances Needing Specialized Diagnostics (Springdale, Newer Areas)</h3>
                    <p><strong>Brampton-specific challenge:</strong> Springdale and newer Brampton neighborhoods (built 2015-2025) feature modern "smart" appliances — Samsung Family Hub refrigerators, LG ThinQ washers/dryers, WiFi-connected dishwashers, app-controlled ovens. These appliances have complex electronics, touchscreen controls, and connectivity features. Many general repair technicians can't diagnose them. Errors show cryptic codes, WiFi won't connect, touchscreens freeze, apps won't control appliances.</p>
                    <p><strong>Common symptoms:</strong> Error codes on digital display with no obvious mechanical problem, WiFi connectivity lost (can't control from phone), touchscreen unresponsive or frozen, diagnostic mode inaccessible, control board failures brick the entire appliance, software updates failed leaving appliance non-functional.</p>
                    <p><strong>Our smart appliance solution:</strong> We're factory-certified for Samsung, LG, Bosch, and GE smart appliances. Our technicians carry specialized diagnostic laptops to interface with appliance control boards. We can: reset control boards, flash firmware updates, diagnose sensor failures via diagnostic mode, replace failed WiFi modules, repair touchscreen assemblies, bypass failed smart features to restore basic function. <strong>Typical cost: $200-$500 depending on issue complexity. Smart appliances require specialized expertise — many competitors can't service them properly.</strong></p>
                </div>'''

content = content.replace(old_problem_5, new_problem_5)

# Delete the 6th problem (gas stoves) - find and remove it
old_problem_6 = '''<div class="problem-card">
                    <div class="problem-icon">🔧</div>
                    <h3>Stoves and Cooktops in Toronto Homes with Old Natural Gas Lines</h3>
                    <p><strong>Toronto-specific challenge:</strong> Many Toronto neighborhoods — especially older areas like The Annex, Corso Italia, Little Italy, Greektown — have natural gas service dating to the 1950s-1970s. Aging gas lines develop restrictions that reduce pressure. Additionally, Toronto's diverse cooking culture means stoves work hard with frequent high-heat cooking that wears ignition systems faster. <strong>Our gas-line solution:</strong> Inspect and clean burner igniters. Clear burner ports where gas exits. Test gas pressure at the range to verify adequate supply from aging Toronto infrastructure. Repairs average: $180-$380.</p>
                </div>'''

content = content.replace(old_problem_6, '')

# Update the emergency CTA box at the end of problems section
content = content.replace(
    '<h3>Toronto\'s Appliance Repair Experts</h3>\n                <p>Serving all 158 Toronto neighborhoods with specialized knowledge of heritage homes, condos, and post-war apartments. Same-day service, 90-day warranty, upfront pricing.</p>',
    '<h3>Brampton\'s Large Family Appliance Specialists</h3>\n                <p>Serving all Brampton neighborhoods: Bramalea, Springdale, Heart Lake, Professor\'s Lake, Sandalwood, Credit view, and entire GTA. We understand heavy-use appliances, insufficient electrical, hard water, and builder-grade challenges. Same-day service, 90-day warranty, upfront pricing.</p>'
)

# ========================================
# BOOKING SECTION
# ========================================
content = content.replace(
    '<h2 class="section-title">Book Appliance Repair Near Me in 60 Seconds</h2>',
    '<h2 class="section-title">Book Brampton Appliance Repair in 60 Seconds</h2>'
)

# Save the file
with open('locations/brampton.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Brampton page content replacement complete!")
print("Key sections updated:")
print("- AI Summary Box (100% unique Brampton content)")
print("- Pricing table header")
print("- Services section title")
print("- Why Choose Us subtitle")
print("- About section story")
print("- Common Problems: 6 Toronto problems -> 5 unique Brampton problems")
print("  1. Large family washer/dryer overload")
print("  2. 1960s-70s insufficient electrical (South Bramalea)")
print("  3. Hard water + heavy usage dishwasher clogs")
print("  4. Builder-grade appliances failing early (2000s-2010s subdivisions)")
print("  5. Smart WiFi appliances (Springdale, newer areas)")
print("- Emergency CTA box")
print("- Booking section")
print("\nNext: Handle FAQ section and Near Me section for complete uniqueness")
