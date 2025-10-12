#!/bin/bash

echo "Fixing internal navigation links for service and location pages..."
echo ""

# Fix SERVICE pages navigation
echo "=== Fixing SERVICE pages ==="
for file in services/*.html; do
    echo "Processing: $(basename $file)"

    # Fix main navigation links in header to point to homepage
    sed -i 's|href="#services"|href="/#services"|g' "$file"
    sed -i 's|href="#about"|href="/#about"|g' "$file"
    sed -i 's|href="#areas"|href="/#areas"|g' "$file"
    sed -i 's|href="#brands"|href="/#brands"|g' "$file"
    sed -i 's|href="#contact"|href="/#contact"|g' "$file"
    sed -i 's|href="#book"|href="/#book"|g' "$file"

    # Fix logo link to point to homepage
    sed -i 's|href="/"|href="/"|g' "$file"  # Keep as is if already correct

    # Fix footer links
    sed -i 's|href="/services/refrigerator-repair.html"|href="/services/refrigerator-repair.html"|g' "$file"
    sed -i 's|href="/services/washer-repair.html"|href="/services/washer-repair.html"|g' "$file"
    sed -i 's|href="/services/dishwasher-repair.html"|href="/services/dishwasher-repair.html"|g' "$file"
    sed -i 's|href="/services/dryer-repair.html"|href="/services/dryer-repair.html"|g' "$file"
    sed -i 's|href="/services/oven-repair.html"|href="/services/oven-repair.html"|g' "$file"
    sed -i 's|href="/services/stove-repair.html"|href="/services/stove-repair.html"|g' "$file"

    echo "  ✓ Fixed navigation for $(basename $file)"
done

echo ""
echo "=== Fixing LOCATION pages ==="
for file in locations/*.html; do
    # Skip locations/index.html if exists
    if [[ "$file" == "locations/index.html" ]]; then
        continue
    fi

    echo "Processing: $(basename $file)"

    # Fix main navigation links in header to point to homepage
    sed -i 's|href="#services"|href="/#services"|g' "$file"
    sed -i 's|href="#about"|href="/#about"|g' "$file"
    sed -i 's|href="#areas"|href="/#areas"|g' "$file"
    sed -i 's|href="#brands"|href="/#brands"|g' "$file"
    sed -i 's|href="#contact"|href="/#contact"|g' "$file"
    sed -i 's|href="#book"|href="/#book"|g' "$file"

    # Fix logo link
    sed -i 's|href="/"|href="/"|g' "$file"  # Already correct

    # Fix footer service links
    sed -i 's|href="/services/refrigerator-repair.html"|href="/services/refrigerator-repair.html"|g' "$file"
    sed -i 's|href="/services/washer-repair.html"|href="/services/washer-repair.html"|g' "$file"
    sed -i 's|href="/services/dishwasher-repair.html"|href="/services/dishwasher-repair.html"|g' "$file"
    sed -i 's|href="/services/dryer-repair.html"|href="/services/dryer-repair.html"|g' "$file"
    sed -i 's|href="/services/oven-repair.html"|href="/services/oven-repair.html"|g' "$file"
    sed -i 's|href="/services/stove-repair.html"|href="/services/stove-repair.html"|g' "$file"

    echo "  ✓ Fixed navigation for $(basename $file)"
done

echo ""
echo "================================================"
echo "Navigation links fixed for all pages!"
echo "================================================"
echo ""
echo "Fixed:"
echo "- Header navigation now points to homepage sections (/#services, /#about, etc)"
echo "- Footer service links remain relative (/services/...)"
echo "- Logo links point to homepage (/)"
echo ""
