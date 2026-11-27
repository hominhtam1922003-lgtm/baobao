import confetti from 'canvas-confetti';
import { renderAppShell } from '../components/AppShell';
import { renderBaoSvg } from '../components/BaoMascot';
import { iconSvg, stickerBadge, type IconName } from '../components/Icons';
import { audioService } from '../services/audioPlayer';
import {
  collectStageAssetUrls,
  loadCurriculum,
  loadStageBundle,
} from '../services/contentLoader';
import { precacheStageAssets, requestPersistentStorage } from '../services/pwa';
import { resolveWardrobe } from '../services/shopCatalog';
import {
  ensureProgress,
  ensureSettings,
  filterQueue,
  getAllCards,
  getCoins,
  getTodayXp,
} from '../services/srsEngine';
import type { LessonItem, StageMeta, TopicMeta } from '../types/curriculum';
import { escapeHtml } from '../utils/html';

const TYPE_STYLE: Record<
  'giao-tiep' | 'doc' | 'nghe' | 'viet',
  { color: string; lip: string; soft: string; icon: IconName; label: string; route: (id: string, readingId?: string) => string }
> = {
  'giao-tiep': { color: 'var(--comm)', lip: 'var(--comm-lip)', soft: 'var(--comm-soft)', icon: 'comm', label: 'Giao tiếp', route: (id) => `#/lesson/${id}` },
  doc: { color: 'var(--read)', lip: 'var(--read-lip)', soft: 'var(--read-soft)', icon: 'read', label: 'Đọc hiểu', route: (_id, rid) => `#/reading/${rid ?? 'r-t1'}` },
  nghe: { color: 'var(--listen)', lip: 'var(--listen-lip)', soft: 'var(--listen-soft)', icon: 'listen', label: 'Luyện nghe', route: (id) => `#/listening/${id}` },
  viet: { color: 'var(--write)', lip: 'var(--write-lip)', soft: 'var(--write-soft)', icon: 'write', label: 'Viết chữ', route: (id) => `#/writing/${id}` },
};

const STAGE_PALETTE: Record<string, { bg: string; lip: string }> = {
  comm: { bg: 'var(--comm-soft)', lip: 'var(--comm)' },
  read: { bg: 'var(--read-soft)', lip: 'var(--read)' },
  review: { bg: 'var(--review-soft)', lip: 'var(--review)' },
  write: { bg: 'var(--write-soft)', lip: 'var(--write)' },
};

const MAP_CHEERS = [
  '加油！(Jiā yóu!) Hôm nay mình chinh phục thêm 1 bài nhé!',
  'Học xong 1 bài là nhận ngay +30~55 Xu Tre sắm đồ siêu xinh!',
  'Bạn đã biết chưa? Bấm vào từng chữ Hán trong bài để xem mẹo nhớ!',
  'Tiệm của Bao có tận 28 món mũ, áo, kính và trà sữa đang chờ đó!',
];

