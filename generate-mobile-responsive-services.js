// Updated Service Page Generator with Mobile Responsive Design
const fs = require('fs');
const path = require('path');

// Service data
const services = [
  {
    name: 'Refrigerator Repair',
    slug: 'refrigerator-repair',
    description: 'Professional refrigerator repair service for all makes and models in Toronto & GTA.',
    problems: ['Not cooling', 'Ice maker issues', 'Water leaking', 'Strange noises', 'Door seal problems', 'Temperature fluctuations'],
    brands: ['Samsung', 'LG', 'Whirlpool', 'GE', 'Frigidaire', 'KitchenAid', 'Maytag', 'Bosch']
  },
  {
    name: 'Washer Repair',
    slug: 'washer-repair',
    description: 'Expert washing machine repair for top-load, front-load, and stackable units.',
    problems: ['Not draining', 'Not spinning', 'Leaking water', 'Error codes', 'Door won\'t lock', 'Excessive vibration'],
    brands: ['Samsung', 'LG', 'Whirlpool', 'GE', 'Maytag', 'Kenmore', 'Frigidaire', 'Electrolux']
  },
  {
    name: 'Dryer Repair',
    slug: 'dryer-repair',
    description: 'Electric dryer repair service - fast, reliable, and affordable.',
    problems: ['Not heating', 'Taking too long', 'Not tumbling', 'Making noises', 'Door issues', 'Thermal fuse blown'],
    brands: ['Samsung', 'LG', 'Whirlpool', 'GE', 'Maytag', 'Kenmore', 'Frigidaire', 'Electrolux']
  },
  {
    name: 'Dishwasher Repair',
    slug: 'dishwasher-repair',
    description: 'Professional dishwasher repair for built-in, portable, and countertop models.',
    problems: ['Not cleaning', 'Not draining', 'Leaking water', 'Door latch broken', 'Control panel issues', 'Spray arm problems'],
    brands: ['Bosch', 'KitchenAid', 'Whirlpool', 'GE', 'Samsung', 'LG', 'Maytag', 'Frigidaire']
  },
  {
    name: 'Oven Repair',
    slug: 'oven-repair',
    description: 'Electric oven and range repair service by certified technicians.',
    problems: ['Not heating', 'Temperature inaccurate', 'Broiler not working', 'Self-clean issues', 'Control panel problems', 'Door won\'t close'],
    brands: ['GE', 'Whirlpool', 'Samsung', 'LG', 'Frigidaire', 'KitchenAid', 'Bosch', 'Electrolux']
  },
  {
    name: 'Stove/Cooktop Repair',
    slug: 'stove-cooktop-repair',
    description: 'Electric stove and cooktop repair - glass top, coil, and induction.',
    problems: ['Burners not heating', 'Uneven heating', 'Glass top cracked', 'Control knobs broken', 'Indicator lights out', 'Surface element issues'],
    brands: ['GE', 'Whirlpool', 'Samsung', 'Frigidaire', 'KitchenAid', 'Bosch', 'Electrolux', 'Maytag']
  },
  {
    name: 'Freezer Repair',
    slug: 'freezer-repair',
    description: 'Standalone and chest freezer repair service throughout Toronto & GTA.',
    problems: ['Not freezing', 'Frost buildup', 'Temperature issues', 'Compressor problems', 'Door seal damaged', 'Strange noises'],
    brands: ['Frigidaire', 'GE', 'Whirlpool', 'Kenmore', 'Danby', 'Kelvinator', 'Maytag', 'Haier']
  }
];

// Create services directory if it doesn't exist
const servicesDir = path.join(__dirname, 'services');
if (!fs.existsSync(servicesDir)) {
  fs.mkdirSync(servicesDir);
}

