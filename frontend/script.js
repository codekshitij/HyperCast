// ===================================
// Configuration & Constants
// ===================================
const API_BASE_URL = 'http://localhost:8000'; // Backend API endpoint
const WEATHER_ICONS = {
    sunny: `<svg width="120" height="120" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <circle cx="12" cy="12" r="5"></circle>
        <line x1="12" y1="1" x2="12" y2="3"></line>
        <line x1="12" y1="21" x2="12" y2="23"></line>
        <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
        <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
        <line x1="1" y1="12" x2="3" y2="12"></line>
        <line x1="21" y1="12" x2="23" y2="12"></line>
        <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
        <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
    </svg>`,
    cloudy: `<svg width="120" height="120" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"></path>
    </svg>`,
    rainy: `<svg width="120" height="120" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <line x1="8" y1="19" x2="8" y2="21"></line>
        <line x1="8" y1="13" x2="8" y2="15"></line>
        <line x1="16" y1="19" x2="16" y2="21"></line>
        <line x1="16" y1="13" x2="16" y2="15"></line>
        <line x1="12" y1="21" x2="12" y2="23"></line>
        <line x1="12" y1="15" x2="12" y2="17"></line>
        <path d="M20 16.58A5 5 0 0 0 18 7h-1.26A8 8 0 1 0 4 15.25"></path>
    </svg>`,
    snowy: `<svg width="120" height="120" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <path d="M20 17.58A5 5 0 0 0 18 8h-1.26A8 8 0 1 0 4 16.25"></path>
        <line x1="8" y1="16" x2="8.01" y2="16"></line>
        <line x1="8" y1="20" x2="8.01" y2="20"></line>
        <line x1="12" y1="18" x2="12.01" y2="18"></line>
        <line x1="12" y1="22" x2="12.01" y2="22"></line>
        <line x1="16" y1="16" x2="16.01" y2="16"></line>
        <line x1="16" y1="20" x2="16.01" y2="20"></line>
    </svg>`,
};

// ===================================
// DOM Elements
// ===================================
const elements = {
    searchInput: document.getElementById('searchInput'),
    searchBtn: document.getElementById('searchBtn'),
    suggestions: document.getElementById('suggestions'),
    weatherSection: document.getElementById('weatherSection'),
    loadingState: document.getElementById('loadingState'),
    weatherCard: document.getElementById('weatherCard'),
    errorState: document.getElementById('errorState'),
    errorMessage: document.getElementById('errorMessage'),
    retryBtn: document.getElementById('retryBtn'),
    aboutBtn: document.getElementById('aboutBtn'),
    settingsBtn: document.getElementById('settingsBtn'),
    themeToggle: document.getElementById('themeToggle'),
    aboutModal: document.getElementById('aboutModal'),
    closeAbout: document.getElementById('closeAbout'),
    favoriteBtn: document.getElementById('favoriteBtn'),
    locationName: document.getElementById('locationName'),
    locationCoords: document.getElementById('locationCoords'),
    temperature: document.getElementById('temperature'),
    weatherIcon: document.getElementById('weatherIcon'),
    weatherCondition: document.getElementById('weatherCondition'),
    weatherDetail: document.getElementById('weatherDetail'),
    humidity: document.getElementById('humidity'),
    windSpeed: document.getElementById('windSpeed'),
    feelsLike: document.getElementById('feelsLike'),
    visibility: document.getElementById('visibility'),
    forecastGrid: document.getElementById('forecastGrid'),
    connectionStatus: document.getElementById('connectionStatus'),
};

// ===================================
// State Management
// ===================================
const state = {
    currentLocation: null,
    favorites: JSON.parse(localStorage.getItem('favorites')) || [],
    units: localStorage.getItem('units') || 'imperial', // 'imperial' or 'metric'
    theme: localStorage.getItem('theme') || 'light', // 'light' or 'dark'
};

// ===================================
// Utility Functions
// ===================================

/**
 * Show loading state
 */
