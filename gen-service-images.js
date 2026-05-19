#!/usr/bin/env node
// Generates appliance repair service images via Imagen 4 API
// Saves to both FIXLIFY and NEARY img/ directories

const https = require('https');
const fs = require('fs');
const path = require('path');

const API_KEY = 'AIzaSyBAQoDlAUEKYuJE9dOBejtD5fTP52MciCM';
const MODEL = 'imagen-4.0-fast-generate-001';

const OUTPUT_DIRS = [
  'C:/fixlifyservices/img',
  'C:/appliancerepairneary/img',
];

const IMAGES = [
  {
    filename: 'appliance-technician-hero.webp',
    prompt: 'Professional male appliance repair technician in navy blue uniform with company logo, smiling confidently, holding diagnostic tablet, standing in clean modern Canadian suburban kitchen, natural window light, photorealistic, commercial photography style, 4K',
  },
  {
    filename: 'dishwasher-repair-service.webp',
    prompt: 'Professional appliance repair technician in navy blue uniform kneeling in front of open stainless steel dishwasher, using multimeter to diagnose issue, clean Canadian kitchen background, tool bag open beside him, photorealistic commercial photography, bright natural lighting',
  },
  {
    filename: 'washer-repair-service.webp',
    prompt: 'Appliance repair technician in blue work uniform examining inside of front-load washing machine with diagnostic tool, laundry room setting, service van visible through window, photorealistic, professional commercial photo, bright lighting',
  },
  {
    filename: 'dryer-repair-service.webp',
    prompt: 'Professional technician in navy uniform replacing dryer heating element, hands working on open electric dryer, Canadian home laundry room, OEM parts box visible, photorealistic commercial photography style, bright clean lighting',
  },
  {
    filename: 'fridge-repair-service.webp',
    prompt: 'Appliance repair technician in blue uniform inspecting refrigerator compressor at back of stainless steel fridge, Canadian kitchen setting, diagnostic tools laid out, photorealistic commercial photography, professional lighting',
  },
  {
    filename: 'oven-repair-service.webp',
    prompt: 'Professional appliance technician in navy uniform replacing oven igniter element in stainless steel range oven, Canadian kitchen, tool bag open, OEM parts visible, photorealistic commercial photography style',
  },
  {
    filename: 'stove-repair-service.webp',
    prompt: 'Appliance repair technician testing gas stove burners with diagnostic equipment, professional uniform, modern Canadian kitchen, natural lighting, photorealistic commercial photo quality',
  },
  {
    filename: 'appliance-repair-tools.webp',
    prompt: 'Close-up of professional appliance repair tools laid out neatly: multimeter, screwdrivers, OEM parts in branded packaging, technician hands in background, clean workshop surface, photorealistic product photography style',
  },
  {
    filename: 'appliance-repair-completed.webp',
    prompt: 'Happy Canadian homeowner giving thumbs up next to repaired stainless steel refrigerator, appliance technician in navy uniform smiling beside them, bright clean suburban kitchen, photorealistic commercial photography',
  },
];

function callImagenAPI(prompt) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      instances: [{ prompt }],
      parameters: {
        sampleCount: 1,
        aspectRatio: '16:9',
        outputMimeType: 'image/webp',
      },
    });

    const options = {
      hostname: 'generativelanguage.googleapis.com',
      path: `/v1beta/models/${MODEL}:predict?key=${API_KEY}`,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
      },
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => (data += chunk));
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          if (parsed.predictions && parsed.predictions[0]) {
            const b64 = parsed.predictions[0].bytesBase64Encoded;
            resolve(Buffer.from(b64, 'base64'));
          } else {
            reject(new Error(`API error: ${data.slice(0, 300)}`));
          }
        } catch (e) {
          reject(new Error(`Parse error: ${e.message} | ${data.slice(0, 200)}`));
        }
      });
    });

    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

async function main() {
  // Ensure output dirs exist
  for (const dir of OUTPUT_DIRS) {
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  }

  for (const img of IMAGES) {
    const existing = path.join(OUTPUT_DIRS[0], img.filename);
    if (fs.existsSync(existing)) {
      console.log(`  [SKIP] ${img.filename} already exists`);
      // Copy to second dir if missing
      const dest2 = path.join(OUTPUT_DIRS[1], img.filename);
      if (!fs.existsSync(dest2)) fs.copyFileSync(existing, dest2);
      continue;
    }

    process.stdout.write(`  Generating ${img.filename}... `);
    try {
      const imageBuffer = await callImagenAPI(img.prompt);
      for (const dir of OUTPUT_DIRS) {
        fs.writeFileSync(path.join(dir, img.filename), imageBuffer);
      }
      console.log(`done (${Math.round(imageBuffer.length / 1024)}KB)`);
    } catch (e) {
      console.log(`FAILED: ${e.message}`);
    }

    // Polite rate limit pause
    await new Promise(r => setTimeout(r, 1500));
  }

  console.log('\nAll images generated. Now run inject-service-images.js to add them to HTML pages.');
}

main().catch(console.error);
