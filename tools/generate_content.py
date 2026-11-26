"""Generate level-controlled Chinese lessons, readings, stories, stage tests, and Tatoeba translations via Gemini API."""

from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import time
from typing import List, Literal
from pydantic import BaseModel, Field

from level_checker import check_level, count_hanzi_chars

ROOT = Path(__file__).resolve().parent.parent


def _call_structured(api_key: str, prompt: str, schema_cls: type[BaseModel], timeout: float = 30.0):
    from google import genai

    client = genai.Client(api_key=api_key, http_options={"timeout": int(timeout * 1000)})
    models = ("gemini-3.1-flash-lite", "gemini-3.5-flash-lite")
    last_err: Exception | None = None
    for attempt in range(3):
        model_name = models[0] if attempt < 2 else models[1]
        try:
            interaction = client.interactions.create(
                model=model_name,
                input=prompt,
                store=False,
                response_format={
                    "type": "text",
                    "mime_type": "application/json",
                    "schema": schema_cls.model_json_schema(),
                },
                timeout=timeout,
            )
            return schema_cls.model_validate_json(interaction.output_text)
        except Exception as exc:
            last_err = exc
            time.sleep(1.5 * (2**attempt))
    raise RuntimeError(f"Gemini structured call failed: {last_err}")


# ---------------- Pydantic Schemas ----------------


class TatoebaViItem(BaseModel):
    cmn: str
    vi: str


class TatoebaViBatch(BaseModel):
    items: List[TatoebaViItem]


class PatternSlotChoiceOut(BaseModel):
    hanzi: str
    vi: str


class PatternOut(BaseModel):
    frame: str
    meaningVi: str
    exampleHanzi: str
    exampleVi: str
    promptVi: str
    choices: List[PatternSlotChoiceOut]
    answerHanzi: str


class DialogueChoiceOut(BaseModel):
    hanzi: str
    vi: str
    correct: bool


class DialogueTurnOut(BaseModel):
    speaker: str
    voiceRole: Literal["female", "male", "formal"]
    hanzi: str
    vi: str
    mode: Literal["npc", "choice", "tiles", "pinyin"]
    goalLabel: str = ""
    choices: List[DialogueChoiceOut] = Field(default_factory=list)
    tilePrompt: List[str] = Field(default_factory=list)


class CommMcqOut(BaseModel):
    promptVi: str
    hanziPrompt: str
    options: List[str]
    answer: str


class CommRoleplayOut(BaseModel):
    npcHanzi: str
    npcVi: str
    promptVi: str
    choices: List[DialogueChoiceOut]
    expectedHanzi: str


class TopicCommOut(BaseModel):
    patterns: List[PatternOut]
    dialogue: List[DialogueTurnOut]
    meaningQuestion: CommMcqOut
    hanziAudioText: str
    hanziAudioOptions: List[str]
    tilePromptVi: str
    tileWords: List[str]
    roleplay: List[CommRoleplayOut]


class ReadingParaOut(BaseModel):
    hanzi: str
    vi: str


class ReadingQuestionOut(BaseModel):
    type: Literal["mcq", "tf", "detail"]
    q: str
    options: List[str]
    answer: int
    explainVi: str


class TopicReadingOut(BaseModel):
    title: str
    paragraphs: List[ReadingParaOut]
    questions: List[ReadingQuestionOut]


class StoryChapterOut(BaseModel):
    title: str
    cliffhangerVi: str
    paragraphs: List[ReadingParaOut]
    questions: List[ReadingQuestionOut]


class ListenTrackOut(BaseModel):
    speaker: str
    voiceRole: Literal["female", "male", "formal"]
    hanzi: str
    vi: str


class ListenMcqOut(BaseModel):
    promptVi: str
    audioText: str
    options: List[str]
    answer: str


class ListenTilesOut(BaseModel):
    promptVi: str
    audioText: str
    tiles: List[str]


class ListenBlankOut(BaseModel):
    promptVi: str
    audioText: str
    options: List[str]
    answer: str


