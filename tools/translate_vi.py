"""Batch translate vocabulary meanings to Vietnamese via Gemini API (google-genai)."""

from __future__ import annotations

import json
import os
from pathlib import Path
import random
import sys
from typing import List
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent.parent
CACHE_PATH = ROOT / "tools" / ".cache" / "vi_cache.json"


class WordTranslation(BaseModel):
    hanzi: str = Field(description="Original simplified Chinese word.")
    meaningVi: str = Field(description="Concise Vietnamese meaning (1-3 common senses).")


class TranslationBatch(BaseModel):
    items: List[WordTranslation]


def load_cache() -> dict[str, str]:
    if CACHE_PATH.exists():
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    return {}


def save_cache(cache: dict[str, str]) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def translate_words(words: list[dict], batch_size: int = 40) -> dict[str, str]:
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        print("GEMINI_API_KEY is not set in environment. Skipping Gemini translation.", file=sys.stderr)
        return load_cache()

    from google import genai  # deferred import so offline runs stay clean

    client = genai.Client(api_key=api_key)
    cache = load_cache()
    pending = [w for w in words if w["hanzi"] not in cache]
    print(f"Pending words for Gemini translation: {len(pending)} (cached: {len(cache)})")

    for i in range(0, len(pending), batch_size):
        chunk = pending[i : i + batch_size]
        lines = [
            f"{w['hanzi']} ({w['pinyin']}): {', '.join(w.get('meaningsEn', [])[:4])}"
            for w in chunk
        ]
        prompt = (
            "Dịch các từ tiếng Trung sau sang nghĩa tiếng Việt ngắn gọn, tự nhiên cho người trẻ Việt Nam "
            "(mỗi từ 1–3 nghĩa thông dụng nhất, phân tách bằng dấu phẩy, không giải thích dài dòng):\n"
            + "\n".join(lines)
        )
        interaction = client.interactions.create(
            model="gemini-4-hydrogen",
            input=prompt,
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": TranslationBatch.model_json_schema(),
            },
        )
        parsed = TranslationBatch.model_validate_json(interaction.output_text)
        for item in parsed.items:
            cache[item.hanzi] = item.meaningVi.strip()
        save_cache(cache)

    return cache


def spot_check_sample(words: list[dict], cache: dict[str, str], rate: float = 0.05) -> list[dict]:
    """Return 5% random sample pairing Vietnamese translation with CC-CEDICT/English gloss for human audit."""
    translated = [w for w in words if w["hanzi"] in cache]
    if not translated:
        return []
    k = max(1, round(len(translated) * rate))
    rng = random.Random(42)
    sample = rng.sample(translated, min(k, len(translated)))
    return [
        {
            "hanzi": w["hanzi"],
            "pinyin": w["pinyin"],
            "meaningVi": cache[w["hanzi"]],
            "cedictOrEn": w.get("cedictGloss") or w.get("meaningsEn", []),
        }
        for w in sample
    ]


if __name__ == "__main__":
    words_file = ROOT / "content" / "stage-1" / "words.json"
    if not words_file.exists():
        print(f"Missing {words_file}")
        sys.exit(1)
    words_data = json.loads(words_file.read_text(encoding="utf-8"))
    cache = translate_words(words_data)
    audit = spot_check_sample(words_data, cache)
    print(f"Spot-check sample ({len(audit)} items):", json.dumps(audit[:5], ensure_ascii=False, indent=2))
