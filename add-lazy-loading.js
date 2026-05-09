/**
 * add-lazy-loading.js — Add loading=lazy to below-fold images on all 4 sites
 * Skips: images with fetchpriority="high", first image in file, hero-section images
 */
const fs = require('fs');
const path = require('path');

const SITES = [
  'C:/NikaApplianceRepair',
  'C:/nappliancerepair',
  'C:/appliancerepairneary',
  'C:/fixlifyservices',
];

const SKIP_DIRS = new Set(['node_modules','.git','_queue','assets','css','js','images','fonts','components','templates','styles','backups','backup','old','archive','reports','tools','compare','preview','_drafts']);

function walk(dir) {
  const out = [];
  let items;
  try { items = fs.readdirSync(dir, { withFileTypes: true }); } catch { return out; }
  for (const item of items) {
    if (item.isDirectory()) {
      if (SKIP_DIRS.has(item.name)) continue;
      out.push(...walk(path.join(dir, item.name)));
    } else if (item.name.endsWith('.html') && !item.name.includes('.bak')) {
      out.push(path.join(dir, item.name));
    }
  }
  return out;
}

let totalPages = 0;
let totalImgs = 0;

for (const dir of SITES) {
  let pagesFixed = 0, imgsFixed = 0;
  const files = walk(dir);

  for (const fp of files) {
    let html = fs.readFileSync(fp, 'utf8');
    let changed = false;
    let isFirstImg = true;

    // Process img tags - add loading=lazy to non-hero, non-priority images
    const newHtml = html.replace(/<img\s([^>]+)>/gi, (match, attrs) => {
      // Skip if already has loading attribute
      if (/\bloading\s*=/i.test(attrs)) return match;
      // Skip first image (likely hero/LCP)
      if (isFirstImg) { isFirstImg = false; return match; }
      // Skip if fetchpriority=high (it's an LCP image)
      if (/fetchpriority\s*=\s*["']?high/i.test(attrs)) return match;
      // Add loading=lazy
      imgsFixed++;
      changed = true;
      return `<img ${attrs} loading="lazy">`;
    });

    if (changed) {
      html = newHtml;
      fs.writeFileSync(fp, html, 'utf8');
      pagesFixed++;
    }
  }

  console.log(`${path.basename(dir)}: ${pagesFixed} pages, ${imgsFixed} images updated`);
  totalPages += pagesFixed;
  totalImgs += imgsFixed;
}

console.log(`\nTotal: ${totalPages} pages, ${totalImgs} images with loading=lazy`);
