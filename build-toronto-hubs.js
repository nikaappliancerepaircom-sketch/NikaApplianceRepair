// build-toronto-hubs.js
// Generates 21 Toronto neighborhood hub pages + locations/index.html
// Appends "Service Coverage by Toronto Neighborhood" section to locations/toronto.html
// Run: node build-toronto-hubs.js

const fs = require('fs');
const path = require('path');

const ROOT = __dirname;
const LOCATIONS_DIR = path.join(ROOT, 'locations');
const SERVICES_DIR = path.join(LOCATIONS_DIR, 'services');

// Toronto neighborhoods with display names + 4-5 unique facts per neighborhood
// (drawn from existing services pages — used for unique 400+ word hubs)
const NEIGHBORHOODS = {
    'bloor-west-village': {
        name: 'Bloor West Village',
        intro: 'Bloor West Village is a tight-knit west-end community along Bloor Street between Jane and Runnymede, defined by Edwardian and turn-of-the-century semi-detached homes, mature tree canopy, and an active main-street retail strip.',
        facts: [
            'Most homes were built between 1905 and 1925, meaning kitchens have been renovated multiple times — older 110V circuits and shallow under-counter clearances often complicate dishwasher and oven swaps.',
            'Many properties have finished basement laundry rooms with stacked washer-dryer towers; we carry low-profile dollies for narrow stair access.',
            'The neighborhood has hard Lake Ontario municipal water (around 130 mg/L), so dishwasher heating elements and washer inlet valves scale up faster than the GTA average.',
            'Bloor West condos near Runnymede station typically use 24-inch European-spec appliances (Bosch, Miele, Blomberg) — we keep common parts on the truck.',
            'Street parking on Bloor is metered and tightly enforced; we schedule longer service windows on weekday afternoons to avoid morning permit conflicts.'
        ]
    },
    'chinatown': {
        name: 'Chinatown',
        intro: 'Chinatown along Spadina and Dundas is one of Toronto\'s densest residential-commercial districts, mixing pre-war row houses, post-war apartment walk-ups, and newer condo towers above ground-floor retail.',
        facts: [
            'Heavy daily cooking — including wok cooking with high-temperature oils and starches — pushes more food debris through dishwashers than average, so drain filters and spray arms need cleaning more often.',
            'Older Spadina and Dundas row houses have built-in dishwashers in compact galley kitchens; full replacement often requires disconnecting plumbing under cramped counters, making repair the more practical option.',
            'Haier and other Asian-market brand appliances are increasingly common here; we service these alongside Samsung, LG, and all North American makes.',
            'Parking on Spadina is restricted; technicians scout legal short-stay options on side streets like Beverley and Huron and carry compact tool kits to minimize street time.',
            'Many residential units sit above commercial kitchens — vibration and ventilation patterns affect freezer condensers and dryer ducts in ways unique to mixed-use buildings.'
        ]
    },
    'corso-italia': {
        name: 'Corso Italia',
        intro: 'Corso Italia stretches along St. Clair Avenue West from Dufferin to Lansdowne and remains one of Toronto\'s most established Italian-Canadian neighborhoods, with two- and three-storey row houses and detached homes from the 1910s–1940s.',
        facts: [
            'Many homes have second kitchens in the basement used for canning, pasta-making, and big-batch cooking; these often house older but well-maintained gas stoves that need igniter, thermocouple, and burner work.',
            'Side-by-side American refrigerators are popular here for hosting large family gatherings — ice maker and water dispenser repairs are common service calls.',
            'Older homes still have galvanized supply lines that introduce sediment into dishwasher inlet valves and washer hoses; we recommend in-line filters during repairs.',
            'Outdoor pizza ovens and grills are common in backyards, but indoor wall ovens and ranges still see heavy weekly use — door hinges and self-clean motors wear faster than average.',
            'Streetcar tracks on St. Clair create temporary parking restrictions; we book service windows that avoid construction and track-maintenance schedules.'
        ]
    },
    'dufferin-grove': {
        name: 'Dufferin Grove',
        intro: 'Dufferin Grove sits between Bloor and College, west of Dufferin Street, anchored by its namesake park and a mix of Victorian row houses, Edwardian semis, and a growing wave of mid-rise infill condos.',
        facts: [
            'Tall, narrow Victorian homes here often have laundry tucked into narrow basement nooks — stacked units are the norm, and lint-trap and venting issues are the most common dryer call.',
            'Kitchens in the row houses are typically galley-style and sit at the back of the home, so we use protective floor covering for long appliance carries down the central hallway.',
            'The neighborhood has a high concentration of rental units; we coordinate access with property managers and provide written invoices that meet Landlord-Tenant Board documentation standards.',
            'Many homes have been retrofitted with European-spec 24-inch fridges and dishwashers (Liebherr, Bosch) to fit narrow kitchens — we stock common 24-inch parts.',
            'Older knob-and-tube remnants in some homes mean appliance circuits sometimes share legs; intermittent issues often turn out to be electrical rather than mechanical.'
        ]
    },
    'east-york': {
        name: 'East York',
        intro: 'East York covers the area roughly bounded by the Don Valley, Victoria Park, O\'Connor, and Danforth, with bungalows from the 1940s–50s, post-war semis, and a steady wave of teardown rebuilds and basement-suite conversions.',
        facts: [
            'Bungalow kitchens often have 30-inch freestanding ranges and top-mount fridges — the most common service calls are oven igniter replacement and refrigerator defrost-thermostat issues.',
            'Many homes have basement in-law suites with second laundry pairs; we frequently service mismatched units installed across different decades.',
            'The 1950s-era electrical panels in some original bungalows top out at 60 amps — induction ranges and large electric dryers require panel upgrades, which we flag during diagnosis.',
            'Hard Lake Ontario water (around 130 mg/L) plus older galvanized supply lines lead to scale buildup in dishwasher heaters and washer solenoids; descaling is part of most service visits.',
            'Streets here permit easy curbside parking, so service windows are predictable; we typically arrive within a 1-hour window for East York calls.'
        ]
    },
    'etobicoke-village': {
        name: 'Etobicoke Village',
        intro: 'Etobicoke Village (the area around Burnhamthorpe and Kipling, sometimes called Old Etobicoke) blends post-war ranch homes, mid-century split-levels, and newer detached infill on generous lots.',
        facts: [
            'Larger lots mean larger kitchens and full-size 36-inch refrigerators with French doors and ice makers — water-line and ice-maker repairs make up about a third of our calls here.',
            'Many homes have full laundry rooms (not closets), so front-load and top-load full-size washer-dryer pairs dominate; suspension and shock-absorber wear is the leading washer issue.',
            'Garage-attached kitchens sometimes have second freezers in the garage; cold-Toronto-winter starting issues on chest freezers are a seasonal call between December and February.',
            'Pool-equipped homes in the area often have wet bars with secondary fridges and ice machines; we service these built-ins alongside primary kitchen appliances.',
            'Newer 200-amp panels on rebuilt homes accommodate dual-fuel ranges and induction cooktops, which we service for both gas igniters and electric control boards.'
        ]
    },
    'greektown': {
        name: 'Greektown',
        intro: 'Greektown on the Danforth runs from Broadview to Pape and remains one of Toronto\'s most active main-street neighborhoods, with brick semis and detached homes from the 1900s–1930s plus a steady mix of restaurants and small commercial kitchens.',
        facts: [
            'Heavy weekend cooking and large family meals push ovens and ranges harder than average; door hinges, self-clean motors, and convection fans are common repair points.',
            'Many homes have subway-tile kitchens with built-in 24-inch dishwashers; tight under-counter clearances mean replacements are difficult, so repair almost always wins on cost.',
            'Older basements with bottled-tile floors sometimes hide laundry pairs in furnace rooms; we carry flexible duct kits for tight dryer venting.',
            'On-street parking on the Danforth is metered and time-limited; weekday morning service slots are easiest to book.',
            'Small commercial kitchens above and behind retail share residential service grids — voltage drops during peak hours occasionally trigger phantom appliance error codes we diagnose as building-side, not appliance-side.'
        ]
    },
    'high-park': {
        name: 'High Park',
        intro: 'The High Park neighborhood spans the area around the city\'s largest park, including Roncesvalles-adjacent residential streets and the apartment-tower corridor along Bloor West, mixing detached Edwardians, post-war high-rises, and contemporary townhomes.',
        facts: [
            'High-rise apartments along Bloor West typically have full-size washer-dryer pairs in stacked closets; common calls are dryer no-heat (vent obstruction) and washer drain pump failures.',
            'Detached homes near High Park often have finished basement kitchens used as second households; we service older but functional 1990s-2000s appliances kept in service for decades.',
            'Stacked condo washer-dryer combos (often Whirlpool or LG) require careful disassembly to access internal components; we keep the right wrenches for their unique top-shelf mounts.',
            'Mature tree roots in the High Park area occasionally affect drain and sewer flow — slow-draining washers turn out to be building-side rather than pump issues about 1 in 8 visits.',
            'Older buildings have weak elevator capacity; we use service elevators during off-peak hours and coordinate with building management for delivery of large parts.'
        ]
    },
    'king-west': {
        name: 'King West',
        intro: 'King West runs from Bathurst to Strachan along King Street West and is dominated by glass condo towers from the 2000s–2020s, plus a small remaining stock of Victorian and warehouse-conversion lofts.',
        facts: [
            'Almost every unit has a 24-inch European-spec stacked or all-in-one washer-dryer combo (Bosch, Whirlpool Duet compact, Miele, LG); we stock door boots, drain pumps, and control boards specific to these models.',
            'Condo kitchens use 24-inch built-in dishwashers and panel-ready fridges (Fisher & Paykel, Liebherr, Bosch); we coordinate cabinet-panel reinstallation when service requires unit removal.',
            'Building service-elevator booking is required for any work involving full appliance removal — we coordinate 24–48 hours in advance with concierge and property management.',
            'Power-quality fluctuations during peak grid demand occasionally trigger error codes on smart appliances; we differentiate building-power issues from genuine board faults during diagnosis.',
            'Loft conversions along King West sometimes have appliances installed in non-standard locations (open-plan kitchens, kitchen islands); we work around exposed-duct ceilings and concrete floors.'
        ]
    },
    'little-italy': {
        name: 'Little Italy',
        intro: 'Little Italy along College Street between Bathurst and Ossington is a mix of two- and three-storey Victorian and Edwardian semis, restaurants, and condo infill, with strong family ownership and multi-generational households.',
        facts: [
            'Basement cantinas and second kitchens with old-school gas ranges and chest freezers are common; we frequently service appliances 20+ years old that owners want kept running.',
            'Tall, narrow houses mean kitchens are small and dishwashers sit under prep counters in tight quarters — pulling a unit usually requires temporary plumbing disconnects we handle on-site.',
            'Hard municipal water plus heavy daily cooking lead to faster scale buildup on dishwasher heaters; we descale during repair visits.',
            'Side-by-side American fridges with ice makers are popular for big family gatherings; ice-maker and water-line repairs are the most common refrigerator call.',
            'College Street parking is metered; we schedule longer Little Italy windows to allow proper diagnosis time without rushing.'
        ]
    },
    'little-portugal': {
        name: 'Little Portugal',
        intro: 'Little Portugal sits roughly between Bathurst and Lansdowne, south of College and north of Queen, with brick row houses and semis from the 1900s–1920s and a recent wave of younger families and infill condos.',
        facts: [
            'Older homes here often have small kitchens with 24-inch ranges and apartment-size fridges; we keep parts for both heritage and current 24-inch models.',
            'Many houses have basement secondary kitchens with industrial-style appliances used for batch cooking and canning — gas stove igniter and oven thermostat work is a common call.',
            'Front-load washers in basement laundry rooms often suffer from drum-bearing wear because of the heavy water content typical of Toronto municipal supply; we flag bearing wear during pump diagnostics.',
            'Two-way streets and tight semi-detached driveways limit truck access; we use compact service vehicles and carry parts in shoulder bags for narrow walk-ups.',
            'Dryer venting through long basement runs is a recurring source of no-heat and overheating issues — we inspect and clean ducts as part of dryer diagnosis.'
        ]
    },
    'midtown': {
        name: 'Midtown',
        intro: 'Midtown Toronto centers around Yonge and Eglinton and includes Davisville, Forest Hill South, and Mount Pleasant West, mixing pre-war detached homes, post-war apartment towers, and a rapid wave of new mid- and high-rise condos.',
        facts: [
            'High-rise condos along Yonge typically have premium 24-inch panel-ready European dishwashers and stacked Bosch or Whirlpool laundry — we stock parts for the most common 12-15 condo models in the area.',
            'Pre-war detached homes north of Eglinton often have full-size 30-inch ranges and 36-inch French-door fridges; ice maker and dispenser repairs lead refrigerator calls.',
            'The Eglinton Crosstown construction has affected access on many side streets; we monitor TTC and city closures and adjust arrival times accordingly.',
            'Older apartment buildings (1950s–60s) along Mount Pleasant have communal laundry rooms still using coin-operated commercial-grade Speed Queens — for in-suite repairs, we focus on residential 24-inch and full-size pairs.',
            'Power issues from older condo electrical rooms occasionally manifest as appliance error codes; we differentiate building-side from appliance-side faults during diagnosis.'
        ]
    },
    'ossington': {
        name: 'Ossington',
        intro: 'The Ossington strip and surrounding residential blocks between Queen and Dundas blend Victorian and Edwardian row houses with newer mid-rise infill, restaurants, and small commercial kitchens.',
        facts: [
            'Smaller kitchens in row houses often use 24-inch ranges and apartment-size fridges; we keep parts for both contemporary European 24-inch and older North American 24-inch models.',
            'Many residential units sit above restaurants — vibration, exhaust fan loads, and shared HVAC affect freezer compressor cycles in upper-floor apartments.',
            'Front-load washers in basement laundry are common; the heavy use typical of younger sharing households leads to faster door-boot and drain-pump wear.',
            'Older homes have undersized 60-amp panels in some cases; running a modern induction range or large electric dryer requires panel work, which we flag during diagnosis.',
            'On-street permit parking is tight; technicians arrive in compact service vehicles and use the most efficient legal parking option for each block.'
        ]
    },
    'parkdale': {
        name: 'Parkdale',
        intro: 'Parkdale stretches along Queen West from Dufferin to Roncesvalles, with grand Victorian mansions converted into rooming houses and apartments, plus newer infill condos and rental towers along King and Queen.',
        facts: [
            'Many subdivided Victorians have multiple compact kitchens per building, each with its own 24-inch range and apartment-size fridge — we maintain inventory of common parts for high-density units.',
            'Apartment towers along Jameson and Tyndall use common-area laundry rooms with coin-operated washers and dryers; in-suite repairs typically focus on residential 24-inch units in newer buildings.',
            'Front-load washers wear faster here due to heavy household use across shared rentals — drain pumps and door boots are the leading service items.',
            'Older homes still have gas service to original kitchens; we coordinate with Enbridge or Toronto Hydro when a gas line needs verification before stove or dryer reinstallation.',
            'Queen West parking is metered; weekday off-peak windows give us the smoothest access for full-service appointments.'
        ]
    },
    'roncesvalles': {
        name: 'Roncesvalles',
        intro: 'Roncesvalles Village runs along Roncesvalles Avenue between Bloor and Queensway and remains a strong Polish-Canadian community, with brick semis and detached homes from 1905–1925 and a thriving main-street retail district.',
        facts: [
            'Many homes still have original woodwork and tight kitchens with 24-inch built-in dishwashers; replacement is intrusive, so repair is almost always the right call.',
            'Basement secondary kitchens are common for canning and pierogi-making; older but well-maintained gas ranges need periodic igniter and thermocouple service.',
            'Hard Lake Ontario water plus the heavy water demand of multi-generational households leads to faster scale buildup on washer inlet valves and dishwasher heaters.',
            'Roncesvalles streetcar service means partial street closures during track work — we monitor TTC schedules and book windows that avoid construction.',
            'Stacked laundry pairs in narrow basement nooks are common; we use low-profile dollies for safe stair extraction during pump or motor service.'
        ]
    },
    'st-lawrence': {
        name: 'St. Lawrence',
        intro: 'The St. Lawrence neighborhood east of Yonge along Front and King streets combines warehouse loft conversions, the St. Lawrence Market district, and newer condo towers, with a mix of working professionals and longtime residents.',
        facts: [
            'Almost every condo here has a 24-inch panel-ready dishwasher and stacked or all-in-one washer-dryer combo; we stock common boards, pumps, and door seals for the most-installed brands (Bosch, Whirlpool, Miele).',
            'Loft conversions in the warehouse blocks have appliances installed against exposed-brick walls and beneath ducting — repairs require careful access planning we handle during the diagnostic visit.',
            'Concierge and service-elevator booking is required for full appliance removal — we coordinate 24–48 hours in advance with building management.',
            'Power-quality variations during peak demand can trigger smart-appliance error codes; we distinguish building-side power issues from genuine appliance faults during diagnosis.',
            'Many St. Lawrence Market-area lofts use compact European fridges (Liebherr, Blomberg); we carry common compressor relays and door-gasket kits.'
        ]
    },
    'swansea': {
        name: 'Swansea',
        intro: 'Swansea sits between High Park and the Humber River, with detached Edwardian and post-war homes, mature treed lots, and one of the most stable owner-occupied housing stocks in west Toronto.',
        facts: [
            'Larger detached homes typically have 30-inch ranges, 36-inch French-door fridges, and full-size laundry pairs — full residential appliance loads, not condo-spec compact units.',
            'Many homes have second kitchens in finished basements; older but functional 1990s–2000s appliances kept in service are common service candidates.',
            'Treed lots and humid summers mean refrigerator compressors run harder — defrost thermostat and condenser-fan failures are seasonal calls between July and September.',
            'Older Swansea homes have galvanized supply lines that introduce sediment to dishwasher inlet valves; we recommend in-line filters during repair.',
            'Detached driveways give us straightforward truck access; service windows here are typically the most predictable in west Toronto.'
        ]
    },
    'the-beaches': {
        name: 'The Beaches',
        intro: 'The Beaches runs along Queen Street East from Coxwell to Victoria Park, fronting the Lake Ontario shoreline, with detached and semi-detached Edwardian and Victorian homes plus a small but growing condo presence near Woodbine.',
        facts: [
            'Lakeside humidity causes faster corrosion on appliance internals — refrigerator compressor terminals, oven control boards, and washer drain pumps need replacement more often than in inland neighborhoods.',
            'Many Beaches homes have small kitchens with 24-inch built-in dishwashers and panel-ready fridges; we stock common 24-inch parts.',
            'Cottage-style homes often have second kitchens in finished basements used during summer entertaining; older gas ranges and chest freezers see seasonal use, with start-up issues common in early summer.',
            'Sand and grit tracked indoors from beach access wears down washer drum bearings and dryer drum supports faster than average; we inspect bearings during pump service.',
            'On-street parking is tight in summer due to beach traffic; we book Beaches windows for early morning or late afternoon to avoid peak parking demand.'
        ]
    },
    'thorncliffe-park': {
        name: 'Thorncliffe Park',
        intro: 'Thorncliffe Park is a high-density apartment community between the Don Valley and Leaside, dominated by 1960s–70s concrete towers with a recent infill of mid-rise condos and townhomes.',
        facts: [
            'Almost all units have full-size laundry pairs in dedicated closets; common calls are dryer no-heat (often venting) and washer drain pump failures from heavy household loads.',
            'Communal laundry rooms in older buildings still use coin-operated commercial-grade Speed Queens; for in-suite repairs we focus on residential 24-inch and full-size pairs.',
            'Many family-sized units have side-by-side American fridges with ice makers — water-line and ice-maker repairs are the most common refrigerator call.',
            'Tower elevator capacity is limited; we book service elevators during off-peak hours and coordinate with property management for any large parts deliveries.',
            'Hard Lake Ontario municipal water (around 130 mg/L) leads to scale buildup on dishwasher heaters and washer solenoids; descaling is part of most repair visits.'
        ]
    },
    'trinity-bellwoods': {
        name: 'Trinity-Bellwoods',
        intro: 'Trinity-Bellwoods centers on its namesake park and runs between Bathurst and Ossington, south of Queen and north of Dundas, with Victorian semis, row houses, and a wave of younger residents and infill condos.',
        facts: [
            'Tight kitchens in Victorian row houses often use 24-inch ranges and built-in dishwashers; pulling and replacing built-ins is intrusive, so repair is almost always more practical.',
            'Basement laundry in narrow nooks is the norm; stacked units predominate, and lint-trap and venting issues lead the dryer service queue.',
            'Many homes have been retrofitted with European 24-inch fridges and dishwashers (Bosch, Liebherr, Blomberg) to fit narrow kitchens — we stock the most common parts.',
            'Ossington and Dundas streetcar service occasionally affects truck access; we monitor TTC schedules and book windows around construction.',
            'Younger renter-heavy buildings see heavy front-load washer use; door-boot wear and drain-pump failures are the leading washer issues.'
        ]
    },
    'wychwood': {
        name: 'Wychwood',
        intro: 'Wychwood (including Wychwood Park and Hillcrest Village) sits west of Bathurst and north of St. Clair, with detached Edwardian and Tudor-revival homes on mature treed lots, plus a small but stable condo presence near St. Clair West Station.',
        facts: [
            'Larger detached homes typically have full-size 30-inch ranges and 36-inch French-door fridges with ice makers; ice-maker and dispenser repairs lead refrigerator calls.',
            'Many homes still have original wood-paneled kitchens with built-in 24-inch dishwashers — repair almost always wins over replacement because of cabinet impact.',
            'Older homes near Wychwood Park have unique heritage features (servant kitchens, butler\'s pantries) that house secondary appliances we service alongside primary kitchens.',
            'Hard municipal water plus heavy household use lead to scale buildup on dishwasher heaters and washer inlet valves; we descale during repair.',
            'Mature trees and tight one-way streets in Wychwood Park can limit truck access; we use compact service vehicles and coordinate with the residents\' association for permit-restricted streets.'
        ]
    }
};