function showLoading() {
    elements.loadingState.classList.add('active');
    elements.weatherCard.classList.remove('active');
    elements.errorState.classList.remove('active');
}

/**
 * Show weather card
 */
function showWeather() {
    elements.loadingState.classList.remove('active');
    elements.weatherCard.classList.add('active');
    elements.errorState.classList.remove('active');
}

/**
 * Show error state
 */
function showError(message = 'Unable to fetch weather data. Please try again.') {
    elements.loadingState.classList.remove('active');
    elements.weatherCard.classList.remove('active');
    elements.errorState.classList.add('active');
    elements.errorMessage.textContent = message;
}

/**
 * Debounce function for search input
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
 * Format temperature based on units
 */
function formatTemp(temp) {
    return state.units === 'imperial' ? `${Math.round(temp)}°F` : `${Math.round((temp - 32) * 5/9)}°C`;
}

/**
 * Get weather icon based on condition
 */
function getWeatherIcon(condition) {
    condition = condition.toLowerCase();
    if (condition.includes('sun') || condition.includes('clear')) {
        return WEATHER_ICONS.sunny;
    } else if (condition.includes('cloud') || condition.includes('overcast')) {
        return WEATHER_ICONS.cloudy;
    } else if (condition.includes('rain') || condition.includes('drizzle')) {
        return WEATHER_ICONS.rainy;
    } else if (condition.includes('snow') || condition.includes('sleet')) {
        return WEATHER_ICONS.snowy;
    }
    return WEATHER_ICONS.cloudy;
}

/**
 * Get day name from date
 */
function getDayName(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { weekday: 'short' });
}

/**
 * Initialize theme from localStorage
 */
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    state.theme = savedTheme;
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon();
}

/**
 * Toggle theme between light and dark
 */
function toggleTheme() {
    const newTheme = state.theme === 'light' ? 'dark' : 'light';
    state.theme = newTheme;
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon();
    
    // Show notification
    showNotification(`${newTheme === 'dark' ? 'Dark' : 'Light'} mode activated`, 'success');
}

/**
 * Update theme toggle icon
 */
function updateThemeIcon() {
    const slider = elements.themeToggle.querySelector('.theme-toggle-slider svg');
    
    if (state.theme === 'dark') {
        // Moon icon for dark mode
        slider.innerHTML = `
            <circle cx="12" cy="12" r="4"></circle>
            <path d="M12 2v2m0 16v2M4.22 4.22l1.42 1.42m12.72 12.72l1.42 1.42M2 12h2m16 0h2M4.22 19.78l1.42-1.42m12.72-12.72l1.42-1.42" opacity="0.3"></path>
        `;
    } else {
        // Sun icon for light mode
        slider.innerHTML = `
            <circle cx="12" cy="12" r="5"></circle>
            <line x1="12" y1="1" x2="12" y2="3"></line>
            <line x1="12" y1="21" x2="12" y2="23"></line>
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
            <line x1="1" y1="12" x2="3" y2="12"></line>
            <line x1="21" y1="12" x2="23" y2="12"></line>
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
        `;
    }
}

/**
 * Update connection status indicator
 */
function updateConnectionStatus(isOnline) {
    const statusText = elements.connectionStatus.querySelector('.connection-status-text');
    
    if (isOnline) {
        elements.connectionStatus.classList.remove('offline');
        statusText.textContent = 'Online';
    } else {
        elements.connectionStatus.classList.add('offline');
        statusText.textContent = 'Offline';
    }
    
    // Show indicator
    elements.connectionStatus.classList.add('show');
    
    // Hide after 3 seconds if online
    if (isOnline) {
        setTimeout(() => {
            elements.connectionStatus.classList.remove('show');
        }, 3000);
    }
}

// ===================================
// API Functions
// ===================================

/**
 * Fetch weather data from API
 * NOTE: This is a placeholder. Replace with actual API call when backend is ready.
 */
