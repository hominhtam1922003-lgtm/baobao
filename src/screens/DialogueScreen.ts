import confetti from 'canvas-confetti';
import { renderFocusShell } from '../components/AppShell';
import { renderBaoSvg } from '../components/BaoMascot';
import { iconSvg } from '../components/Icons';
import { audioService } from '../services/audioPlayer';
import { loadStageLessons } from '../services/contentLoader';
import { createShadowRecorder } from '../services/recorder';
import { addCardToSrs, recordStudyActivity } from '../services/srsEngine';
import { escapeHtml } from '../utils/html';

export async function renderDialogueScreen(root: HTMLElement, lessonId: string): Promise<() => void> {
  const lessons = await loadStageLessons(1);
  const lesson = lessons.find((l) => l.id === lessonId);
  if (!lesson || !lesson.dialogue?.length) {
    root.innerHTML = `<div style="padding:40px;text-align:center;"><h2>Không tìm thấy hội thoại</h2><a href="#/" class="btn btn-comm">Về bản đồ</a></div>`;
    return () => {};
  }

  const turns = lesson.dialogue;
  const goals = turns.filter((t) => t.goalLabel).map((t) => t.goalLabel!);
  audioService.preload(turns.map((t) => t.audio));

  const shell = renderFocusShell({
    root,
    progressPct: 10,
    accentVar: 'var(--comm)',
  });

  let revealedCount = 1;
  let completedGoals = new Set<string>();
  let openPinyinIdx = new Set<number>();
  let shadowUrls = new Map<number, string>();
  let shadowMode = false;
  let recordingIdx: number | null = null;
  let selfCorrectCount = 0;
  let activeTiles: string[] = [];
  let tilePool: string[] = [];
  let keyHandler: ((e: KeyboardEvent) => void) | null = null;
  const recorder = createShadowRecorder();

  const setKey = (fn: ((e: KeyboardEvent) => void) | null) => {
    if (keyHandler) document.removeEventListener('keydown', keyHandler);
    keyHandler = fn;
    if (fn) document.addEventListener('keydown', fn);
  };

  const advanceTurn = () => {
    while (revealedCount < turns.length) {
      const cur = turns[revealedCount - 1];
      if (cur.goalLabel) completedGoals.add(cur.goalLabel);
      const nextTurn = turns[revealedCount];
      revealedCount += 1;
      if (nextTurn.mode && nextTurn.mode !== 'npc') {
        activeTiles = [];
        tilePool = [...(nextTurn.tilePrompt ?? [])].reverse();
        break;
      }
      if (nextTurn.goalLabel) completedGoals.add(nextTurn.goalLabel);
    }
    if (revealedCount >= turns.length && turns[turns.length - 1].mode === 'npc') {
      const last = turns[turns.length - 1];
      if (last.goalLabel) completedGoals.add(last.goalLabel);
    }
    render();
  };

  const render = () => {
    setKey(null);
    const activeTurnIdx = Math.min(revealedCount - 1, turns.length - 1);
    const activeTurn = turns[activeTurnIdx];
    const awaitingInput =
      !shadowMode &&
      activeTurn.mode &&
      activeTurn.mode !== 'npc' &&
      !completedGoals.has(activeTurn.goalLabel ?? `__t${activeTurnIdx}`);

    const pct = shadowMode ? 95 : Math.min(92, Math.round((revealedCount / turns.length) * 90));
    shell.setProgress(pct, `${Math.min(revealedCount, turns.length)}/${turns.length}`);

    const visibleTurns = turns.slice(0, awaitingInput ? revealedCount - 1 : revealedCount);
    const isFinished = !awaitingInput && revealedCount >= turns.length;

    shell.body.innerHTML = `
      <div style="max-width:760px;margin:0 auto;">
        <div class="clay-card" style="padding:14px 18px;margin-bottom:14px;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;">
          <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;">
            <strong style="font-size:14px;">Mục tiêu hội thoại:</strong>
            ${goals
              .map((g) => {
                const done = completedGoals.has(g);
                return `<span class="chip" style="background:${done ? 'var(--read-soft)' : 'var(--bg)'};border-color:${done ? 'var(--read)' : 'var(--border)'};">
                  ${done ? iconSvg('check', 14) : '☐'} ${escapeHtml(g)}
                </span>`;
              })
              .join('')}
          </div>
          <button type="button" class="btn btn-sm ${shadowMode ? 'btn-comm' : 'btn-soft'}" data-toggle-shadow>
            ${iconSvg('mic', 15)} ${shadowMode ? 'Đang luyện đọc vai Bao' : 'Shadowing (thu âm)'}
          </button>
        </div>

        <div class="clay-card" style="padding:20px;background:var(--comm-chat-bg);border-color:var(--comm);display:flex;flex-direction:column;gap:14px;">
          ${visibleTurns
            .map((t, i) => {
              const isBao = t.speaker === 'Bao';
              const showPy = openPinyinIdx.has(i);
              const recUrl = shadowUrls.get(i);
              return `
                <div style="display:flex;gap:10px;align-items:flex-end;${isBao ? 'flex-direction:row-reverse;' : ''}">
                  <div style="flex:0 0 auto;">
                    ${
                      isBao
                        ? renderBaoSvg({ mood: 'happy', size: 42 })
                        : `<div style="width:42px;height:42px;border-radius:999px;background:var(--surface);border:2px solid var(--comm);display:flex;align-items:center;justify-content:center;font-weight:800;">${escapeHtml(t.speaker[0] ?? 'A')}</div>`
                    }
                  </div>
                  <div style="max-width:78%;background:var(--surface);border:1.5px solid var(--border);border-radius:18px;padding:12px 16px;box-shadow:var(--shadow-clay);">
                    <div style="font-size:12px;font-weight:800;color:var(--ink-muted);margin-bottom:4px;">${escapeHtml(t.speaker)}</div>
                    <div class="hanzi" style="font-size:22px;font-weight:600;">${escapeHtml(t.hanzi)}</div>
                    ${showPy ? `<div class="pinyin" style="font-size:14px;margin-top:4px;">${escapeHtml(t.pinyin)}</div>` : ''}
                    <div style="font-size:14px;color:var(--ink-muted);margin-top:4px;">${escapeHtml(t.vi)}</div>
                    <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:8px;">
                      ${t.audio ? `<button type="button" class="btn btn-sm btn-soft" data-turn-play="${i}">${iconSvg('speaker', 15)} Nghe</button>` : ''}
                      <button type="button" class="btn btn-sm btn-soft" data-turn-py="${i}">${showPy ? 'Ẩn pinyin' : 'Pinyin'}</button>
                      ${
                        shadowMode && isBao
                          ? `<button type="button" class="btn btn-sm ${recordingIdx === i ? 'btn-comm' : 'btn-vocab'}" data-rec-turn="${i}">
                               ${iconSvg('mic', 15)} ${recordingIdx === i ? 'Dừng thu' : 'Thu âm đọc theo'}
                             </button>
                             ${recUrl ? `<button type="button" class="btn btn-sm btn-read" data-play-rec="${i}">Nghe lại giọng mình</button>` : ''}`
                          : ''
                      }
                    </div>
                  </div>
                </div>
              `;
            })
            .join('')}

          ${
            awaitingInput
              ? `<div style="margin-top:8px;padding:16px;border-radius:18px;background:var(--surface);border:2px solid var(--comm);">
                   <div style="font-weight:800;margin-bottom:10px;">Lượt của Bao (${escapeHtml(activeTurn.goalLabel ?? 'Trả lời')}):</div>
                   ${
                     activeTurn.mode === 'choice'
                       ? `<div style="display:flex;flex-direction:column;gap:8px;">
                            ${(activeTurn.choices ?? [])
                              .map(
                                (c, idx) => `<button type="button" class="btn btn-soft" data-dlg-choice="${idx}" style="justify-content:flex-start;text-align:left;">
                                  <span class="chip" style="font-size:12px;">${idx + 1}</span>
                                  <span class="hanzi" style="font-size:20px;">${escapeHtml(c.hanzi)}</span>
                                  <span class="pinyin" style="margin-left:6px;">(${escapeHtml(c.vi)})</span>
                                </button>`
                              )
                              .join('')}
                          </div>`
                       : activeTurn.mode === 'tiles'
                       ? `<div>
                            <div style="font-size:14px;color:var(--ink-muted);margin-bottom:8px;">Ghép câu nghĩa là: "${escapeHtml(activeTurn.vi)}"</div>
                            <div style="min-height:52px;padding:10px;border-radius:14px;background:var(--bg);border:1.5px dashed var(--border-path);display:flex;flex-wrap:wrap;gap:8px;margin-bottom:10px;">
                              ${activeTiles.map((t, idx) => `<button type="button" class="btn btn-sm btn-comm" data-dlg-rm="${idx}"><span class="hanzi" style="font-size:20px;">${escapeHtml(t)}</span></button>`).join('')}
                            </div>
                            <div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px;">
                              ${tilePool.map((t, idx) => `<button type="button" class="btn btn-sm btn-soft" data-dlg-add="${idx}"><span class="hanzi" style="font-size:20px;">${escapeHtml(t)}</span></button>`).join('')}
                            </div>
                            <button type="button" class="btn btn-comm" data-dlg-tiles-check ${activeTiles.length === 0 ? 'disabled' : ''}>Gửi câu (Enter)</button>
                          </div>`
                       : `<div>
                            <div style="font-size:14px;color:var(--ink-muted);margin-bottom:8px;">Gõ pinyin không dấu/có dấu cho câu: "${escapeHtml(activeTurn.vi)}"</div>
                            <div style="display:flex;gap:8px;flex-wrap:wrap;">
                              <input type="text" data-dlg-pinyin-input placeholder="Ví dụ: zai jian" style="flex:1;min-width:180px;padding:10px 14px;border-radius:14px;border:1.5px solid var(--border);font-size:16px;" />
                              <button type="button" class="btn btn-comm" data-dlg-pinyin-check>Gửi (Enter)</button>
                              <button type="button" class="btn btn-soft" data-dlg-pinyin-hint>Gợi ý từ</button>
                            </div>
                          </div>`
                   }
                   <div data-dlg-err style="margin-top:8px;color:var(--comm-lip);font-weight:700;font-size:14px;"></div>
                 </div>`
              : ''
          }
        </div>

        ${
          isFinished
            ? `<div class="clay-card" style="padding:24px;margin-top:18px;text-align:center;">
                 ${renderBaoSvg({ mood: 'celebrate', size: 88 })}
                 <h2 style="margin:8px 0 4px;">Hoàn thành hội thoại!</h2>
                 <p style="margin:0 0 14px;color:var(--ink-muted);">Bạn tự hoàn thành ${selfCorrectCount} lượt phản hồi · Chế độ shadowing thu âm chỉ phát lại để bạn tự nghe, không chấm điểm.</p>
                 <div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;">
                   <button type="button" class="btn btn-review" data-save-sentences>Lưu câu hay vào Ôn tập</button>
                   <button type="button" class="btn btn-soft" data-replay-dlg>Chơi lại</button>
                   <a href="#/" class="btn btn-comm">Về bản đồ</a>
                 </div>
               </div>`
            : ''
        }
      </div>
    `;

    shell.body.querySelectorAll<HTMLElement>('[data-turn-play]').forEach((b) => {
      b.addEventListener('click', () => {
        const t = turns[Number(b.dataset.turnPlay)];
        if (t?.audio) audioService.play(t.audio);
      });
    });
    shell.body.querySelectorAll<HTMLElement>('[data-turn-py]').forEach((b) => {
      b.addEventListener('click', () => {
        const idx = Number(b.dataset.turnPy);
        if (openPinyinIdx.has(idx)) openPinyinIdx.delete(idx);
        else openPinyinIdx.add(idx);
        render();
      });
    });
    shell.body.querySelector('[data-toggle-shadow]')?.addEventListener('click', () => {
      shadowMode = !shadowMode;
      render();
    });
    shell.body.querySelectorAll<HTMLElement>('[data-rec-turn]').forEach((b) => {
      b.addEventListener('click', async () => {
        const idx = Number(b.dataset.recTurn);
        if (!recorder.supported) {
          alert('Trình duyệt hiện tại không hỗ trợ thu âm micro.');
          return;
        }
        if (recordingIdx === idx) {
          const url = await recorder.stop();
          recordingIdx = null;
          if (url) shadowUrls.set(idx, url);
          render();
        } else {
          const ok = await recorder.start();
          if (ok) {
            recordingIdx = idx;
            render();
          } else {
            alert('Không truy cập được micro để thu âm shadowing.');
          }
        }
      });
    });
    shell.body.querySelectorAll<HTMLElement>('[data-play-rec]').forEach((b) => {
      b.addEventListener('click', () => {
        const url = shadowUrls.get(Number(b.dataset.playRec));
        if (url) new Audio(url).play().catch(() => {});
      });
    });

    const showErr = (msg: string) => {
      audioService.playSfx('err');
      const el = shell.body.querySelector('[data-dlg-err]') as HTMLElement | null;
      if (el) el.textContent = msg;
    };

    const succeedTurn = (hard = false) => {
      audioService.playSfx('ok');
      selfCorrectCount += 1;
      if (activeTurn.goalLabel) completedGoals.add(activeTurn.goalLabel);
      if (hard) {
        confetti({ particleCount: 30, spread: 50, origin: { y: 0.72 } });
      }
      if (revealedCount >= turns.length) {
        recordStudyActivity({ xpEarned: 20, skill: 'giaoTiep' });
        render();
      } else {
        advanceTurn();
      }
    };

    if (awaitingInput) {
      if (activeTurn.mode === 'choice') {
        const pickChoice = (idx: number) => {
          const c = activeTurn.choices?.[idx];
          if (!c) return;
          if (c.correct) succeedTurn(false);
          else showErr('Chưa hợp ngữ cảnh lắm — thử câu khác nhé!');
        };
        shell.body.querySelectorAll<HTMLElement>('[data-dlg-choice]').forEach((b) => {
          b.addEventListener('click', () => pickChoice(Number(b.dataset.dlgChoice)));
        });
        setKey((e) => {
          const n = Number(e.key);
          if (n >= 1 && n <= (activeTurn.choices?.length ?? 0)) pickChoice(n - 1);
        });
      } else if (activeTurn.mode === 'tiles') {
        shell.body.querySelectorAll<HTMLElement>('[data-dlg-add]').forEach((b) => {
          b.addEventListener('click', () => {
            const [item] = tilePool.splice(Number(b.dataset.dlgAdd), 1);
            if (item) activeTiles.push(item);
            render();
          });
        });
        shell.body.querySelectorAll<HTMLElement>('[data-dlg-rm]').forEach((b) => {
          b.addEventListener('click', () => {
            const [item] = activeTiles.splice(Number(b.dataset.dlgRm), 1);
            if (item) tilePool.push(item);
            render();
          });
        });
        const checkTiles = () => {
          const expected = (activeTurn.tilePrompt ?? []).join('');
          if (activeTiles.join('') === expected) succeedTurn(true);
          else showErr(`Thử sắp xếp lại cho khớp: "${activeTurn.vi}"`);
        };
        shell.body.querySelector('[data-dlg-tiles-check]')?.addEventListener('click', checkTiles);
        setKey((e) => {
          if (e.key === 'Enter' && activeTiles.length > 0) checkTiles();
        });
      } else if (activeTurn.mode === 'pinyin') {
        const inp = shell.body.querySelector<HTMLInputElement>('[data-dlg-pinyin-input]');
        const checkPy = () => {
          const raw = (inp?.value ?? '').trim().toLowerCase().replace(/\s+/g, ' ');
          const normalized = raw.replace(/\s+/g, '');
          const accepted = (activeTurn.acceptedPinyin ?? []).map((x) => x.toLowerCase());
          if (accepted.some((a) => a === raw || a.replace(/\s+/g, '') === normalized)) {
            succeedTurn(true);
          } else {
            showErr(`Gợi ý pinyin: ${activeTurn.pinyin}`);
          }
        };
        shell.body.querySelector('[data-dlg-pinyin-check]')?.addEventListener('click', checkPy);
        shell.body.querySelector('[data-dlg-pinyin-hint]')?.addEventListener('click', () => {
          if (inp) inp.value = activeTurn.acceptedPinyin?.[0] ?? activeTurn.pinyin;
        });
        inp?.addEventListener('keydown', (e) => {
          if (e.key === 'Enter') checkPy();
        });
      }
    }

    shell.body.querySelector('[data-save-sentences]')?.addEventListener('click', async (e) => {
      const btn = e.currentTarget as HTMLButtonElement;
      for (const [idx, t] of turns.entries()) {
        if (t.speaker === 'Bao') {
          await addCardToSrs({
            itemId: `${lesson.id}-s${idx}`,
            facet: 'sentence',
            hanzi: t.hanzi,
            pinyin: t.pinyin,
            meaningVi: t.vi,
            example: { hanzi: t.hanzi, pinyin: t.pinyin, vi: t.vi, audio: t.audio },
            audio: t.audio,
          });
        }
      }
      btn.textContent = 'Đã lưu câu vào Ôn tập';
      btn.disabled = true;
      audioService.playSfx('ok');
    });

    shell.body.querySelector('[data-replay-dlg]')?.addEventListener('click', () => {
      revealedCount = 1;
      completedGoals = new Set();
      selfCorrectCount = 0;
      render();
    });
  };

  render();
  return () => {
    setKey(null);
    audioService.stop();
  };
}
