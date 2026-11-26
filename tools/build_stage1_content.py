"""Build Stage 1 words + full sample lessons & readings for Topic 1 and Topic 6, then verify with level_checker."""

from __future__ import annotations

import json
from pathlib import Path
from pypinyin import pinyin as to_pinyin, Style

from level_checker import check_level

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
STAGE1_DIR = CONTENT_DIR / "stage-1"
CACHE_DIR = ROOT / "tools" / ".cache"
DATA_DIR = ROOT / "data-src"

# Curated Vietnamese dictionary for Stage 1 core words (no HSK label exposed in UI)
STAGE1_VI_CORE: list[tuple[str, str, str]] = [
    # Topic 1 — Chào hỏi & tạm biệt
    ("你好", "xin chào", "Hai người (亻 + 尔) gặp nhau chúc điều tốt lành (好 = 女 mẹ + 子 con)"),
    ("你们", "các bạn", ""),
    ("老师", "thầy / cô giáo", ""),
    ("谢谢", "cảm ơn", "Bộ ngôn (讠) — lời nói cảm tạ"),
    ("不客气", "không có gì, đừng khách sáo", ""),
    ("再见", "tạm biệt", "再 (lại) + 见 (gặp) = hẹn gặp lại"),
    ("早上", "buổi sáng", "Hình mặt trời (日) mọc lên trên đường chân trời (早)"),
    ("晚上", "buổi tối", "Bộ nhật (日) chỉ thời gian lúc trời tối"),
    ("我", "tôi, mình", ""),
    ("你", "bạn", "Bộ nhân đứng (亻) chỉ người đối diện"),
    ("他", "anh ấy", ""),
    ("她", "cô ấy", ""),
    ("我们", "chúng tôi, chúng mình", ""),
    ("好", "tốt, khỏe", "Chữ 女 (nữ) cạnh 子 (tử): mẹ ôm con tượng trưng điều tốt lành"),
    ("很", "rất", ""),
    ("吗", "không? (trợ từ nghi vấn)", "Bộ khẩu (口) ở trước để hỏi"),
    ("呢", "thế còn...? (trợ từ)", ""),
    ("也", "cũng", ""),
    ("是", "là", ""),
    ("不", "không", ""),
    ("没关系", "không sao đâu", ""),
    ("对不起", "xin lỗi", ""),
    ("请", "xin mời", "Bộ ngôn (讠) — lời nói lịch sự"),
    ("进", "vào", ""),
    ("坐", "ngồi", "Hai người (人) ngồi trên đất (土)"),
    ("请坐", "mời ngồi", ""),
    ("见", "gặp, thấy", "Con mắt (目) bước đi để nhìn thấy và gặp mặt"),
    ("新", "mới", ""),
    ("对", "đúng, đối diện", ""),
    ("开心", "vui vẻ", "Mở (开) lòng (心) ra là vui vẻ"),
    ("课", "tiết học, bài học", ""),
    ("后", "sau", ""),
    ("下午", "buổi chiều", ""),
    ("店", "quán, cửa hàng", ""),
    ("一家", "một quán / nhà", ""),
    ("这里", "ở đây", ""),
    ("还有", "còn có", ""),
    ("问", "hỏi", "Cái miệng (口) đặt trong cánh cửa (门) để hỏi"),
    ("一共", "tổng cộng", ""),
    ("四十", "bốn mươi", ""),
    ("十", "mười", "Hình chữ thập (+) tượng trưng số mười"),
    ("请问", "xin hỏi", "请 (xin mời) + 问 (hỏi) = xin phép hỏi"),
    ("还是", "hay là (trong câu hỏi lựa chọn)", ""),
    ("给", "cho, đưa cho", ""),
    ("还", "còn, vẫn", ""),
    ("帮", "giúp, giúp đỡ", ""),
    ("您", "ngài, bạn (kính ngữ)", "你 (bạn) đặt trên 心 (lòng) = kính trọng"),
    ("可以", "có thể, được", ""),
    ("真", "thật là", ""),
    ("红茶", "hồng trà, trà đen", ""),
    ("再", "lại, nữa", ""),
    ("先", "trước", ""),
    ("最后", "cuối cùng", ""),
    # Topic 2-5 core glue words (for natural sentences & reading)
    ("叫", "tên là, gọi", "Bộ khẩu (口) — cất tiếng gọi"),
    ("什么", "cái gì", ""),
    ("名字", "tên", ""),
    ("这", "đây, này", ""),
    ("那", "đó, kia", ""),
    ("谁", "ai", ""),
    ("哪", "nào", ""),
    ("人", "người", "Dáng người đang bước đi"),
    ("越南", "Việt Nam", ""),
    ("中国", "Trung Quốc", ""),
    ("朋友", "bạn bè", ""),
    ("同学", "bạn học", ""),
    ("家", "nhà, gia đình", "Mái nhà (宀) che chở cho cuộc sống bên dưới (豕)"),
    ("今天", "hôm nay", ""),
    ("明天", "ngày mai", ""),
    ("现在", "bây giờ", ""),
    ("点", "giờ / gọi món", ""),
    ("去", "đi", ""),
    ("来", "đến", ""),
    ("在", "ở, đang", ""),
    ("有", "có", ""),
    ("没有", "không có", ""),
    ("看", "nhìn, xem", "Tay (手) che trên mắt (目) để nhìn xa"),
    ("听", "nghe", "Bộ khẩu (口) và tai lắng nghe"),
    ("说", "nói", "Bộ ngôn (讠) — phát ra lời nói"),
    ("读", "đọc", "Bộ ngôn (讠) — đọc thành tiếng"),
    ("写", "viết", ""),
    ("学", "học", ""),
    ("中文", "tiếng Trung", ""),
    ("喜欢", "thích", ""),
    ("想", "muốn, nhớ", "Bộ tâm (心) ở dưới — suy nghĩ trong lòng"),
    ("要", "muốn, cần", ""),
    ("会", "biết, sẽ", ""),
    ("能", "có thể", ""),
    ("都", "đều", ""),
    ("和", "và", ""),
    ("的", "của", ""),
    ("了", "rồi (trợ từ)", ""),
    ("一", "một", "Một nét ngang đơn"),
    ("二", "hai", "Hai nét ngang"),
    ("三", "ba", "Ba nét ngang"),
    ("两", "hai (số lượng)", ""),
    ("几", "mấy", ""),
    ("多少", "bao nhiêu", ""),
    ("个", "cái (lượng từ chung)", ""),
    ("大", "to, lớn", "Người dang rộng hai tay"),
    ("小", "nhỏ, bé", ""),
    ("多", "nhiều", ""),
    ("少", "ít", ""),
    # Topic 6 — Ăn uống: gọi món, trà sữa & cà phê
    ("喝", "uống", "Bộ khẩu (口) — đưa đồ uống vào miệng"),
    ("吃", "ăn", "Bộ khẩu (口) — ăn bằng miệng"),
    ("茶", "trà", "Bộ thảo (艹) chỉ lá cây trà"),
    ("奶茶", "trà sữa", "奶 (sữa) + 茶 (trà)"),
    ("咖啡", "cà phê", "Cả hai chữ đều có bộ khẩu (口)"),
    ("水", "nước", "Dòng nước chảy uốn lượn"),
    ("冰", "đá lạnh", "Bộ băng (冫) hai giọt nước đóng băng"),
    ("热", "nóng", "Bộ hỏa chấm (灬) ở dưới — hơi nóng bốc lên"),
    ("甜", "ngọt", "Bộ thiệt (舌 cái lưỡi) + 甘 (ngọt)"),
    ("杯", "cốc, ly", "Bộ mộc (木) — cốc gỗ ngày xưa"),
    ("菜单", "thực đơn", ""),
    ("点菜", "gọi món", ""),
    ("好吃", "ngon (đồ ăn)", ""),
    ("好喝", "ngon (đồ uống)", ""),
    ("买单", "tính tiền", ""),
    ("钱", "tiền", "Bộ kim (钅) — đồng tiền kim loại"),
    ("块", "đồng / tệ (đơn vị tiền nói)", ""),
    ("便宜", "rẻ", ""),
    ("贵", "đắt", ""),
    ("服务员", "nhân viên phục vụ", ""),
    ("饭", "cơm, bữa ăn", "Bộ thực (饣) liên quan tới thức ăn"),
    ("面条", "mì sợi", ""),
    ("包子", "bánh bao", ""),
    ("水果", "trái cây", ""),
    ("小笼包", "tiểu long bao", ""),
    ("少糖", "ít đường", ""),
    ("去冰", "không đá", ""),
]

