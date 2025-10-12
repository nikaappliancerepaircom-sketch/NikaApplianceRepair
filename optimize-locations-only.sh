#!/bin/bash

# Script to add PageSpeed optimization CSS files to location pages
# Location pages have different structure than service pages

echo "Starting optimization of LOCATION pages only..."
echo ""

for file in locations/*.html; do
    # Skip if it's the locations index page
    if [[ "$file" == "locations/index.html" ]]; then
        continue
    fi

    echo "Processing: $(basename $file)"

    # Check if optimization CSS files are already present
    if grep -q "mobile-bmad-typography.css" "$file"; then
        echo "  ✓ Already optimized: $(basename $file)"
        continue
    fi

    # Add CSS files before </head> tag
    # Use sed to insert before </head>
    sed -i 's|</head>|    <!-- Mobile BMAD Typography \& Buttons -->\
    <link rel="stylesheet" href="../css/mobile-bmad-typography.css">\
    <!-- Lighthouse Accessibility \& Performance Fixes -->\
    <link rel="stylesheet" href="../css/lighthouse-fixes.css">\
    <!-- YouTube Facade (Lazy Loading) -->\
    <link rel="stylesheet" href="../css/youtube-facade.css">\
    <!-- Mobile Overflow \& Centering Fix -->\
    <link rel="stylesheet" href="../css/mobile-overflow-fix.css">\
    <!-- FINAL Overflow Fix - Deprecated API Fix -->\
    <link rel="stylesheet" href="../css/final-overflow-fix.css">\
</head>|' "$file"

    echo "  ✓ Added optimization CSS files to $(basename $file)"
done

echo ""
echo "========================================="
echo "Location pages optimization complete!"
echo "========================================="
echo ""
echo "Added to all location pages:"
echo "- Mobile BMAD Typography CSS"
echo "- Lighthouse Accessibility Fixes"
echo "- YouTube Facade (Lazy Loading)"
echo "- Mobile Overflow Fixes"
echo "- Final Overflow Fix (Deprecated API)"
echo ""