// Cities (existing GTA hubs)
const CITIES = [
    'ajax', 'aurora', 'brampton', 'burlington', 'caledon', 'east-gwillimbury',
    'etobicoke', 'halton-hills', 'markham', 'milton', 'mississauga', 'newmarket',
    'north-york', 'oakville', 'oshawa', 'pickering', 'richmond-hill', 'scarborough',
    'stouffville', 'toronto', 'vaughan', 'whitby'
];

const SERVICES = [
    { slug: 'dishwasher-repair', label: 'Dishwasher Repair', icon: '🍽️' },
    { slug: 'dryer-repair', label: 'Dryer Repair', icon: '🌀' },
    { slug: 'oven-repair', label: 'Oven Repair', icon: '🔥' },
    { slug: 'refrigerator-repair', label: 'Refrigerator Repair', icon: '🧊' },
    { slug: 'stove-repair', label: 'Stove Repair', icon: '🍳' },
    { slug: 'washer-repair', label: 'Washer Repair', icon: '🫧' }
];

function titleCase(slug) {
    return slug.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
}

function getExistingServices(neighborhood) {
    return SERVICES.filter(s => {
        const f = path.join(SERVICES_DIR, `${s.slug}-${neighborhood}.html`);
        return fs.existsSync(f);
    });
}

