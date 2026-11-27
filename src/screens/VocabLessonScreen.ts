import confetti from 'canvas-confetti';
import { renderFocusShell } from '../components/AppShell';
import { renderBaoSvg } from '../components/BaoMascot';
import { iconSvg } from '../components/Icons';
import { showWordPopover, closeWordPopover } from '../components/WordPopover';
import { audioService } from '../services/audioPlayer';
import { loadStageLessons, loadStageWords, resolveStageForLessonId } from '../services/contentLoader';
import { requestPersistentStorage } from '../services/pwa';
import { resolveWardrobe } from '../services/shopCatalog';
import {
  addCardToSrs,
  commitReview,
  ensureProgress,
  ensureSettings,
  filterQueue,
  getAllCards,
  getCoins,
  recordStudyActivity,
} from '../services/srsEngine';
import type { LessonItem, WordItem } from '../types/curriculum';
import { escapeHtml } from '../utils/html';

type StepItem =
  | { kind: 'intro' }
  | { kind: 'warmup' }
  | { kind: 'word'; word: WordItem; wordNum: number; totalWords: number }
  | { kind: 'grammar' }
  | { kind: 'pattern'; idx: number }
  | { kind: 'exercise'; idx: number }
  | { kind: 'roleplay'; idx: number }
  | { kind: 'summary' };

function colorizePinyin(py: string): string {
  return py
    .split(/(\s+)/)
    .map((tok) => {
      if (!tok.trim()) return tok;
      let cls = 'tone-5';
      if (/[āēīōūǖ]/.test(tok)) cls = 'tone-1';
      else if (/[áéíóúǘ]/.test(tok)) cls = 'tone-2';
      else if (/[ǎěǐǒǔǚ]/.test(tok)) cls = 'tone-3';
      else if (/[àèìòùǜ]/.test(tok)) cls = 'tone-4';
      return `<span class="${cls}">${escapeHtml(tok)}</span>`;
    })
    .join('');
}

