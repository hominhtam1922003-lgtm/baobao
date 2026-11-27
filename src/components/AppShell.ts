import type { ProgressRecord, SettingsRecord } from '../services/db';
import { resolveWardrobe } from '../services/shopCatalog';
import { getCoins, getTodayXp } from '../services/srsEngine';
import { escapeHtml } from '../utils/html';
import { renderBaoSvg } from './BaoMascot';
import { iconSvg, type IconName } from './Icons';

export type NavTab = 'map' | 'read' | 'listen' | 'write' | 'review' | 'shop' | 'profile';

const SIDEBAR_ITEMS: { id: NavTab; label: string; mobileLabel: string; href: string; icon: IconName }[] = [
  { id: 'map', label: 'Bản đồ học', mobileLabel: 'Bản đồ', href: '#/', icon: 'map' },
  { id: 'shop', label: 'Tiệm của Bao', mobileLabel: 'Tiệm Bao', href: '#/shop', icon: 'shop' },
  { id: 'read', label: 'Đọc truyện', mobileLabel: 'Đọc', href: '#/reading/r-t1', icon: 'read' },
  { id: 'listen', label: 'Luyện nghe', mobileLabel: 'Nghe', href: '#/listening/t1-nghe', icon: 'listen' },
  { id: 'write', label: 'Viết chữ', mobileLabel: 'Viết', href: '#/writing/t1-viet', icon: 'write' },
  { id: 'review', label: 'Ôn tập', mobileLabel: 'Ôn tập', href: '#/review', icon: 'review' },
  { id: 'profile', label: 'Hồ sơ', mobileLabel: 'Hồ sơ', href: '#/profile', icon: 'profile' },
];

const MOBILE_ITEMS: NavTab[] = ['map', 'shop', 'read', 'review', 'profile'];

export function renderAppShell(opts: {
  root: HTMLElement;
  activeTab: NavTab;
  title: string;
  progress: ProgressRecord;
  settings: SettingsRecord;
  todayXp?: number;
}): HTMLElement {
  const goalXp = opts.settings.dailyGoalMinutes * 4;
  const todayXp = opts.todayXp ?? getTodayXp(opts.progress);
  const pct = Math.min(100, Math.round((todayXp / Math.max(1, goalXp)) * 100));
  const coins = getCoins(opts.progress);
  const wardrobe = resolveWardrobe(opts.progress);

  opts.root.innerHTML = `
    <div class="app-shell">
      <aside class="sidebar" aria-label="Điều hướng chính">
        <a href="#/" class="sidebar-brand">
          ${renderBaoSvg({ mood: 'happy', size: 50, wardrobe })}
          <div>
            <span class="sidebar-brand-name">BaoBao</span>
            <div style="font-size:11px;font-weight:700;color:var(--ink-muted);margin-top:-3px;">Học tiếng Trung vui!</div>
          </div>
        </a>

        <a href="#/shop" class="sidebar-coin-banner" title="Vào tiệm sắm đồ cho Bao">
          <span style="font-size:18px;">🎋</span>
          <div style="flex:1;line-height:1.2;">
            <div style="font-size:14px;font-weight:800;color:var(--ink);">${coins} Xu Tre</div>
            <div style="font-size:11px;color:var(--ink-muted);font-weight:700;">Sắm đồ cho Bao →</div>
          </div>
        </a>

        ${SIDEBAR_ITEMS.map(
          (item) => `
          <a href="${item.href}" class="nav-item ${opts.activeTab === item.id ? 'is-active' : ''}">
            ${iconSvg(item.icon, 20, opts.activeTab === item.id)}
            <span>${escapeHtml(item.label)}</span>
          </a>`
        ).join('')}
      </aside>

      <main class="main-area">
        <div class="main-inner">
          <header class="topbar">
            <h1 class="topbar-title">${escapeHtml(opts.title)}</h1>
            <div class="topbar-chips">
              <a href="#/shop" class="chip coin-chip" title="Xu Tre dùng để mua trang phục & phụ kiện cho Bao" style="text-decoration:none;">
                🎋 ${coins} Xu Tre
              </a>
              <span class="chip" title="Chuỗi ngày học liên tiếp" style="background:var(--write-soft);border-color:var(--write);">
                ${iconSvg('flame', 16)} ${escapeHtml(opts.progress.streak)} ngày
              </span>
              <span class="chip" title="Điểm kinh nghiệm tích lũy" style="background:var(--review-soft);border-color:var(--review);">
                ${iconSvg('star', 16)} ${escapeHtml(opts.progress.xp)} XP
              </span>
              <a href="#/profile" class="chip" title="Mục tiêu ngày" style="text-decoration:none;background:var(--read-soft);border-color:var(--read);">
                ${iconSvg('target', 16)} ${pct}% mục tiêu
              </a>
            </div>
          </header>
          <div data-shell-body></div>
        </div>
      </main>

      <nav class="mobile-tabbar" aria-label="Điều hướng di động">
        ${MOBILE_ITEMS.map((id) => SIDEBAR_ITEMS.find((x) => x.id === id)!)
          .map(
            (item) => `
          <a href="${item.href}" class="mobile-tab ${opts.activeTab === item.id ? 'is-active' : ''}">
            ${iconSvg(item.icon, 20, opts.activeTab === item.id)}
            <span>${escapeHtml(item.mobileLabel)}</span>
          </a>`
          )
          .join('')}
      </nav>
    </div>
  `;

  return opts.root.querySelector('[data-shell-body]') as HTMLElement;
}

export function renderFocusShell(opts: {
  root: HTMLElement;
  progressPct: number;
  accentVar: string;
  wide?: boolean;
  backHref?: string;
  labelRight?: string;
}): { body: HTMLElement; setProgress: (pct: number, labelRight?: string) => void } {
  opts.root.innerHTML = `
    <div class="focus-shell ${opts.wide ? 'is-wide' : ''}">
      <div class="focus-topbar">
        <a href="${opts.backHref ?? '#/'}" class="btn btn-sm btn-soft" aria-label="Thoát bài học">${iconSvg('close', 18)}</a>
        <div class="progress-track" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${Math.round(opts.progressPct)}">
          <div class="progress-fill" data-focus-fill style="width:${opts.progressPct}%;background:${opts.accentVar};"></div>
        </div>
        <span data-focus-label style="font-size:14px;font-weight:700;color:var(--ink-muted);min-width:56px;text-align:right;">
          ${escapeHtml(opts.labelRight ?? `${Math.round(opts.progressPct)}%`)}
        </span>
      </div>
      <div class="focus-body" data-focus-body></div>
    </div>
  `;

  const fill = opts.root.querySelector('[data-focus-fill]') as HTMLElement;
  const label = opts.root.querySelector('[data-focus-label]') as HTMLElement;
  const track = opts.root.querySelector('.progress-track') as HTMLElement;
  const body = opts.root.querySelector('[data-focus-body]') as HTMLElement;

  return {
    body,
    setProgress(pct: number, labelRight?: string) {
      const clamped = Math.max(0, Math.min(100, Math.round(pct)));
      fill.style.width = `${clamped}%`;
      track.setAttribute('aria-valuenow', String(clamped));
      label.textContent = labelRight ?? `${clamped}%`;
    },
  };
}
