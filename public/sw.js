const CACHE_NAME = 'baobao-cache-v1';

const APP_SHELL_FILES = [
  '',
  'index.html',
  'manifest.webmanifest',
  'icons/bao-icon.svg',
  'content/curriculum.json',
  'content/radicals.json',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(async (cache) => {
      const base = self.registration.scope;
      const baseUrls = APP_SHELL_FILES.map((rel) => new URL(rel, base).toString());
      await cache.addAll(baseUrls);
      try {
        const htmlRes = await cache.match(new URL('index.html', base).toString());
        if (htmlRes) {
          const html = await htmlRes.text();
          const assetMatches = [...html.matchAll(/(?:src|href)="([^"]+\.(?:js|css|svg|webmanifest))"/g)];
          const assetUrls = assetMatches.map((m) => new URL(m[1], self.location.origin).toString());
          if (assetUrls.length > 0) {
            await cache.addAll(assetUrls);
          }
        }
      } catch {
        // ignore parse fallback
      }
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME && key !== 'baobao-stage-cache-v1') {
            return caches.delete(key);
          }
          return Promise.resolve();
        })
      )
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  if (req.mode === 'navigate') {
    event.respondWith(
      caches.match(req).then((cached) => {
        if (cached) return cached;
        return fetch(req)
          .then((res) => {
            const copy = res.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(req, copy));
            return res;
          })
          .catch(() => caches.match(new URL('index.html', self.registration.scope).toString()));
      })
    );
    return;
  }

  event.respondWith(
    caches.match(req).then((cached) => {
      if (cached) return cached;
      return fetch(req).then((res) => {
        if (res && res.status === 200) {
          const copy = res.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(req, copy));
        }
        return res;
      });
    })
  );
});

self.addEventListener('message', (event) => {
  const data = event.data;
  if (!data || data.type !== 'CACHE_STAGE' || !Array.isArray(data.urls)) return;

  const urls = data.urls;
  const source = event.source;
  event.waitUntil(
    (async () => {
      const cache = await caches.open(CACHE_NAME);
      let ok = 0;
      for (let i = 0; i < urls.length; i++) {
        const targetUrl = urls[i];
        try {
          const existing = await cache.match(targetUrl);
          if (existing) {
            ok += 1;
          } else {
            const res = await fetch(targetUrl);
            if (res.ok) {
              await cache.put(targetUrl, res.clone());
              ok += 1;
            }
          }
        } catch {
          // ignore individual failure
        }
        if (source) {
          source.postMessage({ type: 'CACHE_STAGE_PROGRESS', done: i + 1, total: urls.length });
        }
      }
      if (source) {
        source.postMessage({ type: 'CACHE_STAGE_DONE', ok, total: urls.length });
      }
    })()
  );
});
