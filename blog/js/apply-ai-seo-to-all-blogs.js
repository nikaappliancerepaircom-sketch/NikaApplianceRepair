/**
 * Apply AI SEO Optimizations to All Blog Posts
 * This script modifies all blog HTML files to include AI-friendly components
 */

const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

// Import our configuration
const BLOG_AI_SEO_CONFIG = require('./blog-ai-seo-config.js');

// Paths
const BLOG_DIR = path.join(__dirname, '..');
const CATEGORIES = ['maintenance', 'troubleshooting', 'guides'];

/**
 * Get all blog HTML files
 */
function getAllBlogPosts() {
    const posts = [];

    CATEGORIES.forEach(category => {
        const categoryPath = path.join(BLOG_DIR, category);
        if (fs.existsSync(categoryPath)) {
            const files = fs.readdirSync(categoryPath);
            files.forEach(file => {
                if (file.endsWith('.html') && file !== 'index.html') {
                    posts.push({
                        path: path.join(categoryPath, file),
                        slug: file.replace('.html', ''),
                        category: category
                    });
                }
            });
        }
    });

    return posts;
}

/**
 * Generate schema markup for article
 */
function generateArticleSchema(config, slug) {
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": config.article?.title || "Appliance Repair Guide",
        "author": {
            "@type": "Person",
            "name": config.author?.name || "Nika Expert Team",
            "jobTitle": config.author?.title || "Appliance Repair Specialist"
        },
        "publisher": {
            "@type": "LocalBusiness",
            "name": "Nika Appliance Repair",
            "logo": {
                "@type": "ImageObject",
                "url": "https://nikaappliancerepair.com/images/logo.png"
            }
        },
        "datePublished": config.publishDate || new Date().toISOString().split('T')[0],
        "dateModified": config.modifiedDate || config.publishDate || new Date().toISOString().split('T')[0],
        "image": "https://nikaappliancerepair.com/images/blog-default.jpg",
        "description": config.description || "Expert appliance repair advice for Toronto homeowners",
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": `https://nikaappliancerepair.com/blog/${config.category}/${slug}.html`
        }
    };
}

/**
 * Generate FAQ schema
 */
function generateFAQSchema(faqs) {
    if (!faqs || faqs.length === 0) return null;

    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faqs.map(faq => ({
            "@type": "Question",
            "name": faq.question,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq.answer.replace(/<[^>]*>/g, '') // Strip HTML for schema
            }
        }))
    };
}

/**
 * Generate breadcrumb schema
 */
function generateBreadcrumbSchema(category, slug) {
    return {
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
            },
            {
                "@type": "ListItem",
                "position": 4,
                "name": slug.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
                "item": `https://nikaappliancerepair.com/blog/${category}/${slug}.html`
            }
        ]
    };
}

/**
 * Inject schema markup into HTML head
 */
function injectSchemaMarkup(dom, schemas) {
    const head = dom.window.document.querySelector('head');

    schemas.forEach(schema => {
        if (schema) {
            const script = dom.window.document.createElement('script');
            script.type = 'application/ld+json';
            script.textContent = JSON.stringify(schema, null, 2);
            head.appendChild(script);
        }
    });
}

/**
 * Add CSS link if not present
 */
function ensureCSSLink(dom) {
    const head = dom.window.document.querySelector('head');
    const existingLink = Array.from(head.querySelectorAll('link')).find(
        link => link.href && link.href.includes('ai-seo-styles.css')
    );

    if (!existingLink) {
        const link = dom.window.document.createElement('link');
        link.rel = 'stylesheet';
        link.href = '/blog/css/ai-seo-styles.css';
        head.appendChild(link);
    }
}

/**
 * Add JavaScript includes if not present
 */
