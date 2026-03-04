#!/usr/bin/env node
// inject-answer-capsule.js — Injects AI-optimised "Quick Answer" capsules
// Skips pages that already have answer-capsule
// Usage: node inject-answer-capsule.js [--dry-run] [--site nar|neary|fixlify|nika]

const fs   = require('fs');
const path = require('path');

const args      = process.argv.slice(2);
const DRY_RUN   = args.includes('--dry-run');
const SITE_FILTER = (() => { const i = args.indexOf('--site'); return i !== -1 ? args[i+1] : null; })();

// ─── Site Configs ─────────────────────────────────────────────────────────────
const SITES = {
  nar: {
    dir:    'C:/nappliancerepair',
    brand:  'N Appliance Repair',
    phone:  '(437) 524-1053',
    // NAR style — blue/white professional
    capsuleStyle: `background:#EFF6FF;border-left:4px solid #2563EB;padding:1rem 1.25rem;margin:1rem auto;max-width:900px;border-radius:0 8px 8px 0;font-family:'Instrument Sans',sans-serif`,
    labelStyle:   `font-size:.7rem;font-weight:700;letter-spacing:.08em;color:#2563EB;text-transform:uppercase;margin-bottom:.4rem`,
    textStyle:    `margin:0;color:#1E3A5F;font-size:.9rem;line-height:1.6`,
    // Inject before this marker
    injectBefore: '<!-- Trust Bar -->',
    fallbackBefore: '<div class="trust-bar"',
  },
  neary: {
    dir:    'C:/appliancerepairneary',
    brand:  'Appliance Repair Neary',
    phone:  '(437) 524-1053',
    capsuleStyle: `background:#E3F2FD;border-left:4px solid #1976D2;padding:1rem 1.25rem;margin:1rem auto;max-width:920px;border-radius:0 10px 10px 0;font-family:'Rubik',sans-serif`,
    labelStyle:   `font-size:.7rem;font-weight:700;letter-spacing:.08em;color:#1565C0;text-transform:uppercase;margin-bottom:.4rem`,
    textStyle:    `margin:0;color:#0D3B66;font-size:.9rem;line-height:1.6`,
    injectBefore: '<!-- Trust Bar -->',
    fallbackBefore: '<div class="page-trust-bar"',
  },
  fixlify: {
    dir:    'C:/fixlifyservices',
    brand:  'Fixlify Appliance Services',
    phone:  '(437) 524-1053',
    // FIXLIFY dark theme — navy/amber
    capsuleStyle: `background:#1A1A2E;border-left:4px solid #F59E0B;padding:1rem 1.25rem;margin:1rem auto;max-width:920px;border-radius:0 10px 10px 0;font-family:'Outfit',sans-serif`,
    labelStyle:   `font-size:.7rem;font-weight:700;letter-spacing:.08em;color:#F59E0B;text-transform:uppercase;margin-bottom:.4rem`,
    textStyle:    `margin:0;color:#CBD5E1;font-size:.9rem;line-height:1.6`,
    injectBefore: '<!-- Trust Strip -->',
    fallbackBefore: '<div class="page-trust-bar"',
  },
  nika: {
    dir:    'C:/NikaApplianceRepair',
    brand:  'Nika Appliance Repair',
    phone:  '(437) 524-1053',
    capsuleStyle: `background:#EFF6FF;border-left:4px solid #2563EB;padding:1rem 1.25rem;margin:1rem auto;max-width:900px;border-radius:0 8px 8px 0`,
    labelStyle:   `font-size:.7rem;font-weight:700;letter-spacing:.08em;color:#2563EB;text-transform:uppercase;margin-bottom:.4rem`,
    textStyle:    `margin:0;color:#1E3A5F;font-size:.9rem;line-height:1.6`,
    injectBefore: '<!-- Trust Bar -->',
    fallbackBefore: '<div class="trust-bar"',
  },
};

// ─── Page Classifier (same as optimize-meta-tags.js) ─────────────────────────
const SERVICES = ['dishwasher','fridge','refrigerator','washer','dryer','oven','stove','microwave','freezer','range','cooktop','appliance','air-conditioner'];
const BRANDS   = ['samsung','lg','whirlpool','bosch','frigidaire','kenmore','ge','miele','maytag','kitchenaid','electrolux','amana','jenn-air','sub-zero','wolf','speed-queen','fisher-paykel','haier','dacor','thermador','viking','aeg','blomberg','beko'];
const CITIES   = ['toronto','mississauga','brampton','scarborough','north-york','etobicoke','oakville','markham','richmond-hill','vaughan','ajax','pickering','oshawa','burlington','hamilton','bayview-village','birchcliff','cabbagetown','danforth-village','davisville-village','don-mills','forest-hill','humber-valley','islington-village','lawrence-park','leaside','leslieville','liberty-village','midtown','rosedale','parkdale','beaches','annex','yorkville','kensington','little-italy','greektown','chinatown','riverdale','swansea','bloor-west','high-park','junction','weston','york','east-york','west-hill','agincourt','malvern','highland-creek','rouge','morningside','woodbine','eglinton','downtown','midtown-toronto','thornhill','woodbridge','stouffville','aurora','newmarket','port-credit','streetsville','meadowvale','concord','maple','whitby','courtice','bowmanville','guelph','kitchener','cambridge','north-toronto','east-toronto','west-toronto','york-mills','willowdale','bathurst','dufferin','wilson','sheppard','finch','steeles','scarborough-village','victoria-park','the-beaches','bloor-yorkville','queen-west','baby-point','old-toronto'];

