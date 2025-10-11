/**
 * Smart Popup System for Nika Appliance Repair
 * Conversion-optimized popup management
 */

class SmartPopupSystem {
    constructor() {
        this.popupsShown = [];
        this.userBehavior = {
            timeOnSite: 0,
            scrollDepth: 0,
            pageViews: 1,
            isReturning: this.checkReturningVisitor(),
            deviceType: this.getDeviceType(),
            referrer: document.referrer,
            currentPage: window.location.pathname
        };
        
        this.initializeTracking();
        this.loadPopupTemplates();
    }
    
    // Initialize behavior tracking
    initializeTracking() {
        // Time tracking
        this.startTime = Date.now();
        setInterval(() => {
            this.userBehavior.timeOnSite = Math.floor((Date.now() - this.startTime) / 1000);
            this.checkPopupTriggers();
        }, 1000);
        
        // Scroll tracking
        window.addEventListener('scroll', () => {
            const scrolled = window.scrollY;
            const height = document.documentElement.scrollHeight - window.innerHeight;
            this.userBehavior.scrollDepth = Math.round((scrolled / height) * 100);
        });        
        // Exit intent tracking
        document.addEventListener('mouseout', (e) => {
            if (e.clientY <= 0 && !this.hasShownExitPopup) {
                this.showExitIntentPopup();
            }
        });
        
        // Form abandonment tracking
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            let formStartTime = null;
            
            form.addEventListener('focusin', () => {
                if (!formStartTime) formStartTime = Date.now();
            });
            
            form.addEventListener('focusout', (e) => {
                if (!form.contains(e.relatedTarget)) {
                    const timeSpent = (Date.now() - formStartTime) / 1000;
                    if (timeSpent > 10 && !form.querySelector('[type="submit"]:focus')) {
                        this.showFormAbandonmentPopup();
                    }
                }
            });
        });
    }
    
    // Check popup triggers
    checkPopupTriggers() {
        // Time-based welcome popup
        if (this.userBehavior.timeOnSite === 30 && !this.hasShownPopup('welcome')) {
            this.showWelcomePopup();
        }    
    canShowPopup() {
        // Check if already converted
        if (this.hasConverted) return false;
        
        // Check popup limit
        if (this.popupsShown.length >= this.maxPopups) return false;
        
        // Check time gap
        if (this.lastPopupTime) {
            const timeSinceLastPopup = Date.now() - this.lastPopupTime;
            if (timeSinceLastPopup < this.minimumGap) return false;
        }
        
        // Check if popup currently showing
        if (document.querySelector('.smart-popup.active')) return false;
        
        return true;
    }
    
    showPopup(type, content) {
        if (!this.canShowPopup()) return;
        
        // Record popup
        this.popupsShown.push({
            type: type,
            timestamp: Date.now(),
            page: window.location.pathname
        });
        
        // Save to session
        sessionStorage.setItem('popupsShown', JSON.stringify(this.popupsShown));
        this.lastPopupTime = Date.now();
        
        // Show the popup
        this.renderPopup(type, content);
    }
    
    determineSecondPopup() {
        const behavior = this.analyzeBehavior();
        
        if (behavior.device === 'mobile' && behavior.scrollDepth > 50) {
            return 'mobileCallPrompt';
        }
        
        if (behavior.timeOnPage > 60 && behavior.pageType === 'service') {
            return 'timeBasedHelper';
        }
        
        if (behavior.scrollDepth > 75) {
            return 'scrollBasedOffer';
        }
        
        if (behavior.formStarted && !behavior.formCompleted) {
            return 'formAbandonment';
        }
        
        return 'timeBasedHelper'; // default
    }
}