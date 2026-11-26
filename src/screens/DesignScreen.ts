import { renderBaoSvg } from '../components/BaoMascot';
import { iconSvg, stickerBadge, type IconName } from '../components/Icons';

export function renderDesignScreen(root: HTMLElement) {
  const swatches = [
    { name: 'Giao tiếp', bg: 'var(--comm)', lip: 'var(--comm-lip)', soft: 'var(--comm-soft)', icon: 'comm' as IconName },
    { name: 'Đọc', bg: 'var(--read)', lip: 'var(--read-lip)', soft: 'var(--read-soft)', icon: 'read' as IconName },
    { name: 'Nghe', bg: 'var(--listen)', lip: 'var(--listen-lip)', soft: 'var(--listen-soft)', icon: 'listen' as IconName },
    { name: 'Viết', bg: 'var(--write)', lip: 'var(--write-lip)', soft: 'var(--write-soft)', icon: 'write' as IconName },
    { name: 'Ôn tập', bg: 'var(--review)', lip: 'var(--review-lip)', soft: 'var(--review-soft)', icon: 'review' as IconName },
    { name: 'Từ & mẫu câu', bg: 'var(--vocab)', lip: 'var(--vocab-lip)', soft: 'var(--vocab-soft)', icon: 'book' as IconName },
  ];

  root.innerHTML = `
    <div style="max-width:1000px;margin:0 auto;padding:32px 20px;">
      <div style="display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-bottom:24px;">
        <div style="display:flex;align-items:center;gap:14px;">
          ${renderBaoSvg({ mood: 'wave', size: 72 })}
          <div>
            <h1 style="margin:0;font-size:30px;font-weight:800;">BaoBao Design System</h1>
            <p style="margin:4px 0 0;color:var(--ink-muted);">Baloo 2 + Noto Sans SC · Lip 4px · Clay Shadow</p>
          </div>
        </div>
        <a href="#/" class="btn btn-read">Về bản đồ học</a>
      </div>

      <div class="clay-card" style="padding:24px;margin-bottom:20px;">
        <h2 style="margin:0 0 16px;">Màu loại bài & Sticker</h2>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;">
          ${swatches
            .map(
              (s) => `
            <div style="padding:14px;border-radius:16px;background:${s.soft};border:1.5px solid var(--border);display:flex;flex-direction:column;gap:8px;align-items:flex-start;">
              ${stickerBadge(s.icon, s.bg)}
              <strong>${s.name}</strong>
              <span style="display:inline-block;width:100%;height:10px;border-radius:999px;background:${s.bg};border-bottom:3px solid ${s.lip};"></span>
            </div>`
            )
            .join('')}
        </div>
      </div>

      <div class="clay-card" style="padding:24px;margin-bottom:20px;">
        <h2 style="margin:0 0 16px;">Nút bấm Lip 4px & Typography</h2>
        <div style="display:flex;flex-wrap:wrap;gap:12px;margin-bottom:20px;">
          <button type="button" class="btn btn-comm">Giao tiếp</button>
          <button type="button" class="btn btn-read">Đọc hiểu</button>
          <button type="button" class="btn btn-listen">Luyện nghe</button>
          <button type="button" class="btn btn-write">Viết chữ</button>
          <button type="button" class="btn btn-review">Ôn tập</button>
          <button type="button" class="btn btn-vocab">Từ mới</button>
          <button type="button" class="btn" disabled>Chưa mở ${iconSvg('lock', 16)}</button>
        </div>
        <div style="padding:18px;border-radius:18px;background:var(--bg);border:1.5px solid var(--border);">
          <div class="hanzi-xl">你好</div>
          <div class="pinyin" style="font-size:20px;">nǐ hǎo</div>
          <div style="font-size:22px;font-weight:700;margin-top:4px;">Xin chào</div>
        </div>
      </div>
    </div>
  `;
}
