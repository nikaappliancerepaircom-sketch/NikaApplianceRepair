#!/usr/bin/env node
/**
 * fix-diagnostic-fee.js
 *
 * Replaces $80 → $65 ONLY in diagnostic fee contexts across all 3 satellite sites.
 * Does NOT touch repair price ranges like "$80–$350" or generic repair costs.
 *
 * Usage:
 *   node fix-diagnostic-fee.js --dry-run   # preview changes
 *   node fix-diagnostic-fee.js             # apply changes
 */

const fs = require('fs');
const path = require('path');
const glob = require('child_process');

const DRY_RUN = process.argv.includes('--dry-run');

const SITES = [
  'C:/nappliancerepair',
  'C:/appliancerepairneary',
  'C:/fixlifyservices',
];

// Collect all .html files recursively
function getHtmlFiles(dir) {
  const results = [];
  function walk(d) {
    for (const entry of fs.readdirSync(d, { withFileTypes: true })) {
      const full = path.join(d, entry.name);
      if (entry.isDirectory() && entry.name !== 'node_modules' && entry.name !== '.git' && entry.name !== '.vercel') {
        walk(full);
      } else if (entry.isFile() && entry.name.endsWith('.html')) {
        results.push(full);
      }
    }
  }
  walk(dir);
  return results;
}

// ── Replacement rules ────────────────────────────────────────────────
// Each rule: [regex, replacement, description]
// Order matters — more specific patterns first.

const rules = [
  // 1. "an $80 diagnostic" / "an $80 CAD diagnostic" → grammar fix: "a $65 ..."
  [/\ban \$80\b(\s+(?:CAD\s+)?diagnostic)/gi,   'a $65$1',   'an $80 diagnostic → a $65 diagnostic (grammar)'],

  // 2. "an $80 diagnostic fee" (standalone)
  [/\ban \$80\b(\s+diagnostic\s+fee)/gi,         'a $65$1',   'an $80 diagnostic fee → a $65 diagnostic fee'],

  // 3. "$80 diagnostic fee" (not preceded by "an ")
  [/\$80(\s+diagnostic\s+fee)/gi,                '$65$1',     '$80 diagnostic fee → $65 diagnostic fee'],

  // 4. "$80 diagnostic" (general — not part of a range)
  [/\$80(\s+diagnostic)/gi,                      '$65$1',     '$80 diagnostic → $65 diagnostic'],

  // 5. "$80 diagnosis"
  [/\$80(\s+diagnosis)/gi,                       '$65$1',     '$80 diagnosis → $65 diagnosis'],

  // 6. "$80 flat fee" / "$80 flat-rate"
  [/\$80(\s+flat[ -](?:fee|rate))/gi,            '$65$1',     '$80 flat fee → $65 flat fee'],

  // 7. "$80 service call"
  [/\$80(\s+service\s+call)/gi,                  '$65$1',     '$80 service call → $65 service call'],

  // 8. "$80 inspection"
  [/\$80(\s+inspection)/gi,                      '$65$1',     '$80 inspection → $65 inspection'],

  // 9. "Diagnostic fee ($80)" / "diagnostic fee ($80)"
  [/((?:D|d)iagnostic\s+fee\s*)\(\$80\)/g,       '$1($65)',   'Diagnostic fee ($80) → ($65)'],

  // 10. "($80) waived" / "($80) is waived" / "($80) is credited"
  [/\(\$80\)(\s+(?:is\s+)?(?:waived|credited|applied))/gi, '($65)$1', '($80) waived → ($65) waived'],

  // 11. Standalone <td>$80</td> — these are always diagnostic visit rows
  //     (verified: always preceded by "Diagnostic visit (waived with repair)")
  [/(<td>)\$80(<\/td>)/g,                        '$1$65$2',   '<td>$80</td> → <td>$65</td>'],

  // 12. "Diagnostics from $80" / "Diagnostics start at $80"
  [/((?:D|d)iagnostics?\s+(?:from|start(?:s|ing)?\s+at))\s+\$80/g,
    '$1 $65', 'Diagnostics from/start at $80 → $65'],

  // 13. "diagnostic visits start at $80"
  [/(diagnostic\s+visits?\s+start(?:s|ing)?\s+at)\s+\$80/gi,
    '$1 $65', 'diagnostic visits start at $80 → $65'],

  // 14. "$80–$100 diagnostic" / "$80-$100 diagnostic" — diagnostic fee range
  [/\$80([–—-])\$100(\s+(?:diagnostic|fee))/gi,  '$65$1$100$2', '$80–$100 diagnostic → $65–$100'],

  // 15. "Diagnostic fee: $80–$100" / "Diagnostic fee:</strong> $80–$100"
  [/((?:D|d)iagnostic\s+(?:fee|visit)(?:<\/strong>)?:\s*(?:<\/strong>\s*)?)\$80([–—-])\$100/g,
    '$1$65$2$100', 'Diagnostic fee: $80–$100 → $65–$100'],

  // 16. "Diagnostic fee is $80–$100"
  [/((?:D|d)iagnostic\s+(?:fee|visit)s?\s+is\s+)\$80([–—-])\$100/g,
    '$1$65$2$100', 'Diagnostic fee is $80–$100 → $65–$100'],

  // 17. "Diagnostic visits start at $80–$100" (shouldn't exist but just in case)

  // 18. "The $80–$100 diagnostic fee"
  [/(The\s+)\$80([–—-])\$100(\s+diagnostic\s+fee)/gi,
    '$1$65$2$100$3', 'The $80–$100 diagnostic fee → $65–$100'],

  // 19. "$80-$100) is credited" / "$80–$100) is waived" etc.
  // These are "(diagnostic fee is $80–$100 and is credited..." patterns already caught above

  // 20. "diagnostic fee ($80-$100)" / "diagnostic fee ($80–$100)"
  [/(diagnostic\s+fee\s*)\(\$80([–—-])\$100\)/gi,
    '$1($65$2$100)', 'diagnostic fee ($80–$100) → ($65–$100)'],

  // 21. In JSON-LD "text" fields: "charges an $80" → "charges a $65"
  [/(charges?\s+)an\s+\$80/gi,                   '$1a $65',   'charges an $80 → charges a $65'],

  // 22. "is an $80" in diagnostic context (e.g. "there is an $80 CAD diagnostic fee")
  [/(is\s+)an\s+\$80(\s+(?:CAD\s+)?diagnostic)/gi, '$1a $65$2', 'is an $80 diagnostic → is a $65 diagnostic'],
];

