import { renderFocusShell } from '../components/AppShell';
import { renderBaoSvg } from '../components/BaoMascot';
import { iconSvg } from '../components/Icons';
import { closeWordPopover, showWordPopover } from '../components/WordPopover';
import { audioService } from '../services/audioPlayer';
import {
  loadStageReadings,
  loadStageWords,
  resolveStageForReadingId,
} from '../services/contentLoader';
import { requestPersistentStorage } from '../services/pwa';
import {
  addCardToSrs,
  ensureProgress,
  ensureSettings,
  getAllCards,
  isWeakCard,
  recordStudyActivity,
  setStoryBookmark,
} from '../services/srsEngine';
import { escapeHtml } from '../utils/html';

export async function renderReadingScreen(root: HTMLElement, readingId: string): Promise<() => void> {
  requestPersistentStorage();
  const stage = resolveStageForReadingId(readingId);
  const [readings, words, progress, settings, allCards] = await Promise.all([
    loadStageReadings(stage),
    loadStageWords(stage),
    ensureProgress(),
    ensureSettings(),
    getAllCards(),
  ]);

  const reading = readings.find((r) => r.id === readingId) ?? readings[0];
  if (!reading) {
    root.innerHTML = `<div style="padding:40px;text-align:center;"><h2>Chưa có bài đọc</h2><a href="#/" class="btn btn-read">Về bản đồ</a></div>`;
    return () => {};
  }

  const weakWords = new Set(allCards.filter(isWeakCard).map((c) => c.hanzi));
  const wordByHanzi = new Map(words.map((w) => [w.hanzi, w]));
  let pinyinMode: 'all' | 'new' | 'off' = settings.pinyinMode;
  let activeParagraph = -1;
  let playingKaraoke = false;
  let hintOpen = false;
  let hintDismissed = false;
  let awardedReadingXp = false;
  let keyHandler: ((e: KeyboardEvent) => void) | null = null;
  const selectedAnswers = new Map<string, number>();
  setStoryBookmark(reading.id, 1);

  audioService.preload([reading.audioFull, ...(reading.audioSentences ?? [])]);

  const shell = renderFocusShell({
    root,
    progressPct: 35,
    accentVar: 'var(--read)',
    wide: true,
    labelRight: `${reading.knownPercent}% từ đã biết`,
  });

  const setKey = (fn: ((e: KeyboardEvent) => void) | null) => {
    if (keyHandler) document.removeEventListener('keydown', keyHandler);
    keyHandler = fn;
    if (fn) document.addEventListener('keydown', fn);
  };

  const playKaraokeFrom = (idx: number) => {
    const list = reading.audioSentences ?? [];
    if (idx < 0 || idx >= list.length) {
      playingKaraoke = false;
      activeParagraph = -1;
      render();
      return;
    }
    playingKaraoke = true;
    activeParagraph = idx;
    render();
    audioService.play(list[idx], 1, () => {
      if (playingKaraoke) playKaraokeFrom(idx + 1);
    });
  };

  const render = () => {
    setKey(null);
    const answeredAll = selectedAnswers.size === reading.questions.length;
    const pct = Math.min(100, 35 + Math.round((selectedAnswers.size / Math.max(1, reading.questions.length)) * 65));
    shell.setProgress(pct, `${reading.knownPercent}% quen thuộc`);

    const stagePills = [1, 2, 3, 4]
      .map(
        (s) =>
          `<button type="button" class="btn btn-sm ${s === stage ? 'btn-read' : 'btn-soft'}" data-read-stage="${s}">Chặng ${s}</button>`
      )
      .join('');

    const selectOptions = readings
      .map(
        (r) =>
          `<option value="${escapeHtml(r.id)}" ${r.id === reading.id ? 'selected' : ''}>${
            r.isStoryChapter ? `★ ${r.title}` : r.title
          }</option>`
      )
      .join('');

    const nextChapterNum = (reading.chapterNumber ?? stage) + 1;

    shell.body.innerHTML = `
      <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:14px;">
        <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;">
          ${stagePills}
          <select data-read-select aria-label="Chọn bài đọc" style="padding:8px 12px;border-radius:14px;border:1.5px solid var(--border);background:var(--surface);font-weight:700;font-size:14px;">
            ${selectOptions}
          </select>
        </div>
        <div class="segmented" role="group" aria-label="Chế độ pinyin">
          <button type="button" data-py-mode="all" aria-pressed="${pinyinMode === 'all'}">Tất cả</button>
          <button type="button" data-py-mode="new" aria-pressed="${pinyinMode === 'new'}">Chỉ từ mới</button>
          <button type="button" data-py-mode="off" aria-pressed="${pinyinMode === 'off'}">Tắt</button>
        </div>
      </div>

      <div style="display:grid;grid-template-columns:minmax(0,760px) minmax(280px,360px);gap:24px;align-items:start;" class="reading-grid">
        <div>
          <article class="clay-card" style="padding:40px;background:var(--surface);">
            <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:16px;">
              <div>
                <div style="display:flex;gap:6px;flex-wrap:wrap;">
                  ${
                    reading.isStoryChapter
                      ? `<span class="chip" style="background:var(--review-soft);border-color:var(--review);">Truyện dài kỳ · Chương ${reading.chapterNumber ?? stage}/4</span>`
                      : ''
                  }
                  <span class="chip" style="background:var(--read-soft);border-color:var(--read);">
                    ${reading.mode === 'fluent' ? 'Đọc trôi (≥95% đã biết)' : 'Đọc học (~90% đã biết)'}
                  </span>
                </div>
                <h1 style="margin:8px 0 0;font-size:30px;line-height:1.25;">${escapeHtml(reading.title)}</h1>
              </div>
              <button type="button" class="btn ${playingKaraoke ? 'btn-comm' : 'btn-read'}" data-karaoke>
                ${iconSvg(playingKaraoke ? 'pause' : 'speaker', 18)} ${playingKaraoke ? 'Dừng nghe (Space)' : 'Nghe cả bài (Space)'}
              </button>
            </div>

            ${reading.paragraphs
              .map((p, pIdx) => {
                const isActive = pIdx === activeParagraph;
                return `
                  <p style="margin:0 0 22px;padding:12px 14px;border-radius:16px;background:${isActive ? 'var(--read-soft)' : 'transparent'};transition:background var(--t-fast) ease;font-family:var(--font-hanzi);font-size:max(20px, calc(21px * var(--hanzi-scale)));line-height:1.9;">
                    ${p.tokens
                      .map((tok) => {
                        if (!tok.pinyin) return `<span>${escapeHtml(tok.w)}</span>`;
                        const showPy = pinyinMode === 'all' || (pinyinMode === 'new' && tok.isNew);
                        const isWeak = weakWords.has(tok.w);
                        const bg = tok.isNew ? 'var(--reading-hl)' : 'transparent';
                        const borderBottom = isWeak ? '2px dotted var(--read-lip)' : 'none';
                        return `<button type="button" data-read-tok="${escapeHtml(tok.w)}" data-read-py="${escapeHtml(tok.pinyin)}" style="display:inline-flex;flex-direction:column;align-items:center;vertical-align:bottom;background:${bg};border:none;border-bottom:${borderBottom};border-radius:6px;padding:0 3px;margin:0 1px;font:inherit;line-height:1.35;">
                          ${showPy ? `<span class="pinyin" style="font-size:12px;line-height:1.1;">${escapeHtml(tok.pinyin)}</span>` : ''}
                          <span>${escapeHtml(tok.w)}</span>
                        </button>`;
                      })
                      .join('')}
                  </p>
                `;
              })
              .join('')}
          </article>

          <section class="clay-card" style="padding:24px;margin-top:20px;">
            <h2 style="margin:0 0 14px;">Câu hỏi đọc hiểu (${selectedAnswers.size}/${reading.questions.length})</h2>
            <div style="display:flex;flex-direction:column;gap:16px;">
              ${reading.questions
                .map((q, qi) => {
                  const chosen = selectedAnswers.get(q.id);
                  const isRight = chosen === q.answer;
                  return `
                    <div style="padding:16px;border-radius:16px;background:var(--bg);border:1.5px solid var(--border);">
                      <div style="font-weight:800;margin-bottom:10px;">Câu ${qi + 1}: ${escapeHtml(q.q)}</div>
                      <div style="display:flex;flex-wrap:wrap;gap:8px;">
                        ${q.options
                          .map((opt, oi) => {
                            let cls = 'btn-soft';
                            if (chosen !== undefined) {
                              if (oi === q.answer) cls = 'btn-read';
                              else if (oi === chosen) cls = 'btn-comm';
                            }
                            return `<button type="button" class="btn btn-sm ${cls}" data-q-id="${escapeHtml(q.id)}" data-q-opt="${oi}">[${oi + 1}] ${escapeHtml(opt)}</button>`;
                          })
                          .join('')}
                      </div>
                      ${
                        chosen !== undefined
                          ? `<div style="margin-top:10px;font-size:14px;color:${isRight ? 'var(--read-lip)' : 'var(--comm-lip)'};font-weight:700;">
                               ${isRight ? 'Đúng rồi!' : 'Chưa đúng — '} ${escapeHtml(q.explainVi)}
                             </div>`
                          : ''
                      }
                    </div>
                  `;
                })
                .join('')}
            </div>

            ${
              reading.isStoryChapter && reading.cliffhangerVi
                ? `<div style="margin-top:18px;padding:16px;border-radius:16px;background:var(--read-soft);border:1.5px solid var(--read);">
                     <div style="font-weight:800;margin-bottom:4px;">Gợi mở chương tiếp theo</div>
                     <p style="margin:0 0 10px;font-size:14px;color:var(--ink);">${escapeHtml(reading.cliffhangerVi)}</p>
                     ${
                       nextChapterNum <= 4
                         ? `<a href="#/reading/story-c${nextChapterNum}" class="btn btn-sm btn-read">Mở Chương ${nextChapterNum} →</a>`
                         : `<a href="#/" class="btn btn-sm btn-review">Xem lại toàn hành trình</a>`
                     }
                   </div>`
                : ''
            }

            ${
              answeredAll
                ? `<div style="margin-top:18px;display:flex;gap:10px;flex-wrap:wrap;align-items:center;">
                     <button type="button" class="btn btn-review" data-save-all-new>Lưu tất cả từ mới vào Ôn tập</button>
                     <a href="#/" class="btn btn-read">Về bản đồ</a>
                   </div>`
                : ''
            }
          </section>
        </div>

        <aside style="display:flex;flex-direction:column;gap:14px;position:sticky;top:16px;">
          <div class="clay-card" style="padding:20px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
              <h2 style="margin:0;font-size:18px;">Từ mới trong bài</h2>
              <span class="chip" style="background:var(--reading-hl);">${reading.newWords.length} từ</span>
            </div>
            <p style="margin:0 0 12px;font-size:13px;color:var(--ink-muted);">Bấm bất kỳ chữ nào trong bài để tra nghĩa & lưu vào Ôn tập.</p>
            <div style="display:flex;flex-direction:column;gap:8px;">
              ${reading.newWords
                .map((nw) => {
                  const w = wordByHanzi.get(nw);
                  return `
                    <div style="padding:10px 12px;border-radius:14px;background:var(--bg);border:1.5px solid var(--border);display:flex;justify-content:space-between;align-items:center;gap:8px;">
                      <div>
                        <span class="hanzi" style="font-size:20px;font-weight:700;">${escapeHtml(nw)}</span>
                        <span class="pinyin" style="margin-left:6px;">${escapeHtml(w?.pinyin ?? '')}</span>
                        <div style="font-size:13px;color:var(--ink-muted);">${escapeHtml(w?.meaningVi ?? '')}</div>
                      </div>
                      ${w?.audio ? `<button type="button" class="btn btn-sm btn-read" data-nw-play="${escapeHtml(w.audio)}">${iconSvg('speaker', 15)}</button>` : ''}
                    </div>
                  `;
                })
                .join('')}
            </div>
          </div>

          ${
            !hintDismissed
              ? `<div class="clay-card" style="padding:16px;display:flex;gap:10px;align-items:flex-start;">
                   ${renderBaoSvg({ mood: 'point', size: 52, accessory: progress.equippedAccessory })}
                   <div style="flex:1;">
                     <div style="font-weight:800;font-size:14px;">Gợi ý đọc của Bao</div>
                     <p style="margin:4px 0 8px;font-size:13px;color:var(--ink-muted);">
                       ${hintOpen ? 'Thử bấm P để chuyển pinyin sang "Chỉ từ mới" ở lượt đọc thứ hai để não tự nhận diện mặt chữ quen!' : 'Cần mẹo đọc nhanh không? Bấm xem gợi ý (tối đa 1 lần/bài).'}
                     </p>
                     <div style="display:flex;gap:6px;">
                       ${!hintOpen ? `<button type="button" class="btn btn-sm btn-read" data-show-hint>Xem gợi ý</button>` : ''}
                       <button type="button" class="btn btn-sm btn-soft" data-hide-hint>Tắt</button>
                     </div>
                   </div>
                 </div>`
              : ''
          }
        </aside>
      </div>
      <style>
        @media (max-width: 960px) {
          .reading-grid { grid-template-columns: 1fr !important; }
        }
      </style>
    `;

    shell.body.querySelectorAll<HTMLElement>('[data-read-stage]').forEach((b) => {
      b.addEventListener('click', async () => {
        const nextStage = Number(b.dataset.readStage);
        const list = await loadStageReadings(nextStage);
        if (list[0]) window.location.hash = `#/reading/${list[0].id}`;
      });
    });

    shell.body.querySelector<HTMLSelectElement>('[data-read-select]')?.addEventListener('change', (e) => {
      const targetId = (e.currentTarget as HTMLSelectElement).value;
      window.location.hash = `#/reading/${targetId}`;
    });

    shell.body.querySelectorAll<HTMLElement>('[data-py-mode]').forEach((b) => {
      b.addEventListener('click', () => {
        pinyinMode = b.dataset.pyMode as 'all' | 'new' | 'off';
        render();
      });
    });

    shell.body.querySelectorAll<HTMLElement>('[data-read-tok]').forEach((el) => {
      el.addEventListener('click', () => {
        showWordPopover({
          anchorEl: el,
          hanzi: el.dataset.readTok!,
          pinyinFallback: el.dataset.readPy,
          sourceTag: 'story',
        });
      });
    });

    shell.body.querySelectorAll<HTMLElement>('[data-nw-play]').forEach((b) => {
      b.addEventListener('click', () => audioService.play(b.dataset.nwPlay!));
    });

    const toggleKaraoke = () => {
      if (playingKaraoke) {
        playingKaraoke = false;
        activeParagraph = -1;
        audioService.stop();
        render();
      } else {
        playKaraokeFrom(Math.max(0, activeParagraph));
      }
    };
    shell.body.querySelector('[data-karaoke]')?.addEventListener('click', toggleKaraoke);

    const answerQuestion = (qid: string, opt: number) => {
      const q = reading.questions.find((x) => x.id === qid);
      selectedAnswers.set(qid, opt);
      if (q) audioService.playSfx(opt === q.answer ? 'ok' : 'err');
      if (selectedAnswers.size === reading.questions.length && !awardedReadingXp) {
        awardedReadingXp = true;
        recordStudyActivity({
          xpEarned: 25,
          skill: 'doc',
          completedLessonId: reading.isStoryChapter ? undefined : `t${reading.topicId}-doc`,
          completedStoryId: reading.isStoryChapter ? reading.id : undefined,
        });
      }
      render();
    };

    shell.body.querySelectorAll<HTMLElement>('[data-q-id]').forEach((b) => {
      b.addEventListener('click', () => answerQuestion(b.dataset.qId!, Number(b.dataset.qOpt)));
    });

    shell.body.querySelector('[data-save-all-new]')?.addEventListener('click', async (e) => {
      const btn = e.currentTarget as HTMLButtonElement;
      for (const nw of reading.newWords) {
        const w = wordByHanzi.get(nw);
        await addCardToSrs({
          itemId: w?.id ?? `read-${nw}`,
          facet: 'vocab',
          hanzi: nw,
          pinyin: w?.pinyin ?? '',
          meaningVi: w?.meaningVi ?? nw,
          example: w?.examples[0],
          audio: w?.audio,
          tags: ['story'],
        });
      }
      btn.textContent = `Đã lưu ${reading.newWords.length} từ mới`;
      btn.disabled = true;
      audioService.playSfx('ok');
    });

    shell.body.querySelector('[data-show-hint]')?.addEventListener('click', () => {
      hintOpen = true;
      render();
    });
    shell.body.querySelector('[data-hide-hint]')?.addEventListener('click', () => {
      hintDismissed = true;
      render();
    });

    setKey((e) => {
      const tag = document.activeElement?.tagName;
      if (tag === 'INPUT' || tag === 'SELECT' || tag === 'TEXTAREA') return;
      if (e.key === ' ') {
        e.preventDefault();
        toggleKaraoke();
      } else if (e.key === 'ArrowRight') {
        e.preventDefault();
        const nextIdx = activeParagraph < 0 ? 0 : Math.min(reading.paragraphs.length - 1, activeParagraph + 1);
        playKaraokeFrom(nextIdx);
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault();
        const prevIdx = Math.max(0, activeParagraph - 1);
        playKaraokeFrom(prevIdx);
      } else if (e.key === 'p' || e.key === 'P') {
        pinyinMode = pinyinMode === 'all' ? 'new' : pinyinMode === 'new' ? 'off' : 'all';
        render();
      } else if (e.key === 'Escape') {
        closeWordPopover();
      } else {
        const n = Number(e.key);
        if (n >= 1 && n <= 4) {
          const nextQ = reading.questions.find((q) => !selectedAnswers.has(q.id));
          if (nextQ && n <= nextQ.options.length) {
            answerQuestion(nextQ.id, n - 1);
          }
        }
      }
    });
  };

  render();
  return () => {
    setKey(null);
    playingKaraoke = false;
    closeWordPopover();
    audioService.stop();
  };
}
