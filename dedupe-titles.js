/**
 * dedupe-titles.js
 * Generates unique <title> and <meta description> for pages with duplicate values.
 * Uses deterministic hash-based template selection — no external API needed.
 *
 * Usage:
 *   node dedupe-titles.js --site=C:/nappliancerepair [--dry-run]
 *   node dedupe-titles.js --all [--dry-run]
 */
'use strict';
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const DRY_RUN = args.includes('--dry-run');
const ALL = args.includes('--all');
const siteArg = args.find(a => a.startsWith('--site='));

const SITES = [
  { dir: 'C:/nappliancerepair',    domain: 'nappliancerepair.com',    brand: "Nick's Appliance Repair", phone: '(437) 747-6737', region: 'York Region' },
  { dir: 'C:/appliancerepairneary',domain: 'appliancerepairneary.com', brand: 'Appliance Repair Near Me', phone: '(437) 524-1053', region: 'West GTA' },
  { dir: 'C:/fixlifyservices',     domain: 'fixlifyservices.com',      brand: 'Fixlify Appliance Services', phone: '(437) 524-1053', region: 'East GTA' },
];

const TITLE_TEMPLATES = [
  (s, c, b) => `${s} in ${c} | Same-Day Service`,
  (s, c, b) => `${c} ${s} — 24/7 Certified Repair`,
  (s, c, b) => `Expert ${s} in ${c} | ${b}`,
  (s, c, b) => `${s} Specialists in ${c} | ${b}`,
  (s, c, b) => `Same-Day ${s} in ${c} | Book Online`,
  (s, c, b) => `Affordable ${s} in ${c} | Certified`,
  (s, c, b) => `${c} ${s} | ${b}`,
  (s, c, b) => `Fast ${s} in ${c} — Same Day`,
];

const DESC_TEMPLATES = [
  (s, c, p, r) => `Need ${s.toLowerCase()} in ${c}? Call ${p} for same-day service across ${r}. Licensed technicians, 90-day warranty on parts & labour.`,
  (s, c, p, r) => `${c} ${s.toLowerCase()} from certified technicians. Available 24/7 in ${r}. Call ${p} — most repairs done same day.`,
  (s, c, p, r) => `Trusted ${s.toLowerCase()} in ${c} and ${r}. Upfront pricing, 90-day guarantee. Call ${p} or book online today.`,
  (s, c, p, r) => `Get your ${s.toLowerCase()} fixed today in ${c}. ${r} coverage, same-day dispatch. Call ${p} for a free quote.`,
  (s, c, p, r) => `${s} in ${c} by factory-certified techs. ${r} service area. Call ${p} — we arrive within 2–4 hours.`,
  (s, c, p, r) => `Looking for ${s.toLowerCase()} near ${c}? We serve all of ${r}. Call ${p} for same-day appointments.`,
];

function simpleHash(str) {
  let h = 0;
  for (let i = 0; i < str.length; i++) {
    h = ((h << 5) - h + str.charCodeAt(i)) | 0;
  }
  return Math.abs(h);
}

function extractSlugParts(filename) {
  const slug = filename.replace(/\.html$/, '');
  const parts = slug.split('-');

  // Known services (longer/specific first to avoid partial matches)
  const services = ['dishwasher', 'refrigerator', 'washer', 'dryer', 'fridge', 'oven', 'stove', 'freezer', 'range', 'microwave'];

  let service = '';
  let city = '';
  let serviceEndIdx = -1;

  // Find service and its end index in parts array
  for (const svc of services) {
    const svcParts = svc.split('-');
    for (let i = 0; i <= parts.length - svcParts.length; i++) {
      if (svcParts.every((p, j) => parts[i + j] === p)) {
        service = svc.charAt(0).toUpperCase() + svc.slice(1) + ' Repair';
        // Find "repair" after service
        const repairIdx = parts.indexOf('repair', i + svcParts.length);
        serviceEndIdx = repairIdx >= 0 ? repairIdx + 1 : i + svcParts.length;
        break;
      }
    }
    if (service) break;
  }

  if (!service) {
    const repairIdx = parts.indexOf('repair');
    if (repairIdx > 0) {
      service = parts.slice(0, repairIdx).map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ') + ' Repair';
      serviceEndIdx = repairIdx + 1;
    } else {
      service = parts.map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
      serviceEndIdx = parts.length;
    }
  }

  // Extract city from remainder of slug after service+repair
  if (serviceEndIdx > 0 && serviceEndIdx < parts.length) {
    const cityParts = parts.slice(serviceEndIdx);
    if (cityParts.length > 0 && cityParts[0] !== 'near' && cityParts[0] !== 'gta') {
      city = cityParts.map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
    }
  }

  // Fallbacks
  if (!city || city === 'Me') city = 'GTA';

  return { service, city };
}