async function fetchWeather(location) {
    try {
        // For MVP, default to Atlanta coordinates
        const lat = 33.749;
        const lon = -84.388;
        
        // Call our LSTM-based forecast API
        const response = await fetch(`${API_BASE_URL}/forecast?lat=${lat}&lon=${lon}&hours=24`);
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Check for errors in response
        if (data.error) {
            throw new Error(data.message || 'Forecast unavailable');
        }
        
        // Transform API response to match frontend format
        const transformedData = {
            location: {
                name: data.location.name,
                state: 'GA',
                coordinates: { lat: data.location.lat, lon: data.location.lon }
            },
            current: {
                temperature: Math.round(data.current.temperature),
                feelsLike: Math.round(data.current.temperature - 2), // Simple approximation
                condition: data.current.temperature > 70 ? 'Sunny' : data.current.temperature > 50 ? 'Partly Cloudy' : 'Cool',
                description: `LSTM prediction - ${data.note}`,
                humidity: Math.round(data.current.humidity),
                windSpeed: 8, // Not available in current data
                visibility: 10, // Not available in current data
            },
            forecast: [
                { 
                    day: 'Forecast', 
                    icon: data.forecast.temperature > 70 ? '☀️' : data.forecast.temperature > 50 ? '⛅' : '🌤️', 
                    high: Math.round(data.forecast.temperature + 5), 
                    low: Math.round(data.forecast.temperature - 5) 
                },
                { day: 'Mon', icon: '⛅', high: 73, low: 61 },
                { day: 'Tue', icon: '🌤️', high: 70, low: 59 },
                { day: 'Wed', icon: '🌧️', high: 65, low: 56 },
                { day: 'Thu', icon: '⛈️', high: 63, low: 55 },
                { day: 'Fri', icon: '🌤️', high: 68, low: 58 },
                { day: 'Sat', icon: '☀️', high: 72, low: 60 },
            ]
        };
        
        return transformedData;
    } catch (error) {
        console.error('Error fetching weather:', error);
        throw error;
    }
}

/**
 * Fetch location suggestions
 * NOTE: This is a placeholder for semantic search API
 */
async function fetchSuggestions(query) {
    try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 300));
        
        // Mock suggestions
        const mockSuggestions = [
            { name: 'San Francisco, CA', coords: '37.7749°N, 122.4194°W' },
            { name: 'San Diego, CA', coords: '32.7157°N, 117.1611°W' },
            { name: 'Santa Monica, CA', coords: '34.0195°N, 118.4912°W' },
        ];
        
        return mockSuggestions.filter(s => 
            s.name.toLowerCase().includes(query.toLowerCase())
        );
    } catch (error) {
        console.error('Error fetching suggestions:', error);
        return [];
    }
}

// ===================================
// UI Update Functions
// ===================================

/**
 * Update weather display with fetched data
 */
function updateWeatherDisplay(data) {
    // Update location info
    elements.locationName.textContent = `${data.location.name}, ${data.location.state}`;
    elements.locationCoords.textContent = `${data.location.coordinates.lat.toFixed(4)}°N, ${Math.abs(data.location.coordinates.lon).toFixed(4)}°W`;
    
    // Update temperature
    elements.temperature.textContent = Math.round(data.current.temperature);
    
    // Update weather icon and condition
    elements.weatherIcon.innerHTML = getWeatherIcon(data.current.condition);
    elements.weatherCondition.textContent = data.current.condition;
    elements.weatherDetail.textContent = data.current.description;
    
    // Update weather details
    elements.humidity.textContent = `${data.current.humidity}%`;
    elements.windSpeed.textContent = `${data.current.windSpeed} mph`;
    elements.feelsLike.textContent = `${Math.round(data.current.feelsLike)}°F`;
    elements.visibility.textContent = `${data.current.visibility} mi`;
    
    // Update forecast
    updateForecast(data.forecast);
    
    // Update favorite button state
    updateFavoriteButton(data.location.name);
    
    // Show weather card
    showWeather();
}

/**
 * Update forecast grid
 */
