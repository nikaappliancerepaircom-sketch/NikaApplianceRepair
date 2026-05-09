/**
 * fix-rating-consistency.js — Update NIKA pages to show 4.9/250 rating
 * Updates both JSON-LD schema and visible hero text
 */
const fs = require('fs');
const path = require('path');

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

const SITES = [
  { dir: 'C:/NikaApplianceRepair', rating: '4.9', count: '250' },
];

let total = 0;

for (const site of SITES) {
  let fixed = 0;
  const files = walk(site.dir);

  for (const fp of files) {
    let html = fs.readFileSync(fp, 'utf8');
    let changed = false;

    // Fix JSON-LD ratingValue and reviewCount
    const newHtml = html
      .replace(/"ratingValue":\s*"4\.[0-8]"/g, `"ratingValue": "${site.rating}"`)
      .replace(/"reviewCount":\s*"\d+"(?=\s*,?\s*\n?\s*"bestRating"|\s*,?\s*\n?\s*"worstRating"|\s*,?\s*\n?\s*"ratingValue")/g, 
               `"reviewCount": "${site.count}"`)
      .replace(/"reviewCount":\s*"(?!250)\d+"/g, `"reviewCount": "${site.count}"`)
      // Fix visible hero text patterns
      .replace(/⭐\s*4\.[0-8]\/5[^<]*?(\d+)\s*reviews/g, 
               `⭐ ${site.rating}/5 rating · ${site.count} reviews`)
      .replace(/(\d+)\/5\s*(?:rating\s*[·•]\s*)(\d+)\s*reviews/g, 
               (m, r, c) => (r !== site.rating || c !== site.count) ? `${site.rating}/5 rating · ${site.count} reviews` : m);

    if (newHtml !== html) {
      fs.writeFileSync(fp, newHtml, 'utf8');
      fixed++;
    }
  }

  console.log(`${path.basename(site.dir)}: ${fixed} pages updated with rating ${site.rating}/${site.count}`);
  total += fixed;
}

console.log(`Total: ${total} pages`);
