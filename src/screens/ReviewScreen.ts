import confetti from 'canvas-confetti';
import { renderAppShell } from '../components/AppShell';
import { renderBaoSvg } from '../components/BaoMascot';
import { iconSvg } from '../components/Icons';
import { audioService } from '../services/audioPlayer';
import { loadStageWords } from '../services/contentLoader';
import {
  addCardToSrs,
  commitReview,
  ensureProgress,
  ensureSettings,
  filterQueue,
  getAllCards,
  previewIntervals,
  recordStudyActivity,
  type QueueFilter,
  type SrsCardRecord,
} from '../services/srsEngine';
import type { ReviewRating } from '../types/curriculum';
import { escapeHtml } from '../utils/html';

export async function renderReviewScreen(root: HTMLElement): Promise<() => void> {
  const [progress, settings, words] = await Promise.all([
    ensureProgress(),
    ensureSettings(),
    loadStageWords(1),
  ]);

  let cards = await getAllCards();
  // Seed 4 starter cards on very first visit so user can test SRS immediately even before completing a lesson
  if (cards.length === 0 && words.length > 0) {
    for (const w of words.slice(0, 4)) {
      await addCardToSrs({
        itemId: w.id,
        facet: 'vocab',
        hanzi: w.hanzi,
        pinyin: w.pinyin,
        meaningVi: w.meaningVi,
        example: w.examples[0],
        audio: w.audio,
      });
    }
    cards = await getAllCards();
  }

  const body = renderAppShell({
    root,
    activeTab: 'review',
    title: 'Ôn tập Flashcard',
    progress,
    settings,
  });

  let filter: QueueFilter = 'due';
  let queue: SrsCardRecord[] = filterQueue(cards, filter);
  let idx = 0;
  let flipped = false;
  let streakInSession = 0;
  let reviewedCount = 0;
  let sessionDone = false;
  let keyHandler: ((e: KeyboardEvent) => void) | null = null;

  const setKey = (fn: ((e: KeyboardEvent) => void) | null) => {
    if (keyHandler) document.removeEventListener('keydown', fn ? keyHandler : () => {});
    if (keyHandler) document.removeEventListener('keydown', keyHandler);
    keyHandler = fn;
    if (fn) document.addEventListener('keydown', fn);
  };

  const refreshCounts = () => ({
    due: filterQueue(cards, 'due').length,
    weak: filterQueue(cards, 'weak').length,
    story: filterQueue(cards, 'story').length,
    writing: filterQueue(cards, 'writing').length,
  });

  const render = () => {
    setKey(null);
    const counts = refreshCounts();
    const current = queue[idx];

    const chips: { id: QueueFilter; label: string; count: number }[] = [
      { id: 'due', label: 'Đến hạn hôm nay', count: counts.due },
      { id: 'weak', label: 'Từ yếu', count: counts.weak },
      { id: 'story', label: 'Từ trong truyện', count: counts.story },
      { id: 'writing', label: 'Chữ viết yếu', count: counts.writing },
    ];

    const filterHtml = `
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:20px;">
        ${chips
          .map(
            (c) => `<button type="button" class="btn btn-sm ${filter === c.id ? 'btn-review' : 'btn-soft'}" data-srs-filter="${c.id}">
              ${escapeHtml(c.label)} <span class="chip" style="padding:2px 8px;font-size:12px;">${c.count}</span>
            </button>`
          )
          .join('')}
      </div>
    `;

    if (sessionDone || !current) {
      body.innerHTML = `
        <div style="max-width:680px;margin:0 auto;">
          ${filterHtml}
          <div class="clay-card" style="padding:32px;text-align:center;">
            ${renderBaoSvg({ mood: reviewedCount > 0 ? 'celebrate' : 'happy', size: 100 })}
            <h2 style="margin:10px 0 6px;">${reviewedCount > 0 ? `Xong phiên ôn tập (${reviewedCount} thẻ)!` : 'Chưa có thẻ đến hạn ở nhóm này'}</h2>
            <p style="margin:0 0 18px;color:var(--ink-muted);">
              ${reviewedCount > 0 ? 'Trí nhớ dài hạn vừa được củng cố theo thuật toán lặp ngắt quãng.' : 'Bạn có thể chuyển sang nhóm lọc khác hoặc học thêm bài mới trên Bản đồ.'}
            </p>
            <div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;">
              ${counts.weak > 0 ? `<button type="button" class="btn btn-review" data-extra-weak>Ôn thêm 5 thẻ yếu</button>` : ''}
              <a href="#/" class="btn btn-soft">Về bản đồ học</a>
            </div>
          </div>
        </div>
      `;
      bindFilterEvents();
      body.querySelector('[data-extra-weak]')?.addEventListener('click', () => {
        filter = 'weak';
        queue = filterQueue(cards, 'weak').slice(0, 5);
        idx = 0;
        flipped = false;
        sessionDone = false;
        render();
      });
      return;
    }

    const intervals = previewIntervals(current);
    const facetLabel =
      current.facet === 'vocab' ? 'Mặt Từ vựng' : current.facet === 'sentence' ? 'Mặt Câu mẫu' : 'Mặt Chữ viết';

    const frontContent =
      current.facet === 'sentence'
        ? `<div class="hanzi" style="font-size:28px;font-weight:600;text-align:center;">${escapeHtml(current.hanzi)}</div>`
        : `<div class="hanzi" style="font-size:56px;font-weight:700;">${escapeHtml(current.hanzi)}</div>`;

    const ratingButtons: { key: string; rating: ReviewRating; label: string; cls: string }[] = [
      { key: '1', rating: 'Again', label: 'Again', cls: 'btn-comm' },
      { key: '2', rating: 'Hard', label: 'Hard', cls: 'btn-write' },
      { key: '3', rating: 'Good', label: 'Good', cls: 'btn-read' },
      { key: '4', rating: 'Easy', label: 'Easy', cls: 'btn-vocab' },
    ];

    body.innerHTML = `
      <div style="max-width:680px;margin:0 auto;">
        ${filterHtml}

        ${
          streakInSession > 0 && streakInSession % 10 === 0
            ? `<div class="clay-card" style="padding:12px 18px;margin-bottom:14px;background:var(--review-soft);border-color:var(--review);display:flex;align-items:center;gap:12px;">
                 ${renderBaoSvg({ mood: 'celebrate', size: 48 })}
                 <strong>Tuyệt đỉnh! ${streakInSession} thẻ đúng liên tiếp trong phiên!</strong>
               </div>`
            : ''
        }

        <div style="perspective:1200px;">
          <div class="flashcard-3d ${flipped ? 'is-flipped' : ''}" data-flip-card tabindex="0" role="button" aria-label="Lật thẻ flashcard (Space)" style="position:relative;width:100%;max-width:640px;min-height:360px;margin:0 auto;transform-style:preserve-3d;transition:transform var(--t-flip) ease;cursor:pointer;">
            <!-- Front -->
            <div class="clay-card" style="position:absolute;inset:0;backface-visibility:hidden;border-radius:var(--r-flash);border:2px solid var(--review);box-shadow:0 5px 0 var(--review-lip), var(--shadow-clay);padding:28px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;">
              <div style="position:absolute;top:16px;left:20px;right:20px;display:flex;justify-content:space-between;align-items:center;">
                <span class="chip" style="background:var(--review-soft);">${escapeHtml(facetLabel)}</span>
                <span style="font-size:13px;color:var(--ink-muted);font-weight:700;">Thẻ ${idx + 1}/${queue.length}</span>
              </div>
              ${frontContent}
              ${current.audio ? `<button type="button" class="btn btn-sm btn-vocab" data-card-audio>${iconSvg('speaker', 16)} Nghe</button>` : ''}
              <div style="font-size:13px;color:var(--ink-muted);">Chạm thẻ hoặc bấm Space để lật</div>
            </div>

            <!-- Back -->
            <div class="clay-card" style="position:absolute;inset:0;backface-visibility:hidden;transform:rotateY(180deg);border-radius:var(--r-flash);border:2px solid var(--review);box-shadow:0 5px 0 var(--review-lip), var(--shadow-clay);padding:26px;display:flex;flex-direction:column;justify-content:center;gap:10px;">
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                  <div class="hanzi" style="font-size:34px;font-weight:700;">${escapeHtml(current.hanzi)}</div>
                  <div class="pinyin" style="font-size:18px;">${escapeHtml(current.pinyin)}</div>
                </div>
                ${current.audio ? `<button type="button" class="btn btn-sm btn-vocab" data-card-audio>${iconSvg('speaker', 16)} Nghe</button>` : ''}
              </div>
              <div style="font-size:22px;font-weight:800;">${escapeHtml(current.meaningVi)}</div>
              ${
                current.example
                  ? `<div style="margin-top:8px;padding:12px 14px;border-radius:14px;background:var(--bg);border:1.5px solid var(--border);display:flex;justify-content:space-between;align-items:center;gap:10px;">
                       <div>
                         <div class="hanzi" style="font-size:20px;">${escapeHtml(current.example.hanzi)}</div>
                         <div class="pinyin">${escapeHtml(current.example.pinyin)}</div>
                         <div style="font-size:14px;color:var(--ink-muted);">${escapeHtml(current.example.vi)}</div>
                       </div>
                       ${current.example.audio ? `<button type="button" class="btn btn-sm btn-vocab" data-ex-audio>${iconSvg('speaker', 15)}</button>` : ''}
                     </div>`
                  : ''
              }
            </div>
          </div>
        </div>

        <style>
          .flashcard-3d.is-flipped { transform: rotateY(180deg); }
        </style>

        <div style="max-width:640px;margin:20px auto 0;display:grid;grid-template-columns:repeat(4,1fr);gap:10px;">
          ${
            flipped
              ? ratingButtons
                  .map(
                    (b) => `<button type="button" class="btn ${b.cls}" data-rate="${b.rating}" style="flex-direction:column;padding:10px 6px;">
                      <span>[${b.key}] ${b.label}</span>
                      <span style="font-size:12px;font-weight:600;opacity:0.9;">${escapeHtml(intervals[b.rating])}</span>
                    </button>`
                  )
                  .join('')
              : `<button type="button" class="btn btn-review btn-lg" data-show-ans style="grid-column:1 / -1;">Lật thẻ (Space)</button>`
          }
        </div>
      </div>
    `;

    bindFilterEvents();

    const toggleFlip = () => {
      flipped = !flipped;
      audioService.playSfx('pop');
      render();
    };

    body.querySelector('[data-flip-card]')?.addEventListener('click', (e) => {
      if ((e.target as HTMLElement).closest('button')) return;
      toggleFlip();
    });
    body.querySelector('[data-show-ans]')?.addEventListener('click', toggleFlip);

    body.querySelectorAll<HTMLElement>('[data-card-audio]').forEach((b) => {
      b.addEventListener('click', (e) => {
        e.stopPropagation();
        if (current.audio) audioService.play(current.audio);
      });
    });
    body.querySelector('[data-ex-audio]')?.addEventListener('click', (e) => {
      e.stopPropagation();
      if (current.example?.audio) audioService.play(current.example.audio);
    });

    const rateCurrent = async (rating: ReviewRating) => {
      const updated = await commitReview(current, rating);
      cards = cards.map((c) => (c.key === updated.key ? updated : c));
      reviewedCount += 1;
      if (rating === 'Good' || rating === 'Easy') {
        streakInSession += 1;
        audioService.playSfx('ok');
        if (streakInSession % 10 === 0) {
          confetti({ particleCount: 25, spread: 45, origin: { y: 0.7 } });
        }
      } else {
        streakInSession = 0;
        audioService.playSfx('pop');
      }
      await recordStudyActivity({ xpEarned: 5 });

      if (idx + 1 < queue.length) {
        idx += 1;
        flipped = false;
      } else {
        sessionDone = true;
      }
      render();
    };

    body.querySelectorAll<HTMLElement>('[data-rate]').forEach((b) => {
      b.addEventListener('click', () => rateCurrent(b.dataset.rate as ReviewRating));
    });

    setKey((e) => {
      if (e.key === ' ') {
        e.preventDefault();
        toggleFlip();
      } else if (flipped) {
        if (e.key === '1') rateCurrent('Again');
        if (e.key === '2') rateCurrent('Hard');
        if (e.key === '3') rateCurrent('Good');
        if (e.key === '4') rateCurrent('Easy');
      }
    });
  };

  function bindFilterEvents() {
    body.querySelectorAll<HTMLElement>('[data-srs-filter]').forEach((b) => {
      b.addEventListener('click', () => {
        filter = b.dataset.srsFilter as QueueFilter;
        queue = filterQueue(cards, filter);
        idx = 0;
        flipped = false;
        sessionDone = false;
        render();
      });
    });
  }

  render();
  return () => {
    setKey(null);
    audioService.stop();
  };
}
