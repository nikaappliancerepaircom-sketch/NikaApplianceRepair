/**
 * add-authority-links.js — Add 1 authority outbound link per service page
 * Fixes: external_entity_links (seo_advanced), external_authority_links (eeat), outbound_authority_links (geo_ai)
 * Only injects into pages that have no outbound authority links already.
 */
const fs = require('fs');
const path = require('path');

const SKIP_DIRS = new Set(['node_modules','.git','_queue','assets','css','js','images','fonts','components','templates','styles','backups','backup','old','archive','reports','tools','compare','preview','_drafts']);

// Authority links relevant to appliance repair, by keyword match
const AUTHORITY_MAP = [
  { keywords: ['dishwasher'], url: 'https://www.energystar.gov/products/dishwashers', anchor: 'ENERGY STAR dishwasher ratings' },
  { keywords: ['refrigerator', 'fridge'], url: 'https://www.energystar.gov/products/refrigerators', anchor: 'ENERGY STAR refrigerator guide' },
  { keywords: ['washer', 'washing machine'], url: 'https://www.energystar.gov/products/clothes_washers', anchor: 'ENERGY STAR washer certification' },
  { keywords: ['dryer'], url: 'https://www.energystar.gov/products/residential_clothes_dryers', anchor: 'ENERGY STAR dryer standards' },
  { keywords: ['oven', 'stove', 'range', 'cooktop'], url: 'https://www.energystar.gov/products/residential_gas_ranges', anchor: 'ENERGY STAR range guidelines' },
  { keywords: ['microwave'], url: 'https://www.consumerreports.org/appliances/microwaves/', anchor: 'Consumer Reports microwave buying guide' },
  { keywords: ['appliance'], url: 'https://www.energystar.gov/products/appliances', anchor: 'ENERGY STAR appliance directory' },
];

const MARKER = '<!-- AUTH-LINK-v1 -->';

const SITES = [
  'C:/NikaApplianceRepair',
  'C:/nappliancerepair',
  'C:/appliancerepairneary',
  'C:/fixlifyservices',
];

function walk(dir) {
  const out = [];
  let items;
  try { items = fs.readdirSync(dir, { withFileTypes: true }); } catch { return out; }
  for (const item of items) {
    if (item.isDirectory()) {
      if (SKIP_DIRS.has(item.name)) continue;
      out.push(...walk(path.join(dir, item.name)));
    } else if (item.name.endsWith('.html') && !item.name.includes('.bak')) {
      out.push(path.join(dir, item.name));
    }
  }
  return out;
}

function hasOutboundAuthority(html) {
  // Check for existing links to authority domains
  const authDomains = ['energystar.gov', 'consumerreports.org', 'canada.ca', 'ontario.ca', 'hc-sc.gc.ca', 'nrcan.gc.ca'];
  return authDomains.some(d => html.includes(d));
}

function pickAuthority(slug) {
  const lowerSlug = slug.toLowerCase();
  for (const entry of AUTHORITY_MAP) {
    if (entry.keywords.some(k => lowerSlug.includes(k))) return entry;
  }
  return AUTHORITY_MAP[AUTHORITY_MAP.length - 1]; // default: appliance
}

let totalFixed = 0;

for (const dir of SITES) {
  let fixed = 0;
  const files = walk(dir);

  for (const fp of files) {
    let html = fs.readFileSync(fp, 'utf8');

    // Skip if already has authority link or marker
    if (html.includes(MARKER) || hasOutboundAuthority(html)) continue;

    const slug = path.basename(fp, '.html');
    const authority = pickAuthority(slug);

    // Find a good paragraph to inject the link — look for last <p> before FAQ or schema section
    // Strategy: find the first <p> tag in main content area and inject a sentence with link
    const linkHtml = `${MARKER}\n<p class="authority-ref" style="font-size:.85rem;color:#6B7280;margin-top:1rem;">For appliance efficiency ratings and safety standards, see the <a href="${authority.url}" target="_blank" rel="noopener noreferrer">${authority.anchor}</a>.</p>`;

    // Inject before the voice-qa block or faq-section or schema section
    let inserted = false;

    // Try before voice-qa block
    if (html.includes('<!-- VOICE-QA-v1 -->')) {
      html = html.replace('<!-- VOICE-QA-v1 -->', linkHtml + '\n<!-- VOICE-QA-v1 -->');
      inserted = true;
    }
    // Try before faq-section
    else if (html.includes('<section class="faq-section"')) {
      html = html.replace('<section class="faq-section"', linkHtml + '\n<section class="faq-section"');
      inserted = true;
    }
    // Try before footer placeholder
    else if (html.includes('<div id="footer-placeholder"')) {
      html = html.replace('<div id="footer-placeholder"', linkHtml + '\n<div id="footer-placeholder"');
      inserted = true;
    }

    if (inserted) {
      fs.writeFileSync(fp, html, 'utf8');
      fixed++;
      totalFixed++;
    }
  }

  console.log(`${path.basename(dir)}: ${fixed} pages updated with authority link`);
}

console.log(`\nTotal: ${totalFixed} pages with authority outbound links`);
