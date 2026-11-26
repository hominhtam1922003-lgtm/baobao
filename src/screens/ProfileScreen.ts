import confetti from 'canvas-confetti';
import { renderAppShell } from '../components/AppShell';
import { renderBaoSvg } from '../components/BaoMascot';
import { iconSvg } from '../components/Icons';
import { audioService } from '../services/audioPlayer';
import type { ProgressRecord } from '../services/db';
import { exportBackupJson, importBackupJson } from '../services/progressBackup';
import {
  BAO_ACCESSORIES,
  BAO_BADGES,
  ensureProgress,
  ensureSettings,
  equipAccessory,
  evaluateBadges,
  evaluateUnlockedAccessories,
  markMilestoneCelebrated,
  saveSettings,
  todayIsoDate,
  useStreakFreeze,
} from '../services/srsEngine';
import { escapeHtml } from '../utils/html';

export function applySettingsToDocument(s: { hanziSize: 'sm' | 'md' | 'lg'; reducedMotion: boolean; sfxEnabled: boolean }) {
  const html = document.documentElement;
  html.classList.remove('hanzi-sm', 'hanzi-md', 'hanzi-lg', 'reduced-motion');
  html.classList.add(`hanzi-${s.hanziSize}`);
  if (s.reducedMotion) html.classList.add('reduced-motion');
  audioService.setSfxEnabled(s.sfxEnabled);
}

