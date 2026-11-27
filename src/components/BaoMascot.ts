import type { BaoAccessory, BaoWardrobe } from '../services/db';
import { DEFAULT_WARDROBE, legacyAccessoryToWardrobe } from '../services/shopCatalog';

export type BaoMood = 'happy' | 'wave' | 'headphones' | 'backpack' | 'celebrate' | 'point' | 'love' | 'think';

export interface BaoOptions {
  mood?: BaoMood;
  size?: number;
  accessory?: BaoAccessory;
  wardrobe?: Partial<BaoWardrobe>;
  label?: string;
  interactive?: boolean;
}

function renderBackground(bg: string): string {
  if (bg === 'bamboo-grove') {
    return `
      <circle cx="80" cy="80" r="74" fill="#D9F6EF" stroke="#1FC8A9" stroke-width="3"/>
      <path d="M26 138V44M36 142V56M134 138V40M124 144V62" stroke="#1FC8A9" stroke-width="5" stroke-linecap="round" opacity="0.45"/>
      <ellipse cx="44" cy="54" rx="10" ry="4" transform="rotate(-25 44 54)" fill="#14A388" opacity="0.5"/>
      <ellipse cx="116" cy="56" rx="10" ry="4" transform="rotate(25 116 56)" fill="#14A388" opacity="0.5"/>
      <circle cx="122" cy="30" r="10" fill="#FFF3B0" opacity="0.85"/>
    `;
  }
  if (bg === 'boba-cafe') {
    return `
      <circle cx="80" cy="80" r="74" fill="#FFF0D9" stroke="#FF9600" stroke-width="3"/>
      <circle cx="34" cy="44" r="10" fill="#FFE3E8"/>
      <circle cx="128" cy="48" r="12" fill="#FFE3E8"/>
      <circle cx="40" cy="126" r="7" fill="#D97E06" opacity="0.28"/>
      <circle cx="56" cy="134" r="6" fill="#D97E06" opacity="0.28"/>
      <circle cx="118" cy="128" r="7" fill="#D97E06" opacity="0.28"/>
      <path d="M22 66q12-10 24 0t24 0 24 0 24 0 24 0" stroke="#FF6B81" stroke-width="3" fill="none" opacity="0.35"/>
    `;
  }
  if (bg === 'lantern-street') {
    return `
      <circle cx="80" cy="80" r="74" fill="#FFE3E8" stroke="#FF6B81" stroke-width="3"/>
      <path d="M20 44q60 16 120 0" stroke="#E04E66" stroke-width="2" fill="none" opacity="0.6"/>
      <ellipse cx="38" cy="54" rx="8" ry="10" fill="#FF6B81" stroke="#3D3654" stroke-width="1.8"/>
      <ellipse cx="122" cy="54" rx="8" ry="10" fill="#FF6B81" stroke="#3D3654" stroke-width="1.8"/>
      <circle cx="38" cy="67" r="2.5" fill="#FFC531"/>
      <circle cx="122" cy="67" r="2.5" fill="#FFC531"/>
      <circle cx="80" cy="30" r="6" fill="#FFC531" opacity="0.7"/>
    `;
  }
  if (bg === 'starry-night') {
    return `
      <circle cx="80" cy="80" r="74" fill="#EFEAF9" stroke="#8F82C8" stroke-width="3"/>
      <path d="M120 28a12 12 0 1 0 10 18 9 9 0 1 1-10-18Z" fill="#FFC531" stroke="#E0A800" stroke-width="1.5"/>
      <path d="M36 36l2 5 5 2-5 2-2 5-2-5-5-2 5-2Z" fill="#FFC531"/>
      <path d="M126 112l1.8 4 4 1.8-4 1.8-1.8 4-1.8-4-4-1.8 4-1.8Z" fill="#FF6B81"/>
      <circle cx="48" cy="54" r="3" fill="#8F82C8" opacity="0.6"/>
      <circle cx="110" cy="48" r="2.5" fill="#1CB0F6" opacity="0.7"/>
    `;
  }
  return '';
}

