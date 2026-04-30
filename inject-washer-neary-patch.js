#!/usr/bin/env node
/**
 * inject-washer-neary-patch.js
 * Patches the sections that the main script couldn't handle
 * for v2-outfit and v3-instrument template variants.
 *
 * v2-outfit (20 files): hero-capsule text + FAQ (uses faq-q/faq-a structure)
 * v3-instrument (2 files): answer-box div + content-intro h2 + FAQ (uses details/summary)
 * Also fixes corrupted answer-capsule in v3 files (Calgary had broken HTML from previous run).
 */

const fs = require('fs');
const path = require('path');

const SITE_DIR = 'C:/appliancerepairneary';
const CONTENT_DIR = 'C:/NikaApplianceRepair';

function loadAllContent() {
  const merged = {};
  for (let i = 1; i <= 4; i++) {
    const fp = path.join(CONTENT_DIR, `washer-content-batch${i}.json`);
    const data = JSON.parse(fs.readFileSync(fp, 'utf8'));
    Object.assign(merged, data.cities);
  }
  return merged;
}

// Build v2-style FAQ items (button/div pattern, onclick)
function buildV2FaqItems(faqs) {
  return faqs.map(faq => `    <div class="faq-item">
      <button class="faq-q" onclick="var n=this.nextElementSibling;n.style.display=n.style.display==='block'?'none':'block'">
        ${faq.q} <span>+</span>
      </button>
      <div class="faq-a" style="display:none">${faq.a}</div>
    </div>`).join('\n');
}

// Build v3-style FAQ items (details/summary pattern)
function buildV3FaqItems(city, faqs) {
  const cityTitle = city.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
  return `<section class="faq-section" aria-labelledby="faq-heading">
  <div class="container">
    <h2 id="faq-heading">Frequently Asked Questions — Washer Repair in ${cityTitle}</h2>
    <div style="margin-top:24px">
${faqs.map(faq => `      <details class="faq-item">
        <summary class="faq-question">
          ${faq.q}
          <span class="faq-icon">+</span>
        </summary>
        <div class="faq-answer">${faq.a}</div>
      </details>`).join('\n')}
    </div>
  </div>
</section>`;
}

const V2_CITIES = [
  'bloor-west-village', 'chinatown', 'corso-italia', 'dufferin-grove', 'east-york',
  'etobicoke-village', 'greektown', 'high-park', 'king-west', 'little-italy',
  'little-portugal', 'midtown', 'ossington', 'roncesvalles', 'st-lawrence',
  'swansea', 'the-beaches', 'thorncliffe-park', 'trinity-bellwoods', 'wychwood'
];

const V3_CITIES = ['calgary', 'edmonton'];

function patchV2File(citySlug, content, filePath) {
  let html = fs.readFileSync(filePath, 'utf8');
  const original = html;
  let changed = false;

  // 1. Replace hero-capsule content (keeping the <strong>Need washer repair...</strong> part replaced)
  // Pattern: <div class="hero-capsule">\n    <strong>...</strong> ...text... \n  </div>
  // Replace the entire inner content
  const cityTitle = citySlug.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
  const newHeroCapsule = `<strong>Need washer repair in ${cityTitle}?</strong> ${content.answer_capsule}`;

  html = html.replace(
    /(<div class="hero-capsule">)\s*[\s\S]*?(<\/div>)/,
    (match, open, close) => {
      changed = true;
      return `${open}\n    ${newHeroCapsule}\n  ${close}`;
    }
  );

  // 2. Replace all FAQ items (the block starting with h2 "Frequently Asked Questions")
  // Pattern: <h2>Frequently Asked Questions...  <div style="margin-top:20px">  ...faq items...  </div>\n</div></section>
  const newFaqItems = buildV2FaqItems(content.faq);

  html = html.replace(
    /(<h2>Frequently Asked Questions[^<]*<\/h2>)\s*(<div style="margin-top:20px">)([\s\S]*?)(<\/div>\s*\n<\/div><\/section>)/,
    (match, h2, divOpen, inner, close) => {
      changed = true;
      return `${h2}\n  ${divOpen}\n${newFaqItems}\n  ${close}`;
    }
  );

  if (!changed) {
    // Try fallback: just replace FAQ items container
    html = html.replace(
      /(Frequently Asked Questions[^<]*<\/h2>[\s\S]*?<div style="margin-top:20px">)([\s\S]*?)(<\/div>\s*\n<\/div><\/section>)/,
      (match, before, inner, after) => {
        changed = true;
        return `${before}\n${newFaqItems}\n  ${after}`;
      }
    );
  }

  if (html !== original) {
    fs.writeFileSync(filePath, html, 'utf8');
    return { changed: true };
  }
  return { changed: false, reason: 'No v2 patterns matched' };
}

