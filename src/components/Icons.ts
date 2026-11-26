export type IconName =
  | 'map'
  | 'read'
  | 'listen'
  | 'write'
  | 'review'
  | 'profile'
  | 'comm'
  | 'speaker'
  | 'flame'
  | 'star'
  | 'target'
  | 'lock'
  | 'crown'
  | 'close'
  | 'check'
  | 'book'
  | 'download'
  | 'mic'
  | 'play'
  | 'pause'
  | 'repeat'
  | 'arrow-left'
  | 'arrow-right';

const PATHS: Record<IconName, string> = {
  map: `<path d="M3 6.5 9 4l6 2.5L21 4v13.5L15 20l-6-2.5L3 20V6.5Z"/><path d="M9 4v13.5M15 6.5V20"/>`,
  read: `<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H12v17H6.5A2.5 2.5 0 0 0 4 22V5.5Z"/><path d="M20 5.5A2.5 2.5 0 0 0 17.5 3H12v17h5.5A2.5 2.5 0 0 1 20 22V5.5Z"/>`,
  listen: `<path d="M4 13a8 8 0 0 1 16 0"/><rect x="3" y="13" width="4" height="7" rx="2"/><rect x="17" y="13" width="4" height="7" rx="2"/>`,
  write: `<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5Z"/>`,
  review: `<rect x="5" y="4" width="14" height="16" rx="3"/><path d="M9 9h6M9 13h4"/>`,
  profile: `<circle cx="12" cy="8" r="4"/><path d="M5 20a7 7 0 0 1 14 0"/>`,
  comm: `<path d="M21 11.5a8 8 0 0 1-8 8 8.4 8.4 0 0 1-3.8-.9L4 20l1.4-4.2A8 8 0 1 1 21 11.5Z"/>`,
  speaker: `<path d="M11 5 6 9H3v6h3l5 4V5Z"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/><path d="M18.5 6a8.5 8.5 0 0 1 0 12"/>`,
  flame: `<path d="M12 3c2 3.2 5 5.4 5 9.5a5 5 0 1 1-10 0c0-2.5 1.3-4.6 2.5-6.2.4 1.6 1.5 2.5 2.5 2.7C11.5 7 12 5 12 3Z"/>`,
  star: `<path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1.1 6.2L12 17.3 6.4 20.2l1.1-6.2L3 9.6l6.2-.9L12 3Z"/>`,
  target: `<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r="1.2"/>`,
  lock: `<rect x="5" y="11" width="14" height="9" rx="2.5"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>`,
  crown: `<path d="m3 18 2-10 5 4 2-6 2 6 5-4 2 10H3Z"/>`,
  close: `<path d="M6 6l12 12M18 6 6 18"/>`,
  check: `<path d="m5 12.5 4.5 4.5L19 7.5"/>`,
  book: `<path d="M5 4h11a3 3 0 0 1 3 3v13H7a2 2 0 0 0-2 2V4Z"/><path d="M5 18h14"/>`,
  download: `<path d="M12 4v11"/><path d="m7.5 11.5 4.5 4.5 4.5-4.5"/><path d="M5 20h14"/>`,
  mic: `<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0"/><path d="M12 18v3"/>`,
  play: `<path d="m7 5 12 7-12 7V5Z"/>`,
  pause: `<rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/>`,
  repeat: `<path d="m17 2 4 4-4 4"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/>`,
  'arrow-left': `<path d="m15 6-6 6 6 6"/>`,
  'arrow-right': `<path d="m9 6 6 6-6 6"/>`,
};

export function iconSvg(name: IconName, size = 20, filled = false): string {
  return `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="${filled ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${PATHS[name]}</svg>`;
}

export function stickerBadge(name: IconName, colorVar: string, size = 34): string {
  return `<span class="sticker-badge" style="display:inline-flex;align-items:center;justify-content:center;width:${size}px;height:${size}px;border-radius:12px;background:${colorVar};border:2px solid #FFFFFF;box-shadow:0 2px 0 rgba(61,54,84,.12);color:#3D3654;">${iconSvg(name, Math.round(size * 0.56))}</span>`;
}
