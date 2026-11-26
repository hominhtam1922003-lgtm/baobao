"""TDD tests for level_checker seam."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from level_checker import check_level, count_hanzi_chars  # noqa: E402

SAMPLE_DICT = {
    "你好",
    "我",
    "叫",
    "小",
    "明",
    "小明",
    "喝",
    "茶",
    "奶茶",
    "咖啡",
    "冰",
    "冰咖啡",
    "量子力学",
}


def test_passes_when_all_words_are_in_allowed_vocab():
    result = check_level(
        text="你好！我叫小明。",
        allowed_vocab={"你好", "我", "叫", "小明"},
        glossed_new=set(),
        dictionary=SAMPLE_DICT,
        max_unknown_ratio=0.10,
    )
    assert result.passed is True
    assert result.unknown_ratio == 0.0
    assert result.unannotated_unknowns == []


def test_fails_when_unannotated_unknown_word_is_present():
    result = check_level(
        text="我喜欢量子力学。",
        allowed_vocab={"我", "喜欢"},
        glossed_new=set(),
        dictionary=SAMPLE_DICT | {"喜欢"},
        max_unknown_ratio=0.10,
    )
    assert result.passed is False
    assert "量子力学" in result.unannotated_unknowns


def test_allows_glossed_new_words_within_threshold():
    # 3 new tokens (奶茶, 冰咖啡, 奶茶) out of 15 total tokens = 0.20 <= 0.25
    result = check_level(
        text="你好，小明！我喝奶茶，你喝冰咖啡吗？我喜欢喝茶。",
        allowed_vocab={"你好", "小明", "我", "喝", "你", "吗", "喜欢", "茶"},
        glossed_new={"奶茶", "冰咖啡"},
        dictionary=SAMPLE_DICT | {"你", "吗", "喜欢"},
        max_unknown_ratio=0.25,
    )
    assert result.passed is True
    assert result.unannotated_unknowns == []


def test_fails_when_glossed_new_word_exceeds_ratio():
    result = check_level(
        text="奶茶咖啡",
        allowed_vocab={"我"},
        glossed_new={"奶茶", "咖啡"},
        dictionary=SAMPLE_DICT,
        max_unknown_ratio=0.10,
    )
    assert result.passed is False
    assert result.unknown_ratio > 0.10


def test_reading_mode_requires_glossed_words_appear_at_least_twice():
    result = check_level(
        text="你好，我喝奶茶，我喝茶。",
        allowed_vocab={"你好", "我", "喝", "茶"},
        glossed_new={"奶茶"},
        dictionary=SAMPLE_DICT,
        max_unknown_ratio=0.20,
        min_new_occurrences=2,
    )
    assert result.passed is False
    assert "奶茶" in result.under_repeated_new


def test_count_hanzi_chars_ignores_punctuation_and_latin():
    assert count_hanzi_chars("Bao说：「你好，请喝茶！」123") == 6
    assert count_hanzi_chars("") == 0
