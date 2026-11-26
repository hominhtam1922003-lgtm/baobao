import confetti from 'canvas-confetti';
import HanziWriter from 'hanzi-writer';
import { renderFocusShell } from '../components/AppShell';
import { renderBaoSvg } from '../components/BaoMascot';
import { iconSvg } from '../components/Icons';
import { audioService } from '../services/audioPlayer';
import { loadRadicals, loadStageLessons, loadStageWords } from '../services/contentLoader';
import { requestPersistentStorage } from '../services/pwa';
import { addCardToSrs, recordStudyActivity } from '../services/srsEngine';
import { escapeHtml } from '../utils/html';

const base = import.meta.env.BASE_URL;

type WriteLevel = 1 | 2 | 3;

export async function renderWritingScreen(root: HTMLElement, lessonId: string): Promise<() => void> {
  requestPersistentStorage();
  const [lessons, radicalsBundle, words] = await Promise.all([
    loadStageLessons(1),
    loadRadicals(),
    loadStageWords(1),
  ]);
  const writingLessons = lessons.filter((l) => l.type === 'viet');
  const lesson = writingLessons.find((l) => l.id === lessonId) ?? writingLessons[0];
  if (!lesson || !lesson.writingChars?.length) {
    root.innerHTML = `<div style="padding:40px;text-align:center;"><h2>Chưa có bài viết</h2><a href="#/" class="btn btn-write">Về bản đồ</a></div>`;
    return () => {};
  }

  const chars = lesson.writingChars;
  const shell = renderFocusShell({
    root,
    progressPct: 10,
    accentVar: 'var(--write)',
    wide: true,
  });

  let charIdx = 0;
  let level: WriteLevel = 1; // 1 = tô mờ, 2 = mẫu nhạt, 3 = viết từ trí nhớ
  let strokeProgress = 'Sẵn sàng viết nét đầu';
  let errorHint = '';
  let charDone = false;
  let quizMode = false;
  let quizResult: { ok: boolean; picked: string } | null = null;
  let finishedAll = false;
  let unmounted = false;
  let writer: HanziWriter | null = null;
  let modalEl: HTMLElement | null = null;

  const closeModal = () => {
    modalEl?.remove();
    modalEl = null;
  };

  const openRadicalModal = (rad: string, note: string) => {
    closeModal();
    const radInfo = radicalsBundle.radicals[rad];
    const siblings = radInfo?.chars ?? [];
    const backdrop = document.createElement('div');
    backdrop.className = 'modal-backdrop';
    backdrop.innerHTML = `
      <div class="modal-card" role="dialog" aria-label="Bộ thủ ${escapeHtml(rad)}">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
          <h2 style="margin:0;">Bộ thủ <span class="hanzi" style="font-size:28px;">${escapeHtml(rad)}</span></h2>
          <button type="button" class="btn btn-sm btn-soft" data-rad-close>${iconSvg('close', 16)}</button>
        </div>
        <p style="margin:0 0 12px;">${escapeHtml(note)}</p>
        ${radInfo?.meaning ? `<div style="font-size:14px;color:var(--ink-muted);margin-bottom:10px;">Nghĩa gốc: ${escapeHtml(radInfo.meaning)}</div>` : ''}
        <div style="font-weight:800;margin-bottom:8px;">Các chữ cùng bộ trong giáo trình:</div>
        <div style="display:flex;flex-wrap:wrap;gap:8px;">
          ${siblings.map((c) => `<span class="chip hanzi" style="font-size:22px;padding:6px 12px;background:var(--write-soft);">${escapeHtml(c)}</span>`).join('') || '<span style="color:var(--ink-muted);">Đang cập nhật</span>'}
        </div>
      </div>
    `;
    document.body.appendChild(backdrop);
    modalEl = backdrop;
    backdrop.addEventListener('click', (e) => {
      if (e.target === backdrop) closeModal();
    });
    backdrop.querySelector('[data-rad-close]')?.addEventListener('click', closeModal);
  };

  const mountWriter = (ch: string) => {
    const target = shell.body.querySelector<HTMLElement>('[data-hw-target]');
    if (!target) return;
    target.innerHTML = '';

    const canvasSize = Math.min(480, Math.max(280, window.innerWidth - 48));
    target.style.width = `${canvasSize}px`;
    target.style.height = `${canvasSize}px`;

    const showOutline = level === 1 || level === 2;
    const outlineColor = level === 1 ? '#D8D2CC' : '#EFE9E0';

    writer = HanziWriter.create(target, ch, {
      width: canvasSize,
      height: canvasSize,
      padding: 24,
      showOutline,
      outlineColor,
      strokeColor: '#3D3654',
      radicalColor: '#D97E06',
      highlightColor: '#FF9600',
      drawingColor: '#3D3654',
      drawingWidth: 16,
      showHintAfterMisses: 2,
      charDataLoader: async (char) => {
        const res = await fetch(`${base}strokes/${encodeURIComponent(char)}.json`);
        if (!res.ok) throw new Error(`Missing stroke data for ${char}`);
        return res.json();
      },
    });

    writer.quiz({
      onCorrectStroke(strokeData) {
        errorHint = '';
        audioService.playSfx('pop');
        const total = strokeData.strokeNum + 1 + strokeData.strokesRemaining;
        strokeProgress = `Nét ${strokeData.strokeNum + 1}/${total}`;
        const progEl = shell.body.querySelector('[data-stroke-progress]');
        if (progEl) progEl.textContent = strokeProgress;
        const errEl = shell.body.querySelector('[data-stroke-err]');
        if (errEl) errEl.textContent = '';
      },
      onMistake(strokeData) {
        audioService.playSfx('err');
        errorHint = `Chưa đúng thứ tự ở nét ${strokeData.strokeNum + 1} — nhìn Bao chỉ gợi ý nhé!`;
        const errEl = shell.body.querySelector('[data-stroke-err]');
        if (errEl) errEl.textContent = errorHint;
      },
      onComplete() {
        audioService.playSfx('ok');
        charDone = true;
        confetti({ particleCount: 28, spread: 50, colors: ['#FF9600', '#FFC531'], origin: { y: 0.7 } });
        render();
      },
    });
  };

  const render = () => {
    if (finishedAll) {
      shell.setProgress(100, 'Hoàn thành');
      shell.body.innerHTML = `
        <div class="clay-card" style="max-width:720px;margin:0 auto;padding:32px;text-align:center;">
          ${renderBaoSvg({ mood: 'celebrate', size: 108 })}
          <h2 style="margin:10px 0 6px;">Hoàn thành bài viết: ${escapeHtml(lesson.title)}</h2>
          <p style="margin:0 0 18px;color:var(--ink-muted);">+${lesson.xp} XP · Đã thêm ${chars.length} mặt thẻ viết vào Ôn tập.</p>
          <div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;">
            <a href="#/" class="btn btn-write">Về bản đồ</a>
            <a href="#/review" class="btn btn-review">Sang Ôn tập</a>
          </div>
        </div>
      `;
      return;
    }

    const cur = chars[charIdx];
    shell.setProgress(((charIdx + (quizMode ? 0.6 : 0.2)) / chars.length) * 100, `Chữ ${charIdx + 1}/${chars.length}`);

    const switcher = writingLessons
      .map(
        (l) => `<a href="#/writing/${escapeHtml(l.id)}" class="btn btn-sm ${l.id === lesson.id ? 'btn-write' : 'btn-soft'}">${escapeHtml(l.title)}</a>`
      )
      .join('');

    shell.body.innerHTML = `
      <div style="display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:14px;">
        <div style="display:flex;gap:8px;flex-wrap:wrap;">${switcher}</div>
        <div class="segmented" aria-label="Mức viết">
          <button type="button" data-w-lvl="1" aria-pressed="${level === 1}">1. Tô nét mờ</button>
          <button type="button" data-w-lvl="2" aria-pressed="${level === 2}">2. Mẫu nhạt</button>
          <button type="button" data-w-lvl="3" aria-pressed="${level === 3}">3. Tự nhớ</button>
        </div>
      </div>

      <div style="display:grid;grid-template-columns:minmax(0,500px) minmax(260px,360px);gap:24px;align-items:start;justify-content:center;" class="write-grid">
        <div>
          <div class="clay-card" style="padding:12px;border:2px solid var(--write);box-shadow:0 5px 0 var(--write-lip), var(--shadow-clay);display:flex;justify-content:center;align-items:center;position:relative;">
            <div style="position:relative;border-radius:18px;overflow:hidden;border:1.5px solid var(--border);background:linear-gradient(to right, transparent 49.5%, #F1E4D8 49.5%, #F1E4D8 50.5%, transparent 50.5%), linear-gradient(to bottom, transparent 49.5%, #F1E4D8 49.5%, #F1E4D8 50.5%, transparent 50.5%), linear-gradient(45deg, transparent 49.6%, #F6ECE2 49.6%, #F6ECE2 50.4%, transparent 50.4%), linear-gradient(-45deg, transparent 49.6%, #F6ECE2 49.6%, #F6ECE2 50.4%, transparent 50.4%), #FFFFFF;">
              <div data-hw-target></div>
            </div>
          </div>

          <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:12px;">
            <button type="button" class="btn btn-soft" data-animate-stroke>Xem nét</button>
            <button type="button" class="btn btn-soft" data-reset-stroke>Viết lại</button>
            ${
              charDone && !quizMode
                ? `<button type="button" class="btn btn-write" data-next-level>
                     ${level < 3 ? `Lên mức ${level + 1}` : 'Sang mini-quiz nhận diện →'}
                   </button>`
                : ''
            }
          </div>

          ${
            quizMode
              ? `<div class="clay-card" style="padding:20px;margin-top:16px;">
                   <h3 style="margin:0 0 8px;">Mini-quiz nhận diện: Đâu là chữ "${escapeHtml(cur.meaningVi)}" (${escapeHtml(cur.pinyin)})?</h3>
                   <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:12px;">
                     ${cur.lookalikes
                       .map((lk) => {
                         const isPicked = quizResult?.picked === lk.hanzi;
                         const cls = quizResult
                           ? lk.hanzi === cur.char
                             ? 'btn-read'
                             : isPicked
                             ? 'btn-comm'
                             : 'btn-soft'
                           : 'btn-soft';
                         return `<button type="button" class="btn ${cls}" data-lk-opt="${escapeHtml(lk.hanzi)}" style="padding:14px 8px;flex-direction:column;">
                           <span class="hanzi" style="font-size:28px;">${escapeHtml(lk.hanzi)}</span>
                         </button>`;
                       })
                       .join('')}
                   </div>
                   ${
                     quizResult
                       ? `<div style="margin-top:12px;display:flex;justify-content:space-between;align-items:center;gap:10px;">
                            <span style="font-weight:700;">${quizResult.ok ? 'Chuẩn xác!' : `Chữ đúng là ${cur.char} (${cur.meaningVi})`}</span>
                            <button type="button" class="btn btn-write" data-next-char>${charIdx + 1 < chars.length ? 'Chữ tiếp theo →' : 'Hoàn thành bài viết'}</button>
                          </div>`
                       : ''
                   }
                 </div>`
              : ''
          }
        </div>

        <aside class="clay-card" style="padding:22px;display:flex;flex-direction:column;gap:14px;">
          <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;">
            <div>
              <div class="hanzi-lg">${level === 3 && !charDone ? '？' : escapeHtml(cur.char)}</div>
              <div class="pinyin" style="font-size:18px;">${escapeHtml(cur.pinyin)}</div>
              <div style="font-size:18px;font-weight:800;margin-top:4px;">${escapeHtml(cur.meaningVi)}</div>
            </div>
            ${renderBaoSvg({ mood: errorHint ? 'point' : charDone ? 'celebrate' : 'happy', size: 68 })}
          </div>

          <div style="padding:12px;border-radius:14px;background:var(--write-soft);font-weight:700;font-size:14px;" data-stroke-progress>
            ${escapeHtml(strokeProgress)}
          </div>
          <div data-stroke-err style="font-size:14px;color:var(--comm-lip);font-weight:700;min-height:20px;">
            ${escapeHtml(errorHint)}
          </div>

          <div>
            <div style="font-size:13px;font-weight:800;color:var(--ink-muted);margin-bottom:6px;">Bộ thủ cấu thành (bấm để xem chi tiết):</div>
            <button type="button" class="btn btn-sm btn-soft" data-open-rad="${escapeHtml(cur.radical)}">
              <span class="hanzi" style="font-size:20px;">${escapeHtml(cur.radical)}</span> · Giải thích bộ thủ
            </button>
          </div>
        </aside>
      </div>
      <style>
        @media (max-width: 920px) {
          .write-grid { grid-template-columns: 1fr !important; }
        }
      </style>
    `;

    mountWriter(cur.char);

    shell.body.querySelectorAll<HTMLElement>('[data-w-lvl]').forEach((b) => {
      b.addEventListener('click', () => {
        level = Number(b.dataset.wLvl) as WriteLevel;
        charDone = false;
        strokeProgress = 'Sẵn sàng viết nét đầu';
        render();
      });
    });

    shell.body.querySelector('[data-animate-stroke]')?.addEventListener('click', () => {
      writer?.animateCharacter({
        onComplete: () => {
          if (!unmounted) mountWriter(cur.char);
        },
      });
    });

    shell.body.querySelector('[data-reset-stroke]')?.addEventListener('click', () => {
      charDone = false;
      errorHint = '';
      strokeProgress = 'Sẵn sàng viết nét đầu';
      render();
    });

    shell.body.querySelector('[data-next-level]')?.addEventListener('click', () => {
      if (level < 3) {
        level = (level + 1) as WriteLevel;
        charDone = false;
        strokeProgress = `Mức ${level}: viết lại chữ ${cur.char}`;
      } else {
        quizMode = true;
      }
      render();
    });

    shell.body.querySelectorAll<HTMLElement>('[data-open-rad]').forEach((b) => {
      b.addEventListener('click', () => openRadicalModal(b.dataset.openRad!, cur.radicalNoteVi));
    });

    shell.body.querySelectorAll<HTMLElement>('[data-lk-opt]').forEach((b) => {
      b.addEventListener('click', async () => {
        if (quizResult) return;
        const picked = b.dataset.lkOpt!;
        const ok = picked === cur.char;
        audioService.playSfx(ok ? 'ok' : 'err');
        quizResult = { ok, picked };
        const matchedWord = words.find((w) => w.hanzi === cur.char) ?? words.find((w) => w.hanzi.includes(cur.char));
        await addCardToSrs({
          itemId: `char-${cur.char}`,
          facet: 'writing',
          hanzi: cur.char,
          pinyin: cur.pinyin,
          meaningVi: cur.meaningVi,
          example: matchedWord?.examples[0],
          audio: matchedWord?.audio,
          isWeakWriting: !ok,
        });
        render();
      });
    });

    shell.body.querySelector('[data-next-char]')?.addEventListener('click', async () => {
      if (charIdx + 1 < chars.length) {
        charIdx += 1;
        level = 1;
        charDone = false;
        quizMode = false;
        quizResult = null;
        strokeProgress = 'Sẵn sàng viết nét đầu';
        render();
      } else {
        finishedAll = true;
        await recordStudyActivity({ xpEarned: lesson.xp, skill: 'viet', completedLessonId: lesson.id });
        render();
      }
    });
  };

  render();
  return () => {
    unmounted = true;
    writer?.cancelQuiz();
    closeModal();
    audioService.stop();
  };
}
