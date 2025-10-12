// observation_detail.js - JavaScript for observation detail page functionality

// Global variables for state management
let apiCallInProgress = false;
let editMode = false;

// DOM Content Loaded Event
document.addEventListener("DOMContentLoaded", function () {
    console.log("Observation detail page loaded");
    initializePage();
});

// Initialize page state
function initializePage() {
    // Ensure API content is visible by default
    const apiContent = document.getElementById("api-content");
    const apiErrorContent = document.getElementById("api-error-content");

    if (apiContent) {
        apiContent.classList.remove("hidden");
        apiContent.classList.add("block");
    }
    if (apiErrorContent) {
        apiErrorContent.classList.add("hidden");
        apiErrorContent.classList.remove("block");
    }

    // Hide action buttons initially
    const actionButtons = document.querySelector(".action-buttons");
    if (actionButtons) {
        actionButtons.classList.add("hidden");
    }

    // Initialize event listeners
    initializeEventListeners();
}

// Initialize event listeners
function initializeEventListeners() {
    // Edit button functionality
    const editButton = document.querySelector(".edit-data-button");
    if (editButton) {
        editButton.addEventListener("click", toggleEditMode);
    }

    // Submit button functionality
    const submitButton = document.querySelector(".submit-update-button");
    if (submitButton) {
        submitButton.addEventListener("click", submitUpdate);
    }

    // Cancel button functionality
    const cancelButton = document.querySelector(".cancel-edit-button");
    if (cancelButton) {
        cancelButton.addEventListener("click", toggleEditMode);
    }

    // Retry API button functionality
    const retryButton = document.querySelector(".retry-api-button");
    if (retryButton) {
        retryButton.addEventListener("click", retryApiCall);
    }
}

// Show/hide API error state
function showApiError() {
    const apiContent = document.getElementById("api-content");
    const apiErrorContent = document.getElementById("api-error-content");
    const apiErrorMessage = document.getElementById("api-error-message");

    if (apiContent) {
        apiContent.classList.remove("block");
        apiContent.classList.add("hidden");
    }
    if (apiErrorContent) {
        apiErrorContent.classList.remove("hidden");
        apiErrorContent.classList.add("block");
    }
    if (apiErrorMessage) {
        apiErrorMessage.classList.remove("hidden");
    }
}

// Show/hide API success state
function showApiSuccess() {
    const apiContent = document.getElementById("api-content");
    const apiErrorContent = document.getElementById("api-error-content");
    const apiErrorMessage = document.getElementById("api-error-message");

    if (apiContent) {
        apiContent.classList.remove("hidden");
        apiContent.classList.add("block");
    }
    if (apiErrorContent) {
        apiErrorContent.classList.add("hidden");
        apiErrorContent.classList.remove("block");
    }
    if (apiErrorMessage) {
        apiErrorMessage.classList.add("hidden");
    }
}

// Show update success message
function showUpdateSuccess() {
    hideAllMessages();
    const successMessage = document.getElementById("update-success-message");
    if (successMessage) {
        successMessage.classList.remove("hidden");
        // Auto-hide after 5 seconds
        setTimeout(() => {
            successMessage.classList.add("hidden");
        }, 5000);
    }
}

// Show update error message
function showUpdateError() {
    hideAllMessages();
    const errorMessage = document.getElementById("update-error-message");
    if (errorMessage) {
        errorMessage.classList.remove("hidden");
    }
}

// Hide all message banners
function hideAllMessages() {
    const messages = [
        "api-error-message",
        "update-success-message",
        "update-error-message",
    ];

    messages.forEach((messageId) => {
        const element = document.getElementById(messageId);
        if (element) {
            element.classList.add("hidden");
        }
    });
}

// Retry API call function
function retryApiCall() {
    if (apiCallInProgress) return;

    apiCallInProgress = true;
    const retryButton = document.querySelector(".retry-api-button");

    if (retryButton) {
        retryButton.textContent = "🔄 Retrying...";
        retryButton.disabled = true;
    }

    // Simulate API call (replace with actual API call later)
    setTimeout(() => {
        // For demo purposes, randomly succeed or fail
        const success = Math.random() > 0.3; // 70% success rate

        if (success) {
            showApiSuccess();
        } else {
            // Reset button state for another retry
            if (retryButton) {
                retryButton.textContent = "🔄 Retry API Call";
                retryButton.disabled = false;
            }
        }

        apiCallInProgress = false;
    }, 2000);
}

// Toggle edit mode for observation data
function toggleEditMode() {
    editMode = !editMode;
    const formFields = document.querySelectorAll(".form-fields input, .form-fields textarea, .form-fields select");
    const editButton = document.querySelector(".edit-data-button");
    const actionButtons = document.querySelector(".action-buttons");

    if (editMode) {
        // Enable editing for crispy form fields
        formFields.forEach((field) => {
            field.disabled = false;
            // Remove any previous validation styling
            field.classList.remove("border-red-500", "border-emerald-500");
        });
        
        if (editButton) {
            editButton.textContent = "Cancel Edit";
            editButton.className =
                "edit-data-button bg-nebula text-white px-4 py-2 rounded-md hover:bg-nebula-hover transition-colors text-sm";
        }
        if (actionButtons) {
            actionButtons.classList.remove("hidden");
        }
    } else {
        // Disable editing for all form fields
        formFields.forEach((field) => {
            field.disabled = true;
            // Clear validation styling
            field.classList.remove("border-red-500", "border-emerald-500");
        });
        
        if (editButton) {
            editButton.textContent = "Edit data";
            editButton.className =
                "edit-data-button bg-accent hover:bg-highlight text-white hover:text-black px-4 py-2 rounded-md transition-all duration-500 ease-in-out font-medium tracking-wide transform hover:scale-105 text-sm";
        }
        if (actionButtons) {
            actionButtons.classList.add("hidden");
        }
        hideAllMessages();
    }
}

// Submit observation updates
function submitUpdate() {
    console.log("Submit button clicked - starting form submission");

    const form = document.getElementById("observation-form");
    
    // Disable submit button during request to prevent double submissions
    const submitButton = document.querySelector(".submit-update-button");
    const originalText = submitButton.textContent;
    submitButton.disabled = true;
    submitButton.textContent = "Updating...";

    // Use standard form submission - Django and Crispy Forms handle all validation
    console.log("Submitting form to Django for validation and processing...");
    form.submit();
}

// Utility function to get CSRF token for Django forms
function getCSRFToken() {
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]");
    return csrfToken ? csrfToken.value : "";
}

// Export functions for potential external use
window.ObservationDetail = {
    showApiError,
    showApiSuccess,
    toggleEditMode,
    submitUpdate,
    retryApiCall,
};
