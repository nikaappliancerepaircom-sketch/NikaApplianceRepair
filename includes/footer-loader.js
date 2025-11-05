// Footer Loader Script
// Loads the unified footer from includes/footer-unified.html

(function() {
    // Create a placeholder for the footer
    const footerPlaceholder = document.getElementById('footer-placeholder');

    if (footerPlaceholder) {
        // Fetch and insert the footer
        fetch('/includes/footer-unified.html')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to load footer');
                }
                return response.text();
            })
            .then(html => {
                footerPlaceholder.innerHTML = html;

                // Execute any scripts in the loaded content
                const scripts = footerPlaceholder.querySelectorAll('script');
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
                console.error('Error loading footer:', error);
                // Fallback: show a simple footer
                footerPlaceholder.innerHTML = '<footer style="background:#2196F3;color:white;padding:2rem;text-align:center;"><p>© 2025 Nika Appliance Repair. All Rights Reserved.</p></footer>';
            });
    }
})();
