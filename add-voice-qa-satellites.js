#!/usr/bin/env node
// add-voice-qa-satellites.js — NEARY + FIXLIFY voice Q&A injection
'use strict';
const fs   = require('fs');
const path = require('path');

const args     = process.argv.slice(2);
const DRY_RUN  = args.includes('--dry-run');
const SITE_KEY = args.indexOf('--site') !== -1 ? args[args.indexOf('--site')+1] : null;

const SITES = {
  neary: {
    dir: 'C:/appliancerepairneary',
    phone: '(437) 524-1053',
    brand: 'Appliance Repair Near Me',
    region: 'West GTA',
    sectionStyle: 'margin:2rem auto;max-width:920px;padding:0 1rem;font-family:Rubik,sans-serif',
    headingStyle: 'font-size:1.35rem;font-weight:700;color:#0D3B66;margin:0 0 1.25rem;border-bottom:2px solid #1976D2;padding-bottom:.5rem',
    cardStyle:    'background:#E3F2FD;border-left:4px solid #1976D2;border-radius:0 10px 10px 0;padding:1rem 1.25rem;margin-bottom:1rem',
    qStyle:       'font-size:1rem;font-weight:600;color:#0D3B66;margin:0 0 .4rem',
    aStyle:       'margin:0;color:#1A3A5C;font-size:.9rem;line-height:1.6',
  },
  fixlify: {
    dir: 'C:/fixlifyservices',
    phone: '(437) 524-1053',
    brand: 'Fixlify Appliance Services',
    region: 'East GTA',
    sectionStyle: 'margin:2rem auto;max-width:920px;padding:0 1rem;font-family:Outfit,sans-serif',
    headingStyle: 'font-size:1.35rem;font-weight:700;color:#F59E0B;margin:0 0 1.25rem;border-bottom:2px solid #F59E0B;padding-bottom:.5rem',
    cardStyle:    'background:#1A1A2E;border-left:4px solid #F59E0B;border-radius:0 10px 10px 0;padding:1rem 1.25rem;margin-bottom:1rem',
    qStyle:       'font-size:1rem;font-weight:600;color:#F59E0B;margin:0 0 .4rem',
    aStyle:       'margin:0;color:#CBD5E1;font-size:.9rem;line-height:1.6',
  },
};

const SKIP = new Set(['404.html','service-template.html','index.html','about.html','privacy.html','terms.html','contact.html','brands.html','locations.html','areas.html','book.html']);
const SKIP_DIRS = new Set(['node_modules','.git','_queue','assets','css','js','images','fonts','reports','tools','backups','backup','old','archive','compare','preview','_drafts','blog']);

const SERVICES = ['dishwasher','refrigerator','fridge','washer','dryer','oven','stove','freezer','range','microwave','cooktop','appliance'];
const CITIES   = ['toronto','mississauga','brampton','north york','scarborough','etobicoke','oakville','markham','richmond hill','vaughan','ajax','pickering','whitby','oshawa','burlington','hamilton','kitchener','london','guelph','barrie'];

function extractInfo(filename) {
  const base = filename.replace(/\.html$/,'').replace(/-/g,' ').toLowerCase();
  let service = SERVICES.find(s => base.includes(s)) || 'appliance';
  let city = CITIES.find(c => base.includes(c)) || 'Toronto';
  service = service.charAt(0).toUpperCase() + service.slice(1);
  city = city.split(' ').map(w=>w.charAt(0).toUpperCase()+w.slice(1)).join(' ');
  return { service, city };
}

function buildBlock(info, site) {
  const { service, city } = info;
  const svc = service.toLowerCase();

  const qas = [
    {
      q: `How long does ${svc} repair take in ${city}?`,
      a: `Most ${svc} repairs in ${city} are done in 1–2 hours on the first visit. Our techs carry common parts on the van, so no second trip needed. Book same-day: ${site.phone}.`,
    },
    {
      q: `How much does ${svc} repair cost in ${city}?`,
      a: `${service} repair in ${city} costs $120–$350 depending on the part and brand. Flat $65 diagnostic fee, waived with repair. Upfront quote — no surprises, 90-day warranty included.`,
    },
    {
      q: `Which ${svc} brands do you fix in ${city}?`,
      a: `We service Samsung, LG, Whirlpool, Bosch, GE, Frigidaire, Maytag, KitchenAid, Miele, Kenmore, and more in ${city}. All repairs come with a 90-day parts and labour warranty.`,
    },
  ];

  const cards = qas.map(({q,a}) => `  <div style="${site.cardStyle}" itemscope itemtype="https://schema.org/Question">
    <h3 style="${site.qStyle}" itemprop="name">${q}</h3>
    <p style="${site.aStyle}" itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">${a}</p>
  </div>`).join('\n');

  return `\n<!-- VOICE-QA-v1 -->\n<section style="${site.sectionStyle}" aria-label="Common questions about ${service} repair in ${city}">\n  <h2 style="${site.headingStyle}">Common Questions</h2>\n${cards}\n</section>\n<!-- /VOICE-QA-v1 -->\n`;
}

function walk(dir) {
  const out = [];
  try {
    for (const e of fs.readdirSync(dir,{withFileTypes:true})) {
      if (e.isDirectory()) { if (!SKIP_DIRS.has(e.name)) out.push(...walk(path.join(dir,e.name))); }
      else if (e.name.endsWith('.html') && !SKIP.has(e.name) && !e.name.startsWith('landing-') && !e.name.includes('.bak')) {
        out.push(path.join(dir,e.name));
      }
    }
  } catch(e) {}
  return out;
}

const sitesToRun = SITE_KEY ? [SITE_KEY] : Object.keys(SITES);

for (const key of sitesToRun) {
  const site = SITES[key];
  if (!site) { console.error('Unknown site:', key); continue; }

  let injected=0, skipped=0, noMarker=0;

  for (const filePath of walk(site.dir)) {
    let html = fs.readFileSync(filePath,'utf8');
    if (html.includes('VOICE-QA-v1')) { skipped++; continue; }

    const info = extractInfo(path.basename(filePath));
    const block = buildBlock(info, site);

    const markers = [
      /(<section[^>]*[iI][dD]="faq)/,
      /(<div[^>]*class="[^"]*faq)/i,
      /(<!-- FAQ|<!-- faq)/i,
      /<\/article>/i,
      /<\/main>/i,
      /<\/body>/i,
    ];

    let newHtml = html;
    let found = false;
    for (const m of markers) {
      const match = newHtml.match(m);
      if (match) {
        newHtml = newHtml.slice(0, match.index) + block + newHtml.slice(match.index);
        found = true;
        break;
      }
    }

    if (!found) { noMarker++; continue; }
    if (!DRY_RUN) fs.writeFileSync(filePath, newHtml, 'utf8');
    injected++;
  }

  console.log(`${key.toUpperCase()}: injected=${injected}, skipped=${skipped}, no_marker=${noMarker}`);
}
