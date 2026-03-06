const fs = require('fs');
const path = require('path');

const ROOT = 'C:/NikaApplianceRepair';
const DOMAIN = 'https://nikaappliancerepair.com';
const OG_IMAGE = DOMAIN + '/og-image.jpg';
const KEEP_NOINDEX = new Set(['404.html']);
const FOLDERS = [ROOT, path.join(ROOT, '_pages_queue')];

let totalFiles = 0, totalFixed = 0;
const changes = [];

function getCanonicalUrl(filename) {
  if (filename === 'index.html') return DOMAIN + '/';
  return DOMAIN + '/' + filename.replace(/\.html$/, '');
}

function getMeta(html, name) {
  const b1 = html.match(new RegExp('<meta\\s+name=["\']' + name + '["\'][^>]*content=["\']([^"\']+)["\']', 'i'));
  const b2 = html.match(new RegExp('<meta\\s+content=["\']([^"\']+)["\'][^>]*name=["\']' + name + '["\']', 'i'));
  const m = b1 || b2;
  return m ? m[1] : null;
}

function getOg(html, prop) {
  const b1 = html.match(new RegExp('<meta\\s+property=["\']' + prop + '["\'][^>]*content=["\']([^"\']+)["\']', 'i'));
  const b2 = html.match(new RegExp('<meta\\s+content=["\']([^"\']+)["\'][^>]*property=["\']' + prop + '["\']', 'i'));
  const m = b1 || b2;
  return m ? m[1] : null;
}

function getTitle(html) {
  const m = html.match(/<title[^>]*>([^<]+)<\/title>/i);
  return m ? m[1].trim() : null;
}

