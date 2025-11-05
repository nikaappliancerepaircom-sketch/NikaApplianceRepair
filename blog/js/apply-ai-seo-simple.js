/**
 * Simple AI SEO Optimizer for Blog Posts
 * Uses string manipulation instead of DOM parsing
 */

const fs = require('fs');
const path = require('path');

// Blog configuration (inline to avoid require issues)
const BLOG_CONFIG = {
    'dishwasher-maintenance-hard-water': { author: 'michael-toronto', category: 'maintenance', publishDate: '2025-10-30' },
    'how-to-maintain-refrigerator': { author: 'sarah-chen', category: 'maintenance', publishDate: '2025-10-25' },
    'refrigerator-not-cooling-toronto': { author: 'sarah-chen', category: 'troubleshooting', publishDate: '2025-10-28' },
    'dishwasher-not-cleaning': { author: 'michael-toronto', category: 'troubleshooting', publishDate: '2025-10-27' },
    'bosch-dishwasher-repair': { author: 'michael-toronto', category: 'guides', publishDate: '2025-10-26' },
    'refrigerator-repair-vs-replace': { author: 'sarah-chen', category: 'guides', publishDate: '2025-10-24' },
    'how-to-avoid-oven-repairs': { author: 'expert-team', category: 'maintenance', publishDate: '2025-10-23' },
    'how-to-extend-washer-life': { author: 'expert-team', category: 'maintenance', publishDate: '2025-10-22' },
    'how-to-prevent-dryer-fires': { author: 'expert-team', category: 'maintenance', publishDate: '2025-10-21' },
    'dryer-not-heating': { author: 'expert-team', category: 'troubleshooting', publishDate: '2025-10-20' }
};

/**
 * Generate Article schema
 */
function generateArticleSchema(slug, config, title) {
    const schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title || slug.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
        "author": {
            "@type": "Person",
            "name": config.author === 'sarah-chen' ? 'Sarah Chen' :
                   config.author === 'michael-toronto' ? 'Michael Toronto' : 'Nika Expert Team',
            "jobTitle": config.author === 'sarah-chen' ? 'Master Appliance Technician' :
                       config.author === 'michael-toronto' ? 'Senior Dishwasher Specialist' : 'Certified Repair Specialists'
        },
        "publisher": {
            "@type": "LocalBusiness",
            "name": "Nika Appliance Repair",
            "logo": {
                "@type": "ImageObject",
                "url": "https://nikaappliancerepair.com/images/logo.png"
            }
        },
        "datePublished": config.publishDate,
        "dateModified": config.publishDate,
        "image": "https://nikaappliancerepair.com/images/blog-default.jpg",
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": `https://nikaappliancerepair.com/blog/${config.category}/${slug}.html`
        }
    };

    return `\n    <script type="application/ld+json">\n${JSON.stringify(schema, null, 6)}\n    </script>`;
}

/**
 * Generate Breadcrumb schema
 */
function generateBreadcrumbSchema(slug, category) {
    const schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": "https://nikaappliancerepair.com"
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Blog",
                "item": "https://nikaappliancerepair.com/blog"
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": category.charAt(0).toUpperCase() + category.slice(1),
                "item": `https://nikaappliancerepair.com/blog/${category}`
            }
        ]
    };

    return `\n    <script type="application/ld+json">\n${JSON.stringify(schema, null, 6)}\n    </script>`;
}

/**
 * Check if HTML already has schema markup
 */
function hasSchemaMarkup(html) {
    return html.includes('application/ld+json') && html.includes('"@type":"Article"');
}

/**
 * Check if HTML already has AI SEO scripts
 */
function hasAISEOScripts(html) {
    return html.includes('ai-seo-components.js') || html.includes('blog-ai-seo-config.js');
}

/**
 * Extract title from HTML
 */
function extractTitle(html) {
    const h1Match = html.match(/<h1[^>]*>(.*?)<\/h1>/i);
    if (h1Match) {
        return h1Match[1].replace(/<[^>]*>/g, ''); // Strip any HTML tags
    }
    const titleMatch = html.match(/<title>(.*?)<\/title>/i);
    if (titleMatch) {
        return titleMatch[1].replace(/<[^>]*>/g, '');
    }
    return null;
}

/**
 * Add CSS link if not present
 */
