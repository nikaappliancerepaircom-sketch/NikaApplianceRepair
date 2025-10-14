#!/usr/bin/env python3
"""
Script to create 10 new location pages based on Richmond Hill template
"""

cities = {
    'mississauga': {
        'name': 'Mississauga',
        'population': '721,000',
        'neighborhoods': ['Port Credit', 'Streetsville', 'Erin Mills', 'Cooksville', 'Square One'],
        'issues': ['Hard water (150-180 mg/L)', 'high-rise condos', 'waterfront humidity'],
        'coordinates': {'lat': '43.5890', 'lon': '-79.6441'},
        'nearby_cities': ['Toronto', 'Brampton', 'Oakville', 'Vaughan'],
        'meta_description': 'Mississauga appliance repair. Samsung, LG, Whirlpool, GE experts. Hard water solutions, condo specialists. Same-day service. Call 437-747-6737',
        'ai_expertise': 'Port Credit waterfront corrosion solutions, Square One high-rise condo appliance access, hard water treatment for dishwashers and washing machines',
        'hero_subtitle': 'From Port Credit to Square One, we fix Samsung, LG, Whirlpool, GE, and all major brands fast',
        'city_problems': [
            'High-rise condo stackable washer/dryer repairs (24" compact units)',
            'Hard water mineral buildup in dishwashers and washing machines'
        ],
        'faq_location': 'Mississauga, including Port Credit, Square One, Erin Mills, Cooksville, and Streetsville'
    },
    'brampton': {
        'name': 'Brampton',
        'population': '656,000',
        'neighborhoods': ['Bramalea', 'Heart Lake', 'Springdale', 'Downtown Brampton'],
        'issues': ['Large families (3.6 people/household)', '60-amp panels (older homes)'],
        'coordinates': {'lat': '43.7315', 'lon': '-79.7624'},
        'nearby_cities': ['Mississauga', 'Vaughan', 'Toronto', 'Caledon'],
        'meta_description': 'Brampton appliance repair. Samsung, LG, Whirlpool, GE experts. Large family solutions, electrical panel upgrades. Same-day service. Call 437-747-6737',
        'ai_expertise': 'Heavy-duty appliance repairs for large families (3.6 people/household), Bramalea 60-amp electrical panel solutions, hard water treatment',
        'hero_subtitle': 'From Bramalea to Springdale, we fix Samsung, LG, Whirlpool, GE, and all major brands fast',
        'city_problems': [
            'Heavy family usage causing faster appliance wear (washers running 8-12 loads weekly)',
            'South Bramalea 60-amp electrical panels requiring circuit upgrades'
        ],
        'faq_location': 'Brampton, including Bramalea, Heart Lake, Springdale, and Downtown Brampton'
    },
    'markham': {
        'name': 'Markham',
        'population': '338,000',
        'neighborhoods': ['Unionville', 'Thornhill', 'Cornell', 'Markville', 'Wismer'],
        'issues': ['Asian cooking appliances (47.9% Chinese)', 'hard water'],
        'coordinates': {'lat': '43.8561', 'lon': '-79.3370'},
        'nearby_cities': ['Richmond Hill', 'Vaughan', 'Toronto', 'Pickering'],
        'meta_description': 'Markham appliance repair. Samsung, LG, Whirlpool, GE experts. Asian cooking appliance specialists. Same-day service. Call 437-747-6737',
        'ai_expertise': 'Asian cooking appliance expertise (rice cookers, high-volume range hoods, wok ranges), Cornell compact home solutions, Unionville heritage home appliance installations',
        'hero_subtitle': 'From Unionville to Cornell, we fix Samsung, LG, Whirlpool, GE, and all major brands fast',
        'city_problems': [
            'High-volume range hood failures from Asian cooking (steam and smoke)',
            'Cornell new urbanism homes with narrow doorways and tight appliance access'
        ],
        'faq_location': 'Markham, including Unionville, Thornhill, Cornell, Markville, and Wismer'
    },
    'vaughan': {
        'name': 'Vaughan',
        'population': '323,000',
        'neighborhoods': ['Woodbridge', 'Thornhill', 'Concord', 'Maple'],
        'issues': ['Italian community (30%)', 'hard water (125 mg/L)', 'large homes'],
        'coordinates': {'lat': '43.8371', 'lon': '-79.4983'},
        'nearby_cities': ['Richmond Hill', 'Markham', 'Brampton', 'Toronto'],
        'meta_description': 'Vaughan appliance repair. Samsung, LG, Whirlpool, GE, Miele experts. Hard water solutions, Italian cooking appliances. Same-day service. Call 437-747-6737',
        'ai_expertise': 'Premium European appliance repairs (Miele, Bosch), Italian cooking appliance expertise (espresso systems, wine fridges), hard water (125 mg/L) solutions',
        'hero_subtitle': 'From Woodbridge to Maple, we fix Samsung, LG, Whirlpool, GE, and all major brands fast',
        'city_problems': [
            'Hard water (125 mg/L) causing dishwasher and steam oven limescale buildup',
            'Woodbridge multi-kitchen estates with multiple appliance sets'
        ],
        'faq_location': 'Vaughan, including Woodbridge, Thornhill, Concord, and Maple'
    },
    'oakville': {
        'name': 'Oakville',
        'population': '194,000',
        'neighborhoods': ['Old Oakville', 'Glen Abbey', 'Bronte', 'Uptown Core'],
        'issues': ['Waterfront corrosion (Lake Ontario)', 'heritage home restrictions', 'empty nesters'],
        'coordinates': {'lat': '43.4675', 'lon': '-79.6877'},
        'nearby_cities': ['Burlington', 'Mississauga', 'Milton', 'Hamilton'],
        'meta_description': 'Oakville appliance repair. Samsung, LG, Whirlpool, GE experts. Waterfront corrosion solutions, premium appliances. Same-day service. Call 437-747-6737',
        'ai_expertise': 'Waterfront corrosion repairs (Bronte, Old Oakville), premium European appliance service, downsizer compact appliance solutions',
        'hero_subtitle': 'From Old Oakville to Glen Abbey, we fix Samsung, LG, Whirlpool, GE, and all major brands fast',
        'city_problems': [
            'Lake Ontario humidity causing refrigerator compressor rust and dishwasher corrosion',
            'Heritage home electrical upgrades for modern appliances'
        ],
        'faq_location': 'Oakville, including Old Oakville, Glen Abbey, Bronte, and Uptown Core'
    },
    'burlington': {
        'name': 'Burlington',
        'population': '186,000',
        'neighborhoods': ['Aldershot', 'Downtown Burlington', 'Tyandaga', 'Orchard'],
        'issues': ['Oldest population (43.3 years median age)', 'waterfront corrosion', '1960s aluminum wiring'],
        'coordinates': {'lat': '43.3255', 'lon': '-79.7990'},
        'nearby_cities': ['Oakville', 'Hamilton', 'Milton', 'Mississauga'],
        'meta_description': 'Burlington appliance repair. Samsung, LG, Whirlpool, GE experts. Legacy appliance repairs, waterfront corrosion solutions. Same-day service. Call 437-747-6737',
        'ai_expertise': 'Legacy appliance repairs (1980s-90s models), waterfront double-corrosion solutions (Hamilton Harbour + Lake Ontario), Aldershot renovation electrical upgrades',
        'hero_subtitle': 'From Aldershot to Downtown Burlington, we fix Samsung, LG, Whirlpool, GE, and all major brands fast',
        'city_problems': [
            'Aging appliances (25-35 years old) with discontinued parts',
            'Waterfront corrosion from Hamilton Harbour and Lake Ontario humidity'
        ],
        'faq_location': 'Burlington, including Aldershot, Downtown Burlington, Tyandaga, and Orchard'
    },
    'oshawa': {
        'name': 'Oshawa',
        'population': '166,000',
        'neighborhoods': ['Downtown Oshawa', 'Eastdale', 'Taunton', 'Northwood'],
        'issues': ['Durham hard water', 'automotive industry workers (shift work)', 'affordable housing'],
        'coordinates': {'lat': '43.8971', 'lon': '-78.8658'},
        'nearby_cities': ['Whitby', 'Ajax', 'Pickering', 'Courtice'],
        'meta_description': 'Oshawa appliance repair. Samsung, LG, Whirlpool, GE experts. Durham hard water solutions, shift worker schedules. Same-day service. Call 437-747-6737',
        'ai_expertise': 'Durham Region hard water treatment, flexible scheduling for shift workers, affordable repair solutions for budget-conscious homeowners',
        'hero_subtitle': 'From Downtown Oshawa to Northwood, we fix Samsung, LG, Whirlpool, GE, and all major brands fast',
        'city_problems': [
            'Durham hard water causing mineral buildup in dishwashers and washing machines',
            'Delayed-start appliance repairs for automotive shift workers'
        ],
        'faq_location': 'Oshawa, including Downtown Oshawa, Eastdale, Taunton, and Northwood'
    },
    'ajax': {
        'name': 'Ajax',
        'population': '126,000',
        'neighborhoods': ['Northeast Ajax', 'Westney Heights', 'Riverside', 'Central Ajax'],
        'issues': ['Durham hard water', 'commuter lifestyle (delay-start timers)', 'young families', 'basement flooding'],
        'coordinates': {'lat': '43.8509', 'lon': '-79.0204'},
        'nearby_cities': ['Pickering', 'Whitby', 'Oshawa', 'Toronto'],
        'meta_description': 'Ajax appliance repair. Samsung, LG, Whirlpool, GE experts. Durham hard water solutions, commuter-friendly service. Same-day service. Call 437-747-6737',
        'ai_expertise': 'Durham Region hard water solutions, delay-start timer repairs for commuters, heavy family usage repairs for young households',
        'hero_subtitle': 'From Northeast Ajax to Westney Heights, we fix Samsung, LG, Whirlpool, GE, and all major brands fast',
        'city_problems': [
            'Durham hard water with unique mineral composition causing scaling',
            'Washer/dryer delay timer failures from unattended overnight operation'
        ],
        'faq_location': 'Ajax, including Northeast Ajax, Westney Heights, Riverside, and Central Ajax'
    },
    'pickering': {
        'name': 'Pickering',
        'population': '99,000',
        'neighborhoods': ['Seaton', 'Duffin Heights', 'Liverpool', 'City Centre'],
        'issues': ['Seaton mega-development (new homes 2015-2020)', 'Tarion warranty expiration', 'Durham hard water'],
        'coordinates': {'lat': '43.8384', 'lon': '-79.0868'},
        'nearby_cities': ['Ajax', 'Whitby', 'Markham', 'Toronto'],
        'meta_description': 'Pickering appliance repair. Samsung, LG, Whirlpool, GE experts. Seaton new home warranty support, Durham hard water solutions. Same-day service. Call 437-747-6737',
        'ai_expertise': 'Seaton mega-development appliance repairs, post-warranty builder-grade appliance fixes, Durham Region hard water treatment',
        'hero_subtitle': 'From Seaton to Duffin Heights, we fix Samsung, LG, Whirlpool, GE, and all major brands fast',
        'city_problems': [
            'Seaton mass construction failures (identical builder appliances failing simultaneously)',
            'Durham hard water clogging washing machine inlet screens within 18-24 months'
        ],
        'faq_location': 'Pickering, including Seaton, Duffin Heights, Liverpool, and City Centre'
    },
    'milton': {
        'name': 'Milton',
        'population': '110,000',
        'neighborhoods': ['Old Milton', 'Harrison', 'Dempsey', 'Timberlea', 'Transit Hub'],
        'issues': ['Well water (400+ mg/L) vs municipal (150 mg/L)', 'Niagara Escarpment temperature swings', 'builder boom failures'],
        'coordinates': {'lat': '43.5183', 'lon': '-79.8774'},
        'nearby_cities': ['Oakville', 'Burlington', 'Mississauga', 'Georgetown'],
        'meta_description': 'Milton appliance repair. Samsung, LG, Whirlpool, GE experts. Well water solutions, Escarpment climate expertise. Same-day service. Call 437-747-6737',
        'ai_expertise': 'Well water vs municipal water diagnostics (400+ mg/L vs 150 mg/L), Niagara Escarpment climate stress repairs, builder boom mass failure solutions',
        'hero_subtitle': 'From Old Milton to Harrison, we fix Samsung, LG, Whirlpool, GE, and all major brands fast',
        'city_problems': [
            'Extreme well water hardness (400+ mg/L) causing dishwasher heating element failures every 18-24 months',
            'Escarpment temperature swings stressing refrigerator compressors in garage installations'
        ],
        'faq_location': 'Milton, including Old Milton, Harrison, Dempsey, Timberlea, and Transit Hub'
    }
}

