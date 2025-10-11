/**
 * Dynamic Breadcrumb System
 * Automatically generates breadcrumb navigation with Schema markup
 */

class BreadcrumbSystem {
    constructor() {
        this.currentPath = window.location.pathname;
        this.pathSegments = this.currentPath.split('/').filter(segment => segment);
        this.breadcrumbData = this.generateBreadcrumbData();
    }
    
    generateBreadcrumbData() {
        const breadcrumbs = [
            {
                name: 'Home',
                url: '/',
                position: 1
            }
        ];
        
        let currentPath = '';
        this.pathSegments.forEach((segment, index) => {
            currentPath += `/${segment}`;
            breadcrumbs.push({
                name: this.formatSegmentName(segment),
                url: currentPath,
                position: index + 2
            });
        });
        
        return breadcrumbs;
    }
    
    formatSegmentName(segment) {
        // Convert URL segment to readable name
        const nameMap = {
            'services': 'Services',
            'locations': 'Service Areas',
            'brands': 'Brands We Service',
            'refrigerator-repair': 'Refrigerator Repair',
            'washer-repair': 'Washer Repair',
            'dryer-repair': 'Dryer Repair',
            'dishwasher-repair': 'Dishwasher Repair',
            'oven-repair': 'Oven Repair',
            'stove-repair': 'Stove Repair',
            'downtown': 'Downtown',
            'north-side': 'North Side',
            'south-side': 'South Side'
        };
        
        return nameMap[segment] || segment.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }