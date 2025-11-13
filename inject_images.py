import json
import sys
import io
import chardet
from pathlib import Path

# Fix encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load mappings
with open("image_mappings.json") as f:
    mappings = json.load(f)

def inject_image(html_file, image_name):
    """Inject responsive image element into blog post"""
    
    file_path = Path(html_file)
    if not file_path.exists():
        return False
    
    # Detect encoding
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    
    detected = chardet.detect(raw_data)
    encoding = detected.get('encoding', 'utf-8')
    
    try:
        content = raw_data.decode(encoding)
    except:
        try:
            content = raw_data.decode('latin-1')
        except:
            return False
    
    # Check if image already injected
    if 'blog-images' in content:
        return False
    
    # Find position after </header>
    header_end = content.find('</header>')
    if header_end == -1:
        return False
    
    # Insert after header
    insert_pos = header_end + len('</header>')
    
    # Create responsive image HTML
    image_html = f'''
    <!-- Feature Image -->
    <section class="blog-feature-image">
        <picture>
            <source srcset="/blog-images/{image_name}.webp" type="image/webp">
            <source srcset="/blog-images/{image_name}.png" type="image/png">
            <img src="/blog-images/{image_name}.png" alt="Blog feature image" loading="lazy" width="1200" height="600">
        </picture>
    </section>
'''
    
    # Insert the image
    new_content = content[:insert_pos] + image_html + content[insert_pos:]
    
    # Write back with detected encoding
    with open(file_path, 'w', encoding=encoding) as f:
        f.write(new_content)
    
    return True

# Process each mapping
success_count = 0
fail_count = 0
for post_path, image_name in mappings.items():
    if inject_image(post_path, image_name):
        print(f"[OK] {post_path}")
        success_count += 1
    else:
        print(f"[SKIP] {post_path}")
        fail_count += 1

print(f"\nInjected images into {success_count} blog posts ({fail_count} skipped)")
