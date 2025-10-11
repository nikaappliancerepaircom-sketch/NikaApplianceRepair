#!/usr/bin/env python3
"""
BMAD V2 - CONTENT UNIQUENESS FIXER
Rewrites duplicate content to be unique for each appliance type
"""

import re
from pathlib import Path

# Unique content templates for each appliance
UNIQUE_CONTENT = {
    'dishwasher-repair.html': {
        'h1': 'Professional Dishwasher Repair Toronto & GTA',
        'hero_intro': """Expert dishwasher repair service specializing in drainage clogs, spray arm failures,
poor cleaning cycles, and water leaks. We fix all major brands including Bosch, KitchenAid, GE, Whirlpool,
Samsung, LG, and Maytag dishwashers. Same-day service available across Toronto and the Greater Toronto Area.""",

        'problems': [
            ('Dishwasher won\'t drain - clogged pump or drain hose', 'drainage-issues'),
            ('Poor cleaning performance - spray arm or filter problems', 'cleaning-problems'),
            ('Water leaks from door seal or tub', 'leak-repair'),
            ('Dishwasher won\'t start or cycle properly', 'won-t-start'),
            ('Unusual noises - pump, motor, or spray arm issues', 'noise-problems'),
            ('Door latch or hinge problems', 'door-repair')
        ],

        'benefits': [
            'Dishwasher drainage experts - we fix clogs fast',
            'Spray arm and cleaning cycle specialists',
            'Door seal and gasket replacement',
            'Control panel and electronics repair',
            'Same-day dishwasher repair in most cases'
        ],

        'faq': [
            ('Why won\'t my dishwasher drain?',
             'Common causes include clogged filters, blocked drain hose, or faulty drain pump. We diagnose and fix drainage issues same-day.'),
            ('Why is my dishwasher not cleaning dishes properly?',
             'This is usually due to clogged spray arms, dirty filters, low water pressure, or worn pump. Our technicians clean and repair all components.'),
            ('How long does dishwasher repair take?',
             'Most dishwasher repairs take 45-90 minutes. Complex issues like control board replacement may take up to 2 hours.'),
            ('Do you repair all dishwasher brands?',
             'Yes! We service Bosch, KitchenAid, GE, Whirlpool, Samsung, LG, Maytag, Frigidaire, and all other major dishwasher brands.')
        ]
    },

    'washer-repair.html': {
        'h1': 'Expert Washing Machine Repair Toronto & GTA',
        'hero_intro': """Professional washer repair service for all types: front-load, top-load, and high-efficiency models.
We fix spin cycle problems, water leaks, drum balance issues, and control malfunctions. Servicing Samsung, LG, Whirlpool,
Maytag, GE, and all major washer brands across Toronto and GTA with same-day availability.""",

        'problems': [
            ('Washer won\'t spin or agitate - motor or belt issues', 'spin-problems'),
            ('Water leaking from door seal or hoses', 'leak-repair'),
            ('Loud vibration or banging - drum balance problems', 'vibration-issues'),
            ('Washer won\'t drain or fill properly', 'drain-fill-issues'),
            ('Door won\'t lock or unlock', 'door-lock-problems'),
            ('Error codes on digital display', 'error-codes')
        ],

        'benefits': [
            'Front-load and top-load washer specialists',
            'Drum balance and vibration experts',
            'Water leak detection and repair',
            'Belt, motor, and pump replacement',
            'Emergency same-day washer repair'
        ],

        'faq': [
            ('Why won\'t my washing machine spin?',
             'Common causes are broken drive belt, worn motor coupling, or faulty lid switch. We diagnose and replace worn components same-day.'),
            ('Why is my washer leaking water?',
             'Leaks usually come from worn door seals, loose hose connections, or damaged tub. Our technicians identify the source and fix it quickly.'),
            ('How long does washer repair take?',
             'Most washer repairs take 60-120 minutes depending on the issue. Belt and seal replacements are typically under 90 minutes.'),
            ('Do you repair both front-load and top-load washers?',
             'Yes! We specialize in all washer types including front-load, top-load, HE models, and stackable units from all major brands.')
        ]
    },

    'dryer-repair.html': {
        'h1': 'Fast Dryer Repair Service Toronto & GTA',
        'hero_intro': """Professional dryer repair for both gas and electric models. We fix no-heat issues, drum problems,
venting failures, and ignition malfunctions. Expert service for Samsung, LG, Whirlpool, Maytag, GE, and all dryer brands.
Same-day repairs available across Toronto and surrounding areas with 90-day warranty.""",

        'problems': [
            ('Dryer won\'t heat - thermal fuse or heating element', 'no-heat'),
            ('Dryer won\'t start or turn on', 'won-t-start'),
            ('Drum not spinning - broken belt or motor', 'drum-problems'),
            ('Takes too long to dry - vent blockage', 'slow-drying'),
            ('Loud squealing or thumping noises', 'noise-issues'),
            ('Gas dryer ignition problems', 'gas-ignition')
        ],

        'benefits': [
            'Electric and gas dryer experts',
            'Heating element and thermal fuse specialists',
            'Vent cleaning and optimization included',
            'Belt and drum roller replacement',
            'Fast same-day dryer repair service'
        ],

        'faq': [
            ('Why won\'t my dryer heat up?',
             'Most common causes are blown thermal fuse, faulty heating element (electric), or bad igniter (gas). We diagnose and replace parts same-day.'),
            ('Why is my dryer taking forever to dry clothes?',
             'This is usually due to clogged lint filter, blocked exhaust vent, or weak airflow. We clean vents and restore proper drying time.'),
            ('How long does dryer repair take?',
             'Most dryer repairs take 45-90 minutes. Heating element replacement typically takes under an hour.'),
            ('Do you repair both gas and electric dryers?',
             'Absolutely! Our technicians are certified for both gas and electric dryer repair, including all major brands and models.')
        ]
    },

    'oven-repair.html': {
        'h1': 'Professional Oven Repair Toronto & GTA',
        'hero_intro': """Expert oven and range repair service for gas and electric models. We fix heating problems, temperature
control issues, ignition failures, and door malfunctions. Servicing all brands including GE, Whirlpool, Samsung, LG,
KitchenAid, and Bosch. Same-day oven repair available throughout Toronto and GTA with comprehensive warranty.""",

        'problems': [
            ('Oven won\'t heat or reach temperature', 'heating-problems'),
            ('Uneven cooking or hot spots', 'temperature-issues'),
            ('Gas oven won\'t ignite properly', 'ignition-problems'),
            ('Oven door won\'t close or seal', 'door-issues'),
            ('Self-cleaning cycle not working', 'cleaning-cycle'),
            ('Control panel or thermostat malfunction', 'control-problems')
        ],

        'benefits': [
            'Gas and electric oven specialists',
            'Heating element and igniter experts',
            'Temperature calibration service',
            'Door seal and hinge replacement',
            'Control board and thermostat repair'
        ],

        'faq': [
            ('Why won\'t my oven heat up properly?',
             'Common causes include faulty heating element (electric) or broken igniter (gas), bad thermostat, or control board issues. We diagnose and fix quickly.'),
            ('Why is my oven cooking unevenly?',
             'Uneven cooking is often due to worn heating elements, poor calibration, or damaged door seal. We test all components and restore even heating.'),
            ('How long does oven repair take?',
             'Most oven repairs take 60-90 minutes. Element replacement is typically under an hour, control boards may take up to 2 hours.'),
            ('Do you repair both built-in and freestanding ovens?',
             'Yes! We service all oven types including built-in wall ovens, slide-in ranges, freestanding stoves, and double ovens from all brands.')
        ]
    },

    'freezer-repair.html': {
        'h1': 'Reliable Freezer Repair Toronto & GTA',
        'hero_intro': """Professional freezer repair service for all types: upright, chest, and built-in models. We fix
temperature problems, ice buildup, compressor failures, and door seal issues. Expert service for Frigidaire, Whirlpool,
GE, Samsung, LG freezers. Same-day repairs available in Toronto and GTA with 90-day parts and labor warranty.""",

        'problems': [
            ('Freezer not cold enough - temperature problems', 'temperature-issues'),
            ('Excessive frost or ice buildup', 'frost-problems'),
            ('Freezer running constantly or cycling too often', 'compressor-issues'),
            ('Water leaking inside or underneath', 'leak-repair'),
            ('Door seal problems - cold air escaping', 'door-seal'),
            ('Ice maker not working properly', 'ice-maker-problems')
        ],

        'benefits': [
            'Upright and chest freezer specialists',
            'Compressor and cooling system experts',
            'Defrost system repair',
            'Door seal and gasket replacement',
            'Temperature control calibration'
        ],

        'faq': [
            ('Why is my freezer not staying cold?',
             'This can be caused by faulty thermostat, failed compressor, refrigerant leak, or dirty condenser coils. We diagnose cooling issues quickly.'),
            ('Why does my freezer have so much frost buildup?',
             'Excessive frost usually indicates door seal problems, defrost system failure, or frequent door opening. We inspect and repair the root cause.'),
            ('How long does freezer repair take?',
             'Most freezer repairs take 60-120 minutes. Thermostat and seal replacement is typically under 90 minutes.'),
            ('Do you repair standalone and chest freezers?',
             'Yes! We service all freezer types including upright freezers, chest freezers, built-in models, and standalone units from all manufacturers.')
        ]
    },

    'stove-repair.html': {
        'h1': 'Expert Stove Repair Toronto & GTA',
        'hero_intro': """Expert stove and cooktop repair service for gas and electric models. We fix burner problems, ignition issues,
temperature control failures, and electrical malfunctions. Servicing all brands including GE, Whirlpool, Samsung, LG,
and Frigidaire stoves. Same-day repair available throughout Toronto and GTA with 90-day warranty.""",

        'problems': [
            ('Burners won\'t light or heat properly', 'burner-problems'),
            ('Gas stove igniter clicking but not lighting', 'ignition-issues'),
            ('Electric burner not heating evenly', 'heating-problems'),
            ('Temperature control not working', 'temperature-issues'),
            ('Gas smell or leak concerns', 'gas-leak'),
            ('Control panel or knobs malfunctioning', 'control-problems')
        ],

        'benefits': [
            'Gas and electric stove specialists',
            'Burner and igniter repair experts',
            'Temperature control calibration',
            'Gas leak detection and safety',
            'Same-day stove repair service'
        ],

        'faq': [
            ('Why won\'t my stove burners light?',
             'Common causes include faulty igniter, clogged burner ports, or gas supply issues. We diagnose and repair ignition problems same-day.'),
            ('Is it safe to use a stove with a gas smell?',
             'No! Turn off gas immediately and call us. We provide emergency gas leak detection and repair to ensure your safety.'),
            ('How long does stove repair take?',
             'Most stove repairs take 45-90 minutes. Burner and igniter replacement typically takes under an hour.'),
            ('Do you repair both gas and electric stoves?',
             'Yes! Our technicians are certified for gas and electric stove repair, including all major brands and cooktop models.')
        ]
    },

    'range-repair.html': {
        'h1': 'Professional Range Repair Toronto & GTA',
        'hero_intro': """Professional range repair service for freestanding, slide-in, and dual-fuel models. We fix oven heating,
cooktop burners, self-cleaning cycles, and control systems. Expert service for GE, Whirlpool, Samsung, LG, KitchenAid ranges.
Same-day repairs available across Toronto and GTA with comprehensive warranty.""",

        'problems': [
            ('Oven won\'t heat but cooktop works', 'oven-heating'),
            ('Cooktop burners not working properly', 'burner-issues'),
            ('Self-cleaning cycle not functioning', 'cleaning-cycle'),
            ('Uneven cooking or temperature issues', 'temperature-problems'),
            ('Control panel or display errors', 'control-issues'),
            ('Door won\'t close or seal properly', 'door-problems')
        ],

        'benefits': [
            'Freestanding and slide-in range experts',
            'Dual-fuel range specialists',
            'Oven and cooktop combination repair',
            'Control system diagnostics',
            'Emergency same-day range repair'
        ],

        'faq': [
            ('Why is my range oven not heating but burners work?',
             'This usually indicates a faulty oven heating element, bad thermostat, or control board issue. We diagnose and fix oven-specific problems quickly.'),
            ('Can you fix both the oven and cooktop on a range?',
             'Absolutely! We specialize in complete range repair including both oven and cooktop components on freestanding and slide-in models.'),
            ('How long does range repair take?',
             'Most range repairs take 60-120 minutes depending on the issue. Simple element replacement is typically under 90 minutes.'),
            ('Do you repair dual-fuel ranges?',
             'Yes! Our technicians are certified for gas and electric systems, making us experts in dual-fuel range repair.')
        ]
    },

    'microwave-repair.html': {
        'h1': 'Fast Microwave Repair Toronto & GTA',
        'hero_intro': """Expert microwave repair service for all types: countertop, over-the-range, and built-in models. We fix
no-heat issues, turntable problems, display errors, and door malfunctions. Servicing Samsung, LG, GE, Whirlpool, Panasonic
microwaves. Same-day repairs available in Toronto and GTA with 90-day warranty.""",

        'problems': [
            ('Microwave won\'t heat food properly', 'no-heat'),
            ('Turntable not spinning', 'turntable-problems'),
            ('Display or control panel not working', 'display-issues'),
            ('Door won\'t close or latch properly', 'door-problems'),
            ('Sparking or unusual noises inside', 'sparking-noise'),
            ('Microwave runs but doesn\'t heat', 'magnetron-failure')
        ],

        'benefits': [
            'Countertop and over-range microwave experts',
            'Magnetron and heating system specialists',
            'Control panel and display repair',
            'Door switch and safety interlock repair',
            'Same-day microwave repair service'
        ],

        'faq': [
            ('Why won\'t my microwave heat food?',
             'Most common cause is a failed magnetron, faulty door switches, or blown high-voltage fuse. We diagnose and replace defective components same-day.'),
            ('Is it worth repairing a microwave?',
             'For high-end models and over-the-range microwaves, yes! Repair costs typically 40-60% less than replacement, with our 90-day warranty.'),
            ('How long does microwave repair take?',
             'Most microwave repairs take 45-75 minutes. Door switch and fuse replacement is typically under an hour.'),
            ('Do you repair over-the-range microwaves?',
             'Yes! We specialize in over-the-range, built-in, and countertop microwave repair from all major brands.')
        ]
    },

    'ice-maker-repair.html': {
        'h1': 'Reliable Ice Maker Repair Toronto & GTA',
        'hero_intro': """Professional ice maker repair service for refrigerator ice makers and standalone units. We fix no-ice production,
water leaks, ice jams, and slow ice making. Expert service for Samsung, LG, Whirlpool, GE, and all major brands.
Same-day repairs available across Toronto and GTA with 90-day parts and labor warranty.""",

        'problems': [
            ('Ice maker not making ice at all', 'no-ice'),
            ('Ice maker producing small or hollow cubes', 'poor-quality-ice'),
            ('Water leaking from ice maker', 'leak-problems'),
            ('Ice maker jammed or frozen over', 'jam-issues'),
            ('Slow ice production or low output', 'slow-production'),
            ('Unusual noises or cycling problems', 'noise-cycling')
        ],

        'benefits': [
            'Refrigerator and standalone ice maker experts',
            'Water inlet valve and line repair',
            'Ice mold and ejector specialists',
            'Control module diagnostics',
            'Fast same-day ice maker repair'
        ],

        'faq': [
            ('Why isn\'t my ice maker producing ice?',
             'Common causes include frozen water line, faulty water inlet valve, bad ice maker module, or low water pressure. We diagnose and fix quickly.'),
            ('How often should ice maker be cleaned?',
             'Every 6 months for optimal performance. We provide ice maker cleaning and maintenance along with repairs.'),
            ('How long does ice maker repair take?',
             'Most ice maker repairs take 30-60 minutes. Water valve and line repairs are typically under an hour.'),
            ('Do you repair built-in refrigerator ice makers?',
             'Yes! We service all ice maker types including built-in fridge models, in-door systems, and standalone ice machines.')
        ]
    },

    'garbage-disposal-repair.html': {
        'h1': 'Expert Garbage Disposal Repair Toronto & GTA',
        'hero_intro': """Expert garbage disposal repair and replacement service for all major brands. We fix jammed disposals,
motor failures, leaks, and unusual noises. Servicing InSinkErator, Waste King, Moen, KitchenAid disposals.
Same-day repairs available throughout Toronto and GTA with warranty on all work.""",

        'problems': [
            ('Garbage disposal jammed or won\'t spin', 'jam-issues'),
            ('Disposal won\'t turn on or motor humming', 'motor-problems'),
            ('Water leaking from disposal unit', 'leak-repair'),
            ('Loud grinding or rattling noises', 'noise-problems'),
            ('Disposal reset button keeps tripping', 'reset-issues'),
            ('Slow draining or clogged drain line', 'drain-problems')
        ],

        'benefits': [
            'Garbage disposal jam removal experts',
            'Motor and electrical repair specialists',
            'Leak detection and seal replacement',
            'Installation and replacement service',
            'Same-day disposal repair and service'
        ],

        'faq': [
            ('Why is my garbage disposal jammed?',
             'Common causes are hard objects, fibrous foods, or lack of water flow. We safely remove jams and restore function same-day.'),
            ('Should I repair or replace my garbage disposal?',
             'If motor is burned out or unit is 10+ years old, replacement is best. Otherwise, repairs are cost-effective with our warranty.'),
            ('How long does garbage disposal repair take?',
             'Most repairs take 30-60 minutes. Simple jams can be cleared in 15-30 minutes.'),
            ('What brands of garbage disposals do you service?',
             'We repair all major brands including InSinkErator, Waste King, Moen, KitchenAid, GE, and Badger disposals.')
        ]
    }
}


