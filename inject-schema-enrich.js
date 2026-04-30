/**
 * inject-schema-enrich.js — Add founder + numberOfEmployees to LocalBusiness JSON-LD
 *
 * Walks all .html files for given site, finds <script type="application/ld+json">,
 * locates LocalBusiness (top-level OR inside @graph), merges in founder/numberOfEmployees
 * if missing. Idempotent via SCHEMA-ENRICH-v1 marker comment placed adjacent to script tag.
 *
 * Usage:
 *   node inject-schema-enrich.js --site=C:/NikaApplianceRepair --founder="Nick" --employees=12 [--limit=5] [--dry-run]
 *
 * Skips files: 404.html, *-template.html, anything in lazy-method/, _pages_queue/, node_modules/.
 * Logs malformed JSON-LD blocks for manual repair (does NOT mutate the malformed block).
 */
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
function arg(name, def) {
  const found = args.find(a => a.startsWith('--' + name + '='));
  return found ? found.slice(name.length + 3) : def;
}
const HAS_FLAG = (n) => args.includes('--' + n);

const SITE_DIR = arg('site');
const FOUNDER = arg('founder');
const EMPLOYEES = parseInt(arg('employees', '0'), 10);
const LIMIT = parseInt(arg('limit', '0'), 10);
const DRY = HAS_FLAG('dry-run');

if (!SITE_DIR || !FOUNDER || !EMPLOYEES) {
  console.error('Usage: --site=DIR --founder=NAME --employees=N [--limit=N] [--dry-run]');
  process.exit(1);
}

const MARKER = '<!-- SCHEMA-ENRICH-v1 -->';
const SKIP_DIRS = new Set(['lazy-method', '_pages_queue', 'node_modules', '.git', 'reports']);
const SKIP_FILE_PATTERNS = [/-template\.html$/, /^404\.html$/, /^landing-v/];
const SCRIPT_RE = /<script\s+type=["']application\/ld\+json["']\s*>([\s\S]*?)<\/script>/g;

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

function enrichOne(node) {
  if (!node || typeof node !== 'object') return false;
  if (node['@type'] !== 'LocalBusiness' && !(Array.isArray(node['@type']) && node['@type'].includes('LocalBusiness'))) {
    return false;
  }
  let changed = false;
  if (!node.founder) {
    node.founder = { '@type': 'Person', 'name': FOUNDER };
    changed = true;
  }
  if (!node.numberOfEmployees) {
    node.numberOfEmployees = { '@type': 'QuantitativeValue', 'value': EMPLOYEES };
    changed = true;
  }
  return changed;
}

function enrichJson(data) {
  let changed = false;
  if (Array.isArray(data)) {
    for (const item of data) if (enrichJson(item)) changed = true;
    return changed;
  }
  if (data && typeof data === 'object') {
    if (Array.isArray(data['@graph'])) {
      for (const g of data['@graph']) if (enrichOne(g)) changed = true;
    }
    if (enrichOne(data)) changed = true;
  }
  return changed;
}

const files = walk(SITE_DIR);
const sliced = LIMIT > 0 ? files.slice(0, LIMIT) : files;

let stats = { scanned: 0, modified: 0, alreadyDone: 0, noLocalBiz: 0, malformed: 0, malformedFiles: [] };

for (const file of sliced) {
  stats.scanned++;
  let html = fs.readFileSync(file, 'utf8');

  if (html.includes(MARKER)) { stats.alreadyDone++; continue; }

  let fileChanged = false;
  let hasLocalBiz = false;
  let hasMalformed = false;

  html = html.replace(SCRIPT_RE, (full, body) => {
    let json;
    try {
      json = JSON.parse(body);
    } catch (err) {
      hasMalformed = true;
      return full;
    }
    const isLB = JSON.stringify(json).includes('"@type":"LocalBusiness"');
    if (!isLB) return full;
    hasLocalBiz = true;
    const changed = enrichJson(json);
    if (!changed) return full;
    fileChanged = true;
    const newBody = JSON.stringify(json, null, 2);
    return '<script type="application/ld+json">\n' + newBody + '\n</script>';
  });

  if (hasMalformed) {
    stats.malformed++;
    stats.malformedFiles.push(path.relative(SITE_DIR, file));
  }

  if (!hasLocalBiz && !hasMalformed) {
    stats.noLocalBiz++;
    continue;
  }

  if (fileChanged) {
    const headIdx = html.indexOf('</head>');
    if (headIdx > -1) html = html.slice(0, headIdx) + MARKER + '\n' + html.slice(headIdx);
    if (!DRY) fs.writeFileSync(file, html);
    stats.modified++;
  }
}

console.log('=== inject-schema-enrich.js ===');
console.log('site:', SITE_DIR);
console.log('founder:', FOUNDER, '| employees:', EMPLOYEES, '| dry:', DRY);
console.log('scanned :', stats.scanned);
console.log('modified:', stats.modified);
console.log('already :', stats.alreadyDone);
console.log('no LocalBiz:', stats.noLocalBiz);
console.log('malformed:', stats.malformed);
if (stats.malformedFiles.length) {
  console.log('malformed files:');
  stats.malformedFiles.slice(0, 30).forEach(f => console.log('  -', f));
  if (stats.malformedFiles.length > 30) console.log('  ... and', stats.malformedFiles.length - 30, 'more');
}
