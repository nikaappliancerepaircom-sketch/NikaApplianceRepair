#!/usr/bin/env node
// gen-sitemap-full.js — nikaappliancerepair.com
// Full filesystem scan — replaces gen-sitemap.js
// Runs LAST in CI after all drip/publish steps.

'use strict';
const fs   = require('fs');
const path = require('path');

const DOMAIN   = 'https://nikaappliancerepair.com';
const SITE_DIR = path.resolve(__dirname);
const TODAY    = new Date().toISOString().slice(0, 10);

const SKIP_FILES = new Set([
  '404.html','service-template.html','ajax.html','book.html',
  'preview.html','sitemap.html','accessibility.html',
  'index.html', // handled as '/' below
]);
const SKIP_DIRS = new Set([
  'node_modules','.git','_queue','assets','css','js','images',
  'fonts','components','templates','styles','backups','backup',
  'old','archive','reports','tools','compare','preview',
  '_drafts','_published_log.json','test-components','premium-blog',
  'maintenance','nul',
]);
const SKIP_PATTERNS = [/^landing/, /\.bak\.html$/];

function shouldSkipFile(name) {
  if (SKIP_FILES.has(name)) return true;
  if (SKIP_PATTERNS.some(p => p.test(name))) return true;
  return false;
}

function mtime(fp) {
  try { return fs.statSync(fp).mtime.toISOString().slice(0, 10); } catch { return TODAY; }
}

const urls = [];

function addUrl(loc, lastmod, priority = '0.8', changefreq = 'weekly') {
  urls.push({ loc, lastmod, priority, changefreq });
}

// Homepage
addUrl(DOMAIN + '/', mtime(path.join(SITE_DIR, 'index.html')), '1.0', 'weekly');

// Walk a directory recursively, building clean URLs
function walk(dir, urlPrefix, priority = '0.8') {
  let items;
  try { items = fs.readdirSync(dir, { withFileTypes: true }); } catch { return; }

  for (const item of items) {
    if (item.isDirectory()) {
      if (SKIP_DIRS.has(item.name)) continue;
      walk(path.join(dir, item.name), urlPrefix + item.name + '/', priority);
    } else if (item.name.endsWith('.html')) {
      if (shouldSkipFile(item.name)) continue;
      const fp = path.join(dir, item.name);
      if (item.name === 'index.html') {
        // directory index — URL is the directory path
        addUrl(DOMAIN + '/' + urlPrefix, mtime(fp), priority, 'weekly');
      } else {
        const slug = item.name.replace(/\.html$/, '');
        addUrl(DOMAIN + '/' + urlPrefix + slug, mtime(fp), priority, 'weekly');
      }
    }
  }
}

// Root service+city pages
walk(SITE_DIR, '', '0.85');

// Output XML
const lines = [
  '<?xml version="1.0" encoding="UTF-8"?>',
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
];
for (const { loc, lastmod, priority, changefreq } of urls) {
  lines.push('  <url>');
  lines.push(`    <loc>${loc}</loc>`);
  lines.push(`    <lastmod>${lastmod}</lastmod>`);
  lines.push(`    <changefreq>${changefreq}</changefreq>`);
  lines.push(`    <priority>${priority}</priority>`);
  lines.push('  </url>');
}
lines.push('</urlset>');

const out = path.join(SITE_DIR, 'sitemap.xml');
fs.writeFileSync(out, lines.join('\n'), 'utf8');
console.log(`nikaappliancerepair.com: sitemap.xml → ${urls.length} URLs`);
