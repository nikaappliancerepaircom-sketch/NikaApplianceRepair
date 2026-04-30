/**
 * inject-trust-strip-universal.js — Inject trust strip HTML inline on EVERY page,
 * regardless of whether the page uses footer-loader.js or has a hard-coded <footer>.
 *
 * Strategy:
 *   - If page has FOOTER-INLINED-v1 marker (placeholder already inlined): skip — strip is in inlined footer.
 *   - Else if page has TRUST-STRIP-INLINE-v1 marker: skip — already injected.
 *   - Else: inject trust strip HTML right BEFORE `<footer` (or before `</body>` if no footer tag).
 *     Mark with TRUST-STRIP-INLINE-v1.
 *
 * Trust strip content matches the footer trust strip (license badge, directions, authority links,
 * definition list, legal links).
 *
 * Usage:
 *   node inject-trust-strip-universal.js --site=DIR --map=CITY [--dry-run]
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
const MAP_CITY = arg('map', 'Toronto+Ontario+Canada');
const LIMIT = parseInt(arg('limit', '0'), 10);
const DRY = FLAG('dry-run');

if (!SITE) {
  console.error('Usage: --site=DIR --map=CITY [--limit=N] [--dry-run]');
  process.exit(1);
}

const MARKER = '<!-- TRUST-STRIP-INLINE-v1 -->';
const ALREADY_INLINED_MARKER = 'FOOTER-INLINED-v1';

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

const TRUST_STRIP = `${MARKER}
<aside class="lz-inline-trust" role="complementary" aria-label="Trust signals" style="max-width:980px;margin:32px auto 16px;padding:18px 20px;border-top:1px solid rgba(15,23,42,0.08);font-size:13px;line-height:1.6;color:#475569;">
  <p style="margin:0 0 10px;display:flex;flex-wrap:wrap;gap:6px 14px;justify-content:center;align-items:center;">
    <span style="display:inline-flex;align-items:center;gap:4px;padding:4px 10px;border:1px solid rgba(15,23,42,0.12);border-radius:999px;font-weight:600;color:#0f172a;background:#fff;font-size:12px;">🛡 TSSA Licensed</span>
    <span style="display:inline-flex;align-items:center;gap:4px;padding:4px 10px;border:1px solid rgba(15,23,42,0.12);border-radius:999px;font-weight:600;color:#0f172a;background:#fff;font-size:12px;">✓ Insured &amp; Bonded</span>
    <span style="display:inline-flex;align-items:center;gap:4px;padding:4px 10px;border:1px solid rgba(15,23,42,0.12);border-radius:999px;font-weight:600;color:#0f172a;background:#fff;font-size:12px;">⏱ Same-Day Service</span>
    <span style="display:inline-flex;align-items:center;gap:4px;padding:4px 10px;border:1px solid rgba(15,23,42,0.12);border-radius:999px;font-weight:600;color:#0f172a;background:#fff;font-size:12px;">📞 Free Diagnostic with Repair</span>
    <a href="https://www.google.com/maps/dir/?api=1&amp;destination=${MAP_CITY}" target="_blank" rel="noopener" style="color:#2563eb;font-weight:600;text-decoration:none;">📍 Get directions</a>
  </p>
  <p style="margin:0 0 10px;font-size:12px;color:#64748b;text-align:center;">Resources we cite:
    <a href="https://natural-resources.canada.ca/energy-efficiency/energy-star-canada/18953" target="_blank" rel="noopener nofollow" style="color:#64748b;">Energy Star Canada</a> ·
    <a href="https://www.csagroup.org/" target="_blank" rel="noopener nofollow" style="color:#64748b;">CSA Group</a> ·
    <a href="https://www.lg.com/ca_en/support" target="_blank" rel="noopener nofollow" style="color:#64748b;">LG Support</a> ·
    <a href="https://www.samsung.com/ca/support/" target="_blank" rel="noopener nofollow" style="color:#64748b;">Samsung Support</a> ·
    <a href="https://www.whirlpool.com/services.html" target="_blank" rel="noopener nofollow" style="color:#64748b;">Whirlpool Support</a>
  </p>
  <dl style="max-width:760px;margin:8px auto 10px;font-size:12px;color:#64748b;text-align:left;">
    <dt style="font-weight:700;color:#1e293b;margin-top:6px;">Diagnostic fee</dt>
    <dd style="margin:0 0 4px 12px;">One-time visit charge that we waive when you proceed with the repair.</dd>
    <dt style="font-weight:700;color:#1e293b;margin-top:6px;">Same-day service</dt>
    <dd style="margin:0 0 4px 12px;">Book before 12 PM on a weekday and our technician typically arrives the same day.</dd>
    <dt style="font-weight:700;color:#1e293b;margin-top:6px;">90-day warranty</dt>
    <dd style="margin:0 0 4px 12px;">All parts replaced and labour performed are covered for 90 days from the repair date.</dd>
  </dl>
  <p style="margin:0;text-align:center;font-size:12px;color:#94a3b8;">
    <a href="/privacy" style="color:#64748b;">Privacy Policy</a> ·
    <a href="/terms" style="color:#64748b;">Terms of Service</a> ·
    <a href="/accessibility" style="color:#64748b;">Accessibility</a>
  </p>
</aside>
<!-- END-TRUST-STRIP-INLINE-v1 -->`;

const files = walk(SITE);
const sliced = LIMIT > 0 ? files.slice(0, LIMIT) : files;

let stats = { scanned: 0, injected: 0, alreadyDone: 0, alreadyInFooter: 0, noAnchor: 0 };

for (const file of sliced) {
  stats.scanned++;
  let html = fs.readFileSync(file, 'utf8');

  if (html.includes(MARKER)) { stats.alreadyDone++; continue; }
  if (html.includes(ALREADY_INLINED_MARKER)) { stats.alreadyInFooter++; continue; }

  // Anchor: prefer </main>, then before <footer, then before </body>
  let idx = html.search(/<\/main>/i);
  if (idx === -1) idx = html.search(/<footer[\s>]/i);
  if (idx === -1) idx = html.search(/<\/body>/i);
  if (idx === -1) { stats.noAnchor++; continue; }

  html = html.slice(0, idx) + TRUST_STRIP + '\n' + html.slice(idx);

  if (!DRY) fs.writeFileSync(file, html);
  stats.injected++;
}

console.log('=== inject-trust-strip-universal.js ===');
console.log('site             :', SITE);
console.log('map city         :', MAP_CITY);
console.log('dry              :', DRY);
console.log('scanned          :', stats.scanned);
console.log('injected         :', stats.injected);
console.log('already inline   :', stats.alreadyDone);
console.log('already in footer:', stats.alreadyInFooter);
console.log('no anchor        :', stats.noAnchor);
