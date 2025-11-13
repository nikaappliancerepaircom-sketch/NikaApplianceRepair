#!/bin/bash

# Find all blog post HTML files and add FAQ script if not already present
find blog -type f -name "*.html" \( -path "*/guides/*" -o -path "*/troubleshooting/*" -o -path "*/maintenance/*" \) | while read file; do
    # Check if file already has the FAQ script
    if ! grep -q 'faq-accordion.js' "$file"; then
        # Add the script before </body> tag
        sed -i 's|</body>|    <script src="/blog/js/faq-accordion.js"></script>\n</body>|' "$file"
        echo "Updated: $file"
    fi
done