export async function renderProfileScreen(root: HTMLElement): Promise<() => void> {
  let progress = await ensureProgress();
  let settings = await ensureSettings();
  let modalEl: HTMLElement | null = null;
  let keyHandler: ((e: KeyboardEvent) => void) | null = null;

  const setKey = (fn: ((e: KeyboardEvent) => void) | null) => {
    if (keyHandler) document.removeEventListener('keydown', keyHandler);
    keyHandler = fn;
    if (fn) document.addEventListener('keydown', fn);
  };

  const closeModal = () => {
    modalEl?.remove();
    modalEl = null;
    setKey(null);
  };

  const render = () => {
    const body = renderAppShell({
      root,
      activeTab: 'profile',
      title: 'Hồ sơ & Streak',
      progress,
      settings,
    });

    const levelNum = Math.floor(progress.xp / 100) + 1;
    const levelPct = progress.xp % 100;
    const activeSet = new Set(progress.activeDates);
    const frozenSet = new Set(progress.frozenDates ?? []);
    const now = new Date();
    const daysInMonth = new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate();
    const ym = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;

    const calendarCells = Array.from({ length: daysInMonth }, (_, i) => {
      const day = i + 1;
      const iso = `${ym}-${String(day).padStart(2, '0')}`;
      const active = activeSet.has(iso);
      const frozen = !active && frozenSet.has(iso);
      const bg = active ? 'var(--write)' : frozen ? 'var(--vocab-soft)' : 'var(--bg)';
      const border = active ? 'var(--write-lip)' : frozen ? 'var(--vocab)' : 'var(--border)';
      return `<span title="${frozen ? 'Đã đóng băng streak' : active ? 'Ngày có học' : ''}" style="width:28px;height:28px;border-radius:9px;display:inline-flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;background:${bg};border:1px solid ${border};">${day}</span>`;
    }).join('');

    const skillMax = Math.max(100, progress.skillXp.giaoTiep, progress.skillXp.doc, progress.skillXp.nghe, progress.skillXp.viet);
    const skills = [
      { label: 'Giao tiếp', xp: progress.skillXp.giaoTiep, color: 'var(--comm)' },
      { label: 'Đọc hiểu', xp: progress.skillXp.doc, color: 'var(--read)' },
      { label: 'Luyện nghe', xp: progress.skillXp.nghe, color: 'var(--listen)' },
      { label: 'Viết chữ', xp: progress.skillXp.viet, color: 'var(--write)' },
    ];

    const unlockedSet = new Set([...progress.unlockedAccessories, ...evaluateUnlockedAccessories(progress.xp)]);
    const earnedBadges = new Set([
      ...progress.badges,
      ...evaluateBadges({
        completedLessons: progress.completedLessons,
        streak: progress.streak,
        xp: progress.xp,
        completedStories: progress.completedStories,
        totalReviews: progress.totalReviews,
      }),
    ]);

    const activeMilestone = ([100, 30, 7] as const).find(
      (m) => progress.streak >= m && !(progress.celebratedMilestones ?? []).includes(m)
    );

    body.innerHTML = `
      ${
        activeMilestone
          ? `<div class="clay-card milestone-banner" style="padding:18px 22px;margin-bottom:18px;background:var(--review-soft);border:2px solid var(--review);display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;">
               <div style="display:flex;align-items:center;gap:12px;">
                 ${renderBaoSvg({ mood: 'celebrate', size: 64, accessory: progress.equippedAccessory })}
                 <div>
                   <div style="font-size:19px;font-weight:800;">Chúc mừng mốc Streak ${activeMilestone} ngày!</div>
                   <div style="font-size:14px;color:var(--ink-muted);">Thói quen bền bỉ thật đáng nể — tiếp tục giữ lửa cùng Bao nhé!</div>
                 </div>
               </div>
               <button type="button" class="btn btn-sm btn-review" data-dismiss-milestone="${activeMilestone}">Tuyệt vời!</button>
             </div>`
          : ''
      }

      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));gap:18px;">
        <!-- 1. Danh tính & Tủ đồ của Bao (8 món) -->
        <section class="clay-card" style="padding:22px;grid-column:span 1;">
          <div style="display:flex;align-items:center;gap:14px;margin-bottom:14px;">
            ${renderBaoSvg({ mood: 'happy', size: 88, accessory: progress.equippedAccessory })}
            <div style="flex:1;">
              <input type="text" data-learner-name value="${escapeHtml(settings.learnerName)}" aria-label="Tên người học" style="font-size:20px;font-weight:800;border:1.5px solid var(--border);border-radius:12px;padding:4px 10px;width:100%;max-width:200px;background:var(--bg);" />
              <div style="font-size:14px;font-weight:700;color:var(--ink-muted);margin-top:4px;">Nhà du hành cấp ${levelNum}</div>
              <div class="progress-track" style="height:10px;margin-top:6px;">
                <div class="progress-fill" style="width:${levelPct}%;background:var(--review);"></div>
              </div>
              <div style="font-size:12px;color:var(--ink-muted);margin-top:3px;">${progress.xp} XP (${levelPct}/100 lên cấp ${levelNum + 1})</div>
            </div>
          </div>
          <div style="font-weight:800;font-size:14px;margin-bottom:8px;">Tủ đồ của Bao (${unlockedSet.size + 1}/${BAO_ACCESSORIES.length} món mở khoá):</div>
          <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:8px;">
            ${BAO_ACCESSORIES.map((acc) => {
              const unlocked = acc.id === 'none' || unlockedSet.has(acc.id);
              const equipped = progress.equippedAccessory === acc.id;
              return `<button type="button" class="btn btn-sm ${equipped ? 'btn-review' : 'btn-soft'}" data-equip-acc="${acc.id}" ${!unlocked ? 'disabled' : ''} title="${escapeHtml(acc.desc)}" style="justify-content:flex-start;padding:6px 10px;text-align:left;min-height:54px;">
                ${renderBaoSvg({ mood: 'happy', size: 36, accessory: acc.id })}
                <span style="display:flex;flex-direction:column;line-height:1.2;">
                  <span style="font-size:13px;">${escapeHtml(acc.label)}</span>
                  <span style="font-size:11px;color:var(--ink-muted);font-weight:600;">${equipped ? 'Đang mặc' : unlocked ? 'Sẵn sàng' : `Mở ở ${acc.reqXp} XP`}</span>
                </span>
              </button>`;
            }).join('')}
          </div>
        </section>

        <!-- 2. Streak + Đóng băng -->
        <section class="clay-card" style="padding:22px;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
            <div>
              <div style="font-size:13px;font-weight:800;color:var(--ink-muted);">STREAK HIỆN TẠI</div>
              <div style="font-size:48px;font-weight:800;line-height:1;color:var(--write-lip);">${progress.streak}</div>
              <div style="font-size:13px;color:var(--ink-muted);">Kỷ lục: ${progress.bestStreak} ngày · Mốc thưởng: 7 / 30 / 100</div>
            </div>
            <button type="button" class="btn btn-sm btn-vocab" data-use-freeze ${progress.freezesLeft <= 0 ? 'disabled' : ''}>
              Đóng băng (${progress.freezesLeft})
            </button>
          </div>
          <div style="display:flex;flex-wrap:wrap;gap:5px;margin-top:10px;">${calendarCells}</div>
          <div style="display:flex;gap:12px;margin-top:10px;font-size:12px;color:var(--ink-muted);">
            <span><span style="display:inline-block;width:10px;height:10px;border-radius:3px;background:var(--write);margin-right:4px;"></span>Ngày học</span>
            <span><span style="display:inline-block;width:10px;height:10px;border-radius:3px;background:var(--vocab-soft);border:1px solid var(--vocab);margin-right:4px;"></span>Đóng băng</span>
          </div>
        </section>

        <!-- 3. Mục tiêu ngày & Phím tắt laptop -->
        <section class="clay-card" style="padding:22px;display:flex;flex-direction:column;justify-content:space-between;gap:14px;">
          <div>
            <h2 style="margin:0 0 10px;font-size:19px;">Mục tiêu hằng ngày</h2>
            <p style="margin:0 0 12px;font-size:14px;color:var(--ink-muted);">Chọn nhịp độ học ngắn mỗi ngày — không phạt khi nghỉ.</p>
            <div style="display:flex;gap:8px;">
              ${([5, 10, 20] as const)
                .map(
                  (m) => `<button type="button" class="btn ${settings.dailyGoalMinutes === m ? 'btn-read' : 'btn-soft'}" data-goal-min="${m}" style="flex:1;">${m} phút</button>`
                )
                .join('')}
            </div>
          </div>
          <div style="padding:12px;border-radius:14px;background:var(--bg);border:1.5px solid var(--border);font-size:13px;">
            <div style="font-weight:800;margin-bottom:6px;">Phím tắt laptop nhanh</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:4px 10px;color:var(--ink-muted);">
              <span><strong>Space</strong>: Phát audio / Lật thẻ / Xem nét</span>
              <span><strong>1–4</strong>: Chọn đáp án / Chấm thẻ</span>
              <span><strong>Enter</strong>: Kiểm tra / Tiếp tục</span>
              <span><strong>← / →</strong>: Tua câu nghe & đọc</span>
              <span><strong>P / S / R</strong>: Pinyin / Chậm / Viết lại</span>
              <span><strong>Esc</strong>: Đóng cửa sổ phụ</span>
            </div>
          </div>
        </section>

        <!-- 4. Thành tích (12 huy hiệu) -->
        <section class="clay-card" style="padding:22px;">
          <h2 style="margin:0 0 12px;font-size:19px;">Thành tích (${earnedBadges.size}/${BAO_BADGES.length})</h2>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
            ${BAO_BADGES.map((b) => {
              const earned = earnedBadges.has(b.id);
              return `<div style="padding:10px;border-radius:14px;background:${earned ? 'var(--review-soft)' : 'var(--bg)'};border:1.5px solid ${earned ? 'var(--review)' : 'var(--border)'};opacity:${earned ? '1' : '0.68'};">
                <div style="font-weight:800;font-size:13px;">${earned ? iconSvg('crown', 14) : iconSvg('lock', 14)} ${escapeHtml(b.title)}</div>
                <div style="font-size:12px;color:var(--ink-muted);margin-top:3px;">${escapeHtml(b.hint)}</div>
              </div>`;
            }).join('')}
          </div>
        </section>

        <!-- 5. 4 Kỹ năng -->
        <section class="clay-card" style="padding:22px;">
          <h2 style="margin:0 0 12px;font-size:19px;">Kỹ năng</h2>
          <div style="display:flex;flex-direction:column;gap:12px;">
            ${skills
              .map(
                (sk) => `
              <div>
                <div style="display:flex;justify-content:space-between;font-size:14px;font-weight:700;margin-bottom:4px;">
                  <span>${escapeHtml(sk.label)}</span><span>${sk.xp} XP</span>
                </div>
                <div class="progress-track" style="height:10px;">
                  <div class="progress-fill" style="width:${Math.min(100, Math.round((sk.xp / skillMax) * 100))}%;background:${sk.color};"></div>
                </div>
              </div>`
              )
              .join('')}
          </div>
        </section>

        <!-- 6. Cài đặt & Sao lưu -->
        <section class="clay-card" style="padding:22px;">
          <h2 style="margin:0 0 12px;font-size:19px;">Cài đặt & Dữ liệu</h2>
          <div style="display:flex;flex-direction:column;gap:10px;">
            <div>
              <div style="font-size:13px;font-weight:700;margin-bottom:4px;">Pinyin mặc định</div>
              <div class="segmented">
                <button type="button" data-set-py="all" aria-pressed="${settings.pinyinMode === 'all'}">Tất cả</button>
                <button type="button" data-set-py="new" aria-pressed="${settings.pinyinMode === 'new'}">Từ mới</button>
                <button type="button" data-set-py="off" aria-pressed="${settings.pinyinMode === 'off'}">Tắt</button>
              </div>
            </div>

            <div>
              <div style="font-size:13px;font-weight:700;margin-bottom:4px;">Cỡ chữ Hán</div>
              <div class="segmented">
                <button type="button" data-set-hz="sm" aria-pressed="${settings.hanziSize === 'sm'}">Vừa</button>
                <button type="button" data-set-hz="md" aria-pressed="${settings.hanziSize === 'md'}">Lớn</button>
                <button type="button" data-set-hz="lg" aria-pressed="${settings.hanziSize === 'lg'}">Rất lớn</button>
              </div>
            </div>

            <div style="display:flex;gap:8px;flex-wrap:wrap;">
              <button type="button" class="btn btn-sm ${settings.sfxEnabled ? 'btn-read' : 'btn-soft'}" data-toggle-sfx>Âm thanh: ${settings.sfxEnabled ? 'Bật' : 'Tắt'}</button>
              <button type="button" class="btn btn-sm ${settings.reducedMotion ? 'btn-read' : 'btn-soft'}" data-toggle-motion>Giảm chuyển động: ${settings.reducedMotion ? 'Bật' : 'Tắt'}</button>
            </div>

            <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:6px;">
              <button type="button" class="btn btn-sm btn-vocab" data-export-json>Xuất tiến độ (JSON)</button>
              <label class="btn btn-sm btn-soft" style="cursor:pointer;">
                Nhập tiến độ (JSON)
                <input type="file" accept="application/json" data-import-json style="display:none;" />
              </label>
            </div>
            <div data-backup-msg style="font-size:13px;font-weight:700;"></div>

            <button type="button" class="btn btn-sm btn-soft" data-open-credits>Về ứng dụng & Giấy phép dữ liệu</button>
          </div>
        </section>
      </div>
    `;

    if (activeMilestone && !settings.reducedMotion) {
      confetti({ particleCount: 55, spread: 75, origin: { y: 0.65 } });
    }

    body.querySelector<HTMLElement>('[data-dismiss-milestone]')?.addEventListener('click', async (e) => {
      const m = Number((e.currentTarget as HTMLElement).dataset.dismissMilestone);
      await markMilestoneCelebrated(m);
      progress = await ensureProgress();
      render();
    });

    body.querySelector<HTMLInputElement>('[data-learner-name]')?.addEventListener('change', async (e) => {
      const name = (e.currentTarget as HTMLInputElement).value.trim() || 'Bạn mới';
      settings = await saveSettings({ learnerName: name });
      render();
    });

    body.querySelectorAll<HTMLElement>('[data-equip-acc]').forEach((b) => {
      b.addEventListener('click', async () => {
        progress = await equipAccessory(b.dataset.equipAcc as ProgressRecord['equippedAccessory']);
        audioService.playSfx('pop');
        render();
      });
    });

    body.querySelector('[data-use-freeze]')?.addEventListener('click', async () => {
      progress = await useStreakFreeze();
      audioService.playSfx('ok');
      if ([7, 30, 100].includes(progress.streak) && !settings.reducedMotion) {
        confetti({ particleCount: 55, spread: 70 });
      }
      render();
    });

    body.querySelectorAll<HTMLElement>('[data-goal-min]').forEach((b) => {
      b.addEventListener('click', async () => {
        settings = await saveSettings({ dailyGoalMinutes: Number(b.dataset.goalMin) as 5 | 10 | 20 });
        render();
      });
    });

    body.querySelectorAll<HTMLElement>('[data-set-py]').forEach((b) => {
      b.addEventListener('click', async () => {
        settings = await saveSettings({ pinyinMode: b.dataset.setPy as 'all' | 'new' | 'off' });
        render();
      });
    });

    body.querySelectorAll<HTMLElement>('[data-set-hz]').forEach((b) => {
      b.addEventListener('click', async () => {
        settings = await saveSettings({ hanziSize: b.dataset.setHz as 'sm' | 'md' | 'lg' });
        applySettingsToDocument(settings);
        render();
      });
    });

    body.querySelector('[data-toggle-sfx]')?.addEventListener('click', async () => {
      settings = await saveSettings({ sfxEnabled: !settings.sfxEnabled });
      applySettingsToDocument(settings);
      render();
    });

    body.querySelector('[data-toggle-motion]')?.addEventListener('click', async () => {
      settings = await saveSettings({ reducedMotion: !settings.reducedMotion });
      applySettingsToDocument(settings);
      render();
    });

    body.querySelector('[data-export-json]')?.addEventListener('click', async () => {
      const raw = await exportBackupJson();
      const blob = new Blob([raw], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `baobao-tien-do-${todayIsoDate()}.json`;
      a.click();
      URL.revokeObjectURL(url);
      const msg = body.querySelector('[data-backup-msg]') as HTMLElement;
      msg.textContent = 'Đã xuất file tiến độ JSON.';
    });

    body.querySelector<HTMLInputElement>('[data-import-json]')?.addEventListener('change', async (e) => {
      const file = (e.currentTarget as HTMLInputElement).files?.[0];
      if (!file) return;
      const text = await file.text();
      const confirmed = window.confirm('Nhập file sẽ tự động sao lưu bản hiện tại rồi ghi đè dữ liệu. Tiếp tục?');
      if (!confirmed) return;
      const res = await importBackupJson(text);
      const msg = body.querySelector('[data-backup-msg]') as HTMLElement;
      if (res.ok) {
        progress = await ensureProgress();
        settings = await ensureSettings();
        applySettingsToDocument(settings);
        render();
        const msgAfter = root.querySelector('[data-backup-msg]') as HTMLElement | null;
        if (msgAfter) msgAfter.textContent = 'Đã khôi phục tiến độ thành công!';
      } else {
        msg.style.color = 'var(--comm-lip)';
        msg.textContent = res.error ?? 'File nhập bị lỗi.';
      }
    });

    body.querySelector('[data-open-credits]')?.addEventListener('click', () => {
      closeModal();
      const backdrop = document.createElement('div');
      backdrop.className = 'modal-backdrop';
      backdrop.innerHTML = `
        <div class="modal-card" role="dialog" aria-label="Về ứng dụng BaoBao">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
            <h2 style="margin:0;">Về BaoBao & Nguồn dữ liệu mở</h2>
            <button type="button" class="btn btn-sm btn-soft" data-cred-close>${iconSvg('close', 16)}</button>
          </div>
          <p style="margin:0 0 12px;">Ứng dụng học tiếng Trung tĩnh, offline hoàn toàn, không tài khoản, không Hearts/Energy.</p>
          <ul style="padding-left:18px;margin:0;display:flex;flex-direction:column;gap:8px;font-size:14px;">
            <li><strong>CC-CEDICT:</strong> Dữ liệu từ điển tiếng Trung mở theo giấy phép <strong>CC BY-SA 4.0</strong>.</li>
            <li><strong>Tatoeba:</strong> Câu ví dụ ngữ liệu mở theo giấy phép <strong>CC BY 2.0 FR</strong> (chỉ dùng dữ liệu câu).</li>
            <li><strong>Arphic Technology + Make Me A Hanzi + hanzi-writer-data:</strong> Dữ liệu nét chữ theo <strong>Arphic Public License</strong> & <strong>LGPL v3+</strong>.</li>
            <li><strong>Danh sách từ vựng cộng đồng (drkameleon):</strong> Dùng làm khung cấp độ nội bộ theo giấy phép <strong>MIT</strong>.</li>
            <li><strong>Audio:</strong> Tổng hợp offline cho toàn bộ bài học, không dùng audio bên ngoài lúc chạy.</li>
          </ul>
        </div>
      `;
      document.body.appendChild(backdrop);
      modalEl = backdrop;
      backdrop.addEventListener('click', (e) => {
        if (e.target === backdrop) closeModal();
      });
      backdrop.querySelector('[data-cred-close]')?.addEventListener('click', closeModal);
      setKey((ev) => {
        if (ev.key === 'Escape') closeModal();
      });
    });
  };

  render();
  return () => closeModal();
}
