#!/usr/bin/env node
/**
 * fix-alberta-nap.js
 * Fixes NAP conflict on all Alberta pages on nikaappliancerepair.com:
 *   1. Remove noindex → index
 *   2. Remove Toronto phone (437) 524-1053 from <title>
 *   3. Remove Toronto phone from <meta name="description">, og:description, twitter:description
 *   4. Remove Toronto phone from og:title, twitter:title (clean, no HTML)
 *   5. Remove telephone from JSON-LD schema
 *   6. Remove phone links / visible phone text from page body
 */

const fs = require('fs');
const path = require('path');

const DIR = path.join(__dirname);

const ALBERTA_PATTERNS = [
  'calgary', 'edmonton', 'airdrie', 'cochrane', 'okotoks',
  'sherwood-park', 'spruce-grove', 'leduc', 'beaumont',
  'fort-saskatchewan', 'canmore', 'chestermere', 'devon',
  'langdon', 'high-river', 'st-albert'
];

let stats = {
  filesScanned: 0,
  filesFixed: 0,
  noindexFixed: 0,
  titleFixed: 0,
  descFixed: 0,
  ogTitleFixed: 0,
  schemaFixed: 0,
  bodyPhoneFixed: 0,
};

function isAlbertaFile(filename) {
  const base = path.basename(filename).toLowerCase();
  return ALBERTA_PATTERNS.some(p => base.includes(p));
}

/** Strip phone from <title> tag (plain text context) */
function fixHtmlTitle(content) {
  const before = content;
  // Remove "| (437) 524-1053 YYYY", "| Call (437) 524-1053 YYYY", etc.
  content = content.replace(
    /(<title>[^<]*?)\s*\|\s*(?:Call\s*)?\(437\)\s*524-1053(?:\s*\d{4})?(<\/title>)/gi,
    '$1$2'
  );
  // Also no separator
  content = content.replace(
    /(<title>[^<]*?)\s*(?:Call\s*)?\(437\)\s*524-1053(?:\s*\d{4})?(<\/title>)/gi,
    '$1$2'
  );
  // Clean trailing "| " or "— " left at end
  content = content.replace(/(<title>[^<]*?)\s*[|—–]\s*(<\/title>)/gi, '$1$2');
  // Trim interior whitespace
  content = content.replace(/(<title>)\s*(.*?)\s*(<\/title>)/gi,
    (m, o, inner, c) => o + inner.trim() + c);
  return content;
}

/** Strip phone from a meta content="..." attribute value (no HTML allowed inside) */
function stripPhoneFromMetaContent(attrValue) {
  // Remove "Call (437) 524-1053" with surrounding punctuation
  attrValue = attrValue.replace(/\.?\s*Call\s*\(437\)\s*524-1053[.!]?/gi, '. Book online.');
  attrValue = attrValue.replace(/\s*\(437\)\s*524-1053[.!]?/gi, '. Book online.');
  // Clean double ". Book online."
  attrValue = attrValue.replace(/\.\s*\.\s*Book online\./gi, '. Book online.');
  attrValue = attrValue.replace(/Book online\.\s*Book online\./gi, 'Book online.');
  return attrValue;
}

/** Strip phone from meta description / og:description / twitter:description attributes */
function fixMetaTags(content) {
  // Match meta tags that have content="..." and process the content attribute
  content = content.replace(
    /(<meta\s[^>]*?content=")([^"]*?)("[^>]*>)/gi,
    (match, prefix, value, suffix) => {
      const fixed = stripPhoneFromMetaContent(value);
      return prefix + fixed + suffix;
    }
  );
  return content;
}

/** Strip phone from og:title / twitter:title — these are now handled by fixMetaTags above */
// The fixMetaTags function handles all meta content= attributes cleanly.

function fixSchema(content) {
  // Remove "telephone": "+14375241053" from JSON-LD
  // Remove the whole line (handles indented JSON)
  content = content.replace(/[ \t]*"telephone"\s*:\s*"\+14375241053"\s*,?\r?\n/gi, '');
  // Remove if it appears without a trailing newline
  content = content.replace(/"telephone"\s*:\s*"\+14375241053"\s*,?/gi, '');
  // Fix JSON that might now have a trailing comma before closing brace/bracket
  content = content.replace(/,(\s*[}\]])/g, '$1');
  return content;
}

