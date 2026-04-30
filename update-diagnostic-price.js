/**
 * Update diagnostic fee: $65 → $89 (waived with repair)
 * Runs across all 4 sites
 */
const fs = require('fs');
const path = require('path');

const SITES = [
  'C:/NikaApplianceRepair',
  'C:/nappliancerepair',
  'C:/appliancerepairneary',
  'C:/fixlifyservices',
];

// Ordered replacements — more specific first to avoid double-replacing
const REPLACEMENTS = [
  // Already has "waived" language — just change number
  [/\$65 diagnostic fee, waived when you proceed with the repair/g, '$89 diagnostic fee, waived when you proceed with the repair'],
  [/\$65 diagnostic fee is waived if you approve the repair/g, '$89 diagnostic fee is waived if you approve the repair'],
  [/\$65 diagnostic fee is waived if you proceed with repair/g, '$89 diagnostic fee is waived if you proceed with repair'],
  [/flat \$65 diagnostic fee is waived when/g, 'flat $89 diagnostic fee is waived when'],
  // Bullet points that have waived inline
  [/\$65 diagnostic waived with repair/g, '$89 diagnostic — waived with repair'],
  [/\$65 diagnostic fee is waived/g, '$89 diagnostic fee is waived'],
  // All remaining $65 diagnostic → $89 with waived note
  [/\$65 diagnostic fee/g, '$89 diagnostic fee (waived with repair)'],
  [/\$65 diagnostic/g, '$89 diagnostic — waived with repair'],
];

function processFile(filePath) {
  let content = fs.readFileSync(filePath, 'utf8');
  const original = content;

  for (const [pattern, replacement] of REPLACEMENTS) {
    content = content.replace(pattern, replacement);
  }

  if (content !== original) {
    fs.writeFileSync(filePath, content, 'utf8');
    return true;
  }
  return false;
}

function walkHtml(dir, excludeDirs = ['backups', 'backup', 'node_modules', '.git']) {
  const results = [];
  if (!fs.existsSync(dir)) return results;
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.isDirectory()) {
      if (!excludeDirs.includes(entry.name)) {
        results.push(...walkHtml(path.join(dir, entry.name), excludeDirs));
      }
    } else if (entry.name.endsWith('.html')) {
      results.push(path.join(dir, entry.name));
    }
  }
  return results;
}

let totalUpdated = 0;
let totalSkipped = 0;

for (const site of SITES) {
  const files = walkHtml(site);
  let siteUpdated = 0;
  for (const f of files) {
    if (processFile(f)) siteUpdated++;
    else totalSkipped++;
  }
  console.log(`${site}: ${siteUpdated}/${files.length} files updated`);
  totalUpdated += siteUpdated;
}

console.log(`\nDone. Total updated: ${totalUpdated}`);
