#!/usr/bin/env node
// Generates photorealistic branded team photos for all 4 sites via Imagen 4
// NOT stock-looking — candid, real homes, branded t-shirts with site name

const https = require('https');
const fs = require('fs');
const path = require('path');

const API_KEY = process.env.GEMINI_API_KEY || process.env.GOOGLE_AI_API_KEY;
const MODEL = 'imagen-4.0-generate-001'; // High quality, not fast

const LENS = 'Canon EOS R5 35mm f/1.8, natural light, slight bokeh, photojournalistic style, NOT stock photo, NOT studio lighting';
const AVOID = 'Avoid: perfect studio lighting, stock photo pose, fake smile, white background, overly clean';

// Per-site photo sets — branded t-shirts, realistic settings
const SITES = [
  {
    name: 'fixlify',
    brand: 'Fixlify',
    shirtColor: 'navy blue',
    city: 'Edmonton, Alberta',
    outputDir: 'C:/fixlifyservices/img',
    photos: [
      {
        filename: 'tech-hero-fixlify.webp',
        prompt: `Photorealistic photo of a male appliance repair technician, mid-30s, South Asian, wearing a navy blue t-shirt with white text "Fixlify" on the left chest, kneeling in front of an open dishwasher in a real Canadian suburban kitchen, using a multimeter, concentrating on his work, afternoon natural light from kitchen window, slightly cluttered counter in background, candid documentary style. ${LENS}. ${AVOID}.`,
      },
      {
        filename: 'tech-female-fixlify.webp',
        prompt: `Photorealistic photo of a female appliance repair technician, late 20s, white, wearing a navy blue t-shirt with "Fixlify" logo on chest, standing beside an open washing machine in a Canadian laundry room, holding a diagnostic tablet and explaining something, warm interior light, real home setting with laundry basket visible. Candid, natural expression. ${LENS}. ${AVOID}.`,
      },
      {
        filename: 'tech-van-fixlify.webp',
        prompt: `Photorealistic photo of two appliance repair technicians — one male Black mid-40s and one female East Asian late-20s — both wearing navy blue "Fixlify" t-shirts, standing beside a white service van on a residential Edmonton street, loading tools into the van, overcast Canadian sky, mature trees in background, natural candid moment. ${LENS}. ${AVOID}.`,
      },
      {
        filename: 'tech-oven-fixlify.webp',
        prompt: `Photorealistic close-up photo: appliance technician's hands in navy blue "Fixlify" shirt sleeves, replacing an oven igniter element inside a stainless steel oven, OEM part box on the kitchen floor beside him, tools laid out on a cloth, harsh natural work lighting, real grease and wear on the oven interior. Authentic, not staged. ${LENS}. ${AVOID}.`,
      },
      {
        filename: 'tech-customer-fixlify.webp',
        prompt: `Photorealistic photo of a male appliance repair technician in navy "Fixlify" t-shirt shaking hands with a middle-aged white Canadian woman homeowner in her kitchen, both smiling naturally — the repaired refrigerator is open in the background showing it's working again, warm late afternoon light, real Canadian suburban kitchen decor. ${LENS}. ${AVOID}.`,
      },
      {
        filename: 'tech-fridge-fixlify.webp',
        prompt: `Photorealistic photo of a male appliance technician in navy blue "Fixlify" shirt crouching behind a pulled-out stainless steel refrigerator, working on the compressor with a wrench, Edmonton home with hardwood floors visible, tool bag open on the floor, focused expression, natural window light from the side. Documentary-style photography. ${LENS}. ${AVOID}.`,
      },
    ],
  },
  {
    name: 'neary',
    brand: 'Neary',
    shirtColor: 'dark green',
    city: 'Calgary, Alberta',
    outputDir: 'C:/appliancerepairneary/img',
    photos: [
      {
        filename: 'tech-hero-neary.webp',
        prompt: `Photorealistic photo of a male appliance repair technician, early 40s, white with beard, wearing a dark green t-shirt with white "Neary" text on left chest, crouching in front of an open dishwasher in a modern Calgary kitchen with quartz countertops, using a phone flashlight to inspect the interior, natural morning light, real home setting. Candid documentary style. ${LENS}. ${AVOID}.`,
      },
      {
        filename: 'tech-female-neary.webp',
        prompt: `Photorealistic photo of a female appliance repair technician, mid-30s, Hispanic, wearing a dark green t-shirt with "Neary" on the chest, kneeling beside a front-load washer in a Calgary home laundry room, replacing a door gasket, concentration on her face, real wear on the machine, natural light, tool bag open. Authentic candid shot. ${LENS}. ${AVOID}.`,
      },
      {
        filename: 'tech-van-neary.webp',
        prompt: `Photorealistic photo of an appliance repair technician, male, South Asian, late 30s, wearing a dark green "Neary" t-shirt, leaning against a white cargo van on a Calgary residential street with Chinook arch visible in the sky, checking his phone schedule, winter jacket on the van seat visible through window, casual natural moment. ${LENS}. ${AVOID}.`,
      },
      {
        filename: 'tech-washer-neary.webp',
        prompt: `Photorealistic close-up photo: appliance repair technician in dark green "Neary" shirt examining a top-load washer's agitator, one hand inside the drum, other hand writing notes on a clipboard, real Canadian basement laundry room with concrete walls, fluorescent light mixed with natural light from small window. Not staged, real work. ${LENS}. ${AVOID}.`,
      },
      {
        filename: 'tech-customer-neary.webp',
        prompt: `Photorealistic photo of a female appliance technician in dark green "Neary" t-shirt explaining the repair bill on a tablet to an older Canadian couple in their Calgary kitchen, repaired stainless steel oven visible behind them, warm kitchen light, genuine expressions, real home environment with family photos on the wall. ${LENS}. ${AVOID}.`,
      },
      {
        filename: 'tech-fridge-neary.webp',
        prompt: `Photorealistic photo of a male technician in dark green "Neary" t-shirt standing at the open refrigerator door, pointing at something inside while talking to a homeowner off-camera, Calgary kitchen with tile backsplash, afternoon sunlight through window, toolbag on the floor. Natural candid documentary photo. ${LENS}. ${AVOID}.`,
      },
    ],
  },
  {
    name: 'nika',
    brand: 'Nika',
    shirtColor: 'charcoal grey',
    city: 'Toronto, Ontario',
    outputDir: 'C:/NikaApplianceRepair/img',
    photos: [
      {
        filename: 'tech-hero-nika.webp',
        prompt: `Photorealistic photo of a male appliance repair technician, mid-30s, East Asian, wearing a charcoal grey t-shirt with white "Nika" text on left chest, sitting on the kitchen floor of a Toronto condo, laptop open beside him with diagnostic software, fixing a dishwasher control board, city apartment aesthetic with modern kitchen, evening indoor light. Candid professional photo. ${LENS}. ${AVOID}.`,
      },
      {
        filename: 'tech-female-nika.webp',
        prompt: `Photorealistic photo of a female appliance repair technician, late 20s, Black, wearing a charcoal grey "Nika" t-shirt, using a socket wrench on a washer panel in a Toronto home laundry closet, focused expression, tight urban space, natural light from doorway. Documentary photography style, not posed. ${LENS}. ${AVOID}.`,
      },
      {
        filename: 'tech-van-nika.webp',
        prompt: `Photorealistic photo of two appliance repair technicians — male white early-40s and female Filipino late-20s — both in charcoal "Nika" t-shirts, walking from their service van toward a Toronto semi-detached home, one carrying a tool bag, Toronto street with parked cars and trees, overcast Ontario sky. Natural candid moment. ${LENS}. ${AVOID}.`,
      },
      {
        filename: 'tech-dryer-nika.webp',
        prompt: `Photorealistic photo of a male technician in charcoal "Nika" t-shirt using a voltage meter on a disassembled electric dryer heating element, Toronto basement laundry room, wood panelling, single bulb light, tools spread on newspaper on the floor, focused authentic work scene. ${LENS}. ${AVOID}.`,
      },
      {
        filename: 'tech-customer-nika.webp',
        prompt: `Photorealistic photo of a male appliance technician in charcoal "Nika" t-shirt receiving payment on a card reader from a young couple in a modern Toronto kitchen, smiling naturally, fixed washing machine visible through laundry room door, warm kitchen light, urban condo feel. ${LENS}. ${AVOID}.`,
      },
    ],
  },
  {
    name: 'nar',
    brand: 'N Appliance',
    shirtColor: 'royal blue',
    city: 'Richmond Hill, Ontario',
    outputDir: 'C:/nappliancerepair/img',
    photos: [
      {
        filename: 'tech-hero-nar.webp',
        prompt: `Photorealistic photo of a male appliance repair technician, early 40s, Middle Eastern, wearing a royal blue t-shirt with white "N Appliance" text on left chest, kneeling beside an open refrigerator in a Richmond Hill Ontario suburban kitchen, replacing a water filter, large suburban kitchen with granite counters, natural light. Candid documentary photo. ${LENS}. ${AVOID}.`,
      },
      {
        filename: 'tech-female-nar.webp',
        prompt: `Photorealistic photo of a female appliance repair technician, mid-30s, South Asian, wearing a royal blue "N Appliance" t-shirt, repairing a dishwasher spray arm in a York Region suburban home kitchen, kneeling on tile floor, tool bag open, natural afternoon light through window. Authentic candid work photo. ${LENS}. ${AVOID}.`,
      },
      {
        filename: 'tech-van-nar.webp',
        prompt: `Photorealistic photo of an appliance technician in royal blue "N Appliance" t-shirt loading equipment into a white service van on a quiet Richmond Hill residential street, mature oak trees, brick homes, Canadian suburban street, overcast spring day. Natural documentary moment. ${LENS}. ${AVOID}.`,
      },
      {
        filename: 'tech-customer-nar.webp',
        prompt: `Photorealistic photo of a male appliance technician in royal blue "N Appliance" t-shirt reviewing repair paperwork on a clipboard with a middle-aged South Asian woman homeowner in a Richmond Hill kitchen, both looking at the form, warm kitchen light, relaxed natural expressions. ${LENS}. ${AVOID}.`,
      },
    ],
  },
];

