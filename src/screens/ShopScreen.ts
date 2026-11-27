import confetti from 'canvas-confetti';
import { renderAppShell } from '../components/AppShell';
import { renderBaoSvg, type BaoMood } from '../components/BaoMascot';
import { iconSvg } from '../components/Icons';
import { audioService } from '../services/audioPlayer';
import type { BaoWardrobe, WardrobeSlot } from '../services/db';
import {
  DEFAULT_WARDROBE,
  getOwnedItemIds,
  RARITY_LABELS,
  resolveWardrobe,
  SHOP_CATALOG,
  SLOT_LABELS,
  type ShopItem,
} from '../services/shopCatalog';
import {
  buyShopItem,
  ensureProgress,
  ensureSettings,
  equipWardrobeItem,
  getCoins,
  resetWardrobe,
} from '../services/srsEngine';
import { escapeHtml } from '../utils/html';

type FilterTab = 'all' | WardrobeSlot | 'owned';

const BAO_QUOTES = [
  { zh: '加油！今天一起学中文吧！', py: 'Jiā yóu! Jīn tiān yì qǐ xué Zhōng wén ba!', vi: 'Cố lên! Hôm nay cùng học tiếng Trung nhé!' },
  { zh: '这套衣服真可爱！', py: 'Zhè tào yī fu zhēn kě ài!', vi: 'Bộ trang phục này dễ thương quá!' },
  { zh: '我想喝一杯少糖奶茶！', py: 'Wǒ xiǎng hē yì bēi shǎo táng nǎi chá!', vi: 'Bao muốn uống một ly trà sữa ít đường!' },
  { zh: '你越来越厉害了！', py: 'Nǐ yuè lái yuè lì hai le!', vi: 'Bạn ngày càng siêu đỉnh rồi đó!' },
  { zh: '学完一课就能领竹币哦！', py: 'Xué wán yí kè jiù néng lǐng zhú bì o!', vi: 'Học xong 1 bài là nhận ngay Xu Tre nha!' },
];

