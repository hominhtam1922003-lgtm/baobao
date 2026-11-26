"""Generate offline MP3 audio files using edge-tts for all content in content/."""

from __future__ import annotations

import asyncio
import hashlib
import json
from pathlib import Path
import edge_tts

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
AUDIO_DIR = ROOT / "public" / "audio"

VOICES = {
    "teacher": ("zh-CN-XiaoxiaoNeural", "+0%"),
    "female": ("zh-CN-XiaoyiNeural", "+0%"),
    "male": ("zh-CN-YunxiNeural", "+0%"),
    "formal": ("zh-CN-YunyangNeural", "+0%"),
    "story": ("zh-CN-XiaoxiaoNeural", "-10%"),
    "slow": ("zh-CN-XiaoxiaoNeural", "-25%"),
}


def audio_filename(text: str, role: str) -> str:
    voice, rate = VOICES.get(role, VOICES["teacher"])
    digest = hashlib.sha1(f"{voice}|{rate}|{text}".encode("utf-8")).hexdigest()[:12]
    return f"{role}-{digest}.mp3"


async def synth_one(sem: asyncio.Semaphore, text: str, role: str, out_path: Path) -> bool:
    if out_path.exists() and out_path.stat().st_size > 1024:
        return True
    voice, rate = VOICES.get(role, VOICES["teacher"])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    async with sem:
        for attempt in range(1, 5):
            tmp = out_path.with_suffix(".mp3.part")
            try:
                comm = edge_tts.Communicate(text=text, voice=voice, rate=rate)
                await comm.save(str(tmp))
                if tmp.exists() and tmp.stat().st_size > 1024:
                    tmp.replace(out_path)
                    return True
            except Exception as exc:
                if tmp.exists():
                    tmp.unlink(missing_ok=True)
                await asyncio.sleep(1.2 * (2 ** (attempt - 1)))
                if attempt == 4:
                    print(f"FAIL audio {out_path.name}: {exc}")
    return False


def collect_jobs() -> tuple[list[tuple[str, str, str]], dict[str, set[str]]]:
    """Scan content/stage-* JSON files and collect unique (text, role, filename) audio jobs."""
    jobs: dict[str, tuple[str, str, str]] = {}
    stage_files: dict[str, set[str]] = {}

    def add(stage_name: str, text: str, role: str) -> str:
        fname = audio_filename(text, role)
        jobs[fname] = (text, role, fname)
        stage_files.setdefault(stage_name, set()).add(fname)
        return f"audio/{fname}"

    for stage_dir in sorted(CONTENT_DIR.glob("stage-*")):
        sname = stage_dir.name
        words_p = stage_dir / "words.json"
        if words_p.exists():
            words = json.loads(words_p.read_text(encoding="utf-8"))
            for w in words:
                w["audio"] = add(sname, w["hanzi"], "teacher")
                for ex in w.get("examples", []):
                    ex["audio"] = add(sname, ex["hanzi"], "teacher")
            words_p.write_text(json.dumps(words, ensure_ascii=False, indent=2), encoding="utf-8")

        lessons_p = stage_dir / "lessons.json"
        if lessons_p.exists():
            lessons = json.loads(lessons_p.read_text(encoding="utf-8"))
            for lesson in lessons:
                for pat in lesson.get("patterns", []):
                    pat["audio"] = add(sname, pat["exampleHanzi"], "teacher")
                for turn in lesson.get("dialogue", []):
                    role = turn.get("voiceRole", "female" if turn.get("speaker") != "Bao" else "male")
                    turn["audio"] = add(sname, turn["hanzi"], role)
                for rp in lesson.get("roleplay", []):
                    rp["npcAudio"] = add(sname, rp["npcHanzi"], "female")
                    rp["replyAudio"] = add(sname, rp["expectedHanzi"], "male")
                for ex in lesson.get("exercises", []):
                    if ex.get("audioText"):
                        ex["audio"] = add(sname, ex["audioText"], "teacher")
                        if lesson.get("type") == "nghe":
                            ex["audioSlow"] = add(sname, ex["audioText"], "slow")
                    for opt in ex.get("optionAudios", []):
                        opt["audio"] = add(sname, opt["hanzi"], "teacher")
                for track in lesson.get("listeningTracks", []):
                    track["audio"] = add(sname, track["hanzi"], track.get("voiceRole", "teacher"))
                    track["audioSlow"] = add(sname, track["hanzi"], "slow")
                for item in lesson.get("stageTestItems", []):
                    if item.get("audioText"):
                        item["audio"] = add(sname, item["audioText"], "teacher")
                        if item.get("skill") == "nghe":
                            item["audioSlow"] = add(sname, item["audioText"], "slow")
                    elif item.get("passageHanzi") and item.get("skill") == "giao-tiep":
                        item["audio"] = add(sname, item["passageHanzi"], "female")
            lessons_p.write_text(json.dumps(lessons, ensure_ascii=False, indent=2), encoding="utf-8")

        readings_p = stage_dir / "readings.json"
        if readings_p.exists():
            readings = json.loads(readings_p.read_text(encoding="utf-8"))
            for r in readings:
                full_text = "".join(p["hanzi"] for p in r.get("paragraphs", []))
                r["audioFull"] = add(sname, full_text, "story")
                sent_audios = []
                for p in r.get("paragraphs", []):
                    p_audio = add(sname, p["hanzi"], "story")
                    p["audio"] = p_audio
                    sent_audios.append(p_audio)
                r["audioSentences"] = sent_audios
            readings_p.write_text(json.dumps(readings, ensure_ascii=False, indent=2), encoding="utf-8")

    return list(jobs.values()), stage_files


async def main() -> None:
    jobs, stage_files = collect_jobs()
    sem = asyncio.Semaphore(4)
    done = 0
    ok = 0
    total = len(jobs)

    async def run_one(text: str, role: str, fname: str) -> bool:
        nonlocal done, ok
        res = await synth_one(sem, text, role, AUDIO_DIR / fname)
        done += 1
        if res:
            ok += 1
        if done % 100 == 0 or done == total:
            print(f"Audio progress: {done}/{total} (ok={ok})", flush=True)
        return res

    await asyncio.gather(*(run_one(text, role, fname) for text, role, fname in jobs))
    total_bytes = sum(p.stat().st_size for p in AUDIO_DIR.glob("*.mp3"))
    for sname, fnames in sorted(stage_files.items()):
        s_ok = sum(1 for fn in fnames if (AUDIO_DIR / fn).exists() and (AUDIO_DIR / fn).stat().st_size > 1024)
        s_mb = sum((AUDIO_DIR / fn).stat().st_size for fn in fnames if (AUDIO_DIR / fn).exists()) / (1024 * 1024)
        print(f"  {sname}: {s_ok}/{len(fnames)} MP3 ({s_mb:.2f} MB)")
    print(f"Audio generated: {ok}/{total} files OK, total {total_bytes / (1024 * 1024):.2f} MB")


if __name__ == "__main__":
    asyncio.run(main())
