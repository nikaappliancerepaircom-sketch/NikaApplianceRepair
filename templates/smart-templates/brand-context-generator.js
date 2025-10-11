// Brand Context Generator Example
// This shows how to generate unique content for each brand page

const brandContexts = {
  lg: {
    name: "LG",
    primaryColor: "#A50034",
    secondaryColor: "#6B6B6B",
    
    // Unique hero content for LG
    heroContent: {
      badge: "LG SERVICE EXPERTS",
      title: "We're the <span class='highlight'>LG appliance</span> repair experts that will <span class='highlight'>fix</span> your problem... <span class='wow'>FAST!</span>",
      subtitle: "Factory-trained technicians • Genuine LG parts • All LG models",
      trustText: "✅ Smart ThinQ Certified • 90-Day Warranty • All LG Models"
    },
    
    // LG-specific expertise
    expertise: [
      "Smart ThinQ connectivity issues resolved same-day",
      "Factory-trained on latest LG inverter technology",
      "Genuine LG parts inventory for faster repairs",
      "All LG electric appliances serviced"
    ],
    
    // Common LG problems
    commonProblems: [
      {
        appliance: "LG Refrigerators",
        issues: ["Ice maker not working", "Er IF error code", "Temperature fluctuations", "Door seal issues"]
      },
      {
        appliance: "LG Washers", 
        issues: ["OE drain error", "UE unbalanced load", "LE motor error", "Won't spin properly"]
      },
      {
        appliance: "LG Dryers",
        issues: ["d80/d90 vent blocked", "Not heating", "Taking too long to dry", "Sensor dry not working"]
      }
    ],
    
    // LG-specific FAQs
    faqs: [
      {
        question: "Do you fix LG Linear Compressor issues?",
        answer: "We do NOT service Linear Compressor repairs. For these specialized repairs, we recommend contacting LG directly or seeking a specialist who focuses on compressor work."
      },
      {
        question: "Can you fix my LG Smart ThinQ connectivity?",
        answer: "Absolutely! We're certified in Smart ThinQ technology and can resolve WiFi connection issues, app problems, and smart feature malfunctions."
      },
      {
        question: "How much does LG appliance repair cost?",
        answer: "LG repairs typically range from $200-$500 including parts and labor. Complex repairs like linear compressor replacement may cost more. We provide upfront pricing before any work."
      }
    ],
    
    // SEO metadata
    seo: {
      title: "LG Appliance Repair Toronto | Same Day Service | Save $40 - Nika",
      description: "LG appliance repair Toronto ⚡ Same-day service • 90-day warranty • No hidden fees • 5,200+ happy customers • Licensed & insured. Call 437-747-6737 for $40 OFF!",
      keywords: "LG appliance repair Toronto, LG refrigerator repair, LG washer repair, LG dryer repair, LG dishwasher repair, LG smart thinq repair"
    }
  },
  
  samsung: {
    name: "Samsung",
    primaryColor: "#1428A0",
    secondaryColor: "#75787B",
    
    heroContent: {
      badge: "🔧 SAMSUNG CERTIFIED TECHNICIANS",
      title: "Toronto's <span class='highlight'>Samsung appliance</span> repair specialists you can <span class='highlight'>trust</span>",
      subtitle: "Digital Inverter experts • Genuine Samsung parts • All models covered",
      trustText: "✅ FlexWash Certified • Smart Home Ready • Same-Day Service"
    },
    
    expertise: [
      "Digital Inverter technology specialists",
      "FlexWash & FlexDry certified technicians",
      "Samsung Smart Home integration experts",
      "Factory-authorized warranty service"
    ],
    
    commonProblems: [
      {
        appliance: "Samsung Refrigerators",
        issues: ["Ice maker freezing up", "Digital display errors", "Twin Cooling problems", "Water leaking"]
      },
      {
        appliance: "Samsung Washers",
        issues: ["DC error code", "Bearing failure", "Door lock issues", "Vibration problems"]
      },
      {
        appliance: "Samsung Dryers",
        issues: ["HE error code", "Not heating", "Moisture sensor issues", "Belt problems"]
      }
    ],
    
    faqs: [
      {
        question: "Do you service Samsung Digital Inverter appliances?",
        answer: "Yes! Our technicians are specially trained on Samsung's Digital Inverter technology found in their refrigerators and washing machines."
      },
      {
        question: "Can you fix Samsung ice maker problems?",
        answer: "Absolutely. Samsung ice maker issues are one of our specialties. We stock the updated parts to permanently fix common freezing problems."
      },
      {
        question: "Are you authorized by Samsung?",
        answer: "Yes, we're Samsung certified technicians with access to genuine Samsung parts and the latest service bulletins."
      }
    ],
    
    seo: {
      title: "Samsung Appliance Repair Toronto | Certified Service | Save $40",
      description: "Samsung appliance repair Toronto 🔧 Certified technicians • Same-day service • 90-day warranty • 5,200+ satisfied customers. Call 437-747-6737!",
      keywords: "Samsung appliance repair Toronto, Samsung refrigerator repair, Samsung washer repair, Samsung dryer repair, Samsung dishwasher repair"
    }
  },
  
  whirlpool: {
    name: "Whirlpool",
    primaryColor: "#FDB913", 
    secondaryColor: "#003DA5",
    
    heroContent: {
      badge: "🏆 WHIRLPOOL FACTORY TRAINED",
      title: "Your trusted <span class='highlight'>Whirlpool appliance</span> repair experts in Toronto",
      subtitle: "American quality service • Original parts • All Whirlpool models",
      trustText: "✅ 6th Sense Technology • Cabrio Specialists • Licensed & Insured"
    },
    
    // ... continue with Whirlpool-specific content
  }
};

// Function to generate unique page content
function generateBrandPage(brandKey) {
  const context = brandContexts[brandKey];
  
  return {
    // Meta tags
    metaDescription: context.seo.description,
    metaKeywords: context.seo.keywords,
    pageTitle: context.seo.title,
    
    // Brand colors
    primaryColor: context.primaryColor,
    secondaryColor: context.secondaryColor,
    
    // Hero section
    heroContent: `
      <div class="brand-badge">${context.heroContent.badge}</div>
      <h1 class="hero-title">${context.heroContent.title}</h1>
      <p class="hero-subtitle">${context.heroContent.subtitle}</p>
      <p class="hero-trust-text">${context.heroContent.trustText}</p>
    `,
    
    // Services section - dynamically generated
    servicesContent: generateServicesHTML(context),
    
    // Expertise section
    expertiseContent: generateExpertiseHTML(context),
    
    // Problems section
    problemsContent: generateProblemsHTML(context),
    
    // FAQs
    faqContent: generateFAQHTML(context)
  };
}

// Helper functions to generate HTML sections
function generateServicesHTML(context) {
  // Generate unique services grid based on brand
  // Each brand highlights different features
}

function generateExpertiseHTML(context) {
  // Create expertise section with brand-specific points
}

function generateProblemsHTML(context) {
  // List common problems for this brand
}

function generateFAQHTML(context) {
  // Generate FAQ accordion with brand-specific questions
}

// Export for use in page generation
module.exports = { brandContexts, generateBrandPage };