function renderOutfit(outfit: string): string {
  if (outfit === 'red-scarf') {
    return `
      <path d="M51 96q29 14 58 0l-4 13q-25 11-50 0Z" fill="#FF6B81" stroke="#3D3654" stroke-width="3" stroke-linejoin="round"/>
      <path d="M92 103l12 17-12 4-8-16Z" fill="#E04E66" stroke="#3D3654" stroke-width="2.5" stroke-linejoin="round"/>
      <path d="M58 103q22 7 44 0" stroke="#FFE3E8" stroke-width="2.2" stroke-linecap="round" fill="none"/>
    `;
  }
  if (outfit === 'peach-hoodie') {
    return `
      <path d="M44 103c4-7 16-10 36-10s32 3 36 10l5 27c-12 10-70 10-82 0Z" fill="#FF6B81" stroke="#3D3654" stroke-width="3.2" stroke-linejoin="round"/>
      <path d="M62 117h36v12c0 4-3 6-6 6H68c-3 0-6-2-6-6Z" fill="#FFE3E8" stroke="#3D3654" stroke-width="2.4"/>
      <path d="M72 97v14M88 97v14" stroke="#FFFFFF" stroke-width="2.6" stroke-linecap="round"/>
      <circle cx="72" cy="112" r="2.5" fill="#FFC531"/>
      <circle cx="88" cy="112" r="2.5" fill="#FFC531"/>
    `;
  }
  if (outfit === 'mint-sweater') {
    return `
      <path d="M44 103c4-7 16-10 36-10s32 3 36 10l5 27c-12 10-70 10-82 0Z" fill="#1FC8A9" stroke="#3D3654" stroke-width="3.2" stroke-linejoin="round"/>
      <path d="M54 98q26 9 52 0" stroke="#D9F6EF" stroke-width="4" stroke-linecap="round" fill="none"/>
      <path d="M46 124q34 9 68 0" stroke="#D9F6EF" stroke-width="3" stroke-linecap="round" fill="none"/>
      <ellipse cx="80" cy="116" rx="10" ry="5" transform="rotate(-18 80 116)" fill="#FFF3B0" stroke="#3D3654" stroke-width="2"/>
    `;
  }
  if (outfit === 'school-uniform') {
    return `
      <path d="M44 103c4-7 16-10 36-10s32 3 36 10l5 27c-12 10-70 10-82 0Z" fill="#FFFFFF" stroke="#3D3654" stroke-width="3.2" stroke-linejoin="round"/>
      <path d="M55 96l25 18 25-18" fill="#1CB0F6" stroke="#3D3654" stroke-width="2.6" stroke-linejoin="round"/>
      <path d="M74 111l6 7 6-7-3 12h-6Z" fill="#FF6B81" stroke="#3D3654" stroke-width="2.2" stroke-linejoin="round"/>
      <circle cx="80" cy="113" r="3.5" fill="#FF6B81" stroke="#3D3654" stroke-width="2"/>
    `;
  }
  if (outfit === 'tang-suit') {
    return `
      <path d="M44 103c4-7 16-10 36-10s32 3 36 10l5 27c-12 10-70 10-82 0Z" fill="#E04E66" stroke="#3D3654" stroke-width="3.2" stroke-linejoin="round"/>
      <path d="M80 95v41" stroke="#FFC531" stroke-width="3"/>
      <path d="M72 106h16M72 116h16M72 126h16" stroke="#FFC531" stroke-width="2.6" stroke-linecap="round"/>
      <circle cx="80" cy="106" r="2.2" fill="#FFF3B0"/>
      <circle cx="80" cy="116" r="2.2" fill="#FFF3B0"/>
      <circle cx="80" cy="126" r="2.2" fill="#FFF3B0"/>
    `;
  }
  if (outfit === 'bamboo-cape') {
    return `
      <path d="M46 98L28 134q24 8 44 2l8-36Z" fill="#FF9600" stroke="#3D3654" stroke-width="2.8" stroke-linejoin="round"/>
      <path d="M114 98l18 36q-24 8-44 2l-8-36Z" fill="#FF9600" stroke="#3D3654" stroke-width="2.8" stroke-linejoin="round"/>
      <path d="M52 96q28 12 56 0" stroke="#FFC531" stroke-width="6" stroke-linecap="round" fill="none"/>
      <circle cx="80" cy="103" r="6" fill="#FFC531" stroke="#3D3654" stroke-width="2.2"/>
    `;
  }
  return '';
}

