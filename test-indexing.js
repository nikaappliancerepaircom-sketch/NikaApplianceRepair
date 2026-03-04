const fs = require('fs');
const https = require('https');
const crypto = require('crypto');

const env = fs.readFileSync('C:/NikaApplianceRepair/.env', 'utf8');
const match = env.match(/GOOGLE_INDEXING_API_KEY=(\{[\s\S]+?\})\n/);
const SA = JSON.parse(match[1]);

function createJWT(sa) {
  const now = Math.floor(Date.now() / 1000);
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

async function getGoogleTime() {
  return new Promise(resolve => {
    https.request({ hostname: 'www.googleapis.com', path: '/', method: 'HEAD' }, r => {
      const d = r.headers['date'];
      resolve(d ? Math.floor(new Date(d).getTime() / 1000) : Math.floor(Date.now() / 1000));
    }).on('error', () => resolve(Math.floor(Date.now() / 1000))).end();
  });
}

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
  return new Promise(async (resolve, reject) => {
    const now = await getGoogleTime();
    console.log('Google time:', now, '| Local time:', Math.floor(Date.now()/1000), '| Diff:', Math.floor(Date.now()/1000) - now, 's');
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
        console.log('OAuth status:', r.statusCode);
        if (resp.error) console.log('OAuth error:', resp.error, resp.error_description);
        if (resp.access_token) console.log('Token OK:', resp.access_token.substring(0, 20) + '...');
        resolve(resp.access_token);
      });
    });
    req.on('error', reject);
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

const URLS = [
  'https://nappliancerepair.com/',
  'https://appliancerepairneary.com/',
  'https://fixlifyservices.com/',
];

(async () => {
  const token = await getToken();
  if (!token) { console.log('No token, stopping'); return; }
  for (const url of URLS) {
    const r = await submit(token, url);
    console.log(r.status === 200 ? '✅' : '❌', url, r.status, r.body.substring(0, 120));
  }
})().catch(console.error);
