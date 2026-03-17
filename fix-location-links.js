const fs = require('fs');
const path = require('path');

const servicesDir = 'C:/NikaApplianceRepair/locations/services';

const serviceTypes = [
  'refrigerator',
  'dishwasher',
  'washer',
  'dryer',
  'oven',
  'stove'
];

const files = fs.readdirSync(servicesDir).filter(f => f.endsWith('.html'));

let totalFilesChanged = 0;
let totalReplacements = 0;
const errors = [];

for (const file of files) {
  const filePath = path.join(servicesDir, file);
  let content;
  try {
    content = fs.readFileSync(filePath, 'utf8');
  } catch (e) {
    errors.push(`Error reading ${file}: ${e.message}`);
    continue;
  }

  let newContent = content;
  let fileReplacements = 0;

  // Fix internal service links
  for (const service of serviceTypes) {
    const pattern = `href="/${service}-repair-`;
    const replacement = `href="/locations/services/${service}-repair-`;
    let idx = 0;
    while (true) {
      const pos = newContent.indexOf(pattern, idx);
      if (pos === -1) break;
      newContent = newContent.slice(0, pos) + replacement + newContent.slice(pos + pattern.length);
      fileReplacements++;
      idx = pos + replacement.length;
    }
  }

  // Fix broken closing tag in washer-repair-vaughan.html
  if (file === 'washer-repair-vaughan.html') {
    const brokenTag = '<h3>Washer Leaking Water</html>';
    const fixedTag = '<h3>Washer Leaking Water</h3>';
    if (newContent.includes(brokenTag)) {
      newContent = newContent.replace(brokenTag, fixedTag);
      fileReplacements++;
      console.log(`  Fixed broken </html> tag in washer-repair-vaughan.html`);
    }
  }

  if (newContent !== content) {
    try {
      fs.writeFileSync(filePath, newContent, 'utf8');
      totalFilesChanged++;
      totalReplacements += fileReplacements;
      console.log(`  Updated: ${file} (${fileReplacements} replacements)`);
    } catch (e) {
      errors.push(`Error writing ${file}: ${e.message}`);
    }
  }
}

console.log('\n=== Summary ===');
console.log(`Files scanned: ${files.length}`);
console.log(`Files changed: ${totalFilesChanged}`);
console.log(`Total replacements: ${totalReplacements}`);
if (errors.length > 0) {
  console.log(`Errors (${errors.length}):`);
  errors.forEach(e => console.log('  ' + e));
} else {
  console.log('Errors: none');
}
