/**
 * Table of Contents Fix Script
 * Fixes anchor links and sticky positioning issues
 */

(function() {
    'use strict';

    // Wait for DOM to be fully loaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTOC);
    } else {
        initTOC();
    }

    function initTOC() {
        addIDsToHeadings();
        fixStickyTOC();
        smoothScrollToAnchors();
    }

    /**
     * Add IDs to all h2 and h3 headings in the main content
     * This allows TOC links to work properly
     */
    function addIDsToHeadings() {
        const mainContent = document.querySelector('.blog-content') || document.querySelector('main') || document.querySelector('article');
        if (!mainContent) return;

        const headings = mainContent.querySelectorAll('h2, h3');
        let h2Index = 0;
        let h3Index = 0;

        headings.forEach((heading) => {
            // Skip if already has an ID
            if (heading.id) return;

            // Generate ID from text content
            let id = heading.textContent
                .toLowerCase()
                .trim()
                .replace(/[^\w\s-]/g, '') // Remove special characters
                .replace(/\s+/g, '-') // Replace spaces with hyphens
                .replace(/--+/g, '-'); // Replace multiple hyphens with single

            // If empty or just numbers, use generic ID
            if (!id || /^\d+$/.test(id)) {
                if (heading.tagName === 'H2') {
                    id = `section-${h2Index}`;
                    h2Index++;
                } else {
                    id = `subsection-${h3Index}`;
                    h3Index++;
                }
            }

            // Ensure uniqueness
            let finalId = id;
            let counter = 1;
            while (document.getElementById(finalId)) {
                finalId = `${id}-${counter}`;
                counter++;
            }

            heading.id = finalId;
        });
    }

    /**
     * Fix sticky TOC positioning to prevent it from going off-screen
     */
    function fixStickyTOC() {
        const sidebar = document.querySelector('.blog-sidebar');
        const tocWidget = document.querySelector('.toc-widget');

        if (!sidebar || !tocWidget) return;

        // Calculate available space
        function updateTOCHeight() {
            const viewportHeight = window.innerHeight;
            const sidebarTop = sidebar.getBoundingClientRect().top;
            const headerHeight = 100; // Approximate header height
            const padding = 40; // Some breathing room

            // Calculate max height for TOC
            const maxHeight = viewportHeight - headerHeight - padding;

            // Apply max-height and overflow to TOC widget
            tocWidget.style.maxHeight = `${maxHeight}px`;
            tocWidget.style.overflowY = 'auto';
            tocWidget.style.overflowX = 'hidden';
        }

        // Update on load and resize
        updateTOCHeight();
        window.addEventListener('resize', updateTOCHeight);
        window.addEventListener('scroll', updateTOCHeight);
    }

    /**
     * Add smooth scrolling to anchor links
     * Also accounts for fixed header offset
     */
    function smoothScrollToAnchors() {
        const tocLinks = document.querySelectorAll('.toc-list a');

        tocLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                const href = this.getAttribute('href');

                // Only handle internal anchors
                if (!href || !href.startsWith('#')) return;

                const targetId = href.substring(1);
                const targetElement = document.getElementById(targetId);

                if (targetElement) {
                    e.preventDefault();

                    // Calculate offset (header height + some padding)
                    const headerOffset = 100;
                    const elementPosition = targetElement.getBoundingClientRect().top;
                    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                    // Smooth scroll to position
                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });

                    // Update URL without jumping
                    if (history.pushState) {
                        history.pushState(null, null, href);
                    }

                    // Highlight the clicked link
                    tocLinks.forEach(l => l.classList.remove('active'));
                    this.classList.add('active');
                }
            });
        });
    }

    /**
     * Highlight current section in TOC while scrolling
     */
    function highlightCurrentSection() {
        const mainContent = document.querySelector('.blog-content') || document.querySelector('main');
        if (!mainContent) return;

        const headings = mainContent.querySelectorAll('h2, h3');
        const tocLinks = document.querySelectorAll('.toc-list a');

        if (headings.length === 0 || tocLinks.length === 0) return;

        let currentSection = null;
        const scrollPosition = window.pageYOffset + 150; // Offset for header

        // Find current section
        headings.forEach(heading => {
            if (heading.id && heading.offsetTop <= scrollPosition) {
                currentSection = heading.id;
            }
        });

        // Update active state
        tocLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href === `#${currentSection}`) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }

    // Update active section on scroll (throttled)
    let ticking = false;
    window.addEventListener('scroll', function() {
        if (!ticking) {
            window.requestAnimationFrame(function() {
                highlightCurrentSection();
                ticking = false;
            });
            ticking = true;
        }
    });

})();
