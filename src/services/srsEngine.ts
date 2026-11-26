import {
  createEmptyCard,
  fsrs,
  generatorParameters,
  Rating,
  State,
  type Grade,
  type RecordLogItem,
} from 'ts-fsrs';
import type { CardFacet, ExampleSentence, ReviewRating } from '../types/curriculum';
import { getDb, type BaoAccessory, type ProgressRecord, type SettingsRecord, type SrsCardRecord } from './db';

export type { SrsCardRecord };
export type QueueFilter = 'due' | 'weak' | 'story' | 'writing';

const params = generatorParameters({
  request_retention: 0.9,
  maximum_interval: 365,
  enable_fuzz: true,
  learning_steps: ['1m', '10m'],
  relearning_steps: ['10m'],
});

const scheduler = fsrs(params);

const RATING_MAP: Record<ReviewRating, Grade> = {
  Again: Rating.Again,
  Hard: Rating.Hard,
  Good: Rating.Good,
  Easy: Rating.Easy,
};

export interface CreateCardInput {
  itemId: string;
  facet: CardFacet;
  hanzi: string;
  pinyin: string;
  meaningVi: string;
  example?: ExampleSentence;
  audio?: string;
  tags?: string[];
  isWeakWriting?: boolean;
}

export function cardKey(itemId: string, facet: CardFacet): string {
  return `${itemId}::${facet}`;
}

export function createOrGetCard(input: CreateCardInput, now = new Date()): SrsCardRecord {
  const iso = now.toISOString();
  return {
    key: cardKey(input.itemId, input.facet),
    itemId: input.itemId,
    facet: input.facet,
    hanzi: input.hanzi,
    pinyin: input.pinyin,
    meaningVi: input.meaningVi,
    example: input.example,
    audio: input.audio,
    tags: input.tags ?? [],
    isWeakWriting: input.isWeakWriting ?? false,
    card: createEmptyCard(now),
    createdAt: iso,
    updatedAt: iso,
  };
}

export function formatIntervalVi(due: Date, now: Date): string {
  const diffMin = Math.max(1, Math.round((due.getTime() - now.getTime()) / 60000));
  if (diffMin < 60) return `${diffMin} phút`;
  const diffHours = Math.round(diffMin / 60);
  if (diffHours < 24) return `${diffHours} giờ`;
  const diffDays = Math.round(diffHours / 24);
  if (diffDays < 30) return `${diffDays} ngày`;
  const diffMonths = Math.round(diffDays / 30);
  return `${diffMonths} tháng`;
}

export function previewIntervals(record: SrsCardRecord, now = new Date()): Record<ReviewRating, string> {
  const normalizedCard = {
    ...record.card,
    due: new Date(record.card.due),
    last_review: record.card.last_review ? new Date(record.card.last_review) : undefined,
  };
  const scheduling = scheduler.repeat(normalizedCard, now);
  return {
    Again: formatIntervalVi((scheduling[Rating.Again] as RecordLogItem).card.due, now),
    Hard: formatIntervalVi((scheduling[Rating.Hard] as RecordLogItem).card.due, now),
    Good: formatIntervalVi((scheduling[Rating.Good] as RecordLogItem).card.due, now),
    Easy: formatIntervalVi((scheduling[Rating.Easy] as RecordLogItem).card.due, now),
  };
}

export function reviewSrsCard(record: SrsCardRecord, rating: ReviewRating, now = new Date()) {
  const normalizedCard = {
    ...record.card,
    due: new Date(record.card.due),
    last_review: record.card.last_review ? new Date(record.card.last_review) : undefined,
  };
  const scheduling = scheduler.repeat(normalizedCard, now);
  const chosen = scheduling[RATING_MAP[rating]] as RecordLogItem;
  const updatedCard: SrsCardRecord = {
    ...record,
    card: chosen.card,
    lastRating: rating,
    isWeakWriting: record.facet === 'writing' ? rating === 'Again' || rating === 'Hard' : record.isWeakWriting,
    updatedAt: now.toISOString(),
  };
  return {
    updatedCard,
    log: chosen.log,
  };
}

