"""
Check all blog posts for missing hero images
Identifies which blog posts need their hero image sections removed
"""
import re
from pathlib import Path

blog_dir = Path('blog')
images_dir = blog_dir / 'images'

# Find all HTML blog files
html_files = list(blog_dir.glob('**/*.html'))

missing_images = []
broken_references = []
valid_images = []

for html_file in sorted(html_files):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip non-blog posts (main blog page)
    if html_file.name == 'blog.html':
        continue

    # Look for hero image references
    # Pattern 1: ../images/[filename].webp or /blog-images/[filename]
    patterns = [
        r'<source srcset="\.\.\/images\/([^"]+)"',
        r'<source srcset="\/blog-images\/([^"]+)"',
        r'<img src="\.\.\/images\/([^"]+)"',
        r'<img src="\/blog-images\/([^"]+)"'
    ]

    found_images = set()
    for pattern in patterns:
        matches = re.findall(pattern, content)
        found_images.update(matches)

    if not found_images:
        # No hero image reference found
        continue

    # Check each referenced image
    for img_name in found_images:
        img_path = images_dir / img_name

        if not img_path.exists():
            broken_references.append({
                'file': str(html_file.relative_to('.')),
                'referenced': img_name,
                'expected_path': str(img_path)
            })
        else:
            valid_images.append({
                'file': str(html_file.relative_to('.')),
                'image': img_name
            })

# Report results
print("=" * 80)
print("BLOG POST HERO IMAGE ANALYSIS")
print("=" * 80)

print(f"\nTotal blog files scanned: {len(html_files)}")
print(f"Posts with valid hero images: {len(set(img['file'] for img in valid_images))}")
print(f"Posts with BROKEN image references: {len(broken_references)}")

if broken_references:
    print("\n" + "=" * 80)
    print("BLOG POSTS WITH MISSING/BROKEN IMAGES (need to remove hero image sections):")
    print("=" * 80)

    for ref in sorted(broken_references, key=lambda x: x['file']):
        print(f"\n[FILE] {ref['file']}")
        print(f"   Referenced: {ref['referenced']}")
        print(f"   Expected:   {ref['expected_path']}")

    print(f"\n\nTotal files to fix: {len(broken_references)}")

print("\n" + "=" * 80)
print("BLOG POSTS WITH VALID HERO IMAGES (keep as is):")
print("=" * 80)
for post in sorted(set(img['file'] for img in valid_images)):
    print(f"[OK] {post}")

print("\n" + "=" * 80)
