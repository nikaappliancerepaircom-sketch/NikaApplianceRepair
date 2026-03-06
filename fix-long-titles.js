#!/usr/bin/env node
/**
 * fix-long-titles.js
 * Trims <title> tags to <=60 chars across all 3 satellite sites.
 *
 * Also updates og:title and twitter:title to match.
 *
 * Usage:
 *   node fix-long-titles.js           # apply fixes
 *   node fix-long-titles.js --dry-run # preview only
 */

const fs = require('fs');
const path = require('path');

const DRY_RUN = process.argv.includes('--dry-run');
const MAX_LEN = 60;

const SITES = [
  { dir: 'C:/nappliancerepair', domain: 'nappliancerepair.com' },
  { dir: 'C:/appliancerepairneary', domain: 'appliancerepairneary.com' },
  { dir: 'C:/fixlifyservices', domain: 'fixlifyservices.com' },
];

const PHONE = '(437) 524-1053';

function getHtmlFiles(dir) {
  const files = [];
  const rootFiles = fs.readdirSync(dir).filter(f => f.endsWith('.html') && f !== '404.html');
  rootFiles.forEach(f => files.push(path.join(dir, f)));
  const blogDir = path.join(dir, 'blog');
  if (fs.existsSync(blogDir)) {
    const blogFiles = fs.readdirSync(blogDir).filter(f => f.endsWith('.html'));
    blogFiles.forEach(f => files.push(path.join(blogDir, f)));
  }
  return files.filter(f => !f.includes('_pages_queue'));
}

/**
 * Intelligently shorten a title to <=60 chars.
 * Preserves the core keyword + city. Tries multiple strategies.
 */
