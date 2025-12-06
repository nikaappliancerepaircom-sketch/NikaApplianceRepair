#!/usr/bin/env python3
"""
Add Hero Images to Blog Posts
- Copies generated images to blog/images/
- Adds hero section HTML to each post
"""

import os
import shutil
import re
from pathlib import Path

# Paths
ROOT_DIR = Path("C:/NikaApplianceRepair")
POSTS_DIR = ROOT_DIR / "blog" / "posts"
DRAFTS_DIR = ROOT_DIR / "blog" / "_drafts"
IMAGES_DIR = ROOT_DIR / "blog" / "images"
SOURCE_IMAGES_DIR = Path("C:/Users/petru/nanobanana-images")

# Ensure images directory exists
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# Map of post slugs to generated image filenames (in order of generation)
IMAGE_MAPPING = {
    # First batch (09:55) - before MCP disconnect
    "dishwasher-leaking-from-bottom-causes-fixes": "gen_20251206_095544_1_1_4240aa7e.png",
    "dishwasher-not-draining-quick-fixes": "gen_20251206_095554_1_1_39caaeaa.png",

    # After MCP reconnect (10:40)
    "dishwasher-soap-dispenser-not-opening": "gen_20251206_104003_1_1_e02af0b6.png",
    "dryer-making-squeaking-noise-causes-fixes": "gen_20251206_104014_1_1_48975be6.png",
    "dryer-not-heating-troubleshooting-guide": "gen_20251206_104022_1_1_742e81dc.png",
    "fix-gas-oven-not-heating": "gen_20251206_104031_1_1_192186e1.png",

    # Batch 2 (10:41)
    "freezer-making-loud-noise-diagnosis": "gen_20251206_104101_1_1_855a0fae.png",
    "gas-stove-burner-not-igniting-safety-guide": "gen_20251206_104111_1_1_45240637.png",
    "ice-maker-troubleshooting-complete-guide": "gen_20251206_104123_1_1_73736bf6.png",
    "kenmore-refrigerator-repair-common-issues": "gen_20251206_104134_1_1_18791771.png",

    # Batch 3 (10:42)
    "lg-appliance-repair-toronto-complete-guide": "gen_20251206_104204_1_1_427022ab.png",
    "lg-dishwasher-error-codes-troubleshooting": "gen_20251206_104214_1_1_741b8a06.png",
    "oven-not-heating-evenly-calibration-tips": "gen_20251206_104227_1_1_791c8b01.png",
    "refrigerator-compressor-problems-signs-repair": "gen_20251206_104236_1_1_3e8575f5.png",

    # Batch 4 (10:43)
    "refrigerator-not-cooling-emergency-repair": "gen_20251206_104330_1_1_3b9545f1.png",
    "samsung-ice-maker-not-making-ice": "gen_20251206_104341_1_1_24833afd.png",
    "washer-leaking-from-bottom-common-causes": "gen_20251206_104350_1_1_d076a890.png",
    "washing-machine-error-codes-brand-guide": "gen_20251206_104357_1_1_c820da95.png",

    # Last batch (10:44)
    "washing-machine-not-spinning-causes-solutions": "gen_20251206_104421_1_1_0508df22.png",
    "whirlpool-dishwasher-not-cleaning-dishes": "gen_20251206_104430_1_1_349a433e.png",
}

# Hero section HTML template
HERO_TEMPLATE = '''            <div class="blog-hero-image">
                <picture>
                    <source srcset="../images/{slug}-hero.webp" type="image/webp">
                    <img src="../images/{slug}-hero.png" alt="{alt}" loading="eager">
                </picture>
            </div>'''

def copy_and_rename_images():
    """Copy images from nanobanana folder to blog/images with proper names"""
    print("Copying images to blog/images/...")
    copied = 0

    for slug, source_filename in IMAGE_MAPPING.items():
        source_path = SOURCE_IMAGES_DIR / source_filename
        dest_path = IMAGES_DIR / f"{slug}-hero.png"

        if source_path.exists():
            shutil.copy2(source_path, dest_path)
            print(f"  [OK] {slug}-hero.png")
            copied += 1
        else:
            print(f"  [MISSING] {source_filename}")

    print(f"\nCopied {copied}/20 images")
    return copied

def get_alt_text(slug):
    """Generate alt text from slug"""
    words = slug.replace("-", " ").title()
    return f"Professional {words} - Nika Appliance Repair Toronto"

def add_hero_to_post(filepath):
    """Add hero image section to a blog post"""
    slug = filepath.stem

    if slug not in IMAGE_MAPPING:
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if hero already exists
    if 'blog-hero-image' in content:
        print(f"  [SKIP] {slug} - already has hero")
        return False

    # Find the article content start (after header, before main content)
    # Look for the pattern after breadcrumb and before h1
    hero_html = HERO_TEMPLATE.format(slug=slug, alt=get_alt_text(slug))

    # Insert after <article class="blog-post"> or similar
    # Try to find a good insertion point
    patterns = [
        (r'(<article[^>]*class="[^"]*blog-post[^"]*"[^>]*>)', r'\1\n' + hero_html),
        (r'(<div[^>]*class="[^"]*blog-content[^"]*"[^>]*>)', r'\1\n' + hero_html),
        (r'(<main[^>]*>)', r'\1\n' + hero_html),
    ]

    modified = False
    for pattern, replacement in patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content, count=1)
            modified = True
            break

    if not modified:
        # Fallback: insert after <body> tag
        content = content.replace('<body>', '<body>\n' + hero_html, 1)
        modified = True

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  [OK] {slug}")
    return True

def main():
    print("=" * 60)
    print("ADD HERO IMAGES TO BLOG POSTS")
    print("=" * 60)

    # Step 1: Copy images
    print("\n" + "-" * 40)
    print("STEP 1: Copy images")
    print("-" * 40)
    copy_and_rename_images()

    # Step 2: Add hero sections to posts
    print("\n" + "-" * 40)
    print("STEP 2: Add hero sections to posts/")
    print("-" * 40)
    posts_modified = 0
    for post in POSTS_DIR.glob("*.html"):
        if add_hero_to_post(post):
            posts_modified += 1

    # Step 3: Add hero sections to drafts
    print("\n" + "-" * 40)
    print("STEP 3: Add hero sections to _drafts/")
    print("-" * 40)
    drafts_modified = 0
    for draft in DRAFTS_DIR.glob("*.html"):
        if not draft.name.startswith("_"):
            if add_hero_to_post(draft):
                drafts_modified += 1

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Posts modified:  {posts_modified}")
    print(f"  Drafts modified: {drafts_modified}")
    print(f"  Total:           {posts_modified + drafts_modified}")
    print("\nDone!")

if __name__ == "__main__":
    main()
