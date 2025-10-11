/**
 * Related Services Widget
 * Automatically shows related services based on current page
 */

class RelatedServicesWidget {
    constructor() {
        this.currentService = this.detectCurrentService();
        this.relatedServices = this.getRelatedServices();
    }
    
    detectCurrentService() {
        const path = window.location.pathname;
        const serviceMatch = path.match(/\/services\/([^\/]+)/);
        return serviceMatch ? serviceMatch[1] : null;
    }
    
    getRelatedServices() {
        const serviceRelations = {
            'refrigerator-repair': [
                {
                    service: 'freezer-repair',
                    name: 'Freezer Repair',
                    icon: '🧊',
                    reason: 'Same cooling system issues'
                },
                {
                    service: 'ice-maker-repair',
                    name: 'Ice Maker Repair',
                    icon: '🧊',
                    reason: 'Part of refrigerator system'
                },
                {
                    service: 'dishwasher-repair',
                    name: 'Dishwasher Repair',
                    icon: '🍽️',
                    reason: 'Kitchen appliance package'
                }
            ],
            'washer-repair': [
                {
                    service: 'dryer-repair',
                    name: 'Dryer Repair',
                    icon: '🔥',
                    reason: 'Complete laundry solution'
                },
                {
                    service: 'dishwasher-repair',
                    name: 'Dishwasher Repair',
                    icon: '🍽️',
                    reason: 'Similar water-based issues'
                }
            ],
            'dryer-repair': [
                {
                    service: 'washer-repair',
                    name: 'Washer Repair',
                    icon: '🌊',
                    reason: 'Complete laundry solution'
                }
            ]
        };
        
        // Always add emergency service
        const emergency = {
            service: 'emergency',
            name: 'Emergency Service',
            icon: '🚨',
            reason: 'Available 24/7',
            urgent: true
        };
        
        const related = serviceRelations[this.currentService] || [];
        return [...related.slice(0, 2), emergency];
    }