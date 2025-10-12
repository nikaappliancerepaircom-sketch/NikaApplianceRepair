#!/bin/bash

# Script to optimize all service and location pages
# Applies all optimizations from homepage:
# 1. Mobile BMAD typography
# 2. Lighthouse fixes
# 3. YouTube facade
# 4. Defer JS

echo "Starting optimization of all pages..."

# Function to add CSS files to HTML if not already present
add_css_if_missing() {
    local file=$1
    local css_file=$2
    local css_comment=$3

    # Check if CSS is already present
    if ! grep -q "$css_file" "$file"; then
        # Find the line with no-scrollbars-fix.css and insert before it
        sed -i "/no-scrollbars-fix.css/i\\    <!-- $css_comment -->\n    <link rel=\"stylesheet\" href=\"../$css_file\">" "$file"
        echo "  Added $css_file to $(basename $file)"
    fi
}

# Function to add defer to scripts
add_defer_to_scripts() {
    local file=$1

    # Add defer to countdown-timer.js if not present
    if grep -q '<script src="../js/countdown-timer.js"></script>' "$file"; then
        sed -i 's|<script src="../js/countdown-timer.js"></script>|<script src="../js/countdown-timer.js" defer></script>|g' "$file"
        echo "  Added defer to countdown-timer.js in $(basename $file)"
    fi

    # Add defer to main.js if present
    if grep -q '<script src="../js/main.js"></script>' "$file"; then
        sed -i 's|<script src="../js/main.js"></script>|<script src="../js/main.js" defer></script>|g' "$file"
        echo "  Added defer to main.js in $(basename $file)"
    fi
}

# Function to add YouTube facade script if not present
add_youtube_facade_script() {
    local file=$1

    # Check if YouTube facade is already present
    if ! grep -q "youtube-facade.js" "$file"; then
        # Find </body> tag and insert before it
        sed -i 's|</body>|    <script src="../js/youtube-facade.js" defer></script>\n</body>|' "$file"
        echo "  Added youtube-facade.js to $(basename $file)"
    fi
}

# Function to add aria-label to mobile menu toggle
fix_mobile_menu_button() {
    local file=$1

    # Check if button already has aria-label
    if grep -q 'class="mobile-menu-toggle"' "$file" && ! grep -q 'aria-label="Toggle mobile menu"' "$file"; then
        sed -i 's|<button class="mobile-menu-toggle">|<button class="mobile-menu-toggle" aria-label="Toggle mobile menu" aria-expanded="false">|g' "$file"
        echo "  Added aria-label to mobile menu in $(basename $file)"
    fi
}

# Function to add skip-to-content link
add_skip_link() {
    local file=$1

    # Check if skip link already exists
    if ! grep -q "skip-to-content" "$file"; then
        # Add after <body> tag
        sed -i 's|<body>|<body>\n    <!-- Skip to main content link for accessibility -->\n    <a href="#main-content" class="skip-to-content">Skip to main content</a>\n|' "$file"
        echo "  Added skip-to-content link to $(basename $file)"
    fi
}

# Function to add id="main-content" to first section
add_main_content_id() {
    local file=$1

    # Check if main-content id already exists
    if ! grep -q 'id="main-content"' "$file"; then
        # Find first <section and add id
        sed -i '0,/<section class="hero-section">/s|<section class="hero-section">|<section class="hero-section" id="main-content">|' "$file"
        echo "  Added id=main-content to $(basename $file)"
    fi
}

echo ""
echo "========================================="
echo "Optimizing SERVICE pages..."
echo "========================================="

for file in services/*.html; do
    echo ""
    echo "Processing: $file"

    # Add CSS files
    add_css_if_missing "$file" "css/mobile-bmad-typography.css" "Mobile BMAD Typography & Buttons"
    add_css_if_missing "$file" "css/lighthouse-fixes.css" "Lighthouse Accessibility & Performance Fixes"
    add_css_if_missing "$file" "css/youtube-facade.css" "YouTube Facade (Lazy Loading)"
    add_css_if_missing "$file" "css/mobile-overflow-fix.css" "Mobile Overflow & Centering Fix"

    # Add defer to scripts
    add_defer_to_scripts "$file"

    # Add YouTube facade script
    add_youtube_facade_script "$file"

    # Fix accessibility issues
    fix_mobile_menu_button "$file"
    add_skip_link "$file"
    add_main_content_id "$file"

    echo "  ✓ Completed: $(basename $file)"
done

echo ""
echo "========================================="
echo "Optimizing LOCATION pages..."
echo "========================================="

for file in locations/*.html; do
    echo ""
    echo "Processing: $file"

    # Add CSS files
    add_css_if_missing "$file" "css/mobile-bmad-typography.css" "Mobile BMAD Typography & Buttons"
    add_css_if_missing "$file" "css/lighthouse-fixes.css" "Lighthouse Accessibility & Performance Fixes"
    add_css_if_missing "$file" "css/youtube-facade.css" "YouTube Facade (Lazy Loading)"
    add_css_if_missing "$file" "css/mobile-overflow-fix.css" "Mobile Overflow & Centering Fix"

    # Add defer to scripts
    add_defer_to_scripts "$file"

    # Add YouTube facade script
    add_youtube_facade_script "$file"

    # Fix accessibility issues
    fix_mobile_menu_button "$file"
    add_skip_link "$file"
    add_main_content_id "$file"

    echo "  ✓ Completed: $(basename $file)"
done

echo ""
echo "========================================="
echo "Optimization complete!"
echo "========================================="
echo ""
echo "Summary:"
echo "- Added Mobile BMAD typography CSS"
echo "- Added Lighthouse accessibility fixes"
echo "- Added YouTube facade for lazy loading"
echo "- Added Mobile overflow fixes"
echo "- Added defer to JavaScript files"
echo "- Fixed mobile menu accessibility"
echo "- Added skip-to-content links"
echo "- Added main-content IDs"
echo ""
echo "All pages should now have PageSpeed scores of 89+"
