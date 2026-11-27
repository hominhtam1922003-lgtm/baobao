import type { CurriculumMeta, LessonItem, ReadingItem, WordItem } from '../types/curriculum';

export interface RadicalsBundle {
  radicals: Record<string, { radical: string; meaning: string; chars: string[] }>;
  characters: Record<string, { radical: string; decomposition: string; etymology?: { type?: string; hint?: string }; definition: string }>;
}

const base = import.meta.env.BASE_URL;

const cache = {
  curriculum: null as CurriculumMeta | null,
  radicals: null as RadicalsBundle | null,
  wordsByStage: new Map<number, WordItem[]>(),
  lessonsByStage: new Map<number, LessonItem[]>(),
  readingsByStage: new Map<number, ReadingItem[]>(),
  wordIndex: new Map<string, WordItem>(),
};

async function fetchJson<T>(relPath: string): Promise<T> {
  const res = await fetch(`${base}${relPath}`);
  if (!res.ok) {
    throw new Error(`Không tải được dữ liệu (${res.status}): ${relPath}`);
  }
  return res.json() as Promise<T>;
}

export async function loadCurriculum(): Promise<CurriculumMeta> {
  if (!cache.curriculum) {
    cache.curriculum = await fetchJson<CurriculumMeta>('content/curriculum.json');
  }
  return cache.curriculum;
}

export async function loadRadicals(): Promise<RadicalsBundle> {
  if (!cache.radicals) {
    cache.radicals = await fetchJson<RadicalsBundle>('content/radicals.json');
  }
  return cache.radicals;
}

export async function loadStageWords(stage = 1): Promise<WordItem[]> {
  if (!cache.wordsByStage.has(stage)) {
    const words = await fetchJson<WordItem[]>(`content/stage-${stage}/words.json`);
    cache.wordsByStage.set(stage, words);
    for (const w of words) {
      cache.wordIndex.set(w.hanzi, w);
      cache.wordIndex.set(w.id, w);
    }
  }
  return cache.wordsByStage.get(stage)!;
}

export async function loadStageLessons(stage = 1): Promise<LessonItem[]> {
  if (!cache.lessonsByStage.has(stage)) {
    const lessons = await fetchJson<LessonItem[]>(`content/stage-${stage}/lessons.json`);
    cache.lessonsByStage.set(stage, lessons);
  }
  return cache.lessonsByStage.get(stage)!;
}

export async function loadStageReadings(stage = 1): Promise<ReadingItem[]> {
  if (!cache.readingsByStage.has(stage)) {
    const readings = await fetchJson<ReadingItem[]>(`content/stage-${stage}/readings.json`);
    cache.readingsByStage.set(stage, readings);
  }
  return cache.readingsByStage.get(stage)!;
}

export function resolveStageForTopic(topicId: number): number {
  if (topicId <= 8) return 1;
  if (topicId <= 16) return 2;
  if (topicId <= 24) return 3;
  return 4;
}

export function resolveStageForLessonId(lessonId: string): number {
  const stageMatch = /^stage-(\d+)-test$/.exec(lessonId);
  if (stageMatch) {
    return Math.min(4, Math.max(1, Number(stageMatch[1])));
  }
  const topicMatch = /^t(\d+)-/.exec(lessonId);
  if (topicMatch) {
    return resolveStageForTopic(Number(topicMatch[1]));
  }
  return 1;
}

export function resolveStageForReadingId(readingId: string): number {
  const storyMatch = /^story-c(\d+)$/.exec(readingId);
  if (storyMatch) {
    return Math.min(4, Math.max(1, Number(storyMatch[1])));
  }
  const topicMatch = /^r-t(\d+)$/.exec(readingId);
  if (topicMatch) {
    return resolveStageForTopic(Number(topicMatch[1]));
  }
  return 1;
}

export async function loadStageBundle(stage: number): Promise<{
  words: WordItem[];
  lessons: LessonItem[];
  readings: ReadingItem[];
}> {
  const [words, lessons, readings] = await Promise.all([
    loadStageWords(stage),
    loadStageLessons(stage),
    loadStageReadings(stage),
  ]);
  return { words, lessons, readings };
}

export function lookupWord(hanziOrId: string): WordItem | undefined {
  return cache.wordIndex.get(hanziOrId);
}

export function collectStageAssetUrls(
  stage: number,
  words: WordItem[],
  lessons: LessonItem[],
  readings: ReadingItem[]
): string[] {
  const urls = new Set<string>([
    `${base}content/curriculum.json`,
    `${base}content/radicals.json`,
    `${base}content/stage-${stage}/words.json`,
    `${base}content/stage-${stage}/lessons.json`,
    `${base}content/stage-${stage}/readings.json`,
  ]);

  const addRel = (rel?: string) => {
    if (rel) urls.add(`${base}${rel.replace(/^\//, '')}`);
  };

  for (const w of words) {
    addRel(w.audio);
    for (const ex of w.examples) addRel(ex.audio);
  }
  for (const l of lessons) {
    for (const p of l.patterns ?? []) addRel(p.audio);
    for (const gex of l.grammarSpotlight?.examples ?? []) addRel(gex.audio);
    for (const t of l.dialogue ?? []) addRel(t.audio);
    for (const rp of l.roleplay ?? []) {
      addRel(rp.npcAudio);
      addRel(rp.replyAudio);
    }
    for (const ex of l.exercises ?? []) {
      addRel(ex.audio);
      addRel(ex.audioSlow);
    }
    for (const tr of l.listeningTracks ?? []) {
      addRel(tr.audio);
      addRel(tr.audioSlow);
    }
    for (const wc of l.writingChars ?? []) {
      urls.add(`${base}strokes/${encodeURIComponent(wc.char)}.json`);
    }
    for (const stItem of l.stageTestItems ?? []) {
      addRel(stItem.audio);
      addRel(stItem.audioSlow);
      if (stItem.writingChar) {
        urls.add(`${base}strokes/${encodeURIComponent(stItem.writingChar.char)}.json`);
      }
    }
  }
  for (const r of readings) {
    addRel(r.audioFull);
    for (const sa of r.audioSentences ?? []) addRel(sa);
  }

  return Array.from(urls);
}
