/**
 * Universal Countdown Timer Script
 * Nika Appliance Repair
 * Works on all pages with countdown timer elements
 */

(function() {
    'use strict';

    // Configuration
    const TIMER_DURATION = 14 * 60 + 45; // 14 minutes 45 seconds
    const STORAGE_KEY = 'nikaCountdownEndTime';

    /**
     * Get or create countdown end time in localStorage
     * Timer persists across page refreshes within the session
     */
    function getEndTime() {
        let endTime = localStorage.getItem(STORAGE_KEY);

        if (!endTime || parseInt(endTime) < Date.now()) {
            // Create new end time
            endTime = Date.now() + (TIMER_DURATION * 1000);
            localStorage.setItem(STORAGE_KEY, endTime.toString());
        }

        return parseInt(endTime);
    }

    /**
     * Calculate remaining time in seconds
     */
    function getRemainingSeconds() {
        const endTime = getEndTime();
        const now = Date.now();
        const remaining = Math.floor((endTime - now) / 1000);

        return remaining > 0 ? remaining : 0;
    }

    /**
     * Reset timer to initial duration
     */
    function resetTimer() {
        const newEndTime = Date.now() + (TIMER_DURATION * 1000);
        localStorage.setItem(STORAGE_KEY, newEndTime.toString());
    }

    /**
     * Update timer display elements
     */
    function updateTimerDisplay() {
        let totalSeconds = getRemainingSeconds();

        // If timer reached 0, hide the countdown section
        if (totalSeconds === 0) {
            hideCountdownSection();
            return; // Stop updating
        }

        const minutes = Math.floor(totalSeconds / 60);
        const seconds = totalSeconds % 60;

        // Format with leading zeros
        const minutesFormatted = minutes.toString().padStart(2, '0');
        const secondsFormatted = seconds.toString().padStart(2, '0');

        // Update main timer elements
        const minutesEl = document.getElementById('timer-minutes');
        const secondsEl = document.getElementById('timer-seconds');

        if (minutesEl) minutesEl.textContent = minutesFormatted;
        if (secondsEl) secondsEl.textContent = secondsFormatted;

        // Update inline timer elements (if exists)
        const inlineMinutesEl = document.getElementById('inline-timer-minutes');
        const inlineSecondsEl = document.getElementById('inline-timer-seconds');

        if (inlineMinutesEl) inlineMinutesEl.textContent = minutesFormatted;
        if (inlineSecondsEl) inlineSecondsEl.textContent = secondsFormatted;

        // Update any other timer instances by class
        const allMinutes = document.querySelectorAll('.countdown-minutes');
        const allSeconds = document.querySelectorAll('.countdown-seconds');

        allMinutes.forEach(el => el.textContent = minutesFormatted);
        allSeconds.forEach(el => el.textContent = secondsFormatted);
    }

    /**
     * Hide countdown section when timer expires
     */
    function hideCountdownSection() {
        // Find and hide countdown sections by common class names and IDs
        const selectors = [
            '.countdown-section',
            '.deal-section',
            '#countdown',
            '#deal',
            '[class*="countdown"]',
            '[id*="countdown"]'
        ];

        selectors.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(el => {
                // Only hide if it contains timer elements
                if (el.querySelector('.countdown-minutes') ||
                    el.querySelector('.countdown-seconds') ||
                    el.querySelector('#timer-minutes') ||
                    el.querySelector('#timer-seconds')) {
                    el.style.display = 'none';
                }
            });
        });
    }

    /**
     * Initialize countdown timer
     */
    function initCountdownTimer() {
        // Check if timer elements exist on page
        const hasTimer = document.getElementById('timer-minutes') ||
                        document.getElementById('timer-seconds') ||
                        document.querySelector('.countdown-minutes');

        if (!hasTimer) {
            // No timer on this page, skip
            return;
        }

        // Update immediately
        updateTimerDisplay();

        // Update every second
        setInterval(updateTimerDisplay, 1000);
    }

    // Start timer when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCountdownTimer);
    } else {
        // DOM already loaded
        initCountdownTimer();
    }

    // Expose reset function globally if needed
    window.nikaResetTimer = resetTimer;

})();