function shortenTitle(title) {
  if (title.length <= MAX_LEN) return title;

  const original = title;
  let t = title;

  // Strategy 1: Remove brand suffix " | N Appliance Repair Blog"
  t = t.replace(/\s*\|\s*N Appliance Repair Blog$/, '');
  if (t.length <= MAX_LEN) return t;

  // Strategy 1b: Remove brand suffix " | N Appliance Repair"
  t = t.replace(/\s*\|\s*N Appliance Repair$/, '');
  if (t.length <= MAX_LEN) return t;

  // Strategy 1c: Remove brand suffix " | N Appliance"
  t = t.replace(/\s*\|\s*N Appliance$/, '');
  if (t.length <= MAX_LEN) return t;

  // Strategy 1d: Remove brand suffix " | Appliance Repair Near Me"
  t = t.replace(/\s*\|\s*Appliance Repair Near Me$/, '');
  if (t.length <= MAX_LEN) return t;

  // Strategy 1e: Remove brand suffix " | Fixlify"
  t = t.replace(/\s*\|\s*Fixlify[^|]*$/, '');
  if (t.length <= MAX_LEN) return t;

  // Strategy 1f: Remove " Toronto" at end of remaining for blog titles if still too long
  // (will be re-added by meta desc context)

  // For pipe-delimited titles: "Service City | Middle | Phone"
  const parts = t.split(/\s*\|\s*/);

  if (parts.length >= 3) {
    const first = parts[0];
    const last = parts[parts.length - 1];

    // Strategy 2: Shorten middle phrases first, keep all segments
    const shortenedParts = [parts[0]];
    for (let i = 1; i < parts.length - 1; i++) {
      let mid = parts[i]
        .replace('Same-Day Service', 'Same-Day')
        .replace('Same-Day Fix', 'Same-Day')
        .replace('Licensed & Insured', '')
        .replace('1-Hour Response', '1-Hour')
        .replace('Upfront Quotes', '')
        .replace('Pricing Guide', 'Pricing')
        .replace('$65 Diagnostic', '$65 Diag')
        .replace('From $65', '$65')
        .trim();
      if (mid) shortenedParts.push(mid);
    }
    shortenedParts.push(last);
    const withShortenedMiddle = shortenedParts.join(' | ');
    if (withShortenedMiddle.length <= MAX_LEN) return withShortenedMiddle;

    // Strategy 3: Drop middle part(s), keep first + last
    const tryDropMiddle = first + ' | ' + last;
    if (tryDropMiddle.length <= MAX_LEN) return tryDropMiddle;

    // Strategy 4: Drop phone (last part) and keep shortened middle
    if (last.includes('437') && shortenedParts.length >= 3) {
      const noPhone = shortenedParts.slice(0, -1).join(' | ');
      if (noPhone.length <= MAX_LEN && noPhone.length >= 35) return noPhone;
    }

    // Strategy 5: Shorten first part (preserve "Near Me" keyword)
    let s1 = first.replace('Installation', 'Install');
    let tryS1 = s1 + ' | ' + last;
    if (tryS1.length <= MAX_LEN) return tryS1;

    // Strategy 5b: Also drop "Near Me" if still too long
    s1 = s1.replace('Near Me ', '');
    tryS1 = s1 + ' | ' + last;
    if (tryS1.length <= MAX_LEN) return tryS1;

    // Strategy 6: Drop phone, keep first only
    if (last.includes('437') && first.length <= MAX_LEN && first.length >= 30) {
      return first;
    }
  }

  if (parts.length === 2) {
    const first = parts[0];
    const second = parts[1];

    // Strategy: Shorten second part
    let s2 = second
      .replace('Same-Day Service', 'Same-Day')
      .replace('Same-Day Fix', 'Same-Day')
      .replace('$65 Diagnostic', '$65 Diag')
      .replace('From $65', '$65')
      .trim();
    const try2 = first + ' | ' + s2;
    if (try2.length <= MAX_LEN) return try2;

    // If second is phone number, first part is too long - try shortening first
    if (second.includes('437')) {
      let s1 = first.replace('Installation', 'Install');
      let try1 = s1 + ' | ' + second;
      if (try1.length <= MAX_LEN) return try1;
      // Drop "Near Me" only if still too long
      s1 = s1.replace('Near Me ', '');
      try1 = s1 + ' | ' + second;
      if (try1.length <= MAX_LEN) return try1;
    }

    // Drop phone if it's the second part
    if (second.includes('437') && first.length <= MAX_LEN && first.length >= 30) {
      return first;
    }
  }

  // Blog-style titles (no pipes): try truncating smartly
  if (!t.includes('|')) {
    // Remove trailing year like "(2025)" or "(2026)"
    t = t.replace(/\s*\(20\d\d\)\s*$/, '');
    if (t.length <= MAX_LEN) return t;

    // Shorten common phrases
    t = t
      .replace('How Much Does ', '')
      .replace(' in Toronto in 2026', ' Toronto 2026')
      .replace(' in Toronto', ' Toronto')
      .replace(': What They Mean and How to Fix Them', ': Meanings & Fixes')
      .replace(': Top Problems Our Techs Fix', ': Common Problems & Fixes')
      .replace(': Causes and Quick Fixes', ': Causes & Fixes')
      .replace(': Complete Guide for Homeowners', ' Guide')
      .replace(': Causes and Fixes', ': Fixes')
      .replace(': Expert Service for Premium Brands', ': Expert Service')
      .replace(': What to Expect', ' Guide')
      .replace(': Top Issues and How to Fix Them', ': Common Fixes')
      .replace(': Common Faults and Fixes', ': Fixes')
      .replace(' All Fixes', ' Fixes');
    if (t.length <= MAX_LEN) return t;

    // Further shortening
    t = t
      .replace('How Toronto Appliance Repair Companies Are Using AI to Never Miss a Service Call', 'AI in Toronto Appliance Repair: Never Miss a Call')
      .replace('How Local Appliance Repair Businesses Near You Use Fixlify', 'How Local Repair Shops Use Fixlify')
      .replace('The Software Behind Our Appliance Repair Operations in Toronto', 'Software Behind Our Appliance Repair in Toronto');
    if (t.length <= MAX_LEN) return t;

    // Last resort: truncate at word boundary, remove dangling connectors
    if (t.length > MAX_LEN) {
      const words = t.split(' ');
      let result = '';
      for (const w of words) {
        const next = result ? result + ' ' + w : w;
        if (next.length > MAX_LEN) break;
        result = next;
      }
      // Remove trailing connectors/punctuation
      result = result.replace(/\s*[&|,—–\-:]\s*$/, '').trim();
      if (result.length >= 35) return result;
    }
  }

  // Fallback: try hard truncation of full pipe-joined title
  if (t.length > MAX_LEN) {
    // Remove everything after last | if that helps
    const lastPipe = t.lastIndexOf(' | ');
    if (lastPipe > 30) {
      const trimmed = t.substring(0, lastPipe);
      if (trimmed.length <= MAX_LEN) return trimmed;
    }
  }

  // If still >60, try removing "Near Me" phrase
  t = t.replace(/ Near Me/g, '').replace(/ Near You/g, '');
  if (t.length <= MAX_LEN) return t;

  // Absolute last resort: word-boundary truncation
  if (t.length > MAX_LEN) {
    const words = t.split(' ');
    let result = '';
    for (const w of words) {
      const next = result ? result + ' ' + w : w;
      if (next.length > MAX_LEN) break;
      result = next;
    }
    // Remove trailing connectors/punctuation
    result = result.replace(/\s*[&|,—–\-:]\s*$/, '').trim();
    return result;
  }

  return t;
}

