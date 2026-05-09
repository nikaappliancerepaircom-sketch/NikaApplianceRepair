'use strict';
const fs = require('fs');
const path = require('path');

const SITE_DIR = 'C:/fixlifyservices';
const DOMAIN = 'fixlifyservices.com';
const DRY = process.argv.includes('--dry-run');

const LB_SCHEMA = {
  '@type': 'LocalBusiness',
  name: 'Fixlify Appliance Services',
  telephone: '+14375241053',
  priceRange: '$$',
  url: 'https://fixlifyservices.com',
  address: {
    '@type': 'PostalAddress',
    addressLocality: 'Scarborough',
    addressRegion: 'Ontario',
    addressCountry: 'CA'
  },
  aggregateRating: {
    '@type': 'AggregateRating',
    ratingValue: '4.9',
    reviewCount: '261'
  },
  openingHours: ['Mo-Sa 08:00-20:00', 'Su 09:00-18:00'],
  founder: { '@type': 'Person', name: 'Alex' },
  numberOfEmployees: { '@type': 'QuantitativeValue', value: 6 }
};

const PAGE_SCHEMAS = {
  'privacy.html': {
    breadcrumb: {
      '@type': 'BreadcrumbList',
      itemListElement: [
        { '@type': 'ListItem', position: 1, name: 'Home', item: 'https://fixlifyservices.com/' },
        { '@type': 'ListItem', position: 2, name: 'Privacy Policy' }
      ]
    },
    faq: {
      '@type': 'FAQPage',
      mainEntity: [
        {
          '@type': 'Question',
          name: 'What personal information does Fixlify Services collect?',
          acceptedAnswer: {
            '@type': 'Answer',
            text: 'Fixlify Services collects your name, phone number, address, and appliance details when you book a repair. We also collect contact messages sent through our forms or email. No payment data is stored on our servers — payments are processed by PCI-compliant third parties.'
          }
        },
        {
          '@type': 'Question',
          name: 'How long does Fixlify keep my data?',
          acceptedAnswer: {
            '@type': 'Answer',
            text: 'We retain booking records for 12 months for warranty and service history purposes. You can request deletion of your data at any time by emailing info@fixlifyservices.com. We will respond within 30 days.'
          }
        }
      ]
    }
  },
  'terms.html': {
    breadcrumb: {
      '@type': 'BreadcrumbList',
      itemListElement: [
        { '@type': 'ListItem', position: 1, name: 'Home', item: 'https://fixlifyservices.com/' },
        { '@type': 'ListItem', position: 2, name: 'Terms of Service' }
      ]
    },
    faq: {
      '@type': 'FAQPage',
      mainEntity: [
        {
          '@type': 'Question',
          name: 'What warranty does Fixlify Services offer on repairs?',
          acceptedAnswer: {
            '@type': 'Answer',
            text: 'Fixlify Services provides a 90-day warranty on all parts and labour. If the same fault recurs within 90 days of the repair, we return at no charge. The warranty covers the specific component replaced or repaired and does not extend to unrelated faults.'
          }
        },
        {
          '@type': 'Question',
          name: 'What is the Fixlify cancellation policy?',
          acceptedAnswer: {
            '@type': 'Answer',
            text: 'You can cancel or reschedule at no charge up to 2 hours before your appointment window. Cancellations with less than 2 hours notice may incur a $40 trip-fee to cover the dispatched technician time. Contact us at info@fixlifyservices.com or call +1-437-524-1053.'
          }
        }
      ]
    }
  },
  'accessibility.html': {
    breadcrumb: {
      '@type': 'BreadcrumbList',
      itemListElement: [
        { '@type': 'ListItem', position: 1, name: 'Home', item: 'https://fixlifyservices.com/' },
        { '@type': 'ListItem', position: 2, name: 'Accessibility Statement' }
      ]
    },
    faq: {
      '@type': 'FAQPage',
      mainEntity: [
        {
          '@type': 'Question',
          name: 'Is fixlifyservices.com accessible for screen-reader users?',
          acceptedAnswer: {
            '@type': 'Answer',
            text: 'Yes — fixlifyservices.com targets WCAG 2.1 Level AA. All images have descriptive alt text, forms have explicit labels, and every page can be navigated by keyboard alone. If you encounter an accessibility barrier, email info@fixlifyservices.com and we will provide an alternate format within 5 business days.'
          }
        },
        {
          '@type': 'Question',
          name: 'How can I request an accessible format of service information from Fixlify?',
          acceptedAnswer: {
            '@type': 'Answer',
            text: 'You can request service information in large print, plain text, or over the phone by calling +1-437-524-1053 or emailing info@fixlifyservices.com. We accommodate requests under the Accessibility for Ontarians with Disabilities Act (AODA).'
          }
        }
      ]
    }
  },
  'for-businesses.html': {
    breadcrumb: {
      '@type': 'BreadcrumbList',
      itemListElement: [
        { '@type': 'ListItem', position: 1, name: 'Home', item: 'https://fixlifyservices.com/' },
        { '@type': 'ListItem', position: 2, name: 'Field Service Management for Appliance Repair Companies' }
      ]
    },
    faq: {
      '@type': 'FAQPage',
      mainEntity: [
        {
          '@type': 'Question',
          name: 'What is Fixlify field service management software?',
          acceptedAnswer: {
            '@type': 'Answer',
            text: 'Fixlify is purpose-built field service management software for appliance repair businesses. It includes an AI dispatcher, online booking widget, job management, CRM, invoicing, and automated customer communications. It is designed to help small and mid-size appliance repair companies grow without adding back-office staff.'
          }
        },
        {
          '@type': 'Question',
          name: 'How does Fixlify help appliance repair businesses get more jobs?',
          acceptedAnswer: {
            '@type': 'Answer',
            text: 'Fixlify AI Dispatcher qualifies and books inbound leads automatically — 24/7, including nights and weekends. Customers book online through your website widget, receive automated confirmation texts, and rate the job on completion. Positive reviews are captured and published automatically, improving your local SEO and Google ranking.'
          }
        }
      ]
    }
  }
};

let added = 0;
for (const [filename, schemas] of Object.entries(PAGE_SCHEMAS)) {
  const filepath = path.join(SITE_DIR, filename);
  if (!fs.existsSync(filepath)) {
    console.log('SKIP (not found): ' + filename);
    continue;
  }

  let html = fs.readFileSync(filepath, 'utf8');

  if (/"BreadcrumbList"/.test(html)) {
    console.log('SKIP (already has BreadcrumbList): ' + filename);
    continue;
  }

  // Build @graph schema block
  const graph = {
    '@context': 'https://schema.org',
    '@graph': [
      LB_SCHEMA,
      schemas.faq,
      schemas.breadcrumb
    ]
  };

  const schemaTag = '\n<script type="application/ld+json">\n' + JSON.stringify(graph, null, 2) + '\n</script>';

  if (!html.includes('</head>')) {
    console.log('SKIP (no </head>): ' + filename);
    continue;
  }

  const newHtml = html.replace('</head>', schemaTag + '\n</head>');

  if (!DRY) {
    fs.writeFileSync(filepath, newHtml, 'utf8');
  }
  console.log((DRY ? '[DRY] ' : '') + 'ADDED schema to: ' + filename);
  added++;
}

console.log('\nTotal pages updated: ' + added);
