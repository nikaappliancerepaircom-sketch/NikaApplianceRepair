"""
Fix blog posts with missing hero images by removing the hero image section
Instead of showing purple gradient fallback, completely remove the section
"""
import re
from pathlib import Path

blog_dir = Path('blog')
images_dir = blog_dir / 'images'

# Find all HTML blog files (exclude main blog pages)
html_files = [f for f in blog_dir.glob('**/*.html')
              if f.name not in ['blog.html', 'image-gallery.html']]

fixed_files = []
failed_files = []

for html_file in sorted(html_files):
    with open(html_file, 'r', encoding='utf-8') as f:
        original_content = f.read()

    # Find the first hero image reference (in <div class="blog-hero-image">)
    # Pattern: <div class="blog-hero-image">...<source srcset="../images/[filename]"...
    hero_pattern = r'<div class="blog-hero-image">.*?</div>'
    hero_match = re.search(hero_pattern, original_content, re.DOTALL)

    if not hero_match:
        # No hero image section found, skip
        continue

    hero_section = hero_match.group()

    # Extract the image filename from the hero section
    img_patterns = [
        r'<source srcset="\.\.\/images\/([^"]+)"',
        r'<img src="\.\.\/images\/([^"]+)"'
    ]

    hero_image_name = None
    for pattern in img_patterns:
        match = re.search(pattern, hero_section)
        if match:
            hero_image_name = match.group(1)
            break

    if not hero_image_name:
        # Couldn't extract image name, skip
        continue

    # Check if the image exists
    img_path = images_dir / hero_image_name

    if img_path.exists():
        # Image exists, keep the section
        continue

    # Image is missing - remove the hero section
    print(f"Removing hero image from: {html_file.relative_to('.')}")
    print(f"  Missing image: {hero_image_name}")

    # Remove the div (including whitespace/newlines around it)
    modified_content = original_content[:hero_match.start()] + original_content[hero_match.end():]

    # Clean up extra blank lines left behind
    modified_content = re.sub(r'\n\s*\n\s*\n', '\n\n', modified_content)

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(modified_content)

    fixed_files.append(str(html_file.relative_to('.')))

print("\n" + "=" * 80)
print(f"FIXED: {len(fixed_files)} blog posts")
print("=" * 80)

if fixed_files:
    for f in fixed_files:
        print(f"  [FIXED] {f}")

print("\n" + "=" * 80)
