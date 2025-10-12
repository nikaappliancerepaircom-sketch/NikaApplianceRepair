#!/bin/bash

echo "🚀 Creating 33 missing location pages with BMAD optimization..."

# Define missing locations (slug | Display Name)
declare -a locations=(
    "agincourt|Agincourt"
    "bayview-glen|Bayview Glen"
    "berczy-village|Berczy Village"
    "beverley-glen|Beverley Glen"
    "bradford|Bradford"
    "beverley-acres|Beverley Acres"
    "cachet|Cachet"
    "cathedraltown|Cathedraltown"
    "calgary|Calgary"
    "barrie|Barrie"
    "bolton|Bolton"
    "caledon|Caledon"
    "don-valley-village|Don Valley Village"
    "elgin-mills|Elgin Mills"
    "east-york|East York"
    "edmonton|Edmonton"
    "greensborough|Greensborough"
    "gta|GTA"
    "gormley|Gormley"
    "hillcrest-village|Hillcrest Village"
    "innisfil|Innisfil"
    "kleinburg|Kleinburg"
    "holland-landing|Holland Landing"
    "langstaff|Langstaff"
    "lamoreaux|Lamoreaux"
    "mount-albert|Mount Albert"
    "milliken|Milliken"
    "oak-ridges|Oak Ridges"
    "richvale|Richvale"
    "raymerville-markville-east|Raymerville Markville East"
    "steeles|Steeles"
    "schomberg|Schomberg"
    "unionville|Unionville"
    "wismer-commons|Wismer Commons"
    "yongehurst|Yongehurst"
    "halton-hills|Halton Hills"
)

# Read ajax.html as template
template_file="locations/ajax.html"

if [ ! -f "$template_file" ]; then
    echo "❌ Error: Template file $template_file not found!"
    exit 1
fi

# Counter
count=0

# Create each location page
for location_pair in "${locations[@]}"; do
    IFS='|' read -r slug display_name <<< "$location_pair"
    output_file="locations/${slug}.html"

    # Skip if file already exists
    if [ -f "$output_file" ]; then
        echo "  ⏭️  Skipping $display_name (already exists)"
        continue
    fi

    echo "  📄 Creating: $display_name → $output_file"

    # Copy template and replace Ajax with location name
    sed "s/Ajax/${display_name}/g" "$template_file" | \
    sed "s/ajax/${slug}/g" > "$output_file"

    ((count++))
done

echo ""
echo "✅ Created $count new location pages!"
echo ""
echo "📋 Summary:"
echo "  • Total pages created: $count"
echo "  • All pages have BMAD optimization (inherited from ajax.html template)"
echo "  • All pages have PageSpeed optimization CSS files"
echo "  • All pages have accessibility features"
echo ""