function updateForecast(forecast) {
    elements.forecastGrid.innerHTML = forecast.map(day => `
        <div class="forecast-item">
            <div class="forecast-day">${day.day}</div>
            <div class="forecast-icon">${day.icon}</div>
            <div class="forecast-temp">
                ${day.high}°
                <span class="forecast-temp-low">${day.low}°</span>
            </div>
        </div>
    `).join('');
}

/**
 * Display search suggestions
 */
function displaySuggestions(suggestions) {
    if (suggestions.length === 0) {
        elements.suggestions.classList.remove('active');
        return;
    }
    
    elements.suggestions.innerHTML = suggestions.map(s => `
        <div class="suggestion-item" data-location="${s.name}">
            <strong>${s.name}</strong><br>
            <small>${s.coords}</small>
        </div>
    `).join('');
    
    elements.suggestions.classList.add('active');
    
    // Add click handlers to suggestions
    document.querySelectorAll('.suggestion-item').forEach(item => {
        item.addEventListener('click', () => {
            elements.searchInput.value = item.dataset.location;
            elements.suggestions.classList.remove('active');
            handleSearch();
        });
    });
}

/**
 * Update favorite button state
 */
function updateFavoriteButton(locationName) {
    const isFavorite = state.favorites.includes(locationName);
    if (isFavorite) {
        elements.favoriteBtn.classList.add('active');
    } else {
        elements.favoriteBtn.classList.remove('active');
    }
}

// ===================================
// Event Handlers
// ===================================

/**
 * Handle search action
 */
async function handleSearch() {
    const query = elements.searchInput.value.trim();
    
    if (!query) {
        showError('Please enter a location to search');
        return;
    }
    
    showLoading();
    
    try {
        const data = await fetchWeather(query);
        state.currentLocation = data.location.name;
        updateWeatherDisplay(data);
    } catch (error) {
        showError('Unable to fetch weather data. Please try again.');
    }
}

/**
 * Handle search input changes
 */
const handleSearchInput = debounce(async (e) => {
    const query = e.target.value.trim();
    
    if (query.length < 2) {
        elements.suggestions.classList.remove('active');
        return;
    }
    
    try {
        const suggestions = await fetchSuggestions(query);
        displaySuggestions(suggestions);
    } catch (error) {
        console.error('Error fetching suggestions:', error);
    }
}, 300);

/**
 * Handle favorite toggle
 */
function handleFavoriteToggle() {
    if (!state.currentLocation) return;
    
    const index = state.favorites.indexOf(state.currentLocation);
    
    if (index > -1) {
        // Remove from favorites
        state.favorites.splice(index, 1);
        elements.favoriteBtn.classList.remove('active');
    } else {
        // Add to favorites
        state.favorites.push(state.currentLocation);
        elements.favoriteBtn.classList.add('active');
    }
    
    // Save to localStorage
    localStorage.setItem('favorites', JSON.stringify(state.favorites));
    
    // Show feedback
    showNotification(
        index > -1 ? 'Removed from favorites' : 'Added to favorites',
        'success'
    );
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        padding: 1rem 1.5rem;
        background: white;
        border-radius: 1rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        z-index: 1000;
        animation: slideInRight 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

/**
 * Handle modal open/close
 */
function openModal(modal) {
    modal.classList.add('active');
}

function closeModal(modal) {
    modal.classList.remove('active');
}

// ===================================
// Event Listeners
// ===================================

// Search functionality
elements.searchBtn.addEventListener('click', handleSearch);
elements.searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleSearch();
    }
});
elements.searchInput.addEventListener('input', handleSearchInput);

// Click outside suggestions to close
document.addEventListener('click', (e) => {
    if (!elements.searchInput.contains(e.target) && !elements.suggestions.contains(e.target)) {
        elements.suggestions.classList.remove('active');
    }
});

// Favorite button
elements.favoriteBtn.addEventListener('click', handleFavoriteToggle);

// Retry button
elements.retryBtn.addEventListener('click', handleSearch);

