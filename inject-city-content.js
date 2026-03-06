/**
 * inject-city-content.js — Inject unique city content from city-content-data.json
 * Replaces existing city content blocks with generated content
 * Usage: node inject-city-content.js [--dry-run]
 */
const fs = require('fs');
const path = require('path');

const DRY_RUN = process.argv.includes('--dry-run');
const DATA_FILE = path.join(__dirname, 'city-content-data.json');
const START_MARKER = '<!-- CITY-CONTENT-v2 -->';
const END_MARKER = '<!-- END-CITY-CONTENT-v2 -->';

const sites = [
  { dir: 'C:/nappliancerepair', domain: 'nappliancerepair.com' },
  { dir: 'C:/appliancerepairneary', domain: 'appliancerepairneary.com' },
  { dir: 'C:/fixlifyservices', domain: 'fixlifyservices.com' },
];

const data = JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
const CITY_SLUGS = Object.keys(data);

function detectCity(filename) {
  const name = filename.replace('.html', '');
  const sorted = CITY_SLUGS.slice().sort((a, b) => b.length - a.length);
  for (const slug of sorted) {
    if (name === slug || name.endsWith('-' + slug)) return slug;
  }
  return null;
}

function buildContentHtml(text) {
  const paragraphs = text.split('\n\n').filter(p => p.trim().length > 0);
  return START_MARKER + '\n' + paragraphs.map(p =>
    '    <p style="margin:0 0 14px;color:#374151;line-height:1.7;font-size:0.9375rem;">' + p.trim() + '</p>'
  ).join('\n') + '\n    ' + END_MARKER;
}

if (DRY_RUN) console.log('=== DRY RUN MODE ===\n');

sites.forEach(({ dir, domain }) => {
  if (!fs.existsSync(dir)) {
    console.log('SKIP ' + domain + ' — dir not found');
    return;
  }

  const files = fs.readdirSync(dir).filter(f =>
    f.endsWith('.html') && f !== '404.html' && f !== 'service-template.html'
  );

  let injected = 0, replaced = 0, skipped = 0;

  files.forEach(file => {
    const city = detectCity(file);
    if (!city || !data[city]) { skipped++; return; }

    const filePath = path.join(dir, file);
    let c = fs.readFileSync(filePath, 'utf8');
    const newContent = buildContentHtml(data[city]);
    let done = false;

    // Strategy 1: Replace existing CITY-CONTENT-v2 block (with proper end marker)
    if (c.includes(START_MARKER) && c.includes(END_MARKER)) {
      const startIdx = c.indexOf(START_MARKER);
      const endIdx = c.indexOf(END_MARKER) + END_MARKER.length;
      c = c.substring(0, startIdx) + newContent + c.substring(endIdx);
      replaced++;
      done = true;
    }

    // Strategy 2: Replace CITY-CONTENT-v2 without end marker (from previous incomplete injection)
    if (!done && c.includes(START_MARKER)) {
      const startIdx = c.indexOf(START_MARKER);
      // Find next landmark: city-context paragraph or UNIQUE-CITY-CONTENT
      let endIdx = c.indexOf('<p class="city-context">', startIdx);
      if (endIdx === -1) endIdx = c.indexOf('<!-- UNIQUE-CITY-CONTENT', startIdx);
      if (endIdx === -1) {
        // Just replace the marker line itself, and inject before the next <p>
        const nextP = c.indexOf('<p', startIdx + START_MARKER.length);
        if (nextP !== -1) endIdx = nextP;
      }
      if (endIdx !== -1) {
        c = c.substring(0, startIdx) + newContent + '\n    ' + c.substring(endIdx);
        replaced++;
        done = true;
      }
    }

    // Strategy 3: Replace UNIQUE-CITY-CONTENT paragraph
    if (!done) {
      const ucStart = c.indexOf('<!-- UNIQUE-CITY-CONTENT -->');
      const ucEnd = c.indexOf('<!-- END-UNIQUE-CITY-CONTENT -->');
      if (ucStart !== -1 && ucEnd !== -1) {
        // Find the containing <p> tag
        const pStart = c.lastIndexOf('<p', ucStart);
        const pEnd = c.indexOf('</p>', ucEnd);
        if (pStart !== -1 && pEnd !== -1) {
          c = c.substring(0, pStart) + newContent + c.substring(pEnd + 4);
          injected++;
          done = true;
        }
      }
    }

    // Strategy 4: Replace <p class="city-context"> tag
    if (!done) {
      const ccMatch = c.match(/<p class="city-context"[^>]*>[\s\S]*?<\/p>/);
      if (ccMatch) {
        c = c.replace(ccMatch[0], newContent);
        injected++;
        done = true;
      }
    }

    // Strategy 5: Inject after H2 mentioning the city or service
    if (!done) {
      const h2Regex = /<h2[^>]*>[^<]*(?:Appliance Repair|Trusted|Local Service)[^<]*<\/h2>/i;
      const h2Match = c.match(h2Regex);
      if (h2Match) {
        const h2Idx = c.indexOf(h2Match[0]);
        const afterH2 = h2Idx + h2Match[0].length;
        const nextP = c.indexOf('<p', afterH2);
        if (nextP !== -1) {
          const nextPEnd = c.indexOf('</p>', nextP);
          if (nextPEnd !== -1) {
            c = c.substring(0, nextP) + newContent + c.substring(nextPEnd + 4);
            injected++;
            done = true;
          }
        }
      }
    }

    if (!done) { skipped++; return; }

    if (!DRY_RUN) {
      fs.writeFileSync(filePath, c, 'utf8');
    }
  });

  console.log('=== ' + domain + ' (' + files.length + ' pages) ===');
  console.log('  New injections:  ' + injected + ' pages');
  console.log('  Replaced:        ' + replaced + ' pages');
  console.log('  Skipped:         ' + skipped + ' pages');
  console.log('');
});

console.log(DRY_RUN ? 'DRY RUN — no files written.' : 'All injections applied.');