def read_template():
    with open('locations/richmond-hill.html', 'r', encoding='utf-8') as f:
        return f.read()

def replace_city_data(template, city_key):
    city = cities[city_key]
    content = template

    # IMPORTANT: Do specific replacements BEFORE general city name replacement
    # Replace meta description (both regular and HTML-encoded versions)
    old_desc1 = 'Richmond Hill appliance repair experts. Oak Ridges well water fix. Persian &amp; Chinese community experts. Same-day service. Call 437-747-6737'
    old_desc2 = 'Richmond Hill appliance repair experts. Oak Ridges well water fix. Persian & Chinese community experts. Same-day service. Call 437-747-6737'
    content = content.replace(old_desc1, city['meta_description'])
    content = content.replace(old_desc2, city['meta_description'])

    # Replace title
    old_title = '<title>Richmond Hill Appliance Repair | Same-Day Fix</title>'
    new_title = f'<title>{city["name"]} Appliance Repair | Fast Service Available</title>'
    content = content.replace(old_title, new_title)

    # Replace Open Graph description (both regular and HTML-encoded versions)
    og_desc_old1 = 'Richmond Hill appliance repair. Oak Ridges well water solutions. Persian &amp; Chinese community experts. Same-day service. Call 437-747-6737'
    og_desc_old2 = 'Richmond Hill appliance repair. Oak Ridges well water solutions. Persian & Chinese community experts. Same-day service. Call 437-747-6737'
    content = content.replace(og_desc_old1, city['meta_description'])
    content = content.replace(og_desc_old2, city['meta_description'])

    # Replace Twitter description
    twitter_desc_old = 'Richmond Hill appliance repair. Oak Ridges well water solutions. Persian &amp; Chinese community experts. Same-day service.'
    twitter_desc_new = city['meta_description'].replace('Call 437-747-6737', '').strip()
    content = content.replace(twitter_desc_old, twitter_desc_new)

    # Replace coordinates in schema
    content = content.replace('"latitude": "44.0389"', f'"latitude": "{city["coordinates"]["lat"]}"')
    content = content.replace('"longitude": "-79.4537"', f'"longitude": "{city["coordinates"]["lon"]}"')

    # Replace areaServed cities - do individual replacements
    content = content.replace('"name": "Richmond Hill"', f'"name": "{city["name"]}"', 1)  # First occurrence only
    content = content.replace('"name": "Oak Ridges"', f'"name": "{city["nearby_cities"][0]}"')
    content = content.replace('"name": "Vaughan"', f'"name": "{city["nearby_cities"][1]}"')
    content = content.replace('"name": "Markham"', f'"name": "{city["nearby_cities"][2]}"')
    content = content.replace('"name": "Aurora"', f'"name": "{city["nearby_cities"][3]}"')

    # Replace AI Answer Box H2
    ai_h2_old = 'Looking for reliable appliance repair in Richmond Hill?'
    ai_h2_new = f'Looking for reliable appliance repair in {city["name"]}?'
    content = content.replace(ai_h2_old, ai_h2_new)

    # Replace AI expertise section
    ai_expertise_old = '<strong>Richmond Hill expertise:</strong> Oak Ridges well water solutions (400+ mg/L hardness), Yonge Corridor compact European appliances (18-24"), serving all neighborhoods including Bayview Hill, Westbrook, and Elgin Mills.'
    ai_expertise_new = f'<strong>{city["name"]} expertise:</strong> {city["ai_expertise"]}'
    content = content.replace(ai_expertise_old, ai_expertise_new)

    # Replace hero subtitle
    hero_old = 'From Oak Ridges to Yonge Street, we fix Samsung, LG, Whirlpool, GE, and all major brands fast'
    content = content.replace(hero_old, city['hero_subtitle'])

    # Replace city-specific problems in Common Problems section
    # We'll find the section and add city-specific items
    problem1_old = 'Oak Ridges well water causing extreme mineral buildup'
    problem2_old = 'Persian cooking appliances needing specialized repair'
    content = content.replace(problem1_old, city['city_problems'][0])
    content = content.replace(problem2_old, city['city_problems'][1])

    # Replace the detailed problem sections
    # Problem 1 - Well water challenge (H3 and paragraph)
    h3_1_old = 'How to Fix Oak Ridges Well Water Damage Flooding Your Richmond Hill Home?'
    h3_1_new = f'How to Fix {city["city_problems"][0].split(" causing")[0].split(" (")[0]}?'
    content = content.replace(h3_1_old, h3_1_new)

    # Problem 1 paragraph
    p1_old = '<strong>Richmond Hill Challenge:</strong> Oak Ridges well water has extreme hardness (400+ mg/L vs. 150 municipal) causing urgent stress: brown stains on dishes and clothes, completely clogged dishwasher spray arms causing flooding, and seized washing machine inlet valves. <strong>What Causes This:</strong> Mineral buildup from hard well water destroys appliances fast. <strong>How to Fix It:</strong> Industrial descaling, component replacement, inline sediment filters, and water softener systems. <strong>Cost: $220-$380.</strong>'
    p1_new = f'<strong>{city["name"]} Challenge:</strong> {city["city_problems"][0]}. <strong>What Causes This:</strong> Local conditions create unique appliance stress. <strong>How to Fix It:</strong> Specialized diagnostics, component replacement, preventive solutions, and expert local knowledge. <strong>Cost: $220-$380.</strong>'
    content = content.replace(p1_old, p1_new)

    # Problem 2 - Compact appliances challenge (H3 and paragraph)
    h3_2_old = 'Yonge Corridor 18-24" Compact European Appliances Without Parts'
    h3_2_new = f'How to Fix {city["city_problems"][1].split(" (")[0]}?'
    content = content.replace(h3_2_old, h3_2_new)

    # Problem 2 paragraph
    p2_old = '<strong>Richmond Hill Challenge:</strong> New Yonge Corridor condos (Major Mackenzie to Elgin Mills) feature 18-24" European compact appliances like Bosch, Blomberg, and Asko. Most repair companies don\'t stock metric parts, creating 5-7 day delays or outright service refusals. <strong>Our Solution:</strong> European parts stocked in inventory (metric fittings, 220V components), experienced with all major European brands, condo building access coordination, and fast service without week-long waits. <strong>Typical Cost: $200-$400.</strong>'
    p2_new = f'<strong>{city["name"]} Challenge:</strong> {city["city_problems"][1]}. <strong>Our Solution:</strong> Local expertise, specialized parts inventory, fast diagnosis, and same-day service when possible. <strong>Typical Cost: $200-$400.</strong>'
    content = content.replace(p2_old, p2_new)

    # Problem 3 - Cooking appliances (H3 and paragraph) - make generic
    h3_3_old = 'How to Fix Residential Ranges for Persian & Chinese Cooking in Richmond Hill?'
    h3_3_new = f'How to Fix Common Appliance Issues in {city["name"]}?'
    content = content.replace(h3_3_old, h3_3_new)

    # Problem 3 paragraph - simplified for all cities
    p3_old = '<strong>Richmond Hill Challenge:</strong> Richmond Hill\'s Chinese (28.5%, 57,600+ residents) and Persian (10.1%, 20,400+ residents) communities face urgent stress when residential burners fail during wok cooking, Persian tahdig, or kebabs. Food spoils and special meals are ruined. <strong>What Causes Failures:</strong> High-heat traditional cooking causes unique wear. <strong>How to Fix It:</strong> We repair residential ranges (up to 18,000 BTU), source parts for Asian brands (Midea, Haier) and major residential brands (Samsung, LG, Whirlpool, GE), understand traditional cooking needs, and calibrate for optimal performance. <strong>Cost: $200-$450.</strong>'
    p3_new = f'<strong>{city["name"]} Challenge:</strong> Local families face urgent stress when appliances fail unexpectedly. Food spoils, routines disrupted, and daily life interrupted. <strong>What Causes Failures:</strong> Normal wear and tear plus local conditions create unique challenges. <strong>How to Fix It:</strong> We repair all major residential brands (Samsung, LG, Whirlpool, GE, Bosch, KitchenAid), maintain large parts inventory, understand local needs, and provide fast same-day service. <strong>Cost: $200-$450.</strong>'
    content = content.replace(p3_old, p3_new)

    # Replace FAQ location reference
    faq_old = 'Richmond Hill, including Oak Ridges and Yonge Street corridor'
    content = content.replace(faq_old, city['faq_location'])

    # NOW do general city name replacement (after all specific strings)
    content = content.replace('Richmond Hill', city['name'])
    content = content.replace('richmond-hill', city_key)

    return content

def main():
    print("Creating 10 new location pages based on Richmond Hill template...\n")

    template = read_template()
    results = []

    for city_key in cities.keys():
        print(f"Creating {cities[city_key]['name']} page...")

        new_content = replace_city_data(template, city_key)

        output_file = f'locations/{city_key}.html'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(new_content)

        # Count words (approximate)
        word_count = len(new_content.split())
        results.append({
            'city': cities[city_key]['name'],
            'file': output_file,
            'words': word_count
        })

        print(f"  [OK] Created {output_file} ({word_count} words)")

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    for result in results:
        print(f"{result['city']:20} | {result['words']:6} words | {result['file']}")

    print(f"\nTotal pages created: {len(results)}")
    print("\nAll files created successfully!")

if __name__ == "__main__":
    main()
