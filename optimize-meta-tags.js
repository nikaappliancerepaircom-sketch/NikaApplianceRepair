#!/usr/bin/env node
// optimize-meta-tags.js — Meta Title & Description Optimizer for 4 Sites
// Usage: node optimize-meta-tags.js [--dry-run] [--site nar|neary|fixlify|nika]

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const DRY_RUN = args.includes('--dry-run');
const SITE_FILTER = (() => {
  const idx = args.indexOf('--site');
  return idx !== -1 ? args[idx + 1] : null;
})();

// ─── Site Configs ─────────────────────────────────────────────────────────────
const SITES = {
  nika: {
    dir: 'C:/NikaApplianceRepair',
    domain: 'nikaappliancerepair.com',
    brand: 'Nika Appliance Repair',
    phone: '(437) 524-1053',
    voice: 'authority',
  },
  nar: {
    dir: 'C:/nappliancerepair',
    domain: 'nappliancerepair.com',
    brand: 'N Appliance Repair',
    phone: '(437) 524-1053',
    voice: 'professional',
  },
  neary: {
    dir: 'C:/appliancerepairneary',
    domain: 'appliancerepairneary.com',
    brand: 'Appliance Repair Near Me',
    phone: '(437) 524-1053',
    voice: 'proximity',
  },
  fixlify: {
    dir: 'C:/fixlifyservices',
    domain: 'fixlifyservices.com',
    brand: 'Fixlify Services',
    phone: '(437) 524-1053',
    voice: 'value',
  },
};

// ─── Known Lists ──────────────────────────────────────────────────────────────
const SERVICES = [
  'dishwasher', 'fridge', 'refrigerator', 'washer', 'dryer', 'oven', 'stove',
  'microwave', 'freezer', 'range', 'cooktop', 'appliance', 'air-conditioner',
  'wine-fridge', 'ice-maker', 'garbage-disposal',
];

const BRANDS = [
  'samsung', 'lg', 'whirlpool', 'bosch', 'frigidaire', 'kenmore', 'ge', 'miele',
  'maytag', 'kitchenaid', 'electrolux', 'amana', 'jenn-air', 'sub-zero', 'wolf',
  'speed-queen', 'fisher-paykel', 'haier', 'dacor', 'thermador', 'gaggenau',
  'liebherr', 'viking', 'aeg', 'blomberg', 'beko',
];

const CITIES = [
  'toronto', 'mississauga', 'brampton', 'scarborough', 'north-york', 'etobicoke',
  'oakville', 'markham', 'richmond-hill', 'vaughan', 'ajax', 'pickering', 'oshawa',
  'burlington', 'hamilton', 'bayview-village', 'birchcliff', 'cabbagetown',
  'danforth-village', 'davisville-village', 'don-mills', 'forest-hill',
  'humber-valley', 'islington-village', 'lawrence-park', 'leaside', 'leslieville',
  'liberty-village', 'midtown', 'rosedale', 'parkdale', 'beaches', 'annex',
  'yorkville', 'kensington', 'little-italy', 'greektown', 'chinatown',
  'riverdale', 'swansea', 'bloor-west', 'high-park', 'junction', 'weston',
  'york', 'east-york', 'west-hill', 'agincourt', 'malvern', 'highland-creek',
  'rouge', 'morningside', 'woodbine', 'eglinton', 'downtown', 'midtown-toronto',
  'thornhill', 'woodbridge', 'stouffville', 'aurora', 'newmarket',
  'port-credit', 'streetsville', 'meadowvale', 'concord', 'maple',
  'whitby', 'courtice', 'bowmanville', 'guelph', 'kitchener', 'cambridge',
  'north-toronto', 'east-toronto', 'west-toronto', 'york-mills', 'willowdale',
  'bathurst', 'dufferin', 'wilson', 'sheppard', 'finch', 'steeles',
];

