import { audioService } from '../services/audioPlayer';
import { lookupWord } from '../services/contentLoader';
import { addCardToSrs } from '../services/srsEngine';
import { escapeHtml } from '../utils/html';
import { iconSvg } from './Icons';

let activePopover: HTMLElement | null = null;
let outsideHandler: ((e: MouseEvent) => void) | null = null;

export function closeWordPopover() {
  if (activePopover) {
    activePopover.remove();
    activePopover = null;
  }
  if (outsideHandler) {
    document.removeEventListener('click', outsideHandler);
    outsideHandler = null;
  }
}

export function showWordPopover(opts: {
  anchorEl: HTMLElement;
  hanzi: string;
  pinyinFallback?: string;
  meaningFallback?: string;
  sourceTag?: string;
}) {
  closeWordPopover();

  const word = lookupWord(opts.hanzi);
  const hanzi = word?.hanzi ?? opts.hanzi;
  const pinyin = word?.pinyin ?? opts.pinyinFallback ?? '';
  const meaning = word?.meaningVi ?? opts.meaningFallback ?? 'Chưa có chú thích chi tiết';
  const audio = word?.audio;

  const pop = document.createElement('div');
  pop.className = 'word-popover';
  pop.setAttribute('role', 'dialog');
  pop.setAttribute('aria-label', `Tra từ ${hanzi}`);

  pop.innerHTML = `
    <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:10px;">
      <div>
        <div class="hanzi" style="font-size:32px;font-weight:700;">${escapeHtml(hanzi)}</div>
        ${pinyin ? `<div class="pinyin" style="font-size:16px;">${escapeHtml(pinyin)}</div>` : ''}
      </div>
      <div style="display:flex;gap:6px;">
        ${audio ? `<button type="button" class="btn btn-sm btn-vocab" data-pop-play aria-label="Nghe phát âm">${iconSvg('speaker', 16)}</button>` : ''}
        <button type="button" class="btn btn-sm btn-soft" data-pop-close aria-label="Đóng">${iconSvg('close', 16)}</button>
      </div>
    </div>
    <div style="margin:8px 0 12px;font-weight:700;">${escapeHtml(meaning)}</div>
    ${word?.radical ? `<div style="font-size:13px;color:var(--ink-muted);margin-bottom:10px;">Bộ thủ: <strong>${escapeHtml(word.radical)}</strong></div>` : ''}
    <button type="button" class="btn btn-sm btn-review" data-pop-save style="width:100%;">+ Lưu vào Ôn tập</button>
  `;

  document.body.appendChild(pop);
  activePopover = pop;

  const rect = opts.anchorEl.getBoundingClientRect();
  const popRect = pop.getBoundingClientRect();
  let top = rect.bottom + 8;
  if (top + popRect.height > window.innerHeight - 12) {
    top = Math.max(12, rect.top - popRect.height - 8);
  }
  const left = Math.min(Math.max(12, rect.left), window.innerWidth - popRect.width - 12);
  pop.style.top = `${top}px`;
  pop.style.left = `${left}px`;

  pop.querySelector('[data-pop-close]')?.addEventListener('click', closeWordPopover);
  pop.querySelector('[data-pop-play]')?.addEventListener('click', (e) => {
    const btn = e.currentTarget as HTMLElement;
    if (!audio) return;
    btn.classList.add('is-speaking');
    audioService.play(audio, 1, () => btn.classList.remove('is-speaking'));
  });
  pop.querySelector('[data-pop-save]')?.addEventListener('click', async (e) => {
    const btn = e.currentTarget as HTMLButtonElement;
    audioService.playSfx('ok');
    await addCardToSrs({
      itemId: word?.id ?? `custom-${hanzi}`,
      facet: 'vocab',
      hanzi,
      pinyin,
      meaningVi: meaning,
      example: word?.examples[0],
      audio,
      tags: opts.sourceTag ? [opts.sourceTag] : [],
    });
    btn.textContent = 'Đã lưu vào Ôn tập';
    btn.disabled = true;
  });

  setTimeout(() => {
    outsideHandler = (e: MouseEvent) => {
      if (!pop.contains(e.target as Node) && e.target !== opts.anchorEl) {
        closeWordPopover();
      }
    };
    document.addEventListener('click', outsideHandler);
  }, 0);
}