def replace_content_sections(html_content, appliance_file):
    """Replace generic content with appliance-specific content"""
    if appliance_file not in UNIQUE_CONTENT:
        print(f"[WARN] No unique content defined for {appliance_file}")
        return html_content, []

    content = UNIQUE_CONTENT[appliance_file]
    changes = []

    # 1. Replace H1
    h1_pattern = r'<h1[^>]*>(.*?)</h1>'
    if re.search(h1_pattern, html_content, re.IGNORECASE | re.DOTALL):
        html_content = re.sub(
            h1_pattern,
            f'<h1>{content["h1"]}</h1>',
            html_content,
            count=1,
            flags=re.IGNORECASE | re.DOTALL
        )
        changes.append(f"Updated H1 to: {content['h1']}")

    # 2. Find and replace hero intro (paragraph after H1)
    # Look for the first substantial paragraph after H1
    hero_pattern = r'(<h1[^>]*>.*?</h1>.*?<p[^>]*>)(.*?)(</p>)'
    match = re.search(hero_pattern, html_content, re.IGNORECASE | re.DOTALL)
    if match:
        html_content = re.sub(
            hero_pattern,
            r'\1' + content['hero_intro'] + r'\3',
            html_content,
            count=1,
            flags=re.IGNORECASE | re.DOTALL
        )
        changes.append("Updated hero intro paragraph")

    # 3. Replace problems/services list
    # Look for common problems section
    problems_section_pattern = r'(<(?:section|div)[^>]*class="[^"]*(?:problems|services|issues|repairs)[^"]*"[^>]*>.*?<(?:h2|h3)[^>]*>.*?</(?:h2|h3)>.*?<ul[^>]*>)(.*?)(</ul>)'
    problems_match = re.search(problems_section_pattern, html_content, re.IGNORECASE | re.DOTALL)
    if problems_match and 'problems' in content:
        problems_html = '\n'.join([f'<li>{problem[0]}</li>' for problem in content['problems']])
        html_content = re.sub(
            problems_section_pattern,
            r'\1' + problems_html + r'\3',
            html_content,
            count=1,
            flags=re.IGNORECASE | re.DOTALL
        )
        changes.append(f"Updated problems list ({len(content['problems'])} items)")

    # 4. Replace benefits/why choose us list
    benefits_section_pattern = r'(<(?:section|div)[^>]*class="[^"]*(?:benefits|why-choose|advantages)[^"]*"[^>]*>.*?<(?:h2|h3)[^>]*>.*?</(?:h2|h3)>.*?<ul[^>]*>)(.*?)(</ul>)'
    benefits_match = re.search(benefits_section_pattern, html_content, re.IGNORECASE | re.DOTALL)
    if benefits_match and 'benefits' in content:
        benefits_html = '\n'.join([f'<li>{benefit}</li>' for benefit in content['benefits']])
        html_content = re.sub(
            benefits_section_pattern,
            r'\1' + benefits_html + r'\3',
            html_content,
            count=1,
            flags=re.IGNORECASE | re.DOTALL
        )
        changes.append(f"Updated benefits list ({len(content['benefits'])} items)")

    # 5. Replace FAQ section
    if 'faq' in content:
        faq_section_pattern = r'<section[^>]*class="[^"]*faq[^"]*"[^>]*>.*?</section>'
        faq_match = re.search(faq_section_pattern, html_content, re.IGNORECASE | re.DOTALL)
        if faq_match:
            faq_items_html = '\n'.join([
                f'''<div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
    <h3 itemprop="name">{q}</h3>
    <div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
        <p itemprop="text">{a}</p>
    </div>
</div>''' for q, a in content['faq']
            ])
            faq_html = f'''<section class="faq-section" itemscope itemtype="https://schema.org/FAQPage">
    <h2>Frequently Asked Questions</h2>
    {faq_items_html}
</section>'''
            html_content = re.sub(
                faq_section_pattern,
                faq_html,
                html_content,
                count=1,
                flags=re.IGNORECASE | re.DOTALL
            )
            changes.append(f"Updated FAQ section ({len(content['faq'])} questions)")

    return html_content, changes


