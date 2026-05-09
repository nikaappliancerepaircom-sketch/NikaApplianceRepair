#!/usr/bin/env node
// add-voice-qa.js — injects styled question H3 + answer blocks for geo_ai score
// Marker: <!-- VOICE-QA-v1 --> (idempotent)

'use strict';
const fs   = require('fs');
const path = require('path');

const args     = process.argv.slice(2);
const DRY_RUN  = args.includes('--dry-run');

// Parse --site nar  OR  --site=nar
let SITE_KEY = null;
const siteEq = args.find(a => a.startsWith('--site='));
if (siteEq) {
  SITE_KEY = siteEq.split('=')[1];
} else {
  const siteIdx = args.indexOf('--site');
  if (siteIdx !== -1) SITE_KEY = args[siteIdx + 1];
}

const SITES = {
  nika: {
    dir:   'C:/NikaApplianceRepair',
    phone: '(437) 524-1053',
    brand: 'Nika Appliance Repair',
    diag:  '$89',
    style: {
      section: 'margin:2rem auto;max-width:880px;padding:0 1rem',
      heading: 'font-size:1.4rem;font-weight:700;color:#0F172A;margin:0 0 1.25rem;border-bottom:2px solid #2563EB;padding-bottom:.5rem;font-family:\'Instrument Sans\',sans-serif',
      card:    'background:#EFF6FF;border-left:4px solid #2563EB;border-radius:0 8px 8px 0;padding:1rem 1.25rem;margin-bottom:1rem',
      q:       'font-size:1rem;font-weight:600;color:#1E3A5F;margin:0 0 .4rem;font-family:\'Instrument Sans\',sans-serif',
      a:       'margin:0;color:#374151;font-size:.9rem;line-height:1.6',
    },
  },
  nar: {
    dir:   'C:/nappliancerepair',
    phone: '(437) 524-1053',
    brand: 'N Appliance Repair',
    diag:  '$89',
    style: {
      section: 'margin:2rem auto;max-width:900px;padding:0 1rem',
      heading: 'font-size:1.4rem;font-weight:700;color:#0F172A;margin:0 0 1.25rem;border-bottom:2px solid #2563EB;padding-bottom:.5rem;font-family:\'Instrument Sans\',sans-serif',
      card:    'background:#EFF6FF;border-left:4px solid #2563EB;border-radius:0 8px 8px 0;padding:1rem 1.25rem;margin-bottom:1rem',
      q:       'font-size:1rem;font-weight:600;color:#1E3A5F;margin:0 0 .4rem;font-family:\'Instrument Sans\',sans-serif',
      a:       'margin:0;color:#374151;font-size:.9rem;line-height:1.6',
    },
  },
};

const SKIP = new Set([
  '404.html','service-template.html','index.html','about.html',
  'privacy.html','terms.html','contact.html','brands.html',
  'locations.html','areas.html','book.html','accessibility.html',
  'sitemap.html','compare.html',
]);
const SKIP_DIRS = new Set([
  'node_modules','.git','_queue','assets','css','js','images',
  'fonts','reports','tools','backups','backup','old','archive',
  'compare','preview','_drafts','blog',
]);

const SERVICES = [
  'dishwasher','refrigerator','fridge','washer','dryer',
  'oven','stove','freezer','range','microwave','cooktop',
];

function extractInfo(filename) {
  const base = filename.replace(/\.html$/, '').replace(/-/g, ' ');
  let service = SERVICES.find(s => base.includes(s)) || 'appliance';
  // Derive city: everything after "repair " in the slug
  let city = 'the area';
  const repairIdx = base.indexOf('repair ');
  if (repairIdx !== -1) {
    city = base.slice(repairIdx + 'repair '.length).trim();
  } else {
    // city hub page e.g. "toronto" or "calgary"
    city = base.trim();
  }
  // Capitalize each word
  service = service.charAt(0).toUpperCase() + service.slice(1);
  city = city.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
  return { service, city };
}

