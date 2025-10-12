/**
 * Add Observation Form Handler
 * 
 * Manages the dynamic form selection and session handling for the Add Observation page.
 * Provides UI logic for switching between different observation types (Solar System, 
 * Star, Deep Sky, Special Event) and displays relevant forms and educational content.
 * 
 * Features:
 * - Dynamic form switching based on observation type
 * - Session selection propagation across forms
 * - Educational intro display for each observation type
 * - Form state management and navigation
 * 
 * @author Lodestar Project
 * @version 1.0.0
 */

document.addEventListener("DOMContentLoaded", function () {
    // Cache DOM elements for performance
    const sessionSelect = document.getElementById("session-select");
    const observationTypeSelect = document.getElementById("observation-type");
    const observationForms = document.querySelectorAll(
        "#observation-forms form"
    );
    const astronomicalIntros = document.querySelectorAll(
        "#astronomical-intros > div"
    );
    const goBackButtons = document.querySelectorAll(".js-go-back");

    /**
     * Handle observation type selection change
     * Shows appropriate form and educational content based on user selection
     */
    observationTypeSelect.addEventListener("change", function () {
        const selectedType = this.value;
        const selectedSession = sessionSelect.value;

        // Hide all forms and intros to reset the display
        observationForms.forEach((form) => {
            form.classList.add("hidden");
        });
        astronomicalIntros.forEach((intro) => {
            intro.classList.add("hidden");
        });

        // Show educational introduction for selected observation type
        if (selectedType) {
            const targetIntroId = selectedType + "-intro";
            const targetIntro = document.getElementById(targetIntroId);
            if (targetIntro) {
                targetIntro.classList.remove("hidden");
            }
        }

        // Show the observation form if both type and session are selected
        if (selectedType && selectedSession) {
            const targetFormId = selectedType + "-form";
            const targetForm = document.getElementById(targetFormId);

            if (targetForm) {
                targetForm.classList.remove("hidden");

                // Propagate selected session to the form fields
                const sessionInput = targetForm.querySelector(
                    'input[name="selected_session"]'
                );
                const sessionField = targetForm.querySelector(
                    'select[name="session"]'
                );
                if (sessionInput) sessionInput.value = selectedSession;
                if (sessionField) sessionField.value = selectedSession;

                // Hide the session field since we're selecting it above
                const sessionFieldContainer = targetForm
                    .querySelector('select[name="session"]')
                    ?.closest("div");
                if (sessionFieldContainer) {
                    sessionFieldContainer.classList.add("hidden");
                }
            }
        } else if (selectedType && !selectedSession) {
            alert("Please select an observing session first.");
            observationTypeSelect.value = "";
            // Hide intro if session not selected
            astronomicalIntros.forEach((intro) => {
                intro.classList.add("hidden");
            });
        }
    });

    // Handle session selection
    sessionSelect.addEventListener("change", function () {
        // If an observation type is already selected, update the form
        if (observationTypeSelect.value) {
            observationTypeSelect.dispatchEvent(new Event("change"));
        }
    });

    // Handle go back buttons
    goBackButtons.forEach((button) => {
        button.addEventListener("click", function () {
            // Hide all forms and intros
            observationForms.forEach((form) => {
                form.classList.add("hidden");
                form.classList.remove("active");
            });
            astronomicalIntros.forEach((intro) => {
                intro.classList.add("hidden");
            });

            // Reset selections
            observationTypeSelect.value = "";
        });
    });
});
