/**
 * FAQ Accordion Toggle Functionality
 * Makes FAQ items expandable/collapsible on click
 */

function initFaqAccordion() {
    // Find all FAQ items
    const faqItems = document.querySelectorAll('.faq-item');

    if (faqItems.length === 0) {
        console.warn('No FAQ items found on this page');
        return;
    }

    // Add click handler to each FAQ heading
    faqItems.forEach((item) => {
        const heading = item.querySelector('h3');

        if (heading) {
            heading.addEventListener('click', function(e) {
                e.preventDefault();

                // Check if this item is already active
                const isActive = item.classList.contains('active');

                // Close all other FAQ items
                faqItems.forEach((otherItem) => {
                    if (otherItem !== item) {
                        otherItem.classList.remove('active');
                    }
                });

                // Toggle current item
                if (isActive) {
                    item.classList.remove('active');
                } else {
                    item.classList.add('active');
                }
            });

            // Make heading keyboard accessible
            heading.setAttribute('tabindex', '0');
            heading.setAttribute('role', 'button');
            heading.setAttribute('aria-expanded', 'false');

            heading.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    heading.click();
                    const isActive = item.classList.contains('active');
                    heading.setAttribute('aria-expanded', isActive);
                }
            });
        }
    });

    // Update aria-expanded on toggle
    faqItems.forEach((item) => {
        const heading = item.querySelector('h3');
        const observer = new MutationObserver(() => {
            if (heading) {
                const isActive = item.classList.contains('active');
                heading.setAttribute('aria-expanded', isActive);
            }
        });

        if (item) {
            observer.observe(item, { attributes: true, attributeFilter: ['class'] });
        }
    });
}

// Initialize FAQ accordion
// Check if DOM is already loaded before adding event listener
if (document.readyState === 'loading') {
    // DOM is still loading, wait for DOMContentLoaded
    document.addEventListener('DOMContentLoaded', initFaqAccordion);
} else {
    // DOM is already loaded, initialize immediately
    initFaqAccordion();
}
