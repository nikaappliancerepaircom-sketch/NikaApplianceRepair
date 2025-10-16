/**
 * Global Header & Footer Insertion Script
 * Automatically inserts SEO header and footer from index.html into all service and location pages
 * Run with: node insert-global-components.js
 */

const fs = require('fs');
const path = require('path');

// Files to update
const FILES_TO_UPDATE = [
    // Service pages
    'services/dishwasher-repair.html',
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

// Extract header from services/dishwasher-repair.html (which has complete header)
function extractHeader() {
    const sourceFile = path.join(__dirname, 'services', 'dishwasher-repair.html');
    const content = fs.readFileSync(sourceFile, 'utf8');

    const startMarker = '<!-- Skip to main content link for accessibility -->';
    const endMarker = '</script>\n\n    <!-- Breadcrumb Navigation -->';

    const startIndex = content.indexOf(startMarker);
    const endIndex = content.indexOf(endMarker);

    if (startIndex === -1 || endIndex === -1) {
        throw new Error('Could not find header markers');
    }

    return content.substring(startIndex, endIndex + '</script>'.length);
}

// Extract footer from index.html
function extractFooter() {
    const sourceFile = path.join(__dirname, 'index.html');
    const content = fs.readFileSync(sourceFile, 'utf8');

    const startMarker = '<!-- SEO-Optimized Footer with Blue Gradient -->';
    const endMarker = '</script>\n</body>';

    const startIndex = content.indexOf(startMarker);
    const endIndex = content.indexOf(endMarker);

    if (startIndex === -1 || endIndex === -1) {
        throw new Error('Could not find footer markers in index.html');
    }

    return content.substring(startIndex, endIndex + '</script>'.length);
}

// Replace header and footer in a file
function replaceComponentsInFile(filePath, headerContent, footerContent) {
    const fullPath = path.join(__dirname, filePath);

    if (!fs.existsSync(fullPath)) {
        console.log(`❌ File not found: ${filePath}`);
        return false;
    }

    let content = fs.readFileSync(fullPath, 'utf8');
    let headerUpdated = false;

    // Replace header (only if markers exist - service pages)
    const headerStartMarker = '<!-- Skip to main content link for accessibility -->';
    const headerEndMarker = '<!-- Breadcrumb Navigation -->';

    const headerStartIndex = content.indexOf(headerStartMarker);
    let headerEndIndex = content.indexOf(headerEndMarker);

    if (headerStartIndex !== -1 && headerEndIndex !== -1) {
        // Replace header section
        const beforeHeader = content.substring(0, headerStartIndex);
        const afterHeader = content.substring(headerEndIndex);

        content = beforeHeader + headerContent + '\n\n    ' + afterHeader;
        headerUpdated = true;
    }

    // Replace footer
    const footerStartMarker = '<!-- Footer Placeholder (loaded from /includes/footer.html) -->';
    const footerEndMarker = '</body>';

    let footerStartIndex = content.indexOf(footerStartMarker);

    // If placeholder exists, remove it
    if (footerStartIndex !== -1) {
        const footerEndIndex = content.indexOf(footerEndMarker, footerStartIndex);
        if (footerEndIndex !== -1) {
            // Remove everything between footer placeholder and </body>
            const beforeFooter = content.substring(0, footerStartIndex);
            content = beforeFooter + '\n    ' + footerContent + '\n' + footerEndMarker;
        }
    } else {
        // If no placeholder, insert before </body>
        const bodyEndIndex = content.lastIndexOf('</body>');
        if (bodyEndIndex !== -1) {
            const beforeFooter = content.substring(0, bodyEndIndex);
            content = beforeFooter + '    ' + footerContent + '\n' + '</body>\n</html>';
        }
    }

    // Write back to file
    fs.writeFileSync(fullPath, content, 'utf8');
    console.log(`✅ Updated: ${filePath}`);
    return true;
}

// Main execution
try {
    console.log('🔧 Extracting header from index.html...\n');
    const headerContent = extractHeader();
    console.log(`✅ Extracted header: ${headerContent.length} characters\n`);

    console.log('🔧 Extracting footer from index.html...\n');
    const footerContent = extractFooter();
    console.log(`✅ Extracted footer: ${footerContent.length} characters\n`);

    console.log('📝 Updating files...\n');
    let successCount = 0;
    let failCount = 0;

    FILES_TO_UPDATE.forEach(filePath => {
        if (replaceComponentsInFile(filePath, headerContent, footerContent)) {
            successCount++;
        } else {
            failCount++;
        }
    });

    console.log(`\n✅ Successfully updated: ${successCount} files`);
    if (failCount > 0) {
        console.log(`❌ Failed to update: ${failCount} files`);
    }

    console.log('\n🎉 Done! All files now have unified header and footer.');
    console.log('📝 Next step: git add . && git commit && git push');

} catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
}
