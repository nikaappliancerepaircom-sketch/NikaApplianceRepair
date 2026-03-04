#!/usr/bin/env node
/**
 * patch-body-content.js
 * Patches the body content of generated location pages with unique city-specific content.
 * Fixes the bug where replaceBodyContent couldn't find 'content-body' (actual class: 'content-intro').
 *
 * Usage:
 *   node patch-body-content.js [--dry-run] [--site=nar|neary|fixlify|all] [--file=dryer-repair-bradford]
 */

const fs    = require('fs');
const path  = require('path');
const https = require('https');

const CLAUDE_KEY   = process.env.ANTHROPIC_API_KEY || '';
const CLAUDE_MODEL = 'claude-sonnet-4-6';
const DELAY_MS     = 1000;

const args     = process.argv.slice(2);
const DRY_RUN  = args.includes('--dry-run');
const SITE_ARG = (args.find(a => a.startsWith('--site=')) || '').replace('--site=', '') || 'all';
const FILE_ARG = (args.find(a => a.startsWith('--file=')) || '').replace('--file=', '') || '';

// ── Sites ─────────────────────────────────────────────────────────────────────
const SITES = {
  nar: {
    dir: 'C:/nappliancerepair', domain: 'https://nappliancerepair.com',
    name: 'N Appliance Repair', phone: '(437) 524-1053',
    angle: 'professional Toronto GTA service, trusted since 2017, $65 flat diagnostic fee, licensed & insured technicians',
  },
  neary: {
    dir: 'C:/appliancerepairneary', domain: 'https://appliancerepairneary.com',
    name: 'Appliance Repair Near Me', phone: '(437) 524-1053',
    angle: 'convenient local service near you, technicians dispatched from your neighbourhood, same-day booking, $65 diagnostic',
  },
  fixlify: {
    dir: 'C:/fixlifyservices', domain: 'https://fixlifyservices.com',
    name: 'Fixlify Appliance Services', phone: '(437) 524-1053',
    angle: 'transparent $65 diagnostic pricing, modern brand, expert technicians, same-day service, no hidden fees',
  },
};

// ── City info ─────────────────────────────────────────────────────────────────
const CITIES = {
  'newmarket': {
    label: 'Newmarket', region: 'York Region', population: '~95,000',
    distance: '50km north of Toronto on Highway 400',
    housing: 'Mix of historic downtown homes (1900s–1960s) near Main Street, 1970s–1980s subdivisions in Central Newmarket and Huron Heights, and fast-growing new developments in Woodland Hill, Stonehaven, Glenway, and Summerhill Estates.',
    applianceTrends: 'New builds in Glenway and Woodland Hill predominantly have Samsung and LG front-load pairs. Older homes on Prospect and Eagle streets run Whirlpool and GE top-loaders. York Region water hardness (120–140 mg/L) causes scale buildup.',
    neighbourhoods: ['Woodland Hill', 'Stonehaven', 'Glenway', 'Huron Heights', 'Central Newmarket', 'Summerhill Estates', 'Rogers Reservoir area', 'Armitage'],
    uniqueNote: 'Many new-build appliances in Newmarket are just now coming out of manufacturer warranty, making independent repair the cost-effective choice.',
  },
  'bradford': {
    label: 'Bradford', region: 'Simcoe County (Bradford West Gwillimbury)', population: '~48,000',
    distance: '65km north of Toronto on Highway 400',
    housing: 'Predominantly newer builds from the 2000s–2020s in master-planned subdivisions. Some older semi-detached homes in the Bradford town centre. Rural properties in Bond Head and Holland Landing areas.',
    applianceTrends: 'Near-universal adoption of LG, Samsung, and Whirlpool in new builds. Many appliances purchased at house closing (2010–2020) are entering their first major repair cycle. Hard water from Simcoe County municipal supply accelerates scale buildup.',
    neighbourhoods: ['Bradford town centre', 'Holland Landing', 'Bond Head', 'Summerlyn Village', 'Green Valley Estates', 'Harvest Hills', 'Marshview neighbourhoods'],
    uniqueNote: 'Bradford is a rapidly developing exurb where thousands of homes built 2010–2022 have appliances now exiting warranty. Residents often face their first independent repair call.',
  },
  'richmond-hill': {
    label: 'Richmond Hill', region: 'York Region', population: '~220,000',
    distance: '30km north of Toronto on Yonge Street and Hwy 404',
    housing: 'Mix of established 1980s–1990s subdivisions in South Richvale, Bayview Hill, and Mill Pond, plus newer upscale developments in Langstaff, Jefferson, and Elgin Mills. Many large executive homes with premium appliance suites.',
    applianceTrends: 'Premium brands dominate: Miele dishwashers, Sub-Zero fridges, Wolf ranges in Bayview Hill executive homes. LG and Samsung lead in 2000s subdivisions. York Region water hardness hits dishwashers and washing machines with scale buildup.',
    neighbourhoods: ['Bayview Hill', 'South Richvale', 'Mill Pond', 'Langstaff', 'Jefferson', 'Elgin Mills', 'Crosby', 'North Leslie', 'Oak Ridges'],
    uniqueNote: 'Richmond Hill has one of the highest concentrations of Miele and premium European appliances in the GTA, requiring technicians with specialized training for these brands.',
  },
  'north-york': {
    label: 'North York', region: 'City of Toronto', population: '~670,000',
    distance: 'North Toronto — Yonge-Sheppard to Steeles Ave corridor',
    housing: 'Diverse mix: 1960s–1970s high-rise apartments along Yonge and Sheppard, 1950s–1980s bungalows in Don Mills and Willowdale, upscale condos near North York Centre, newer townhomes in Bayview Village.',
    applianceTrends: 'Condo towers along Yonge and Sheppard have integrated LG and Samsung units. Willowdale bungalows run older Whirlpool and GE machines. Bayview Village homes favour premium brands. Hard water from Toronto municipal supply causes spray arm and inlet valve issues.',
    neighbourhoods: ['Willowdale', 'Don Mills', 'Bayview Village', 'North York Centre', 'Newtonbrook', 'Lansing', 'Bathurst Manor', 'Jane-Lawrence', 'Emery'],
    uniqueNote: 'North York is the most densely populated part of the GTA with thousands of high-rise units — condo appliance logistics (elevator booking, tight kitchens) is a core competency for our techs.',
  },
};

