/**
 * Google Indexing API — Submit 148 location service pages
 * nikaappliancerepair.com
 */
const fs = require('fs');
const https = require('https');
const crypto = require('crypto');

const env = fs.readFileSync('C:/NikaApplianceRepair/.env', 'utf8');
const match = env.match(/GOOGLE_INDEXING_API_KEY=(\{[\s\S]+?\})\n/);
const SA = JSON.parse(match[1]);

const BASE = 'https://nikaappliancerepair.com/locations/services';

const SLUGS = [
  // dishwasher (25)
  'dishwasher-repair-bloor-west-village','dishwasher-repair-brampton','dishwasher-repair-chinatown',
  'dishwasher-repair-corso-italia','dishwasher-repair-dufferin-grove','dishwasher-repair-east-york',
  'dishwasher-repair-etobicoke-village','dishwasher-repair-greektown','dishwasher-repair-high-park',
  'dishwasher-repair-king-west','dishwasher-repair-little-italy','dishwasher-repair-little-portugal',
  'dishwasher-repair-markham','dishwasher-repair-midtown','dishwasher-repair-mississauga',
  'dishwasher-repair-ossington','dishwasher-repair-richmond-hill','dishwasher-repair-roncesvalles',
  'dishwasher-repair-st-lawrence','dishwasher-repair-swansea','dishwasher-repair-the-beaches',
  'dishwasher-repair-thorncliffe-park','dishwasher-repair-trinity-bellwoods',
  'dishwasher-repair-vaughan','dishwasher-repair-wychwood',
  // dryer (26)
  'dryer-repair-bloor-west-village','dryer-repair-brampton','dryer-repair-chinatown',
  'dryer-repair-corso-italia','dryer-repair-dufferin-grove','dryer-repair-east-york',
  'dryer-repair-etobicoke-village','dryer-repair-greektown','dryer-repair-high-park',
  'dryer-repair-king-west','dryer-repair-little-italy','dryer-repair-little-portugal',
  'dryer-repair-markham','dryer-repair-midtown','dryer-repair-mississauga',
  'dryer-repair-ossington','dryer-repair-parkdale','dryer-repair-richmond-hill',
  'dryer-repair-roncesvalles','dryer-repair-st-lawrence','dryer-repair-swansea',
  'dryer-repair-the-beaches','dryer-repair-thorncliffe-park','dryer-repair-trinity-bellwoods',
  'dryer-repair-vaughan','dryer-repair-wychwood',
  // oven (25)
  'oven-repair-bloor-west-village','oven-repair-brampton','oven-repair-chinatown',
  'oven-repair-corso-italia','oven-repair-dufferin-grove','oven-repair-east-york',
  'oven-repair-etobicoke-village','oven-repair-greektown','oven-repair-high-park',
  'oven-repair-king-west','oven-repair-little-italy','oven-repair-little-portugal',
  'oven-repair-markham','oven-repair-midtown','oven-repair-mississauga',
  'oven-repair-ossington','oven-repair-richmond-hill','oven-repair-roncesvalles',
  'oven-repair-st-lawrence','oven-repair-swansea','oven-repair-the-beaches',
  'oven-repair-thorncliffe-park','oven-repair-trinity-bellwoods',
  'oven-repair-vaughan','oven-repair-wychwood',
  // refrigerator (26)
  'refrigerator-repair-bloor-west-village','refrigerator-repair-brampton','refrigerator-repair-chinatown',
  'refrigerator-repair-corso-italia','refrigerator-repair-dufferin-grove','refrigerator-repair-east-york',
  'refrigerator-repair-etobicoke-village','refrigerator-repair-greektown','refrigerator-repair-high-park',
  'refrigerator-repair-king-west','refrigerator-repair-little-italy','refrigerator-repair-little-portugal',
  'refrigerator-repair-markham','refrigerator-repair-midtown','refrigerator-repair-mississauga',
  'refrigerator-repair-ossington','refrigerator-repair-parkdale','refrigerator-repair-richmond-hill',
  'refrigerator-repair-roncesvalles','refrigerator-repair-st-lawrence','refrigerator-repair-swansea',
  'refrigerator-repair-the-beaches','refrigerator-repair-thorncliffe-park','refrigerator-repair-trinity-bellwoods',
  'refrigerator-repair-vaughan','refrigerator-repair-wychwood',
  // stove (20)
  'stove-repair-bloor-west-village','stove-repair-chinatown','stove-repair-corso-italia',
  'stove-repair-dufferin-grove','stove-repair-east-york','stove-repair-etobicoke-village',
  'stove-repair-greektown','stove-repair-high-park','stove-repair-king-west',
  'stove-repair-little-italy','stove-repair-little-portugal','stove-repair-midtown',
  'stove-repair-ossington','stove-repair-roncesvalles','stove-repair-st-lawrence',
  'stove-repair-swansea','stove-repair-the-beaches','stove-repair-thorncliffe-park',
  'stove-repair-trinity-bellwoods','stove-repair-wychwood',
  // washer (26)
  'washer-repair-bloor-west-village','washer-repair-brampton','washer-repair-chinatown',
  'washer-repair-corso-italia','washer-repair-dufferin-grove','washer-repair-east-york',
  'washer-repair-etobicoke-village','washer-repair-greektown','washer-repair-high-park',
  'washer-repair-king-west','washer-repair-little-italy','washer-repair-little-portugal',
  'washer-repair-markham','washer-repair-midtown','washer-repair-mississauga',
  'washer-repair-ossington','washer-repair-parkdale','washer-repair-richmond-hill',
  'washer-repair-roncesvalles','washer-repair-st-lawrence','washer-repair-swansea',
  'washer-repair-the-beaches','washer-repair-thorncliffe-park','washer-repair-trinity-bellwoods',
  'washer-repair-vaughan','washer-repair-wychwood',
];

