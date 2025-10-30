#!/usr/bin/env python3
"""
Script to apply internal linking strategy to 44 troubleshooting posts.
Based on INTERNAL_LINKING_STRATEGY.md
"""

import os
import re
from pathlib import Path

# Define the linking map from INTERNAL_LINKING_STRATEGY.md
LINKING_MAP = {
    # Refrigerator Group
    "refrigerator-not-cooling-toronto.html": [
        ("ice-maker-not-working.html", "Refrigerator Ice Maker Not Working: Complete Repair Guide", "Troubleshooting"),
        ("refrigerator-door-seal-replacement.html", "Refrigerator Door Seal Replacement: Save $150+ DIY Guide", "Troubleshooting"),
        ("ice-maker-repair.html", "Ice Maker Repair: Complete Troubleshooting Guide", "Troubleshooting"),
        ("refrigerator-repair-toronto.html", "Refrigerator Repair Toronto: Expert Service & Costs", "Troubleshooting"),
    ],
    "ice-maker-not-working.html": [
        ("refrigerator-not-cooling-toronto.html", "Refrigerator Not Cooling: Toronto Troubleshooting Guide", "Troubleshooting"),
        ("ice-maker-repair.html", "Ice Maker Repair: Complete Troubleshooting Guide", "Troubleshooting"),
        ("../guides/refrigerator-repair-vs-replace.html", "Refrigerator Repair vs Replace: Complete Decision Guide", "Guides"),
        ("emergency-appliance-repair-24-7.html", "Emergency Appliance Repair 24/7: Immediate Help Available", "Troubleshooting"),
    ],
    "refrigerator-door-seal-replacement.html": [
        ("refrigerator-not-cooling-toronto.html", "Refrigerator Not Cooling: Toronto Troubleshooting Guide", "Troubleshooting"),
        ("ice-maker-not-working.html", "Refrigerator Ice Maker Not Working: Complete Repair Guide", "Troubleshooting"),
        ("best-appliance-repair-near-me.html", "Best Appliance Repair Near Me: Find Local Trusted Experts", "Troubleshooting"),
        ("refrigerator-repair-toronto.html", "Refrigerator Repair Toronto: Expert Service & Costs", "Troubleshooting"),
    ],
    "ice-maker-repair.html": [
        ("ice-maker-not-working.html", "Ice Maker Troubleshooting: Common Problems & Solutions", "Troubleshooting"),
        ("refrigerator-not-cooling-toronto.html", "Refrigerator Not Cooling: Toronto Troubleshooting Guide", "Troubleshooting"),
        ("same-day-appliance-repair.html", "Same-Day Appliance Repair: Quick Emergency Service", "Troubleshooting"),
        ("../guides/refrigerator-repair-vs-replace.html", "Refrigerator Repair vs Replace: Decision Guide", "Guides"),
    ],
    "refrigerator-repair-toronto.html": [
        ("refrigerator-not-cooling-toronto.html", "Refrigerator Not Cooling: Toronto Troubleshooting Guide", "Troubleshooting"),
        ("ice-maker-repair.html", "Ice Maker Repair: Complete Guide", "Troubleshooting"),
        ("../guides/appliance-repair-cabbagetown.html", "Appliance Repair Cabbagetown: Local Service", "Guides"),
        ("emergency-appliance-repair-24-7.html", "Emergency Appliance Repair 24/7: Now Available", "Troubleshooting"),
    ],

    # Washer/Dryer Group
    "washer-wont-drain.html": [
        ("washing-machine-leaking.html", "Washing Machine Leaking: Causes & Solutions", "Troubleshooting"),
        ("washing-machine-repair-complete-guide.html", "Washing Machine Repair: Complete DIY Guide", "Troubleshooting"),
        ("dryer-not-heating.html", "Dryer Not Heating: Troubleshooting & Repair", "Troubleshooting"),
        ("same-day-appliance-repair.html", "Same-Day Appliance Repair: Quick Help", "Troubleshooting"),
    ],
    "washing-machine-leaking.html": [
        ("washer-wont-drain.html", "Washer Won't Drain: Complete Troubleshooting", "Troubleshooting"),
        ("washing-machine-repair-complete-guide.html", "Washing Machine Repair: Complete Guide", "Troubleshooting"),
        ("dishwasher-not-cleaning.html", "Dishwasher Not Cleaning: Solutions & Fixes", "Troubleshooting"),
        ("../guides/appliance-repair-king-west.html", "Appliance Repair King West: Local Expert Service", "Guides"),
    ],
    "dryer-not-heating.html": [
        ("dryer-making-noise.html", "Dryer Making Noise: Troubleshooting Guide", "Troubleshooting"),
        ("dryer-repair-toronto.html", "Dryer Repair Toronto: Expert Service", "Troubleshooting"),
        ("washer-wont-drain.html", "Washer Won't Drain: Causes & Fixes", "Troubleshooting"),
        ("emergency-appliance-repair-24-7.html", "Emergency Appliance Repair 24/7 Service", "Troubleshooting"),
    ],
    "dryer-making-noise.html": [
        ("dryer-not-heating.html", "Dryer Not Heating: Complete Troubleshooting", "Troubleshooting"),
        ("dryer-repair-toronto.html", "Dryer Repair Toronto: Professional Service", "Troubleshooting"),
        ("washing-machine-leaking.html", "Washing Machine Leaking: Repair Guide", "Troubleshooting"),
        ("best-appliance-repair-near-me.html", "Best Appliance Repair Near Me: Find Experts", "Troubleshooting"),
    ],
    "dryer-repair-toronto.html": [
        ("dryer-not-heating.html", "Dryer Not Heating: Troubleshooting & Fixes", "Troubleshooting"),
        ("dryer-making-noise.html", "Dryer Making Noise: Causes & Solutions", "Troubleshooting"),
        ("../guides/appliance-repair-cabbagetown.html", "Appliance Repair Cabbagetown: Local Service", "Guides"),
        ("same-day-appliance-repair.html", "Same-Day Dryer Repair Service", "Troubleshooting"),
    ],
    "washing-machine-repair-complete-guide.html": [
        ("washer-wont-drain.html", "Washer Won't Drain: Troubleshooting", "Troubleshooting"),
        ("washing-machine-leaking.html", "Washing Machine Leaking: Guide", "Troubleshooting"),
        ("dryer-repair-toronto.html", "Dryer Repair Toronto: Service", "Troubleshooting"),
        ("../guides/appliance-repair-distillery-district.html", "Appliance Repair Distillery: Local Expert", "Guides"),
    ],

    # Oven/Stove Group
    "oven-not-heating.html": [
        ("oven-door-wont-close.html", "Oven Door Won't Close: Easy Fix", "Troubleshooting"),
        ("stove-burner-not-working.html", "Stove Burner Not Working: Troubleshooting", "Troubleshooting"),
        ("oven-repair-toronto.html", "Oven Repair Toronto: Expert Service", "Troubleshooting"),
        ("emergency-appliance-repair-24-7.html", "Emergency Appliance Repair Available", "Troubleshooting"),
    ],
    "oven-door-wont-close.html": [
        ("oven-not-heating.html", "Oven Not Heating: Troubleshooting Guide", "Troubleshooting"),
        ("stove-burner-not-working.html", "Stove Burner Not Working: Solutions", "Troubleshooting"),
        ("../guides/appliance-repair-queen-west.html", "Appliance Repair Queen West: Local Service", "Guides"),
        ("best-appliance-repair-near-me.html", "Best Appliance Repair Near Me", "Troubleshooting"),
    ],
    "stove-burner-not-working.html": [
        ("oven-not-heating.html", "Oven Not Heating: Complete Guide", "Troubleshooting"),
        ("oven-door-wont-close.html", "Oven Door Issues: How to Fix", "Troubleshooting"),
        ("stove-repair-toronto.html", "Stove Repair Toronto: Professional Service", "Troubleshooting"),
        ("same-day-appliance-repair.html", "Same-Day Stove Repair", "Troubleshooting"),
    ],
    "oven-repair-toronto.html": [
        ("oven-not-heating.html", "Oven Not Heating: Troubleshooting", "Troubleshooting"),
        ("stove-burner-not-working.html", "Stove Burner Not Working: Fix", "Troubleshooting"),
        ("../guides/appliance-repair-yorkville.html", "Appliance Repair Yorkville: Local Expert", "Guides"),
        ("emergency-appliance-repair-24-7.html", "Emergency Oven Repair 24/7", "Troubleshooting"),
    ],
    "stove-repair-toronto.html": [
        ("oven-not-heating.html", "Oven Not Heating: Complete Guide", "Troubleshooting"),
        ("stove-burner-not-working.html", "Stove Burner Not Working: Solutions", "Troubleshooting"),
        ("oven-repair-toronto.html", "Oven Repair Toronto: Service", "Troubleshooting"),
        ("../guides/appliance-repair-cabbagetown.html", "Appliance Repair Cabbagetown: Local", "Guides"),
    ],

    # Microwave/Disposal Group
    "microwave-not-heating.html": [
        ("microwave-repair-toronto.html", "Microwave Repair Toronto: Expert Service", "Troubleshooting"),
        ("garbage-disposal-jammed.html", "Garbage Disposal Jammed: How to Fix", "Troubleshooting"),
        ("garbage-disposal-repair.html", "Garbage Disposal Repair: Complete Guide", "Troubleshooting"),
        ("same-day-appliance-repair.html", "Same-Day Appliance Repair Service", "Troubleshooting"),
    ],
    "microwave-repair-toronto.html": [
        ("microwave-not-heating.html", "Microwave Not Heating: Troubleshooting", "Troubleshooting"),
        ("garbage-disposal-repair.html", "Garbage Disposal Repair: Guide", "Troubleshooting"),
        ("../guides/appliance-repair-distillery-district.html", "Appliance Repair Distillery District", "Guides"),
        ("best-appliance-repair-near-me.html", "Best Appliance Repair Near Me", "Troubleshooting"),
    ],
    "garbage-disposal-jammed.html": [
        ("garbage-disposal-repair.html", "Garbage Disposal Repair: Complete Guide", "Troubleshooting"),
        ("microwave-not-heating.html", "Microwave Not Heating: Solutions", "Troubleshooting"),
        ("../guides/appliance-repair-king-west.html", "Appliance Repair King West: Local", "Guides"),
        ("emergency-appliance-repair-24-7.html", "Emergency Disposal Repair 24/7", "Troubleshooting"),
    ],
    "garbage-disposal-repair.html": [
        ("garbage-disposal-jammed.html", "Garbage Disposal Jammed: How to Fix", "Troubleshooting"),
        ("microwave-repair-toronto.html", "Microwave Repair Toronto: Service", "Troubleshooting"),
        ("../guides/appliance-repair-peterborough.html", "Appliance Repair Peterborough: Expert", "Guides"),
        ("same-day-appliance-repair.html", "Same-Day Appliance Repair Available", "Troubleshooting"),
    ],

    # Freezer Group
    "freezer-not-freezing.html": [
        ("freezer-repair-guide.html", "Freezer Repair: Complete Troubleshooting Guide", "Troubleshooting"),
    ],
    "freezer-repair-guide.html": [
        ("freezer-not-freezing.html", "Freezer Not Freezing: Troubleshooting", "Troubleshooting"),
    ],

    # Dishwasher Group
    "dishwasher-not-cleaning.html": [
        ("dishwasher-repair-toronto.html", "Dishwasher Repair Toronto: Expert Service", "Troubleshooting"),
    ],
    "dishwasher-repair-toronto.html": [
        ("dishwasher-not-cleaning.html", "Dishwasher Not Cleaning: Solutions", "Troubleshooting"),
    ],

    # Location Group (Toronto Neighborhoods)
    "appliance-repair-cabbagetown.html": [
        ("../guides/appliance-repair-distillery-district.html", "Appliance Repair Distillery District", "Guides"),
        ("../guides/appliance-repair-king-west.html", "Appliance Repair King West", "Guides"),
        ("refrigerator-repair-toronto.html", "Refrigerator Repair Toronto: Expert", "Troubleshooting"),
        ("dryer-repair-toronto.html", "Dryer Repair Toronto: Service", "Troubleshooting"),
    ],
    "appliance-repair-distillery-district.html": [
        ("../guides/appliance-repair-cabbagetown.html", "Appliance Repair Cabbagetown", "Guides"),
        ("../guides/appliance-repair-queen-west.html", "Appliance Repair Queen West", "Guides"),
        ("oven-repair-toronto.html", "Oven Repair Toronto: Expert", "Troubleshooting"),
        ("same-day-appliance-repair.html", "Same-Day Service Available", "Troubleshooting"),
    ],
    "appliance-repair-king-west.html": [
        ("../guides/appliance-repair-cabbagetown.html", "Appliance Repair Cabbagetown", "Guides"),
        ("../guides/appliance-repair-yorkville.html", "Appliance Repair Yorkville", "Guides"),
        ("microwave-repair-toronto.html", "Microwave Repair Toronto: Service", "Troubleshooting"),
        ("best-appliance-repair-near-me.html", "Best Appliance Repair Near Me", "Troubleshooting"),
    ],
    "appliance-repair-queen-west.html": [
        ("../guides/appliance-repair-distillery-district.html", "Appliance Repair Distillery", "Guides"),
        ("../guides/appliance-repair-yorkville.html", "Appliance Repair Yorkville", "Guides"),
        ("refrigerator-repair-toronto.html", "Refrigerator Repair Toronto: Expert", "Troubleshooting"),
        ("emergency-appliance-repair-24-7.html", "Emergency Service 24/7", "Troubleshooting"),
    ],
    "appliance-repair-yorkville.html": [
        ("../guides/appliance-repair-king-west.html", "Appliance Repair King West", "Guides"),
        ("../guides/appliance-repair-cabbagetown.html", "Appliance Repair Cabbagetown", "Guides"),
        ("dishwasher-repair-toronto.html", "Dishwasher Repair Toronto: Service", "Troubleshooting"),
        ("same-day-appliance-repair.html", "Same-Day Service Available", "Troubleshooting"),
    ],

    # Regional Group
    "mobile-appliance-repair-whitehorse.html": [
        ("same-day-appliance-repair.html", "Same-Day Appliance Repair Service", "Troubleshooting"),
        ("emergency-appliance-repair-24-7.html", "Emergency Appliance Repair 24/7", "Troubleshooting"),
        ("../guides/appliance-repair-grande-prairie.html", "Appliance Repair Grande Prairie", "Guides"),
        ("best-appliance-repair-near-me.html", "Best Appliance Repair Near Me", "Troubleshooting"),
    ],
    "appliance-repair-grande-prairie.html": [
        ("mobile-appliance-repair-whitehorse.html", "Mobile Appliance Repair Whitehorse", "Troubleshooting"),
        ("../guides/appliance-repair-peterborough.html", "Appliance Repair Peterborough", "Guides"),
        ("same-day-appliance-repair.html", "Same-Day Service Available", "Troubleshooting"),
        ("emergency-appliance-repair-24-7.html", "Emergency Service 24/7", "Troubleshooting"),
    ],
    "appliance-repair-peterborough.html": [
        ("../guides/appliance-repair-grande-prairie.html", "Appliance Repair Grande Prairie", "Guides"),
        ("mobile-appliance-repair-whitehorse.html", "Mobile Appliance Repair Whitehorse", "Troubleshooting"),
        ("best-appliance-repair-near-me.html", "Best Appliance Repair Near Me", "Troubleshooting"),
        ("same-day-appliance-repair.html", "Same-Day Service Available", "Troubleshooting"),
    ],

    # Service Group
    "same-day-appliance-repair.html": [
        ("emergency-appliance-repair-24-7.html", "Emergency Appliance Repair 24/7", "Troubleshooting"),
        ("refrigerator-repair-toronto.html", "Refrigerator Repair Toronto", "Troubleshooting"),
        ("best-appliance-repair-near-me.html", "Best Appliance Repair Near Me", "Troubleshooting"),
    ],
    "emergency-appliance-repair-24-7.html": [
        ("same-day-appliance-repair.html", "Same-Day Appliance Repair Service", "Troubleshooting"),
        ("refrigerator-repair-toronto.html", "Refrigerator Repair Toronto", "Troubleshooting"),
        ("best-appliance-repair-near-me.html", "Best Appliance Repair Near Me", "Troubleshooting"),
    ],
    "refrigerator-repair-toronto.html": [
        ("same-day-appliance-repair.html", "Same-Day Service Available", "Troubleshooting"),
        ("emergency-appliance-repair-24-7.html", "Emergency Service 24/7", "Troubleshooting"),
        ("best-appliance-repair-near-me.html", "Best Appliance Repair Near Me", "Troubleshooting"),
    ],
    "best-appliance-repair-near-me.html": [
        ("same-day-appliance-repair.html", "Same-Day Appliance Repair", "Troubleshooting"),
        ("emergency-appliance-repair-24-7.html", "Emergency Appliance Repair 24/7", "Troubleshooting"),
        ("refrigerator-repair-toronto.html", "Refrigerator Repair Toronto", "Troubleshooting"),
    ],

    # Other Posts (Not yet mapped, but exist)
    "ice-maker-repair.html": [],
    "water-heater-repair-toronto.html": [],
    "samsung-appliance-repair.html": [],
    "whirlpool-customer-service-repair.html": [],
    "lg-appliance-repair-service.html": [],
}

