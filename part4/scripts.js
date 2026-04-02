// Helper to get cookie by name
function getCookie(name) {
    const cookies = document.cookie.split('; ');
    for (let cookie of cookies) {
        const [key, value] = cookie.split('=');
        if (key === name) return value;
    }
    return null;
}

// Check login/logout links
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');

    if (!token) {
        if (loginLink) loginLink.style.display = 'block';
        if (logoutLink) logoutLink.style.display = 'none';
    } else {
        if (loginLink) loginLink.style.display = 'none';
        if (logoutLink) logoutLink.style.display = 'block';
    }
}

// Logout click handler
function setupLogout() {
    const logoutLink = document.getElementById('logout-link');
    if (logoutLink) {
        logoutLink.addEventListener('click', (event) => {
            event.preventDefault();
            document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
            window.location.href = 'index.html';
        });
    }
}

// Ensure user is authenticated, otherwise redirect
function checkAuthOrRedirect() {
    const token = getCookie('token');
    if (!token) window.location.href = 'login.html';
    return token;
}

// Get place ID from URL
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

// Fetch all places for index page
async function fetchPlaces() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/places');
        const data = await response.json();

        if (response.ok) {
            displayPlaces(data);
        } else {
            console.error('Failed to fetch places:', data);
        }
    } catch (err) {
        console.error('Error fetching places:', err);
    }
}

// Display all places on index page
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    placesList.innerHTML = '';

    places.forEach(place => {
        const placeDiv = document.createElement('div');
        placeDiv.classList.add('place');
        placeDiv.dataset.price = place.price;
        placeDiv.style.cursor = 'pointer';

        placeDiv.addEventListener('click', () => {
            window.location.href = `place.html?id=${place.id}`;
        });

        placeDiv.innerHTML = `
            <h3>${place.title}</h3>
            <p><strong>Price:</strong> $${place.price}</p>
            <p>Location: (${place.latitude}, ${place.longitude})</p>
        `;

        placesList.appendChild(placeDiv);
    });
}

// Setup price filter dropdown
function setupPriceFilter() {
    const filter = document.getElementById('price-filter');
    if (!filter) return;

    const options = [10, 50, 100, 'All'];

    options.forEach(value => {
        const option = document.createElement('option');
        option.value = value;
        option.textContent = value;
        filter.appendChild(option);
    });

    filter.addEventListener('change', handleFilterChange);
}

// Filter places by selected price
function handleFilterChange(event) {
    const maxPrice = event.target.value;
    const places = document.querySelectorAll('.place');

    places.forEach(place => {
        const price = parseFloat(place.dataset.price);
        if (maxPrice === 'All' || price <= maxPrice) {
            place.style.display = 'block';
        } else {
            place.style.display = 'none';
        }
    });
}

// Fetch single place (without reviews)
async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = {};
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, { headers });
        const data = await response.json();

        if (response.ok) {
            displayPlaceDetails(data);
        } else {
            console.error('Failed to fetch place details:', data);
        }
    } catch (err) {
        console.error('Error fetching place details:', err);
    }
}

function displayPlaceDetails(place) {
    const container = document.getElementById('place-details');

    if (container) {
        container.innerHTML = `
            <div class="place-card"> <!-- KEEP CSS CLASS -->
                <h2>${place.title}</h2>
                <p><strong>Host:</strong> ${place.host || 'Unknown'}</p>
                <p><strong>Price per night:</strong> $${place.price}</p>
                <p><strong>Description:</strong> ${place.description || 'No description available'}</p>
                <p><strong>Location:</strong> (${place.latitude}, ${place.longitude})</p>
            </div>
        `;

        if (place.amenities && place.amenities.length > 0) {
            const amenitiesP = document.createElement('p');
            amenitiesP.innerHTML = `<strong>Amenities:</strong> ${place.amenities.map(a => a.name).join(', ')}`;
            container.appendChild(amenitiesP);
        }
    }

    // 🔥 IMPORTANT: DO NOT USE place.reviews ANYMORE
    // We will fetch reviews separately

    const placeId = place.id;
    fetchReviewsForPlace(placeId); // 👈 THIS is the real fix

    // Add Review button
    const addReviewLink = document.getElementById('add-review-link');
    if (addReviewLink) {
        addReviewLink.href = `add_review.html?id=${place.id}`;
    }

    // Hidden input
    const hiddenInput = document.getElementById('place_id');
    if (hiddenInput) hiddenInput.value = place.id;
}

