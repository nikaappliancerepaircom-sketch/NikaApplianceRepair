#!/usr/bin/env node
/**
 * fix-gradient-text.js
 * Replace inline gradient text styles with solid color on all location/brand pages
 */
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname);

const DIRS = ['locations', 'brands', 'services'];

// Match inline style with gradient text pattern
const OLD_PATTERN = /style="([^"]*)background:\s*linear-gradient\([^)]+\)[^"]*-webkit-text-fill-color:\s*transparent[^"]*"/g;

function fixFile(filePath) {
  let html = fs.readFileSync(filePath, 'utf8');
  if (!html.includes('-webkit-text-fill-color: transparent')) return false;

  const newHtml = html.replace(OLD_PATTERN, (match, before) => {
    // Extract any non-gradient styles (text-decoration, font-weight, etc.)
    const extras = (before + match.replace(/.*style="/, '').replace(/"$/, ''))
      .replace(/background:[^;]+;/g, '')
      .replace(/-webkit-background-clip:[^;]+;/g, '')
      .replace(/background-clip:[^;]+;/g, '')
      .replace(/-webkit-text-fill-color:[^;]+;/g, '')
      .replace(/color:[^;]+;/g, '')
      .trim()
      .replace(/^;+|;+$/g, '')
      .trim();

    const extraParts = extras ? ' ' + extras : '';
    return `style="color: #1565C0; text-decoration: none; font-weight: 700;${extraParts}"`;
  });

  if (newHtml !== html) {
    fs.writeFileSync(filePath, newHtml, 'utf8');
    return true;
  }
  return false;
}

let total = 0;
for (const dir of DIRS) {
  const dirPath = path.join(ROOT, dir);
  if (!fs.existsSync(dirPath)) continue;
  for (const f of fs.readdirSync(dirPath)) {
    if (!f.endsWith('.html')) continue;
    const fixed = fixFile(path.join(dirPath, f));
    if (fixed) {
      console.log(`  Fixed: ${dir}/${f}`);
      total++;
    }
  }
}
console.log(`\nTotal files fixed: ${total}`);
