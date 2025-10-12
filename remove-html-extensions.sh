#!/bin/bash

echo "🔧 Removing .html extensions from all internal links for clean URLs..."
echo ""

# Function to remove .html from links in a file
remove_html_extensions() {
    local file=$1

    # Remove .html from href attributes (but not external links)
    sed -i 's|href="/services/\([^"]*\)\.html"|href="/services/\1"|g' "$file"
    sed -i 's|href="/locations/\([^"]*\)\.html"|href="/locations/\1"|g' "$file"

    # Also handle relative paths without leading slash
    sed -i 's|href="services/\([^"]*\)\.html"|href="services/\1"|g' "$file"
    sed -i 's|href="locations/\([^"]*\)\.html"|href="locations/\1"|g' "$file"

    # Handle links in optimizations.html and other tracking pages
    sed -i 's|/services/\([^"]*\)\.html|/services/\1|g' "$file"
    sed -i 's|/locations/\([^"]*\)\.html|/locations/\1|g' "$file"
}

# Counter
count=0

# Process homepage
if [ -f "index.html" ]; then
    echo "  📄 Processing: index.html"
    remove_html_extensions "index.html"
    ((count++))
fi

# Process all service pages
for file in services/*.html; do
    if [ -f "$file" ]; then
        echo "  📄 Processing: $(basename $file)"
        remove_html_extensions "$file"
        ((count++))
    fi
done

# Process all location pages
for file in locations/*.html; do
    if [ -f "$file" ]; then
        echo "  📄 Processing: $(basename $file)"
        remove_html_extensions "$file"
        ((count++))
    fi
done

# Process optimizations.html
if [ -f "optimizations.html" ]; then
    echo "  📄 Processing: optimizations.html"
    remove_html_extensions "optimizations.html"
    ((count++))
fi

echo ""
echo "✅ Processed $count files"
echo ""
echo "🎯 Clean URL Structure:"
echo "  • /services/refrigerator-repair (instead of .html)"
echo "  • /locations/toronto (instead of .html)"
echo "  • / (homepage)"
echo ""
echo "📝 Vercel Configuration:"
echo "  • cleanUrls: true (automatic .html removal)"
echo "  • trailingSlash: false (no trailing slashes)"
echo "  • Security headers added"
echo "  • Cache headers for assets"
echo ""
