export type BaoMood = 'happy' | 'wave' | 'headphones' | 'backpack' | 'celebrate' | 'point';

export interface BaoOptions {
  mood?: BaoMood;
  size?: number;
  accessory?: 'none' | 'bamboo-hat' | 'red-scarf' | 'star-glasses' | 'crown';
  label?: string;
}

export function renderBaoSvg(opts: BaoOptions = {}): string {
  const mood = opts.mood ?? 'happy';
  const size = opts.size ?? 88;
  const accessory = opts.accessory ?? 'none';
  const aria = opts.label ?? 'Gấu trúc Bao';

  const eyeLeft =
    mood === 'celebrate'
      ? `<path d="M41 62q6-7 12 0" stroke="#FFFFFF" stroke-width="3.2" stroke-linecap="round" fill="none"/>`
      : `<circle cx="49" cy="62" r="4" fill="#FFFFFF"/>`;
  const eyeRight =
    mood === 'celebrate'
      ? `<path d="M75 62q6-7 12 0" stroke="#FFFFFF" stroke-width="3.2" stroke-linecap="round" fill="none"/>`
      : `<circle cx="79" cy="62" r="4" fill="#FFFFFF"/>`;

  const mouth =
    mood === 'celebrate'
      ? `<path d="M54 83c4 7 16 7 20 0Z" fill="#FF6B81" stroke="#3D3654" stroke-width="2.5"/>`
      : `<path d="M56 85c3 4 13 4 16 0" stroke="#3D3654" stroke-width="3.5" stroke-linecap="round"/>`;

  const extra =
    mood === 'headphones'
      ? `<path d="M25 63c0-23 17-39 39-39s39 16 39 39" stroke="#8F82C8" stroke-width="6" stroke-linecap="round" fill="none"/>
         <rect x="17" y="54" width="13" height="24" rx="6.5" fill="#8F82C8" stroke="#3D3654" stroke-width="2.5"/>
         <rect x="98" y="54" width="13" height="24" rx="6.5" fill="#8F82C8" stroke="#3D3654" stroke-width="2.5"/>`
      : mood === 'backpack'
      ? `<rect x="88" y="76" width="22" height="28" rx="9" fill="#FF9600" stroke="#3D3654" stroke-width="3"/>
         <path d="M92 84h14" stroke="#FFFBF3" stroke-width="3" stroke-linecap="round"/>`
      : mood === 'point'
      ? `<path d="M98 78l16-10" stroke="#3D3654" stroke-width="8" stroke-linecap="round"/>
         <circle cx="115" cy="67" r="5" fill="#FFFFFF" stroke="#3D3654" stroke-width="2.5"/>`
      : mood === 'wave'
      ? `<path d="M24 78l-10-14" stroke="#3D3654" stroke-width="9" stroke-linecap="round"/>`
      : '';

  let accSvg = '';
  if (accessory === 'bamboo-hat') {
    accSvg = `<path d="M28 36L64 14l36 22Z" fill="#FFC531" stroke="#3D3654" stroke-width="3" stroke-linejoin="round"/>`;
  } else if (accessory === 'red-scarf') {
    accSvg = `<path d="M37 95q27 12 54 0l-5 12q-22 9-44 0Z" fill="#FF6B81" stroke="#3D3654" stroke-width="2.5"/>`;
  } else if (accessory === 'star-glasses') {
    accSvg = `<rect x="34" y="54" width="24" height="16" rx="7" fill="none" stroke="#1CB0F6" stroke-width="3.5"/>
              <rect x="70" y="54" width="24" height="16" rx="7" fill="none" stroke="#1CB0F6" stroke-width="3.5"/>
              <path d="M58 62h12" stroke="#1CB0F6" stroke-width="3.5"/>`;
  } else if (accessory === 'crown') {
    accSvg = `<path d="M44 29l6-14 14 9 14-9 6 14Z" fill="#FFC531" stroke="#3D3654" stroke-width="2.5" stroke-linejoin="round"/>`;
  }

  return `<svg width="${size}" height="${size}" viewBox="0 0 128 128" fill="none" role="img" aria-label="${aria}">
    <circle cx="35" cy="36" r="14" fill="#3D3654"/>
    <circle cx="93" cy="36" r="14" fill="#3D3654"/>
    <circle cx="64" cy="68" r="38" fill="#FFFFFF" stroke="#3D3654" stroke-width="4.5"/>
    <ellipse cx="47" cy="64" rx="10.5" ry="12.5" transform="rotate(-14 47 64)" fill="#3D3654"/>
    <ellipse cx="81" cy="64" rx="10.5" ry="12.5" transform="rotate(14 81 64)" fill="#3D3654"/>
    ${eyeLeft}
    ${eyeRight}
    <ellipse cx="64" cy="76" rx="6.5" ry="4.5" fill="#3D3654"/>
    ${mouth}
    <circle cx="38" cy="78" r="5.5" fill="#FF6B81" opacity="0.5"/>
    <circle cx="90" cy="78" r="5.5" fill="#FF6B81" opacity="0.5"/>
    ${extra}
    ${accSvg}
  </svg>`;
}