function renderGlasses(glasses: string): string {
  if (glasses === 'star-glasses') {
    return `
      <path d="M54 54l3 7 8 1-6 5 2 8-7-4-7 4 2-8-6-5 8-1Z" fill="rgba(28,176,246,0.22)" stroke="#1CB0F6" stroke-width="2.8" stroke-linejoin="round"/>
      <path d="M106 54l3 7 8 1-6 5 2 8-7-4-7 4 2-8-6-5 8-1Z" fill="rgba(28,176,246,0.22)" stroke="#1CB0F6" stroke-width="2.8" stroke-linejoin="round"/>
      <path d="M68 64h24" stroke="#1CB0F6" stroke-width="3.2" stroke-linecap="round"/>
    `;
  }
  if (glasses === 'round-scholar') {
    return `
      <circle cx="62" cy="64" r="13" fill="rgba(255,246,214,0.25)" stroke="#D97E06" stroke-width="3"/>
      <circle cx="98" cy="64" r="13" fill="rgba(255,246,214,0.25)" stroke="#D97E06" stroke-width="3"/>
      <path d="M75 64h10" stroke="#D97E06" stroke-width="3"/>
    `;
  }
  if (glasses === 'cool-shades') {
    return `
      <rect x="47" y="54" width="28" height="19" rx="7" fill="#3D3654" stroke="#1CB0F6" stroke-width="2.6"/>
      <rect x="85" y="54" width="28" height="19" rx="7" fill="#3D3654" stroke="#1CB0F6" stroke-width="2.6"/>
      <path d="M75 62h10" stroke="#1CB0F6" stroke-width="3.2"/>
      <path d="M53 60l7 7M91 60l7 7" stroke="#FFFFFF" stroke-width="2.4" stroke-linecap="round" opacity="0.65"/>
    `;
  }
  if (glasses === 'heart-blush') {
    return `
      <path d="M46 76c0-3 4-4 5.5-1.5C53 72 57 73 57 76c0 3.5-5.5 6.5-5.5 6.5S46 79.5 46 76Z" fill="#FF6B81"/>
      <path d="M103 76c0-3 4-4 5.5-1.5C110 72 114 73 114 76c0 3.5-5.5 6.5-5.5 6.5S103 79.5 103 76Z" fill="#FF6B81"/>
      <circle cx="44" cy="72" r="2" fill="#FFC531"/>
      <circle cx="116" cy="72" r="2" fill="#FFC531"/>
    `;
  }
  return '';
}

function renderHat(hat: string): string {
  if (hat === 'bamboo-hat') {
    return `
      <path d="M34 36L80 11l46 25Z" fill="#FFC531" stroke="#3D3654" stroke-width="3.2" stroke-linejoin="round"/>
      <path d="M52 34L80 17l28 17" stroke="#D97E06" stroke-width="2" fill="none"/>
      <path d="M46 36h68" stroke="#FF6B81" stroke-width="4" stroke-linecap="round"/>
    `;
  }
  if (hat === 'sakura-bow') {
    return `
      <path d="M80 30c-12-12-26-8-24 4s16 8 24-1c8 9 22 13 24 1s-12-16-24-4Z" fill="#FF6B81" stroke="#3D3654" stroke-width="2.8" stroke-linejoin="round"/>
      <circle cx="80" cy="30" r="6" fill="#FFE3E8" stroke="#3D3654" stroke-width="2.4"/>
      <circle cx="80" cy="30" r="2.2" fill="#FFC531"/>
    `;
  }
  if (hat === 'tea-beret') {
    return `
      <ellipse cx="80" cy="28" rx="30" ry="12" fill="#1FC8A9" stroke="#3D3654" stroke-width="3"/>
      <path d="M80 16v-6" stroke="#3D3654" stroke-width="3.2" stroke-linecap="round"/>
      <circle cx="80" cy="9" r="3.5" fill="#14A388"/>
      <ellipse cx="94" cy="25" rx="6" ry="3" fill="#D9F6EF" opacity="0.7"/>
    `;
  }
  if (hat === 'bunny-ears') {
    return `
      <ellipse cx="63" cy="17" rx="8" ry="17" transform="rotate(-12 63 17)" fill="#FFFFFF" stroke="#3D3654" stroke-width="3"/>
      <ellipse cx="63" cy="18" rx="4" ry="11" transform="rotate(-12 63 18)" fill="#FFE3E8"/>
      <ellipse cx="97" cy="17" rx="8" ry="17" transform="rotate(12 97 17)" fill="#FFFFFF" stroke="#3D3654" stroke-width="3"/>
      <ellipse cx="97" cy="18" rx="4" ry="11" transform="rotate(12 97 18)" fill="#FFE3E8"/>
    `;
  }
  if (hat === 'chef-hat') {
    return `
      <path d="M54 34c-8-4-7-17 4-18 3-9 19-11 26-4 8-5 21-1 19 10 8 2 7 12-1 14H54Z" fill="#FFFFFF" stroke="#3D3654" stroke-width="3" stroke-linejoin="round"/>
      <rect x="54" y="30" width="52" height="9" rx="4" fill="#FFFBF3" stroke="#3D3654" stroke-width="2.6"/>
    `;
  }
  if (hat === 'explorer-cap') {
    return `
      <path d="M48 33c3-18 61-18 64 0Z" fill="#FF9600" stroke="#3D3654" stroke-width="3" stroke-linejoin="round"/>
      <path d="M42 33h76l-8 8H50Z" fill="#D97E06" stroke="#3D3654" stroke-width="2.8" stroke-linejoin="round"/>
      <circle cx="80" cy="23" r="5" fill="#FFC531" stroke="#3D3654" stroke-width="2.2"/>
    `;
  }
  if (hat === 'grad-cap') {
    return `
      <path d="M42 25L80 12l38 13-38 12Z" fill="#3D3654" stroke="#3D3654" stroke-width="2.5" stroke-linejoin="round"/>
      <path d="M56 30v8c8 5 40 5 48 0v-8" fill="#5B517A" stroke="#3D3654" stroke-width="2.5"/>
      <path d="M112 26v14" stroke="#FFC531" stroke-width="2.8" stroke-linecap="round"/>
      <circle cx="112" cy="42" r="3.5" fill="#FFC531"/>
    `;
  }
  if (hat === 'crown') {
    return `
      <path d="M54 31l7-18 19 11 19-11 7 18Z" fill="#FFC531" stroke="#3D3654" stroke-width="2.8" stroke-linejoin="round"/>
      <circle cx="80" cy="25" r="3.5" fill="#FF6B81"/>
      <circle cx="66" cy="26" r="2.5" fill="#1CB0F6"/>
      <circle cx="94" cy="26" r="2.5" fill="#1FC8A9"/>
    `;
  }
  return '';
}

