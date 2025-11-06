/**
 * Responsive Tables Script
 * Automatically wraps all tables in the blog content with a scrollable wrapper
 * This prevents tables from breaking the mobile layout
 */

document.addEventListener('DOMContentLoaded', function() {
    // Find all tables in the blog content
    const blogContent = document.querySelector('.blog-content');

    if (blogContent) {
        const tables = blogContent.querySelectorAll('table');

        tables.forEach(function(table) {
            // Check if the table is not already wrapped
            if (!table.parentElement.classList.contains('table-wrapper')) {
                // Create wrapper div
                const wrapper = document.createElement('div');
                wrapper.className = 'table-wrapper';

                // Insert wrapper before table
                table.parentNode.insertBefore(wrapper, table);

                // Move table into wrapper
                wrapper.appendChild(table);
            }
        });

        console.log(`Wrapped ${tables.length} tables in responsive wrappers`);
    }
});
