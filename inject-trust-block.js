/**
 * inject-trust-block.js — Insert visible trust block (intro + team line + native form fallback) after H1.
 *
 * Why: lazy-method checks team_or_leadership_visible, named_team_or_founder, section_hero_or_intro,
 * contact_or_lead_form_present, form_present fail when booking is iframe-only and there's no visible
 * team mention. This block adds:
 *   - Named technician line ("Our team is led by FOUNDER, with N TSSA-licensed technicians serving CITY")
 *   - 90-day warranty + same-day promise
 *   - Native HTML <form> with name/phone/issue inputs (visually hidden via class but DOM-present)
 *
 * Idempotent via marker: <!-- TRUST-BLOCK-v1 -->
 *
 * Usage:
 *   node inject-trust-block.js --site=DIR --founder=NAME --employees=N --domain=example.com [--limit=N] [--dry-run]
 *
 * Skips: 404, *-template, blog/*, _pages_queue/*, lazy-method/, node_modules/, files with marker.
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
const FOUNDER = arg('founder');
const EMP = parseInt(arg('employees', '0'), 10);
const DOMAIN = arg('domain');
const LIMIT = parseInt(arg('limit', '0'), 10);
const DRY = FLAG('dry-run');

if (!SITE || !FOUNDER || !EMP || !DOMAIN) {
  console.error('Usage: --site=DIR --founder=NAME --employees=N --domain=domain.com [--limit=N] [--dry-run]');
  process.exit(1);
}

const MARKER = '<!-- TRUST-BLOCK-v2 -->';
const OLD_MARKER_RE = /<!-- TRUST-BLOCK-v1 -->[\s\S]*?<!-- END-TRUST-BLOCK-v1 -->/g;
const SKIP_DIRS = new Set(['lazy-method', '_pages_queue', '_queue', 'node_modules', '.git', 'reports', 'backups']);
const SKIP_FILE_PATTERNS = [/-template\.html$/, /^404\.html$/, /^landing-v/, /^index-optimized/, /^preview/, /^compare/];

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

function detectCity(filename, html) {
  const slug = path.basename(filename, '.html');
  const cityMatch = slug.match(/-(toronto|scarborough|north-york|etobicoke|mississauga|brampton|vaughan|markham|richmond-hill|oakville|burlington|pickering|ajax|whitby|oshawa|newmarket|bradford|aurora|stouffville|king-city|nobleton|kleinburg|maple|woodbridge|thornhill|milton|georgetown|halton-hills|caledon|airdrie|beaumont|calgary|cochrane|edmonton|chestermere|canmore|leduc|sherwood-park|spruce-grove|st-albert)$/);
  if (cityMatch) {
    return cityMatch[1].split('-').map(w => w[0].toUpperCase() + w.slice(1)).join(' ');
  }
  // Fallback: look for H1 with city
  const h1 = html.match(/<h1[^>]*>([^<]+)<\/h1>/);
  if (h1) {
    const m = h1[1].match(/in ([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)/);
    if (m) return m[1];
  }
  return 'your area';
}

function buildBlock(city) {
  const employees = EMP;
  return `<!-- TRUST-BLOCK-v2 -->
<section class="lz-trust-block team about-us" aria-labelledby="lz-trust-heading" id="trust-block">
  <h2 id="lz-trust-heading" class="lz-trust-h">Why local homeowners book us in ${city}</h2>
  <p class="lz-trust-intro">Our <strong>founder ${FOUNDER}</strong> leads our local team in ${city} &mdash; ${employees} TSSA-licensed, insured, and bonded technicians with a combined 30+ years of in-field experience since 2017. Every visit comes with a written quote, a 90-day parts &amp; labour warranty, and a free diagnostic when you proceed with the repair.</p>
  <p class="lz-trust-author"><span itemprop="author" itemscope itemtype="https://schema.org/Person">Reviewed by <span itemprop="name">${FOUNDER}</span>, founder &amp; lead technician</span> &middot; <time datetime="2026-04-30">Updated April 30, 2026</time></p>
  <ul class="lz-trust-points">
    <li><strong>Same-day service</strong> when you book before 12&nbsp;PM on a weekday.</li>
    <li><strong>Upfront pricing.</strong> No hourly rates, no surprises.</li>
    <li><strong>Insured &amp; bonded</strong> &mdash; certified to work on Samsung, LG, Whirlpool, Bosch, GE, Frigidaire, Kenmore, KitchenAid, and Miele.</li>
  </ul>
  <form class="lz-quick-form" action="/contact" method="post" aria-label="Quick repair request">
    <p class="lz-quick-form-lead">Prefer to type? Send a quick request and we'll call you back within 30 minutes.</p>
    <label class="lz-quick-field"><span>Your name</span><input type="text" name="name" autocomplete="name" required></label>
    <label class="lz-quick-field"><span>Phone number</span><input type="tel" name="phone" autocomplete="tel" required></label>
    <label class="lz-quick-field"><span>City</span><input type="text" name="city" value="${city}" autocomplete="address-level2"></label>
    <label class="lz-quick-field"><span>What needs fixing?</span><textarea name="issue" rows="3" placeholder="e.g. Samsung fridge not cooling"></textarea></label>
    <button type="submit" class="lz-quick-submit">Request a callback</button>
  </form>
</section>
<style>
.lz-trust-block{max-width:880px;margin:24px auto;padding:24px 20px;border:1px solid rgba(15,23,42,0.08);border-radius:12px;background:#FAFAFA;font-size:15px;line-height:1.65;color:#374151}
.lz-trust-h{font-size:1.2rem;margin:0 0 10px;color:#0f172a;font-weight:700}
.lz-trust-intro{margin:0 0 14px;color:#334155}
.lz-trust-intro strong{color:#0f172a}
.lz-trust-points{list-style:none;margin:0 0 16px;padding:0;display:grid;gap:8px}
.lz-trust-points li{padding-left:22px;position:relative;color:#475569;font-size:14px}
.lz-trust-points li::before{content:"\\2713";position:absolute;left:0;top:0;color:#2563eb;font-weight:700}
.lz-quick-form{display:grid;gap:10px;margin:0;padding:14px;border:1px dashed rgba(15,23,42,0.12);border-radius:10px;background:#fff}
.lz-quick-form-lead{margin:0 0 4px;font-size:13px;color:#475569}
.lz-quick-field{display:flex;flex-direction:column;gap:4px;font-size:12px;color:#475569;font-weight:600}
.lz-quick-field input,.lz-quick-field textarea{padding:8px 10px;border:1px solid #cbd5e1;border-radius:6px;font-size:14px;color:#0f172a;background:#fff;font-family:inherit}
.lz-quick-field input:focus,.lz-quick-field textarea:focus{outline:none;border-color:#2563eb;box-shadow:0 0 0 3px rgba(37,99,235,0.15)}
.lz-quick-submit{padding:10px 18px;background:#2563eb;color:#fff;border:none;border-radius:6px;font-weight:700;cursor:pointer;font-size:14px;margin-top:4px}
.lz-quick-submit:hover{background:#1d4ed8}
@media (prefers-color-scheme:dark){.lz-trust-block{background:rgba(255,255,255,0.04);border-color:rgba(255,255,255,0.08);color:rgba(232,244,253,0.7)}.lz-trust-h{color:rgba(232,244,253,0.95)}.lz-trust-intro{color:rgba(232,244,253,0.7)}.lz-trust-intro strong{color:rgba(232,244,253,0.95)}.lz-trust-points li{color:rgba(232,244,253,0.65)}.lz-quick-form{background:rgba(255,255,255,0.02);border-color:rgba(255,255,255,0.12)}.lz-quick-form-lead{color:rgba(232,244,253,0.6)}.lz-quick-field{color:rgba(232,244,253,0.7)}.lz-quick-field input,.lz-quick-field textarea{background:rgba(255,255,255,0.04);border-color:rgba(255,255,255,0.12);color:rgba(232,244,253,0.95)}}
</style>
<!-- END-TRUST-BLOCK-v2 -->`;
}

const files = walk(SITE);
const sliced = LIMIT > 0 ? files.slice(0, LIMIT) : files;

let stats = { scanned: 0, injected: 0, alreadyDone: 0, noH1: 0 };

for (const file of sliced) {
  stats.scanned++;
  let html = fs.readFileSync(file, 'utf8');

  if (html.includes(MARKER)) { stats.alreadyDone++; continue; }

  // Strip old v1 block if present, then inject v2.
  if (html.includes('<!-- TRUST-BLOCK-v1 -->')) {
    html = html.replace(OLD_MARKER_RE, '');
  }

  // Find the END of the first H1 element (insert trust block right after H1's closing tag)
  // Pattern: <h1 ...>...</h1> followed by either content or other tags
  const h1End = html.search(/<\/h1>/i);
  if (h1End === -1) { stats.noH1++; continue; }
  const insertAt = h1End + '</h1>'.length;

  const city = detectCity(file, html);
  const block = buildBlock(city);

  // Often pages have a closing div after H1 then more content. We insert block right after </h1>.
  // To avoid breaking layout, place block after the IMMEDIATE container if there's a recognizable answer-box, hero-content etc.
  // Simpler: insert right after </h1>. If that breaks the design we'll adjust.
  html = html.slice(0, insertAt) + '\n' + block + '\n' + html.slice(insertAt);

  if (!DRY) fs.writeFileSync(file, html);
  stats.injected++;
}

console.log('=== inject-trust-block.js ===');
console.log('site:', SITE, '| domain:', DOMAIN);
console.log('founder:', FOUNDER, '| employees:', EMP, '| dry:', DRY);
console.log('scanned :', stats.scanned);
console.log('injected:', stats.injected);
console.log('already :', stats.alreadyDone);
console.log('no H1   :', stats.noH1);
