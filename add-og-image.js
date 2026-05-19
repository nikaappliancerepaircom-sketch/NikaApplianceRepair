#!/usr/bin/env node
/**
 * add-og-image.js
 * Adds og:image and twitter:image meta tags to service/brand pages
 * that are missing them.
 *
 * Usage: node add-og-image.js <site-dir> <domain>
 * Example: node add-og-image.js C:/fixlifyservices fixlifyservices.com
 */

const fs = require('fs');
const path = require('path');

// --- Config ---
const SKIP_FILES = new Set(['index.html', 'about.html', '404.html', 'terms.html', 'privacy.html']);

const IMAGE_MAP = [
  { prefix: 'dishwasher', image: 'dishwasher-repair-service.webp' },
  { prefix: 'washer',     image: 'washer-repair-service.webp' },
  { prefix: 'dryer',      image: 'dryer-repair-service.webp' },
  { prefix: 'fridge',     image: 'fridge-repair-service.webp' },
  { prefix: 'refrigerator', image: 'fridge-repair-service.webp' },
  { prefix: 'oven',       image: 'oven-repair-service.webp' },
  { prefix: 'stove',      image: 'stove-repair-service.webp' },
  { prefix: 'range',      image: 'stove-repair-service.webp' },
];
const DEFAULT_IMAGE = 'appliance-technician-hero.webp';

// --- Helpers ---
function getImageForFile(filename) {
  const base = filename.toLowerCase();
  for (const { prefix, image } of IMAGE_MAP) {
    if (base.startsWith(prefix)) return image;
  }
  return DEFAULT_IMAGE;
}

function buildMetaTags(imageUrl) {
  return [
    `<meta property="og:image" content="${imageUrl}" />`,
    `<meta property="og:image:width" content="1200" />`,
    `<meta property="og:image:height" content="675" />`,
    `<meta name="twitter:image" content="${imageUrl}" />`,
  ].join('\n    ');
}

function getAllHtmlFiles(dir) {
  const results = [];
  function walk(current) {
    const entries = fs.readdirSync(current, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(current, entry.name);
      if (entry.isDirectory()) {
        walk(fullPath);
      } else if (entry.isFile() && entry.name.endsWith('.html')) {
        results.push(fullPath);
      }
    }
  }
  walk(dir);
  return results;
}

// --- Main ---
const [,, siteDir, domain] = process.argv;

if (!siteDir || !domain) {
  console.error('Usage: node add-og-image.js <site-dir> <domain>');
  process.exit(1);
}

if (!fs.existsSync(siteDir)) {
  console.error(`Directory not found: ${siteDir}`);
  process.exit(1);
}

const allFiles = getAllHtmlFiles(siteDir);
let updated = 0;
let skippedHasTag = 0;
let skippedName = 0;

for (const filePath of allFiles) {
  const filename = path.basename(filePath);

  // Skip excluded files
  if (SKIP_FILES.has(filename)) {
    skippedName++;
    continue;
  }

  let content = fs.readFileSync(filePath, 'utf8');

  // Skip if og:image already present
  if (content.includes('og:image')) {
    skippedHasTag++;
    continue;
  }

  const imageFile = getImageForFile(filename);
  const imageUrl = `https://${domain}/img/${imageFile}`;
  const tags = buildMetaTags(imageUrl);

  // Inject before </head>
  const newContent = content.replace('</head>', `    ${tags}\n</head>`);

  if (newContent === content) {
    // </head> not found — skip silently
    continue;
  }

  fs.writeFileSync(filePath, newContent, 'utf8');
  updated++;
  console.log(`  + ${path.relative(siteDir, filePath)}  →  ${imageFile}`);
}

console.log(`\nDone: ${updated} files updated, ${skippedHasTag} already had og:image, ${skippedName} skipped by name.`);
