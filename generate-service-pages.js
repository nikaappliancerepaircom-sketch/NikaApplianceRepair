// Generate Service Pages for Nika Appliance Repair
const fs = require('fs');
const path = require('path');

// Service data
const services = [
  {
    name: 'Refrigerator Repair',
    slug: 'refrigerator-repair',
    icon: 'refrigerator',
    description: 'Professional refrigerator repair service for all makes and models in Toronto & GTA.',
    problems: [
      'Not cooling properly',
      'Ice maker not working',
      'Water leaking',
      'Strange noises',
      'Door seal issues',
      'Temperature fluctuations'
    ],
    brands: ['Samsung', 'LG', 'Whirlpool', 'GE', 'Frigidaire', 'KitchenAid', 'Maytag', 'Bosch'],
    priceRange: '$150-$400',
    avgRepairTime: '1-2 hours'
  },
  {
    name: 'Washer Repair',
    slug: 'washer-repair',
    icon: 'washer',
    description: 'Expert washing machine repair for top-load, front-load, and stackable units.',
    problems: [
      'Not draining',
      'Not spinning',
      'Leaking water',
      'Error codes',
      'Door won\'t lock',
      'Excessive vibration'
    ]
  }
];
    brands: ['Samsung', 'LG', 'Whirlpool', 'GE', 'Maytag', 'Kenmore', 'Frigidaire', 'Electrolux'],
    priceRange: '$120-$350',
    avgRepairTime: '1-2 hours'
  },
  {
    name: 'Dryer Repair',
    slug: 'dryer-repair',
    icon: 'dryer',
    description: 'Electric dryer repair service - fast, reliable, and affordable.',
    problems: [
      'Not heating',
      'Taking too long to dry',
      'Not tumbling',
      'Making loud noises',
      'Door issues',
      'Thermal fuse blown'
    ],
    brands: ['Samsung', 'LG', 'Whirlpool', 'GE', 'Maytag', 'Kenmore', 'Frigidaire', 'Electrolux'],
    priceRange: '$100-$300',
    avgRepairTime: '1 hour'
  },
  {
    name: 'Dishwasher Repair',
    slug: 'dishwasher-repair',
    icon: 'dishwasher',
    description: 'Professional dishwasher repair for built-in, portable, and countertop models.',
    problems: [
      'Not cleaning dishes',
      'Not draining',
      'Leaking water',
      'Door latch broken',
      'Control panel issues',
      'Spray arm problems'
    ]
  }
];
    brands: ['Bosch', 'KitchenAid', 'Whirlpool', 'GE', 'Samsung', 'LG', 'Maytag', 'Frigidaire'],
    priceRange: '$120-$350',
    avgRepairTime: '1-2 hours'
  },
  {
    name: 'Oven Repair',
    slug: 'oven-repair',
    icon: 'oven',
    description: 'Electric oven and range repair service by certified technicians.',
    problems: [
      'Not heating properly',
      'Temperature inaccurate',
      'Broiler not working',
      'Self-clean issues',
      'Control panel problems',
      'Door won\'t close'
    ],
    brands: ['GE', 'Whirlpool', 'Samsung', 'LG', 'Frigidaire', 'KitchenAid', 'Bosch', 'Electrolux'],
    priceRange: '$150-$400',
    avgRepairTime: '1-2 hours'
  },
  {
    name: 'Stove/Cooktop Repair',
    slug: 'stove-cooktop-repair',
    icon: 'stove',
    description: 'Electric stove and cooktop repair - glass top, coil, and induction.',
    problems: [
      'Burners not heating',
      'Uneven heating',
      'Glass top cracked',
      'Control knobs broken',
      'Indicator lights out',
      'Surface element issues'
    ]
  }
];
    brands: ['GE', 'Whirlpool', 'Samsung', 'Frigidaire', 'KitchenAid', 'Bosch', 'Electrolux', 'Maytag'],
    priceRange: '$150-$400',
    avgRepairTime: '1-2 hours'
  },
  {
    name: 'Freezer Repair',
    slug: 'freezer-repair',
    icon: 'freezer',
    description: 'Standalone and chest freezer repair service throughout Toronto & GTA.',
    problems: [
      'Not freezing',
      'Frost buildup',
      'Temperature issues',
      'Compressor problems',
      'Door seal damaged',
      'Strange noises'
    ],
    brands: ['Frigidaire', 'GE', 'Whirlpool', 'Kenmore', 'Danby', 'Kelvinator', 'Maytag', 'Haier'],
    priceRange: '$150-$400',
    avgRepairTime: '1-2 hours'
  }
];

// Read service template
const templatePath = path.join(__dirname, 'templates', 'service-template.html');
let template;

try {
  template = fs.readFileSync(templatePath, 'utf8');
} catch (error) {
  console.error('Error reading template:', error);
  console.log('Creating basic service template...');
  
  // Create a basic template if the file doesn't exist
  template = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{{description}} Same-day service • Licensed technicians • 90-day warranty • Call 437-747-6737 for $40 OFF!">
    <meta name="keywords" content="{{slug}} Toronto, {{name}} GTA, appliance repair">
    <title>{{name}} Toronto | Same Day Service | Nika Appliance Repair</title>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;500;600;700&family=Rubik:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- Stylesheets -->
    <link rel="stylesheet" href="../css/style.css">
    <link rel="stylesheet" href="../css/service-pages.css">
</head>
<body>
    <!-- Emergency Bar -->
    <div class="emergency-bar">
        <div class="container">
            <p>🚨 Emergency Service Available 24/7 • Call Now: <a href="tel:437-747-6737" class="emergency-phone">437-747-6737</a></p>
        </div>
    </div>

    <!-- Header -->
    <header>
        <div class="container">
            <nav>
                <a href="/" class="logo">
                    <img src="../assets/images/logo.png" alt="Nika Appliance Repair">
                </a>
                <ul class="nav-menu">
                    <li><a href="/">Home</a></li>
                    <li class="dropdown">
                        <a href="/services/">Services</a>
                    </li>
                    <li><a href="/locations/">Locations</a></li>
                    <li><a href="/brands/">Brands</a></li>
                    <li><a href="/emergency/">Emergency</a></li>
                    <li><a href="/contact/">Contact</a></li>
                </ul>
                <a href="tel:437-747-6737" class="cta-button">📞 437-747-6737</a>
            </nav>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="service-hero">
        <div class="container">
            <div class="hero-content">
                <h1>{{name}} in Toronto & GTA</h1>
                <p class="hero-description">{{description}}</p>
                <div class="hero-features">
                    <span>✅ Same Day Service</span>
                    <span>✅ 90-Day Warranty</span>
                    <span>✅ Licensed Technicians</span>
                    <span>✅ $40 OFF First Repair</span>
                </div>
                <div class="hero-cta">
                    <a href="tel:437-747-6737" class="cta-button primary">Call Now: 437-747-6737</a>
                    <a href="#booking-form" class="cta-button secondary">Book Online</a>
                </div>
            </div>
            <div class="hero-form">
                <form class="quick-quote-form">
                    <h3>Get $40 OFF Your Repair</h3>
                    <input type="text" name="name" placeholder="Your Name" required>
                    <input type="tel" name="phone" placeholder="Phone Number" required>
                    <select name="appliance" required>
                        <option value="">Select Appliance</option>
                        <option value="refrigerator">Refrigerator</option>
                        <option value="washer">Washer</option>
                        <option value="dryer">Dryer</option>
                        <option value="dishwasher">Dishwasher</option>
                        <option value="oven">Oven</option>
