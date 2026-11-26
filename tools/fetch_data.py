"""Fetch the 4 open datasets into data-src/ and report verified counts."""

from __future__ import annotations

import bz2
import gzip
import io
import json
import tarfile
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data-src"

SOURCES = {
    "hsk": "https://raw.githubusercontent.com/drkameleon/complete-hsk-vocabulary/main/complete.json",
    "cedict": "https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.txt.gz",
    "tatoeba_cmn": "https://downloads.tatoeba.org/exports/per_language/cmn/cmn_sentences.tsv.bz2",
    "tatoeba_vie": "https://downloads.tatoeba.org/exports/per_language/vie/vie_sentences.tsv.bz2",
    "tatoeba_eng": "https://downloads.tatoeba.org/exports/per_language/eng/eng_sentences.tsv.bz2",
    "tatoeba_links": "https://downloads.tatoeba.org/exports/links.tar.bz2",
    "mmah_dict": "https://raw.githubusercontent.com/skishore/makemeahanzi/master/dictionary.txt",
    "mmah_graphics": "https://raw.githubusercontent.com/skishore/makemeahanzi/master/graphics.txt",
}


def download(url: str, dest: Path, timeout: int = 120) -> Path:
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=timeout, headers={"User-Agent": "BaoBaoDataFetcher/1.0"}) as r:
        r.raise_for_status()
        tmp = dest.with_suffix(dest.suffix + ".part")
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 256):
                if chunk:
                    f.write(chunk)
        tmp.replace(dest)
    return dest


def parse_tsv_bz2(path: Path) -> dict[int, str]:
    out: dict[int, str] = {}
    with bz2.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 3:
                try:
                    sid = int(parts[0])
                except ValueError:
                    continue
                out[sid] = parts[2]
    return out


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # 1. HSK
    hsk_path = download(SOURCES["hsk"], DATA_DIR / "complete.json")
    hsk_data = json.loads(hsk_path.read_text(encoding="utf-8"))
    print(f"HSK entries: {len(hsk_data)}")

    # 2. CC-CEDICT
    cedict_gz = download(SOURCES["cedict"], DATA_DIR / "cedict_1_0_ts_utf-8_mdbg.txt.gz")
    cedict_u8 = DATA_DIR / "cedict_ts.u8"
    if not cedict_u8.exists():
        with gzip.open(cedict_gz, "rb") as gz, open(cedict_u8, "wb") as out:
            out.write(gz.read())
    cedict_count = sum(1 for line in cedict_u8.open(encoding="utf-8") if line and not line.startswith("#"))
    print(f"CC-CEDICT entries: {cedict_count}")

    # 3. Make Me A Hanzi
    dict_path = download(SOURCES["mmah_dict"], DATA_DIR / "makemeahanzi_dictionary.txt")
    gfx_path = download(SOURCES["mmah_graphics"], DATA_DIR / "makemeahanzi_graphics.txt")
    dict_count = sum(1 for line in dict_path.open(encoding="utf-8") if line.strip())
    gfx_count = sum(1 for line in gfx_path.open(encoding="utf-8") if line.strip())
    print(f"MakeMeAHanzi dictionary: {dict_count}, graphics: {gfx_count}")

    # 4. Tatoeba sentences + links
    cmn_bz2 = download(SOURCES["tatoeba_cmn"], DATA_DIR / "cmn_sentences.tsv.bz2")
    vie_bz2 = download(SOURCES["tatoeba_vie"], DATA_DIR / "vie_sentences.tsv.bz2")
    eng_bz2 = download(SOURCES["tatoeba_eng"], DATA_DIR / "eng_sentences.tsv.bz2")
    links_tar = download(SOURCES["tatoeba_links"], DATA_DIR / "links.tar.bz2", timeout=300)

    cmn = parse_tsv_bz2(cmn_bz2)
    vie = parse_tsv_bz2(vie_bz2)
    eng = parse_tsv_bz2(eng_bz2)
    print(f"Tatoeba sentences cmn={len(cmn)}, vie={len(vie)}, eng={len(eng)}")

    pairs_path = DATA_DIR / "tatoeba_cmn_pairs.json"
    cmn_vie: dict[int, list[str]] = {}
    cmn_eng: dict[int, list[str]] = {}
    with tarfile.open(links_tar, "r:bz2") as tf:
        member = next(m for m in tf.getmembers() if m.isfile())
        raw = tf.extractfile(member)
        assert raw is not None
        for line in io.TextIOWrapper(raw, encoding="utf-8"):
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 2:
                continue
            try:
                a, b = int(parts[0]), int(parts[1])
            except ValueError:
                continue
            if a in cmn:
                if b in vie:
                    cmn_vie.setdefault(a, []).append(vie[b])
                elif b in eng and len(cmn_eng.get(a, ())) < 2:
                    cmn_eng.setdefault(a, []).append(eng[b])

    compact = {
        "cmn_count": len(cmn),
        "vie_count": len(vie),
        "eng_count": len(eng),
        "cmn_vie_links": len(cmn_vie),
        "cmn_eng_links": len(cmn_eng),
        "sentences": [
            {
                "id": sid,
                "cmn": text,
                "vie": cmn_vie.get(sid, []),
                "eng": cmn_eng.get(sid, []),
            }
            for sid, text in cmn.items()
            if sid in cmn_vie or sid in cmn_eng
        ],
    }
    pairs_path.write_text(json.dumps(compact, ensure_ascii=False), encoding="utf-8")
    print(
        f"Tatoeba pairs saved: cmn-vie={len(cmn_vie)}, cmn-eng={len(cmn_eng)}, total_linked={len(compact['sentences'])}"
    )


if __name__ == "__main__":
    main()
