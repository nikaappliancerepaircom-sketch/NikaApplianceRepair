'use strict';
const fs = require('fs');
const path = require('path');

const SITES = [
  { key:'nika',    dir:'C:/NikaApplianceRepair', defaultOg:'https://nikaappliancerepair.com/assets/og-image.jpg' },
  { key:'nar',     dir:'C:/nappliancerepair',    defaultOg:'https://nappliancerepair.com/assets/og-image.jpg' },
  { key:'neary',   dir:'C:/appliancerepairneary',defaultOg:'https://appliancerepairneary.com/assets/og-image.jpg' },
  { key:'fixlify', dir:'C:/fixlifyservices',     defaultOg:'https://fixlifyservices.com/assets/og-image.jpg' },
];

const SKIP = new Set(['404.html','service-template.html']);
const SKIP_DIRS = new Set(['node_modules','.git','_queue','assets','css','js','images','reports','tools','backups','.playwright-mcp']);

const args = process.argv.slice(2);
const DRY_RUN = args.includes('--dry-run');

function walk(dir) {
  const out = [];
  let entries;
  try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch (e) { return out; }
  for (const e of entries) {
    if (e.isDirectory()) {
      if (!SKIP_DIRS.has(e.name)) out.push(...walk(path.join(dir, e.name)));
    } else if (
      e.name.endsWith('.html') &&
      !SKIP.has(e.name) &&
      !e.name.startsWith('landing-') &&
      !e.name.includes('.bak')
    ) {
      out.push(path.join(dir, e.name));
    }
  }
  return out;
}

function extractMeta(html, property) {
  const m =
    html.match(new RegExp('property="' + property + '"\s+content="([^"]*)"', 'i')) ||
    html.match(new RegExp('content="([^"]*)"\s+property="' + property + '"', 'i'));
  return m ? m[1] : '';
}

let totalFixed = 0;
let totalSkipped = 0;

for (const site of SITES) {
  if (!fs.existsSync(site.dir)) {
    console.log(site.key.toUpperCase() + ': directory not found, skipping');
    continue;
  }

  const files = walk(site.dir);
  let fixed = 0;
  let skipped = 0;

  for (const f of files) {
    let html;
    try { html = fs.readFileSync(f, 'utf8'); } catch (e) { continue; }

    if (html.includes('twitter:card')) { skipped++; continue; }
    if (!html.includes('</head>')) { continue; }

    const ogTitle = extractMeta(html, 'og:title');
    const ogDesc  = extractMeta(html, 'og:description');
    const ogImg   = extractMeta(html, 'og:image') || site.defaultOg;

    const lines = [
      '    <meta name="twitter:card" content="summary_large_image">',
    ];
    if (ogTitle) lines.push('    <meta name="twitter:title" content="' + ogTitle + '">');
    if (ogDesc)  lines.push('    <meta name="twitter:description" content="' + ogDesc + '">');
    lines.push('    <meta name="twitter:image" content="' + ogImg + '">');

    const twitterBlock = lines.join('\n');

    // Insert after last og: meta tag
    const ogMetaRe = /<meta\s[^>]*property="og:[^"]*"[^>]*>/gi;
    let lastMatch = null;
    let m;
    while ((m = ogMetaRe.exec(html)) !== null) lastMatch = m;

    let newHtml;
    if (lastMatch) {
      const insertPos = lastMatch.index + lastMatch[0].length;
      newHtml = html.slice(0, insertPos) + '\n' + twitterBlock + html.slice(insertPos);
    } else {
      newHtml = html.replace('</head>', twitterBlock + '\n</head>');
    }

    if (newHtml === html) continue;

    if (!DRY_RUN) fs.writeFileSync(f, newHtml, 'utf8');
    fixed++;
  }

  console.log(site.key.toUpperCase() + ': ' + fixed + ' pages updated, ' + skipped + ' already had twitter:card' + (DRY_RUN ? ' [DRY RUN]' : ''));
  totalFixed += fixed;
  totalSkipped += skipped;
}

console.log('\nTOTAL: ' + totalFixed + ' pages updated, ' + totalSkipped + ' already had twitter:card' + (DRY_RUN ? ' [DRY RUN]' : ''));