// Modal controls
elements.aboutBtn.addEventListener('click', () => openModal(elements.aboutModal));
elements.closeAbout.addEventListener('click', () => closeModal(elements.aboutModal));
elements.aboutModal.addEventListener('click', (e) => {
    if (e.target === elements.aboutModal) {
        closeModal(elements.aboutModal);
    }
});

// Settings button (placeholder for future functionality)
elements.settingsBtn.addEventListener('click', () => {
    showNotification('Settings coming soon!', 'info');
});

// Theme toggle
elements.themeToggle.addEventListener('click', toggleTheme);
elements.themeToggle.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        toggleTheme();
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // ESC to close modal
    if (e.key === 'Escape') {
        closeModal(elements.aboutModal);
    }
    
    // Ctrl/Cmd + K to focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        elements.searchInput.focus();
    }
});

// ===================================
// Service Worker Registration
// ===================================
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker
            .register('./sw.js')
            .then(registration => {
                console.log('Service Worker registered successfully:', registration.scope);
                
                // Listen for updates
                registration.addEventListener('updatefound', () => {
                    const newWorker = registration.installing;
                    newWorker.addEventListener('statechange', () => {
                        if (newWorker.state === 'activated') {
                            showNotification('App updated! Refresh for latest version.', 'info');
                        }
                    });
                });
            })
            .catch(error => {
                console.log('Service Worker registration failed:', error);
            });
    });
    
    // Listen for messages from service worker
    navigator.serviceWorker.addEventListener('message', (event) => {
        if (event.data.type === 'ONLINE') {
            updateConnectionStatus(true);
            showNotification('🌐 Back online! Fetching fresh data...', 'success');
            // Optionally refresh weather data
            if (state.currentLocation) {
                handleSearch();
            }
        } else if (event.data.type === 'OFFLINE') {
            updateConnectionStatus(false);
            showNotification('📴 You\'re offline. Showing cached data.', 'info');
        }
    });
}

// Browser online/offline events
window.addEventListener('online', () => {
    updateConnectionStatus(true);
    showNotification('🌐 Connection restored!', 'success');
    console.log('Browser: Back online');
    
    // Refresh weather if we have a current location
    if (state.currentLocation) {
        setTimeout(() => handleSearch(), 500);
    }
});

window.addEventListener('offline', () => {
    updateConnectionStatus(false);
    showNotification('📴 No internet connection', 'info');
    console.log('Browser: Gone offline');
});

// ===================================
// Initialize App
// ===================================
function initApp() {
    console.log('WeatherAI initialized!');
    
    // Initialize theme
    initTheme();
    
    // Try to get user's location and fetch weather
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                // In production, use these coordinates to fetch weather
                console.log('User location:', position.coords);
                // For now, just show default San Francisco weather
                handleSearch();
            },
            (error) => {
                console.log('Geolocation error:', error);
                // Show default weather on geolocation error
                handleSearch();
            }
        );
    } else {
        // Show default weather if geolocation not available
        handleSearch();
    }
}

// Start the app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
} else {
    initApp();
}

// ===================================
// Weather Particle Effects
// ===================================

function createWeatherParticles() {
    const particlesContainer = document.getElementById('weatherParticles');
    if (!particlesContainer) return;
    
    // Clear existing particles
    particlesContainer.innerHTML = '';
    
    // Create 50 particles
    const particleCount = 50;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // Random positioning
        particle.style.left = Math.random() * 100 + '%';
        particle.style.animationDuration = (Math.random() * 3 + 2) + 's';
        particle.style.animationDelay = Math.random() * 5 + 's';
        particle.style.opacity = Math.random() * 0.5 + 0.3;
        
        particlesContainer.appendChild(particle);
    }
}

// Initialize particles on load
createWeatherParticles();

// Add smooth scroll behavior
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ===================================
// Animation Utilities
// ===================================

// Add CSS for notification animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100%);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100%);
        }
    }
`;
document.head.appendChild(style);

