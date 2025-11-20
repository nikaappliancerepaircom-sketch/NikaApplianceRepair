"""Generate hero images for all blog posts with placeholders"""
import os
import time
from pathlib import Path
from PIL import Image
import subprocess
import json

# Image generation prompts based on blog post topics
IMAGE_PROMPTS = {
    'bosch-dishwasher-repair': 'Professional appliance repair technician fixing a Bosch dishwasher in a modern Toronto kitchen, wearing blue uniform, diagnostic tools on counter, open dishwasher door showing interior racks, clean professional setting, natural lighting, photorealistic style',
    'electrolux-appliance-repair': 'Certified Electrolux appliance repair technician working on a modern stainless steel refrigerator in Toronto home, professional blue uniform, diagnostic equipment, clean kitchen background, photorealistic style',
    'refrigerator-not-cooling-toronto': 'Appliance technician diagnosing a refrigerator not cooling, checking temperature with infrared thermometer, open fridge door, Toronto residential kitchen, professional repair service, photorealistic',
    'washing-machine-leaking': 'Professional technician inspecting a front-load washing machine for water leaks, kneeling beside machine with tools, water puddle visible, residential laundry room, diagnostic equipment, photorealistic style',
    'dryer-not-heating': 'Appliance repair expert testing dryer heating element with multimeter, open dryer back panel showing internal components, professional tools on floor, residential setting, photorealistic',
    'oven-not-heating': 'Certified technician troubleshooting an oven that will not heat, oven door open showing interior, diagnostic tools and multimeter, modern kitchen setting in Toronto, professional uniform, photorealistic style',
    'ice-maker-not-working': 'Appliance technician repairing refrigerator ice maker, looking inside freezer compartment, ice maker mechanism visible, diagnostic tools nearby, professional service, photorealistic',
    'dishwasher-not-cleaning': 'Professional repair technician examining dishwasher spray arms and filters, dishwasher racks pulled out, dirty dishes visible, diagnostic inspection, Toronto home kitchen, photorealistic style',
    'washer-wont-drain': 'Appliance repair expert checking washing machine drain pump and hoses, machine tilted forward, water hose in hand, residential laundry room, professional tools scattered, photorealistic',
    'microwave-not-heating': 'Certified technician servicing a built-in microwave, control panel open showing circuit boards, multimeter testing components, modern kitchen, professional repair service, photorealistic style',
    'garbage-disposal-jammed': 'Professional plumber/appliance technician fixing a jammed garbage disposal under sink, using hex wrench tool, flashlight illuminating under-sink area, residential kitchen, photorealistic',
    'freezer-not-freezing': 'Appliance repair expert diagnosing freezer temperature issue, checking thermostat and evaporator coils, frost buildup visible, professional diagnostic equipment, Toronto home, photorealistic style',
    'stove-burner-not-working': 'Certified technician repairing electric stove burner, testing heating elements with multimeter, stove top open, modern kitchen setting, professional tools and diagnostic equipment, photorealistic',
    'dishwasher-leaving-food-spots': 'Appliance technician inspecting dishwasher dishes with food residue, checking spray arm and filter, dishwasher racks pulled out, professional service in Toronto kitchen, photorealistic style',
    'range-hood-filter-cleaning-maintenance': 'Professional technician cleaning and servicing range hood, removing and examining greasy metal filters, modern kitchen with stainless steel hood, cleaning supplies nearby, photorealistic',
    'refrigerator-door-seal-replacement': 'Appliance repair expert installing new refrigerator door gasket seal, removing old worn seal, professional tools on counter, modern kitchen in Toronto, photorealistic style',
    'washing-machine-filter-maintenance-guide': 'Technician demonstrating washing machine filter maintenance, removing drain filter with water and lint visible, front-load washer, educational repair setting, photorealistic',
    'dryer-vent-cleaning-service': 'Professional dryer vent cleaning specialist with long rotating brush and vacuum equipment, removing lint from dryer vent duct, Toronto residential setting, safety-focused service, photorealistic',
    'gas-range-igniter-not-working': 'Certified gas appliance technician replacing stove igniter, gas burner assembly open, testing with multimeter, safety equipment visible, professional repair in Toronto home, photorealistic style',
    'refrigerator-water-dispenser-not-working': 'Appliance technician troubleshooting refrigerator water dispenser, testing water lines and dispenser mechanism, holding water filter, modern stainless steel fridge, professional service, photorealistic',
}

