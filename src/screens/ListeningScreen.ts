import { renderFocusShell } from '../components/AppShell';
import { renderBaoSvg } from '../components/BaoMascot';
import { iconSvg } from '../components/Icons';
import { audioService } from '../services/audioPlayer';
import { loadStageLessons, resolveStageForLessonId } from '../services/contentLoader';
import { requestPersistentStorage } from '../services/pwa';
import { ensureProgress, ensureSettings, recordStudyActivity } from '../services/srsEngine';
import { escapeHtml } from '../utils/html';

export async function renderListeningScreen(root: HTMLElement, lessonId: string): Promise<() => void> {
  requestPersistentStorage();
  const stage = resolveStageForLessonId(lessonId);
  const [lessons, progress, settings] = await Promise.all([
    loadStageLessons(stage),
    ensureProgress(),
    ensureSettings(),
  ]);
  const listeningLessons = lessons.filter((l) => l.type === 'nghe');
  const lesson = listeningLessons.find((l) => l.id === lessonId) ?? listeningLessons[0];
  if (!lesson || !lesson.exercises?.length) {
    root.innerHTML = `<div style="padding:40px;text-align:center;"><h2>Chưa có bài nghe</h2><a href="#/" class="btn btn-listen">Về bản đồ</a></div>`;
    return () => {};
  }

  const exercises = lesson.exercises;
  audioService.preload(exercises.flatMap((ex) => [ex.audio, ex.audioSlow]));

  const shell = renderFocusShell({
    root,
    progressPct: 10,
    accentVar: 'var(--listen)',
  });

  let idx = 0;
  let speed: '0.75' | '1' | '1.25' = '1';
  let subtitleMode: 'all' | 'new' | 'off' = settings.pinyinMode;
  let isPlaying = false;
  let loopTrack = false;
  let chosenTiles: string[] = [];
  let tilePool: string[] = [...(exercises[0].tiles ?? [])];
  let feedback: { ok: boolean; msg: string } | null = null;
  let completed = false;
  let keyHandler: ((e: KeyboardEvent) => void) | null = null;

  const setKey = (fn: ((e: KeyboardEvent) => void) | null) => {
    if (keyHandler) document.removeEventListener('keydown', keyHandler);
    keyHandler = fn;
    if (fn) document.addEventListener('keydown', fn);
  };

  const playCurrent = (forceSlow = false) => {
    const ex = exercises[idx];
    if (!ex) return;
    const useSlow = forceSlow || speed === '0.75';
    const src = useSlow && ex.audioSlow ? ex.audioSlow : ex.audio;
    if (!src) return;
    const rate = !useSlow && speed === '1.25' ? 1.25 : 1;
    isPlaying = true;
    render();
    audioService.play(src, rate, () => {
      isPlaying = false;
      if (loopTrack && !feedback) {
        playCurrent(false);
      } else {
        render();
      }
    });
  };

  const goTo = (nextIdx: number) => {
    audioService.stop();
    isPlaying = false;
    feedback = null;
    if (nextIdx >= exercises.length) {
      completed = true;
      recordStudyActivity({ xpEarned: lesson.xp, skill: 'nghe', completedLessonId: lesson.id });
      render();
      return;
    }
    idx = Math.max(0, nextIdx);
    chosenTiles = [];
    tilePool = [...(exercises[idx].tiles ?? [])];
    render();
  };

  const checkAnswer = (userVal: string, expected: string) => {
    const norm = (s: string) => s.trim().toLowerCase().replace(/\s+/g, '');
    const ok = norm(userVal) === norm(expected);
    audioService.playSfx(ok ? 'ok' : 'err');
    if (!ok) {
      playCurrent(true);
    }
    feedback = {
      ok,
      msg: ok ? 'Nghe chuẩn lắm!' : `Đáp án đúng: ${expected} (đang phát lại bản chậm 0.75×)`,
    };
    render();
  };

  const render = () => {
    setKey(null);
    if (completed) {
      shell.setProgress(100, 'Hoàn thành');
      shell.body.innerHTML = `
        <div class="clay-card" style="max-width:760px;margin:0 auto;padding:32px;text-align:center;">
          ${renderBaoSvg({ mood: 'headphones', size: 108, accessory: progress.equippedAccessory })}
          <h2 style="margin:10px 0 6px;">Xong bài nghe: ${escapeHtml(lesson.title)}</h2>
          <p style="margin:0 0 18px;color:var(--ink-muted);">+${lesson.xp} XP · Đã cộng vào kỹ năng Nghe.</p>
          <div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;">
            <a href="#/" class="btn btn-listen">Về bản đồ</a>
            <button type="button" class="btn btn-soft" data-replay-listen>Nghe lại từ đầu</button>
          </div>
        </div>
      `;
      shell.body.querySelector('[data-replay-listen]')?.addEventListener('click', () => {
        completed = false;
        goTo(0);
      });
      return;
    }

    const ex = exercises[idx];
    shell.setProgress(((idx + 1) / exercises.length) * 95, `${idx + 1}/${exercises.length}`);

    const stagePills = [1, 2, 3, 4]
      .map(
        (s) =>
          `<button type="button" class="btn btn-sm ${s === stage ? 'btn-listen' : 'btn-soft'}" data-listen-stage="${s}">Chặng ${s}</button>`
      )
      .join('');

    const selectOptions = listeningLessons
      .map(
        (l) => `<option value="${escapeHtml(l.id)}" ${l.id === lesson.id ? 'selected' : ''}>${escapeHtml(l.title)}</option>`
      )
      .join('');

    shell.body.innerHTML = `
      <div style="max-width:760px;margin:0 auto;">
        <div style="display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:14px;">
          <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;">
            ${stagePills}
            <select data-listen-select aria-label="Chọn bài nghe" style="padding:8px 12px;border-radius:14px;border:1.5px solid var(--border);background:var(--surface);font-weight:700;font-size:14px;">
              ${selectOptions}
            </select>
          </div>
          <div class="segmented" aria-label="Phụ đề">
            <button type="button" data-sub="all" aria-pressed="${subtitleMode === 'all'}">Hiện chữ</button>
            <button type="button" data-sub="new" aria-pressed="${subtitleMode === 'new'}">Gợi ý</button>
            <button type="button" data-sub="off" aria-pressed="${subtitleMode === 'off'}">Ẩn</button>
          </div>
        </div>

        <div class="clay-card" style="padding:26px;text-align:center;margin-bottom:18px;">
          <div style="display:flex;flex-direction:column;align-items:center;gap:14px;">
            <button type="button" data-play-toggle aria-label="Phát hoặc dừng audio" style="width:180px;height:180px;border-radius:999px;border:5px solid #FFFFFF;background:var(--listen);box-shadow:0 6px 0 var(--listen-lip), var(--shadow-clay);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;position:relative;color:#FFFFFF;">
              ${renderBaoSvg({ mood: 'headphones', size: 84, accessory: progress.equippedAccessory })}
              <span style="display:inline-flex;align-items:center;gap:6px;background:var(--listen-lip);padding:4px 12px;border-radius:999px;font-weight:800;font-size:13px;">
                ${iconSvg(isPlaying ? 'pause' : 'play', 14)} ${isPlaying ? 'Đang phát' : 'Nghe (Space)'}
              </span>
            </button>

            <div style="display:flex;gap:4px;height:18px;align-items:flex-end;" aria-hidden="true">
              ${[10, 16, 12, 18, 14, 16, 10]
                .map((h) => `<span style="width:6px;height:${isPlaying ? h : 6}px;border-radius:999px;background:var(--listen);transition:height 160ms ease;"></span>`)
                .join('')}
            </div>

            <div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center;justify-content:center;">
              <div class="segmented" aria-label="Tốc độ phát">
                <button type="button" data-spd="0.75" aria-pressed="${speed === '0.75'}">0.75× (chậm thật)</button>
                <button type="button" data-spd="1" aria-pressed="${speed === '1'}">1×</button>
                <button type="button" data-spd="1.25" aria-pressed="${speed === '1.25'}">1.25×</button>
              </div>
              <button type="button" class="btn btn-sm ${loopTrack ? 'btn-listen' : 'btn-soft'}" data-loop-btn>${iconSvg('repeat', 15)} Lặp câu</button>
              <button type="button" class="btn btn-sm btn-soft" data-prev-ex ${idx === 0 ? 'disabled' : ''}>${iconSvg('arrow-left', 16)}</button>
              <button type="button" class="btn btn-sm btn-soft" data-next-ex ${idx >= exercises.length - 1 ? 'disabled' : ''}>${iconSvg('arrow-right', 16)}</button>
            </div>

            ${
              subtitleMode !== 'off' && ex.audioText
                ? `<div class="hanzi" style="font-size:22px;padding:8px 14px;border-radius:12px;background:var(--listen-soft);">${escapeHtml(subtitleMode === 'new' ? ex.audioText.slice(0, 2) + '…' : ex.audioText)}</div>`
                : ''
            }
          </div>
        </div>

        <div class="clay-card" style="padding:24px;">
          <h2 style="margin:0 0 14px;">${escapeHtml(ex.promptVi)}</h2>
          ${
            ex.kind === 'listen-tiles'
              ? `<div>
                   <div style="min-height:54px;padding:10px;border-radius:14px;background:var(--bg);border:1.5px dashed var(--border-path);display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px;">
                     ${chosenTiles.map((t, i) => `<button type="button" class="btn btn-sm btn-listen" data-lt-rm="${i}"><span class="hanzi" style="font-size:20px;">${escapeHtml(t)}</span></button>`).join('')}
                   </div>
                   <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px;">
                     ${tilePool.map((t, i) => `<button type="button" class="btn btn-sm btn-soft" data-lt-add="${i}"><span class="hanzi" style="font-size:20px;">${escapeHtml(t)}</span></button>`).join('')}
                   </div>
                   <button type="button" class="btn btn-listen" data-lt-check ${chosenTiles.length === 0 || feedback ? 'disabled' : ''}>Kiểm tra (Enter)</button>
                 </div>`
              : ex.kind === 'dictation'
              ? `<div>
                   <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px;">
                     <input type="text" data-dict-inp placeholder="Gõ pinyin (vd: nihao zaijian)" style="flex:1;min-width:200px;padding:10px 14px;border-radius:14px;border:1.5px solid var(--border);font-size:16px;" />
                     <button type="button" class="btn btn-listen" data-dict-check ${feedback ? 'disabled' : ''}>Chấm (Enter)</button>
                   </div>
                   <div style="display:flex;gap:8px;flex-wrap:wrap;">
                     ${(ex.tiles ?? []).map((t) => `<button type="button" class="btn btn-sm btn-soft" data-dict-chip="${escapeHtml(t)}"><span class="hanzi" style="font-size:20px;">${escapeHtml(t)}</span></button>`).join('')}
                   </div>
                 </div>`
              : `<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">
                   ${(ex.options ?? [])
                     .map(
                       (o, i) => `<button type="button" class="btn btn-soft" data-l-opt="${escapeHtml(o.value)}" ${feedback ? 'disabled' : ''} style="justify-content:flex-start;padding:12px 16px;">
                         <span class="chip" style="font-size:12px;">${i + 1}</span>
                         <span class="${ex.kind === 'listen-hanzi' || ex.kind === 'listen-blank' ? 'hanzi' : ''}" style="font-size:${ex.kind === 'listen-hanzi' || ex.kind === 'listen-blank' ? '22px' : '16px'};">${escapeHtml(o.label)}</span>
                       </button>`
                     )
                     .join('')}
                 </div>`
          }
        </div>
      </div>

      ${
        feedback
          ? `<div class="feedback-bar ${feedback.ok ? 'is-ok' : 'is-err'}">
               <div class="feedback-inner">
                 <div><strong>${feedback.ok ? 'Chính xác!' : 'Nghe chậm lại nhé'}</strong> ${escapeHtml(feedback.msg)}</div>
                 <button type="button" class="btn ${feedback.ok ? 'btn-read' : 'btn-listen'}" data-l-next>Tiếp tục (Enter)</button>
               </div>
             </div>`
          : ''
      }
    `;

    shell.body.querySelectorAll<HTMLElement>('[data-listen-stage]').forEach((b) => {
      b.addEventListener('click', async () => {
        const nextStage = Number(b.dataset.listenStage);
        const list = (await loadStageLessons(nextStage)).filter((l) => l.type === 'nghe');
        if (list[0]) window.location.hash = `#/listening/${list[0].id}`;
      });
    });

    shell.body.querySelector<HTMLSelectElement>('[data-listen-select]')?.addEventListener('change', (e) => {
      window.location.hash = `#/listening/${(e.currentTarget as HTMLSelectElement).value}`;
    });

    shell.body.querySelector('[data-play-toggle]')?.addEventListener('click', () => {
      if (isPlaying) {
        audioService.stop();
        isPlaying = false;
        render();
      } else {
        playCurrent(false);
      }
    });
    shell.body.querySelectorAll<HTMLElement>('[data-spd]').forEach((b) => {
      b.addEventListener('click', () => {
        speed = b.dataset.spd as '0.75' | '1' | '1.25';
        render();
      });
    });
    shell.body.querySelectorAll<HTMLElement>('[data-sub]').forEach((b) => {
      b.addEventListener('click', () => {
        subtitleMode = b.dataset.sub as 'all' | 'new' | 'off';
        render();
      });
    });
    shell.body.querySelector('[data-loop-btn]')?.addEventListener('click', () => {
      loopTrack = !loopTrack;
      render();
    });
    shell.body.querySelector('[data-prev-ex]')?.addEventListener('click', () => goTo(idx - 1));
    shell.body.querySelector('[data-next-ex]')?.addEventListener('click', () => goTo(idx + 1));

    shell.body.querySelectorAll<HTMLElement>('[data-l-opt]').forEach((b) => {
      b.addEventListener('click', () => checkAnswer(b.dataset.lOpt!, ex.answer));
    });
    shell.body.querySelectorAll<HTMLElement>('[data-lt-add]').forEach((b) => {
      b.addEventListener('click', () => {
        const [item] = tilePool.splice(Number(b.dataset.ltAdd), 1);
        if (item) chosenTiles.push(item);
        render();
      });
    });
    shell.body.querySelectorAll<HTMLElement>('[data-lt-rm]').forEach((b) => {
      b.addEventListener('click', () => {
        const [item] = chosenTiles.splice(Number(b.dataset.ltRm), 1);
        if (item) tilePool.push(item);
        render();
      });
    });
    shell.body.querySelector('[data-lt-check]')?.addEventListener('click', () => checkAnswer(chosenTiles.join(''), ex.answer));

    const dictInp = shell.body.querySelector<HTMLInputElement>('[data-dict-inp]');
    shell.body.querySelectorAll<HTMLElement>('[data-dict-chip]').forEach((b) => {
      b.addEventListener('click', () => {
        if (dictInp) dictInp.value = `${dictInp.value} ${b.dataset.dictChip!}`.trim();
      });
    });
    const submitDictation = () => {
      const val = dictInp?.value ?? '';
      const ok = val.replace(/\s+/g, '').toLowerCase() === ex.answer.replace(/\s+/g, '').toLowerCase() || val.replace(/\s+/g, '') === (ex.tiles ?? []).join('');
      checkAnswer(ok ? ex.answer : val, ex.answer);
    };
    shell.body.querySelector('[data-dict-check]')?.addEventListener('click', submitDictation);

    document.querySelector('[data-l-next]')?.addEventListener('click', () => goTo(idx + 1));

    setKey((e) => {
      const tag = document.activeElement?.tagName;
      if (tag === 'SELECT' || tag === 'TEXTAREA') return;
      if (tag === 'INPUT') {
        if (e.key === 'Enter' && !feedback && ex.kind === 'dictation') submitDictation();
        return;
      }
      if (e.key === ' ') {
        e.preventDefault();
        if (isPlaying) {
          audioService.stop();
          isPlaying = false;
          render();
        } else {
          playCurrent(false);
        }
      } else if (e.key === 's' || e.key === 'S') {
        speed = speed === '0.75' ? '1' : '0.75';
        render();
      } else if (e.key === 'ArrowLeft' && idx > 0) {
        goTo(idx - 1);
      } else if (e.key === 'ArrowRight' && idx < exercises.length - 1) {
        goTo(idx + 1);
      } else if (e.key === 'Backspace' && !feedback && ex.kind === 'listen-tiles' && chosenTiles.length > 0) {
        e.preventDefault();
        const item = chosenTiles.pop();
        if (item) tilePool.push(item);
        render();
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (feedback) {
          goTo(idx + 1);
        } else if (ex.kind === 'listen-tiles' && chosenTiles.length > 0) {
          checkAnswer(chosenTiles.join(''), ex.answer);
        } else if (ex.kind === 'dictation') {
          submitDictation();
        }
      } else if (!feedback && ex.options) {
        const n = Number(e.key);
        if (n >= 1 && n <= ex.options.length) checkAnswer(ex.options[n - 1].value, ex.answer);
      }
    });
  };

  render();
  return () => {
    setKey(null);
    document.querySelector('.feedback-bar')?.remove();
    audioService.stop();
  };
}
