/**
 * Mobile Navigation Menu Handler
 * 
 * Manages the responsive mobile navigation menu functionality for the Lodestar application.
 * Handles menu toggle on button click and auto-closes the menu when clicking outside.
 * 
 * @author Lodestar Project
 * @version 1.0.0
 */

document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements for mobile menu functionality
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    // Only initialize if both required elements exist
    if (mobileMenuButton && mobileMenu) {
        /**
         * Toggle mobile navigation menu visibility
         * Adds/removes 'hidden' class to show/hide the mobile menu
         */
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
        
        /**
         * Auto-close mobile menu when clicking outside
         * Improves UX by closing menu when user clicks elsewhere on page
         */
        document.addEventListener('click', function(event) {
            // Check if click is outside both menu button and menu content
            if (!mobileMenuButton.contains(event.target) && !mobileMenu.contains(event.target)) {
                mobileMenu.classList.add('hidden');
            }
        });
    }
});