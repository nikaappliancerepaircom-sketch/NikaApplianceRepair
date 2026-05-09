/**
 * fix-schema-email.js — Add email to LocalBusiness JSON-LD if missing
 */
const fs = require('fs');
const path = require('path');

const SITES = [
  { dir: 'C:/NikaApplianceRepair', email: 'info@nikaappliancerepair.com' },
  { dir: 'C:/nappliancerepair', email: 'info@nappliancerepair.com' },
  { dir: 'C:/appliancerepairneary', email: 'info@appliancerepairneary.com' },
  { dir: 'C:/fixlifyservices', email: 'info@fixlifyservices.com' },
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

for (const site of SITES) {
  let fixed = 0;
  const files = walk(site.dir);

  for (const fp of files) {
    let html = fs.readFileSync(fp, 'utf8');

    // Skip if email already in page
    if (html.includes(site.email)) { continue; }

    // Find LocalBusiness JSON-LD and add email after telephone
    const newHtml = html.replace(
      /("telephone"\s*:\s*"[^"]+")(\s*,)?/,
      (match, tel, comma) => {
        fixed++;
        return `${tel},\n  "email": "${site.email}"${comma || ''}`;
      }
    );

    if (newHtml !== html) {
      fs.writeFileSync(fp, newHtml, 'utf8');
    }
  }

  console.log(`${path.basename(site.dir)}: ${fixed} pages updated with email`);
  totalFixed += fixed;
}

console.log(`\nTotal: ${totalFixed} pages`);
