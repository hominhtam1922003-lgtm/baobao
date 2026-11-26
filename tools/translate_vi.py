"""Batch translate vocabulary meanings to Vietnamese via Gemini API (google-genai)."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
from pathlib import Path
import random
import re
import sys
import threading
import time
from typing import List
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_POOL_PATH = ROOT / "tools" / ".cache" / "hsk_1_3_pool.json"
CACHE_PATH = ROOT / "tools" / ".cache" / "vi_cache.json"
SPOT_CHECK_PATH = ROOT / "tools" / ".cache" / "vi_spot_check_report.json"
STAGE1_WORDS_PATH = ROOT / "content" / "stage-1" / "words.json"

VI_DIACRITIC_RE = re.compile(
    r"[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]",
    re.IGNORECASE,
)


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
    tmp = CACHE_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(CACHE_PATH)


def seed_cache_from_stage1(cache: dict[str, str]) -> int:
    if not STAGE1_WORDS_PATH.exists():
        return 0
    stage1 = json.loads(STAGE1_WORDS_PATH.read_text(encoding="utf-8"))
    added = 0
    for w in stage1:
        hz = (w.get("hanzi") or "").strip()
        vi = (w.get("meaningVi") or "").strip()
        if hz and vi and hz not in cache:
            cache[hz] = vi
            added += 1
    return added


def _call_gemini_batch(api_key: str, chunk: list[dict]) -> list[WordTranslation]:
    from google import genai  # deferred import so offline runs stay clean

    client = genai.Client(api_key=api_key)
    lines = [
        f"{w['hanzi']} ({w['pinyin']}): {', '.join((w.get('meaningsEn') or w.get('cedictGloss') or [])[:4])}"
        for w in chunk
    ]
    prompt = (
        "Dịch các từ tiếng Trung sau sang nghĩa tiếng Việt ngắn gọn, tự nhiên cho người trẻ Việt Nam "
        "(mỗi từ 1–3 nghĩa thông dụng nhất, phân tách bằng dấu phẩy, không giải thích dài dòng, giữ nguyên hanzi gốc):\n"
        + "\n".join(lines)
    )
    models = ("gemini-3.5-flash-lite", "gemini-3.1-flash-lite")
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
                    "schema": TranslationBatch.model_json_schema(),
                },
                timeout=35.0,
            )
            parsed = TranslationBatch.model_validate_json(interaction.output_text)
            return parsed.items
        except Exception as exc:
            last_err = exc
            time.sleep(1.5 * (2**attempt))
    raise RuntimeError(f"Gemini batch translation failed after retries: {last_err}")


def is_suspicious_meaning(vi: str, meanings_en: list[str]) -> bool:
    s = vi.strip()
    if not s:
        return True
    if not VI_DIACRITIC_RE.search(s) and len(s.split()) >= 2:
        en_joined = " ".join(meanings_en).lower()
        if s.lower() in en_joined:
            return True
    return False


def translate_words(words: list[dict], batch_size: int = 50, workers: int = 3) -> dict[str, str]:
    cache = load_cache()
    seeded = seed_cache_from_stage1(cache)
    if seeded:
        save_cache(cache)

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        print("GEMINI_API_KEY is not set in environment. Skipping Gemini translation.", file=sys.stderr)
        return cache

    # Deduplicate by hanzi preserving order
    unique_words: list[dict] = []
    seen: set[str] = set()
    for w in words:
        hz = w["hanzi"]
        if hz not in seen:
            seen.add(hz)
            unique_words.append(w)

    pending = [
        w
        for w in unique_words
        if w["hanzi"] not in cache or is_suspicious_meaning(cache.get(w["hanzi"], ""), w.get("meaningsEn", []))
    ]
    print(f"Unique pool: {len(unique_words)} | Cached: {len(cache)} (seeded {seeded}) | Pending: {len(pending)}")
    if not pending:
        return cache

    chunks = [pending[i : i + batch_size] for i in range(0, len(pending), batch_size)]
    lock = threading.Lock()
    done_batches = 0

    with ThreadPoolExecutor(max_workers=max(1, workers)) as executor:
        futures = {executor.submit(_call_gemini_batch, api_key, ch): idx for idx, ch in enumerate(chunks)}
        for fut in as_completed(futures):
            idx = futures[fut]
            chunk = chunks[idx]
            items = fut.result()
            by_hz = {it.hanzi.strip(): it.meaningVi.strip() for it in items if it.meaningVi.strip()}
            with lock:
                for w in chunk:
                    hz = w["hanzi"]
                    if hz in by_hz:
                        cache[hz] = by_hz[hz]
                save_cache(cache)
                done_batches += 1
                print(f"Batch {done_batches}/{len(chunks)} saved (cache size: {len(cache)})")

    # Retry pass for any missed/blank items individually in a compact batch
    still_missing = [
        w
        for w in unique_words
        if not cache.get(w["hanzi"], "").strip()
        or is_suspicious_meaning(cache.get(w["hanzi"], ""), w.get("meaningsEn", []))
    ]
    if still_missing:
        print(f"Retrying {len(still_missing)} remaining/flagged words...")
        for i in range(0, len(still_missing), min(25, batch_size)):
            chunk = still_missing[i : i + min(25, batch_size)]
            items = _call_gemini_batch(api_key, chunk)
            for it in items:
                if it.meaningVi.strip():
                    cache[it.hanzi.strip()] = it.meaningVi.strip()
            save_cache(cache)

    return cache


def spot_check_sample(words: list[dict], cache: dict[str, str], rate: float = 0.05) -> list[dict]:
    """Return 5% random sample pairing Vietnamese translation with CC-CEDICT/English gloss for human audit."""
    seen: set[str] = set()
    translated: list[dict] = []
    for w in words:
        hz = w["hanzi"]
        if hz not in seen and cache.get(hz, "").strip():
            seen.add(hz)
            translated.append(w)
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Translate HSK 1-3 vocabulary pool to Vietnamese.")
    parser.add_argument("--pool", type=Path, default=DEFAULT_POOL_PATH)
    parser.add_argument("--batch-size", type=int, default=50)
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()

    if not args.pool.exists():
        print(f"Missing {args.pool}")
        sys.exit(1)

    words_data = json.loads(args.pool.read_text(encoding="utf-8"))
    cache = translate_words(words_data, batch_size=args.batch_size, workers=args.workers)

    # Programmatic completeness check across all pool entries
    missing_vi = [w["hanzi"] for w in words_data if not cache.get(w["hanzi"], "").strip()]
    flagged_vi = [
        {"hanzi": w["hanzi"], "meaningVi": cache.get(w["hanzi"], ""), "en": w.get("meaningsEn", [])[:2]}
        for w in words_data
        if cache.get(w["hanzi"], "").strip() and is_suspicious_meaning(cache[w["hanzi"]], w.get("meaningsEn", []))
    ]
    audit = spot_check_sample(words_data, cache, rate=0.05)
    SPOT_CHECK_PATH.parent.mkdir(parents=True, exist_ok=True)
    SPOT_CHECK_PATH.write_text(
        json.dumps(
            {
                "poolCount": len(words_data),
                "translatedCount": sum(1 for w in words_data if cache.get(w["hanzi"], "").strip()),
                "missingCount": len(missing_vi),
                "flaggedCount": len(flagged_vi),
                "flaggedItems": flagged_vi,
                "spotCheckCount": len(audit),
                "spotCheck": audit,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(
        f"Translation complete: {len(words_data) - len(missing_vi)}/{len(words_data)} covered | "
        f"missing={len(missing_vi)} | flagged={len(flagged_vi)} | spotCheck={len(audit)} -> {SPOT_CHECK_PATH}"
    )


if __name__ == "__main__":
    main()