// ── Service info ──────────────────────────────────────────────────────────────
const SERVICES = {
  'dishwasher-repair': { label: 'Dishwasher Repair', priceRange: '$120–$350', serviceType: 'DishwasherRepair' },
  'fridge-repair':     { label: 'Refrigerator Repair', priceRange: '$150–$400', serviceType: 'RefrigeratorRepair' },
  'washer-repair':     { label: 'Washer Repair', priceRange: '$120–$320', serviceType: 'WasherRepair' },
  'dryer-repair':      { label: 'Dryer Repair', priceRange: '$100–$280', serviceType: 'DryerRepair' },
  'oven-repair':       { label: 'Oven Repair', priceRange: '$130–$350', serviceType: 'OvenRepair' },
  'stove-repair':      { label: 'Stove Repair', priceRange: '$130–$350', serviceType: 'StoveRepair' },
};

// ── All generated pages to patch ──────────────────────────────────────────────
const PAGES = [
  // NAR
  { site:'nar', type:'service', service:'dishwasher-repair', city:'north-york' },
  { site:'nar', type:'service', service:'dryer-repair',      city:'north-york' },
  { site:'nar', type:'service', service:'oven-repair',       city:'north-york' },
  { site:'nar', type:'service', service:'stove-repair',      city:'north-york' },
  { site:'nar', type:'service', service:'dishwasher-repair', city:'richmond-hill' },
  { site:'nar', type:'service', service:'fridge-repair',     city:'richmond-hill' },
  { site:'nar', type:'service', service:'washer-repair',     city:'richmond-hill' },
  { site:'nar', type:'service', service:'dryer-repair',      city:'richmond-hill' },
  { site:'nar', type:'service', service:'oven-repair',       city:'richmond-hill' },
  { site:'nar', type:'service', service:'stove-repair',      city:'richmond-hill' },
  { site:'nar', type:'city-hub', service:null,              city:'newmarket' },
  { site:'nar', type:'service', service:'dishwasher-repair', city:'newmarket' },
  { site:'nar', type:'service', service:'fridge-repair',     city:'newmarket' },
  { site:'nar', type:'service', service:'washer-repair',     city:'newmarket' },
  { site:'nar', type:'service', service:'dryer-repair',      city:'newmarket' },
  { site:'nar', type:'service', service:'oven-repair',       city:'newmarket' },
  { site:'nar', type:'service', service:'stove-repair',      city:'newmarket' },
  { site:'nar', type:'city-hub', service:null,              city:'bradford' },
  { site:'nar', type:'service', service:'dishwasher-repair', city:'bradford' },
  { site:'nar', type:'service', service:'fridge-repair',     city:'bradford' },
  { site:'nar', type:'service', service:'washer-repair',     city:'bradford' },
  { site:'nar', type:'service', service:'dryer-repair',      city:'bradford' },
  { site:'nar', type:'service', service:'oven-repair',       city:'bradford' },
  { site:'nar', type:'service', service:'stove-repair',      city:'bradford' },
  // NEARY
  { site:'neary', type:'service', service:'dishwasher-repair', city:'newmarket' },
  { site:'neary', type:'service', service:'fridge-repair',     city:'newmarket' },
  { site:'neary', type:'service', service:'washer-repair',     city:'newmarket' },
  { site:'neary', type:'service', service:'dryer-repair',      city:'newmarket' },
  { site:'neary', type:'service', service:'oven-repair',       city:'newmarket' },
  { site:'neary', type:'service', service:'stove-repair',      city:'newmarket' },
  { site:'neary', type:'service', service:'dishwasher-repair', city:'bradford' },
  { site:'neary', type:'service', service:'fridge-repair',     city:'bradford' },
  { site:'neary', type:'service', service:'washer-repair',     city:'bradford' },
  { site:'neary', type:'service', service:'dryer-repair',      city:'bradford' },
  { site:'neary', type:'service', service:'oven-repair',       city:'bradford' },
  { site:'neary', type:'service', service:'stove-repair',      city:'bradford' },
  // FIXLIFY
  { site:'fixlify', type:'city-hub', service:null,              city:'newmarket' },
  { site:'fixlify', type:'service', service:'dishwasher-repair', city:'newmarket' },
  { site:'fixlify', type:'service', service:'fridge-repair',     city:'newmarket' },
  { site:'fixlify', type:'service', service:'washer-repair',     city:'newmarket' },
  { site:'fixlify', type:'service', service:'dryer-repair',      city:'newmarket' },
  { site:'fixlify', type:'service', service:'oven-repair',       city:'newmarket' },
  { site:'fixlify', type:'service', service:'stove-repair',      city:'newmarket' },
  { site:'fixlify', type:'city-hub', service:null,              city:'bradford' },
  { site:'fixlify', type:'service', service:'dishwasher-repair', city:'bradford' },
  { site:'fixlify', type:'service', service:'fridge-repair',     city:'bradford' },
  { site:'fixlify', type:'service', service:'washer-repair',     city:'bradford' },
  { site:'fixlify', type:'service', service:'dryer-repair',      city:'bradford' },
  { site:'fixlify', type:'service', service:'oven-repair',       city:'bradford' },
  { site:'fixlify', type:'service', service:'stove-repair',      city:'bradford' },
];

