import confetti from 'canvas-confetti';
import HanziWriter from 'hanzi-writer';
import { renderFocusShell } from '../components/AppShell';
import { renderBaoSvg } from '../components/BaoMascot';
import { iconSvg } from '../components/Icons';
import { audioService } from '../services/audioPlayer';
import { loadStageLessons, resolveStageForLessonId } from '../services/contentLoader';
import { requestPersistentStorage } from '../services/pwa';
import { ensureProgress, ensureSettings, recordStudyActivity } from '../services/srsEngine';
import type { StageTestItem } from '../types/curriculum';
import { escapeHtml } from '../utils/html';

const base = import.meta.env.BASE_URL;

const SKILL_META: Record<StageTestItem['skill'], { label: string; chipBg: string; accent: string }> = {
  'giao-tiep': { label: 'Giao tiếp', chipBg: 'var(--comm-soft)', accent: 'var(--comm)' },
  doc: { label: 'Đọc hiểu', chipBg: 'var(--read-soft)', accent: 'var(--read)' },
  nghe: { label: 'Luyện nghe', chipBg: 'var(--listen-soft)', accent: 'var(--listen)' },
  viet: { label: 'Viết & nhận diện', chipBg: 'var(--write-soft)', accent: 'var(--write)' },
};

export async function renderStageTestScreen(root: HTMLElement, testId: string): Promise<() => void> {
  requestPersistentStorage();
  const stage = resolveStageForLessonId(testId);
  const [lessons, progress, settings] = await Promise.all([
    loadStageLessons(stage),
    ensureProgress(),
    ensureSettings(),
  ]);
  const testLesson = lessons.find((l) => l.id === testId && l.type === 'stage-test');
  if (!testLesson || !testLesson.stageTestItems?.length) {
    root.innerHTML = `<div style="padding:40px;text-align:center;"><h2>Không tìm thấy bài kiểm tra chặng</h2><a href="#/" class="btn btn-comm">Về bản đồ</a></div>`;
    return () => {};
  }

  const items = testLesson.stageTestItems;
  audioService.preload(items.flatMap((it) => [it.audio, it.audioSlow]));

  const shell = renderFocusShell({
    root,
    progressPct: 8,
    accentVar: 'var(--review)',
  });

  let idx = 0;
  let score = 0;
  let showPinyin = settings.pinyinMode !== 'off';
  let slowMode = false;
  let answered: { ok: boolean; picked: string } | null = null;
  let writer: HanziWriter | null = null;
  let writeDone = false;
  let writeHint = '';
  let finished = false;
  let recorded = false;
  let unmounted = false;
  let keyHandler: ((e: KeyboardEvent) => void) | null = null;

  const setKey = (fn: ((e: KeyboardEvent) => void) | null) => {
    if (keyHandler) document.removeEventListener('keydown', keyHandler);
    keyHandler = fn;
    if (fn) document.addEventListener('keydown', fn);
  };

  const playItemAudio = (it: StageTestItem, forceSlow = false) => {
    const useSlow = forceSlow || slowMode;
    const src = useSlow && it.audioSlow ? it.audioSlow : it.audio;
    if (src) audioService.play(src);
  };

  const mountTestWriter = (char: string, interactive = true) => {
    const target = shell.body.querySelector<HTMLElement>('[data-st-hw]');
    if (!target) return;
    target.innerHTML = '';
    const size = Math.min(340, Math.max(240, window.innerWidth - 72));
    target.style.width = `${size}px`;
    target.style.height = `${size}px`;
    writer = HanziWriter.create(target, char, {
      width: size,
      height: size,
      padding: 20,
      showOutline: true,
      showCharacter: !interactive,
      outlineColor: '#D8D2CC',
      strokeColor: '#3D3654',
      radicalColor: '#D97E06',
      highlightColor: '#FF9600',
      drawingColor: '#3D3654',
      drawingWidth: 14,
      showHintAfterMisses: 2,
      charDataLoader: async (ch) => {
        const res = await fetch(`${base}strokes/${encodeURIComponent(ch)}.json`);
        if (!res.ok) throw new Error(`Missing stroke ${ch}`);
        return res.json();
      },
    });
    if (!interactive) return;
    writer.quiz({
      onCorrectStroke() {
        audioService.playSfx('pop');
        writeHint = '';
        const h = shell.body.querySelector('[data-st-whint]');
        if (h) h.textContent = '';
      },
      onMistake(sd) {
        audioService.playSfx('err');
        writeHint = `Thử lại nét ${sd.strokeNum + 1} nhé!`;
        const h = shell.body.querySelector('[data-st-whint]');
        if (h) h.textContent = writeHint;
      },
      onComplete() {
        audioService.playSfx('ok');
        writeDone = true;
        answered = { ok: true, picked: char };
        score += 1;
        render();
      },
    });
  };

  const goNext = () => {
    writer?.cancelQuiz();
    writer = null;
    audioService.stop();
    if (idx + 1 >= items.length) {
      finished = true;
    } else {
      idx += 1;
      answered = null;
      writeDone = false;
      writeHint = '';
      slowMode = false;
    }
    render();
  };

  const render = () => {
    setKey(null);
    if (finished) {
      shell.setProgress(100, 'Hoàn thành');
      const pct = Math.round((score / items.length) * 100);
      const passed = pct >= 75;
      const earnedXp = passed ? testLesson.xp : 20;

      if (!recorded) {
        recorded = true;
        recordStudyActivity({
          xpEarned: earnedXp,
          skill: 'all',
          completedLessonId: passed ? testLesson.id : undefined,
        });
        if (passed && !settings.reducedMotion) {
          confetti({ particleCount: 70, spread: 80, origin: { y: 0.65 } });
        }
      }

      shell.body.innerHTML = `
        <div class="clay-card" style="padding:32px;text-align:center;">
          ${renderBaoSvg({ mood: passed ? 'celebrate' : 'wave', size: 112, accessory: progress.equippedAccessory })}
          <h2 style="margin:12px 0 6px;font-size:28px;">${passed ? `Chinh phục ${escapeHtml(testLesson.title)}!` : 'Cố thêm chút nữa nhé!'}</h2>
          <p style="margin:0 0 18px;color:var(--ink-muted);font-size:17px;">
            Bạn đạt <strong>${score}/${items.length}</strong> câu (${pct}%) · +${earnedXp} XP cộng đều cả 4 kỹ năng.
            ${passed ? ` Huy hiệu Chặng ${stage} đã mở khoá!` : ' Đạt từ 75% trở lên để nhận huy hiệu hoàn thành chặng (không mất lượt thử).'}
          </p>
          <div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;">
            <a href="#/" class="btn btn-review">Về bản đồ học</a>
            ${!passed ? `<button type="button" class="btn btn-soft" data-st-retry>Làm lại bài kiểm tra</button>` : ''}
            ${stage < 4 && passed ? `<a href="#/reading/story-c${stage}" class="btn btn-read">Đọc tiếp Truyện dài kỳ</a>` : ''}
          </div>
        </div>
      `;
      shell.body.querySelector('[data-st-retry]')?.addEventListener('click', () => {
        idx = 0;
        score = 0;
        answered = null;
        writeDone = false;
        finished = false;
        recorded = false;
        render();
      });
      return;
    }

    const it = items[idx];
    const meta = SKILL_META[it.skill];
    shell.setProgress(((idx + 1) / items.length) * 95, `${idx + 1}/${items.length}`);

    shell.body.innerHTML = `
      <div class="clay-card" style="padding:26px;">
        <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:14px;">
          <span class="chip" style="background:var(--surface);border-color:${meta.accent};">${escapeHtml(meta.label)}</span>
          ${it.passageHanzi ? `<button type="button" class="btn btn-sm btn-soft" data-st-py>[P] ${showPinyin ? 'Ẩn pinyin' : 'Hiện pinyin'}</button>` : ''}
        </div>

        <h2 style="margin:0 0 14px;">${escapeHtml(it.promptVi)}</h2>

        ${
          it.passageHanzi
            ? `<div style="padding:16px;border-radius:16px;background:var(--bg);border:1.5px solid var(--border);margin-bottom:16px;">
                 <div class="hanzi" style="font-size:22px;font-weight:600;line-height:1.7;">${escapeHtml(it.passageHanzi)}</div>
                 ${showPinyin && it.passagePinyin ? `<div class="pinyin" style="margin-top:6px;">${escapeHtml(it.passagePinyin)}</div>` : ''}
               </div>`
            : ''
        }

        ${
          it.audio
            ? `<div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:16px;">
                 <button type="button" class="btn btn-review" data-st-play>${iconSvg('speaker', 18)} Nghe (Space)</button>
                 ${
                   it.audioSlow
                     ? `<button type="button" class="btn btn-sm btn-soft" aria-pressed="${slowMode}" style="${slowMode ? 'border-color:var(--review);background:var(--review-soft);' : ''}" data-st-slow>[S] Nghe chậm 0.75×</button>`
                     : ''
                 }
               </div>`
            : ''
        }

        ${
          it.writingChar
            ? `<div style="display:flex;flex-direction:column;align-items:center;gap:12px;">
                 <div style="padding:10px;border-radius:18px;border:2px solid var(--write);background:#FFF;">
                   <div style="position:relative;border-radius:14px;overflow:hidden;border:1.5px solid var(--border);background:linear-gradient(to right, transparent 49.5%, #F1E4D8 49.5%, #F1E4D8 50.5%, transparent 50.5%), linear-gradient(to bottom, transparent 49.5%, #F1E4D8 49.5%, #F1E4D8 50.5%, transparent 50.5%), linear-gradient(45deg, transparent 49.6%, #F6ECE2 49.6%, #F6ECE2 50.4%, transparent 50.4%), linear-gradient(-45deg, transparent 49.6%, #F6ECE2 49.6%, #F6ECE2 50.4%, transparent 50.4%), #FFFFFF;">
                     <div data-st-hw></div>
                   </div>
                 </div>
                 <div style="display:flex;gap:10px;flex-wrap:wrap;">
                   <button type="button" class="btn btn-sm btn-soft" data-st-anim>[Space] Xem nét</button>
                   <button type="button" class="btn btn-sm btn-soft" data-st-reset>[R] Viết lại</button>
                   <span class="chip">Bộ <span class="hanzi" style="font-size:20px;margin-left:4px;">${escapeHtml(it.writingChar.radical)}</span></span>
                 </div>
                 <div data-st-whint style="font-weight:700;color:var(--comm-lip);min-height:20px;">${escapeHtml(writeHint)}</div>
               </div>`
            : `<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:10px;">
                 ${(it.options ?? [])
                   .map((o, oi) => {
                     let cls = 'btn-soft';
                     if (answered) {
                       if (o.value === it.answer) cls = 'btn-read';
                       else if (o.value === answered.picked) cls = 'btn-comm';
                     }
                     return `<button type="button" class="btn ${cls}" data-st-opt="${escapeHtml(o.value)}" ${answered ? 'disabled' : ''} style="justify-content:flex-start;padding:12px 14px;">
                       <span class="chip" style="font-size:12px;">${oi + 1}</span>
                       <span class="${/[\u4e00-\u9fff]/.test(o.label) ? 'hanzi' : ''}" style="font-size:${/[\u4e00-\u9fff]/.test(o.label) ? '22px' : '16px'};">${escapeHtml(o.label)}</span>
                     </button>`;
                   })
                   .join('')}
               </div>`
        }
      </div>

      ${
        answered
          ? `<div class="feedback-bar ${answered.ok ? 'is-ok' : 'is-err'}">
               <div class="feedback-inner">
                 <div>
                   <strong>${
                     answered.ok
                       ? 'Chính xác!'
                       : `Đáp án đúng: <span class="${/[\u4e00-\u9fff]/.test(it.answer) ? 'hanzi' : ''}" style="font-size:${/[\u4e00-\u9fff]/.test(it.answer) ? '20px' : 'inherit'};">${escapeHtml(it.answer)}</span>`
                   }</strong>
                   ${it.explainVi ? `<span style="margin-left:8px;">${escapeHtml(it.explainVi)}</span>` : ''}
                 </div>
                 <button type="button" class="btn ${answered.ok ? 'btn-read' : 'btn-comm'}" data-st-next>Tiếp theo (Enter)</button>
               </div>
             </div>`
          : ''
      }
    `;

    if (it.writingChar) {
      mountTestWriter(it.writingChar.char, !writeDone);
    }

    shell.body.querySelector('[data-st-py]')?.addEventListener('click', () => {
      showPinyin = !showPinyin;
      render();
    });
    shell.body.querySelector('[data-st-play]')?.addEventListener('click', () => playItemAudio(it, false));
    shell.body.querySelector('[data-st-slow]')?.addEventListener('click', () => {
      slowMode = !slowMode;
      playItemAudio(it, slowMode);
    });
    shell.body.querySelector('[data-st-anim]')?.addEventListener('click', () => {
      writer?.animateCharacter({
        onComplete: () => {
          if (!unmounted && it.writingChar && !writeDone) mountTestWriter(it.writingChar.char);
        },
      });
    });
    shell.body.querySelector('[data-st-reset]')?.addEventListener('click', () => {
      if (it.writingChar) mountTestWriter(it.writingChar.char);
    });

    const pickOption = (val: string) => {
      if (answered) return;
      const ok = val === it.answer;
      if (ok) score += 1;
      answered = { ok, picked: val };
      audioService.playSfx(ok ? 'ok' : 'err');
      if (!ok && it.skill === 'nghe' && it.audioSlow) {
        playItemAudio(it, true);
      }
      render();
    };

    shell.body.querySelectorAll<HTMLElement>('[data-st-opt]').forEach((b) => {
      b.addEventListener('click', () => pickOption(b.dataset.stOpt!));
    });
    document.querySelector('[data-st-next]')?.addEventListener('click', goNext);

    setKey((e) => {
      if (e.key === ' ') {
        e.preventDefault();
        if (it.writingChar) {
          writer?.animateCharacter({
            onComplete: () => {
              if (!unmounted && it.writingChar && !writeDone) mountTestWriter(it.writingChar.char);
            },
          });
        } else if (it.audio) {
          playItemAudio(it, false);
        }
      } else if (e.key === 'Enter' && answered) {
        e.preventDefault();
        goNext();
      } else if ((e.key === 'p' || e.key === 'P') && it.passageHanzi) {
        showPinyin = !showPinyin;
        render();
      } else if ((e.key === 's' || e.key === 'S') && it.audioSlow) {
        slowMode = !slowMode;
        playItemAudio(it, slowMode);
      } else if ((e.key === 'r' || e.key === 'R') && it.writingChar && !writeDone) {
        mountTestWriter(it.writingChar.char);
      } else if (!answered && it.options) {
        const n = Number(e.key);
        if (n >= 1 && n <= it.options.length) pickOption(it.options[n - 1].value);
      }
    });
  };

  render();
  return () => {
    unmounted = true;
    setKey(null);
    writer?.cancelQuiz();
    document.querySelector('.feedback-bar')?.remove();
    audioService.stop();
  };
}
