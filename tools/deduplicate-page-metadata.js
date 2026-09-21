#!/usr/bin/env node

/** Fix duplicate titles/descriptions on published Toronto neighborhood pages. */

const fs = require('fs');
const path = require('path');

const mode = process.argv[2];
if (!['--check', '--write'].includes(mode)) {
  console.error('Usage: node tools/deduplicate-page-metadata.js --check|--write');
  process.exit(2);
}

const ROOT = path.resolve(__dirname, '..');
const SERVICES_DIR = path.join(ROOT, 'locations', 'services');
const GENERIC_TITLE = /^(Dishwasher|Dryer|Oven|Refrigerator|Stove|Washer) Repair Toronto \| Certified Experts \| \(437\) 524-1053 2026$/;

function replaceOne(html, pattern, replacement, file, label) {
  const matches = html.match(pattern) || [];
  if (matches.length !== 1) {
    throw new Error(`${file}: expected one ${label}, found ${matches.length}`);
  }
  return html.replace(pattern, replacement);
}

function updateNeighborhoodPage(file) {
  let html = fs.readFileSync(file, 'utf8');
  const currentTitleMatch = html.match(/<title>([^<]+)<\/title>/);
  const genericTitleMatch = currentTitleMatch?.[1].match(GENERIC_TITLE);
  if (!genericTitleMatch) {
    return { html, changed: false };
  }

  const service = genericTitleMatch[1];
  const h1Markup = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i)?.[1] || '';
  const h1Text = h1Markup.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
  const neighborhoodMatch = h1Text.match(/Repair in (.+?), Toronto/i);
  if (!neighborhoodMatch) {
    throw new Error(`${file}: cannot derive neighborhood from H1 text: ${h1Text}`);
  }
  const neighborhood = neighborhoodMatch[1].trim();
  const descriptiveTitle = `${service} Repair ${neighborhood}, Toronto | Same-Day Service`;
  const title = descriptiveTitle.length <= 65
    ? descriptiveTitle
    : `${service} Repair ${neighborhood}, Toronto | Nika`;
  const description = `${service} repair in ${neighborhood}, Toronto. $89 diagnostic waived with repair, upfront quote, 90-day warranty, and same-day appointments when available.`;

  if (title.length > 65) {
    throw new Error(`${file}: generated title is too long (${title.length}): ${title}`);
  }
  html = replaceOne(html, /<title>[^<]+<\/title>/, `<title>${title}</title>`, file, 'title');
  html = replaceOne(
    html,
    /<meta name="description" content="[^"]*">/,
    `<meta name="description" content="${description}">`,
    file,
    'meta description'
  );
  html = replaceOne(
    html,
    /<meta property="og:title" content="[^"]*">/,
    `<meta property="og:title" content="${title}">`,
    file,
    'Open Graph title'
  );
  html = replaceOne(
    html,
    /<meta property="og:description" content="[^"]*">/,
    `<meta property="og:description" content="${description}">`,
    file,
    'Open Graph description'
  );
  return { html, changed: true };
}

function updateBrandPage(slug, brand) {
  const file = path.join(ROOT, 'brands', `${slug}-appliance-repair-toronto.html`);
  let html = fs.readFileSync(file, 'utf8');
  const title = `${brand} Appliance Repair Toronto | Same-Day Service | Nika`;
  const currentTitle = html.match(/<title>([^<]+)<\/title>/)?.[1] || '';
  if (currentTitle.includes(brand)) {
    return { file, html, changed: false };
  }
  html = replaceOne(html, /<title>[^<]+<\/title>/, `<title>${title}</title>`, file, 'brand title');
  const ogPattern = /<meta property="og:title" content="[^"]*">/;
  if (ogPattern.test(html)) {
    html = replaceOne(
      html,
      ogPattern,
      `<meta property="og:title" content="${title}">`,
      file,
      'brand Open Graph title'
    );
  }
  return { file, html, changed: true };
}

let changed = 0;
const files = fs.readdirSync(SERVICES_DIR)
  .filter((name) => name.endsWith('.html'))
  .map((name) => path.join(SERVICES_DIR, name))
  .sort();

for (const file of files) {
  const result = updateNeighborhoodPage(file);
  if (!result.changed) continue;
  if (mode === '--write') {
    fs.writeFileSync(file, result.html, 'utf8');
  }
  changed += 1;
}

for (const [slug, brand] of [['danby', 'Danby'], ['hotpoint', 'Hotpoint']]) {
  const result = updateBrandPage(slug, brand);
  if (!result.changed) continue;
  if (mode === '--write') {
    fs.writeFileSync(result.file, result.html, 'utf8');
  }
  changed += 1;
}

if (mode === '--check' && changed) {
  console.error(`${changed} pages still have generic duplicate metadata.`);
  process.exit(1);
}
console.log(mode === '--write' ? `Updated ${changed} pages.` : 'Metadata is unique in the targeted groups.');
