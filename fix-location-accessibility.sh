#!/bin/bash

# Script to add accessibility features to location pages

echo "Adding accessibility features to location pages..."
echo ""

for file in locations/*.html; do
    # Skip if it's the locations index page
    if [[ "$file" == "locations/index.html" ]]; then
        continue
    fi

    echo "Processing: $(basename $file)"

    # Add id="main-content" to hero section if not already present
    if ! grep -q 'id="main-content"' "$file"; then
        # Add id="main-content" to hero section
        sed -i 's|<section aria-label="Hero banner" class="hero-section">|<section aria-label="Hero banner" class="hero-section" id="main-content">|g' "$file"
        echo "  ✓ Added id=main-content to $(basename $file)"
    else
        echo "  ✓ Already has main-content ID: $(basename $file)"
    fi
done

echo ""
echo "========================================="
echo "Accessibility features added!"
echo "========================================="
echo ""
