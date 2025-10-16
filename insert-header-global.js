/**
 * Global Header Insertion Script
 * Automatically inserts SEO header from index.html into all service and location pages
 * Run with: node insert-header-global.js
 */

const fs = require('fs');
const path = require('path');

// Files to update
const FILES_TO_UPDATE = [
    // Service pages
    'services/dryer-repair.html',
    'services/freezer-repair.html',
    'services/microwave-repair.html',
    'services/oven-repair.html',
    'services/range-repair.html',
    'services/refrigerator-repair.html',
    'services/stove-repair.html',
    'services/washer-repair.html',
    // Location pages
    'locations/ajax.html',
    'locations/brampton.html',
    'locations/burlington.html',
    'locations/markham.html',
    'locations/milton.html',
    'locations/mississauga.html',
    'locations/oakville.html',
    'locations/oshawa.html',
    'locations/pickering.html',
    'locations/richmond-hill.html',
    'locations/toronto.html',
    'locations/vaughan.html'
];

// Read the header from dishwasher-repair.html (which has been updated)
function extractHeader() {
    const sourceFile = path.join(__dirname, 'services', 'dishwasher-repair.html');
    const content = fs.readFileSync(sourceFile, 'utf8');

    // Extract from skip-to-content through the closing </script> tag after toggleMenu function
    const startMarker = '<!-- Skip to main content link for accessibility -->';
    const endMarker = '</script>\n\n    <!-- Breadcrumb Navigation -->';

    const startIndex = content.indexOf(startMarker);
    const endIndex = content.indexOf(endMarker);

    if (startIndex === -1 || endIndex === -1) {
        throw new Error('Could not find header markers in source file');
    }

    return content.substring(startIndex, endIndex + '</script>'.length);
}

// Replace header in a file
function replaceHeaderInFile(filePath, headerContent) {
    const fullPath = path.join(__dirname, filePath);

    if (!fs.existsSync(fullPath)) {
        console.log(`❌ File not found: ${filePath}`);
        return false;
    }

    let content = fs.readFileSync(fullPath, 'utf8');

    // Find the section to replace
    const startMarker = '<!-- Skip to main content link for accessibility -->';
    const endMarker1 = '<div id="header-placeholder"></div>';
    const endMarker2 = '<!-- Breadcrumb Navigation -->';

    const startIndex = content.indexOf(startMarker);
    let endIndex = content.indexOf(endMarker1);

    // If header-placeholder exists, remove it
    if (endIndex !== -1) {
        endIndex = content.indexOf('\n', endIndex) + 1;
    } else {
        // Otherwise, insert before breadcrumb
        endIndex = content.indexOf(endMarker2);
        if (endIndex === -1) {
            console.log(`❌ Could not find insertion point in: ${filePath}`);
            return false;
        }
    }

    if (startIndex === -1) {
        console.log(`❌ Could not find start marker in: ${filePath}`);
        return false;
    }

    // Replace the section
    const newContent = content.substring(0, startIndex) +
                      headerContent +
                      '\n\n    ' +
                      content.substring(endIndex);

    // Write back to file
    fs.writeFileSync(fullPath, newContent, 'utf8');
    console.log(`✅ Updated: ${filePath}`);
    return true;
}

// Main execution
try {
    console.log('🔧 Extracting SEO header from dishwasher-repair.html...\n');
    const headerContent = extractHeader();
    console.log(`✅ Extracted ${headerContent.length} characters\n`);

    console.log('📝 Updating files...\n');
    let successCount = 0;
    let failCount = 0;

    FILES_TO_UPDATE.forEach(filePath => {
        if (replaceHeaderInFile(filePath, headerContent)) {
            successCount++;
        } else {
            failCount++;
        }
    });

    console.log(`\n✅ Successfully updated: ${successCount} files`);
    if (failCount > 0) {
        console.log(`❌ Failed to update: ${failCount} files`);
    }

    console.log('\n🎉 Done! All files now have the unified SEO header.');
    console.log('📝 Next step: git add . && git commit && git push');

} catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
}
