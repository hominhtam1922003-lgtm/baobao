import type { BaoAccessory, BaoWardrobe, ProgressRecord, WardrobeSlot } from './db';

export type ItemRarity = 'co-ban' | 'de-thuong' | 'le-hoi' | 'huyen-thoai';

export interface ShopItem {
  id: string;
  slot: WardrobeSlot;
  nameVi: string;
  nameZh: string;
  pinyin: string;
  descVi: string;
  price: number;
  rarity: ItemRarity;
  tagColor: string;
}

export const SLOT_LABELS: Record<WardrobeSlot, { label: string; emoji: string }> = {
  hat: { label: 'Mũ & Đầu', emoji: '🎀' },
  outfit: { label: 'Trang phục', emoji: '👕' },
  glasses: { label: 'Kính & Mặt', emoji: '✨' },
  prop: { label: 'Phụ kiện', emoji: '🎁' },
  bg: { label: 'Khung nền', emoji: '🌸' },
};

export const RARITY_LABELS: Record<ItemRarity, { label: string; bg: string; border: string }> = {
  'co-ban': { label: 'Dễ thương', bg: '#E1F5FE', border: '#1CB0F6' },
  'de-thuong': { label: 'Sành điệu', bg: '#D9F6EF', border: '#1FC8A9' },
  'le-hoi': { label: 'Lễ hội', bg: '#FFE3E8', border: '#FF6B81' },
  'huyen-thoai': { label: 'Huyền thoại', bg: '#FFF6D6', border: '#FFC531' },
};

export const DEFAULT_WARDROBE: BaoWardrobe = {
  hat: 'none',
  outfit: 'none',
  glasses: 'none',
  prop: 'none',
  bg: 'none',
};

