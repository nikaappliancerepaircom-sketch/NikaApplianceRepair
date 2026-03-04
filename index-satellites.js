const fs = require('fs');
const https = require('https');
const crypto = require('crypto');

const env = fs.readFileSync('C:/NikaApplianceRepair/.env', 'utf8');
const match = env.match(/GOOGLE_INDEXING_API_KEY=(\{[\s\S]+?\})\n/);
const SA = JSON.parse(match[1]);

async function getGoogleTime() {
  return new Promise(resolve => {
    https.request({ hostname: 'www.googleapis.com', path: '/', method: 'HEAD' }, r => {
      const d = r.headers['date'];
      resolve(d ? Math.floor(new Date(d).getTime() / 1000) : Math.floor(Date.now() / 1000));
    }).on('error', () => resolve(Math.floor(Date.now() / 1000))).end();
  });
}

async function getToken() {
  const now = await getGoogleTime();
  const h = Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' })).toString('base64url');
  const p = Buffer.from(JSON.stringify({ iss: SA.client_email, scope: 'https://www.googleapis.com/auth/indexing', aud: SA.token_uri, iat: now, exp: now + 3600 })).toString('base64url');
  const s = crypto.createSign('RSA-SHA256'); s.update(h + '.' + p);
  const jwt = h + '.' + p + '.' + s.sign(SA.private_key, 'base64url');
  return new Promise((resolve, reject) => {
    const body = 'grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Ajwt-bearer&assertion=' + jwt;
    const req = https.request({ hostname: 'oauth2.googleapis.com', path: '/token', method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }, r => {
      let d = ''; r.on('data', c => d += c); r.on('end', () => resolve(JSON.parse(d).access_token));
    });
    req.on('error', reject); req.write(body); req.end();
  });
}

async function submit(token, url) {
  return new Promise(resolve => {
    const body = JSON.stringify({ url, type: 'URL_UPDATED' });
    const req = https.request({ hostname: 'indexing.googleapis.com', path: '/v3/urlNotifications:publish', method: 'POST', headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' } }, r => {
      let d = ''; r.on('data', c => d += c); r.on('end', () => resolve(r.statusCode));
    });
    req.on('error', () => resolve(0)); req.write(body); req.end();
  });
}

const URLS = [
  // nappliancerepair.com
  'https://nappliancerepair.com/',
  'https://nappliancerepair.com/fridge-repair',
  'https://nappliancerepair.com/washer-repair',
  'https://nappliancerepair.com/dryer-repair',
  'https://nappliancerepair.com/dishwasher-repair',
  'https://nappliancerepair.com/oven-repair',
  'https://nappliancerepair.com/stove-repair',
  'https://nappliancerepair.com/toronto',
  'https://nappliancerepair.com/mississauga',
  'https://nappliancerepair.com/brampton',
  'https://nappliancerepair.com/scarborough',
  'https://nappliancerepair.com/north-york',
  'https://nappliancerepair.com/etobicoke',
  'https://nappliancerepair.com/vaughan',
  'https://nappliancerepair.com/markham',
  'https://nappliancerepair.com/richmond-hill',
  'https://nappliancerepair.com/oakville',
  'https://nappliancerepair.com/about',
  'https://nappliancerepair.com/blog',
  'https://nappliancerepair.com/contact',
  // appliancerepairneary.com
  'https://appliancerepairneary.com/',
  'https://appliancerepairneary.com/services/refrigerator-repair',
  'https://appliancerepairneary.com/services/washer-repair',
  'https://appliancerepairneary.com/services/dryer-repair',
  'https://appliancerepairneary.com/services/dishwasher-repair',
  'https://appliancerepairneary.com/services/oven-repair',
  'https://appliancerepairneary.com/services/freezer-repair',
  'https://appliancerepairneary.com/areas/toronto',
  'https://appliancerepairneary.com/areas/mississauga',
  'https://appliancerepairneary.com/areas/brampton',
  'https://appliancerepairneary.com/areas/scarborough',
  'https://appliancerepairneary.com/areas/north-york',
  'https://appliancerepairneary.com/areas/etobicoke',
  'https://appliancerepairneary.com/areas/vaughan',
  'https://appliancerepairneary.com/areas/markham',
  'https://appliancerepairneary.com/areas/richmond-hill',
  'https://appliancerepairneary.com/areas/oakville',
  'https://appliancerepairneary.com/areas/pickering',
  'https://appliancerepairneary.com/areas/ajax',
  'https://appliancerepairneary.com/areas/whitby',
  'https://appliancerepairneary.com/areas/oshawa',
  'https://appliancerepairneary.com/brands/samsung',
  'https://appliancerepairneary.com/brands/lg',
  'https://appliancerepairneary.com/brands/whirlpool',
  'https://appliancerepairneary.com/brands/ge',
  'https://appliancerepairneary.com/brands/bosch',
  'https://appliancerepairneary.com/brands/frigidaire',
  'https://appliancerepairneary.com/brands/kitchenaid',
  'https://appliancerepairneary.com/brands/maytag',
  'https://appliancerepairneary.com/brands/kenmore',
  // fixlifyservices.com
  'https://fixlifyservices.com/',
  'https://fixlifyservices.com/services/refrigerator-repair/',
  'https://fixlifyservices.com/services/washer-repair/',
  'https://fixlifyservices.com/services/dryer-repair/',
  'https://fixlifyservices.com/services/dishwasher-repair/',
  'https://fixlifyservices.com/services/oven-repair/',
  'https://fixlifyservices.com/services/stove-repair/',
  'https://fixlifyservices.com/locations/toronto/',
  'https://fixlifyservices.com/locations/mississauga/',
  'https://fixlifyservices.com/locations/brampton/',
  'https://fixlifyservices.com/locations/scarborough/',
  'https://fixlifyservices.com/locations/north-york/',
  'https://fixlifyservices.com/locations/etobicoke/',
  'https://fixlifyservices.com/locations/vaughan/',
  'https://fixlifyservices.com/locations/markham/',
  'https://fixlifyservices.com/locations/richmond-hill/',
  'https://fixlifyservices.com/locations/oakville/',
  'https://fixlifyservices.com/locations/pickering/',
  'https://fixlifyservices.com/locations/ajax/',
  'https://fixlifyservices.com/brands/samsung/',
  'https://fixlifyservices.com/brands/lg/',
  'https://fixlifyservices.com/brands/whirlpool/',
  'https://fixlifyservices.com/brands/ge/',
  'https://fixlifyservices.com/brands/bosch/',
  'https://fixlifyservices.com/brands/frigidaire/',
  'https://fixlifyservices.com/brands/kenmore/',
  'https://fixlifyservices.com/brands/maytag/',
  'https://fixlifyservices.com/brands/kitchenaid/',
  'https://fixlifyservices.com/emergency/',
  'https://fixlifyservices.com/about/',
  'https://fixlifyservices.com/blog/',
  'https://fixlifyservices.com/pricing/',
];

(async () => {
  console.log('Getting token...');
  const token = await getToken();
  if (!token) { console.log('Failed to get token'); return; }
  console.log('Submitting', URLS.length, 'URLs...\n');
  let ok = 0, fail = 0;
  for (const url of URLS) {
    const status = await submit(token, url);
    if (status === 200) { ok++; process.stdout.write('✅ '); }
    else { fail++; process.stdout.write(`❌(${status}) `); }
    console.log(url.replace(/https:\/\/[^\/]+/, ''));
  }
  console.log(`\nDone: ${ok} submitted, ${fail} failed`);
})().catch(console.error);