export function isWeakCard(record: SrsCardRecord): boolean {
  return (
    record.lastRating === 'Again' ||
    record.card.lapses > 0 ||
    record.card.state === State.Relearning ||
    (record.card.difficulty > 7.2 && record.card.reps > 0)
  );
}

export function filterQueue(cards: SrsCardRecord[], filter: QueueFilter, now = new Date()): SrsCardRecord[] {
  const nowMs = now.getTime();
  return cards
    .filter((rec) => {
      const dueMs = new Date(rec.card.due).getTime();
      if (filter === 'due') return dueMs <= nowMs;
      if (filter === 'weak') return isWeakCard(rec);
      if (filter === 'story') return (rec.tags ?? []).includes('story');
      if (filter === 'writing') return rec.facet === 'writing' && (rec.isWeakWriting || dueMs <= nowMs);
      return false;
    })
    .sort((a, b) => new Date(a.card.due).getTime() - new Date(b.card.due).getTime());
}

export const BAO_ACCESSORIES: { id: BaoAccessory; label: string; reqXp: number; desc: string }[] = [
  { id: 'none', label: 'Mặc định', reqXp: 0, desc: 'Bộ lông gấu trúc nguyên bản' },
  { id: 'bamboo-hat', label: 'Nón lá', reqXp: 30, desc: 'Quà mở màn hành trình' },
  { id: 'red-scarf', label: 'Khăn đào', reqXp: 80, desc: 'Ấm áp giao tiếp mỗi ngày' },
  { id: 'tea-beret', label: 'Mũ trà xanh', reqXp: 140, desc: 'Phong cách quán trà phố cổ' },
  { id: 'star-glasses', label: 'Kính sao', reqXp: 220, desc: 'Sành điệu tập đọc & nghe' },
  { id: 'lantern-pin', label: 'Huy hiệu đèn lồng', reqXp: 340, desc: 'Rực rỡ lễ hội cuối tuần' },
  { id: 'explorer-cap', label: 'Mũ thám hiểm', reqXp: 500, desc: 'Bứt phá chặng nâng cao' },
  { id: 'crown', label: 'Vương miện', reqXp: 800, desc: 'Nhà du hành tinh thông' },
];

export const BAO_BADGES: { id: string; title: string; hint: string }[] = [
  { id: 'first-lesson', title: 'Bước chân đầu tiên', hint: 'Hoàn thành bài học đầu tiên' },
  { id: 'four-skills', title: 'Đủ 4 kỹ năng', hint: 'Hoàn thành 4 bài học' },
  { id: 'story-reader', title: 'Mọt truyện phố cổ', hint: 'Hoàn thành ít nhất 1 chương truyện dài kỳ' },
  { id: 'srs-50', title: 'Trí nhớ bền bỉ', hint: 'Ôn tập 50 lượt flashcard FSRS' },
  { id: 'stage-1-master', title: 'Chinh phục Chặng 1', hint: 'Vượt qua Kiểm tra Chặng 1' },
  { id: 'stage-2-master', title: 'Chinh phục Chặng 2', hint: 'Vượt qua Kiểm tra Chặng 2' },
  { id: 'stage-3-master', title: 'Chinh phục Chặng 3', hint: 'Vượt qua Kiểm tra Chặng 3' },
  { id: 'stage-4-master', title: 'Chinh phục Chặng 4', hint: 'Vượt qua Kiểm tra Chặng 4' },
  { id: 'streak-7', title: 'Ngọn lửa 7 ngày', hint: 'Giữ streak 7 ngày liên tiếp' },
  { id: 'streak-30', title: 'Thói quen 30 ngày', hint: 'Giữ streak 30 ngày liên tiếp' },
  { id: 'xp-100', title: 'Nhà du hành chăm chỉ', hint: 'Đạt 100 XP tích luỹ' },
  { id: 'xp-500', title: 'Cao thủ 500 XP', hint: 'Đạt 500 XP tích luỹ' },
];

