import os
from pathlib import Path

today = "2025-11-13"

# Start sitemap
lines = ["<?xml version='1.0' encoding='UTF-8'?>"]
lines.append("<ns0:urlset xmlns:ns0=\"http://www.sitemaps.org/schemas/sitemap/0.9\">")

# Root level pages
root_pages = [
    ("", 1.0, "weekly", "2025-11-13"),
    ("/about", 1.0, "weekly", "2025-11-06"),
    ("/services", 1.0, "weekly", "2025-11-13"),
    ("/locations", 0.9, "weekly", "2025-11-06"),
    ("/brands", 0.9, "weekly", "2025-11-06"),
    ("/book", 0.95, "weekly", "2025-11-13"),
    ("/team", 0.85, "monthly", "2025-11-06"),
    ("/optimizations", 0.7, "monthly", "2025-11-06"),
]

# Add root pages
for path, pri, freq, mod in root_pages:
    url = "https://nikaappliancerepair.com" + path
    lines.append("  <ns0:url>")
    lines.append(f"    <ns0:loc>{url}</ns0:loc>")
    lines.append(f"    <ns0:lastmod>{mod}</ns0:lastmod>")
    lines.append(f"    <ns0:changefreq>{freq}</ns0:changefreq>")
    lines.append(f"    <ns0:priority>{pri}</ns0:priority>")
    lines.append("  </ns0:url>")

# Blog archive page
lines.append("  <ns0:url>")
lines.append(f"    <ns0:loc>https://nikaappliancerepair.com/blog/</ns0:loc>")
lines.append(f"    <ns0:lastmod>{today}</ns0:lastmod>")
lines.append(f"    <ns0:changefreq>daily</ns0:changefreq>")
lines.append(f"    <ns0:priority>1.0</ns0:priority>")
lines.append("  </ns0:url>")

# Image gallery page
lines.append("  <ns0:url>")
lines.append(f"    <ns0:loc>https://nikaappliancerepair.com/blog/image-gallery.html</ns0:loc>")
lines.append(f"    <ns0:lastmod>{today}</ns0:lastmod>")
lines.append(f"    <ns0:changefreq>weekly</ns0:changefreq>")
lines.append(f"    <ns0:priority>0.95</ns0:priority>")
lines.append("  </ns0:url>")

# Brand pages
print("Finding brand pages...")
brand_count = 0
for f in sorted(Path("brands").glob("*.html")):
    url = "https://nikaappliancerepair.com/brands/" + f.name
    lines.append("  <ns0:url>")
    lines.append(f"    <ns0:loc>{url}</ns0:loc>")
    lines.append(f"    <ns0:lastmod>{today}</ns0:lastmod>")
    lines.append(f"    <ns0:changefreq>weekly</ns0:changefreq>")
    lines.append(f"    <ns0:priority>0.85</ns0:priority>")
    lines.append("  </ns0:url>")
    brand_count += 1

# Service pages
print("Finding service pages...")
service_count = 0
for f in sorted(Path("services").glob("*.html")):
    url = "https://nikaappliancerepair.com/services/" + f.name
    lines.append("  <ns0:url>")
    lines.append(f"    <ns0:loc>{url}</ns0:loc>")
    lines.append(f"    <ns0:lastmod>{today}</ns0:lastmod>")
    lines.append(f"    <ns0:changefreq>weekly</ns0:changefreq>")
    lines.append(f"    <ns0:priority>0.85</ns0:priority>")
    lines.append("  </ns0:url>")
    service_count += 1

# Location pages
print("Finding location pages...")
location_count = 0
for f in sorted(Path("locations").glob("*.html")):
    url = "https://nikaappliancerepair.com/locations/" + f.name
    lines.append("  <ns0:url>")
    lines.append(f"    <ns0:loc>{url}</ns0:loc>")
    lines.append(f"    <ns0:lastmod>{today}</ns0:lastmod>")
    lines.append(f"    <ns0:changefreq>weekly</ns0:changefreq>")
    lines.append(f"    <ns0:priority>0.9</ns0:priority>")
    lines.append("  </ns0:url>")
    location_count += 1

# Blog posts
print("Finding blog posts...")
blog_count = 0
for f in sorted(Path("blog").rglob("*.html")):
    s = str(f).replace("\\", "/")
    if any(x in s for x in ["_drafts", "template", "backup", "test-components", "premium-blog"]):
        continue
    if f.name in ["index.html", "image-gallery.html"]:
        continue
    url = "https://nikaappliancerepair.com/" + s
    lines.append("  <ns0:url>")
    lines.append(f"    <ns0:loc>{url}</ns0:loc>")
    lines.append(f"    <ns0:lastmod>{today}</ns0:lastmod>")
    lines.append(f"    <ns0:changefreq>weekly</ns0:changefreq>")
    lines.append(f"    <ns0:priority>0.9</ns0:priority>")
    lines.append("  </ns0:url>")
    blog_count += 1

lines.append("</ns0:urlset>")

with open("sitemap.xml", "w") as f:
    f.write("\n".join(lines))

total = len(root_pages) + 2 + brand_count + service_count + location_count + blog_count
print(f"\nGenerated complete sitemap:")
print(f"  Root pages: {len(root_pages)}")
print(f"  Blog pages: 2 (archive + gallery)")
print(f"  Brand pages: {brand_count}")
print(f"  Service pages: {service_count}")
print(f"  Location pages: {location_count}")
print(f"  Blog posts: {blog_count}")
print(f"  TOTAL: {total} URLs")

