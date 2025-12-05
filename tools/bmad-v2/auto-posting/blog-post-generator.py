#!/usr/bin/env python3
"""
BMAD Blog Post Generator
Generates SEO-optimized blog posts using the proven BMAD template structure.
Based on keyword gap analysis from DataForSEO.

Part of BMAD v2 Auto-Posting System for Nika Appliance Repair
"""

import os
import re
from pathlib import Path
from datetime import datetime, timedelta

# 20 Blog Posts based on DataForSEO Keyword Gap Analysis
# Low competition keywords where competitors rank but nikaappliancerepair.com doesn't
BLOG_POSTS = [
    {
        "slug": "lg-dishwasher-error-codes-troubleshooting",
        "title": "LG Dishwasher Error Codes: Complete Troubleshooting Guide",
        "category": "troubleshooting",
        "keyword": "lg dishwasher troubleshooting codes",
        "volume": 880,
        "appliance": "dishwasher",
        "brand": "LG"
    },
    {
        "slug": "fix-gas-oven-not-heating",
        "title": "Fix Gas Oven Not Heating: Toronto Repair Guide 2025",
        "category": "troubleshooting",
        "keyword": "fix gas oven",
        "volume": 880,
        "appliance": "oven",
        "brand": None
    },
    {
        "slug": "dishwasher-leaking-from-bottom-causes-fixes",
        "title": "Dishwasher Leaking From Bottom: Causes & Professional Fixes",
        "category": "troubleshooting",
        "keyword": "dishwasher leaking",
        "volume": 590,
        "appliance": "dishwasher",
        "brand": None
    },
    {
        "slug": "lg-appliance-repair-toronto-complete-guide",
        "title": "LG Appliance Repair Toronto: Expert Service Guide 2025",
        "category": "guides",
        "keyword": "lg appliance repair",
        "volume": 590,
        "appliance": "appliance",
        "brand": "LG"
    },
    {
        "slug": "samsung-ice-maker-not-making-ice",
        "title": "Samsung Ice Maker Not Making Ice: Troubleshooting Solutions",
        "category": "troubleshooting",
        "keyword": "samsung ice maker not making ice",
        "volume": 590,
        "appliance": "refrigerator",
        "brand": "Samsung"
    },
    {
        "slug": "whirlpool-dishwasher-not-cleaning-dishes",
        "title": "Whirlpool Dishwasher Not Cleaning Dishes: Quick Fixes",
        "category": "troubleshooting",
        "keyword": "whirlpool dishwasher not cleaning",
        "volume": 320,
        "appliance": "dishwasher",
        "brand": "Whirlpool"
    },
    {
        "slug": "kenmore-refrigerator-repair-common-issues",
        "title": "Kenmore Refrigerator Repair: Common Issues & Solutions",
        "category": "guides",
        "keyword": "kenmore refrigerator repair",
        "volume": 260,
        "appliance": "refrigerator",
        "brand": "Kenmore"
    },
    {
        "slug": "dryer-not-heating-troubleshooting-guide",
        "title": "Dryer Not Heating: Complete Troubleshooting Guide Toronto",
        "category": "troubleshooting",
        "keyword": "dryer not heating",
        "volume": 240,
        "appliance": "dryer",
        "brand": None
    },
    {
        "slug": "washing-machine-not-spinning-causes-solutions",
        "title": "Washing Machine Not Spinning: Causes & DIY Solutions",
        "category": "troubleshooting",
        "keyword": "washing machine not spinning",
        "volume": 220,
        "appliance": "washer",
        "brand": None
    },
    {
        "slug": "refrigerator-not-cooling-emergency-repair",
        "title": "Refrigerator Not Cooling: Emergency Repair Guide Toronto",
        "category": "troubleshooting",
        "keyword": "refrigerator not cooling",
        "volume": 200,
        "appliance": "refrigerator",
        "brand": None
    },
    {
        "slug": "oven-not-heating-evenly-calibration-tips",
        "title": "Oven Not Heating Evenly: Calibration & Repair Tips",
        "category": "troubleshooting",
        "keyword": "oven not heating evenly",
        "volume": 180,
        "appliance": "oven",
        "brand": None
    },
    {
        "slug": "dishwasher-not-draining-quick-fixes",
        "title": "Dishwasher Not Draining: Quick Fixes & When to Call Pro",
        "category": "troubleshooting",
        "keyword": "dishwasher not draining",
        "volume": 170,
        "appliance": "dishwasher",
        "brand": None
    },
    {
        "slug": "freezer-making-loud-noise-diagnosis",
        "title": "Freezer Making Loud Noise: Diagnosis & Repair Toronto",
        "category": "troubleshooting",
        "keyword": "freezer making noise",
        "volume": 160,
        "appliance": "refrigerator",
        "brand": None
    },
    {
        "slug": "washer-leaking-from-bottom-common-causes",
        "title": "Washer Leaking From Bottom: Common Causes & Solutions",
        "category": "troubleshooting",
        "keyword": "washer leaking from bottom",
        "volume": 150,
        "appliance": "washer",
        "brand": None
    },
    {
        "slug": "gas-stove-burner-not-igniting-safety-guide",
        "title": "Gas Stove Burner Not Igniting: Safety & Repair Guide",
        "category": "troubleshooting",
        "keyword": "stove burner not igniting",
        "volume": 140,
        "appliance": "oven",
        "brand": None
    },
    {
        "slug": "ice-maker-troubleshooting-complete-guide",
        "title": "Ice Maker Troubleshooting: Complete Repair Guide Toronto",
        "category": "troubleshooting",
        "keyword": "ice maker troubleshooting",
        "volume": 130,
        "appliance": "refrigerator",
        "brand": None
    },
    {
        "slug": "dryer-making-squeaking-noise-causes-fixes",
        "title": "Dryer Making Squeaking Noise: Causes & Easy Fixes",
        "category": "troubleshooting",
        "keyword": "dryer squeaking noise",
        "volume": 120,
        "appliance": "dryer",
        "brand": None
    },
    {
        "slug": "refrigerator-compressor-problems-signs-repair",
        "title": "Refrigerator Compressor Problems: Signs & Repair Options",
        "category": "troubleshooting",
        "keyword": "refrigerator compressor problems",
        "volume": 110,
        "appliance": "refrigerator",
        "brand": None
    },
    {
        "slug": "dishwasher-soap-dispenser-not-opening",
        "title": "Dishwasher Soap Dispenser Not Opening: Easy Fixes",
        "category": "troubleshooting",
        "keyword": "dishwasher soap dispenser not opening",
        "volume": 100,
        "appliance": "dishwasher",
        "brand": None
    },
    {
        "slug": "washing-machine-error-codes-brand-guide",
        "title": "Washing Machine Error Codes: Complete Brand Guide Toronto",
        "category": "guides",
        "keyword": "washing machine error codes",
        "volume": 200,
        "appliance": "washer",
        "brand": None
    },
]


