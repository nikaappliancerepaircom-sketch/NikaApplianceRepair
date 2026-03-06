#!/usr/bin/env node
/**
 * fix-schema-gaps.js
 * Fixes 3 schema gaps across all 3 satellite sites:
 * 1. Add openingHours to LocalBusiness JSON-LD if missing
 * 2. Add datePublished / dateModified to main JSON-LD if missing
 * 3. Add twitter:card meta tags if missing
 *
 * Usage:
 *   node fix-schema-gaps.js           # apply fixes
 *   node fix-schema-gaps.js --dry-run # preview only
 */

const fs = require('fs');
const path = require('path');

const DRY_RUN = process.argv.includes('--dry-run');

const SITES = [
  { dir: 'C:/nappliancerepair', domain: 'nappliancerepair.com' },
  { dir: 'C:/appliancerepairneary', domain: 'appliancerepairneary.com' },
  { dir: 'C:/fixlifyservices', domain: 'fixlifyservices.com' },
];

const OPENING_HOURS = '["Mo-Fr 08:00-20:00","Sa 09:00-18:00","Su 10:00-16:00"]';
const DATE_PUBLISHED = '2024-01-15';
const DATE_MODIFIED = '2026-03-06';

const stats = {};

// Fix common JSON syntax issues before parsing
function sanitizeJson(str) {
  // Fix double commas: "value",,  → "value",
  let s = str.replace(/,\s*,/g, ',');
  // Fix trailing comma before } or ]
  s = s.replace(/,\s*([}\]])/g, '$1');
  return s;
}

function getHtmlFiles(dir) {
  const files = [];
  // Root html files
  const rootFiles = fs.readdirSync(dir).filter(f => f.endsWith('.html') && f !== '404.html');
  rootFiles.forEach(f => files.push(path.join(dir, f)));
  // Blog html files
  const blogDir = path.join(dir, 'blog');
  if (fs.existsSync(blogDir)) {
    const blogFiles = fs.readdirSync(blogDir).filter(f => f.endsWith('.html'));
    blogFiles.forEach(f => files.push(path.join(blogDir, f)));
  }
  // Skip _pages_queue
  return files.filter(f => !f.includes('_pages_queue'));
}

function fixOpeningHours(html, filePath) {
  // Skip if already has openingHours (either format)
  if (html.includes('"openingHours"') || html.includes('"openingHoursSpecification"')) {
    return { html, fixed: false };
  }

  // Find LocalBusiness JSON-LD and add openingHours
  // Handle minified, formatted, and compact styles

  // Strategy: find all <script type="application/ld+json">...</script> blocks,
  // parse them, and add openingHours to any LocalBusiness object

  const scriptPattern = /(<script type="application\/ld\+json">)([\s\S]*?)(<\/script>)/g;
  let matched = false;

  let newHtml = html.replace(scriptPattern, (fullMatch, open, jsonStr, close) => {
    if (matched) return fullMatch; // only fix first LocalBusiness
    try {
      const sanitized = sanitizeJson(jsonStr);
      const obj = JSON.parse(sanitized);

      // Direct LocalBusiness
      if (obj['@type'] === 'LocalBusiness') {
        obj.openingHours = ["Mo-Fr 08:00-20:00", "Sa 09:00-18:00", "Su 10:00-16:00"];
        matched = true;
        const isMinified = !jsonStr.includes('\n') || jsonStr.trim().split('\n').length <= 2;
        return open + (isMinified ? JSON.stringify(obj) : '\n' + JSON.stringify(obj, null, 2) + '\n') + close;
      }

      // @graph array containing LocalBusiness
      if (obj['@graph'] && Array.isArray(obj['@graph'])) {
        for (const item of obj['@graph']) {
          if (item['@type'] === 'LocalBusiness' && !item.openingHours) {
            item.openingHours = ["Mo-Fr 08:00-20:00", "Sa 09:00-18:00", "Su 10:00-16:00"];
            matched = true;
          }
        }
        if (matched) {
          const isMinified = !jsonStr.includes('\n') || jsonStr.trim().split('\n').length <= 2;
          return open + (isMinified ? JSON.stringify(obj) : '\n' + JSON.stringify(obj, null, 2) + '\n') + close;
        }
      }
    } catch (e) {
      // Not valid JSON even after sanitization, skip
    }
    return fullMatch;
  });

  if (matched) return { html: newHtml, fixed: true };
  return { html, fixed: false };
}

