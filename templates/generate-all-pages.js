// Complete Page Generator Script for Nika Appliance Repair
// Generates both brand and location pages from templates

const fs = require('fs');
const path = require('path');

// Read templates
const brandTemplatePath = path.join(__dirname, 'brand-page-template.html');
const brandTemplate = fs.readFileSync(brandTemplatePath, 'utf8');

const locationTemplatePath = path.join(__dirname, 'location-page-template.html');
const locationTemplate = fs.readFileSync(locationTemplatePath, 'utf8');

// Read data files
const brandDataPath = path.join(__dirname, 'brand-data-complete.json');
const brandData = JSON.parse(fs.readFileSync(brandDataPath, 'utf8'));

const locationDataPath = path.join(__dirname, 'location-data.json');
const locationData = JSON.parse(fs.readFileSync(locationDataPath, 'utf8'));

// Helper function to generate service cards for brands
function generateBrandServiceCards(services) {
    return services.map(service => `
                <div class="service-card">
                    <div class="service-icon">
                        <img src="../assets/icons/${service.icon}.svg" alt="${service.title}">
                    </div>
                    <h3>${service.title}</h3>
                    <p>${service.description}</p>
                </div>`).join('');
}

// Helper function to generate problems list
function generateProblemsList(problems) {
    return `
                <div class="problems-grid">
                    ${problems.map(problem => `
                    <div class="problem-item">
                        <span class="problem-icon">⚠️</span>
                        <p>${problem}</p>
                    </div>`).join('')}
                </div>`;
}

// Helper function to generate models list
function generateModelsList(models) {
    return `
                <div class="models-grid">
                    ${models.map(model => `
                    <div class="model-card">
                        <h4>Popular Model</h4>
                        <p>${model}</p>
                    </div>`).join('')}
                </div>`;
}

// Helper function to generate neighborhood list
function generateNeighborhoodsList(neighborhoods) {
    return neighborhoods.map(n => `
                    <div class="neighborhood-item">📍 ${n}</div>`).join('');
}

// Helper function to generate landmarks list
function generateLandmarksList(landmarks) {
    return landmarks.map(l => `
                    <span class="landmark-item">${l}</span>`).join(' • ');
}        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>`);
});

// Add location pages
locationData.locations.forEach(location => {
    sitemapEntries.push(`    <url>
        <loc>https://nikaappliancerepair.ca/locations/${location.slug}</loc>
        <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>`);
});

// Write sitemap entries to file
const sitemapPath = path.join(__dirname, 'sitemap-entries.xml');
fs.writeFileSync(sitemapPath, sitemapEntries.join('\n'));

console.log(`\n📄 Sitemap entries saved to: ${sitemapPath}`);
console.log('   Add these entries to your main sitemap.xml file');