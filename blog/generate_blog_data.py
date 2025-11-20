"""Generate blog data from actual HTML files"""
import os
import re
from pathlib import Path
from datetime import datetime, timedelta

def extract_title_from_html(filepath):
    """Extract title from HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Try to find h1 title
            match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
            if match:
                title = re.sub(r'<[^>]+>', '', match.group(1)).strip()
                return title
            # Fallback to filename
            return filepath.stem.replace('-', ' ').title()
    except:
        return filepath.stem.replace('-', ' ').title()

def categorize_file(filepath):
    """Determine category from path"""
    # Use parts to get the parent directory name (works on Windows & Unix)
    parts = filepath.parts
    if 'maintenance' in parts:
        return 'maintenance'
    elif 'troubleshooting' in parts:
        return 'troubleshooting'
    elif 'guides' in parts:
        return 'guides'
    return 'guides'

def generate_excerpt(title):
    """Generate simple excerpt from title"""
    category = title.lower()
    if 'repair' in category:
        return f"Expert {title.lower()} solutions for Toronto homeowners with professional tips and guidance."
    elif 'maintenance' in category:
        return f"Essential {title.lower()} tips to keep your appliances running smoothly."
    else:
        return f"Complete guide to {title.lower()} with step-by-step instructions."

# Get all blog HTML files
blog_dir = Path('C:/NikaApplianceRepair/blog')
blog_files = []

for category in ['guides', 'maintenance', 'troubleshooting']:
    category_path = blog_dir / category
    if category_path.exists():
        for html_file in category_path.glob('*.html'):
            if html_file.name != 'index.html':
                blog_files.append(html_file)

# Sort by name for consistency
blog_files.sort()

# Generate date (starting from recent and going back)
start_date = datetime(2025, 1, 15)

# Generate JavaScript array
print("const blogPosts = [")
for i, filepath in enumerate(blog_files):
    category = categorize_file(filepath)
    title = extract_title_from_html(filepath)

    # Generate URL with blog/ prefix since archive page is at root
    url = f"blog/{category}/{filepath.stem}.html"

    # Generate excerpt
    excerpt = generate_excerpt(title)

    # Generate date (go backwards from start date)
    date = (start_date - timedelta(days=i)).strftime('%Y-%m-%d')

    # Estimate read time based on title length (simple heuristic)
    read_time = f"{7 + (i % 6)} min"

    print(f"    {{category: '{category}', title: '{title}', url: '{url}', excerpt: '{excerpt}', date: '{date}', readTime: '{read_time}'}},")

print("];")
print(f"\n// Total posts: {len(blog_files)}")