function fixDatePublished(html, filePath) {
  if (html.includes('"datePublished"')) {
    return { html, fixed: false };
  }

  const scriptPattern = /(<script type="application\/ld\+json">)([\s\S]*?)(<\/script>)/g;
  let matched = false;

  let newHtml = html.replace(scriptPattern, (fullMatch, open, jsonStr, close) => {
    if (matched) return fullMatch;
    try {
      const sanitized = sanitizeJson(jsonStr);
      const obj = JSON.parse(sanitized);

      // Direct LocalBusiness
      if (obj['@type'] === 'LocalBusiness') {
        obj.datePublished = DATE_PUBLISHED;
        obj.dateModified = DATE_MODIFIED;
        matched = true;
        const isMinified = !jsonStr.includes('\n') || jsonStr.trim().split('\n').length <= 2;
        return open + (isMinified ? JSON.stringify(obj) : '\n' + JSON.stringify(obj, null, 2) + '\n') + close;
      }

      // @graph array containing LocalBusiness
      if (obj['@graph'] && Array.isArray(obj['@graph'])) {
        for (const item of obj['@graph']) {
          if (item['@type'] === 'LocalBusiness' && !item.datePublished) {
            item.datePublished = DATE_PUBLISHED;
            item.dateModified = DATE_MODIFIED;
            matched = true;
          }
        }
        if (matched) {
          const isMinified = !jsonStr.includes('\n') || jsonStr.trim().split('\n').length <= 2;
          return open + (isMinified ? JSON.stringify(obj) : '\n' + JSON.stringify(obj, null, 2) + '\n') + close;
        }
      }
    } catch (e) {}
    return fullMatch;
  });

  if (matched) return { html: newHtml, fixed: true };
  return { html, fixed: false };
}

