import { renderAppShell } from '../components/AppShell';
import { renderBaoSvg } from '../components/BaoMascot';
import { iconSvg, stickerBadge, type IconName } from '../components/Icons';
import {
  collectStageAssetUrls,
  loadCurriculum,
  loadStageBundle,
} from '../services/contentLoader';
import { precacheStageAssets, requestPersistentStorage } from '../services/pwa';
import { ensureProgress, ensureSettings, filterQueue, getAllCards, getTodayXp } from '../services/srsEngine';
import type { LessonItem, StageMeta, TopicMeta } from '../types/curriculum';
import { escapeHtml } from '../utils/html';

const TYPE_STYLE: Record<
  'giao-tiep' | 'doc' | 'nghe' | 'viet',
  { color: string; lip: string; icon: IconName; label: string; route: (id: string, readingId?: string) => string }
> = {
  'giao-tiep': { color: 'var(--comm)', lip: 'var(--comm-lip)', icon: 'comm', label: 'Giao tiếp', route: (id) => `#/lesson/${id}` },
  doc: { color: 'var(--read)', lip: 'var(--read-lip)', icon: 'read', label: 'Đọc hiểu', route: (_id, rid) => `#/reading/${rid ?? 'r-t1'}` },
  nghe: { color: 'var(--listen)', lip: 'var(--listen-lip)', icon: 'listen', label: 'Luyện nghe', route: (id) => `#/listening/${id}` },
  viet: { color: 'var(--write)', lip: 'var(--write-lip)', icon: 'write', label: 'Viết chữ', route: (id) => `#/writing/${id}` },
};

const STAGE_PALETTE: Record<string, { bg: string; lip: string }> = {
  comm: { bg: 'var(--comm-soft)', lip: 'var(--comm)' },
  read: { bg: 'var(--read-soft)', lip: 'var(--read)' },
  review: { bg: 'var(--review-soft)', lip: 'var(--review)' },
  write: { bg: 'var(--write-soft)', lip: 'var(--write)' },
};

