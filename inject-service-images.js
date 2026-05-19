#!/usr/bin/env node
// Injects a hero <img> into service pages that have 0 images.
// Maps service type (from filename) to the appropriate generated image.
// Run from: node inject-service-images.js <site-dir> <site-domain> <site-label>

const fs = require('fs');
const path = require('path');

const siteDir = process.argv[2];
const siteDomain = process.argv[3]; // e.g. fixlifyservices.com
const siteLabel = process.argv[4];  // e.g. Edmonton or Calgary

if (!siteDir || !siteDomain) {
  console.error('Usage: node inject-service-images.js <site-dir> <site-domain> <city-label>');
  process.exit(1);
}

// Maps slug fragment → image filename
const SERVICE_IMAGE_MAP = {
  dishwasher: 'dishwasher-repair-service.webp',
  washer:     'washer-repair-service.webp',
  dryer:      'dryer-repair-service.webp',
  fridge:     'fridge-repair-service.webp',
  refrigerator: 'fridge-repair-service.webp',
  oven:       'oven-repair-service.webp',
  stove:      'stove-repair-service.webp',
  range:      'stove-repair-service.webp',
  // brand pages → generic technician
  lg:         'appliance-technician-hero.webp',
  samsung:    'appliance-technician-hero.webp',
  whirlpool:  'appliance-technician-hero.webp',
  frigidaire: 'appliance-technician-hero.webp',
  kenmore:    'appliance-technician-hero.webp',
  maytag:     'appliance-technician-hero.webp',
  bosch:      'appliance-technician-hero.webp',
  ge:         'appliance-technician-hero.webp',
  kitchenaid: 'appliance-technician-hero.webp',
  electrolux: 'appliance-technician-hero.webp',
  miele:      'appliance-technician-hero.webp',
};

// Alt text templates
const SERVICE_ALT_MAP = {
  dishwasher: `Certified dishwasher repair technician servicing ${siteLabel}`,
  washer:     `Professional washer repair service in ${siteLabel}`,
  dryer:      `Expert dryer repair technician in ${siteLabel}`,
  fridge:     `Refrigerator repair specialist in ${siteLabel}`,
  refrigerator: `Refrigerator repair specialist in ${siteLabel}`,
  oven:       `Oven repair professional in ${siteLabel}`,
  stove:      `Gas stove repair expert in ${siteLabel}`,
  range:      `Range repair technician in ${siteLabel}`,
};

function getImageForFile(filename) {
  const slug = path.basename(filename, '.html').toLowerCase();
  for (const [key, img] of Object.entries(SERVICE_IMAGE_MAP)) {
    if (slug.startsWith(key + '-') || slug.includes('-' + key + '-') || slug.endsWith('-' + key)) {
      return img;
    }
  }
  return 'appliance-technician-hero.webp';
}

function getAltForFile(filename) {
  const slug = path.basename(filename, '.html').toLowerCase();
  for (const [key, alt] of Object.entries(SERVICE_ALT_MAP)) {
    if (slug.startsWith(key + '-') || slug.includes('-' + key + '-') || slug.endsWith('-' + key)) {
      return alt;
    }
  }
  return `Appliance repair technician in ${siteLabel}`;
}

function hasImages(html) {
  return /<img\s/i.test(html);
}

function injectHeroImage(html, imgFile, altText) {
  // Inject after the first <h1> tag
  const h1End = html.indexOf('</h1>');
  if (h1End === -1) return html;

  const insertion = `
<figure class="service-hero-img" style="margin:1.5rem 0;border-radius:12px;overflow:hidden;max-height:420px;">
  <img src="/img/${imgFile}" alt="${altText}" width="1200" height="675" loading="eager" decoding="async" style="width:100%;height:auto;object-fit:cover;display:block;" />
</figure>`;

  return html.slice(0, h1End + 6) + insertion + html.slice(h1End + 6);
}

const htmlFiles = [];
function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory() && !['node_modules', '.git', 'lazy-method'].includes(entry.name)) {
      walk(full);
    } else if (entry.isFile() && entry.name.endsWith('.html')) {
      // Skip index, about, 404, terms, privacy pages
      const base = entry.name.toLowerCase();
      if (!['index.html','about.html','404.html','terms.html','privacy.html','contact.html'].includes(base)) {
        htmlFiles.push(full);
      }
    }
  }
}
walk(siteDir);

let processed = 0, skipped = 0, errors = 0;

for (const file of htmlFiles) {
  try {
    const html = fs.readFileSync(file, 'utf8');
    if (hasImages(html)) { skipped++; continue; }

    const imgFile = getImageForFile(file);
    const altText = getAltForFile(file);
    const newHtml = injectHeroImage(html, imgFile, altText);

    if (newHtml !== html) {
      fs.writeFileSync(file, newHtml, 'utf8');
      processed++;
    } else {
      skipped++;
    }
  } catch (e) {
    console.error(`  ERROR ${file}: ${e.message}`);
    errors++;
  }
}

console.log(`\n${siteLabel} done.`);
console.log(`  Injected: ${processed} | Already had images: ${skipped} | Errors: ${errors}`);
