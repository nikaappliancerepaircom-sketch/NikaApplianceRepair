/**
 * add-main-landmark.js — Add <main> landmark to pages missing it
 * Injects <main id="main-content" role="main"> after header block,
 * closes </main> before footer-placeholder div.
 */
const fs = require('fs');
const path = require('path');

const SITES = [
  { dir: 'C:/NikaApplianceRepair', name: 'NIKA', brand: 'Nika Appliance Repair' },
  { dir: 'C:/nappliancerepair', name: 'NAR', brand: "Nick's Appliance Repair" },
  { dir: 'C:/appliancerepairneary', name: 'NEARY', brand: 'Appliance Repair Near Me' },
  { dir: 'C:/fixlifyservices', name: 'FIXLIFY', brand: 'Fixlify Appliance Services' },
];

const SKIP_DIRS = new Set(['node_modules','.git','_queue','assets','css','js','images','fonts','components','templates','styles','backups','backup','old','archive','reports','tools','compare','preview','_drafts']);

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

let totalFixed = 0;
let totalSkipped = 0;

for (const site of SITES) {
  let siteFixed = 0;
  const files = walk(site.dir);

  for (const fp of files) {
    let html = fs.readFileSync(fp, 'utf8');

    // Skip if already has <main
    if (/<main[\s>]/i.test(html)) { totalSkipped++; continue; }

    // Find insertion point for opening <main>:
    // After header-placeholder div + optional header-loader script
    // Pattern: after </div> that contains "header-placeholder", then skip optional <script> tags
    let insertOpen = -1;

    // Try: after header-loader script
    const headerLoaderMatch = html.match(/(<script[^>]*header-loader[^>]*>(?:<\/script>)?)/i);
    if (headerLoaderMatch) {
      const idx = html.indexOf(headerLoaderMatch[0]);
      insertOpen = idx + headerLoaderMatch[0].length;
    } else {
      // Try: after header-placeholder div closing tag
      const hpMatch = html.match(/<div[^>]*id=["']header-placeholder["'][^>]*>\s*<\/div>/i);
      if (hpMatch) {
        insertOpen = html.indexOf(hpMatch[0]) + hpMatch[0].length;
      } else {
        // Try: after <body> tag itself
        const bodyMatch = html.match(/<body[^>]*>/i);
        if (bodyMatch) {
          insertOpen = html.indexOf(bodyMatch[0]) + bodyMatch[0].length;
        }
      }
    }

    // Find insertion point for closing </main>: before footer-placeholder
    const footerIdx = html.indexOf('<div id="footer-placeholder"');
    if (footerIdx === -1) { totalSkipped++; continue; }

    if (insertOpen === -1 || insertOpen >= footerIdx) { totalSkipped++; continue; }

    // Insert
    html = html.slice(0, insertOpen) +
           '\n<main id="main-content" role="main">' +
           html.slice(insertOpen, footerIdx) +
           '</main>\n' +
           html.slice(footerIdx);

    fs.writeFileSync(fp, html, 'utf8');
    siteFixed++;
    totalFixed++;
  }

  console.log(`${site.name}: ${siteFixed} pages updated with <main> landmark`);
}

console.log(`\nTotal: ${totalFixed} fixed, ${totalSkipped} skipped (already had <main>)`);
