import { describe, expect, it } from 'vitest';
import {
  resolveStageForLessonId,
  resolveStageForReadingId,
  resolveStageForTopic,
} from './contentLoader';

describe('contentLoader stage resolution across 28 topics, 4 stories, and 4 stage tests', () => {
  it('maps topics 1-28 to stages 1-4 accurately', () => {
    expect(resolveStageForTopic(1)).toBe(1);
    expect(resolveStageForTopic(8)).toBe(1);
    expect(resolveStageForTopic(9)).toBe(2);
    expect(resolveStageForTopic(16)).toBe(2);
    expect(resolveStageForTopic(17)).toBe(3);
    expect(resolveStageForTopic(24)).toBe(3);
    expect(resolveStageForTopic(25)).toBe(4);
    expect(resolveStageForTopic(28)).toBe(4);
  });

  it('resolves lesson IDs and stage tests to the correct stage', () => {
    expect(resolveStageForLessonId('t1-giao-tiep')).toBe(1);
    expect(resolveStageForLessonId('t9-nghe')).toBe(2);
    expect(resolveStageForLessonId('t20-viet')).toBe(3);
    expect(resolveStageForLessonId('t28-doc')).toBe(4);
    expect(resolveStageForLessonId('stage-1-test')).toBe(1);
    expect(resolveStageForLessonId('stage-3-test')).toBe(3);
    expect(resolveStageForLessonId('stage-4-test')).toBe(4);
  });

  it('resolves topic readings and story chapters 1-4 to the correct stage', () => {
    expect(resolveStageForReadingId('r-t1')).toBe(1);
    expect(resolveStageForReadingId('r-t12')).toBe(2);
    expect(resolveStageForReadingId('r-t21')).toBe(3);
    expect(resolveStageForReadingId('r-t27')).toBe(4);
    expect(resolveStageForReadingId('story-c1')).toBe(1);
    expect(resolveStageForReadingId('story-c2')).toBe(2);
    expect(resolveStageForReadingId('story-c3')).toBe(3);
    expect(resolveStageForReadingId('story-c4')).toBe(4);
  });
});