// FIX 1: Canonical tag
function fixCanonical(html, filename, fc) {
  const expected = getCanonicalUrl(filename);
  const existing = html.match(/<link\s[^>]*rel=["']canonical["'][^>]*>/i);
  if (!existing) {
    const cm = html.match(/(<meta\s[^>]*charset[^>]*>)/i);
    const tag = '<link rel="canonical" href="' + expected + '">';
    if (cm) {
      html = html.replace(cm[0], cm[0] + '\n    ' + tag);
    } else {
      html = html.replace(/<head>/i, '<head>\n    ' + tag);
    }
    fc.push('  + Added canonical: ' + expected);
  } else {
    const hm = existing[0].match(/href=["']([^"']+)["']/i);
    const cur = hm ? hm[1] : '';
    if (cur !== expected) {
      const fixed = existing[0].replace(/href=["'][^"']*["']/i, 'href="' + expected + '"');
      html = html.replace(existing[0], fixed);
      fc.push('  ~ Fixed canonical: ' + cur + ' to ' + expected);
    }
  }
  return html;
}

// FIX 2: OG tags
function fixOgTags(html, filename, fc) {
  const canonical = getCanonicalUrl(filename);
  const title = getTitle(html);
  const desc = getMeta(html, 'description');
  const ogTitle = getOg(html, 'og:title');
  const ogDesc = getOg(html, 'og:description');
  const ogUrl = getOg(html, 'og:url');
  const ogType = getOg(html, 'og:type');
  const ogImage = getOg(html, 'og:image');

  // Fix og:url if wrong domain OR doesn't match canonical (e.g. has .html extension)
  if (ogUrl && ogUrl !== canonical) {
    const r1 = /(property=["']og:url["'][^>]*content=["'])([^"']+)(["'])/i;
    const r2 = /(content=["'])([^"']+)(["'][^>]*property=["']og:url["'])/i;
    if (r1.test(html)) html = html.replace(r1, '$1' + canonical + '$3');
    else html = html.replace(r2, '$1' + canonical + '$3');
    fc.push('  ~ Fixed og:url: ' + ogUrl + ' to ' + canonical);
  }

  const tagsToAdd = [];
  if (!ogType) {
    tagsToAdd.push('<meta property="og:type" content="website">');
    fc.push('  + Added og:type=website');
  }
  if (!ogTitle && title) {
    tagsToAdd.push('<meta property="og:title" content="' + title.replace(/"/g, '&quot;') + '">');
    fc.push('  + Added og:title');
  }
  if (!ogDesc && desc) {
    tagsToAdd.push('<meta property="og:description" content="' + desc.replace(/"/g, '&quot;') + '">');
    fc.push('  + Added og:description');
  }
  if (!ogUrl) {
    tagsToAdd.push('<meta property="og:url" content="' + canonical + '">');
    fc.push('  + Added og:url: ' + canonical);
  }
  if (!ogImage) {
    tagsToAdd.push('<meta property="og:image" content="' + OG_IMAGE + '">');
    fc.push('  + Added og:image');
  }

  if (tagsToAdd.length === 0) return html;
  const newTags = tagsToAdd.join('\n    ');

  // Find last og: meta for insertion point
  const ogRe = /<meta\s+(?:property=["']og:[^"']+["'][^>]*|content=["'][^"']*["'][^>]*property=["']og:[^"']+["'][^>]*)>/gi;
  let om, lastOgTag = null;
  while ((om = ogRe.exec(html)) !== null) lastOgTag = om[0];

  if (lastOgTag) {
    const ip = html.lastIndexOf(lastOgTag) + lastOgTag.length;
    html = html.slice(0, ip) + '\n    ' + newTags + html.slice(ip);
  } else {
    const cm = html.match(/<link\s[^>]*rel=["']canonical["'][^>]*>/i);
    if (cm) {
      const ip = html.indexOf(cm[0]) + cm[0].length;
      html = html.slice(0, ip) + '\n    ' + newTags + html.slice(ip);
    } else {
      const ch = html.match(/<meta\s[^>]*charset[^>]*>/i);
      if (ch) {
        const ip = html.indexOf(ch[0]) + ch[0].length;
        html = html.slice(0, ip) + '\n    ' + newTags + html.slice(ip);
      }
    }
  }
  return html;
}

// FIX 3: robots - remove noindex
function fixRobots(html, filename, fc) {
  if (KEEP_NOINDEX.has(filename)) return html;
  const re = /<meta\s+name=["']robots["'][^>]*content=["']([^"']+)["'][^>]*>/gi;
  let m;
  const hits = [];
  while ((m = re.exec(html)) !== null) {
    if (/noindex/i.test(m[1])) hits.push({ tag: m[0], content: m[1] });
  }
  for (const h of hits) {
    let nc = h.content
      .replace(/,?\s*noindex/gi, '')
      .replace(/noindex\s*,?\s*/gi, '')
      .trim()
      .replace(/^,\s*/, '')
      .replace(/\s*,$/, '');
    if (!nc) nc = 'index, follow';
    const ft = h.tag.replace(/content=["'][^"']+["']/i, 'content="' + nc + '"');
    html = html.replace(h.tag, ft);
    fc.push('  ~ Removed noindex: "' + h.content + '" to "' + nc + '"');
  }
  return html;
}

// FIX 4: Schema.org wrong domains in JSON-LD
function fixSchemaUrls(html, filename, fc) {
  const wrong = [
    /https?:\/\/nappliancerepair\.com/g,
    /https?:\/\/appliancerepairneary\.com/g,
    /https?:\/\/fixlifyservices\.com/g,
    /https?:\/\/www\.nikaappliancerepair\.com/g,
  ];
  const sRe = /(<script\s+type=["']application\/ld\+json["'][^>]*>)([\s\S]*?)(<\/script>)/gi;
  let changed = false;
  const result = html.replace(sRe, function(full, open, json, close) {
    let j = json;
    for (const p of wrong) {
      if (p.test(j)) { j = j.replace(p, DOMAIN); changed = true; }
      p.lastIndex = 0;
    }
    return open + j + close;
  });
  if (changed) fc.push('  ~ Fixed wrong domain in JSON-LD schema');
  return result;
}

function processFile(filePath) {
  const filename = path.basename(filePath);
  let html = fs.readFileSync(filePath, 'utf8');
  const orig = html;
  const fc = [];
  html = fixCanonical(html, filename, fc);
  html = fixOgTags(html, filename, fc);
  html = fixRobots(html, filename, fc);
  html = fixSchemaUrls(html, filename, fc);
  totalFiles++;
  if (html !== orig) {
    fs.writeFileSync(filePath, html, 'utf8');
    totalFixed++;
    const rel = filePath.replace(ROOT + '/', '').replace(ROOT + path.sep, '');
    changes.push({ file: rel, changes: fc });
  }
}

console.log('=== Technical SEO Fix Script ===\n');
for (const dir of FOLDERS) {
  if (!fs.existsSync(dir)) { console.log('Skipping (not found): ' + dir); continue; }
  const files = fs.readdirSync(dir).filter(function(f) { return f.endsWith('.html'); }).map(function(f) { return path.join(dir, f); });
  console.log('Processing ' + files.length + ' files in: ' + dir);
  for (const f of files) processFile(f);
}

console.log('\n=== RESULTS ===\n');
console.log('Total files scanned: ' + totalFiles);
console.log('Files modified: ' + totalFixed);
console.log('');
if (changes.length === 0) {
  console.log('No changes needed - all files already clean.');
} else {
  for (const e of changes) {
    console.log('[' + e.file + ']');
    for (const l of e.changes) console.log(l);
    console.log('');
  }
}
console.log('Done.');
