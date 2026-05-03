/**
 * regen-jsonld.js — Regenerate clean JSON-LD on pages where the existing block is unparseable.
 *
 * For each .html file:
 *   - Try to JSON.parse the first <script type="application/ld+json"> body.
 *   - If parses OK: skip.
 *   - If unparseable: strip the entire malformed block and replace with a fresh @graph
 *     containing LocalBusiness + Service (if service detected) + FAQPage (3 generic Qs) + BreadcrumbList.
 *
 * Page metadata extracted: title, description, canonical, H1, filename-derived brand/service/city.
 * Site-level data: name, phone, email, address from lazy-config.json.
 *
 * Usage:
 *   node regen-jsonld.js --site=DIR [--limit=N] [--dry-run]
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

const cfg = JSON.parse(fs.readFileSync(path.join(SITE, 'lazy-config.json'), 'utf8'));
const SITE_NAME = cfg.site.name;
const DOMAIN = cfg.site.domain;
const PHONE = cfg.contact.phone;
const EMAIL = cfg.contact.email;
const ADDRESS = cfg.contact.address;
const REVIEW_COUNT = cfg.business.review_count || 250;
const RATING = cfg.business.rating || 4.9;
const TEAM_SIZE = cfg.business.team_size || 8;

const SKIP_DIRS = new Set(['lazy-method', '_pages_queue', '_queue', 'node_modules', '.git', 'reports', 'backups', 'includes']);
const SKIP_FILE_PATTERNS = [/-template\.html$/, /^landing-v/, /^index-optimized/, /^preview/, /^compare/];

const BRANDS = ['samsung', 'lg', 'whirlpool', 'bosch', 'ge', 'frigidaire', 'kenmore', 'maytag', 'kitchenaid', 'miele', 'amana', 'electrolux', 'fisher-paykel', 'thermador', 'viking', 'sub-zero', 'wolf', 'jenn-air', 'haier', 'panasonic', 'sharp', 'danby', 'hotpoint'];
const SERVICES = {
  fridge: 'Refrigerator Repair',
  refrigerator: 'Refrigerator Repair',
  freezer: 'Freezer Repair',
  washer: 'Washer Repair',
  dryer: 'Dryer Repair',
  dishwasher: 'Dishwasher Repair',
  oven: 'Oven Repair',
  stove: 'Stove Repair',
  range: 'Range Repair',
  microwave: 'Microwave Repair',
};
const CITIES = ['toronto','scarborough','north-york','etobicoke','mississauga','brampton','vaughan','markham','richmond-hill','oakville','burlington','pickering','ajax','whitby','oshawa','newmarket','bradford','aurora','stouffville','king-city','nobleton','kleinburg','maple','woodbridge','thornhill','milton','georgetown','halton-hills','caledon','airdrie','beaumont','calgary','cochrane','edmonton','chestermere','canmore','leduc','sherwood-park','spruce-grove','st-albert','devon','fort-saskatchewan'];

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

function detectFromSlug(slug) {
  let brand = null, service = null, city = null;
  // Sort by length DESC to match longest brand/city first
  for (const b of [...BRANDS].sort((a, b) => b.length - a.length)) {
    if (slug.includes(b)) { brand = b; break; }
  }
  for (const c of [...CITIES].sort((a, b) => b.length - a.length)) {
    if (slug === c || slug.endsWith('-' + c)) { city = c; break; }
  }
  for (const s of Object.keys(SERVICES).sort((a, b) => b.length - a.length)) {
    if (slug.includes(s)) { service = s; break; }
  }
  return { brand, service, city };
}

function titleCase(s) {
  return s.replace(/(^|\s|-)([a-z])/g, (m, p, c) => p.replace('-', ' ') + c.toUpperCase());
}

function buildGraph({ pageUrl, title, description, brand, service, city, h1 }) {
  const cityName = city ? titleCase(city) : 'Toronto';
  const brandName = brand ? titleCase(brand) : null;
  const serviceName = service ? SERVICES[service] : null;
  const fullServiceName = brandName && serviceName ? `${brandName} ${serviceName}` : (serviceName || 'Appliance Repair');

  const graph = [];

  // 1. LocalBusiness
  graph.push({
    '@type': 'LocalBusiness',
    'name': SITE_NAME,
    'telephone': PHONE,
    'email': EMAIL,
    'url': `https://${DOMAIN}`,
    'priceRange': '$$',
    'datePublished': '2026-02-22',
    'dateModified': '2026-04-30',
    'address': {
      '@type': 'PostalAddress',
      'addressLocality': cityName,
      'addressRegion': 'Ontario',
      'addressCountry': 'CA',
    },
    'aggregateRating': {
      '@type': 'AggregateRating',
      'ratingValue': String(RATING),
      'reviewCount': String(REVIEW_COUNT),
    },
    'openingHours': ['Mo-Sa 08:00-20:00', 'Su 09:00-18:00'],
    'numberOfEmployees': { '@type': 'QuantitativeValue', 'value': TEAM_SIZE },
    'areaServed': { '@type': 'AdministrativeArea', 'name': cityName + ', Ontario, Canada' },
  });

  // 2. Service (if applicable)
  if (serviceName) {
    graph.push({
      '@type': 'Service',
      'serviceType': fullServiceName,
      'name': fullServiceName,
      'description': `Professional ${fullServiceName.toLowerCase()} in ${cityName} and the GTA. Same-day service, 90-day warranty, licensed technicians.`,
      'provider': { '@type': 'LocalBusiness', 'name': SITE_NAME, 'telephone': PHONE },
      'areaServed': { '@type': 'AdministrativeArea', 'name': cityName + ', Ontario, Canada' },
    });
  }

  // 3. FAQPage (3 generic but useful Qs)
  const priceMin = brand && ['miele','sub-zero','wolf','viking','thermador'].includes(brand) ? 150 : 89;
  const priceMax = serviceName && /refrigerator|fridge/.test(serviceName) ? 600 : 450;
  graph.push({
    '@type': 'FAQPage',
    'mainEntity': [
      {
        '@type': 'Question',
        'name': `How much does ${fullServiceName.toLowerCase()} cost in ${cityName}?`,
        'acceptedAnswer': {
          '@type': 'Answer',
          'text': `${fullServiceName} in ${cityName} typically costs $${priceMin}–$${priceMax} depending on the issue and parts required. ${SITE_NAME} provides upfront pricing before any work begins. Call ${PHONE} for a free estimate.`,
        },
      },
      {
        '@type': 'Question',
        'name': `Do you offer same-day ${fullServiceName.toLowerCase()} in ${cityName}?`,
        'acceptedAnswer': {
          '@type': 'Answer',
          'text': `Yes, ${SITE_NAME} offers same-day ${fullServiceName.toLowerCase()} in ${cityName}. Book before 12 PM on a weekday for best availability. Call ${PHONE}.`,
        },
      },
      {
        '@type': 'Question',
        'name': `Is your repair work covered by a warranty?`,
        'acceptedAnswer': {
          '@type': 'Answer',
          'text': `All ${fullServiceName.toLowerCase()} performed by ${SITE_NAME} comes with a 90-day parts and labour warranty from the repair date.`,
        },
      },
    ],
  });

  // 4. BreadcrumbList
  graph.push({
    '@type': 'BreadcrumbList',
    'itemListElement': [
      { '@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': `https://${DOMAIN}/` },
      { '@type': 'ListItem', 'position': 2, 'name': h1 || title || fullServiceName },
    ],
  });

  return { '@context': 'https://schema.org', '@graph': graph };
}

const SCRIPT_RE = /<script\s+type=["']application\/ld\+json["']\s*>([\s\S]*?)<\/script>/;
const REGEN_MARKER = '<!-- JSONLD-REGEN-v1 -->';

function regenFile(filepath) {
  const html = fs.readFileSync(filepath, 'utf8');
  const m = html.match(SCRIPT_RE);
  if (!m) return { changed: false, reason: 'no jsonld' };
  // Try parse
  try { JSON.parse(m[1]); return { changed: false, reason: 'valid' }; } catch (e) {}
  // Already regen'd? Skip if marker present
  if (html.includes(REGEN_MARKER)) return { changed: false, reason: 'already regen' };

  // Build replacement
  const slug = path.basename(filepath, '.html');
  const detected = detectFromSlug(slug);
  const title = (html.match(/<title>([^<]+)<\/title>/) || [, ''])[1].trim();
  const desc = (html.match(/<meta\s+name=["']description["']\s+content=["']([^"']+)["']/) || [, ''])[1].trim();
  const canonical = (html.match(/<link\s+rel=["']canonical["']\s+href=["']([^"']+)["']/) || [, ''])[1].trim();
  const h1 = (html.match(/<h1[^>]*>([^<]+)<\/h1>/) || [, ''])[1].replace(/<[^>]+>/g, '').trim();
  const pageUrl = canonical || `https://${DOMAIN}/${slug}`;

  const graph = buildGraph({ pageUrl, title, description: desc, brand: detected.brand, service: detected.service, city: detected.city, h1 });
  const newJson = JSON.stringify(graph, null, 2);
  const newScript = REGEN_MARKER + '\n<script type="application/ld+json">\n' + newJson + '\n</script>';

  // Replace the FIRST JSON-LD block. Use captured indices (m.index).
  const newHtml = html.slice(0, m.index) + newScript + html.slice(m.index + m[0].length);

  if (!DRY) fs.writeFileSync(filepath, newHtml);
  return { changed: true, brand: detected.brand, service: detected.service, city: detected.city };
}

const files = walk(SITE);
const sliced = LIMIT > 0 ? files.slice(0, LIMIT) : files;

let stats = { scanned: 0, regen: 0, alreadyValid: 0, alreadyDone: 0, noJsonld: 0, sample: [] };

for (const file of sliced) {
  stats.scanned++;
  const r = regenFile(file);
  if (r.changed) {
    stats.regen++;
    if (stats.sample.length < 8) stats.sample.push(path.relative(SITE, file) + ' [' + (r.brand || '-') + '/' + (r.service || '-') + '/' + (r.city || '-') + ']');
  } else if (r.reason === 'valid') stats.alreadyValid++;
  else if (r.reason === 'already regen') stats.alreadyDone++;
  else stats.noJsonld++;
}

console.log('=== regen-jsonld.js ===');
console.log('site         :', SITE);
console.log('dry          :', DRY);
console.log('scanned      :', stats.scanned);
console.log('regen        :', stats.regen);
console.log('already valid:', stats.alreadyValid);
console.log('already regen:', stats.alreadyDone);
console.log('no jsonld    :', stats.noJsonld);
if (stats.sample.length) {
  console.log('Samples:');
  stats.sample.forEach(s => console.log('  -', s));
}
