"""Extract stroke JSON files and radical metadata only for characters used in content/."""

from __future__ import annotations

import json
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
DATA_DIR = ROOT / "data-src"
STROKES_DIR = ROOT / "public" / "strokes"
HW_DATA_DIR = ROOT / "node_modules" / "hanzi-writer-data"
CJK_CHAR_RE = re.compile(r"[\u4e00-\u9fff]")


def load_mmah_dictionary() -> dict[str, dict]:
    dict_path = DATA_DIR / "makemeahanzi_dictionary.txt"
    out: dict[str, dict] = {}
    if not dict_path.exists():
        return out
    with dict_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            ch = item.get("character")
            if ch:
                out[ch] = item
    return out


def collect_curriculum_chars() -> set[str]:
    chars: set[str] = set()
    for p in CONTENT_DIR.rglob("*.json"):
        if p.name == "radicals.json":
            continue
        text = p.read_text(encoding="utf-8")
        chars.update(CJK_CHAR_RE.findall(text))
    return chars


def main() -> None:
    STROKES_DIR.mkdir(parents=True, exist_ok=True)
    chars = sorted(collect_curriculum_chars())
    mmah = load_mmah_dictionary()

    copied = 0
    missing: list[str] = []
    radicals_map: dict[str, dict] = {}

    for ch in chars:
        src = HW_DATA_DIR / f"{ch}.json"
        dest = STROKES_DIR / f"{ch}.json"
        if src.exists():
            shutil.copyfile(src, dest)
            copied += 1
        else:
            missing.append(ch)

        info = mmah.get(ch)
        if info:
            rad = info.get("radical") or ""
            if rad:
                entry = radicals_map.setdefault(
                    rad,
                    {
                        "radical": rad,
                        "meaning": info.get("definition", "").split(";")[0].strip() if ch == rad else "",
                        "chars": [],
                    },
                )
                if len(entry["chars"]) < 12 and ch not in entry["chars"]:
                    entry["chars"].append(ch)
                if not entry["meaning"] and ch == rad and info.get("definition"):
                    entry["meaning"] = info["definition"].split(";")[0].strip()

    char_info = {
        ch: {
            "radical": mmah[ch].get("radical", ""),
            "decomposition": mmah[ch].get("decomposition", ""),
            "etymology": mmah[ch].get("etymology", {}),
            "definition": mmah[ch].get("definition", ""),
        }
        for ch in chars
        if ch in mmah
    }

    radicals_out = {
        "radicals": radicals_map,
        "characters": char_info,
    }
    (CONTENT_DIR / "radicals.json").write_text(
        json.dumps(radicals_out, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Strokes extracted: {copied}/{len(chars)} chars (missing={len(missing)})")
    if missing:
        print("Missing chars:", "".join(missing))


if __name__ == "__main__":
    main()
