"""Convert generated PNG to WebP and save to blog images"""
from PIL import Image
from pathlib import Path

# Path to the generated image
generated_png = Path('C:/Users/petru/Documents/nano-banana-images/generated-2025-11-20T14-41-08-140Z-cu1oio.png')
output_webp = Path('C:/NikaApplianceRepair/blog/images/bosch-dishwasher-repair-hero.webp')

if generated_png.exists():
    print(f"Converting {generated_png.name}...")
    img = Image.open(generated_png)

    # Resize to 1200x630 (standard hero image size)
    if img.size != (1200, 630):
        img = img.resize((1200, 630), Image.Resampling.LANCZOS)
        print(f"Resized from {img.size} to 1200x630")

    # Save as WebP
    img.save(output_webp, 'WEBP', quality=85)

    # Check size
    size_kb = output_webp.stat().st_size / 1024
    print(f"[OK] Saved to {output_webp}")
    print(f"    Size: {size_kb:.1f} KB")
else:
    print(f"[ERROR] File not found: {generated_png}")
