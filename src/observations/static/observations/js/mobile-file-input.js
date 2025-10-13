// Mobile file input enhancements
document.addEventListener('DOMContentLoaded', function() {
    // Function to truncate long file names on mobile
    function truncateFileName(input) {
        const maxLength = window.innerWidth < 640 ? 20 : 40; // Shorter on mobile
        const files = input.files;
        
        if (files.length > 0) {
            const fileName = files[0].name;
            
            // Create a truncated display name
            if (fileName.length > maxLength) {
                const extension = fileName.split('.').pop();
                const nameWithoutExtension = fileName.substring(0, fileName.lastIndexOf('.'));
                const truncatedName = nameWithoutExtension.substring(0, maxLength - extension.length - 4) + '...' + '.' + extension;
                
                // Create or update a display label
                let displayLabel = input.parentNode.querySelector('.file-name-display');
                if (!displayLabel) {
                    displayLabel = document.createElement('span');
                    displayLabel.className = 'file-name-display text-sm text-gray-400 mt-1 block';
                    input.parentNode.appendChild(displayLabel);
                }
                displayLabel.textContent = 'Selected: ' + truncatedName;
            }
        }
    }
    
    // Add event listeners to all file inputs
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            truncateFileName(this);
        });
    });
    
    // Handle window resize to adjust truncation
    window.addEventListener('resize', function() {
        fileInputs.forEach(function(input) {
            if (input.files.length > 0) {
                truncateFileName(input);
            }
        });
    });
});