console.log('Generating mobile-responsive service pages...');

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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- Stylesheets -->
    <link rel="stylesheet" href="../css/style.css">
    <link rel="stylesheet" href="../css/mobile-responsive.css">
    
    <style>
        /* Mobile-First Design */
        * {
            box-sizing: border-box;
        }
        
        body {
            margin: 0;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            overflow-x: hidden;
        }
        
        .container {
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        /* Emergency Bar */
        .emergency-bar {
            background: #ef4444;
            color: white;
            padding: 8px 15px;
            text-align: center;
            font-size: 14px;
        }
        
        .emergency-bar a {
            color: white;
            font-weight: bold;
            text-decoration: none;
        }
        
        /* Header */
        header {
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 15px 0;
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        
        nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }
        
        .logo {
            font-size: 1.25rem;
            font-weight: bold;
            color: #0ea5e9;
            text-decoration: none;
        }
        
        .nav-menu {
            display: none;
            list-style: none;
            gap: 20px;
            margin: 0;
            padding: 0;
        }
        
        .mobile-menu-btn {
            display: block;
            background: none;
            border: none;
            font-size: 24px;
            cursor: pointer;
            padding: 5px;
        }
        
        /* Hero Section */
        .service-hero {
            background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
            color: white;
            padding: 60px 0 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .service-hero h1 {
            font-size: 1.875rem;
            line-height: 1.2;
            margin-bottom: 1rem;
        }
        
        .hero-description {
            font-size: 1.1rem;
            margin-bottom: 1.5rem;
            opacity: 0.95;
        }
        
        .hero-features {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
            margin-bottom: 1.5rem;
        }
        
        .hero-features span {
            font-size: 0.875rem;
            padding: 5px 12px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 20px;
        }
        
        .hero-cta {
            display: flex;
            flex-direction: column;
            gap: 10px;
            align-items: center;
        }
        
        .cta-button {
            display: inline-block;
            padding: 12px 24px;
            background: #f59e0b;
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            font-size: 0.875rem;
            transition: all 0.3s ease;
            white-space: nowrap;
        }
        
        .cta-button.secondary {
            background: white;
            color: #0ea5e9;
        }
        
        .cta-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        /* Content Sections */
        .content-section {
            padding: 40px 0;
        }
        
        h2 {
            font-size: 1.75rem;
            text-align: center;
            margin-bottom: 1rem;
            color: #0f172a;
        }
        
        .section-subtitle {
            text-align: center;
            font-size: 1rem;
            color: #64748b;
            margin-bottom: 2rem;
        }
        
        /* Problems Grid */
        .problems-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 15px;
        }
        
        .problem-card {
            background: #f8fafc;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #0ea5e9;
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .problem-icon {
            font-size: 1.5rem;
            flex-shrink: 0;
        }
        
        /* Brands Section */
        .brands-section {
            background: #f8fafc;
        }
        
        .brands-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            justify-content: center;
        }
        
        .brand-tag {
            background: white;
            padding: 8px 16px;
            border-radius: 25px;
            border: 2px solid #e2e8f0;
            font-size: 0.875rem;
        }
        
        /* CTA Section */
        .cta-section {
            background: #f59e0b;
            color: white;
            padding: 40px 0;
            text-align: center;
        }
        
        .cta-section h2 {
            color: white;
            margin-bottom: 0.5rem;
        }
        
        .cta-section p {
            font-size: 1.1rem;
            margin-bottom: 1.5rem;
        }
        
        /* Footer */
        footer {
            background: #1e293b;
            color: white;
            padding: 40px 0 20px;
            text-align: center;
        }
        
        footer p {
            margin: 5px 0;
            color: #94a3b8;
        }
        
        /* Tablet Styles */
        @media (min-width: 640px) {
            .problems-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .hero-cta {
                flex-direction: row;
                justify-content: center;
            }
        }
        
        /* Desktop Styles */
        @media (min-width: 768px) {
            .emergency-bar {
                font-size: 16px;
                padding: 10px 0;
            }
            
            header {
                padding: 20px 0;
            }
            
            .logo {
                font-size: 1.5rem;
            }
            
            .nav-menu {
                display: flex !important;
            }
            
            .nav-menu a {
                text-decoration: none;
                color: #334155;
                font-weight: 500;
                transition: color 0.3s ease;
            }
            
            .nav-menu a:hover {
                color: #0ea5e9;
            }
            
            .mobile-menu-btn {
                display: none;
            }
            
            .service-hero {
                padding: 80px 0 60px;
                text-align: left;
            }
            
            .service-hero h1 {
                font-size: 2.5rem;
            }
            
            .hero-features {
                justify-content: flex-start;
            }
            
            .hero-features span {
                font-size: 1rem;
            }
            
            .cta-button {
                font-size: 1rem;
                padding: 15px 30px;
            }
            
            .content-section {
                padding: 60px 0;
            }
            
            h2 {
                font-size: 2rem;
            }
            
            .problems-grid {
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
            }
            
            .cta-section {
                padding: 60px 0;
            }
        }
        
        /* Large Desktop */
        @media (min-width: 1024px) {
            .service-hero h1 {
                font-size: 3rem;
            }
            
            h2 {
                font-size: 2.5rem;
            }
            
            .hero-description {
                font-size: 1.25rem;
            }
        }
        
        /* Prevent horizontal scroll */
        html, body {
            overflow-x: hidden;
            width: 100%;
        }
        
        /* Ensure all content stays within viewport */
        section {
            overflow-x: hidden;
        }
    </style>
</head>
<body>
    <!-- Emergency Bar -->
    <div class="emergency-bar">
        <div class="container">
            <p>🚨 Emergency Service Available 24/7 • Call Now: <a href="tel:437-747-6737">437-747-6737</a></p>
        </div>
    </div>

    <!-- Header -->
    <header>
        <div class="container">
            <nav>
                <a href="/" class="logo">Nika Appliance Repair</a>
                <ul class="nav-menu">
                    <li><a href="/">Home</a></li>
                    <li><a href="/services/">Services</a></li>
                    <li><a href="/locations/">Locations</a></li>
                    <li><a href="/brands/">Brands</a></li>
                    <li><a href="/emergency/">Emergency</a></li>
                </ul>
                <button class="mobile-menu-btn">☰</button>
                <a href="tel:437-747-6737" class="cta-button">📞 437-747-6737</a>
            </nav>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="service-hero">
        <div class="container">
            <h1>${service.name} in Toronto & GTA</h1>
            <p class="hero-description">${service.description}</p>
            <div class="hero-features">
                <span>✅ Same Day Service</span>
                <span>✅ 90-Day Warranty</span>
                <span>✅ Licensed Technicians</span>
                <span>✅ $40 OFF First Repair</span>
            </div>
            <div class="hero-cta">
                <a href="tel:437-747-6737" class="cta-button">📞 Call Now: 437-747-6737</a>
                <a href="#book" class="cta-button secondary">Book Online</a>
            </div>
        </div>
    </section>

    <!-- Common Problems Section -->
    <section class="content-section">
        <div class="container">
            <h2>Common ${service.name.split(' ')[0]} Problems We Fix</h2>
            <p class="section-subtitle">Our expert technicians can diagnose and repair all issues</p>
            
            <div class="problems-grid">
                ${service.problems.map(problem => `
                <div class="problem-card">
                    <span class="problem-icon">⚠️</span>
                    <div>
                        <h3 style="margin: 0; font-size: 1.1rem;">${problem}</h3>
                        <p style="margin: 5px 0 0 0; color: #64748b; font-size: 0.875rem;">Fast & reliable repair</p>
                    </div>
                </div>
                `).join('')}
            </div>
        </div>
    </section>

    <!-- Brands Section -->
    <section class="content-section brands-section">
        <div class="container">
            <h2>Brands We Service</h2>
            <p class="section-subtitle">Factory-authorized repairs for all major brands</p>
            
            <div class="brands-grid">
                ${service.brands.map(brand => `<span class="brand-tag">✓ ${brand}</span>`).join('')}
            </div>
        </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
        <div class="container">
            <h2>Need ${service.name} Today?</h2>
            <p>Get $40 OFF your repair + FREE diagnostic with service!</p>
            <a href="tel:437-747-6737" class="cta-button" style="background: white; color: #f59e0b;">📞 Call Now: 437-747-6737</a>
        </div>
    </section>

    <!-- Footer -->
    <footer>
        <div class="container">
            <p>&copy; 2024 Nika Appliance Repair. All rights reserved.</p>
            <p>Serving Toronto & GTA | Licensed & Insured | 90-Day Warranty</p>
        </div>
    </footer>

    <script>
        // Mobile menu toggle
        document.querySelector('.mobile-menu-btn').addEventListener('click', function() {
            const menu = document.querySelector('.nav-menu');
            menu.style.display = menu.style.display === 'flex' ? 'none' : 'flex';
        });
    </script>
</body>
</html>`;
}

console.log('\\n✅ Mobile-responsive service page generation complete!');