const SKIP_FILES = new Set([
  '404.html', 'ajax.html', 'book.html', 'about.html', 'contact.html',
  'brands.html', 'compare.html', 'areas.html', 'team.html', 'preview.html',
  'locations.html', 'blog-nika-appliance-repair.html', 'sitemap.html',
  'privacy.html', 'terms.html', 'services.html',
]);

const SKIP_DIRS = new Set([
  'node_modules', '.git', '_queue', 'assets', 'css', 'js', 'images', 'fonts',
  'components', 'templates', 'styles', 'backups', 'backup', 'old', 'archive',
]);

// Proper display names for brands
const BRAND_DISPLAY = {
  lg: 'LG', ge: 'GE', aeg: 'AEG',
  samsung: 'Samsung', whirlpool: 'Whirlpool', bosch: 'Bosch',
  frigidaire: 'Frigidaire', kenmore: 'Kenmore', miele: 'Miele',
  maytag: 'Maytag', kitchenaid: 'KitchenAid', electrolux: 'Electrolux',
  amana: 'Amana', 'jenn-air': 'Jenn-Air', 'sub-zero': 'Sub-Zero',
  wolf: 'Wolf', 'speed-queen': 'Speed Queen', 'fisher-paykel': 'Fisher & Paykel',
  haier: 'Haier', dacor: 'Dacor', thermador: 'Thermador', gaggenau: 'Gaggenau',
  liebherr: 'Liebherr', viking: 'Viking', blomberg: 'Blomberg', beko: 'Beko',
};

// ─── Helpers ──────────────────────────────────────────────────────────────────
function toTitleCase(str) {
  return str.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
}

function extractFromFilename(filename) {
  const base = filename.replace(/\.html$/, '');

  // Brand detection (must appear at start)
  let brand = null;
  for (const b of BRANDS) {
    if (base === b || base.startsWith(b + '-')) {
      brand = b;
      break;
    }
  }

  // City detection (must appear at end)
  let city = null;
  for (const c of CITIES) {
    if (base === c || base.endsWith('-' + c)) {
      city = c;
      break;
    }
  }

  // Service detection
  let service = null;
  for (const s of SERVICES) {
    if (base.includes(s)) {
      service = s;
      break;
    }
  }

  const isInstallation = base.includes('-installation');
  const isRepair = base.includes('-repair') && !isInstallation;

  return { brand, city, service, isInstallation, isRepair, base };
}

function classifyPage(filename, relPath) {
  const base = filename;

  if (relPath.startsWith('blog/') || relPath.includes('/blog/')) return 'skip';
  if (relPath.startsWith('_queue/') || relPath.includes('/_queue/')) return 'skip';
  if (SKIP_FILES.has(base)) return 'skip';
  if (/^landing/.test(base) || base.startsWith('landing-')) return 'skip';

  if (base === 'index.html') return 'homepage';

  const b = base.replace(/\.html$/, '');

  if (b.startsWith('emergency')) return 'emergency';

  if (b.endsWith('-cost') || b.endsWith('-pricing') || b.endsWith('-price') ||
      b.includes('-repair-cost') || b.includes('appliance-repair-cost') ||
      b.includes('average-appliance-repair') || b.includes('-repair-prices')) return 'cost-guide';

  if (/-not-/.test(b) || /wont-/.test(b) || b.endsWith('-leaking') ||
      b.endsWith('-stopped-working') || b.endsWith('-making-noise')) return 'problem';

  if (b.includes('-installation')) return 'installation';

  const { brand, city, service } = extractFromFilename(base);

  if (CITIES.includes(b)) return 'city-hub';

  if (brand && service && city) return 'brand-service-city';
  if (brand && city && !service) return 'brand-city';
  if (brand && service && !city) return 'brand-service';
  if (service && city && !brand) return 'service-city';
  if (brand && !city && !service) return 'brand';
  if (service && b.includes('-repair')) return 'service';

  return 'other';
}