function fixTwitterCard(html, filePath) {
  if (html.includes('twitter:card')) {
    return { html, fixed: false };
  }

  // Extract og:title and og:description values
  const ogTitleMatch = html.match(/og:title"\s+content="([^"]*)"/);
  const ogDescMatch = html.match(/og:description"\s+content="([^"]*)"/);

  const title = ogTitleMatch ? ogTitleMatch[1] : '';
  const desc = ogDescMatch ? ogDescMatch[1] : '';

  if (!title && !desc) {
    // Try to get from <title> tag
    const titleTag = html.match(/<title>([^<]*)<\/title>/);
    const metaDesc = html.match(/name="description"\s+content="([^"]*)"/);
    if (!titleTag && !metaDesc) return { html, fixed: false };
  }

  const twitterTitle = title || (html.match(/<title>([^<]*)<\/title>/) || ['', ''])[1];
  const twitterDesc = desc || (html.match(/name="description"\s+content="([^"]*)"/) || ['', ''])[1];

  const twitterTags = `\n<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:title" content="${twitterTitle}">\n<meta name="twitter:description" content="${twitterDesc}">`;

  // Insert after og:site_name or last og: tag or before </head>
  let newHtml;

  // After og:site_name
  const siteNamePattern = /(<meta property="og:site_name"[^>]*>)/;
  if (siteNamePattern.test(html)) {
    newHtml = html.replace(siteNamePattern, (m) => m + twitterTags);
    return { html: newHtml, fixed: true };
  }

  // After og:image
  const ogImagePattern = /(<meta property="og:image"[^>]*>)/;
  if (ogImagePattern.test(html)) {
    newHtml = html.replace(ogImagePattern, (m) => m + twitterTags);
    return { html: newHtml, fixed: true };
  }

  // After last og: tag
  const ogUrlPattern = /(<meta property="og:url"[^>]*>)/;
  if (ogUrlPattern.test(html)) {
    newHtml = html.replace(ogUrlPattern, (m) => m + twitterTags);
    return { html: newHtml, fixed: true };
  }

  // After og:type
  const ogTypePattern = /(<meta property="og:type"[^>]*>)/;
  if (ogTypePattern.test(html)) {
    newHtml = html.replace(ogTypePattern, (m) => m + twitterTags);
    return { html: newHtml, fixed: true };
  }

  // Before </head>
  newHtml = html.replace('</head>', twitterTags + '\n</head>');
  if (newHtml !== html) return { html: newHtml, fixed: true };

  return { html, fixed: false };
}

function processSite(site) {
  const siteStats = { openingHours: 0, datePublished: 0, twitterCard: 0, jsonFixed: 0, total: 0, errors: 0 };
  const files = getHtmlFiles(site.dir);
  siteStats.total = files.length;

  for (const filePath of files) {
    try {
      let html = fs.readFileSync(filePath, 'utf8');
      let changed = false;

      // Fix 0: Fix JSON syntax errors (double commas) in ld+json blocks
      if (html.includes(',,')) {
        const fixed = html.replace(/(<script type="application\/ld\+json">)([\s\S]*?)(<\/script>)/g, (full, open, json, close) => {
          const sanitized = sanitizeJson(json);
          if (sanitized !== json) return open + sanitized + close;
          return full;
        });
        if (fixed !== html) {
          html = fixed;
          changed = true;
          siteStats.jsonFixed++;
        }
      }

      // Fix 1: openingHours
      const oh = fixOpeningHours(html, filePath);
      if (oh.fixed) {
        html = oh.html;
        changed = true;
        siteStats.openingHours++;
      }

      // Fix 2: datePublished
      const dp = fixDatePublished(html, filePath);
      if (dp.fixed) {
        html = dp.html;
        changed = true;
        siteStats.datePublished++;
      }

      // Fix 3: twitter:card
      const tc = fixTwitterCard(html, filePath);
      if (tc.fixed) {
        html = tc.html;
        changed = true;
        siteStats.twitterCard++;
      }

      if (changed && !DRY_RUN) {
        fs.writeFileSync(filePath, html, 'utf8');
      }
    } catch (e) {
      console.error(`  ERROR: ${filePath}: ${e.message}`);
      siteStats.errors++;
    }
  }

  return siteStats;
}

// Main
console.log(DRY_RUN ? '=== DRY RUN ===' : '=== APPLYING FIXES ===');
console.log('');

for (const site of SITES) {
  console.log(`--- ${site.domain} (${site.dir}) ---`);
  const s = processSite(site);
  stats[site.domain] = s;
  console.log(`  Total pages: ${s.total}`);
  console.log(`  + openingHours: ${s.openingHours}`);
  console.log(`  + datePublished: ${s.datePublished}`);
  console.log(`  + twitter:card:  ${s.twitterCard}`);
  if (s.jsonFixed) console.log(`  ~ JSON syntax fixed: ${s.jsonFixed}`);
  if (s.errors) console.log(`  ERRORS: ${s.errors}`);
  console.log('');
}

const totalOH = Object.values(stats).reduce((a, b) => a + b.openingHours, 0);
const totalDP = Object.values(stats).reduce((a, b) => a + b.datePublished, 0);
const totalTC = Object.values(stats).reduce((a, b) => a + b.twitterCard, 0);
console.log('=== TOTALS ===');
console.log(`openingHours added: ${totalOH}`);
console.log(`datePublished added: ${totalDP}`);
console.log(`twitter:card added:  ${totalTC}`);
console.log(`TOTAL fixes: ${totalOH + totalDP + totalTC}`);
