/**
 * Publish next N queued location/service pages from _pages_queue/
 * - Reads N oldest files (alphabetical) from _pages_queue/
 * - Moves them to site root
 * - Submits URLs to Google Indexing API
 *
 * Usage: node publish-next-page.js [--count N] [--dry-run]
 */
const fs = require('fs');
const path = require('path');
const https = require('https');

const QUEUE_DIR = path.join(__dirname, '_pages_queue');
const ROOT_DIR  = __dirname;
const DOMAIN    = 'https://nikaappliancerepair.com';

const args  = process.argv.slice(2);
const DRY   = args.includes('--dry-run');
const COUNT = parseInt((args.find(a => a.startsWith('--count='))?.split('=')[1]) || (args[args.indexOf('--count')+1]) || '5', 10);

if (!fs.existsSync(QUEUE_DIR)) {
  console.log('[pages] No _pages_queue/ directory, skipping.');
  process.exit(0);
}

const files = fs.readdirSync(QUEUE_DIR)
  .filter(f => f.endsWith('.html'))
  .sort()
  .slice(0, COUNT);

if (files.length === 0) {
  console.log('[pages] Queue empty, nothing to publish.');
  process.exit(0);
}

async function submitIndexing(url) {
  const saJson = process.env.GOOGLE_INDEXING_SA || process.env.GOOGLE_INDEXING_API_KEY;
  if (!saJson) {
    console.warn(`  [indexing] no GOOGLE_INDEXING_SA / GOOGLE_INDEXING_API_KEY env var; skipping ${url}`);
    return;
  }
  try {
    const { createSign } = require('crypto');
    const sa = JSON.parse(saJson);
    const now = Math.floor(Date.now() / 1000);
    const header = Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' })).toString('base64url');
    const payload = Buffer.from(JSON.stringify({
      iss: sa.client_email, sub: sa.client_email,
      aud: 'https://oauth2.googleapis.com/token', iat: now, exp: now + 3600,
      scope: 'https://www.googleapis.com/auth/indexing'
    })).toString('base64url');
    const sign = createSign('RSA-SHA256');
    sign.update(`${header}.${payload}`);
    const jwt = `${header}.${payload}.${sign.sign(sa.private_key, 'base64url')}`;

    const tokenRes = await new Promise((resolve) => {
      const body = `grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Ajwt-bearer&assertion=${jwt}`;
      const req = https.request({ hostname: 'oauth2.googleapis.com', path: '/token', method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'Content-Length': body.length }
      }, res => { let d = ''; res.on('data', c => d += c); res.on('end', () => resolve(JSON.parse(d))); });
      req.write(body); req.end();
    });

    if (!tokenRes.access_token) {
      console.warn(`  [indexing] OAuth token request failed for ${url}: ${JSON.stringify(tokenRes).slice(0, 200)}`);
      return;
    }

    const indexingResult = await new Promise((resolve) => {
      const body = JSON.stringify({ url, type: 'URL_UPDATED' });
      const req = https.request({
        hostname: 'indexing.googleapis.com',
        path: '/v3/urlNotifications:publish',
        method: 'POST',
        headers: { 'Authorization': `Bearer ${tokenRes.access_token}`, 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) }
      }, res => {
        let d = '';
        res.on('data', c => d += c);
        res.on('end', () => resolve({ status: res.statusCode, body: d }));
      });
      req.on('error', err => resolve({ status: 0, body: err.message }));
      req.write(body); req.end();
    });

    if (indexingResult.status !== 200) {
      console.warn(`  [indexing] HTTP ${indexingResult.status} for ${url}: ${indexingResult.body.slice(0, 200)}`);
    } else {
      console.log(`  [indexing] OK ${url}`);
    }
  } catch (e) {
    console.warn(`  [indexing] exception for ${url}: ${e.message}`);
  }
}

(async () => {
  console.log(`[pages] Publishing ${files.length} pages from queue (${DRY ? 'DRY RUN' : 'LIVE'}):`);
  for (const file of files) {
    const src = path.join(QUEUE_DIR, file);
    const dst = path.join(ROOT_DIR, file);
    const url = `${DOMAIN}/${file.replace('.html', '')}`;
    if (DRY) {
      console.log(`  [DRY] ${file} → / (${url})`);
    } else {
      if (fs.existsSync(dst)) {
        console.warn(`  [SKIP] ${path.basename(dst)} already exists; skipping to avoid overwrite.`);
        continue;
      }
      fs.renameSync(src, dst);
      await submitIndexing(url);
      console.log(`  ✓ ${file}`);
    }
  }
  const remaining = fs.readdirSync(QUEUE_DIR).filter(f => f.endsWith('.html')).length;
  console.log(`[pages] Done. ${remaining} pages remaining in queue.`);
})();