// ── Claude Sonnet 4.6 API call ─────────────────────────────────────────────────
function gemini(prompt) {
  return new Promise((resolve, reject) => {
    if (!CLAUDE_KEY) return reject(new Error('ANTHROPIC_API_KEY not set. Add it to .env file.'));
    const body = JSON.stringify({
      model: CLAUDE_MODEL,
      max_tokens: 4096,
      temperature: 0.85,
      messages: [{ role: 'user', content: prompt }],
    });
    const req = https.request({
      hostname: 'api.anthropic.com',
      path: '/v1/messages',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
        'x-api-key': CLAUDE_KEY,
        'anthropic-version': '2023-06-01',
      },
    }, res => {
      let data = '';
      res.on('data', d => data += d);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          const text = json?.content?.[0]?.text;
          if (text) resolve(text.trim());
          else reject(new Error('No text in Claude response: ' + data.slice(0, 200)));
        } catch(e) { reject(e); }
      });
    });
    req.on('error', reject);
    req.setTimeout(60000, () => { req.destroy(new Error('Timeout')); });
    req.write(body);
    req.end();
  });
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// ── Generate body content ──────────────────────────────────────────────────────
async function generateBody(siteName, type, service, city) {
  const site = SITES[siteName];
  const c = CITIES[city];
  const s = service ? SERVICES[service] : null;
  const serviceLabel = s ? s.label : 'Appliance Repair';

  if (type === 'city-hub') {
    const prompt = `Write exactly 5 HTML paragraphs (each in <p> tags, no class/id attributes) for the body section of a local appliance repair city hub page.

Business: ${site.name}
Phone: ${site.phone}
City: ${c.label}, Ontario
Region: ${c.region}, population ${c.population}
Location: ${c.distance}
Business angle: ${site.angle}

City housing: ${c.housing}
Appliance trends: ${c.applianceTrends}
Neighbourhoods: ${c.neighbourhoods.join(', ')}
Unique note: ${c.uniqueNote}

Paragraph requirements:
1. City geography and housing mix — how does housing type affect appliance types?
2. Most common appliance brands by neighbourhood — specific model series where possible.
3. Most common appliance failures in this city and WHY — tied to local water, housing age, brand patterns.
4. How service works logistically — dispatch, travel time, same-day availability, any unique access considerations.
5. CTA: mention ${c.label}, ${site.name}, phone ${site.phone}, same-day, 90-day warranty.

Professional third-person tone. 130–180 words each. NO markdown, NO headings — pure <p> tags only.`;
    return await gemini(prompt);
  } else {
    const prompt = `Write exactly 5 HTML paragraphs (each in <p> tags, no class/id attributes) for the body section of a local appliance repair service page.

Business: ${site.name}
Phone: ${site.phone}
Service: ${serviceLabel} (price range: ${s.priceRange})
City: ${c.label}, Ontario
Region: ${c.region}
Business angle: ${site.angle}

City housing: ${c.housing}
Appliance trends: ${c.applianceTrends}
Neighbourhoods: ${c.neighbourhoods.join(', ')}
Unique note: ${c.uniqueNote}

Paragraph requirements:
1. ${serviceLabel} landscape in ${c.label} — which neighbourhoods have which appliance types/brands?
2. The #1 most common ${serviceLabel.toLowerCase().split(' ')[0]} failure in ${c.label} and WHY — model-specific details, local water/housing causes.
3. A second major failure type — technical diagnosis approach, parts carried on the truck.
4. How ${site.name} handles ${serviceLabel.toLowerCase()} in ${c.label} — dispatch, arrival time, condo/house logistics.
5. CTA: mention ${c.label}, ${serviceLabel.toLowerCase()}, ${site.name}, phone ${site.phone}, same-day, 90-day warranty.

Professional third-person tone. 120–170 words each. NO markdown, NO headings — pure <p> tags only.`;
    return await gemini(prompt);
  }
}

