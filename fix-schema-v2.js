/**
 * fix-schema-v2.js — Add priceRange, serviceArea, dateModified to schema
 * Processes all .html files in NAR + NEARY + FIXLIFY root dirs
 * Usage: node fix-schema-v2.js [--dry-run]
 */
const fs = require('fs');
const path = require('path');

const DRY_RUN = process.argv.includes('--dry-run');

const sites = [
  { dir: 'C:/nappliancerepair', domain: 'nappliancerepair.com' },
  { dir: 'C:/appliancerepairneary', domain: 'appliancerepairneary.com' },
  { dir: 'C:/fixlifyservices', domain: 'fixlifyservices.com' },
];

const TODAY = '2026-03-06';

if (DRY_RUN) console.log('=== DRY RUN MODE ===\n');

sites.forEach(({ dir, domain }) => {
  if (!fs.existsSync(dir)) {
    console.log('SKIP ' + domain + ' — dir not found');
    return;
  }

  const files = fs.readdirSync(dir).filter(f => {
    if (!f.endsWith('.html')) return false;
    if (f === '404.html' || f === 'service-template.html') return false;
    return true;
  });

  let fixPR = 0, fixSA = 0, fixDM = 0, filesChanged = 0;

  files.forEach(file => {
    const filePath = path.join(dir, file);
    let c = fs.readFileSync(filePath, 'utf8');
    let changed = false;

    // ── Fix 1: Add priceRange after "telephone" line ──
    if (c.includes('"LocalBusiness"') && !c.includes('"priceRange"')) {
      // Match: "telephone": "+1234567890", (with optional trailing comma and newline)
      const telRegex = /("telephone"\s*:\s*"[^"]*"),?\s*\n/;
      const telMatch = c.match(telRegex);
      if (telMatch) {
        const matchStart = c.indexOf(telMatch[0]);
        const lineStart = c.lastIndexOf('\n', matchStart) + 1;
        const indent = c.substring(lineStart, matchStart);

        // Build replacement: telephone line with comma, then priceRange line
        const newBlock = telMatch[1] + ',\n' + indent + '"priceRange": "$$",\n';
        c = c.substring(0, matchStart) + newBlock + c.substring(matchStart + telMatch[0].length);
        changed = true;
        fixPR++;
      }
    }

    // ── Fix 2: Add areaServed after address block ──
    if (c.includes('"LocalBusiness"') && !c.includes('"areaServed"') && !c.includes('"serviceArea"')) {
      const cityMatch = c.match(/"addressLocality"\s*:\s*"([^"]+)"/);
      const city = cityMatch ? cityMatch[1] : 'Toronto';

      const addrIdx = c.indexOf('"address"');
      if (addrIdx !== -1) {
        // Find the matching closing brace for the address object
        let braceCount = 0;
        let startBrace = c.indexOf('{', addrIdx);
        let endBrace = -1;
        for (let i = startBrace; i < c.length; i++) {
          if (c[i] === '{') braceCount++;
          if (c[i] === '}') braceCount--;
          if (braceCount === 0) { endBrace = i; break; }
        }
        if (endBrace !== -1) {
          // Get indentation of "address" line
          const addrLineStart = c.lastIndexOf('\n', addrIdx) + 1;
          const indent = c.substring(addrLineStart, addrIdx);

          // Ensure comma after address closing brace
          let afterBrace = c[endBrace + 1];
          let insertAt;
          if (afterBrace === ',') {
            insertAt = endBrace + 2;
          } else {
            // Add comma
            c = c.substring(0, endBrace + 1) + ',' + c.substring(endBrace + 1);
            insertAt = endBrace + 2;
          }

          const areaBlock = '\n' + indent + '"areaServed": {\n' +
            indent + '  "@type": "City",\n' +
            indent + '  "name": "' + city + '"\n' +
            indent + '},';

          c = c.substring(0, insertAt) + areaBlock + c.substring(insertAt);
          changed = true;
          fixSA++;
        }
      }
    }

    // ── Fix 3: Add dateModified after datePublished ──
    if (c.includes('"datePublished"') && !c.includes('"dateModified"')) {
      const dpRegex = /("datePublished"\s*:\s*"[^"]*"),?\s*\n/;
      const dpMatch = c.match(dpRegex);
      if (dpMatch) {
        const matchStart = c.indexOf(dpMatch[0]);
        const lineStart = c.lastIndexOf('\n', matchStart) + 1;
        const indent = c.substring(lineStart, matchStart);

        const newBlock = dpMatch[1] + ',\n' + indent + '"dateModified": "' + TODAY + '",\n';
        c = c.substring(0, matchStart) + newBlock + c.substring(matchStart + dpMatch[0].length);
        changed = true;
        fixDM++;
      }
    }

    if (changed) {
      filesChanged++;
      if (!DRY_RUN) {
        fs.writeFileSync(filePath, c, 'utf8');
      }
    }
  });

  console.log('=== ' + domain + ' (' + files.length + ' pages) ===');
  console.log('  priceRange added:   ' + fixPR + ' pages');
  console.log('  areaServed added:   ' + fixSA + ' pages');
  console.log('  dateModified added: ' + fixDM + ' pages');
  console.log('  Files changed:      ' + filesChanged);
  console.log('');
});

console.log(DRY_RUN ? 'DRY RUN — no files written.' : 'All fixes applied.');