// === GENERATE NEIGHBORHOOD HUB PAGE ===
function generateNeighborhoodHub(slug, data) {
    const services = getExistingServices(slug);
    const name = data.name;
    const escName = name.replace(/'/g, '&#39;');

    const serviceCards = services.map(s => `
          <a href="/locations/services/${s.slug}-${slug}" class="service-link-card" style="display:block;background:white;border-radius:12px;padding:1.5rem;text-align:center;text-decoration:none;box-shadow:0 2px 8px rgba(0,0,0,0.08);border:1px solid #e9ecef;transition:box-shadow 0.2s;">
            <div style="font-size:2rem;margin-bottom:0.5rem;">${s.icon}</div>
            <div style="font-family:'Fredoka',cursive;font-size:1.1rem;color:#1976D2;font-weight:600;">${s.label}</div>
            <div style="font-size:0.85rem;color:#6c757d;margin-top:0.25rem;">${escName}</div>
          </a>`).join('\n');

    const factListItems = data.facts.map(f => `<li style="margin-bottom:0.75rem;">${f}</li>`).join('\n          ');

    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Same-day appliance repair in ${escName}, Toronto. Fridge, washer, dryer, oven, dishwasher &amp; stove. Certified since 2017. Call (437) 524-1053.">
    <title>Appliance Repair ${escName} | Same-Day Service | Nika</title>
    <link rel="canonical" href="https://nikaappliancerepair.com/locations/${slug}">

    <meta property="og:type" content="website">
    <meta property="og:title" content="Appliance Repair ${escName} | Same-Day Service | Nika">
    <meta property="og:description" content="Same-day appliance repair in ${escName}, Toronto. Fridge, washer, dryer, oven, dishwasher &amp; stove. Certified since 2017. Call (437) 524-1053.">
    <meta property="og:url" content="https://nikaappliancerepair.com/locations/${slug}">
    <meta property="og:image" content="https://nikaappliancerepair.com/assets/images/friendly-technician-character-min.webp">

    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "Nika Appliance Repair - ${escName}",
        "image": "https://nikaappliancerepair.com/assets/images/friendly-technician-character-min.webp",
        "url": "https://nikaappliancerepair.com/locations/${slug}",
        "telephone": "+14375241053",
        "email": "nicksappliancerepair@on.fixlify.app",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "755 Steeles Ave W #311",
            "addressLocality": "North York",
            "addressRegion": "ON",
            "postalCode": "M2R 3W9",
            "addressCountry": "CA"
        },
        "priceRange": "$$",
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.7",
            "reviewCount": "176",
            "bestRating": "5",
            "worstRating": "1"
        },
        "areaServed": [
            { "@type": "Place", "name": "${escName}" },
            { "@type": "City", "name": "Toronto" }
        ],
        "openingHoursSpecification": [
            { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "08:00", "closes": "20:00" },
            { "@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "09:00", "closes": "18:00" },
            { "@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "10:00", "closes": "17:00" }
        ]
    }
    </script>

    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://nikaappliancerepair.com/" },
            { "@type": "ListItem", "position": 2, "name": "Service Areas", "item": "https://nikaappliancerepair.com/locations" },
            { "@type": "ListItem", "position": 3, "name": "Toronto", "item": "https://nikaappliancerepair.com/locations/toronto" },
            { "@type": "ListItem", "position": 4, "name": "${escName}", "item": "https://nikaappliancerepair.com/locations/${slug}" }
        ]
    }
    </script>

    <link rel="preload" as="image" href="../assets/images/friendly-technician-character-min.webp" fetchpriority="high">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;500;600;700;800&family=Rubik:wght@300;400;500;600;700&display=swap" rel="stylesheet">

    <link rel="stylesheet" href="../css/tokens.css">
    <link rel="stylesheet" href="../css/design-system.css">
    <link rel="stylesheet" href="../css/style.css">
    <link rel="stylesheet" href="../css/header-v2-styles.css">
    <link rel="stylesheet" href="../css/header-optimized.css">
    <link rel="stylesheet" href="../css/footer-optimized.css">
    <link rel="stylesheet" href="../css/responsive-comprehensive.css">
    <link rel="stylesheet" href="../css/combined-fixes.css">
    <link rel="stylesheet" href="../css/cta-buttons.css">
    <link rel="stylesheet" href="../css/design-fixes-2026.css">