CURRICULUM = {
    "stages": [
        {
            "id": 1,
            "title": "Chặng 1 — Sinh tồn",
            "subtitle": "Chào hỏi, giới thiệu, ăn uống, mua sắm và hỏi đường hằng ngày",
            "colorToken": "comm",
            "grammarNotes": [
                {
                    "title": "Câu hỏi Có/Không với 吗 (ma)",
                    "pattern": "Chủ ngữ + Động từ + Tân ngữ + 吗？",
                    "explainVi": "Chỉ cần thêm 吗 vào cuối câu trần thuật để tạo câu hỏi Có/Không.",
                    "exampleHanzi": "你喝奶茶吗？",
                    "exampleVi": "Bạn uống trà sữa không?",
                },
                {
                    "title": "Muốn hoặc định làm gì với 想 (xiǎng)",
                    "pattern": "Chủ ngữ + 想 + Động từ + Tân ngữ",
                    "explainVi": "想 đứng trước động từ để diễn đạt mong muốn lịch sự khi gọi món hay rủ bạn.",
                    "exampleHanzi": "我想喝一杯热茶。",
                    "exampleVi": "Mình muốn uống một ly trà nóng.",
                },
                {
                    "title": "Lượng từ 杯 (bēi) cho đồ uống",
                    "pattern": "Số từ + 杯 + (Tính từ) + Đồ uống",
                    "explainVi": "Dùng 一杯, 两杯 (không dùng 二杯) khi gọi trà sữa hoặc cà phê.",
                    "exampleHanzi": "我要两杯冰咖啡。",
                    "exampleVi": "Cho mình hai ly cà phê đá.",
                },
            ],
            "storyChapter": {
                "title": "Chương 1: Ngày đầu Bao tới phố cổ",
                "teaserVi": "Bao lần đầu tự đi quán trà sữa gọi món bằng tiếng Trung — liệu cậu có gọi đúng ly ít đường không đá?",
                "readingId": "r-t6",
            },
            "topics": [
                {"id": 1, "stage": 1, "title": "Chào hỏi & tạm biệt", "subtitle": "Làm quen, cảm ơn, xin lỗi tự nhiên", "ready": True, "lessonIds": ["t1-giao-tiep", "t1-doc", "t1-nghe", "t1-viet"], "readingId": "r-t1"},
                {"id": 2, "stage": 1, "title": "Giới thiệu bản thân", "subtitle": "Tên, quốc tịch, bạn mới", "ready": False, "lessonIds": []},
                {"id": 3, "stage": 1, "title": "Số đếm, tuổi & ngày tháng", "subtitle": "Đọc số, hỏi tuổi, sinh nhật", "ready": False, "lessonIds": []},
                {"id": 4, "stage": 1, "title": "Gia đình & bạn bè", "subtitle": "Kể về người thân và bạn thân", "ready": False, "lessonIds": []},
                {"id": 5, "stage": 1, "title": "Thời gian & hẹn gặp", "subtitle": "Hỏi giờ và đặt lịch gặp", "ready": False, "lessonIds": []},
                {"id": 6, "stage": 1, "title": "Ăn uống: gọi món, trà sữa & cà phê", "subtitle": "Xem thực đơn, chọn ít đường/đá, tính tiền", "ready": True, "lessonIds": ["t6-giao-tiep", "t6-doc", "t6-nghe", "t6-viet"], "readingId": "r-t6"},
                {"id": 7, "stage": 1, "title": "Mua sắm & mặc cả", "subtitle": "Hỏi giá, chọn cỡ và trả giá nhẹ", "ready": False, "lessonIds": []},
                {"id": 8, "stage": 1, "title": "Hỏi đường & đi lại", "subtitle": "Rẽ trái phải, tàu điện và taxi", "ready": False, "lessonIds": []},
            ],
        },
        {
            "id": 2,
            "title": "Chặng 2 — Đời sống",
            "subtitle": "Sở thích, thời tiết, công việc, nhà ở và mua sắm online",
            "colorToken": "read",
            "grammarNotes": [],
            "storyChapter": {"title": "Chương 2: Căn phòng mới của Bao", "teaserVi": "Mở khoá ở Đợt 2 sau khi hoàn thành 80% Chặng 1."},
            "topics": [
                {"id": 9, "stage": 2, "title": "Sở thích & thời gian rảnh", "subtitle": "Đợt 2", "ready": False, "lessonIds": []},
                {"id": 10, "stage": 2, "title": "Thời tiết & mùa", "subtitle": "Đợt 2", "ready": False, "lessonIds": []},
                {"id": 11, "stage": 2, "title": "Trường học & học tập", "subtitle": "Đợt 2", "ready": False, "lessonIds": []},
                {"id": 12, "stage": 2, "title": "Công việc & nghề nghiệp", "subtitle": "Đợt 2", "ready": False, "lessonIds": []},
                {"id": 13, "stage": 2, "title": "Sức khỏe: đi khám, mua thuốc", "subtitle": "Đợt 2", "ready": False, "lessonIds": []},
                {"id": 14, "stage": 2, "title": "Nhà ở: thuê nhà, hỏi tiện nghi", "subtitle": "Đợt 2", "ready": False, "lessonIds": []},
                {"id": 15, "stage": 2, "title": "Điện thoại, mạng xã hội & internet", "subtitle": "Đợt 2", "ready": False, "lessonIds": []},
                {"id": 16, "stage": 2, "title": "Mua sắm online & nhận hàng", "subtitle": "Đợt 2", "ready": False, "lessonIds": []},
            ],
        },
        {
            "id": 3,
            "title": "Chặng 3 — Xã hội & giải trí",
            "subtitle": "Kết bạn, hẹn đi chơi, phim nhạc, du lịch và lễ tết",
            "colorToken": "review",
            "grammarNotes": [],
            "storyChapter": {"title": "Chương 3: Chuyến tàu cuối tuần", "teaserVi": "Mở khoá ở Đợt 2."},
            "topics": [
                {"id": 17, "stage": 3, "title": "Kết bạn mới & giữ liên lạc", "subtitle": "Đợt 2", "ready": False, "lessonIds": []},
                {"id": 18, "stage": 3, "title": "Hẹn gặp & lên kế hoạch đi chơi", "subtitle": "Đợt 2", "ready": False, "lessonIds": []},
                {"id": 19, "stage": 3, "title": "Phim, nhạc & thần tượng", "subtitle": "Đợt 2", "ready": False, "lessonIds": []},
                {"id": 20, "stage": 3, "title": "Thể thao & vận động", "subtitle": "Đợt 2", "ready": False, "lessonIds": []},
                {"id": 21, "stage": 3, "title": "Du lịch: khách sạn, vé, điểm tham quan", "subtitle": "Đợt 2", "ready": False, "lessonIds": []},
                {"id": 22, "stage": 3, "title": "Lễ tết & phong tục", "subtitle": "Đợt 2", "ready": False, "lessonIds": []},
                {"id": 23, "stage": 3, "title": "Cảm xúc & tính cách", "subtitle": "Đợt 2", "ready": False, "lessonIds": []},
                {"id": 24, "stage": 3, "title": "Kể chuyện đã qua", "subtitle": "Đợt 2", "ready": False, "lessonIds": []},
            ],
        },
        {
            "id": 4,
            "title": "Chặng 4 — Tự tin giao tiếp",
            "subtitle": "Trình bày quan điểm, dự định tương lai và xử lý tình huống khó",
            "colorToken": "write",
            "grammarNotes": [],
            "storyChapter": {"title": "Chương 4: Hội chợ mùa thu", "teaserVi": "Mở khoá ở Đợt 2."},
            "topics": [
                {"id": 25, "stage": 4, "title": "Bày tỏ ý kiến & đồng ý/phản đối nhẹ nhàng", "subtitle": "Đợt 2", "ready": False, "lessonIds": []},
                {"id": 26, "stage": 4, "title": "Dự định & ước mơ tương lai", "subtitle": "Đợt 2", "ready": False, "lessonIds": []},
                {"id": 27, "stage": 4, "title": "Công nghệ & AI trong đời sống", "subtitle": "Đợt 2", "ready": False, "lessonIds": []},
                {"id": 28, "stage": 4, "title": "Tình huống khó: nhờ giúp đỡ, khẩn cấp & xin lỗi", "subtitle": "Đợt 2", "ready": False, "lessonIds": []},
            ],
        },
    ]
}


