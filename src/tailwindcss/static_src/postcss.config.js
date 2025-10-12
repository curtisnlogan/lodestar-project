/**
 * PostCSS Configuration for Lodestar Project
 * 
 * Configures PostCSS plugins for processing CSS in the Tailwind CSS pipeline.
 * This configuration enables:
 * - Tailwind CSS processing for utility-first CSS framework
 * - CSS variables support for dynamic theming
 * - CSS nesting for improved stylesheet organization
 * 
 * Used by the Django Tailwind CSS integration to process stylesheets
 * during development and production builds.
 * 
 * @see {@link https://postcss.org/} PostCSS Documentation
 * @see {@link https://tailwindcss.com/docs/using-with-preprocessors} Tailwind with PostCSS
 */
module.exports = {
  plugins: {
    // Tailwind CSS processor - handles utility class generation and purging
    "@tailwindcss/postcss": {},
    
    // CSS variables support - enables dynamic theming and custom properties
    "postcss-simple-vars": {},
    
    // CSS nesting support - allows nested CSS rules for better organization
    "postcss-nested": {}
  },
}
