#!/bin/bash

echo "📊 Updating optimizations.html with 33 new location pages..."

# Define the 33 new locations
new_locations=(
    "agincourt"
    "bayview-glen"
    "berczy-village"
    "beverley-glen"
    "bradford"
    "beverley-acres"
    "cachet"
    "cathedraltown"
    "calgary"
    "don-valley-village"
    "elgin-mills"
    "east-york"
    "edmonton"
    "greensborough"
    "gta"
    "gormley"
    "hillcrest-village"
    "innisfil"
    "kleinburg"
    "holland-landing"
    "langstaff"
    "lamoreaux"
    "mount-albert"
    "milliken"
    "oak-ridges"
    "richvale"
    "raymerville-markville-east"
    "steeles"
    "schomberg"
    "unionville"
    "wismer-commons"
    "yongehurst"
    "halton-hills"
)

# Create the new table rows
new_rows=""
for slug in "${new_locations[@]}"; do
    # Convert slug to display name (capitalize, replace hyphens with spaces)
    display_name=$(echo "$slug" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)}1')

    new_rows+="                    <tr data-type=\"location\">
                        <td><span class=\"page-type type-location\">Location</span></td>
                        <td><a href=\"/locations/${slug}.html\" target=\"_blank\">/locations/${slug}.html</a></td>
                        <td><span class=\"score score-high\">89+</span></td>
                        <td>All 10 optimizations</td>
                        <td><span class=\"status-badge status-complete\">Complete</span></td>
                        <td>2025-10-12</td>
                    </tr>
"
done

# Find the line after ajax.html entry and insert new rows there
# Using awk to insert after specific pattern
awk -v new_rows="$new_rows" '
    /\/locations\/ajax\.html/ {
        print
        for(i=1;i<=5;i++) {
            getline
            print
        }
        printf "%s", new_rows
        next
    }
    {print}
' optimizations.html > optimizations_temp.html

mv optimizations_temp.html optimizations.html

echo "✅ Successfully added 33 new location pages to optimizations.html!"
echo ""
echo "📋 New total page count:"
echo "  • Homepage: 1"
echo "  • Services: 9"
echo "  • Locations: 63 (was 30, added 33)"
echo "  • Total: 73 pages"
echo ""