def get_content_for_post(post):
    """Generate unique content based on post type"""

    appliance = post["appliance"]
    keyword = post["keyword"]
    brand = post.get("brand", "")
    brand_text = f"{brand} " if brand else ""

    # Content templates based on appliance type
    content_templates = {
        "dishwasher": {
            "intro": f"""
                <p>Is your {brand_text}dishwasher giving you trouble? You're not alone. As Toronto's trusted appliance repair specialists, we handle {keyword} issues every day. This comprehensive guide will help you understand the problem, try safe DIY fixes, and know when it's time to call a professional.</p>

                <p>At Nika Appliance Repair, we've completed over 8,500 dishwasher repairs across Toronto since 2017. Our factory-trained technicians understand the unique challenges Toronto's hard water presents for dishwashers. Whether you need a quick fix or professional service, we're here to help with same-day appointments and a 90-day warranty on all repairs.</p>
            """,
            "problems": f"""
                <h2 id="common-problems">Understanding {brand_text}Dishwasher Problems</h2>

                <p>Based on our extensive experience with {keyword} issues in Toronto, here are the most common causes:</p>

                <h3>1. Water Supply Issues</h3>
                <p>Many dishwasher problems stem from water-related issues:</p>
                <ul>
                    <li><strong>Clogged inlet valve:</strong> Toronto's hard water causes mineral buildup that restricts water flow</li>
                    <li><strong>Water temperature too low:</strong> Dishwashers need hot water (120°F minimum) for proper cleaning</li>
                    <li><strong>Low water pressure:</strong> Can affect fill times and cleaning performance</li>
                </ul>

                <h3>2. Drainage Problems</h3>
                <p>Drainage issues are among the most common complaints:</p>
                <ul>
                    <li><strong>Clogged filter:</strong> Food debris accumulates and blocks drainage</li>
                    <li><strong>Blocked drain hose:</strong> Kinks or clogs prevent water from draining</li>
                    <li><strong>Faulty drain pump:</strong> Motor failure prevents water evacuation</li>
                    <li><strong>Air gap blockage:</strong> Required by Toronto building code, can clog over time</li>
                </ul>

                <h3>3. Mechanical Failures</h3>
                <ul>
                    <li><strong>Spray arm problems:</strong> Clogged holes or worn bearings reduce cleaning power</li>
                    <li><strong>Door latch issues:</strong> Prevents cycle from starting</li>
                    <li><strong>Heating element failure:</strong> Affects drying and sanitization</li>
                </ul>

                <div class="tip-box">
                    <strong>💡 Pro Tip:</strong> Toronto's hard water (6-7 grains per gallon) accelerates wear on dishwasher components. Using rinse aid and running a monthly descaling cycle can extend your dishwasher's life by 3-5 years.
                </div>
            """,
            "diy": """
                <h2 id="diy-fixes">Safe DIY Troubleshooting Steps</h2>

                <p>Before calling for service, try these safe troubleshooting steps:</p>

                <h3>Step 1: Check the Basics</h3>
                <ul>
                    <li>Verify the dishwasher is plugged in and receiving power</li>
                    <li>Check that the door latches completely</li>
                    <li>Ensure water supply valve under sink is fully open</li>
                    <li>Run hot water at kitchen sink before starting cycle</li>
                </ul>

                <h3>Step 2: Clean the Filter System</h3>
                <p>Most dishwasher problems start with a dirty filter:</p>
                <ol>
                    <li>Remove the lower rack</li>
                    <li>Locate and remove the filter (usually bottom center)</li>
                    <li>Rinse under hot water and scrub with soft brush</li>
                    <li>Check for debris in the filter cavity</li>
                    <li>Reinstall filter securely</li>
                </ol>

                <h3>Step 3: Inspect Spray Arms</h3>
                <ul>
                    <li>Remove spray arms (usually twist off)</li>
                    <li>Clear blocked holes with toothpick</li>
                    <li>Soak in white vinegar for 30 minutes</li>
                    <li>Verify arms spin freely when reinstalled</li>
                </ul>

                <h3>Step 4: Run a Cleaning Cycle</h3>
                <p>Empty the dishwasher and run a hot cycle with 2 cups of white vinegar or dishwasher cleaner to remove buildup.</p>

                <div class="warning-box">
                    <h4>⚠️ Safety Warning</h4>
                    <p>Never attempt repairs involving electrical components, water valves, or the pump system without professional training. These repairs require proper tools and knowledge to avoid injury or further damage.</p>
                </div>
            """,
            "costs": """
                <h2 id="repair-costs">Dishwasher Repair Costs in Toronto</h2>

                <p>Understanding repair costs helps you make informed decisions:</p>

                <table>
                    <thead>
                        <tr>
                            <th>Repair Type</th>
                            <th>Cost Range</th>
                            <th>Time Required</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Diagnostic Service Call</td>
                            <td>$95 (waived with repair)</td>
                            <td>30-45 minutes</td>
                        </tr>
                        <tr>
                            <td>Drain Pump Replacement</td>
                            <td>$180-$280</td>
                            <td>45-75 minutes</td>
                        </tr>
                        <tr>
                            <td>Water Inlet Valve</td>
                            <td>$150-$220</td>
                            <td>30-60 minutes</td>
                        </tr>
                        <tr>
                            <td>Door Latch Assembly</td>
                            <td>$120-$200</td>
                            <td>30-45 minutes</td>
                        </tr>
                        <tr>
                            <td>Spray Arm Replacement</td>
                            <td>$80-$150</td>
                            <td>20-30 minutes</td>
                        </tr>
                        <tr>
                            <td>Control Board</td>
                            <td>$250-$400</td>
                            <td>60-90 minutes</td>
                        </tr>
                        <tr>
                            <td>Heating Element</td>
                            <td>$180-$260</td>
                            <td>60-90 minutes</td>
                        </tr>
                    </tbody>
                </table>
            """
        },
        "refrigerator": {
            "intro": f"""
                <p>A malfunctioning {brand_text}refrigerator can quickly turn into a food safety emergency. When you're dealing with {keyword}, time is critical to prevent food spoilage. This guide provides expert troubleshooting steps and helps you understand when professional repair is necessary.</p>

                <p>At Nika Appliance Repair, we offer same-day refrigerator service across Toronto because we understand that a broken fridge can't wait. Our certified technicians have repaired over 6,200 refrigerators since 2017, and we stock common parts on our trucks for faster repairs.</p>
            """,
            "problems": f"""
                <h2 id="common-problems">Common {brand_text}Refrigerator Issues</h2>

                <p>Understanding the root cause of {keyword} helps determine the best solution:</p>

                <h3>1. Cooling System Problems</h3>
                <ul>
                    <li><strong>Dirty condenser coils:</strong> Dust buildup forces compressor to work harder, reducing efficiency</li>
                    <li><strong>Evaporator fan failure:</strong> Prevents cold air circulation in fresh food compartment</li>
                    <li><strong>Compressor issues:</strong> The heart of your cooling system may be failing</li>
                    <li><strong>Refrigerant leak:</strong> Requires professional repair and recharging</li>
                </ul>

                <h3>2. Temperature Control Issues</h3>
                <ul>
                    <li><strong>Thermostat malfunction:</strong> Incorrect temperature readings cause over/under cooling</li>
                    <li><strong>Control board failure:</strong> Electronic controls stop responding</li>
                    <li><strong>Temperature sensor problems:</strong> Sends wrong signals to control system</li>
                </ul>

                <h3>3. Ice Maker and Freezer Problems</h3>
                <ul>
                    <li><strong>Ice maker not producing:</strong> Water line frozen or inlet valve failed</li>
                    <li><strong>Frost buildup:</strong> Defrost system malfunction</li>
                    <li><strong>Freezer too cold/warm:</strong> Air damper or sensor issues</li>
                </ul>

                <div class="info-box">
                    <h3>🌡️ Optimal Temperature Settings</h3>
                    <p>For food safety and energy efficiency:</p>
                    <ul>
                        <li><strong>Refrigerator:</strong> 35-38°F (2-3°C)</li>
                        <li><strong>Freezer:</strong> 0°F (-18°C)</li>
                        <li>Allow 24 hours after adjustment for temperature to stabilize</li>
                    </ul>
                </div>
            """,
            "diy": """
                <h2 id="diy-fixes">DIY Troubleshooting Steps</h2>

                <p>Many refrigerator issues can be diagnosed or resolved without professional help:</p>

                <h3>Step 1: Check Power and Settings</h3>
                <ul>
                    <li>Verify refrigerator is plugged in and outlet works</li>
                    <li>Check that temperature controls weren't accidentally adjusted</li>
                    <li>Ensure the interior light turns on when door opens</li>
                    <li>Listen for compressor running (low humming sound)</li>
                </ul>

                <h3>Step 2: Clean Condenser Coils</h3>
                <p>Dirty coils are the #1 cause of cooling problems:</p>
                <ol>
                    <li>Unplug the refrigerator</li>
                    <li>Locate coils (back or bottom of unit)</li>
                    <li>Use coil brush or vacuum to remove dust</li>
                    <li>Clean every 6-12 months</li>
                </ol>

                <h3>Step 3: Check Door Seals</h3>
                <ul>
                    <li>Close door on a dollar bill - if it slides out easily, seal is worn</li>
                    <li>Clean gaskets with warm soapy water</li>
                    <li>Check for cracks or tears in rubber</li>
                </ul>

                <h3>Step 4: Ensure Proper Airflow</h3>
                <ul>
                    <li>Don't overfill refrigerator - air needs to circulate</li>
                    <li>Keep vents clear between freezer and fridge sections</li>
                    <li>Maintain 2-3 inches clearance around exterior</li>
                </ul>

                <div class="warning-box">
                    <h4>⚠️ Safety First</h4>
                    <p>Never attempt to repair sealed system components (compressor, evaporator, condenser) yourself. These repairs require EPA certification and specialized tools. Improper handling of refrigerant is illegal and dangerous.</p>
                </div>
            """,
            "costs": """
                <h2 id="repair-costs">Refrigerator Repair Costs in Toronto</h2>

                <table>
                    <thead>
                        <tr>
                            <th>Repair Type</th>
                            <th>Cost Range</th>
                            <th>Time Required</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Diagnostic Service</td>
                            <td>$95 (waived with repair)</td>
                            <td>30-45 minutes</td>
                        </tr>
                        <tr>
                            <td>Thermostat Replacement</td>
                            <td>$150-$250</td>
                            <td>30-60 minutes</td>
                        </tr>
                        <tr>
                            <td>Evaporator Fan Motor</td>
                            <td>$180-$280</td>
                            <td>45-75 minutes</td>
                        </tr>
                        <tr>
                            <td>Ice Maker Assembly</td>
                            <td>$200-$350</td>
                            <td>60-90 minutes</td>
                        </tr>
                        <tr>
                            <td>Door Seal Replacement</td>
                            <td>$150-$250</td>
                            <td>30-60 minutes</td>
                        </tr>
                        <tr>
                            <td>Control Board</td>
                            <td>$300-$450</td>
                            <td>60-90 minutes</td>
                        </tr>
                        <tr>
                            <td>Compressor Replacement</td>
                            <td>$400-$700</td>
                            <td>2-4 hours</td>
                        </tr>
                    </tbody>
                </table>
            """
        },
        "dryer": {
            "intro": f"""
                <p>A {brand_text}dryer that won't heat or makes strange noises can disrupt your entire household routine. When dealing with {keyword}, understanding the cause helps you decide whether it's a DIY fix or time for professional service.</p>

                <p>Nika Appliance Repair has completed over 4,300 dryer repairs in Toronto since 2017. Our technicians are trained to handle both gas and electric dryers from all major brands. We offer same-day service and back all repairs with our 90-day warranty.</p>
            """,
            "problems": f"""
                <h2 id="common-problems">Common {brand_text}Dryer Issues</h2>

                <h3>1. Heating Problems</h3>
                <p>When your dryer runs but doesn't heat:</p>
                <ul>
                    <li><strong>Faulty heating element:</strong> Electric dryers use a coil that can burn out over time ($150-$250 repair)</li>
                    <li><strong>Broken thermal fuse:</strong> Safety device trips when dryer overheats ($120-$180 repair)</li>
                    <li><strong>Gas igniter failure:</strong> Gas dryers need working igniter to heat ($150-$220 repair)</li>
                    <li><strong>Clogged vent:</strong> Restricted airflow causes dryer to overheat and shut off</li>
                </ul>

                <h3>2. Noise Issues</h3>
                <ul>
                    <li><strong>Worn drum rollers:</strong> Cause thumping or rumbling sounds</li>
                    <li><strong>Damaged belt:</strong> Creates squealing or screeching</li>
                    <li><strong>Failing motor bearings:</strong> Produce grinding noises</li>
                    <li><strong>Loose blower wheel:</strong> Causes rattling or squeaking</li>
                </ul>

                <h3>3. Operational Problems</h3>
                <ul>
                    <li><strong>Won't start:</strong> Door switch, start switch, or control board failure</li>
                    <li><strong>Stops mid-cycle:</strong> Often thermal fuse or motor overload</li>
                    <li><strong>Takes too long:</strong> Usually vent restriction or failing heating</li>
                </ul>

                <div class="tip-box">
                    <strong>🔥 Fire Safety:</strong> Clogged dryer vents cause over 15,000 house fires annually in North America. Clean your lint trap after every load and have vents professionally cleaned yearly.
                </div>
            """,
            "diy": """
                <h2 id="diy-fixes">Safe DIY Troubleshooting</h2>

                <h3>Step 1: Check the Basics</h3>
                <ul>
                    <li>Verify dryer is plugged in securely (electric dryers need 240V)</li>
                    <li>Check circuit breaker - dryers use two breakers, both must be on</li>
                    <li>Ensure door latches completely</li>
                    <li>For gas dryers, verify gas supply valve is open</li>
                </ul>

                <h3>Step 2: Clean the Exhaust System</h3>
                <ol>
                    <li>Clean lint trap thoroughly (soap and water for residue buildup)</li>
                    <li>Disconnect vent hose and check for blockages</li>
                    <li>Vacuum inside vent connection on dryer</li>
                    <li>Check exterior vent flap opens freely</li>
                </ol>

                <h3>Step 3: Test Airflow</h3>
                <p>Run the dryer and check outside vent - you should feel strong, warm air. Weak airflow indicates vent blockage.</p>

                <h3>Step 4: Listen and Observe</h3>
                <ul>
                    <li>Note any unusual sounds during operation</li>
                    <li>Check if drum rotates smoothly</li>
                    <li>Observe if dryer heats at all (clothes should be warm)</li>
                </ul>

                <div class="warning-box">
                    <h4>⚠️ Gas Dryer Warning</h4>
                    <p>If you smell gas, DO NOT use the dryer. Turn off gas supply, ventilate the area, and call a professional immediately. Gas leaks are serious safety hazards.</p>
                </div>
            """,
            "costs": """
                <h2 id="repair-costs">Dryer Repair Costs in Toronto</h2>

                <table>
                    <thead>
                        <tr>
                            <th>Repair Type</th>
                            <th>Cost Range</th>
                            <th>Time Required</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Diagnostic Service</td>
                            <td>$95 (waived with repair)</td>
                            <td>30-45 minutes</td>
                        </tr>
                        <tr>
                            <td>Thermal Fuse</td>
                            <td>$120-$180</td>
                            <td>30-45 minutes</td>
                        </tr>
                        <tr>
                            <td>Heating Element</td>
                            <td>$150-$250</td>
                            <td>45-75 minutes</td>
                        </tr>
                        <tr>
                            <td>Gas Igniter</td>
                            <td>$150-$220</td>
                            <td>45-60 minutes</td>
                        </tr>
                        <tr>
                            <td>Drum Rollers (set)</td>
                            <td>$140-$200</td>
                            <td>60-90 minutes</td>
                        </tr>
                        <tr>
                            <td>Drive Belt</td>
                            <td>$100-$160</td>
                            <td>45-60 minutes</td>
                        </tr>
                        <tr>
                            <td>Motor</td>
                            <td>$250-$400</td>
                            <td>90-120 minutes</td>
                        </tr>
                    </tbody>
                </table>
            """
        },
        "washer": {
            "intro": f"""
                <p>When your {brand_text}washing machine isn't working properly, laundry piles up fast. Whether you're dealing with {keyword} or other issues, this guide helps you troubleshoot the problem and understand your repair options.</p>

                <p>Nika Appliance Repair has serviced over 5,100 washing machines across Toronto since 2017. Our technicians handle both top-load and front-load washers from all major brands. Same-day service is available, and all repairs include our 90-day warranty.</p>
            """,
            "problems": f"""
                <h2 id="common-problems">Common {brand_text}Washing Machine Issues</h2>

                <h3>1. Spin Cycle Problems</h3>
                <ul>
                    <li><strong>Unbalanced load:</strong> Overloading or uneven distribution triggers safety shutoff</li>
                    <li><strong>Lid switch failure:</strong> Top-loaders won't spin if switch doesn't detect closed lid</li>
                    <li><strong>Door latch issue:</strong> Front-loaders need secure latch to operate</li>
                    <li><strong>Worn belt:</strong> Loose or broken belt can't transfer motor power to drum</li>
                    <li><strong>Motor coupler failure:</strong> Direct-drive washers need this part to spin</li>
                </ul>

                <h3>2. Drainage Issues</h3>
                <ul>
                    <li><strong>Clogged drain pump:</strong> Small items like coins or socks block pump</li>
                    <li><strong>Kinked drain hose:</strong> Prevents water from exiting</li>
                    <li><strong>Pump failure:</strong> Motor burns out preventing drainage</li>
                </ul>

                <h3>3. Leaking Problems</h3>
                <ul>
                    <li><strong>Door boot seal (front-load):</strong> Rubber seal deteriorates and leaks</li>
                    <li><strong>Hose connections:</strong> Loose or cracked fill/drain hoses</li>
                    <li><strong>Tub seal:</strong> Seal between tub and transmission fails</li>
                    <li><strong>Detergent overdose:</strong> Excess suds can overflow</li>
                </ul>

                <div class="info-box">
                    <h3>Toronto Hard Water Tip</h3>
                    <p>Toronto's hard water causes mineral buildup in washers. Run a hot cleaning cycle with washer cleaner monthly. Use HE (high-efficiency) detergent in proper amounts to prevent residue buildup.</p>
                </div>
            """,
            "diy": """
                <h2 id="diy-fixes">DIY Troubleshooting Steps</h2>

                <h3>Step 1: Check Power and Water</h3>
                <ul>
                    <li>Verify washer is plugged in and outlet works</li>
                    <li>Check that both hot and cold water valves are open</li>
                    <li>Ensure drain hose is positioned correctly (not too deep in standpipe)</li>
                </ul>

                <h3>Step 2: Balance the Load</h3>
                <ul>
                    <li>Redistribute clothes evenly around drum</li>
                    <li>Don't overload - leave room for clothes to move</li>
                    <li>Wash similar items together (towels with towels, etc.)</li>
                </ul>

                <h3>Step 3: Clean the Machine</h3>
                <ol>
                    <li>Clean door seal/gasket with diluted bleach</li>
                    <li>Wipe detergent dispenser</li>
                    <li>Run hot cleaning cycle monthly</li>
                    <li>Leave door open between uses to prevent mold</li>
                </ol>

                <h3>Step 4: Check for Blockages</h3>
                <ul>
                    <li>Clean lint filter if equipped</li>
                    <li>Check drain pump filter (front-loaders have access panel)</li>
                    <li>Inspect drain hose for kinks</li>
                </ul>

                <div class="warning-box">
                    <h4>⚠️ Flood Prevention</h4>
                    <p>Always turn off water supply valves when leaving for extended periods. A failed fill hose can cause thousands in water damage. Consider installing automatic shutoff valves for peace of mind.</p>
                </div>
            """,
            "costs": """
                <h2 id="repair-costs">Washing Machine Repair Costs in Toronto</h2>

                <table>
                    <thead>
                        <tr>
                            <th>Repair Type</th>
                            <th>Cost Range</th>
                            <th>Time Required</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Diagnostic Service</td>
                            <td>$95 (waived with repair)</td>
                            <td>30-45 minutes</td>
                        </tr>
                        <tr>
                            <td>Lid/Door Switch</td>
                            <td>$120-$180</td>
                            <td>30-45 minutes</td>
                        </tr>
                        <tr>
                            <td>Drain Pump</td>
                            <td>$180-$280</td>
                            <td>45-75 minutes</td>
                        </tr>
                        <tr>
                            <td>Door Boot Seal</td>
                            <td>$200-$300</td>
                            <td>60-90 minutes</td>
                        </tr>
                        <tr>
                            <td>Drive Belt</td>
                            <td>$100-$160</td>
                            <td>45-60 minutes</td>
                        </tr>
                        <tr>
                            <td>Motor Coupler</td>
                            <td>$150-$220</td>
                            <td>60-90 minutes</td>
                        </tr>
                        <tr>
                            <td>Control Board</td>
                            <td>$280-$420</td>
                            <td>60-90 minutes</td>
                        </tr>
                    </tbody>
                </table>
            """
        },
        "oven": {
            "intro": f"""
                <p>When your {brand_text}oven isn't working properly, meal preparation becomes a challenge. Whether you're dealing with {keyword} or other heating issues, understanding the problem helps you make smart repair decisions.</p>

                <p>Nika Appliance Repair has serviced over 3,800 ovens and ranges across Toronto since 2017. Our certified technicians handle both gas and electric ovens, including convection and professional-grade units. We prioritize gas appliance safety and offer same-day service for urgent repairs.</p>
            """,
            "problems": f"""
                <h2 id="common-problems">Common {brand_text}Oven Issues</h2>

                <h3>1. Heating Problems</h3>
                <ul>
                    <li><strong>Electric element failure:</strong> Bake or broil element burns out, visible as breaks or blisters</li>
                    <li><strong>Gas igniter failure:</strong> Glowing igniter doesn't get hot enough to open gas valve</li>
                    <li><strong>Temperature sensor fault:</strong> Oven doesn't reach or maintain correct temperature</li>
                    <li><strong>Control board issues:</strong> Electronic controls malfunction</li>
                </ul>

                <h3>2. Uneven Heating</h3>
                <ul>
                    <li><strong>Convection fan problems:</strong> Fan doesn't circulate air properly</li>
                    <li><strong>Calibration needed:</strong> Temperature setting doesn't match actual temperature</li>
                    <li><strong>Damaged heating element:</strong> Partial failure causes hot spots</li>
                    <li><strong>Door seal wear:</strong> Heat escapes through worn gasket</li>
                </ul>

                <h3>3. Ignition Issues (Gas Ovens)</h3>
                <ul>
                    <li><strong>Worn igniter:</strong> Takes too long to heat up</li>
                    <li><strong>Faulty safety valve:</strong> Won't open even with hot igniter</li>
                    <li><strong>Burner clogs:</strong> Food debris blocks gas flow</li>
                </ul>

                <div class="warning-box">
                    <h4>⚠️ Gas Safety Warning</h4>
                    <p>If you smell gas or suspect a leak, do NOT use the oven. Turn off gas supply, ventilate your home, and call a professional immediately. Never attempt DIY repairs on gas components.</p>
                </div>
            """,
            "diy": """
                <h2 id="diy-fixes">Safe DIY Troubleshooting</h2>

                <h3>Step 1: Basic Checks</h3>
                <ul>
                    <li>Verify oven is plugged in (electric) or gas supply is on</li>
                    <li>Check circuit breaker hasn't tripped</li>
                    <li>Ensure clock is set (some ovens won't heat without time set)</li>
                    <li>Clear any error codes by unplugging for 5 minutes</li>
                </ul>

                <h3>Step 2: Inspect Heating Elements (Electric)</h3>
                <ul>
                    <li>Look for visible damage - breaks, blisters, or burn spots</li>
                    <li>Turn on bake - element should glow red evenly</li>
                    <li>Check broil element the same way</li>
                </ul>

                <h3>Step 3: Test Oven Temperature</h3>
                <ol>
                    <li>Place oven thermometer in center rack</li>
                    <li>Set oven to 350°F and preheat 30 minutes</li>
                    <li>Compare thermometer reading to set temperature</li>
                    <li>Difference over 25°F indicates calibration or sensor issue</li>
                </ol>

                <h3>Step 4: Check Door Seal</h3>
                <ul>
                    <li>Inspect rubber gasket around door for cracks or gaps</li>
                    <li>With oven hot, feel for heat escaping around door</li>
                    <li>Replace seal if damaged (usually DIY-friendly)</li>
                </ul>

                <div class="tip-box">
                    <strong>💡 Self-Clean Caution:</strong> Self-cleaning cycles reach 800-900°F and can damage electronic components in older ovens. Use sparingly and never run when you'll be away from home.
                </div>
            """,
            "costs": """
                <h2 id="repair-costs">Oven Repair Costs in Toronto</h2>

                <table>
                    <thead>
                        <tr>
                            <th>Repair Type</th>
                            <th>Cost Range</th>
                            <th>Time Required</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Diagnostic Service</td>
                            <td>$95 (waived with repair)</td>
                            <td>30-45 minutes</td>
                        </tr>
                        <tr>
                            <td>Bake Element</td>
                            <td>$150-$220</td>
                            <td>30-45 minutes</td>
                        </tr>
                        <tr>
                            <td>Broil Element</td>
                            <td>$140-$200</td>
                            <td>30-45 minutes</td>
                        </tr>
                        <tr>
                            <td>Gas Igniter</td>
                            <td>$180-$260</td>
                            <td>45-75 minutes</td>
                        </tr>
                        <tr>
                            <td>Temperature Sensor</td>
                            <td>$130-$190</td>
                            <td>30-45 minutes</td>
                        </tr>
                        <tr>
                            <td>Door Seal</td>
                            <td>$120-$180</td>
                            <td>30-45 minutes</td>
                        </tr>
                        <tr>
                            <td>Control Board</td>
                            <td>$280-$450</td>
                            <td>60-90 minutes</td>
                        </tr>
                    </tbody>
                </table>
            """
        },
    }

    # Get content for the appliance type, or use generic
    content = content_templates.get(appliance, content_templates["dishwasher"])

    return content