export async function renderMapScreen(root: HTMLElement): Promise<() => void> {
  const [curriculum, progress, settings, cards] = await Promise.all([
    loadCurriculum(),
    ensureProgress(),
    ensureSettings(),
    getAllCards(),
  ]);

  const completedSet = new Set(progress.completedLessons);
  const wardrobe = resolveWardrobe(progress);
  const coins = getCoins(progress);

  const stageCompletionRatio = (st: StageMeta): number => {
    const ids = st.topics.flatMap((t) => t.lessonIds);
    if (ids.length === 0) return 0;
    const done = ids.filter((id) => completedSet.has(id)).length;
    return done / ids.length;
  };

  let selectedStageId = 1;
  for (const st of curriculum.stages) {
    if (stageCompletionRatio(st) < 1) {
      selectedStageId = st.id;
      break;
    }
    selectedStageId = st.id;
  }

  let cheerIdx = 0;
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
      title: 'Hành trình du học cùng Bao',
      progress,
      settings,
    });

    const stage = curriculum.stages.find((s) => s.id === selectedStageId) ?? curriculum.stages[0];
    const { lessons, words } = await loadStageBundle(stage.id);
    const lessonById = new Map(lessons.map((l) => [l.id, l]));
    const wordById = new Map(words.map((w) => [w.id, w]));

    const playableIds = stage.topics.flatMap((tp) => (tp.ready ? tp.lessonIds : []));
    const currentLessonId = playableIds.find((id) => !completedSet.has(id)) ?? playableIds[0];
    const currentLesson = lessonById.get(currentLessonId);
    const currentTopic = stage.topics.find((t) => t.lessonIds.includes(currentLessonId)) ?? stage.topics[0];
    const currentStyle = currentLesson && currentLesson.type !== 'stage-test' ? TYPE_STYLE[currentLesson.type] : TYPE_STYLE['giao-tiep'];

    const renderTopicJourneyCard = (topic: TopicMeta, tIdx: number) => {
      const gtLesson = lessonById.get(topic.lessonIds[0]);
      const topicDoneCount = topic.lessonIds.filter((id) => completedSet.has(id)).length;
      const isTopicDone = topicDoneCount === topic.lessonIds.length;
      const isCurrentTopic = topic.lessonIds.includes(currentLessonId);
      const previewHanzi = (gtLesson?.newWords ?? [])
        .slice(0, 5)
        .map((wid) => wordById.get(wid)?.hanzi)
        .filter(Boolean)
        .join(' · ');

      const nodesHtml = topic.lessonIds
        .map((lid) => {
          const lesson = lessonById.get(lid);
          if (!lesson || lesson.type === 'stage-test') return '';
          const st = TYPE_STYLE[lesson.type];
          const isDone = completedSet.has(lid);
          const isCurrent = lid === currentLessonId;
          const coinBonus = lesson.coinReward ?? (lesson.type === 'giao-tiep' ? 40 : 30);

          const nodeStyle = `width:68px;height:68px;border-radius:999px;border:3px solid #FFFFFF;background:${st.color};box-shadow:0 5px 0 ${st.lip}, var(--shadow-clay);display:flex;align-items:center;justify-content:center;position:relative;color:#3D3654;margin:0 auto;${
            isCurrent ? 'animation:baoBounce 1.8s ease-in-out infinite;' : ''
          }`;

          return `
            <div style="display:flex;flex-direction:column;align-items:center;text-align:center;padding:8px 4px;border-radius:18px;background:${
              isCurrent ? st.soft : 'var(--bg)'
            };border:1.5px solid ${isCurrent ? st.color : 'var(--border)'};">
              <button type="button" data-lesson-node="${escapeHtml(lid)}" style="${nodeStyle}" aria-label="${escapeHtml(lesson.title)}">
                ${stickerBadge(st.icon, st.color, 38)}
                ${
                  isDone
                    ? `<span style="position:absolute;top:-6px;right:-6px;width:24px;height:24px;border-radius:999px;background:var(--review);border:2px solid #FFF;display:flex;align-items:center;justify-content:center;">${iconSvg('crown', 13)}</span>`
                    : ''
                }
              </button>
              <div style="margin-top:8px;font-size:14px;font-weight:800;">${escapeHtml(st.label)}</div>
              <div style="font-size:11px;font-weight:700;color:var(--ink-muted);">+${lesson.xp} XP · 🎋+${coinBonus}</div>
              ${
                lesson.type === 'giao-tiep'
                  ? `<a href="#/dialogue/${escapeHtml(lid)}" style="font-size:11px;color:var(--comm-lip);font-weight:800;margin-top:3px;text-decoration:none;">💬 Hội thoại riêng →</a>`
                  : ''
              }
            </div>
          `;
        })
        .join('');

      return `
        ${
          tIdx > 0
            ? `<div style="display:flex;flex-direction:column;align-items:center;margin:-10px 0 12px;">
                 <div style="width:3px;height:16px;border-left:3px dashed var(--border-path);"></div>
                 <span class="chip" style="font-size:11px;padding:3px 10px;background:var(--surface);color:var(--ink-muted);">↓ ${escapeHtml(topic.connectsFromVi ?? `Nối tiếp Bài ${topic.id - 1}`)}</span>
                 <div style="width:3px;height:14px;border-left:3px dashed var(--border-path);"></div>
               </div>`
            : ''
        }
        <section class="clay-card topic-journey-card" style="${
          isCurrentTopic ? 'border-color:var(--comm);box-shadow:0 6px 0 rgba(255,107,129,0.22), var(--shadow-clay);' : ''
        }">
          <div class="topic-journey-header">
            <div style="flex:1;min-width:220px;">
              <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:4px;">
                <span class="chip" style="font-size:12px;padding:3px 10px;background:${isTopicDone ? 'var(--read-soft)' : 'var(--comm-soft)'};border-color:${
                  isTopicDone ? 'var(--read)' : 'var(--comm)'
                };">
                  Chủ đề ${topic.id} ${isTopicDone ? '✓ Hoàn thành' : isCurrentTopic ? '★ Đang học' : ''}
                </span>
                ${
                  topic.storyTagVi
                    ? `<span class="chip" style="font-size:12px;padding:3px 10px;background:var(--review-soft);border-color:var(--review);">📖 ${escapeHtml(topic.storyTagVi)}</span>`
                    : ''
                }
              </div>
              <h3 style="margin:2px 0;font-size:20px;font-weight:800;">${escapeHtml(topic.title)}</h3>
              <div style="font-size:14px;color:var(--ink-muted);">${escapeHtml(topic.subtitle)}</div>
              ${
                previewHanzi
                  ? `<div style="margin-top:6px;font-size:13px;color:var(--ink-muted);">Từ trọng tâm: <span class="hanzi" style="font-size:20px;color:var(--ink);font-weight:600;">${escapeHtml(previewHanzi)}</span></div>`
                  : ''
              }
            </div>
            <div style="display:flex;flex-direction:column;align-items:flex-end;gap:6px;">
              <span class="chip" style="font-size:12px;">${topicDoneCount}/${topic.lessonIds.length} kỹ năng</span>
              ${
                isCurrentTopic
                  ? renderBaoSvg({ mood: 'wave', size: 58, wardrobe })
                  : ''
              }
            </div>
          </div>

          <div class="topic-nodes-row">
            ${nodesHtml}
          </div>
        </section>
      `;
    };

    const renderStageBanner = (st: StageMeta, active: boolean) => {
      const palette = STAGE_PALETTE[st.colorToken] ?? STAGE_PALETTE.comm;
      const ratioPct = Math.round(stageCompletionRatio(st) * 100);
      const cardBg = active ? palette.bg : 'var(--surface)';
      const cardBorder = active ? palette.lip : 'var(--border)';

      return `
        <section class="clay-card" style="padding:20px;margin-bottom:18px;background:${cardBg};border-color:${cardBorder};">
          <div style="display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;">
            <div style="display:flex;align-items:center;gap:12px;">
              ${active ? renderBaoSvg({ mood: 'backpack', size: 68, wardrobe }) : ''}
              <div>
                <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
                  <h2 style="margin:0;font-size:22px;font-weight:800;">${escapeHtml(st.title)}</h2>
                  <span class="chip" style="font-size:12px;">${ratioPct}% hoàn thành</span>
                </div>
                <p style="margin:4px 0 0;color:var(--ink-muted);font-size:14px;">${escapeHtml(st.subtitle)}</p>
              </div>
            </div>
            <div style="display:flex;gap:8px;flex-wrap:wrap;">
              ${
                st.grammarNotes.length > 0
                  ? `<button type="button" class="btn btn-sm btn-soft" data-open-notebook="${st.id}">${iconSvg('book', 16)} Sổ tay ngữ pháp</button>`
                  : ''
              }
              <button type="button" class="btn btn-sm btn-soft" data-cache-stage="${st.id}">${iconSvg('download', 16)} Tải offline</button>
              ${
                !active
                  ? `<button type="button" class="btn btn-sm btn-comm" data-select-stage="${st.id}">Mở Chặng ${st.id}</button>`
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

    const stageTabsHtml = curriculum.stages
      .map((st) => {
        const donePct = Math.round(stageCompletionRatio(st) * 100);
        return `<button type="button" class="btn btn-sm ${st.id === selectedStageId ? 'btn-comm' : 'btn-soft'}" data-select-stage="${st.id}">
          Chặng ${st.id} · ${donePct}%
        </button>`;
      })
      .join('');

    body.innerHTML = `
      <!-- Welcome Hero & Continue Learning Banner -->
      <section class="clay-card" style="padding:20px 24px;margin-bottom:18px;background:linear-gradient(135deg, #FFF1F3 0%, #FFFBF3 52%, #D9F6EF 100%);border-color:var(--comm);display:flex;align-items:center;justify-content:space-between;gap:18px;flex-wrap:wrap;">
        <div style="display:flex;align-items:center;gap:16px;flex:1;min-width:260px;">
          <button type="button" data-map-pet style="border:none;background:transparent;padding:0;" aria-label="Chơi với Bao">
            ${renderBaoSvg({ mood: 'celebrate', size: 96, wardrobe, interactive: true })}
          </button>
          <div>
            <div style="font-size:13px;font-weight:800;color:var(--comm-lip);">✨ Chào ${escapeHtml(settings.learnerName)}!</div>
            <h2 style="margin:2px 0 4px;font-size:21px;font-weight:800;">Tiếp tục: Chủ đề ${currentTopic.id} — ${escapeHtml(currentTopic.title)}</h2>
            <div data-map-cheer style="font-size:14px;color:var(--ink-muted);">${escapeHtml(MAP_CHEERS[cheerIdx % MAP_CHEERS.length])}</div>
          </div>
        </div>
        <div style="display:flex;gap:10px;flex-wrap:wrap;">
          ${
            currentLesson
              ? `<a href="${currentStyle.route(currentLesson.id, currentLesson.readingId)}" class="btn btn-comm btn-lg">Học tiếp ngay →</a>`
              : ''
          }
          <a href="#/shop" class="btn btn-review">🛍️ Tiệm Bao (🎋 ${coins})</a>
        </div>
      </section>

      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px;" role="tablist" aria-label="Chọn chặng học">
        ${stageTabsHtml}
      </div>

      <div style="display:grid;grid-template-columns:minmax(0,750px) minmax(260px,330px);gap:24px;align-items:start;" class="map-grid">
        <div>
          ${renderStageBanner(stage, true)}
          ${stage.topics.map((tp, idx) => renderTopicJourneyCard(tp, idx)).join('')}

          <!-- Stage Story Chapter & End-of-Stage Mixed Test -->
          <div class="clay-card" style="padding:20px;margin:8px 0 28px;display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;">
            <div style="padding:16px;border-radius:18px;background:var(--read-soft);border:2px solid var(--read);">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                <span class="chip" style="background:var(--surface);font-size:12px;">📖 Truyện dài kỳ · 🎋+35</span>
                ${storyDone ? iconSvg('crown', 18) : ''}
              </div>
              <div style="font-weight:800;font-size:16px;margin-bottom:4px;">${escapeHtml(stage.storyChapter.title)}</div>
              <p style="margin:0 0 12px;font-size:13px;color:var(--ink-muted);">${escapeHtml(stage.storyChapter.teaserVi)}</p>
              <a href="#/reading/${escapeHtml(storyId)}" class="btn btn-sm btn-read" style="width:100%;">Đọc Chương ${stage.id} →</a>
            </div>

            <div style="padding:16px;border-radius:18px;background:var(--review-soft);border:2px solid var(--review);">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                <span class="chip" style="background:var(--surface);font-size:12px;">🏆 Kiểm tra 4 kỹ năng · 🎋+100</span>
                ${testDone ? iconSvg('crown', 18) : ''}
              </div>
              <div style="font-weight:800;font-size:16px;margin-bottom:4px;">Tổng kết ${escapeHtml(stage.title)}</div>
              <p style="margin:0 0 12px;font-size:13px;color:var(--ink-muted);">8 câu trộn Giao tiếp · Đọc · Nghe · Viết (+60 XP, +100 Xu Tre & huy hiệu).</p>
              <a href="#/stage-test/${escapeHtml(testId)}" class="btn btn-sm btn-review" style="width:100%;">${testDone ? 'Làm lại kiểm tra' : 'Kiểm tra cuối chặng →'}</a>
            </div>
          </div>

          <!-- Other stages overview -->
          <div style="margin-top:8px;">
            <h3 style="margin:0 0 12px;font-size:17px;color:var(--ink-muted);">Các chặng khác trong lộ trình (28 chủ đề liên kết)</h3>
            ${curriculum.stages
              .filter((st) => st.id !== selectedStageId)
              .map((st) => renderStageBanner(st, false))
              .join('')}
          </div>
        </div>

        <aside style="display:flex;flex-direction:column;gap:16px;position:sticky;top:20px;">
          <!-- Cute BaoBao Wardrobe & Coin Companion Card -->
          <div class="clay-card" style="padding:18px;text-align:center;background:linear-gradient(180deg, #FFFFFF 0%, #FFF6D6 100%);border-color:var(--review);">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
              <span class="chip" style="font-size:12px;background:var(--surface);">🐼 Gấu trúc Bao</span>
              <span class="chip coin-chip" style="font-size:13px;">🎋 ${coins} Xu</span>
            </div>
            ${renderBaoSvg({ mood: 'love', size: 120, wardrobe, interactive: true })}
            <p style="margin:6px 0 12px;font-size:13px;color:var(--ink-muted);">Học thêm bài để nhận Xu Tre sắm mũ, áo hoodie, kính sao & trà sữa cho Bao!</p>
            <a href="#/shop" class="btn btn-comm btn-sm" style="width:100%;">🛍️ Mở Tiệm Thời Trang Bao</a>
          </div>

          <div class="clay-card" style="padding:18px;">
            <h2 style="margin:0 0 12px;font-size:18px;">Mục tiêu hôm nay</h2>
            <div style="display:flex;align-items:center;gap:14px;margin-bottom:14px;">
              <div style="width:62px;height:62px;border-radius:999px;background:conic-gradient(var(--read) ${pct * 3.6}deg, var(--border) 0deg);display:flex;align-items:center;justify-content:center;">
                <div style="width:46px;height:46px;border-radius:999px;background:var(--surface);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:13px;">${pct}%</div>
              </div>
              <div>
                <div style="font-weight:800;">${settings.dailyGoalMinutes} phút/ngày (+40 Xu)</div>
                <div style="font-size:13px;color:var(--ink-muted);">${dueCount} thẻ đến hạn ôn tập</div>
              </div>
            </div>
            <a href="#/review" class="btn btn-review btn-sm" style="width:100%;">Ôn tập Flashcard (${dueCount})</a>
          </div>

          <div class="clay-card" style="padding:18px;background:var(--read-soft);border-color:var(--read);">
            <div style="font-size:12px;font-weight:800;text-transform:uppercase;color:var(--read-lip);">Truyện dài kỳ (4 chương)</div>
            <h3 style="margin:4px 0 8px;font-size:17px;">${escapeHtml(stage.storyChapter.title)}</h3>
            <p style="margin:0 0 12px;font-size:13px;color:var(--ink-muted);">${escapeHtml(stage.storyChapter.teaserVi)}</p>
            <div style="display:flex;gap:6px;margin-bottom:10px;">
              ${[1, 2, 3, 4]
                .map((c) => `<a href="#/reading/story-c${c}" class="btn btn-sm ${stage.id === c ? 'btn-read' : 'btn-soft'}" style="flex:1;padding:4px 8px;">Ch.${c}</a>`)
                .join('')}
            </div>
            <a href="#/reading/${escapeHtml(storyId)}" class="btn btn-read btn-sm" style="width:100%;">Đọc Chương ${stage.id}</a>
          </div>
        </aside>
      </div>
      <style>
        @media (max-width: 960px) {
          .map-grid { grid-template-columns: 1fr !important; }
        }
      </style>
    `;

    body.querySelector('[data-map-pet]')?.addEventListener('click', () => {
      cheerIdx = (cheerIdx + 1) % MAP_CHEERS.length;
      audioService.playSfx('pop');
      const el = body.querySelector('[data-map-cheer]');
      if (el) el.textContent = MAP_CHEERS[cheerIdx];
      if (!settings.reducedMotion) {
        confetti({ particleCount: 16, spread: 45, origin: { x: 0.25, y: 0.25 } });
      }
    });

    body.querySelectorAll<HTMLElement>('[data-select-stage]').forEach((b) => {
      b.addEventListener('click', () => {
        selectedStageId = Number(b.dataset.selectStage);
        render();
      });
    });

    // Node preview modal
    body.querySelectorAll<HTMLElement>('[data-lesson-node]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const lid = btn.dataset.lessonNode!;
        const lesson: LessonItem | undefined = lessonById.get(lid);
        if (!lesson || lesson.type === 'stage-test') return;
        const st = TYPE_STYLE[lesson.type];
        const coinBonus = lesson.coinReward ?? (lesson.type === 'giao-tiep' ? 40 : 30);
        closeModal();
        const backdrop = document.createElement('div');
        backdrop.className = 'modal-backdrop';
        backdrop.innerHTML = `
          <div class="modal-card" role="dialog" aria-label="${escapeHtml(lesson.title)}">
            <div style="display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:12px;flex-wrap:wrap;">
              <span class="chip" style="background:${st.color};">${escapeHtml(st.label)}</span>
              <div style="display:flex;gap:6px;">
                <span class="chip">+${lesson.xp} XP</span>
                <span class="chip coin-chip">🎋 +${coinBonus} Xu</span>
              </div>
            </div>
            <h2 style="margin:0 0 8px;">${escapeHtml(lesson.title)}</h2>
            ${
              lesson.storyContextVi
                ? `<div style="padding:12px 14px;border-radius:16px;background:var(--comm-chat-bg);border:1.5px solid var(--comm);font-size:14px;margin-bottom:12px;">
                     <strong>📖 Bối cảnh:</strong> ${escapeHtml(lesson.storyContextVi)}
                   </div>`
                : ''
            }
            <p style="margin:0 0 16px;color:var(--ink-muted);font-size:14px;">
              ${
                lesson.type === 'giao-tiep'
                  ? `Gồm ${lesson.newWords.length} từ trọng tâm kèm mẹo nhớ, ngữ pháp chi tiết, ghép cặp vui, luyện tập & đóng vai!`
                  : lesson.type === 'doc'
                  ? 'Đọc hiểu bấm tra từng từ, nghe karaoke & trả lời câu hỏi.'
                  : lesson.type === 'nghe'
                  ? '6 bài nghe đa dạng kèm tốc độ chậm 0.75× thật & chép chính tả.'
                  : 'Tập viết theo thứ tự nét chuẩn kèm giải thích bộ thủ & mini-quiz.'
              }
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
