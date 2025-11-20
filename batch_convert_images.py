"""Batch convert generated PNG images to WebP and save to blog directory"""
from PIL import Image
from pathlib import Path

# Map of generated PNG files to their target WebP filenames
images_to_convert = {
    'C:/Users/petru/Documents/nano-banana-images/generated-2025-11-20T14-56-57-199Z-12ql62.png': 'ice-maker-not-working-hero.webp',
    'C:/Users/petru/Documents/nano-banana-images/generated-2025-11-20T14-57-03-815Z-qs15oy.png': 'dishwasher-not-cleaning-hero.webp',
    'C:/Users/petru/Documents/nano-banana-images/generated-2025-11-20T14-57-12-354Z-l6387d.png': 'dryer-not-heating-hero.webp',
    'C:/Users/petru/Documents/nano-banana-images/generated-2025-11-20T14-57-18-368Z-bm7jej.png': 'washer-wont-drain-hero.webp',
    'C:/Users/petru/Documents/nano-banana-images/generated-2025-11-20T14-57-25-118Z-eb1bki.png': 'microwave-not-heating-hero.webp',
}

blog_images_dir = Path('C:/NikaApplianceRepair/blog/images')

for png_path_str, webp_name in images_to_convert.items():
    png_path = Path(png_path_str)
    webp_path = blog_images_dir / webp_name

    if png_path.exists():
        print(f"Converting {png_path.name}...")
        img = Image.open(png_path)

        # Resize to 1200x630 (standard hero image size)
        if img.size != (1200, 630):
            img = img.resize((1200, 630), Image.Resampling.LANCZOS)

        # Save as WebP
        img.save(webp_path, 'WEBP', quality=85)

        # Check size
        size_kb = webp_path.stat().st_size / 1024
        print(f"[OK] Saved {webp_name}: {size_kb:.1f} KB")
    else:
        print(f"[ERROR] File not found: {png_path}")

print("\nConversion complete!")
