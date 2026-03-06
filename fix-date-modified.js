/**
 * fix-date-modified.js — Replace hardcoded "2026-03-06" dateModified with real git dates
 * Also adds dateModified where missing (using git log date)
 * Usage: node fix-date-modified.js [--dry-run]
 */
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const DRY_RUN = process.argv.includes('--dry-run');

const sites = [
  { dir: 'C:/nappliancerepair', domain: 'nappliancerepair.com' },
  { dir: 'C:/appliancerepairneary', domain: 'appliancerepairneary.com' },
  { dir: 'C:/fixlifyservices', domain: 'fixlifyservices.com' },
];

if (DRY_RUN) console.log('=== DRY RUN MODE ===\n');

function getFileGitDate(filePath, dir) {
  const basename = path.basename(filePath);
  try {
    // Last commit date for this file
    const lastModified = execFileSync(
      'git', ['-C', dir, 'log', '-1', '--format=%ci', '--', basename],
      { encoding: 'utf8', timeout: 5000 }
    ).trim().slice(0, 10);

    // First commit date (published)
    const rawPublished = execFileSync(
      'git', ['-C', dir, 'log', '--diff-filter=A', '--format=%ci', '--', basename],
      { encoding: 'utf8', timeout: 5000 }
    ).trim();
    const lines = rawPublished.split('\n').filter(l => l.trim());
    const firstPublished = lines.length > 0 ? lines[lines.length - 1].slice(0, 10) : '';

    return {
      datePublished: firstPublished || lastModified || '2024-06-01',
      dateModified: lastModified || null,
    };
  } catch {
    return { datePublished: '2024-06-01', dateModified: null };
  }
}

function getPreBulkDate(dir, basename) {
  // Get all commit dates for this file, find last one that is NOT 2026-03-06
  try {
    const allDates = execFileSync(
      'git', ['-C', dir, 'log', '--format=%ci', '--', basename],
      { encoding: 'utf8', timeout: 10000 }
    ).trim().split('\n').map(d => d.trim().slice(0, 10)).filter(d => d.length === 10);
    // Find the first date that is not today's bulk date
    const preBulk = allDates.find(d => d !== '2026-03-06');
    return preBulk || null;
  } catch {
    return null;
  }
}

function getFallbackDate(filePath) {
  try {
    const stat = fs.statSync(filePath);
    return stat.mtime.toISOString().slice(0, 10);
  } catch {
    return '2026-01-01';
  }
}

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

  let fixedHardcoded = 0, addedMissing = 0, noGitDate = 0;
  const dateSamples = [];

  files.forEach(file => {
    const filePath = path.join(dir, file);
    let c = fs.readFileSync(filePath, 'utf8');
    let changed = false;

    const hasHardcoded = c.includes('"dateModified": "2026-03-06"');
    const hasMissing = c.includes('"datePublished"') && !c.includes('"dateModified"');

    if (!hasHardcoded && !hasMissing) return;

    const gitDates = getFileGitDate(filePath, dir);
    let finalDate = gitDates.dateModified || getFallbackDate(filePath);

    // If git date is 2026-03-06 (from bulk commits today),
    // find the most recent commit date before today's bulk runs
    if (finalDate === '2026-03-06') {
      const preBulk = getPreBulkDate(dir, file);
      if (preBulk) {
        finalDate = preBulk;
      } else {
        // No pre-bulk date — use datePublished if available, else fallback
        finalDate = gitDates.datePublished || getFallbackDate(filePath);
      }
    }

    // Collect samples for logging
    if (dateSamples.length < 5) {
      dateSamples.push(file + ' → ' + finalDate);
    }

    // Fix 1: Replace hardcoded 2026-03-06
    if (hasHardcoded) {
      c = c.replace('"dateModified": "2026-03-06"', '"dateModified": "' + finalDate + '"');
      changed = true;
      fixedHardcoded++;
    }

    // Fix 2: Add dateModified where missing (after datePublished)
    if (hasMissing) {
      const dpRegex = /("datePublished"\s*:\s*"[^"]*"),?\s*\n/;
      const dpMatch = c.match(dpRegex);
      if (dpMatch) {
        const matchStart = c.indexOf(dpMatch[0]);
        const lineStart = c.lastIndexOf('\n', matchStart) + 1;
        const indent = c.substring(lineStart, matchStart);

        const newBlock = dpMatch[1] + ',\n' + indent + '"dateModified": "' + finalDate + '",\n';
        c = c.substring(0, matchStart) + newBlock + c.substring(matchStart + dpMatch[0].length);
        changed = true;
        addedMissing++;
      }
    }

    if (!gitDates.dateModified) noGitDate++;

    if (changed && !DRY_RUN) {
      fs.writeFileSync(filePath, c, 'utf8');
    }
  });

  console.log('=== ' + domain + ' (' + files.length + ' pages) ===');
  console.log('  Hardcoded 2026-03-06 fixed: ' + fixedHardcoded + ' pages');
  console.log('  Missing dateModified added: ' + addedMissing + ' pages');
  if (noGitDate > 0) console.log('  Used fs.stat fallback:     ' + noGitDate + ' pages');
  if (dateSamples.length > 0) {
    console.log('  Sample dates:');
    dateSamples.forEach(s => console.log('    ' + s));
  }
  console.log('');
});

console.log(DRY_RUN ? 'DRY RUN — no files written.' : 'All fixes applied.');