</head>
<body>
    <!-- Unified Header -->
    <div id="header-placeholder"></div>
    <script src="/includes/header-loader.js" defer></script>

    <!-- Hero -->
    <section class="hero-section" id="main-content" style="padding:3rem 0;background:linear-gradient(135deg,#e3f2fd 0%,#fff 100%);">
        <div class="container" style="max-width:1100px;margin:0 auto;padding:0 1rem;">
            <nav aria-label="Breadcrumb" style="font-size:0.9rem;color:#6c757d;margin-bottom:1rem;">
                <a href="/" style="color:#1976D2;text-decoration:none;">Home</a> &rsaquo;
                <a href="/locations" style="color:#1976D2;text-decoration:none;">Service Areas</a> &rsaquo;
                <a href="/locations/toronto" style="color:#1976D2;text-decoration:none;">Toronto</a> &rsaquo;
                <span>${escName}</span>
            </nav>
            <h1 style="font-family:'Fredoka',cursive;font-size:2.4rem;color:#0d47a1;margin-bottom:1rem;line-height:1.2;">Appliance Repair in ${escName}, Toronto</h1>
            <p style="font-size:1.15rem;color:#212529;line-height:1.6;max-width:850px;">Nika Appliance Repair has been the trusted same-day repair team for ${escName} homes since 2017. Call <a href="tel:4375241053" style="color:#1976D2;font-weight:600;">(437) 524-1053</a> for fridge, washer, dryer, oven, stove, and dishwasher service backed by a 90-day parts &amp; labour warranty.</p>
            <div style="margin-top:1.5rem;">
                <a href="tel:4375241053" class="cta-primary" style="display:inline-block;background:#1976D2;color:white;padding:0.9rem 1.6rem;border-radius:8px;text-decoration:none;font-weight:600;margin-right:0.5rem;">Call (437) 524-1053</a>
                <a href="/#book" class="cta-secondary" style="display:inline-block;background:white;color:#1976D2;padding:0.9rem 1.6rem;border-radius:8px;text-decoration:none;font-weight:600;border:2px solid #1976D2;">Book Online</a>
            </div>
        </div>
    </section>

    <!-- Service links -->
    <section style="background:#f8f9fa;padding:3rem 1rem;">
        <div style="max-width:1100px;margin:0 auto;">
            <h2 style="text-align:center;font-family:'Fredoka',cursive;color:#0d47a1;font-size:2rem;margin-bottom:0.5rem;">${escName} Appliance Repair Services</h2>
            <p style="text-align:center;color:#6c757d;margin-bottom:2rem;">Pick the appliance you need fixed — every page has local pricing, brand list, and same-day booking.</p>
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1rem;">${serviceCards}
            </div>
        </div>
    </section>

    <!-- About neighborhood -->
    <section style="background:white;padding:3rem 1rem;">
        <div style="max-width:900px;margin:0 auto;">
            <h2 style="font-family:'Fredoka',cursive;color:#0d47a1;font-size:1.8rem;margin-bottom:1rem;">Why ${escName} Homes Need a Specialist</h2>
            <p style="line-height:1.7;color:#212529;margin-bottom:1.5rem;">${data.intro}</p>
            <p style="line-height:1.7;color:#212529;margin-bottom:1.5rem;">Working in ${escName} for the better part of a decade has taught us that the housing stock and water conditions here create a recognizable pattern of appliance issues. Below are the local realities that shape almost every service call we run in this part of Toronto.</p>
            <h3 style="font-family:'Fredoka',cursive;color:#0d47a1;font-size:1.3rem;margin:1.5rem 0 1rem;">Local Service Notes for ${escName}</h3>
            <ul style="line-height:1.7;color:#212529;padding-left:1.25rem;">
          ${factListItems}
            </ul>
            <p style="line-height:1.7;color:#212529;margin-top:1.5rem;">Every visit starts with a $89 diagnostic that we waive when you proceed with the repair. Our technicians are insured, drug-tested, and arrive in marked vehicles. We back every job with a 90-day parts and labour warranty, and we use OEM parts wherever the manufacturer still produces them.</p>
            <p style="line-height:1.7;color:#212529;margin-top:1rem;">If your appliance is acting up, the fastest way to get a confirmed window is to call <a href="tel:4375241053" style="color:#1976D2;font-weight:600;">(437) 524-1053</a>. We answer seven days a week from 8&nbsp;a.m. to 8&nbsp;p.m. on weekdays and offer evening slots when same-day windows fill up. For non-urgent jobs, you can also book online at the bottom of this page and we will confirm by text within fifteen minutes.</p>
        </div>
    </section>

    <!-- Toronto context / related neighborhoods -->
    <section style="background:#f8f9fa;padding:3rem 1rem;">
        <div style="max-width:1100px;margin:0 auto;">
            <h2 style="text-align:center;font-family:'Fredoka',cursive;color:#0d47a1;font-size:1.8rem;margin-bottom:1rem;">More Toronto Neighborhoods We Serve</h2>
            <p style="text-align:center;color:#6c757d;margin-bottom:2rem;">${escName} is part of our full Toronto coverage map. Browse nearby areas:</p>
            <div style="display:flex;flex-wrap:wrap;gap:0.5rem;justify-content:center;">
                ${Object.entries(NEIGHBORHOODS).filter(([k]) => k !== slug).map(([k, v]) =>
                    `<a href="/locations/${k}" style="display:inline-block;padding:0.5rem 1rem;background:white;border-radius:20px;text-decoration:none;color:#1976D2;border:1px solid #e9ecef;font-size:0.9rem;">${v.name}</a>`
                ).join('\n                ')}
            </div>
            <div style="text-align:center;margin-top:2rem;">
                <a href="/locations/toronto" style="color:#1976D2;font-weight:600;text-decoration:underline;">View all Toronto coverage &rarr;</a> &nbsp;|&nbsp;
                <a href="/locations" style="color:#1976D2;font-weight:600;text-decoration:underline;">All Service Areas &rarr;</a>
            </div>
        </div>
    </section>

    <!-- Unified Footer -->
    <div id="footer-placeholder"></div>
    <script src="/includes/footer-loader.js"></script>
