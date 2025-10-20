#!/usr/bin/env python3
"""
Create unique brand-specific content for all brand pages
This fixes the duplicate content SEO issue
"""

import os
import re

# Brand-specific data with unique problems, FAQs, and information
BRAND_DATA = {
    'lg': {
        'name': 'LG',
        'subtitle': 'LG appliances are known for advanced smart features and inverter technology. Our certified technicians specialize in LG refrigerators, washers, dryers, and dishwashers across Toronto and the GTA. We stock genuine LG parts and handle everything from LinearCooling issues to ThinQ connectivity problems.',
        'problems': [
            {
                'icon': '❄️',
                'title': 'LG Linear Compressor Failure',
                'description': 'LG refrigerators with Linear Compressors can fail prematurely. We diagnose compressor issues, check the 10-year warranty status, and provide expert repairs or replacements for models like LFXS, LMXS, and LRFVS series.'
            },
            {
                'icon': '🌊',
                'title': 'LG Front Load Washer OE Error',
                'description': 'The dreaded OE error code indicates drainage problems in LG front-load washers. We clean out clogged drain pumps, fix faulty pressure switches, and resolve drain hose issues in WM series models.'
            },
            {
                'icon': '🔧',
                'title': 'LG Dishwasher LE Error Code',
                'description': 'LE error means motor issue or leak detection. Common in LG QuadWash models. We fix seized motors, clear blockages causing false leak detection, and replace faulty hall sensors.'
            },
            {
                'icon': '🧊',
                'title': 'LG Ice Maker Freezing Up',
                'description': 'LG InstaView and SmartThinQ refrigerators often have ice makers that freeze solid. We fix the drain tube, replace the ice maker assembly, and prevent recurring freeze-ups.'
            },
            {
                'icon': '🔥',
                'title': 'LG Dryer D80/D90/D95 Error',
                'description': 'Flow sense errors indicate blocked venting. We inspect the entire vent system, clean out lint buildup, and ensure your LG SteamDryer operates safely and efficiently.'
            },
            {
                'icon': '📱',
                'title': 'LG ThinQ Connectivity Issues',
                'description': 'Smart features not working? We troubleshoot Wi-Fi connections, reset ThinQ modules, update firmware, and restore smart functionality on LG SmartThinQ appliances.'
            }
        ],
        'faqs': [
            {
                'question': 'Are LG refrigerator compressors covered under warranty?',
                'answer': 'Yes! LG offers a 10-year warranty on Linear Compressors in refrigerators manufactured after 2015. We can help you file warranty claims and perform covered repairs. Even if your warranty has expired, we can replace the compressor at competitive prices.'
            },
            {
                'question': 'Why does my LG washer say OE all the time?',
                'answer': 'The OE error code means the washer isn\'t draining properly. Common causes include a clogged drain pump filter, kinked drain hose, or faulty drain pump. We can diagnose and fix this issue in one visit. Regular cleaning of the drain pump filter every 3 months helps prevent this error.'
            },
            {
                'question': 'Can you fix LG ThinQ smart features?',
                'answer': 'Absolutely! We troubleshoot and repair all LG ThinQ connectivity issues including Wi-Fi connection problems, app pairing failures, and firmware update errors. Most smart feature issues can be resolved through module replacement or software updates.'
            },
            {
                'question': 'How much do LG appliance parts cost?',
                'answer': 'LG parts are moderately priced. Common parts like door seals run $80-120, drain pumps $100-150, and compressors $400-600. We use genuine LG parts when available and high-quality equivalents that meet or exceed OEM specifications.'
            },
            {
                'question': 'Is LG a reliable appliance brand?',
                'answer': 'LG is generally reliable, especially newer models with inverter technology. However, some models have had issues with Linear Compressors (covered by 10-year warranty) and front-load washer bearings. With proper maintenance, LG appliances typically last 10-15 years.'
            }
        ]
    },
    'samsung': {
        'name': 'Samsung',
        'subtitle': 'Samsung leads in smart appliance innovation with Family Hub refrigerators, FlexWash washers, and Wi-Fi connected appliances. Our technicians are Samsung-certified and experienced with SmartThings integration, ice maker repairs, and the unique challenges of Samsung\'s advanced technology across Toronto and the GTA.',
        'problems': [
            {
                'icon': '🧊',
                'title': 'Samsung Ice Maker Failure',
                'description': 'Samsung refrigerators are notorious for ice maker problems. The ice maker freezes up, stops making ice, or leaks water. We fix the defrost issue, replace faulty ice makers, and install upgraded parts to prevent recurrence on RF, RH, and Family Hub models.'
            },
            {
                'icon': '⚠️',
                'title': 'Samsung Refrigerator Error Codes',
                'description': 'Codes like 22E, 39C, or OF OF indicate specific issues. We diagnose error codes, fix faulty sensors, repair control boards, and resolve cooling problems in Samsung French door and side-by-side refrigerators.'
            },
            {
                'icon': '🌊',
                'title': 'Samsung Washer 4C/4E Error',
                'description': 'Water supply error common in Samsung front-loaders. We check water inlet valves, clean clogged filters, fix pressure switches, and ensure proper water flow to your WF series washer.'
            },
            {
                'icon': '📱',
                'title': 'Samsung SmartThings Not Working',
                'description': 'Smart features disconnected? We troubleshoot Wi-Fi modules, reset SmartThings connections, update firmware, and restore app control on Samsung smart appliances including Family Hub refrigerators.'
            },
            {
                'icon': '🔥',
                'title': 'Samsung Dryer Heating Issues',
                'description': 'Samsung dryers stop heating due to thermal fuse failure, bad heating elements, or gas valve issues. We diagnose the problem quickly and restore full drying performance on DV series models.'
            },
            {
                'icon': '💧',
                'title': 'Samsung Dishwasher LC/LE Error',
                'description': 'Leak error codes that often appear even without leaks. We identify false triggers, fix actual leaks, replace sensors, and ensure your WaterWall or StormWash dishwasher operates without error codes.'
            }
        ],
        'faqs': [
            {
                'question': 'Why do Samsung ice makers always break?',
                'answer': 'Samsung ice makers have a design flaw where the defrost drain freezes, causing ice buildup. This affects many RF and RH series refrigerators. We fix this by replacing the ice maker with an improved version and modifying the defrost drain to prevent freezing. The repair typically lasts 3-5 years before needing attention again.'
            },
            {
                'question': 'What does 22E error mean on Samsung fridge?',
                'answer': 'The 22E error indicates a fan problem - usually the evaporator fan motor has failed or is obstructed by ice. We defrost the system, replace the faulty fan motor if needed, and check for underlying cooling system issues. This is a common problem in Samsung refrigerators.'
            },
            {
                'question': 'Are Samsung appliances expensive to repair?',
                'answer': 'Samsung parts can be pricier than average. Control boards run $200-400, ice makers $150-250, and specialty parts for Family Hub features can exceed $500. However, many repairs are straightforward and cost-effective. We provide upfront quotes before proceeding.'
            },
            {
                'question': 'Can you fix Samsung Family Hub screens?',
                'answer': 'Yes! We repair and replace Family Hub touchscreens, fix connectivity issues, resolve app problems, and troubleshoot camera failures. Family Hub repairs typically run $300-800 depending on the issue. We can also help with software updates and SmartThings integration.'
            },
            {
                'question': 'Is Samsung or LG better for appliances?',
                'answer': 'Both are quality brands with pros and cons. Samsung excels in innovation and smart features but has more complex repairs. LG offers better compressor warranties and slightly better reliability. We service both extensively and can provide honest comparisons based on specific models.'
            }
        ]
    },
    'whirlpool': {
        'name': 'Whirlpool',
        'subtitle': 'Whirlpool is America\'s most trusted appliance brand, known for reliability and straightforward repairs. Our technicians have decades of combined experience servicing Whirlpool refrigerators, washers, dryers, and dishwashers. We stock common Whirlpool parts for fast, same-day repairs across Toronto and the GTA.',
        'problems': [
            {
                'icon': '🌊',
                'title': 'Whirlpool Washer Won\'t Drain',
                'description': 'Drain pump failure is common in Whirlpool top-loaders and Cabrio models. We replace clogged pumps, fix drain hoses, and resolve lid switch issues that prevent draining. Most repairs completed same-day.'
            },
            {
                'icon': '🔧',
                'title': 'Whirlpool Cabrio/Duet Bearing Noise',
                'description': 'Loud grinding during spin cycle indicates worn bearings. Common in Cabrio and Duet front-loaders after 8-10 years. We assess repair vs replacement costs and provide honest recommendations.'
            },
            {
                'icon': '❄️',
                'title': 'Whirlpool Refrigerator Not Cold',
                'description': 'Failed start relay, bad compressor, or defrost issues. We diagnose cooling problems in side-by-side and French door models, replace faulty components, and restore proper temperatures quickly.'
            },
            {
                'icon': '💧',
                'title': 'Whirlpool Dishwasher Not Cleaning',
                'description': 'Spray arm clogs, worn wash motor, or detergent dispenser issues. We service Gold, Quiet Partner, and modern Whirlpool dishwashers to restore sparkling clean dishes.'
            },
            {
                'icon': '🔥',
                'title': 'Whirlpool Dryer Takes Too Long',
                'description': 'Clogged venting, faulty moisture sensor, or heating element issues. We optimize drying time on Cabrio, Duet, and traditional Whirlpool dryers for energy-efficient operation.'
            },
            {
                'icon': '🧊',
                'title': 'Whirlpool Ice Maker Problems',
                'description': 'Ice maker not working, slow ice production, or jammed ice. We fix water inlet valves, replace ice maker assemblies, and resolve all ice-related issues in Whirlpool refrigerators.'
            }
        ],
        'faqs': [
            {
                'question': 'Are Whirlpool appliances easy to repair?',
                'answer': 'Yes! Whirlpool appliances are among the easiest and most cost-effective to repair. Parts are readily available, reasonably priced, and repair procedures are straightforward. This is one reason Whirlpool remains so popular - they\'re built to be serviced.'
            },
            {
                'question': 'How long do Whirlpool appliances last?',
                'answer': 'Whirlpool appliances typically last 13-18 years with proper maintenance. Washers and dryers often exceed 15 years, while dishwashers average 12-14 years. Refrigerators can last 15-20 years. This longevity makes them excellent value for money.'
            },
            {
                'question': 'What is the most common Whirlpool washer problem?',
                'answer': 'The drain pump failing is the #1 issue we see in Whirlpool washers. Symptoms include water not draining, error codes, or the washer stopping mid-cycle. The repair is straightforward and costs $150-250 including parts and labor.'
            },
            {
                'question': 'Is Whirlpool owned by another company?',
                'answer': 'Whirlpool Corporation is an independent company and the world\'s largest appliance manufacturer. They also own Maytag, KitchenAid, Amana, and Jenn-Air brands. This means many parts are interchangeable, which helps keep repair costs down.'
            },
            {
                'question': 'Are Whirlpool parts expensive?',
                'answer': 'Whirlpool parts are very affordable compared to premium brands. Most common parts range from $50-200. Parts availability is excellent, and we typically have common Whirlpool components on our trucks for same-day repairs.'
            }
        ]
    },
    'ge': {
        'name': 'GE',
        'subtitle': 'GE Appliances combines American engineering with modern innovation. From classic GE Profile to advanced GE Café and smart GE Appliances with WiFi, our technicians service all GE product lines. We handle everything from Monogram luxury appliances to budget-friendly GE models across Toronto and the GTA.',
        'problems': [
            {
                'icon': '❄️',
                'title': 'GE Refrigerator Not Cooling',
                'description': 'GE Profile and Café models can have compressor, sealed system, or control board issues. We diagnose cooling problems, check warranty coverage, and provide expert repairs on side-by-side, French door, and top-freezer GE refrigerators.'
            },
            {
                'icon': '🌊',
                'title': 'GE Washer Won\'t Spin',
                'description': 'Failed motor coupling, worn clutch, or lid switch problems common in GE top-loaders. We fix spin issues in GTW, GE Profile, and older GE washer models with quick, reliable repairs.'
            },
            {
                'icon': '🔧',
                'title': 'GE Dishwasher Not Draining',
                'description': 'Drain pump failure or clogged drain common in GE and GE Profile dishwashers. We clear blockages, replace drain pumps, and fix check valves to restore proper drainage.'
            },
            {
                'icon': '🧊',
                'title': 'GE Ice Maker Stopped Working',
                'description': 'GE ice makers fail due to water inlet valve issues, frozen fill tubes, or faulty ice maker modules. We diagnose and fix all GE ice maker problems, including Opal nugget ice makers.'
            },
            {
                'icon': '🔥',
                'title': 'GE Oven Won\'t Heat Properly',
                'description': 'Igniter failure in gas ovens or bake element failure in electric models. Common in GE Profile and Café ranges. We restore accurate temperatures and proper heating on all GE cooking appliances.'
            },
            {
                'icon': '📱',
                'title': 'GE WiFi Connect Issues',
                'description': 'GE Profile and Café appliances with WiFi having connection problems. We troubleshoot the GE Appliances Kitchen app, reset WiFi modules, and restore smart functionality.'
            }
        ],
        'faqs': [
            {
                'question': 'Is GE a good appliance brand?',
                'answer': 'GE Appliances offers solid reliability, especially the Profile and Café lines. While no longer owned by General Electric (now Haier), they maintain good build quality. GE appliances are mid-range priced with reasonable repair costs and good parts availability.'
            },
            {
                'question': 'What\'s the difference between GE, GE Profile, and GE Café?',
                'answer': 'GE is the base line (budget-friendly), GE Profile is mid-tier with more features and better performance, and GE Café is premium with professional styling and advanced features. Café appliances have unique design elements and the highest build quality. We service all three lines.'
            },
            {
                'question': 'Are GE appliances made in USA?',
                'answer': 'Many GE appliances are still manufactured in the USA (Louisville, KY and other facilities), though GE Appliances is now owned by Chinese company Haier. The manufacturing and design remain largely American, which means good parts availability and service support.'
            },
            {
                'question': 'How much does it cost to fix a GE refrigerator?',
                'answer': 'GE refrigerator repairs typically run $150-450. Simple fixes like thermostats or door seals cost $150-250. More complex repairs like compressors or sealed system work run $400-700. We provide exact quotes after diagnosis.'
            },
            {
                'question': 'Do GE appliances have good warranties?',
                'answer': 'GE offers standard 1-year limited warranties on most appliances. Some components like compressors have extended warranties (up to 5 years on select models). GE Café sometimes includes 2-year warranties. We can help you navigate warranty claims for covered repairs.'
            }
        ]
    },
    'maytag': {
        'name': 'Maytag',
        'subtitle': 'Maytag built its reputation on durability with the iconic "Maytag Man" who had nothing to do. While owned by Whirlpool since 2006, Maytag still focuses on heavy-duty construction and reliability. Our technicians specialize in Maytag washers, dryers, and refrigerators throughout Toronto and the GTA.',
        'problems': [
            {
                'icon': '🌊',
                'title': 'Maytag Washer Transmission Issues',
                'description': 'Maytag Bravos and older top-loaders can have transmission failures causing agitation problems. We diagnose gearcase issues, assess repair vs replacement economics, and provide honest recommendations.'
            },
            {
                'icon': '🔧',
                'title': 'Maytag Centennial Lid Lock',
                'description': 'Lid lock failures prevent washing. Common in Centennial and Bravos models. We replace faulty lid lock assemblies and get your Maytag washer back to working order quickly.'
            },
            {
                'icon': '🔥',
                'title': 'Maytag Dryer Not Heating',
                'description': 'Thermal fuse blows or heating element fails in Maytag Bravos and Centennial dryers. We fix heating issues, clean ventilation, and prevent future thermal fuse failures.'
            },
            {
                'icon': '❄️',
                'title': 'Maytag Refrigerator Ice Buildup',
                'description': 'Defrost system failures cause ice buildup in Maytag French door and side-by-side refrigerators. We replace defrost heaters, timers, and thermostats to restore proper defrost cycles.'
            },
            {
                'icon': '💧',
                'title': 'Maytag Dishwasher Won\'t Fill',
                'description': 'Water inlet valve or float switch problems prevent filling. We diagnose and fix water supply issues in Maytag Jetclean and quiet series dishwashers.'
            },
            {
                'icon': '⚙️',
                'title': 'Maytag Neptune Bearing Failure',
                'description': 'Older Maytag Neptune front-loaders notorious for bearing failures. We assess whether bearing replacement or new washer makes more financial sense.'
            }
        ],
        'faqs': [
            {
                'question': 'Are Maytag appliances still reliable?',
                'answer': 'Modern Maytag appliances (post-2006 Whirlpool acquisition) are quite reliable, though perhaps not as legendary as the old "Lonely Maytag Repairman" days. They\'re built tougher than budget brands with commercial-grade components. Expect 12-18 years of service with proper maintenance.'
            },
            {
                'question': 'Is Maytag better than Whirlpool?',
                'answer': 'Maytag and Whirlpool are now the same company (Whirlpool owns Maytag). Maytag positions itself as the more durable, heavy-duty option while Whirlpool is mainstream. In practice, they share many parts and similar reliability. Maytag often has beefier components and slightly higher price.'
            },
            {
                'question': 'Why did my Maytag washer stop working?',
                'answer': 'Common causes: lid lock failure (Bravos/Centennial models), drain pump clog, motor coupling failure, or transmission issues in older units. We can diagnose the exact problem in 15-20 minutes and usually fix it same-day with parts on our truck.'
            },
            {
                'question': 'How much does Maytag washer repair cost?',
                'answer': 'Typical Maytag washer repairs run $150-350. Lid lock replacement costs about $150-200, drain pumps $180-250, and motor couplings $150-200. More complex transmission repairs can reach $400-500, at which point we discuss replacement options.'
            },
            {
                'question': 'Are Maytag parts expensive?',
                'answer': 'Maytag parts are moderately priced, similar to Whirlpool. Many parts are actually interchangeable between the brands. Common components range from $50-200, and availability is excellent. We stock frequently needed Maytag parts for same-day repairs.'
            }
        ]
    }
}

