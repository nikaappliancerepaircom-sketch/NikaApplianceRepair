/**
 * FAQ Accordion Toggle Functionality
 * Makes FAQ items expandable/collapsible on click
 */

document.addEventListener('DOMContentLoaded', function() {
    // Find all FAQ items
    const faqItems = document.querySelectorAll('.faq-item');

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
});
