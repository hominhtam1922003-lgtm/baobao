"""Master pipeline: build 4-stage curriculum (28 topics x 4 skills, 4 story chapters, 4 stage tests) with level checking."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
from pathlib import Path
import re
import sys
import threading
import time
from typing import Any
from pypinyin import pinyin as to_pinyin, Style

from generate_content import (
    TopicCommOut,
    TopicListeningOut,
    TopicReadingOut,
    StoryChapterOut,
    StageTestOut,
    generate_radical_notes_batch,
    generate_stage_test_items,
    generate_story_chapter,
    generate_topic_comm,
    generate_topic_listening,
    generate_topic_reading,
    translate_tatoeba_en_batch,
    _call_structured,
)
from level_checker import check_level, segment_chinese
from prepare_stage1 import load_cedict
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data-src"
CONTENT_DIR = ROOT / "content"
CACHE_DIR = ROOT / "tools" / ".cache"
GEN_CACHE_DIR = CACHE_DIR / "generated_topics"
HW_DATA_DIR = ROOT / "node_modules" / "hanzi-writer-data"

CJK_RUN_RE = re.compile(r"([\u4e00-\u9fff]+)")
CJK_ONLY_RE = re.compile(r"^[\u4e00-\u9fff]+$")

PROPER_PROUNS = {"越南", "中国", "北京", "上海", "汉语", "中文"}

# Explicit tone-sandhi / modern standard pinyin preferences where complete.json forms[0] had archaic/surname readings
PINYIN_OVERRIDES = {
    "谢谢": "xiè xie",
    "不客气": "bú kè qi",
    "早上": "zǎo shang",
    "晚上": "wǎn shang",
    "没关系": "méi guān xi",
    "对不起": "duì bu qǐ",
    "还是": "hái shi",
    "名字": "míng zi",
    "谁": "shéi",
    "朋友": "péng you",
    "喜欢": "xǐ huan",
    "便宜": "pián yi",
    "吗": "ma",
    "呢": "ne",
    "吧": "ba",
    "啊": "a",
    "个": "gè",
    "说": "shuō",
    "听": "tīng",
    "读": "dú",
    "看": "kàn",
    "要": "yào",
    "都": "dōu",
    "还": "hái",
    "那": "nà",
    "几": "jǐ",
    "长": "cháng",
    "行": "xíng",
    "得": "de",
    "着": "zhe",
    "地": "dì",
    "张": "zhāng",
    "米": "mǐ",
    "句": "jù",
    "万": "wàn",
    "过": "guò",
    "打": "dǎ",
    "上": "shàng",
    "号": "hào",
    "喂": "wèi",
    "只": "zhǐ",
    "觉": "jué",
    "乐": "lè",
    "重": "zhòng",
    "假": "jiǎ",
    "和": "hé",
    "为": "wèi",
    "中": "zhōng",
    "干": "gàn",
    "发": "fā",
    "当": "dāng",
    "种": "zhǒng",
    "好": "hǎo",
    "少": "shǎo",
    "多少": "duō shao",
    "怎么": "zěn me",
    "什么": "shén me",
    "东西": "dōng xi",
    "知道": "zhī dào",
    "时候": "shí hou",
    "起来": "qǐ lai",
    "那里": "nà lǐ",
    "这里": "zhè lǐ",
}

STAGES_META = [
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
            {
                "title": "Hỏi vị trí với 在哪儿 / 在哪里",
                "pattern": "Danh từ + 在哪里 / 在哪儿？",
                "explainVi": "Dùng để hỏi đường tới nhà ga, cửa hàng hoặc hỏi người thân đang ở đâu.",
                "exampleHanzi": "请问，地铁站在哪里？",
                "exampleVi": "Xin hỏi, ga tàu điện ngầm ở đâu ạ?",
            },
        ],
        "storyChapter": {
            "title": "Chương 1: Ngày đầu Bao tới phố cổ",
            "teaserVi": "Bao lần đầu tự đi phố cổ làm quen bạn mới và gọi ly trà sữa đúng gu — cậu sẽ xoay xở ra sao?",
            "readingId": "story-c1",
        },
        "stageTestId": "stage-1-test",
    },
    {
        "id": 2,
        "title": "Chặng 2 — Đời sống",
        "subtitle": "Sở thích, thời tiết, công việc, nhà ở và mua sắm online",
        "colorToken": "read",
        "grammarNotes": [
            {
                "title": "So sánh hơn với 比 (bǐ)",
                "pattern": "A + 比 + B + Tính từ",
                "explainVi": "Đặt 比 giữa hai đối tượng để so sánh (nóng hơn, đắt hơn, nhanh hơn).",
                "exampleHanzi": "今天比昨天热得多。",
                "exampleVi": "Hôm nay nóng hơn hôm qua nhiều.",
            },
            {
                "title": "Nhấn mạnh cặp tương phản 虽然……但是……",
                "pattern": "虽然 + Vế 1，但是 + Vế 2",
                "explainVi": "Nghĩa là 'Tuy... nhưng...' dùng để diễn tả hai ý trái ngược tự nhiên.",
                "exampleHanzi": "虽然有点儿累，但是我很开心。",
                "exampleVi": "Tuy hơi mệt một chút nhưng mình rất vui.",
            },
            {
                "title": "Diễn tả hành động đang diễn ra với 正在 / 着",
                "pattern": "Chủ ngữ + 正在 + Động từ / Động từ + 着",
                "explainVi": "正在 nhấn mạnh đang làm gì lúc này; 着 gắn sau động từ chỉ trạng thái duy trì.",
                "exampleHanzi": "外面正在下着小雨。",
                "exampleVi": "Bên ngoài trời đang mưa nhỏ.",
            },
        ],
        "storyChapter": {
            "title": "Chương 2: Căn phòng mới của Bao",
            "teaserVi": "Bao chuyển vào phòng trọ mới, tự đặt đồ online và trải qua cơn mưa đầu mùa cùng hàng xóm mới.",
            "readingId": "story-c2",
        },
        "stageTestId": "stage-2-test",
    },
    {
        "id": 3,
        "title": "Chặng 3 — Xã hội & giải trí",
        "subtitle": "Kết bạn, hẹn đi chơi, phim nhạc, du lịch và lễ tết",
        "colorToken": "review",
        "grammarNotes": [
            {
                "title": "Trải nghiệm đã từng với 过 (guo)",
                "pattern": "Chủ ngữ + Động từ + 过 + Tân ngữ",
                "explainVi": "Đặt 过 ngay sau động từ để nói mình từng trải nghiệm một món ăn, bộ phim hay chuyến đi.",
                "exampleHanzi": "我看过这部中国电影。",
                "exampleVi": "Mình đã từng xem bộ phim Trung Quốc này rồi.",
            },
            {
                "title": "Mức độ ngày càng tăng với 越来越",
                "pattern": "Chủ ngữ + 越来越 + Tính từ / Động từ tâm lý",
                "explainVi": "Diễn tả sự thay đổi tăng tiến theo thời gian ('ngày càng...').",
                "exampleHanzi": "我们的关系越来越好了。",
                "exampleVi": "Mối quan hệ của chúng mình ngày càng tốt hơn.",
            },
            {
                "title": "Ngoại trừ / Ngoài ra với 除了……以外",
                "pattern": "除了 + A + 以外，……都 / 还……",
                "explainVi": "Dùng kèm 都 để loại trừ A, hoặc kèm 还 để bổ sung thêm ý ngoài A.",
                "exampleHanzi": "除了唱歌以外，他还喜欢踢足球。",
                "exampleVi": "Ngoài ca hát ra, bạn ấy còn thích đá bóng nữa.",
            },
        ],
        "storyChapter": {
            "title": "Chương 3: Chuyến tàu cuối tuần",
            "teaserVi": "Nhóm bạn rủ Bao bắt chuyến tàu sớm đi du lịch cuối tuần và đón lễ hội đèn lồng rực rỡ.",
            "readingId": "story-c3",
        },
        "stageTestId": "stage-3-test",
    },
    {
        "id": 4,
        "title": "Chặng 4 — Tự tin giao tiếp",
        "subtitle": "Bày tỏ quan điểm, dự định tương lai, công nghệ & tình huống khó",
        "colorToken": "write",
        "grammarNotes": [
            {
                "title": "Câu chữ 把 (bǎ) nhấn mạnh tác động",
                "pattern": "Chủ ngữ + 把 + Tân ngữ + Động từ + Bổ ngữ",
                "explainVi": "Đưa đối tượng chịu tác động lên trước động từ để nêu rõ kết quả xử lý sự việc.",
                "exampleHanzi": "请把你的问题写下来。",
                "exampleVi": "Xin hãy viết vấn đề của bạn xuống giấy.",
            },
            {
                "title": "Nêu quan điểm nhẹ nhàng với 在我看来 / 我认为",
                "pattern": "我认为 / 对我来说 + Mệnh đề",
                "explainVi": "Giúp bày tỏ ý kiến cá nhân lịch sự khi thảo luận công việc hay đời sống.",
                "exampleHanzi": "我认为这个办法既简单又安全。",
                "exampleVi": "Mình cho rằng cách này vừa đơn giản vừa an toàn.",
            },
            {
                "title": "Điều kiện & mục đích với 只要……就…… / 为了",
                "pattern": "只要 + Điều kiện + 就 + Kết quả",
                "explainVi": "只要...就... = 'Chỉ cần... thì...'; 为了... = 'Vì để...' giúp câu lập luận mạch lạc.",
                "exampleHanzi": "只要坚持练习，就一定能做到。",
                "exampleVi": "Chỉ cần kiên trì luyện tập thì nhất định làm được.",
            },
        ],
        "storyChapter": {
            "title": "Chương 4: Hội chợ mùa thu",
            "teaserVi": "Ngày hội lớn cuối hành trình: Bao tự tin thuyết trình ý tưởng và giúp khách xử lý sự cố bất ngờ.",
            "readingId": "story-c4",
        },
        "stageTestId": "stage-4-test",
    },
]

TOPICS_SPEC = [
    # Stage 1 (8 topics; T1 and T6 preserved from DOT 1)
    {"id": 1, "stage": 1, "title": "Chào hỏi & tạm biệt", "subtitle": "Làm quen, cảm ơn, xin lỗi tự nhiên", "seeds": ["你好", "早上", "谢谢", "不客气", "再见"], "preserve": True},
    {"id": 2, "stage": 1, "title": "Giới thiệu bản thân", "subtitle": "Tên tuổi, quốc tịch và bạn mới", "seeds": ["叫", "名字", "越南", "中国", "同学", "认识"]},
    {"id": 3, "stage": 1, "title": "Số đếm, tuổi & ngày tháng", "subtitle": "Đếm số, hỏi tuổi, ngày sinh nhật", "seeds": ["岁", "年", "月", "号", "生日", "今年"]},
    {"id": 4, "stage": 1, "title": "Gia đình & bạn bè", "subtitle": "Kể về người thân và bạn thân", "seeds": ["家", "爸爸", "妈妈", "哥哥", "姐姐", "朋友"]},
    {"id": 5, "stage": 1, "title": "Thời gian & hẹn gặp", "subtitle": "Hỏi giờ và đặt lịch gặp mặt", "seeds": ["今天", "明天", "现在", "点", "分钟", "时间"]},
    {"id": 6, "stage": 1, "title": "Ăn uống: gọi món, trà sữa & cà phê", "subtitle": "Xem thực đơn, chọn ít đường/đá, tính tiền", "seeds": ["喝", "奶茶", "咖啡", "杯", "少糖", "买单"], "preserve": True},
    {"id": 7, "stage": 1, "title": "Mua sắm & mặc cả", "subtitle": "Hỏi giá, chọn món và trả giá nhẹ", "seeds": ["买", "东西", "钱", "块", "多少", "便宜"]},
    {"id": 8, "stage": 1, "title": "Hỏi đường & đi lại", "subtitle": "Chỉ hướng, ga tàu và bắt xe", "seeds": ["去", "路", "车站", "左边", "右边", "走"]},
    # Stage 2 (8 topics)
    {"id": 9, "stage": 2, "title": "Sở thích & thời gian rảnh", "subtitle": "Nghe nhạc, đọc sách, vận động cuối tuần", "seeds": ["跳舞", "画", "运动", "球", "公园", "周末"]},
    {"id": 10, "stage": 2, "title": "Thời tiết & mùa", "subtitle": "Nắng mưa, nóng lạnh và bốn mùa", "seeds": ["风", "春天", "夏天", "秋天", "冬天", "公园"]},
    {"id": 11, "stage": 2, "title": "Trường học & học tập", "subtitle": "Lớp học, bài tập, kỳ thi", "seeds": ["教室", "题", "懂", "准备", "考试", "教"]},
    {"id": 12, "stage": 2, "title": "Công việc & nghề nghiệp", "subtitle": "Công ty, đồng nghiệp và giờ làm", "seeds": ["同事", "准备", "希望", "事情", "帮", "完"]},
    {"id": 13, "stage": 2, "title": "Sức khỏe: đi khám, mua thuốc", "subtitle": "Hỏi thăm khi ốm, khám bác sĩ", "seeds": ["身体", "疼", "药", "累", "洗", "床"]},
    {"id": 14, "stage": 2, "title": "Nhà ở: thuê nhà, hỏi tiện nghi", "subtitle": "Tìm phòng trọ, bàn ghế và phòng tắm", "seeds": ["楼", "门", "床", "空调", "里面", "外面"]},
    {"id": 15, "stage": 2, "title": "Điện thoại, mạng xã hội & internet", "subtitle": "Gọi điện, nhắn tin và Wi-Fi", "seeds": ["上网", "照片", "发", "用", "告诉", "快"]},
    {"id": 16, "stage": 2, "title": "Mua sắm online & nhận hàng", "subtitle": "Đặt đơn, giao hàng nhanh và kiểm hàng", "seeds": ["网购", "快递", "送", "银行卡", "包", "方便"]},
    # Stage 3 (8 topics)
    {"id": 17, "stage": 3, "title": "Kết bạn mới & giữ liên lạc", "subtitle": "Làm quen sâu hơn và trò chuyện thân thiết", "seeds": ["认识", "介绍", "关系", "聊天", "联系", "欢迎"]},
    {"id": 18, "stage": 3, "title": "Hẹn gặp & lên kế hoạch đi chơi", "subtitle": "Sắp xếp lịch, rủ bạn cuối tuần", "seeds": ["打算", "决定", "周末", "一起", "方便", "迟到"]},
    {"id": 19, "stage": 3, "title": "Phim, nhạc & thần tượng", "subtitle": "Bình luận phim hay và bài hát yêu thích", "seeds": ["电影", "音乐", "故事", "演员", "声音", "节目"]},
    {"id": 20, "stage": 3, "title": "Thể thao & vận động", "subtitle": "Chạy bộ, đá bóng và cổ vũ thi đấu", "seeds": ["比赛", "体育馆", "跑", "游泳", "赢", "加油"]},
    {"id": 21, "stage": 3, "title": "Du lịch: khách sạn, vé, điểm tham quan", "subtitle": "Đặt phòng, mua vé tàu và tham quan", "seeds": ["旅游", "酒店", "票", "行李", "地图", "城市"]},
    {"id": 22, "stage": 3, "title": "Lễ tết & phong tục", "subtitle": "Đón Tết, quà tặng và món truyền thống", "seeds": ["节日", "春节", "饺子", "礼物", "热闹", "文化"]},
    {"id": 23, "stage": 3, "title": "Cảm xúc & tính cách", "subtitle": "Diễn đạt tâm trạng, lo lắng, tự tin", "seeds": ["开心", "担心", "紧张", "认真", "聪明", "可爱"]},
    {"id": 24, "stage": 3, "title": "Kể chuyện đã qua", "subtitle": "Thuật lại kỷ niệm đáng nhớ", "seeds": ["过去", "刚才", "突然", "碰到", "记得", "忘记"]},
    # Stage 4 (4 topics)
    {"id": 25, "stage": 4, "title": "Bày tỏ ý kiến & đồng ý/phản đối nhẹ nhàng", "subtitle": "Thảo luận, nêu lý do và đồng thuận", "seeds": ["认为", "同意", "其实", "影响", "重要", "清楚"]},
    {"id": 26, "stage": 4, "title": "Dự định & ước mơ tương lai", "subtitle": "Mục tiêu nghề nghiệp và kế hoạch dài hạn", "seeds": ["希望", "机会", "选择", "努力", "完成", "办法"]},
    {"id": 27, "stage": 4, "title": "Công nghệ & AI trong đời sống", "subtitle": "Trí tuệ nhân tạo, ứng dụng thông minh", "seeds": ["人工智能", "变化", "世界", "简单", "帮助", "提高"]},
    {"id": 28, "stage": 4, "title": "Tình huống khó: nhờ giúp đỡ, khẩn cấp & xin lỗi", "subtitle": "Xử lý sự cố, xin lỗi và hỗ trợ kịp thời", "seeds": ["安全", "检查", "解决", "小心", "原谅", "感谢"]},
]

# Essential thematic words added if missing from HSK 1-3 pool
EXTRA_THEMATIC_WORDS = [
    {"hanzi": "网购", "pinyin": "wǎng gòu", "meaningVi": "mua sắm online", "radical": "糸", "level": 2, "stage": 2},
    {"hanzi": "快递", "pinyin": "kuài dì", "meaningVi": "chuyển phát nhanh, shipper", "radical": "心", "level": 2, "stage": 2},
    {"hanzi": "外卖", "pinyin": "wài mài", "meaningVi": "đồ ăn giao tận nơi", "radical": "夕", "level": 2, "stage": 2},
    {"hanzi": "人工智能", "pinyin": "rén gōng zhì néng", "meaningVi": "trí tuệ nhân tạo (AI)", "radical": "人", "level": 3, "stage": 4},
    {"hanzi": "原谅", "pinyin": "yuán liàng", "meaningVi": "tha thứ, thông cảm", "radical": "讠", "level": 3, "stage": 4},
    {"hanzi": "聊天", "pinyin": "liáo tiān", "meaningVi": "trò chuyện, tán gẫu", "radical": "耳", "level": 3, "stage": 3},
    {"hanzi": "高铁", "pinyin": "gāo tiě", "meaningVi": "tàu cao tốc", "radical": "金", "level": 3, "stage": 3},
    {"hanzi": "空调", "pinyin": "kōng tiáo", "meaningVi": "điều hòa không khí", "radical": "穴", "level": 2, "stage": 2},
    {"hanzi": "游泳", "pinyin": "yóu yǒng", "meaningVi": "bơi lội", "radical": "氵", "level": 3, "stage": 3},
    {"hanzi": "赢", "pinyin": "yíng", "meaningVi": "thắng, chiến thắng", "radical": "贝", "level": 3, "stage": 3},
    {"hanzi": "演员", "pinyin": "yǎn yuán", "meaningVi": "diễn viên", "radical": "氵", "level": 3, "stage": 3},
    {"hanzi": "礼物", "pinyin": "lǐ wù", "meaningVi": "quà tặng", "radical": "礻", "level": 3, "stage": 3},
    {"hanzi": "春节", "pinyin": "Chūn jié", "meaningVi": "Tết Nguyên Đán", "radical": "日", "level": 3, "stage": 3},
    {"hanzi": "加油", "pinyin": "jiā yóu", "meaningVi": "cố lên", "radical": "力", "level": 3, "stage": 3},
    {"hanzi": "生病", "pinyin": "shēng bìng", "meaningVi": "bị ốm, đổ bệnh", "radical": "疒", "level": 2, "stage": 2},
    {"hanzi": "左边", "pinyin": "zuǒ biān", "meaningVi": "bên trái", "radical": "工", "level": 1, "stage": 1},
    {"hanzi": "右边", "pinyin": "yòu biān", "meaningVi": "bên phải", "radical": "口", "level": 1, "stage": 1},
    {"hanzi": "生日", "pinyin": "shēng rì", "meaningVi": "sinh nhật", "radical": "生", "level": 1, "stage": 1},
    {"hanzi": "今年", "pinyin": "jīn nián", "meaningVi": "năm nay", "radical": "人", "level": 1, "stage": 1},
    {"hanzi": "联系", "pinyin": "lián xì", "meaningVi": "liên hệ, giữ liên lạc", "radical": "耳", "level": 3, "stage": 3},
    {"hanzi": "热闹", "pinyin": "rè nao", "meaningVi": "náo nhiệt, đông vui", "radical": "火", "level": 3, "stage": 3},
    {"hanzi": "紧张", "pinyin": "jǐn zhāng", "meaningVi": "hồi hộp, căng thẳng", "radical": "糸", "level": 3, "stage": 3},
    {"hanzi": "感谢", "pinyin": "gǎn xiè", "meaningVi": "cảm ơn, cảm kích", "radical": "心", "level": 3, "stage": 4},
    {"hanzi": "春天", "pinyin": "chūn tiān", "meaningVi": "mùa xuân", "radical": "日", "level": 2, "stage": 2},
    {"hanzi": "夏天", "pinyin": "xià tiān", "meaningVi": "mùa hè", "radical": "夂", "level": 2, "stage": 2},
    {"hanzi": "秋天", "pinyin": "qiū tiān", "meaningVi": "mùa thu", "radical": "禾", "level": 2, "stage": 2},
    {"hanzi": "冬天", "pinyin": "dōng tiān", "meaningVi": "mùa đông", "radical": "冫", "level": 2, "stage": 2},
    {"hanzi": "公园", "pinyin": "gōng yuán", "meaningVi": "công viên", "radical": "八", "level": 2, "stage": 2},
    {"hanzi": "周末", "pinyin": "zhōu mò", "meaningVi": "cuối tuần", "radical": "木", "level": 2, "stage": 2},
]


class GeneratedExamplesBatch(BaseModel):
    class ExItem(BaseModel):
        hanzi: str
        sentenceHanzi: str
        sentenceVi: str

    items: list[ExItem]


def to_py(text: str) -> str:
    return " ".join(x[0] for x in to_pinyin(text, style=Style.TONE))


def pick_best_pinyin(hanzi: str, complete_map: dict[str, dict], cedict: dict[str, dict], fallback_py: str) -> str:
    if hanzi in PINYIN_OVERRIDES:
        return PINYIN_OVERRIDES[hanzi]
    comp = complete_map.get(hanzi)
    cpy = to_py(hanzi)
    if comp:
        forms = comp.get("forms") or []
        valid_forms = []
        for f in forms:
            py = ((f.get("transcriptions") or {}).get("pinyin") or "").strip()
            meanings = " ".join(f.get("meanings") or []).lower()
            if not py:
                continue
            if py[0].isupper() and hanzi not in PROPER_PROUNS:
                continue
            if "surname" in meanings or "archaic" in meanings or "used in" in meanings or "variant of" in meanings:
                continue
            valid_forms.append(py)
        for py in valid_forms:
            if py.replace(" ", "").lower() == cpy.replace(" ", "").lower():
                return py
        if valid_forms:
            return valid_forms[0]
    if hanzi in cedict:
        return cedict[hanzi]["pinyin"]
    return fallback_py or cpy


def load_mmah() -> dict[str, dict]:
    out: dict[str, dict] = {}
    with (DATA_DIR / "makemeahanzi_dictionary.txt").open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                obj = json.loads(line)
                if obj.get("character"):
                    out[obj["character"]] = obj
    return out


def tokenize_paragraph(hanzi: str, vi: str, glossed_new: set[str], full_dict: set[str], word_py_map: dict[str, str], cedict: dict[str, dict]) -> dict:
    parts = CJK_RUN_RE.split(hanzi)
    tokens: list[dict] = []
    for part in parts:
        if not part:
            continue
        if CJK_ONLY_RE.match(part):
            for tok in segment_chinese(part, full_dict):
                py = word_py_map.get(tok) or cedict.get(tok, {}).get("pinyin") or to_py(tok)
                entry: dict[str, Any] = {"w": tok, "pinyin": py}
                if tok in glossed_new:
                    entry["isNew"] = True
                tokens.append(entry)
        else:
            tokens.append({"w": part, "pinyin": ""})
    return {"hanzi": hanzi, "vi": vi, "tokens": tokens}


def build_all_stage_words(
    pool: list[dict],
    vi_cache: dict[str, str],
    complete_map: dict[str, dict],
    cedict: dict[str, dict],
    mmah: dict[str, dict],
) -> tuple[dict[int, list[dict]], dict[str, dict]]:
    existing_s1: list[dict] = json.loads((CONTENT_DIR / "stage-1" / "words.json").read_text(encoding="utf-8"))
    for w in existing_s1:
        w["pinyin"] = pick_best_pinyin(w["hanzi"], complete_map, cedict, w["pinyin"])

    seen_hz = {w["hanzi"] for w in existing_s1}

    # Map every topic seed to the earliest stage it belongs to so 100% of topic seeds live in that stage's words.json
    seed_stage_override: dict[str, int] = {}
    for t in TOPICS_SPEC:
        for hz in t["seeds"]:
            if hz not in seed_stage_override or t["stage"] < seed_stage_override[hz]:
                seed_stage_override[hz] = t["stage"]

    def make_word_entry(word_id: str, raw: dict, stage_override: int | None = None) -> dict:
        hz = raw["hanzi"]
        seen_hz.add(hz)
        py = pick_best_pinyin(hz, complete_map, cedict, raw.get("pinyin", ""))
        vi = vi_cache.get(hz) or raw.get("meaningVi") or ", ".join(raw.get("meaningsEn", [])[:2])
        rad = raw.get("radical") or (mmah.get(hz[0], {}).get("radical", ""))
        return {
            "id": word_id,
            "hanzi": hz,
            "pinyin": py,
            "meaningVi": vi,
            "radical": rad,
            "level": stage_override if stage_override is not None else raw.get("level", 1),
            "frequency": raw.get("frequency", 9999),
            "mnemonic": raw.get("mnemonic", ""),
            "examples": raw.get("examples", []),
        }

    stage_lists: dict[int, list[dict]] = {1: list(existing_s1), 2: [], 3: [], 4: []}
    prefixes = {1: "w", 2: "w2", 3: "w3", 4: "w4"}

    # First pull higher-level seeds down to their earliest needed topic stage, NEVER pushing HSK-1/2 words UP out of earlier stages
    for raw in pool:
        hz = raw["hanzi"]
        if hz in seen_hz:
            continue
        if hz in seed_stage_override:
            target_st = min(raw["level"], seed_stage_override[hz])
            arr = stage_lists[target_st]
            arr.append(make_word_entry(f"{prefixes[target_st]}-{len(arr) + 1:03d}", raw, target_st))

    # Then distribute remaining pool words across stages 1..4 cleanly
    l1_rest = [w for w in pool if w["level"] == 1 and w["hanzi"] not in seen_hz]
    l2_all = [w for w in pool if w["level"] == 2 and w["hanzi"] not in seen_hz]
    l3_all = [w for w in pool if w["level"] == 3 and w["hanzi"] not in seen_hz]
    half_l3 = len(l3_all) // 2

    for raw in l1_rest:
        stage_lists[1].append(make_word_entry(f"w-{len(stage_lists[1]) + 1:03d}", raw, 1))
    for raw in l2_all:
        stage_lists[2].append(make_word_entry(f"w2-{len(stage_lists[2]) + 1:03d}", raw, 2))
    for raw in l3_all[:half_l3]:
        stage_lists[3].append(make_word_entry(f"w3-{len(stage_lists[3]) + 1:03d}", raw, 3))
    for raw in l3_all[half_l3:]:
        stage_lists[4].append(make_word_entry(f"w4-{len(stage_lists[4]) + 1:03d}", raw, 4))

    for extra in EXTRA_THEMATIC_WORDS:
        hz = extra["hanzi"]
        if hz not in seen_hz:
            st = extra["stage"]
            arr = stage_lists[st]
            arr.append(make_word_entry(f"{prefixes[st]}-{len(arr) + 1:03d}", extra, st))

    # Match Tatoeba examples cleanly + batch-translate cmn-eng & synthesize missing examples
    tatoeba = json.loads((DATA_DIR / "tatoeba_cmn_pairs.json").read_text(encoding="utf-8"))
    short_vie = [s for s in tatoeba["sentences"] if s["vie"] and 3 <= len(s["cmn"]) <= 24]
    short_eng = [s for s in tatoeba["sentences"] if not s["vie"] and s.get("eng") and 4 <= len(s["cmn"]) <= 22]

    # Index by char for fast lookup
    vie_idx: dict[str, list[dict]] = {}
    eng_idx: dict[str, list[dict]] = {}
    for s in short_vie:
        for ch in set(s["cmn"]):
            vie_idx.setdefault(ch, []).append(s)
    for s in short_eng:
        for ch in set(s["cmn"]):
            b = eng_idx.setdefault(ch, [])
            if len(b) < 80:
                b.append(s)

    tat_cache_path = CACHE_DIR / "tatoeba_vi_cache.json"
    tat_cache: dict[str, Any] = json.loads(tat_cache_path.read_text(encoding="utf-8")) if tat_cache_path.exists() else {}

    pending_en: list[tuple[str, str]] = []
    pending_gen: list[dict] = []
    chosen_eng_map: dict[str, tuple[str, str]] = {}

    tatoeba_stats = {"existing": 0, "direct_vie": 0, "tatoeba_en_gemini": 0, "ai_example": 0}

    for st_id, words in stage_lists.items():
        for w in words:
            if w["examples"] and not str(w["examples"][0]["hanzi"]).startswith("我学「"):
                tatoeba_stats["existing"] += 1
                continue
            hz = w["hanzi"]
            hit_vie = next((s for s in vie_idx.get(hz[0], []) if hz in s["cmn"]), None)
            if hit_vie:
                w["examples"] = [{"hanzi": hit_vie["cmn"], "pinyin": to_py(hit_vie["cmn"]), "vi": hit_vie["vie"][0]}]
                tatoeba_stats["direct_vie"] += 1
                continue
            hit_eng = next((s for s in eng_idx.get(hz[0], []) if hz in s["cmn"] and len(s["cmn"]) <= 22), None)
            if hit_eng:
                cmn = hit_eng["cmn"]
                eng = hit_eng["eng"][0]
                chosen_eng_map[hz] = (cmn, eng)
                if cmn not in tat_cache:
                    pending_en.append((cmn, eng))
                tatoeba_stats["tatoeba_en_gemini"] += 1
            else:
                if f"gen::{hz}" not in tat_cache:
                    pending_gen.append(w)
                tatoeba_stats["ai_example"] += 1

    # Batch translate pending cmn-eng Tatoeba sentences
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if pending_en and api_key:
        dedup_en = list(dict.fromkeys(pending_en))
        print(f"Translating {len(dedup_en)} Tatoeba cmn-eng example sentences via Gemini...")
        chunks = [dedup_en[i : i + 50] for i in range(0, len(dedup_en), 50)]
        lock = threading.Lock()
        with ThreadPoolExecutor(max_workers=3) as ex_pool:
            futs = [ex_pool.submit(translate_tatoeba_en_batch, ch) for ch in chunks]
            for i, fut in enumerate(as_completed(futs), 1):
                res_map = fut.result()
                with lock:
                    tat_cache.update(res_map)
                    tat_cache_path.write_text(json.dumps(tat_cache, ensure_ascii=False, indent=2), encoding="utf-8")
                if i % 5 == 0 or i == len(chunks):
                    print(f"  Tatoeba EN->VI batches: {i}/{len(chunks)}")

    # Synthesize examples for words without any short Tatoeba match
    if pending_gen and api_key:
        print(f"Generating {len(pending_gen)} short natural examples for words without Tatoeba hits...")
        for i in range(0, len(pending_gen), 40):
            chunk = pending_gen[i : i + 40]
            prompt = (
                "Viết đúng 1 câu ví dụ tiếng Trung ngắn gọn (6-14 chữ, tự nhiên, đời thường) kèm dịch Việt (xưng hô mình/bạn) "
                "cho từng từ sau, đảm bảo câu ví dụ có chứa đúng từ hanzi gốc:\n"
                + "\n".join(f"{w['hanzi']} ({w['meaningVi']})" for w in chunk)
            )
            out: GeneratedExamplesBatch = _call_structured(api_key, prompt, GeneratedExamplesBatch, timeout=45.0)
            for item in out.items:
                tat_cache[f"gen::{item.hanzi.strip()}"] = {
                    "hanzi": item.sentenceHanzi.strip(),
                    "vi": item.sentenceVi.strip(),
                }
            tat_cache_path.write_text(json.dumps(tat_cache, ensure_ascii=False, indent=2), encoding="utf-8")

    # Hydrate examples back into stage_lists
    word_by_hz: dict[str, dict] = {}
    for words in stage_lists.values():
        for w in words:
            hz = w["hanzi"]
            if not w["examples"] or str(w["examples"][0]["hanzi"]).startswith("我学「"):
                if hz in chosen_eng_map:
                    cmn, eng = chosen_eng_map[hz]
                    vi = tat_cache.get(cmn) or eng
                    w["examples"] = [{"hanzi": cmn, "pinyin": to_py(cmn), "vi": vi}]
                elif isinstance(tat_cache.get(f"gen::{hz}"), dict):
                    g = tat_cache[f"gen::{hz}"]
                    w["examples"] = [{"hanzi": g["hanzi"], "pinyin": to_py(g["hanzi"]), "vi": g["vi"]}]
                else:
                    w["examples"] = [{"hanzi": f"我们常常用到「{hz}」。", "pinyin": to_py(f"我们常常用到{hz}。"), "vi": f"Chúng mình hay dùng từ \"{w['meaningVi']}\"."}]
            word_by_hz[hz] = w

    print("Example sources summary:", tatoeba_stats)
    return stage_lists, word_by_hz


def pick_writing_chars(topic_words: list[dict], stage_words: list[dict], mmah: dict[str, dict], used_chars: set[str]) -> list[dict]:
    """Select 3-4 verified hanzi-writer-data characters for a topic's writing lesson."""
    candidates: list[dict] = []
    # 1. Exact 1-char words from topic_words
    for w in topic_words:
        for ch in w["hanzi"]:
            if "\u4e00" <= ch <= "\u9fff" and (HW_DATA_DIR / f"{ch}.json").exists():
                candidates.append({"char": ch, "word": w})

    chosen: list[dict] = []
    seen_ch: set[str] = set()
    for c in candidates:
        ch = c["char"]
        if ch in seen_ch or ch in used_chars:
            continue
        seen_ch.add(ch)
        chosen.append(c)
        if len(chosen) >= 3:
            break

    # Fallback if < 3 unique chars in topic
    if len(chosen) < 3:
        for c in candidates:
            ch = c["char"]
            if ch not in seen_ch:
                seen_ch.add(ch)
                chosen.append(c)
                if len(chosen) >= 3:
                    break
    if len(chosen) < 3:
        for w in stage_words:
            for ch in w["hanzi"]:
                if "\u4e00" <= ch <= "\u9fff" and ch not in seen_ch and ch not in used_chars and (HW_DATA_DIR / f"{ch}.json").exists():
                    seen_ch.add(ch)
                    chosen.append({"char": ch, "word": w})
                    if len(chosen) >= 3:
                        break
            if len(chosen) >= 3:
                break

    for c in chosen:
        used_chars.add(c["char"])
    return chosen