class TopicListeningOut(BaseModel):
    listeningTracks: List[ListenTrackOut]
    listenMeaning: ListenMcqOut
    listenHanzi: ListenMcqOut
    listenTiles: ListenTilesOut
    listenBlank: ListenBlankOut
    listenDialogue: ListenMcqOut
    dictationText: str
    dictationTiles: List[str]


class StageTestGeneratedItem(BaseModel):
    skill: Literal["giao-tiep", "doc", "nghe"]
    promptVi: str
    passageHanzi: str = ""
    passageVi: str = ""
    audioText: str = ""
    options: List[str]
    answer: str
    explainVi: str


class StageTestOut(BaseModel):
    items: List[StageTestGeneratedItem]


class RadicalNoteItem(BaseModel):
    char: str
    radical: str
    noteVi: str


class RadicalNoteBatch(BaseModel):
    items: List[RadicalNoteItem]


# ---------------- Controlled Generation Helpers ----------------


def translate_tatoeba_en_batch(pairs: list[tuple[str, str]]) -> dict[str, str]:
    """Translate list of (cmn, eng) into natural Vietnamese."""
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key or not pairs:
        return {}
    lines = [f"{i+1}. {cmn} || EN: {eng}" for i, (cmn, eng) in enumerate(pairs)]
    prompt = (
        "Dịch các câu tiếng Trung (kèm bản tham khảo tiếng Anh) sau sang tiếng Việt tự nhiên, ngắn gọn, dùng xưng hô 'mình/bạn'. "
        "Giữ nguyên trường cmn gốc:\n" + "\n".join(lines)
    )
    out: TatoebaViBatch = _call_structured(api_key, prompt, TatoebaViBatch, timeout=45.0)
    return {it.cmn.strip(): it.vi.strip() for it in out.items if it.vi.strip()}


def generate_radical_notes_batch(chars: list[dict]) -> dict[str, str]:
    """Generate concise Vietnamese mnemonic notes for writing characters."""
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key or not chars:
        return {}
    lines = [
        f"{c['char']} (bộ {c['radical']}, nghĩa '{c['meaningVi']}', gợi ý EN: {c.get('definition', '')[:80]})"
        for c in chars
    ]
    prompt = (
        "Viết ghi chú mẹo nhớ bộ thủ ngắn gọn bằng tiếng Việt (1 câu ≤28 từ) giúp người trẻ nhớ cách viết từng chữ Hán dưới đây. "
        "KHÔNG nhắc tới 'HSK':\n" + "\n".join(lines)
    )
    out: RadicalNoteBatch = _call_structured(api_key, prompt, RadicalNoteBatch, timeout=45.0)
    return {it.char.strip(): it.noteVi.strip() for it in out.items if it.noteVi.strip()}


def _vocab_sample_str(allowed_vocab: set[str], new_words: list[str]) -> str:
    ordered = sorted(allowed_vocab)
    neg_guard = (
        "\nTUYỆT ĐỐI KHÔNG dùng các từ cấp cao hơn như: 常常, 一起, 快乐, 以后, 以前, 可是, 每, 从, 老板, 完, 放学, 幸福, 可爱, 比较, 另外, 因为, 所以, 但是, 虽然, 大姐, 许多."
        if len(ordered) < 800
        else ""
    )
    return (
        f"Từ mới trọng tâm BẮT BUỘC dùng: {', '.join(new_words)}\n"
        f"Tên riêng nhân vật ĐƯỢC PHÉP dùng duy nhất: Bao, 小明, 小美, 王老师 (KHÔNG tự bịa tên hay họ khác như 阮, 丽, 安)."
        f"{neg_guard}\n"
        f"Vốn từ đã biết cho phép (CHỈ được dùng các từ dưới đây + từ mới trên): {'、'.join(ordered)}"
    )