// ─── Meta Templates ───────────────────────────────────────────────────────────
function generateMeta(pageType, info, site) {
  const { brand, city, service, isInstallation } = info;
  const { phone, voice } = site;

  // SAFETY: cityLabel defaults to 'Toronto' for pageType='service'/'brand'/etc.
  // For Alberta or other non-Toronto cities, callers MUST pass pageType='service-city'
  // or 'brand-city' AND a city. See bug history: queue files were once generated with
  // pageType='service' and a city, which incorrectly hardcoded Toronto in title/meta.
  const cityLabel    = city    ? toTitleCase(city)    : 'Toronto';
  const serviceLabel = service ? toTitleCase(service) : 'Appliance';
  const brandLabel   = brand   ? (BRAND_DISPLAY[brand] || toTitleCase(brand)) : '';
  const action     = isInstallation ? 'Installation' : 'Repair';
  const actionL    = isInstallation ? 'installation' : 'repair';

  // Voice-based desc endings
  function tail() {
    switch (voice) {
      case 'authority':   return `Certified experts since 2017. Call ${phone}.`;
      case 'professional': return `Licensed & insured. Call ${phone}!`;
      case 'proximity':   return `Local experts near you. Call ${phone}!`;
      case 'value':       return `$89 flat diagnostic, no hidden fees. Book today!`;
    }
  }

  switch (pageType) {

    case 'homepage': {
      const T = {
        authority:    `Nika Appliance Repair Toronto | Certified Since 2017 | ${phone}`,
        professional: `Appliance Repair Toronto | Same-Day Service | ${phone}`,
        proximity:    `Appliance Repair Near Me Toronto | 1-Hour Response | ${phone}`,
        value:        `Appliance Repair Toronto | $89 Diagnostic | ${phone}`,
      };
      const D = {
        authority:    `Toronto's certified appliance repair experts since 2017. Same-day service for all brands. $89 diagnostic fee. 4.8★ rated. Call ${phone}.`,
        professional: `Toronto's trusted appliance repair. Same-day service for fridges, washers, dryers & more. Licensed technicians, $89 diagnostic. Call ${phone} today.`,
        proximity:    `Fast appliance repair near you in Toronto & GTA. Certified local technicians fix fridges, washers, dishwashers same day. $89 flat diagnostic. Call now!`,
        value:        `Expert appliance repair in Toronto. Transparent pricing starting at $89 diagnostic. Same-day fixes for all major brands. Licensed & insured. Book today!`,
      };
      return { title: T[voice], desc: D[voice] };
    }

    case 'service': {
      const T = {
        authority:    `${serviceLabel} ${action} Toronto | Certified Experts | ${phone}`,
        professional: `${serviceLabel} ${action} Toronto | Same-Day Fix | ${phone}`,
        proximity:    `${serviceLabel} ${action} Near Me Toronto | Same-Day | ${phone}`,
        value:        `${serviceLabel} ${action} Toronto | From $89 | ${phone}`,
      };
      const D = {
        authority:    `Certified ${serviceLabel.toLowerCase()} ${actionL} in Toronto since 2017. All brands: Samsung, LG, Bosch & more. $89 diagnostic, same-day service. Call ${phone}.`,
        professional: `Professional ${serviceLabel.toLowerCase()} ${actionL} in Toronto. Same-day service for all brands — Samsung, Bosch, LG & more. $89 diagnostic, licensed technicians. Call now!`,
        proximity:    `${serviceLabel} ${actionL} near you in Toronto & GTA. Certified local technicians, same-day service. Samsung, LG, Bosch & all brands. $89 diagnostic. Call ${phone}!`,
        value:        `Expert ${serviceLabel.toLowerCase()} ${actionL} in Toronto. $89 flat diagnostic, transparent pricing. All brands — Samsung, LG, Bosch & more. Same-day service. Book today!`,
      };
      return { title: T[voice], desc: D[voice] };
    }

    case 'service-city': {
      const T = {
        authority:    `${serviceLabel} ${action} ${cityLabel} | Certified Techs | ${phone}`,
        professional: `${serviceLabel} ${action} ${cityLabel} | Same-Day Service | ${phone}`,
        proximity:    `${serviceLabel} ${action} Near Me ${cityLabel} | Same-Day | ${phone}`,
        value:        `${serviceLabel} ${action} ${cityLabel} | $89 Diagnostic | ${phone}`,
      };
      const D = {
        authority:    `Certified ${serviceLabel.toLowerCase()} ${actionL} in ${cityLabel} since 2017. Samsung, LG, Bosch & all brands. $89 diagnostic, same-day service. Call ${phone}.`,
        professional: `Fast ${serviceLabel.toLowerCase()} ${actionL} in ${cityLabel}. Licensed technicians fix Samsung, LG, Bosch & all brands same day. $89 flat diagnostic. Call ${phone}!`,
        proximity:    `${serviceLabel} ${actionL} near you in ${cityLabel}. Local certified technicians, same-day service for all brands. $89 diagnostic. Call ${phone}!`,
        value:        `${serviceLabel} ${actionL} in ${cityLabel}. $89 flat diagnostic, transparent pricing. Samsung, LG, Bosch & all brands, same-day service. Book today!`,
      };
      return { title: T[voice], desc: D[voice] };
    }

    case 'brand': {
      const T = {
        authority:    `${brandLabel} Appliance Repair Toronto | Certified | ${phone}`,
        professional: `${brandLabel} Appliance Repair Toronto | Same-Day | ${phone}`,
        proximity:    `${brandLabel} Repair Near Me Toronto | Same-Day | ${phone}`,
        value:        `${brandLabel} Appliance Repair Toronto | $89 Diagnostic | ${phone}`,
      };
      const D = {
        authority:    `Certified ${brandLabel} appliance repair in Toronto since 2017. Fridges, washers, dishwashers & dryers. $89 diagnostic, same-day service. Call ${phone}.`,
        professional: `${brandLabel} appliance repair in Toronto. Licensed technicians fix all models same-day. $89 diagnostic, 90-day warranty. Call ${phone}!`,
        proximity:    `${brandLabel} appliance repair near you in Toronto & GTA. Local certified technicians, same-day service for all models. $89 diagnostic. Call ${phone}!`,
        value:        `${brandLabel} appliance repair in Toronto. $89 flat diagnostic, transparent pricing. Expert fixes for fridges, washers, dishwashers & dryers. Same-day. Book today!`,
      };
      return { title: T[voice], desc: D[voice] };
    }

    case 'brand-service': {
      const T = {
        authority:    `${brandLabel} ${serviceLabel} ${action} Toronto | Certified | ${phone}`,
        professional: `${brandLabel} ${serviceLabel} ${action} Toronto | Same-Day | ${phone}`,
        proximity:    `${brandLabel} ${serviceLabel} ${action} Near Me | Same-Day | ${phone}`,
        value:        `${brandLabel} ${serviceLabel} ${action} Toronto | $89 | ${phone}`,
      };
      const D = {
        authority:    `Certified ${brandLabel} ${serviceLabel.toLowerCase()} ${actionL} in Toronto since 2017. All models, $89 diagnostic, same-day service. Call ${phone}.`,
        professional: `Professional ${brandLabel} ${serviceLabel.toLowerCase()} ${actionL} in Toronto. Same-day service, all models. $89 diagnostic, licensed techs. Call ${phone}!`,
        proximity:    `${brandLabel} ${serviceLabel.toLowerCase()} ${actionL} near you in Toronto. Local certified technicians, all models, same-day. $89 diagnostic. Call ${phone}!`,
        value:        `${brandLabel} ${serviceLabel.toLowerCase()} ${actionL} in Toronto. $89 flat diagnostic, transparent pricing. All models, same-day service. Book today!`,
      };
      return { title: T[voice], desc: D[voice] };
    }

    case 'brand-city': {
      const T = {
        authority:    `${brandLabel} Appliance Repair ${cityLabel} | Certified | ${phone}`,
        professional: `${brandLabel} Appliance Repair ${cityLabel} | Same-Day | ${phone}`,
        proximity:    `${brandLabel} Repair Near Me ${cityLabel} | Same-Day | ${phone}`,
        value:        `${brandLabel} Appliance Repair ${cityLabel} | $89 Diag | ${phone}`,
      };
      const D = {
        authority:    `Certified ${brandLabel} appliance repair in ${cityLabel} since 2017. All models fixed same day. $89 diagnostic, 90-day warranty. Call ${phone}.`,
        professional: `Fast ${brandLabel} appliance repair in ${cityLabel}. Licensed technicians, all models, same-day service. $89 diagnostic. Call ${phone}!`,
        proximity:    `${brandLabel} appliance repair near you in ${cityLabel}. Certified local techs, same-day service, all models. $89 diagnostic. Call ${phone}!`,
        value:        `${brandLabel} appliance repair in ${cityLabel}. $89 flat diagnostic, transparent pricing, same-day service. Licensed & insured. Book today!`,
      };
      return { title: T[voice], desc: D[voice] };
    }

    case 'brand-service-city': {
      const T = {
        authority:    `${brandLabel} ${serviceLabel} ${action} ${cityLabel} | ${phone}`,
        professional: `${brandLabel} ${serviceLabel} ${action} ${cityLabel} | Same-Day | ${phone}`,
        proximity:    `${brandLabel} ${serviceLabel} ${action} Near Me ${cityLabel} | ${phone}`,
        value:        `${brandLabel} ${serviceLabel} ${action} ${cityLabel} | $89 | ${phone}`,
      };
      const D = {
        authority:    `Certified ${brandLabel} ${serviceLabel.toLowerCase()} ${actionL} in ${cityLabel} since 2017. All models, $89 diagnostic, same-day service. Call ${phone}.`,
        professional: `Fast ${brandLabel} ${serviceLabel.toLowerCase()} ${actionL} in ${cityLabel}. Licensed techs, all models, $89 diagnostic. Call ${phone}!`,
        proximity:    `${brandLabel} ${serviceLabel.toLowerCase()} ${actionL} near you in ${cityLabel}. Local certified techs, same-day service. $89 diagnostic. Call ${phone}!`,
        value:        `${brandLabel} ${serviceLabel.toLowerCase()} ${actionL} in ${cityLabel}. $89 flat diagnostic, transparent pricing, same-day. Book today!`,
      };
      return { title: T[voice], desc: D[voice] };
    }

    case 'city-hub': {
      const T = {
        authority:    `Appliance Repair ${cityLabel} | Certified Since 2017 | ${phone}`,
        professional: `Appliance Repair ${cityLabel} | Same-Day Service | ${phone}`,
        proximity:    `Appliance Repair Near Me ${cityLabel} | Same-Day | ${phone}`,
        value:        `Appliance Repair ${cityLabel} | $89 Diagnostic | ${phone}`,
      };
      const D = {
        authority:    `Certified appliance repair in ${cityLabel} since 2017. All brands fixed same day — Samsung, LG, Bosch & more. $89 diagnostic. Call ${phone}.`,
        professional: `Trusted appliance repair in ${cityLabel}. Licensed technicians fix fridges, washers, dryers & dishwashers. Same-day service, $89 diagnostic. Call ${phone}!`,
        proximity:    `Appliance repair near you in ${cityLabel}. Certified local technicians, same-day service for all brands. $89 diagnostic. Call ${phone}!`,
        value:        `Expert appliance repair in ${cityLabel}. $89 flat diagnostic, transparent pricing. All brands, same-day service. Licensed & insured. Book today!`,
      };
      return { title: T[voice], desc: D[voice] };
    }

    case 'problem': {
      const b = info.base;
      const readable = b.replace(/-/g, ' ');
      const readableCap = readable.replace(/\b\w/g, l => l.toUpperCase());
      const T = {
        authority:    `${readableCap}? Fix Today Toronto | ${phone}`,
        professional: `${readableCap}? Same-Day Repair Toronto | ${phone}`,
        proximity:    `${readableCap}? Local Repair Near You | ${phone}`,
        value:        `${readableCap}? From $89 Fix Toronto | ${phone}`,
      };
      const D = {
        authority:    `${serviceLabel} ${readable}? Certified Toronto technicians diagnose & fix same day since 2017. $89 diagnostic. Call ${phone}.`,
        professional: `${serviceLabel} ${readable}? Same-day repair in Toronto from $89 diagnostic. Licensed technicians, all brands. Call ${phone}!`,
        proximity:    `${serviceLabel} ${readable}? Local repair technicians near you in Toronto. Same-day service, $89 diagnostic. All brands. Call ${phone}!`,
        value:        `${serviceLabel} ${readable}? $89 flat diagnostic in Toronto. Transparent pricing, same-day repair, all brands. Licensed & insured. Book today!`,
      };
      return { title: T[voice], desc: D[voice] };
    }

    case 'cost-guide': {
      const svcLabel = service ? `${serviceLabel} Repair` : 'Appliance Repair';
      const T = {
        authority:    `${svcLabel} Cost Toronto 2026 | Certified Pricing | ${phone}`,
        professional: `${svcLabel} Cost Toronto 2026 | Honest Pricing | ${phone}`,
        proximity:    `${svcLabel} Cost Near Me Toronto 2026 | ${phone}`,
        value:        `${svcLabel} Cost Toronto 2026 | $89 Diagnostic | Pricing Guide`,
      };
      const D = {
        authority:    `How much does ${svcLabel.toLowerCase()} cost in Toronto? Average $150–$400. Certified experts since 2017. $89 diagnostic fee. Get a quote: ${phone}.`,
        professional: `How much does ${svcLabel.toLowerCase()} cost in Toronto? Average $150–$400. $89 flat diagnostic, no hidden fees. Licensed technicians. Call ${phone}!`,
        proximity:    `How much does ${svcLabel.toLowerCase()} cost near you in Toronto? Average $150–$400. $89 diagnostic. Local certified techs. Call ${phone}!`,
        value:        `How much does ${svcLabel.toLowerCase()} cost in Toronto? Average $150–$400. $89 flat diagnostic, transparent pricing, no hidden charges. Get a quote today!`,
      };
      return { title: T[voice], desc: D[voice] };
    }

    case 'installation': {
      const T = {
        authority:    `${serviceLabel} Installation ${cityLabel !== 'Toronto' ? cityLabel + ' | ' : 'Toronto | '}Certified Techs | ${phone}`,
        professional: `${serviceLabel} Installation ${cityLabel !== 'Toronto' ? cityLabel + ' | ' : 'Toronto | '}Same-Day | ${phone}`,
        proximity:    `${serviceLabel} Installation Near Me ${cityLabel} | ${phone}`,
        value:        `${serviceLabel} Installation ${cityLabel !== 'Toronto' ? cityLabel + ' | ' : 'Toronto | '}From $89 | ${phone}`,
      };
      const D = {
        authority:    `Professional ${serviceLabel.toLowerCase()} installation in ${cityLabel} since 2017. Certified technicians, all brands. Same-day service. Call ${phone}.`,
        professional: `Professional ${serviceLabel.toLowerCase()} installation in ${cityLabel}. Licensed technicians, same-day service, all brands. Call ${phone}!`,
        proximity:    `${serviceLabel} installation near you in ${cityLabel}. Certified local technicians, all brands, same-day service. Call ${phone}!`,
        value:        `${serviceLabel} installation in ${cityLabel}. Transparent pricing, all brands covered. Licensed & insured. Book today!`,
      };
      return { title: T[voice], desc: D[voice] };
    }

    case 'emergency': {
      const T = {
        authority:    `Emergency Appliance Repair Toronto | 24/7 Certified | ${phone}`,
        professional: `Emergency Appliance Repair Toronto | 24/7 Same-Day | ${phone}`,
        proximity:    `Emergency Appliance Repair Near Me Toronto | 24/7 | ${phone}`,
        value:        `Emergency Appliance Repair Toronto | $89 Diag | 24/7 | ${phone}`,
      };
      const D = {
        authority:    `24/7 emergency appliance repair in Toronto. Certified technicians since 2017, rapid response. $89 diagnostic. All brands. Call ${phone}.`,
        professional: `24/7 emergency appliance repair in Toronto. Licensed technicians, rapid same-day response. $89 diagnostic. Call ${phone} now!`,
        proximity:    `Emergency appliance repair near you in Toronto, 24/7. Local certified technicians, rapid response. $89 diagnostic. Call ${phone}!`,
        value:        `24/7 emergency appliance repair in Toronto. $89 flat diagnostic, transparent pricing. Rapid response for all brands. Call ${phone}!`,
      };
      return { title: T[voice], desc: D[voice] };
    }

    default:
      return null;
  }
}

