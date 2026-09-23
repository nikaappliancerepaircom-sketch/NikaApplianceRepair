// Header Loader Script
// Loads the appropriate header while preserving Alberta page content.

(function() {
    // Create a placeholder for the header
    const headerPlaceholder = document.getElementById('header-placeholder');

    if (headerPlaceholder) {
        const isAlbertaPage = Array.from(document.querySelectorAll('script[type="application/ld+json"]'))
            .some(script => /"addressRegion"\s*:\s*"(?:AB|Alberta)"/i.test(script.textContent || ''));
        const headerPath = isAlbertaPage
            ? '/includes/header-alberta.html'
            : '/includes/header-unified.html';

        // Fetch and insert the header
        fetch(headerPath)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to load header');
                }
                return response.text();
            })
            .then(html => {
                headerPlaceholder.innerHTML = html;

                // Execute any scripts in the loaded content
                const scripts = headerPlaceholder.querySelectorAll('script');
                scripts.forEach(oldScript => {
                    const newScript = document.createElement('script');
                    Array.from(oldScript.attributes).forEach(attr => {
                        newScript.setAttribute(attr.name, attr.value);
                    });
                    newScript.textContent = oldScript.textContent;
                    oldScript.parentNode.replaceChild(newScript, oldScript);
                });
            })
            .catch(error => {
                console.error('Error loading header:', error);
                // Fallback: show a simple header
                headerPlaceholder.innerHTML = '<header class="site-header"><div class="header-container"><div class="header-logo"><a href="/">NIKA Appliance Repair</a></div></div></header>';
            });
    }
})();

// Keep booking navigation consistent on newly published pages.
(function(){if(!document.querySelector('script[src="/js/site-booking.js"]')){var s=document.createElement("script");s.src="/js/site-booking.js";s.defer=true;document.head.appendChild(s);}})();
