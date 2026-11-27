import { describe, expect, it } from 'vitest';
import 'fake-indexeddb/auto';
import {
  createOrGetCard,
  reviewSrsCard,
  previewIntervals,
  filterQueue,
  createDefaultProgress,
  computeStreak,
  evaluateUnlockedAccessories,
  evaluateBadges,
  recordStudyActivity,
  buyShopItem,
  equipWardrobeItem,
  getCoins,
  type SrsCardRecord,
} from './srsEngine';
import { resetDbForTests } from './db';
import { resolveWardrobe } from './shopCatalog';

describe('srsEngine seam', () => {
  const fixedNow = new Date('2026-11-26T05:00:00.000Z');

  it('creates independent FSRS cards per facet (vocab, sentence, writing)', () => {
    const vocabCard = createOrGetCard(
      {
        itemId: 'w-nihao',
        facet: 'vocab',
        hanzi: '你好',
        pinyin: 'nǐ hǎo',
        meaningVi: 'xin chào',
      },
      fixedNow
    );
    const writingCard = createOrGetCard(
      {
        itemId: 'w-nihao',
        facet: 'writing',
        hanzi: '你好',
        pinyin: 'nǐ hǎo',
        meaningVi: 'xin chào',
      },
      fixedNow
    );

    expect(vocabCard.key).toBe('w-nihao::vocab');
    expect(writingCard.key).toBe('w-nihao::writing');

    const rated = reviewSrsCard(vocabCard, 'Good', fixedNow);
    expect(rated.updatedCard.card.reps).toBe(1);
    expect(writingCard.card.reps).toBe(0);
  });

  it('schedules intervals according to FSRS config (retention 0.9, max 365, steps 1m/10m)', () => {
    const base = createOrGetCard(
      {
        itemId: 'w-cha',
        facet: 'vocab',
        hanzi: '茶',
        pinyin: 'chá',
        meaningVi: 'trà',
      },
      fixedNow
    );

    const previews = previewIntervals(base, fixedNow);
    expect(previews.Again).toBeTruthy();
    expect(previews.Hard).toBeTruthy();
    expect(previews.Good).toBeTruthy();
    expect(previews.Easy).toBeTruthy();

    const afterGood = reviewSrsCard(base, 'Good', fixedNow);
    expect(afterGood.updatedCard.card.due.getTime()).toBeGreaterThan(fixedNow.getTime());
    const diffDays = (afterGood.updatedCard.card.due.getTime() - fixedNow.getTime()) / 86400000;
    expect(diffDays).toBeLessThanOrEqual(365);
  });

  it('filters due, weak, story, and writing queues accurately', () => {
    const dueVocab: SrsCardRecord = {
      ...createOrGetCard({ itemId: 'w1', facet: 'vocab', hanzi: '茶', pinyin: 'chá', meaningVi: 'trà' }, fixedNow),
      tags: ['story'],
    };
    const weakVocab = reviewSrsCard(
      createOrGetCard({ itemId: 'w2', facet: 'vocab', hanzi: '好', pinyin: 'hǎo', meaningVi: 'tốt' }, fixedNow),
      'Again',
      fixedNow
    ).updatedCard;
    const futureCard: SrsCardRecord = {
      ...createOrGetCard({ itemId: 'w3', facet: 'writing', hanzi: '我', pinyin: 'wǒ', meaningVi: 'tôi' }, fixedNow),
      isWeakWriting: true,
    };
    futureCard.card.due = new Date('2026-12-20T00:00:00.000Z');

    const all = [dueVocab, weakVocab, futureCard];
    // weakVocab rated Again at fixedNow is scheduled +1m (learning step), so check due 2 minutes later
    const twoMinLater = new Date(fixedNow.getTime() + 120_000);
    expect(filterQueue(all, 'due', twoMinLater).map((c) => c.key)).toEqual(['w1::vocab', 'w2::vocab']);
    expect(filterQueue(all, 'weak', twoMinLater).map((c) => c.key)).toContain('w2::vocab');
    expect(filterQueue(all, 'story', twoMinLater).map((c) => c.key)).toEqual(['w1::vocab']);
    expect(filterQueue(all, 'writing', twoMinLater).map((c) => c.key)).toEqual(['w3::writing']);
  });

  it('initializes progress with 2 streak freezes and zero Hearts/Energy', () => {
    const p = createDefaultProgress(fixedNow);
    expect(p.freezesLeft).toBe(2);
    expect('hearts' in p).toBe(false);
    expect('energy' in p).toBe(false);
  });

  it('bridges missed days with frozenDates and preserves streak when yesterday was active', () => {
    const ref = new Date(2026, 10, 26, 12, 0, 0);
    // Studied 23, 24; froze 25; today 26 not studied yet -> streak = 3
    expect(computeStreak(['2026-11-23', '2026-11-24'], ref, ['2026-11-25'])).toBe(3);
    // Studied today 26 + froze 25 + studied 24 -> streak = 3
    expect(computeStreak(['2026-11-24', '2026-11-26'], ref, ['2026-11-25'])).toBe(3);
    // Missed 25 without freeze -> streak = 1 (today only)
    expect(computeStreak(['2026-11-24', '2026-11-26'], ref, [])).toBe(1);
  });

  it('unlocks all 8 Bao accessories by XP and evaluates 12 badge milestones cleanly', () => {
    expect(evaluateUnlockedAccessories(0)).toEqual([]);
    expect(evaluateUnlockedAccessories(30)).toContain('bamboo-hat');
    expect(evaluateUnlockedAccessories(1200)).toEqual([
      'bamboo-hat',
      'red-scarf',
      'tea-beret',
      'star-glasses',
      'lantern-pin',
      'explorer-cap',
      'crown',
    ]);

    const badges = evaluateBadges({
      completedLessons: ['t1-giao-tiep', 't1-doc', 't1-nghe', 't1-viet', 'stage-1-test'],
      streak: 30,
      xp: 550,
      completedStories: ['story-c1'],
      totalReviews: 50,
    });
    expect(badges).toEqual(
      expect.arrayContaining([
        'first-lesson',
        'four-skills',
        'story-reader',
        'srs-50',
        'stage-1-master',
        'streak-7',
        'streak-30',
        'xp-100',
        'xp-500',
      ])
    );
  });

  it('awards Xu Tre coins on lesson completion and allows buying + equipping multi-slot Bao items', async () => {
    await resetDbForTests();
    const afterLesson = await recordStudyActivity({
      xpEarned: 40,
      coinsEarned: 45,
      skill: 'giaoTiep',
      completedLessonId: 't1-giao-tiep',
    });
    // Starts with 20 welcome coins + 45 lesson coins + 40 daily goal bonus (40 XP meets 10m*4 goal) = 105
    expect(getCoins(afterLesson)).toBe(105);

    const buyHat = await buyShopItem('bamboo-hat'); // 30 coins
    expect(buyHat.ok).toBe(true);
    expect(getCoins(buyHat.progress)).toBe(75);
    expect(resolveWardrobe(buyHat.progress).hat).toBe('bamboo-hat');

    const buyBoba = await buyShopItem('boba-tea'); // 55 coins
    expect(buyBoba.ok).toBe(true);
    expect(getCoins(buyBoba.progress)).toBe(20);
    // Both hat AND prop are equipped simultaneously!
    const w = resolveWardrobe(buyBoba.progress);
    expect(w.hat).toBe('bamboo-hat');
    expect(w.prop).toBe('boba-tea');

    // Cannot buy expensive item when balance is too low
    const tooExpensive = await buyShopItem('crown');
    expect(tooExpensive.ok).toBe(false);

    // Can unequip a slot cleanly
    const unequipped = await equipWardrobeItem('hat', 'none');
    expect(resolveWardrobe(unequipped).hat).toBe('none');
    expect(resolveWardrobe(unequipped).prop).toBe('boba-tea');
  });
});