const URLS = SLUGS.map(s => `${BASE}/${s}`);

function createJWTWithTime(sa, now) {
  const h = Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' })).toString('base64url');
  const p = Buffer.from(JSON.stringify({
    iss: sa.client_email,
    scope: 'https://www.googleapis.com/auth/indexing',
    aud: sa.token_uri,
    iat: now,
    exp: now + 3600
  })).toString('base64url');
  const s = crypto.createSign('RSA-SHA256');
  s.update(h + '.' + p);
  return h + '.' + p + '.' + s.sign(sa.private_key, 'base64url');
}

async function getToken() {
  return new Promise(async resolve => {
    const now = await new Promise(r => {
      https.request({ hostname: 'www.googleapis.com', path: '/', method: 'HEAD' }, res => {
        const d = res.headers['date'];
        r(d ? Math.floor(new Date(d).getTime() / 1000) : Math.floor(Date.now() / 1000));
      }).on('error', () => r(Math.floor(Date.now() / 1000))).end();
    });
    const jwt = createJWTWithTime(SA, now);
    const body = 'grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Ajwt-bearer&assertion=' + jwt;
    const req = https.request({
      hostname: 'oauth2.googleapis.com',
      path: '/token',
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }, r => {
      let d = '';
      r.on('data', c => d += c);
      r.on('end', () => {
        const resp = JSON.parse(d);
        if (resp.error) console.error('OAuth error:', resp.error, resp.error_description);
        resolve(resp.access_token || null);
      });
    });
    req.on('error', e => { console.error(e); resolve(null); });
    req.write(body);
    req.end();
  });
}

async function submit(token, url) {
  return new Promise(resolve => {
    const body = JSON.stringify({ url, type: 'URL_UPDATED' });
    const req = https.request({
      hostname: 'indexing.googleapis.com',
      path: '/v3/urlNotifications:publish',
      method: 'POST',
      headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' }
    }, r => {
      let d = '';
      r.on('data', c => d += c);
      r.on('end', () => resolve({ status: r.statusCode, body: d }));
    });
    req.on('error', e => resolve({ status: 0, body: e.message }));
    req.write(body);
    req.end();
  });
}

(async () => {
  console.log(`Submitting ${URLS.length} URLs to Google Indexing API...`);
  const token = await getToken();
  if (!token) { console.error('Failed to get token'); process.exit(1); }
  console.log('Token OK\n');

  let ok = 0, fail = 0;
  for (const url of URLS) {
    const r = await submit(token, url);
    const icon = r.status === 200 ? '✅' : '❌';
    const slug = url.split('/').pop();
    console.log(`${icon} ${r.status} ${slug}`);
    if (r.status === 200) ok++;
    else { fail++; console.log('   ', r.body.substring(0, 150)); }
    await new Promise(r => setTimeout(r, 100)); // 100ms between requests
  }

  console.log(`\n✅ ${ok} submitted | ❌ ${fail} failed | Total: ${URLS.length}`);
})().catch(console.error);
