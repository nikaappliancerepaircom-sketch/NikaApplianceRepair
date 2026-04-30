const fs = require('fs');
const path = require('path');

const pkg = path.join(process.env.LOCALAPPDATA, 'Packages', '5319275A.WhatsAppDesktop_cv1g1gvanyjgm');
const base = path.join(pkg, 'LocalCache', 'EBWebView', 'Default');

function dirSize(dir) {
  let total = 0;
  try {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      try {
        if (entry.isDirectory()) total += dirSize(full);
        else total += fs.statSync(full).size;
      } catch {}
    }
  } catch {}
  return total;
}

function clearDir(dir) {
  if (!fs.existsSync(dir)) return 0;
  let freed = 0;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    try {
      const before = entry.isDirectory() ? dirSize(full) : fs.statSync(full).size;
      fs.rmSync(full, { recursive: true, force: true });
      freed += before;
    } catch (e) {
      console.log(`  skip: ${entry.name} (${e.code})`);
    }
  }
  return freed;
}

const before = dirSize(pkg);
const targets = [
  path.join(base, 'Cache'),
  path.join(base, 'Code Cache'),
  path.join(base, 'Service Worker', 'CacheStorage'),
  path.join(base, 'Service Worker', 'ScriptCache'),
  path.join(base, 'GPUCache'),
];

let freed = 0;
for (const t of targets) {
  console.log(`Clearing: ${t.replace(pkg, '')}`);
  freed += clearDir(t);
}

const after = dirSize(pkg);
const mb = (b) => (b / 1024 / 1024).toFixed(1);
console.log(`\nBefore: ${mb(before)} MB | After: ${mb(after)} MB | Freed: ${mb(before - after)} MB`);
