document.addEventListener('DOMContentLoaded', () => {

    const token = getCookie('token'); // Shared for all pages

    // -------------------------
    // Login page
    // -------------------------
    const loginForm = document.getElementById('login-form');
    if (loginForm) setupLoginForm();

    // -------------------------
    // Index page
    // -------------------------
    const placesList = document.getElementById('places-list');
    const loginLink = document.getElementById('login-link');
    if (loginLink) loginLink.style.display = token ? 'none' : 'block';
    if (placesList) fetchPlaces(token);

    // -------------------------
    // Place Details page
    // -------------------------
    const placeDetailsSection = document.getElementById('place-details');
    if (placeDetailsSection) {
        const placeId = getPlaceIdFromURL();
        const addReviewSection = document.getElementById('add-review');
        if (addReviewSection) addReviewSection.style.display = token ? 'block' : 'none';
        fetchPlaceDetails(token, placeId);
    }

    // -------------------------
    // Add Review page
    // -------------------------
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) setupAddReviewForm(token);

    // -------------------------
    // Shared Functions
    // -------------------------
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    function getPlaceIdFromURL() {
        return new URLSearchParams(window.location.search).get('id');
    }

    // Index functions: fetch places, display, filter
    async function fetchPlaces(token) { /* ... code كما سبق ... */ }
    function displayPlaces(places) { /* ... code كما سبق ... */ }
    function setupFilter(places) { /* ... code كما سبق ... */ }

    // Place Details functions
    async function fetchPlaceDetails(token, placeId) { /* ... code كما سبق ... */ }
    function displayPlaceDetails(place) { /* ... code كما سبق ... */ }

    // Login form handler
    function setupLoginForm() { /* ... code login كما سبق ... */ }

    // Add Review form handler
    function setupAddReviewForm(token) { /* ... code add review كما سبق ... */ }

});