def build_words() -> tuple[list[dict], dict[str, int]]:
    pool_list = json.loads((CACHE_DIR / "hsk_1_3_pool.json").read_text(encoding="utf-8"))
    pool_map = {item["hanzi"]: item for item in pool_list}
    tatoeba = json.loads((DATA_DIR / "tatoeba_cmn_pairs.json").read_text(encoding="utf-8"))
    short_vie = [s for s in tatoeba["sentences"] if s["vie"] and 3 <= len(s["cmn"]) <= 18]

    def find_tatoeba_example(hanzi: str) -> list[dict]:
        hits = []
        for s in short_vie:
            if hanzi in s["cmn"]:
                py = " ".join(x[0] for x in to_pinyin(s["cmn"], style=Style.TONE))
                hits.append({"hanzi": s["cmn"], "pinyin": py, "vi": s["vie"][0]})
                if len(hits) >= 2:
                    break
        return hits

    fallback_examples = {
        "你好": [{"hanzi": "你好，请问你叫什么名字？", "pinyin": "nǐ hǎo, qǐng wèn nǐ jiào shén me míng zi?", "vi": "Xin chào, xin hỏi bạn tên gì?"}],
        "谢谢": [{"hanzi": "谢谢你的茶！", "pinyin": "xiè xie nǐ de chá!", "vi": "Cảm ơn trà của bạn!"}],
        "不客气": [{"hanzi": "不客气，我们是好朋友。", "pinyin": "bú kè qi, wǒ men shì hǎo péng you.", "vi": "Không có gì, chúng ta là bạn tốt mà."}],
        "再见": [{"hanzi": "明天见，再见！", "pinyin": "míng tiān jiàn, zài jiàn!", "vi": "Hẹn gặp ngày mai, tạm biệt!"}],
        "早上": [{"hanzi": "早上好，今天天气很好。", "pinyin": "zǎo shang hǎo, jīn tiān tiān qì hěn hǎo.", "vi": "Chào buổi sáng, hôm nay trời rất đẹp."}],
        "晚上": [{"hanzi": "晚上我们一起喝茶吧。", "pinyin": "wǎn shang wǒ men yì qǐ hē chá ba.", "vi": "Tối nay chúng mình cùng uống trà nhé."}],
        "奶茶": [{"hanzi": "我想喝一杯冰奶茶。", "pinyin": "wǒ xiǎng hē yì bēi bīng nǎi chá.", "vi": "Mình muốn uống một ly trà sữa đá."}],
        "咖啡": [{"hanzi": "你要热咖啡还是冰咖啡？", "pinyin": "nǐ yào rè kā fēi hái shi bīng kā fēi?", "vi": "Bạn muốn cà phê nóng hay cà phê đá?"}],
        "少糖": [{"hanzi": "这杯奶茶请给我少糖。", "pinyin": "zhè bēi nǎi chá qǐng gěi wǒ shǎo táng.", "vi": "Ly trà sữa này cho mình ít đường nhé."}],
        "去冰": [{"hanzi": "我要一杯红茶，去冰。", "pinyin": "wǒ yào yì bēi hóng chá, qù bīng.", "vi": "Cho mình một ly hồng trà, không đá."}],
        "买单": [{"hanzi": "服务员，请帮我买单。", "pinyin": "fú wù yuán, qǐng bāng wǒ mǎi dān.", "vi": "Phục vụ ơi, làm ơn tính tiền giúp mình."}],
        "好喝": [{"hanzi": "这家店的奶茶很好喝！", "pinyin": "zhè jiā diàn de nǎi chá hěn hǎo hē!", "vi": "Trà sữa quán này ngon lắm!"}],
        "好吃": [{"hanzi": "今天的小笼包真好吃。", "pinyin": "jīn tiān de xiǎo lóng bāo zhēn hǎo chī.", "vi": "Tiểu long bao hôm nay ngon thật."}],
        "菜单": [{"hanzi": "请问，可以看看菜单吗？", "pinyin": "qǐng wèn, kě yǐ kàn kan cài dān ma?", "vi": "Xin hỏi, mình xem thực đơn được không?"}],
        "小笼包": [{"hanzi": "我想点一份小笼包。", "pinyin": "wǒ xiǎng diǎn yí fèn xiǎo lóng bāo.", "vi": "Mình muốn gọi một phần tiểu long bao."}],
    }

    words: list[dict] = []
    tatoeba_count = 0
    for idx, (hanzi, vi, mnemonic) in enumerate(STAGE1_VI_CORE, start=1):
        meta = pool_map.get(hanzi, {})
        py = meta.get("pinyin") or " ".join(x[0] for x in to_pinyin(hanzi, style=Style.TONE))
        examples = find_tatoeba_example(hanzi)
        if examples:
            tatoeba_count += 1
        elif hanzi in fallback_examples:
            examples = fallback_examples[hanzi]
        else:
            examples = [
                {
                    "hanzi": f"我学「{hanzi}」。",
                    "pinyin": f"wǒ xué {py}.",
                    "vi": f"Mình học từ \"{vi}\".",
                }
            ]
        words.append(
            {
                "id": f"w-{idx:03d}",
                "hanzi": hanzi,
                "pinyin": py,
                "meaningVi": vi,
                "radical": meta.get("radical") or "",
                "level": meta.get("level", 1),
                "frequency": meta.get("frequency", idx * 10),
                "mnemonic": mnemonic,
                "examples": examples,
            }
        )

    return words, {"words": len(words), "tatoeba_matched": tatoeba_count}


