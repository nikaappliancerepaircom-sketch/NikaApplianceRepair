## Hero Section Icon Positioning Update

### Changes Made:

1. **WOW Text Color**
   - Already set to yellow (#FFD600) - no changes needed

2. **Floating Icon Positions Adjusted**
   - Icon 1: top: 5%, left: 5% (was 10%, 10%)
   - Icon 2: top: 10%, right: 5% (was 20%, 15%)
   - Icon 3: bottom: 10%, left: 5% (was 30%, 20%)
   - Icon 4: bottom: 5%, right: 5% (was 20%, 10%)
   - Icon 5: top: 50%, left: 2% (was 40%, 40%)
   - Icon 6: top: 60%, right: 2% (was 10%, 40%)
   
   Icons are now positioned closer to the edges to avoid overlapping with text and image.

3. **Animation Improvements**
   - Reduced movement range from 100px to 50px
   - Made rotation more subtle
   - Added overflow: hidden to hero-bg-animation container
   - Added pointer-events: none to prevent interaction

4. **Z-Index Hierarchy**
   - hero-bg-animation: z-index: 0 (background)
   - hero-content: z-index: 2 (main content)
   - hero-image: z-index: 3 (technician image on top)

5. **Container Constraints**
   - Added overflow: hidden to prevent icons from escaping bounds
   - Ensured icons stay within the hero section boundaries

The floating appliance icons now move more subtly around the edges of the hero section, avoiding the main content area where the text and technician image are displayed.