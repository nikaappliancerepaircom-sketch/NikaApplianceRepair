const fs = require('fs');
const path = require('path');
const DIRS = ['C:/NikaApplianceRepair','C:/nappliancerepair','C:/appliancerepairneary','C:/fixlifyservices'];
const SKIP = new Set(['node_modules','.git','_queue','assets','css','js','images','fonts','components','templates','styles','backups','backup','old','archive','reports','tools','compare','preview','_drafts']);

let total = 0;
function walk(d) {
  let items; try { items = fs.readdirSync(d,{withFileTypes:true}); } catch { return; }
  for (const item of items) {
    if (item.isDirectory()) { if (!SKIP.has(item.name)) walk(path.join(d,item.name)); }
    else if (item.name.endsWith('.html') && !item.name.includes('.bak')) {
      const fp = path.join(d, item.name);
      let html = fs.readFileSync(fp,'utf8');
      if (!html.includes('VOICE-QA-v1')) continue;
      if (html.includes('class="summary"')) continue;
      // Add class="summary" to first <section inside VOICE-QA block
      const marker = '<!-- VOICE-QA-v1 -->';
      const idx = html.indexOf(marker);
      if (idx === -1) continue;
      const afterMarker = html.indexOf('<section ', idx);
      if (afterMarker === -1) continue;
      html = html.slice(0, afterMarker + 8) + 'class="summary" ' + html.slice(afterMarker + 8);
      fs.writeFileSync(fp, html, 'utf8');
      total++;
    }
  }
}

for (const dir of DIRS) walk(dir);
console.log('Total updated:', total);
