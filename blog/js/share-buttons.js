/**
 * Share Button Handler
 * Handles social media sharing for blog posts
 * Platforms: Facebook, Twitter, LinkedIn, Email
 */

document.addEventListener('DOMContentLoaded', function() {
    const shareButtons = document.querySelectorAll('.social-share .share-btn');

    if (shareButtons.length === 0) {
        console.warn('No share buttons found on this page');
        return;
    }

    // Get current page details
    const pageUrl = window.location.href;
    const pageTitle = document.querySelector('.blog-title')?.textContent || document.title;
    const pageDescription = document.querySelector('meta[name="description"]')?.getAttribute('content') || '';

    shareButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();

            const platform = this.classList[1]; // Get the platform class (facebook, twitter, linkedin, email)

            switch(platform) {
                case 'facebook':
                    shareFacebook(pageUrl);
                    break;
                case 'twitter':
                    shareTwitter(pageUrl, pageTitle);
                    break;
                case 'linkedin':
                    shareLinkedIn(pageUrl, pageTitle, pageDescription);
                    break;
                case 'email':
                    shareEmail(pageUrl, pageTitle);
                    break;
                default:
                    console.warn('Unknown share platform:', platform);
            }
        });
    });

    /**
     * Share on Facebook
     * Opens Facebook Share Dialog with current page URL
     */
    function shareFacebook(url) {
        const facebookShareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`;
        openShareWindow(facebookShareUrl, 'Facebook Share', 600, 400);
    }

    /**
     * Share on Twitter
     * Opens Twitter share intent with URL and title
     */
    function shareTwitter(url, title) {
        const twitterShareUrl = `https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}`;
        openShareWindow(twitterShareUrl, 'Twitter Share', 600, 400);
    }

    /**
     * Share on LinkedIn
     * Opens LinkedIn share dialog with URL and title
     */
    function shareLinkedIn(url, title, description) {
        const linkedInShareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`;
        openShareWindow(linkedInShareUrl, 'LinkedIn Share', 600, 500);
    }

    /**
     * Share via Email
     * Opens default email client with subject and body
     */
    function shareEmail(url, title) {
        const subject = encodeURIComponent(`Check this out: ${title}`);
        const body = encodeURIComponent(`I found this interesting article: ${url}`);
        window.location.href = `mailto:?subject=${subject}&body=${body}`;
    }

    /**
     * Helper function to open share window
     * @param {string} url - The share URL
     * @param {string} windowName - Name for the popup window
     * @param {number} width - Window width
     * @param {number} height - Window height
     */
    function openShareWindow(url, windowName, width, height) {
        const left = (screen.width - width) / 2;
        const top = (screen.height - height) / 2;

        const windowFeatures = `
            width=${width},
            height=${height},
            left=${left},
            top=${top},
            resizable=yes,
            scrollbars=yes,
            status=yes
        `.replace(/\s+/g, '');

        try {
            window.open(url, windowName, windowFeatures);
        } catch (error) {
            console.error('Error opening share window:', error);
            // Fallback: open in regular window if popup blocked
            window.open(url, '_blank');
        }
    }
});
