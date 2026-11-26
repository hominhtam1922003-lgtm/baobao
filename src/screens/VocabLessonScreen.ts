import confetti from 'canvas-confetti';
import { renderFocusShell } from '../components/AppShell';
import { renderBaoSvg } from '../components/BaoMascot';
import { iconSvg } from '../components/Icons';
import { showWordPopover, closeWordPopover } from '../components/WordPopover';
import { audioService } from '../services/audioPlayer';
import { loadStageLessons, loadStageWords } from '../services/contentLoader';
import { requestPersistentStorage } from '../services/pwa';
import {
  addCardToSrs,
  commitReview,
  filterQueue,
  getAllCards,
  recordStudyActivity,
} from '../services/srsEngine';
import type { LessonItem, WordItem } from '../types/curriculum';
import { escapeHtml } from '../utils/html';

type StepItem =
  | { kind: 'warmup' }
  | { kind: 'word'; word: WordItem }
  | { kind: 'pattern'; idx: number }
  | { kind: 'exercise'; idx: number }
  | { kind: 'roleplay'; idx: number }
  | { kind: 'summary' };

export async function renderVocabLessonScreen(root: HTMLElement, lessonId: string): Promise<() => void> {
  requestPersistentStorage();
  const [lessons, words, allCards] = await Promise.all([
    loadStageLessons(1),
    loadStageWords(1),
    getAllCards(),
  ]);
  const lesson: LessonItem | undefined = lessons.find((l) => l.id === lessonId);
  if (!lesson) {
    root.innerHTML = `<div style="padding:40px;text-align:center;"><h2>Không tìm thấy bài học</h2><a href="#/" class="btn btn-comm">Về bản đồ</a></div>`;
    return () => {};
  }

  const wordMap = new Map(words.map((w) => [w.id, w]));
  const lessonWords = lesson.newWords.map((id) => wordMap.get(id)).filter((w): w is WordItem => Boolean(w));
  const dueWarmup = filterQueue(allCards, 'due').slice(0, 4);

  const steps: StepItem[] = [];
  if (dueWarmup.length > 0) steps.push({ kind: 'warmup' });
  for (const w of lessonWords) steps.push({ kind: 'word', word: w });
  for (let i = 0; i < (lesson.patterns?.length ?? 0); i++) steps.push({ kind: 'pattern', idx: i });
  for (let i = 0; i < (lesson.exercises?.length ?? 0); i++) steps.push({ kind: 'exercise', idx: i });
  for (let i = 0; i < (lesson.roleplay?.length ?? 0); i++) steps.push({ kind: 'roleplay', idx: i });
  steps.push({ kind: 'summary' });

  audioService.preload(lessonWords.flatMap((w) => [w.audio, w.examples[0]?.audio]));

  const shell = renderFocusShell({
    root,
    progressPct: 4,
    accentVar: 'var(--vocab)',
  });

  let stepIdx = 0;
  let showPinyin = true;
  let keyHandler: ((e: KeyboardEvent) => void) | null = null;
  let earnedXp = 0;

  const setKeyHandler = (fn: ((e: KeyboardEvent) => void) | null) => {
    if (keyHandler) document.removeEventListener('keydown', keyHandler);
    keyHandler = fn;
    if (fn) document.addEventListener('keydown', fn);
  };

  const renderFeedback = (ok: boolean, message: string, onNext: () => void) => {
    audioService.playSfx(ok ? 'ok' : 'err');
    const old = document.querySelector('.feedback-bar');
    old?.remove();
    const bar = document.createElement('div');
    bar.className = `feedback-bar ${ok ? 'is-ok' : 'is-err'}`;
    bar.innerHTML = `
      <div class="feedback-inner">
        <div style="display:flex;align-items:center;gap:12px;">
          <strong style="font-size:18px;">${ok ? 'Chính xác!' : 'Gần đúng rồi — xem lại nhé'}</strong>
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
            <span class="chip" style="background:var(--vocab-soft);margin-bottom:12px;">Khởi động ôn thẻ đến hạn (${wIdx + 1}/${dueWarmup.length})</span>
            <div class="hanzi-xl" style="margin:10px 0;">${escapeHtml(card.hanzi)}</div>
            <div class="pinyin" style="font-size:20px;">${escapeHtml(card.pinyin)}</div>
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

    if (cur.kind === 'word') {
      const w = cur.word;
      const ex = w.examples[0];
      shell.body.innerHTML = `
        <div class="clay-card" style="padding:28px;position:relative;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;gap:8px;flex-wrap:wrap;">
            <span class="chip" style="background:var(--vocab-soft);">Từ mới · Bộ ${escapeHtml(w.radical || '—')}</span>
            <button type="button" class="btn btn-sm btn-soft" data-toggle-py>${showPinyin ? 'Ẩn pinyin' : 'Hiện pinyin'}</button>
          </div>

          <div style="display:grid;grid-template-columns:1fr auto;gap:16px;align-items:center;">
            <div>
              <div class="hanzi-xl">${escapeHtml(w.hanzi)}</div>
              ${showPinyin ? `<div class="pinyin" style="font-size:20px;margin-top:4px;">${escapeHtml(w.pinyin)}</div>` : ''}
              <div style="font-size:22px;font-weight:800;margin-top:8px;">${escapeHtml(w.meaningVi)}</div>
            </div>
            <div style="display:flex;flex-direction:column;align-items:center;gap:10px;">
              ${
                w.audio
                  ? `<button type="button" class="btn btn-vocab btn-pill" style="width:62px;height:62px;" data-play-word aria-label="Phát âm từ mới">${iconSvg('speaker', 24)}</button>`
                  : ''
              }
              ${
                w.mnemonic
                  ? `<div style="max-width:220px;padding:10px 12px;border-radius:14px;background:var(--review-soft);font-size:13px;">${escapeHtml(w.mnemonic)}</div>`
                  : ''
              }
            </div>
          </div>

          ${
            ex
              ? `<div style="margin-top:22px;padding:16px;border-radius:18px;background:var(--bg);border:1.5px solid var(--border);">
                   <div style="display:flex;align-items:center;justify-content:space-between;gap:10px;">
                     <div style="display:flex;flex-wrap:wrap;gap:6px;align-items:baseline;">
                       ${Array.from(ex.hanzi)
                         .map((ch) => {
                           const isTarget = w.hanzi.includes(ch);
                           return `<button type="button" data-pop-char="${escapeHtml(ch)}" style="background:${isTarget ? 'var(--reading-hl)' : 'transparent'};border:none;padding:2px 4px;border-radius:6px;font-family:var(--font-hanzi);font-size:22px;font-weight:600;">${escapeHtml(ch)}</button>`;
                         })
                         .join('')}
                     </div>
                     ${ex.audio ? `<button type="button" class="btn btn-sm btn-vocab" data-play-ex>${iconSvg('speaker', 16)}</button>` : ''}
                   </div>
                   ${showPinyin ? `<div class="pinyin" style="font-size:15px;margin-top:6px;">${escapeHtml(ex.pinyin)}</div>` : ''}
                   <div style="font-size:15px;color:var(--ink-muted);margin-top:4px;">${escapeHtml(ex.vi)}</div>
                 </div>`
              : ''
          }

          <div style="display:flex;justify-content:flex-end;margin-top:22px;">
            <button type="button" class="btn btn-vocab btn-lg" data-word-next>Đã hiểu, tiếp tục (Enter)</button>
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
      shell.body.querySelector('[data-play-ex]')?.addEventListener('click', () => ex?.audio && audioService.play(ex.audio));
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
        if (e.key === ' ') {
          e.preventDefault();
          playWord();
        } else if (e.key === 'Enter') {
          e.preventDefault();
          advance();
        }
      });
      return;
    }

    if (cur.kind === 'pattern') {
      const pat = lesson.patterns![cur.idx];
      shell.body.innerHTML = `
        <div class="clay-card" style="padding:28px;">
          <span class="chip" style="background:var(--vocab-soft);margin-bottom:12px;">Mẫu câu khung ${cur.idx + 1}/${lesson.patterns!.length}</span>
          <div class="hanzi-lg" style="margin:6px 0;">${escapeHtml(pat.frame)}</div>
          <div class="pinyin" style="font-size:18px;">${escapeHtml(pat.pinyin)}</div>
          <div style="font-weight:700;margin:8px 0 18px;">${escapeHtml(pat.meaningVi)}</div>

          <div style="padding:14px;border-radius:16px;background:var(--bg);border:1.5px solid var(--border);margin-bottom:18px;display:flex;justify-content:space-between;align-items:center;gap:12px;">
            <div>
              <div class="hanzi" style="font-size:22px;font-weight:600;">${escapeHtml(pat.exampleHanzi)}</div>
              <div class="pinyin">${escapeHtml(pat.examplePinyin)}</div>
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
                <span class="pinyin">${escapeHtml(ch.pinyin)}</span>
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
        if (ok) earnedXp += 10;
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

    if (cur.kind === 'exercise') {
      const ex = lesson.exercises![cur.idx];
      if (ex.kind === 'sentence-tiles') {
        const chosen: string[] = [];
        const pool = [...(ex.tiles ?? [])];
        const drawTiles = () => {
          shell.body.innerHTML = `
            <div class="clay-card" style="padding:28px;">
              <span class="chip" style="background:var(--vocab-soft);margin-bottom:12px;">Sắp xếp thẻ từ</span>
              <h2 style="margin:0 0 16px;">${escapeHtml(ex.promptVi)}</h2>
              <div style="min-height:64px;padding:12px;border-radius:16px;background:var(--bg);border:1.5px dashed var(--border-path);display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px;">
                ${
                  chosen.length
                    ? chosen
                        .map(
                          (t, idx) => `<button type="button" class="btn btn-vocab btn-sm" data-rm-tile="${idx}"><span class="hanzi" style="font-size:20px;">${escapeHtml(t)}</span></button>`
                        )
                        .join('')
                    : `<span style="color:var(--ink-muted);">Chạm thẻ bên dưới để ghép câu...</span>`
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
            if (ok) earnedXp += 10;
            renderFeedback(ok, ex.explainVi ?? `Thứ tự đúng: ${ex.answer}`, advance);
          };
          shell.body.querySelector('[data-check-tiles]')?.addEventListener('click', check);
          setKeyHandler((e) => {
            if (e.key === 'Enter' && chosen.length > 0) check();
          });
        };
        drawTiles();
        return;
      }

      // choice exercise (meaning-choice / hanzi-choice)
      shell.body.innerHTML = `
        <div class="clay-card" style="padding:28px;">
          <span class="chip" style="background:var(--vocab-soft);margin-bottom:12px;">Luyện tập nhanh</span>
          <h2 style="margin:0 0 14px;">${escapeHtml(ex.promptVi)}</h2>
          ${ex.hanziPrompt ? `<div class="hanzi-lg" style="margin-bottom:4px;">${escapeHtml(ex.hanziPrompt)}</div>` : ''}
          ${ex.pinyinPrompt ? `<div class="pinyin" style="font-size:18px;margin-bottom:14px;">${escapeHtml(ex.pinyinPrompt)}</div>` : ''}
          ${ex.audio ? `<button type="button" class="btn btn-vocab" data-ex-play style="margin-bottom:16px;">${iconSvg('speaker', 18)} Nghe audio (Space)</button>` : ''}
          <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">
            ${(ex.options ?? [])
              .map(
                (o, i) => `<button type="button" class="btn btn-soft" data-ex-opt="${escapeHtml(o.value)}" style="justify-content:flex-start;padding:14px;">
                  <span class="chip" style="font-size:12px;">${i + 1}</span>
                  <span class="${ex.kind === 'hanzi-choice' ? 'hanzi' : ''}" style="font-size:${ex.kind === 'hanzi-choice' ? '22px' : '16px'};">${escapeHtml(o.label)}</span>
                </button>`
              )
              .join('')}
          </div>
        </div>
      `;
      shell.body.querySelector('[data-ex-play]')?.addEventListener('click', () => ex.audio && audioService.play(ex.audio));
      const choose = (val: string) => {
        const ok = val === ex.answer;
        if (ok) earnedXp += 10;
        renderFeedback(ok, `Đáp án đúng: ${ex.answer}`, advance);
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

    if (cur.kind === 'roleplay') {
      const rp = lesson.roleplay![cur.idx];
      shell.body.innerHTML = `
        <div class="clay-card" style="padding:28px;background:var(--comm-chat-bg);border-color:var(--comm);">
          <span class="chip" style="background:var(--comm);margin-bottom:12px;">Thử thách đóng vai (${cur.idx + 1}/${lesson.roleplay!.length})</span>
          <div style="padding:16px;border-radius:18px;background:var(--surface);border:1.5px solid var(--border);margin-bottom:16px;">
            <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;">
              <div>
                <div class="hanzi" style="font-size:22px;font-weight:600;">${escapeHtml(rp.npcHanzi)}</div>
                <div class="pinyin">${escapeHtml(rp.npcPinyin)}</div>
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
                    <div class="pinyin">${escapeHtml(o.pinyin)} · ${escapeHtml(o.vi)}</div>
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
        if (opt.correct) earnedXp += 10;
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

    // Summary step
    const totalXp = lesson.xp + earnedXp;
    shell.setProgress(100, 'Hoàn thành');
    shell.body.innerHTML = `
      <div class="clay-card" style="padding:32px;text-align:center;">
        ${renderBaoSvg({ mood: 'celebrate', size: 112 })}
        <h2 style="margin:10px 0 6px;font-size:28px;">Tuyệt vời! Xong bài ${escapeHtml(lesson.title)}</h2>
        <p style="color:var(--ink-muted);margin:0 0 18px;">
          +${totalXp} XP · ${lessonWords.length} từ mới đã tự động vào hàng đợi Ôn tập.
        </p>
        <div style="display:flex;justify-content:center;gap:12px;flex-wrap:wrap;">
          <a href="#/dialogue/${escapeHtml(lesson.id)}" class="btn btn-comm">Luyện thêm Hội thoại</a>
          <a href="#/reading/r-t${lesson.topicId}" class="btn btn-read">Sang bài Đọc cùng chủ đề</a>
          <a href="#/" class="btn btn-soft">Về bản đồ</a>
        </div>
      </div>
    `;
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
      await recordStudyActivity({ xpEarned: totalXp, skill: 'giaoTiep', completedLessonId: lesson.id });
      confetti({ particleCount: 40, spread: 60, origin: { y: 0.7 } });
    })();
  };

  renderStep();
  return () => {
    setKeyHandler(null);
    closeWordPopover();
    document.querySelector('.feedback-bar')?.remove();
    audioService.stop();
  };
}