function patchV3File(citySlug, content, filePath) {
  let html = fs.readFileSync(filePath, 'utf8');
  const original = html;

  // 1. Fix answer-capsule (Calgary had corrupted HTML from previous run)
  // The answer-capsule p was corrupted with embedded HTML. Clean it up.
  html = html.replace(
    /(<div class="answer-capsule"[^>]*>[\s\S]*?<p[^>]*itemprop="description"[^>]*>)([\s\S]*?)(<\/p>\s*<\/div>)/,
    (match, open, inner, close) => {
      // Replace with clean content
      return `${open}${content.answer_capsule}${close}`;
    }
  );

  // 2. Replace the answer-box div content (v3 has <div class="answer-box">text</div> without inner <p>)
  html = html.replace(
    /(<div class="answer-box">)([\s\S]*?)(<\/div>)/,
    (match, open, inner, close) => {
      return `${open}${content.answer_box}${close}`;
    }
  );

  // 3. Replace content-intro h2
  html = html.replace(
    /(<div class="content-intro[^"]*">\s*<h2>)([\s\S]*?)(<\/h2>)/,
    (match, open, inner, close) => {
      return `${open}${content.content_h2}${close}`;
    }
  );

  // 4. Add FAQ section before </main> if no FAQ exists, or replace existing one
  const hasFaqSection = html.includes('faq-section') || html.includes('Frequently Asked Questions');
  const newFaqSection = buildV3FaqItems(citySlug, content.faq);

  if (hasFaqSection) {
    // Try to replace existing FAQ section
    html = html.replace(
      /<section class="faq-section"[\s\S]*?<\/section>/,
      newFaqSection
    );
  } else {
    // Insert before </main>
    html = html.replace('</main>', `\n${newFaqSection}\n</main>`);
  }

  if (html !== original) {
    fs.writeFileSync(filePath, html, 'utf8');
    return { changed: true };
  }
  return { changed: false, reason: 'No v3 patterns matched' };
}

// Main
const allContent = loadAllContent();
console.log(`Loaded content for ${Object.keys(allContent).length} cities`);

let successes = 0;
let failures = 0;

console.log('\n--- Patching v2-outfit template files (20 cities) ---');
for (const citySlug of V2_CITIES) {
  const filePath = path.join(SITE_DIR, `washer-repair-${citySlug}.html`);
  if (!fs.existsSync(filePath)) {
    console.log(`SKIP  ${citySlug} — file not found`);
    continue;
  }
  if (!allContent[citySlug]) {
    console.log(`SKIP  ${citySlug} — no content data`);
    continue;
  }
  try {
    const result = patchV2File(citySlug, allContent[citySlug], filePath);
    if (result.changed) {
      console.log(`OK    ${citySlug}`);
      successes++;
    } else {
      console.log(`WARN  ${citySlug} — ${result.reason}`);
      failures++;
    }
  } catch (err) {
    console.error(`ERR   ${citySlug} — ${err.message}`);
    failures++;
  }
}

console.log('\n--- Patching v3-instrument template files (2 cities) ---');
for (const citySlug of V3_CITIES) {
  const filePath = path.join(SITE_DIR, `washer-repair-${citySlug}.html`);
  if (!fs.existsSync(filePath)) {
    console.log(`SKIP  ${citySlug} — file not found`);
    continue;
  }
  if (!allContent[citySlug]) {
    console.log(`SKIP  ${citySlug} — no content data`);
    continue;
  }
  try {
    const result = patchV3File(citySlug, allContent[citySlug], filePath);
    if (result.changed) {
      console.log(`OK    ${citySlug}`);
      successes++;
    } else {
      console.log(`WARN  ${citySlug} — ${result.reason}`);
      failures++;
    }
  } catch (err) {
    console.error(`ERR   ${citySlug} — ${err.message}`);
    failures++;
  }
}

console.log(`\n===== PATCH SUMMARY =====`);
console.log(`Success: ${successes}`);
console.log(`Warn/Err: ${failures}`);
