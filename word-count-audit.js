/**
 * word-count-audit.js — Check word count distribution across all 4 sites
 */
const fs = require('fs');
const path = require('path');

const SITES = [
  { dir: 'C:/NikaApplianceRepair', name: 'NIKA' },
  { dir: 'C:/nappliancerepair', name: 'NAR' },
  { dir: 'C:/appliancerepairneary', name: 'NEARY' },
  { dir: 'C:/fixlifyservices', name: 'FIXLIFY' },
];

const SKIP_DIRS = new Set(['node_modules','.git','_queue','assets','css','js','images','fonts','components','templates','styles','backups','backup','old','archive','reports','tools','compare','preview','_drafts']);
const MIN_WORDS = 1200;

function stripTags(html) {
  // Remove scripts, styles, nav, header, footer, schema
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<style[\s\S]*?<\/style>/gi, '')
    .replace(/<nav[\s\S]*?<\/nav>/gi, '')
    .replace(/<header[\s\S]*?<\/header>/gi, '')
    .replace(/<footer[\s\S]*?<\/footer>/gi, '')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function walk(dir) {
  const out = [];
  let items;
  try { items = fs.readdirSync(dir, { withFileTypes: true }); } catch { return out; }
  for (const item of items) {
    if (item.isDirectory()) {
      if (SKIP_DIRS.has(item.name)) continue;
      out.push(...walk(path.join(dir, item.name)));
    } else if (item.name.endsWith('.html') && !item.name.includes('.bak')) {
      const skip = ['404','about','contact','sitemap','privacy','terms','ajax','book','service-template'];
      if (!skip.some(s => item.name.includes(s))) {
        out.push(path.join(dir, item.name));
      }
    }
  }
  return out;
}

console.log('\n=== WORD COUNT AUDIT — All 4 Sites ===\n');

for (const site of SITES) {
  const files = walk(site.dir);
  const counts = [];
  let under1200 = 0, under800 = 0, over4500 = 0;

  for (const fp of files) {
    const html = fs.readFileSync(fp, 'utf8');
    const text = stripTags(html);
    const wc = text.split(/\s+/).filter(w => w.length > 0).length;
    counts.push({ file: path.relative(site.dir, fp), wc });
    if (wc < 800) under800++;
    if (wc < 1200) under1200++;
    if (wc > 4500) over4500++;
  }

  counts.sort((a, b) => a.wc - b.wc);
  const total = counts.length;
  const avg = Math.round(counts.reduce((s, c) => s + c.wc, 0) / total);
  const median = counts[Math.floor(total / 2)].wc;
  const min5 = counts.slice(0, 5);
  const max5 = counts.slice(-5).reverse();

  console.log(`📊 ${site.name} (${total} pages):`);
  console.log(`   Avg: ${avg} words | Median: ${median} | Min threshold: ${MIN_WORDS}`);
  console.log(`   Under 800 words: ${under800} pages (${Math.round(under800/total*100)}%)`);
  console.log(`   Under 1200 words: ${under1200} pages (${Math.round(under1200/total*100)}%)`);
  console.log(`   Over 4500 words: ${over4500} pages`);
  console.log(`   5 shortest pages:`);
  min5.forEach(c => console.log(`     ${c.wc} words — ${c.file}`));
  console.log();
}
