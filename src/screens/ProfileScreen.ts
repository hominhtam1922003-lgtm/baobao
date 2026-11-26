import confetti from 'canvas-confetti';
import { renderAppShell } from '../components/AppShell';
import { renderBaoSvg } from '../components/BaoMascot';
import { iconSvg } from '../components/Icons';
import { audioService } from '../services/audioPlayer';
import { getDb, type ProgressRecord } from '../services/db';
import { exportBackupJson, importBackupJson } from '../services/progressBackup';
import { ensureProgress, ensureSettings, saveSettings, todayIsoDate } from '../services/srsEngine';
import { escapeHtml } from '../utils/html';

const ACCESSORIES: { id: ProgressRecord['equippedAccessory']; label: string; reqXp: number }[] = [
  { id: 'none', label: 'Mặc định', reqXp: 0 },
  { id: 'bamboo-hat', label: 'Nón lá', reqXp: 30 },
  { id: 'red-scarf', label: 'Khăn đào', reqXp: 80 },
  { id: 'star-glasses', label: 'Kính sao', reqXp: 160 },
  { id: 'crown', label: 'Vương miện', reqXp: 300 },
];

const BADGES: { id: string; title: string; hint: string }[] = [
  { id: 'first-lesson', title: 'Bước chân đầu tiên', hint: 'Hoàn thành bài học đầu tiên' },
  { id: 'four-skills', title: 'Đủ 4 kỹ năng', hint: 'Hoàn thành 4 bài học' },
  { id: 'streak-7', title: 'Ngọn lửa 7 ngày', hint: 'Giữ streak 7 ngày liên tiếp' },
  { id: 'xp-100', title: 'Nhà du hành chăm chỉ', hint: 'Đạt 100 XP tích luỹ' },
];

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

  const closeModal = () => {
    modalEl?.remove();
    modalEl = null;
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
    const now = new Date();
    const daysInMonth = new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate();
    const ym = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;

    const calendarCells = Array.from({ length: daysInMonth }, (_, i) => {
      const day = i + 1;
      const iso = `${ym}-${String(day).padStart(2, '0')}`;
      const active = activeSet.has(iso);
      return `<span style="width:28px;height:28px;border-radius:9px;display:inline-flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;background:${
        active ? 'var(--write)' : 'var(--bg)'
      };border:1px solid ${active ? 'var(--write-lip)' : 'var(--border)'};">${day}</span>`;
    }).join('');

    const skillMax = Math.max(100, progress.skillXp.giaoTiep, progress.skillXp.doc, progress.skillXp.nghe, progress.skillXp.viet);
    const skills = [
      { label: 'Giao tiếp', xp: progress.skillXp.giaoTiep, color: 'var(--comm)' },
      { label: 'Đọc hiểu', xp: progress.skillXp.doc, color: 'var(--read)' },
      { label: 'Luyện nghe', xp: progress.skillXp.nghe, color: 'var(--listen)' },
      { label: 'Viết chữ', xp: progress.skillXp.viet, color: 'var(--write)' },
    ];

    body.innerHTML = `
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:18px;">
        <!-- 1. Danh tính & Tủ đồ của Bao -->
        <section class="clay-card" style="padding:22px;">
          <div style="display:flex;align-items:center;gap:14px;margin-bottom:14px;">
            ${renderBaoSvg({ mood: 'happy', size: 88, accessory: progress.equippedAccessory })}
            <div style="flex:1;">
              <div style="display:flex;gap:6px;align-items:center;">
                <input type="text" data-learner-name value="${escapeHtml(settings.learnerName)}" aria-label="Tên người học" style="font-size:20px;font-weight:800;border:1.5px solid var(--border);border-radius:12px;padding:4px 10px;width:100%;max-width:190px;background:var(--bg);" />
              </div>
              <div style="font-size:14px;font-weight:700;color:var(--ink-muted);margin-top:4px;">Nhà du hành cấp ${levelNum}</div>
              <div class="progress-track" style="height:10px;margin-top:6px;">
                <div class="progress-fill" style="width:${levelPct}%;background:var(--review);"></div>
              </div>
              <div style="font-size:12px;color:var(--ink-muted);margin-top:3px;">${progress.xp} XP (${levelPct}/100 lên cấp ${levelNum + 1})</div>
            </div>
          </div>
          <div style="font-weight:800;font-size:14px;margin-bottom:8px;">Tủ đồ của Bao (mở khoá bằng XP):</div>
          <div style="display:flex;flex-wrap:wrap;gap:8px;">
            ${ACCESSORIES.map((acc) => {
              const unlocked = progress.xp >= acc.reqXp || progress.unlockedAccessories.includes(acc.id);
              const equipped = progress.equippedAccessory === acc.id;
              return `<button type="button" class="btn btn-sm ${equipped ? 'btn-review' : 'btn-soft'}" data-equip-acc="${acc.id}" ${!unlocked ? 'disabled' : ''}>
                ${escapeHtml(acc.label)} ${!unlocked ? `(${acc.reqXp} XP)` : ''}
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
              <div style="font-size:13px;color:var(--ink-muted);">Kỷ lục: ${progress.bestStreak} ngày</div>
            </div>
            <button type="button" class="btn btn-sm btn-vocab" data-use-freeze ${progress.freezesLeft <= 0 ? 'disabled' : ''}>
              Đóng băng (${progress.freezesLeft})
            </button>
          </div>
          <div style="display:flex;flex-wrap:wrap;gap:5px;margin-top:10px;">${calendarCells}</div>
        </section>

        <!-- 3. Mục tiêu ngày -->
        <section class="clay-card" style="padding:22px;">
          <h2 style="margin:0 0 12px;font-size:19px;">Mục tiêu hằng ngày</h2>
          <p style="margin:0 0 12px;font-size:14px;color:var(--ink-muted);">Chọn nhịp độ học ngắn mỗi ngày — không phạt khi nghỉ.</p>
          <div style="display:flex;gap:8px;">
            ${([5, 10, 20] as const)
              .map(
                (m) => `<button type="button" class="btn ${settings.dailyGoalMinutes === m ? 'btn-read' : 'btn-soft'}" data-goal-min="${m}" style="flex:1;">${m} phút</button>`
              )
              .join('')}
          </div>
        </section>

        <!-- 4. Thành tích -->
        <section class="clay-card" style="padding:22px;">
          <h2 style="margin:0 0 12px;font-size:19px;">Thành tích</h2>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
            ${BADGES.map((b) => {
              const earned = progress.badges.includes(b.id);
              return `<div style="padding:10px;border-radius:14px;background:${earned ? 'var(--review-soft)' : 'var(--bg)'};border:1.5px solid ${earned ? 'var(--review)' : 'var(--border)'};opacity:${earned ? '1' : '0.68'};">
                <div style="font-weight:800;font-size:14px;">${earned ? iconSvg('crown', 14) : iconSvg('lock', 14)} ${escapeHtml(b.title)}</div>
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

    body.querySelector<HTMLInputElement>('[data-learner-name]')?.addEventListener('change', async (e) => {
      const name = (e.currentTarget as HTMLInputElement).value.trim() || 'Bạn mới';
      settings = await saveSettings({ learnerName: name });
      render();
    });

    body.querySelectorAll<HTMLElement>('[data-equip-acc]').forEach((b) => {
      b.addEventListener('click', async () => {
        const db = await getDb();
        progress = {
          ...progress,
          equippedAccessory: b.dataset.equipAcc as ProgressRecord['equippedAccessory'],
          updatedAt: new Date().toISOString(),
        };
        await db.put('progress', progress);
        render();
      });
    });

    body.querySelector('[data-use-freeze]')?.addEventListener('click', async () => {
      if (progress.freezesLeft <= 0) return;
      const db = await getDb();
      const today = todayIsoDate();
      progress = {
        ...progress,
        freezesLeft: progress.freezesLeft - 1,
        activeDates: Array.from(new Set([...progress.activeDates, today])),
        updatedAt: new Date().toISOString(),
      };
      await db.put('progress', progress);
      if ([7, 30, 100].includes(progress.streak)) {
        confetti({ particleCount: 50, spread: 70 });
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
            <li><strong>Danh sách từ vựng cộng đồng (complete-hsk-vocabulary):</strong> Dùng làm khung cấp độ nội bộ theo giấy phép <strong>MIT</strong>.</li>
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
    });
  };

  render();
  return () => closeModal();
}
