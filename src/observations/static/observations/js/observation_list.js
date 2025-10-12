// observation_list.js
// Handles infinite scroll, filtering, and dynamic updates for the observations list page

document.addEventListener("DOMContentLoaded", function () {
    let currentPage = 1;
    let isLoading = false;
    let hasMore = true;
    const observationsContainer = document.getElementById(
        "observations-container"
    );
    const loadingIndicator = document.getElementById("loading-indicator");
    const filterForm = document.getElementById("filter-form");
    const clearFiltersBtn = document.getElementById("clear-filters");

    // Get current filters from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const initialFilters = {
        session: urlParams.get("session") || "",
        object_type: urlParams.get("object_type") || "",
        search: urlParams.get("search") || "",
    };

    // Initialize filters in form
    document.getElementById("session-filter").value = initialFilters.session;
    document.getElementById("object-type-filter").value =
        initialFilters.object_type;
    document.getElementById("search-filter").value = initialFilters.search;

    // Update hasMore based on initial load
    hasMore = document.querySelector("[data-has-next]")
        ? document.querySelector("[data-has-next]").dataset.hasNext === "True"
        : false;

    // Infinite scroll functionality
    function loadMoreObservations() {
        if (isLoading || !hasMore) return;

        isLoading = true;
        loadingIndicator.classList.remove("hidden");

        const nextPage = currentPage + 1;
        const currentFilters = getCurrentFilters();

        // Build URL with current filters and next page
        const params = new URLSearchParams(currentFilters);
        params.set("page", nextPage);

        fetch(`${window.location.pathname}?${params.toString()}`, {
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            },
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.observations && data.observations.length > 0) {
                    appendObservations(data.observations);
                    currentPage = nextPage;
                    hasMore = data.has_next;
                } else {
                    hasMore = false;
                }
            })
            .catch((error) => {
                console.error("Error loading more observations:", error);
                showErrorMessage(
                    "Failed to load more observations. Please try again."
                );
            })
            .finally(() => {
                isLoading = false;
                loadingIndicator.classList.add("hidden");

                // Show end message if no more results
                if (!hasMore && !document.querySelector(".end-of-results")) {
                    const endMessage = document.createElement("div");
                    endMessage.className =
                        "end-of-results p-4 text-center text-gray-500 text-sm";
                    endMessage.innerHTML =
                        "<!-- INFINITE SCROLL --><br>End of observations";
                    observationsContainer.parentNode.appendChild(endMessage);
                }
            });
    }

    // Append new observations to the container
    function appendObservations(observations) {
        observations.forEach((obs) => {
            const observationRow = createObservationRow(obs);
            observationsContainer.appendChild(observationRow);
        });
    }

    // Create HTML for an observation row
    function createObservationRow(obs) {
        const row = document.createElement("div");
        row.className =
            "observation-row grid grid-cols-1 md:grid-cols-6 gap-4 p-4 border-b border-gray-700 hover:bg-nebula-hover transition-colors";

        // Format the created_at timestamp
        const createdAt = new Date(obs.created_at);
        const formattedCreatedAt = createdAt.toLocaleDateString() + ' ' + createdAt.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        
        // Calculate relative time
        const relativeTime = getRelativeTime(createdAt);

        // Extract and format session date from slug
        const sessionDate = extractDateFromSlug(obs.session_slug).toUpperCase();

        row.innerHTML = `
            <!-- Session -->
            <div class="md:col-span-1">
                <div class="md:hidden text-sm font-medium text-gray-400 mb-1">Session:</div>
                <div class="text-white text-sm">${sessionDate}</div>
            </div>
            
            <!-- Observation Type -->
            <div class="md:col-span-1">
                <div class="md:hidden text-sm font-medium text-gray-400 mb-1">Observation:</div>
                <div class="text-white">${obs.object_type}</div>
            </div>
            
            <!-- Date/Time -->
            <div class="md:col-span-1">
                <div class="md:hidden text-sm font-medium text-gray-400 mb-1">Created:</div>
                <div class="text-white">${formattedCreatedAt}</div>
                <div class="text-xs text-gray-400" title="Session: ${obs.date_time}">${relativeTime}</div>
            </div>
            
            <!-- Object -->
            <div class="md:col-span-1">
                <div class="md:hidden text-sm font-medium text-gray-400 mb-1">Object:</div>
                <div class="text-white font-medium">${obs.object_name}</div>
            </div>
            
            <!-- Actions -->
            <div class="md:col-span-2 flex flex-col md:flex-row space-y-2 md:space-y-0 md:space-x-2 md:justify-center">
                <button class="delete-btn bg-red-900 text-white px-4 py-1 rounded-md hover:bg-red-700 transition-colors text-sm"
                        data-id="${obs.id}" data-type="${obs.type_class}" data-created-at="${obs.created_at}">
                    Delete
                </button>
                <button class="view-update-btn bg-accent text-white px-4 py-1 rounded-md hover:bg-blue-700 transition-colors text-sm"
                        data-id="${obs.id}" data-type="${obs.type_class}" data-created-at="${obs.created_at}">
                    View/Update
                </button>
            </div>
        `;

        // Add event listeners to the new buttons
        addButtonEventListeners(row);

        return row;
    }

    // Get current filter values
    function getCurrentFilters() {
        return {
            session: document.getElementById("session-filter").value,
            object_type: document.getElementById("object-type-filter").value,
            search: document.getElementById("search-filter").value,
        };
    }

    // Handle filter form submission
    function handleFilterSubmit(event) {
        event.preventDefault();
        applyFilters();
    }

    // Apply filters and reload the page
    function applyFilters() {
        const filters = getCurrentFilters();
        const params = new URLSearchParams();

        // Only add non-empty filters to URL
        Object.keys(filters).forEach((key) => {
            if (filters[key]) {
                params.set(key, filters[key]);
            }
        });

        // Reload page with new filters
        const newUrl = params.toString()
            ? `${window.location.pathname}?${params.toString()}`
            : window.location.pathname;

        window.location.href = newUrl;
    }

    // Clear all filters
    function clearFilters() {
        document.getElementById("session-filter").value = "";
        document.getElementById("object-type-filter").value = "";
        document.getElementById("search-filter").value = "";

        // Reload page without filters
        window.location.href = window.location.pathname;
    }

    // Show message (success or error)
    function showMessage(message, type = "success") {
        const div = document.createElement("div");
        div.className =
            (type === "success" ? "bg-green-600" : "bg-red-600") +
            " text-white p-3 rounded-md mb-4 fixed top-4 right-4 z-50";
        div.textContent = message;

        document.body.appendChild(div);

        setTimeout(() => {
            if (div.parentNode) {
                div.parentNode.removeChild(div);
            }
        }, 5000);
    }

    function showErrorMessage(message) {
        showMessage(message, "error");
    }

    function showSuccessMessage(message) {
        showMessage(message, "success");
    }

    // Add event listeners to action buttons
    function addButtonEventListeners(container) {
        const deleteButtons = container.querySelectorAll(".delete-btn");
        const viewUpdateButtons =
            container.querySelectorAll(".view-update-btn");

        deleteButtons.forEach((btn) => {
            btn.addEventListener("click", handleDeleteObservation);
        });

        viewUpdateButtons.forEach((btn) => {
            btn.addEventListener("click", handleViewUpdateObservation);
        });
    }

    // Handle delete observation
    function handleDeleteObservation(event) {
        const button = event.target;
        const obsId = button.dataset.id;
        const obsType = button.dataset.type;

        if (
            confirm(
                "Are you sure you want to delete this observation? This action cannot be undone."
            )
        ) {
            // Disable the button and show loading state
            button.disabled = true;
            button.textContent = "Deleting...";

            // Get CSRF token
            const csrfTokenElement = document.querySelector(
                "[name=csrfmiddlewaretoken]"
            );
            if (!csrfTokenElement) {
                console.error("CSRF token not found");
                showErrorMessage(
                    "CSRF token not found - please refresh the page"
                );
                button.disabled = false;
                button.textContent = "Delete";
                return;
            }
            const csrfToken = csrfTokenElement.value;
            console.log("CSRF token found:", csrfToken ? "yes" : "no");

            const deleteUrl = `/observations/delete/${obsType}/${obsId}/`;
            console.log("Making request to:", deleteUrl);

            // Make AJAX request to delete the observation
            fetch(deleteUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
                credentials: "same-origin",
            })
                .then((response) => {
                    console.log("Response status:", response.status);
                    return response.json();
                })
                .then((data) => {
                    console.log("Response data:", data);
                    if (data.success) {
                        // Show success message
                        showSuccessMessage(data.message);

                        // Remove the observation from the DOM
                        const observationRow =
                            button.closest(".observation-row");
                        if (observationRow) {
                            observationRow.style.transition =
                                "opacity 0.3s ease";
                            observationRow.style.opacity = "0";
                            setTimeout(() => {
                                observationRow.remove();
                                updateObservationCount();
                            }, 300);
                        }
                    } else {
                        // Show error message
                        showErrorMessage(
                            data.error || "Failed to delete observation"
                        );
                        // Re-enable button
                        button.disabled = false;
                        button.textContent = "Delete";
                    }
                })
                .catch((error) => {
                    console.error("Error deleting observation:", error);
                    showErrorMessage(
                        "An error occurred while deleting the observation"
                    );
                    // Re-enable button
                    button.disabled = false;
                    button.textContent = "Delete";
                });
        }
    }

    // Update observation count after deletion
    function updateObservationCount() {
        const remainingObservations =
            document.querySelectorAll(".observation-row").length;
        const countElement = document.querySelector(
            ".text-4xl.font-bold.text-blue-400"
        );
        if (countElement) {
            countElement.textContent = remainingObservations;
        }

        // Update the pluralization text
        const pluralElement = countElement?.parentNode.querySelector(
            ".text-lg.text-white"
        );
        if (pluralElement) {
            pluralElement.textContent =
                remainingObservations === 1 ? "Observation" : "Observations";
        }

        // Show "no observations" message if none left
        if (remainingObservations === 0) {
            const container = document.getElementById("observations-container");
            if (container) {
                container.innerHTML = `
                    <div class="p-8 text-center text-gray-400">
                        No observations found. <a href="/observations/add/" class="text-blue-400 hover:text-blue-300 underline">Add your first observation!</a>
                    </div>
                `;
            }
        }
    }

    // Handle view/update observation
    function handleViewUpdateObservation(event) {
        const button = event.target;
        const obsId = button.dataset.id;
        const obsType = button.dataset.type;

        // Navigate to observation detail page
        const detailUrl = `/observations/detail/${obsType}/${obsId}/`;
        window.location.href = detailUrl;
    }

    // Scroll event listener for infinite scroll
    function handleScroll() {
        if (isLoading || !hasMore) return;

        const scrollTop =
            window.pageYOffset || document.documentElement.scrollTop;
        const windowHeight = window.innerHeight;
        const documentHeight = document.documentElement.scrollHeight;

        // Load more when user is near the bottom (within 200px)
        if (scrollTop + windowHeight >= documentHeight - 200) {
            loadMoreObservations();
        }
    }

    // Debounce function for search input
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Helper function to extract date from session slug (matches Django template filter)
    function extractDateFromSlug(slug) {
        /**
         * Extract the date part from a session slug.
         * Examples:
         * "1-2025-10-11-1" -> "2025-10-11"
         * "2-2024-12-25-3" -> "2024-12-25"
         */
        const parts = slug.split("-");
        if (parts.length >= 4) {
            // Extract the date parts (YYYY-MM-DD)
            return `${parts[1]}-${parts[2]}-${parts[3]}`;
        }
        return slug;
    }

    // Helper function to calculate relative time
    function getRelativeTime(date) {
        const now = new Date();
        const diffMs = now - date;
        const diffMinutes = diffMs / (1000 * 60);
        const diffHours = diffMs / (1000 * 60 * 60);
        const diffDays = diffMs / (1000 * 60 * 60 * 24);
        
        if (diffMinutes < 1) {
            return 'Just now';
        } else if (diffMinutes < 60) {
            return `${Math.floor(diffMinutes)}m ago`;
        } else if (diffHours < 24) {
            return `${Math.floor(diffHours)}h ago`;
        } else if (diffDays < 7) {
            return `${Math.floor(diffDays)}d ago`;
        } else {
            return date.toLocaleDateString();
        }
    }

    // Event listeners
    filterForm.addEventListener("submit", handleFilterSubmit);
    clearFiltersBtn.addEventListener("click", clearFilters);

    // Auto-submit on filter changes (with debounce for search)
    document
        .getElementById("session-filter")
        .addEventListener("change", applyFilters);
    document
        .getElementById("object-type-filter")
        .addEventListener("change", applyFilters);
    document
        .getElementById("search-filter")
        .addEventListener("input", debounce(applyFilters, 500)); // 500ms delay for search

    // Infinite scroll
    window.addEventListener("scroll", debounce(handleScroll, 100));

    // Add event listeners to existing buttons on page load
    addButtonEventListeners(document);

    // Handle browser back/forward navigation
    window.addEventListener("popstate", function () {
        // Reload the page to reflect the new URL state
        window.location.reload();
    });
});
