import { renderAppShell } from '../components/AppShell';
import { renderBaoSvg } from '../components/BaoMascot';
import { iconSvg, stickerBadge, type IconName } from '../components/Icons';
import {
  collectStageAssetUrls,
  loadCurriculum,
  loadStageLessons,
  loadStageReadings,
  loadStageWords,
} from '../services/contentLoader';
import { precacheStageAssets, requestPersistentStorage } from '../services/pwa';
import { ensureProgress, ensureSettings, filterQueue, getAllCards, getTodayXp } from '../services/srsEngine';
import type { LessonItem, StageMeta, TopicMeta } from '../types/curriculum';
import { escapeHtml } from '../utils/html';

const TYPE_STYLE: Record<LessonItem['type'], { color: string; lip: string; icon: IconName; label: string; route: (id: string, readingId?: string) => string }> = {
  'giao-tiep': { color: 'var(--comm)', lip: 'var(--comm-lip)', icon: 'comm', label: 'Giao tiếp', route: (id) => `#/lesson/${id}` },
  doc: { color: 'var(--read)', lip: 'var(--read-lip)', icon: 'read', label: 'Đọc hiểu', route: (_id, rid) => `#/reading/${rid ?? 'r-t1'}` },
  nghe: { color: 'var(--listen)', lip: 'var(--listen-lip)', icon: 'listen', label: 'Luyện nghe', route: (id) => `#/listening/${id}` },
  viet: { color: 'var(--write)', lip: 'var(--write-lip)', icon: 'write', label: 'Viết chữ', route: (id) => `#/writing/${id}` },
};

