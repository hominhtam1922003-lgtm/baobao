import { describe, expect, it, beforeEach } from 'vitest';
import 'fake-indexeddb/auto';
import { resetDbForTests, getDb } from './db';
import { exportBackupJson, importBackupJson, getAutoBackup } from './progressBackup';

describe('progressBackup seam', () => {
  beforeEach(async () => {
    await resetDbForTests();
  });

  it('exports all 4 IndexedDB stores and restores them cleanly after creating an auto-backup', async () => {
    const db = await getDb();
    await db.put('progress', {
      id: 'main',
      xp: 120,
      streak: 3,
      bestStreak: 5,
      freezesLeft: 2,
      activeDates: ['2026-11-26'],
      completedLessons: ['t1-giao-tiep'],
      lessonProgress: { 't1-giao-tiep': 1 },
      storyBookmarks: {},
      unlockedAccessories: ['bamboo-hat'],
      equippedAccessory: 'bamboo-hat',
      badges: ['first-lesson'],
      skillXp: { giaoTiep: 60, doc: 20, nghe: 20, viet: 20 },
      updatedAt: '2026-11-26T05:00:00.000Z',
    });
    await db.put('settings', {
      id: 'user',
      learnerName: 'Minh Tâm',
      dailyGoalMinutes: 10,
      pinyinMode: 'new',
      sfxEnabled: true,
      reducedMotion: false,
      hanziSize: 'md',
      updatedAt: '2026-11-26T05:00:00.000Z',
    });

    const exported = await exportBackupJson();
    const parsed = JSON.parse(exported);
    expect(parsed.version).toBe(1);
    expect(parsed.stores.progress).toHaveLength(1);
    expect(parsed.stores.settings).toHaveLength(1);

    // Mutate DB to represent older state, then import exported snapshot
    await db.put('progress', {
      id: 'main',
      xp: 15,
      streak: 1,
      bestStreak: 1,
      freezesLeft: 2,
      activeDates: [],
      completedLessons: [],
      lessonProgress: {},
      storyBookmarks: {},
      unlockedAccessories: [],
      equippedAccessory: 'none',
      badges: [],
      skillXp: { giaoTiep: 15, doc: 0, nghe: 0, viet: 0 },
      updatedAt: '2026-11-26T04:00:00.000Z',
    });

    const result = await importBackupJson(exported);
    expect(result.ok).toBe(true);

    const restored = await db.get('progress', 'main');
    expect(restored?.xp).toBe(120);

    const backup = getAutoBackup();
    expect(backup).toBeTruthy();
    expect(JSON.parse(backup!).stores.progress[0].xp).toBe(15);
  });

  it('rejects corrupt or invalid JSON without destroying existing IndexedDB state', async () => {
    const db = await getDb();
    await db.put('settings', {
      id: 'user',
      learnerName: 'An Toàn',
      dailyGoalMinutes: 10,
      pinyinMode: 'all',
      sfxEnabled: true,
      reducedMotion: false,
      hanziSize: 'md',
      updatedAt: '2026-11-26T05:00:00.000Z',
    });

    const bad1 = await importBackupJson('{not valid json');
    expect(bad1.ok).toBe(false);

    const bad2 = await importBackupJson(JSON.stringify({ version: 99, stores: {} }));
    expect(bad2.ok).toBe(false);

    const stillThere = await db.get('settings', 'user');
    expect(stillThere?.learnerName).toBe('An Toàn');
  });
});