export function evaluateUnlockedAccessories(xp: number): BaoAccessory[] {
  return BAO_ACCESSORIES.filter((a) => a.id !== 'none' && xp >= a.reqXp).map((a) => a.id);
}

export function evaluateBadges(opts: {
  completedLessons: string[];
  streak: number;
  xp: number;
  completedStories?: string[];
  totalReviews?: number;
}): string[] {
  const badges = new Set<string>();
  const done = new Set(opts.completedLessons);
  if (done.size >= 1) badges.add('first-lesson');
  if (done.size >= 4) badges.add('four-skills');
  if ((opts.completedStories?.length ?? 0) >= 1) badges.add('story-reader');
  if ((opts.totalReviews ?? 0) >= 50) badges.add('srs-50');
  if (done.has('stage-1-test')) badges.add('stage-1-master');
  if (done.has('stage-2-test')) badges.add('stage-2-master');
  if (done.has('stage-3-test')) badges.add('stage-3-master');
  if (done.has('stage-4-test')) badges.add('stage-4-master');
  if (opts.streak >= 7) badges.add('streak-7');
  if (opts.streak >= 30) badges.add('streak-30');
  if (opts.xp >= 100) badges.add('xp-100');
  if (opts.xp >= 500) badges.add('xp-500');
  return Array.from(badges);
}

export function createDefaultProgress(now = new Date()): ProgressRecord {
  return {
    id: 'main',
    xp: 0,
    dailyXp: 0,
    dailyXpDate: todayIsoDate(now),
    streak: 0,
    bestStreak: 0,
    freezesLeft: 2,
    activeDates: [],
    frozenDates: [],
    celebratedMilestones: [],
    completedLessons: [],
    completedStories: [],
    totalReviews: 0,
    lessonProgress: {},
    storyBookmarks: {},
    unlockedAccessories: [],
    equippedAccessory: 'none',
    badges: [],
    skillXp: { giaoTiep: 0, doc: 0, nghe: 0, viet: 0 },
    updatedAt: now.toISOString(),
  };
}

export function createDefaultSettings(now = new Date()): SettingsRecord {
  return {
    id: 'user',
    learnerName: 'Bạn mới',
    dailyGoalMinutes: 10,
    pinyinMode: 'new',
    sfxEnabled: true,
    reducedMotion: false,
    hanziSize: 'md',
    updatedAt: now.toISOString(),
  };
}

export async function ensureProgress(): Promise<ProgressRecord> {
  const db = await getDb();
  const existing = await db.get('progress', 'main');
  if (existing) return existing;
  const fresh = createDefaultProgress();
  await db.put('progress', fresh);
  return fresh;
}

export async function ensureSettings(): Promise<SettingsRecord> {
  const db = await getDb();
  const existing = await db.get('settings', 'user');
  if (existing) return existing;
  const fresh = createDefaultSettings();
  await db.put('settings', fresh);
  return fresh;
}

export async function saveSettings(patch: Partial<SettingsRecord>): Promise<SettingsRecord> {
  const db = await getDb();
  const cur = await ensureSettings();
  const next: SettingsRecord = {
    ...cur,
    ...patch,
    id: 'user',
    updatedAt: new Date().toISOString(),
  };
  await db.put('settings', next);
  return next;
}

export async function addCardToSrs(input: CreateCardInput): Promise<SrsCardRecord> {
  const db = await getDb();
  const key = cardKey(input.itemId, input.facet);
  const existing = await db.get('cards', key);
  if (existing) {
    const mergedTags = Array.from(new Set([...(existing.tags ?? []), ...(input.tags ?? [])]));
    const updated: SrsCardRecord = {
      ...existing,
      tags: mergedTags,
      example: existing.example ?? input.example,
      audio: existing.audio ?? input.audio,
      updatedAt: new Date().toISOString(),
    };
    await db.put('cards', updated);
    return updated;
  }
  const fresh = createOrGetCard(input);
  await db.put('cards', fresh);
  return fresh;
}