function clamp(str, min, max) {
  if (str.length >= min && str.length <= max) return str;
  if (str.length > max) return str.slice(0, max - 1) + '…';
  return str;
}

function processFile(filePath, site, dryRun, groupOffset = 0) {
  let html = fs.readFileSync(filePath, 'utf8');
  const filename = path.basename(filePath);

  const { service, city } = extractSlugParts(filename);
  const key = (service + city).toLowerCase();
  const hash = simpleHash(key) + groupOffset;

  const titleFn = TITLE_TEMPLATES[hash % TITLE_TEMPLATES.length];
  const descFn = DESC_TEMPLATES[hash % DESC_TEMPLATES.length];

  const newTitle = clamp(titleFn(service, city, site.brand), 40, 60);
  const newDesc = clamp(descFn(service, city, site.phone, site.region), 140, 160);

  let changed = false;

  // Replace <title>
  const titleMatch = html.match(/<title>(.*?)<\/title>/s);
  if (titleMatch) {
    const oldTitle = titleMatch[1];
    if (oldTitle !== newTitle) {
      html = html.replace(/<title>.*?<\/title>/s, `<title>${newTitle}</title>`);
      changed = true;
    }
  }

  // Replace <meta name="description">
  const descMatch = html.match(/<meta\s+name="description"\s+content="([^"]*)"[^>]*>/i);
  if (descMatch) {
    const oldDesc = descMatch[1];
    if (oldDesc !== newDesc) {
      html = html.replace(
        /<meta\s+name="description"\s+content="[^"]*"[^>]*>/i,
        `<meta name="description" content="${newDesc}">`
      );
      changed = true;
    }
  }

  if (changed && !dryRun) {
    fs.writeFileSync(filePath, html, 'utf8');
  }

  return { changed, filename, newTitle, newDesc };
}

function processSite(site) {
  console.log(`\n=== ${site.domain} ===`);
  const htmlFiles = fs.readdirSync(site.dir)
    .filter(f => f.endsWith('.html') && f !== 'service-template.html' && f !== '404.html' && f !== 'index.html' && !f.includes('.bak'));

  // Build title → files map to find duplicates
  const titleMap = {};
  for (const f of htmlFiles) {
    const filePath = path.join(site.dir, f);
    const html = fs.readFileSync(filePath, 'utf8');
    const m = html.match(/<title>(.*?)<\/title>/s);
    if (m) {
      const t = m[1].trim();
      if (!titleMap[t]) titleMap[t] = [];
      titleMap[t].push(f);
    }
  }

  // Find duplicates
  const dupeGroups = Object.entries(titleMap).filter(([, files]) => files.length > 1);
  console.log(`Duplicate title groups found: ${dupeGroups.length}`);

  if (dupeGroups.length === 0) {
    console.log('  ✓ No duplicates — skipping');
    return { fixed: 0, dupeGroups: 0 };
  }

  // For each duplicate group, fix all files EXCEPT the first (canonical file)
  const tracker = [];
  let fixedCount = 0;

  for (const [origTitle, files] of dupeGroups) {
    // Keep first file with original title; fix all others
    for (let i = 1; i < files.length; i++) {
      const filePath = path.join(site.dir, files[i]);
      const result = processFile(filePath, site, DRY_RUN, i);
      tracker.push({
        file: files[i],
        site: site.domain,
        oldTitle: origTitle,
        newTitle: result.newTitle,
        newDesc: result.newDesc,
        changed: result.changed,
      });
      if (result.changed) fixedCount++;
      console.log(`  ${result.changed ? '✓' : '-'} ${files[i]}: "${result.newTitle}"`);
    }
  }

  // Save tracker
  if (!DRY_RUN) {
    const trackerPath = path.join(site.dir, 'dupe-fix-tracker.json');
    let existing = [];
    if (fs.existsSync(trackerPath)) {
      try { existing = JSON.parse(fs.readFileSync(trackerPath, 'utf8')); } catch (e) {}
    }
    fs.writeFileSync(trackerPath, JSON.stringify([...existing, ...tracker], null, 2));
    console.log(`  Tracker saved: ${trackerPath}`);
  }

  console.log(`  Fixed: ${fixedCount}/${tracker.length} files`);
  return { fixed: fixedCount, dupeGroups: dupeGroups.length };
}

// Main
const targetSites = ALL ? SITES : (siteArg ? SITES.filter(s => siteArg.includes(s.domain) || siteArg.includes(path.basename(s.dir))) : SITES);

if (targetSites.length === 0) {
  console.error('No matching sites. Use --site=<path> or --all');
  process.exit(1);
}

console.log(`Mode: ${DRY_RUN ? 'DRY RUN' : 'WRITE'}`);
let totalFixed = 0;
for (const site of targetSites) {
  const { fixed } = processSite(site);
  totalFixed += fixed;
}
console.log(`\nTotal files fixed: ${totalFixed}`);