def generate_topic_comm(
    topic_id: int,
    topic_title: str,
    allowed_vocab: set[str],
    new_words: list[dict],
    dictionary: set[str],
    stats: dict,
    max_attempts: int = 8,
) -> TopicCommOut:
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY missing")

    new_hz = [w["hanzi"] for w in new_words]
    glossed = set(new_hz)
    vocab_desc = _vocab_sample_str(allowed_vocab, new_hz)
    new_desc = "; ".join(f"{w['hanzi']} ({w['meaningVi']})" for w in new_words)
    feedback = ""

    for attempt in range(1, max_attempts + 1):
        stats["attempted"] += 1
        prompt = (
            f"Soạn phần GIAO TIẾP cho Chủ đề {topic_id}: '{topic_title}' (app BaoBao dạy tiếng Trung cho người trẻ Việt).\n"
            f"Từ mới bài này: {new_desc}\n{vocab_desc}\n"
            "Yêu cầu schema:\n"
            "- patterns: đúng 2 mẫu câu khung (frame có '___', ví dụ câu hoàn chỉnh, câu hỏi điền chỗ trống 3 lựa chọn; answerHanzi PHẢI nằm y nguyên trong choices).\n"
            "- dialogue: đúng 6 lượt xen kẽ NPC (mode='npc', speaker='Linh' hoặc 'Nhân viên' hoặc tên Việt/Trung đơn giản) và nhân vật 'Bao' (voiceRole='male'). "
            "3 lượt của Bao phải tăng dần: lượt Bao 1 mode='choice' (3 choices, 1 correct=true), lượt Bao 2 mode='tiles' (tilePrompt là mảng từ ghép thành hanzi, nối lại đúng bằng hanzi), lượt Bao 3 mode='pinyin'. "
            "Các lượt có goalLabel tiếng Việt ngắn gọn (2-4 chữ).\n"
            "- meaningQuestion: 1 câu trắc nghiệm nghĩa (4 options tiếng Việt, answer PHẢI nằm y nguyên trong options).\n"
            "- hanziAudioText & hanziAudioOptions (4 phương án chữ Hán, hanziAudioText PHẢI nằm y nguyên trong hanziAudioOptions).\n"
            "- tilePromptVi & tileWords (mảng 3-5 mảnh từ ghép đúng thứ tự tạo thành 1 câu hoàn chỉnh).\n"
            "- roleplay: đúng 3 lượt đóng vai mini (3 choices mỗi lượt, expectedHanzi là đáp án đúng).\n"
            "LUẬT CỨNG: MỌI câu tiếng Trung chỉ được dùng từ trong vốn từ cho phép + từ mới trọng tâm. TUYỆT ĐỐI không dùng từ lạ."
            + feedback
        )
        cand: TopicCommOut = _call_structured(api_key, prompt, TopicCommOut)
        cand.meaningQuestion.answer = cand.meaningQuestion.answer.strip()
        cand.meaningQuestion.options = [o.strip() for o in cand.meaningQuestion.options]
        cand.hanziAudioText = cand.hanziAudioText.strip()
        cand.hanziAudioOptions = [o.strip() for o in cand.hanziAudioOptions]

        texts = (
            [p.exampleHanzi for p in cand.patterns]
            + [t.hanzi for t in cand.dialogue]
            + ["".join(cand.tileWords)]
            + [rp.npcHanzi + rp.expectedHanzi for rp in cand.roleplay]
        )
        res = check_level(
            text="".join(texts),
            allowed_vocab=allowed_vocab,
            glossed_new=glossed,
            dictionary=dictionary,
            max_unknown_ratio=0.14,
            min_new_occurrences=1,
        )
        struct_errors: list[str] = []
        if len(cand.patterns) < 2:
            struct_errors.append("cần đúng 2 patterns")
        if len(cand.dialogue) < 6:
            struct_errors.append("cần đúng 6 lượt dialogue")
        if len(cand.roleplay) < 3:
            struct_errors.append("cần đúng 3 lượt roleplay")
        if len(cand.tileWords) < 2:
            struct_errors.append("cần ít nhất 2 tileWords")
        if cand.meaningQuestion.answer not in cand.meaningQuestion.options:
            struct_errors.append("meaningQuestion.answer phải nằm y nguyên trong meaningQuestion.options")
        if cand.hanziAudioText not in cand.hanziAudioOptions:
            struct_errors.append("hanziAudioText phải nằm y nguyên trong hanziAudioOptions")
        for pi, p in enumerate(cand.patterns[:2]):
            if p.answerHanzi.strip() not in [c.hanzi.strip() for c in p.choices]:
                struct_errors.append(f"pattern[{pi}].answerHanzi phải nằm trong choices")

        if res.passed and not struct_errors:
            stats["accepted"] += 1
            return cand

        stats["rejected"] += 1
        print(f"  [REJECT] t{topic_id}-comm attempt {attempt}: unannotated={res.unannotated_unknowns[:8]} ratio={res.unknown_ratio} struct={struct_errors}", flush=True)
        stats["rejectionReasons"].append(
            {
                "unit": f"t{topic_id}-giao-tiep",
                "attempt": attempt,
                "unannotated": res.unannotated_unknowns[:12],
                "ratio": res.unknown_ratio,
                "struct": struct_errors,
            }
        )
        use_draft = attempt % 2 == 0
        draft_note = f"\nBẢN NHÁP LẦN TRƯỚC ĐỂ SỬA (giữ phần đạt, CHỈ thay từ ngoài vốn và sửa lỗi cấu trúc): {cand.model_dump_json()[:2400]}" if use_draft else "\nHãy viết lại MỚI HOÀN TOÀN tránh các từ ngoài vốn bên trên!"
        feedback = (
            f"\nLẦN TRƯỚC BỊ LOẠI: từ ngoài vốn={res.unannotated_unknowns[:15]}; tỷ lệ mới={res.unknown_ratio}; lỗi cấu trúc={struct_errors}."
            + draft_note
        )
    raise RuntimeError(f"Level check rejected {topic_id} comm after {max_attempts} attempts: {res}")