export async function getAllCards(): Promise<SrsCardRecord[]> {
  const db = await getDb();
  return db.getAll('cards');
}

export async function commitReview(record: SrsCardRecord, rating: ReviewRating, elapsedMs = 2000): Promise<SrsCardRecord> {
  const db = await getDb();
  const now = new Date();
  const { updatedCard, log } = reviewSrsCard(record, rating, now);
  const curProg = await ensureProgress();
  const nextReviews = (curProg.totalReviews ?? 0) + 1;
  const mergedBadges = Array.from(
    new Set([
      ...curProg.badges,
      ...evaluateBadges({
        completedLessons: curProg.completedLessons,
        streak: curProg.streak,
        xp: curProg.xp,
        completedStories: curProg.completedStories,
        totalReviews: nextReviews,
      }),
    ])
  );
  const tx = db.transaction(['cards', 'reviewLog', 'progress'], 'readwrite');
  await tx.objectStore('cards').put(updatedCard);
  await tx.objectStore('reviewLog').add({
    key: updatedCard.key,
    facet: updatedCard.facet,
    rating,
    state: log.state,
    reviewedAt: now.toISOString(),
    elapsedMs,
  });
  await tx.objectStore('progress').put({
    ...curProg,
    totalReviews: nextReviews,
    badges: mergedBadges,
    updatedAt: now.toISOString(),
  });
  await tx.done;
  return updatedCard;
}

