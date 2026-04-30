const fs = require('fs');
const path = require('path');

function countWords(html) {
  // Remove script, style, schema, nav, footer, header blocks
  let text = html
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<style[\s\S]*?<\/style>/gi, '')
    .replace(/<nav[\s\S]*?<\/nav>/gi, '')
    .replace(/<footer[\s\S]*?<\/footer>/gi, '')
    .replace(/<header[\s\S]*?<\/header>/gi, '')
    .replace(/<!--[\s\S]*?-->/g, '')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
  return text.split(' ').filter(w => w.length > 1).length;
}

const dirs = [
  'blog/posts',
  'blog/maintenance',
  'blog/troubleshooting',
  'blog/guides',
  'blog/tips',
  'locations/services',
];

const results = { ok: [], low: [], missing: [] };

for (const dir of dirs) {
  const fullDir = path.join('C:/NikaApplianceRepair', dir);
  if (!fs.existsSync(fullDir)) continue;
  const files = fs.readdirSync(fullDir).filter(f => f.endsWith('.html'));
  for (const file of files) {
    // skip noindex pages
    if (['appliance-repair-cabbagetown.html','appliance-repair-distillery-district.html','appliance-repair-king-west.html','appliance-repair-queen-west.html','appliance-repair-peterborough.html'].includes(file)) continue;
    const filepath = path.join(fullDir, file);
    const html = fs.readFileSync(filepath, 'utf8');
    const words = countWords(html);
    const url = `/${dir}/${file.replace('.html','')}`;
    const entry = { url, words, file: filepath.replace('C:/NikaApplianceRepair/', '') };
    if (words >= 1300) results.ok.push(entry);
    else results.low.push(entry);
  }
}

// Also check hub pages
for (const hub of ['blog-nika-appliance-repair.html', 'brands.html', 'locations.html']) {
  const fp = path.join('C:/NikaApplianceRepair', hub);
  if (!fs.existsSync(fp)) { results.missing.push(hub); continue; }
  const html = fs.readFileSync(fp, 'utf8');
  const words = countWords(html);
  const entry = { url: '/' + hub.replace('.html',''), words, file: hub };
  if (words >= 1300) results.ok.push(entry);
  else results.low.push(entry);
}

console.log(`\n✅ OK (≥1300 words): ${results.ok.length} pages`);
console.log(`❌ LOW (<1300 words): ${results.low.length} pages`);

if (results.low.length > 0) {
  console.log('\n--- PAGES BELOW 1300 WORDS ---');
  results.low.sort((a,b) => a.words - b.words);
  results.low.forEach(p => console.log(`  ${p.words.toString().padStart(5)} words  ${p.url}`));
}

console.log('\n--- WORD COUNT DISTRIBUTION (low pages) ---');
const buckets = { '<400': 0, '400-699': 0, '700-999': 0, '1000-1299': 0 };
results.low.forEach(p => {
  if (p.words < 400) buckets['<400']++;
  else if (p.words < 700) buckets['400-699']++;
  else if (p.words < 1000) buckets['700-999']++;
  else buckets['1000-1299']++;
});
Object.entries(buckets).forEach(([k,v]) => v > 0 && console.log(`  ${k}: ${v} pages`));
