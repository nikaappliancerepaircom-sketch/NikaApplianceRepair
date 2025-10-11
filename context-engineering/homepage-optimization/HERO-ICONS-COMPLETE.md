# Fixed Floating Icons Section

## Instructions:
Replace the entire hero-bg-animation div in the optimized file (starting at line 103) with the complete version below.

## Find this section:
```html
<div class="hero-bg-animation">
    <!-- Refrigerator Icon -->
    ...
    <!-- Additional floating icons remain the same -->
</div>
```

## Replace with:
```html
<div class="hero-bg-animation">
    <!-- Refrigerator Icon -->
    <div class="floating-icon icon-1">
        <svg width="60" height="60" viewBox="0 0 100 100" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
            <rect x="20" y="10" width="60" height="80" rx="8" fill="currentColor"/>
            <rect x="25" y="15" width="50" height="35" rx="4" fill="currentColor" opacity="0.3"/>
            <rect x="25" y="55" width="50" height="30" rx="4" fill="currentColor" opacity="0.3"/>
            <rect x="65" y="60" width="6" height="20" rx="3" fill="currentColor" opacity="0.6"/>
        </svg>
    </div>
    <!-- Washing Machine Icon -->
    <div class="floating-icon icon-2">
        <svg width="60" height="60" viewBox="0 0 100 100" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
            <rect x="15" y="10" width="70" height="80" rx="8" fill="currentColor"/>
            <circle cx="50" cy="55" r="25" fill="currentColor" opacity="0.3"/>
            <circle cx="50" cy="55" r="20" fill="currentColor" opacity="0.2"/>
        </svg>
    </div>
    <!-- Dishwasher Icon -->
    <div class="floating-icon icon-3">
        <svg width="60" height="60" viewBox="0 0 100 100" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
            <rect x="15" y="20" width="70" height="60" rx="6" fill="currentColor"/>
            <rect x="20" y="25" width="60" height="45" rx="4" fill="currentColor" opacity="0.3"/>
            <circle cx="30" cy="75" r="2" fill="currentColor" opacity="0.6"/>
            <circle cx="40" cy="75" r="2" fill="currentColor" opacity="0.6"/>
            <circle cx="50" cy="75" r="2" fill="currentColor" opacity="0.6"/>
        </svg>
    </div>
    <!-- Dryer Icon -->
    <div class="floating-icon icon-4">
        <svg width="60" height="60" viewBox="0 0 100 100" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
            <rect x="15" y="15" width="70" height="70" rx="8" fill="currentColor"/>
            <circle cx="50" cy="50" r="25" fill="currentColor" opacity="0.3"/>
            <circle cx="30" cy="24" r="3" fill="currentColor" opacity="0.6"/>
            <circle cx="40" cy="24" r="3" fill="currentColor" opacity="0.6"/>
        </svg>
    </div>
    <!-- Stove Icon -->
    <div class="floating-icon icon-5">
        <svg width="60" height="60" viewBox="0 0 100 100" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
            <rect x="10" y="40" width="80" height="45" rx="6" fill="currentColor"/>
            <circle cx="30" cy="60" r="12" fill="currentColor" opacity="0.3"/>
            <circle cx="70" cy="60" r="12" fill="currentColor" opacity="0.3"/>
            <circle cx="20" cy="75" r="4" fill="currentColor" opacity="0.6"/>
            <circle cx="80" cy="75" r="4" fill="currentColor" opacity="0.6"/>
        </svg>
    </div>
    <!-- Oven Icon -->
    <div class="floating-icon icon-6">
        <svg width="60" height="60" viewBox="0 0 100 100" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
            <rect x="15" y="20" width="70" height="65" rx="6" fill="currentColor"/>
            <rect x="20" y="40" width="60" height="40" rx="4" fill="currentColor" opacity="0.3"/>
            <rect x="25" y="45" width="50" height="30" rx="3" fill="currentColor" opacity="0.2"/>
            <circle cx="30" cy="30" r="3" fill="currentColor" opacity="0.6"/>
            <circle cx="50" cy="30" r="3" fill="currentColor" opacity="0.6"/>
        </svg>
    </div>
</div>
```

This includes all 6 appliance icons:
1. Refrigerator (icon-1)
2. Washing Machine (icon-2)
3. Dishwasher (icon-3)
4. Dryer (icon-4)
5. Stove (icon-5)
6. Oven (icon-6)

These will float and animate around the blue hero background as intended.