const BRAND_DISPLAY = {lg:'LG',ge:'GE',aeg:'AEG',samsung:'Samsung',whirlpool:'Whirlpool',bosch:'Bosch',frigidaire:'Frigidaire',kenmore:'Kenmore',miele:'Miele',maytag:'Maytag',kitchenaid:'KitchenAid',electrolux:'Electrolux',amana:'Amana','jenn-air':'Jenn-Air','sub-zero':'Sub-Zero',wolf:'Wolf','speed-queen':'Speed Queen','fisher-paykel':'Fisher & Paykel',haier:'Haier',dacor:'Dacor',thermador:'Thermador',viking:'Viking',blomberg:'Blomberg',beko:'Beko'};

const SKIP_FILES = new Set(['404.html','ajax.html','book.html','about.html','contact.html','brands.html','compare.html','areas.html','team.html','preview.html','locations.html','blog-nika-appliance-repair.html','sitemap.html','privacy.html','terms.html','services.html']);
const SKIP_DIRS  = new Set(['node_modules','.git','_queue','assets','css','js','images','fonts','components','templates','styles','backups','backup','old','archive']);

function toTitleCase(s) { return s.split('-').map(w=>w[0].toUpperCase()+w.slice(1)).join(' '); }

function extract(filename) {
  const base = filename.replace(/\.html$/,'');
  let brand=null, city=null, service=null;
  for (const b of BRANDS) if (base===b||base.startsWith(b+'-')) { brand=b; break; }
  for (const c of CITIES) if (base===c||base.endsWith('-'+c)) { city=c; break; }
  for (const s of SERVICES) if (base.includes(s)) { service=s; break; }
  const isInstallation = base.includes('-installation');
  return { brand, city, service, isInstallation, base };
}

function classify(filename, relPath) {
  if (relPath.startsWith('blog/')||relPath.includes('/blog/')) return 'skip';
  if (relPath.startsWith('_queue/')||relPath.includes('/_queue/')) return 'skip';
  if (SKIP_FILES.has(filename)) return 'skip';
  if (/^landing/.test(filename)||filename.startsWith('landing-')) return 'skip';
  if (filename==='index.html') return 'homepage';
  const b = filename.replace(/\.html$/,'');
  if (b.startsWith('emergency')) return 'emergency';
  if (b.endsWith('-cost')||b.endsWith('-pricing')||b.includes('-repair-cost')||b.includes('appliance-repair-cost')||b.includes('average-appliance-repair')) return 'cost-guide';
  if (/-not-/.test(b)||/wont-/.test(b)||b.endsWith('-leaking')||b.endsWith('-making-noise')) return 'problem';
  if (b.includes('-installation')) return 'installation';
  const { brand, city, service } = extract(b+'.html');
  if (CITIES.includes(b)) return 'city-hub';
  if (brand&&service&&city) return 'brand-service-city';
  if (brand&&city&&!service) return 'brand-city';
  if (brand&&service&&!city) return 'brand-service';
  if (service&&city&&!brand) return 'service-city';
  if (brand&&!city&&!service) return 'brand';
  if (service&&b.includes('-repair')) return 'service';
  return 'other';
}

// ─── Capsule Text Generator ───────────────────────────────────────────────────
function buildCapsuleText(pageType, info, site) {
  const { brand, city, service, isInstallation } = info;
  const { brand: siteBrand, phone } = site;

  const cityLabel    = city    ? toTitleCase(city)    : 'Toronto';
  const serviceLabel = service ? toTitleCase(service) : 'Appliance';
  const brandLabel   = brand   ? (BRAND_DISPLAY[brand]||toTitleCase(brand)) : '';
  const action       = isInstallation ? 'installation' : 'repair';
  const cost         = isInstallation ? 'CAD $150-$250' : 'CAD $120-$350';

  const base = `${siteBrand} provides same-day`;
  const tail = `Call ${phone} — available 7 days a week, including evenings. Typical cost ${cost}. All major brands: Samsung, LG, Whirlpool, Bosch, GE, Maytag. Most jobs completed in 1–2 hours on the first visit. 90-day parts & labour warranty.`;

  switch (pageType) {
    case 'homepage':
      return `${base} appliance repair in Toronto & GTA. ${tail}`;
    case 'service':
      return `${base} ${serviceLabel.toLowerCase()} ${action} in Toronto. ${tail}`;
    case 'service-city':
      return `${base} ${serviceLabel.toLowerCase()} ${action} in ${cityLabel}. ${tail}`;
    case 'brand':
      return `${base} ${brandLabel} appliance repair in Toronto. ${tail}`;
    case 'brand-service':
      return `${base} ${brandLabel} ${serviceLabel.toLowerCase()} ${action} in Toronto. ${tail}`;
    case 'brand-city':
      return `${base} ${brandLabel} appliance repair in ${cityLabel}. ${tail}`;
    case 'brand-service-city':
      return `${base} ${brandLabel} ${serviceLabel.toLowerCase()} ${action} in ${cityLabel}. ${tail}`;
    case 'city-hub':
      return `${base} appliance repair in ${cityLabel}. ${tail}`;
    case 'installation':
      return `${base} ${serviceLabel.toLowerCase()} installation in ${cityLabel}. ${tail}`;
    case 'emergency':
      return `${siteBrand} provides 24/7 emergency appliance repair in Toronto & GTA. ${tail}`;
    case 'cost-guide':
      return `How much does ${serviceLabel.toLowerCase()} repair cost in Toronto? Typical range: ${cost}. ${siteBrand} offers flat $65 diagnostic fee, transparent pricing, no hidden charges. Call ${phone}.`;
    case 'problem':
      return `${base} ${serviceLabel.toLowerCase()} repair in Toronto including ${info.base.replace(/-/g,' ')} issues. ${tail}`;
    default:
      return null;
  }
}