# Continue with remaining brands...
BRAND_DATA.update({
    'kitchenaid': {
        'name': 'KitchenAid',
        'subtitle': 'KitchenAid represents premium quality and professional-grade performance, from iconic stand mixers to high-end appliances. Our technicians are experienced with KitchenAid\'s unique features including ProScrub dishwashers, Commercial-Style ranges, and Built-in refrigeration across Toronto and the GTA.',
        'problems': [
            {
                'icon': '💧',
                'title': 'KitchenAid Dishwasher Not Cleaning',
                'description': 'ProWash, ProScrub, and PrintShield dishwashers with cleaning issues. We fix clogged spray arms, replace worn wash pumps, clean filter assemblies, and restore KitchenAid\'s signature cleaning performance.'
            },
            {
                'icon': '❄️',
                'title': 'KitchenAid Built-in Fridge Issues',
                'description': 'Premium built-in refrigerators with temperature control problems. We service KitchenAid French door and side-by-side models, fix sealed system issues, and handle complex refrigeration repairs.'
            },
            {
                'icon': '🔥',
                'title': 'KitchenAid Range Igniter Problems',
                'description': 'Commercial-Style and Dual Fuel ranges with ignition issues. We replace igniters, fix gas valve problems, and ensure safe, reliable ignition on all KitchenAid cooking appliances.'
            },
            {
                'icon': '🌊',
                'title': 'KitchenAid Washer Spin Issues',
                'description': 'Front-load washers not spinning properly. We fix suspension issues, replace bad bearings, and service KitchenAid washers to restore balanced, quiet operation.'
            },
            {
                'icon': '🔧',
                'title': 'KitchenAid Ice Maker Failures',
                'description': 'Undercounter ice makers and built-in fridge ice makers failing. We diagnose water supply issues, replace ice maker modules, and ensure consistent ice production.'
            },
            {
                'icon': '⚙️',
                'title': 'KitchenAid Control Board Issues',
                'description': 'Electronic control failures in high-end appliances. We diagnose control board problems, perform repairs when possible, and replace boards to restore full functionality.'
            }
        ],
        'faqs': [
            {
                'question': 'Is KitchenAid worth the extra money?',
                'answer': 'KitchenAid appliances offer premium build quality, professional-grade performance, and attractive design. They\'re worth it if you value aesthetics, quieter operation, and advanced features. Repair costs are higher than mainstream brands but longevity (15-20 years) offsets the investment.'
            },
            {
                'question': 'Who makes KitchenAid appliances?',
                'answer': 'KitchenAid is owned by Whirlpool Corporation but maintains separate design and engineering teams. KitchenAid appliances use higher-grade components, quieter motors, and premium materials compared to Whirlpool. The quality difference justifies the price premium.'
            },
            {
                'question': 'Are KitchenAid appliances expensive to fix?',
                'answer': 'Yes, KitchenAid repairs tend to cost 20-40% more than mainstream brands. Parts are pricier (control boards $300-600, specialized components $200-400), but repairs are less frequent. The premium construction means fewer service calls over the appliance\'s lifetime.'
            },
            {
                'question': 'How long do KitchenAid dishwashers last?',
                'answer': 'KitchenAid dishwashers typically last 12-16 years with proper maintenance. ProWash and ProScrub models are particularly durable. The stainless steel tubs, robust wash motors, and quality components contribute to this longevity - significantly better than budget brands.'
            },
            {
                'question': 'Can you get KitchenAid parts quickly?',
                'answer': 'KitchenAid parts are generally available but may require special order for certain components. Common parts (pumps, heating elements, seals) we stock. Specialized items (control boards, custom panels) may take 2-5 days. We inform you of any delays upfront.'
            }
        ]
    },
    'frigidaire': {
        'name': 'Frigidaire',
        'subtitle': 'Frigidaire invented the refrigerator and remains a popular choice for value-conscious buyers. From Gallery to Professional series, our technicians service all Frigidaire appliances. We\'re experienced with Frigidaire refrigerators, ranges, dishwashers, and laundry appliances throughout Toronto and the GTA.',
        'problems': [
            {
                'icon': '❄️',
                'title': 'Frigidaire Fridge Not Cooling',
                'description': 'Gallery and Professional refrigerators with cooling failures. We diagnose compressor issues, fix defrost problems, and repair sealed system leaks in Frigidaire French door and side-by-side models.'
            },
            {
                'icon': '🧊',
                'title': 'Frigidaire Ice Maker Leaking',
                'description': 'Water leaks around ice maker or into freezer. Common in Gallery refrigerators. We replace fill tubes, fix water inlet valves, and prevent ice maker water damage.'
            },
            {
                'icon': '🔥',
                'title': 'Frigidaire Range Burner Won\'t Light',
                'description': 'Gas range igniters clicking but not lighting. We replace worn igniters, clean burner ports, and ensure proper gas flow in Frigidaire and Gallery gas ranges.'
            },
            {
                'icon': '💧',
                'title': 'Frigidaire Dishwasher Won\'t Drain',
                'description': 'Standing water after cycle. We fix drain pumps, clear blockages, and replace check valves in Frigidaire Gallery and Professional dishwashers.'
            },
            {
                'icon': '🌊',
                'title': 'Frigidaire Front Load Washer Leaks',
                'description': 'Door seal leaks common in Frigidaire Affinity washers. We replace door boots, fix suspension issues causing leaks, and prevent water damage to your floor.'
            },
            {
                'icon': '⚠️',
                'title': 'Frigidaire Error Code Problems',
                'description': 'Cryptic error codes appearing on displays. We diagnose Frigidaire error codes, fix underlying issues, and clear error messages to restore normal operation.'
            }
        ],
        'faqs': [
            {
                'question': 'Is Frigidaire a good brand?',
                'answer': 'Frigidaire is a solid mid-range brand offering good value. Gallery models provide near-premium features at reasonable prices. While not as refined as luxury brands, Frigidaire appliances are reliable workhorses. Expect 10-14 years of service with typical maintenance.'
            },
            {
                'question': 'Who owns Frigidaire?',
                'answer': 'Frigidaire is owned by Electrolux, the Swedish appliance giant. This means Frigidaire and Electrolux share many components and technologies. The benefit: established parts supply chains and proven engineering. Frigidaire represents Electrolux\'s value-oriented line.'
            },
            {
                'question': 'Why is my Frigidaire refrigerator not cold enough?',
                'answer': 'Common causes include defrost system failure, bad evaporator fan, compressor issues, or sealed system leaks. Frigidaire Gallery models sometimes have control board problems affecting cooling. We diagnose the exact cause and provide repair options with upfront pricing.'
            },
            {
                'question': 'Are Frigidaire parts expensive?',
                'answer': 'Frigidaire parts are affordably priced. Most common components run $60-150, with control boards $150-300. Parts availability is excellent since Electrolux maintains robust supply chains. This makes Frigidaire economical to maintain over its lifetime.'
            },
            {
                'question': 'How long do Frigidaire appliances last?',
                'answer': 'Frigidaire appliances typically last 10-14 years. Refrigerators average 12-14 years, ranges 13-16 years, dishwashers 10-12 years, and washers 10-13 years. Gallery series tends toward the higher end of these ranges with better build quality.'
            }
        ]
    },
    'electrolux': {
        'name': 'Electrolux',
        'subtitle': 'Electrolux brings Scandinavian design and engineering excellence to the premium appliance market. Our technicians specialize in Electrolux luxury appliances including Perfect Steam washers, LuxCare dishwashers, and sophisticated refrigeration. We provide expert service for Electrolux appliances across Toronto and the GTA.',
        'problems': [
            {
                'icon': '🌊',
                'title': 'Electrolux Perfect Steam Washer Issues',
                'description': 'Front-load washers with steam features having problems. We fix steam generators, resolve drainage issues, and service the advanced wash systems in Electrolux EFLS and ELFW series washers.'
            },
            {
                'icon': '💧',
                'title': 'Electrolux LuxCare Dishwasher Problems',
                'description': 'Premium dishwashers not cleaning properly or having drainage issues. We service the sophisticated wash systems, replace circulation pumps, and restore LuxCare performance.'
            },
            {
                'icon': '❄️',
                'title': 'Electrolux Refrigerator Cooling Issues',
                'description': 'French door and counter-depth refrigerators with temperature problems. We diagnose sealed system issues, fix control problems, and handle complex refrigeration repairs on luxury Electrolux models.'
            },
            {
                'icon': '🔥',
                'title': 'Electrolux Induction Range Issues',
                'description': 'Induction cooktops with error codes or heating problems. We diagnose electronics, replace faulty induction coils, and service advanced cooking appliances with specialized expertise.'
            },
            {
                'icon': '⚙️',
                'title': 'Electrolux Control Board Failures',
                'description': 'Sophisticated electronics failing in premium appliances. We diagnose control system issues, source specialized parts, and restore full functionality to Electrolux appliances.'
            },
            {
                'icon': '🧊',
                'title': 'Electrolux Ice & Water Dispenser',
                'description': 'Dispenser not working or leaking. We fix water inlet valves, replace dispenser controls, and resolve ice maker problems in Electrolux refrigerators with integrated dispensers.'
            }
        ],
        'faqs': [
            {
                'question': 'Is Electrolux a luxury brand?',
                'answer': 'Yes, Electrolux positions itself in the premium/luxury segment with sophisticated features, European design, and higher-end materials. While not ultra-luxury like Miele, Electrolux offers excellent value in the premium category with features rivaling $2000+ appliances.'
            },
            {
                'question': 'Where are Electrolux appliances made?',
                'answer': 'Electrolux is a Swedish company that manufactures worldwide. Many Electrolux appliances sold in North America are made in USA facilities (alongside Frigidaire). The brand benefits from European engineering heritage combined with North American manufacturing.'
            },
            {
                'question': 'Are Electrolux appliances expensive to repair?',
                'answer': 'Electrolux repairs cost more than mainstream brands due to premium components. Control boards run $300-500, specialized parts $200-400, but repair frequency is lower than budget brands. Factor in the 12-18 year lifespan, and cost-per-year remains reasonable.'
            },
            {
                'question': 'Is Electrolux better than Frigidaire?',
                'answer': 'Yes - while both are owned by the same company, Electrolux is the premium tier. Electrolux features better build quality, quieter operation, more sophisticated features, and upscale aesthetics. Frigidaire represents value, while Electrolux represents refinement.'
            },
            {
                'question': 'Do Electrolux appliances have good warranties?',
                'answer': 'Electrolux offers standard 1-year comprehensive warranties, with extended coverage on certain components (2-5 years on select parts). Being a major manufacturer, they honor warranties reliably. We can coordinate warranty service for covered repairs.'
            }
        ]
    },
    'bosch': {
        'name': 'Bosch',
        'subtitle': 'Bosch represents German engineering excellence with ultra-quiet operation and precision performance. From legendary Bosch dishwashers to premium refrigeration and cooking appliances, our technicians are trained on Bosch\'s unique European technology. We provide expert Bosch appliance service throughout Toronto and the GTA.',
        'problems': [
            {
                'icon': '💧',
                'title': 'Bosch Dishwasher Not Draining',
                'description': 'Premium German dishwashers with drainage issues. We fix drain pumps, clear check valves, and resolve error codes in Bosch 300, 500, and 800 series dishwashers known for whisper-quiet operation.'
            },
            {
                'icon': '🚫',
                'title': 'Bosch Dishwasher E15 Error Code',
                'description': 'Leak detection error in base pan. Often false alarm but requires proper diagnosis. We drain the base, identify actual leaks if present, and reset the system to clear E15 errors.'
            },
            {
                'icon': '🔥',
                'title': 'Bosch Induction Cooktop Problems',
                'description': 'Induction elements not heating or showing error codes. We diagnose electronics, replace faulty power modules, and service the sophisticated controls in Bosch Benchmark and 800 series cooktops.'
            },
            {
                'icon': '❄️',
                'title': 'Bosch Refrigerator Temperature Issues',
                'description': 'European-style refrigerators with cooling problems. We service Bosch counter-depth and built-in refrigerators, fix evaporator fans, and handle complex temperature control repairs.'
            },
            {
                'icon': '🌊',
                'title': 'Bosch Washer Won\'t Spin',
                'description': 'Compact and full-size Bosch washers with spin cycle issues. We fix drain problems preventing spin, replace worn carbon brushes, and service the quiet motor systems.'
            },
            {
                'icon': '⚙️',
                'title': 'Bosch Control Module Failures',
                'description': 'Sophisticated German electronics requiring specialized diagnosis. We troubleshoot control boards, replace faulty modules, and restore full functionality to Bosch appliances.'
            }
        ],
        'faqs': [
            {
                'question': 'Are Bosch dishwashers really that quiet?',
                'answer': 'Yes! Bosch dishwashers are legitimately the quietest on the market, typically 44-46 dB (800 series as low as 42 dB). For comparison, that\'s quieter than rainfall. The German engineering with insulation and precision motors makes them nearly silent. This is their signature feature.'
            },
            {
                'question': 'Are Bosch appliances worth the money?',
                'answer': 'For dishwashers - absolutely yes. Bosch dishwashers are the gold standard for quiet operation and reliability. For other appliances (refrigerators, ranges), Bosch offers solid quality but faces stiff competition at similar price points. The brand excels most in dishwashers and cooking appliances.'
            },
            {
                'question': 'How long do Bosch appliances last?',
                'answer': 'Bosch dishwashers typically last 12-16 years - excellent longevity. Other Bosch appliances average 12-18 years. The German engineering emphasizes durability and precision. Maintenance requirements are low, but when repairs are needed, parts and service can be more expensive.'
            },
            {
                'question': 'Are Bosch parts expensive?',
                'answer': 'Yes, Bosch parts are premium-priced. Control modules run $300-600, circulation pumps $200-350, and specialized European components can be costly. However, Bosch appliances need repairs less frequently than budget brands, partially offsetting the higher parts costs.'
            },
            {
                'question': 'What does E15 error mean on Bosch dishwasher?',
                'answer': 'E15 indicates water in the base pan (leak protection activated). Often it\'s a false alarm from spills or humidity. We drain the base pan, check for actual leaks, and reset the system. If there\'s a genuine leak, we fix it - common causes are door seals or hose connections.'
            }
        ]
    },
    'miele': {
        'name': 'Miele',
        'subtitle': 'Miele represents the pinnacle of appliance engineering with the motto "Immer Besser" (Forever Better). These ultra-premium German appliances are built to last 20+ years. Our technicians receive specialized Miele training to service these sophisticated machines across Toronto and the GTA.',
        'problems': [
            {
                'icon': '💧',
                'title': 'Miele Dishwasher Drainage Issues',
                'description': 'Premium G-series dishwashers with drain problems. We service Miele\'s sophisticated drain systems, replace circulation pumps, and maintain the precision engineering that makes Miele dishwashers legendary.'
            },
            {
                'icon': '🌊',
                'title': 'Miele Washer Drain Pump Issues',
                'description': 'W1 series front-loaders with drainage concerns. We service the unique Miele drain systems, fix honeycomb drums, and maintain these ultra-reliable German washing machines.'
            },
            {
                'icon': '⚙️',
                'title': 'Miele Control Module Problems',
                'description': 'Sophisticated European electronics requiring expert diagnosis. We troubleshoot Miele\'s advanced controls, program repairs when possible, and replace modules with genuine Miele parts.'
            },
            {
                'icon': '🔥',
                'title': 'Miele Range Ignition Issues',
                'description': 'Dual-fuel and gas ranges with igniter problems. We service Miele\'s precision cooking appliances, replace igniters, and maintain the legendary Miele build quality.'
            },
            {
                'icon': '🧊',
                'title': 'Miele Refrigerator Repairs',
                'description': 'Built-in and freestanding refrigerators with cooling or ice maker issues. We provide specialized service for Miele refrigeration, handling complex repairs on these premium appliances.'
            },
            {
                'icon': '🔧',
                'title': 'Miele Door Lock Failures',
                'description': 'Dishwashers and washers with door lock malfunctions. We replace Miele\'s precision-engineered locks, reset electronics, and restore safe operation.'
            }
        ],
        'faqs': [
            {
                'question': 'Are Miele appliances worth the high price?',
                'answer': 'For committed quality seekers, yes. Miele appliances cost 2-3x mainstream brands but last 20+ years (they test for 20-year lifespan). Built with exceptional materials and engineering, they\'re quieter, more efficient, and require fewer repairs. Calculate cost-per-year over 20 years vs replacing cheaper appliances twice.'
            },
            {
                'question': 'How long do Miele appliances last?',
                'answer': 'Miele tests their appliances for 20-year lifespans. In practice, Miele washers, dryers, and dishwashers regularly exceed 20 years. We service Miele appliances from the 1990s still running strong. This longevity is unmatched in the industry and justifies the premium pricing.'
            },
            {
                'question': 'Are Miele repairs very expensive?',
                'answer': 'Yes - Miele parts and service are premium-priced. Control boards can exceed $500, specialized components $300-600. However, repair frequency is significantly lower than any other brand. Many Miele owners report no repairs for 10-15 years. When repairs are needed, we ensure they\'re done correctly.'
            },
            {
                'question': 'Is Miele better than Bosch?',
                'answer': 'Yes, Miele is higher tier than Bosch. While both are German, Miele focuses on ultimate quality and longevity. Miele uses better materials, more durable components, and tests for longer lifespans. Bosch offers excellent value in premium segment; Miele is ultra-premium with price to match.'
            },
            {
                'question': 'Where can I get Miele service in Toronto?',
                'answer': 'We provide Miele-trained service across Toronto and the GTA. Miele appliances require specialized knowledge and genuine parts. We maintain relationships with Miele parts suppliers and have experience with G-series dishwashers, W1 washers, and other Miele products. Call us for expert Miele service.'
            }
        ]
    },
    'fisher-paykel': {
        'name': 'Fisher & Paykel',
        'subtitle': 'Fisher & Paykel brings innovative New Zealand design to the appliance world with unique features like DishDrawers and ActiveSmart refrigeration. Our technicians are experienced with Fisher & Paykel\'s distinctive technology including drawer dishwashers and vertical washers across Toronto and the GTA.',
        'problems': [
            {
                'icon': '💧',
                'title': 'Fisher & Paykel DishDrawer Issues',
                'description': 'Unique drawer dishwashers with drainage or cleaning problems. We service DD24, DD60, and newer models, fix water inlet issues, and maintain these innovative machines.'
            },
            {
                'icon': '❄️',
                'title': 'Fisher & Paykel Fridge Not Cooling',
                'description': 'ActiveSmart refrigerators with temperature control issues. We diagnose Variable Temperature Zones, fix fan problems, and service the sophisticated refrigeration in French door and counter-depth models.'
            },
            {
                'icon': '🌊',
                'title': 'Fisher & Paykel Washer Won\'t Agitate',
                'description': 'Top-loaders with Smartdrive or AquaSmart having agitation issues. We service the unique motorized systems, fix electronic controls, and resolve wash cycle problems.'
            },
            {
                'icon': '🔥',
                'title': 'Fisher & Paykel Gas Range Problems',
                'description': 'Dual-fuel and gas ranges with ignition or temperature issues. We service the sealed dual-flow burners, replace igniters, and maintain precise temperature control.'
            },
            {
                'icon': '⚠️',
                'title': 'Fisher & Paykel Error Codes',
                'description': 'DishDrawers and other appliances showing error codes. We diagnose F codes in DishDrawers, resolve electronic issues, and clear error conditions to restore operation.'
            },
            {
                'icon': '🧊',
                'title': 'Fisher & Paykel Ice Maker Problems',
                'description': 'Built-in ice makers in refrigerators not working. We fix water supply issues, replace ice maker assemblies, and service the ActiveSmart systems.'
            }
        ],
        'faqs': [
            {
                'question': 'Are Fisher & Paykel DishDrawers reliable?',
                'answer': 'DishDrawers have a mixed reputation - brilliant design but can be finicky. Earlier models (2000s) had more issues; current generation is significantly improved. When working properly, they\'re fantastic for convenience. We service all generations and can keep them running reliably with proper maintenance.'
            },
            {
                'question': 'Who makes Fisher & Paykel?',
                'answer': 'Fisher & Paykel is a New Zealand company now owned by Chinese manufacturer Haier (who also owns GE Appliances). Despite ownership, F&P maintains independent design in New Zealand with focus on innovation. The brand retains its distinctive identity and unique features.'
            },
            {
                'question': 'Are Fisher & Paykel appliances expensive to fix?',
                'answer': 'Parts can be pricey due to unique designs - DishDrawer components run $150-400, control boards $250-500. However, their innovative features justify the investment. We stock common F&P parts and have experience with their distinctive technology for efficient repairs.'
            },
            {
                'question': 'How long do Fisher & Paykel appliances last?',
                'answer': 'Fisher & Paykel appliances typically last 12-16 years with proper maintenance. DishDrawers may need more service than traditional dishwashers, but refrigerators and ranges are quite durable. The ActiveSmart technology has proven reliable over time.'
            },
            {
                'question': 'What makes Fisher & Paykel different?',
                'answer': 'Innovation! DishDrawer dishwashers, ErgoDynamic washers, and ActiveSmart refrigeration are unique to F&P. They focus on user experience and efficiency over following conventional designs. You either love their approach or prefer traditional appliances - there\'s little middle ground.'
            }
        ]
    },
    'kenmore': {
        'name': 'Kenmore',
        'subtitle': 'Kenmore was Sears\' flagship brand for decades, known for value and availability. While Sears closed, Kenmore continues through other retailers. Our technicians service all Kenmore appliances - understanding they\'re manufactured by Whirlpool, LG, and others across Toronto and the GTA.',
        'problems': [
            {
                'icon': '🌊',
                'title': 'Kenmore Washer Won\'t Drain',
                'description': 'Elite and 600-series washers with drainage issues. We identify the actual manufacturer (Whirlpool or LG), diagnose pump problems, and fix drainage using the correct parts.'
            },
            {
                'icon': '❄️',
                'title': 'Kenmore Refrigerator Not Cold',
                'description': 'Elite and Pro models with cooling problems. We determine if it\'s LG-made or Whirlpool-made, diagnose the issue, and repair using manufacturer-appropriate parts.'
            },
            {
                'icon': '🔥',
                'title': 'Kenmore Dryer Not Heating',
                'description': 'Elite and 600-series dryers with heating issues. We fix thermal fuses, replace heating elements, and service both Whirlpool-based and LG-based Kenmore dryers.'
            },
            {
                'icon': '💧',
                'title': 'Kenmore Dishwasher Leaking',
                'description': 'Elite and Ultra Wash dishwashers with leak problems. We replace door seals, fix pump seals, and determine if repairs use Whirlpool or other manufacturer parts.'
            },
            {
                'icon': '🧊',
                'title': 'Kenmore Ice Maker Stopped',
                'description': 'Ice makers not working in Kenmore refrigerators. We identify the base manufacturer (often LG), fix water valves, and replace ice maker assemblies.'
            },
            {
                'icon': '⚙️',
                'title': 'Kenmore Control Board Issues',
                'description': 'Electronic controls failing in various Kenmore appliances. We identify the manufacturer, source the correct control board, and restore functionality.'
            }
        ],
        'faqs': [
            {
                'question': 'Are Kenmore appliances still made?',
                'answer': 'Yes! Though Sears closed, Kenmore continues as a brand sold through Home Depot, Amazon, and other retailers. Current Kenmore appliances are manufactured by Whirlpool, LG, Electrolux, and others. The brand name continues but product quality varies by who made your specific model.'
            },
            {
                'question': 'Who actually makes Kenmore appliances?',
                'answer': 'Kenmore is a brand label applied to appliances made by various manufacturers: Whirlpool (most models), LG (refrigerators, dishwashers), Frigidaire/Electrolux (some ranges), and others. We identify your model\'s manufacturer to use correct parts and repair procedures.'
            },
            {
                'question': 'Can you still get Kenmore parts?',
                'answer': 'Yes! Once we identify which company made your Kenmore appliance, parts are readily available. Whirlpool-made Kenmore parts are easy to get. LG-made Kenmore uses LG parts. We cross-reference your model to get the correct components for reliable repairs.'
            },
            {
                'question': 'Is Kenmore a good brand?',
                'answer': 'Kenmore quality varies by manufacturer. LG-made Kenmore Elite refrigerators are essentially LG appliances - quite good. Whirlpool-made Kenmore washers are solid. The brand\'s reputation for value and decent quality continues, though consistency varies more than single-manufacturer brands.'
            },
            {
                'question': 'How do I know who made my Kenmore?',
                'answer': 'The model number reveals the manufacturer. First 3 digits often indicate: 110/253/417/587 = Whirlpool, 795 = LG, 790 = Frigidaire, 596/106 = Whirlpool. We decode your model number to determine the manufacturer for proper service and parts.'
            }
        ]
    },
    'amana': {
        'name': 'Amana',
        'subtitle': 'Amana pioneered the microwave oven and remains a value-oriented brand offering reliability at budget-friendly prices. Owned by Whirlpool since 2002, Amana shares technology with premium brands while keeping costs low. Our technicians service all Amana appliances across Toronto and the GTA.',
        'problems': [
            {
                'icon': '❄️',
                'title': 'Amana Refrigerator Not Cooling',
                'description': 'Top-freezer and side-by-side models with cooling problems. We diagnose compressor issues, fix defrost problems, and restore proper cooling in Amana refrigerators at affordable repair prices.'
            },
            {
                'icon': '🌊',
                'title': 'Amana Washer Agitator Not Working',
                'description': 'Top-load washers with agitation problems. We fix motor couplings, replace agitator dogs, and service the simple, reliable mechanisms in Amana washers.'
            },
            {
                'icon': '🔥',
                'title': 'Amana Dryer Not Heating',
                'description': 'Electric dryers with heating element failures. We replace elements, fix thermal fuses, and restore drying capability in budget-friendly Amana dryers.'
            },
            {
                'icon': '💧',
                'title': 'Amana Dishwasher Not Cleaning',
                'description': 'Budget dishwashers with wash performance issues. We clean spray arms, replace wash motors, and improve cleaning results in Amana dishwashers.'
            },
            {
                'icon': '⚙️',
                'title': 'Amana Range Igniter Replacement',
                'description': 'Gas ranges with slow ignition or no ignition. We replace worn igniters, clean burner ports, and ensure safe operation in Amana gas ranges.'
            },
            {
                'icon': '🧊',
                'title': 'Amana Ice Maker Issues',
                'description': 'Ice makers in refrigerators not producing ice. We fix water valves, replace ice maker assemblies, and use affordable parts for cost-effective repairs.'
            }
        ],
        'faqs': [
            {
                'question': 'Is Amana a good brand for the price?',
                'answer': 'Yes! Amana offers excellent value - reliable appliances at budget prices. While lacking premium features, Amana delivers solid performance and easy repairs. Perfect for rentals, first homes, or budget-conscious buyers. Expect 10-14 years of service with basic maintenance.'
            },
            {
                'question': 'Who makes Amana appliances?',
                'answer': 'Whirlpool Corporation owns Amana (since 2002) and uses Amana as their value brand. Amana appliances share many parts with Whirlpool but use simpler controls and fewer features to hit lower price points. This means proven technology at accessible prices.'
            },
            {
                'question': 'Are Amana appliances cheap to repair?',
                'answer': 'Yes! Amana repairs are very affordable. Parts are budget-friendly ($40-150 for most components) and share inventory with Whirlpool. Simple designs make repairs straightforward, reducing labor time. This cost-effectiveness extends value throughout the appliance\'s lifetime.'
            },
            {
                'question': 'How long do Amana appliances last?',
                'answer': 'Amana appliances typically last 10-14 years - very good for the price point. Refrigerators average 12-14 years, washers and dryers 10-13 years. While not matching premium brands\' 15-20 year lifespans, Amana offers excellent longevity-per-dollar-spent.'
            },
            {
                'question': 'Is Amana better than Frigidaire?',
                'answer': 'They\'re comparable budget brands with different ownership. Amana (Whirlpool-owned) tends toward simpler, more reliable designs. Frigidaire (Electrolux-owned) offers slightly more features. Both deliver good value. Repair costs and reliability are similar. Choose based on specific model features you need.'
            }
        ]
    },
    'hotpoint': {
        'name': 'Hotpoint',
        'subtitle': 'Hotpoint is one of the oldest appliance brands (founded 1911) offering basic, budget-friendly appliances. Now owned by Haier, Hotpoint focuses on simple, reliable designs at entry-level prices. Our technicians service all Hotpoint appliances across Toronto and the GTA.',
        'problems': [
            {
                'icon': '❄️',
                'title': 'Hotpoint Fridge Not Cold Enough',
                'description': 'Top-freezer and bottom-freezer refrigerators with temperature issues. We diagnose thermostat problems, fix defrost systems, and restore proper cooling in budget-friendly Hotpoint refrigerators.'
            },
            {
                'icon': '🌊',
                'title': 'Hotpoint Washer Won\'t Spin',
                'description': 'Top-load washers with spin cycle problems. We fix lid switches, replace motor couplings, and service the straightforward mechanisms in Hotpoint washing machines.'
            },
            {
                'icon': '🔥',
                'title': 'Hotpoint Dryer Not Drying',
                'description': 'Electric dryers taking too long or not heating. We replace heating elements, clear venting, and optimize drying efficiency in basic Hotpoint dryers.'
            },
            {
                'icon': '💧',
                'title': 'Hotpoint Dishwasher Not Draining',
                'description': 'Standing water in budget dishwashers. We fix drain pumps, clear clogs, and ensure proper drainage in entry-level Hotpoint dishwashers.'
            },
            {
                'icon': '🔧',
                'title': 'Hotpoint Range Burner Issues',
                'description': 'Electric coil burners not heating or gas burners not lighting. We replace coils, fix igniters, and service basic Hotpoint ranges economically.'
            },
            {
                'icon': '⚙️',
                'title': 'Hotpoint Control Problems',
                'description': 'Simple mechanical or basic electronic controls failing. We replace timers, fix control boards, and keep repair costs low for budget appliances.'
            }
        ],
        'faqs': [
            {
                'question': 'Is Hotpoint a good brand?',
                'answer': 'Hotpoint is a basic, no-frills brand perfect for tight budgets. Don\'t expect premium features or longest lifespans, but they deliver functional performance at rock-bottom prices. Good for rentals, secondary homes, or anyone prioritizing cost over features. Expect 8-12 years of service.'
            },
            {
                'question': 'Who owns Hotpoint?',
                'answer': 'Hotpoint is owned by Haier (Chinese company that also owns GE Appliances). Hotpoint was historically a GE brand, then sold to Indesit, then acquired by Haier. Despite ownership changes, Hotpoint maintains its position as a budget-friendly entry-level brand.'
            },
            {
                'question': 'Are Hotpoint appliances cheap to fix?',
                'answer': 'Yes! Hotpoint repairs are very economical. Parts are inexpensive ($30-120 for most components), designs are simple, and repairs are straightforward. For budget appliances, Hotpoint offers good repair economics, though with simpler models, eventual replacement may make more sense than complex repairs.'
            },
            {
                'question': 'How long do Hotpoint appliances last?',
                'answer': 'Hotpoint appliances typically last 8-12 years - acceptable for the price point. Refrigerators average 10-12 years, washers/dryers 8-11 years. While shorter than premium brands, the low purchase price means reasonable cost-per-year of ownership.'
            },
            {
                'question': 'Should I buy Hotpoint or spend more?',
                'answer': 'Depends on your situation. Hotpoint works great for: rentals, tight budgets, temporary housing, or basic needs. Spend more if: you want 15+ year lifespan, value advanced features, use appliances heavily, or prefer quieter operation. We can honestly assess repair vs replacement for your Hotpoint.'
            }
        ]
    },
    'danby': {
        'name': 'Danby',
        'subtitle': 'Danby is a Canadian company specializing in compact and specialty appliances perfect for condos, apartments, and smaller spaces. From mini-fridges to portable dishwashers, Danby focuses on space-saving solutions. Our technicians service all Danby appliances across Toronto and the GTA.',
        'problems': [
            {
                'icon': '❄️',
                'title': 'Danby Mini Fridge Not Cooling',
                'description': 'Compact refrigerators and wine coolers with cooling issues. We diagnose compressor problems, fix thermoelectric cooling systems, and service both compressor and Peltier-based Danby refrigerators.'
            },
            {
                'icon': '💧',
                'title': 'Danby Portable Dishwasher Issues',
                'description': 'Countertop and portable dishwashers with drainage or cleaning problems. We fix pump issues, clear clogs, and service the compact mechanisms in Danby portable dishwashers.'
            },
            {
                'icon': '🌊',
                'title': 'Danby Portable Washer Won\'t Drain',
                'description': 'Compact washing machines with drainage issues. We fix drain pumps, clear hoses, and service space-saving Danby portable washers used in apartments and condos.'
            },
            {
                'icon': '❄️',
                'title': 'Danby Window Air Conditioner',
                'description': 'Window A/C units not cooling properly. We diagnose compressor issues, fix refrigerant leaks, clean coils, and assess repair vs replacement for Danby air conditioners.'
            },
            {
                'icon': '🧊',
                'title': 'Danby Ice Maker Not Working',
                'description': 'Countertop ice makers not producing ice. We fix water pumps, clear mineral buildup, and service portable ice makers for home and small office use.'
            },
            {
                'icon': '🔧',
                'title': 'Danby Dehumidifier Problems',
                'description': 'Portable dehumidifiers not collecting water. We fix compressors, clean coils, and service Danby dehumidifiers for basements and humid spaces.'
            }
        ],
        'faqs': [
            {
                'question': 'Is Danby a good brand for compact appliances?',
                'answer': 'Yes! Danby specializes in compact appliances and does it well. While not luxury quality, Danby offers reliable performance in small packages perfect for condos, apartments, dorms, and offices. For space-constrained situations, Danby provides excellent solutions at reasonable prices.'
            },
            {
                'question': 'Where is Danby made?',
                'answer': 'Danby is a Canadian company (headquartered in Ontario) but manufactures in China and other locations. Despite offshore production, Danby maintains Canadian-based design and quality control. They\'re one of the few Canadian-owned appliance brands still operating.'
            },
            {
                'question': 'Are Danby appliances worth repairing?',
                'answer': 'It depends on the appliance and repair cost. Compact refrigerators and specialty items often make sense to repair ($100-250 typically). For very small units like mini-fridges under $200 new, replacement might be more economical. We provide honest assessment of repair vs replace.'
            },
            {
                'question': 'How long do Danby appliances last?',
                'answer': 'Danby compact appliances typically last 6-10 years - good for their category and price point. Full-size Danby appliances (less common) last 8-12 years. Portable and specialty units may have shorter lifespans but often face lighter use in their typical applications.'
            },
            {
                'question': 'Can you service Danby portable dishwashers?',
                'answer': 'Absolutely! We service all Danby portable and countertop dishwashers. Common issues include drain pump failures, water inlet problems, and control issues. Parts are available and repairs are usually straightforward. We can also help with installation and connection questions for portable units.'
            }
        ]
    }
})