def generate_faq_section(post):
    """Generate FAQ section based on post topic"""
    keyword = post["keyword"]
    appliance = post["appliance"]
    brand = post.get("brand", "")
    brand_text = f"{brand} " if brand else ""

    faqs = [
        {
            "q": f"How much does {brand_text}{appliance} repair cost in Toronto?",
            "a": f"Professional {brand_text}{appliance} repair in Toronto typically costs between $150-$400 depending on the issue. Our diagnostic fee is $95 but is waived when you proceed with the repair. All repairs include our comprehensive 90-day warranty on parts and labor."
        },
        {
            "q": f"Can I fix {keyword} myself?",
            "a": f"Some {keyword} issues can be resolved with basic troubleshooting like cleaning filters, checking power connections, or resetting the appliance. However, repairs involving electrical components, gas connections, or sealed systems should always be handled by certified professionals for safety reasons."
        },
        {
            "q": f"Do you offer same-day {brand_text}{appliance} repair?",
            "a": f"Yes! Nika Appliance Repair offers same-day service 7 days a week across Toronto and the GTA. We stock common parts on our service vehicles, allowing us to complete most repairs on the first visit. Call before 2 PM for same-day availability."
        },
        {
            "q": f"When should I replace vs repair my {brand_text}{appliance}?",
            "a": f"Generally, repair makes sense if your {appliance} is under 8 years old and the repair cost is less than 50% of replacement cost. For older appliances or those with multiple failing components, replacement may be more economical. Our technicians provide honest assessments to help you make the best decision."
        },
        {
            "q": "What areas do you serve?",
            "a": "We serve all of Toronto and the Greater Toronto Area including Mississauga, Brampton, Markham, Vaughan, Richmond Hill, Scarborough, Etobicoke, North York, and surrounding communities. Same-day service is available throughout our service area."
        },
    ]

    faq_html = """
                <h2 id="faq">Frequently Asked Questions</h2>

                <div class="faq-section">
    """

    for faq in faqs:
        faq_html += f"""
                    <div class="faq-item">
                        <h3>{faq['q']}</h3>
                        <p>{faq['a']}</p>
                    </div>
    """

    faq_html += """
                </div>
    """

    return faq_html


