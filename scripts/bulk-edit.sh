#!/bin/bash

# Bulk HTML Editor Script
# Usage: ./bulk-edit.sh

# Example 1: Replace text across all location pages
# find locations/*.html -type f -exec sed -i 's/old-text/new-text/g' {} \;

# Example 2: Remove a specific element by ID from all service pages
# find services/*.html -type f -exec sed -i '/<div id="element-to-remove"/,/<\/div>/d' {} \;

# Example 3: Add something before closing </body> tag on all pages
# find . -name "*.html" -type f -exec sed -i 's|</body>|<!-- new content -->\n</body>|' {} \;

# Example 4: Replace phone numbers across all HTML files
# find . -name "*.html" -type f -exec sed -i 's/437-747-6737/NEW-PHONE-NUMBER/g' {} \;

echo "Bulk edit script ready. Uncomment the commands you need."
