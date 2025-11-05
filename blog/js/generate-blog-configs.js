/**
 * Blog AI SEO Config Generator
 * Generates template configurations for all blog posts
 */

const fs = require('fs');
const path = require('path');

// Get all blog HTML files
const blogDir = 'C:\\NikaApplianceRepair\\blog';

// Already configured posts
const configuredPosts = [
    'dishwasher-maintenance-hard-water',
    'how-to-maintain-refrigerator',
    'refrigerator-not-cooling-toronto',
    'dishwasher-not-cleaning',
    'bosch-dishwasher-repair',
    'refrigerator-repair-vs-replace',
    'how-to-avoid-oven-repairs',
    'how-to-extend-washer-life',
    'how-to-prevent-dryer-fires',
    'dryer-not-heating'
];

// Remaining posts that need configuration
const remainingPosts = {
    // TROUBLESHOOTING
    troubleshooting: [
        'appliance-repair-cabbagetown',
        'appliance-repair-distillery-district',
        'appliance-repair-grande-prairie',
        'appliance-repair-king-west',
        'appliance-repair-peterborough',
        'appliance-repair-queen-west',
        'best-appliance-repair-near-me',
        'dishwasher-leaving-food-spots',
        'dishwasher-repair-toronto',
        'dryer-making-noise',
        'dryer-not-drying-clothes',
        'dryer-repair-toronto',
        'emergency-appliance-repair-24-7',
        'freezer-not-freezing',
        'freezer-repair-guide',
        'garbage-disposal-jammed',
        'garbage-disposal-repair',
        'ice-maker-not-working',
        'ice-maker-repair',
        'lg-appliance-repair-service',
        'microwave-not-heating',
        'microwave-repair-toronto',
        'mobile-appliance-repair-whitehorse',
        'oven-door-wont-close',
        'oven-not-heating',
        'oven-repair-toronto',
        'refrigerator-door-seal-replacement',
        'refrigerator-ice-maker-not-working',
        'refrigerator-repair-toronto',
        'refrigerator-water-dispenser-not-working',
        'same-day-appliance-repair',
        'samsung-appliance-repair',
        'stove-burner-not-working',
        'stove-repair-toronto',
        'washer-wont-drain',
        'washing-machine-leaking',
        'washing-machine-leaking-water',
        'washing-machine-repair-complete-guide',
        'water-heater-repair-toronto',
        'whirlpool-customer-service-repair'
    ],

    // GUIDES
    guides: [
        'electrolux-appliance-repair',
        'frigidaire-refrigerator-repair',
        'ge-appliance-repair-toronto',
        'maytag-washer-dryer-repair',
        'should-you-repair-oven',
        'washing-machine-repair-vs-replace',
        'when-to-replace-dryer'
    ]
};

// Generate configuration template for a post
function generateConfig(slug, category) {
    // Determine author based on appliance type
    let author = 'expert-team';
    if (slug.includes('dishwasher')) author = 'michael-toronto';
    else if (slug.includes('refrigerator') || slug.includes('fridge') || slug.includes('freezer')) author = 'sarah-chen';

    // Generate title from slug
    const title = slug
        .split('-')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');

    // Generate publish date (spread across October 2025)
    const day = Math.floor(Math.random() * 20) + 10; // Oct 10-29
    const publishDate = `2025-10-${day.toString().padStart(2, '0')}`;

    return `
    '${slug}': {
        category: '${category}',
        author: '${author}',
        publishDate: '${publishDate}',
        directAnswer: {
            question: '',  // TODO: Add question
            answer: ''     // TODO: Add concise answer
        },
        atAGlance: [
            { label: 'Most Common Cause', value: '' },        // TODO: Add data
            { label: 'Average Repair Cost', value: '$150-$400' },
            { label: 'DIY Success Rate', value: '40-60%' },
            { label: 'Typical Repair Time', value: '1-2 hours' },
            { label: 'Replacement Threshold', value: '8-10 years' }
        ],
        experience: '', // TODO: Add real case study from Toronto
        faqs: [
            {
                question: '', // TODO: Add FAQ 1
                answer: ''
            },
            {
                question: '', // TODO: Add FAQ 2
                answer: ''
            },
            {
                question: '', // TODO: Add FAQ 3
                answer: ''
            },
            {
                question: '', // TODO: Add FAQ 4
                answer: ''
            },
            {
                question: '', // TODO: Add FAQ 5
                answer: ''
            }
        ]
    },`;
}

// Generate all configs
console.log('// ============================================');
console.log('// MORE TROUBLESHOOTING POSTS');
console.log('// ============================================\n');

remainingPosts.troubleshooting.forEach(slug => {
    console.log(generateConfig(slug, 'troubleshooting'));
});

console.log('\n// ============================================');
console.log('// MORE GUIDES');
console.log('// ============================================\n');

remainingPosts.guides.forEach(slug => {
    console.log(generateConfig(slug, 'guides'));
});

console.log('\n// Total posts to configure:', remainingPosts.troubleshooting.length + remainingPosts.guides.length);
console.log('// Already configured:', configuredPosts.length);
console.log('// Total blog posts:', configuredPosts.length + remainingPosts.troubleshooting.length + remainingPosts.guides.length);