function renderProp(prop: string): string {
  if (prop === 'bamboo-shoot') {
    return `
      <g transform="translate(115, 76)">
        <path d="M10 46V6" stroke="#14A388" stroke-width="6.5" stroke-linecap="round"/>
        <path d="M6 20h8M6 34h8" stroke="#D9F6EF" stroke-width="2.2"/>
        <ellipse cx="18" cy="14" rx="9" ry="4" transform="rotate(-24 18 14)" fill="#1FC8A9" stroke="#3D3654" stroke-width="2"/>
        <ellipse cx="2" cy="26" rx="8" ry="3.5" transform="rotate(24 2 26)" fill="#1FC8A9" stroke="#3D3654" stroke-width="2"/>
      </g>
    `;
  }
  if (prop === 'boba-tea') {
    return `
      <g transform="translate(112, 82)">
        <path d="M14 2V-8l6-3" stroke="#FF6B81" stroke-width="3.2" stroke-linecap="round" fill="none"/>
        <path d="M4 6h20l-3 28H7Z" fill="#FFF0D9" stroke="#3D3654" stroke-width="2.6" stroke-linejoin="round"/>
        <path d="M5 14h18l-2 20H7Z" fill="#F2C693"/>
        <rect x="2" y="3" width="24" height="5" rx="2.5" fill="#FF9600" stroke="#3D3654" stroke-width="2.2"/>
        <circle cx="10" cy="29" r="2.2" fill="#3D3654"/>
        <circle cx="15" cy="30" r="2.2" fill="#3D3654"/>
        <circle cx="19" cy="28" r="2.2" fill="#3D3654"/>
      </g>
    `;
  }
  if (prop === 'lantern-pin') {
    return `
      <g transform="translate(114, 78)">
        <path d="M14 0v6" stroke="#D97E06" stroke-width="2.5"/>
        <ellipse cx="14" cy="18" rx="11" ry="13" fill="#FF6B81" stroke="#3D3654" stroke-width="2.5"/>
        <path d="M5 18h18" stroke="#FFC531" stroke-width="2"/>
        <rect x="9" y="4" width="10" height="4" rx="1.5" fill="#FFC531" stroke="#3D3654" stroke-width="1.8"/>
        <rect x="9" y="29" width="10" height="4" rx="1.5" fill="#FFC531" stroke="#3D3654" stroke-width="1.8"/>
        <path d="M14 33v8" stroke="#FFC531" stroke-width="3" stroke-linecap="round"/>
      </g>
    `;
  }
  if (prop === 'orange-backpack') {
    return `
      <g transform="translate(108, 92)">
        <rect x="2" y="4" width="24" height="30" rx="10" fill="#FF9600" stroke="#3D3654" stroke-width="3"/>
        <rect x="6" y="16" width="16" height="12" rx="5" fill="#FFC531" stroke="#3D3654" stroke-width="2.2"/>
        <path d="M8 11h12" stroke="#FFFBF3" stroke-width="2.8" stroke-linecap="round"/>
      </g>
    `;
  }
  if (prop === 'paper-fan') {
    return `
      <g transform="translate(106, 86)">
        <path d="M14 28L2 8a24 24 0 0 1 32 0Z" fill="#FFE3E8" stroke="#3D3654" stroke-width="2.5" stroke-linejoin="round"/>
        <path d="M14 28L12 5M14 28L22 5" stroke="#FF6B81" stroke-width="1.6"/>
        <circle cx="18" cy="14" r="3" fill="#FF6B81"/>
      </g>
    `;
  }
  if (prop === 'music-notes') {
    return `
      <g>
        <path d="M126 44v-16l12-3v14" stroke="#8F82C8" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        <circle cx="123" cy="44" r="3.5" fill="#8F82C8"/>
        <circle cx="135" cy="39" r="3.5" fill="#FF6B81"/>
        <path d="M24 54v-12l8-2" stroke="#1CB0F6" stroke-width="2.5" stroke-linecap="round" fill="none"/>
        <circle cx="21" cy="54" r="3" fill="#1CB0F6"/>
      </g>
    `;
  }
  return '';
}

