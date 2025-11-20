/**
 * Header Navigation Handler
 * Manages header interactions and navigation
 */

document.addEventListener('DOMContentLoaded', function() {
    initHeaderNavigation();
    initStickyHeader();
    initSearchFunctionality();
});

/**
 * Initialize header navigation
 */
function initHeaderNavigation() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');

    if (!navToggle || !navMenu) return;

    navToggle.addEventListener('click', function() {
        navMenu.classList.toggle('active');
        navToggle.classList.toggle('active');
    });

    // Close menu on link click
    const navLinks = navMenu.querySelectorAll('a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navMenu.classList.remove('active');
            navToggle.classList.remove('active');
        });
    });
}

/**
 * Initialize sticky header functionality
 */
function initStickyHeader() {
    const header = document.querySelector('header');
    if (!header) return;

    window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
            header.classList.add('sticky');
        } else {
            header.classList.remove('sticky');
        }
    });
}

/**
 * Initialize search functionality
 */
function initSearchFunctionality() {
    const searchInput = document.querySelector('.search-input');
    const searchBtn = document.querySelector('.search-btn');

    if (!searchInput || !searchBtn) return;

    searchBtn.addEventListener('click', function() {
        performSearch(searchInput.value);
    });

    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performSearch(this.value);
        }
    });
}

/**
 * Perform search action
 */
function performSearch(query) {
    if (!query.trim()) {
        console.warn('Search query is empty');
        return;
    }

    // Redirect to search or filter results
    const searchUrl = `/search?q=${encodeURIComponent(query)}`;
    window.location.href = searchUrl;
}
