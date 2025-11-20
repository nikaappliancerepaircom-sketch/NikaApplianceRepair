"""Check all blog posts for HTML issues"""
import os
import re
from pathlib import Path
from html.parser import HTMLParser

class BlogHTMLChecker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tag_stack = []
        self.errors = []
        self.warnings = []

    def handle_starttag(self, tag, attrs):
        # Track opening tags
        if tag not in ['img', 'br', 'hr', 'meta', 'link', 'source', 'input']:
            self.tag_stack.append(tag)

    def handle_endtag(self, tag):
        # Check for matching closing tags
        if self.tag_stack and self.tag_stack[-1] == tag:
            self.tag_stack.pop()
        elif tag in self.tag_stack:
            self.errors.append(f"Mismatched closing tag: </{tag}>, expected </{self.tag_stack[-1]}>")
        else:
            self.warnings.append(f"Unexpected closing tag: </{tag}>")

def check_picture_tags(filepath):
    """Check for mismatched picture/source tags"""
    issues = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

        # Find all picture elements
        picture_pattern = r'<picture>.*?</picture>'
        pictures = re.findall(picture_pattern, content, re.DOTALL)

        for i, pic in enumerate(pictures):
            # Extract srcset and img src
            srcset_match = re.search(r'srcset="([^"]+)"', pic)
            img_src_match = re.search(r'<img[^>]+src="([^"]+)"', pic)

            if srcset_match and img_src_match:
                srcset = srcset_match.group(1)
                img_src = img_src_match.group(1)

                # Check if they're different (might indicate mismatch)
                if srcset != img_src:
                    # Extract just filenames
                    srcset_file = os.path.basename(srcset)
                    img_file = os.path.basename(img_src)

                    if srcset_file != img_file:
                        issues.append({
                            'type': 'picture_mismatch',
                            'detail': f"Picture #{i+1}: srcset={srcset_file}, img={img_file}"
                        })

    return issues

def check_html_structure(filepath):
    """Check basic HTML structure"""
    issues = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        parser = BlogHTMLChecker()
        parser.feed(content)

        # Check for unclosed tags
        if parser.tag_stack:
            issues.append({
                'type': 'unclosed_tags',
                'detail': f"Unclosed tags: {', '.join(parser.tag_stack)}"
            })

        # Add parser errors
        for error in parser.errors:
            issues.append({
                'type': 'structure_error',
                'detail': error
            })

    except Exception as e:
        issues.append({
            'type': 'parse_error',
            'detail': str(e)
        })

    return issues

def check_blog_posts():
    blog_dir = Path('C:/NikaApplianceRepair/blog')
    all_issues = {}

    for category in ['guides', 'maintenance', 'troubleshooting']:
        category_path = blog_dir / category
        if not category_path.exists():
            continue

        for html_file in category_path.glob('*.html'):
            if html_file.name == 'index.html':
                continue

            issues = []

            # Check picture tags
            picture_issues = check_picture_tags(html_file)
            issues.extend(picture_issues)

            # Check HTML structure
            structure_issues = check_html_structure(html_file)
            issues.extend(structure_issues)

            if issues:
                all_issues[f"{category}/{html_file.name}"] = issues

    # Print results
    if not all_issues:
        print("[OK] No issues found in blog posts!")
    else:
        print(f"\n[FOUND] {len(all_issues)} blog posts with issues:\n")
        for filepath, issues in all_issues.items():
            print(f"\n{filepath}:")
            for issue in issues:
                print(f"  [{issue['type']}] {issue['detail']}")

    return all_issues

if __name__ == '__main__':
    check_blog_posts()