def build_lessons_and_readings(words: list[dict]) -> tuple[list[dict], list[dict]]:
    by_hz = {w["hanzi"]: w for w in words}

    t1_new = [by_hz[h]["id"] for h in ["你好", "早上", "谢谢", "不客气", "再见"]]
    t6_new = [by_hz[h]["id"] for h in ["喝", "奶茶", "咖啡", "杯", "少糖", "买单"]]

    lessons = [
        # ---------------- TOPIC 1 ----------------
        {
            "id": "t1-giao-tiep",
            "stage": 1,
            "topicId": 1,
            "title": "Chào hỏi & tạm biệt",
            "type": "giao-tiep",
            "xp": 30,
            "newWords": t1_new,
            "patterns": [
                {
                    "id": "p-t1-1",
                    "frame": "___好！",
                    "pinyin": "___ hǎo!",
                    "meaningVi": "Chào [ai đó / buổi trong ngày]!",
                    "exampleHanzi": "老师好！",
                    "examplePinyin": "lǎo shī hǎo!",
                    "exampleVi": "Em chào thầy/cô ạ!",
                    "slots": {
                        "promptVi": "Chọn từ để nói 'Chào buổi sáng!'",
                        "choices": [
                            {"hanzi": "早上", "pinyin": "zǎo shang", "vi": "buổi sáng"},
                            {"hanzi": "谢谢", "pinyin": "xiè xie", "vi": "cảm ơn"},
                            {"hanzi": "再见", "pinyin": "zài jiàn", "vi": "tạm biệt"},
                        ],
                        "answerHanzi": "早上",
                    },
                },
                {
                    "id": "p-t1-2",
                    "frame": "谢谢你！— ___。",
                    "pinyin": "xiè xie nǐ! — ___.",
                    "meaningVi": "Cảm ơn bạn! — Không có gì.",
                    "exampleHanzi": "谢谢你，不客气。",
                    "examplePinyin": "xiè xie nǐ, bú kè qi.",
                    "exampleVi": "Cảm ơn bạn — Không có gì đâu.",
                    "slots": {
                        "promptVi": "Đáp lại lời cảm ơn một cách lịch sự",
                        "choices": [
                            {"hanzi": "不客气", "pinyin": "bú kè qi", "vi": "không có gì"},
                            {"hanzi": "对不起", "pinyin": "duì bu qǐ", "vi": "xin lỗi"},
                            {"hanzi": "你好", "pinyin": "nǐ hǎo", "vi": "xin chào"},
                        ],
                        "answerHanzi": "不客气",
                    },
                },
            ],
            "dialogue": [
                {"speaker": "Linh", "voiceRole": "female", "hanzi": "早上好！你是新同学吗？", "pinyin": "zǎo shang hǎo! nǐ shì xīn tóng xué ma?", "vi": "Chào buổi sáng! Bạn là bạn học mới à?", "mode": "npc", "goalLabel": "Chào buổi sáng"},
                {
                    "speaker": "Bao",
                    "voiceRole": "male",
                    "hanzi": "早上好！对，我是Bao。",
                    "pinyin": "zǎo shang hǎo! duì, wǒ shì Bao.",
                    "vi": "Chào buổi sáng! Đúng rồi, mình là Bao.",
                    "mode": "choice",
                    "goalLabel": "Đáp lời chào & giới thiệu",
                    "choices": [
                        {"hanzi": "早上好！对，我是Bao。", "pinyin": "zǎo shang hǎo! duì, wǒ shì Bao.", "vi": "Chào buổi sáng! Đúng rồi, mình là Bao.", "correct": True},
                        {"hanzi": "再见！我是咖啡。", "pinyin": "zài jiàn! wǒ shì kā fēi.", "vi": "Tạm biệt! Mình là cà phê.", "correct": False},
                        {"hanzi": "不客气，谢谢。", "pinyin": "bú kè qi, xiè xie.", "vi": "Không có gì, cảm ơn.", "correct": False},
                    ],
                },
                {"speaker": "Linh", "voiceRole": "female", "hanzi": "你好！请坐。", "pinyin": "nǐ hǎo! qǐng zuò.", "vi": "Xin chào! Mời ngồi.", "mode": "npc"},
                {
                    "speaker": "Bao",
                    "voiceRole": "male",
                    "hanzi": "谢谢你！",
                    "pinyin": "xiè xie nǐ!",
                    "vi": "Cảm ơn bạn!",
                    "mode": "tiles",
                    "goalLabel": "Nói lời cảm ơn",
                    "tilePrompt": ["谢谢", "你"],
                },
                {"speaker": "Linh", "voiceRole": "female", "hanzi": "不客气！明天见。", "pinyin": "bú kè qi! míng tiān jiàn.", "vi": "Không có gì! Hẹn gặp ngày mai nhé.", "mode": "npc"},
                {
                    "speaker": "Bao",
                    "voiceRole": "male",
                    "hanzi": "再见！",
                    "pinyin": "zài jiàn!",
                    "vi": "Tạm biệt!",
                    "mode": "pinyin",
                    "goalLabel": "Chào tạm biệt",
                    "acceptedPinyin": ["zaijian", "zàijiàn", "zai jian", "再见"],
                },
            ],
            "exercises": [
                {
                    "id": "ex-t1-1",
                    "kind": "meaning-choice",
                    "promptVi": "Cụm 「谢谢」 có nghĩa là gì?",
                    "hanziPrompt": "谢谢",
                    "pinyinPrompt": "xiè xie",
                    "options": [
                        {"label": "Cảm ơn", "value": "Cảm ơn"},
                        {"label": "Tạm biệt", "value": "Tạm biệt"},
                        {"label": "Xin lỗi", "value": "Xin lỗi"},
                        {"label": "Chào buổi sáng", "value": "Chào buổi sáng"},
                    ],
                    "answer": "Cảm ơn",
                },
                {
                    "id": "ex-t1-2",
                    "kind": "hanzi-choice",
                    "promptVi": "Nghe và chọn chữ Hán đúng với nghĩa 'Không có gì'",
                    "audioText": "不客气",
                    "options": [
                        {"label": "不客气", "value": "不客气"},
                        {"label": "对不起", "value": "对不起"},
                        {"label": "没关系", "value": "没关系"},
                        {"label": "早上好", "value": "早上好"},
                    ],
                    "answer": "不客气",
                },
                {
                    "id": "ex-t1-3",
                    "kind": "sentence-tiles",
                    "promptVi": "Ghép câu: 'Chào buổi sáng, thầy/cô giáo!'",
                    "tiles": ["老师", "早上", "好"],
                    "answer": "早上好老师",
                    "explainVi": "Nói '老师，早上好！' hoặc '早上好老师' đều tự nhiên; đặt 早上好 lên trước để chào buổi sáng.",
                },
            ],
            "roleplay": [
                {
                    "npcHanzi": "你好！请问你叫什么名字？",
                    "npcPinyin": "nǐ hǎo! qǐng wèn nǐ jiào shén me míng zi?",
                    "npcVi": "Xin chào! Xin hỏi bạn tên gì?",
                    "promptVi": "Chào lại và nói tên của bạn",
                    "options": [
                        {"hanzi": "你好！我叫小明。", "pinyin": "nǐ hǎo! wǒ jiào Xiǎo Míng.", "vi": "Xin chào! Mình tên là Tiểu Minh.", "correct": True},
                        {"hanzi": "再见！老师好。", "pinyin": "zài jiàn! lǎo shī hǎo.", "vi": "Tạm biệt! Chào thầy cô.", "correct": False},
                        {"hanzi": "不客气。", "pinyin": "bú kè qi.", "vi": "Không có gì.", "correct": False},
                    ],
                    "expectedHanzi": "你好！我叫小明。",
                },
                {
                    "npcHanzi": "请进，请坐！",
                    "npcPinyin": "qǐng jìn, qǐng zuò!",
                    "npcVi": "Mời vào, mời ngồi!",
                    "promptVi": "Đáp lại lời mời lịch sự",
                    "options": [
                        {"hanzi": "谢谢你！", "pinyin": "xiè xie nǐ!", "vi": "Cảm ơn bạn!", "correct": True},
                        {"hanzi": "对不起！", "pinyin": "duì bu qǐ!", "vi": "Xin lỗi!", "correct": False},
                        {"hanzi": "早上好。", "pinyin": "zǎo shang hǎo.", "vi": "Chào buổi sáng.", "correct": False},
                    ],
                    "expectedHanzi": "谢谢你！",
                },
                {
                    "npcHanzi": "不客气！明天见！",
                    "npcPinyin": "bú kè qi! míng tiān jiàn!",
                    "npcVi": "Không có gì! Hẹn gặp ngày mai!",
                    "promptVi": "Chào tạm biệt để kết thúc cuộc trò chuyện",
                    "options": [
                        {"hanzi": "明天见，再见！", "pinyin": "míng tiān jiàn, zài jiàn!", "vi": "Ngày mai gặp, tạm biệt!", "correct": True},
                        {"hanzi": "你好！", "pinyin": "nǐ hǎo!", "vi": "Xin chào!", "correct": False},
                        {"hanzi": "请坐！", "pinyin": "qǐng zuò!", "vi": "Mời ngồi!", "correct": False},
                    ],
                    "expectedHanzi": "明天见，再见！",
                },
            ],
        },
        {"id": "t1-doc", "stage": 1, "topicId": 1, "title": "Đọc: Ngày đầu ở lớp tiếng Trung", "type": "doc", "xp": 25, "newWords": [], "readingId": "r-t1"},
        {
            "id": "t1-nghe",
            "stage": 1,
            "topicId": 1,
            "title": "Nghe: Chào hỏi buổi sáng",
            "type": "nghe",
            "xp": 25,
            "newWords": t1_new,
            "listeningTracks": [
                {"id": "lt1-1", "speaker": "Linh", "voiceRole": "female", "hanzi": "早上好，老师！", "pinyin": "zǎo shang hǎo, lǎo shī!", "vi": "Chào buổi sáng thầy/cô!"},
                {"id": "lt1-2", "speaker": "Thầy Minh", "voiceRole": "formal", "hanzi": "你好！请坐。", "pinyin": "nǐ hǎo! qǐng zuò.", "vi": "Chào em! Mời ngồi."},
                {"id": "lt1-3", "speaker": "Linh", "voiceRole": "female", "hanzi": "谢谢老师！", "pinyin": "xiè xie lǎo shī!", "vi": "Em cảm ơn thầy/cô!"},
                {"id": "lt1-4", "speaker": "Thầy Minh", "voiceRole": "formal", "hanzi": "不客气，再见！", "pinyin": "bú kè qi, zài jiàn!", "vi": "Không có gì, tạm biệt!"},
            ],
            "exercises": [
                {
                    "id": "ng1-1",
                    "kind": "listen-meaning",
                    "promptVi": "Nghe câu và chọn nghĩa đúng",
                    "audioText": "早上好！",
                    "options": [
                        {"label": "Chào buổi sáng!", "value": "Chào buổi sáng!"},
                        {"label": "Chúc ngủ ngon!", "value": "Chúc ngủ ngon!"},
                        {"label": "Tạm biệt!", "value": "Tạm biệt!"},
                        {"label": "Xin lỗi!", "value": "Xin lỗi!"},
                    ],
                    "answer": "Chào buổi sáng!",
                },
                {
                    "id": "ng1-2",
                    "kind": "listen-hanzi",
                    "promptVi": "Nghe và chọn chữ Hán khớp với âm thanh",
                    "audioText": "谢谢你",
                    "options": [
                        {"label": "谢谢你", "value": "谢谢你"},
                        {"label": "对不起", "value": "对不起"},
                        {"label": "不客气", "value": "不客气"},
                        {"label": "没关系", "value": "没关系"},
                    ],
                    "answer": "谢谢你",
                },
                {
                    "id": "ng1-3",
                    "kind": "listen-tiles",
                    "promptVi": "Chạm vào các thẻ từ theo đúng thứ tự bạn nghe được",
                    "audioText": "老师早上好",
                    "tiles": ["好", "老师", "早上"],
                    "answer": "老师早上好",
                },
                {
                    "id": "ng1-4",
                    "kind": "listen-blank",
                    "promptVi": "Nghe và điền từ còn thiếu vào chỗ trống: 「不客气，___！」",
                    "audioText": "不客气，再见！",
                    "options": [
                        {"label": "再见", "value": "再见"},
                        {"label": "你好", "value": "你好"},
                        {"label": "请坐", "value": "请坐"},
                        {"label": "早上", "value": "早上"},
                    ],
                    "answer": "再见",
                },
                {
                    "id": "ng1-5",
                    "kind": "listen-dialogue",
                    "promptVi": "Nghe câu đáp lại: Người nói đã mời bạn làm gì?",
                    "audioText": "请进，请坐！",
                    "options": [
                        {"label": "Mời vào và mời ngồi", "value": "Mời vào và mời ngồi"},
                        {"label": "Hẹn gặp ngày mai", "value": "Hẹn gặp ngày mai"},
                        {"label": "Hỏi tên bạn", "value": "Hỏi tên bạn"},
                    ],
                    "answer": "Mời vào và mời ngồi",
                },
                {
                    "id": "ng1-6",
                    "kind": "dictation",
                    "promptVi": "Chép chính tả rút gọn: gõ pinyin (hoặc chữ Hán) của câu ngắn bạn nghe",
                    "audioText": "你好，再见！",
                    "tiles": ["你好", "再见"],
                    "answer": "nihao zaijian",
                },
            ],
        },
        {
            "id": "t1-viet",
            "stage": 1,
            "topicId": 1,
            "title": "Viết: Chữ chào hỏi căn bản",
            "type": "viet",
            "xp": 25,
            "newWords": t1_new,
            "writingChars": [
                {
                    "char": "你",
                    "pinyin": "nǐ",
                    "meaningVi": "bạn",
                    "radical": "亻",
                    "radicalNoteVi": "Bộ nhân đứng (亻) — hình dáng một người đứng nghiêng, xuất hiện ở nhiều chữ chỉ người như 他, 们.",
                    "lookalikes": [
                        {"hanzi": "你", "pinyin": "nǐ", "vi": "bạn"},
                        {"hanzi": "他", "pinyin": "tā", "vi": "anh ấy"},
                        {"hanzi": "们", "pinyin": "men", "vi": "các (số nhiều)"},
                        {"hanzi": "作", "pinyin": "zuò", "vi": "làm"},
                    ],
                },
                {
                    "char": "好",
                    "pinyin": "hǎo",
                    "meaningVi": "tốt, khỏe",
                    "radical": "女",
                    "radicalNoteVi": "Bộ nữ (女) ghép với bộ tử (子) — người mẹ bế con là hình ảnh tốt đẹp, an lành.",
                    "lookalikes": [
                        {"hanzi": "好", "pinyin": "hǎo", "vi": "tốt, khỏe"},
                        {"hanzi": "她", "pinyin": "tā", "vi": "cô ấy"},
                        {"hanzi": "妈", "pinyin": "mā", "vi": "mẹ"},
                        {"hanzi": "子", "pinyin": "zǐ", "vi": "con"},
                    ],
                },
                {
                    "char": "见",
                    "pinyin": "jiàn",
                    "meaningVi": "gặp, thấy",
                    "radical": "见",
                    "radicalNoteVi": "Bộ kiến (见) — con mắt (目) đặt trên đôi chân bước tới: nhìn thấy, gặp gỡ.",
                    "lookalikes": [
                        {"hanzi": "见", "pinyin": "jiàn", "vi": "gặp"},
                        {"hanzi": "贝", "pinyin": "bèi", "vi": "vỏ sò / tiền"},
                        {"hanzi": "风", "pinyin": "fēng", "vi": "gió"},
                        {"hanzi": "几", "pinyin": "jǐ", "vi": "mấy"},
                    ],
                },
            ],
        },

        # ---------------- TOPIC 6 ----------------
        {
            "id": "t6-giao-tiep",
            "stage": 1,
            "topicId": 6,
            "title": "Ăn uống: gọi món, trà sữa & cà phê",
            "type": "giao-tiep",
            "xp": 35,
            "newWords": t6_new,
            "patterns": [
                {
                    "id": "p-t6-1",
                    "frame": "我想喝一杯___。",
                    "pinyin": "wǒ xiǎng hē yì bēi ___.",
                    "meaningVi": "Mình muốn uống một ly [đồ uống].",
                    "exampleHanzi": "我想喝一杯冰奶茶。",
                    "examplePinyin": "wǒ xiǎng hē yì bēi bīng nǎi chá.",
                    "exampleVi": "Mình muốn uống một ly trà sữa đá.",
                    "slots": {
                        "promptVi": "Điền món để gọi 'một ly cà phê'",
                        "choices": [
                            {"hanzi": "咖啡", "pinyin": "kā fēi", "vi": "cà phê"},
                            {"hanzi": "菜单", "pinyin": "cài dān", "vi": "thực đơn"},
                            {"hanzi": "买单", "pinyin": "mǎi dān", "vi": "tính tiền"},
                        ],
                        "answerHanzi": "咖啡",
                    },
                },
                {
                    "id": "p-t6-2",
                    "frame": "这杯请给我___。",
                    "pinyin": "zhè bēi qǐng gěi wǒ ___.",
                    "meaningVi": "Ly này làm ơn cho mình [ít đường / không đá].",
                    "exampleHanzi": "这杯请给我少糖。",
                    "examplePinyin": "zhè bēi qǐng gěi wǒ shǎo táng.",
                    "exampleVi": "Ly này cho mình ít đường nhé.",
                    "slots": {
                        "promptVi": "Chọn yêu cầu 'ít đường'",
                        "choices": [
                            {"hanzi": "少糖", "pinyin": "shǎo táng", "vi": "ít đường"},
                            {"hanzi": "小笼包", "pinyin": "xiǎo lóng bāo", "vi": "tiểu long bao"},
                            {"hanzi": "老师", "pinyin": "lǎo shī", "vi": "giáo viên"},
                        ],
                        "answerHanzi": "少糖",
                    },
                },
            ],
            "dialogue": [
                {"speaker": "Nhân viên", "voiceRole": "female", "hanzi": "你好，请问要喝什么？", "pinyin": "nǐ hǎo, qǐng wèn yào hē shén me?", "vi": "Xin chào, bạn muốn uống gì ạ?", "mode": "npc", "goalLabel": "Vào quán"},
                {
                    "speaker": "Bao",
                    "voiceRole": "male",
                    "hanzi": "我想喝一杯奶茶。",
                    "pinyin": "wǒ xiǎng hē yì bēi nǎi chá.",
                    "vi": "Mình muốn uống một ly trà sữa.",
                    "mode": "choice",
                    "goalLabel": "Gọi trà sữa",
                    "choices": [
                        {"hanzi": "我想喝一杯奶茶。", "pinyin": "wǒ xiǎng hē yì bēi nǎi chá.", "vi": "Mình muốn uống một ly trà sữa.", "correct": True},
                        {"hanzi": "我想喝一杯菜单。", "pinyin": "wǒ xiǎng hē yì bēi cài dān.", "vi": "Mình muốn uống một ly thực đơn.", "correct": False},
                        {"hanzi": "再见，明天见。", "pinyin": "zài jiàn, míng tiān jiàn.", "vi": "Tạm biệt, hẹn mai gặp.", "correct": False},
                    ],
                },
                {"speaker": "Nhân viên", "voiceRole": "female", "hanzi": "好的，要少糖还是去冰？", "pinyin": "hǎo de, yào shǎo táng hái shi qù bīng?", "vi": "Vâng, bạn muốn ít đường hay không đá ạ?", "mode": "npc"},
                {
                    "speaker": "Bao",
                    "voiceRole": "male",
                    "hanzi": "少糖去冰，谢谢！",
                    "pinyin": "shǎo táng qù bīng, xiè xie!",
                    "vi": "Ít đường không đá, cảm ơn!",
                    "mode": "tiles",
                    "goalLabel": "Chọn ít đường & không đá",
                    "tilePrompt": ["少糖", "去冰", "谢谢"],
                },
                {"speaker": "Nhân viên", "voiceRole": "female", "hanzi": "一共二十块，请问买单吗？", "pinyin": "yí gòng èr shí kuài, qǐng wèn mǎi dān ma?", "vi": "Tổng cộng 20 tệ, bạn thanh toán luôn không ạ?", "mode": "npc"},
                {
                    "speaker": "Bao",
                    "voiceRole": "male",
                    "hanzi": "好的，买单！",
                    "pinyin": "hǎo de, mǎi dān!",
                    "vi": "Vâng, tính tiền ạ!",
                    "mode": "pinyin",
                    "goalLabel": "Tính tiền",
                    "acceptedPinyin": ["haode maidan", "hǎo de mǎi dān", "maidan", "mǎidān", "买单"],
                },
            ],
            "exercises": [
                {
                    "id": "ex-t6-1",
                    "kind": "meaning-choice",
                    "promptVi": "Khi muốn nói 'ít đường', bạn dùng từ nào?",
                    "hanziPrompt": "少糖",
                    "pinyinPrompt": "shǎo táng",
                    "options": [
                        {"label": "Ít đường", "value": "Ít đường"},
                        {"label": "Nhiều đá", "value": "Nhiều đá"},
                        {"label": "Tính tiền", "value": "Tính tiền"},
                        {"label": "Trà nóng", "value": "Trà nóng"},
                    ],
                    "answer": "Ít đường",
                },
                {
                    "id": "ex-t6-2",
                    "kind": "hanzi-choice",
                    "promptVi": "Nghe và chọn chữ Hán đúng cho 'cà phê'",
                    "audioText": "咖啡",
                    "options": [
                        {"label": "咖啡", "value": "咖啡"},
                        {"label": "奶茶", "value": "奶茶"},
                        {"label": "菜单", "value": "菜单"},
                        {"label": "买单", "value": "买单"},
                    ],
                    "answer": "咖啡",
                },
                {
                    "id": "ex-t6-3",
                    "kind": "sentence-tiles",
                    "promptVi": "Ghép câu: 'Mình muốn uống một ly trà sữa'",
                    "tiles": ["喝", "我想", "奶茶", "一杯"],
                    "answer": "我想喝一杯奶茶",
                },
            ],
            "roleplay": [
                {
                    "npcHanzi": "欢迎光临！请问您想喝点什么？",
                    "npcPinyin": "huān yíng guāng lín! qǐng wèn nín xiǎng hē diǎn shén me?",
                    "npcVi": "Chào mừng quý khách! Bạn muốn uống gì ạ?",
                    "promptVi": "Gọi một ly cà phê đá",
                    "options": [
                        {"hanzi": "我想喝一杯冰咖啡。", "pinyin": "wǒ xiǎng hē yì bēi bīng kā fēi.", "vi": "Mình muốn uống một ly cà phê đá.", "correct": True},
                        {"hanzi": "我是新同学。", "pinyin": "wǒ shì xīn tóng xué.", "vi": "Mình là bạn học mới.", "correct": False},
                        {"hanzi": "老师早上好。", "pinyin": "lǎo shī zǎo shang hǎo.", "vi": "Chào buổi sáng thầy cô.", "correct": False},
                    ],
                    "expectedHanzi": "我想喝一杯冰咖啡。",
                },
                {
                    "npcHanzi": "好的，需要少糖吗？",
                    "npcPinyin": "hǎo de, xū yào shǎo táng ma?",
                    "npcVi": "Vâng, có cần ít đường không ạ?",
                    "promptVi": "Xác nhận lấy ít đường",
                    "options": [
                        {"hanzi": "对，请给我少糖，谢谢。", "pinyin": "duì, qǐng gěi wǒ shǎo táng, xiè xie.", "vi": "Đúng rồi, cho mình ít đường, cảm ơn.", "correct": True},
                        {"hanzi": "不要咖啡，我要再见。", "pinyin": "bú yào kā fēi, wǒ yào zài jiàn.", "vi": "Không cần cà phê, mình cần tạm biệt.", "correct": False},
                        {"hanzi": "对不起。", "pinyin": "duì bu qǐ.", "vi": "Xin lỗi.", "correct": False},
                    ],
                    "expectedHanzi": "对，请给我少糖，谢谢。",
                },
                {
                    "npcHanzi": "您的咖啡好了，请慢用！",
                    "npcPinyin": "nín de kā fēi hǎo le, qǐng màn yòng!",
                    "npcVi": "Cà phê của bạn xong rồi, chúc ngon miệng!",
                    "promptVi": "Cảm ơn và hỏi tính tiền",
                    "options": [
                        {"hanzi": "谢谢！请问可以买单吗？", "pinyin": "xiè xie! qǐng wèn kě yǐ mǎi dān ma?", "vi": "Cảm ơn! Xin hỏi tính tiền được chưa ạ?", "correct": True},
                        {"hanzi": "不客气，请问你叫什么？", "pinyin": "bú kè qi, qǐng wèn nǐ jiào shén me?", "vi": "Không có gì, bạn tên gì?", "correct": False},
                        {"hanzi": "我不喝水。", "pinyin": "wǒ bù hē shuǐ.", "vi": "Mình không uống nước.", "correct": False},
                    ],
                    "expectedHanzi": "谢谢！请问可以买单吗？",
                },
            ],
        },
        {"id": "t6-doc", "stage": 1, "topicId": 6, "title": "Đọc: Buổi chiều ở quán trà sữa", "type": "doc", "xp": 30, "newWords": [], "readingId": "r-t6"},
        {
            "id": "t6-nghe",
            "stage": 1,
            "topicId": 6,
            "title": "Nghe: Gọi cà phê & trà sữa",
            "type": "nghe",
            "xp": 30,
            "newWords": t6_new,
            "listeningTracks": [
                {"id": "lt6-1", "speaker": "Bao", "voiceRole": "male", "hanzi": "你好，请问有菜单吗？", "pinyin": "nǐ hǎo, qǐng wèn yǒu cài dān ma?", "vi": "Xin chào, cho hỏi có thực đơn không?"},
                {"id": "lt6-2", "speaker": "Linh", "voiceRole": "female", "hanzi": "给你！你喝奶茶还是咖啡？", "pinyin": "gěi nǐ! nǐ hē nǎi chá hái shi kā fēi?", "vi": "Gửi bạn! Bạn uống trà sữa hay cà phê?"},
                {"id": "lt6-3", "speaker": "Bao", "voiceRole": "male", "hanzi": "我要一杯热奶茶，少糖。", "pinyin": "wǒ yào yì bēi rè nǎi chá, shǎo táng.", "vi": "Mình lấy một ly trà sữa nóng, ít đường."},
                {"id": "lt6-4", "speaker": "Linh", "voiceRole": "female", "hanzi": "这家的奶茶很好喝，小笼包也好吃。", "pinyin": "zhè jiā de nǎi chá hěn hǎo hē, xiǎo lóng bāo yě hǎo chī.", "vi": "Trà sữa quán này ngon lắm, tiểu long bao cũng ngon nữa."},
            ],
            "exercises": [
                {
                    "id": "ng6-1",
                    "kind": "listen-meaning",
                    "promptVi": "Nghe và chọn đồ uống người nói muốn gọi",
                    "audioText": "我想喝一杯冰咖啡。",
                    "options": [
                        {"label": "Một ly cà phê đá", "value": "Một ly cà phê đá"},
                        {"label": "Một ly trà nóng", "value": "Một ly trà nóng"},
                        {"label": "Hai ly trà sữa", "value": "Hai ly trà sữa"},
                        {"label": "Một đĩa mì sợi", "value": "Một đĩa mì sợi"},
                    ],
                    "answer": "Một ly cà phê đá",
                },
                {
                    "id": "ng6-2",
                    "kind": "listen-hanzi",
                    "promptVi": "Nghe và chọn cụm chữ Hán đúng",
                    "audioText": "少糖去冰",
                    "options": [
                        {"label": "少糖去冰", "value": "少糖去冰"},
                        {"label": "热茶买单", "value": "热茶买单"},
                        {"label": "咖啡好吃", "value": "咖啡好吃"},
                        {"label": "菜单谢谢", "value": "菜单谢谢"},
                    ],
                    "answer": "少糖去冰",
                },
                {
                    "id": "ng6-3",
                    "kind": "listen-tiles",
                    "promptVi": "Nghe audio và chạm ghép đúng thứ tự thẻ từ",
                    "audioText": "我要一杯热茶",
                    "tiles": ["茶", "热", "我要", "一杯"],
                    "answer": "我要一杯热茶",
                },
                {
                    "id": "ng6-4",
                    "kind": "listen-blank",
                    "promptVi": "Nghe và điền từ còn thiếu: 「这家店的奶茶很___！」",
                    "audioText": "这家店的奶茶很好喝！",
                    "options": [
                        {"label": "好喝", "value": "好喝"},
                        {"label": "好吃", "value": "好吃"},
                        {"label": "买单", "value": "买单"},
                        {"label": "少糖", "value": "少糖"},
                    ],
                    "answer": "好喝",
                },
                {
                    "id": "ng6-5",
                    "kind": "listen-dialogue",
                    "promptVi": "Nghe hội thoại: Khách muốn thanh toán câu nào?",
                    "audioText": "服务员，请帮我买单！",
                    "options": [
                        {"label": "Gọi phục vụ tính tiền", "value": "Gọi phục vụ tính tiền"},
                        {"label": "Xin thêm đá lạnh", "value": "Xin thêm đá lạnh"},
                        {"label": "Hỏi đường ra quán", "value": "Hỏi đường ra quán"},
                    ],
                    "answer": "Gọi phục vụ tính tiền",
                },
                {
                    "id": "ng6-6",
                    "kind": "dictation",
                    "promptVi": "Chép chính tả rút gọn: gõ pinyin (hoặc chọn thẻ) câu vừa nghe",
                    "audioText": "谢谢，买单！",
                    "tiles": ["谢谢", "买单"],
                    "answer": "xiexie maidan",
                },
            ],
        },
        {
            "id": "t6-viet",
            "stage": 1,
            "topicId": 6,
            "title": "Viết: Bộ khẩu & đồ uống",
            "type": "viet",
            "xp": 30,
            "newWords": t6_new,
            "writingChars": [
                {
                    "char": "喝",
                    "pinyin": "hē",
                    "meaningVi": "uống",
                    "radical": "口",
                    "radicalNoteVi": "Bộ khẩu (口) nằm bên trái như cái miệng — hầu hết chữ liên quan đến ăn, uống, nói đều mang bộ 口 (喝, 吃, 咖啡).",
                    "lookalikes": [
                        {"hanzi": "喝", "pinyin": "hē", "vi": "uống"},
                        {"hanzi": "渴", "pinyin": "kě", "vi": "khát"},
                        {"hanzi": "吃", "pinyin": "chī", "vi": "ăn"},
                        {"hanzi": "叫", "pinyin": "jiào", "vi": "gọi"},
                    ],
                },
                {
                    "char": "茶",
                    "pinyin": "chá",
                    "meaningVi": "trà",
                    "radical": "艹",
                    "radicalNoteVi": "Bộ thảo đầu (艹) ở trên tượng trưng hai ngọn cỏ non — gợi nhắc trà làm từ lá cây tự nhiên.",
                    "lookalikes": [
                        {"hanzi": "茶", "pinyin": "chá", "vi": "trà"},
                        {"hanzi": "菜", "pinyin": "cài", "vi": "món ăn / rau"},
                        {"hanzi": "花", "pinyin": "huā", "vi": "hoa"},
                        {"hanzi": "草", "pinyin": "cǎo", "vi": "cỏ"},
                    ],
                },
                {
                    "char": "杯",
                    "pinyin": "bēi",
                    "meaningVi": "cốc, ly",
                    "radical": "木",
                    "radicalNoteVi": "Bộ mộc (木) bên trái — chiếc cốc thuở xưa được tiện từ gỗ.",
                    "lookalikes": [
                        {"hanzi": "杯", "pinyin": "bēi", "vi": "cốc, ly"},
                        {"hanzi": "果", "pinyin": "guǒ", "vi": "quả"},
                        {"hanzi": "桌", "pinyin": "zhuō", "vi": "cái bàn"},
                        {"hanzi": "不", "pinyin": "bù", "vi": "không"},
                    ],
                },
            ],
        },
    ]

    readings = [
        {
            "id": "r-t1",
            "stage": 1,
            "topicId": 1,
            "title": "Ngày đầu ở lớp tiếng Trung",
            "mode": "fluent",
            "knownPercent": 96,
            "newWords": ["早上", "同学"],
            "paragraphs": [
                {
                    "hanzi": "今天早上，我和朋友去学中文。老师说：「你们好！我叫王老师。」",
                    "vi": "Sáng nay, mình và bạn đi học tiếng Trung. Thầy/cô nói: 'Chào các em! Cô là cô Vương.'",
                    "tokens": [
                        {"w": "今天", "pinyin": "jīn tiān"},
                        {"w": "早上", "pinyin": "zǎo shang", "isNew": True},
                        {"w": "，", "pinyin": ""},
                        {"w": "我", "pinyin": "wǒ"},
                        {"w": "和", "pinyin": "hé"},
                        {"w": "朋友", "pinyin": "péng you"},
                        {"w": "去", "pinyin": "qù"},
                        {"w": "学", "pinyin": "xué"},
                        {"w": "中文", "pinyin": "zhōng wén"},
                        {"w": "。", "pinyin": ""},
                        {"w": "老师", "pinyin": "lǎo shī"},
                        {"w": "说", "pinyin": "shuō"},
                        {"w": "：「", "pinyin": ""},
                        {"w": "你们", "pinyin": "nǐ men"},
                        {"w": "好", "pinyin": "hǎo"},
                        {"w": "！", "pinyin": ""},
                        {"w": "我", "pinyin": "wǒ"},
                        {"w": "叫", "pinyin": "jiào"},
                        {"w": "王", "pinyin": "Wáng"},
                        {"w": "老师", "pinyin": "lǎo shī"},
                        {"w": "。」", "pinyin": ""},
                    ],
                },
                {
                    "hanzi": "我说：「老师好！我是越南人。」新同学说：「你好，请坐！」我说谢谢，同学说不客气。",
                    "vi": "Mình nói: 'Em chào cô ạ! Em là người Việt Nam.' Bạn học mới nói: 'Xin chào, mời ngồi!' Mình nói cảm ơn, bạn ấy đáp không có gì.",
                    "tokens": [
                        {"w": "我", "pinyin": "wǒ"},
                        {"w": "说", "pinyin": "shuō"},
                        {"w": "：「", "pinyin": ""},
                        {"w": "老师", "pinyin": "lǎo shī"},
                        {"w": "好", "pinyin": "hǎo"},
                        {"w": "！", "pinyin": ""},
                        {"w": "我", "pinyin": "wǒ"},
                        {"w": "是", "pinyin": "shì"},
                        {"w": "越南", "pinyin": "Yuè nán"},
                        {"w": "人", "pinyin": "rén"},
                        {"w": "。」", "pinyin": ""},
                        {"w": "新", "pinyin": "xīn"},
                        {"w": "同学", "pinyin": "tóng xué", "isNew": True},
                        {"w": "说", "pinyin": "shuō"},
                        {"w": "：「", "pinyin": ""},
                        {"w": "你好", "pinyin": "nǐ hǎo"},
                        {"w": "，", "pinyin": ""},
                        {"w": "请", "pinyin": "qǐng"},
                        {"w": "坐", "pinyin": "zuò"},
                        {"w": "！」", "pinyin": ""},
                        {"w": "我", "pinyin": "wǒ"},
                        {"w": "说", "pinyin": "shuō"},
                        {"w": "谢谢", "pinyin": "xiè xie"},
                        {"w": "，", "pinyin": ""},
                        {"w": "同学", "pinyin": "tóng xué", "isNew": True},
                        {"w": "说", "pinyin": "shuō"},
                        {"w": "不客气", "pinyin": "bú kè qi"},
                        {"w": "。", "pinyin": ""},
                    ],
                },
                {
                    "hanzi": "早上课后，我们都很开心。我说：「老师再见，同学明天见！」",
                    "vi": "Sau buổi học sáng, chúng mình đều rất vui. Mình nói: 'Em chào cô tạm biệt, các bạn hẹn mai gặp!'",
                    "tokens": [
                        {"w": "早上", "pinyin": "zǎo shang", "isNew": True},
                        {"w": "课", "pinyin": "kè"},
                        {"w": "后", "pinyin": "hòu"},
                        {"w": "，", "pinyin": ""},
                        {"w": "我们", "pinyin": "wǒ men"},
                        {"w": "都", "pinyin": "dōu"},
                        {"w": "很", "pinyin": "hěn"},
                        {"w": "开心", "pinyin": "kāi xīn"},
                        {"w": "。", "pinyin": ""},
                        {"w": "我", "pinyin": "wǒ"},
                        {"w": "说", "pinyin": "shuō"},
                        {"w": "：「", "pinyin": ""},
                        {"w": "老师", "pinyin": "lǎo shī"},
                        {"w": "再见", "pinyin": "zài jiàn"},
                        {"w": "，", "pinyin": ""},
                        {"w": "同学", "pinyin": "tóng xué", "isNew": True},
                        {"w": "明天", "pinyin": "míng tiān"},
                        {"w": "见", "pinyin": "jiàn"},
                        {"w": "！」", "pinyin": ""},
                    ],
                },
            ],
            "questions": [
                {"id": "rq1-1", "type": "mcq", "q": "Nhân vật chính đi học tiếng Trung vào lúc nào?", "options": ["Buổi sáng", "Buổi tối", "Ngày mai"], "answer": 0, "explainVi": "Đoạn 1 ghi rõ 「今天早上」 (sáng nay)."},
                {"id": "rq1-2", "type": "tf", "q": "Đúng hay Sai: Bạn học mới nói '不客气' khi nhân vật chính cảm ơn.", "options": ["Đúng", "Sai"], "answer": 0, "explainVi": "Đoạn 2: 「我说谢谢，同学说不客气。」"},
                {"id": "rq1-3", "type": "detail", "q": "Cuối buổi học, nhân vật chính hẹn gặp bạn học khi nào?", "options": ["Ngày mai (明天见)", "Buổi tối", "Tuần sau"], "answer": 0, "explainVi": "Câu cuối bài: 「同学明天见！」"},
            ],
        },
        {
            "id": "r-t6",
            "stage": 1,
            "topicId": 6,
            "title": "Buổi chiều ở quán trà sữa",
            "mode": "study",
            "knownPercent": 90,
            "newWords": ["奶茶", "少糖", "去冰", "买单"],
            "paragraphs": [
                {
                    "hanzi": "今天下午，我和好朋友去一家新店。这里有很多茶，还有冰咖啡和奶茶。",
                    "vi": "Chiều nay, mình và bạn thân đến một quán mới. Ở đây có rất nhiều loại trà, còn có cà phê đá và trà sữa.",
                    "tokens": [
                        {"w": "今天", "pinyin": "jīn tiān"},
                        {"w": "下午", "pinyin": "xià wǔ"},
                        {"w": "，", "pinyin": ""},
                        {"w": "我", "pinyin": "wǒ"},
                        {"w": "和", "pinyin": "hé"},
                        {"w": "好", "pinyin": "hǎo"},
                        {"w": "朋友", "pinyin": "péng you"},
                        {"w": "去", "pinyin": "qù"},
                        {"w": "一家", "pinyin": "yì jiā"},
                        {"w": "新", "pinyin": "xīn"},
                        {"w": "店", "pinyin": "diàn"},
                        {"w": "。", "pinyin": ""},
                        {"w": "这里", "pinyin": "zhè lǐ"},
                        {"w": "有", "pinyin": "yǒu"},
                        {"w": "很", "pinyin": "hěn"},
                        {"w": "多", "pinyin": "duō"},
                        {"w": "茶", "pinyin": "chá"},
                        {"w": "，", "pinyin": ""},
                        {"w": "还有", "pinyin": "hái yǒu"},
                        {"w": "冰", "pinyin": "bīng"},
                        {"w": "咖啡", "pinyin": "kā fēi"},
                        {"w": "和", "pinyin": "hé"},
                        {"w": "奶茶", "pinyin": "nǎi chá", "isNew": True},
                        {"w": "。", "pinyin": ""},
                    ],
                },
                {
                    "hanzi": "服务员问我想喝什么。我想喝一杯热奶茶，少糖去冰。朋友要一杯冰咖啡，也少糖去冰。",
                    "vi": "Nhân viên phục vụ hỏi mình muốn uống gì. Mình muốn một ly trà sữa nóng, ít đường không đá. Bạn mình gọi một ly cà phê đá, cũng ít đường không đá.",
                    "tokens": [
                        {"w": "服务员", "pinyin": "fú wù yuán"},
                        {"w": "问", "pinyin": "wèn"},
                        {"w": "我", "pinyin": "wǒ"},
                        {"w": "想", "pinyin": "xiǎng"},
                        {"w": "喝", "pinyin": "hē"},
                        {"w": "什么", "pinyin": "shén me"},
                        {"w": "。", "pinyin": ""},
                        {"w": "我", "pinyin": "wǒ"},
                        {"w": "想", "pinyin": "xiǎng"},
                        {"w": "喝", "pinyin": "hē"},
                        {"w": "一杯", "pinyin": "yì bēi"},
                        {"w": "热", "pinyin": "rè"},
                        {"w": "奶茶", "pinyin": "nǎi chá", "isNew": True},
                        {"w": "，", "pinyin": ""},
                        {"w": "少糖", "pinyin": "shǎo táng", "isNew": True},
                        {"w": "去冰", "pinyin": "qù bīng", "isNew": True},
                        {"w": "。", "pinyin": ""},
                        {"w": "朋友", "pinyin": "péng you"},
                        {"w": "要", "pinyin": "yào"},
                        {"w": "一杯", "pinyin": "yì bēi"},
                        {"w": "冰", "pinyin": "bīng"},
                        {"w": "咖啡", "pinyin": "kā fēi"},
                        {"w": "，", "pinyin": ""},
                        {"w": "也", "pinyin": "yě"},
                        {"w": "少糖", "pinyin": "shǎo táng", "isNew": True},
                        {"w": "去冰", "pinyin": "qù bīng", "isNew": True},
                        {"w": "。", "pinyin": ""},
                    ],
                },
                {
                    "hanzi": "我们还点了小笼包。奶茶很好喝，小笼包也好吃！最后我说：「请买单！」服务员说一共四十块，谢谢再来，我先去买单了。",
                    "vi": "Chúng mình còn gọi tiểu long bao. Trà sữa rất ngon, tiểu long bao cũng ngon! Cuối cùng mình nói: 'Tính tiền ạ!' Nhân viên nói tổng cộng 40 tệ, cảm ơn lần sau ghé nhé, mình đi thanh toán trước đây.",
                    "tokens": [
                        {"w": "我们", "pinyin": "wǒ men"},
                        {"w": "还", "pinyin": "hái"},
                        {"w": "点", "pinyin": "diǎn"},
                        {"w": "了", "pinyin": "le"},
                        {"w": "小笼包", "pinyin": "xiǎo lóng bāo"},
                        {"w": "。", "pinyin": ""},
                        {"w": "奶茶", "pinyin": "nǎi chá", "isNew": True},
                        {"w": "很", "pinyin": "hěn"},
                        {"w": "好喝", "pinyin": "hǎo hē"},
                        {"w": "，", "pinyin": ""},
                        {"w": "小笼包", "pinyin": "xiǎo lóng bāo"},
                        {"w": "也", "pinyin": "yě"},
                        {"w": "好吃", "pinyin": "hǎo chī"},
                        {"w": "！", "pinyin": ""},
                        {"w": "最后", "pinyin": "zuì hòu"},
                        {"w": "我", "pinyin": "wǒ"},
                        {"w": "说", "pinyin": "shuō"},
                        {"w": "：「", "pinyin": ""},
                        {"w": "请", "pinyin": "qǐng"},
                        {"w": "买单", "pinyin": "mǎi dān", "isNew": True},
                        {"w": "！」", "pinyin": ""},
                        {"w": "服务员", "pinyin": "fú wù yuán"},
                        {"w": "说", "pinyin": "shuō"},
                        {"w": "一共", "pinyin": "yí gòng"},
                        {"w": "四十", "pinyin": "sì shí"},
                        {"w": "块", "pinyin": "kuài"},
                        {"w": "，", "pinyin": ""},
                        {"w": "谢谢", "pinyin": "xiè xie"},
                        {"w": "再", "pinyin": "zài"},
                        {"w": "来", "pinyin": "lái"},
                        {"w": "，", "pinyin": ""},
                        {"w": "我", "pinyin": "wǒ"},
                        {"w": "先", "pinyin": "xiān"},
                        {"w": "去", "pinyin": "qù"},
                        {"w": "买单", "pinyin": "mǎi dān", "isNew": True},
                        {"w": "了", "pinyin": "le"},
                        {"w": "。", "pinyin": ""},
                    ],
                },
            ],
            "questions": [
                {"id": "rq6-1", "type": "mcq", "q": "Nhân vật 'tôi' đã gọi ly đồ uống nào?", "options": ["Trà sữa nóng, ít đường không đá", "Cà phê đá, nhiều đường", "Trà đá miễn phí"], "answer": 0, "explainVi": "Đoạn 2: 「我想喝一杯热奶茶，少糖去冰。」"},
                {"id": "rq6-2", "type": "mcq", "q": "Ngoài đồ uống, hai bạn còn gọi thêm món ăn nào?", "options": ["Tiểu long bao (小笼包)", "Mì sợi (面条)", "Bánh bao chay"], "answer": 0, "explainVi": "Đoạn 3: 「我们还点了小笼包。」"},
                {"id": "rq6-3", "type": "tf", "q": "Đúng hay Sai: Tổng hóa đơn là 40 tệ.", "options": ["Đúng", "Sai"], "answer": 0, "explainVi": "Nhân viên nói 「一共四十块」."},
                {"id": "rq6-4", "type": "detail", "q": "Chữ nào trong bài có nghĩa là 'tính tiền'?", "options": ["买单", "好喝", "菜单"], "answer": 0, "explainVi": "买单 (mǎi dān) = tính tiền / thanh toán."},
            ],
        },
    ]

    return lessons, readings


