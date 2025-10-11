/**
 * Dynamic Urgency Elements System
 * Creates real-time urgency and scarcity indicators
 */

class UrgencySystem {
    constructor() {
        this.config = {
            updateInterval: 60000, // Update every minute
            peakHours: { start: 16, end: 20 }, // 4 PM - 8 PM
            baseAvailability: 8, // Base number of daily slots
            bookingRate: 0.7 // 70% booking rate simulation
        };
        
        this.elements = {
            availabilityWidget: '.availability-widget',
            urgencyBanner: '.urgency-banner',
            countdown: '.countdown-timer',
            recentActivity: '.recent-activity',
            slotsRemaining: '.slots-remaining'
        };
        
        this.init();
    }
    
    init() {
        this.updateAvailability();
        this.startCountdowns();
        this.showRecentActivity();
        
        // Update periodically
        setInterval(() => {
            this.updateAvailability();
        }, this.config.updateInterval);
    }