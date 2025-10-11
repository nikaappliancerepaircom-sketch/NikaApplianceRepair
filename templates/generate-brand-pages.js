// Brand Page Generator Script
// Run this with Node.js to generate brand pages from template

const fs = require('fs');
const path = require('path');

// Read the template
const templatePath = path.join(__dirname, 'brand-page-template.html');
const template = fs.readFileSync(templatePath, 'utf8');

// Read brand data
const brandDataPath = path.join(__dirname, 'brand-data.json');
const brandData = JSON.parse(fs.readFileSync(brandDataPath, 'utf8'));

// Function to generate service cards HTML
function generateServiceCards(services) {
    return services.map(service => `
                <div class="service-card">
                    <div class="service-icon">
                        <!-- ${service.icon} icon -->
                        <img src="../assets/icons/${service.icon}.svg" alt="${service.title}">
                    </div>
                    <h3>${service.title}</h3>
                    <p>${service.description}</p>
                </div>`).join('');
}

// Function to generate problems list
function generateProblemsList(problems) {
    return `
                <ul class="problems-list">
                    ${problems.map(problem => `<li>${problem}</li>`).join('\n                    ')}
                </ul>`;
}

// Function to generate models list
function generateModelsList(models) {
    return `
                <div class="models-grid">
                    ${models.map(model => `<div class="model-item">${model}</div>`).join('\n                    ')}
                </div>`;
}
// Process each brand
brandData.brands.forEach(brand => {
    let pageContent = template;
    
    // Replace all placeholders
    pageContent = pageContent.replace(/{BRAND_NAME}/g, brand.name);
    pageContent = pageContent.replace(/{BRAND_SLUG}/g, brand.slug);
    pageContent = pageContent.replace(/{BRAND_COLOR_PRIMARY}/g, brand.primary_color);
    pageContent = pageContent.replace(/{BRAND_COLOR_SECONDARY}/g, brand.secondary_color);
    pageContent = pageContent.replace(/{CITY}/g, 'Toronto');
    
    // Generate dynamic content
    const servicesHTML = generateServiceCards(brand.services);
    pageContent = pageContent.replace(/{BRAND_SERVICES_GRID}/g, servicesHTML);
    
    const problemsHTML = generateProblemsList(brand.common_problems);
    pageContent = pageContent.replace(/{BRAND_PROBLEMS_CONTENT}/g, problemsHTML);
    
    const modelsHTML = generateModelsList(brand.popular_models);
    pageContent = pageContent.replace(/{BRAND_MODELS_CONTENT}/g, modelsHTML);
    
    // Create output directory if it doesn't exist
    const outputDir = path.join(__dirname, '..', 'brands');
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
    }
    
    // Write the file
    const outputPath = path.join(outputDir, `${brand.slug}-appliance-repair.html`);
    fs.writeFileSync(outputPath, pageContent);
    
    console.log(`✅ Generated: ${brand.name} page at ${outputPath}`);
});

console.log('\n🎉 All brand pages generated successfully!');

// Instructions for use
console.log('\n📝 To generate pages:');
console.log('1. Make sure Node.js is installed');
console.log('2. Run: node generate-brand-pages.js');
console.log('3. Check the /brands directory for generated pages');