# Generic prompts for categories
GENERIC_PROMPTS = {
    'dishwasher': 'Professional appliance technician repairing a dishwasher in modern Toronto kitchen, blue uniform, open dishwasher with racks visible, diagnostic tools, clean setting, photorealistic',
    'refrigerator': 'Certified appliance repair expert working on refrigerator in Toronto home, stainless steel fridge, diagnostic equipment, professional uniform, modern kitchen, photorealistic style',
    'washer': 'Professional technician servicing front-load washing machine in residential laundry room, blue uniform, tools and equipment, Toronto home, photorealistic',
    'dryer': 'Appliance repair specialist fixing clothes dryer, open back panel showing components, diagnostic tools, residential setting in Toronto, professional service, photorealistic style',
    'oven': 'Certified technician repairing oven in modern kitchen, oven door open, diagnostic tools and multimeter, professional uniform, Toronto residential, photorealistic',
    'stove': 'Professional appliance technician servicing gas or electric stove, burners visible, testing equipment, modern kitchen in Toronto, blue uniform, photorealistic style',
    'microwave': 'Appliance repair expert fixing built-in microwave, control panel and interior visible, diagnostic tools, professional service in Toronto home, photorealistic',
    'garbage-disposal': 'Professional technician repairing garbage disposal under kitchen sink, tools and flashlight, residential Toronto home, expert plumbing service, photorealistic style',
    'location': 'Professional Nika Appliance Repair service van parked in front of Toronto residential home, technician with tools walking to front door, branded vehicle, clean neighborhood, photorealistic',
    'general': 'Professional appliance repair technician in blue uniform with fully stocked toolbox, standing in modern Toronto kitchen with various appliances, confident expert, photorealistic style',
}

def get_prompt_for_image(filename):
    """Get the appropriate prompt for an image filename"""
    slug = filename.replace('-hero.webp', '')

    # Check if we have a specific prompt
    if slug in IMAGE_PROMPTS:
        return IMAGE_PROMPTS[slug]

    # Use generic prompts based on keywords
    if 'dishwasher' in slug:
        return GENERIC_PROMPTS['dishwasher']
    elif 'refrigerator' in slug or 'fridge' in slug or 'freezer' in slug or 'ice-maker' in slug:
        return GENERIC_PROMPTS['refrigerator']
    elif 'washer' in slug or 'washing' in slug:
        return GENERIC_PROMPTS['washer']
    elif 'dryer' in slug:
        return GENERIC_PROMPTS['dryer']
    elif 'oven' in slug:
        return GENERIC_PROMPTS['oven']
    elif 'stove' in slug or 'range' in slug or 'burner' in slug:
        return GENERIC_PROMPTS['stove']
    elif 'microwave' in slug:
        return GENERIC_PROMPTS['microwave']
    elif 'garbage-disposal' in slug:
        return GENERIC_PROMPTS['garbage-disposal']
    elif 'appliance-repair' in slug and any(loc in slug for loc in ['cabbagetown', 'distillery', 'king-west', 'queen-west', 'peterborough', 'grande-prairie']):
        return GENERIC_PROMPTS['location']
    else:
        return GENERIC_PROMPTS['general']

def convert_png_to_webp(png_path, webp_path):
    """Convert PNG to WebP format"""
    try:
        img = Image.open(png_path)
        # Resize to 1200x630 if needed (hero image standard size)
        if img.size != (1200, 630):
            img = img.resize((1200, 630), Image.Resampling.LANCZOS)
        img.save(webp_path, 'WEBP', quality=85)
        return True
    except Exception as e:
        print(f"Error converting {png_path}: {e}")
        return False

def main():
    # Get list of small placeholder images
    blog_images_dir = Path('C:/NikaApplianceRepair/blog/images')
    placeholder_images = []

    for img_file in blog_images_dir.glob('*-hero.webp'):
        size_kb = img_file.stat().st_size / 1024
        if size_kb < 10:  # Placeholder images are < 10KB
            placeholder_images.append(img_file.name)

    print(f"Found {len(placeholder_images)} placeholder images to regenerate\n")

    # For now, just show what we would generate
    print("Images to generate:")
    for i, img_name in enumerate(placeholder_images[:10], 1):
        prompt = get_prompt_for_image(img_name)
        print(f"\n{i}. {img_name}")
        print(f"   Prompt: {prompt[:100]}...")

    print(f"\n... and {len(placeholder_images) - 10} more")

    # Return list for batch processing
    return [(name, get_prompt_for_image(name)) for name in placeholder_images]

if __name__ == '__main__':
    image_list = main()

    # Save to JSON for reference
    with open('C:/NikaApplianceRepair/image_generation_queue.json', 'w') as f:
        json.dump([{'filename': name, 'prompt': prompt} for name, prompt in image_list], f, indent=2)

    print(f"\nSaved generation queue to image_generation_queue.json")