function processSite(site) {
  const siteStats = { fixed: 0, stillLong: 0, total: 0 };
  const files = getHtmlFiles(site.dir);
  siteStats.total = files.length;

  for (const filePath of files) {
    try {
      let html = fs.readFileSync(filePath, 'utf8');
      const titleMatch = html.match(/<title>([^<]*)<\/title>/);
      if (!titleMatch) continue;

      const oldTitle = titleMatch[1];
      if (oldTitle.length <= MAX_LEN) continue;

      const newTitle = shortenTitle(oldTitle);

      if (newTitle.length > MAX_LEN) {
        siteStats.stillLong++;
        console.log(`  STILL LONG: ${path.basename(filePath)}: (${newTitle.length}) ${newTitle}`);
        continue;
      }

      if (newTitle === oldTitle) continue;

      console.log(`  ${oldTitle.length} → ${newTitle.length} | ${oldTitle}`);
      console.log(`  ${''.padEnd(oldTitle.length.toString().length)}   ${''.padEnd(newTitle.length.toString().length)}   ${newTitle}`);

      // Replace <title>
      let newHtml = html.replace(`<title>${oldTitle}</title>`, `<title>${newTitle}</title>`);

      // Replace og:title if it matches old title
      const ogTitleRe = new RegExp(`(og:title"\\s+content=")${escapeRegExp(oldTitle)}(")`);
      newHtml = newHtml.replace(ogTitleRe, `$1${newTitle}$2`);

      // Replace twitter:title if it matches old title
      const twTitleRe = new RegExp(`(twitter:title"\\s+content=")${escapeRegExp(oldTitle)}(")`);
      newHtml = newHtml.replace(twTitleRe, `$1${newTitle}$2`);

      if (!DRY_RUN) {
        fs.writeFileSync(filePath, newHtml, 'utf8');
      }
      siteStats.fixed++;
    } catch (e) {
      console.error(`  ERROR: ${filePath}: ${e.message}`);
    }
  }

  return siteStats;
}

function escapeRegExp(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// Main
console.log(DRY_RUN ? '=== DRY RUN ===' : '=== APPLYING FIXES ===');
console.log('');

const allStats = {};
for (const site of SITES) {
  console.log(`--- ${site.domain} ---`);
  const s = processSite(site);
  allStats[site.domain] = s;
  console.log(`  Fixed: ${s.fixed} | Still long: ${s.stillLong}`);
  console.log('');
}

const totalFixed = Object.values(allStats).reduce((a, b) => a + b.fixed, 0);
const totalStill = Object.values(allStats).reduce((a, b) => a + b.stillLong, 0);
console.log('=== TOTALS ===');
console.log(`Titles trimmed: ${totalFixed}`);
console.log(`Still >60 chars: ${totalStill}`);
