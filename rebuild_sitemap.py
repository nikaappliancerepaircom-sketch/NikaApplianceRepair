import os
from pathlib import Path

today = "2025-11-13"

# Start sitemap
lines = ["<?xml version='1.0' encoding='UTF-8'?>"]
lines.append("<ns0:urlset xmlns:ns0=\"http://www.sitemaps.org/schemas/sitemap/0.9\">")

# Main pages
main = [
    ("https://nikaappliancerepair.com", "2025-11-13", "weekly", "1.0"),
    ("https://nikaappliancerepair.com/about", "2025-11-06", "weekly", "1.0"),
    ("https://nikaappliancerepair.com/services", "2025-11-13", "weekly", "1.0"),
    ("https://nikaappliancerepair.com/locations", "2025-11-06", "weekly", "0.9"),
    ("https://nikaappliancerepair.com/brands", "2025-11-05", "monthly", "0.9"),
    ("https://nikaappliancerepair.com/blog/", "2025-11-13", "daily", "1.0"),
    ("https://nikaappliancerepair.com/blog/image-gallery.html", "2025-11-13", "weekly", "0.95"),
]

for url, mod, freq, pri in main:
    lines.append("  <ns0:url>")
    lines.append(f"    <ns0:loc>{url}</ns0:loc>")
    lines.append(f"    <ns0:lastmod>{mod}</ns0:lastmod>")
    lines.append(f"    <ns0:changefreq>{freq}</ns0:changefreq>")
    lines.append(f"    <ns0:priority>{pri}</ns0:priority>")
    lines.append("  </ns0:url>")

# Find all blog posts
blog_files = []
for f in Path("blog").rglob("*.html"):
    s = str(f).replace("\\", "/")
    if any(x in s for x in ["_drafts", "template", "backup", "test-components", "premium-blog"]):
        continue
    if f.name in ["index.html", "image-gallery.html"]:
        continue
    blog_files.append(s)

# Add blog posts
for f in sorted(blog_files):
    url = "https://nikaappliancerepair.com/" + f
    lines.append("  <ns0:url>")
    lines.append(f"    <ns0:loc>{url}</ns0:loc>")
    lines.append(f"    <ns0:lastmod>{today}</ns0:lastmod>")
    lines.append(f"    <ns0:changefreq>weekly</ns0:changefreq>")
    lines.append(f"    <ns0:priority>0.9</ns0:priority>")
    lines.append("  </ns0:url>")

lines.append("</ns0:urlset>")

with open("sitemap.xml", "w") as f:
    f.write("\n".join(lines))

print(f"Generated sitemap with {len(main) + len(blog_files)} URLs")
print(f"Main pages: {len(main)}")
print(f"Blog posts: {len(blog_files)}")

