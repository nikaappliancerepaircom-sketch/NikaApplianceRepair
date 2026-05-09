/**
 * add-howto-schema.js — Add HowTo schema to pages with ordered lists
 * Targets pages with <ol> that have 3+ <li> items but no HowTo in JSON-LD
 */
const fs = require('fs');
const path = require('path');

const SITES = [
  'C:/NikaApplianceRepair',
  'C:/nappliancerepair',
  'C:/appliancerepairneary',
  'C:/fixlifyservices',
];

const SKIP_DIRS = new Set(['node_modules','.git','_queue','assets','css','js','images','fonts','components','templates','styles','backups','backup','old','archive','reports','tools','compare','preview','_drafts']);
const MARKER = '"@type": "HowTo"';

function walk(dir) {
  const out = [];
  let items;
  try { items = fs.readdirSync(dir, { withFileTypes: true }); } catch { return out; }
  for (const item of items) {
    if (item.isDirectory()) {
      if (SKIP_DIRS.has(item.name)) continue;
      out.push(...walk(path.join(dir, item.name)));
    } else if (item.name.endsWith('.html') && !item.name.includes('.bak')) {
      out.push(path.join(dir, item.name));
    }
  }
  return out;
}

function extractOlItems(html) {
  const results = [];
  const olRegex = /<ol[^>]*>([\s\S]*?)<\/ol>/gi;
  let olMatch;
  while ((olMatch = olRegex.exec(html)) !== null) {
    const olContent = olMatch[1];
    const liRegex = /<li[^>]*>([\s\S]*?)<\/li>/gi;
    const items = [];
    let liMatch;
    while ((liMatch = liRegex.exec(olContent)) !== null) {
      const text = liMatch[1].replace(/<[^>]+>/g, '').trim().slice(0, 120);
      if (text.length > 5) items.push(text);
    }
    if (items.length >= 3) {
      results.push(items.slice(0, 8)); // max 8 steps
    }
  }
  return results;
}

function getTitle(html) {
  const m = html.match(/<title>([^<]+)<\/title>/);
  return m ? m[1].replace(/\s*\|[^|]*$/, '').trim() : 'Appliance Repair Guide';
}

function getDesc(html) {
  const m = html.match(/<meta\s+name="description"\s+content="([^"]+)"/i);
  return m ? m[1].slice(0, 200) : '';
}

function getImage(html) {
  const m = html.match(/<meta\s+property="og:image"\s+content="([^"]+)"/i);
  return m ? m[1] : '';
}

let totalFixed = 0;

for (const dir of SITES) {
  let fixed = 0;
  const files = walk(dir);

  for (const fp of files) {
    let html = fs.readFileSync(fp, 'utf8');

    // Skip if already has HowTo
    if (html.includes(MARKER)) continue;

    const olSets = extractOlItems(html);
    if (olSets.length === 0) continue;

    // Use the first OL with 3+ steps
    const steps = olSets[0];
    const title = getTitle(html);
    const desc = getDesc(html);
    const image = getImage(html);

    const stepsJson = steps.map((step, i) => ({
      '@type': 'HowToStep',
      'position': i + 1,
      'name': step.slice(0, 80),
      'text': step,
    }));

    const howToSchema = {
      '@context': 'https://schema.org',
      '@type': 'HowTo',
      'name': title,
      'description': desc,
      ...(image ? { 'image': image } : {}),
      'step': stepsJson,
    };

    const schemaTag = `<script type="application/ld+json">\n${JSON.stringify(howToSchema, null, 2)}\n</script>`;

    // Inject before </head>
    if (html.includes('</head>')) {
      html = html.replace('</head>', `${schemaTag}\n</head>`);
      fs.writeFileSync(fp, html, 'utf8');
      fixed++;
      totalFixed++;
    }
  }

  console.log(`${path.basename(dir)}: ${fixed} pages with HowTo schema added`);
}

console.log(`\nTotal: ${totalFixed} pages`);