def verify_all_content(words: list[dict], lessons: list[dict], readings: list[dict]) -> None:
    pool_list = json.loads((CACHE_DIR / "hsk_1_3_pool.json").read_text(encoding="utf-8"))
    allowed = {w["hanzi"] for w in words} | {"王", "还"}
    dictionary = allowed | {item["hanzi"] for item in pool_list}

    passed_count = 0
    failed_count = 0

    for lesson in lessons:
        if lesson["type"] == "giao-tiep":
            txt = "".join(t["hanzi"] for t in lesson.get("dialogue", []))
            res = check_level(txt, allowed, set(), dictionary, max_unknown_ratio=0.10)
            if not res.passed:
                failed_count += 1
                raise RuntimeError(f"Level check failed for {lesson['id']}: {res}")
            passed_count += 1
        elif lesson["type"] == "nghe":
            txt = "".join(t["hanzi"] for t in lesson.get("listeningTracks", []))
            res = check_level(txt, allowed, set(), dictionary, max_unknown_ratio=0.10)
            if not res.passed:
                failed_count += 1
                raise RuntimeError(f"Level check failed for {lesson['id']}: {res}")
            passed_count += 1

    for reading in readings:
        txt = "".join(p["hanzi"] for p in reading["paragraphs"])
        glossed = set(reading["newWords"])
        res = check_level(
            txt,
            allowed - glossed,
            glossed,
            dictionary,
            max_unknown_ratio=0.18,
            min_new_occurrences=2,
        )
        if not res.passed:
            failed_count += 1
            raise RuntimeError(f"Level check failed for reading {reading['id']}: {res}")
        passed_count += 1

    print(f"Level check summary: {passed_count} passed, {failed_count} rejected (100% pass)")


def main() -> None:
    STAGE1_DIR.mkdir(parents=True, exist_ok=True)
    words, word_stats = build_words()
    lessons, readings = build_lessons_and_readings(words)
    verify_all_content(words, lessons, readings)

    (CONTENT_DIR / "curriculum.json").write_text(json.dumps(CURRICULUM, ensure_ascii=False, indent=2), encoding="utf-8")
    (STAGE1_DIR / "words.json").write_text(json.dumps(words, ensure_ascii=False, indent=2), encoding="utf-8")
    (STAGE1_DIR / "lessons.json").write_text(json.dumps(lessons, ensure_ascii=False, indent=2), encoding="utf-8")
    (STAGE1_DIR / "readings.json").write_text(json.dumps(readings, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        f"Stage 1 built: words={word_stats['words']} (tatoeba_cmn_vie={word_stats['tatoeba_matched']}), "
        f"lessons={len(lessons)}, readings={len(readings)}"
    )


if __name__ == "__main__":
    main()