def generate_topic_reading(
    topic_id: int,
    topic_title: str,
    mode: Literal["fluent", "study"],
    target_min_chars: int,
    target_max_chars: int,
    allowed_vocab: set[str],
    new_words: list[dict],
    dictionary: set[str],
    stats: dict,
    max_attempts: int = 10,
) -> tuple[TopicReadingOut, int]:
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY missing")

    new_hz = [w["hanzi"] for w in new_words]
    glossed = set(new_hz)
    base_allowed = allowed_vocab - glossed
    vocab_desc = _vocab_sample_str(base_allowed, new_hz)
    max_ratio = 0.14 if mode == "fluent" else 0.18
    if target_min_chars <= 130:
        para_guide = "đúng 4 đoạn, MỖI đoạn viết 2–3 câu đầy đủ (~30–40 chữ Hán/đoạn)"
    elif target_min_chars <= 180:
        para_guide = "đúng 4 đoạn, MỖI đoạn viết 3 câu đầy đủ (~40–55 chữ Hán/đoạn)"
    elif target_min_chars <= 230:
        para_guide = "đúng 5 đoạn, MỖI đoạn viết 3 câu đầy đủ (~45–60 chữ Hán/đoạn)"
    else:
        para_guide = "đúng 5 đoạn, MỖI đoạn viết 3–4 câu đầy đủ (~55–72 chữ Hán/đoạn)"
    feedback = ""

    last_res = None
    for attempt in range(1, max_attempts + 1):
        stats["attempted"] += 1
        prompt = (
            f"Viết 1 BÀI ĐỌC HIỂU tiếng Trung cho Chủ đề {topic_id}: '{topic_title}'.\n"
            f"Chế độ: {'Đọc trôi (≥95% từ đã biết)' if mode == 'fluent' else 'Đọc học (~90% từ đã biết)'}.\n"
            f"Độ dài BẮT BUỘC: tổng cộng {target_min_chars}–{target_max_chars} chữ Hán, chia làm {para_guide} (mỗi đoạn có dịch nghĩa Việt đầy đủ).\n"
            f"MỖI từ mới trong nhóm sau PHẢI xuất hiện 2–3 LẦN (đủ 2 lần, không quá 3 lần): {', '.join(new_hz)}.\n"
            f"{vocab_desc}\n"
            "Kèm 3 câu hỏi đọc hiểu tiếng Việt (mix type: mcq, tf, detail; mỗi câu 2-3 lựa chọn, answer là index 0-based, kèm explainVi trích dẫn câu Hán trong bài).\n"
            "LUẬT CỨNG: KHÔNG dùng bất kỳ chữ Hán nào ngoài vốn từ đã biết và danh sách từ mới bắt buộc trên."
            + feedback
        )
        cand: TopicReadingOut = _call_structured(api_key, prompt, TopicReadingOut)
        joined = "".join(p.hanzi for p in cand.paragraphs)
        hz_len = count_hanzi_chars(joined)
        res = check_level(
            text=joined,
            allowed_vocab=base_allowed,
            glossed_new=glossed,
            dictionary=dictionary,
            max_unknown_ratio=max_ratio,
            min_new_occurrences=2,
        )
        last_res = res
        min_ok_len = 78 if target_min_chars <= 100 else max(110, target_min_chars - 35)
        if res.passed and hz_len >= min_ok_len:
            stats["accepted"] += 1
            known_pct = max(85, min(99, round((1.0 - res.unknown_ratio) * 100)))
            return cand, known_pct

        stats["rejected"] += 1
        print(f"  [REJECT] r-t{topic_id} attempt {attempt}: len={hz_len}, unannotated={res.unannotated_unknowns[:8]}, under={res.under_repeated_new}, ratio={res.unknown_ratio}", flush=True)
        stats["rejectionReasons"].append(
            {
                "unit": f"r-t{topic_id}",
                "attempt": attempt,
                "hzLen": hz_len,
                "unannotated": res.unannotated_unknowns[:12],
                "underRepeated": res.under_repeated_new,
                "ratio": res.unknown_ratio,
            }
        )
        use_draft = ((attempt % 2 == 0) or not res.unannotated_unknowns) and hz_len >= min_ok_len
        draft_note = (
            f"\nBẢN NHÁP ĐỂ SỬA (giữ câu tốt, CHỈ thay đúng các từ ngoài vốn bên trên bằng từ trong vốn cho phép và lặp thêm từ thiếu): {cand.model_dump_json()[:2600]}"
            if use_draft
            else f"\nLẦN NÀY HÃY VIẾT BÀI MỚI DÀI HƠN (ít nhất {target_min_chars + 15} chữ Hán, mỗi đoạn thêm 1–2 câu dùng nhiều từ quen đã biết để giảm tỷ lệ từ mới xuống <= {max_ratio} và BỎ HẾT các từ bị loại trên)!"
        )
        feedback = (
            f"\nLẦN TRƯỚC BỊ LOẠI (độ dài={hz_len} chữ, cần >= {target_min_chars}; "
            f"từ ngoài vốn={res.unannotated_unknowns[:12]}; từ mới chưa lặp đủ 2 lần={res.under_repeated_new}; tỷ lệ mới={res.unknown_ratio} <= {max_ratio})."
            + draft_note
        )

    raise RuntimeError(f"Level check rejected r-t{topic_id} after {max_attempts} attempts: {last_res}")