export async function renderShopScreen(root: HTMLElement): Promise<() => void> {
  let progress = await ensureProgress();
  const settings = await ensureSettings();

  let activeTab: FilterTab = 'all';
  let previewWardrobe: Partial<BaoWardrobe> = {};
  let previewMood: BaoMood = 'happy';
  let quoteIdx = 0;
  let toastMsg = '';
  let toastOk = true;
  let toastTimer: number | null = null;

  const setToast = (msg: string, ok = true) => {
    toastMsg = msg;
    toastOk = ok;
    if (toastTimer) window.clearTimeout(toastTimer);
    toastTimer = window.setTimeout(() => {
      toastMsg = '';
      const el = root.querySelector('[data-shop-toast]');
      if (el) el.remove();
    }, 3200);
  };

  const render = () => {
    const coins = getCoins(progress);
    const owned = getOwnedItemIds(progress);
    const equipped = resolveWardrobe(progress);
    const displayedWardrobe: BaoWardrobe = { ...equipped, ...previewWardrobe };
    const hasPreview = Object.keys(previewWardrobe).length > 0;
    const quote = BAO_QUOTES[quoteIdx % BAO_QUOTES.length];

    const body = renderAppShell({
      root,
      activeTab: 'shop',
      title: 'Tiệm thời trang của Bao',
      progress,
      settings,
    });

    const filteredItems: ShopItem[] = SHOP_CATALOG.filter((item) => {
      if (activeTab === 'all') return true;
      if (activeTab === 'owned') return owned.has(item.id);
      return item.slot === activeTab;
    });

    const tabs: { id: FilterTab; label: string }[] = [
      { id: 'all', label: `✨ Tất cả (${SHOP_CATALOG.length})` },
      { id: 'hat', label: `${SLOT_LABELS.hat.emoji} ${SLOT_LABELS.hat.label}` },
      { id: 'outfit', label: `${SLOT_LABELS.outfit.emoji} ${SLOT_LABELS.outfit.label}` },
      { id: 'glasses', label: `${SLOT_LABELS.glasses.emoji} ${SLOT_LABELS.glasses.label}` },
      { id: 'prop', label: `${SLOT_LABELS.prop.emoji} ${SLOT_LABELS.prop.label}` },
      { id: 'bg', label: `${SLOT_LABELS.bg.emoji} ${SLOT_LABELS.bg.label}` },
      { id: 'owned', label: `🎒 Tủ đồ (${owned.size})` },
    ];

    const moodChoices: { id: BaoMood; label: string }[] = [
      { id: 'happy', label: '😊 Vui vẻ' },
      { id: 'celebrate', label: '🥳 Ăn mừng' },
      { id: 'love', label: '🥰 Đáng yêu' },
      { id: 'wave', label: '👋 Vẫy tay' },
    ];

    body.innerHTML = `
      ${
        toastMsg
          ? `<div data-shop-toast class="clay-card milestone-banner" style="padding:12px 18px;margin-bottom:16px;background:${
              toastOk ? 'var(--read-soft)' : 'var(--comm-soft)'
            };border-color:${toastOk ? 'var(--read)' : 'var(--comm)'};font-weight:800;display:flex;align-items:center;gap:10px;">
               ${toastOk ? '🎉' : '💡'} <span>${escapeHtml(toastMsg)}</span>
             </div>`
          : ''
      }

      <div class="shop-layout">
        <!-- Left: Live Interactive BaoBao Dressing Stage -->
        <aside class="clay-card shop-stage-card">
          <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;width:100%;margin-bottom:10px;">
            <span class="chip coin-chip" style="font-size:15px;">🎋 ${coins} Xu Tre</span>
            <span class="chip" style="background:var(--bg);font-size:12px;">Đã sở hữu ${owned.size}/${SHOP_CATALOG.length}</span>
          </div>

          <div class="bao-speech-bubble" data-bao-speech>
            <div class="hanzi" style="font-size:20px;font-weight:700;">${escapeHtml(quote.zh)}</div>
            <div class="pinyin" style="font-size:13px;">${escapeHtml(quote.py)}</div>
            <div style="font-size:13px;color:var(--ink-muted);margin-top:2px;">${escapeHtml(quote.vi)}</div>
          </div>

          <button type="button" class="bao-stage-btn" data-pet-bao aria-label="Vuốt ve gấu trúc Bao">
            ${renderBaoSvg({ mood: previewMood, size: 210, wardrobe: displayedWardrobe, interactive: true })}
            <span class="pet-hint-pill">Chạm vào Bao để chơi cùng! 💕</span>
          </button>

          ${
            hasPreview
              ? `<div style="margin-top:10px;padding:8px 12px;border-radius:14px;background:var(--review-soft);border:1.5px solid var(--review);font-size:13px;font-weight:700;width:100%;display:flex;align-items:center;justify-content:space-between;gap:8px;">
                   <span>👀 Đang mặc thử đồ mới</span>
                   <button type="button" class="btn btn-sm btn-soft" data-clear-preview>Bỏ mặc thử</button>
                 </div>`
              : ''
          }

          <div style="display:flex;gap:6px;flex-wrap:wrap;justify-content:center;margin-top:12px;">
            ${moodChoices
              .map(
                (m) => `<button type="button" class="btn btn-sm ${previewMood === m.id ? 'btn-comm' : 'btn-soft'}" data-set-mood="${m.id}" style="padding:5px 10px;font-size:12px;">${m.label}</button>`
              )
              .join('')}
          </div>

          <!-- Active 5 slots bar -->
          <div style="width:100%;margin-top:14px;padding:12px;border-radius:16px;background:var(--bg);border:1.5px solid var(--border);">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
              <strong style="font-size:13px;">Đang phối (5 ngăn đồ):</strong>
              <button type="button" class="btn btn-sm btn-soft" data-reset-wardrobe style="min-height:28px;padding:2px 10px;font-size:12px;">Mặc nguyên bản</button>
            </div>
            <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:6px;">
              ${(['hat', 'outfit', 'glasses', 'prop', 'bg'] as WardrobeSlot[])
                .map((slot) => {
                  const activeId = displayedWardrobe[slot];
                  const activeItem = SHOP_CATALOG.find((x) => x.id === activeId);
                  return `<button type="button" data-unequip-slot="${slot}" title="${activeItem ? `Tháo ${activeItem.nameVi}` : SLOT_LABELS[slot].label}" style="border:1.5px solid ${activeItem ? 'var(--comm)' : 'var(--border)'};background:${activeItem ? 'var(--comm-soft)' : 'var(--surface)'};border-radius:12px;padding:6px 4px;font-size:11px;font-weight:700;display:flex;flex-direction:column;align-items:center;gap:2px;">
                    <span style="font-size:15px;">${SLOT_LABELS[slot].emoji}</span>
                    <span style="max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${activeItem ? 'Đang đeo' : 'Trống'}</span>
                  </button>`;
                })
                .join('')}
            </div>
          </div>

          <!-- How to earn Xu Tre card -->
          <div style="width:100%;margin-top:12px;padding:12px 14px;border-radius:16px;background:var(--read-soft);border:1.5px solid var(--read);text-align:left;font-size:13px;">
            <div style="font-weight:800;margin-bottom:4px;">🎋 Cách kiếm Xu Tre siêu nhanh:</div>
            <ul style="margin:0;padding-left:18px;display:flex;flex-direction:column;gap:3px;color:var(--ink);">
              <li>Hoàn thành 1 bài Giao tiếp / Đọc / Nghe / Viết: <strong>+30 ~ +55 Xu</strong></li>
              <li>Đạt 100% mục tiêu mỗi ngày: <strong>+40 Xu thưởng</strong></li>
              <li>Vượt qua Kiểm tra cuối chặng: <strong>+100 Xu</strong></li>
            </ul>
          </div>
        </aside>

        <!-- Right: Shop Catalog Grid -->
        <div>
          <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px;" role="tablist" aria-label="Danh mục cửa hàng">
            ${tabs
              .map(
                (t) => `<button type="button" class="btn btn-sm ${activeTab === t.id ? 'btn-comm' : 'btn-soft'}" data-shop-tab="${t.id}">${escapeHtml(t.label)}</button>`
              )
              .join('')}
          </div>

          ${
            filteredItems.length === 0
              ? `<div class="clay-card" style="padding:36px;text-align:center;">
                   ${renderBaoSvg({ mood: 'wave', size: 108, wardrobe: equipped })}
                   <h3 style="margin:10px 0 6px;">Tủ đồ đang chờ món đầu tiên!</h3>
                   <p style="color:var(--ink-muted);margin:0 0 16px;">Học xong 1 bài trên Bản đồ là bạn có ngay Xu Tre để sắm đồ siêu xinh cho Bao!</p>
                   <a href="#/" class="btn btn-comm">Học bài kiếm Xu Tre →</a>
                 </div>`
              : `<div class="shop-grid">
                   ${filteredItems
                     .map((item) => {
                       const isOwned = owned.has(item.id);
                       const isEquipped = equipped[item.slot] === item.id;
                       const isPreviewing = previewWardrobe[item.slot] === item.id;
                       const canAfford = coins >= item.price;
                       const rarity = RARITY_LABELS[item.rarity];
                       const previewMiniWardrobe: BaoWardrobe = { ...DEFAULT_WARDROBE, [item.slot]: item.id };

                       return `
                         <article class="clay-card shop-item-card ${isEquipped ? 'is-equipped' : ''}">
                           <div style="display:flex;justify-content:space-between;align-items:center;gap:6px;width:100%;">
                             <span class="chip" style="font-size:11px;padding:3px 9px;background:${rarity.bg};border-color:${rarity.border};">${escapeHtml(rarity.label)}</span>
                             <span style="font-size:12px;font-weight:800;color:var(--ink-muted);">${SLOT_LABELS[item.slot].emoji} ${SLOT_LABELS[item.slot].label}</span>
                           </div>

                           <div class="shop-item-preview">
                             ${renderBaoSvg({ mood: 'happy', size: 104, wardrobe: previewMiniWardrobe })}
                           </div>

                           <div style="text-align:center;width:100%;">
                             <div style="font-weight:800;font-size:16px;line-height:1.25;">${escapeHtml(item.nameVi)}</div>
                             <div style="margin-top:2px;">
                               <span class="hanzi" style="font-size:20px;font-weight:700;">${escapeHtml(item.nameZh)}</span>
                               <span class="pinyin" style="margin-left:5px;font-size:13px;">${escapeHtml(item.pinyin)}</span>
                             </div>
                             <p style="margin:6px 0 12px;font-size:13px;color:var(--ink-muted);min-height:36px;">${escapeHtml(item.descVi)}</p>
                           </div>

                           <div style="display:flex;gap:8px;width:100%;margin-top:auto;">
                             ${
                               isOwned
                                 ? `<button type="button" class="btn btn-sm ${isEquipped ? 'btn-read' : 'btn-vocab'}" data-equip-item="${item.id}" style="flex:1;">
                                      ${isEquipped ? `${iconSvg('check', 15)} Đang mặc (Tháo)` : 'Mặc ngay'}
                                    </button>`
                                 : `<button type="button" class="btn btn-sm ${isPreviewing ? 'btn-review' : 'btn-soft'}" data-try-item="${item.id}" title="Mặc thử lên Bao">
                                      ${isPreviewing ? 'Đang thử' : 'Thử'}
                                    </button>
                                    <button type="button" class="btn btn-sm ${canAfford ? 'btn-comm' : 'btn-soft'}" data-buy-item="${item.id}" style="flex:1;">
                                      🎋 ${item.price} Xu
                                    </button>`
                             }
                           </div>
                         </article>
                       `;
                     })
                     .join('')}
                 </div>`
          }
        </div>
      </div>
    `;

    // Interactive events
    body.querySelector('[data-pet-bao]')?.addEventListener('click', () => {
      audioService.playSfx('pop');
      quoteIdx = (quoteIdx + 1) % BAO_QUOTES.length;
      previewMood = previewMood === 'love' ? 'celebrate' : 'love';
      if (!settings.reducedMotion) {
        confetti({
          particleCount: 16,
          spread: 50,
          origin: { x: 0.25, y: 0.5 },
          colors: ['#FF6B81', '#FFC531', '#1FC8A9'],
        });
      }
      render();
    });

    body.querySelectorAll<HTMLElement>('[data-set-mood]').forEach((b) => {
      b.addEventListener('click', () => {
        previewMood = b.dataset.setMood as BaoMood;
        audioService.playSfx('pop');
        render();
      });
    });

    body.querySelector('[data-clear-preview]')?.addEventListener('click', () => {
      previewWardrobe = {};
      render();
    });

    body.querySelector('[data-reset-wardrobe]')?.addEventListener('click', async () => {
      previewWardrobe = {};
      progress = await resetWardrobe();
      audioService.playSfx('pop');
      setToast('Bao đã trở về bộ lông gấu trúc nguyên bản!');
      render();
    });

    body.querySelectorAll<HTMLElement>('[data-unequip-slot]').forEach((b) => {
      b.addEventListener('click', async () => {
        const slot = b.dataset.unequipSlot as WardrobeSlot;
        if (previewWardrobe[slot]) {
          delete previewWardrobe[slot];
          render();
          return;
        }
        if (equipped[slot] !== 'none') {
          progress = await equipWardrobeItem(slot, 'none');
          audioService.playSfx('pop');
          render();
        }
      });
    });

    body.querySelectorAll<HTMLElement>('[data-shop-tab]').forEach((b) => {
      b.addEventListener('click', () => {
        activeTab = b.dataset.shopTab as FilterTab;
        render();
      });
    });

    body.querySelectorAll<HTMLElement>('[data-try-item]').forEach((b) => {
      b.addEventListener('click', () => {
        const item = SHOP_CATALOG.find((x) => x.id === b.dataset.tryItem);
        if (!item) return;
        if (previewWardrobe[item.slot] === item.id) {
          delete previewWardrobe[item.slot];
        } else {
          previewWardrobe[item.slot] = item.id;
        }
        previewMood = 'happy';
        audioService.playSfx('pop');
        render();
      });
    });

    body.querySelectorAll<HTMLElement>('[data-buy-item]').forEach((b) => {
      b.addEventListener('click', async () => {
        const item = SHOP_CATALOG.find((x) => x.id === b.dataset.buyItem);
        if (!item) return;
        const res = await buyShopItem(item.id);
        progress = res.progress;
        if (res.ok) {
          delete previewWardrobe[item.slot];
          previewMood = 'celebrate';
          audioService.playSfx('coin');
          setToast(`Đã mua và mặc ngay "${item.nameVi}" (${item.nameZh}) cho Bao!`, true);
          if (!settings.reducedMotion) {
            confetti({ particleCount: 55, spread: 70, origin: { y: 0.65 } });
          }
        } else {
          audioService.playSfx('err');
          setToast(res.error ?? 'Chưa đủ Xu Tre!', false);
        }
        render();
      });
    });

    body.querySelectorAll<HTMLElement>('[data-equip-item]').forEach((b) => {
      b.addEventListener('click', async () => {
        const item = SHOP_CATALOG.find((x) => x.id === b.dataset.equipItem);
        if (!item) return;
        delete previewWardrobe[item.slot];
        const nextVal = equipped[item.slot] === item.id ? 'none' : item.id;
        progress = await equipWardrobeItem(item.slot, nextVal);
        previewMood = nextVal === 'none' ? 'happy' : 'love';
        audioService.playSfx('pop');
        render();
      });
    });
  };

  render();
  return () => {
    if (toastTimer) window.clearTimeout(toastTimer);
  };
}
