const fs = require('fs');

function countRealWords(html) {
  let text = html
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<style[\s\S]*?<\/style>/gi, '')
    .replace(/<nav[\s\S]*?<\/nav>/gi, '')
    .replace(/<footer[\s\S]*?<\/footer>/gi, '')
    .replace(/<header[\s\S]*?<\/header>/gi, '')
    .replace(/<!--[\s\S]*?-->/g, '')
    // Remove ALL html tag attributes (strip tag contents too)
    .replace(/<[^>]+>/g, ' ')
    // Remove standalone numbers, URLs, codes
    .replace(/https?:\/\/\S+/g, '')
    .replace(/\b\d+\b/g, '')
    // Remove short tokens (1-2 chars, likely html noise)
    .replace(/\b\w{1,2}\b/g, '')
    .replace(/\s+/g, ' ')
    .trim();
  
  // Count only words with real letters (3+ chars)
  return text.split(/\s+/).filter(w => /[a-zA-Z]{3,}/.test(w)).length;
}

// Check a few sample pages to verify accuracy
const samples = [
  'locations/services/dishwasher-repair-ossington.html',   // ~757 words
  'locations/services/dryer-repair-markham.html',           // ~913 words  
  'locations/services/dishwasher-repair-richmond-hill.html',// ~1001 words
  'locations/services/washer-repair-vaughan.html',          // ~878 words
  'blog/posts/samsung-washer-not-spinning-toronto.html',   // ~1031 words
  'blog/troubleshooting/dryer-belt-replacement-guide.html', // good
  'blog/maintenance/fridge-temperature-guide.html',         // good
];

for (const s of samples) {
  const fp = 'C:/NikaApplianceRepair/' + s;
  if (!fs.existsSync(fp)) { console.log('MISSING:', s); continue; }
  const html = fs.readFileSync(fp, 'utf8');
  const w = countRealWords(html);
  console.log(`${w.toString().padStart(5)} real words  ${s}`);
}
