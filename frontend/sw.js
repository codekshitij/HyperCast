// Service Worker for WeatherAI PWA
// This enables offline functionality and caching
//
// CACHING STRATEGY:
// - Network First: Always try to fetch fresh data when online
// - Cache Fallback: Use cached data only when offline or network fails
// - This ensures you always get live data with an internet connection
//
// Version: 2.0 - Network First Strategy

const CACHE_NAME = 'weatherai-v2';
const STATIC_CACHE = 'weatherai-static-v2';
const DYNAMIC_CACHE = 'weatherai-dynamic-v2';

// Assets to cache immediately
const STATIC_ASSETS = [
    '/',
    '/index.html',
    '/styles.css',
    '/script.js',
    '/manifest.json',
    'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap',
];

// Install event - cache static assets
self.addEventListener('install', (event) => {
    console.log('Service Worker: Installing...');
    
    event.waitUntil(
        caches.open(STATIC_CACHE)
            .then((cache) => {
                console.log('Service Worker: Caching static assets');
                return cache.addAll(STATIC_ASSETS);
            })
            .catch((error) => {
                console.error('Service Worker: Error caching static assets', error);
            })
    );
    
    // Force the waiting service worker to become the active service worker
    self.skipWaiting();
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
    console.log('Service Worker: Activating...');
    
    event.waitUntil(
        caches.keys()
            .then((cacheNames) => {
                return Promise.all(
                    cacheNames.map((cache) => {
                        if (cache !== STATIC_CACHE && cache !== DYNAMIC_CACHE) {
                            console.log('Service Worker: Deleting old cache:', cache);
                            return caches.delete(cache);
                        }
                    })
                );
            })
    );
    
    // Claim all clients immediately
    return self.clients.claim();
});

// Fetch event - Network First strategy (fresh data when online)
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);
    
    // Handle external resources (fonts, CDN assets) with Cache First
    if (url.origin !== location.origin) {
        event.respondWith(
            caches.match(request).then((cachedResponse) => {
                if (cachedResponse) {
                    return cachedResponse;
                }
                return fetch(request).then((response) => {
                    return caches.open(STATIC_CACHE).then((cache) => {
                        cache.put(request, response.clone());
                        return response;
                    });
                }).catch(() => cachedResponse);
            })
        );
        return;
    }
    
    // Network First Strategy for local resources
    event.respondWith(
        fetch(request)
            .then((networkResponse) => {
                // If network request succeeds, cache it and return
                console.log('Service Worker: Fetching fresh from network:', request.url);
                
                // Clone the response before caching
                const responseToCache = networkResponse.clone();
                
                // Cache successful responses (200-299 status codes)
                if (networkResponse.ok) {
                    caches.open(DYNAMIC_CACHE).then((cache) => {
                        cache.put(request, responseToCache);
                    });
                }
                
                return networkResponse;
            })
            .catch((error) => {
                // Network failed, try to serve from cache
                console.log('Service Worker: Network failed, trying cache:', request.url);
                
                return caches.match(request)
                    .then((cachedResponse) => {
                        if (cachedResponse) {
                            console.log('Service Worker: Serving from cache (offline):', request.url);
                            return cachedResponse;
                        }
                        
                        // If not in cache, try to return the offline page
                        console.error('Service Worker: Resource not found in cache:', request.url);
                        
                        // For navigation requests, return the main page
                        if (request.mode === 'navigate') {
                            return caches.match('/index.html');
                        }
                        
                        // For other requests, throw the error
                        throw error;
                    });
            })
    );
});

// Listen for messages from the client
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
    
    if (event.data && event.data.type === 'CLEAR_CACHE') {
        event.waitUntil(
            caches.keys().then((cacheNames) => {
                return Promise.all(
                    cacheNames.map((cacheName) => {
                        return caches.delete(cacheName);
                    })
                );
            })
        );
    }
});

// Background sync for offline requests
self.addEventListener('sync', (event) => {
    console.log('Service Worker: Background sync', event.tag);
    
    if (event.tag === 'sync-weather-data') {
        event.waitUntil(syncWeatherData());
    }
});

// Function to sync weather data in background
async function syncWeatherData() {
    try {
        // Implement background sync logic here
        console.log('Service Worker: Syncing weather data...');
        // This would fetch latest weather data when connection is restored
    } catch (error) {
        console.error('Service Worker: Background sync failed', error);
    }
}

// Push notification handler (for future real-time updates)
self.addEventListener('push', (event) => {
    console.log('Service Worker: Push notification received');
    
    if (event.data) {
        const data = event.data.json();
        
        const options = {
            body: data.body || 'New weather update available',
            icon: data.icon || '/icon-192x192.png',
            badge: '/badge-72x72.png',
            data: data.data || {},
            actions: [
                {
                    action: 'view',
                    title: 'View Weather'
                },
                {
                    action: 'close',
                    title: 'Close'
                }
            ],
            vibrate: [200, 100, 200],
            tag: 'weather-update',
            renotify: true,
        };
        
        event.waitUntil(
            self.registration.showNotification(data.title || 'WeatherAI Update', options)
        );
    }
});

// Notification click handler
self.addEventListener('notificationclick', (event) => {
    console.log('Service Worker: Notification clicked', event.action);
    
    event.notification.close();
    
    if (event.action === 'view') {
        event.waitUntil(
            clients.openWindow('/')
        );
    }
});

// Handle periodic background sync (experimental)
self.addEventListener('periodicsync', (event) => {
    if (event.tag === 'weather-refresh') {
        event.waitUntil(syncWeatherData());
    }
});

// Network status change handlers
self.addEventListener('online', () => {
    console.log('Service Worker: Back online - will fetch fresh data');
    
    // Notify all clients that we're back online
    self.clients.matchAll().then(clients => {
        clients.forEach(client => {
            client.postMessage({
                type: 'ONLINE',
                message: 'Connection restored - fetching fresh data'
            });
        });
    });
    
    syncWeatherData();
});

self.addEventListener('offline', () => {
    console.log('Service Worker: Gone offline - will use cached data');
    
    // Notify all clients that we're offline
    self.clients.matchAll().then(clients => {
        clients.forEach(client => {
            client.postMessage({
                type: 'OFFLINE',
                message: 'No connection - using cached data'
            });
        });
    });
});