// ─── HTML Tag Replacement ─────────────────────────────────────────────────────
function replaceTag(html, pattern, replacement) {
  if (pattern.test(html)) {
    return html.replace(pattern, replacement);
  }
  return html;
}

function processHtml(html, title, desc) {
  let out = html;

  // Escape special chars for HTML attribute values
  const safeTitle = title.replace(/&/g, '&amp;').replace(/"/g, '&quot;');
  const safeDesc  = desc.replace(/&/g, '&amp;').replace(/"/g, '&quot;');

  // <title>
  out = out.replace(/<title>[^<]*<\/title>/i, `<title>${safeTitle}</title>`);

  // meta description (both attribute orderings)
  out = out.replace(/<meta\s+name="description"\s+content="[^"]*"\s*\/?>/i,
    `<meta name="description" content="${safeDesc}">`);
  out = out.replace(/<meta\s+content="[^"]*"\s+name="description"\s*\/?>/i,
    `<meta name="description" content="${safeDesc}">`);

  // og:title
  out = out.replace(/<meta\s+property="og:title"\s+content="[^"]*"\s*\/?>/i,
    `<meta property="og:title" content="${safeTitle}">`);
  out = out.replace(/<meta\s+content="[^"]*"\s+property="og:title"\s*\/?>/i,
    `<meta property="og:title" content="${safeTitle}">`);

  // og:description
  out = out.replace(/<meta\s+property="og:description"\s+content="[^"]*"\s*\/?>/i,
    `<meta property="og:description" content="${safeDesc}">`);
  out = out.replace(/<meta\s+content="[^"]*"\s+property="og:description"\s*\/?>/i,
    `<meta property="og:description" content="${safeDesc}">`);

  // twitter:title
  out = out.replace(/<meta\s+name="twitter:title"\s+content="[^"]*"\s*\/?>/i,
    `<meta name="twitter:title" content="${safeTitle}">`);

  // twitter:description
  out = out.replace(/<meta\s+name="twitter:description"\s+content="[^"]*"\s*\/?>/i,
    `<meta name="twitter:description" content="${safeDesc}">`);

  return out;
}

