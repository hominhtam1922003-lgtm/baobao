import { describe, expect, it } from 'vitest';
import 'fake-indexeddb/auto';
import {
  createOrGetCard,
  reviewSrsCard,
  previewIntervals,
  filterQueue,
  createDefaultProgress,
  type SrsCardRecord,
} from './srsEngine';

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
});
