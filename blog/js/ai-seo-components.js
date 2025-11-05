/**
 * AI SEO Optimization Components
 * Reusable JavaScript templates for adding AI-friendly content to blog posts
 */

// ============================================
// SCHEMA MARKUP GENERATORS
// ============================================

function generateArticleSchema(config) {
    const schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": config.title,
        "author": {
            "@type": "Person",
            "name": config.author.name,
            "jobTitle": config.author.title,
            "url": `https://nikaappliancerepair.com/authors/${config.author.slug}`
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
        "dateModified": config.modifiedDate || config.publishDate,
        "image": config.image || "https://nikaappliancerepair.com/images/blog-default.jpg",
        "description": config.description,
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": config.url
        }
    };

    const scriptTag = document.createElement('script');
    scriptTag.type = 'application/ld+json';
    scriptTag.textContent = JSON.stringify(schema, null, 2);
    document.head.appendChild(scriptTag);
}

function generateFAQSchema(faqs) {
    const schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faqs.map(faq => ({
            "@type": "Question",
            "name": faq.question,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq.answer
            }
        }))
    };

    const scriptTag = document.createElement('script');
    scriptTag.type = 'application/ld+json';
    scriptTag.textContent = JSON.stringify(schema, null, 2);
    document.head.appendChild(scriptTag);
}

function generateBreadcrumbSchema(breadcrumbs) {
    const schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": breadcrumbs.map((item, index) => ({
            "@type": "ListItem",
            "position": index + 1,
            "name": item.name,
            "item": item.url
        }))
    };

    const scriptTag = document.createElement('script');
    scriptTag.type = 'application/ld+json';
    scriptTag.textContent = JSON.stringify(schema, null, 2);
    document.head.appendChild(scriptTag);
}

function generateHowToSchema(config) {
    const schema = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": config.name,
        "description": config.description,
        "totalTime": config.totalTime || "PT30M",
        "step": config.steps.map((step, index) => ({
            "@type": "HowToStep",
            "name": step.name,
            "text": step.text,
            "position": index + 1
        }))
    };

    const scriptTag = document.createElement('script');
    scriptTag.type = 'application/ld+json';
    scriptTag.textContent = JSON.stringify(schema, null, 2);
    document.head.appendChild(scriptTag);
}

// ============================================
// AUTHOR PROFILES
// ============================================

const AUTHORS = {
    'sarah-chen': {
        name: 'Sarah Chen',
        title: 'Master Appliance Technician',
        experience: '12 years',
        certifications: ['Samsung Certified', 'LG Certified', 'Whirlpool Certified'],
        specialties: ['Refrigerators', 'Cooling Systems'],
        repairCount: '1,800+',
        successRate: '98%',
        email: 'sarah@nikaappliancerepair.com',
        bio: 'Sarah has 12 years of experience repairing major appliances across Toronto. She specializes in diagnosing complex cooling system failures and has a 98% first-visit fix rate.',
        phone: '647-557-6342',
        location: 'Toronto, ON'
    },
    'michael-toronto': {
        name: 'Michael Toronto',
        title: 'Senior Dishwasher Specialist',
        experience: '10 years',
        certifications: ['Bosch Certified', 'KitchenAid Certified'],
        specialties: ['Dishwashers', 'Hard Water Solutions'],
        repairCount: '1,500+',
        successRate: '96%',
        email: 'michael@nikaappliancerepair.com',
        bio: 'Michael specializes in dishwasher repairs and hard water solutions across the GTA. He has extensive experience with Toronto\'s water conditions.',
        phone: '647-557-6342',
        location: 'Toronto, ON'
    },
    'james-wilson': {
        name: 'James Wilson',
        title: 'Washer & Dryer Specialist',
        experience: '14 years',
        certifications: ['Maytag Certified', 'GE Certified', 'Speed Queen Certified'],
        specialties: ['Washing Machines', 'Dryers', 'Laundry Systems'],
        repairCount: '2,200+',
        successRate: '97%',
        email: 'james@nikaappliancerepair.com',
        bio: 'James has 14 years of experience specializing in washer and dryer repairs across Toronto. He has extensive knowledge of both front-load and top-load systems and can diagnose complex drainage and heating issues.',
        phone: '647-557-6342',
        location: 'Toronto, ON'
    },
    'david-martinez': {
        name: 'David Martinez',
        title: 'Oven & Stove Expert',
        experience: '11 years',
        certifications: ['Wolf Certified', 'Viking Certified', 'Thermador Certified'],
        specialties: ['Ovens', 'Stoves', 'Ranges', 'Cooktops'],
        repairCount: '1,600+',
        successRate: '96%',
        email: 'david@nikaappliancerepair.com',
        bio: 'David has 11 years of experience repairing ovens, stoves, and ranges across Toronto. He specializes in gas and electric cooking appliances and has expertise in diagnosing heating element failures and control board issues.',
        phone: '647-557-6342',
        location: 'Toronto, ON'
    },
    'expert-team': {
        name: 'Nika Expert Team',
        title: 'Certified Appliance Repair Specialists',
        experience: '15+ years',
        certifications: ['All Major Brands Certified'],
        specialties: ['All Appliances'],
        repairCount: '5,000+',
        successRate: '97%',
        email: 'info@nikaappliancerepair.com',
        bio: 'Our team of certified technicians has over 15 years of combined experience repairing all major appliances across Toronto and the GTA.',
        phone: '647-557-6342',
        location: 'Toronto, ON'
    }
};

