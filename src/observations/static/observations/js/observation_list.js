/**
 * Observation List Page JavaScript
 * 
 * Manages the interactive functionality for the observations list page including:
 * - Infinite scroll pagination for large datasets
 * - Real-time filtering by session, object type, and search terms
 * - AJAX-based observation deletion with confirmation
 * - Dynamic URL updates for bookmarkable filter states
 * - Responsive UI updates and loading indicators
 * 
 * The page provides a comprehensive view of all user observations with advanced
 * filtering capabilities and seamless infinite scroll for optimal performance.
 * 
 * @author Lodestar Project
 * @version 1.0.0
 */

document.addEventListener("DOMContentLoaded", function () {
    // Pagination and loading state management
    let currentPage = 1; // Track current page for infinite scroll
    let isLoading = false; // Prevent multiple concurrent requests
    let hasMore = true; // Track if more observations are available
    
    // Cache DOM elements for performance
    const observationsContainer = document.getElementById("observations-container");
    const loadingIndicator = document.getElementById("loading-indicator");
    const filterForm = document.getElementById("filter-form");
    const clearFiltersBtn = document.getElementById("clear-filters");

    // Extract current filters from URL parameters for bookmarkable state
    const urlParams = new URLSearchParams(window.location.search);
    const initialFilters = {
        session: urlParams.get("session") || "",
        object_type: urlParams.get("object_type") || "",
        search: urlParams.get("search") || "",
    };

    // Initialize filter form with URL parameters
    document.getElementById("session-filter").value = initialFilters.session;
    document.getElementById("object-type-filter").value = initialFilters.object_type;
    document.getElementById("search-filter").value = initialFilters.search;

    // Update pagination state based on server-side data attribute
    hasMore = document.querySelector("[data-has-next]")
        ? document.querySelector("[data-has-next]").dataset.hasNext === "True"
        : false;

    /**
     * Load more observations via AJAX for infinite scroll
     * Fetches next page of results and appends to existing list
     */
    function loadMoreObservations() {
        // Prevent loading if already in progress or no more data available
        if (isLoading || !hasMore) return;

        isLoading = true;
        loadingIndicator.classList.remove("hidden");

        const nextPage = currentPage + 1;
        const currentFilters = getCurrentFilters();

        // Build URL with current filters and next page number
        const params = new URLSearchParams(currentFilters);
        params.set("page", nextPage);

        // Fetch next page of observations
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
    /**
     * Append new observation data to the DOM container
     * Converts observation objects into HTML elements and adds them to the list
     * @param {Array} observations - Array of observation objects from AJAX response
     */
    function appendObservations(observations) {
        observations.forEach((obs) => {
            const observationRow = createObservationRow(obs);
            observationsContainer.appendChild(observationRow);
        });
    }

    /**
     * Create HTML element for a single observation row
     * Generates complete observation card with session info, object details, and action buttons
     * @param {Object} obs - Observation object containing all observation data
     * @param {string} obs.id - Unique observation identifier
     * @param {string} obs.object_type - Type of astronomical object observed
     * @param {string} obs.object_name - Name of the observed object
     * @param {string} obs.session_slug - Session identifier with date information
     * @param {string} obs.created_at - ISO timestamp of observation creation
     * @param {string} obs.date_time - Observation session date/time
     * @param {string} obs.type_class - CSS class for observation type styling
     * @returns {HTMLElement} Complete observation row element ready for insertion
     */
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
                <button class="view-update-btn bg-accent text-white hover:text-black px-4 py-1 rounded-md hover:bg-blue-700 transition-colors text-sm"
                        data-id="${obs.id}" data-type="${obs.type_class}" data-created-at="${obs.created_at}">
                    View/Update
                </button>
            </div>
        `;

        // Add event listeners to the new buttons
        addButtonEventListeners(row);

        return row;
    }

    /**
     * Extract current filter values from form inputs
     * Used for building filter parameters for AJAX requests and URL updates
     * @returns {Object} Object containing current filter values
     * @property {string} session - Selected session filter value
     * @property {string} object_type - Selected object type filter value  
     * @property {string} search - Current search term filter value
     */
    function getCurrentFilters() {
        return {
            session: document.getElementById("session-filter").value,
            object_type: document.getElementById("object-type-filter").value,
            search: document.getElementById("search-filter").value,
        };
    }

    /**
     * Handle form submission for filter application
     * Prevents default form submission and applies filters via AJAX
     * @param {Event} event - Form submit event object
     */
    function handleFilterSubmit(event) {
        event.preventDefault();
        applyFilters();
    }

    /**
     * Apply current filters and reload the page with filtered results
     * Updates URL parameters to maintain bookmarkable filter state
     * Redirects to new URL with filter parameters included
     */
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

    /**
     * Clear all active filters and reload page
     * Resets all filter form inputs and redirects to unfiltered view
     */
    function clearFilters() {
        document.getElementById("session-filter").value = "";
        document.getElementById("object-type-filter").value = "";
        document.getElementById("search-filter").value = "";

        // Reload page without filters
        window.location.href = window.location.pathname;
    }

    /**
     * Display temporary notification message to user
     * Creates floating notification that auto-dismisses after 5 seconds
     * @param {string} message - Message text to display
     * @param {string} type - Message type ('success' or 'error') for styling
     */
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

    /**
     * Show error notification message
     * Convenience wrapper for showMessage with error styling
     * @param {string} message - Error message to display
     */
    function showErrorMessage(message) {
        showMessage(message, "error");
    }

    /**
     * Show success notification message  
     * Convenience wrapper for showMessage with success styling
     * @param {string} message - Success message to display
     */
    function showSuccessMessage(message) {
        showMessage(message, "success");
    }

    /**
     * Attach event listeners to observation action buttons
     * Adds click handlers for delete and view/update buttons in container
     * @param {HTMLElement} container - DOM container holding buttons to bind
     */
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

    /**
     * Handle observation deletion with confirmation and AJAX request
     * Shows confirmation dialog, makes AJAX delete request, and updates UI
     * @param {Event} event - Click event from delete button
     */
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

    /**
     * Update observation count and UI after successful deletion
     * Updates count display, handles pluralization, and shows empty state if needed
     */
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

    /**
     * Handle navigation to observation detail/update page
     * Redirects user to observation detail page for viewing and editing
     * @param {Event} event - Click event from view/update button
     */
    function handleViewUpdateObservation(event) {
        const button = event.target;
        const obsId = button.dataset.id;
        const obsType = button.dataset.type;

        // Navigate to observation detail page
        const detailUrl = `/observations/detail/${obsType}/${obsId}/`;
        window.location.href = detailUrl;
    }

    /**
     * Scroll event handler for infinite scroll functionality
     * Triggers loading of more observations when user approaches bottom of page
     */
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

    /**
     * Debounce utility function to limit function execution frequency
     * Prevents excessive API calls during rapid user input (e.g., typing in search)
     * @param {Function} func - Function to debounce
     * @param {number} wait - Milliseconds to wait before execution
     * @returns {Function} Debounced function
     */
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

    /**
     * Extract date portion from Django session slug format
     * Parses session slug to extract the date components for display
     * @param {string} slug - Session slug in format "id-YYYY-MM-DD-sequence"  
     * @returns {string} Extracted date in YYYY-MM-DD format
     * @example
     * extractDateFromSlug("1-2025-10-11-1") returns "2025-10-11"
     * extractDateFromSlug("2-2024-12-25-3") returns "2024-12-25"
     */
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

    /**
     * Calculate human-readable relative time from a date
     * Converts timestamp to user-friendly relative time display
     * @param {Date} date - Date object to calculate relative time from
     * @returns {string} Human-readable relative time string
     * @example
     * getRelativeTime(new Date(Date.now() - 60000)) returns "1m ago"
     * getRelativeTime(new Date(Date.now() - 3600000)) returns "1h ago"
     */
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
