/**
 * add-year-meta.js — Add current year to meta description if missing
 * Fixes: meta_desc_or_title_includes_year (seo_advanced)
 */
const fs = require('fs');
const path = require('path');

const YEAR = '2026';
const SKIP_DIRS = new Set(['node_modules','.git','_queue','assets','css','js','images','fonts','components','templates','styles','backups','backup','old','archive','reports','tools','compare','preview','_drafts']);

const SITES = [
  'C:/NikaApplianceRepair',
  'C:/nappliancerepair',
  'C:/appliancerepairneary',
  'C:/fixlifyservices',
];

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

for (const dir of SITES) {
  let fixed = 0;
  const files = walk(dir);

  for (const fp of files) {
    let html = fs.readFileSync(fp, 'utf8');

    // Skip if year already in title or meta desc
    const titleMatch = html.match(/<title>([^<]+)<\/title>/);
    const metaDescMatch = html.match(/<meta\s+name="description"\s+content="([^"]+)"/i);

    if (!titleMatch && !metaDescMatch) continue;

    const titleHasYear = titleMatch && titleMatch[1].includes(YEAR);
    const metaHasYear = metaDescMatch && metaDescMatch[1].includes(YEAR);

    if (titleHasYear || metaHasYear) continue;

    // Add year to meta description (append before closing quote)
    if (metaDescMatch) {
      const currentDesc = metaDescMatch[1];
      if (currentDesc.length < 140) {
        const newDesc = currentDesc.replace(/\.$/, '') + ` Updated ${YEAR}.`;
        const newHtml = html.replace(metaDescMatch[0], metaDescMatch[0].replace(currentDesc, newDesc));
        if (newHtml !== html) {
          fs.writeFileSync(fp, newHtml, 'utf8');
          fixed++;
          continue;
        }
      }
    }

    // Fallback: add year to title if meta is too long
    if (titleMatch && !titleHasYear) {
      const currentTitle = titleMatch[1];
      // Insert year before last pipe or at end
      const newTitle = currentTitle.includes('|')
        ? currentTitle.replace(/\s*\|\s*([^|]+)$/, ` | $1 ${YEAR}`)
        : currentTitle + ` ${YEAR}`;
      if (newTitle !== currentTitle) {
        const newHtml = html.replace(`<title>${currentTitle}</title>`, `<title>${newTitle}</title>`);
        fs.writeFileSync(fp, newHtml, 'utf8');
        fixed++;
      }
    }
  }

  console.log(`${path.basename(dir)}: ${fixed} pages updated with ${YEAR}`);
  totalFixed += fixed;
}

console.log(`\nTotal: ${totalFixed} pages`);