// ── Main ─────────────────────────────────────────────────────────────

let totalFiles = 0;
let totalChanges = 0;
const changedFiles = [];

for (const site of SITES) {
  const siteName = path.basename(site);
  const files = getHtmlFiles(site);
  console.log(`\n${'═'.repeat(60)}`);
  console.log(`Site: ${siteName} (${files.length} HTML files)`);
  console.log('═'.repeat(60));

  let siteChanges = 0;

  for (const file of files) {
    const original = fs.readFileSync(file, 'utf8');
    let content = original;
    const fileChanges = [];

    for (const [regex, replacement, desc] of rules) {
      // Reset lastIndex for global regexes
      regex.lastIndex = 0;
      const matches = content.match(regex);
      if (matches && matches.length > 0) {
        fileChanges.push({ desc, count: matches.length });
        content = content.replace(regex, replacement);
      }
    }

    if (content !== original) {
      const rel = path.relative(site, file).replace(/\\/g, '/');
      const changeCount = fileChanges.reduce((s, c) => s + c.count, 0);
      console.log(`  ${DRY_RUN ? '[DRY-RUN] ' : ''}${rel} — ${changeCount} replacement(s)`);
      for (const ch of fileChanges) {
        console.log(`    • ${ch.desc} (×${ch.count})`);
      }
      siteChanges += changeCount;
      changedFiles.push(file);

      if (!DRY_RUN) {
        fs.writeFileSync(file, content, 'utf8');
      }
    }

    totalFiles++;
  }

  console.log(`  → ${siteName}: ${siteChanges} total replacement(s)${DRY_RUN ? ' (dry run)' : ''}`);
  totalChanges += siteChanges;
}

console.log(`\n${'═'.repeat(60)}`);
console.log(`TOTAL: ${totalChanges} replacements across ${changedFiles.length} files${DRY_RUN ? ' (DRY RUN — no files written)' : ' (APPLIED)'}`);
console.log('═'.repeat(60));