def build_lookalikes(target: str, meaning_vi: str, target_py: str, mmah: dict[str, dict], word_by_hz: dict[str, dict], stage_words: list[dict]) -> list[dict]:
    rad = mmah.get(target, {}).get("radical", "")
    same_rad = [
        ch
        for ch, info in mmah.items()
        if ch != target and info.get("radical") == rad and (HW_DATA_DIR / f"{ch}.json").exists()
    ]
    # Prefer characters that actually appear in our stage/curriculum words
    in_vocab = [ch for ch in same_rad if ch in word_by_hz]
    pool_chars = in_vocab + [ch for ch in same_rad if ch not in in_vocab]
    if len(pool_chars) < 3:
        for w in stage_words:
            for ch in w["hanzi"]:
                if ch != target and ch not in pool_chars and "\u4e00" <= ch <= "\u9fff" and (HW_DATA_DIR / f"{ch}.json").exists():
                    pool_chars.append(ch)
                    if len(pool_chars) >= 6:
                        break
            if len(pool_chars) >= 6:
                break

    items = [{"hanzi": target, "pinyin": target_py, "vi": meaning_vi}]
    for ch in pool_chars[:3]:
        w = word_by_hz.get(ch)
        py = w["pinyin"] if w else to_py(ch)
        vi = w["meaningVi"] if w else (mmah.get(ch, {}).get("definition", "").split(";")[0].strip() or ch)
        items.append({"hanzi": ch, "pinyin": py, "vi": vi})
    # Rotate deterministically so target isn't always index 0
    shift = ord(target) % len(items)
    return items[shift:] + items[:shift]