// ── Build h2 heading for content-intro ───────────────────────────────────────
function buildH2(siteName, type, service, city) {
  const c = CITIES[city];
  const s = service ? SERVICES[service] : null;
  const serviceLabel = s ? s.label : 'Appliance Repair';
  if (type === 'city-hub') {
    return `<h2>${serviceLabel} in ${c.label} — Local Expertise, Same-Day Service</h2>`;
  }
  return `<h2>${serviceLabel} in ${c.label} — Trusted Local Technicians</h2>`;
}

// ── Replace content body section in HTML ──────────────────────────────────────
function replaceContentIntro(html, h2, paragraphs) {
  const section = findContentSection(html);
  if (!section) return null;

  const endIdx = findContentEnd(html, section.contentStart);
  if (endIdx === -1) return null;

  const before = html.slice(0, section.contentStart);
  const after  = html.slice(endIdx);

  const newContent = `\n${h2}\n${paragraphs}\n`;
  return before + newContent + after;
}

// ── Find content body div and its end in HTML ─────────────────────────────────
function findContentSection(html) {
  // Try in order: content-intro (NAR), content-body reveal (NEARY/FIXLIFY), content-body
  const patterns = [
    /<div class="content-intro[^"]*"[^>]*>/,
    /<div class="content-body[^"]*reveal[^"]*"[^>]*>/,
    /<div class="content-body[^"]*"[^>]*>/,
  ];
  for (const pat of patterns) {
    const m = html.match(pat);
    if (m) {
      const openIdx = html.indexOf(m[0]);
      const contentStart = openIdx + m[0].length;
      return { openTag: m[0], openIdx, contentStart };
    }
  }
  return null;
}

