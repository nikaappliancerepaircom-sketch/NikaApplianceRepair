/**
 * repair-malformed-jsonld.js — v2: nuke stray <script type=\"application/ld+json\">...</script>
 * patterns embedded inside JSON text values.
 *
 * The bug: a previous price-replace script wrapped `$` characters with `<script type="application/ld+json">`
 * tags inside FAQ "text" values. Some of those got further corrupted by a SECOND script run that
 * inserted an entire nested JSON-LD object between the open/close, so the corrupted region looks like:
 *   "text": "...costs <script type=\"application/ld+json\">20–{NESTED_JSON}</script>50 depending..."
 *
 * Approach: walk through HTML char-by-char. When we encounter `<script type="application/ld+json">`,
 * peek at what comes before. If preceded by JSON-string content (non-tag context), treat as stray
 * and remove from start of `<script>` through end of corresponding `</script>` PLUS any balanced
 * brace block in the middle. Replace with `$prefix$suffix` to recover price-text approximation.
 *
 * If preceded by a `>` character or whitespace at start of line (HTML-tag context), treat as
 * legitimate JSON-LD wrapper.
 *
 * Usage:
 *   node repair-malformed-jsonld.js --site=DIR [--limit=N] [--dry-run]
 */
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const arg = (n, def) => {
  const f = args.find(a => a.startsWith('--' + n + '='));
  return f ? f.slice(n.length + 3) : def;
};
const FLAG = (n) => args.includes('--' + n);

const SITE = arg('site');
const LIMIT = parseInt(arg('limit', '0'), 10);
const DRY = FLAG('dry-run');
if (!SITE) { console.error('Usage: --site=DIR [--limit=N] [--dry-run]'); process.exit(1); }

const SKIP_DIRS = new Set(['lazy-method', '_pages_queue', '_queue', 'node_modules', '.git', 'reports', 'backups']);
const SKIP_FILE_PATTERNS = [/-template\.html$/, /^landing-v/, /^index-optimized/];

function walk(dir, list = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const e of entries) {
    if (e.isDirectory()) {
      if (SKIP_DIRS.has(e.name)) continue;
      walk(path.join(dir, e.name), list);
    } else if (e.isFile() && e.name.endsWith('.html')) {
      if (SKIP_FILE_PATTERNS.some(re => re.test(e.name))) continue;
      list.push(path.join(dir, e.name));
    }
  }
  return list;
}

const OPEN_TAG = '<script type="application/ld+json">';
const CLOSE_TAG = '</script>';

function isStrayContext(html, idx) {
  // Stray: opens INSIDE a JSON string. Check ~100 chars before for typical FAQ-text context.
  const before = html.slice(Math.max(0, idx - 120), idx);
  // Heuristic: stray injection is preceded by lowercase prose and a non-tag char
  if (/(cost|costs|fee|price|warranty|repair in|elements|valves|service|charge|—|–|\$\d|usually|typically|depending|under)\s*$/i.test(before)) return true;
  // Also stray if directly preceded by alphanumeric or punctuation (not `>` or whitespace at line-start)
  const lastNonWS = before.replace(/\s+$/, '').slice(-1);
  if (/[a-z\d.,;:!?—–]/i.test(lastNonWS)) return true;
  return false;
}

