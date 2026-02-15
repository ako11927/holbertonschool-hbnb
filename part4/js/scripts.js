// ================== CONFIGURATION ==================
// Change this to your actual Flask API URL (e.g., http://127.0.0.1:5000/api/v1)
const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

// ================== UTILITY FUNCTIONS ==================
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function setCookie(name, value, days = 7) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = `${name}=${value}; expires=${date.toUTCString()}; path=/`;
}

function deleteCookie(name) {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/`;
}

function isAuthenticated() {
    return getCookie('token') !== null;
}

function updateAuthUI() {
    const loginLink = document.getElementById('login-link');
    if (!loginLink) return;
    loginLink.style.display = isAuthenticated() ? 'none' : 'inline';
}

// ================== API CALLS ==================
async function loginUser(email, password) {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include', // Important for cookies
        body: JSON.stringify({ email, password })
    });
    if (response.ok) {
        const data = await response.json();
        setCookie('token', data.access_token);
        window.location.href = 'index.html';
    } else {
        const error = await response.json();
        throw new Error(error.message || 'Login failed');
    }
}

async function fetchPlaces() {
    const token = getCookie('token');
    const headers = {};
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    const response = await fetch(`${API_BASE_URL}/places`, {
        headers,
        credentials: 'include'
    });
    if (!response.ok) throw new Error('Failed to fetch places');
    return await response.json();
}

async function fetchPlaceById(placeId) {
    const token = getCookie('token');
    const headers = {};
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    const response = await fetch(`${API_BASE_URL}/places/${placeId}`, {
        headers,
        credentials: 'include'
    });
    if (!response.ok) throw new Error('Failed to fetch place details');
    return await response.json();
}

async function submitReview(placeId, reviewText, rating) {
    const token = getCookie('token');
    if (!token) throw new Error('Not authenticated');
    const response = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        credentials: 'include',
        body: JSON.stringify({ text: reviewText, rating: parseInt(rating) })
    });
    if (!response.ok) throw new Error('Failed to submit review');
    return await response.json();
}

// ================== PAGE FUNCTIONS ==================
// Index page (index.html)
async function initIndexPage() {
    updateAuthUI();
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    try {
        const places = await fetchPlaces();
        displayPlaces(places);
        setupPriceFilter(places);
    } catch (error) {
        placesList.innerHTML = `<p class="error">Error loading places: ${error.message}</p>`;
    }
}

function displayPlaces(places) {
    const container = document.getElementById('places-list');
    container.innerHTML = '';
    places.forEach(place => {
        const card = document.createElement('article');
        card.className = 'place-card';
        card.dataset.price = place.price_per_night;
        card.innerHTML = `
            <h3>${place.name || 'Unnamed'}</h3>
            <p>${place.description || ''}</p>
            <p><strong>Price per night:</strong> $${place.price_per_night}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        container.appendChild(card);
    });
}

function setupPriceFilter(places) {
    const filter = document.getElementById('price-filter');
    if (!filter) return;
    filter.addEventListener('change', () => {
        const maxPrice = filter.value;
        const cards = document.querySelectorAll('.place-card');
        cards.forEach(card => {
            const price = parseInt(card.dataset.price);
            if (maxPrice === 'all' || price <= parseInt(maxPrice)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
}

// Login page (login.html)
async function initLoginPage() {
    const form = document.getElementById('login-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const errorDiv = document.getElementById('error-message');

        try {
            await loginUser(email, password);
        } catch (error) {
            errorDiv.textContent = error.message;
        }
    });
}

// Place details page (place.html)
async function initPlacePage() {
    updateAuthUI();
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');
    if (!placeId) {
        window.location.href = 'index.html';
        return;
    }

    try {
        const place = await fetchPlaceById(placeId);
        displayPlaceDetails(place);
        displayReviews(place.reviews || []);
        setupAddReviewButton(placeId);
    } catch (error) {
        document.getElementById('place-details').innerHTML = `<p class="error">Error: ${error.message}</p>`;
    }
}

function displayPlaceDetails(place) {
    const container = document.getElementById('place-details');
    container.innerHTML = `
        <div class="place-details">
            <h2>${place.name}</h2>
            <div class="place-info">
                <p><strong>Host:</strong> ${place.owner?.name || 'Unknown'}</p>
                <p><strong>Price per night:</strong> $${place.price_per_night}</p>
                <p><strong>Description:</strong> ${place.description || ''}</p>
                <p><strong>Amenities:</strong> ${place.amenities ? place.amenities.map(a => a.name).join(', ') : 'None'}</p>
            </div>
        </div>
    `;
}

function displayReviews(reviews) {
    const container = document.getElementById('reviews-list');
    if (!container) return;
    container.innerHTML = '<h3>Reviews</h3>';
    if (reviews.length === 0) {
        container.innerHTML += '<p>No reviews yet.</p>';
        return;
    }
    reviews.forEach(review => {
        const card = document.createElement('div');
        card.className = 'review-card';
        card.innerHTML = `
            <p><strong>${review.user?.name || 'Anonymous'}</strong> (Rating: ${review.rating}/5)</p>
            <p>${review.text}</p>
        `;
        container.appendChild(card);
    });
}

function setupAddReviewButton(placeId) {
    const container = document.getElementById('add-review-container');
    if (!container) return;
    if (isAuthenticated()) {
        container.innerHTML = `<a href="add_review.html?place_id=${placeId}" class="details-button">Add a Review</a>`;
    } else {
        container.innerHTML = '';
    }
}

// Add review page (add_review.html)
async function initAddReviewPage() {
    // Redirect if not authenticated
    if (!isAuthenticated()) {
        window.location.href = 'index.html';
        return;
    }
    updateAuthUI();

    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('place_id');
    if (!placeId) {
        window.location.href = 'index.html';
        return;
    }

    const form = document.getElementById('review-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const text = document.getElementById('review-text').value;
        const rating = document.getElementById('rating').value;
        const errorDiv = document.getElementById('error-message');

        try {
            await submitReview(placeId, text, rating);
            window.location.href = `place.html?id=${placeId}`;
        } catch (error) {
            errorDiv.textContent = error.message;
        }
    });
}

// ================== INITIALIZATION ==================
document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    if (path.endsWith('index.html') || path === '/' || path.endsWith('/')) {
        initIndexPage();
    } else if (path.endsWith('login.html')) {
        initLoginPage();
    } else if (path.endsWith('place.html')) {
        initPlacePage();
    } else if (path.endsWith('add_review.html')) {
        initAddReviewPage();
    }
});