def generate_topic_listening(
    topic_id: int,
    topic_title: str,
    allowed_vocab: set[str],
    new_words: list[dict],
    dictionary: set[str],
    stats: dict,
    max_attempts: int = 8,
) -> TopicListeningOut:
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY missing")

    new_hz = [w["hanzi"] for w in new_words]
    glossed = set(new_hz)
    vocab_desc = _vocab_sample_str(allowed_vocab, new_hz)
    feedback = ""
    last_res = None

    for attempt in range(1, max_attempts + 1):
        stats["attempted"] += 1
        prompt = (
            f"Soạn bài LUYỆN NGHE cho Chủ đề {topic_id}: '{topic_title}'.\n"
            f"{vocab_desc}\n"
            "Yêu cầu schema:\n"
            "- listeningTracks: đúng 4 câu thoại mẫu ngắn giữa 2 người (speaker, voiceRole='female'|'male'|'formal', hanzi, vi).\n"
            "- listenMeaning: nghe audioText (1 câu ngắn ≤12 chữ) chọn nghĩa Việt (4 options, answer PHẢI nằm y nguyên trong options).\n"
            "- listenHanzi: nghe audioText (cụm 2-4 chữ) chọn đúng chữ Hán (4 options chữ Hán, answer PHẢI nằm y nguyên trong options).\n"
            "- listenTiles: audioText là 1 câu ngắn 4-6 chữ (không dấu câu trong tiles), tiles là mảng 3-4 cụm từ ghép lại đúng bằng audioText.\n"
            "- listenBlank: promptVi chứa câu khuyết '___', audioText là câu đầy đủ, 4 options từ điền, answer PHẢI nằm y nguyên trong options.\n"
            "- listenDialogue: nghe audioText (1 câu hội thoại) chọn ý hiểu đúng (3 options tiếng Việt, answer nằm trong options).\n"
            "- dictationText (câu ngắn 4-8 chữ Hán), dictationTiles (2-3 cụm từ tạo thành dictationText).\n"
            "LUẬT CỨNG: Chỉ dùng từ trong vốn cho phép và từ mới trọng tâm. Không dùng từ lạ."
            + feedback
        )
        cand: TopicListeningOut = _call_structured(api_key, prompt, TopicListeningOut)
        for q in (cand.listenMeaning, cand.listenHanzi, cand.listenBlank, cand.listenDialogue):
            q.answer = q.answer.strip()
            q.options = [o.strip() for o in q.options]

        texts = (
            [t.hanzi for t in cand.listeningTracks]
            + [
                cand.listenMeaning.audioText,
                cand.listenHanzi.audioText,
                cand.listenTiles.audioText,
                cand.listenBlank.audioText,
                cand.listenDialogue.audioText,
                cand.dictationText,
            ]
        )
        res = check_level(
            text="".join(texts),
            allowed_vocab=allowed_vocab,
            glossed_new=glossed,
            dictionary=dictionary,
            max_unknown_ratio=0.14,
            min_new_occurrences=1,
        )
        last_res = res
        struct_errors: list[str] = []
        if len(cand.listeningTracks) < 4:
            struct_errors.append("listeningTracks < 4")
        if len(cand.listenTiles.tiles) < 2:
            struct_errors.append("listenTiles.tiles < 2")
        for label, q in (("listenMeaning", cand.listenMeaning), ("listenHanzi", cand.listenHanzi), ("listenBlank", cand.listenBlank), ("listenDialogue", cand.listenDialogue)):
            if q.answer not in q.options:
                struct_errors.append(f"{label}.answer not in options")

        if res.passed and not struct_errors:
            stats["accepted"] += 1
            return cand

        stats["rejected"] += 1
        print(f"  [REJECT] t{topic_id}-nghe attempt {attempt}: unannotated={res.unannotated_unknowns[:8]} struct={struct_errors} ratio={res.unknown_ratio}", flush=True)
        stats["rejectionReasons"].append(
            {
                "unit": f"t{topic_id}-nghe",
                "attempt": attempt,
                "unannotated": res.unannotated_unknowns[:12],
                "struct": struct_errors,
                "ratio": res.unknown_ratio,
            }
        )
        use_draft = attempt % 2 == 0
        draft_note = f"\nBẢN NHÁP ĐỂ SỬA (giữ phần đạt, CHỈ thay từ ngoài vốn và đặt answer trong options): {cand.model_dump_json()[:2400]}" if use_draft else "\nHãy viết lại MỚI HOÀN TOÀN tránh các từ ngoài vốn trên!"
        feedback = (
            f"\nLẦN TRƯỚC BỊ LOẠI: từ ngoài vốn={res.unannotated_unknowns[:15]}; lỗi cấu trúc={struct_errors}."
            + draft_note
        )

    raise RuntimeError(f"Level check rejected t{topic_id}-nghe after {max_attempts} attempts: {last_res}")


