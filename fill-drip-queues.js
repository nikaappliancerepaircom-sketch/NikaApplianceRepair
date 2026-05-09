#!/usr/bin/env node
// fill-drip-queues.js
// Adds all sitemap URLs not yet in url-drip-queue.json for each satellite.

'use strict';
const fs   = require('fs');
const path = require('path');

const SITES = [
  { dir: 'C:/nappliancerepair',     domain: 'https://nappliancerepair.com' },
  { dir: 'C:/appliancerepairneary', domain: 'https://appliancerepairneary.com' },
  { dir: 'C:/fixlifyservices',      domain: 'https://fixlifyservices.com' },
];

for (const site of SITES) {
  const sitemapPath = path.join(site.dir, 'sitemap.xml');
  const queuePath   = path.join(site.dir, 'url-drip-queue.json');

  if (!fs.existsSync(sitemapPath)) { console.error(`Missing sitemap: ${sitemapPath}`); continue; }

  // Extract all URLs from sitemap
  const sitemapXml  = fs.readFileSync(sitemapPath, 'utf8');
  const sitemapUrls = [...sitemapXml.matchAll(/<loc>(.*?)<\/loc>/g)].map(m => m[1].trim());

  // Load existing queue
  let queue = [];
  if (fs.existsSync(queuePath)) {
    try { queue = JSON.parse(fs.readFileSync(queuePath, 'utf8')); } catch { queue = []; }
  }
  const queueSet = new Set(queue);

  // Find missing URLs (in sitemap but not in queue)
  const missing = sitemapUrls.filter(u => !queueSet.has(u));

  // Append missing at the end
  const newQueue = [...queue, ...missing];
  fs.writeFileSync(queuePath, JSON.stringify(newQueue, null, 2));

  console.log(`${site.domain}: sitemap=${sitemapUrls.length}, queue_before=${queue.length}, added=${missing.length}, queue_after=${newQueue.length}`);
}

console.log('\nDone.');
