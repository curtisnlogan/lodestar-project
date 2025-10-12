document.addEventListener("DOMContentLoaded", function () {
    const sessionSelect = document.getElementById("session-select");
    const observationTypeSelect = document.getElementById("observation-type");
    const observationForms = document.querySelectorAll(
        "#observation-forms form"
    );
    const astronomicalIntros = document.querySelectorAll(
        "#astronomical-intros > div"
    );
    const goBackButtons = document.querySelectorAll(".js-go-back");

    // Handle observation type selection
    observationTypeSelect.addEventListener("change", function () {
        const selectedType = this.value;
        const selectedSession = sessionSelect.value;

        // Hide all forms and intros
        observationForms.forEach((form) => {
            form.classList.add("hidden");
        });
        astronomicalIntros.forEach((intro) => {
            intro.classList.add("hidden");
        });

        if (selectedType) {
            // Show the corresponding astronomical introduction
            const targetIntroId = selectedType + "-intro";
            const targetIntro = document.getElementById(targetIntroId);
            if (targetIntro) {
                targetIntro.classList.remove("hidden");
            }
        }

        if (selectedType && selectedSession) {
            // Show the selected form
            const targetFormId = selectedType + "-form";
            const targetForm = document.getElementById(targetFormId);

            if (targetForm) {
                targetForm.classList.remove("hidden");

                // Set the selected session in the form
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
