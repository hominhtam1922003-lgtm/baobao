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


def collect_jobs() -> list[tuple[str, str, str]]:
    """Scan content/stage-* JSON files and collect unique (text, role, filename) audio jobs."""
    jobs: dict[str, tuple[str, str, str]] = {}

    def add(text: str, role: str) -> str:
        fname = audio_filename(text, role)
        jobs[fname] = (text, role, fname)
        return f"audio/{fname}"

    for stage_dir in sorted(CONTENT_DIR.glob("stage-*")):
        words_p = stage_dir / "words.json"
        if words_p.exists():
            words = json.loads(words_p.read_text(encoding="utf-8"))
            for w in words:
                w["audio"] = add(w["hanzi"], "teacher")
                for ex in w.get("examples", []):
                    ex["audio"] = add(ex["hanzi"], "teacher")
            words_p.write_text(json.dumps(words, ensure_ascii=False, indent=2), encoding="utf-8")

        lessons_p = stage_dir / "lessons.json"
        if lessons_p.exists():
            lessons = json.loads(lessons_p.read_text(encoding="utf-8"))
            for lesson in lessons:
                for pat in lesson.get("patterns", []):
                    pat["audio"] = add(pat["exampleHanzi"], "teacher")
                for turn in lesson.get("dialogue", []):
                    role = turn.get("voiceRole", "female" if turn.get("speaker") != "Bao" else "male")
                    turn["audio"] = add(turn["hanzi"], role)
                for rp in lesson.get("roleplay", []):
                    rp["npcAudio"] = add(rp["npcHanzi"], "female")
                    rp["replyAudio"] = add(rp["expectedHanzi"], "male")
                for ex in lesson.get("exercises", []):
                    if ex.get("audioText"):
                        ex["audio"] = add(ex["audioText"], "teacher")
                        if lesson.get("type") == "nghe":
                            ex["audioSlow"] = add(ex["audioText"], "slow")
                    for opt in ex.get("optionAudios", []):
                        opt["audio"] = add(opt["hanzi"], "teacher")
                for track in lesson.get("listeningTracks", []):
                    track["audio"] = add(track["hanzi"], track.get("voiceRole", "teacher"))
                    track["audioSlow"] = add(track["hanzi"], "slow")
            lessons_p.write_text(json.dumps(lessons, ensure_ascii=False, indent=2), encoding="utf-8")

        readings_p = stage_dir / "readings.json"
        if readings_p.exists():
            readings = json.loads(readings_p.read_text(encoding="utf-8"))
            for r in readings:
                full_text = "".join(p["hanzi"] for p in r.get("paragraphs", []))
                r["audioFull"] = add(full_text, "story")
                sent_audios = []
                for p in r.get("paragraphs", []):
                    p_audio = add(p["hanzi"], "story")
                    p["audio"] = p_audio
                    sent_audios.append(p_audio)
                r["audioSentences"] = sent_audios
            readings_p.write_text(json.dumps(readings, ensure_ascii=False, indent=2), encoding="utf-8")

    return list(jobs.values())


async def main() -> None:
    jobs = collect_jobs()
    sem = asyncio.Semaphore(3)
    results = await asyncio.gather(
        *(synth_one(sem, text, role, AUDIO_DIR / fname) for text, role, fname in jobs)
    )
    ok = sum(1 for r in results if r)
    total_bytes = sum(p.stat().st_size for p in AUDIO_DIR.glob("*.mp3"))
    print(f"Audio generated: {ok}/{len(jobs)} files OK, total {total_bytes / (1024 * 1024):.2f} MB")


if __name__ == "__main__":
    asyncio.run(main())