// ─── File Walker ──────────────────────────────────────────────────────────────
function getAllHtmlFiles(dir, prefix = '') {
  const results = [];
  let items;
  try { items = fs.readdirSync(dir, { withFileTypes: true }); }
  catch { return results; }

  for (const item of items) {
    if (item.isDirectory()) {
      if (SKIP_DIRS.has(item.name)) continue;
      results.push(...getAllHtmlFiles(path.join(dir, item.name), prefix + item.name + '/'));
    } else if (item.name.endsWith('.html')) {
      results.push(prefix + item.name);
    }
  }
  return results;
}

// ─── Process One Site ─────────────────────────────────────────────────────────
function processSite(siteName) {
  const site = SITES[siteName];
  const dir  = site.dir;

  console.log(`\n${'═'.repeat(70)}`);
  console.log(`Site: ${siteName.toUpperCase()}  (${dir})`);
  console.log(`${'═'.repeat(70)}`);

  if (!fs.existsSync(dir)) {
    console.error(`  ❌ Directory not found: ${dir}`);
    return;
  }

  const files = getAllHtmlFiles(dir);
  let processed = 0, skipped = 0, errors = 0;
  const warnings = [];

  for (const relPath of files) {
    const filename  = path.basename(relPath);
    const pageType  = classifyPage(filename, relPath);

    if (pageType === 'skip' || pageType === 'other') {
      skipped++;
      continue;
    }

    const info = extractFromFilename(filename);
    const meta = generateMeta(pageType, info, site);
    if (!meta) { skipped++; continue; }

    const { title, desc } = meta;

    if (title.length > 72) warnings.push(`⚠ TITLE LONG (${title.length}): ${relPath} → "${title}"`);
    if (desc.length  > 165) warnings.push(`⚠ DESC  LONG (${desc.length}): ${relPath}`);
    if (desc.length  < 100) warnings.push(`⚠ DESC SHORT (${desc.length}): ${relPath}`);

    const filePath = path.join(dir, relPath);
    try {
      const html = fs.readFileSync(filePath, 'utf8');

      const oldTitle = (html.match(/<title>([^<]*)<\/title>/i) || [])[1] || '(none)';
      const oldDesc  = (html.match(/<meta\s+name="description"\s+content="([^"]*)"/i) ||
                        html.match(/<meta\s+content="([^"]*)"\s+name="description"/i) || [])[1] || '(none)';

      console.log(`\n[${pageType}] ${relPath}`);
      console.log(`  OLD title: ${oldTitle}`);
      console.log(`  NEW title: ${title} (${title.length}c)`);
      console.log(`  OLD desc : ${oldDesc.substring(0, 80)}...`);
      console.log(`  NEW desc : ${desc} (${desc.length}c)`);

      if (!DRY_RUN) {
        const newHtml = processHtml(html, title, desc);
        if (newHtml !== html) {
          fs.writeFileSync(filePath, newHtml, 'utf8');
          console.log(`  ✅ Written`);
        } else {
          console.log(`  ⚠  No regex match — check HTML structure`);
        }
      }
      processed++;
    } catch (e) {
      console.error(`  ❌ Error: ${e.message}`);
      errors++;
    }
  }

  console.log(`\n${'─'.repeat(70)}`);
  console.log(`${siteName.toUpperCase()} → processed: ${processed}, skipped: ${skipped}, errors: ${errors}`);
  if (warnings.length) {
    console.log(`Warnings:`);
    warnings.forEach(w => console.log(`  ${w}`));
  }
}

// ─── Main ─────────────────────────────────────────────────────────────────────
console.log(`\noptimize-meta-tags.js — Meta Title & Description Optimizer`);
console.log(`Mode: ${DRY_RUN ? '🔍 DRY RUN (read-only)' : '✏️  LIVE (writing files)'}`);
if (SITE_FILTER) console.log(`Filter: --site ${SITE_FILTER}`);

const sitesToProcess = SITE_FILTER
  ? [SITE_FILTER]
  : ['nika', 'nar', 'neary', 'fixlify'];

for (const name of sitesToProcess) {
  if (!SITES[name]) { console.error(`Unknown site: ${name}`); process.exit(1); }
  processSite(name);
}

console.log('\n✅ All done!');
