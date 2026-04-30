#!/usr/bin/env node
/**
 * inject-washer-neary.js
 * Rewrites key content sections in washer-repair-[city].html files
 * on appliancerepairneary.com to achieve 80-90% uniqueness.
 *
 * Sections replaced per city:
 *  1. Answer box paragraph (inside .answer-box)
 *  2. Answer capsule paragraph (inside .answer-capsule)
 *  3. Content section H2 (first h2 in .content-body)
 *  4. CITY-CONTENT-v2 block (3 paragraphs between markers)
 *  5. UNIQUE-CITY-CONTENT inline content
 *  6. FAQ items in .faq-list section
 */

const fs = require('fs');
const path = require('path');

const SITE_DIR = 'C:/appliancerepairneary';
const CONTENT_DIR = 'C:/NikaApplianceRepair';

// Load all 4 batches and merge
function loadAllContent() {
  const merged = {};
  for (let i = 1; i <= 4; i++) {
    const fp = path.join(CONTENT_DIR, `washer-content-batch${i}.json`);
    if (!fs.existsSync(fp)) {
      console.error(`Missing batch file: ${fp}`);
      process.exit(1);
    }
    const data = JSON.parse(fs.readFileSync(fp, 'utf8'));
    Object.assign(merged, data.cities);
  }
  return merged;
}

// Escape string for use in a regex
function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// Build 4 FAQ item HTML blocks
function buildFaqItems(faqs) {
  return faqs.map(faq => `
<div class="faq-item">
  <button class="faq-question" aria-expanded="false">
    <span class="faq-question-text">${faq.q}</span>
    <span class="faq-icon">+</span>
  </button>
  <div class="faq-answer">
    <div class="faq-answer-inner"><p>${faq.a}</p></div>
  </div>
</div>`).join('\n');
}

function processFile(citySlug, content, filePath) {
  let html = fs.readFileSync(filePath, 'utf8');
  const original = html;

  // --- 1. Replace answer-box paragraph ---
  // Pattern: <div class="answer-box" ...><p>...text...</p></div>
  html = html.replace(
    /(<div class="answer-box"[^>]*>\s*<p[^>]*>)([^<]*?)(<\/p>\s*<\/div>)/s,
    `$1${content.answer_box}$3`
  );

  // --- 2. Replace answer-capsule paragraph text ---
  // Pattern: <p style="..." itemprop="description">...text...</p>  inside .answer-capsule
  html = html.replace(
    /(<div class="answer-capsule"[^>]*>[\s\S]*?<p[^>]*itemprop="description"[^>]*>)([^<]+?)(<\/p>)/,
    `$1${content.answer_capsule}$3`
  );

  // --- 3. Replace content section H2 (first h2 in .content-body) ---
  // The H2 immediately follows <div class="content-body reveal">
  html = html.replace(
    /(<div class="content-body reveal">\s*<h2>)([^<]+?)(<\/h2>)/,
    `$1${content.content_h2}$3`
  );

  // --- 4. Replace CITY-CONTENT-v2 block ---
  // Replaces everything between <!-- CITY-CONTENT-v2 --> and <!-- END-CITY-CONTENT-v2 -->
  const newCityBlock = `<!-- CITY-CONTENT-v2 -->
    <p style="margin:0 0 14px;color:#374151;line-height:1.7;font-size:0.9375rem;">${content.intro_p1}</p>
    <p style="margin:0 0 14px;color:#374151;line-height:1.7;font-size:0.9375rem;">${content.intro_p2}</p>
    <!-- END-CITY-CONTENT-v2 -->`;

  html = html.replace(
    /<!-- CITY-CONTENT-v2 -->[\s\S]*?<!-- END-CITY-CONTENT-v2 -->/,
    newCityBlock
  );

  // --- 5. Replace UNIQUE-CITY-CONTENT inline content ---
  html = html.replace(
    /<!-- UNIQUE-CITY-CONTENT -->[\s\S]*?<!-- END-UNIQUE-CITY-CONTENT -->/,
    `<!-- UNIQUE-CITY-CONTENT -->${content.city_context}<!-- END-UNIQUE-CITY-CONTENT -->`
  );

  // --- 6. Replace FAQ items in .faq-list ---
  // Find the faq-list div and replace all faq-item blocks inside it
  const newFaqItems = buildFaqItems(content.faq);

  // Match the faq-list opening, content (all faq-item divs), and closing
  html = html.replace(
    /(<div class="faq-list">)([\s\S]*?)(<\/div>\s*<\/div>\s*<\/div>\s*<\/section>)/,
    (match, open, inner, close) => {
      return `${open}\n${newFaqItems}\n\n    ${close}`;
    }
  );

  if (html === original) {
    return { changed: false, reason: 'No changes detected — patterns may not have matched' };
  }

  fs.writeFileSync(filePath, html, 'utf8');
  return { changed: true };
}

// Main
const allContent = loadAllContent();
console.log(`Loaded content for ${Object.keys(allContent).length} cities`);

// Get list of files to process
const files = fs.readdirSync(SITE_DIR)
  .filter(f => f.startsWith('washer-repair-') && f.endsWith('.html'))
  .filter(f => !f.includes('near-me'));

console.log(`Found ${files.length} city files to process\n`);

let successes = 0;
let failures = 0;
let skipped = 0;

for (const file of files.sort()) {
  const citySlug = file.replace('washer-repair-', '').replace('.html', '');
  const filePath = path.join(SITE_DIR, file);

  if (!allContent[citySlug]) {
    console.log(`SKIP  ${file} — no content data for slug "${citySlug}"`);
    skipped++;
    continue;
  }

  try {
    const result = processFile(citySlug, allContent[citySlug], filePath);
    if (result.changed) {
      console.log(`OK    ${file}`);
      successes++;
    } else {
      console.log(`WARN  ${file} — ${result.reason}`);
      failures++;
    }
  } catch (err) {
    console.error(`ERR   ${file} — ${err.message}`);
    failures++;
  }
}

console.log(`\n===== SUMMARY =====`);
console.log(`Processed: ${successes + failures + skipped}`);
console.log(`Success:   ${successes}`);
console.log(`Warnings:  ${failures}`);
console.log(`Skipped:   ${skipped}`);