// ─── HTML Capsule Builder ─────────────────────────────────────────────────────
function buildCapsuleHtml(text, site) {
  return `<div class="answer-capsule" style="${site.capsuleStyle}" itemscope itemtype="https://schema.org/Service">
  <div style="${site.labelStyle}">Quick Answer</div>
  <p style="${site.textStyle}" itemprop="description">${text}</p>
</div>\n`;
}

// ─── File Walker ──────────────────────────────────────────────────────────────
function walk(dir, prefix='') {
  const out = [];
  let items; try { items = fs.readdirSync(dir,{withFileTypes:true}); } catch { return out; }
  for (const item of items) {
    if (item.isDirectory()) {
      if (SKIP_DIRS.has(item.name)) continue;
      out.push(...walk(path.join(dir,item.name), prefix+item.name+'/'));
    } else if (item.name.endsWith('.html')) {
      out.push(prefix+item.name);
    }
  }
  return out;
}

// ─── Process Site ─────────────────────────────────────────────────────────────
function processSite(siteName) {
  const site = SITES[siteName];
  const dir  = site.dir;

  console.log(`\n${'═'.repeat(70)}`);
  console.log(`Site: ${siteName.toUpperCase()}  (${dir})`);
  console.log(`${'═'.repeat(70)}`);

  if (!fs.existsSync(dir)) { console.error(`  ❌ Dir not found: ${dir}`); return; }

  const files = walk(dir);
  let injected=0, alreadyHas=0, noMarker=0, skipped=0, errors=0;

  for (const relPath of files) {
    const filename = path.basename(relPath);
    const pageType = classify(filename, relPath);
    if (pageType==='skip'||pageType==='other') { skipped++; continue; }

    const info = extract(filename);
    const text = buildCapsuleText(pageType, info, site);
    if (!text) { skipped++; continue; }

    const filePath = path.join(dir, relPath);
    try {
      const html = fs.readFileSync(filePath,'utf8');

      // Skip if already has capsule (any form)
      if (html.includes('answer-capsule') || html.includes('hero-capsule') ||
          html.includes('class="answer-box"') || html.includes("class='answer-box'") ||
          html.includes('Who does') || html.includes('does — call')) { alreadyHas++; continue; }

      // Find injection point
      let marker = site.injectBefore;
      let idx = html.indexOf(marker);
      if (idx === -1) {
        // Fallback: before trust-bar div
        marker = site.fallbackBefore;
        idx = html.indexOf(marker);
      }
      if (idx === -1) {
        console.log(`  ⚠ No marker found: ${relPath}`);
        noMarker++;
        continue;
      }

      const capsuleHtml = buildCapsuleHtml(text, site);
      console.log(`\n[${pageType}] ${relPath}`);
      console.log(`  Text: ${text.substring(0,100)}...`);

      if (!DRY_RUN) {
        const newHtml = html.slice(0, idx) + capsuleHtml + html.slice(idx);
        fs.writeFileSync(filePath, newHtml, 'utf8');
        console.log(`  ✅ Injected`);
      }
      injected++;
    } catch(e) {
      console.error(`  ❌ ${relPath}: ${e.message}`);
      errors++;
    }
  }

  console.log(`\n${'─'.repeat(70)}`);
  console.log(`${siteName.toUpperCase()} → injected: ${injected}, already had: ${alreadyHas}, no-marker: ${noMarker}, skipped: ${skipped}, errors: ${errors}`);
}

// ─── Main ─────────────────────────────────────────────────────────────────────
console.log(`\ninject-answer-capsule.js`);
console.log(`Mode: ${DRY_RUN ? '🔍 DRY RUN' : '✏️  LIVE'}`);
if (SITE_FILTER) console.log(`Filter: --site ${SITE_FILTER}`);

const sites = SITE_FILTER ? [SITE_FILTER] : ['nar','neary','fixlify'];
for (const name of sites) {
  if (!SITES[name]) { console.error(`Unknown site: ${name}`); process.exit(1); }
  processSite(name);
}
console.log('\n✅ Done!');
