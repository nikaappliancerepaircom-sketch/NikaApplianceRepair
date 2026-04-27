"""Fix truncated FAQPage JSON-LD acceptedAnswer.text values.

The /locations/services/*.html pages have acceptedAnswer.text strings that were
cut off mid-sentence during generation. The visible FAQ in each page body has
the complete answer. This script finds each truncated schema answer and replaces
it with the matching full answer from the visible FAQ.
"""

import glob
import re
from pathlib import Path

ROOT = Path(__file__).parent
PATTERNS = [
    'locations/services/*.html',
]


def html_to_plain(html: str) -> str:
    text = re.sub(r'</?(p|br|strong|em|b|i|u|span|div|a|li|ul|ol)[^>]*>', ' ', html, flags=re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = (text
            .replace('&nbsp;', ' ')
            .replace('&amp;', '&')
            .replace('&quot;', '"')
            .replace('&#39;', "'")
            .replace('&lt;', '<')
            .replace('&gt;', '>'))
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def escape_json(text: str) -> str:
    return (text
            .replace('\\', '\\\\')
            .replace('"', '\\"')
            .replace('\n', ' ')
            .replace('\r', ''))


VISIBLE_FAQ_RE = re.compile(
    r'<div class="faq-item">\s*<div class="faq-question">([^<]+)</div>\s*<div class="faq-answer">(.*?)</div>\s*</div>',
    re.DOTALL,
)

SCHEMA_QA_RE = re.compile(
    r'(\{\s*"@type":\s*"Question",\s*"name":\s*")([^"]+)("\s*,\s*"acceptedAnswer":\s*\{\s*"@type":\s*"Answer",\s*"text":\s*")([^"]*)(")',
)


def fix_file(filepath: Path):
    original = filepath.read_text(encoding='utf-8')

    visible = {}
    for m in VISIBLE_FAQ_RE.finditer(original):
        q = m.group(1).strip()
        a = html_to_plain(m.group(2))
        visible[q] = a

    if not visible:
        return ('skipped', 0)

    changed = [0]

    def replace_match(m: re.Match) -> str:
        p1, qname, p3, schema_text, p5 = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
        trimmed = schema_text.strip()
        if not trimmed:
            return m.group(0)
        # Truncated if doesn't end with sentence-ending punctuation
        if re.search(r'[.!?]$', trimmed) or re.search(r'[.!?]"$', trimmed):
            return m.group(0)

        full = visible.get(qname.strip())
        if not full:
            # Fuzzy: prefix match against visible answers
            prefix = trimmed[:60]
            for vq, va in visible.items():
                if va.startswith(prefix):
                    full = va
                    break
        if not full:
            return m.group(0)

        changed[0] += 1
        return p1 + qname + p3 + escape_json(full) + p5

    new_content = SCHEMA_QA_RE.sub(replace_match, original)

    if changed[0] > 0 and new_content != original:
        filepath.write_text(new_content, encoding='utf-8')
    return ('ok', changed[0])


def main():
    files = []
    for pat in PATTERNS:
        files.extend(sorted(ROOT.glob(pat)))
    print(f'Scanning {len(files)} files...')
    files_changed = 0
    total_fixed = 0
    skipped = 0
    no_change = 0
    for f in files:
        status, count = fix_file(f)
        if status == 'skipped':
            skipped += 1
            continue
        if count > 0:
            files_changed += 1
            total_fixed += count
        else:
            no_change += 1
    print(f'\nDone.')
    print(f'Files modified: {files_changed}/{len(files)}')
    print(f'Total truncated answers fixed: {total_fixed}')
    print(f'Files with no truncation: {no_change}')
    print(f'Files skipped (no visible FAQ): {skipped}')


if __name__ == '__main__':
    main()
