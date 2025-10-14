/**
 * Unified Header & Footer Loader
 * Loads header and footer from /includes/ folder into all pages
 * With caching for performance
 */

(function() {
    'use strict';

    // Cache for 1 hour (3600000 ms)
    const CACHE_DURATION = 3600000;

    /**
     * Load HTML content with caching
     */
    function loadHTML(url, targetId, cacheKey) {
        const placeholder = document.getElementById(targetId);
        if (!placeholder) {
            console.error(`Element with id "${targetId}" not found`);
            return;
        }

        // Check cache first
        const cached = getCachedContent(cacheKey);
        if (cached) {
            placeholder.innerHTML = cached;
            initializeScripts(placeholder);
            return;
        }

        // Fetch from server
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.text();
            })
            .then(html => {
                placeholder.innerHTML = html;
                setCachedContent(cacheKey, html);
                initializeScripts(placeholder);
            })
            .catch(error => {
                console.error(`Error loading ${url}:`, error);
                placeholder.innerHTML = `<div class="load-error">Failed to load content. Please refresh the page.</div>`;
            });
    }

    /**
     * Get cached content from localStorage
     */
    function getCachedContent(key) {
        try {
            const cached = localStorage.getItem(key);
            if (cached) {
                const data = JSON.parse(cached);
                const now = new Date().getTime();
                if (now - data.timestamp < CACHE_DURATION) {
                    return data.content;
                } else {
                    localStorage.removeItem(key);
                }
            }
        } catch (e) {
            console.error('Cache read error:', e);
        }
        return null;
    }

    /**
     * Set content to cache in localStorage
     */
    function setCachedContent(key, content) {
        try {
            const data = {
                content: content,
                timestamp: new Date().getTime()
            };
            localStorage.setItem(key, JSON.stringify(data));
        } catch (e) {
            console.error('Cache write error:', e);
        }
    }

    /**
     * Initialize scripts in loaded HTML
     */
    function initializeScripts(container) {
        const scripts = container.querySelectorAll('script');
        scripts.forEach(script => {
            const newScript = document.createElement('script');
            if (script.src) {
                newScript.src = script.src;
            } else {
                newScript.textContent = script.textContent;
            }
            script.parentNode.replaceChild(newScript, script);
        });
    }

    /**
     * Load header and footer when DOM is ready
     */
    function init() {
        loadHTML('/includes/header.html', 'header-placeholder', 'cached-header');
        loadHTML('/includes/footer.html', 'footer-placeholder', 'cached-footer');
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Expose function to clear cache (for development)
    window.clearIncludesCache = function() {
        localStorage.removeItem('cached-header');
        localStorage.removeItem('cached-footer');
        console.log('Includes cache cleared!');
    };

})();
