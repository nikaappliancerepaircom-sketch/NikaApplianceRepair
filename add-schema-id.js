#!/usr/bin/env node
// add-schema-id.js — adds @id to JSON-LD blocks that are missing it
// Usage: node add-schema-id.js [--site nar|neary|fixlify|nika] [--dry-run]

'use strict';
const fs   = require('fs');
const path = require('path');

const args     = process.argv.slice(2);
const DRY_RUN  = args.includes('--dry-run');
const siteIdx  = args.indexOf('--site');
const SITE_KEY = siteIdx !== -1 ? args[siteIdx + 1] :
                 (args.find(a => a.startsWith('--site=')) || '').replace('--site=', '');

const SITES = {
  nika:    { dir: 'C:/NikaApplianceRepair',    domain: 'https://nikaappliancerepair.com' },
  nar:     { dir: 'C:/nappliancerepair',        domain: 'https://nappliancerepair.com' },
  neary:   { dir: 'C:/appliancerepairneary',    domain: 'https://appliancerepairneary.com' },
  fixlify: { dir: 'C:/fixlifyservices',         domain: 'https://fixlifyservices.com' },
};

const SKIP = new Set(['404.html', 'service-template.html', 'index.html']);
const SKIP_PREFIXES = ['landing-v'];

function walk(dir) {
  const out = [];
  const skipDirs = new Set(['node_modules', '.git', '_queue', 'assets', 'css', 'js', 'images', 'reports', 'tools', 'backups', '.playwright-mcp']);
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) {
      if (skipDirs.has(entry.name)) continue;
      out.push(...walk(path.join(dir, entry.name)));
    } else if (
      entry.name.endsWith('.html') &&
      !SKIP.has(entry.name) &&
      !entry.name.includes('.bak') &&
      !SKIP_PREFIXES.some(p => entry.name.startsWith(p))
    ) {
      out.push(path.join(dir, entry.name));
    }
  }
  return out;
}

function slugToUrl(filePath, siteDir, domain) {
  // Normalize path separators
  const normFile = filePath.replace(/\\/g, '/');
  const normDir  = siteDir.replace(/\\/g, '/');
  const rel = normFile.slice(normDir.length).replace(/^\//, '');
  const slug = rel.replace(/\.html$/, '').replace(/\/index$/, '/');
  return domain + '/' + slug;
}

function addIdToEntity(entity, pageUrl, domain) {
  if (entity['@id']) return entity; // already has @id

  const type = entity['@type'];
  const types = Array.isArray(type) ? type : [type];

  const businessTypes = ['LocalBusiness', 'Plumber', 'HomeAndConstructionBusiness', 'ProfessionalService', 'HomeRepairBusiness'];
  if (businessTypes.some(t => types.includes(t))) {
    return { '@id': domain + '/#business', ...entity };
  }
  if (types.includes('WebPage') || types.includes('WebSite')) {
    return { '@id': pageUrl + '#webpage', ...entity };
  }
  if (types.includes('Service')) {
    return { '@id': pageUrl + '#service', ...entity };
  }
  if (types.includes('BreadcrumbList')) {
    return { '@id': pageUrl + '#breadcrumb', ...entity };
  }
  if (types.includes('FAQPage')) {
    return { '@id': pageUrl + '#faq', ...entity };
  }
  return entity; // unknown type, skip
}

function readFileWithRetry(filePath, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      return fs.readFileSync(filePath, 'utf8');
    } catch (e) {
      if (i === retries - 1) throw e;
      // Brief synchronous wait via a tight loop (avoid async complexity)
      const end = Date.now() + 50;
      while (Date.now() < end) { /* wait */ }
    }
  }
}

function processFile(filePath, domain, siteDir) {
  let html = readFileWithRetry(filePath);
  const pageUrl = slugToUrl(filePath, siteDir, domain);

  const schemaRegex = /(<script type="application\/ld\+json">)([\s\S]*?)(<\/script>)/g;
  let fileChanged = false;
  let schemasModified = 0;

  html = html.replace(schemaRegex, (match, open, json, close) => {
    let parsed;
    try {
      parsed = JSON.parse(json.trim());
    } catch {
      return match; // skip unparseable blocks
    }

    let blockChanged = false;

    if (parsed['@graph']) {
      const newGraph = parsed['@graph'].map(entity => {
        const updated = addIdToEntity(entity, pageUrl, domain);
        if (updated !== entity || updated['@id'] !== entity['@id']) {
          blockChanged = true;
        }
        return updated;
      });
      // Check if anything actually changed
      const changed = newGraph.some((e, i) => e['@id'] !== parsed['@graph'][i]['@id']);
      if (changed) {
        parsed['@graph'] = newGraph;
        blockChanged = true;
      }
    } else {
      const updated = addIdToEntity(parsed, pageUrl, domain);
      if (updated['@id'] && !json.includes('"@id"')) {
        parsed = updated;
        blockChanged = true;
      }
    }

    if (blockChanged) {
      fileChanged = true;
      schemasModified++;
      return open + '\n' + JSON.stringify(parsed, null, 2) + '\n' + close;
    }
    return match;
  });

  return { changed: fileChanged, html, count: schemasModified };
}

const sitesToProcess = SITE_KEY ? [SITE_KEY] : ['nika', 'nar', 'neary', 'fixlify'];

for (const key of sitesToProcess) {
  const site = SITES[key];
  if (!site) {
    console.error('Unknown site:', key);
    continue;
  }

  const files = walk(site.dir);
  let filesFixed = 0;
  let totalSchemas = 0;

  for (const f of files) {
    const { changed, html, count } = processFile(f, site.domain, site.dir);
    if (changed) {
      if (!DRY_RUN) fs.writeFileSync(f, html, 'utf8');
      filesFixed++;
      totalSchemas += count;
    }
  }

  console.log(
    `${key.toUpperCase()}: ${filesFixed} files updated, ${totalSchemas} schema blocks modified` +
    (DRY_RUN ? ' [DRY RUN]' : '') +
    ` (${files.length} total HTML files scanned)`
  );
}
