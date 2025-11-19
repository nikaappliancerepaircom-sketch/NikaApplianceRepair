#!/usr/bin/env python3
"""
Categorize blog posts by appliance type to plan stock images
"""

import os
from pathlib import Path
from collections import defaultdict

# Posts missing images (from parallel agent report)
posts_without_images = [
    # Guides (11)
    "blog/guides/bosch-dishwasher-repair.html",
    "blog/guides/electrolux-appliance-repair.html",
    "blog/guides/frigidaire-refrigerator-repair.html",
    "blog/guides/ge-appliance-repair-toronto.html",
    "blog/guides/maytag-washer-dryer-repair.html",
    "blog/guides/refrigerator-repair-vs-replace.html",
    "blog/guides/should-you-repair-oven.html",
    "blog/guides/washing-machine-repair-vs-replace.html",
    "blog/guides/when-to-replace-dryer.html",
    "blog/guides/dishwasher-repair-vs-replace-toronto.html",
    "blog/guides/oven-temperature-calibration-guide.html",

    # Maintenance (8)
    "blog/maintenance/dishwasher-maintenance-hard-water.html",
    "blog/maintenance/dryer-vent-cleaning-fire-prevention.html",
    "blog/maintenance/how-to-avoid-oven-repairs.html",
    "blog/maintenance/how-to-extend-washer-life.html",
    "blog/maintenance/how-to-maintain-refrigerator.html",
    "blog/maintenance/how-to-prevent-dryer-fires.html",
    "blog/maintenance/microwave-door-seal-replacement-guide.html",
    "blog/maintenance/range-hood-filter-cleaning-maintenance.html",

    # Troubleshooting (48)
    "blog/troubleshooting/appliance-repair-cabbagetown.html",
    "blog/troubleshooting/appliance-repair-distillery-district.html",
    "blog/troubleshooting/appliance-repair-grande-prairie.html",
    "blog/troubleshooting/appliance-repair-king-west.html",
    "blog/troubleshooting/appliance-repair-peterborough.html",
    "blog/troubleshooting/appliance-repair-queen-west.html",
    "blog/troubleshooting/best-appliance-repair-near-me.html",
    "blog/troubleshooting/clothes-dryer-fire-hazard-prevention.html",
    "blog/troubleshooting/dishwasher-leaving-food-spots.html",
    "blog/troubleshooting/dishwasher-not-cleaning.html",
    "blog/troubleshooting/dishwasher-repair-toronto.html",
    "blog/troubleshooting/dishwasher-spray-arm-not-rotating-repair.html",
    "blog/troubleshooting/dishwasher-water-not-draining-completely.html",
    "blog/troubleshooting/dryer-making-noise.html",
    "blog/troubleshooting/dryer-not-drying-clothes.html",
    "blog/troubleshooting/dryer-not-heating.html",
    "blog/troubleshooting/dryer-repair-toronto.html",
    "blog/troubleshooting/electric-stove-burner-not-heating.html",
    "blog/troubleshooting/emergency-appliance-repair-24-7.html",
    "blog/troubleshooting/freezer-frost-buildup-ice-problems.html",
    "blog/troubleshooting/freezer-not-freezing.html",
    "blog/troubleshooting/freezer-repair-guide.html",
    "blog/troubleshooting/garbage-disposal-grinding-noise-repair.html",
    "blog/troubleshooting/garbage-disposal-jammed.html",
    "blog/troubleshooting/garbage-disposal-repair.html",
    "blog/troubleshooting/gas-range-igniter-not-working.html",
    "blog/troubleshooting/ice-maker-not-working.html",
    "blog/troubleshooting/ice-maker-repair.html",
    "blog/troubleshooting/lg-appliance-repair-service.html",
    "blog/troubleshooting/microwave-not-heating.html",
    "blog/troubleshooting/microwave-repair-toronto.html",
    "blog/troubleshooting/microwave-sparking-arcing-safety.html",
    "blog/troubleshooting/mobile-appliance-repair-whitehorse.html",
    "blog/troubleshooting/oven-door-wont-close.html",
    "blog/troubleshooting/oven-not-heating.html",
    "blog/troubleshooting/oven-repair-toronto.html",
    "blog/troubleshooting/refrigerator-compressor-noise-diagnosis.html",
    "blog/troubleshooting/refrigerator-door-seal-replacement.html",
    "blog/troubleshooting/refrigerator-ice-maker-repair-guide.html",
    "blog/troubleshooting/refrigerator-not-cooling-toronto.html",
    "blog/troubleshooting/refrigerator-repair-toronto.html",
    "blog/troubleshooting/refrigerator-water-dispenser-not-working.html",
    "blog/troubleshooting/refrigerator-water-dispenser-troubleshooting-guide.html",
    "blog/troubleshooting/same-day-appliance-repair.html",
    "blog/troubleshooting/samsung-appliance-repair.html",
    "blog/troubleshooting/stove-burner-not-working.html",
    "blog/troubleshooting/stove-repair-toronto.html",
    "blog/troubleshooting/washer-drum-not-spinning-repair.html",
    "blog/troubleshooting/washer-wont-drain.html",
    "blog/troubleshooting/washing-machine-filter-maintenance-guide.html",
    "blog/troubleshooting/washing-machine-leaking-water.html",
    "blog/troubleshooting/washing-machine-leaking.html",
    "blog/troubleshooting/washing-machine-not-agitating-repairs.html",
    "blog/troubleshooting/washing-machine-overflow-prevention-guide.html",
    "blog/troubleshooting/washing-machine-repair-complete-guide.html",
    "blog/troubleshooting/water-heater-repair-toronto.html",
    "blog/troubleshooting/whirlpool-customer-service-repair.html",
    "blog/troubleshooting/oven-temperature-calibration-guide.html",
    "blog/troubleshooting/front-load-washer-problems-toronto.html",
    "blog/troubleshooting/smart-appliance-troubleshooting-guide.html",
]

def categorize_posts():
    """Categorize posts by appliance type"""
    categories = defaultdict(list)

    for post in posts_without_images:
        filename = post.lower()

        # Categorize by appliance type
        if 'dishwasher' in filename:
            categories['dishwasher'].append(post)
        elif 'refrigerator' in filename or 'freezer' in filename or 'ice-maker' in filename or 'ice maker' in filename:
            categories['refrigerator'].append(post)
        elif 'washer' in filename or 'washing-machine' in filename or 'washing machine' in filename:
            categories['washer'].append(post)
        elif 'dryer' in filename:
            categories['dryer'].append(post)
        elif 'oven' in filename or 'stove' in filename or 'range' in filename:
            categories['oven'].append(post)
        elif 'microwave' in filename:
            categories['microwave'].append(post)
        elif 'garbage-disposal' in filename or 'garbage disposal' in filename:
            categories['garbage-disposal'].append(post)
        elif 'water-heater' in filename or 'water heater' in filename:
            categories['water-heater'].append(post)
        else:
            categories['general'].append(post)

    return categories

if __name__ == "__main__":
    categories = categorize_posts()

    print("Blog Posts by Appliance Type")
    print("=" * 60)

    total = 0
    for category, posts in sorted(categories.items()):
        print(f"\n{category.upper()}: {len(posts)} posts")
        total += len(posts)
        for post in posts[:3]:  # Show first 3
            print(f"  - {post}")
        if len(posts) > 3:
            print(f"  ... and {len(posts) - 3} more")

    print(f"\n{'=' * 60}")
    print(f"TOTAL: {total} posts need images")
    print(f"\nImage types needed: {len(categories)}")