</body>
</html>
`;
}

// === GENERATE LOCATIONS INDEX ===
function generateLocationsIndex() {
    const cityLinks = CITIES.map(c => {
        const fullName = c === 'st-lawrence' ? 'St. Lawrence' : titleCase(c);
        return `<li><a href="/locations/${c}">${fullName}</a></li>`;
    }).join('\n                    ');

    const neighborhoodLinks = Object.entries(NEIGHBORHOODS).map(([slug, data]) =>
        `<li><a href="/locations/${slug}">${data.name}</a></li>`
    ).join('\n                    ');

    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Full directory of Toronto and Greater Toronto Area service areas covered by Nika Appliance Repair — 22 cities and 21 Toronto neighborhoods. Same-day repair (437) 524-1053.">
    <title>All Toronto Service Areas | Nika Appliance Repair</title>
    <link rel="canonical" href="https://nikaappliancerepair.com/locations">

    <meta property="og:type" content="website">
    <meta property="og:title" content="All Toronto Service Areas | Nika Appliance Repair">
    <meta property="og:description" content="Full directory of Toronto and GTA service areas covered by Nika Appliance Repair — 22 cities and 21 Toronto neighborhoods.">
    <meta property="og:url" content="https://nikaappliancerepair.com/locations">
    <meta property="og:image" content="https://nikaappliancerepair.com/assets/images/friendly-technician-character-min.webp">

    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "Nika Appliance Repair",
        "image": "https://nikaappliancerepair.com/assets/images/friendly-technician-character-min.webp",
        "url": "https://nikaappliancerepair.com/locations",
        "telephone": "+14375241053",
        "email": "nicksappliancerepair@on.fixlify.app",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "755 Steeles Ave W #311",
            "addressLocality": "North York",
            "addressRegion": "ON",
            "postalCode": "M2R 3W9",
            "addressCountry": "CA"
        },
        "priceRange": "$$",
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.7",
            "reviewCount": "176",
            "bestRating": "5",
            "worstRating": "1"
        },
        "openingHoursSpecification": [
            { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "08:00", "closes": "20:00" },
            { "@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "09:00", "closes": "18:00" },
            { "@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "10:00", "closes": "17:00" }
        ],
        "areaServed": [
            ${[...CITIES, ...Object.keys(NEIGHBORHOODS)].map(s => {
                const name = NEIGHBORHOODS[s] ? NEIGHBORHOODS[s].name : (s === 'st-lawrence' ? 'St. Lawrence' : titleCase(s));
                return `{ "@type": "Place", "name": "${name}" }`;
            }).join(',\n            ')}
        ]
    }
    </script>

    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://nikaappliancerepair.com/" },
            { "@type": "ListItem", "position": 2, "name": "Service Areas", "item": "https://nikaappliancerepair.com/locations" }
        ]
    }
    </script>

    <link rel="preload" as="image" href="../assets/images/friendly-technician-character-min.webp" fetchpriority="high">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;500;600;700;800&family=Rubik:wght@300;400;500;600;700&display=swap" rel="stylesheet">

    <link rel="stylesheet" href="../css/tokens.css">
    <link rel="stylesheet" href="../css/design-system.css">
    <link rel="stylesheet" href="../css/style.css">
    <link rel="stylesheet" href="../css/header-v2-styles.css">
    <link rel="stylesheet" href="../css/header-optimized.css">
    <link rel="stylesheet" href="../css/footer-optimized.css">
    <link rel="stylesheet" href="../css/responsive-comprehensive.css">
    <link rel="stylesheet" href="../css/combined-fixes.css">
    <link rel="stylesheet" href="../css/cta-buttons.css">
    <link rel="stylesheet" href="../css/design-fixes-2026.css">

    <style>
        .locations-index .area-section { background:white; padding:2.5rem 1rem; }
        .locations-index .area-section.alt { background:#f8f9fa; }
        .locations-index ul.area-grid {
            list-style:none;padding:0;margin:0;
            display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:0.75rem;
        }
        .locations-index ul.area-grid li {
            background:white;border:1px solid #e9ecef;border-radius:8px;
        }
        .locations-index .area-section.alt ul.area-grid li { background:white; }
        .locations-index ul.area-grid a {
            display:block;padding:0.85rem 1rem;color:#1976D2;text-decoration:none;font-weight:500;
        }
        .locations-index ul.area-grid a:hover { background:#e3f2fd;border-radius:8px; }
        .locations-index h1 { font-family:'Fredoka',cursive;color:#0d47a1;font-size:2.2rem;margin-bottom:1rem; }
        .locations-index h2 { font-family:'Fredoka',cursive;color:#0d47a1;font-size:1.6rem;margin:0 0 1.5rem; }
    </style>
</head>
<body class="locations-index">
    <!-- Unified Header -->
    <div id="header-placeholder"></div>
    <script src="/includes/header-loader.js" defer></script>

    <!-- Hero -->
    <section style="padding:3rem 1rem;background:linear-gradient(135deg,#e3f2fd 0%,#fff 100%);" id="main-content">
        <div style="max-width:1100px;margin:0 auto;">
            <nav aria-label="Breadcrumb" style="font-size:0.9rem;color:#6c757d;margin-bottom:1rem;">
                <a href="/" style="color:#1976D2;text-decoration:none;">Home</a> &rsaquo;
                <span>Service Areas</span>
            </nav>
            <h1>Service Areas Across Greater Toronto and Beyond</h1>
            <p style="font-size:1.15rem;line-height:1.6;color:#212529;max-width:900px;">Nika Appliance Repair has been serving the Greater Toronto Area since 2017 from our base at 755 Steeles Avenue West in North York. Our service map covers 22 cities across the GTA and 21 Toronto neighborhoods, with same-day appointments available seven days a week. Call <a href="tel:4375241053" style="color:#1976D2;font-weight:600;">(437) 524-1053</a> to book or browse the directory below to find local pricing, common appliance issues, and brand-specific service notes for your area.</p>
            <p style="line-height:1.7;color:#212529;margin-top:1rem;max-width:900px;">Every service area page covers the same six appliance categories — refrigerators, washers, dryers, dishwashers, ovens, and stoves — but the local context shifts with the territory. Toronto neighborhoods deal with compact 24-inch European-spec appliances in condos, hard Lake Ontario water that scales heaters and inlet valves, and tight kitchen geometry in Victorian and Edwardian housing stock. GTA suburbs tend to have full-size 30-inch and 36-inch residential pairs, larger laundry rooms, well-water hardness in the outer ring, and more straightforward truck access. Picking the right neighborhood page below gives you the pricing range, brand availability, and access notes that match your home before you call.</p>
            <p style="line-height:1.7;color:#212529;margin-top:1rem;max-width:900px;">If you do not see your area listed, call us anyway — we cover the full GTA, including all 416 and 905 area codes, and we serve adjacent regions like Halton, Peel, York, and Durham daily. Our truck stock and parts inventory is built around the brands we see most often across these communities: Samsung, LG, Whirlpool, Bosch, Frigidaire, Kenmore, GE, KitchenAid, Maytag, Electrolux, Miele, Liebherr, Blomberg, and Fisher &amp; Paykel. We also handle several Asian-market and European import brands that show up regularly in Toronto Chinatown and condo districts. Every repair carries our 90-day parts and labour warranty, and the $89 diagnostic is waived whenever you go ahead with the recommended fix.</p>
            <div style="margin-top:1.5rem;">
                <a href="tel:4375241053" style="display:inline-block;background:#1976D2;color:white;padding:0.9rem 1.6rem;border-radius:8px;text-decoration:none;font-weight:600;margin-right:0.5rem;">Call (437) 524-1053</a>
                <a href="/#book" style="display:inline-block;background:white;color:#1976D2;padding:0.9rem 1.6rem;border-radius:8px;text-decoration:none;font-weight:600;border:2px solid #1976D2;">Book Online</a>
            </div>
        </div>
    </section>

    <!-- Cities -->
    <section class="area-section alt">
        <div style="max-width:1100px;margin:0 auto;">
            <h2>Cities We Serve (Greater Toronto Area)</h2>
            <p style="color:#6c757d;margin-bottom:1.5rem;">Each city has its own dedicated hub page with local pricing, brand list, and same-day availability.</p>
            <ul class="area-grid">
                    ${cityLinks}
            </ul>
        </div>
    </section>

    <!-- Toronto neighborhoods -->
    <section class="area-section">
        <div style="max-width:1100px;margin:0 auto;">
            <h2>Toronto Neighborhoods</h2>
            <p style="color:#6c757d;margin-bottom:1.5rem;">Detailed service notes for downtown, midtown, east, and west Toronto neighborhoods, including condo-specific 24-inch appliance support.</p>
            <ul class="area-grid">
                    ${neighborhoodLinks}
            </ul>
        </div>
    </section>

    <!-- About coverage -->
    <section class="area-section alt">
        <div style="max-width:900px;margin:0 auto;">
            <h2>How Our Service Coverage Works</h2>
            <p style="line-height:1.7;color:#212529;margin-bottom:1rem;">Our base of operations at 755 Steeles Avenue West sits at the intersection of Toronto, North York, Vaughan, and Markham, which means our trucks are typically within 25 to 40 minutes of any address in the GTA core. We schedule routes daily to balance same-day availability with realistic arrival windows — most customers get a confirmed two-hour window within the first phone call.</p>
            <p style="line-height:1.7;color:#212529;margin-bottom:1rem;">For Toronto neighborhoods, we run dedicated downtown routes that batch King West, St. Lawrence, Trinity-Bellwoods, Little Italy, Ossington, and the surrounding neighborhoods together. East-end routes group Greektown, Riverside, the Beaches, and East York. West-end routes cover Bloor West Village, Roncesvalles, Parkdale, High Park, and Swansea. Midtown and Wychwood share a route with Forest Hill and Mount Pleasant. This routing keeps our same-day capacity high even when the Eglinton Crosstown or Lakeshore construction creates traffic surprises.</p>
            <p style="line-height:1.7;color:#212529;margin-bottom:1rem;">For GTA cities, we run fixed daily routes covering York Region (Richmond Hill, Markham, Vaughan, Newmarket, Aurora, Stouffville, East Gwillimbury), Peel (Mississauga, Brampton, Caledon), Halton (Oakville, Burlington, Milton, Halton Hills), and Durham (Ajax, Pickering, Whitby, Oshawa). We hold same-day capacity on every route, with afternoon slots typically filling up by 11 a.m. — calling first thing in the morning gives you the widest window selection.</p>
            <p style="line-height:1.7;color:#212529;">Pricing is consistent across all service areas: $89 diagnostic (waived with repair), $200–$450 typical full repair range, 90-day parts and labour warranty, and OEM parts wherever the manufacturer still produces them. Brand coverage includes Samsung, LG, Whirlpool, Bosch, Frigidaire, Kenmore, GE, KitchenAid, Maytag, Electrolux, Miele, Liebherr, Blomberg, Fisher &amp; Paykel, Haier, and most other current and recent residential makes. For a confirmed quote on your specific situation, call <a href="tel:4375241053" style="color:#1976D2;font-weight:600;">(437) 524-1053</a> — we can give a typical price range over the phone before any technician is dispatched.</p>
        </div>
    </section>

    <!-- Unified Footer -->
    <div id="footer-placeholder"></div>
    <script src="/includes/footer-loader.js"></script>
</body>
</html>
`;
}

