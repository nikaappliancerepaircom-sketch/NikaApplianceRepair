/**
 * gen-sitemap.js — nikaappliancerepair.com
 * Generates sitemap.xml — clean URLs (no .html extension)
 * Uses file mtime for lastmod (respects backdating)
 * node C:/NikaApplianceRepair/gen-sitemap.js
 */
const fs = require('fs');
const path = require('path');

const DOMAIN = 'https://nikaappliancerepair.com';
const SITE_DIR = 'C:/NikaApplianceRepair';

function mtime(filepath) {
  try {
    return fs.statSync(filepath).mtime.toISOString().slice(0, 10);
  } catch {
    return new Date().toISOString().slice(0, 10);
  }
}

// Normalize filepath to forward slashes and strip SITE_DIR prefix + .html
function toUrl(filepath) {
  return filepath.replace(/\\/g, '/').replace(SITE_DIR, '').replace(/\.html$/, '');
}

const urls = [];

function addUrl(loc, lastmod, priority = '0.8', changefreq = 'weekly') {
  urls.push({ loc, lastmod, priority, changefreq });
}

// Main pages (static)
const mainPages = [
  ['/', '1.0', 'weekly'],
  ['/about', '0.9', 'monthly'],
  ['/services', '1.0', 'weekly'],
  ['/locations', '0.9', 'weekly'],
  ['/brands', '0.8', 'monthly'],
  ['/blog/', '1.0', 'daily'],
  ['/privacy', '0.5', 'yearly'],
];

for (const [slug, pri, freq] of mainPages) {
  let lm;
  try {
    const fp = slug === '/' ? path.join(SITE_DIR, 'index.html')
             : slug.endsWith('/') ? path.join(SITE_DIR, slug, 'index.html')
             : path.join(SITE_DIR, slug + '.html');
    lm = mtime(fp);
  } catch {
    lm = new Date().toISOString().slice(0, 10);
  }
  addUrl(DOMAIN + slug, lm, pri, freq);
}

// Blog posts — walk all subdirs, strip .html, skip index/image-gallery
const blogDir = path.join(SITE_DIR, 'blog');
if (fs.existsSync(blogDir)) {
  const skipNames = ['index.html', 'image-gallery.html'];
  const skipDirs = ['_drafts', '_queue', '_published_log.json', 'template', 'backup', 'test-components', 'premium-blog', 'css', 'js', 'images', 'maintenance', 'nul'];
  function walkBlog(dir) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      if (entry.isDirectory()) {
        if (!skipDirs.includes(entry.name)) walkBlog(path.join(dir, entry.name));
      } else if (entry.name.endsWith('.html') && !skipNames.includes(entry.name)) {
        const filepath = path.join(dir, entry.name);
        const urlPath = toUrl(filepath);
        addUrl(DOMAIN + urlPath, mtime(filepath), '0.85', 'weekly');
      }
    }
  }
  walkBlog(blogDir);
}

// Service pages: /services/[service] (strip .html)
const servicesDir = path.join(SITE_DIR, 'services');
if (fs.existsSync(servicesDir)) {
  for (const entry of fs.readdirSync(servicesDir, { withFileTypes: true })) {
    if (entry.isDirectory()) {
      const idx = path.join(servicesDir, entry.name, 'index.html');
      if (fs.existsSync(idx)) {
        addUrl(`${DOMAIN}/services/${entry.name}/`, mtime(idx), '0.9', 'weekly');
      }
    } else if (entry.name.endsWith('.html') && entry.name !== 'index.html') {
      const filepath = path.join(servicesDir, entry.name);
      addUrl(`${DOMAIN}/services/${entry.name.replace(/\.html$/, '')}`, mtime(filepath), '0.85', 'weekly');
    }
  }
}

// Location pages: /locations/[city] (strip .html)
const locDir = path.join(SITE_DIR, 'locations');
if (fs.existsSync(locDir)) {
  for (const entry of fs.readdirSync(locDir, { withFileTypes: true })) {
    if (entry.isDirectory() && entry.name !== 'services') {
      const idx = path.join(locDir, entry.name, 'index.html');
      if (fs.existsSync(idx)) {
        addUrl(`${DOMAIN}/locations/${entry.name}/`, mtime(idx), '0.85', 'weekly');
      }
    } else if (entry.name.endsWith('.html') && entry.name !== 'index.html') {
      const filepath = path.join(locDir, entry.name);
      addUrl(`${DOMAIN}/locations/${entry.name.replace(/\.html$/, '')}`, mtime(filepath), '0.8', 'weekly');
    }
  }
}

// Locations/services pages: /locations/services/[service]-[city] (strip .html)
const locServDir = path.join(SITE_DIR, 'locations', 'services');
if (fs.existsSync(locServDir)) {
  for (const file of fs.readdirSync(locServDir)) {
    if (!file.endsWith('.html')) continue;
    const filepath = path.join(locServDir, file);
    addUrl(`${DOMAIN}/locations/services/${file.replace(/\.html$/, '')}`, mtime(filepath), '0.8', 'weekly');
  }
}

// Generate XML
const xmlLines = [
  '<?xml version="1.0" encoding="UTF-8"?>',
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
];

for (const { loc, lastmod, priority, changefreq } of urls) {
  xmlLines.push('  <url>');
  xmlLines.push(`    <loc>${loc}</loc>`);
  xmlLines.push(`    <lastmod>${lastmod}</lastmod>`);
  xmlLines.push(`    <changefreq>${changefreq}</changefreq>`);
  xmlLines.push(`    <priority>${priority}</priority>`);
  xmlLines.push('  </url>');
}

xmlLines.push('</urlset>');

const sitemapPath = path.join(SITE_DIR, 'sitemap.xml');
fs.writeFileSync(sitemapPath, xmlLines.join('\n'), 'utf8');
console.log(`nikaappliancerepair: sitemap.xml with ${urls.length} URLs`);
