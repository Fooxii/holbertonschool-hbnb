function getCookie(name) {
    const cookies = document.cookie.split('; ');
    for (let cookie of cookies) {
        const [key, value] = cookie.split('=');
        if (key === name) return value;
    }
    return null;
}

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

        fetchPlaces();
    }
}

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

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');

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

function setupPriceFilter() {
    const filter = document.getElementById('price-filter');

    const options = [10, 50, 100, 'All'];

    options.forEach(value => {
        const option = document.createElement('option');
        option.value = value;
        option.textContent = value;
        filter.appendChild(option);
    });

    filter.addEventListener('change', handleFilterChange);
}

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

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

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

async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = {};

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
            method: 'GET',
            headers
        });

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

    if (!container) return;

    container.innerHTML = '';

    const div = document.createElement('div');

    div.innerHTML = `
        <h2>${place.title}</h2>
        <p><strong>Price:</strong> $${place.price}</p>
        <p><strong>Description:</strong> ${place.description || 'No description available'}</p>
        <p><strong>Location:</strong> (${place.latitude}, ${place.longitude})</p>
    `;

    container.appendChild(div);

    if (place.amenities && place.amenities.length > 0) {
        const amenitiesList = document.createElement('ul');
        amenitiesList.innerHTML = '<h3>Amenities:</h3>';

        place.amenities.forEach(a => {
            const li = document.createElement('li');
            li.textContent = a.name;
            amenitiesList.appendChild(li);
        });

        container.appendChild(amenitiesList);
    }

    if (place.reviews && place.reviews.length > 0) {
        const reviewsList = document.createElement('ul');
        reviewsList.innerHTML = '<h3>Reviews:</h3>';

        place.reviews.forEach(r => {
            const li = document.createElement('li');
            li.textContent = `${r.text} (Rating: ${r.rating})`;
            reviewsList.appendChild(li);
        });

        container.appendChild(reviewsList);
    }
}

function checkAuthOrRedirect() {
    const token = getCookie('token');

    if (!token) {
        window.location.href = 'index.html';
    }

    return token;
}

async function submitReview(token, placeId, reviewText, rating) {
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
            return true;
        } else {
            alert('Failed: ' + (data.error || response.statusText));
            return false;
        }
    } catch (err) {
        console.error('Error submitting review:', err);
        alert('Something went wrong.');
        return false;
      }
}
    
document.addEventListener('DOMContentLoaded', () => {

    if (document.getElementById('price-filter')) {
        setupPriceFilter();
    }

    checkAuthentication();

    if (document.getElementById('place-details')) {
        checkAuthenticationForPlacePage();
    }

    const logoutLink = document.getElementById('logout-link');

    if (logoutLink) {
        logoutLink.addEventListener('click', (event) => {
            event.preventDefault();
            document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
            window.location.href = 'index.html';
        });
    }

    const reviewForm = document.getElementById('review-form');

    if (reviewForm) {
        const token = checkAuthOrRedirect();
        const placeId = getPlaceIdFromURL();

        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const reviewText = document.getElementById('review').value.trim();
            const rating = document.getElementById('rating').value;

            if (!reviewText) {
                alert('Review cannot be empty');
                return;
            }

            const success = await submitReview(token, placeId, reviewText, rating);

            if (success) {
                window.location.href = `place.html?id=${placeId}`;
            }
        });
    }

    const loginForm = document.getElementById('login-form');

    if (loginForm) {
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
});
