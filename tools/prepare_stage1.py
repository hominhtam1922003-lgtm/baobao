"""Normalize HSK 1-3 + CC-CEDICT + Tatoeba + MakeMeAHanzi data and prepare Stage 1 pool."""

from __future__ import annotations

import json
from pathlib import Path
import re
from pypinyin import pinyin as to_pinyin, Style

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data-src"
CACHE_DIR = ROOT / "tools" / ".cache"

CEDICT_LINE_RE = re.compile(r"^(\S+)\s+(\S+)\s+\[([^\]]+)\]\s+/(.+)/$")

TONE_MAP = {
    "a": "āáǎàa",
    "e": "ēéěèe",
    "i": "īíǐìi",
    "o": "ōóǒòo",
    "u": "ūúǔùu",
    "ü": "ǖǘǚǜü",
}


def numeric_to_tone_syllable(syl: str) -> str:
    if not syl or not syl[-1].isdigit():
        return syl
    tone = int(syl[-1])
    core = syl[:-1].replace("u:", "ü").replace("v", "ü")
    if tone < 1 or tone > 5:
        return core
    idx_tone = tone - 1
    lower = core.lower()
    for vowel in ("a", "e"):
        pos = lower.find(vowel)
        if pos != -1:
            rep = TONE_MAP[vowel][idx_tone]
            return core[:pos] + (rep.upper() if core[pos].isupper() else rep) + core[pos + 1 :]
    if "ou" in lower:
        pos = lower.find("o")
        rep = TONE_MAP["o"][idx_tone]
        return core[:pos] + (rep.upper() if core[pos].isupper() else rep) + core[pos + 1 :]
    for i in range(len(lower) - 1, -1, -1):
        ch = lower[i]
        if ch in TONE_MAP:
            rep = TONE_MAP[ch][idx_tone]
            return core[:i] + (rep.upper() if core[i].isupper() else rep) + core[i + 1 :]
    return core


def cedict_pinyin_to_marks(num_pinyin: str) -> str:
    return " ".join(numeric_to_tone_syllable(s) for s in num_pinyin.split())


def load_cedict() -> dict[str, dict]:
    path = DATA_DIR / "cedict_ts.u8"
    out: dict[str, dict] = {}
    with path.open(encoding="utf-8") as f:
        for line in f:
            if not line or line.startswith("#"):
                continue
            m = CEDICT_LINE_RE.match(line.strip())
            if not m:
                continue
            _, simp, num_py, defs = m.groups()
            if simp not in out:
                out[simp] = {
                    "pinyin": cedict_pinyin_to_marks(num_py),
                    "meanings": [d.strip() for d in defs.split("/") if d.strip()],
                }
    return out


def load_mmah_radicals() -> dict[str, str]:
    path = DATA_DIR / "makemeahanzi_dictionary.txt"
    out: dict[str, str] = {}
    with path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            if obj.get("character") and obj.get("radical"):
                out[obj["character"]] = obj["radical"]
    return out


def extract_level(labels: list[str]) -> int | None:
    newest = [int(lv.split("-")[1]) for lv in labels if lv.startswith("newest-") and lv.split("-")[1].isdigit()]
    new = [int(lv.split("-")[1]) for lv in labels if lv.startswith("new-") and lv.split("-")[1].isdigit()]
    candidates = [lv for lv in (newest or new) if 1 <= lv <= 3]
    if not candidates:
        return None
    return min(candidates)


def main() -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    hsk_raw = json.loads((DATA_DIR / "complete.json").read_text(encoding="utf-8"))
    cedict = load_cedict()
    mmah_rad = load_mmah_radicals()
    tatoeba = json.loads((DATA_DIR / "tatoeba_cmn_pairs.json").read_text(encoding="utf-8"))

    # Index short Tatoeba sentences (<=20 chars) prioritizing cmn-vie
    sentences = tatoeba["sentences"]
    short_sentences = [s for s in sentences if len(s["cmn"]) <= 20]
    short_sentences.sort(key=lambda s: (0 if s["vie"] else 1, len(s["cmn"])))

    pool: list[dict] = []
    for item in hsk_raw:
        lvl = extract_level(item.get("level", []))
        if lvl is None:
            continue
        simp = item["simplified"]
        form0 = (item.get("forms") or [{}])[0]
        py = (form0.get("transcriptions") or {}).get("pinyin") or ""
        if not py and simp in cedict:
            py = cedict[simp]["pinyin"]
        if not py:
            py = " ".join(x[0] for x in to_pinyin(simp, style=Style.TONE))
        meanings = form0.get("meanings") or (cedict[simp]["meanings"] if simp in cedict else [])
        rad = item.get("radical") or mmah_rad.get(simp[0], "")
        pool.append(
            {
                "hanzi": simp,
                "pinyin": py,
                "meaningsEn": meanings,
                "cedictGloss": cedict.get(simp, {}).get("meanings", [])[:3],
                "radical": rad,
                "level": lvl,
                "frequency": item.get("frequency", 999999),
            }
        )

    pool.sort(key=lambda x: (x["level"], x["frequency"]))
    (CACHE_DIR / "hsk_1_3_pool.json").write_text(
        json.dumps(pool, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # Index short sentences for quick lookup by word substring
    by_char_bucket: dict[str, list[dict]] = {}
    for s in short_sentences:
        seen_chars = set(s["cmn"])
        for ch in seen_chars:
            bucket = by_char_bucket.setdefault(ch, [])
            if len(bucket) < 120:
                bucket.append(s)

    matched_vie = 0
    matched_eng = 0
    for entry in pool[:300]:
        w = entry["hanzi"]
        cands = by_char_bucket.get(w[0], [])
        hits = [s for s in cands if w in s["cmn"]][:2]
        entry["tatoeba"] = hits
        if any(s["vie"] for s in hits):
            matched_vie += 1
        elif hits:
            matched_eng += 1

    (CACHE_DIR / "stage1_candidates.json").write_text(
        json.dumps(pool[:300], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(
        f"HSK 1-3 pool: {len(pool)} words | top-300 Stage 1 candidates: {matched_vie} with cmn-vie, {matched_eng} with cmn-eng Tatoeba"
    )


if __name__ == "__main__":
    main()