def generate_problems_html(problems):
    """Generate HTML for brand-specific problems section"""
    html = []
    for problem in problems:
        html.append(f'''                <div class="problem-card">
                    <div class="problem-icon">{problem['icon']}</div>
                    <h3>{problem['title']}</h3>
                    <p>{problem['description']}</p>
                </div>
''')
    return ''.join(html)

def generate_faqs_html(faqs):
    """Generate HTML for brand-specific FAQ section"""
    html = []
    for faq in faqs:
        # Escape single quotes in answers for proper HTML
        answer = faq['answer'].replace("'", "&#39;")
        html.append(f'''                <div class="faq-item">
                    <div class="faq-question" role="button" tabindex="0" aria-expanded="false">
                        <span>{faq['question']}</span>
                        <span class="faq-icon">+</span>
                    </div>
                    <div class="faq-answer">
                        <p>{faq['answer']}</p>
                    </div>
                </div>
''')
    return ''.join(html)

def update_brand_page(brand_slug, brand_data):
    """Update a single brand page with unique content"""
    filepath = f'brands/{brand_slug}-appliance-repair-toronto.html'

    if not os.path.exists(filepath):
        print(f"WARNING: File not found: {filepath}")
        return False

    print(f"\nUpdating {brand_data['name']} brand page...")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find and replace the subtitle in Common Problems section
    subtitle_pattern = r'(<h2 class="section-title-light">What Are the Most Common Appliance Problems\?</h2>\s*<p class="section-subtitle">)[^<]+(</p>)'
    subtitle_replacement = f'\\1{brand_data["subtitle"]}\\2'
    content = re.sub(subtitle_pattern, subtitle_replacement, content)

    # Find and replace the problems grid
    problems_pattern = r'(<div class="problems-grid">)(.*?)(</div>\s*<div class="emergency-cta-box">)'
    problems_html = generate_problems_html(brand_data['problems'])
    problems_replacement = f'\\1\n{problems_html}            \\3'
    content = re.sub(problems_pattern, problems_replacement, content, flags=re.DOTALL)

    # Find and replace the FAQ section
    faq_pattern = r'(<h2 class="section-title">Frequently Asked Questions</h2>\s*<div class="faq-grid">)(.*?)(</div>\s*</section>)'
    faq_html = generate_faqs_html(brand_data['faqs'])
    faq_replacement = f'\\1\n{faq_html}            \\3'
    content = re.sub(faq_pattern, faq_replacement, content, flags=re.DOTALL)

    # Write back to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"OK Updated {brand_data['name']} with {len(brand_data['problems'])} unique problems and {len(brand_data['faqs'])} unique FAQs")
    return True

# Main execution
print("=" * 60)
print("CREATING UNIQUE BRAND CONTENT FOR ALL BRAND PAGES")
print("=" * 60)

updated_count = 0
for brand_slug, brand_data in BRAND_DATA.items():
    if update_brand_page(brand_slug, brand_data):
        updated_count += 1

print("\n" + "=" * 60)
print(f"COMPLETE! Updated {updated_count}/{len(BRAND_DATA)} brand pages")
print("=" * 60)
print("\nEach brand page now has:")
print("  - Unique brand-specific subtitle")
print("  - 6 brand-specific common problems")
print("  - 5 brand-specific FAQ questions")
print("\nThis will significantly improve SEO and eliminate duplicate content penalties!")
