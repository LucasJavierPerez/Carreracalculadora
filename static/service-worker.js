self.addEventListener("install", event => {
  event.waitUntil(
    caches.open("app-cache-v2").then(cache => {
      return cache.addAll([
        "/",
        "/calculator",
        "/training_table",
        "/static/style.css",
        "/static/manifest.json"
      ]).catch(error => {
        console.error('Failed to cache resources:', error);
      });
    })
  );
});

self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});