def main() -> None:
    GEN_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    pool = json.loads((CACHE_DIR / "hsk_1_3_pool.json").read_text(encoding="utf-8"))
    vi_cache = json.loads((CACHE_DIR / "vi_cache.json").read_text(encoding="utf-8"))
    complete_map = {x["simplified"]: x for x in json.loads((DATA_DIR / "complete.json").read_text(encoding="utf-8"))}
    cedict = load_cedict()
    mmah = load_mmah()

    stage_lists, word_by_hz = build_all_stage_words(pool, vi_cache, complete_map, cedict, mmah)
    word_py_map = {hz: w["pinyin"] for hz, w in word_by_hz.items()}
    # Use the 11,470 HSK 1-9 complete vocabulary + curriculum words for segmentation so rare CC-CEDICT slang (e.g. 的哥 inside 我的哥哥) never causes false splits while all out-of-level HSK 4-9 words and unknown chars are strictly caught
    full_dict = set(complete_map.keys()) | set(word_by_hz.keys()) | {
        "Bao", "小美", "小明", "王老师", "小笼包", "奶茶", "咖啡", "少糖", "去冰", "网购", "快递", "外卖", "人工智能", "高铁", "春节"
    }

    # Build cumulative allowed vocab per stage & assign 5-6 topic seed words strictly from that stage's words.json
    topic_new_words: dict[int, list[dict]] = {}
    used_topic_words = set()
    for t in TOPICS_SPEC:
        tid = t["id"]
        st = t["stage"]
        st_words = stage_lists[st]
        stage_hz_map = {w["hanzi"]: w for w in st_words}
        picked: list[dict] = []
        for hz in t["seeds"]:
            w = stage_hz_map.get(hz)
            if w:
                picked.append(w)
                used_topic_words.add(hz)
        # Ensure at least 5 words from this stage
        for w in st_words:
            if len(picked) >= 5:
                break
            if w["hanzi"] not in used_topic_words:
                picked.append(w)
                used_topic_words.add(w["hanzi"])
        topic_new_words[tid] = picked[:6]

    # Single-char glue tokens + common names allowed across all levels so segmentation never false-flags pronouns/names/single chars
    base_names_chars = {"Bao", "小明", "小美", "王老师", "小王", "小李", "林", "明", "王", "李", "张", "小", "老", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "百", "千", "两", "零", "了", "吗", "呢", "吧", "啊", "的", "得", "地"}

    def allowed_for_stage(stage_num: int) -> set[str]:
        voc = set(base_names_chars)
        for s in range(1, stage_num + 1):
            for w in stage_lists[s]:
                voc.add(w["hanzi"])
                for ch in w["hanzi"]:
                    voc.add(ch)
        return voc

    # Load preserved DOT 1 lessons & readings for T1 and T6
    dot1_lessons = json.loads((CONTENT_DIR / "stage-1" / "lessons.json").read_text(encoding="utf-8"))
    dot1_readings = json.loads((CONTENT_DIR / "stage-1" / "readings.json").read_text(encoding="utf-8"))
    preserved_lessons_by_topic = {
        1: [l for l in dot1_lessons if l["topicId"] == 1],
        6: [l for l in dot1_lessons if l["topicId"] == 6],
    }
    preserved_readings_by_topic = {
        1: [r for r in dot1_readings if r["topicId"] == 1],
        6: [r for r in dot1_readings if r["topicId"] == 6],
    }

    stats_path = CACHE_DIR / "level_check_stats.json"
    if stats_path.exists():
        stats = json.loads(stats_path.read_text(encoding="utf-8"))
    else:
        stats = {
            "attempted": 0,
            "accepted": 0,
            "rejected": 0,
            "rejectionReasons": [],
        }
    stats_lock = threading.Lock()

    def record_stats(local_stats: dict) -> None:
        with stats_lock:
            stats["attempted"] += local_stats["attempted"]
            stats["accepted"] += local_stats["accepted"]
            stats["rejected"] += local_stats["rejected"]
            stats["rejectionReasons"].extend(local_stats["rejectionReasons"])
            stats_path.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")

    def dict_for_vocab(allowed: set[str]) -> set[str]:
        return {
            w for w in full_dict
            if w in allowed or not (len(w) >= 2 and all(ch in allowed for ch in w))
        }

    # Worker per topic (topics 2-5, 7-28) with per-part caching
    def process_topic(t: dict) -> dict:
        tid = t["id"]
        cache_p = GEN_CACHE_DIR / f"t{tid}.json"
        if cache_p.exists():
            return json.loads(cache_p.read_text(encoding="utf-8"))

        st = t["stage"]
        nwords = topic_new_words[tid]
        allowed = allowed_for_stage(st)
        st_dict = dict_for_vocab(allowed)
        r_mode = "fluent" if tid % 2 == 1 else "study"
        len_bounds = {1: (85, 145), 2: (110, 185), 3: (160, 250), 4: (215, 315)}[st]
        sorted_nw = sorted(nwords, key=lambda w: (-len(w["hanzi"]), -w.get("frequency", 0)))
        if st == 1:
            reading_new = sorted_nw[:2]
        else:
            reading_new = sorted_nw[:2] if r_mode == "fluent" else sorted_nw[:3]

        comm_p = GEN_CACHE_DIR / f"t{tid}_comm.json"
        if comm_p.exists():
            comm_data = json.loads(comm_p.read_text(encoding="utf-8"))
        else:
            ls = {"attempted": 0, "accepted": 0, "rejected": 0, "rejectionReasons": []}
            try:
                comm = generate_topic_comm(tid, t["title"], allowed, nwords, st_dict, ls)
                comm_data = comm.model_dump()
                comm_p.write_text(json.dumps(comm_data, ensure_ascii=False, indent=2), encoding="utf-8")
                print(f"  t{tid} comm OK (att={ls['attempted']}, rej={ls['rejected']})", flush=True)
            finally:
                record_stats(ls)

        read_p = GEN_CACHE_DIR / f"t{tid}_read.json"
        if read_p.exists():
            read_bundle = json.loads(read_p.read_text(encoding="utf-8"))
        else:
            ls = {"attempted": 0, "accepted": 0, "rejected": 0, "rejectionReasons": []}
            try:
                reading, known_pct = generate_topic_reading(
                    tid, t["title"], r_mode, len_bounds[0], len_bounds[1], allowed, reading_new, st_dict, ls
                )
                read_bundle = {"reading": reading.model_dump(), "knownPercent": known_pct}
                read_p.write_text(json.dumps(read_bundle, ensure_ascii=False, indent=2), encoding="utf-8")
                print(f"  t{tid} read OK (att={ls['attempted']}, rej={ls['rejected']}, known={known_pct}%)", flush=True)
            finally:
                record_stats(ls)

        lis_p = GEN_CACHE_DIR / f"t{tid}_listen.json"
        if lis_p.exists():
            lis_data = json.loads(lis_p.read_text(encoding="utf-8"))
        else:
            ls = {"attempted": 0, "accepted": 0, "rejected": 0, "rejectionReasons": []}
            try:
                listen = generate_topic_listening(tid, t["title"], allowed, nwords, st_dict, ls)
                lis_data = listen.model_dump()
                lis_p.write_text(json.dumps(lis_data, ensure_ascii=False, indent=2), encoding="utf-8")
                print(f"  t{tid} listen OK (att={ls['attempted']}, rej={ls['rejected']})", flush=True)
            finally:
                record_stats(ls)

        payload = {
            "topicId": tid,
            "comm": comm_data,
            "reading": read_bundle["reading"],
            "readingMode": r_mode,
            "knownPercent": read_bundle["knownPercent"],
            "readingNewWords": [w["hanzi"] for w in reading_new],
            "listening": lis_data,
        }
        cache_p.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Topic {tid}/28 complete (known={read_bundle['knownPercent']}%)", flush=True)
        return payload

    pending_topics = [t for t in TOPICS_SPEC if not t.get("preserve")]
    topic_results: dict[int, dict] = {}
    topic_failed: dict[int, Exception] = {}
    with ThreadPoolExecutor(max_workers=4) as executor:
        futs = {executor.submit(process_topic, t): t["id"] for t in pending_topics}
        for fut in as_completed(futs):
            tid = futs[fut]
            try:
                topic_results[tid] = fut.result()
            except Exception as exc:
                topic_failed[tid] = exc
                print(f"Topic {tid}/28 FAILED: {exc}", flush=True)
    if topic_failed:
        summary = "; ".join(f"T{tid}: {exc}" for tid, exc in sorted(topic_failed.items()))
        raise RuntimeError(f"{len(topic_failed)} topic(s) failed: {summary}")

    # Generate 4 Story Chapters & 4 Stage Tests
    story_results: dict[int, dict] = {}
    test_results: dict[int, dict] = {}

    def process_stage_capstone(st_meta: dict):
        sid = st_meta["id"]
        allowed = allowed_for_stage(sid)
        st_dict = dict_for_vocab(allowed)
        # Collect highlight words for the story chapter from this stage's topics
        st_topics = [t for t in TOPICS_SPEC if t["stage"] == sid]
        glossed = {w["hanzi"] for t in st_topics[:2] for w in topic_new_words[t["id"]][:1]}
        s_cache = GEN_CACHE_DIR / f"story_c{sid}.json"
        if s_cache.exists():
            story_results[sid] = json.loads(s_cache.read_text(encoding="utf-8"))
        else:
            local_stats = {"attempted": 0, "accepted": 0, "rejected": 0, "rejectionReasons": []}
            bounds = {1: (125, 185), 2: (175, 245), 3: (225, 305), 4: (280, 370)}[sid]
            try:
                sc, known_pct = generate_story_chapter(
                    sid, st_meta["storyChapter"]["title"], st_meta["storyChapter"]["teaserVi"],
                    bounds[0], bounds[1], allowed, glossed, st_dict, local_stats
                )
                data = {"story": sc.model_dump(), "knownPercent": known_pct, "newWords": sorted(glossed)}
                s_cache.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
                story_results[sid] = data
                print(f"Story Chapter {sid}/4 generated (known={known_pct}%)", flush=True)
            finally:
                record_stats(local_stats)

        t_cache = GEN_CACHE_DIR / f"stage_test_{sid}.json"
        if t_cache.exists():
            test_results[sid] = json.loads(t_cache.read_text(encoding="utf-8"))
        else:
            local_stats = {"attempted": 0, "accepted": 0, "rejected": 0, "rejectionReasons": []}
            try:
                st_out = generate_stage_test_items(sid, st_meta["title"], allowed, st_dict, local_stats)
                data = st_out.model_dump()
                t_cache.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
                test_results[sid] = data
                print(f"Stage Test {sid}/4 generated", flush=True)
            finally:
                record_stats(local_stats)

    capstone_failed: dict[int, Exception] = {}
    with ThreadPoolExecutor(max_workers=2) as executor:
        cfuts = {executor.submit(process_stage_capstone, sm): sm["id"] for sm in STAGES_META}
        for fut in as_completed(cfuts):
            sid = cfuts[fut]
            try:
                fut.result()
            except Exception as exc:
                capstone_failed[sid] = exc
                print(f"Stage capstone {sid}/4 FAILED: {exc}", flush=True)
    if capstone_failed:
        summary = "; ".join(f"Stage {sid}: {exc}" for sid, exc in sorted(capstone_failed.items()))
        raise RuntimeError(f"{len(capstone_failed)} capstone(s) failed: {summary}")

    # Deterministic selection of writing chars for Topics 2-5, 7-28 + radical note generation via Gemini
    used_writing_chars = {"你", "好", "见", "喝", "茶", "杯"}
    topic_writing_picks: dict[int, list[dict]] = {}
    need_notes: list[dict] = []
    rad_notes_cache_p = CACHE_DIR / "radical_notes_vi.json"
    rad_notes_cache: dict[str, str] = (
        json.loads(rad_notes_cache_p.read_text(encoding="utf-8")) if rad_notes_cache_p.exists() else {}
    )

    for t in TOPICS_SPEC:
        if t.get("preserve"):
            continue
        tid = t["id"]
        picks = pick_writing_chars(topic_new_words[tid], stage_lists[t["stage"]], mmah, used_writing_chars)
        topic_writing_picks[tid] = picks
        for c in picks:
            ch = c["char"]
            if ch not in rad_notes_cache:
                info = mmah.get(ch, {})
                w = word_by_hz.get(ch) or c["word"]
                need_notes.append(
                    {
                        "char": ch,
                        "radical": info.get("radical") or w.get("radical", ""),
                        "meaningVi": w["meaningVi"],
                        "definition": info.get("definition", ""),
                    }
                )

    if need_notes and os.environ.get("GEMINI_API_KEY", "").strip():
        print(f"Generating {len(need_notes)} Vietnamese radical mnemonic notes...")
        for i in range(0, len(need_notes), 30):
            notes = generate_radical_notes_batch(need_notes[i : i + 30])
            rad_notes_cache.update(notes)
            rad_notes_cache_p.write_text(json.dumps(rad_notes_cache, ensure_ascii=False, indent=2), encoding="utf-8")

    # Assemble all stage bundles cleanly matching schema
    lessons_by_stage: dict[int, list[dict]] = {1: [], 2: [], 3: [], 4: []}
    readings_by_stage: dict[int, list[dict]] = {1: [], 2: [], 3: [], 4: []}

    for t in TOPICS_SPEC:
        tid = t["id"]
        st = t["stage"]
        if t.get("preserve"):
            lessons_by_stage[st].extend(preserved_lessons_by_topic[tid])
            readings_by_stage[st].extend(preserved_readings_by_topic[tid])
            continue

        gen = topic_results[tid]
        nwords = topic_new_words[tid]
        nw_ids = [w["id"] for w in nwords]
        xp_base = 30 + (st - 1) * 5

        comm = gen["comm"]
        patterns = []
        for pi, p in enumerate(comm["patterns"][:2], start=1):
            patterns.append(
                {
                    "id": f"p-t{tid}-{pi}",
                    "frame": p["frame"],
                    "pinyin": to_py(p["frame"].replace("___", "")),
                    "meaningVi": p["meaningVi"],
                    "exampleHanzi": p["exampleHanzi"],
                    "examplePinyin": to_py(p["exampleHanzi"]),
                    "exampleVi": p["exampleVi"],
                    "slots": {
                        "promptVi": p["promptVi"],
                        "choices": [{"hanzi": c["hanzi"], "pinyin": to_py(c["hanzi"]), "vi": c["vi"]} for c in p["choices"]],
                        "answerHanzi": p["answerHanzi"],
                    },
                }
            )

        dialogue = []
        for turn in comm["dialogue"]:
            d_item: dict[str, Any] = {
                "speaker": turn["speaker"],
                "voiceRole": turn["voiceRole"],
                "hanzi": turn["hanzi"],
                "pinyin": to_py(turn["hanzi"]),
                "vi": turn["vi"],
                "mode": turn["mode"],
            }
            if turn.get("goalLabel"):
                d_item["goalLabel"] = turn["goalLabel"]
            if turn["mode"] == "choice":
                d_item["choices"] = [
                    {"hanzi": c["hanzi"], "pinyin": to_py(c["hanzi"]), "vi": c["vi"], "correct": bool(c["correct"])}
                    for c in turn.get("choices", [])
                ]
            elif turn["mode"] == "tiles":
                d_item["tilePrompt"] = turn.get("tilePrompt") or segment_chinese(turn["hanzi"], full_dict)
            elif turn["mode"] == "pinyin":
                py_full = to_py(turn["hanzi"])
                plain = re.sub(r"[^\w\s]", "", "".join(x[0] for x in to_pinyin(turn["hanzi"], style=Style.NORMAL)))
                d_item["acceptedPinyin"] = [plain.strip(), py_full, turn["hanzi"].rstrip("！。？!?.,")]
            dialogue.append(d_item)

        mq = comm["meaningQuestion"]
        comm_exercises = [
            {
                "id": f"ex-t{tid}-1",
                "kind": "meaning-choice",
                "promptVi": mq["promptVi"],
                "hanziPrompt": mq["hanziPrompt"],
                "pinyinPrompt": word_py_map.get(mq["hanziPrompt"]) or to_py(mq["hanziPrompt"]),
                "options": [{"label": o, "value": o} for o in mq["options"]],
                "answer": mq["answer"],
            },
            {
                "id": f"ex-t{tid}-2",
                "kind": "hanzi-choice",
                "promptVi": f"Nghe và chọn chữ Hán đúng ({word_by_hz.get(comm['hanziAudioText'], {}).get('meaningVi', comm['hanziAudioText'])})",
                "audioText": comm["hanziAudioText"],
                "options": [{"label": o, "value": o} for o in comm["hanziAudioOptions"]],
                "answer": comm["hanziAudioText"],
            },
            {
                "id": f"ex-t{tid}-3",
                "kind": "sentence-tiles",
                "promptVi": comm["tilePromptVi"],
                "tiles": comm["tileWords"],
                "answer": "".join(comm["tileWords"]),
            },
        ]

        roleplay = []
        for rp in comm["roleplay"][:3]:
            roleplay.append(
                {
                    "npcHanzi": rp["npcHanzi"],
                    "npcPinyin": to_py(rp["npcHanzi"]),
                    "npcVi": rp["npcVi"],
                    "promptVi": rp["promptVi"],
                    "options": [
                        {"hanzi": c["hanzi"], "pinyin": to_py(c["hanzi"]), "vi": c["vi"], "correct": bool(c["correct"])}
                        for c in rp["choices"]
                    ],
                    "expectedHanzi": rp["expectedHanzi"],
                }
            )

        comm_lesson = {
            "id": f"t{tid}-giao-tiep",
            "stage": st,
            "topicId": tid,
            "title": t["title"],
            "type": "giao-tiep",
            "xp": xp_base,
            "newWords": nw_ids,
            "patterns": patterns,
            "dialogue": dialogue,
            "exercises": comm_exercises,
            "roleplay": roleplay,
        }

        doc_lesson = {
            "id": f"t{tid}-doc",
            "stage": st,
            "topicId": tid,
            "title": f"Đọc: {gen['reading']['title']}",
            "type": "doc",
            "xp": xp_base - 5,
            "newWords": [],
            "readingId": f"r-t{tid}",
        }

        r_data = gen["reading"]
        glossed_set = set(gen["readingNewWords"])
        reading_entry = {
            "id": f"r-t{tid}",
            "stage": st,
            "topicId": tid,
            "title": r_data["title"],
            "mode": gen["readingMode"],
            "knownPercent": gen["knownPercent"],
            "newWords": gen["readingNewWords"],
            "paragraphs": [
                tokenize_paragraph(p["hanzi"], p["vi"], glossed_set, full_dict, word_py_map, cedict)
                for p in r_data["paragraphs"]
            ],
            "questions": [
                {
                    "id": f"rq{tid}-{qi}",
                    "type": q["type"],
                    "q": q["q"],
                    "options": q["options"],
                    "answer": q["answer"],
                    "explainVi": q["explainVi"],
                }
                for qi, q in enumerate(r_data["questions"], start=1)
            ],
        }

        lis = gen["listening"]
        dict_plain = re.sub(r"[^\w\s]", "", "".join(x[0] for x in to_pinyin(lis["dictationText"], style=Style.NORMAL))).strip()
        nghe_lesson = {
            "id": f"t{tid}-nghe",
            "stage": st,
            "topicId": tid,
            "title": f"Nghe: {t['title']}",
            "type": "nghe",
            "xp": xp_base - 5,
            "newWords": nw_ids,
            "listeningTracks": [
                {
                    "id": f"lt{tid}-{ti}",
                    "speaker": tr["speaker"],
                    "voiceRole": tr["voiceRole"],
                    "hanzi": tr["hanzi"],
                    "pinyin": to_py(tr["hanzi"]),
                    "vi": tr["vi"],
                }
                for ti, tr in enumerate(lis["listeningTracks"][:4], start=1)
            ],
            "exercises": [
                {
                    "id": f"ng{tid}-1",
                    "kind": "listen-meaning",
                    "promptVi": lis["listenMeaning"]["promptVi"],
                    "audioText": lis["listenMeaning"]["audioText"],
                    "options": [{"label": o, "value": o} for o in lis["listenMeaning"]["options"]],
                    "answer": lis["listenMeaning"]["answer"],
                },
                {
                    "id": f"ng{tid}-2",
                    "kind": "listen-hanzi",
                    "promptVi": lis["listenHanzi"]["promptVi"],
                    "audioText": lis["listenHanzi"]["audioText"],
                    "options": [{"label": o, "value": o} for o in lis["listenHanzi"]["options"]],
                    "answer": lis["listenHanzi"]["answer"],
                },
                {
                    "id": f"ng{tid}-3",
                    "kind": "listen-tiles",
                    "promptVi": lis["listenTiles"]["promptVi"],
                    "audioText": lis["listenTiles"]["audioText"],
                    "tiles": lis["listenTiles"]["tiles"],
                    "answer": "".join(lis["listenTiles"]["tiles"]),
                },
                {
                    "id": f"ng{tid}-4",
                    "kind": "listen-blank",
                    "promptVi": lis["listenBlank"]["promptVi"],
                    "audioText": lis["listenBlank"]["audioText"],
                    "options": [{"label": o, "value": o} for o in lis["listenBlank"]["options"]],
                    "answer": lis["listenBlank"]["answer"],
                },
                {
                    "id": f"ng{tid}-5",
                    "kind": "listen-dialogue",
                    "promptVi": lis["listenDialogue"]["promptVi"],
                    "audioText": lis["listenDialogue"]["audioText"],
                    "options": [{"label": o, "value": o} for o in lis["listenDialogue"]["options"]],
                    "answer": lis["listenDialogue"]["answer"],
                },
                {
                    "id": f"ng{tid}-6",
                    "kind": "dictation",
                    "promptVi": "Chép chính tả rút gọn: gõ pinyin (hoặc chạm thẻ) câu vừa nghe",
                    "audioText": lis["dictationText"],
                    "tiles": lis["dictationTiles"],
                    "answer": dict_plain,
                },
            ],
        }

        w_specs = []
        for pick in topic_writing_picks[tid]:
            ch = pick["char"]
            w_ref = word_by_hz.get(ch) or pick["word"]
            rad = mmah.get(ch, {}).get("radical") or w_ref.get("radical") or ch
            py_ch = word_by_hz[ch]["pinyin"] if ch in word_by_hz else to_py(ch)
            vi_ch = word_by_hz[ch]["meaningVi"] if ch in word_by_hz else w_ref["meaningVi"]
            note = rad_notes_cache.get(ch) or f"Bộ {rad} — thành phần gợi nghĩa quan trọng trong chữ '{ch}' ({vi_ch})."
            w_specs.append(
                {
                    "char": ch,
                    "pinyin": py_ch,
                    "meaningVi": vi_ch,
                    "radical": rad,
                    "radicalNoteVi": note,
                    "lookalikes": build_lookalikes(ch, vi_ch, py_ch, mmah, word_by_hz, stage_lists[st]),
                }
            )

        viet_lesson = {
            "id": f"t{tid}-viet",
            "stage": st,
            "topicId": tid,
            "title": f"Viết: {t['title']}",
            "type": "viet",
            "xp": xp_base - 5,
            "newWords": nw_ids,
            "writingChars": w_specs,
        }

        lessons_by_stage[st].extend([comm_lesson, doc_lesson, nghe_lesson, viet_lesson])
        readings_by_stage[st].append(reading_entry)

    # Append Serialized Story Chapters & Stage Tests to each stage
    for st_meta in STAGES_META:
        sid = st_meta["id"]
        sdata = story_results[sid]
        sc = sdata["story"]
        s_new = set(sdata["newWords"])
        readings_by_stage[sid].append(
            {
                "id": f"story-c{sid}",
                "stage": sid,
                "topicId": sid * 100,
                "title": sc["title"],
                "mode": "study",
                "knownPercent": sdata["knownPercent"],
                "isStoryChapter": True,
                "chapterNumber": sid,
                "cliffhangerVi": sc["cliffhangerVi"],
                "newWords": sdata["newWords"],
                "paragraphs": [
                    tokenize_paragraph(p["hanzi"], p["vi"], s_new, full_dict, word_py_map, cedict)
                    for p in sc["paragraphs"]
                ],
                "questions": [
                    {
                        "id": f"scq{sid}-{qi}",
                        "type": q["type"],
                        "q": q["q"],
                        "options": q["options"],
                        "answer": q["answer"],
                        "explainVi": q["explainVi"],
                    }
                    for qi, q in enumerate(sc["questions"], start=1)
                ],
            }
        )

        # Build 8-item Stage Test: 6 Gemini items (2 giao-tiep, 2 doc, 2 nghe) + 2 Viet items from stage chars
        gen_test_items = test_results[sid]["items"]
        test_items: list[dict] = []
        for idx_it, it in enumerate(gen_test_items[:6], start=1):
            test_items.append(
                {
                    "id": f"st{sid}-q{idx_it}",
                    "skill": it["skill"],
                    "promptVi": it["promptVi"],
                    "passageHanzi": it.get("passageHanzi") or "",
                    "passagePinyin": to_py(it["passageHanzi"]) if it.get("passageHanzi") else "",
                    "passageVi": it.get("passageVi") or "",
                    "audioText": it.get("audioText") or "",
                    "options": [{"label": o, "value": o} for o in it["options"]],
                    "answer": it["answer"],
                    "explainVi": it.get("explainVi") or "",
                }
            )
        # Pick 2 writing characters from stage writing lessons
        stage_writing_specs = [
            wc
            for l in lessons_by_stage[sid]
            if l["type"] == "viet"
            for wc in l.get("writingChars", [])
        ]
        if len(stage_writing_specs) >= 2:
            w1_spec, w2_spec = stage_writing_specs[0], stage_writing_specs[-1]
            test_items.append(
                {
                    "id": f"st{sid}-q7",
                    "skill": "viet",
                    "promptVi": f"Viết đúng thứ tự nét chữ '{w1_spec['meaningVi']}' ({w1_spec['pinyin']})",
                    "writingChar": w1_spec,
                    "answer": w1_spec["char"],
                    "explainVi": w1_spec["radicalNoteVi"],
                }
            )
            test_items.append(
                {
                    "id": f"st{sid}-q8",
                    "skill": "viet",
                    "promptVi": f"Nhận diện mặt chữ: Đâu là chữ '{w2_spec['meaningVi']}' ({w2_spec['pinyin']})?",
                    "options": [{"label": lk["hanzi"], "value": lk["hanzi"]} for lk in w2_spec["lookalikes"]],
                    "answer": w2_spec["char"],
                    "explainVi": w2_spec["radicalNoteVi"],
                }
            )

        lessons_by_stage[sid].append(
            {
                "id": f"stage-{sid}-test",
                "stage": sid,
                "topicId": sid * 100,
                "title": f"Kiểm tra tổng hợp {st_meta['title']}",
                "type": "stage-test",
                "xp": 60,
                "newWords": [],
                "stageTestItems": test_items,
            }
        )

    # Curriculum manifest
    curriculum_out = {"stages": []}
    for st_meta in STAGES_META:
        sid = st_meta["id"]
        st_topics = [
            {
                "id": t["id"],
                "stage": sid,
                "title": t["title"],
                "subtitle": t["subtitle"],
                "ready": True,
                "lessonIds": [f"t{t['id']}-giao-tiep", f"t{t['id']}-doc", f"t{t['id']}-nghe", f"t{t['id']}-viet"],
                "readingId": f"r-t{t['id']}",
            }
            for t in TOPICS_SPEC
            if t["stage"] == sid
        ]
        curriculum_out["stages"].append({**st_meta, "topics": st_topics})

    # Write files
    (CONTENT_DIR / "curriculum.json").write_text(json.dumps(curriculum_out, ensure_ascii=False, indent=2), encoding="utf-8")
    for sid in (1, 2, 3, 4):
        sdir = CONTENT_DIR / f"stage-{sid}"
        sdir.mkdir(parents=True, exist_ok=True)
        (sdir / "words.json").write_text(json.dumps(stage_lists[sid], ensure_ascii=False, indent=2), encoding="utf-8")
        (sdir / "lessons.json").write_text(json.dumps(lessons_by_stage[sid], ensure_ascii=False, indent=2), encoding="utf-8")
        (sdir / "readings.json").write_text(json.dumps(readings_by_stage[sid], ensure_ascii=False, indent=2), encoding="utf-8")

    # Save exact level-check generation telemetry
    (CACHE_DIR / "level_check_stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")

    # Final verification summary across all 4 stages
    for sid in (1, 2, 3, 4):
        print(
            f"Stage {sid}: words={len(stage_lists[sid])}, lessons={len(lessons_by_stage[sid])}, readings={len(readings_by_stage[sid])}"
        )
    rej_pct = (stats["rejected"] / stats["attempted"] * 100) if stats["attempted"] else 0.0
    print(f"Level checker generation stats: attempted={stats['attempted']}, accepted={stats['accepted']}, rejected={stats['rejected']} ({rej_pct:.2f}% rejected)")


if __name__ == "__main__":
    main()
