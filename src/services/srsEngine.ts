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
import { getDb, type ProgressRecord, type SettingsRecord, type SrsCardRecord } from './db';

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

export function createDefaultProgress(now = new Date()): ProgressRecord {
  return {
    id: 'main',
    xp: 0,
    streak: 0,
    bestStreak: 0,
    freezesLeft: 2,
    activeDates: [],
    completedLessons: [],
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
  const tx = db.transaction(['cards', 'reviewLog'], 'readwrite');
  await tx.objectStore('cards').put(updatedCard);
  await tx.objectStore('reviewLog').add({
    key: updatedCard.key,
    facet: updatedCard.facet,
    rating,
    state: log.state,
    reviewedAt: now.toISOString(),
    elapsedMs,
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

export async function recordStudyActivity(opts: {
  xpEarned: number;
  skill?: 'giaoTiep' | 'doc' | 'nghe' | 'viet';
  completedLessonId?: string;
  lessonRatio?: number;
}): Promise<ProgressRecord> {
  const db = await getDb();
  const cur = await ensureProgress();
  const today = todayIsoDate();
  const dates = Array.from(new Set([...cur.activeDates, today])).sort();

  // Compute current consecutive streak ending today
  let streak = 0;
  const cursor = new Date();
  while (true) {
    const iso = todayIsoDate(cursor);
    if (dates.includes(iso)) {
      streak += 1;
      cursor.setDate(cursor.getDate() - 1);
    } else {
      break;
    }
  }

  const nextXp = cur.xp + opts.xpEarned;
  const unlocked = new Set(cur.unlockedAccessories);
  if (nextXp >= 30) unlocked.add('bamboo-hat');
  if (nextXp >= 80) unlocked.add('red-scarf');
  if (nextXp >= 160) unlocked.add('star-glasses');
  if (nextXp >= 300) unlocked.add('crown');

  const badges = new Set(cur.badges);
  const completed = Array.from(
    new Set(opts.completedLessonId ? [...cur.completedLessons, opts.completedLessonId] : cur.completedLessons)
  );
  if (completed.length >= 1) badges.add('first-lesson');
  if (completed.length >= 4) badges.add('four-skills');
  if (streak >= 7) badges.add('streak-7');
  if (nextXp >= 100) badges.add('xp-100');

  const lessonProgress = { ...cur.lessonProgress };
  if (opts.completedLessonId) {
    lessonProgress[opts.completedLessonId] = 1;
  }

  const skillXp = { ...cur.skillXp };
  if (opts.skill) {
    skillXp[opts.skill] += opts.xpEarned;
  }

  const next: ProgressRecord = {
    ...cur,
    xp: nextXp,
    streak,
    bestStreak: Math.max(cur.bestStreak, streak),
    activeDates: dates,
    completedLessons: completed,
    lessonProgress,
    unlockedAccessories: Array.from(unlocked),
    badges: Array.from(badges),
    skillXp,
    updatedAt: new Date().toISOString(),
  };
  await db.put('progress', next);
  return next;
}
