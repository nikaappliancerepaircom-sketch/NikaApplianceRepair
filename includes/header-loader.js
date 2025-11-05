// Header Loader Script
// Loads the unified header from includes/header-unified.html

(function() {
    // Create a placeholder for the header
    const headerPlaceholder = document.getElementById('header-placeholder');

    if (headerPlaceholder) {
        // Fetch and insert the header
        fetch('/includes/header-unified.html')
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
