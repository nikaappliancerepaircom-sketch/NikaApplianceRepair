// Simple Service Page Generator for Nika Appliance Repair
const fs = require('fs');
const path = require('path');

// Service data
const services = [
  {
    name: 'Refrigerator Repair',
    slug: 'refrigerator-repair',
    description: 'Professional refrigerator repair service for all makes and models in Toronto & GTA.'
  },
  {
    name: 'Washer Repair',
    slug: 'washer-repair',
    description: 'Expert washing machine repair for top-load, front-load, and stackable units.'
  },
  {
    name: 'Dryer Repair',
    slug: 'dryer-repair',
    description: 'Electric dryer repair service - fast, reliable, and affordable.'
  },
  {
    name: 'Dishwasher Repair',
    slug: 'dishwasher-repair',
    description: 'Professional dishwasher repair for built-in, portable, and countertop models.'
  },
  {
    name: 'Oven Repair',
    slug: 'oven-repair',
    description: 'Electric oven and range repair service by certified technicians.'
  },
  {
    name: 'Stove/Cooktop Repair',
    slug: 'stove-cooktop-repair',
    description: 'Electric stove and cooktop repair - glass top, coil, and induction.'
  },
  {
    name: 'Freezer Repair',
    slug: 'freezer-repair',
    description: 'Standalone and chest freezer repair service throughout Toronto & GTA.'
  }
];

// Create services directory if it doesn't exist
const servicesDir = path.join(__dirname, 'services');
if (!fs.existsSync(servicesDir)) {
  fs.mkdirSync(servicesDir);
}

console.log('Generating service pages...');

// Generate each service page
services.forEach(service => {
  const filename = `${service.slug}.html`;
  const filepath = path.join(servicesDir, filename);
  
  const html = generateServiceHTML(service);
  
  fs.writeFileSync(filepath, html);
  console.log(`✅ Created: services/${filename}`);
});

function generateServiceHTML(service) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="${service.description} Same-day service • Licensed technicians • 90-day warranty • Call 437-747-6737 for $40 OFF!">
    <title>${service.name} Toronto | Same Day Service | Nika Appliance Repair</title>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;500;600;700&family=Rubik:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- Stylesheets -->
    <link rel="stylesheet" href="../css/style.css">
    <style>
        .service-hero {
            background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
            color: white;
            padding: 100px 0 60px;
        }
        .service-hero h1 {
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        .hero-features {
            display: flex;
            gap: 2rem;
            margin: 2rem 0;
            flex-wrap: wrap;
        }
        .hero-features span {
            font-size: 1.1rem;
        }
        .cta-button {
            display: inline-block;
            padding: 15px 30px;
            background: #f59e0b;
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .cta-button:hover {
            background: #d97706;
            transform: translateY(-2px);
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        .content-section {
            padding: 60px 0;
        }
        .problems-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .problem-card {
            background: #f8fafc;
            padding: 25px;
            border-radius: 10px;
            border-left: 4px solid #0ea5e9;
        }
    </style>
</head>
<body>
    <!-- Emergency Bar -->
    <div class="emergency-bar" style="background: #ef4444; color: white; padding: 10px 0; text-align: center;">
        <div class="container">
            <p>🚨 Emergency Service Available 24/7 • Call Now: <a href="tel:437-747-6737" style="color: white; font-weight: bold;">437-747-6737</a></p>
        </div>
    </div>

    <!-- Header -->
    <header style="background: white; box-shadow: 0 2px 10px rgba(0,0,0,0.1); padding: 20px 0; position: sticky; top: 0; z-index: 1000;">
        <div class="container">
            <nav style="display: flex; justify-content: space-between; align-items: center;">
                <a href="/" style="font-size: 1.5rem; font-weight: bold; color: #0ea5e9; text-decoration: none;">Nika Appliance Repair</a>
                <ul style="display: flex; gap: 30px; list-style: none; margin: 0; padding: 0;">
                    <li><a href="/" style="text-decoration: none; color: #333;">Home</a></li>
                    <li><a href="/services/" style="text-decoration: none; color: #333;">Services</a></li>
                    <li><a href="/locations/" style="text-decoration: none; color: #333;">Locations</a></li>
                    <li><a href="/brands/" style="text-decoration: none; color: #333;">Brands</a></li>
                    <li><a href="/emergency/" style="text-decoration: none; color: #333;">Emergency</a></li>
                </ul>
                <a href="tel:437-747-6737" class="cta-button">📞 437-747-6737</a>
            </nav>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="service-hero">
        <div class="container">
            <h1>${service.name} in Toronto & GTA</h1>
            <p style="font-size: 1.3rem; margin-bottom: 2rem;">${service.description}</p>
            <div class="hero-features">
                <span>✅ Same Day Service</span>
                <span>✅ 90-Day Warranty</span>
                <span>✅ Licensed Technicians</span>
                <span>✅ $40 OFF First Repair</span>
            </div>
            <div style="margin-top: 2rem;">
                <a href="tel:437-747-6737" class="cta-button" style="margin-right: 1rem;">📞 Call Now: 437-747-6737</a>
                <a href="#book" class="cta-button" style="background: white; color: #0ea5e9;">Book Online</a>
            </div>
        </div>
    </section>

    <!-- Common Problems Section -->
    <section class="content-section">
        <div class="container">
            <h2 style="font-size: 2.5rem; text-align: center; margin-bottom: 1rem;">Common ${service.name.split(' ')[0]} Problems We Fix</h2>
            <p style="text-align: center; font-size: 1.2rem; color: #666;">Our expert technicians can diagnose and repair all issues</p>
            
            <div class="problems-grid">
                <div class="problem-card">
                    <h3>Not Working Properly</h3>
                    <p>Complete diagnosis and repair of all operational issues</p>
                </div>
                <div class="problem-card">
                    <h3>Strange Noises</h3>
                    <p>Identify and fix unusual sounds during operation</p>
                </div>
                <div class="problem-card">
                    <h3>Error Codes</h3>
                    <p>Expert diagnosis and resolution of all error codes</p>
                </div>
                <div class="problem-card">
                    <h3>Performance Issues</h3>
                    <p>Restore optimal performance and efficiency</p>
                </div>
            </div>
        </div>
    </section>

    <!-- CTA Section -->
    <section style="background: #f59e0b; color: white; padding: 60px 0; text-align: center;">
        <div class="container">
            <h2 style="font-size: 2.5rem; margin-bottom: 1rem;">Need ${service.name} Today?</h2>
            <p style="font-size: 1.3rem; margin-bottom: 2rem;">Get $40 OFF your repair + FREE diagnostic with service!</p>
            <a href="tel:437-747-6737" class="cta-button" style="background: white; color: #f59e0b; font-size: 1.2rem;">📞 Call Now: 437-747-6737</a>
        </div>
    </section>

    <!-- Footer -->
    <footer style="background: #1e293b; color: white; padding: 40px 0; text-align: center;">
        <div class="container">
            <p>&copy; 2024 Nika Appliance Repair. All rights reserved.</p>
            <p style="margin-top: 10px;">Serving Toronto & GTA | Licensed & Insured | 90-Day Warranty</p>
        </div>
    </footer>
</body>
</html>`;
}

console.log('\\n✅ Service page generation complete!');
