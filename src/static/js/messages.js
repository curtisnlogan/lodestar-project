/**
 * Handles auto-hiding and manual dismissal by user of Django messages in base.html
 */

document.addEventListener("DOMContentLoaded", function () {
    // code below only runs when page is fully loaded
    const messages = document.querySelectorAll(".message-alert");
    // loop through all messages in array
    messages.forEach(function (message) {
        // Auto-hide message div after 5 seconds
        setTimeout(function () {
            hideMessage(message);
        }, 5000);

        // Manual close button functionality
        const closeButton = message.querySelector(".close-message");
        if (closeButton) {
            closeButton.addEventListener("click", function () {
                hideMessage(message);
            });
        }
    });
    // modifies css properties to hide django messages and then remove after delay with `setTimout`
    function hideMessage(message) {
        message.style.opacity = "0";
        message.style.transform = "translateY(-20px)";
        setTimeout(function () {
            message.remove();
        }, 300);
    }
});
