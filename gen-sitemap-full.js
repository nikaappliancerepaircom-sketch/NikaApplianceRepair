#!/usr/bin/env node

'use strict';

const fs = require('fs');
const path = require('path');

const DOMAIN = 'https://nikaappliancerepair.com';
const SITE_DIR = path.resolve(__dirname);
const SITEMAP_PATH = path.join(SITE_DIR, 'sitemap.xml');

const SKIP_DIRS = new Set([
  '.git', '.github', '.wrangler', 'archive', 'assets', 'backup', 'backups',
  'compare', 'components', 'css', 'fonts', 'images', 'includes', 'js',
  'node_modules', 'old', 'preview', 'reports', 'templates', 'test-components',
  'tests', 'tools', '_drafts', '_queue',
]);
const SKIP_FILES = new Set([
  '404.html', 'accessibility.html', 'book.html', 'preview.html',
  'service-template.html', 'sitemap.html',
]);
const SKIP_PATTERNS = [/^landing/i, /\.bak\.html$/i];

function normalizePath(value) {
  let pathname = value;
  try {
    pathname = new URL(value, DOMAIN).pathname;
  } catch {
    return null;
  }

  pathname = decodeURI(pathname).replace(/\\/g, '/');
  pathname = pathname.replace(/\/index\.html$/i, '/');
  pathname = pathname.replace(/\.html$/i, '');
  pathname = pathname.replace(/\/{2,}/g, '/');
  if (!pathname.startsWith('/')) pathname = `/${pathname}`;
  if (pathname.length > 1) pathname = pathname.replace(/\/$/, '');
  return pathname;
}

function escapeXml(value) {
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

function readPublishedPaths() {
  if (!fs.existsSync(SITEMAP_PATH)) {
    throw new Error('sitemap.xml is required to preserve the existing published URL set');
  }

  const xml = fs.readFileSync(SITEMAP_PATH, 'utf8');
  const paths = new Set();
  for (const match of xml.matchAll(/<loc>\s*([^<]+?)\s*<\/loc>/gi)) {
    const pathname = normalizePath(match[1]);
    if (pathname) paths.add(pathname);
  }
  if (paths.size === 0) throw new Error('sitemap.xml contains no published URLs');
  return paths;
}

function shouldSkipFile(filePath) {
  const relative = path.relative(SITE_DIR, filePath);
  const parts = relative.split(path.sep);
  if (parts.slice(0, -1).some((part) => SKIP_DIRS.has(part))) return true;
  const name = parts.at(-1);
  return SKIP_FILES.has(name) || SKIP_PATTERNS.some((pattern) => pattern.test(name));
}

function collectHtmlFiles(directory, files = []) {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    if (entry.isDirectory() && SKIP_DIRS.has(entry.name)) continue;
    const absolute = path.join(directory, entry.name);
    if (entry.isDirectory()) collectHtmlFiles(absolute, files);
    else if (entry.name.endsWith('.html') && !shouldSkipFile(absolute)) files.push(absolute);
  }
  return files;
}

function routeForFile(filePath) {
  const relative = path.relative(SITE_DIR, filePath).split(path.sep).join('/');
  return normalizePath(`/${relative}`);
}

function inspectPage(filePath) {
  const html = fs.readFileSync(filePath, 'utf8');
  const route = routeForFile(filePath);
  const canonicalMatches = [...html.matchAll(/<link\b[^>]*\brel=["'][^"']*canonical[^"']*["'][^>]*>/gi)];
  const canonicalValues = canonicalMatches
    .map((match) => match[0].match(/\bhref=["']([^"']+)["']/i)?.[1])
    .filter(Boolean);
  const canonical = canonicalValues.length === 1 ? normalizePath(canonicalValues[0]) : null;
  const noindex = /<meta\b[^>]*\bname=["']robots["'][^>]*\bcontent=["'][^"']*noindex/i.test(html)
    || /<meta\b[^>]*\bcontent=["'][^"']*noindex[^"']*["'][^>]*\bname=["']robots["']/i.test(html);
  const redirect = /<meta\b[^>]*http-equiv=["']refresh["']/i.test(html);

  return { route, canonical, canonicalCount: canonicalValues.length, noindex, redirect };
}

function buildSitemap() {
  const publishedPaths = readPublishedPaths();
  const included = new Set();
  const skipped = {
    alternateCanonical: 0,
    duplicateCanonical: 0,
    missingCanonical: 0,
    noindex: 0,
    redirect: 0,
    unpublished: 0,
  };

  for (const filePath of collectHtmlFiles(SITE_DIR)) {
    const page = inspectPage(filePath);
    if (!publishedPaths.has(page.route)) {
      skipped.unpublished += 1;
      continue;
    }
    if (page.redirect) {
      skipped.redirect += 1;
      continue;
    }
    if (page.noindex) {
      skipped.noindex += 1;
      continue;
    }
    if (page.canonicalCount === 0) {
      skipped.missingCanonical += 1;
      continue;
    }
    if (page.canonicalCount > 1) {
      skipped.duplicateCanonical += 1;
      continue;
    }
    if (page.canonical !== page.route) {
      skipped.alternateCanonical += 1;
      continue;
    }
    included.add(page.route);
  }

  const urls = [...included].sort((a, b) => a.localeCompare(b));
  const lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ...urls.map((pathname) => `  <url><loc>${escapeXml(`${DOMAIN}${pathname === '/' ? '/' : pathname}`)}</loc></url>`),
    '</urlset>',
    '',
  ];
  fs.writeFileSync(SITEMAP_PATH, lines.join('\n'), 'utf8');
  return { domain: DOMAIN, urls: urls.length, skipped };
}

try {
  console.log(JSON.stringify(buildSitemap()));
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