export function renderBaoSvg(opts: BaoOptions = {}): string {
  const mood = opts.mood ?? 'happy';
  const size = opts.size ?? 96;
  const aria = opts.label ?? 'Gấu trúc Bao';
  const w: BaoWardrobe = {
    ...DEFAULT_WARDROBE,
    ...(opts.accessory && opts.accessory !== 'none' ? legacyAccessoryToWardrobe(opts.accessory) : {}),
    ...(opts.wardrobe ?? {}),
  };

  // Eyes based on mood (kawaii chibi sparkle eyes)
  let eyeLeft = `<circle cx="64" cy="61.5" r="3.2" fill="#FFFFFF"/><circle cx="60.2" cy="66.5" r="1.4" fill="#FFFFFF" opacity="0.85"/>`;
  let eyeRight = `<circle cx="96" cy="61.5" r="3.2" fill="#FFFFFF"/><circle cx="99.8" cy="66.5" r="1.4" fill="#FFFFFF" opacity="0.85"/>`;

  if (mood === 'celebrate') {
    eyeLeft = `<path d="M56 64q6-8 13 0" stroke="#FFFFFF" stroke-width="3.4" stroke-linecap="round" fill="none"/>`;
    eyeRight = `<path d="M91 64q6-8 13 0" stroke="#FFFFFF" stroke-width="3.4" stroke-linecap="round" fill="none"/>`;
  } else if (mood === 'love') {
    eyeLeft = `<path d="M58 62c0-2.5 3-3.5 4.5-1 1.5-2.5 4.5-1.5 4.5 1 0 3-4.5 5.5-4.5 5.5S58 65 58 62Z" fill="#FF6B81"/>`;
    eyeRight = `<path d="M93 62c0-2.5 3-3.5 4.5-1 1.5-2.5 4.5-1.5 4.5 1 0 3-4.5 5.5-4.5 5.5S93 65 93 62Z" fill="#FF6B81"/>`;
  }

  const mouth =
    mood === 'celebrate' || mood === 'love'
      ? `<path d="M70 81c4 9 16 9 20 0Z" fill="#FF6B81" stroke="#3D3654" stroke-width="2.5" stroke-linejoin="round"/>`
      : mood === 'think'
      ? `<circle cx="80" cy="83" r="3.5" fill="#FF6B81" stroke="#3D3654" stroke-width="2.2"/>`
      : `<path d="M71 82q4.5 5 9 0q4.5 5 9 0" stroke="#3D3654" stroke-width="3" stroke-linecap="round" fill="none"/>`;

  const moodExtra =
    mood === 'headphones'
      ? `<path d="M38 62c0-24 19-41 42-41s42 17 42 41" stroke="#8F82C8" stroke-width="6.5" stroke-linecap="round" fill="none"/>
         <rect x="30" y="52" width="13" height="25" rx="6.5" fill="#8F82C8" stroke="#3D3654" stroke-width="2.8"/>
         <rect x="117" y="52" width="13" height="25" rx="6.5" fill="#8F82C8" stroke="#3D3654" stroke-width="2.8"/>`
      : mood === 'backpack' && w.prop === 'none'
      ? renderProp('orange-backpack')
      : mood === 'celebrate'
      ? `<path d="M26 36l2 5 5 2-5 2-2 5-2-5-5-2 5-2Z" fill="#FFC531"/>
         <path d="M132 32l2 5 5 2-5 2-2 5-2-5-5-2 5-2Z" fill="#FF6B81"/>`
      : '';

  const leftArm =
    mood === 'wave' || mood === 'celebrate'
      ? `<ellipse cx="36" cy="96" rx="10" ry="15" transform="rotate(-48 36 96)" fill="#3D3654"/>`
      : `<ellipse cx="42" cy="112" rx="10" ry="15" transform="rotate(20 42 112)" fill="#3D3654"/>`;

  const rightArm =
    mood === 'point' || mood === 'celebrate'
      ? `<ellipse cx="124" cy="96" rx="10" ry="15" transform="rotate(48 124 96)" fill="#3D3654"/>`
      : `<ellipse cx="118" cy="112" rx="10" ry="15" transform="rotate(-20 118 112)" fill="#3D3654"/>`;

  return `<svg class="bao-mascot ${opts.interactive ? 'is-interactive' : ''}" width="${size}" height="${size}" viewBox="0 0 160 160" fill="none" role="img" aria-label="${aria}">
    ${renderBackground(w.bg)}
    <!-- Soft ground shadow -->
    <ellipse cx="80" cy="145" rx="38" ry="7" fill="rgba(61,54,84,0.08)"/>
    <!-- Chubby Panda Body -->
    ${leftArm}
    ${rightArm}
    <ellipse cx="80" cy="116" rx="34" ry="27" fill="#FFFFFF" stroke="#3D3654" stroke-width="4"/>
    <ellipse cx="80" cy="118" rx="22" ry="16" fill="#FFFBF3"/>
    <!-- Outfit layer -->
    ${renderOutfit(w.outfit)}
    <!-- Cute Feet with pink paw pads -->
    <ellipse cx="59" cy="138" rx="13" ry="9" fill="#3D3654"/>
    <ellipse cx="101" cy="138" rx="13" ry="9" fill="#3D3654"/>
    <ellipse cx="59" cy="139" rx="5.5" ry="3.8" fill="#FFE3E8"/>
    <ellipse cx="101" cy="139" rx="5.5" ry="3.8" fill="#FFE3E8"/>
    <!-- Panda Ears -->
    <circle cx="49" cy="36" r="14" fill="#3D3654"/>
    <circle cx="49" cy="36" r="6" fill="#FFE3E8" opacity="0.45"/>
    <circle cx="111" cy="36" r="14" fill="#3D3654"/>
    <circle cx="111" cy="36" r="6" fill="#FFE3E8" opacity="0.45"/>
    <!-- Round Kawaii Head -->
    <ellipse cx="80" cy="66" rx="40" ry="36" fill="#FFFFFF" stroke="#3D3654" stroke-width="4.2"/>
    <!-- Eye Patches -->
    <ellipse cx="62" cy="64" rx="11.5" ry="13.5" transform="rotate(-14 62 64)" fill="#3D3654"/>
    <ellipse cx="98" cy="64" rx="11.5" ry="13.5" transform="rotate(14 98 64)" fill="#3D3654"/>
    ${eyeLeft}
    ${eyeRight}
    <!-- Cute Nose & Rosy Cheeks -->
    <ellipse cx="80" cy="74" rx="6.5" ry="4.5" fill="#3D3654"/>
    ${mouth}
    <ellipse cx="48" cy="77" rx="7" ry="4.5" fill="#FF6B81" opacity="0.42"/>
    <ellipse cx="112" cy="77" rx="7" ry="4.5" fill="#FF6B81" opacity="0.42"/>
    <!-- Face/Glasses layer -->
    ${renderGlasses(w.glasses)}
    <!-- Mood extras -->
    ${moodExtra}
    <!-- Hat layer -->
    ${renderHat(w.hat)}
    <!-- Handheld prop layer -->
    ${renderProp(w.prop)}
  </svg>`;
}
