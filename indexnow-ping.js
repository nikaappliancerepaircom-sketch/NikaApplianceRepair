#!/usr/bin/env node
// indexnow-ping.js — Submit priority URLs to IndexNow (Bing) for all 4 sites
const https = require('https');
const fs = require('fs');
const path = require('path');

const SITES = [
  { domain: 'nikaappliancerepair.com', dir: 'C:/NikaApplianceRepair', key: 'nika2026indexnow' },
  { domain: 'nappliancerepair.com',    dir: 'C:/nappliancerepair',    key: 'nar2026indexnow' },
  { domain: 'appliancerepairneary.com',dir: 'C:/appliancerepairneary',key: 'neary2026indexnow' },
  { domain: 'fixlifyservices.com',     dir: 'C:/fixlifyservices',     key: 'fixlify2026indexnow' },
];

function getSitemapUrls(dir, domain) {
  const sitemapPath = path.join(dir, 'sitemap.xml');
  if (!fs.existsSync(sitemapPath)) return [];
  const xml = fs.readFileSync(sitemapPath, 'utf8');
  const matches = xml.match(/<loc>([^<]+)<\/loc>/g) || [];
  return matches.map(m => m.replace(/<\/?loc>/g, '').trim());
}

function ping(site, urls) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      host: site.domain,
      key: site.key,
      keyLocation: `https://${site.domain}/${site.key}.txt`,
      urlList: urls.slice(0, 10000)
    });
    const req = https.request({
      hostname: 'api.indexnow.org',
      path: '/indexnow',
      method: 'POST',
      headers: { 'Content-Type': 'application/json; charset=utf-8', 'Content-Length': Buffer.byteLength(body) }
    }, res => {
      let data = '';
      res.on('data', d => data += d);
      res.on('end', () => resolve({ status: res.statusCode, body: data.slice(0, 200) }));
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

async function main() {
  for (const site of SITES) {
    // Write key file
    const keyFile = path.join(site.dir, `${site.key}.txt`);
    fs.writeFileSync(keyFile, site.key);
    console.log(`\n[${site.domain}]`);
    console.log(`  Key file: ${keyFile}`);

    const urls = getSitemapUrls(site.dir, site.domain);
    console.log(`  URLs to submit: ${urls.length}`);
    if (urls.length === 0) { console.log('  ⚠ No sitemap URLs found'); continue; }

    try {
      const result = await ping(site, urls);
      console.log(`  Status: ${result.status} ${result.status === 200 ? '✅' : result.status === 202 ? '✅ queued' : '⚠'}`);
      if (result.body) console.log(`  Response: ${result.body}`);
    } catch(e) {
      console.error(`  ❌ Error: ${e.message}`);
    }
  }
}

main().then(() => console.log('\n✅ IndexNow done')).catch(console.error);
