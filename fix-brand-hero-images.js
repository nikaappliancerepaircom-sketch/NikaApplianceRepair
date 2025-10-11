// Fix Hero Images on All Brand Pages
const fs = require('fs');
const path = require('path');

const brandsDir = path.join(__dirname, 'brands');

// CSS files to add to all brand pages
const cssToAdd = `    <!-- Mobile Responsive CSS -->
    <link rel="stylesheet" href="../css/mobile-responsive.css">
    <!-- Floating Icons Fix -->
    <link rel="stylesheet" href="../css/floating-icons-fix.css">
    <!-- Mobile Layout Critical -->
    <link rel="stylesheet" href="../css/mobile-layout-critical.css">
    <!-- Correct Button Colors -->
    <link rel="stylesheet" href="../css/correct-button-colors.css">
    <!-- Brand Hero Fix -->
    <link rel="stylesheet" href="../css/brand-hero-fix.css">`;

// Get all HTML files in brands directory
const brandFiles = fs.readdirSync(brandsDir).filter(file => file.endsWith('.html'));

console.log(`Found ${brandFiles.length} brand pages to update...`);

brandFiles.forEach(file => {
    const filePath = path.join(brandsDir, file);
    let content = fs.readFileSync(filePath, 'utf8');
    
    // Check if already has the CSS files
    if (!content.includes('mobile-responsive.css')) {
        // Find where to insert (after about-redesign.css)
        const insertAfter = 'about-redesign.css">';
        const insertIndex = content.indexOf(insertAfter);
        
        if (insertIndex !== -1) {
            const insertPosition = insertIndex + insertAfter.length;
            content = content.slice(0, insertPosition) + '\n' + cssToAdd + content.slice(insertPosition);
            
            fs.writeFileSync(filePath, content);
            console.log(`✅ Updated: ${file}`);
        } else {
            console.log(`⚠️  Could not find insertion point in: ${file}`);
        }
    } else {
        console.log(`✓ Already updated: ${file}`);
    }
});

console.log('\nDone! All brand pages should now have consistent hero image sizing on mobile.');