export async function renderMapScreen(root: HTMLElement): Promise<() => void> {
  const [curriculum, progress, settings, words, lessons, readings, cards] = await Promise.all([
    loadCurriculum(),
    ensureProgress(),
    ensureSettings(),
    loadStageWords(1),
    loadStageLessons(1),
    loadStageReadings(1),
    getAllCards(),
  ]);

  const dueCount = filterQueue(cards, 'due').length;
  const body = renderAppShell({
    root,
    activeTab: 'map',
    title: 'Đường du hành của Bao',
    progress,
    settings,
  });

  const lessonById = new Map(lessons.map((l) => [l.id, l]));
  const completedSet = new Set(progress.completedLessons);

  // Build flat ordered list of playable nodes in Stage 1 ready topics to determine the single "current" node
  const playableIds: string[] = [];
  for (const st of curriculum.stages) {
    for (const tp of st.topics) {
      if (tp.ready) {
        for (const lid of tp.lessonIds) playableIds.push(lid);
      }
    }
  }
  const currentLessonId = playableIds.find((id) => !completedSet.has(id)) ?? playableIds[0];

  const goalXp = settings.dailyGoalMinutes * 4;
  const pct = Math.min(100, Math.round((getTodayXp(progress) / Math.max(1, goalXp)) * 100));

  const renderStageBanner = (stage: StageMeta) => {
    const colorMap: Record<string, { bg: string; lip: string }> = {
      comm: { bg: 'var(--comm-soft)', lip: 'var(--comm)' },
      read: { bg: 'var(--read-soft)', lip: 'var(--read)' },
      review: { bg: 'var(--review-soft)', lip: 'var(--review)' },
      write: { bg: 'var(--write-soft)', lip: 'var(--write)' },
    };
    const palette = colorMap[stage.colorToken] ?? colorMap.comm;
    const isStage1 = stage.id === 1;

    return `
      <section class="clay-card" style="padding:20px;margin-bottom:24px;background:${palette.bg};border-color:${palette.lip};">
        <div style="display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;">
          <div style="display:flex;align-items:center;gap:12px;">
            ${isStage1 ? renderBaoSvg({ mood: 'backpack', size: 60, accessory: progress.equippedAccessory }) : ''}
            <div>
              <h2 style="margin:0;font-size:22px;font-weight:800;">${escapeHtml(stage.title)}</h2>
              <p style="margin:4px 0 0;color:var(--ink-muted);font-size:14px;">${escapeHtml(stage.subtitle)}</p>
            </div>
          </div>
          <div style="display:flex;gap:8px;flex-wrap:wrap;">
            ${
              stage.grammarNotes.length > 0
                ? `<button type="button" class="btn btn-sm btn-soft" data-open-notebook="${stage.id}">${iconSvg('book', 16)} Sổ tay</button>`
                : ''
            }
            ${
              isStage1
                ? `<button type="button" class="btn btn-sm btn-vocab" data-cache-stage="1">${iconSvg('download', 16)} Tải sẵn chặng này</button>`
                : ''
            }
          </div>
        </div>
        ${isStage1 ? `<div data-cache-status style="margin-top:8px;font-size:13px;color:var(--ink-muted);"></div>` : ''}
      </section>
    `;
  };

  const renderTopicNodes = (topic: TopicMeta) => {
    if (!topic.ready) {
      return `
        <div style="margin:14px 0 26px;padding:14px 18px;border-radius:18px;border:1.5px dashed var(--border-path);background:rgba(255,255,255,.55);display:flex;align-items:center;justify-content:space-between;gap:12px;">
          <div>
            <strong>Chủ đề ${topic.id}: ${escapeHtml(topic.title)}</strong>
            <div style="font-size:13px;color:var(--ink-muted);">${escapeHtml(topic.subtitle)}</div>
          </div>
          <span class="chip" style="background:var(--bg);color:var(--ink-muted);">${iconSvg('lock', 14)} Đợt 2</span>
        </div>
      `;
    }

    const nodesHtml = topic.lessonIds
      .map((lid, idx) => {
        const lesson = lessonById.get(lid);
        if (!lesson) return '';
        const st = TYPE_STYLE[lesson.type];
        const isDone = completedSet.has(lid);
        const isCurrent = lid === currentLessonId;
        const partialRatio = !isDone ? (progress.lessonProgress[lid] ?? 0) : 0;
        const isLocked = !isDone && !isCurrent && partialRatio === 0 && playableIds.indexOf(lid) > playableIds.indexOf(currentLessonId);
        const offsetPx = idx % 2 === 0 ? -44 : 44;

        const btnBg = !isLocked ? st.color : 'var(--locked)';
        const btnLip = !isLocked ? st.lip : 'var(--locked-lip)';
        const nodeStyle = `width:72px;height:72px;border-radius:999px;border:3px solid #FFFFFF;background:${btnBg};box-shadow:0 5px 0 ${btnLip}, var(--shadow-clay);display:flex;align-items:center;justify-content:center;position:relative;color:#3D3654;${
          isCurrent ? 'animation:baoBounce 1.8s ease-in-out infinite;' : ''
        }`;

        const ringSvg =
          partialRatio > 0
            ? `<svg width="84" height="84" viewBox="0 0 84 84" style="position:absolute;inset:-9px;pointer-events:none;transform:rotate(-90deg);">
                 <circle cx="42" cy="42" r="38" fill="none" stroke="var(--border)" stroke-width="5"/>
                 <circle cx="42" cy="42" r="38" fill="none" stroke="${st.lip}" stroke-width="5" stroke-dasharray="${Math.round(2 * Math.PI * 38)}" stroke-dashoffset="${Math.round(2 * Math.PI * 38 * (1 - partialRatio))}" stroke-linecap="round"/>
               </svg>`
            : '';

        return `
          <div style="display:flex;flex-direction:column;align-items:center;transform:translateX(${offsetPx}px);position:relative;margin:14px 0;">
            ${
              isCurrent
                ? `<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                     ${renderBaoSvg({ mood: 'wave', size: 54, accessory: progress.equippedAccessory })}
                     <div style="background:var(--surface);border:1.5px solid var(--border);border-radius:14px;padding:6px 12px;font-size:13px;font-weight:700;box-shadow:var(--shadow-clay);">Học tiếp nhé!</div>
                   </div>`
                : ''
            }
            <button type="button" data-lesson-node="${escapeHtml(lid)}" style="${nodeStyle}" aria-label="${escapeHtml(lesson.title)}">
              ${ringSvg}
              ${isLocked ? iconSvg('lock', 26) : stickerBadge(st.icon, btnBg, 40)}
              ${
                isDone
                  ? `<span style="position:absolute;top:-6px;right:-6px;width:24px;height:24px;border-radius:999px;background:var(--review);border:2px solid #FFF;display:flex;align-items:center;justify-content:center;">${iconSvg('crown', 13)}</span>`
                  : ''
              }
            </button>
            <div style="margin-top:8px;font-size:14px;font-weight:700;text-align:center;">${escapeHtml(st.label)}</div>
            ${
              lesson.type === 'giao-tiep'
                ? `<a href="#/dialogue/${escapeHtml(lid)}" style="font-size:12px;color:var(--comm-lip);font-weight:700;margin-top:2px;text-decoration:none;">Vào hội thoại riêng →</a>`
                : ''
            }
          </div>
        `;
      })
      .join(`<div style="width:2px;height:18px;border-left:3px dashed var(--border-path);margin:0 auto;"></div>`);

    return `
      <div style="margin-bottom:28px;">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;padding:0 4px;">
          <h3 style="margin:0;font-size:18px;font-weight:800;">Chủ đề ${topic.id}: ${escapeHtml(topic.title)}</h3>
          <span class="chip" style="font-size:12px;">${topic.lessonIds.filter((id) => completedSet.has(id)).length}/${topic.lessonIds.length} bài</span>
        </div>
        <div style="display:flex;flex-direction:column;align-items:center;padding:8px 0;">
          ${nodesHtml}
        </div>
      </div>
    `;
  };

  const chapter1 = curriculum.stages[0].storyChapter;
  const bookmarkedStoryId = Object.keys(progress.storyBookmarks)[0] ?? chapter1.readingId ?? 'r-t6';
  const activeReadingMeta = readings.find((r) => r.id === bookmarkedStoryId);

  body.innerHTML = `
    <div style="display:grid;grid-template-columns:minmax(0,720px) minmax(260px,320px);gap:24px;align-items:start;" class="map-grid">
      <div>
        ${curriculum.stages
          .map(
            (st) =>
              renderStageBanner(st) +
              (st.id === 1 ? st.topics.map(renderTopicNodes).join('') : `<p style="color:var(--ink-muted);margin:-10px 0 24px 8px;font-size:14px;">Hoàn thành ~80% chặng trước để mở khoá (${st.topics.length} chủ đề).</p>`)
          )
          .join('')}
      </div>

      <aside style="display:flex;flex-direction:column;gap:16px;position:sticky;top:20px;">
        <div class="clay-card" style="padding:20px;">
          <h2 style="margin:0 0 12px;font-size:19px;">Hôm nay</h2>
          <div style="display:flex;align-items:center;gap:14px;margin-bottom:14px;">
            <div style="width:64px;height:64px;border-radius:999px;background:conic-gradient(var(--read) ${pct * 3.6}deg, var(--border) 0deg);display:flex;align-items:center;justify-content:center;">
              <div style="width:48px;height:48px;border-radius:999px;background:var(--surface);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:14px;">${pct}%</div>
            </div>
            <div>
              <div style="font-weight:800;">Mục tiêu ${settings.dailyGoalMinutes} phút/ngày</div>
              <div style="font-size:13px;color:var(--ink-muted);">${dueCount} thẻ đến hạn ôn tập</div>
            </div>
          </div>
          <a href="#/review" class="btn btn-review" style="width:100%;">Ôn tập ngay (${dueCount})</a>
        </div>

        <div class="clay-card" style="padding:20px;background:var(--read-soft);border-color:var(--read);">
          <div style="font-size:12px;font-weight:800;text-transform:uppercase;color:var(--read-lip);">Truyện dài kỳ</div>
          <h3 style="margin:4px 0 8px;font-size:18px;">${escapeHtml(activeReadingMeta?.title ?? chapter1.title)}</h3>
          <p style="margin:0 0 14px;font-size:14px;color:var(--ink-muted);">${escapeHtml(chapter1.teaserVi)}</p>
          <a href="#/reading/${escapeHtml(bookmarkedStoryId)}" class="btn btn-read btn-sm" style="width:100%;">Đọc tiếp</a>
        </div>
      </aside>
    </div>
    <style>
      @media (max-width: 960px) {
        .map-grid { grid-template-columns: 1fr !important; }
      }
    </style>
  `;

  // Node popover
  let activeModal: HTMLElement | null = null;
  const closeModal = () => {
    activeModal?.remove();
    activeModal = null;
  };

  body.querySelectorAll<HTMLElement>('[data-lesson-node]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const lid = btn.dataset.lessonNode!;
      const lesson = lessonById.get(lid);
      if (!lesson) return;
      const st = TYPE_STYLE[lesson.type];
      closeModal();
      const backdrop = document.createElement('div');
      backdrop.className = 'modal-backdrop';
      backdrop.innerHTML = `
        <div class="modal-card" role="dialog" aria-label="${escapeHtml(lesson.title)}">
          <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:12px;">
            <span class="chip" style="background:${st.color};">${escapeHtml(st.label)}</span>
            <span class="chip">+${lesson.xp} XP</span>
          </div>
          <h2 style="margin:0 0 8px;">${escapeHtml(lesson.title)}</h2>
          <p style="margin:0 0 18px;color:var(--ink-muted);">
            Phiên ngắn 7–10 phút · ${lesson.newWords.length > 0 ? `${lesson.newWords.length} từ mới trọng tâm` : 'Đọc hiểu & câu hỏi tương tác'}. Không giới hạn lượt thử.
          </p>
          <div style="display:flex;gap:10px;flex-wrap:wrap;">
            <a href="${st.route(lesson.id, lesson.readingId)}" class="btn btn-comm" data-start-lesson style="flex:1;">BẮT ĐẦU</a>
            ${
              lesson.type === 'giao-tiep'
                ? `<a href="#/dialogue/${escapeHtml(lesson.id)}" class="btn btn-soft">Hội thoại riêng</a>`
                : ''
            }
            <button type="button" class="btn btn-soft" data-close-modal>Đóng</button>
          </div>
        </div>
      `;
      document.body.appendChild(backdrop);
      activeModal = backdrop;
      backdrop.addEventListener('click', (e) => {
        if (e.target === backdrop) closeModal();
      });
      backdrop.querySelector('[data-close-modal]')?.addEventListener('click', closeModal);
      backdrop.querySelector('[data-start-lesson]')?.addEventListener('click', () => {
        requestPersistentStorage();
        closeModal();
      });
    });
  });

  // Grammar notebook modal
  body.querySelectorAll<HTMLElement>('[data-open-notebook]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const sid = Number(btn.dataset.openNotebook);
      const stage = curriculum.stages.find((s) => s.id === sid);
      if (!stage) return;
      closeModal();
      const backdrop = document.createElement('div');
      backdrop.className = 'modal-backdrop';
      backdrop.innerHTML = `
        <div class="modal-card" role="dialog" aria-label="Sổ tay ngữ pháp">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;">
            <h2 style="margin:0;">Sổ tay: ${escapeHtml(stage.title)}</h2>
            <button type="button" class="btn btn-sm btn-soft" data-close-modal>${iconSvg('close', 16)}</button>
          </div>
          ${stage.grammarNotes
            .map(
              (n) => `
            <div style="padding:14px;border-radius:16px;background:var(--bg);border:1.5px solid var(--border);margin-bottom:12px;">
              <div style="font-weight:800;margin-bottom:4px;">${escapeHtml(n.title)}</div>
              <div style="font-size:13px;color:var(--vocab-lip);font-weight:700;margin-bottom:6px;">${escapeHtml(n.pattern)}</div>
              <div style="font-size:14px;margin-bottom:8px;">${escapeHtml(n.explainVi)}</div>
              <div class="hanzi" style="font-size:20px;font-weight:600;">${escapeHtml(n.exampleHanzi)}</div>
              <div style="font-size:13px;color:var(--ink-muted);">${escapeHtml(n.exampleVi)}</div>
            </div>`
            )
            .join('')}
        </div>
      `;
      document.body.appendChild(backdrop);
      activeModal = backdrop;
      backdrop.addEventListener('click', (e) => {
        if (e.target === backdrop) closeModal();
      });
      backdrop.querySelector('[data-close-modal]')?.addEventListener('click', closeModal);
    });
  });

  // Precache Stage 1 for offline
  body.querySelector('[data-cache-stage="1"]')?.addEventListener('click', async (e) => {
    const btn = e.currentTarget as HTMLButtonElement;
    const statusEl = body.querySelector('[data-cache-status]') as HTMLElement;
    btn.disabled = true;
    const urls = collectStageAssetUrls(1, words, lessons, readings);
    statusEl.textContent = `Đang tải sẵn ${urls.length} tệp offline...`;
    const res = await precacheStageAssets(urls, (done, total) => {
      statusEl.textContent = `Đã lưu ${done}/${total} tệp cho chế độ offline...`;
    });
    statusEl.textContent = `Sẵn sàng offline: đã lưu ${res.ok}/${res.total} tệp Chặng 1.`;
    btn.disabled = false;
  });

  return () => closeModal();
}
