export type CardFacet = 'vocab' | 'sentence' | 'writing';

export type ReviewRating = 'Again' | 'Hard' | 'Good' | 'Easy';

export interface ExampleSentence {
  hanzi: string;
  pinyin: string;
  vi: string;
  audio?: string;
}

export interface WordItem {
  id: string;
  hanzi: string;
  pinyin: string;
  meaningVi: string;
  radical: string;
  level: number;
  frequency?: number;
  mnemonic?: string;
  literalVi?: string;
  usageNoteVi?: string;
  partOfSpeech?: string;
  audio?: string;
  examples: ExampleSentence[];
}

export interface GrammarSpotlight {
  title: string;
  formula: string;
  explainVi: string;
  vsVietnameseVi?: string;
  commonMistakeVi?: string;
  examples: ExampleSentence[];
}

export interface PatternItem {
  id: string;
  frame: string;
  pinyin: string;
  meaningVi: string;
  exampleHanzi: string;
  examplePinyin: string;
  exampleVi: string;
  audio?: string;
  slots: {
    promptVi: string;
    choices: { hanzi: string; pinyin: string; vi: string }[];
    answerHanzi: string;
  };
}

export interface DialogueTurn {
  speaker: string;
  voiceRole?: 'female' | 'male' | 'formal';
  hanzi: string;
  pinyin: string;
  vi: string;
  audio?: string;
  mode?: 'npc' | 'choice' | 'tiles' | 'pinyin' | 'shadow';
  goalLabel?: string;
  choices?: { hanzi: string; pinyin: string; vi: string; correct: boolean }[];
  tilePrompt?: string[];
  acceptedPinyin?: string[];
}

export interface ExerciseItem {
  id: string;
  kind:
    | 'meaning-choice'
    | 'hanzi-choice'
    | 'sentence-tiles'
    | 'match-pairs'
    | 'fill-blank'
    | 'listen-meaning'
    | 'listen-hanzi'
    | 'listen-tiles'
    | 'listen-blank'
    | 'listen-dialogue'
    | 'dictation';
  promptVi: string;
  audioText?: string;
  audio?: string;
  audioSlow?: string;
  hanziPrompt?: string;
  pinyinPrompt?: string;
  options?: { label: string; sub?: string; value: string }[];
  pairs?: { hanzi: string; pinyin: string; vi: string }[];
  tiles?: string[];
  answer: string;
  explainVi?: string;
}

export interface RoleplayTurn {
  npcHanzi: string;
  npcPinyin: string;
  npcVi: string;
  npcAudio?: string;
  promptVi: string;
  options: { hanzi: string; pinyin: string; vi: string; correct: boolean }[];
  expectedHanzi: string;
  replyAudio?: string;
}

export interface WritingCharSpec {
  char: string;
  pinyin: string;
  meaningVi: string;
  radical: string;
  radicalNoteVi: string;
  lookalikes: { hanzi: string; pinyin: string; vi: string }[];
}

export interface StageTestItem {
  id: string;
  skill: 'giao-tiep' | 'doc' | 'nghe' | 'viet';
  promptVi: string;
  passageHanzi?: string;
  passagePinyin?: string;
  passageVi?: string;
  audioText?: string;
  audio?: string;
  audioSlow?: string;
  writingChar?: WritingCharSpec;
  options?: { label: string; value: string }[];
  answer: string;
  explainVi?: string;
}

export interface LessonItem {
  id: string;
  stage: number;
  topicId: number;
  title: string;
  type: 'giao-tiep' | 'doc' | 'nghe' | 'viet' | 'stage-test';
  xp: number;
  coinReward?: number;
  storyContextVi?: string;
  bridgeFromPrevVi?: string;
  bridgeToNextVi?: string;
  recapWordIds?: string[];
  grammarSpotlight?: GrammarSpotlight;
  cultureTipVi?: string;
  newWords: string[];
  patterns?: PatternItem[];
  dialogue?: DialogueTurn[];
  exercises?: ExerciseItem[];
  roleplay?: RoleplayTurn[];
  listeningTracks?: { id: string; speaker: string; hanzi: string; pinyin: string; vi: string; audio?: string; audioSlow?: string; voiceRole?: string }[];
  writingChars?: WritingCharSpec[];
  stageTestItems?: StageTestItem[];
  readingId?: string;
}

export interface ReadingToken {
  w: string;
  pinyin: string;
  isNew?: boolean;
}

export interface ReadingParagraph {
  hanzi: string;
  vi: string;
  audio?: string;
  tokens: ReadingToken[];
}

export interface ReadingQuestion {
  id: string;
  type: 'mcq' | 'tf' | 'detail';
  q: string;
  options: string[];
  answer: number;
  explainVi: string;
}

export interface ReadingItem {
  id: string;
  stage: number;
  topicId: number;
  title: string;
  mode: 'fluent' | 'study';
  knownPercent: number;
  paragraphs: ReadingParagraph[];
  newWords: string[];
  questions: ReadingQuestion[];
  audioFull?: string;
  audioSentences?: string[];
  isStoryChapter?: boolean;
  chapterNumber?: number;
  cliffhangerVi?: string;
}

export interface TopicMeta {
  id: number;
  stage: number;
  title: string;
  subtitle: string;
  storyTagVi?: string;
  connectsFromVi?: string;
  ready: boolean;
  lessonIds: string[];
  readingId?: string;
}

export interface StageMeta {
  id: number;
  title: string;
  subtitle: string;
  colorToken: string;
  grammarNotes: { title: string; pattern: string; explainVi: string; exampleHanzi: string; exampleVi: string }[];
  storyChapter: { title: string; teaserVi: string; readingId?: string };
  stageTestId?: string;
  topics: TopicMeta[];
}

export interface CurriculumMeta {
  stages: StageMeta[];
}
