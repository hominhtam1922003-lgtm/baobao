const base = import.meta.env.BASE_URL;

export async function registerPwa(): Promise<void> {
  if (!('serviceWorker' in navigator)) return;
  try {
    let reloaded = false;
    navigator.serviceWorker.addEventListener('controllerchange', () => {
      if (reloaded) return;
      reloaded = true;
      window.location.reload();
    });
    const reg = await navigator.serviceWorker.register(`${base}sw.js`, { scope: base });
    reg.update().catch(() => {});
  } catch {
    // SW registration may fail on unsupported contexts; app still works online.
  }
}

export async function requestPersistentStorage(): Promise<boolean> {
  if (typeof navigator === 'undefined' || !navigator.storage?.persist) return false;
  try {
    const persisted = await navigator.storage.persisted();
    if (persisted) return true;
    return await navigator.storage.persist();
  } catch {
    return false;
  }
}

export async function precacheStageAssets(
  urls: string[],
  onProgress?: (done: number, total: number) => void
): Promise<{ ok: number; total: number }> {
  const total = urls.length;
  if ('serviceWorker' in navigator && navigator.serviceWorker.controller) {
    const ctrl = navigator.serviceWorker.controller;
    return new Promise((resolve) => {
      const handler = (ev: MessageEvent) => {
        const msg = ev.data;
        if (!msg || typeof msg !== 'object') return;
        if (msg.type === 'CACHE_STAGE_PROGRESS') {
          onProgress?.(msg.done, msg.total);
        } else if (msg.type === 'CACHE_STAGE_DONE') {
          navigator.serviceWorker.removeEventListener('message', handler);
          resolve({ ok: msg.ok, total: msg.total });
        }
      };
      navigator.serviceWorker.addEventListener('message', handler);
      ctrl.postMessage({ type: 'CACHE_STAGE', urls });
    });
  }

  // Fallback directly via Cache API if SW hasn't claimed yet
  if (typeof caches !== 'undefined') {
    const cache = await caches.open('baobao-stage-cache-v2');
    let ok = 0;
    for (let i = 0; i < urls.length; i++) {
      try {
        const res = await fetch(urls[i]);
        if (res.ok) {
          await cache.put(urls[i], res.clone());
          ok += 1;
        }
      } catch {
        // skip unreachable
      }
      onProgress?.(i + 1, total);
    }
    return { ok, total };
  }
  return { ok: 0, total };
}
