#!/usr/bin/env node
/**
 * fix-css-perf.js — Fix render-blocking CSS on static HTML site
 *
 * 1. Removes duplicate <link rel="stylesheet"> tags (same href)
 * 2. Converts non-critical CSS to async preload pattern
 *
 * Usage:
 *   node fix-css-perf.js            # apply fixes
 *   node fix-css-perf.js --dry-run  # preview only
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname);
const DRY_RUN = process.argv.includes('--dry-run');

// Files to skip (root-level)
const SKIP_ROOT = new Set([
  'blog-nika-appliance-repair.html',
  'preview.html',
  'book.html',
  'about.html',
  'compare.html',
  'locations.html',
  'brands.html',
  '404.html',
  'services.html',
  'team.html',
]);

// Non-critical CSS filenames (just the basename) — defer with preload pattern
const NON_CRITICAL = new Set([
  'countdown-horizontal.css',
  'cta-buttons.css',
  'mobile-icon-centering-fix.css',
  'video-custom.css',
  'about-redesign.css',
  'desktop-tablet-optimization.css',
  'mobile-strict-fix.css',
  'mobile-bmad-typography.css',
  'lighthouse-fixes.css',
  'youtube-facade.css',
  'mobile-overflow-fix.css',
  'no-scrollbars-fix.css',
  'final-overflow-fix.css',
  'ai-seo-styles.css',
  'combined-fixes.css',
  'design-fixes-2026.css',
  'common-problems-premium.css',
  'brands-premium.css',
  'areas-premium.css',
  'booking-form-optimized.css',
  'hero-image-mobile-fix.css',
]);

// Critical CSS filenames — keep synchronous (do NOT defer)
const CRITICAL = new Set([
  'design-system.css',
  'style.css',
  'responsive-comprehensive.css',
  'video-modern.css',
  'how-it-works-modern.css',
  'header-optimized.css',
]);

// Collect target files
function collectFiles() {
  const files = [];

  // services/, locations/, brands/ — all .html
  for (const dir of ['services', 'locations', 'brands']) {
    const dirPath = path.join(ROOT, dir);
    if (!fs.existsSync(dirPath)) continue;
    for (const f of fs.readdirSync(dirPath)) {
      if (f.endsWith('.html')) {
        files.push(path.join(dirPath, f));
      }
    }
  }

  // Root *.html — skip landing*.html, skip list, skip blog dir
  for (const f of fs.readdirSync(ROOT)) {
    if (!f.endsWith('.html')) continue;
    if (f.startsWith('landing')) continue;
    if (SKIP_ROOT.has(f)) continue;
    files.push(path.join(ROOT, f));
  }

  return files;
}

/**
 * Extract the CSS filename from an href attribute value.
 * e.g. "../css/style.css" -> "style.css", "/css/foo.css" -> "foo.css"
 */
function cssBasename(href) {
  return path.basename(href);
}

/**
 * Check if a line is a non-critical CSS link we should convert.
 * Returns the href if yes, null otherwise.
 */
function getNonCriticalHref(line) {
  // Match <link rel="stylesheet" href="...">
  const m = line.match(/<link\s[^>]*rel=["']stylesheet["'][^>]*href=["']([^"']+)["'][^>]*>/i)
         || line.match(/<link\s[^>]*href=["']([^"']+)["'][^>]*rel=["']stylesheet["'][^>]*>/i);
  if (!m) return null;
  const href = m[1];
  const base = cssBasename(href);
  // Skip Google Fonts
  if (href.includes('fonts.googleapis.com')) return null;
  // Only convert if it's in our non-critical list
  if (NON_CRITICAL.has(base)) return href;
  return null;
}

/**
 * Process a single HTML file. Returns changes log array.
 */
function processFile(filePath) {
  const relPath = path.relative(ROOT, filePath);
  let html = fs.readFileSync(filePath, 'utf8');
  const changes = [];

  // --- 1. Remove duplicate stylesheet links (same href) ---
  const seenHrefs = new Set();
  const lines = html.split('\n');
  const deduped = [];
  let dupsRemoved = 0;

  for (const line of lines) {
    const stylesheetMatch = line.match(/<link\s[^>]*rel=["']stylesheet["'][^>]*href=["']([^"']+)["'][^>]*>/i)
                         || line.match(/<link\s[^>]*href=["']([^"']+)["'][^>]*rel=["']stylesheet["'][^>]*>/i);
    if (stylesheetMatch) {
      const href = stylesheetMatch[1];
      // Normalize: strip leading ../ or ./ or / for comparison
      const normalized = href.replace(/^\.\.\/|^\.\/|^\//g, '');
      if (seenHrefs.has(normalized)) {
        dupsRemoved++;
        changes.push(`  REMOVED duplicate: ${href}`);
        continue; // skip this duplicate line
      }
      seenHrefs.add(normalized);
    }
    deduped.push(line);
  }
  html = deduped.join('\n');

  // --- 2. Convert non-critical CSS to async preload pattern ---
  // Process line by line again to handle replacements
  const finalLines = html.split('\n');
  const result = [];
  let cssDeferred = 0;

  for (const line of finalLines) {
    // Skip lines that already have the preload+onload pattern
    if (line.includes('onload=') && line.includes('rel=\'stylesheet\'')) {
      result.push(line);
      continue;
    }

    const href = getNonCriticalHref(line);
    if (href) {
      // Get the indentation from original line
      const indent = line.match(/^(\s*)/)[1];
      // Replace with async preload pattern
      result.push(`${indent}<link rel="preload" href="${href}" as="style" onload="this.onload=null;this.rel='stylesheet'">`);
      result.push(`${indent}<noscript><link rel="stylesheet" href="${href}"></noscript>`);
      cssDeferred++;
      changes.push(`  ASYNC PRELOAD: ${cssBasename(href)}`);
    } else {
      result.push(line);
    }
  }

  html = result.join('\n');

  // --- Write if changes were made ---
  if (changes.length > 0) {
    if (!DRY_RUN) {
      fs.writeFileSync(filePath, html, 'utf8');
    }
  }

  return { relPath, changes, dupsRemoved, cssDeferred };
}

// --- Main ---
function main() {
  console.log(`\n=== CSS Performance Fix ${DRY_RUN ? '(DRY RUN)' : '(LIVE)'} ===\n`);

  const files = collectFiles();
  let totalFiles = 0;
  let totalDups = 0;
  let totalDeferred = 0;
  let totalHeaderDefer = 0;
  const allResults = [];

  for (const f of files) {
    const { relPath, changes, dupsRemoved, cssDeferred } = processFile(f);
    if (changes.length > 0) {
      totalFiles++;
      totalDups += dupsRemoved;
      totalDeferred += cssDeferred;
      if (changes.some(c => c.includes('DEFERRED: header-loader'))) totalHeaderDefer++;
      allResults.push({ relPath, changes });
    }
  }

  // Print results
  for (const { relPath, changes } of allResults) {
    console.log(`${relPath}`);
    for (const c of changes) {
      console.log(c);
    }
    console.log('');
  }

  // Summary
  console.log('--- SUMMARY ---');
  console.log(`Files processed: ${files.length}`);
  console.log(`Files with changes: ${totalFiles}`);
  console.log(`Duplicate stylesheets removed: ${totalDups}`);
  console.log(`CSS files converted to async preload: ${totalDeferred}`);
  console.log(`header-loader.js deferred: ${totalHeaderDefer}`);
  if (DRY_RUN) {
    console.log('\n(Dry run — no files were modified)\n');
  } else {
    console.log('\n(Changes applied successfully)\n');
  }
}

main();