def generate_story_chapter(
    chapter_num: int,
    title: str,
    teaser_vi: str,
    min_chars: int,
    max_chars: int,
    allowed_vocab: set[str],
    glossed_new: set[str],
    dictionary: set[str],
    stats: dict,
    max_attempts: int = 10,
) -> tuple[StoryChapterOut, int]:
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY missing")

    base_allowed = allowed_vocab - glossed_new
    vocab_desc = _vocab_sample_str(base_allowed, sorted(glossed_new))
    per_para = max(35, min_chars // 4)
    stage2_hint = (
        "\nGợi ý diễn đạt bằng từ cấp độ hiện tại: dùng 新房间, 新朋友, 上网买东西, 快递, 下雨, 风, 空调, 门, 就/也/还; "
        "TUYỆT ĐỐI tránh 又, 把, 好像, 一切, 极了, 吹, 搬, 邻居, 隔壁, 窗, 窗户, 生活, 感觉, 特别, 聊天, 屋子, 停, 干净, 树, 树叶 (thay 一会儿又... thành 一会儿就...)."
        if chapter_num == 2
        else ""
    )
    feedback = ""
    last_res = None
    best_cand: StoryChapterOut | None = None
    best_res = None
    best_err_count = 999

    for attempt in range(1, max_attempts + 1):
        stats["attempted"] += 1
        prompt = (
            f"Viết Chương {chapter_num}/4 của truyện dài kỳ xuyên suốt: '{title}'.\n"
            f"Cốt truyện gợi ý: {teaser_vi}\n"
            f"Nhân vật chính là gấu trúc Bao cùng bạn học. Độ dài BẮT BUỘC: {min_chars}–{max_chars} chữ Hán, chia làm 4–5 đoạn văn, MỖI đoạn viết 3–4 câu (~{per_para}–{per_para+20} chữ Hán/đoạn), kèm dịch Việt từng đoạn.\n"
            f"MỖI từ trong nhóm điểm nhấn sau phải xuất hiện 2–3 lần: {', '.join(sorted(glossed_new))}.\n"
            f"{vocab_desc}{stage2_hint}\n"
            "Thêm 4 câu hỏi đọc hiểu (mix mcq, tf, detail; answer là index 0-based; kèm explainVi) và 1 câu cliffhangerVi hấp dẫn gợi mở sang chương sau (riêng Chương 4 là lời kết ấm áp).\n"
            "LUẬT CỨNG: KHÔNG dùng chữ Hán ngoài danh sách từ vựng cho phép."
            + feedback
        )
        cand: StoryChapterOut = _call_structured(api_key, prompt, StoryChapterOut)
        joined = "".join(p.hanzi for p in cand.paragraphs)
        hz_len = count_hanzi_chars(joined)
        res = check_level(
            text=joined,
            allowed_vocab=base_allowed,
            glossed_new=glossed_new,
            dictionary=dictionary,
            max_unknown_ratio=0.14,
            min_new_occurrences=2,
        )
        last_res = res
        min_ok_len = max(95, min_chars - 30)
        if res.passed and hz_len >= min_ok_len and len(cand.questions) >= 3:
            stats["accepted"] += 1
            known_pct = max(86, min(98, round((1.0 - res.unknown_ratio) * 100)))
            return cand, known_pct

        if hz_len >= min_ok_len:
            err_count = len(res.unannotated_unknowns) + len(res.under_repeated_new)
            if err_count < best_err_count:
                best_cand = cand
                best_res = res
                best_err_count = err_count

        stats["rejected"] += 1
        print(f"  [REJECT] story-c{chapter_num} attempt {attempt}: len={hz_len}, unannotated={res.unannotated_unknowns[:8]}, under={res.under_repeated_new}", flush=True)
        stats["rejectionReasons"].append(
            {
                "unit": f"story-c{chapter_num}",
                "attempt": attempt,
                "hzLen": hz_len,
                "unannotated": res.unannotated_unknowns[:12],
                "underRepeated": res.under_repeated_new,
            }
        )
        if best_cand is not None and best_res is not None and best_err_count <= 4:
            feedback = (
                f"\nSỬA BẢN NHÁP TỐT NHẤT (giữ nguyên mọi câu khác, CHỈ thay đúng các từ ngoài vốn={best_res.unannotated_unknowns} "
                f"bằng từ trong vốn cho phép và bổ sung từ thiếu lặp={best_res.under_repeated_new}): "
                + best_cand.model_dump_json()
            )
        else:
            use_draft = ((attempt % 2 == 0) or not res.unannotated_unknowns) and hz_len >= min_ok_len
            draft_note = f"\nBẢN NHÁP ĐỂ SỬA (thay đúng các từ lạ và lặp từ thiếu): {cand.model_dump_json()[:2800]}" if use_draft else f"\nHãy viết MỚI hoàn toàn dài hơn ({min_chars + 15}–{max_chars} chữ Hán) và BỎ HẾT từ lạ trên!"
            feedback = (
                f"\nLẦN TRƯỚC BỊ LOẠI (độ dài={hz_len}, cần {min_chars}–{max_chars}; từ lạ={res.unannotated_unknowns[:12]}, thiếu lặp={res.under_repeated_new})."
                + draft_note
            )

    raise RuntimeError(f"Level check rejected story-c{chapter_num} after {max_attempts} attempts: {last_res}")


def generate_stage_test_items(
    stage_id: int,
    stage_title: str,
    allowed_vocab: set[str],
    dictionary: set[str],
    stats: dict,
    max_attempts: int = 8,
) -> StageTestOut:
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY missing")

    vocab_desc = _vocab_sample_str(allowed_vocab, [])
    feedback = ""
    last_res = None

    for attempt in range(1, max_attempts + 1):
        stats["attempted"] += 1
        prompt = (
            f"Soạn 6 câu hỏi kiểm tra tổng hợp cuối {stage_title} (đúng 2 câu skill='giao-tiep', 2 câu skill='doc', 2 câu skill='nghe').\n"
            f"{vocab_desc}\n"
            "Mỗi item gồm:\n"
            "- skill: 'giao-tiep' (tình huống giao tiếp thực tế, có passageHanzi là lời đối thoại + passageVi + 3-4 options + answer + explainVi),\n"
            "  hoặc 'doc' (passageHanzi dài 35-65 chữ + passageVi + câu hỏi đọc hiểu + 3 options + answer + explainVi),\n"
            "  hoặc 'nghe' (audioText 1 câu rõ ràng + 3-4 options tiếng Việt/chữ Hán + answer + explainVi).\n"
            "LUẬT CỨNG: MỌI câu chữ Hán chỉ dùng từ trong danh sách cho phép, KHÔNG nhắc chữ 'HSK'."
            + feedback
        )
        cand: StageTestOut = _call_structured(api_key, prompt, StageTestOut)
        for it in cand.items:
            it.answer = it.answer.strip()
            it.options = [o.strip() for o in it.options]
        texts = [
            it.passageHanzi + it.audioText + "".join(o for o in it.options if any("\u4e00" <= c <= "\u9fff" for c in o))
            for it in cand.items
        ]
        res = check_level(
            text="".join(texts),
            allowed_vocab=allowed_vocab,
            glossed_new=set(),
            dictionary=dictionary,
            max_unknown_ratio=0.10,
            min_new_occurrences=1,
        )
        last_res = res
        skills = [it.skill for it in cand.items]
        answers_ok = all(it.answer in it.options and len(it.options) >= 2 for it in cand.items)
        if res.passed and answers_ok and skills.count("giao-tiep") >= 2 and skills.count("doc") >= 2 and skills.count("nghe") >= 2:
            stats["accepted"] += 1
            return cand

        stats["rejected"] += 1
        print(f"  [REJECT] stage-{stage_id}-test attempt {attempt}: unannotated={res.unannotated_unknowns[:8]} answers_ok={answers_ok}", flush=True)
        stats["rejectionReasons"].append(
            {
                "unit": f"stage-{stage_id}-test",
                "attempt": attempt,
                "unannotated": res.unannotated_unknowns[:12],
            }
        )
        use_draft = attempt % 2 == 0
        draft_note = f"\nBẢN NHÁP ĐỂ SỬA (CHỈ thay các từ ngoài vốn và đảm bảo answer nằm trong options): {cand.model_dump_json()[:2400]}" if use_draft else "\nHãy viết lại MỚI hoàn toàn, tránh các từ ngoài vốn trên!"
        feedback = (
            f"\nLẦN TRƯỚC BỊ LOẠI: từ ngoài vốn={res.unannotated_unknowns[:12]}; answers_ok={answers_ok}."
            + draft_note
        )

    raise RuntimeError(f"Level check rejected stage-{stage_id}-test after {max_attempts} attempts: {last_res}")
