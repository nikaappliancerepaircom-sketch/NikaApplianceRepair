/**
 * Word Counter for Visible Content Only
 * Counts actual readable words on a webpage, excluding HTML, CSS, JS, and meta content
 */

const fs = require('fs');
const path = require('path');

function countVisibleWords(filePath) {
    try {
        // Read the HTML file
        let content = fs.readFileSync(filePath, 'utf8');
        
        // Remove script tags and their content
        content = content.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');
        
        // Remove style tags and their content
        content = content.replace(/<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>/gi, '');
        
        // Remove HTML comments
        content = content.replace(/<!--[\s\S]*?-->/g, '');
        
        // Remove everything in <head> section (meta, title, etc.)
        content = content.replace(/<head\b[^<]*(?:(?!<\/head>)<[^<]*)*<\/head>/gi, '');
        
        // Remove all HTML tags but keep their content
        content = content.replace(/<[^>]+>/g, ' ');
        
        // Remove extra whitespace
        content = content.replace(/\s+/g, ' ').trim();
        
        // Count words (split by spaces and filter out empty strings)
        const words = content.split(' ').filter(word => word.length > 0);
        const wordCount = words.length;
        
        // Analyze sections if possible
        console.log('===================================');
        console.log(`FILE: ${path.basename(filePath)}`);
        console.log('===================================');
        console.log(`VISIBLE WORD COUNT: ${wordCount} words`);
        console.log('===================================');
        
        // Check if meets requirements
        if (filePath.includes('service') || filePath.includes('location')) {
            const requirement = filePath.includes('location') ? 1500 : 1200;
            const status = wordCount >= requirement ? '✅ PASSES' : '❌ NEEDS MORE CONTENT';
            const difference = wordCount - requirement;
            
            console.log(`Requirement: ${requirement} words`);
            console.log(`Status: ${status}`);
            if (difference < 0) {
                console.log(`Needs: ${Math.abs(difference)} more words`);
            } else {
                console.log(`Exceeds by: ${difference} words`);
            }
        } else if (filePath.includes('brand')) {
            const requirement = 1200;
            const status = wordCount >= requirement ? '✅ PASSES' : '❌ NEEDS MORE CONTENT';
            const difference = wordCount - requirement;
            
            console.log(`Requirement: ${requirement} words`);
            console.log(`Status: ${status}`);
            if (difference < 0) {
                console.log(`Needs: ${Math.abs(difference)} more words`);
            } else {
                console.log(`Exceeds by: ${difference} words`);
            }
        }
        
        console.log('===================================\n');
        
        return wordCount;
        
    } catch (error) {
        console.error('Error reading file:', error.message);
        return 0;
    }
}

// Command line usage
if (process.argv[2]) {
    const filePath = process.argv[2];
    countVisibleWords(filePath);
} else {
    console.log('Usage: node count-visible-words.js <path-to-html-file>');
    console.log('Example: node count-visible-words.js ../brands/lg-appliance-repair-toronto.html');
}

module.exports = countVisibleWords;