#!/usr/bin/env python3
"""
BMAD Auto-Improvement Script
Automatically improves pages to meet BMAD 277 parameters
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

PROJECT_ROOT = Path(__file__).parent.parent

# Global data consistency standards
CONSISTENCY_DATA = {
    "years_in_business": "6+",
    "phone": "437-747-6737",
    "phone_href": "tel:4377476737",
    "warranty": "90-day",
    "service_hours": "24/7",
    "rating": "4.9",
    "reviews_count": "5,200+"
}

def fix_years_consistency(html_content):
    """Fix years in business consistency"""
    # Replace common variations
    html_content = re.sub(r'\b5\+ years?\b', '6+ years', html_content, flags=re.IGNORECASE)
    html_content = re.sub(r'\bsince 2019\b', 'with 6+ years of experience', html_content, flags=re.IGNORECASE)
    html_content = re.sub(r'>5\+<', '>6+<', html_content)

    return html_content

def fix_service_hours_consistency(html_content):
    """Fix service hours consistency - standardize to 24/7"""
    # Replace common variations
    html_content = re.sub(r'\b8AM-6PM\b', '24/7', html_content, flags=re.IGNORECASE)
    html_content = re.sub(r'\b9AM-5PM\b', '24/7', html_content, flags=re.IGNORECASE)
    html_content = re.sub(r'\b8:00 AM - 6:00 PM\b', '24/7 Emergency Service', html_content, flags=re.IGNORECASE)

    return html_content

def add_ratings_if_missing(soup):
    """Add rating stars if missing"""
    # Check if ratings already exist
    if soup.find(string=re.compile(r'4\.9|★')):
        return soup

    # Find hero section and add rating
    hero = soup.find('section', class_=re.compile('hero'))
    if hero:
        rating_html = '''
        <div class="hero-rating" style="display: flex; align-items: center; gap: 0.5rem; margin: 1rem 0;">
            <span style="color: #FFD700; font-size: 1.2rem;">★★★★★</span>
            <span style="font-weight: 600; color: #0f172a;">4.9/5</span>
            <span style="color: #64748b;">(5,200+ reviews)</span>
        </div>
        '''
        subtitle = hero.find('p', class_='hero-subtitle')
        if subtitle:
            rating_div = BeautifulSoup(rating_html, 'html.parser')
            subtitle.insert_after(rating_div)

    return soup

def add_schema_markup(soup):
    """Add LocalBusiness and Service schema"""
    # Check if schema already exists
    if soup.find('script', type='application/ld+json'):
        return soup

    schema_html = '''
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "LocalBusiness",
      "name": "Nika Appliance Repair",
      "image": "https://nikaappliancerepair.ca/assets/images/logo.png",
      "@id": "https://nikaappliancerepair.ca",
      "url": "https://nikaappliancerepair.ca",
      "telephone": "437-747-6737",
      "priceRange": "$$",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "",
        "addressLocality": "Toronto",
        "addressRegion": "ON",
        "postalCode": "",
        "addressCountry": "CA"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": 43.6532,
        "longitude": -79.3832
      },
      "openingHoursSpecification": {
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": [
          "Monday",
          "Tuesday",
          "Wednesday",
          "Thursday",
          "Friday",
          "Saturday",
          "Sunday"
        ],
        "opens": "00:00",
        "closes": "23:59"
      },
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "4.9",
        "reviewCount": "5200"
      }
    }
    </script>
    '''

    head = soup.find('head')
    if head:
        schema_tag = BeautifulSoup(schema_html, 'html.parser')
        head.append(schema_tag)

    return soup

def improve_page(file_path):
    """Improve a single page"""
    print(f"\nImproving: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Fix 1: Years consistency
        html_content = fix_years_consistency(html_content)
        print("  [OK] Fixed years consistency")

        # Fix 2: Service hours
        html_content = fix_service_hours_consistency(html_content)
        print("  [OK] Fixed service hours")

        # Parse with BeautifulSoup for more complex fixes
        soup = BeautifulSoup(html_content, 'html.parser')

        # Fix 3: Add ratings
        soup = add_ratings_if_missing(soup)
        print("  [OK] Checked/added ratings")

        # Fix 4: Add schema
        soup = add_schema_markup(soup)
        print("  [OK] Checked/added schema markup")

        # Save improved content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))

        print(f"  [DONE] Successfully improved {file_path}")
        return True

    except Exception as e:
        print(f"  [ERROR] Failed to improve {file_path}: {str(e)}")
        return False

def main():
    print("=" * 70)
    print("BMAD AUTO-IMPROVEMENT SCRIPT")
    print("=" * 70)
    print()
    print("This script will automatically fix common issues:")
    print("  1. Years in business consistency (5+ -> 6+)")
    print("  2. Service hours consistency (-> 24/7)")
    print("  3. Add ratings if missing (4.9 stars with 5,200+ reviews)")
    print("  4. Add LocalBusiness schema if missing")
    print()

    # Get all HTML files
    pages_to_improve = []

    # Main page
    index_file = PROJECT_ROOT / "index.html"
    if index_file.exists():
        pages_to_improve.append(index_file)

    # Service pages
    services_dir = PROJECT_ROOT / "services"
    if services_dir.exists():
        pages_to_improve.extend(services_dir.glob("*.html"))

    # Location pages
    locations_dir = PROJECT_ROOT / "locations"
    if locations_dir.exists():
        pages_to_improve.extend(locations_dir.glob("*.html"))

    print(f"Found {len(pages_to_improve)} pages to improve")
    print("=" * 70)

    improved_count = 0
    failed_count = 0

    for page_path in pages_to_improve:
        if improve_page(page_path):
            improved_count += 1
        else:
            failed_count += 1

    print("\n" + "=" * 70)
    print("AUTO-IMPROVEMENT COMPLETE")
    print("=" * 70)
    print(f"Successfully improved: {improved_count}/{len(pages_to_improve)}")
    print(f"Failed: {failed_count}/{len(pages_to_improve)}")
    print()
    print("Next step: Run mass-test-all-pages.py to verify improvements")
    print("=" * 70)

if __name__ == "__main__":
    main()
