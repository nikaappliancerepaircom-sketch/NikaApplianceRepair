import os
import sys
import shutil
from pathlib import Path
from PIL import Image
import json

# Fix encoding on Windows
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Image source directory
source_dir = Path.home() / "Documents" / "nano-banana-images"
target_dir = Path("public/blog-images")

# Create target directory
target_dir.mkdir(parents=True, exist_ok=True)

# Map of blog posts to generated images
image_mappings = {
    "blog/guides/dryer-vent-cleaning-fire-prevention.html": "clothes-dryer-lint-hazard",
    "blog/guides/washing-machine-filter-maintenance-guide.html": "washing-machine-filter",
    "blog/guides/refrigerator-repair-vs-replace.html": "refrigerator-temperature",
    "blog/guides/dishwasher-hard-water-solutions-toronto.html": "dishwasher-spray-arm",
    "blog/guides/oven-temperature-calibration-guide.html": "oven-calibration",
    "blog/troubleshooting/washing-machine-repair-complete-guide.html": "washing-machine-agitator",
    "blog/troubleshooting/refrigerator-ice-maker-not-working.html": "ice-maker-assembly",
    "blog/guides/gas-range-repair-safety-toronto.html": "gas-range-igniter",
    "blog/troubleshooting/freezer-frost-buildup-ice-problems.html": "freezer-frost",
    "blog/troubleshooting/dishwasher-water-not-draining-completely.html": "dishwasher-drain",
    "blog/troubleshooting/microwave-sparking-arcing-safety.html": "microwave-arcing",
    "blog/troubleshooting/washer-drum-not-spinning-repair.html": "washer-belt",
    "blog/troubleshooting/garbage-disposal-repair.html": "garbage-disposal",
    "blog/troubleshooting/electric-stove-burner-not-heating.html": "electric-stove",
    "blog/troubleshooting/refrigerator-compressor-noise-diagnosis.html": "compressor-diagnosis",
}

# List all images
images = sorted([f for f in source_dir.glob("generated-*.png")])
print(f"Found {len(images)} images")

# Process images - take the last 15 (most recent)
images_to_use = images[-15:] if len(images) >= 15 else images

converted = 0
for idx, (post_path, img_name) in enumerate(image_mappings.items()):
    if idx < len(images_to_use):
        src_img = images_to_use[idx]
        
        # Convert to WebP
        output_file = target_dir / f"{img_name}.webp"
        
        try:
            img = Image.open(src_img)
            img.thumbnail((1200, 800), Image.Resampling.LANCZOS)
            img.save(output_file, 'WEBP', quality=85, method=6)
            size_mb = output_file.stat().st_size / 1024 / 1024
            print(f"[OK] {img_name}.webp ({size_mb:.2f}MB)")
            converted += 1
        except Exception as e:
            print(f"[ERR] {img_name}: {e}")

print(f"\nConverted {converted} WebP images")

# Save mapping
with open("image_mappings.json", "w") as f:
    json.dump(image_mappings, f, indent=2)
print("Mapping saved to image_mappings.json")
