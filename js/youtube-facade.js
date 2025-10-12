/**
 * YouTube Facade - Lazy Loading Implementation
 * Загружает YouTube видео только при клике пользователя
 * Экономит ~4.4 KiB JS и ~4.7s main-thread time на каждое видео
 */

(function() {
    'use strict';

    /**
     * Initialize all YouTube facades on the page
     */
    function initYouTubeFacades() {
        const facades = document.querySelectorAll('.youtube-facade:not(.youtube-facade--initialized)');

        facades.forEach(function(facade) {
            const videoId = facade.dataset.videoId;
            const startTime = facade.dataset.startTime || 0;

            if (!videoId) {
                console.warn('YouTube facade missing data-video-id attribute', facade);
                return;
            }

            // Load thumbnail image
            loadThumbnail(facade, videoId);

            // Add click listener
            facade.addEventListener('click', function() {
                loadYouTubeIframe(facade, videoId, startTime);
            });

            facade.classList.add('youtube-facade--initialized');
        });
    }

    /**
     * Load YouTube thumbnail image
     */
    function loadThumbnail(facade, videoId) {
        // Try to get high quality thumbnail first
        const imgHQ = new Image();
        imgHQ.src = `https://i.ytimg.com/vi/${videoId}/hqdefault.jpg`;

        imgHQ.onload = function() {
            // Check if it's a valid thumbnail (not the default gray placeholder)
            if (imgHQ.width > 120) {
                appendImage(facade, imgHQ.src);
            } else {
                // Fallback to medium quality
                appendImage(facade, `https://i.ytimg.com/vi/${videoId}/mqdefault.jpg`);
            }
        };

        imgHQ.onerror = function() {
            // Fallback to medium quality
            appendImage(facade, `https://i.ytimg.com/vi/${videoId}/mqdefault.jpg`);
        };
    }

    /**
     * Append image to facade
     */
    function appendImage(facade, src) {
        const img = document.createElement('img');
        img.src = src;
        img.alt = 'YouTube Video Thumbnail';
        img.loading = 'lazy';
        facade.appendChild(img);
    }

    /**
     * Load YouTube iframe when user clicks
     */
    function loadYouTubeIframe(facade, videoId, startTime) {
        // Prevent multiple loads
        if (facade.classList.contains('youtube-facade--active')) {
            return;
        }

        // Show loading state
        facade.classList.add('youtube-facade--loading');

        // Build iframe URL with parameters
        const params = [
            'autoplay=1',
            'modestbranding=1',
            'rel=0',
            'showinfo=0',
            'controls=1',
            'fs=0',
            'iv_load_policy=3',
            'disablekb=1',
            'playsinline=1'
        ];

        if (startTime && parseInt(startTime) > 0) {
            params.push(`start=${startTime}`);
        }

        const iframeUrl = `https://www.youtube.com/embed/${videoId}?${params.join('&')}`;

        // Create iframe
        const iframe = document.createElement('iframe');
        iframe.src = iframeUrl;
        iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
        iframe.allowFullscreen = true;
        iframe.title = 'YouTube Video';

        // Wait a bit for smooth transition
        setTimeout(function() {
            // Remove loading state
            facade.classList.remove('youtube-facade--loading');
            facade.classList.add('youtube-facade--active');

            // Remove thumbnail image
            const img = facade.querySelector('img');
            if (img) {
                img.remove();
            }

            // Append iframe
            facade.appendChild(iframe);
        }, 300);
    }

    /**
     * Initialize when DOM is ready
     */
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initYouTubeFacades);
    } else {
        initYouTubeFacades();
    }

    /**
     * Re-initialize if new facades are added dynamically
     */
    window.initYouTubeFacades = initYouTubeFacades;

})();
