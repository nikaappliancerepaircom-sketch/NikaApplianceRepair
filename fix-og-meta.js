/**
 * fix-og-meta.js — Fix og:site_name + add dateModified to JSON-LD
 */
const fs = require('fs');
const path = require('path');

const SITES = [
  { dir: 'C:/NikaApplianceRepair', name: 'NIKA', siteName: 'Nika Appliance Repair' },
  { dir: 'C:/nappliancerepair', name: 'NAR', siteName: "Nick's Appliance Repair" },
  { dir: 'C:/appliancerepairneary', name: 'NEARY', siteName: 'Appliance Repair Near Me' },
  { dir: 'C:/fixlifyservices', name: 'FIXLIFY', siteName: 'Fixlify Appliance Services' },
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

function getMtime(fp) {
  try { return fs.statSync(fp).mtime.toISOString().slice(0, 10); } catch { return new Date().toISOString().slice(0, 10); }
}

let totalOgFixed = 0;
let totalDateFixed = 0;

for (const site of SITES) {
  let ogFixed = 0, dateFixed = 0;
  const files = walk(site.dir);

  for (const fp of files) {
    let html = fs.readFileSync(fp, 'utf8');
    let changed = false;

    // Fix og:site_name — add if missing
    if (!html.includes('og:site_name')) {
      // Insert after og:type or og:title
      const ogInsertMatch = html.match(/<meta property="og:(type|title)"[^>]*>/i);
      if (ogInsertMatch) {
        const idx = html.indexOf(ogInsertMatch[0]) + ogInsertMatch[0].length;
        html = html.slice(0, idx) +
               `\n    <meta property="og:site_name" content="${site.siteName}">` +
               html.slice(idx);
        ogFixed++;
        changed = true;
      }
    } else if (html.includes('og:site_name" content=""')) {
      html = html.replace(/og:site_name" content=""/, `og:site_name" content="${site.siteName}"`);
      ogFixed++;
      changed = true;
    }

    // Add dateModified to JSON-LD blocks that have @type: LocalBusiness or Service
    if (!html.includes('"dateModified"') && !html.includes('"datePublished"')) {
      const mtime = getMtime(fp);
      // Find JSON-LD blocks with LocalBusiness/Service/FAQPage
      html = html.replace(
        /(<script type="application\/ld\+json">\s*\{)([\s\S]*?)(\}\s*<\/script>)/g,
        (match, open, body, close) => {
          if (!body.includes('"@type"')) return match;
          // Add dateModified before closing brace
          const newBody = body.trimEnd();
          const hasTrailingComma = newBody.endsWith(',');
          const separator = hasTrailingComma ? '' : ',';
          dateFixed++;
          changed = true;
          return `${open}${body}${hasTrailingComma ? '' : ','}
  "dateModified": "${mtime}"
${close}`;
        }
      );
    }

    if (changed) {
      fs.writeFileSync(fp, html, 'utf8');
    }
  }

  console.log(`${site.name}: og:site_name ${ogFixed} pages, dateModified ${dateFixed} blocks`);
  totalOgFixed += ogFixed;
  totalDateFixed += dateFixed;
}

console.log(`\nTotal: og:site_name ${totalOgFixed} pages, dateModified ${totalDateFixed} blocks`);
