/**
 * inline-footer.js — Inline /includes/footer.html into static HTML before <div id="footer-placeholder">.
 *
 * Why: footer-loader.js fetches footer.html at runtime via JS. Crawlers (and the lazy-method audit
 * checker) read raw HTML and never see footer content, so all footer-trust-strip checks fail.
 *
 * Strategy: read footer.html once, walk all .html files, replace
 *   <div id="footer-placeholder"></div>
 * with
 *   <div id="footer-placeholder">[FOOTER HTML]</div><!-- FOOTER-INLINED-v1 -->
 *
 * Idempotent via FOOTER-INLINED-v1 marker. The JS loader can still run (it overwrites the inlined
 * content with the same content from footer.html — net zero, but ensures any future footer.html
 * edits still propagate to clients without requiring a re-inline).
 *
 * Usage:
 *   node inline-footer.js --site=DIR [--limit=N] [--dry-run]
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

if (!SITE) {
  console.error('Usage: --site=DIR [--limit=N] [--dry-run]');
  process.exit(1);
}

const FOOTER_PATH = path.join(SITE, 'includes', 'footer.html');
if (!fs.existsSync(FOOTER_PATH)) {
  console.error('No footer at:', FOOTER_PATH);
  process.exit(1);
}
const FOOTER_HTML = fs.readFileSync(FOOTER_PATH, 'utf8').trim();

const MARKER = '<!-- FOOTER-INLINED-v1 -->';
const PLACEHOLDER_RE = /<div\s+id=["']footer-placeholder["']\s*>\s*<\/div>/i;
// Match ALSO an already-inlined version so we can re-inline (refresh) without leaving stale content.
const INLINED_RE = /<div\s+id=["']footer-placeholder["']\s*>[\s\S]*?<\/div>\s*<!--\s*FOOTER-INLINED-v1\s*-->/i;

const SKIP_DIRS = new Set(['lazy-method', '_pages_queue', '_queue', 'node_modules', '.git', 'reports', 'backups', 'includes']);
const SKIP_FILE_PATTERNS = [/-template\.html$/, /^landing-v/, /^index-optimized/, /^preview/, /^compare/];

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

const files = walk(SITE);
const sliced = LIMIT > 0 ? files.slice(0, LIMIT) : files;

let stats = { scanned: 0, inlined: 0, refreshed: 0, noPlaceholder: 0 };
const replacement = `<div id="footer-placeholder">${FOOTER_HTML}</div>${MARKER}`;

for (const file of sliced) {
  stats.scanned++;
  let html = fs.readFileSync(file, 'utf8');

  // Already-inlined: refresh
  if (INLINED_RE.test(html)) {
    html = html.replace(INLINED_RE, replacement);
    if (!DRY) fs.writeFileSync(file, html);
    stats.refreshed++;
    continue;
  }

  // First-time inline: replace empty placeholder
  if (PLACEHOLDER_RE.test(html)) {
    html = html.replace(PLACEHOLDER_RE, replacement);
    if (!DRY) fs.writeFileSync(file, html);
    stats.inlined++;
    continue;
  }

  stats.noPlaceholder++;
}

console.log('=== inline-footer.js ===');
console.log('site         :', SITE);
console.log('footer source:', FOOTER_PATH, `(${FOOTER_HTML.length} chars)`);
console.log('dry          :', DRY);
console.log('scanned      :', stats.scanned);
console.log('first-inline :', stats.inlined);
console.log('refreshed    :', stats.refreshed);
console.log('no placehold :', stats.noPlaceholder);