function findEndOfStray(html, openIdx) {
  // After the open tag, content may be: PREFIX_TEXT [{...nested JSON...}] [SUFFIX_TEXT] </script> [SUFFIX_NUM]
  // Walk forward, scanning for close tag and tracking brace depth.
  let i = openIdx + OPEN_TAG.length;
  let prefixEnd = -1;
  let braceStart = -1;
  // Find first `{` or close tag, whichever comes first (within 200 chars)
  while (i < html.length && i < openIdx + OPEN_TAG.length + 200) {
    if (html[i] === '{') { braceStart = i; break; }
    if (html.startsWith(CLOSE_TAG, i)) { prefixEnd = i; break; }
    i++;
  }
  let prefix = '';
  let closeIdx = -1;
  if (braceStart !== -1) {
    prefix = html.slice(openIdx + OPEN_TAG.length, braceStart);
    // Balanced brace scan
    let depth = 0, p = braceStart, inStr = false, esc = false;
    for (; p < html.length; p++) {
      const c = html[p];
      if (esc) { esc = false; continue; }
      if (c === '\\') { esc = true; continue; }
      if (c === '"') { inStr = !inStr; continue; }
      if (inStr) continue;
      if (c === '{') depth++;
      else if (c === '}') { depth--; if (depth === 0) { p++; break; } }
    }
    // Now find close tag after balanced brace
    closeIdx = html.indexOf(CLOSE_TAG, p);
    if (closeIdx === -1) closeIdx = html.indexOf(CLOSE_TAG, openIdx);
  } else if (prefixEnd !== -1) {
    prefix = html.slice(openIdx + OPEN_TAG.length, prefixEnd);
    closeIdx = prefixEnd;
  } else {
    return null;
  }
  // Optional numeric suffix after </script>
  const after = closeIdx + CLOSE_TAG.length;
  const suffMatch = html.slice(after, after + 30).match(/^[\d.,]+/);
  const suffix = suffMatch ? suffMatch[0] : '';
  const endOfStray = after + (suffix ? suffix.length : 0);
  return { prefix: prefix.trim(), suffix, endOfStray };
}

function repairFile(html) {
  let cursor = 0;
  let out = '';
  let repaired = 0;
  while (true) {
    const idx = html.indexOf(OPEN_TAG, cursor);
    if (idx === -1) { out += html.slice(cursor); break; }
    if (!isStrayContext(html, idx)) {
      // Legitimate JSON-LD outer block — copy through start; advance cursor past open tag (continue scanning inside body)
      out += html.slice(cursor, idx + OPEN_TAG.length);
      cursor = idx + OPEN_TAG.length;
      continue;
    }
    // Stray injection
    const stray = findEndOfStray(html, idx);
    if (!stray) {
      // Couldn't repair; pass through
      out += html.slice(cursor, idx + OPEN_TAG.length);
      cursor = idx + OPEN_TAG.length;
      continue;
    }
    out += html.slice(cursor, idx) + '$' + stray.prefix + '$' + stray.suffix;
    cursor = stray.endOfStray;
    repaired++;
  }
  return { html: out, repaired };
}

const files = walk(SITE);
const sliced = LIMIT > 0 ? files.slice(0, LIMIT) : files;

let stats = { scanned: 0, fileRepaired: 0, totalReplacements: 0, stillMalformed: 0, malformed: [] };

for (const file of sliced) {
  stats.scanned++;
  let html = fs.readFileSync(file, 'utf8');
  const { html: newHtml, repaired } = repairFile(html);
  if (repaired > 0) {
    if (!DRY) fs.writeFileSync(file, newHtml);
    stats.fileRepaired++;
    stats.totalReplacements += repaired;
    html = newHtml;
  }
  const m = html.match(/<script\s+type=["']application\/ld\+json["']\s*>([\s\S]*?)<\/script>/);
  if (m) {
    try { JSON.parse(m[1]); }
    catch (err) {
      stats.stillMalformed++;
      if (stats.malformed.length < 8) stats.malformed.push(path.relative(SITE, file) + ' :: ' + err.message.slice(0, 70));
    }
  }
}

console.log('=== repair-malformed-jsonld.js v2 ===');
console.log('site         :', SITE);
console.log('dry          :', DRY);
console.log('scanned      :', stats.scanned);
console.log('files fixed  :', stats.fileRepaired);
console.log('replacements :', stats.totalReplacements);
console.log('still malformed:', stats.stillMalformed);
if (stats.malformed.length) {
  console.log('Examples:');
  stats.malformed.forEach(m => console.log('  -', m));
}
