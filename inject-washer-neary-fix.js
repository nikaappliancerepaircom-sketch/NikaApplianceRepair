#!/usr/bin/env node
/**
 * inject-washer-neary-fix.js
 * Final fixes for remaining issues:
 * 1. Calgary & Edmonton: Insert FAQ section (before </main>)
 * 2. 6 v2 files without CITY-CONTENT-v2 markers: replace About paragraph
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

// Build v3-style FAQ section (details/summary pattern, inserted before </main>)
function buildV3FaqSection(citySlug, faqs) {
  const cityTitle = citySlug.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
  const items = faqs.map(faq => `      <details class="faq-item">
        <summary class="faq-question">
          ${faq.q}
          <span class="faq-icon">+</span>
        </summary>
        <div class="faq-answer">${faq.a}</div>
      </details>`).join('\n');

  return `\n<section class="faq-section" aria-labelledby="faq-heading-${citySlug}" style="padding:56px 0;border-top:1px solid #e5e7eb">
  <div class="container">
    <h2 id="faq-heading-${citySlug}" style="font-size:clamp(1.5rem,3vw,2rem);font-weight:700;letter-spacing:-.03em;color:#0a0a0a;margin-bottom:32px">Frequently Asked Questions — Washer Repair in ${cityTitle}</h2>
    <div style="margin-top:24px">
${items}
    </div>
  </div>
</section>\n`;
}

const allContent = loadAllContent();

let successes = 0;
let failures = 0;

// --- Fix 1: Calgary & Edmonton — insert FAQ before </main> ---
console.log('--- Fixing Calgary & Edmonton FAQ ---');
['calgary', 'edmonton'].forEach(citySlug => {
  const filePath = path.join(SITE_DIR, `washer-repair-${citySlug}.html`);
  let html = fs.readFileSync(filePath, 'utf8');
  const original = html;

  // Make sure we don't already have an actual HTML faq-section element
  const hasActualFaq = /<section[^>]*class="faq-section"/.test(html);
  if (hasActualFaq) {
    console.log(`SKIP  ${citySlug} — already has faq-section element`);
    return;
  }

  const faqSection = buildV3FaqSection(citySlug, allContent[citySlug].faq);
  html = html.replace('</main>', faqSection + '</main>');

  if (html !== original) {
    fs.writeFileSync(filePath, html, 'utf8');
    console.log(`OK    ${citySlug} — FAQ inserted`);
    successes++;
  } else {
    console.log(`WARN  ${citySlug} — </main> not found`);
    failures++;
  }
});

// --- Fix 2: 6 v2 files without CITY-CONTENT-v2 markers ---
// These have <h2>About City</h2> followed by 1-2 paragraphs to replace
const V2_NO_MARKER = ['ossington', 'roncesvalles', 'st-lawrence', 'thorncliffe-park', 'trinity-bellwoods', 'wychwood'];

console.log('\n--- Fixing v2 files without CITY-CONTENT-v2 markers ---');
V2_NO_MARKER.forEach(citySlug => {
  const filePath = path.join(SITE_DIR, `washer-repair-${citySlug}.html`);
  let html = fs.readFileSync(filePath, 'utf8');
  const original = html;
  const content = allContent[citySlug];
  const cityTitle = citySlug.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');

  // Replace the <h2>About City</h2> heading with new H2 and inject CITY-CONTENT-v2 block
  // The pattern is: <h2>About CityTitle</h2>\n      <p>...</p>\n      <p class="city-context">...
  // We keep the city-context paragraph (already updated) and replace the first <p> block

  // Step 1: Replace h2 heading
  html = html.replace(
    new RegExp(`<h2>About ${cityTitle}<\\/h2>`),
    `<h2>${content.content_h2}</h2>`
  );

  // Step 2: Find the first <p> block after the (now replaced) h2 and replace it
  // with CITY-CONTENT-v2 markers + new content
  // Pattern: after the h2, there's a <p>...description of city...</p>
  // We need to replace that <p> block with our new 2 paragraphs
  html = html.replace(
    new RegExp(`(<h2>${escapeRegex(content.content_h2)}<\\/h2>\\s*)<p>([^<]*(?:<(?!\\/p>)[^<]*)*)</p>(\\s*<p class="city-context">)`),
    (match, h2end, oldContent, cityCtxStart) => {
      return `${h2end}<!-- CITY-CONTENT-v2 -->
    <p style="margin:0 0 14px;color:#374151;line-height:1.7;font-size:0.9375rem;">${content.intro_p1}</p>
    <p style="margin:0 0 14px;color:#374151;line-height:1.7;font-size:0.9375rem;">${content.intro_p2}</p>
    <!-- END-CITY-CONTENT-v2 -->
    ${cityCtxStart}`;
    }
  );

  if (html !== original) {
    fs.writeFileSync(filePath, html, 'utf8');
    console.log(`OK    ${citySlug}`);
    successes++;
  } else {
    // Try a broader regex
    // Some files might have slightly different structure
    let html2 = fs.readFileSync(filePath, 'utf8');
    // Get the About h2 area and replace with new content directly
    const aboutH2Regex = /<h2>About ([^<]+)<\/h2>/;
    const abMatch = html2.match(aboutH2Regex);
    if (abMatch) {
      html2 = html2.replace(aboutH2Regex, `<h2>${content.content_h2}</h2>\n<!-- CITY-CONTENT-v2 -->\n    <p style="margin:0 0 14px;color:#374151;line-height:1.7;font-size:0.9375rem;">${content.intro_p1}</p>\n    <p style="margin:0 0 14px;color:#374151;line-height:1.7;font-size:0.9375rem;">${content.intro_p2}</p>\n    <!-- END-CITY-CONTENT-v2 -->`);
      // Now remove the old paragraph that was below the h2
      // Pattern: the first <p> that doesn't have class="city-context" after END-CITY-CONTENT-v2 heading
      html2 = html2.replace(
        /(<\/-- END-CITY-CONTENT-v2 -->\s*)<p>(?!<strong>)([^]*?)<\/p>(\s*<p class="city-context">)/,
        '$1$3'
      );
    }

    if (html2 !== fs.readFileSync(filePath, 'utf8')) {
      fs.writeFileSync(filePath, html2, 'utf8');
      console.log(`OK    ${citySlug} (fallback)`);
      successes++;
    } else {
      console.log(`WARN  ${citySlug} — pattern didn't match`);
      failures++;
    }
  }
});

function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

console.log(`\n===== FIX SUMMARY =====`);
console.log(`Success: ${successes}`);
console.log(`Warn/Err: ${failures}`);