function ensureJSIncludes(dom, slug) {
    const body = dom.window.document.querySelector('body');

    // Check if scripts already exist
    const existingScripts = Array.from(body.querySelectorAll('script')).map(s => s.src);

    const scriptsToAdd = [
        '/blog/js/ai-seo-components.js',
        '/blog/js/blog-ai-seo-config.js'
    ];

    scriptsToAdd.forEach(src => {
        if (!existingScripts.some(existing => existing && existing.includes(path.basename(src)))) {
            const script = dom.window.document.createElement('script');
            script.src = src;
            body.appendChild(script);
        }
    });

    // Add initialization script
    const initScriptExists = Array.from(body.querySelectorAll('script')).some(
        s => s.textContent && s.textContent.includes('initializeAIComponents')
    );

    if (!initScriptExists) {
        const initScript = dom.window.document.createElement('script');
        initScript.textContent = `
document.addEventListener('DOMContentLoaded', function() {
    const slug = '${slug}';
    const config = BLOG_AI_SEO_CONFIG[slug];

    if (config) {
        // Initialize AI components with config
        initializeAIComponents({
            article: {
                title: document.querySelector('h1')?.textContent || '',
                author: config.author,
                publishDate: config.publishDate,
                description: document.querySelector('meta[name="description"]')?.content || ''
            },
            breadcrumbs: [
                { name: 'Home', url: 'https://nikaappliancerepair.com' },
                { name: 'Blog', url: 'https://nikaappliancerepair.com/blog' },
                { name: '${slug}', url: window.location.href }
            ],
            faqs: config.faqs,
            components: {
                directAnswer: config.directAnswer,
                atAGlance: config.atAGlance,
                author: config.author,
                experience: config.experience
            }
        });
    }
});
        `.trim();
        body.appendChild(initScript);
    }
}

/**
 * Process a single blog post
 */
function processBlogPost(post) {
    try {
        console.log(`Processing: ${post.slug}`);

        // Read HTML file
        const html = fs.readFileSync(post.path, 'utf8');
        const dom = new JSDOM(html);
        const document = dom.window.document;

        // Get configuration for this post
        const config = BLOG_AI_SEO_CONFIG[post.slug] || {
            category: post.category,
            author: 'expert-team',
            publishDate: new Date().toISOString().split('T')[0],
            faqs: []
        };

        // Generate and inject schema markup
        const articleSchema = generateArticleSchema(config, post.slug);
        const faqSchema = generateFAQSchema(config.faqs);
        const breadcrumbSchema = generateBreadcrumbSchema(post.category, post.slug);

        // Check if schemas already exist
        const existingSchemas = Array.from(document.querySelectorAll('script[type="application/ld+json"]'));
        const hasArticleSchema = existingSchemas.some(s => s.textContent.includes('"@type":"Article"'));

        if (!hasArticleSchema) {
            injectSchemaMarkup(dom, [articleSchema, faqSchema, breadcrumbSchema]);
        }

        // Ensure CSS and JS links
        ensureCSSLink(dom);
        ensureJSIncludes(dom, post.slug);

        // Write back to file
        fs.writeFileSync(post.path, dom.serialize(), 'utf8');

        console.log(`✓ Completed: ${post.slug}`);
        return true;
    } catch (error) {
        console.error(`✗ Error processing ${post.slug}:`, error.message);
        return false;
    }
}

/**
 * Main execution
 */
function main() {
    console.log('========================================');
    console.log('AI SEO Optimization - Blog Posts');
    console.log('========================================\n');

    const posts = getAllBlogPosts();
    console.log(`Found ${posts.length} blog posts to process\n`);

    let processed = 0;
    let failed = 0;

    posts.forEach(post => {
        if (processBlogPost(post)) {
            processed++;
        } else {
            failed++;
        }
    });

    console.log('\n========================================');
    console.log('SUMMARY');
    console.log('========================================');
    console.log(`Total posts: ${posts.length}`);
    console.log(`Processed: ${processed}`);
    console.log(`Failed: ${failed}`);
    console.log('========================================\n');
}

// Run if called directly
if (require.main === module) {
    main();
}

module.exports = { processBlogPost, getAllBlogPosts };
