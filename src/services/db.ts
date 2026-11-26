import { openDB, deleteDB, type DBSchema, type IDBPDatabase } from 'idb';
import type { Card } from 'ts-fsrs';
import type { CardFacet, ExampleSentence, ReviewRating } from '../types/curriculum';

export interface SrsCardRecord {
  key: string;
  itemId: string;
  facet: CardFacet;
  hanzi: string;
  pinyin: string;
  meaningVi: string;
  example?: ExampleSentence;
  audio?: string;
  tags?: string[];
  isWeakWriting?: boolean;
  lastRating?: ReviewRating;
  card: Card;
  createdAt: string;
  updatedAt: string;
}

export interface ReviewLogRecord {
  id?: number;
  key: string;
  facet: CardFacet;
  rating: string;
  state: number;
  reviewedAt: string;
  elapsedMs: number;
}

export interface ProgressRecord {
  id: 'main';
  xp: number;
  streak: number;
  bestStreak: number;
  freezesLeft: number;
  activeDates: string[];
  completedLessons: string[];
  lessonProgress: Record<string, number>;
  storyBookmarks: Record<string, number>;
  unlockedAccessories: string[];
  equippedAccessory: 'none' | 'bamboo-hat' | 'red-scarf' | 'star-glasses' | 'crown';
  badges: string[];
  skillXp: {
    giaoTiep: number;
    doc: number;
    nghe: number;
    viet: number;
  };
  updatedAt: string;
}

export interface SettingsRecord {
  id: 'user';
  learnerName: string;
  dailyGoalMinutes: 5 | 10 | 20;
  pinyinMode: 'all' | 'new' | 'off';
  sfxEnabled: boolean;
  reducedMotion: boolean;
  hanziSize: 'sm' | 'md' | 'lg';
  updatedAt: string;
}

export interface BaoBaoDB extends DBSchema {
  cards: {
    key: string;
    value: SrsCardRecord;
    indexes: { 'by-facet': CardFacet; 'by-updated': string };
  };
  reviewLog: {
    key: number;
    value: ReviewLogRecord;
    indexes: { 'by-key': string; 'by-date': string };
  };
  progress: {
    key: string;
    value: ProgressRecord;
  };
  settings: {
    key: string;
    value: SettingsRecord;
  };
}

const DB_NAME = 'baobao-db';
const DB_VERSION = 1;

let dbPromise: Promise<IDBPDatabase<BaoBaoDB>> | null = null;

export function getDb(): Promise<IDBPDatabase<BaoBaoDB>> {
  if (!dbPromise) {
    dbPromise = openDB<BaoBaoDB>(DB_NAME, DB_VERSION, {
      upgrade(db) {
        if (!db.objectStoreNames.contains('cards')) {
          const cards = db.createObjectStore('cards', { keyPath: 'key' });
          cards.createIndex('by-facet', 'facet');
          cards.createIndex('by-updated', 'updatedAt');
        }
        if (!db.objectStoreNames.contains('reviewLog')) {
          const logs = db.createObjectStore('reviewLog', { keyPath: 'id', autoIncrement: true });
          logs.createIndex('by-key', 'key');
          logs.createIndex('by-date', 'reviewedAt');
        }
        if (!db.objectStoreNames.contains('progress')) {
          db.createObjectStore('progress', { keyPath: 'id' });
        }
        if (!db.objectStoreNames.contains('settings')) {
          db.createObjectStore('settings', { keyPath: 'id' });
        }
      },
    });
  }
  return dbPromise;
}

export async function resetDbForTests(): Promise<void> {
  if (dbPromise) {
    const db = await dbPromise;
    db.close();
    dbPromise = null;
  }
  await deleteDB(DB_NAME);
}