export const SHOP_CATALOG: ShopItem[] = [
  // HATS (8)
  {
    id: 'bamboo-hat', slot: 'hat', nameVi: 'Nón lá tre vàng', nameZh: '竹笠', pinyin: 'zhú lì',
    descVi: 'Chiếc nón lá đan tre xinh xắn cho chuyến du hành đầu tiên!', price: 30, rarity: 'co-ban', tagColor: 'var(--review)',
  },
  {
    id: 'sakura-bow', slot: 'hat', nameVi: 'Nơ hoa anh đào', nameZh: '樱花结', pinyin: 'yīng huā jié',
    descVi: 'Chiếc nơ hồng pastel kèm cánh hoa đào cực dễ thương!', price: 45, rarity: 'co-ban', tagColor: 'var(--comm)',
  },
  {
    id: 'tea-beret', slot: 'hat', nameVi: 'Mũ beret trà xanh', nameZh: '抹茶帽', pinyin: 'mǒ chá mào',
    descVi: 'Phong cách nghệ sĩ phố cổ, hợp ngồi quán trà đọc truyện.', price: 65, rarity: 'de-thuong', tagColor: 'var(--read)',
  },
  {
    id: 'bunny-ears', slot: 'hat', nameVi: 'Tai thỏ bông mềm', nameZh: '兔耳朵', pinyin: 'tù ěr duo',
    descVi: 'Cài tai thỏ hồng mềm mại làm Bao đáng yêu gấp bội!', price: 85, rarity: 'de-thuong', tagColor: 'var(--comm)',
  },
  {
    id: 'chef-hat', slot: 'hat', nameVi: 'Mũ đầu bếp Dimsum', nameZh: '厨师帽', pinyin: 'chú shī mào',
    descVi: 'Hóa thân siêu đầu bếp làm bánh bao và trà sữa!', price: 100, rarity: 'de-thuong', tagColor: 'var(--write)',
  },
  {
    id: 'explorer-cap', slot: 'hat', nameVi: 'Mũ thám hiểm cam', nameZh: '探险帽', pinyin: 'tàn xiǎn mào',
    descVi: 'Sẵn sàng chinh phục mọi thành phố cổ trên bản đồ!', price: 120, rarity: 'le-hoi', tagColor: 'var(--write)',
  },
  {
    id: 'grad-cap', slot: 'hat', nameVi: 'Mũ cử nhân thông thái', nameZh: '学士帽', pinyin: 'xué shì mào',
    descVi: 'Dành tặng học bá tiếng Trung chăm chỉ ôn tập mỗi ngày!', price: 150, rarity: 'le-hoi', tagColor: 'var(--listen)',
  },
  {
    id: 'crown', slot: 'hat', nameVi: 'Vương miện hoàng kim', nameZh: '皇冠', pinyin: 'huáng guān',
    descVi: 'Biểu tượng lấp lánh của bậc thầy giao tiếp tiếng Trung!', price: 240, rarity: 'huyen-thoai', tagColor: 'var(--review)',
  },

  // OUTFITS (6)
  {
    id: 'red-scarf', slot: 'outfit', nameVi: 'Khăn choàng đào ấm', nameZh: '红围巾', pinyin: 'hóng wéi jīn',
    descVi: 'Chiếc khăn len mềm mại giữ ấm những ngày gió thu!', price: 35, rarity: 'co-ban', tagColor: 'var(--comm)',
  },
  {
    id: 'peach-hoodie', slot: 'outfit', nameVi: 'Áo hoodie đào pastel', nameZh: '卫衣', pinyin: 'wèi yī',
    descVi: 'Áo hoodie hồng đào năng động có túi trước siêu cute!', price: 80, rarity: 'de-thuong', tagColor: 'var(--comm)',
  },
  {
    id: 'mint-sweater', slot: 'outfit', nameVi: 'Áo len lá tre mint', nameZh: '毛衣', pinyin: 'máo yī',
    descVi: 'Áo len xanh mint dịu mắt thêu chiếc lá tre may mắn.', price: 95, rarity: 'de-thuong', tagColor: 'var(--read)',
  },
  {
    id: 'school-uniform', slot: 'outfit', nameVi: 'Đồng phục lớp học', nameZh: '校服', pinyin: 'xiào fú',
    descVi: 'Áo cổ thủy thủ cài nơ đỏ chuẩn bạn học cùng bàn của Linh!', price: 125, rarity: 'le-hoi', tagColor: 'var(--vocab)',
  },
  {
    id: 'tang-suit', slot: 'outfit', nameVi: 'Đường trang đỏ lễ hội', nameZh: '唐装', pinyin: 'táng zhuāng',
    descVi: 'Trang phục truyền thống đỏ viền vàng rực rỡ dịp Trung Thu!', price: 180, rarity: 'le-hoi', tagColor: 'var(--comm)',
  },
  {
    id: 'bamboo-cape', slot: 'outfit', nameVi: 'Áo choàng siêu nhân tre', nameZh: '披风', pinyin: 'pī fēng',
    descVi: 'Siêu anh hùng BaoBao bay khắp 4 chặng không sợ chữ Hán khó!', price: 220, rarity: 'huyen-thoai', tagColor: 'var(--write)',
  },

  // GLASSES & FACE (4)
  {
    id: 'heart-blush', slot: 'glasses', nameVi: 'Má hồng trái tim', nameZh: '爱心腮红', pinyin: 'ài xīn sāi hóng',
    descVi: 'Hai trái tim hồng lấp lánh trên má mỗi khi trả lời đúng!', price: 40, rarity: 'co-ban', tagColor: 'var(--comm)',
  },
  {
    id: 'round-scholar', slot: 'glasses', nameVi: 'Kính tròn học giả', nameZh: '圆眼镜', pinyin: 'yuán yǎn jìng',
    descVi: 'Gọng vàng thanh lịch chuẩn mọt truyện phố cổ!', price: 70, rarity: 'de-thuong', tagColor: 'var(--review)',
  },
  {
    id: 'star-glasses', slot: 'glasses', nameVi: 'Kính ngôi sao xanh', nameZh: '星星眼镜', pinyin: 'xīng xing yǎn jìng',
    descVi: 'Cặp kính ngôi sao tỏa sáng mỗi lần đạt Combo!', price: 95, rarity: 'le-hoi', tagColor: 'var(--vocab)',
  },
  {
    id: 'cool-shades', slot: 'glasses', nameVi: 'Kính râm siêu ngầu', nameZh: '墨镜', pinyin: 'mò jìng',
    descVi: 'Gấu trúc cool ngầu tự tin dạo phố cổ ngày nắng!', price: 130, rarity: 'huyen-thoai', tagColor: 'var(--listen)',
  },

  // PROPS (6)
  {
    id: 'bamboo-shoot', slot: 'prop', nameVi: 'Cành tre non mũm mĩm', nameZh: '嫩竹叶', pinyin: 'nèn zhú yè',
    descVi: 'Món ăn vặt yêu thích nhất của Bao trong giờ giải lao!', price: 25, rarity: 'co-ban', tagColor: 'var(--read)',
  },
  {
    id: 'boba-tea', slot: 'prop', nameVi: 'Ly trà sữa ít đường', nameZh: '珍珠奶茶', pinyin: 'zhēn zhū nǎi chá',
    descVi: 'Ly trà sữa trân châu 少糖少冰 nổi tiếng ở Bài 6!', price: 55, rarity: 'co-ban', tagColor: 'var(--write)',
  },
  {
    id: 'lantern-pin', slot: 'prop', nameVi: 'Đèn lồng đỏ lễ hội', nameZh: '红灯笼', pinyin: 'hóng dēng long',
    descVi: 'Chiếc đèn lồng đỏ tỏa sáng lung linh trong đêm Trung Thu!', price: 85, rarity: 'le-hoi', tagColor: 'var(--comm)',
  },
  {
    id: 'orange-backpack', slot: 'prop', nameVi: 'Ba lô du hành cam', nameZh: '小书包', pinyin: 'xiǎo shū bāo',
    descVi: 'Đựng đầy sổ tay ngữ pháp và bản đồ du lịch!', price: 105, rarity: 'de-thuong', tagColor: 'var(--write)',
  },
  {
    id: 'paper-fan', slot: 'prop', nameVi: 'Quạt giấy thư pháp', nameZh: '折扇', pinyin: 'zhé shàn',
    descVi: 'Chiếc quạt xếp vẽ hoa đào đậm chất văn hóa Trung Hoa!', price: 140, rarity: 'le-hoi', tagColor: 'var(--comm)',
  },
  {
    id: 'music-notes', slot: 'prop', nameVi: 'Giai điệu bay bổng', nameZh: '音符', pinyin: 'yīn fú',
    descVi: 'Những nốt nhạc màu tím bay quanh Bao khi luyện nghe!', price: 160, rarity: 'huyen-thoai', tagColor: 'var(--listen)',
  },

  // BACKGROUNDS (4)
  {
    id: 'bamboo-grove', slot: 'bg', nameVi: 'Vườn tre bình minh', nameZh: '竹林晨光', pinyin: 'zhú lín',
    descVi: 'Nền xanh mát rợp bóng tre non tươi tắn mỗi sáng!', price: 60, rarity: 'co-ban', tagColor: 'var(--read)',
  },
  {
    id: 'boba-cafe', slot: 'bg', nameVi: 'Quán trà sữa pastel', nameZh: '奶茶小店', pinyin: 'nǎi chá diàn',
    descVi: 'Tông kem đào ngọt ngào như góc quán quen của Bao!', price: 90, rarity: 'de-thuong', tagColor: 'var(--write)',
  },
  {
    id: 'lantern-street', slot: 'bg', nameVi: 'Phố cổ đèn lồng', nameZh: '灯笼古街', pinyin: 'gǔ jiē',
    descVi: 'Ánh đèn lồng đỏ rực rỡ lễ hội cuối tuần!', price: 145, rarity: 'le-hoi', tagColor: 'var(--comm)',
  },
  {
    id: 'starry-night', slot: 'bg', nameVi: 'Bầu trời ngàn sao', nameZh: '星光夜空', pinyin: 'xīng kōng',
    descVi: 'Vầng trăng và những vì sao lấp lánh ước mơ tương lai!', price: 210, rarity: 'huyen-thoai', tagColor: 'var(--listen)',
  },
];

export const SHOP_BY_ID = new Map(SHOP_CATALOG.map((item) => [item.id, item]));

export function getShopItem(id: string): ShopItem | undefined {
  return SHOP_BY_ID.get(id);
}

/** Map legacy single BaoAccessory into multi-slot BaoWardrobe cleanly */
export function legacyAccessoryToWardrobe(acc?: BaoAccessory): BaoWardrobe {
  const base = { ...DEFAULT_WARDROBE };
  if (!acc || acc === 'none') return base;
  const item = SHOP_BY_ID.get(acc);
  if (item) {
    base[item.slot] = item.id;
  }
  return base;
}

export function resolveWardrobe(progress: ProgressRecord): BaoWardrobe {
  if (progress.wardrobe) {
    return {
      ...DEFAULT_WARDROBE,
      ...progress.wardrobe,
    };
  }
  return legacyAccessoryToWardrobe(progress.equippedAccessory);
}

export function getOwnedItemIds(progress: ProgressRecord): Set<string> {
  return new Set(progress.ownedItems ?? []);
}
