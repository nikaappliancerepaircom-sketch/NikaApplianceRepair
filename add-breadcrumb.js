/**
 * add-breadcrumb.js
 * Adds BreadcrumbList to existing JSON-LD @graph on pages missing it.
 * Reads site config from lazy-config.json. Non-destructive: only modifies
 * the JSON-LD block, leaves all other HTML untouched.
 *
 * Usage:
 *   node add-breadcrumb.js --site=C:/nappliancerepair [--dry-run]
 *   node add-breadcrumb.js --all [--dry-run]
 */
'use strict';
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const DRY = args.includes('--dry-run');
const ALL = args.includes('--all');
const siteArg = args.find(a => a.startsWith('--site='));

const ALL_SITES = [
  'C:/NikaApplianceRepair',
  'C:/nappliancerepair',
  'C:/appliancerepairneary',
  'C:/fixlifyservices',
];

const SKIP_DIRS = new Set(['lazy-method', 'node_modules', '.git', 'reports', 'backups', 'tools']);
const SKIP_PATTERNS = [/-template\.html$/, /^landing-v/, /^compare/, /^preview/];

const SERVICES = ['dishwasher','refrigerator','washer','dryer','fridge','oven','stove','freezer','range','microwave'];
const BRANDS   = ['samsung','lg','whirlpool','bosch','ge','frigidaire','kenmore','maytag','kitchenaid','miele','amana','electrolux'];
const CITIES   = ['toronto','scarborough','north-york','etobicoke','mississauga','brampton','vaughan','markham','richmond-hill','oakville','burlington','pickering','ajax','whitby','oshawa','newmarket','bradford','aurora','calgary','edmonton','airdrie','beaumont','cochrane','canmore','chestermere','leduc','st-albert','sherwood-park'];

function toTitle(s) {
  return s.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
}

function detectSlug(slug) {
  let service = null, city = null;
  for (const s of SERVICES) { if (slug.includes(s)) { service = s; break; } }
  for (const c of [...CITIES].sort((a,b) => b.length - a.length)) {
    if (slug === c || slug.endsWith('-' + c)) { city = c; break; }
  }
  return { service, city };
}

function buildBreadcrumb(domain, slug, h1, service, city) {
  const items = [
    { '@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': `https://${domain}/` },
  ];

  if (service && city) {
    // 3-level: Home > Service > Service in City
    items.push({
      '@type': 'ListItem', 'position': 2,
      'name': toTitle(service) + ' Repair',
      'item': `https://${domain}/${service}-repair`,
    });
    items.push({
      '@type': 'ListItem', 'position': 3,
      'name': h1 || (toTitle(service) + ' Repair in ' + toTitle(city)),
    });
  } else if (service) {
    items.push({
      '@type': 'ListItem', 'position': 2,
      'name': h1 || (toTitle(service) + ' Repair'),
    });
  } else if (city) {
    items.push({
      '@type': 'ListItem', 'position': 2,
      'name': h1 || ('Appliance Repair in ' + toTitle(city)),
    });
  } else {
    items.push({
      '@type': 'ListItem', 'position': 2,
      'name': h1 || 'Appliance Repair',
    });
  }

  return { '@type': 'BreadcrumbList', 'itemListElement': items };
}

function processFile(filepath, domain) {
  const html = fs.readFileSync(filepath, 'utf8');

  // Already has BreadcrumbList?
  if (/"@type"\s*:\s*"BreadcrumbList"/.test(html)) {
    return { changed: false, reason: 'already-has' };
  }

  // Find JSON-LD block
  const scriptRe = /<script\s+type=["']application\/ld\+json["']\s*>([\s\S]*?)<\/script>/;
  const m = html.match(scriptRe);
  if (!m) return { changed: false, reason: 'no-jsonld' };

  let schema;
  try { schema = JSON.parse(m[1]); } catch (e) { return { changed: false, reason: 'malformed-jsonld' }; }

  // Handle both @graph array and single schema
  const h1 = (html.match(/<h1[^>]*>(.*?)<\/h1>/si) || [,''])[1].replace(/<[^>]+>/g, '').trim();
  const slug = path.basename(filepath, '.html');
  const { service, city } = detectSlug(slug);
  const breadcrumb = buildBreadcrumb(domain, slug, h1, service, city);

  if (schema['@graph']) {
    // @graph array — add BreadcrumbList to it
    schema['@graph'].push(breadcrumb);
  } else if (schema['@type']) {
    // Single type — wrap in @graph
    schema = { '@context': 'https://schema.org', '@graph': [schema, breadcrumb] };
  } else {
    return { changed: false, reason: 'unknown-schema-structure' };
  }

  const newJson = JSON.stringify(schema, null, 2);
  const newHtml = html.slice(0, m.index) +
    '<script type="application/ld+json">\n' + newJson + '\n</script>' +
    html.slice(m.index + m[0].length);

  if (!DRY) fs.writeFileSync(filepath, newHtml, 'utf8');
  return { changed: true, service, city };
}

function walk(dir) {
  const out = [];
  let items;
  try { items = fs.readdirSync(dir, { withFileTypes: true }); } catch { return out; }
  for (const item of items) {
    if (item.isDirectory()) {
      if (SKIP_DIRS.has(item.name)) continue;
      out.push(...walk(path.join(dir, item.name)));
    } else if (item.name.endsWith('.html')) {
      if (SKIP_PATTERNS.some(re => re.test(item.name))) continue;
      out.push(path.join(dir, item.name));
    }
  }
  return out;
}

function processSite(siteDir) {
  if (!fs.existsSync(siteDir)) { console.log(`SKIP (not found): ${siteDir}`); return 0; }

  let cfg = { site: { domain: '' } };
  const cfgPath = path.join(siteDir, 'lazy-config.json');
  if (fs.existsSync(cfgPath)) {
    cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
  }
  const domain = cfg.site.domain || path.basename(siteDir) + '.com';

  const files = walk(siteDir);
  let added = 0, alreadyHas = 0, skipped = 0, errors = 0;

  for (const f of files) {
    try {
      const r = processFile(f, domain);
      if (r.changed) { added++; }
      else if (r.reason === 'already-has') { alreadyHas++; }
      else { skipped++; }
    } catch (e) {
      console.error(`  ERROR ${f}: ${e.message}`);
      errors++;
    }
  }

  const pct = files.length ? Math.round((alreadyHas / files.length) * 100) : 0;
  console.log(`${domain}: added=${added}, already=${alreadyHas} (${pct}%), skipped=${skipped}, errors=${errors}`);
  return added;
}

// Main
const sites = ALL ? ALL_SITES :
  siteArg ? ALL_SITES.filter(s => siteArg.includes(path.basename(s))) :
  ALL_SITES;

console.log(`Mode: ${DRY ? 'DRY RUN' : 'WRITE'}`);
let total = 0;
for (const s of sites) total += processSite(s);
console.log(`\nTotal BreadcrumbList added: ${total}`);