export function todayIsoDate(now = new Date()): string {
  const y = now.getFullYear();
  const m = String(now.getMonth() + 1).padStart(2, '0');
  const d = String(now.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

export function computeStreak(dates: string[], refDate = new Date(), frozenDates: string[] = []): number {
  const activeSet = new Set(dates);
  const frozenSet = new Set(frozenDates);
  const hasCovered = (iso: string) => activeSet.has(iso) || frozenSet.has(iso);

  const cursor = new Date(refDate);
  const todayIso = todayIsoDate(cursor);
  // If user hasn't studied today yet, start checking streak continuity from yesterday
  if (!hasCovered(todayIso)) {
    cursor.setDate(cursor.getDate() - 1);
  }

  let streak = 0;
  while (hasCovered(todayIsoDate(cursor))) {
    streak += 1;
    cursor.setDate(cursor.getDate() - 1);
  }
  return streak;
}

export function getTodayXp(progress: ProgressRecord, now = new Date()): number {
  return progress.dailyXpDate === todayIsoDate(now) ? (progress.dailyXp ?? 0) : 0;
}

export async function equipAccessory(acc: ProgressRecord['equippedAccessory']): Promise<ProgressRecord> {
  const db = await getDb();
  const cur = await ensureProgress();
  const next: ProgressRecord = { ...cur, equippedAccessory: acc, updatedAt: new Date().toISOString() };
  await db.put('progress', next);
  return next;
}

export async function useStreakFreeze(): Promise<ProgressRecord> {
  const db = await getDb();
  const cur = await ensureProgress();
  if (cur.freezesLeft <= 0) return cur;

  const activeSet = new Set(cur.activeDates);
  const frozenList = [...(cur.frozenDates ?? [])];
  const frozenSet = new Set(frozenList);

  // Pick the most recent uncovered day (yesterday first, else walk back 1-7 days, else today) to protect streak continuity
  let targetIso = '';
  const probe = new Date();
  for (let offset = 1; offset <= 7; offset++) {
    probe.setTime(Date.now() - offset * 86400000);
    const iso = todayIsoDate(probe);
    if (!activeSet.has(iso) && !frozenSet.has(iso)) {
      targetIso = iso;
      break;
    }
  }
  if (!targetIso) {
    targetIso = todayIsoDate();
  }
  frozenSet.add(targetIso);
  const nextFrozen = Array.from(frozenSet).sort();
  const streak = computeStreak(cur.activeDates, new Date(), nextFrozen);
  const badges = Array.from(
    new Set([
      ...cur.badges,
      ...evaluateBadges({
        completedLessons: cur.completedLessons,
        streak,
        xp: cur.xp,
        completedStories: cur.completedStories,
        totalReviews: cur.totalReviews,
      }),
    ])
  );
  const next: ProgressRecord = {
    ...cur,
    freezesLeft: cur.freezesLeft - 1,
    frozenDates: nextFrozen,
    streak,
    bestStreak: Math.max(cur.bestStreak, streak),
    badges,
    updatedAt: new Date().toISOString(),
  };
  await db.put('progress', next);
  return next;
}

export async function markMilestoneCelebrated(milestone: number): Promise<void> {
  const db = await getDb();
  const cur = await ensureProgress();
  const set = new Set(cur.celebratedMilestones ?? []);
  set.add(milestone);
  await db.put('progress', { ...cur, celebratedMilestones: Array.from(set), updatedAt: new Date().toISOString() });
}

export async function setStoryBookmark(readingId: string, step = 1): Promise<void> {
  const db = await getDb();
  const cur = await ensureProgress();
  const next: ProgressRecord = {
    ...cur,
    storyBookmarks: { ...cur.storyBookmarks, [readingId]: step },
    updatedAt: new Date().toISOString(),
  };
  await db.put('progress', next);
}

export async function recordStudyActivity(opts: {
  xpEarned: number;
  skill?: 'giaoTiep' | 'doc' | 'nghe' | 'viet' | 'all';
  completedLessonId?: string;
  completedStoryId?: string;
  lessonRatio?: number;
}): Promise<ProgressRecord> {
  const db = await getDb();
  const cur = await ensureProgress();
  const today = todayIsoDate();
  const dates = Array.from(new Set([...cur.activeDates, today])).sort();
  const frozenDates = cur.frozenDates ?? [];
  const streak = computeStreak(dates, new Date(), frozenDates);
  const prevDaily = cur.dailyXpDate === today ? (cur.dailyXp ?? 0) : 0;

  const nextXp = cur.xp + opts.xpEarned;
  const unlocked = new Set([...cur.unlockedAccessories, ...evaluateUnlockedAccessories(nextXp)]);
  const completed = Array.from(
    new Set(opts.completedLessonId ? [...cur.completedLessons, opts.completedLessonId] : cur.completedLessons)
  );
  const completedStories = Array.from(
    new Set(opts.completedStoryId ? [...(cur.completedStories ?? []), opts.completedStoryId] : (cur.completedStories ?? []))
  );

  const badges = new Set([
    ...cur.badges,
    ...evaluateBadges({
      completedLessons: completed,
      streak,
      xp: nextXp,
      completedStories,
      totalReviews: cur.totalReviews,
    }),
  ]);

  const lessonProgress = { ...cur.lessonProgress };
  if (opts.completedLessonId) {
    lessonProgress[opts.completedLessonId] = 1;
  }

  const skillXp = { ...cur.skillXp };
  if (opts.skill === 'all') {
    const share = Math.round(opts.xpEarned / 4);
    skillXp.giaoTiep += share;
    skillXp.doc += share;
    skillXp.nghe += share;
    skillXp.viet += share;
  } else if (opts.skill) {
    skillXp[opts.skill] += opts.xpEarned;
  }

  const next: ProgressRecord = {
    ...cur,
    xp: nextXp,
    dailyXp: prevDaily + opts.xpEarned,
    dailyXpDate: today,
    streak,
    bestStreak: Math.max(cur.bestStreak, streak),
    activeDates: dates,
    frozenDates,
    completedLessons: completed,
    completedStories,
    lessonProgress,
    unlockedAccessories: Array.from(unlocked),
    badges: Array.from(badges),
    skillXp,
    updatedAt: new Date().toISOString(),
  };
  await db.put('progress', next);
  return next;
}