function ensureCSSLink(html) {
    if (html.includes('ai-seo-styles.css')) {
        return html;
    }

    // Add before </head>
    return html.replace('</head>', '    <link rel="stylesheet" href="/blog/css/ai-seo-styles.css">\n</head>');
}

/**
 * Add JS scripts if not present
 */
function ensureJSScripts(html, slug) {
    if (hasAISEOScripts(html)) {
        return html;
    }

    const scripts = `
    <!-- AI SEO Components -->
    <script src="/blog/js/ai-seo-components.js"></script>
    <script src="/blog/js/blog-ai-seo-config.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const config = BLOG_AI_SEO_CONFIG['${slug}'];
            if (config) {
                initializeAIComponents({
                    article: {
                        title: document.querySelector('h1')?.textContent || '',
                        author: config.author,
                        publishDate: config.publishDate
                    },
                    breadcrumbs: [
                        { name: 'Home', url: 'https://nikaappliancerepair.com' },
                        { name: 'Blog', url: 'https://nikaappliancerepair.com/blog' }
                    ],
                    faqs: config.faqs || [],
                    components: {
                        directAnswer: config.directAnswer,
                        atAGlance: config.atAGlance,
                        author: config.author,
                        experience: config.experience
                    }
                });
            }
        });
    </script>
`;

    // Add before </body>
    return html.replace('</body>', `${scripts}\n</body>`);
}

/**
 * Process a single blog post file
 */
function processBlogPost(filePath) {
    const slug = path.basename(filePath, '.html');
    const category = path.basename(path.dirname(filePath));

    // Get config or use defaults
    const config = BLOG_CONFIG[slug] || {
        author: 'expert-team',
        category: category,
        publishDate: '2025-10-15'
    };

    console.log(`Processing: ${slug} (${category})`);

    try {
        // Read file
        let html = fs.readFileSync(filePath, 'utf8');

        // Extract title
        const title = extractTitle(html);

        // Check if already has schema markup
        if (hasSchemaMarkup(html)) {
            console.log(`  ⚠ Already has schema markup, skipping: ${slug}`);
            return { success: true, skipped: true };
        }

        // Add schema markup (before </head>)
        const articleSchema = generateArticleSchema(slug, config, title);
        const breadcrumbSchema = generateBreadcrumbSchema(slug, category);
        html = html.replace('</head>', `${articleSchema}${breadcrumbSchema}\n</head>`);

        // Add CSS link
        html = ensureCSSLink(html);

        // Add JS scripts
        html = ensureJSScripts(html, slug);

        // Write back
        fs.writeFileSync(filePath, html, 'utf8');

        console.log(`  ✓ Completed: ${slug}`);
        return { success: true, skipped: false };
    } catch (error) {
        console.error(`  ✗ Error: ${slug} - ${error.message}`);
        return { success: false, skipped: false, error: error.message };
    }
}

/**
 * Get all blog HTML files
 */
function getAllBlogFiles() {
    const blogDir = path.join(__dirname, '..');
    const categories = ['maintenance', 'troubleshooting', 'guides'];
    const files = [];

    categories.forEach(category => {
        const categoryPath = path.join(blogDir, category);
        if (fs.existsSync(categoryPath)) {
            const categoryFiles = fs.readdirSync(categoryPath);
            categoryFiles.forEach(file => {
                if (file.endsWith('.html') && file !== 'index.html') {
                    files.push(path.join(categoryPath, file));
                }
            });
        }
    });

    return files;
}

/**
 * Main execution
 */
function main() {
    console.log('========================================');
    console.log('AI SEO Blog Optimization');
    console.log('========================================\n');

    const files = getAllBlogFiles();
    console.log(`Found ${files.length} blog posts\n`);

    let processed = 0;
    let skipped = 0;
    let failed = 0;

    files.forEach(file => {
        const result = processBlogPost(file);
        if (result.success) {
            if (result.skipped) {
                skipped++;
            } else {
                processed++;
            }
        } else {
            failed++;
        }
    });

    console.log('\n========================================');
    console.log('SUMMARY');
    console.log('========================================');
    console.log(`Total files: ${files.length}`);
    console.log(`Processed: ${processed}`);
    console.log(`Skipped (already optimized): ${skipped}`);
    console.log(`Failed: ${failed}`);
    console.log('========================================\n');

    if (failed === 0) {
        console.log('✓ All blog posts optimized successfully!');
    }
}

// Run
if (require.main === module) {
    main();
}

module.exports = { processBlogPost, getAllBlogFiles };