function createAuthorBox(authorSlug = 'expert-team') {
    const author = AUTHORS[authorSlug];
    if (!author) return '';

    return `
        <div class="author-box-ai">
            <div class="author-info">
                <h3 class="author-name">${author.name}</h3>
                <p class="author-title">${author.title}</p>
                <ul class="author-credentials">
                    <li><i class="fas fa-check-circle"></i> ${author.experience} experience in Toronto</li>
                    ${author.certifications.map(cert => `<li><i class="fas fa-check-circle"></i> ${cert}</li>`).join('')}
                    <li><i class="fas fa-check-circle"></i> ${author.repairCount} repairs completed</li>
                    <li><i class="fas fa-check-circle"></i> ${author.successRate} success rate</li>
                </ul>
                <p class="author-bio">${author.bio}</p>
                <div class="author-contact">
                    <a href="mailto:${author.email}"><i class="fas fa-envelope"></i> ${author.email}</a>
                </div>
            </div>
        </div>
    `;
}

// ============================================
// DIRECT ANSWER BOXES
// ============================================

function createDirectAnswerBox(question, answer) {
    return `
        <div class="direct-answer-box">
            <div class="answer-icon">
                <i class="fas fa-lightbulb"></i>
            </div>
            <div class="answer-content">
                <h3>Quick Answer</h3>
                <p><strong>${answer}</strong></p>
            </div>
        </div>
    `;
}

// ============================================
// AT-A-GLANCE BOXES
// ============================================

function createAtAGlanceBox(items) {
    const itemsHTML = items.map(item => `
        <div class="glance-item">
            <div class="glance-label">${item.label}</div>
            <div class="glance-value">${item.value}</div>
        </div>
    `).join('');

    return `
        <div class="at-a-glance">
            <h3><i class="fas fa-tachometer-alt"></i> At a Glance</h3>
            <div class="glance-grid">
                ${itemsHTML}
            </div>
        </div>
    `;
}

// ============================================
// FAQ SECTIONS
// ============================================

function createFAQSection(faqs) {
    const faqItemsHTML = faqs.map((faq, index) => `
        <div class="faq-item">
            <button class="faq-question" aria-expanded="false" data-faq-index="${index}">
                <span>${faq.question}</span>
                <i class="fas fa-chevron-down"></i>
            </button>
            <div class="faq-answer" style="display: none;">
                ${faq.answer}
            </div>
        </div>
    `).join('');

    return `
        <div class="faq-section">
            <h2><i class="fas fa-question-circle"></i> Frequently Asked Questions</h2>
            ${faqItemsHTML}
        </div>
    `;
}

// FAQ Toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.faq-question').forEach(button => {
        button.addEventListener('click', function() {
            const isExpanded = this.getAttribute('aria-expanded') === 'true';
            const answer = this.nextElementSibling;

            this.setAttribute('aria-expanded', !isExpanded);
            answer.style.display = isExpanded ? 'none' : 'block';

            const icon = this.querySelector('i');
            icon.classList.toggle('fa-chevron-down');
            icon.classList.toggle('fa-chevron-up');
        });
    });
});

// ============================================
// EXPERIENCE BOX
// ============================================

function createExperienceBox(story) {
    return `
        <div class="experience-box">
            <h3><i class="fas fa-user-tie"></i> From Our Experience</h3>
            <p>${story}</p>
        </div>
    `;
}

// ============================================
// INITIALIZATION
// ============================================

function initializeAIComponents(config) {
    // Add Article Schema
    if (config.article) {
        generateArticleSchema(config.article);
    }

    // Add Breadcrumb Schema
    if (config.breadcrumbs) {
        generateBreadcrumbSchema(config.breadcrumbs);
    }

    // Add FAQ Schema
    if (config.faqs && config.faqs.length > 0) {
        generateFAQSchema(config.faqs);
    }

    // Add HowTo Schema
    if (config.howTo) {
        generateHowToSchema(config.howTo);
    }

    // Insert components into DOM
    const contentArea = document.querySelector('.blog-content, article');

    if (contentArea && config.components) {
        // Add Direct Answer Box (at the top)
        if (config.components.directAnswer) {
            const answerBox = createDirectAnswerBox(
                config.components.directAnswer.question,
                config.components.directAnswer.answer
            );
            contentArea.insertAdjacentHTML('afterbegin', answerBox);
        }

        // Add At-A-Glance Box
        if (config.components.atAGlance) {
            const glanceBox = createAtAGlanceBox(config.components.atAGlance);
            const firstH2 = contentArea.querySelector('h2');
            if (firstH2) {
                firstH2.insertAdjacentHTML('beforebegin', glanceBox);
            }
        }

        // Add Author Box
        if (config.components.author) {
            const authorBox = createAuthorBox(config.components.author);
            const firstParagraph = contentArea.querySelector('p');
            if (firstParagraph) {
                firstParagraph.insertAdjacentHTML('afterend', authorBox);
            }
        }

        // Add Experience Box
        if (config.components.experience) {
            const expBox = createExperienceBox(config.components.experience);
            // Insert before FAQ section or at end
            const faqSection = contentArea.querySelector('.faq-section');
            if (faqSection) {
                faqSection.insertAdjacentHTML('beforebegin', expBox);
            } else {
                contentArea.insertAdjacentHTML('beforeend', expBox);
            }
        }

        // Add FAQ Section (at the end)
        if (config.faqs && config.faqs.length > 0) {
            const faqSection = createFAQSection(config.faqs);
            contentArea.insertAdjacentHTML('beforeend', faqSection);
        }
    }
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        generateArticleSchema,
        generateFAQSchema,
        generateBreadcrumbSchema,
        generateHowToSchema,
        createAuthorBox,
        createDirectAnswerBox,
        createAtAGlanceBox,
        createFAQSection,
        createExperienceBox,
        initializeAIComponents,
        AUTHORS
    };
}
