"""Apply complete curriculum overhaul across all 4 stages (28 topics) and validate zero defects."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any
from pypinyin import pinyin as to_pinyin, Style

from curriculum_data_s1 import STAGE1_TOPICS
from curriculum_data_s2 import STAGE2_TOPICS
from curriculum_data_s3 import STAGE3_TOPICS
from curriculum_data_s4 import STAGE4_TOPICS, STAGE4_READINGS

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
STROKES_DIR = ROOT / "public" / "strokes"

# Comprehensive Traditional -> Simplified character map for cleaning any remaining Tatoeba examples
TRAD_TO_SIMP = str.maketrans({
    "們": "们", "這": "这", "來": "来", "時": "时", "對": "对", "說": "说", "問": "问",
    "麼": "么", "學": "学", "國": "国", "會": "会", "關": "关", "開": "开", "見": "见",
    "車": "车", "書": "书", "寫": "写", "聽": "听", "電": "电", "話": "话", "氣": "气",
    "進": "进", "點": "点", "還": "还", "現": "现", "經": "经", "樣": "样", "從": "从",
    "讓": "让", "給": "给", "當": "当", "後": "后", "裏": "里", "邊": "边", "體": "体",
    "師": "师", "習": "习", "歡": "欢", "樂": "乐", "錯": "错", "試": "试", "發": "发",
    "號": "号", "買": "买", "賣": "卖", "錢": "钱", "飯": "饭", "飲": "饮", "麵": "面",
    "條": "条", "覺": "觉", "請": "请", "嗎": "吗", "為": "为", "與": "与", "東": "东",
    "兩": "两", "嚴": "严", "豐": "丰", "臨": "临", "麗": "丽", "舉": "举", "義": "义",
    "鄉": "乡", "亂": "乱", "乾": "干", "爭": "争", "虧": "亏", "雲": "云", "亞": "亚",
    "親": "亲", "億": "亿", "僅": "仅", "僕": "仆", "儀": "仪", "價": "价", "眾": "众",
    "優": "优", "夥": "伙", "傘": "伞", "偉": "伟", "傳": "传", "傷": "伤", "倫": "伦",
    "偽": "伪", "個": "个", "備": "备", "傢": "家", "傭": "佣", "償": "偿", "儲": "储",
    "羅": "罗", "廣": "广", "廳": "厅", "應": "应", "實": "实", "將": "将", "專": "专",
    "尋": "寻", "導": "导", "層": "层", "歲": "岁", "島": "岛", "幣": "币", "帥": "帅",
    "帳": "账", "帶": "带", "幫": "帮", "幾": "几", "庫": "库", "廁": "厕", "廠": "厂",
    "張": "张", "強": "强", "彈": "弹", "歸": "归", "錄": "录", "復": "复", "徵": "征",
    "憶": "忆", "懷": "怀", "懸": "悬", "戀": "恋", "戲": "戏", "戰": "战", "執": "执",
    "擴": "扩", "掃": "扫", "揚": "扬", "換": "换", "揮": "挥", "損": "损", "搖": "摇",
    "搶": "抢", "攜": "携", "擺": "摆", "攤": "摊", "據": "据", "擠": "挤", "擬": "拟",
    "擲": "掷", "擾": "扰", "敘": "叙", "數": "数", "整": "整", "敵": "敌", "斷": "断",
    "無": "无", "舊": "旧", "暢": "畅", "暫": "暂", "曉": "晓", "歷": "历", "殘": "残",
    "殺": "杀", "毀": "毁", "畢": "毕", "漢": "汉", "溝": "沟", "溫": "温", "準": "准",
    "滾": "滚", "滿": "满", "漁": "渔", "漸": "渐", "潔": "洁", "潛": "潜", "潤": "润",
    "潮": "潮", "澤": "泽", "激": "激", "濃": "浓", "濕": "湿", "濟": "济", "濤": "涛",
    "濫": "滥", "濱": "滨", "熱": "热", "燈": "灯", "燒": "烧", "營": "营", "燦": "灿",
    "燭": "烛", "爛": "烂", "爾": "尔", "牆": "墙", "版": "版", "牽": "牵", "狀": "状",
    "猶": "犹", "狹": "狭", "獨": "独", "獄": "狱", "獅": "狮", "獎": "奖", "獻": "献",
    "獸": "兽", "獲": "获", "環": "环", "畫": "画", "異": "异", "疊": "叠", "療": "疗",
    "監": "监", "盤": "盘", "睜": "睁", "矯": "矫", "礦": "矿", "碼": "码", "磚": "砖",
    "礎": "础", "礙": "碍", "禮": "礼", "祥": "祥", "禍": "祸", "離": "离", "種": "种",
    "稱": "称", "穀": "谷", "積": "积", "穩": "稳", "穫": "获", "窮": "穷", "窗": "窗",
    "競": "竞", "筆": "笔", "築": "筑", "簽": "签", "簡": "简", "節": "节", "範": "范",
    "籃": "篮", "類": "类", "糧": "粮", "紀": "纪", "約": "约", "紅": "红", "納": "纳",
    "紙": "纸", "級": "级", "紛": "纷", "細": "细", "紳": "绅", "紹": "绍", "絡": "络",
    "絕": "绝", "統": "统", "絲": "丝", "綜": "综", "綠": "绿", "維": "维", "網": "网",
    "緊": "紧", "緒": "绪", "線": "线", "編": "编", "緣": "缘", "緩": "缓", "練": "练",
    "縛": "缚", "縣": "县", "縮": "缩", "縱": "纵", "總": "总", "績": "绩", "繁": "繁",
    "織": "织", "繞": "绕", "繪": "绘", "繳": "缴", "繼": "继", "罰": "罚", "罷": "罢",
    "罵": "骂", "群": "群", "羨": "羡", "翹": "翘", "聖": "圣", "聞": "闻", "聯": "联",
    "聰": "聪", "聲": "声", "職": "职", "肅": "肃", "勝": "胜", "脈": "脉", "脫": "脱",
    "脹": "胀", "臘": "腊", "腦": "脑", "腳": "脚", "騰": "腾", "臟": "脏", "興": "兴",
    "艦": "舰", "艱": "艰", "艷": "艳", "藝": "艺", "藥": "药", "莊": "庄", "萊": "莱",
    "華": "华", "萬": "万", "葉": "叶", "著": "着", "藍": "蓝", "蘋": "苹", "處": "处",
    "虛": "虚", "蠟": "蜡", "蟲": "虫", "衛": "卫", "衝": "冲", "裝": "装", "補": "补",
    "製": "制", "複": "复", "褲": "裤", "襪": "袜", "襲": "袭", "觀": "观", "規": "规",
    "視": "视", "覽": "览", "觸": "触", "計": "计", "訂": "订", "認": "认", "討": "讨",
    "訓": "训", "議": "议", "訊": "讯", "記": "记", "講": "讲", "許": "许", "論": "论",
    "設": "设", "訪": "访", "證": "证", "評": "评", "識": "识", "詐": "诈", "訴": "诉",
    "診": "诊", "詞": "词", "譯": "译", "詩": "诗", "誠": "诚", "誕": "诞", "詢": "询",
    "該": "该", "詳": "详", "語": "语", "誤": "误", "諸": "诸", "諾": "诺", "讀": "读",
    "課": "课", "誰": "谁", "調": "调", "諒": "谅", "談": "谈", "誼": "谊", "謀": "谋",
    "諧": "谐", "謂": "谓", "謎": "谜", "謝": "谢", "謙": "谦", "謹": "谨", "譜": "谱",
    "警": "警", "護": "护", "譽": "誉", "變": "变", "豐": "丰", "豎": "竖", "豬": "猪",
    "貓": "猫", "貝": "贝", "貞": "贞", "負": "负", "財": "财", "貢": "贡", "貧": "贫",
    "貨": "货", "販": "贩", "貪": "贪", "貫": "贯", "責": "责", "貴": "贵", "貶": "贬",
    "貸": "贷", "費": "费", "貼": "贴", "賀": "贺", "賃": "赁", "賄": "贿", "資": "资",
    "賈": "贾", "賊": "贼", "賓": "宾", "賜": "赐", "賞": "赏", "賠": "赔", "賢": "贤",
    "賤": "贱", "賦": "赋", "質": "质", "賭": "赌", "賴": "赖", "賺": "赚", "賽": "赛",
    "贈": "赠", "贊": "赞", "贏": "赢", "贖": "赎", "趙": "赵", "趕": "赶", "趨": "趋",
    "跡": "迹", "踐": "践", "踴": "踊", "躍": "跃", "軋": "轧", "軌": "轨", "軍": "军",
    "軒": "轩", "軟": "软", "較": "较", "載": "载", "輔": "辅", "輕": "轻", "輛": "辆",
    "輝": "辉", "輩": "辈", "輪": "轮", "輯": "辑", "輸": "输", "轉": "转", "轟": "轰",
    "辦": "办", "辭": "辞", "辯": "辩", "農": "农", "達": "达", "違": "违", "遙": "遥",
    "遜": "逊", "遞": "递", "遠": "远", "適": "适", "遭": "遭", "遮": "遮", "遲": "迟",
    "遷": "迁", "選": "选", "遺": "遗", "避": "避", "邁": "迈", "郵": "邮", "鄰": "邻",
    "鄭": "郑", "鄧": "邓", "醫": "医", "醬": "酱", "釀": "酿", "釋": "释", "針": "针",
    "釘": "钉", "釣": "钓", "鈍": "钝", "鈔": "钞", "鐘": "钟", "鈉": "钠", "鋼": "钢",
    "欽": "钦", "鈞": "钧", "鉤": "钩", "鈕": "钮", "鉗": "钳", "鑽": "钻", "鐵": "铁",
    "鈴": "铃", "鉛": "铅", "銀": "银", "銅": "铜", "銘": "铭", "銜": "衔", "銷": "销",
    "鋁": "铝", "鋒": "锋", "銳": "锐", "錨": "锚", "錫": "锡", "錦": "锦", "鍵": "键",
    "鍋": "锅", "鍛": "锻", "鎮": "镇", "鎖": "锁", "鏡": "镜", "鑒": "鉴", "長": "长",
    "門": "门", "閉": "闭", "閒": "闲", "間": "间", "閘": "闸", "閣": "阁", "閥": "阀",
    "閱": "阅", "闊": "阔", "陽": "阳", "陰": "阴", "陣": "阵", "階": "阶", "際": "际",
    "障": "障", "隱": "隐", "隻": "只", "雙": "双", "雜": "杂", "雞": "鸡", "難": "难",
    "雲": "云", "霧": "雾", "靈": "灵", "靜": "静", "鞏": "巩", "韋": "韦", "韓": "韩",
    "頁": "页", "頂": "顶", "項": "项", "順": "顺", "須": "须", "頑": "顽", "顧": "顾",
    "頓": "顿", "頒": "颁", "頌": "颂", "預": "预", "領": "领", "頗": "颇", "頸": "颈",
    "頻": "频", "顆": "颗", "題": "题", "額": "额", "顏": "颜", "願": "愿", "顛": "颠",
    "顯": "显", "風": "风", "飄": "飘", "飛": "飞", "飢": "饥", "飼": "饲", "飽": "饱",
    "飾": "饰", "餅": "饼", "養": "养", "餐": "餐", "餘": "余", "館": "馆", "馬": "马",
    "駁": "驳", "駐": "驻", "駕": "驾", "駛": "驶", "驗": "验", "騎": "骑", "騙": "骗",
    "騷": "骚", "驅": "驱", "驟": "骤", "髮": "发", "鬆": "松", "鬧": "闹", "鬱": "郁",
    "魅": "魅", "魚": "鱼", "魯": "鲁", "鮮": "鲜", "鯉": "鲤", "鯨": "鲸", "鳥": "鸟",
    "鳴": "鸣", "鴉": "鸦", "鴨": "鸭", "鴻": "鸿", "鵝": "鹅", "鷹": "鹰", "鹽": "盐",
    "麥": "麦", "黃": "黄", "黨": "党", "齊": "齐", "齒": "齿", "龍": "龙", "龜": "龟",
    "遊": "游", "繫": "系", "機": "机", "臺": "台", "甚": "什", "麽": "么", "裡": "里",
    "６": "6", "１": "1", "８": "8", "０": "0", "２": "2", "３": "3", "４": "4", "５": "5", "７": "7", "９": "9",
})

RADICAL_MEANINGS_VI = {
    "亻": "bộ nhân đứng (người)", "人": "bộ nhân (người)", "口": "bộ khẩu (miệng / lời nói)",
    "讠": "bộ ngôn (lời nói)", "女": "bộ nữ (phụ nữ)", "子": "bộ tử (trẻ con)",
    "日": "bộ nhật (mặt trời / thời gian)", "月": "bộ nguyệt (mặt trăng / cơ thể)",
    "木": "bộ mộc (cây gỗ)", "水": "bộ thủy (nước)", "氵": "bộ chấm thủy (nước)",
    "火": "bộ hỏa (lửa / nhiệt)", "灬": "bộ hỏa bốn chấm (lửa / nóng)",
    "心": "bộ tâm (trái tim / cảm xúc)", "忄": "bộ tâm đứng (cảm xúc / suy nghĩ)",
    "手": "bộ thủ (bàn tay)", "扌": "bộ tài gẩy (hành động bằng tay)",
    "足": "bộ túc (bàn chân / di chuyển)", "走": "bộ tẩu (bước đi)",
    "辶": "bộ xước (con đường / di chuyển)", "宀": "bộ miên (mái nhà)",
    "艹": "bộ thảo (cây cỏ / thực vật)", "竹": "bộ trúc (tre trúc)",
    "钅": "bộ kim (kim loại / tiền tệ)", "贝": "bộ bối (vỏ sò / tài sản)",
    "土": "bộ thổ (đất đai)", "山": "bộ sơn (núi)", "雨": "bộ vũ (mưa / thời tiết)",
    "冫": "bộ băng (băng giá / lạnh)", "疒": "bộ nạch (bệnh tật)",
    "目": "bộ mục (đôi mắt)", "耳": "bộ nhĩ (đôi tai)", "门": "bộ môn (cánh cửa)",
    "车": "bộ xa (xe cộ)", "食": "bộ thực (thức ăn)", "饣": "bộ thực (ăn uống)",
    "纟": "bộ mịch (sợi tơ / kết nối)", "糸": "bộ mịch (sợi tơ / kết nối)",
    "力": "bộ lực (sức mạnh)", "刀": "bộ đao (con dao)", "刂": "bộ đao đứng (cắt / chia)",
    "禾": "bộ hòa (cây lúa)", "田": "bộ điền (ruộng / khung)", "广": "bộ nghiễm (mái che)",
    "见": "bộ kiến (nhìn thấy)", "页": "bộ hiệt (đầu / trang giấy)", "风": "bộ phong (gió)",
    "示": "bộ thị (nghi lễ)", "礻": "bộ thị (lễ nghi / chúc phúc)", "衣": "bộ y (trang phục)",
    "衤": "bộ y (quần áo)", "马": "bộ mã (con ngựa)", "鸟": "bộ điểu (chim)",
    "鱼": "bộ ngư (cá)", "王": "bộ ngọc (viên ngọc quý)", "石": "bộ thạch (đá)",
    "米": "bộ mễ (gạo)", "白": "bộ bạch (màu trắng)", "大": "bộ đại (to lớn)",
    "小": "bộ tiểu (nhỏ bé)", "一": "nét nhất căn bản", "十": "nét thập",
}

SURNAME_RE = re.compile(r"(?:^|,\s*)họ\s+[A-ZĐÀ-Ỹ][a-zà-ỹ]*(?:,\s*|$)", re.UNICODE)
CJK_RE = re.compile(r"[\u4e00-\u9fff]+")


def clean_meaning_vi(meaning: str) -> str:
    cleaned = SURNAME_RE.sub(", ", meaning).strip(" ,;")
    cleaned = re.sub(r",\s*,+", ", ", cleaned).strip(" ,;")
    return cleaned or meaning


def to_pinyin_str(text: str) -> str:
    parts = to_pinyin(text, style=Style.TONE, errors="default")
    return " ".join(p[0] for p in parts if p and p[0].strip())


def strip_tones(py: str) -> str:
    table = str.maketrans(
        "āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü",
        "aaaaeeeeiiiioooouuuuvvvvv",
    )
    return re.sub(r"[^a-z0-9]", "", py.lower().translate(table))


def tokenize_reading_paragraph(hanzi: str, new_words: list[str], known_words: dict[str, str]) -> list[dict[str, Any]]:
    """Segment a Chinese paragraph cleanly into tokens with accurate pinyin and isNew markers."""
    vocab = sorted(set(new_words) | set(known_words.keys()), key=len, reverse=True)
    new_set = set(new_words)
    tokens: list[dict[str, Any]] = []
    i = 0
    n = len(hanzi)
    while i < n:
        ch = hanzi[i]
        # ASCII run (like "Bao" or "Wi-Fi")
        if ch.isascii() and ch.isalnum():
            j = i + 1
            while j < n and (hanzi[j].isascii() and (hanzi[j].isalnum() or hanzi[j] == "-")):
                j += 1
            tokens.append({"w": hanzi[i:j], "pinyin": ""})
            i = j
            continue
        # Punctuation / non-CJK
        if not ("\u4e00" <= ch <= "\u9fff"):
            j = i + 1
            while j < n and not ("\u4e00" <= hanzi[j] <= "\u9fff") and not (hanzi[j].isascii() and hanzi[j].isalnum()):
                j += 1
            tokens.append({"w": hanzi[i:j], "pinyin": ""})
            i = j
            continue
        # Greedy longest match from known vocab
        matched = None
        for w in vocab:
            if len(w) >= 1 and hanzi.startswith(w, i):
                matched = w
                break
        if matched:
            py = known_words.get(matched) or to_pinyin_str(matched)
            tok: dict[str, Any] = {"w": matched, "pinyin": py}
            if matched in new_set:
                tok["isNew"] = True
            tokens.append(tok)
            i += len(matched)
        else:
            py = to_pinyin_str(ch)
            tok = {"w": ch, "pinyin": py}
            if ch in new_set:
                tok["isNew"] = True
            tokens.append(tok)
            i += 1
    return tokens


def build_listening_lesson(topic: dict[str, Any], stage: int, word_ids: list[str]) -> dict[str, Any]:
    """Generate a cohesive, 100% accurate 6-exercise Listening lesson synced with the topic."""
    tid = topic["topicId"]
    ws = topic["words"]
    pats = topic["patterns"]
    dlg = topic["dialogue"]

    w0, w1, w2, w3 = ws[0], ws[1], ws[2], ws[3]
    w4 = ws[4] if len(ws) > 4 else ws[0]
    w5 = ws[5] if len(ws) > 5 else ws[1]

    # Pick a clean dialogue/pattern sentence for tiles
    tile_ex = next((e for e in topic["exercises"] if e["kind"] == "sentence-tiles"), None)
    tile_ans = tile_ex["answer"] if tile_ex else pats[0]["exampleHanzi"].rstrip("。！？!")
    tiles_shuffled = list(tile_ex["tiles"]) if tile_ex else list(tile_ans)

    # Pick pattern 0 for listen-blank
    p0 = pats[0]
    blank_ans = p0["slots"]["answerHanzi"]
    blank_full = p0["frame"].replace("___", blank_ans)
    blank_opts = [{"label": c["hanzi"], "value": c["hanzi"]} for c in p0["slots"]["choices"]]
    if len(blank_opts) < 4:
        for cand in ws:
            if cand["hanzi"] not in {o["value"] for o in blank_opts}:
                blank_opts.append({"label": cand["hanzi"], "value": cand["hanzi"]})
                break

    # Pick dialogue line 0 or 1 for listen-dialogue comprehension
    d_turn = dlg[1] if len(dlg) > 1 else dlg[0]
    distractors = [
        w2["examples"][0]["vi"],
        w4["examples"][0]["vi"],
        w5["examples"][0]["vi"],
    ]
    # Ensure distinct distractors
    dlg_opts = [{"label": d_turn["vi"], "value": d_turn["vi"]}]
    for d in distractors:
        if d != d_turn["vi"] and d not in {o["value"] for o in dlg_opts}:
            dlg_opts.append({"label": d, "value": d})
        if len(dlg_opts) == 3:
            break

    # Short dictation from 2 core words
    dict_text = f"{w0['hanzi']}，{w1['hanzi']}"
    dict_ans = strip_tones(f"{w0['pinyin']} {w1['pinyin']}")

    exercises = [
        {
            "id": f"ng{tid}-1",
            "kind": "listen-meaning",
            "promptVi": "Nghe từ vựng sau và chọn nghĩa tiếng Việt đúng:",
            "audioText": w0["hanzi"],
            "options": [
                {"label": w0["meaningVi"].capitalize(), "value": w0["meaningVi"].capitalize()},
                {"label": w1["meaningVi"].capitalize(), "value": w1["meaningVi"].capitalize()},
                {"label": w2["meaningVi"].capitalize(), "value": w2["meaningVi"].capitalize()},
                {"label": w3["meaningVi"].capitalize(), "value": w3["meaningVi"].capitalize()},
            ],
            "answer": w0["meaningVi"].capitalize(),
            "explainVi": f"{w0['hanzi']} ({w0['pinyin']}) = {w0['meaningVi']}.",
        },
        {
            "id": f"ng{tid}-2",
            "kind": "listen-hanzi",
            "promptVi": "Nghe âm thanh và chọn đúng chữ Hán:",
            "audioText": w2["hanzi"],
            "options": [
                {"label": w1["hanzi"], "value": w1["hanzi"]},
                {"label": w2["hanzi"], "value": w2["hanzi"]},
                {"label": w3["hanzi"], "value": w3["hanzi"]},
                {"label": w4["hanzi"], "value": w4["hanzi"]},
            ],
            "answer": w2["hanzi"],
            "explainVi": f"{w2['hanzi']} ({w2['pinyin']}) = {w2['meaningVi']}.",
        },
        {
            "id": f"ng{tid}-3",
            "kind": "listen-tiles",
            "promptVi": "Nghe câu hoàn chỉnh và chạm thẻ theo đúng thứ tự:",
            "audioText": tile_ans,
            "tiles": tiles_shuffled,
            "answer": tile_ans,
            "explainVi": f"Câu đúng: {tile_ans}.",
        },
        {
            "id": f"ng{tid}-4",
            "kind": "listen-blank",
            "promptVi": f"Nghe và điền từ còn thiếu: 「{p0['frame']}」",
            "audioText": blank_full,
            "options": blank_opts,
            "answer": blank_ans,
            "explainVi": f"Câu đầy đủ: {blank_full} ({p0['exampleVi']}).",
        },
        {
            "id": f"ng{tid}-5",
            "kind": "listen-dialogue",
            "promptVi": "Nghe câu hội thoại trong bài và chọn ý nghĩa chính xác:",
            "audioText": d_turn["hanzi"],
            "options": dlg_opts,
            "answer": d_turn["vi"],
            "explainVi": f"{d_turn['hanzi']} ({d_turn['pinyin']})",
        },
        {
            "id": f"ng{tid}-6",
            "kind": "dictation",
            "promptVi": "Chép chính tả nhanh: gõ pinyin không dấu (hoặc bấm thẻ chữ) theo âm thanh:",
            "audioText": dict_text,
            "tiles": [w0["hanzi"], w1["hanzi"]],
            "answer": dict_ans,
            "explainVi": f"{dict_text} ({w0['pinyin']}, {w1['pinyin']})",
        },
    ]

    return {
        "id": f"t{tid}-nghe",
        "stage": stage,
        "topicId": tid,
        "title": f"Nghe: {topic['title']}",
        "type": "nghe",
        "xp": 25 + (stage - 1) * 5,
        "coinReward": 30 + (stage - 1) * 5,
        "newWords": word_ids,
        "listeningTracks": [
            {
                "id": f"tr-{tid}-{i+1}",
                "speaker": t["speaker"],
                "hanzi": t["hanzi"],
                "pinyin": t["pinyin"],
                "vi": t["vi"],
                "voiceRole": t.get("voiceRole", "female"),
            }
            for i, t in enumerate(dlg[:4])
        ],
        "exercises": exercises,
    }


def build_writing_lesson(topic: dict[str, Any], stage: int, word_ids: list[str]) -> dict[str, Any]:
    tid = topic["topicId"]
    return {
        "id": f"t{tid}-viet",
        "stage": stage,
        "topicId": tid,
        "title": f"Viết: {topic['title']}",
        "type": "viet",
        "xp": 25 + (stage - 1) * 5,
        "coinReward": 30 + (stage - 1) * 5,
        "newWords": word_ids,
        "writingChars": topic["writing"],
    }


def build_stage4_test() -> dict[str, Any]:
    """Rebuild stage-4-test so all 8 items accurately test the rebuilt Stage 4 topics 25-28."""
    return {
        "id": "stage-4-test",
        "stage": 4,
        "topicId": 28,
        "title": "Kiểm tra Chặng 4 — Tự tin giao tiếp",
        "type": "stage-test",
        "xp": 60,
        "coinReward": 100,
        "newWords": [],
        "stageTestItems": [
            {
                "id": "st4-1", "skill": "giao-tiep",
                "promptVi": "Khi muốn phản đối nhẹ nhàng và lịch sự trong buổi thảo luận, câu nào tự nhiên nhất?",
                "passageHanzi": "你觉得我们把活动改到周日怎么样？",
                "passagePinyin": "nǐ jué de wǒ men bǎ huó dòng gǎi dào zhōu rì zěn me yàng?",
                "options": [
                    {"label": "你说得很有道理，不过周六大家时间更方便。", "value": "你说得很有道理，不过周六大家时间更方便。"},
                    {"label": "你完全错了，我不听。", "value": "你完全错了，我不听。"},
                    {"label": "这个杯子三十块。", "value": "这个杯子三十块。"},
                    {"label": "今天天气真冷。", "value": "今天天气真冷。"},
                ],
                "answer": "你说得很有道理，不过周六大家时间更方便。",
                "explainVi": "Dùng 「有道理，不过…」 giúp ghi nhận đối phương trước khi nêu góp ý riêng.",
            },
            {
                "id": "st4-2", "skill": "giao-tiep",
                "promptVi": "Chọn câu nói ĐÚNG ngữ pháp khi nhờ ai đó giúp một việc:",
                "options": [
                    {"label": "不好意思，麻烦你帮我一个忙可以吗？", "value": "不好意思，麻烦你帮我一个忙可以吗？"},
                    {"label": "不好意思，请你帮忙我可以吗？", "value": "不好意思，请你帮忙我可以吗？"},
                    {"label": "请把帮忙给我。", "value": "请把帮忙给我。"},
                    {"label": "我反对你帮忙。", "value": "我反对你帮忙。"},
                ],
                "answer": "不好意思，麻烦你帮我一个忙可以吗？",
                "explainVi": "帮忙 là động từ ly hợp: phải tách thành 帮我(一个)忙, không nói 帮忙我.",
            },
            {
                "id": "st4-3", "skill": "doc",
                "promptVi": "Đọc đoạn ngắn: Bao cho rằng điều gì giúp thực hiện được ước mơ?",
                "passageHanzi": "为了实现未来的梦想，Bao每天都用智能软件坚持练习中文。他认为只要坚持努力，就一定能提高效率，实现目标。",
                "passagePinyin": "wèi le shí xiàn wèi lái de mèng xiǎng, Bao měi tiān dōu yòng zhì néng ruǎn jiàn jiān chí liàn xí Zhōng wén. tā rèn wéi zhǐ yào jiān chí nǔ lì, jiù yí dìng néng tí gāo xiào lǜ, shí xiàn mù biāo.",
                "options": [
                    {"label": "Chỉ cần kiên trì nỗ lực mỗi ngày", "value": "Chỉ cần kiên trì nỗ lực mỗi ngày"},
                    {"label": "Không cần ôn tập từ mới", "value": "Không cần ôn tập từ mới"},
                    {"label": "Chỉ dựa vào may mắn", "value": "Chỉ dựa vào may mắn"},
                    {"label": "Đổi mục tiêu mỗi tuần", "value": "Đổi mục tiêu mỗi tuần"},
                ],
                "answer": "Chỉ cần kiên trì nỗ lực mỗi ngày",
                "explainVi": "Câu cuối nêu rõ: 「只要坚持努力，就一定能提高效率，实现目标」.",
            },
            {
                "id": "st4-4", "skill": "doc",
                "promptVi": "Đọc thông báo: Gặp tình huống khẩn cấp ở hội chợ nên làm gì trước tiên?",
                "passageHanzi": "遇到紧急情况时，请大家先保持冷静，不要慌张，及时联系工作人员一起想办法解决。",
                "passagePinyin": "yù dào jǐn jí qíng kuàng shí, qǐng dà jiā xiān bǎo chí lěng jìng, bú yào huāng zhāng, jí shí lián xì gōng zuò rén yuán yì qǐ xiǎng bàn fǎ jiě jué.",
                "options": [
                    {"label": "Giữ bình tĩnh và liên hệ kịp thời với nhân viên", "value": "Giữ bình tĩnh và liên hệ kịp thời với nhân viên"},
                    {"label": "Rời khỏi hội chợ ngay lập tức không báo ai", "value": "Rời khỏi hội chợ ngay lập tức không báo ai"},
                    {"label": "Đợi hết buổi hội chợ mới xử lý", "value": "Đợi hết buổi hội chợ mới xử lý"},
                    {"label": "Tắt điện thoại để tiết kiệm pin", "value": "Tắt điện thoại để tiết kiệm pin"},
                ],
                "answer": "Giữ bình tĩnh và liên hệ kịp thời với nhân viên",
                "explainVi": "「先保持冷静…及时联系工作人员」 = giữ bình tĩnh trước và liên hệ nhân viên kịp thời.",
            },
            {
                "id": "st4-5", "skill": "nghe",
                "promptVi": "Nghe câu sau và chọn ý đúng:",
                "audioText": "只要坚持努力，就一定能实现梦想！",
                "options": [
                    {"label": "Chỉ cần kiên trì nỗ lực thì nhất định thực hiện được ước mơ!", "value": "Chỉ cần kiên trì nỗ lực thì nhất định thực hiện được ước mơ!"},
                    {"label": "Hôm nay trời mưa nên hủy cuộc họp.", "value": "Hôm nay trời mưa nên hủy cuộc họp."},
                    {"label": "Mình hoàn toàn phản đối quan điểm này.", "value": "Mình hoàn toàn phản đối quan điểm này."},
                    {"label": "Xin lỗi, mình quên mang theo dữ liệu rồi.", "value": "Xin lỗi, mình quên mang theo dữ liệu rồi."},
                ],
                "answer": "Chỉ cần kiên trì nỗ lực thì nhất định thực hiện được ước mơ!",
                "explainVi": "只要坚持努力，就一定能实现梦想！",
            },
            {
                "id": "st4-6", "skill": "nghe",
                "promptVi": "Nghe đoạn audio: Phần mềm thông minh giúp ích điều gì?",
                "audioText": "这款人工智能软件把学习效率提高了很多。",
                "options": [
                    {"label": "Nâng cao hiệu suất học tập lên rất nhiều", "value": "Nâng cao hiệu suất học tập lên rất nhiều"},
                    {"label": "Làm điện thoại chạy chậm hơn", "value": "Làm điện thoại chạy chậm hơn"},
                    {"label": "Đặt vé máy bay giá rẻ", "value": "Đặt vé máy bay giá rẻ"},
                    {"label": "Gọi trà sữa giao tận nhà", "value": "Gọi trà sữa giao tận nhà"},
                ],
                "answer": "Nâng cao hiệu suất học tập lên rất nhiều",
                "explainVi": "「把学习效率提高了很多」 = đã nâng cao hiệu suất học tập rất nhiều.",
            },
            {
                "id": "st4-7", "skill": "viet",
                "promptVi": "Tập viết đúng thứ tự nét chữ 「梦」 (giấc mơ — trong 梦想):",
                "writingChar": {
                    "char": "梦", "pinyin": "mèng", "meaningVi": "giấc mơ", "radical": "木",
                    "radicalNoteVi": "Khu rừng (林) trong màn đêm (夕) — giấc mơ ngọt ngào.",
                    "lookalikes": [
                        {"hanzi": "梦", "pinyin": "mèng", "vi": "giấc mơ"},
                        {"hanzi": "林", "pinyin": "lín", "vi": "rừng"},
                        {"hanzi": "想", "pinyin": "xiǎng", "vi": "nghĩ"},
                        {"hanzi": "多", "pinyin": "duō", "vi": "nhiều"},
                    ],
                },
                "answer": "梦",
                "explainVi": "梦 (mèng) nằm trong 梦想 (ước mơ).",
            },
            {
                "id": "st4-8", "skill": "viet",
                "promptVi": "Chọn chữ Hán đúng nghĩa 'bình tĩnh' (lěng jìng):",
                "options": [
                    {"label": "冷静", "value": "冷静"},
                    {"label": "紧急", "value": "紧急"},
                    {"label": "原谅", "value": "原谅"},
                    {"label": "效率", "value": "效率"},
                ],
                "answer": "冷静",
                "explainVi": "冷静 (lěng jìng) = bình tĩnh.",
            },
        ],
    }


def main() -> None:
    radicals_bundle = json.loads((CONTENT_DIR / "radicals.json").read_text(encoding="utf-8"))
    char_radicals = radicals_bundle.get("characters", {})
    curriculum = json.loads((CONTENT_DIR / "curriculum.json").read_text(encoding="utf-8"))

    all_stage_topics = {
        1: STAGE1_TOPICS,
        2: STAGE2_TOPICS,
        3: STAGE3_TOPICS,
        4: STAGE4_TOPICS,
    }

    # Global hanzi -> id lookup across stages for recapWordIds
    global_word_id: dict[str, str] = {}
    global_word_pinyin: dict[str, str] = {}

    for stage_num in [1, 2, 3, 4]:
        stage_dir = CONTENT_DIR / f"stage-{stage_num}"
        words: list[dict[str, Any]] = json.loads((stage_dir / "words.json").read_text(encoding="utf-8"))
        lessons: list[dict[str, Any]] = json.loads((stage_dir / "lessons.json").read_text(encoding="utf-8"))
        readings: list[dict[str, Any]] = json.loads((stage_dir / "readings.json").read_text(encoding="utf-8"))

        # 1) Sanitize ALL existing words in this stage
        word_by_hanzi: dict[str, dict[str, Any]] = {}
        for w in words:
            w["meaningVi"] = clean_meaning_vi(w.get("meaningVi", ""))
            # Ensure radical
            if not w.get("radical"):
                first_ch = next((c for c in w["hanzi"] if "\u4e00" <= c <= "\u9fff"), "")
                w["radical"] = char_radicals.get(first_ch, {}).get("radical", first_ch)
            # Clean Traditional Chinese in examples
            for ex in w.get("examples", []):
                ex["hanzi"] = ex["hanzi"].translate(TRAD_TO_SIMP)
            # Ensure mnemonic
            if not w.get("mnemonic"):
                rad = w.get("radical", "")
                rad_desc = RADICAL_MEANINGS_VI.get(rad, f"bộ {rad}" if rad else "cấu trúc chữ")
                w["mnemonic"] = f"Gắn với {rad_desc}, ghi nhớ cụm 「{w['hanzi']}」 ({w['pinyin']}) = {w['meaningVi']}."
            word_by_hanzi[w["hanzi"]] = w

        # 2) Upsert all hand-curated topic words into this stage's words.json
        next_custom_idx = 1
        topic_word_ids: dict[int, list[str]] = {}
        for topic in all_stage_topics[stage_num]:
            tid = topic["topicId"]
            ids_for_topic: list[str] = []
            for cw in topic["words"]:
                hz = cw["hanzi"]
                if hz in word_by_hanzi:
                    target = word_by_hanzi[hz]
                else:
                    wid = f"w{stage_num}-c{next_custom_idx:03d}"
                    next_custom_idx += 1
                    target = {
                        "id": wid,
                        "hanzi": hz,
                        "level": min(3, stage_num),
                        "frequency": 500 + next_custom_idx,
                    }
                    words.append(target)
                    word_by_hanzi[hz] = target

                target["pinyin"] = cw["pinyin"]
                target["meaningVi"] = cw["meaningVi"]
                target["radical"] = cw["radical"]
                target["mnemonic"] = cw["mnemonic"]
                target["literalVi"] = cw.get("literalVi", "")
                target["usageNoteVi"] = cw.get("usageNoteVi", "")
                target["partOfSpeech"] = cw.get("pos", "")
                target["examples"] = [
                    {"hanzi": ex["hanzi"], "pinyin": ex["pinyin"], "vi": ex["vi"]}
                    for ex in cw["examples"]
                ]
                ids_for_topic.append(target["id"])
                global_word_id[hz] = target["id"]
                global_word_pinyin[hz] = target["pinyin"]
            topic_word_ids[tid] = ids_for_topic

        for w in words:
            global_word_id.setdefault(w["hanzi"], w["id"])
            global_word_pinyin.setdefault(w["hanzi"], w["pinyin"])

        # 3) Rebuild lessons for every topic in this stage
        lesson_by_id = {l["id"]: l for l in lessons}
        new_lessons: list[dict[str, Any]] = []

        for topic in all_stage_topics[stage_num]:
            tid = topic["topicId"]
            w_ids = topic_word_ids[tid]
            recap_ids = [global_word_id[h] for h in topic.get("recapWordIds", []) if h in global_word_id]

            gt_lesson = {
                "id": f"t{tid}-giao-tiep",
                "stage": stage_num,
                "topicId": tid,
                "title": topic["title"],
                "type": "giao-tiep",
                "xp": 30 + (stage_num - 1) * 5,
                "coinReward": 40 + (stage_num - 1) * 5,
                "storyContextVi": topic["storyContextVi"],
                "bridgeFromPrevVi": topic["bridgeFromPrevVi"],
                "bridgeToNextVi": topic["bridgeToNextVi"],
                "recapWordIds": recap_ids,
                "grammarSpotlight": topic["grammarSpotlight"],
                "cultureTipVi": topic["cultureTipVi"],
                "newWords": w_ids,
                "patterns": topic["patterns"],
                "dialogue": topic["dialogue"],
                "exercises": topic["exercises"],
                "roleplay": topic["roleplay"],
            }
            new_lessons.append(gt_lesson)

            # Reading lesson pointer
            old_doc = lesson_by_id.get(f"t{tid}-doc", {})
            doc_lesson = {
                "id": f"t{tid}-doc",
                "stage": stage_num,
                "topicId": tid,
                "title": old_doc.get("title", f"Đọc: {topic['title']}"),
                "type": "doc",
                "xp": 25 + (stage_num - 1) * 5,
                "coinReward": 30 + (stage_num - 1) * 5,
                "newWords": [],
                "readingId": f"r-t{tid}",
            }
            if stage_num == 4:
                r4_match = next((r for r in STAGE4_READINGS if r["id"] == f"r-t{tid}"), None)
                if r4_match:
                    doc_lesson["title"] = f"Đọc: {r4_match['title']}"
            new_lessons.append(doc_lesson)

            # Listening lesson synced to curated topic
            new_lessons.append(build_listening_lesson(topic, stage_num, w_ids))

            # Writing lesson synced to curated topic
            new_lessons.append(build_writing_lesson(topic, stage_num, w_ids))

        # Keep or rebuild stage-test
        st_id = f"stage-{stage_num}-test"
        if stage_num == 4:
            new_lessons.append(build_stage4_test())
        elif st_id in lesson_by_id:
            st_obj = lesson_by_id[st_id]
            st_obj["coinReward"] = 100
            new_lessons.append(st_obj)

        # 4) Sanitize readings (and replace Stage 4 topic readings r-t25..r-t28)
        if stage_num == 4:
            story_c4 = next((r for r in readings if r["id"] == "story-c4"), None)
            rebuilt_r4: list[dict[str, Any]] = []
            for r_spec in STAGE4_READINGS:
                paras = []
                for p in r_spec["paragraphs"]:
                    paras.append({
                        "hanzi": p["hanzi"],
                        "vi": p["vi"],
                        "tokens": tokenize_reading_paragraph(p["hanzi"], r_spec["newWords"], global_word_pinyin),
                    })
                rebuilt_r4.append({
                    "id": r_spec["id"],
                    "stage": 4,
                    "topicId": r_spec["topicId"],
                    "title": r_spec["title"],
                    "mode": r_spec["mode"],
                    "knownPercent": r_spec["knownPercent"],
                    "newWords": r_spec["newWords"],
                    "paragraphs": paras,
                    "questions": r_spec["questions"],
                })
            if story_c4:
                for p in story_c4.get("paragraphs", []):
                    p["hanzi"] = p["hanzi"].translate(TRAD_TO_SIMP)
                    for tok in p.get("tokens", []):
                        tok["w"] = tok["w"].translate(TRAD_TO_SIMP)
                rebuilt_r4.append(story_c4)
            readings = rebuilt_r4
        else:
            for r in readings:
                for p in r.get("paragraphs", []):
                    p["hanzi"] = p["hanzi"].translate(TRAD_TO_SIMP)
                    for tok in p.get("tokens", []):
                        tok["w"] = tok["w"].translate(TRAD_TO_SIMP)

        # 5) Update curriculum.json metadata for this stage
        stage_meta = next(s for s in curriculum["stages"] if s["id"] == stage_num)
        for topic in all_stage_topics[stage_num]:
            tm = next(t for t in stage_meta["topics"] if t["id"] == topic["topicId"])
            tm["title"] = topic["title"]
            tm["subtitle"] = topic["subtitle"]
            tm["storyTagVi"] = topic["storyTagVi"]
            tm["connectsFromVi"] = topic["connectsFromVi"]

        # Write stage files
        (stage_dir / "words.json").write_text(json.dumps(words, ensure_ascii=False, indent=2), encoding="utf-8")
        (stage_dir / "lessons.json").write_text(json.dumps(new_lessons, ensure_ascii=False, indent=2), encoding="utf-8")
        (stage_dir / "readings.json").write_text(json.dumps(readings, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Updated Stage {stage_num}: {len(words)} words, {len(new_lessons)} lessons, {len(readings)} readings.")

    (CONTENT_DIR / "curriculum.json").write_text(json.dumps(curriculum, ensure_ascii=False, indent=2), encoding="utf-8")

    # 6) Strict automated validation
    strict_trad = set("們這來時對說問麼學國會關開見車書寫聽電話氣進點還現經樣從讓給當後裏邊體師習歡樂錯試發號買賣錢飯飲麵條覺請嗎為與東兩嚴豐臨麗舉義鄉買亂乾爭虧雲亞親億僅僕從儀價眾優夥傘偉傳傷倫偽個備傢傭償儲羅")
    errors = []
    for s in [1, 2, 3, 4]:
        words = json.loads((CONTENT_DIR / f"stage-{s}/words.json").read_text(encoding="utf-8"))
        lessons = json.loads((CONTENT_DIR / f"stage-{s}/lessons.json").read_text(encoding="utf-8"))
        readings = json.loads((CONTENT_DIR / f"stage-{s}/readings.json").read_text(encoding="utf-8"))
        wmap = {w["id"]: w for w in words}

        for w in words:
            if not w.get("mnemonic"):
                errors.append(f"Stage {s} word {w['hanzi']} missing mnemonic")
            if not w.get("radical"):
                errors.append(f"Stage {s} word {w['hanzi']} missing radical")
            for ex in w.get("examples", []):
                bad = [c for c in ex["hanzi"] if c in strict_trad]
                if bad:
                    errors.append(f"Stage {s} word {w['hanzi']} example has trad chars {bad}: {ex['hanzi']}")

        seen_in_stage: dict[str, str] = {}
        for l in lessons:
            if l["type"] == "giao-tiep":
                for wid in l["newWords"]:
                    hz = wmap[wid]["hanzi"]
                    if hz in seen_in_stage:
                        errors.append(f"Stage {s} duplicate newWord {hz} in {seen_in_stage[hz]} and {l['id']}")
                    seen_in_stage[hz] = l["id"]
                if not l.get("grammarSpotlight") or not l.get("storyContextVi"):
                    errors.append(f"Lesson {l['id']} missing grammarSpotlight or storyContextVi")
            if l["type"] == "viet":
                for wc in l.get("writingChars", []):
                    if not (STROKES_DIR / f"{wc['char']}.json").exists():
                        errors.append(f"Missing stroke file for {wc['char']} in {l['id']}")
            if l["type"] == "stage-test":
                for it in l.get("stageTestItems", []):
                    if it.get("writingChar"):
                        ch = it["writingChar"]["char"]
                        if not (STROKES_DIR / f"{ch}.json").exists():
                            errors.append(f"Missing stroke file for {ch} in {l['id']}")

        for r in readings:
            for p in r.get("paragraphs", []):
                bad = [c for c in p["hanzi"] if c in strict_trad]
                if bad:
                    errors.append(f"Stage {s} reading {r['id']} has trad chars {bad}")

        raw_bundle = json.dumps({"w": words, "l": lessons, "r": readings}, ensure_ascii=False)
        if "HSK" in raw_bundle:
            errors.append(f"Stage {s} contains forbidden string 'HSK'")

    if errors:
        print(f"VALIDATION FAILED with {len(errors)} errors:")
        for e in errors[:20]:
            print("  -", e)
        raise SystemExit(1)
    print("ALL VALIDATION CHECKS PASSED WITH ZERO ERRORS!")


if __name__ == "__main__":
    main()