def fix_appliance_content(html_file):
    """Fix content uniqueness for a specific appliance page"""
    html_path = Path(html_file)
    appliance_name = html_path.name

    print(f"\n{'='*70}")
    print(f"CONTENT UNIQUENESS FIXER - {appliance_name}")
    print(f"{'='*70}\n")

    # Read file
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(f"[ERROR] Reading file: {e}")
        return False

    # Backup
    backup_path = html_path.with_suffix('.html.content.backup')
    try:
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"[OK] Backup created: {backup_path}")
    except Exception as e:
        print(f"[ERROR] Creating backup: {e}")
        return False

    # Replace content
    html_content, changes = replace_content_sections(html_content, appliance_name)

    if not changes:
        print("[OK] No changes needed")
        return True

    # Save
    try:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"\n[OK] Saved: {html_path}")
        print(f"\n[FIX] Applied changes:")
        for i, change in enumerate(changes, 1):
            print(f"  {i}. {change}")
        return True
    except Exception as e:
        print(f"[ERROR] Saving file: {e}")
        return False


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python content-uniqueness-fixer.py <html_file>")
        sys.exit(1)

    html_file = sys.argv[1]
    success = fix_appliance_content(html_file)

    if success:
        print(f"\n{'='*70}")
        print("[SUCCESS] Content uniqueness improved")
        print(f"{'='*70}\n")
    else:
        print(f"\n{'='*70}")
        print("[FAILED] Could not update content")
        print(f"{'='*70}\n")
        sys.exit(1)