function buildQAs(info, site) {
  const { service, city } = info;
  const svc = service.toLowerCase();
  return [
    {
      q: `How long does ${svc} repair take in ${city}?`,
      a: `Most ${svc} repairs in ${city} finish in 1–2 hours on the first visit. Technicians carry common parts on every van. Call ${site.phone} to book same-day service.`,
    },
    {
      q: `What does ${svc} repair cost in ${city}?`,
      a: `${service} repair in ${city} typically costs $120–$350 depending on the fault. A flat ${site.diag} diagnostic fee applies, waived when you proceed. Upfront quote before any work starts — no hidden charges.`,
    },
    {
      q: `Which ${svc} brands does ${site.brand} service in ${city}?`,
      a: `We repair all major brands in ${city}: Samsung, LG, Whirlpool, Bosch, GE, Frigidaire, Maytag, KitchenAid, Kenmore, and more. Every repair includes a 90-day parts and labour warranty.`,
    },
  ];
}

function buildHtml(info, site) {
  const qas  = buildQAs(info, site);
  const { style } = site;
  const rows = qas.map(({ q, a }) => `
  <div style="${style.card}">
    <h3 style="${style.q}">${q}</h3>
    <p style="${style.a}">${a}</p>
  </div>`).join('');

  return (
    '\n<!-- VOICE-QA-v1 -->\n' +
    `<section style="${style.section}" aria-label="Common questions about ${info.service} repair in ${info.city}">\n` +
    `  <h2 style="${style.heading}">Common Questions</h2>` +
    rows + '\n' +
    '</section>\n' +
    '<!-- /VOICE-QA-v1 -->\n'
  );
}

function walk(dir) {
  const out = [];
  let entries;
  try { entries = fs.readdirSync(dir, { withFileTypes: true }); }
  catch (e) { return out; }
  for (const e of entries) {
    if (e.isDirectory()) {
      if (!SKIP_DIRS.has(e.name)) out.push(...walk(path.join(dir, e.name)));
    } else if (
      e.name.endsWith('.html') &&
      !SKIP.has(e.name) &&
      !e.name.startsWith('landing-') &&
      !e.name.includes('.bak') &&
      !e.name.startsWith('preview-')
    ) {
      out.push(path.join(dir, e.name));
    }
  }
  return out;
}

const sitesToRun = SITE_KEY ? [SITE_KEY] : Object.keys(SITES);

for (const key of sitesToRun) {
  const site = SITES[key];
  if (!site) { console.error('Unknown site:', key); process.exit(1); }

  let injected = 0, skipped = 0, noMarker = 0;
  const noMarkerFiles = [];

  for (const filePath of walk(site.dir)) {
    let html = fs.readFileSync(filePath, 'utf8');

    // Skip if already injected (idempotent)
    if (html.includes('VOICE-QA-v1')) { skipped++; continue; }

    const info = extractInfo(path.basename(filePath));
    const block = buildHtml(info, site);

    // Injection order of preference:
    // 1. Before <section class="faq-section  (most pages)
    // 2. Before <!-- FAQ Section -->
    // 3. Before </main>
    // 4. Before </body>
    const markers = [
      /<section[^>]*class="[^"]*faq-section[^"]*"/i,
      /<!--\s*FAQ\s*Section\s*-->/i,
      /<\/main>/i,
      /<\/body>/i,
    ];

    let newHtml = html;
    let injectedHere = false;
    for (const marker of markers) {
      const m = newHtml.match(marker);
      if (m) {
        newHtml = newHtml.slice(0, m.index) + block + newHtml.slice(m.index);
        injectedHere = true;
        break;
      }
    }

    if (!injectedHere) {
      noMarker++;
      noMarkerFiles.push(path.basename(filePath));
      continue;
    }
    if (newHtml === html) { skipped++; continue; }

    if (!DRY_RUN) fs.writeFileSync(filePath, newHtml, 'utf8');
    injected++;
  }

  const mode = DRY_RUN ? '[DRY RUN] ' : '';
  console.log(`${mode}${key.toUpperCase()}: injected=${injected}, already_had=${skipped}, no_marker=${noMarker}`);
  if (noMarkerFiles.length) {
    console.log(`  No-marker files (first 10): ${noMarkerFiles.slice(0, 10).join(', ')}`);
  }
}
