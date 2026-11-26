"""Generate level-controlled Chinese dialogues and readings via Gemini API (google-genai)."""

from __future__ import annotations

import json
import os
from pathlib import Path
import sys
from typing import List
from pydantic import BaseModel, Field

from level_checker import check_level

ROOT = Path(__file__).resolve().parent.parent


class DialogueTurnOut(BaseModel):
    speaker: str = Field(description="Speaker name or role.")
    hanzi: str = Field(description="Natural simplified Chinese sentence.")
    pinyin: str = Field(description="Tone-marked pinyin.")
    vi: str = Field(description="Natural Vietnamese translation.")


class GeneratedDialogue(BaseModel):
    turns: List[DialogueTurnOut]


def generate_controlled_dialogue(
    topic_title: str,
    allowed_vocab: set[str],
    new_words: set[str],
    dictionary: set[str],
    max_attempts: int = 3,
) -> tuple[GeneratedDialogue | None, dict]:
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        print("GEMINI_API_KEY is not set in environment. Skipping Gemini generation.", file=sys.stderr)
        return None, {"attempted": 0, "accepted": 0, "rejected": 0}

    from google import genai

    client = genai.Client(api_key=api_key)
    stats = {"attempted": 0, "accepted": 0, "rejected": 0}

    for attempt in range(1, max_attempts + 1):
        stats["attempted"] += 1
        prompt = (
            f"Hãy viết một hội thoại tiếng Trung tự nhiên 6–8 lượt cho chủ đề '{topic_title}'.\n"
            f"CHỈ ĐƯỢC DÙNG các từ trong vốn từ cho phép: {', '.join(sorted(allowed_vocab))}\n"
            f"Và tối đa 5–10% từ mới của bài: {', '.join(sorted(new_words))}.\n"
            "KHÔNG dùng thêm từ Hán nào ngoài hai danh sách trên."
        )
        interaction = client.interactions.create(
            model="gemini-4-hydrogen",
            input=prompt,
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": GeneratedDialogue.model_json_schema(),
            },
        )
        candidate = GeneratedDialogue.model_validate_json(interaction.output_text)
        joined = "".join(t.hanzi for t in candidate.turns)
        res = check_level(
            text=joined,
            allowed_vocab=allowed_vocab,
            glossed_new=new_words,
            dictionary=dictionary,
            max_unknown_ratio=0.12,
        )
        if res.passed:
            stats["accepted"] += 1
            return candidate, stats
        stats["rejected"] += 1
        print(f"Attempt {attempt} rejected: unannotated={res.unannotated_unknowns}, ratio={res.unknown_ratio}")

    return None, stats


if __name__ == "__main__":
    print("generate_content.py ready. Run via pipeline or import generate_controlled_dialogue().")