def generate_related_posts_html(links):
    """Generate HTML for related posts section."""
    if not links:
        return ""

    html = '            <!-- Related Posts -->\n'
    html += '            <div class="related-widget">\n'
    html += '                <h3>Related Articles</h3>\n'

    for href, title, category in links:
        html += f'                <div class="related-post">\n'
        html += f'                    <a href="{href}">{title}</a>\n'
        html += f'                    <div class="related-post-meta">\n'
        html += f'                        <i class="far fa-folder"></i> {category}\n'
        html += f'                    </div>\n'
        html += f'                </div>\n'

    html += '            </div>\n'
    return html

def update_post_file(filepath, links):
    """Update a post file with internal links."""
    if not links:
        return False

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Generate new related posts HTML
        new_related_html = generate_related_posts_html(links)

        # Pattern to find and replace the related posts section
        pattern = r'            <!-- Related Posts -->.*?</div>'

        if re.search(pattern, content, re.DOTALL):
            # Replace existing related posts section
            new_content = re.sub(
                pattern,
                new_related_html.rstrip(),
                content,
                count=1,
                flags=re.DOTALL
            )
        else:
            # If no related posts section, add before the emergency contact box
            emergency_pattern = r'            <!-- Emergency Contact Box -->'
            new_content = re.sub(
                emergency_pattern,
                new_related_html + '\n            <!-- Emergency Contact Box -->',
                content
            )

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True
    except Exception as e:
        print(f"Error updating {filepath}: {e}")
        return False

def main():
    """Main function to process all posts."""
    blog_dir = Path("C:\\NikaApplianceRepair\\blog\\troubleshooting")

    updated_count = 0
    skipped_count = 0

    for filename, links in LINKING_MAP.items():
        filepath = blog_dir / filename

        if not filepath.exists():
            print(f"[SKIP] Not found: {filename}")
            skipped_count += 1
            continue

        if update_post_file(str(filepath), links):
            print(f"[OK] Updated: {filename}")
            updated_count += 1
        else:
            print(f"[FAIL] Error: {filename}")

    print(f"\nSummary:")
    print(f"   Updated: {updated_count}")
    print(f"   Skipped: {skipped_count}")
    print(f"   Total: {updated_count + skipped_count}")

if __name__ == "__main__":
    main()