// === GENERATE TORONTO.HTML APPENDED SECTION ===
function generateTorontoNeighborhoodSection() {
    let serviceBlocks = SERVICES.map(s => {
        const links = Object.entries(NEIGHBORHOODS).filter(([slug]) => {
            const f = path.join(SERVICES_DIR, `${s.slug}-${slug}.html`);
            return fs.existsSync(f);
        }).map(([slug, data]) =>
            `                    <a href="/locations/services/${s.slug}-${slug}" style="display:inline-block;padding:0.4rem 0.85rem;background:white;border:1px solid #e9ecef;border-radius:18px;color:#1976D2;text-decoration:none;font-size:0.9rem;margin:0.2rem 0.15rem;">${data.name}</a>`
        ).join('\n');

        return `            <div style="margin-bottom:2rem;">
                <h3 style="font-family:'Fredoka',cursive;color:#0d47a1;font-size:1.3rem;margin-bottom:0.75rem;display:flex;align-items:center;gap:0.5rem;">
                    <span style="font-size:1.5rem;">${s.icon}</span> ${s.label} by Toronto Neighborhood
                </h3>
                <div>
${links}
                </div>
            </div>`;
    }).join('\n');

    let hubLinks = Object.entries(NEIGHBORHOODS).map(([slug, data]) =>
        `                <a href="/locations/${slug}" style="display:inline-block;padding:0.6rem 1rem;background:#1976D2;color:white;border-radius:8px;text-decoration:none;font-weight:500;font-size:0.95rem;margin:0.25rem 0.2rem;">${data.name} Hub</a>`
    ).join('\n');

    return `
    <!-- TORONTO NEIGHBORHOOD HUBS - INTERNAL LINK BUILDING -->
    <section style="background:#f8f9fa;padding:3rem 1rem;">
        <div style="max-width:1100px;margin:0 auto;">
            <h2 style="text-align:center;font-family:'Fredoka',cursive;color:#0d47a1;font-size:2rem;margin-bottom:0.5rem;">Service Coverage by Toronto Neighborhood</h2>
            <p style="text-align:center;color:#6c757d;margin-bottom:2rem;">Browse our 21 dedicated Toronto neighborhood hubs — each with local pricing, common appliance issues, and same-day availability.</p>
            <div style="text-align:center;margin-bottom:2.5rem;">
${hubLinks}
            </div>
            <h3 style="text-align:center;font-family:'Fredoka',cursive;color:#0d47a1;font-size:1.5rem;margin:2rem 0 1.5rem;">Or Browse by Appliance Type</h3>
${serviceBlocks}
            <p style="text-align:center;margin-top:2rem;">
                <a href="/locations" style="color:#1976D2;font-weight:600;text-decoration:underline;">View All Service Areas (Cities + Neighborhoods) &rarr;</a>
            </p>
        </div>
    </section>
`;
}