export async function renderMapScreen(root: HTMLElement): Promise<() => void> {
  const [curriculum, progress, settings, cards] = await Promise.all([
    loadCurriculum(),
    ensureProgress(),
    ensureSettings(),
    getAllCards(),
  ]);

  const completedSet = new Set(progress.completedLessons);

  const stageCompletionRatio = (st: StageMeta): number => {
    const ids = st.topics.flatMap((t) => t.lessonIds);
    if (ids.length === 0) return 0;
    const done = ids.filter((id) => completedSet.has(id)).length;
    return done / ids.length;
  };

  const isStageUnlocked = (stageId: number): boolean => {
    if (stageId <= 1) return true;
    const prev = curriculum.stages.find((s) => s.id === stageId - 1);
    return prev ? stageCompletionRatio(prev) >= 0.8 : true;
  };

  // Pick initial active stage: highest unlocked stage that isn't 100% done, else highest unlocked stage
  let highestUnlocked = 1;
  let highestIncomplete = 0;
  for (const st of curriculum.stages) {
    if (isStageUnlocked(st.id)) {
      highestUnlocked = st.id;
      if (stageCompletionRatio(st) < 1) {
        highestIncomplete = st.id;
      }
    }
  }
  let selectedStageId = highestIncomplete || highestUnlocked;

  let activeModal: HTMLElement | null = null;
  let keyHandler: ((e: KeyboardEvent) => void) | null = null;

  const setKey = (fn: ((e: KeyboardEvent) => void) | null) => {
    if (keyHandler) document.removeEventListener('keydown', keyHandler);
    keyHandler = fn;
    if (fn) document.addEventListener('keydown', fn);
  };

  const closeModal = () => {
    activeModal?.remove();
    activeModal = null;
  };

  const dueCount = filterQueue(cards, 'due').length;
  const goalXp = settings.dailyGoalMinutes * 4;
  const pct = Math.min(100, Math.round((getTodayXp(progress) / Math.max(1, goalXp)) * 100));

  const render = async () => {
    setKey(null);
    const body = renderAppShell({
      root,
      activeTab: 'map',
      title: 'Đường du hành của Bao',
      progress,
      settings,
    });

    const stage = curriculum.stages.find((s) => s.id === selectedStageId) ?? curriculum.stages[0];
    const { lessons } = await loadStageBundle(stage.id);
    const lessonById = new Map(lessons.map((l) => [l.id, l]));

    const playableIds = stage.topics.flatMap((tp) => (tp.ready ? tp.lessonIds : []));
    const currentLessonId = playableIds.find((id) => !completedSet.has(id)) ?? playableIds[0];

    const renderTopicNodes = (topic: TopicMeta) => {
      const nodesHtml = topic.lessonIds
        .map((lid, idx) => {
          const lesson = lessonById.get(lid);
          if (!lesson || lesson.type === 'stage-test') return '';
          const st = TYPE_STYLE[lesson.type];
          const isDone = completedSet.has(lid);
          const isCurrent = lid === currentLessonId;
          const partialRatio = !isDone ? (progress.lessonProgress[lid] ?? 0) : 0;
          const isLocked =
            !isDone &&
            !isCurrent &&
            partialRatio === 0 &&
            playableIds.indexOf(lid) > playableIds.indexOf(currentLessonId);
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
            <div style="display:flex;flex-direction:column;align-items:center;transform:translateX(${offsetPx}px);position:relative;margin:12px 0;">
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
        .join(`<div style="width:2px;height:16px;border-left:3px dashed var(--border-path);margin:0 auto;"></div>`);

      return `
        <div style="margin-bottom:26px;">
          <div style="display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:8px;padding:0 4px;">
            <div>
              <h3 style="margin:0;font-size:18px;font-weight:800;">Chủ đề ${topic.id}: ${escapeHtml(topic.title)}</h3>
              <div style="font-size:13px;color:var(--ink-muted);">${escapeHtml(topic.subtitle)}</div>
            </div>
            <span class="chip" style="font-size:12px;">${topic.lessonIds.filter((id) => completedSet.has(id)).length}/${topic.lessonIds.length} bài</span>
          </div>
          <div style="display:flex;flex-direction:column;align-items:center;padding:8px 0;">
            ${nodesHtml}
          </div>
        </div>
      `;
    };

    const renderStageBanner = (st: StageMeta, active: boolean) => {
      const palette = STAGE_PALETTE[st.colorToken] ?? STAGE_PALETTE.comm;
      const unlocked = isStageUnlocked(st.id);
      const ratioPct = Math.round(stageCompletionRatio(st) * 100);
      const prevStage = curriculum.stages.find((x) => x.id === st.id - 1);
      const prevPct = prevStage ? Math.round(stageCompletionRatio(prevStage) * 100) : 100;

      const cardBg = active ? palette.bg : 'var(--surface)';
      const cardBorder = active ? palette.lip : 'var(--border)';

      return `
        <section class="clay-card" style="padding:20px;margin-bottom:18px;background:${cardBg};border-color:${cardBorder};">
          <div style="display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;">
            <div style="display:flex;align-items:center;gap:12px;">
              ${active ? renderBaoSvg({ mood: 'backpack', size: 60, accessory: progress.equippedAccessory }) : ''}
              <div>
                <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
                  <h2 style="margin:0;font-size:21px;font-weight:800;">${escapeHtml(st.title)}</h2>
                  <span class="chip" style="font-size:12px;">${ratioPct}% hoàn thành</span>
                  ${!unlocked ? `<span class="chip" style="font-size:12px;background:var(--bg);">${iconSvg('lock', 13)} Mở khoá đề xuất ≥80% Chặng ${st.id - 1} (${prevPct}%)</span>` : ''}
                </div>
                <p style="margin:4px 0 0;color:var(--ink-muted);font-size:14px;">${escapeHtml(st.subtitle)}</p>
              </div>
            </div>
            <div style="display:flex;gap:8px;flex-wrap:wrap;">
              ${
                st.grammarNotes.length > 0
                  ? `<button type="button" class="btn btn-sm btn-soft" data-open-notebook="${st.id}">${iconSvg('book', 16)} Sổ tay</button>`
                  : ''
              }
              <button type="button" class="btn btn-sm btn-soft" data-cache-stage="${st.id}">${iconSvg('download', 16)} Tải sẵn chặng này</button>
              ${
                !active
                  ? `<button type="button" class="btn btn-sm btn-soft" data-select-stage="${st.id}">Mở Chặng ${st.id}</button>`
                  : ''
              }
            </div>
          </div>
          <div data-cache-status="${st.id}" style="margin-top:8px;font-size:13px;color:var(--ink-muted);"></div>
        </section>
      `;
    };

    const storyId = stage.storyChapter.readingId ?? `story-c${stage.id}`;
    const testId = stage.stageTestId ?? `stage-${stage.id}-test`;
    const testDone = completedSet.has(testId);
    const storyDone = (progress.completedStories ?? []).includes(storyId);

    const openedStories = Object.keys(progress.storyBookmarks)
      .filter((id) => /^story-c\d+$/.test(id))
      .sort((a, b) => Number(b.slice(7)) - Number(a.slice(7)));
    const bookmarkedStoryId =
      stage.storyChapter.readingId && progress.storyBookmarks[stage.storyChapter.readingId] !== undefined
        ? stage.storyChapter.readingId
        : openedStories[0] ?? stage.storyChapter.readingId ?? 'story-c1';
    const sidebarStoryMeta =
      curriculum.stages.find((s) => s.storyChapter.readingId === bookmarkedStoryId)?.storyChapter ??
      stage.storyChapter;

    const stageTabsHtml = curriculum.stages
      .map(
        (st) => `<button type="button" class="btn btn-sm ${st.id === selectedStageId ? 'btn-comm' : 'btn-soft'}" data-select-stage="${st.id}">
          Chặng ${st.id} (${st.topics.length} chủ đề)
        </button>`
      )
      .join('');

    body.innerHTML = `
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:18px;" role="tablist" aria-label="Chọn chặng học">
        ${stageTabsHtml}
      </div>

      <div style="display:grid;grid-template-columns:minmax(0,720px) minmax(260px,320px);gap:24px;align-items:start;" class="map-grid">
        <div>
          ${renderStageBanner(stage, true)}
          ${stage.topics.map(renderTopicNodes).join('')}

          <!-- Stage Story Chapter & End-of-Stage Mixed Test -->
          <div class="clay-card" style="padding:20px;margin:8px 0 28px;display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;">
            <div style="padding:14px;border-radius:16px;background:var(--read-soft);border:1.5px solid var(--read);">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                <span class="chip" style="background:var(--surface);font-size:12px;">Truyện dài kỳ</span>
                ${storyDone ? iconSvg('crown', 18) : ''}
              </div>
              <div style="font-weight:800;font-size:16px;margin-bottom:4px;">${escapeHtml(stage.storyChapter.title)}</div>
              <p style="margin:0 0 12px;font-size:13px;color:var(--ink-muted);">${escapeHtml(stage.storyChapter.teaserVi)}</p>
              <a href="#/reading/${escapeHtml(storyId)}" class="btn btn-sm btn-read" style="width:100%;">Đọc Chương ${stage.id}</a>
            </div>

            <div style="padding:14px;border-radius:16px;background:var(--review-soft);border:1.5px solid var(--review);">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                <span class="chip" style="background:var(--surface);font-size:12px;">Kiểm tra 4 kỹ năng</span>
                ${testDone ? iconSvg('crown', 18) : ''}
              </div>
              <div style="font-weight:800;font-size:16px;margin-bottom:4px;">Tổng kết ${escapeHtml(stage.title)}</div>
              <p style="margin:0 0 12px;font-size:13px;color:var(--ink-muted);">8 câu trộn Giao tiếp · Đọc · Nghe · Viết (+60 XP & huy hiệu chặng).</p>
              <a href="#/stage-test/${escapeHtml(testId)}" class="btn btn-sm btn-review" style="width:100%;">${testDone ? 'Làm lại kiểm tra' : 'Kiểm tra cuối chặng'}</a>
            </div>
          </div>

          <!-- Other stages overview -->
          <div style="margin-top:8px;">
            <h3 style="margin:0 0 12px;font-size:17px;color:var(--ink-muted);">Các chặng khác trong lộ trình (28 chủ đề)</h3>
            ${curriculum.stages
              .filter((st) => st.id !== selectedStageId)
              .map((st) => renderStageBanner(st, false))
              .join('')}
          </div>
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
            <div style="font-size:12px;font-weight:800;text-transform:uppercase;color:var(--read-lip);">Truyện dài kỳ (4 chương)</div>
            <h3 style="margin:4px 0 8px;font-size:18px;">${escapeHtml(sidebarStoryMeta.title)}</h3>
            <p style="margin:0 0 12px;font-size:14px;color:var(--ink-muted);">${escapeHtml(sidebarStoryMeta.teaserVi)}</p>
            <div style="display:flex;gap:6px;margin-bottom:12px;">
              ${[1, 2, 3, 4]
                .map((c) => `<a href="#/reading/story-c${c}" class="btn btn-sm ${bookmarkedStoryId === `story-c${c}` ? 'btn-read' : 'btn-soft'}" style="flex:1;padding:4px 8px;">Ch.${c}</a>`)
                .join('')}
            </div>
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

    body.querySelectorAll<HTMLElement>('[data-select-stage]').forEach((b) => {
      b.addEventListener('click', () => {
        selectedStageId = Number(b.dataset.selectStage);
        render();
      });
    });

    // Node popover
    body.querySelectorAll<HTMLElement>('[data-lesson-node]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const lid = btn.dataset.lessonNode!;
        const lesson: LessonItem | undefined = lessonById.get(lid);
        if (!lesson || lesson.type === 'stage-test') return;
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
              <a href="${st.route(lesson.id, lesson.readingId)}" class="btn btn-comm" data-start-lesson style="flex:1;">BẮT ĐẦU (Enter)</a>
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
        const closeAndClean = () => {
          closeModal();
          setKey(null);
        };
        backdrop.addEventListener('click', (e) => {
          if (e.target === backdrop) closeAndClean();
        });
        backdrop.querySelector('[data-close-modal]')?.addEventListener('click', closeAndClean);
        backdrop.querySelector('[data-start-lesson]')?.addEventListener('click', () => {
          requestPersistentStorage();
          closeAndClean();
        });
        setKey((e) => {
          if (e.key === 'Escape') closeAndClean();
          else if (e.key === 'Enter') {
            backdrop.querySelector<HTMLAnchorElement>('[data-start-lesson]')?.click();
          }
        });
      });
    });

    // Grammar notebook modal on any stage
    body.querySelectorAll<HTMLElement>('[data-open-notebook]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const sid = Number(btn.dataset.openNotebook);
        const stObj = curriculum.stages.find((s) => s.id === sid);
        if (!stObj) return;
        closeModal();
        const backdrop = document.createElement('div');
        backdrop.className = 'modal-backdrop';
        backdrop.innerHTML = `
          <div class="modal-card" role="dialog" aria-label="Sổ tay ngữ pháp">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;">
              <h2 style="margin:0;">Sổ tay: ${escapeHtml(stObj.title)}</h2>
              <button type="button" class="btn btn-sm btn-soft" data-close-modal>${iconSvg('close', 16)}</button>
            </div>
            ${stObj.grammarNotes
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
        const closeAndClean = () => {
          closeModal();
          setKey(null);
        };
        backdrop.addEventListener('click', (e) => {
          if (e.target === backdrop) closeAndClean();
        });
        backdrop.querySelector('[data-close-modal]')?.addEventListener('click', closeAndClean);
        setKey((e) => {
          if (e.key === 'Escape') closeAndClean();
        });
      });
    });

    // Precache Stage N for offline
    body.querySelectorAll<HTMLButtonElement>('[data-cache-stage]').forEach((btn) => {
      btn.addEventListener('click', async () => {
        const sid = Number(btn.dataset.cacheStage);
        const statusEl = body.querySelector(`[data-cache-status="${sid}"]`) as HTMLElement;
        btn.disabled = true;
        const bundle = await loadStageBundle(sid);
        const urls = collectStageAssetUrls(sid, bundle.words, bundle.lessons, bundle.readings);
        if (statusEl) statusEl.textContent = `Đang tải sẵn ${urls.length} tệp Chặng ${sid}...`;
        const res = await precacheStageAssets(urls, (done, total) => {
          if (statusEl) statusEl.textContent = `Đã lưu ${done}/${total} tệp cho chế độ offline...`;
        });
        if (statusEl) statusEl.textContent = `Sẵn sàng offline: đã lưu ${res.ok}/${res.total} tệp Chặng ${sid}.`;
        btn.disabled = false;
      });
    });
  };

  await render();
  return () => {
    setKey(null);
    closeModal();
  };
}
