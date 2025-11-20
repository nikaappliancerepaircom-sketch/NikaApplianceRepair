"""Check hero image file sizes"""
from pathlib import Path

blog_images = Path('C:/NikaApplianceRepair/blog/images')
hero_images = sorted(blog_images.glob('*-hero.webp'))

print(f"Found {len(hero_images)} hero images\n")

# Group by size
small_images = []  # < 10KB
medium_images = []  # 10-50KB
large_images = []  # > 50KB

for img in hero_images:
    size_kb = img.stat().st_size / 1024
    if size_kb < 10:
        small_images.append((img.name, size_kb))
    elif size_kb < 50:
        medium_images.append((img.name, size_kb))
    else:
        large_images.append((img.name, size_kb))

print(f"[SMALL < 10KB] {len(small_images)} images (likely placeholders):")
for name, size in small_images[:10]:  # Show first 10
    print(f"  {name}: {size:.1f} KB")
if len(small_images) > 10:
    print(f"  ... and {len(small_images) - 10} more")

print(f"\n[MEDIUM 10-50KB] {len(medium_images)} images:")
for name, size in medium_images[:5]:
    print(f"  {name}: {size:.1f} KB")

print(f"\n[LARGE > 50KB] {len(large_images)} images (real hero images):")
for name, size in large_images[:10]:
    print(f"  {name}: {size:.1f} KB")
if len(large_images) > 10:
    print(f"  ... and {len(large_images) - 10} more")