// === MAIN ===
function main() {
    let created = [];
    let skipped = [];

    // 1. Generate neighborhood hub pages
    Object.entries(NEIGHBORHOODS).forEach(([slug, data]) => {
        const out = path.join(LOCATIONS_DIR, `${slug}.html`);
        if (fs.existsSync(out)) {
            skipped.push(`${slug}.html (already exists)`);
            return;
        }
        const html = generateNeighborhoodHub(slug, data);
        fs.writeFileSync(out, html, 'utf8');
        created.push(`locations/${slug}.html`);
    });

    // 2. Generate locations/index.html
    const indexPath = path.join(LOCATIONS_DIR, 'index.html');
    if (!fs.existsSync(indexPath)) {
        fs.writeFileSync(indexPath, generateLocationsIndex(), 'utf8');
        created.push('locations/index.html');
    } else {
        // Overwrite — this index is what we're explicitly building
        fs.writeFileSync(indexPath, generateLocationsIndex(), 'utf8');
        created.push('locations/index.html (rewritten)');
    }

    // 3. Append section to toronto.html (only if not already added)
    const torontoPath = path.join(LOCATIONS_DIR, 'toronto.html');
    let torontoHtml = fs.readFileSync(torontoPath, 'utf8');
    const marker = '<!-- TORONTO NEIGHBORHOOD HUBS - INTERNAL LINK BUILDING -->';
    if (torontoHtml.includes(marker)) {
        skipped.push('toronto.html (section already present)');
    } else {
        const section = generateTorontoNeighborhoodSection();
        // Insert before </body>
        const insertBefore = '    <!-- Unified Footer -->';
        torontoHtml = torontoHtml.replace(insertBefore, section + '\n' + insertBefore);
        fs.writeFileSync(torontoPath, torontoHtml, 'utf8');
        created.push('locations/toronto.html (appended neighborhood section)');
    }

    console.log('\n=== BUILD COMPLETE ===');
    console.log('\nCREATED:');
    created.forEach(f => console.log('  +', f));
    if (skipped.length) {
        console.log('\nSKIPPED:');
        skipped.forEach(f => console.log('  -', f));
    }

    // Stats
    const cityCount = CITIES.length;
    const hubCount = Object.keys(NEIGHBORHOODS).length;
    console.log(`\n/locations/index.html links to ${cityCount} cities + ${hubCount} neighborhoods = ${cityCount + hubCount} hubs`);

    let totalServiceLinks = 0;
    SERVICES.forEach(s => {
        const c = Object.keys(NEIGHBORHOODS).filter(slug =>
            fs.existsSync(path.join(SERVICES_DIR, `${s.slug}-${slug}.html`))
        ).length;
        totalServiceLinks += c;
        console.log(`  ${s.label}: ${c} neighborhood links`);
    });
    console.log(`Total service-page links added to toronto.html: ${totalServiceLinks}`);
}

main();