async function fetchReviewsForPlace(placeId) {
    const reviewsContainer = document.getElementById('reviews');
    if (!reviewsContainer) return;

    reviewsContainer.innerHTML = '<h3>Reviews</h3>';

    try {
        // ✅ Use the new dedicated endpoint
        const response = await fetch(`http://127.0.0.1:5000/api/v1/reviews/place/${placeId}`);
        const data = await response.json();

        if (!response.ok) {
            console.error('Failed to fetch reviews:', data);
            const errorMsg = document.createElement('p');
            errorMsg.textContent = data.error || 'Error fetching reviews';
            reviewsContainer.appendChild(errorMsg);
            return;
        }

        if (!Array.isArray(data) || data.length === 0) {
            const noReviews = document.createElement('p');
            noReviews.textContent = 'No reviews yet.';
            reviewsContainer.appendChild(noReviews);
            return;
        }

        data.forEach(r => {
            const reviewDiv = document.createElement('div');
            reviewDiv.classList.add('review-card'); // keep your CSS

            // Use author_name field from API; fallback to 'Anonymous'
            const authorName = r.author_name || 'Anonymous';
            const reviewText = r.text || '[No text]';
            const rating = Number(r.rating) || 0;
            const stars = '★'.repeat(rating) + '☆'.repeat(5 - rating);

            reviewDiv.innerHTML = `
                <h4>${authorName}</h4>
                <p>${reviewText}</p>
                <p><strong>Rating:</strong> ${stars}</p>
            `;

            reviewsContainer.appendChild(reviewDiv);
        });

    } catch (err) {
        console.error('Error fetching reviews:', err);
        const errorMsg = document.createElement('p');
        errorMsg.textContent = 'Error fetching reviews';
        reviewsContainer.appendChild(errorMsg);
    }
}

// Check authentication and show/hide Add Review form
function checkAuthenticationForPlacePage() {
    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review');
    const placeId = getPlaceIdFromURL();

    if (!placeId) {
        console.error('No place ID in URL');
        return;
    }

    if (!token) {
        if (addReviewSection) addReviewSection.style.display = 'none';
        fetchPlaceDetails(null, placeId);
    } else {
        if (addReviewSection) addReviewSection.style.display = 'block';
        fetchPlaceDetails(token, placeId);
    }
}

// Submit review to backend
async function submitReview(token, placeId, reviewText, rating) {
    if (!placeId) {
        console.error('Cannot submit review: placeId missing');
        alert('Error: Place not found.');
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/reviews/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                text: reviewText,
                rating: parseInt(rating),
                place_id: placeId
            })
        });

        const data = await response.json();

        if (response.ok) {
            alert('Review submitted successfully!');
            fetchReviewsForPlace(placeId);
        } else {
            alert('Failed: ' + (data.error || response.statusText));
        }
    } catch (err) {
        console.error('Error submitting review:', err);
        alert('Something went wrong.');
    }
}

// Handle login form submission
function setupLoginForm() {
    const loginForm = document.getElementById('login-form');
    if (!loginForm) return;

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;

        if (!email || !password) {
            alert('Please enter both email and password.');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                const expires = new Date();
                expires.setTime(expires.getTime() + 24 * 60 * 60 * 1000);
                document.cookie = `token=${data.access_token}; path=/; expires=${expires.toUTCString()}`;

                window.location.href = 'index.html';
            } else {
                alert('Login failed: ' + (data.error || response.statusText));
            }
        } catch (err) {
            console.error('Error during login:', err);
            alert('An unexpected error occurred. Please try again later.');
        }
    });
}

// Initialize everything after DOM loaded
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('places-list')) fetchPlaces();
    if (document.getElementById('price-filter')) setupPriceFilter();

    checkAuthentication();
    setupLogout();
    setupLoginForm();

    if (document.getElementById('place-details')) checkAuthenticationForPlacePage();

    // Review form submission
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        const token = checkAuthOrRedirect();
        const placeIdInput = document.getElementById('place_id');

        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const placeId = placeIdInput ? placeIdInput.value : getPlaceIdFromURL();
            const reviewText = document.getElementById('review-text').value.trim();
            const rating = document.getElementById('rating').value;

            if (!reviewText) { alert('Review cannot be empty'); return; }
            if (!rating || isNaN(rating) || rating < 1 || rating > 5) { alert('Rating must be 1-5'); return; }

            await submitReview(token, placeId, reviewText, rating);
        });
    }
});