function callImagenAPI(prompt) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      instances: [{ prompt }],
      parameters: {
        sampleCount: 1,
        aspectRatio: '4:3',
        outputMimeType: 'image/webp',
        personGeneration: 'allow_adult',
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
          if (parsed.predictions && parsed.predictions[0] && parsed.predictions[0].bytesBase64Encoded) {
            resolve(Buffer.from(parsed.predictions[0].bytesBase64Encoded, 'base64'));
          } else {
            // Try raiFilteredReason
            const reason = parsed.predictions?.[0]?.raiFilteredReason || 'unknown';
            reject(new Error(`Filtered/no image: ${reason} | ${data.slice(0, 200)}`));
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
  const targetSite = process.argv[2]; // optional: 'fixlify', 'neary', 'nika', 'nar' — or omit for all

  for (const site of SITES) {
    if (targetSite && site.name !== targetSite) continue;

    console.log(`\n=== ${site.brand} (${site.city}) ===`);
    if (!fs.existsSync(site.outputDir)) {
      fs.mkdirSync(site.outputDir, { recursive: true });
    }

    for (const photo of site.photos) {
      const outPath = path.join(site.outputDir, photo.filename);
      if (fs.existsSync(outPath)) {
        console.log(`  [SKIP] ${photo.filename} already exists`);
        continue;
      }

      process.stdout.write(`  Generating ${photo.filename}... `);
      try {
        const buf = await callImagenAPI(photo.prompt);
        fs.writeFileSync(outPath, buf);
        console.log(`✓ (${Math.round(buf.length / 1024)}KB)`);
      } catch (e) {
        console.log(`✗ FAILED: ${e.message.slice(0, 120)}`);
        // Try backup key
        const originalKey = API_KEY;
        // Could add retry with backup key here if needed
      }

      await new Promise(r => setTimeout(r, 2000)); // 2s between calls
    }
  }

  console.log('\nDone. Run inject-team-photos.js to add to pages.');
}

main().catch(console.error);