function findContentEnd(html, contentStart) {
  // Try in order: standard end markers
  const endMarkers = [
    '<!-- Service Details -->',       // NAR
    '<h2 class="section-title">',    // NEARY
    '<div class="pricing-card ',     // FIXLIFY
    '\n\n  <!-- ',                    // any comment section
    '</div>\n\n  <section ',          // fallback
  ];
  for (const marker of endMarkers) {
    const idx = html.indexOf(marker, contentStart);
    if (idx !== -1) {
      // For markers that come after the closing </div>, find the </div> before it
      if (marker.startsWith('<h2 class') || marker.startsWith('<div class="pricing')) {
        // The end IS the marker itself — we want to keep everything before it
        return idx;
      }
      // For comment markers, find the </div> just before the marker
      const closingDiv = html.lastIndexOf('</div>', idx);
      if (closingDiv !== -1 && closingDiv > contentStart) return closingDiv + 6;
      return idx;
    }
  }
  return -1;
}

// ── Check if page already has city-specific content ──────────────────────────
function alreadyPatched(html, cityLabel) {
  const section = findContentSection(html);
  if (!section) return false;
  const endIdx = findContentEnd(html, section.contentStart);
  if (endIdx === -1) return false;
  const introContent = html.slice(section.openIdx, endIdx);
  // Must have city label 3+ times AND enough content (5 paragraphs = 800+ chars)
  const matches = (introContent.match(new RegExp(cityLabel, 'g')) || []).length;
  return matches >= 3 && introContent.length > 800;
}

// ── Main ──────────────────────────────────────────────────────────────────────
async function main() {
  console.log(`\npatch-body-content.js — Mode: ${DRY_RUN ? 'DRY RUN' : 'LIVE'}`);
  if (SITE_ARG !== 'all') console.log(`Site filter: ${SITE_ARG}`);
  if (FILE_ARG) console.log(`File filter: ${FILE_ARG}`);

  let pages = PAGES;
  if (SITE_ARG !== 'all') pages = pages.filter(p => p.site === SITE_ARG);
  if (FILE_ARG) pages = pages.filter(p => {
    const slug = p.type === 'city-hub' ? p.city : `${p.service}-${p.city}`;
    return slug === FILE_ARG;
  });

  console.log(`Processing ${pages.length} pages...\n`);

  let patched = 0, skipped = 0, errors = 0;

  for (const page of pages) {
    const { site, type, service, city } = page;
    const slug = type === 'city-hub' ? city : `${service}-${city}`;
    const filePath = path.join(SITES[site].dir, `${slug}.html`);
    const cityConf = CITIES[city];

    if (!fs.existsSync(filePath)) {
      console.log(`  ⏭  NOT FOUND: [${site}] ${slug}`);
      skipped++;
      continue;
    }

    const html = fs.readFileSync(filePath, 'utf8');

    // Check if already patched
    if (alreadyPatched(html, cityConf.label)) {
      console.log(`  ✓  ALREADY PATCHED: [${site}] ${slug}`);
      skipped++;
      continue;
    }

    console.log(`\n▶ [${site.toUpperCase()}] ${slug}`);

    try {
      if (DRY_RUN) {
        console.log(`  [DRY] Would generate Gemini content for ${cityConf.label} ${service || 'hub'}`);
        patched++;
        continue;
      }

      // Generate new body content
      const bodyContent = await generateBody(site, type, service, city);
      const h2 = buildH2(site, type, service, city);

      // Replace content-intro section
      const newHtml = replaceContentIntro(html, h2, bodyContent);
      if (!newHtml) {
        console.error(`  ❌ Could not find content-intro section in ${slug}`);
        errors++;
        continue;
      }

      fs.writeFileSync(filePath, newHtml, 'utf8');
      console.log(`  ✅ Patched — body content (${bodyContent.length} chars)`);
      patched++;

      await sleep(DELAY_MS);
    } catch(e) {
      console.error(`  ❌ ${slug}: ${e.message}`);
      errors++;
      await sleep(2000);
    }
  }

  console.log(`\n${'─'.repeat(60)}`);
  console.log(`Patched: ${patched} | Skipped: ${skipped} | Errors: ${errors}`);
  if (DRY_RUN) console.log('[DRY RUN] No files changed.');
}

main().catch(console.error);