function fixBody(content) {
  let changed = false;

  // 1. Call button (btn-primary) linking to tel:
  if (/<a\s+href="tel:\+14375241053"[^>]*class="[^"]*btn-primary[^"]*"/i.test(content)) {
    content = content.replace(
      /<a\s+href="tel:\+14375241053"[^>]*class="[^"]*btn-primary[^"]*"[^>]*>[\s\S]*?<\/a>/gi,
      '<a href="/book" class="btn-primary">Book Online</a>'
    );
    changed = true;
  }

  // 2. Sticky call button
  if (/<a\s+href="tel:\+14375241053"[^>]*class="[^"]*sticky/i.test(content)) {
    content = content.replace(
      /<a\s+href="tel:\+14375241053"[^>]*class="[^"]*sticky[^"]*"[^>]*>[\s\S]*?<\/a>/gi,
      ''
    );
    changed = true;
  }

  // 3. Any remaining tel: links
  if (/href="tel:\+14375241053"/i.test(content)) {
    content = content.replace(
      /<a\s+href="tel:\+14375241053"[^>]*>([\s\S]*?)<\/a>/gi,
      '<a href="/book">Book Online</a>'
    );
    changed = true;
  }

  // 4. Bare "Call (437) 524-1053" text in HTML body
  if (/Call\s*\(437\)\s*524-1053/.test(content)) {
    content = content.replace(
      /Call\s*\(437\)\s*524-1053/g,
      'Book online at <a href="/book">nikaappliancerepair.com/book</a>'
    );
    changed = true;
  }

  // 5. Bare phone number remaining
  if (/\(437\)\s*524-1053/.test(content)) {
    content = content.replace(/\(437\)\s*524-1053/g, '<a href="/book">Book Online</a>');
    changed = true;
  }

  return { content, changed };
}

function processFile(filePath) {
  let content = fs.readFileSync(filePath, 'utf8');
  const original = content;
  let fileChanges = {
    noindex: false,
    title: false,
    metaTags: false,
    schema: false,
    body: false,
  };

  // Fix 1: noindex → index
  if (/content="noindex,\s*follow"/i.test(content)) {
    content = content.replace(/content="noindex,\s*follow"/gi, 'content="index, follow"');
    fileChanges.noindex = true;
  }

  // Fix 2: <title> phone removal (before meta tag processing)
  const titleBefore = content;
  content = fixHtmlTitle(content);
  if (content !== titleBefore) fileChanges.title = true;

  // Fix 3+4: All meta content attributes (desc, og:desc, twitter:desc, og:title, twitter:title)
  const metaBefore = content;
  content = fixMetaTags(content);
  if (content !== metaBefore) fileChanges.metaTags = true;

  // Fix 5: JSON-LD schema telephone
  const schemaBefore = content;
  content = fixSchema(content);
  if (content !== schemaBefore) fileChanges.schema = true;

  // Fix 6: Body phone links and text
  const { content: bodyFixed, changed: bodyChanged } = fixBody(content);
  content = bodyFixed;
  fileChanges.body = bodyChanged;

  if (content !== original) {
    fs.writeFileSync(filePath, content, 'utf8');
    stats.filesFixed++;
    if (fileChanges.noindex) stats.noindexFixed++;
    if (fileChanges.title) stats.titleFixed++;
    if (fileChanges.metaTags) stats.descFixed++;
    if (fileChanges.schema) stats.schemaFixed++;
    if (fileChanges.body) stats.bodyPhoneFixed++;

    const changes = Object.entries(fileChanges)
      .filter(([, v]) => v)
      .map(([k]) => k)
      .join(', ');
    console.log(`  FIXED [${changes}]: ${path.basename(filePath)}`);
  } else {
    console.log(`  ok (no changes): ${path.basename(filePath)}`);
  }
}

// Main
const files = fs.readdirSync(DIR)
  .filter(f => f.endsWith('.html') && isAlbertaFile(f))
  .map(f => path.join(DIR, f));

console.log(`\nFound ${files.length} Alberta HTML files\n`);
stats.filesScanned = files.length;

files.forEach(f => processFile(f));

console.log('\n=== SUMMARY ===');
console.log(`Files scanned  : ${stats.filesScanned}`);
console.log(`Files modified : ${stats.filesFixed}`);
console.log(`  noindex→index: ${stats.noindexFixed}`);
console.log(`  title fixed  : ${stats.titleFixed}`);
console.log(`  meta tags    : ${stats.descFixed}`);
console.log(`  schema fixed : ${stats.schemaFixed}`);
console.log(`  body phone   : ${stats.bodyPhoneFixed}`);
