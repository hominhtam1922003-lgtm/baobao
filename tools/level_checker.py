"""Chinese word segmentation and vocabulary level checker."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import re

CJK_RUN_RE = re.compile(r"[\u4e00-\u9fff]+")


@dataclass
class LevelCheckResult:
    passed: bool
    total_tokens: int
    unknown_tokens: int
    unknown_ratio: float
    unannotated_unknowns: list[str]
    under_repeated_new: list[str]
    tokens: list[str]


def segment_chinese(text: str, dictionary: set[str], max_len: int = 6) -> list[str]:
    """Greedy forward maximum matching over CJK runs using dictionary."""
    tokens: list[str] = []
    for run in CJK_RUN_RE.findall(text):
        i = 0
        n = len(run)
        while i < n:
            matched = None
            upper = min(max_len, n - i)
            for length in range(upper, 1, -1):
                cand = run[i : i + length]
                if cand in dictionary:
                    matched = cand
                    break
            if matched is None:
                matched = run[i]
            tokens.append(matched)
            i += len(matched)
    return tokens


def check_level(
    text: str,
    allowed_vocab: set[str],
    glossed_new: set[str],
    dictionary: set[str],
    max_unknown_ratio: float = 0.10,
    min_new_occurrences: int = 1,
) -> LevelCheckResult:
    """Validate that text stays within allowed_vocab + glossed_new."""
    full_dict = dictionary | allowed_vocab | glossed_new
    tokens = segment_chinese(text, full_dict)
    total = len(tokens)
    if total == 0:
        return LevelCheckResult(
            passed=True,
            total_tokens=0,
            unknown_tokens=0,
            unknown_ratio=0.0,
            unannotated_unknowns=[],
            under_repeated_new=[],
            tokens=[],
        )

    counts = Counter(tokens)
    unannotated = sorted({tok for tok in tokens if tok not in allowed_vocab and tok not in glossed_new})
    unknown_count = sum(1 for tok in tokens if tok not in allowed_vocab)
    unknown_ratio = unknown_count / total

    under_repeated: list[str] = []
    if min_new_occurrences > 1:
        under_repeated = sorted(
            w for w in glossed_new if counts.get(w, 0) < min_new_occurrences
        )

    passed = (
        len(unannotated) == 0
        and unknown_ratio <= max_unknown_ratio
        and len(under_repeated) == 0
    )

    return LevelCheckResult(
        passed=passed,
        total_tokens=total,
        unknown_tokens=unknown_count,
        unknown_ratio=round(unknown_ratio, 4),
        unannotated_unknowns=unannotated,
        under_repeated_new=under_repeated,
        tokens=tokens,
    )