def generate_blog_post(post, publish_date):
    """Generate complete blog post HTML using BMAD template"""

    content = get_content_for_post(post)
    faq_section = generate_faq_section(post)

    brand = post.get("brand", "")
    brand_text = f"{brand} " if brand else ""

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{post["title"]} - Nika Appliance Repair</title>
    <meta name="description" content="Expert {post["keyword"]} repair in Toronto. Professional troubleshooting guide with step-by-step solutions. Same-day service available. Call (437) 747-6737.">
    <meta name="keywords" content="{post["keyword"]}, toronto {post["appliance"]} repair, {post["appliance"]} troubleshooting, appliance repair toronto">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;500;600;700&family=Rubik:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="../css/blog-premium.css">
    <link rel="stylesheet" href="../css/ai-seo-styles.css">
    <link rel="stylesheet" href="../css/header-optimized.css">
    <link rel="canonical" href="https://nikaappliancerepair.com/blog/{post["category"]}/{post["slug"]}">
    <meta property="og:title" content="{post["title"]}">
    <meta property="og:description" content="Expert {post["keyword"]} repair guide for Toronto homeowners">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://nikaappliancerepair.com/blog/{post["category"]}/{post["slug"]}">
    <meta property="article:published_time" content="{publish_date}">
    <meta property="article:modified_time" content="{publish_date}">

    <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{post["title"]}",
  "author": {{
    "@type": "Organization",
    "name": "Nika Appliance Repair",
    "url": "https://nikaappliancerepair.com"
  }},
  "publisher": {{
    "@type": "LocalBusiness",
    "name": "Nika Appliance Repair",
    "telephone": "+1-437-747-6737",
    "address": {{
      "@type": "PostalAddress",
      "addressLocality": "Toronto",
      "addressRegion": "ON",
      "addressCountry": "CA"
    }}
  }},
  "datePublished": "{publish_date}",
  "dateModified": "{publish_date}",
  "mainEntityOfPage": {{
    "@type": "WebPage",
    "@id": "https://nikaappliancerepair.com/blog/{post["category"]}/{post["slug"]}"
  }}
}}
    </script>
    <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://nikaappliancerepair.com"}},
    {{"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://nikaappliancerepair.com/blog"}},
    {{"@type": "ListItem", "position": 3, "name": "{post["category"].title()}", "item": "https://nikaappliancerepair.com/blog/{post["category"]}"}}
  ]
}}
    </script>
    <!-- Footer Styles -->
    <style>
        .seo-footer-premium {{
            background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
            color: white;
            padding: 3rem 0 1.5rem;
            margin-top: 4rem;
        }}
        .seo-footer-premium .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 2rem;
        }}
        .footer-trust-badges {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
            padding-bottom: 2rem;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        .trust-badge-item {{
            display: flex;
            align-items: center;
            gap: 1rem;
        }}
        .badge-icon {{ font-size: 2rem; }}
        .badge-text strong {{ display: block; font-size: 1rem; margin-bottom: 0.25rem; }}
        .badge-text span {{ font-size: 0.875rem; opacity: 0.8; }}
        .footer-main-content {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }}
        .footer-heading {{ font-size: 1.125rem; margin-bottom: 1rem; font-weight: 600; }}
        .footer-links {{ list-style: none; padding: 0; margin: 0; }}
        .footer-links li {{ margin-bottom: 0.5rem; }}
        .footer-links a {{ color: rgba(255,255,255,0.8); text-decoration: none; font-size: 0.95rem; transition: color 0.2s; }}
        .footer-links a:hover {{ color: white; }}
        .footer-contact-box {{ margin-bottom: 1.5rem; }}
        .contact-item {{ margin-bottom: 1rem; font-size: 0.95rem; line-height: 1.6; }}
        .contact-link {{ color: #93c5fd; text-decoration: none; }}
        .contact-link:hover {{ color: #60a5fa; text-decoration: underline; }}
        .footer-cta-button {{
            display: inline-flex;
            align-items: center;
            gap: 0.75rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem 2rem;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            transition: transform 0.2s;
        }}
        .footer-cta-button:hover {{ transform: translateY(-2px); }}
        .footer-bottom {{ margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.1); }}
        .footer-bottom-content {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }}
        .copyright {{ font-size: 0.875rem; opacity: 0.8; margin: 0; }}
        .separator {{ margin: 0 0.5rem; }}
        .footer-tagline {{ font-size: 0.875rem; opacity: 0.8; }}
        @media (max-width: 768px) {{
            .footer-trust-badges {{ grid-template-columns: 1fr; }}
            .footer-main-content {{ grid-template-columns: 1fr; }}
            .footer-bottom-content {{ flex-direction: column; text-align: center; }}
        }}
    </style>
</head>
<body>
    <div class="reading-progress" id="progressBar"></div>
    <header class="site-header">
        <div class="header-container">
            <div class="header-logo"><a href="/">Nika Appliance Repair</a></div>
            <nav class="header-nav" id="mainNav">
                <ul class="nav-list">
                    <li><a href="/" class="nav-link">Home</a></li>
                    <li><a href="/services" class="nav-link">Services</a></li>
                    <li><a href="/locations" class="nav-link">Locations</a></li>
                    <li><a href="/about" class="nav-link">About</a></li>
                    <li><a href="/blog" class="nav-link">Blog</a></li>
                </ul>
            </nav>
            <div class="header-trust">
                <div class="trust-stars">⭐⭐⭐⭐⭐</div>
                <div class="trust-rating">4.9/5</div>
                <div class="trust-reviews">5,200+ Reviews</div>
            </div>
            <div class="header-cta">
                <a href="tel:4377476737" class="cta-phone"><i class="fas fa-phone"></i> (437) 747-6737</a>
                <a href="/book" class="cta-book"><i class="fas fa-calendar-check"></i> Book Now</a>
            </div>
            <button class="mobile-menu-btn" aria-label="Menu" aria-expanded="false">
                <span class="menu-bar"></span><span class="menu-bar"></span><span class="menu-bar"></span>
            </button>
        </div>
    </header>
    <div class="blog-wrapper">
        <main class="blog-main">
            <header class="blog-header">
                <div class="blog-meta-top">
                    <span class="blog-category"><i class="fas fa-wrench"></i> {post["category"].title()}</span>
                    <span class="reading-time"><i class="far fa-clock"></i> 10 min read</span>
                </div>
                <h1 class="blog-title">{post["title"]}</h1>
                <div class="blog-meta">
                    <span class="meta-item"><i class="far fa-calendar"></i> {datetime.strptime(publish_date, '%Y-%m-%d').strftime('%B %d, %Y')}</span>
                    <span class="meta-item"><i class="far fa-user"></i> Expert Team</span>
                </div>
            </header>
            <div class="social-share">
                <a href="#" class="share-btn facebook" aria-label="Share on Facebook"><i class="fab fa-facebook-f"></i></a>
                <a href="#" class="share-btn twitter" aria-label="Share on Twitter"><i class="fab fa-twitter"></i></a>
                <a href="#" class="share-btn linkedin" aria-label="Share on LinkedIn"><i class="fab fa-linkedin-in"></i></a>
                <a href="#" class="share-btn email" aria-label="Share via Email"><i class="far fa-envelope"></i></a>
            </div>

            <article class="blog-content">
                {content["intro"]}

                {content["problems"]}

                {content["diy"]}

                <div class="cta-box">
                    <h3>Need Professional Help with {brand_text}{post["appliance"].title()} Repair?</h3>
                    <p>Our certified technicians are available for same-day service across Toronto and the GTA!</p>
                    <a href="tel:4377476737" class="btn">
                        <i class="fas fa-phone"></i> Call (437) 747-6737
                    </a>
                </div>

                {content["costs"]}

                <h2 id="when-to-call">When to Call a Professional</h2>

                <p>While some {post["appliance"]} issues can be resolved with DIY troubleshooting, certain situations require professional expertise:</p>

                <ul>
                    <li><strong>Electrical problems:</strong> Any repair involving wiring, control boards, or high-voltage components</li>
                    <li><strong>Gas appliance issues:</strong> All repairs on gas appliances should be done by licensed technicians</li>
                    <li><strong>Refrigerant systems:</strong> Sealed system repairs require EPA certification</li>
                    <li><strong>Persistent problems:</strong> Issues that return after DIY attempts indicate deeper problems</li>
                    <li><strong>Under warranty:</strong> DIY repairs can void manufacturer coverage</li>
                    <li><strong>Water damage risk:</strong> Leak repairs need proper diagnosis to prevent flood damage</li>
                </ul>

                <h2 id="why-choose-us">Why Choose Nika Appliance Repair</h2>

                <ul>
                    <li><strong>Same-Day Service:</strong> We understand appliance emergencies can't wait</li>
                    <li><strong>Certified Technicians:</strong> Factory-trained on all major brands</li>
                    <li><strong>Transparent Pricing:</strong> Upfront quotes with no hidden fees</li>
                    <li><strong>90-Day Warranty:</strong> All repairs backed by comprehensive warranty</li>
                    <li><strong>Parts in Stock:</strong> Common parts on trucks for first-visit repairs</li>
                    <li><strong>Serving All Toronto:</strong> From Downtown to North York, Scarborough to Etobicoke</li>
                </ul>

                <h2 id="service-areas">Areas We Serve</h2>

                <p>We provide expert {brand_text}{post["appliance"]} repair throughout the Greater Toronto Area:</p>

                <ul>
                    <li>Downtown Toronto</li>
                    <li>North York</li>
                    <li>Scarborough</li>
                    <li>Etobicoke</li>
                    <li>Mississauga</li>
                    <li>Brampton</li>
                    <li>Vaughan</li>
                    <li>Richmond Hill</li>
                    <li>Markham</li>
                    <li>Oakville</li>
                </ul>

                {faq_section}

                <h2 id="conclusion">Get Your {brand_text}{post["appliance"].title()} Fixed Today</h2>

                <p>Don't let {post["keyword"]} problems disrupt your daily routine. Whether you need a quick diagnosis or a complete repair, Nika Appliance Repair is here to help. Our experienced technicians provide honest assessments, transparent pricing, and quality repairs backed by our 90-day warranty.</p>

                <div class="cta-box">
                    <h3>Schedule Your Repair Today</h3>
                    <p>Same-day service available. Call now for expert {brand_text}{post["appliance"]} repair!</p>
                    <a href="tel:4377476737" class="btn">
                        <i class="fas fa-phone"></i> Call (437) 747-6737
                    </a>
                </div>
            </article>
        </main>
        <aside class="blog-sidebar">
            <div class="toc-widget">
                <h3>Table of Contents</h3>
                <ul class="toc-list">
                    <li><a href="#common-problems">Common Problems</a></li>
                    <li><a href="#diy-fixes">DIY Troubleshooting</a></li>
                    <li><a href="#repair-costs">Repair Costs</a></li>
                    <li><a href="#when-to-call">When to Call a Pro</a></li>
                    <li><a href="#why-choose-us">Why Choose Us</a></li>
                    <li><a href="#service-areas">Service Areas</a></li>
                    <li><a href="#faq">FAQ</a></li>
                    <li><a href="#conclusion">Conclusion</a></li>
                </ul>
            </div>
            <div class="cta-widget">
                <h3>Need Help Now?</h3>
                <p>Same-day service available!</p>
                <a href="tel:4377476737" class="btn-sidebar">
                    <i class="fas fa-phone"></i> (437) 747-6737
                </a>
            </div>
        </aside>
    </div>
    <footer class="seo-footer-premium">
        <div class="container">
            <div class="footer-trust-badges">
                <div class="trust-badge-item"><div class="badge-icon">⭐</div><div class="badge-text"><strong>4.9/5 Rating</strong><span>5,200+ Reviews</span></div></div>
                <div class="trust-badge-item"><div class="badge-icon">🏆</div><div class="badge-text"><strong>Licensed & Insured</strong><span>Since 2017</span></div></div>
                <div class="trust-badge-item"><div class="badge-icon">🛡️</div><div class="badge-text"><strong>90-Day Warranty</strong><span>Parts & Labor</span></div></div>
                <div class="trust-badge-item"><div class="badge-icon">⚡</div><div class="badge-text"><strong>Same-Day Service</strong><span>7 Days a Week</span></div></div>
            </div>
            <div class="footer-main-content">
                <div class="footer-column"><h4 class="footer-heading">Our Services</h4><ul class="footer-links">
                    <li><a href="/services/refrigerator-repair">Refrigerator Repair</a></li>
                    <li><a href="/services/dishwasher-repair">Dishwasher Repair</a></li>
                    <li><a href="/services/washer-repair">Washer Repair</a></li>
                    <li><a href="/services/dryer-repair">Dryer Repair</a></li>
                    <li><a href="/services/oven-repair">Oven Repair</a></li>
                </ul></div>
                <div class="footer-column"><h4 class="footer-heading">Service Areas</h4><ul class="footer-links">
                    <li><a href="/locations/mississauga">Mississauga</a></li>
                    <li><a href="/locations/brampton">Brampton</a></li>
                    <li><a href="/locations/markham">Markham</a></li>
                    <li><a href="/locations/vaughan">Vaughan</a></li>
                    <li><a href="/locations/oakville">Oakville</a></li>
                </ul></div>
                <div class="footer-column"><h4 class="footer-heading">Company</h4><ul class="footer-links">
                    <li><a href="/about">About Us</a></li>
                    <li><a href="/reviews">Customer Reviews</a></li>
                    <li><a href="/faq">FAQ</a></li>
                    <li><a href="/book">Book Online</a></li>
                    <li><a href="/privacy">Privacy Policy</a></li>
                </ul></div>
                <div class="footer-column footer-column-contact"><h4 class="footer-heading">Contact Us</h4><div class="footer-contact-box">
                    <p class="contact-item"><i class="fas fa-phone"></i><a href="tel:4377476737" class="contact-link">(437) 747-6737</a></p>
                    <p class="contact-item"><i class="far fa-envelope"></i><a href="mailto:care@niappliancerepair.ca" class="contact-link">care@niappliancerepair.ca</a></p>
                    <p class="contact-item"><i class="fas fa-map-marker-alt"></i><span>Serving Toronto & GTA</span></p>
                </div>
                <a href="tel:4377476737" class="footer-cta-button"><i class="fas fa-phone"></i>Call for Same-Day Service</a></div>
            </div>
            <div class="footer-bottom"><div class="footer-bottom-content">
                <p class="copyright">© 2025 Nika Appliance Repair. All Rights Reserved.<span class="separator">|</span>Licensed & Insured</p>
                <span class="footer-tagline">Trusted by 5,200+ Happy Customers</span>
            </div></div>
        </div>
    </footer>
    <script>
        window.addEventListener('scroll', function() {{
            const progressBar = document.getElementById('progressBar');
            const windowHeight = window.innerHeight;
            const documentHeight = document.documentElement.scrollHeight - windowHeight;
            const scrolled = (window.scrollY / documentHeight) * 100;
            progressBar.style.width = scrolled + '%';
        }});
        const menuBtn = document.querySelector('.mobile-menu-btn');
        const mainNav = document.getElementById('mainNav');
        if (menuBtn) {{
            menuBtn.addEventListener('click', function() {{
                const isOpen = this.getAttribute('aria-expanded') === 'true';
                this.setAttribute('aria-expanded', !isOpen);
                mainNav.classList.toggle('menu-open');
            }});
        }}
    </script>
    <script src="/blog/js/responsive-tables.js"></script>
    <script src="/blog/js/faq-accordion.js"></script>
    <script src="/blog/js/share-buttons.js"></script>
</body>
</html>'''

    return html


def main():
    """Generate all 20 blog posts"""
    base_dir = Path(__file__).parent.parent.parent.parent
    drafts_dir = base_dir / "blog" / "_drafts"

    # Create drafts directory
    drafts_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("BMAD BLOG POST GENERATOR")
    print("Generating 20 SEO-optimized posts from keyword gap analysis")
    print("=" * 70)
    print(f"\nOutput: {drafts_dir}")
    print(f"Posts: {len(BLOG_POSTS)}\n")

    # Start date for posts (tomorrow)
    start_date = datetime.now() + timedelta(days=1)

    for i, post in enumerate(BLOG_POSTS):
        # Each post gets published one day apart
        publish_date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')

        filename = f"{post['slug']}.html"
        filepath = drafts_dir / filename

        html_content = generate_blog_post(post, publish_date)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"[{i+1:02d}/{len(BLOG_POSTS)}] {filename}")
        print(f"         Keyword: {post['keyword']} (vol: {post['volume']})")
        print(f"         Publish: {publish_date}")

    print(f"\n{'=' * 70}")
    print(f"[SUCCESS] Generated {len(BLOG_POSTS)} blog posts")
    print(f"Posts saved to: {drafts_dir}")
    print("=" * 70)

    # Create summary file
    summary_path = drafts_dir / "_post_schedule.txt"
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("BLOG POST PUBLISHING SCHEDULE\n")
        f.write("=" * 50 + "\n\n")
        for i, post in enumerate(BLOG_POSTS):
            publish_date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
            f.write(f"{publish_date}: {post['title']}\n")
            f.write(f"           URL: /blog/{post['category']}/{post['slug']}\n")
            f.write(f"           Keyword: {post['keyword']} ({post['volume']} vol)\n\n")

    print(f"\nSchedule saved to: {summary_path}")


if __name__ == "__main__":
    main()