export async function renderVocabLessonScreen(root: HTMLElement, lessonId: string): Promise<() => void> {
  requestPersistentStorage();
  const stage = resolveStageForLessonId(lessonId);
  const [lessons, words, allCards, progress, settings] = await Promise.all([
    loadStageLessons(stage),
    loadStageWords(stage),
    getAllCards(),
    ensureProgress(),
    ensureSettings(),
  ]);
  const lesson: LessonItem | undefined = lessons.find((l) => l.id === lessonId);
  if (!lesson) {
    root.innerHTML = `<div style="padding:40px;text-align:center;"><h2>Không tìm thấy bài học</h2><a href="#/" class="btn btn-comm">Về bản đồ</a></div>`;
    return () => {};
  }

  const wardrobe = resolveWardrobe(progress);
  const wordMap = new Map(words.map((w) => [w.id, w]));
  const lessonWords = lesson.newWords.map((id) => wordMap.get(id)).filter((w): w is WordItem => Boolean(w));
  const dueWarmup = filterQueue(allCards, 'due').slice(0, 3);

  const steps: StepItem[] = [];
  if (lesson.storyContextVi || lesson.bridgeFromPrevVi) {
    steps.push({ kind: 'intro' });
  }
  if (dueWarmup.length > 0) steps.push({ kind: 'warmup' });
  lessonWords.forEach((w, idx) => steps.push({ kind: 'word', word: w, wordNum: idx + 1, totalWords: lessonWords.length }));
  if (lesson.grammarSpotlight) {
    steps.push({ kind: 'grammar' });
  }
  for (let i = 0; i < (lesson.patterns?.length ?? 0); i++) steps.push({ kind: 'pattern', idx: i });
  for (let i = 0; i < (lesson.exercises?.length ?? 0); i++) steps.push({ kind: 'exercise', idx: i });
  for (let i = 0; i < (lesson.roleplay?.length ?? 0); i++) steps.push({ kind: 'roleplay', idx: i });
  steps.push({ kind: 'summary' });

  audioService.preload(
    lessonWords.flatMap((w) => [w.audio, ...w.examples.map((e) => e.audio)])
  );

  const shell = renderFocusShell({
    root,
    progressPct: 4,
    accentVar: 'var(--vocab)',
  });

  let stepIdx = 0;
  let showPinyin = settings.pinyinMode !== 'off';
  let keyHandler: ((e: KeyboardEvent) => void) | null = null;
  let earnedXp = 0;
  let combo = 0;
  let maxCombo = 0;
  let recordedSummary = false;

  const setKeyHandler = (fn: ((e: KeyboardEvent) => void) | null) => {
    if (keyHandler) document.removeEventListener('keydown', keyHandler);
    keyHandler = fn;
    if (fn) document.addEventListener('keydown', fn);
  };

  const isTyping = () => {
    const tag = document.activeElement?.tagName;
    return tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT';
  };

  const renderFeedback = (ok: boolean, message: string, onNext: () => void) => {
    if (ok) {
      combo += 1;
      maxCombo = Math.max(maxCombo, combo);
      earnedXp += 10;
      audioService.playSfx(combo >= 3 ? 'cheer' : 'ok');
    } else {
      combo = 0;
      audioService.playSfx('err');
    }

    const old = document.querySelector('.feedback-bar');
    old?.remove();
    const bar = document.createElement('div');
    bar.className = `feedback-bar ${ok ? 'is-ok' : 'is-err'}`;
    bar.innerHTML = `
      <div class="feedback-inner">
        <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;">
          <strong style="font-size:18px;">${ok ? (combo >= 3 ? `🔥 Combo ×${combo}! Quá đỉnh!` : '🎉 Chính xác!') : '💡 Gần đúng rồi — xem lại nhé'}</strong>
          <span>${escapeHtml(message)}</span>
          ${ok ? `<span class="xp-float">+10 XP</span>` : ''}
        </div>
        <button type="button" class="btn ${ok ? 'btn-read' : 'btn-comm'}" data-fb-next>Tiếp tục (Enter)</button>
      </div>
    `;
    document.body.appendChild(bar);
    const goNext = () => {
      bar.remove();
      onNext();
    };
    bar.querySelector('[data-fb-next]')?.addEventListener('click', goNext);
    setKeyHandler((e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        goNext();
      }
    });
  };

  const advance = () => {
    closeWordPopover();
    document.querySelector('.feedback-bar')?.remove();
    stepIdx += 1;
    renderStep();
  };

  const renderStep = () => {
    setKeyHandler(null);
    const cur = steps[stepIdx] ?? { kind: 'summary' };
    shell.setProgress((stepIdx / Math.max(1, steps.length - 1)) * 100, `${stepIdx + 1}/${steps.length}`);

    // STEP 0: COHESIVE INTRO & BRIDGE CARD
    if (cur.kind === 'intro') {
      const coinReward = lesson.coinReward ?? 40;
      shell.body.innerHTML = `
        <div class="clay-card milestone-banner" style="padding:28px;">
          <div style="display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:14px;">
            <span class="chip" style="background:var(--comm-soft);border-color:var(--comm);">📖 Chủ đề ${lesson.topicId} · Hành trình của Bao</span>
            <span class="chip coin-chip">🎋 Hoàn thành nhận +${coinReward} Xu Tre</span>
          </div>

          <div style="display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin-bottom:16px;">
            ${renderBaoSvg({ mood: 'wave', size: 108, wardrobe })}
            <div style="flex:1;min-width:240px;">
              <h1 style="margin:0 0 6px;font-size:26px;font-weight:800;">${escapeHtml(lesson.title)}</h1>
              ${lesson.storyContextVi ? `<p style="margin:0;font-size:15px;">${escapeHtml(lesson.storyContextVi)}</p>` : ''}
            </div>
          </div>

          ${
            lesson.bridgeFromPrevVi
              ? `<div style="padding:14px 16px;border-radius:16px;background:var(--read-soft);border:1.5px solid var(--read);margin-bottom:16px;font-size:14px;">
                   <strong>🔗 Liên kết bài học:</strong> ${escapeHtml(lesson.bridgeFromPrevVi)}
                 </div>`
              : ''
          }

          <div style="margin-bottom:18px;">
            <div style="font-weight:800;font-size:14px;color:var(--ink-muted);margin-bottom:8px;">✨ ${lessonWords.length} từ mới trọng tâm trong bài:</div>
            <div style="display:flex;flex-wrap:wrap;gap:8px;">
              ${lessonWords
                .map(
                  (w) => `<span class="chip" style="background:var(--bg);padding:6px 12px;">
                    <span class="hanzi" style="font-size:20px;font-weight:700;">${escapeHtml(w.hanzi)}</span>
                    <span style="font-size:12px;color:var(--ink-muted);">${escapeHtml(w.meaningVi)}</span>
                  </span>`
                )
                .join('')}
            </div>
          </div>

          <div style="display:flex;justify-content:flex-end;">
            <button type="button" class="btn btn-comm btn-lg" data-intro-go>Bắt đầu học ngay! (Enter) →</button>
          </div>
        </div>
      `;
      shell.body.querySelector('[data-intro-go]')?.addEventListener('click', () => {
        audioService.playSfx('pop');
        advance();
      });
      setKeyHandler((e) => {
        if (e.key === 'Enter') {
          e.preventDefault();
          advance();
        }
      });
      return;
    }

    // WARMUP SRS STEP
    if (cur.kind === 'warmup') {
      let wIdx = 0;
      const drawWarmup = () => {
        const card = dueWarmup[wIdx];
        if (!card) {
          advance();
          return;
        }
        shell.body.innerHTML = `
          <div class="clay-card" style="padding:28px;text-align:center;">
            <span class="chip" style="background:var(--vocab-soft);margin-bottom:12px;">🔁 Ôn nhanh thẻ cũ trước khi học mới (${wIdx + 1}/${dueWarmup.length})</span>
            <div class="hanzi-xl" style="margin:10px 0;">${escapeHtml(card.hanzi)}</div>
            <div class="pinyin" style="font-size:20px;">${colorizePinyin(card.pinyin)}</div>
            <div style="font-size:20px;font-weight:700;margin:8px 0 18px;">${escapeHtml(card.meaningVi)}</div>
            <div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;">
              ${card.audio ? `<button type="button" class="btn btn-vocab" data-wu-play>${iconSvg('speaker', 18)} Nghe (Space)</button>` : ''}
              <button type="button" class="btn btn-read" data-wu-good>Đã nhớ tốt</button>
              <button type="button" class="btn btn-soft" data-wu-again>Ôn lại sau</button>
            </div>
          </div>
        `;
        shell.body.querySelector('[data-wu-play]')?.addEventListener('click', () => card.audio && audioService.play(card.audio));
        const markWarmup = async (rating: 'Good' | 'Again') => {
          await commitReview(card, rating);
          wIdx += 1;
          drawWarmup();
        };
        shell.body.querySelector('[data-wu-good]')?.addEventListener('click', () => markWarmup('Good'));
        shell.body.querySelector('[data-wu-again]')?.addEventListener('click', () => markWarmup('Again'));
        setKeyHandler((e) => {
          if (e.key === ' ' && card.audio) {
            e.preventDefault();
            audioService.play(card.audio);
          } else if (e.key === '1' || e.key === 'Enter') {
            markWarmup('Good');
          } else if (e.key === '2') {
            markWarmup('Again');
          }
        });
      };
      drawWarmup();
      return;
    }

    // RICH WORD CARD STEP
    if (cur.kind === 'word') {
      const w = cur.word;
      shell.body.innerHTML = `
        <div class="clay-card" style="padding:26px;position:relative;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;gap:8px;flex-wrap:wrap;">
            <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;">
              <span class="chip" style="background:var(--vocab-soft);border-color:var(--vocab);">Từ mới ${cur.wordNum}/${cur.totalWords}</span>
              ${w.partOfSpeech ? `<span class="chip" style="background:var(--bg);font-size:12px;">${escapeHtml(w.partOfSpeech)}</span>` : ''}
              <span class="chip" style="background:var(--write-soft);border-color:var(--write);font-size:12px;">Bộ ${escapeHtml(w.radical || '—')}</span>
            </div>
            <button type="button" class="btn btn-sm btn-soft" data-toggle-py>[P] ${showPinyin ? 'Ẩn pinyin' : 'Hiện pinyin'}</button>
          </div>

          <div style="display:grid;grid-template-columns:1fr auto;gap:16px;align-items:center;">
            <div>
              <div class="hanzi-xl" style="font-weight:700;">${escapeHtml(w.hanzi)}</div>
              ${showPinyin ? `<div class="pinyin" style="font-size:21px;margin-top:4px;font-weight:700;">${colorizePinyin(w.pinyin)}</div>` : ''}
              <div style="font-size:23px;font-weight:800;margin-top:6px;">${escapeHtml(w.meaningVi)}</div>
              ${
                w.literalVi
                  ? `<div style="margin-top:6px;font-size:13px;color:var(--ink-muted);">🧩 Chiết tự: <strong>${escapeHtml(w.literalVi)}</strong></div>`
                  : ''
              }
            </div>
            <div style="display:flex;flex-direction:column;align-items:center;gap:10px;">
              ${
                w.audio
                  ? `<button type="button" class="btn btn-vocab btn-pill" style="width:66px;height:66px;" data-play-word aria-label="Phát âm từ mới">${iconSvg('speaker', 26)}</button>`
                  : ''
              }
              <span style="font-size:11px;font-weight:700;color:var(--ink-muted);">Space để nghe</span>
            </div>
          </div>

          <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px;margin-top:16px;">
            ${
              w.mnemonic
                ? `<div style="padding:12px 14px;border-radius:16px;background:var(--review-soft);border:1.5px solid var(--review);font-size:13px;">
                     <strong>💡 Mẹo nhớ nhanh:</strong> ${escapeHtml(w.mnemonic)}
                   </div>`
                : ''
            }
            ${
              w.usageNoteVi
                ? `<div style="padding:12px 14px;border-radius:16px;background:var(--read-soft);border:1.5px solid var(--read);font-size:13px;">
                     <strong>🗣️ Lưu ý khi nói:</strong> ${escapeHtml(w.usageNoteVi)}
                   </div>`
                : ''
            }
          </div>

          ${
            w.examples.length > 0
              ? `<div style="margin-top:18px;display:flex;flex-direction:column;gap:10px;">
                   <div style="font-size:13px;font-weight:800;color:var(--ink-muted);">Ví dụ thực tế (chạm từng chữ để tra nhanh):</div>
                   ${w.examples
                     .slice(0, 2)
                     .map(
                       (ex, exIdx) => `
                     <div style="padding:14px 16px;border-radius:16px;background:var(--bg);border:1.5px solid var(--border);">
                       <div style="display:flex;align-items:center;justify-content:space-between;gap:10px;">
                         <div style="display:flex;flex-wrap:wrap;gap:2px;align-items:baseline;">
                           ${(ex.hanzi.match(/[\u4e00-\u9fff]|[A-Za-z0-9-]+|[^\u4e00-\u9fffA-Za-z0-9-]+/g) ?? [])
                             .map((seg) => {
                               if (!/^[\u4e00-\u9fff]$/.test(seg)) {
                                 return `<span style="font-family:var(--font-ui);font-size:20px;font-weight:700;padding:0 1px;">${escapeHtml(seg)}</span>`;
                               }
                               const isTarget = w.hanzi.includes(seg);
                               return `<button type="button" data-pop-char="${escapeHtml(seg)}" style="background:${
                                 isTarget ? 'var(--reading-hl)' : 'transparent'
                               };border:none;padding:2px 3px;border-radius:6px;font-family:var(--font-hanzi);font-size:22px;font-weight:600;">${escapeHtml(seg)}</button>`;
                             })
                             .join('')}
                         </div>
                         ${ex.audio ? `<button type="button" class="btn btn-sm btn-vocab" data-play-ex="${exIdx}">${iconSvg('speaker', 16)}</button>` : ''}
                       </div>
                       ${showPinyin ? `<div class="pinyin" style="font-size:15px;margin-top:4px;">${colorizePinyin(ex.pinyin)}</div>` : ''}
                       <div style="font-size:14px;color:var(--ink-muted);margin-top:3px;">${escapeHtml(ex.vi)}</div>
                     </div>`
                     )
                     .join('')}
                 </div>`
              : ''
          }

          <div style="display:flex;justify-content:flex-end;margin-top:20px;">
            <button type="button" class="btn btn-vocab btn-lg" data-word-next>Đã nhớ, tiếp tục (Enter) →</button>
          </div>
        </div>
      `;

      const playWord = () => {
        const btn = shell.body.querySelector('[data-play-word]') as HTMLElement | null;
        if (!w.audio || !btn) return;
        btn.classList.add('is-speaking');
        audioService.play(w.audio, 1, () => btn.classList.remove('is-speaking'));
      };
      shell.body.querySelector('[data-play-word]')?.addEventListener('click', playWord);
      shell.body.querySelectorAll<HTMLElement>('[data-play-ex]').forEach((b) => {
        b.addEventListener('click', () => {
          const ex = w.examples[Number(b.dataset.playEx)];
          if (ex?.audio) audioService.play(ex.audio);
        });
      });
      shell.body.querySelector('[data-toggle-py]')?.addEventListener('click', () => {
        showPinyin = !showPinyin;
        renderStep();
      });
      shell.body.querySelectorAll<HTMLElement>('[data-pop-char]').forEach((el) => {
        el.addEventListener('click', () => {
          showWordPopover({ anchorEl: el, hanzi: el.dataset.popChar! });
        });
      });
      shell.body.querySelector('[data-word-next]')?.addEventListener('click', () => {
        audioService.playSfx('pop');
        advance();
      });
      setKeyHandler((e) => {
        if (isTyping()) return;
        if (e.key === ' ') {
          e.preventDefault();
          playWord();
        } else if (e.key === 'Enter') {
          e.preventDefault();
          advance();
        } else if (e.key === 'p' || e.key === 'P') {
          showPinyin = !showPinyin;
          renderStep();
        }
      });
      return;
    }

    // GRAMMAR SPOTLIGHT STEP
    if (cur.kind === 'grammar' && lesson.grammarSpotlight) {
      const g = lesson.grammarSpotlight;
      shell.body.innerHTML = `
        <div class="clay-card milestone-banner" style="padding:28px;">
          <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:12px;">
            <span class="chip" style="background:var(--review-soft);border-color:var(--review);">📘 Ngữ pháp trọng tâm bài này</span>
            ${renderBaoSvg({ mood: 'point', size: 62, wardrobe })}
          </div>
          <h2 style="margin:0 0 10px;font-size:23px;">${escapeHtml(g.title)}</h2>
          <div style="padding:14px 18px;border-radius:16px;background:var(--vocab-soft);border:2px solid var(--vocab);font-size:18px;font-weight:800;margin-bottom:14px;text-align:center;">
            ${escapeHtml(g.formula)}
          </div>
          <p style="margin:0 0 12px;font-size:15px;">${escapeHtml(g.explainVi)}</p>

          <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px;margin-bottom:16px;">
            ${
              g.vsVietnameseVi
                ? `<div style="padding:12px 14px;border-radius:14px;background:var(--read-soft);border:1.5px solid var(--read);font-size:13px;">
                     <strong>🇻🇳 So với tiếng Việt:</strong> ${escapeHtml(g.vsVietnameseVi)}
                   </div>`
                : ''
            }
            ${
              g.commonMistakeVi
                ? `<div style="padding:12px 14px;border-radius:14px;background:var(--comm-soft);border:1.5px solid var(--comm);font-size:13px;">
                     <strong>⚠️ Tránh nhầm:</strong> ${escapeHtml(g.commonMistakeVi)}
                   </div>`
                : ''
            }
          </div>

          <div style="display:flex;flex-direction:column;gap:10px;margin-bottom:20px;">
            ${g.examples
              .map(
                (ex, i) => `<div style="padding:12px 16px;border-radius:16px;background:var(--bg);border:1.5px solid var(--border);display:flex;align-items:center;justify-content:space-between;gap:10px;">
                  <div>
                    <div class="hanzi" style="font-size:22px;font-weight:600;">${escapeHtml(ex.hanzi)}</div>
                    <div class="pinyin">${colorizePinyin(ex.pinyin)}</div>
                    <div style="font-size:14px;color:var(--ink-muted);">${escapeHtml(ex.vi)}</div>
                  </div>
                  ${ex.audio ? `<button type="button" class="btn btn-sm btn-vocab" data-g-play="${i}">${iconSvg('speaker', 16)}</button>` : ''}
                </div>`
              )
              .join('')}
          </div>

          <div style="display:flex;justify-content:flex-end;">
            <button type="button" class="btn btn-comm btn-lg" data-gram-next>Hiểu rõ rồi, luyện tập ngay! (Enter) →</button>
          </div>
        </div>
      `;
      shell.body.querySelectorAll<HTMLElement>('[data-g-play]').forEach((b) => {
        b.addEventListener('click', () => {
          const ex = g.examples[Number(b.dataset.gPlay)];
          if (ex?.audio) audioService.play(ex.audio);
        });
      });
      shell.body.querySelector('[data-gram-next]')?.addEventListener('click', () => {
        audioService.playSfx('pop');
        advance();
      });
      setKeyHandler((e) => {
        if (e.key === 'Enter') {
          e.preventDefault();
          advance();
        }
      });
      return;
    }

    // PATTERN PRACTICE STEP
    if (cur.kind === 'pattern') {
      const pat = lesson.patterns![cur.idx];
      shell.body.innerHTML = `
        <div class="clay-card" style="padding:28px;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
            <span class="chip" style="background:var(--vocab-soft);">🧩 Mẫu câu khung ${cur.idx + 1}/${lesson.patterns!.length}</span>
            ${combo >= 2 ? `<span class="chip" style="background:var(--write-soft);border-color:var(--write);">🔥 Combo ×${combo}</span>` : ''}
          </div>
          <div class="hanzi-lg" style="margin:6px 0;">${escapeHtml(pat.frame)}</div>
          <div class="pinyin" style="font-size:18px;">${colorizePinyin(pat.pinyin)}</div>
          <div style="font-weight:700;margin:8px 0 18px;">${escapeHtml(pat.meaningVi)}</div>

          <div style="padding:14px;border-radius:16px;background:var(--bg);border:1.5px solid var(--border);margin-bottom:18px;display:flex;justify-content:space-between;align-items:center;gap:12px;">
            <div>
              <div class="hanzi" style="font-size:22px;font-weight:600;">${escapeHtml(pat.exampleHanzi)}</div>
              <div class="pinyin">${colorizePinyin(pat.examplePinyin)}</div>
              <div style="font-size:14px;color:var(--ink-muted);">${escapeHtml(pat.exampleVi)}</div>
            </div>
            ${pat.audio ? `<button type="button" class="btn btn-sm btn-vocab" data-pat-play>${iconSvg('speaker', 16)}</button>` : ''}
          </div>

          <div style="font-weight:800;margin-bottom:10px;">${escapeHtml(pat.slots.promptVi)}</div>
          <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;">
            ${pat.slots.choices
              .map(
                (ch, i) => `
              <button type="button" class="btn btn-soft" data-pat-choice="${escapeHtml(ch.hanzi)}" style="flex-direction:column;padding:14px;">
                <span class="hanzi" style="font-size:24px;">${escapeHtml(ch.hanzi)}</span>
                <span class="pinyin">${colorizePinyin(ch.pinyin)}</span>
                <span style="font-size:13px;color:var(--ink-muted);">[${i + 1}] ${escapeHtml(ch.vi)}</span>
              </button>`
              )
              .join('')}
          </div>
        </div>
      `;
      shell.body.querySelector('[data-pat-play]')?.addEventListener('click', () => pat.audio && audioService.play(pat.audio));
      const pick = (val: string) => {
        const ok = val === pat.slots.answerHanzi;
        renderFeedback(ok, `Đáp án đúng: ${pat.slots.answerHanzi}`, advance);
      };
      shell.body.querySelectorAll<HTMLElement>('[data-pat-choice]').forEach((b) => {
        b.addEventListener('click', () => pick(b.dataset.patChoice!));
      });
      setKeyHandler((e) => {
        const n = Number(e.key);
        if (n >= 1 && n <= pat.slots.choices.length) {
          pick(pat.slots.choices[n - 1].hanzi);
        }
      });
      return;
    }

    // EXERCISES STEP (including NEW match-pairs mini-game & fill-blank!)
    if (cur.kind === 'exercise') {
      const ex = lesson.exercises![cur.idx];

      // NEW FUN MINI-GAME: MATCH PAIRS
      if (ex.kind === 'match-pairs' && ex.pairs?.length) {
        const leftList = [...ex.pairs];
        const rightList = [...ex.pairs].sort((a, b) => a.vi.localeCompare(b.vi));
        const matched = new Set<string>();
        let selLeft: string | null = null;
        let selRight: string | null = null;
        let errNotice = '';

        const drawMatch = () => {
          shell.body.innerHTML = `
            <div class="clay-card" style="padding:26px;">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                <span class="chip" style="background:var(--review-soft);border-color:var(--review);">🎮 Mini-game Ghép cặp (${matched.size}/${ex.pairs!.length})</span>
                ${combo >= 2 ? `<span class="chip" style="background:var(--write-soft);border-color:var(--write);">🔥 Combo ×${combo}</span>` : ''}
              </div>
              <h2 style="margin:0 0 14px;">${escapeHtml(ex.promptVi)}</h2>
              ${errNotice ? `<div style="margin-bottom:10px;color:var(--comm-lip);font-weight:800;font-size:14px;">${escapeHtml(errNotice)}</div>` : ''}
              <div class="match-grid">
                <div style="display:flex;flex-direction:column;gap:10px;">
                  ${leftList
                    .map((p) => {
                      const isDone = matched.has(p.hanzi);
                      const isSel = selLeft === p.hanzi;
                      return `<button type="button" class="btn btn-soft match-tile ${isSel ? 'is-selected' : ''} ${isDone ? 'is-matched' : ''}" data-ml="${escapeHtml(p.hanzi)}" style="flex-direction:column;">
                        <span class="hanzi" style="font-size:24px;font-weight:700;">${escapeHtml(p.hanzi)}</span>
                        <span class="pinyin" style="font-size:13px;">${colorizePinyin(p.pinyin)}</span>
                      </button>`;
                    })
                    .join('')}
                </div>
                <div style="display:flex;flex-direction:column;gap:10px;">
                  ${rightList
                    .map((p) => {
                      const isDone = matched.has(p.hanzi);
                      const isSel = selRight === p.hanzi;
                      return `<button type="button" class="btn btn-soft match-tile ${isSel ? 'is-selected' : ''} ${isDone ? 'is-matched' : ''}" data-mr="${escapeHtml(p.hanzi)}">
                        <span style="font-size:16px;font-weight:700;">${escapeHtml(p.vi)}</span>
                      </button>`;
                    })
                    .join('')}
                </div>
              </div>
            </div>
          `;

          const tryResolve = () => {
            if (!selLeft || !selRight) return;
            if (selLeft === selRight) {
              matched.add(selLeft);
              selLeft = null;
              selRight = null;
              errNotice = '';
              audioService.playSfx('ok');
              if (matched.size === ex.pairs!.length) {
                renderFeedback(true, 'Ghép chuẩn hết cả 4 cặp luôn!', advance);
              } else {
                drawMatch();
              }
            } else {
              audioService.playSfx('err');
              errNotice = 'Chưa khớp cặp này — thử ghép lại nhé!';
              selLeft = null;
              selRight = null;
              drawMatch();
            }
          };

          shell.body.querySelectorAll<HTMLElement>('[data-ml]').forEach((b) => {
            b.addEventListener('click', () => {
              selLeft = b.dataset.ml!;
              audioService.playSfx('pop');
              if (selRight) tryResolve();
              else drawMatch();
            });
          });
          shell.body.querySelectorAll<HTMLElement>('[data-mr]').forEach((b) => {
            b.addEventListener('click', () => {
              selRight = b.dataset.mr!;
              audioService.playSfx('pop');
              if (selLeft) tryResolve();
              else drawMatch();
            });
          });
        };
        drawMatch();
        return;
      }

      if (ex.kind === 'sentence-tiles') {
        const chosen: string[] = [];
        const pool = [...(ex.tiles ?? [])];
        const drawTiles = () => {
          shell.body.innerHTML = `
            <div class="clay-card" style="padding:28px;">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                <span class="chip" style="background:var(--vocab-soft);">🧱 Sắp xếp thẻ từ</span>
                ${combo >= 2 ? `<span class="chip" style="background:var(--write-soft);border-color:var(--write);">🔥 Combo ×${combo}</span>` : ''}
              </div>
              <h2 style="margin:0 0 16px;">${escapeHtml(ex.promptVi)}</h2>
              <div style="min-height:66px;padding:12px;border-radius:16px;background:var(--bg);border:2px dashed var(--border-path);display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px;align-items:center;">
                ${
                  chosen.length
                    ? chosen
                        .map(
                          (t, idx) => `<button type="button" class="btn btn-vocab btn-sm" data-rm-tile="${idx}"><span class="hanzi" style="font-size:20px;">${escapeHtml(t)}</span></button>`
                        )
                        .join('')
                    : `<span style="color:var(--ink-muted);">Chạm các thẻ bên dưới theo đúng thứ tự...</span>`
                }
              </div>
              <div style="display:flex;flex-wrap:wrap;gap:10px;margin-bottom:20px;">
                ${pool
                  .map(
                    (t, idx) => `<button type="button" class="btn btn-soft" data-add-tile="${idx}"><span class="hanzi" style="font-size:22px;">${escapeHtml(t)}</span></button>`
                  )
                  .join('')}
              </div>
              <button type="button" class="btn btn-comm" data-check-tiles ${chosen.length === 0 ? 'disabled' : ''}>Kiểm tra (Enter)</button>
            </div>
          `;
          shell.body.querySelectorAll<HTMLElement>('[data-add-tile]').forEach((b) => {
            b.addEventListener('click', () => {
              const i = Number(b.dataset.addTile);
              const [picked] = pool.splice(i, 1);
              if (picked) chosen.push(picked);
              audioService.playSfx('pop');
              drawTiles();
            });
          });
          shell.body.querySelectorAll<HTMLElement>('[data-rm-tile]').forEach((b) => {
            b.addEventListener('click', () => {
              const i = Number(b.dataset.rmTile);
              const [removed] = chosen.splice(i, 1);
              if (removed) pool.push(removed);
              drawTiles();
            });
          });
          const check = () => {
            const joined = chosen.join('');
            const ok = joined === ex.answer;
            renderFeedback(ok, ex.explainVi ?? `Thứ tự đúng: ${ex.answer}`, advance);
          };
          shell.body.querySelector('[data-check-tiles]')?.addEventListener('click', check);
          setKeyHandler((e) => {
            if (isTyping()) return;
            if (e.key === 'Enter' && chosen.length > 0) {
              e.preventDefault();
              check();
            } else if (e.key === 'Backspace' && chosen.length > 0) {
              e.preventDefault();
              const removed = chosen.pop();
              if (removed) pool.push(removed);
              drawTiles();
            }
          });
        };
        drawTiles();
        return;
      }

      // choice exercise (meaning-choice / hanzi-choice / fill-blank)
      const isHanziOpt = ex.kind === 'hanzi-choice' || ex.kind === 'fill-blank';
      shell.body.innerHTML = `
        <div class="clay-card" style="padding:28px;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
            <span class="chip" style="background:var(--vocab-soft);">${ex.kind === 'fill-blank' ? '✍️ Điền vào chỗ trống' : '⚡ Luyện tập nhanh'}</span>
            ${combo >= 2 ? `<span class="chip" style="background:var(--write-soft);border-color:var(--write);">🔥 Combo ×${combo}</span>` : ''}
          </div>
          <h2 style="margin:0 0 14px;">${escapeHtml(ex.promptVi)}</h2>
          ${ex.hanziPrompt ? `<div class="hanzi-lg" style="margin-bottom:4px;">${escapeHtml(ex.hanziPrompt)}</div>` : ''}
          ${ex.pinyinPrompt ? `<div class="pinyin" style="font-size:18px;margin-bottom:14px;">${colorizePinyin(ex.pinyinPrompt)}</div>` : ''}
          ${ex.audio ? `<button type="button" class="btn btn-vocab" data-ex-play style="margin-bottom:16px;">${iconSvg('speaker', 18)} Nghe audio (Space)</button>` : ''}
          <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">
            ${(ex.options ?? [])
              .map(
                (o, i) => `<button type="button" class="btn btn-soft" data-ex-opt="${escapeHtml(o.value)}" style="justify-content:flex-start;padding:14px;text-align:left;">
                  <span class="chip" style="font-size:12px;">${i + 1}</span>
                  <span class="${isHanziOpt ? 'hanzi' : ''}" style="font-size:${isHanziOpt ? '22px' : '16px'};">${escapeHtml(o.label)}</span>
                </button>`
              )
              .join('')}
          </div>
        </div>
      `;
      shell.body.querySelector('[data-ex-play]')?.addEventListener('click', () => ex.audio && audioService.play(ex.audio));
      const choose = (val: string) => {
        const ok = val === ex.answer;
        renderFeedback(ok, ex.explainVi ?? `Đáp án đúng: ${ex.answer}`, advance);
      };
      shell.body.querySelectorAll<HTMLElement>('[data-ex-opt]').forEach((b) => {
        b.addEventListener('click', () => choose(b.dataset.exOpt!));
      });
      setKeyHandler((e) => {
        if (e.key === ' ' && ex.audio) {
          e.preventDefault();
          audioService.play(ex.audio);
        }
        const n = Number(e.key);
        if (ex.options && n >= 1 && n <= ex.options.length) {
          choose(ex.options[n - 1].value);
        }
      });
      return;
    }

    // ROLEPLAY STEP
    if (cur.kind === 'roleplay') {
      const rp = lesson.roleplay![cur.idx];
      shell.body.innerHTML = `
        <div class="clay-card" style="padding:28px;background:var(--comm-chat-bg);border-color:var(--comm);">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
            <span class="chip" style="background:var(--comm);">🎭 Thử thách đóng vai (${cur.idx + 1}/${lesson.roleplay!.length})</span>
            ${combo >= 2 ? `<span class="chip" style="background:var(--write-soft);border-color:var(--write);">🔥 Combo ×${combo}</span>` : ''}
          </div>
          <div style="padding:16px;border-radius:18px;background:var(--surface);border:1.5px solid var(--border);margin-bottom:16px;">
            <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;">
              <div>
                <div class="hanzi" style="font-size:22px;font-weight:600;">${escapeHtml(rp.npcHanzi)}</div>
                <div class="pinyin">${colorizePinyin(rp.npcPinyin)}</div>
                <div style="font-size:14px;color:var(--ink-muted);margin-top:4px;">${escapeHtml(rp.npcVi)}</div>
              </div>
              ${rp.npcAudio ? `<button type="button" class="btn btn-sm btn-comm" data-rp-play>${iconSvg('speaker', 16)}</button>` : ''}
            </div>
          </div>
          <div style="font-weight:800;margin-bottom:10px;">Nhiệm vụ của Bao: ${escapeHtml(rp.promptVi)}</div>
          <div style="display:flex;flex-direction:column;gap:10px;">
            ${rp.options
              .map(
                (o, i) => `<button type="button" class="btn btn-soft" data-rp-opt="${i}" style="justify-content:flex-start;text-align:left;padding:12px 16px;">
                  <span class="chip" style="font-size:12px;">${i + 1}</span>
                  <div>
                    <div class="hanzi" style="font-size:20px;">${escapeHtml(o.hanzi)}</div>
                    <div class="pinyin">${colorizePinyin(o.pinyin)} · ${escapeHtml(o.vi)}</div>
                  </div>
                </button>`
              )
              .join('')}
          </div>
        </div>
      `;
      shell.body.querySelector('[data-rp-play]')?.addEventListener('click', () => rp.npcAudio && audioService.play(rp.npcAudio));
      const pickRp = (idx: number) => {
        const opt = rp.options[idx];
        if (!opt) return;
        renderFeedback(opt.correct, `Câu tự nhiên nhất: ${rp.expectedHanzi}`, advance);
      };
      shell.body.querySelectorAll<HTMLElement>('[data-rp-opt]').forEach((b) => {
        b.addEventListener('click', () => pickRp(Number(b.dataset.rpOpt)));
      });
      setKeyHandler((e) => {
        const n = Number(e.key);
        if (n >= 1 && n <= rp.options.length) pickRp(n - 1);
      });
      return;
    }

    // SUMMARY STEP WITH XU TRE REWARD & STORY CONTINUITY!
    const totalXp = lesson.xp + earnedXp;
    const comboBonusCoins = maxCombo >= 4 ? 15 : maxCombo >= 2 ? 5 : 0;
    const totalCoins = (lesson.coinReward ?? 40) + comboBonusCoins;
    shell.setProgress(100, 'Hoàn thành');

    shell.body.innerHTML = `
      <div class="clay-card milestone-banner" style="padding:32px;text-align:center;">
        ${renderBaoSvg({ mood: 'celebrate', size: 132, wardrobe })}
        <h2 style="margin:8px 0 6px;font-size:28px;">🎉 Tuyệt vời! Xong bài ${escapeHtml(lesson.title)}</h2>
        <p style="color:var(--ink-muted);margin:0 0 18px;">
          ${lessonWords.length} từ mới đã tự động thêm vào hàng đợi Ôn tập Flashcard!
        </p>

        <div style="display:flex;justify-content:center;gap:12px;flex-wrap:wrap;margin-bottom:20px;">
          <div class="chip" style="padding:10px 18px;font-size:17px;background:var(--review-soft);border-color:var(--review);">
            ⭐ +${totalXp} XP
          </div>
          <div class="chip coin-chip" style="padding:10px 18px;font-size:17px;">
            🎋 +${totalCoins} Xu Tre ${comboBonusCoins > 0 ? `(gồm +${comboBonusCoins} thưởng Combo!)` : ''}
          </div>
          ${maxCombo >= 2 ? `<div class="chip" style="padding:10px 18px;font-size:16px;background:var(--write-soft);border-color:var(--write);">🔥 Kỷ lục Combo ×${maxCombo}</div>` : ''}
        </div>

        ${
          lesson.cultureTipVi
            ? `<div style="text-align:left;padding:14px 16px;border-radius:16px;background:var(--review-soft);border:1.5px solid var(--review);margin-bottom:14px;font-size:14px;">
                 <strong>🏮 Mẹo văn hóa từ Bao:</strong> ${escapeHtml(lesson.cultureTipVi)}
               </div>`
            : ''
        }

        ${
          lesson.bridgeToNextVi
            ? `<div style="text-align:left;padding:14px 16px;border-radius:16px;background:var(--read-soft);border:1.5px solid var(--read);margin-bottom:20px;font-size:14px;">
                 <strong>🗺️ Bước tiếp theo:</strong> ${escapeHtml(lesson.bridgeToNextVi)}
               </div>`
            : ''
        }

        <div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;">
          <a href="#/shop" class="btn btn-review">🛍️ Dùng Xu Tre sắm đồ cho Bao</a>
          <a href="#/reading/r-t${lesson.topicId}" class="btn btn-read">📖 Sang bài Đọc cùng chủ đề →</a>
          <a href="#/dialogue/${escapeHtml(lesson.id)}" class="btn btn-comm">💬 Luyện thêm Hội thoại</a>
          <a href="#/" class="btn btn-soft">Về bản đồ</a>
        </div>
        <div data-coin-balance-after style="margin-top:12px;font-size:13px;font-weight:700;color:var(--ink-muted);"></div>
      </div>
    `;

    if (!recordedSummary) {
      recordedSummary = true;
      (async () => {
        for (const w of lessonWords) {
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
        const updated = await recordStudyActivity({
          xpEarned: totalXp,
          coinsEarned: totalCoins,
          skill: 'giaoTiep',
          completedLessonId: lesson.id,
        });
        audioService.playSfx('coin');
        const balEl = shell.body.querySelector('[data-coin-balance-after]');
        if (balEl) balEl.textContent = `Ví hiện tại: 🎋 ${getCoins(updated)} Xu Tre`;
        if (!settings.reducedMotion) {
          confetti({ particleCount: 65, spread: 75, origin: { y: 0.65 } });
        }
      })();
    }
  };

  renderStep();
  return () => {
    setKeyHandler(null);
    closeWordPopover();
    document.querySelector('.feedback-bar')?.remove();
    audioService.stop();
  };
}
