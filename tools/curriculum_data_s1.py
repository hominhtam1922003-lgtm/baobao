"""Hand-curated, 100% accurate, cohesive Stage 1 (Topics 1-8) curriculum data for BaoBao."""

STAGE1_TOPICS = [
    {
        "topicId": 1,
        "title": "Chào hỏi & tạm biệt",
        "subtitle": "Làm quen, cảm ơn, xin lỗi tự nhiên ngay ngày đầu",
        "storyTagVi": "Ngày 1 · Bước vào lớp tiếng Trung",
        "connectsFromVi": "Khởi đầu hành trình cùng gấu trúc Bao",
        "storyContextVi": "Sáng đầu tiên tới lớp tiếng Trung ở phố cổ, Bao hơi hồi hộp nhưng sẵn sàng chào cô Vương và cô bạn bàn bên tên Linh!",
        "bridgeFromPrevVi": "Bắt đầu từ con số 0: chỉ cần 8 cụm từ vàng này, bạn đã có thể mở lời lịch sự với bất kỳ ai ở Trung Quốc!",
        "bridgeToNextVi": "Sau khi chào hỏi xong, ở Bài 2 Bao sẽ giới thiệu tên và quốc tịch Việt Nam với Linh!",
        "recapWordIds": [],
        "cultureTipVi": "Người Trung Quốc thường chào buổi sáng ngắn gọn là 「早！」(Zǎo!) với bạn thân, còn với thầy cô hay người lớn tuổi sẽ nói 「您好！」(Nín hǎo!) hoặc 「老师好！」(Lǎoshī hǎo!).",
        "grammarSpotlight": {
            "title": "Cách chào bằng 「___好！」 và đáp lời lịch sự",
            "formula": "Đối tượng / Thời điểm + 好！",
            "explainVi": "Đặt tên người, chức danh hoặc buổi trong ngày trước chữ 好 (hǎo = tốt) để tạo lời chào tự nhiên.",
            "vsVietnameseVi": "Ngược trật tự với tiếng Việt: tiếng Việt nói 'Chào cô' (Chào + Cô), còn tiếng Trung đặt 'Cô' lên trước: 老师好！",
            "commonMistakeVi": "Tránh dịch từng chữ '你好老师' — người bản xứ luôn nói 「老师好！」 hoặc 「老师，您好！」.",
            "examples": [
                {"hanzi": "老师好！", "pinyin": "lǎo shī hǎo!", "vi": "Em chào thầy/cô ạ!"},
                {"hanzi": "大家早上好！", "pinyin": "dà jiā zǎo shang hǎo!", "vi": "Chào buổi sáng mọi người!"},
            ],
        },
        "words": [
            {
                "hanzi": "你好", "pinyin": "nǐ hǎo", "meaningVi": "xin chào", "pos": "Cụm giao tiếp",
                "radical": "亻", "literalVi": "你 (bạn) + 好 (tốt lành)",
                "mnemonic": "Hai người (亻) gặp nhau chúc điều tốt đẹp (好 = mẹ 女 bế con 子).",
                "usageNoteVi": "Biến điệu thanh 3: hai thanh 3 đi liền (nǐ + hǎo) đọc thành ní hǎo cho êm miệng!",
                "examples": [
                    {"hanzi": "你好！我是Bao。", "pinyin": "nǐ hǎo! wǒ shì Bao.", "vi": "Xin chào! Mình là Bao."},
                    {"hanzi": "你好，很高兴见到你！", "pinyin": "nǐ hǎo, hěn gāo xìng jiàn dào nǐ!", "vi": "Xin chào, rất vui được gặp bạn!"},
                ],
            },
            {
                "hanzi": "早上好", "pinyin": "zǎo shang hǎo", "meaningVi": "chào buổi sáng", "pos": "Cụm giao tiếp",
                "radical": "日", "literalVi": "早上 (buổi sáng) + 好 (tốt)",
                "mnemonic": "早 có mặt trời (日) vừa nhô lên trên đường chân trời (十) — trời sáng rồi!",
                "usageNoteVi": "Thường dùng từ lúc thức dậy đến khoảng 9–10 giờ sáng.",
                "examples": [
                    {"hanzi": "早上好，老师！", "pinyin": "zǎo shang hǎo, lǎo shī!", "vi": "Chào buổi sáng cô giáo ạ!"},
                    {"hanzi": "早上好，你今天好吗？", "pinyin": "zǎo shang hǎo, nǐ jīn tiān hǎo ma?", "vi": "Chào buổi sáng, hôm nay bạn khỏe không?"},
                ],
            },
            {
                "hanzi": "老师", "pinyin": "lǎo shī", "meaningVi": "thầy giáo, cô giáo", "pos": "Danh từ",
                "radical": "老", "literalVi": "老 (lão/kính trọng) + 师 (thầy)",
                "mnemonic": "Người đi trước giàu kinh nghiệm (老) truyền dạy tri thức (师).",
                "usageNoteVi": "Gọi kèm họ ở trước: 王老师 (cô Vương / thầy Vương), không nói 老师王.",
                "examples": [
                    {"hanzi": "王老师好！", "pinyin": "Wáng lǎo shī hǎo!", "vi": "Em chào cô Vương ạ!"},
                    {"hanzi": "老师，谢谢您！", "pinyin": "lǎo shī, xiè xie nín!", "vi": "Thưa cô, em cảm ơn cô ạ!"},
                ],
            },
            {
                "hanzi": "谢谢", "pinyin": "xiè xie", "meaningVi": "cảm ơn", "pos": "Động từ",
                "radical": "讠", "literalVi": "Lời nói (讠) bày tỏ lòng biết ơn",
                "mnemonic": "Bộ ngôn (讠) bên trái — lời cảm ơn xuất phát từ lời nói chân thành.",
                "usageNoteVi": "Chữ 谢 thứ hai đọc thanh nhẹ (xiè xie). Thêm 你 thành 谢谢你 (cảm ơn bạn).",
                "examples": [
                    {"hanzi": "谢谢你！", "pinyin": "xiè xie nǐ!", "vi": "Cảm ơn bạn!"},
                    {"hanzi": "谢谢老师，明天见！", "pinyin": "xiè xie lǎo shī, míng tiān jiàn!", "vi": "Em cảm ơn cô, hẹn gặp cô ngày mai ạ!"},
                ],
            },
            {
                "hanzi": "不客气", "pinyin": "bú kè qi", "meaningVi": "không có gì, đừng khách sáo", "pos": "Cụm giao tiếp",
                "radical": "一", "literalVi": "不 (không) + 客气 (khách sáo)",
                "mnemonic": "Không (不) cần khách sáo (客气) với nhau đâu nhé!",
                "usageNoteVi": "Biến điệu của 不: trước thanh 4 (kè), 不 đọc thành bú (bú kè qi).",
                "examples": [
                    {"hanzi": "谢谢你！— 不客气。", "pinyin": "xiè xie nǐ! — bú kè qi.", "vi": "Cảm ơn bạn! — Không có gì đâu."},
                    {"hanzi": "不客气，我们是朋友。", "pinyin": "bú kè qi, wǒ men shì péng you.", "vi": "Đừng khách sáo, chúng mình là bạn mà."},
                ],
            },
            {
                "hanzi": "对不起", "pinyin": "duì bu qǐ", "meaningVi": "xin lỗi", "pos": "Cụm giao tiếp",
                "radical": "寸", "literalVi": "对 (đối diện) + 不起 (không xứng đáng)",
                "mnemonic": "Khi làm phiền ai, cảm thấy khó đối diện (对不起) nên nói lời xin lỗi.",
                "usageNoteVi": "Dùng khi bạn thực sự có lỗi (đến muộn, va phải ai). Chữ 不 ở giữa đọc nhẹ.",
                "examples": [
                    {"hanzi": "对不起，我来晚了。", "pinyin": "duì bu qǐ, wǒ lái wǎn le.", "vi": "Xin lỗi, mình đến muộn rồi."},
                    {"hanzi": "对不起，请问老师在吗？", "pinyin": "duì bu qǐ, qǐng wèn lǎo shī zài ma?", "vi": "Xin lỗi, cho hỏi cô giáo có ở đây không ạ?"},
                ],
            },
            {
                "hanzi": "没关系", "pinyin": "méi guān xi", "meaningVi": "không sao đâu", "pos": "Cụm giao tiếp",
                "radical": "氵", "literalVi": "没 (không có) + 关系 (vấn đề/liên hệ)",
                "mnemonic": "Đáp lại '对不起': không có chuyện gì đâu (没关系)!",
                "usageNoteVi": "Luôn đi cặp tự nhiên với 对不起: 对不起！— 没关系！",
                "examples": [
                    {"hanzi": "没关系，请坐吧。", "pinyin": "méi guān xi, qǐng zuò ba.", "vi": "Không sao đâu, mời bạn ngồi nhé."},
                    {"hanzi": "没关系，下次早点来。", "pinyin": "méi guān xi, xià cì zǎo diǎn lái.", "vi": "Không sao đâu, lần sau đến sớm hơn nhé."},
                ],
            },
            {
                "hanzi": "再见", "pinyin": "zài jiàn", "meaningVi": "tạm biệt", "pos": "Động từ",
                "radical": "见", "literalVi": "再 (lần nữa) + 见 (gặp mặt)",
                "mnemonic": "再 (lại) + 见 (gặp) = hẹn ngày gặp lại!",
                "usageNoteVi": "Rất lịch sự, dùng được với cả thầy cô lẫn bạn bè. Nếu hẹn mai gặp, nói 明天见！",
                "examples": [
                    {"hanzi": "老师再见！", "pinyin": "lǎo shī zài jiàn!", "vi": "Em chào cô tạm biệt ạ!"},
                    {"hanzi": "明天见，再见！", "pinyin": "míng tiān jiàn, zài jiàn!", "vi": "Hẹn mai gặp, tạm biệt nhé!"},
                ],
            },
        ],
        "patterns": [
            {
                "id": "p-t1-1", "frame": "___好！", "pinyin": "___ hǎo!", "meaningVi": "Chào [ai đó / buổi trong ngày]!",
                "exampleHanzi": "老师好！", "examplePinyin": "lǎo shī hǎo!", "exampleVi": "Em chào thầy/cô ạ!",
                "slots": {
                    "promptVi": "Chọn từ để chào thầy/cô giáo vào đầu buổi học:",
                    "choices": [
                        {"hanzi": "老师", "pinyin": "lǎo shī", "vi": "thầy/cô giáo"},
                        {"hanzi": "谢谢", "pinyin": "xiè xie", "vi": "cảm ơn"},
                        {"hanzi": "再见", "pinyin": "zài jiàn", "vi": "tạm biệt"},
                    ],
                    "answerHanzi": "老师",
                },
            },
            {
                "id": "p-t1-2", "frame": "谢谢你！— ___。", "pinyin": "xiè xie nǐ! — ___.", "meaningVi": "Cảm ơn bạn! — Không có gì.",
                "exampleHanzi": "谢谢你！不客气。", "examplePinyin": "xiè xie nǐ! bú kè qi.", "exampleVi": "Cảm ơn bạn! Không có gì đâu.",
                "slots": {
                    "promptVi": "Linh cảm ơn Bao, Bao đáp lại lịch sự thế nào?",
                    "choices": [
                        {"hanzi": "不客气", "pinyin": "bú kè qi", "vi": "không có gì"},
                        {"hanzi": "对不起", "pinyin": "duì bu qǐ", "vi": "xin lỗi"},
                        {"hanzi": "你好", "pinyin": "nǐ hǎo", "vi": "xin chào"},
                    ],
                    "answerHanzi": "不客气",
                },
            },
            {
                "id": "p-t1-3", "frame": "对不起！— ___。", "pinyin": "duì bu qǐ! — ___.", "meaningVi": "Xin lỗi! — Không sao đâu.",
                "exampleHanzi": "对不起！没关系。", "examplePinyin": "duì bu qǐ! méi guān xi.", "exampleVi": "Xin lỗi! Không sao đâu.",
                "slots": {
                    "promptVi": "Bạn làm rơi bút của Linh và xin lỗi, Linh đáp thế nào?",
                    "choices": [
                        {"hanzi": "没关系", "pinyin": "méi guān xi", "vi": "không sao đâu"},
                        {"hanzi": "再见", "pinyin": "zài jiàn", "vi": "tạm biệt"},
                        {"hanzi": "早上好", "pinyin": "zǎo shang hǎo", "vi": "chào buổi sáng"},
                    ],
                    "answerHanzi": "没关系",
                },
            },
        ],
        "dialogue": [
            {"speaker": "Linh", "voiceRole": "female", "hanzi": "早上好！你好！", "pinyin": "zǎo shang hǎo! nǐ hǎo!", "vi": "Chào buổi sáng! Xin chào!", "mode": "npc", "goalLabel": "Chào buổi sáng"},
            {
                "speaker": "Bao", "voiceRole": "male", "hanzi": "早上好！请坐。", "pinyin": "zǎo shang hǎo! qǐng zuò.", "vi": "Chào buổi sáng! Mời bạn ngồi.",
                "mode": "choice", "goalLabel": "Đáp lời chào",
                "choices": [
                    {"hanzi": "早上好！请坐。", "pinyin": "zǎo shang hǎo! qǐng zuò.", "vi": "Chào buổi sáng! Mời bạn ngồi.", "correct": True},
                    {"hanzi": "再见！不客气。", "pinyin": "zài jiàn! bú kè qi.", "vi": "Tạm biệt! Không có gì.", "correct": False},
                    {"hanzi": "对不起！老师。", "pinyin": "duì bu qǐ! lǎo shī.", "vi": "Xin lỗi! Cô giáo.", "correct": False},
                ],
            },
            {"speaker": "Linh", "voiceRole": "female", "hanzi": "谢谢你！", "pinyin": "xiè xie nǐ!", "vi": "Cảm ơn bạn!", "mode": "npc"},
            {"speaker": "Bao", "voiceRole": "male", "hanzi": "不客气！", "pinyin": "bú kè qi!", "vi": "Không có gì đâu!", "mode": "tiles", "goalLabel": "Đáp lại lời cảm ơn", "tilePrompt": ["不", "客气"]},
            {"speaker": "Cô Vương", "voiceRole": "formal", "hanzi": "同学们，早上好！", "pinyin": "tóng xué men, zǎo shang hǎo!", "vi": "Chào buổi sáng các em!", "mode": "npc"},
            {"speaker": "Bao", "voiceRole": "male", "hanzi": "老师好！对不起，我来晚了。", "pinyin": "lǎo shī hǎo! duì bu qǐ, wǒ lái wǎn le.", "vi": "Em chào cô ạ! Xin lỗi, em đến muộn ạ.", "mode": "npc"},
            {"speaker": "Cô Vương", "voiceRole": "formal", "hanzi": "没关系，下课了，明天见！", "pinyin": "méi guān xi, xià kè le, míng tiān jiàn!", "vi": "Không sao đâu, hết giờ rồi, hẹn gặp ngày mai nhé!", "mode": "npc"},
            {"speaker": "Bao", "voiceRole": "male", "hanzi": "老师再见！", "pinyin": "lǎo shī zài jiàn!", "vi": "Em chào cô tạm biệt ạ!", "mode": "pinyin", "goalLabel": "Chào tạm biệt", "acceptedPinyin": ["laoshi zaijian", "laoshizaijian", "lǎo shī zài jiàn", "老师再见"]},
        ],
        "exercises": [
            {
                "id": "ex-t1-1", "kind": "meaning-choice", "promptVi": "Cụm 「不客气」 có nghĩa là gì?",
                "hanziPrompt": "不客气", "pinyinPrompt": "bú kè qi",
                "options": [
                    {"label": "Không có gì, đừng khách sáo", "value": "Không có gì, đừng khách sáo"},
                    {"label": "Xin lỗi", "value": "Xin lỗi"},
                    {"label": "Tạm biệt", "value": "Tạm biệt"},
                    {"label": "Chào buổi sáng", "value": "Chào buổi sáng"},
                ],
                "answer": "Không có gì, đừng khách sáo",
                "explainVi": "不客气 (bú kè qi) dùng để đáp lại 谢谢 (cảm ơn).",
            },
            {
                "id": "ex-t1-2", "kind": "hanzi-choice", "promptVi": "Nghe và chọn chữ Hán có nghĩa 'Xin lỗi'",
                "audioText": "对不起",
                "options": [
                    {"label": "对不起", "value": "对不起"},
                    {"label": "没关系", "value": "没关系"},
                    {"label": "不客气", "value": "不客气"},
                    {"label": "早上好", "value": "早上好"},
                ],
                "answer": "对不起",
                "explainVi": "对不起 (duì bu qǐ) = xin lỗi.",
            },
            {
                "id": "ex-t1-3", "kind": "match-pairs", "promptVi": "Ghép nhanh 4 cặp chữ Hán với nghĩa tiếng Việt nhé!",
                "pairs": [
                    {"hanzi": "你好", "pinyin": "nǐ hǎo", "vi": "Xin chào"},
                    {"hanzi": "谢谢", "pinyin": "xiè xie", "vi": "Cảm ơn"},
                    {"hanzi": "没关系", "pinyin": "méi guān xi", "vi": "Không sao đâu"},
                    {"hanzi": "再见", "pinyin": "zài jiàn", "vi": "Tạm biệt"},
                ],
                "answer": "matched",
            },
            {
                "id": "ex-t1-4", "kind": "fill-blank", "promptVi": "Chọn từ điền vào chỗ trống: 「对不起！— ___！」",
                "hanziPrompt": "对不起！— ___！", "pinyinPrompt": "duì bu qǐ! — ___!",
                "options": [
                    {"label": "没关系", "value": "没关系"},
                    {"label": "老师", "value": "老师"},
                    {"label": "再见", "value": "再见"},
                    {"label": "谢谢", "value": "谢谢"},
                ],
                "answer": "没关系",
                "explainVi": "Khi ai đó nói 对不起 (xin lỗi), ta đáp 没关系 (không sao đâu).",
            },
            {
                "id": "ex-t1-5", "kind": "sentence-tiles", "promptVi": "Sắp xếp thẻ từ: 'Em chào cô giáo buổi sáng ạ!'",
                "tiles": ["好", "老师", "早上"],
                "answer": "老师早上好",
                "explainVi": "Đặt người được chào (老师) lên trước, rồi đến 早上好!",
            },
            {
                "id": "ex-t1-6", "kind": "meaning-choice", "promptVi": "Câu 「老师，谢谢您！再见！」 nghĩa là gì?",
                "hanziPrompt": "老师，谢谢您！再见！", "pinyinPrompt": "lǎo shī, xiè xie nín! zài jiàn!",
                "options": [
                    {"label": "Thưa cô, em cảm ơn cô! Em chào cô tạm biệt ạ!", "value": "Thưa cô, em cảm ơn cô! Em chào cô tạm biệt ạ!"},
                    {"label": "Chào buổi sáng bạn học mới!", "value": "Chào buổi sáng bạn học mới!"},
                    {"label": "Xin lỗi cô, em đến muộn ạ!", "value": "Xin lỗi cô, em đến muộn ạ!"},
                    {"label": "Không có gì, không sao đâu!", "value": "Không có gì, không sao đâu!"},
                ],
                "answer": "Thưa cô, em cảm ơn cô! Em chào cô tạm biệt ạ!",
            },
        ],
        "roleplay": [
            {
                "npcHanzi": "早上好！你好吗？", "npcPinyin": "zǎo shang hǎo! nǐ hǎo ma?", "npcVi": "Chào buổi sáng! Bạn khỏe không?",
                "promptVi": "Chào buổi sáng lại và nói mình rất khỏe:",
                "options": [
                    {"hanzi": "早上好！我很好，谢谢！", "pinyin": "zǎo shang hǎo! wǒ hěn hǎo, xiè xie!", "vi": "Chào buổi sáng! Mình rất khỏe, cảm ơn!", "correct": True},
                    {"hanzi": "再见！对不起。", "pinyin": "zài jiàn! duì bu qǐ.", "vi": "Tạm biệt! Xin lỗi.", "correct": False},
                    {"hanzi": "没关系。", "pinyin": "méi guān xi.", "vi": "Không sao đâu.", "correct": False},
                ],
                "expectedHanzi": "早上好！我很好，谢谢！",
            },
            {
                "npcHanzi": "对不起，我来晚了！", "npcPinyin": "duì bu qǐ, wǒ lái wǎn le!", "npcVi": "Xin lỗi, mình đến muộn rồi!",
                "promptVi": "An ủi bạn rằng không sao đâu:",
                "options": [
                    {"hanzi": "没关系，请坐吧！", "pinyin": "méi guān xi, qǐng zuò ba!", "vi": "Không sao đâu, mời ngồi nhé!", "correct": True},
                    {"hanzi": "不客气！", "pinyin": "bú kè qi!", "vi": "Không có gì!", "correct": False},
                    {"hanzi": "老师再见！", "pinyin": "lǎo shī zài jiàn!", "vi": "Chào cô tạm biệt!", "correct": False},
                ],
                "expectedHanzi": "没关系，请坐吧！",
            },
            {
                "npcHanzi": "下课了，明天见！", "npcPinyin": "xià kè le, míng tiān jiàn!", "npcVi": "Hết giờ rồi, hẹn gặp ngày mai nhé!",
                "promptVi": "Cảm ơn cô và chào tạm biệt:",
                "options": [
                    {"hanzi": "谢谢老师，再见！", "pinyin": "xiè xie lǎo shī, zài jiàn!", "vi": "Em cảm ơn cô, tạm biệt cô ạ!", "correct": True},
                    {"hanzi": "早上好！", "pinyin": "zǎo shang hǎo!", "vi": "Chào buổi sáng!", "correct": False},
                    {"hanzi": "对不起！", "pinyin": "duì bu qǐ!", "vi": "Xin lỗi!", "correct": False},
                ],
                "expectedHanzi": "谢谢老师，再见！",
            },
        ],
        "writing": [
            {"char": "你", "pinyin": "nǐ", "meaningVi": "bạn", "radical": "亻", "radicalNoteVi": "Bộ nhân đứng (亻) — hình dáng người đứng, xuất hiện ở 他, 们.", "lookalikes": [{"hanzi": "你", "pinyin": "nǐ", "vi": "bạn"}, {"hanzi": "他", "pinyin": "tā", "vi": "anh ấy"}, {"hanzi": "们", "pinyin": "men", "vi": "các"}, {"hanzi": "作", "pinyin": "zuò", "vi": "làm"}]},
            {"char": "好", "pinyin": "hǎo", "meaningVi": "tốt, khỏe", "radical": "女", "radicalNoteVi": "Bộ nữ (女) ghép bộ tử (子) — mẹ bế con là hình ảnh tốt đẹp.", "lookalikes": [{"hanzi": "好", "pinyin": "hǎo", "vi": "tốt"}, {"hanzi": "她", "pinyin": "tā", "vi": "cô ấy"}, {"hanzi": "妈", "pinyin": "mā", "vi": "mẹ"}, {"hanzi": "子", "pinyin": "zǐ", "vi": "con"}]},
            {"char": "见", "pinyin": "jiàn", "meaningVi": "gặp, thấy", "radical": "见", "radicalNoteVi": "Bộ kiến (见) — đôi mắt bước đi để nhìn thấy, gặp gỡ.", "lookalikes": [{"hanzi": "见", "pinyin": "jiàn", "vi": "gặp"}, {"hanzi": "贝", "pinyin": "bèi", "vi": "vỏ sò"}, {"hanzi": "风", "pinyin": "fēng", "vi": "gió"}, {"hanzi": "几", "pinyin": "jǐ", "vi": "mấy"}]},
        ],
    },
    {
        "topicId": 2,
        "title": "Giới thiệu bản thân",
        "subtitle": "Hỏi tên, giới thiệu quốc tịch Việt Nam và làm quen bạn mới",
        "storyTagVi": "Ngày 1 · Làm quen bạn cùng bàn",
        "connectsFromVi": "Tiếp nối Bài 1: Chào hỏi & tạm biệt",
        "storyContextVi": "Sau khi chào hỏi ở Bài 1, giờ ra chơi Bao quay sang hỏi tên cô bạn bàn bên và hào hứng giới thiệu mình đến từ Việt Nam!",
        "bridgeFromPrevVi": "Ở Bài 1 bạn đã biết 「你好」「谢谢」「再见」 — giờ hãy nối tiếp bằng cách hỏi tên và giới thiệu bản thân thật tự nhiên!",
        "bridgeToNextVi": "Biết tên nhau rồi, sang Bài 3 Bao và Linh sẽ học đếm số, hỏi tuổi và hẹn mừng sinh nhật!",
        "recapWordIds": ["你好", "老师", "谢谢"],
        "cultureTipVi": "Trong tiếng Trung, người ta nói 「我叫 + Tên」 khi giới thiệu tên riêng, còn khi giới thiệu nghề nghiệp hay quốc tịch sẽ dùng 「我是 + Danh từ」 (VD: 我是越南人).",
        "grammarSpotlight": {
            "title": "Phân biệt 「我叫…」 (tên) và 「我是…」 (là…)",
            "formula": "我叫 + [Tên]  |  我是 + [Quốc tịch / Nghề nghiệp]",
            "explainVi": "叫 (jiào) dùng để nói tên gọi; 是 (shì) là động từ 'là', dùng cho quốc tịch, nghề nghiệp hoặc danh tính. Thêm 吗 cuối câu để biến thành câu hỏi Có/Không!",
            "vsVietnameseVi": "Giống tiếng Việt! Nhưng nhớ: khi phủ định, thêm 不 trước 是 thành 「不是」(bú shì = không phải).",
            "commonMistakeVi": "Quên 吗 khi hỏi Có/Không: phải nói 「你是中国人吗？」 chứ không chỉ nói 「你是中国人？」.",
            "examples": [
                {"hanzi": "我叫Bao，我是越南人。", "pinyin": "wǒ jiào Bao, wǒ shì Yuè nán rén.", "vi": "Mình tên là Bao, mình là người Việt Nam."},
                {"hanzi": "你是中国同学吗？", "pinyin": "nǐ shì Zhōng guó tóng xué ma?", "vi": "Bạn là bạn học người Trung Quốc phải không?"},
            ],
        },
        "words": [
            {
                "hanzi": "我", "pinyin": "wǒ", "meaningVi": "tôi, mình", "pos": "Đại từ",
                "radical": "戈", "literalVi": "Ngôi thứ nhất số ít",
                "mnemonic": "Chữ 我 như bàn tay cầm cây giáo bảo vệ chính mình.",
                "usageNoteVi": "Thêm 们 thành 我们 (wǒ men = chúng tôi / chúng mình).",
                "examples": [
                    {"hanzi": "我叫Bao，你好！", "pinyin": "wǒ jiào Bao, nǐ hǎo!", "vi": "Mình tên là Bao, xin chào!"},
                    {"hanzi": "我们是好同学。", "pinyin": "wǒ men shì hǎo tóng xué.", "vi": "Chúng mình là bạn học tốt."},
                ],
            },
            {
                "hanzi": "叫", "pinyin": "jiào", "meaningVi": "tên là, gọi là", "pos": "Động từ",
                "radical": "口", "literalVi": "Bộ khẩu (口) — mở miệng gọi tên",
                "mnemonic": "Bên trái có cái miệng (口) để cất tiếng gọi tên ai đó!",
                "usageNoteVi": "Hỏi tên lịch sự: 请问你叫什么名字？(Xin hỏi bạn tên gì?).",
                "examples": [
                    {"hanzi": "你叫什么名字？", "pinyin": "nǐ jiào shén me míng zi?", "vi": "Bạn tên là gì?"},
                    {"hanzi": "我叫小玲。", "pinyin": "wǒ jiào Xiǎo Líng.", "vi": "Mình tên là Tiểu Linh."},
                ],
            },
            {
                "hanzi": "名字", "pinyin": "míng zi", "meaningVi": "tên, họ tên", "pos": "Danh từ",
                "radical": "口", "literalVi": "名 (danh/tên) + 字 (chữ viết)",
                "mnemonic": "Chiều tối (夕) phải lên tiếng bằng miệng (口) xưng tên (名); 字 là đứa trẻ (子) học chữ dưới mái nhà (宀).",
                "usageNoteVi": "Chữ 字 đọc thanh nhẹ (míng zi).",
                "examples": [
                    {"hanzi": "你的名字很好听！", "pinyin": "nǐ de míng zi hěn hǎo tīng!", "vi": "Tên của bạn nghe hay quá!"},
                    {"hanzi": "请问，你叫什么名字？", "pinyin": "qǐng wèn, nǐ jiào shén me míng zi?", "vi": "Xin hỏi, bạn tên là gì?"},
                ],
            },
            {
                "hanzi": "是", "pinyin": "shì", "meaningVi": "là, đúng vậy", "pos": "Động từ",
                "radical": "日", "literalVi": "Mặt trời (日) ngay thẳng (正) = chân lý, là",
                "mnemonic": "Mặt trời (日) soi sáng điều đúng đắn — khẳng định 'là'.",
                "usageNoteVi": "Phủ định của 是 là 不是 (bú shì). Không dùng 是 trước tính từ đơn (nói 我很好, không nói 我是好).",
                "examples": [
                    {"hanzi": "她是王老师。", "pinyin": "tā shì Wáng lǎo shī.", "vi": "Cô ấy là cô Vương."},
                    {"hanzi": "我是新同学。", "pinyin": "wǒ shì xīn tóng xué.", "vi": "Mình là bạn học mới."},
                ],
            },
            {
                "hanzi": "越南", "pinyin": "Yuè nán", "meaningVi": "Việt Nam", "pos": "Danh từ",
                "radical": "走", "literalVi": "越 (Việt) + 南 (phương Nam)",
                "mnemonic": "Âm Hán-Việt chuẩn: 越 (Việt) + 南 (Nam). Thêm 人 thành 越南人 (người Việt Nam)!",
                "usageNoteVi": "Ngôn ngữ tiếng Việt là 越南语 (Yuènányǔ).",
                "examples": [
                    {"hanzi": "我是越南人。", "pinyin": "wǒ shì Yuè nán rén.", "vi": "Mình là người Việt Nam."},
                    {"hanzi": "我来自越南。", "pinyin": "wǒ lái zì Yuè nán.", "vi": "Mình đến từ Việt Nam."},
                ],
            },
            {
                "hanzi": "中国", "pinyin": "Zhōng guó", "meaningVi": "Trung Quốc", "pos": "Danh từ",
                "radical": "丨", "literalVi": "中 (ở giữa) + 国 (đất nước)",
                "mnemonic": "中 là nét thẳng xuyên chính giữa; 国 là viên ngọc (玉) nằm trong biên giới (囗).",
                "usageNoteVi": "Người Trung Quốc: 中国人. Tiếng Trung: 中文 hoặc 汉语.",
                "examples": [
                    {"hanzi": "你去过中国吗？", "pinyin": "nǐ qù guo Zhōng guó ma?", "vi": "Bạn từng đi Trung Quốc chưa?"},
                    {"hanzi": "王老师是中国人。", "pinyin": "Wáng lǎo shī shì Zhōng guó rén.", "vi": "Cô Vương là người Trung Quốc."},
                ],
            },
            {
                "hanzi": "同学", "pinyin": "tóng xué", "meaningVi": "bạn học", "pos": "Danh từ",
                "radical": "口", "literalVi": "同 (cùng nhau) + 学 (học tập)",
                "mnemonic": "Cùng (同) ngồi học (学) trong một lớp gọi là bạn học!",
                "usageNoteVi": "Thêm 们 thành 同学们 (các bạn học / các em học sinh).",
                "examples": [
                    {"hanzi": "小玲是我的新同学。", "pinyin": "Xiǎo Líng shì wǒ de xīn tóng xué.", "vi": "Tiểu Linh là bạn học mới của mình."},
                    {"hanzi": "同学们早上好！", "pinyin": "tóng xué men zǎo shang hǎo!", "vi": "Chào buổi sáng các bạn học!"},
                ],
            },
            {
                "hanzi": "认识", "pinyin": "rèn shi", "meaningVi": "quen biết", "pos": "Động từ",
                "radical": "讠", "literalVi": "Cả hai chữ đều có bộ ngôn (讠) — trò chuyện mà quen nhau",
                "mnemonic": "Hai người cùng nói chuyện (讠 + 讠) nên dần quen biết nhau!",
                "usageNoteVi": "Câu cửa miệng khi mới gặp: 很高兴认识你！(Rất vui được quen bạn!).",
                "examples": [
                    {"hanzi": "很高兴认识你！", "pinyin": "hěn gāo xìng rèn shi nǐ!", "vi": "Rất vui được quen biết bạn!"},
                    {"hanzi": "你认识王老师吗？", "pinyin": "nǐ rèn shi Wáng lǎo shī ma?", "vi": "Bạn có quen cô Vương không?"},
                ],
            },
        ],
        "patterns": [
            {
                "id": "p-t2-1", "frame": "我叫___。", "pinyin": "wǒ jiào ___.", "meaningVi": "Mình tên là ___.",
                "exampleHanzi": "我叫Bao。", "examplePinyin": "wǒ jiào Bao.", "exampleVi": "Mình tên là Bao.",
                "slots": {
                    "promptVi": "Điền tên để nói 'Mình tên là Tiểu Linh':",
                    "choices": [
                        {"hanzi": "小玲", "pinyin": "Xiǎo Líng", "vi": "Tiểu Linh"},
                        {"hanzi": "认识", "pinyin": "rèn shi", "vi": "quen biết"},
                        {"hanzi": "名字", "pinyin": "míng zi", "vi": "tên"},
                    ],
                    "answerHanzi": "小玲",
                },
            },
            {
                "id": "p-t2-2", "frame": "你是___人吗？", "pinyin": "nǐ shì ___ rén ma?", "meaningVi": "Bạn là người nước ___ phải không?",
                "exampleHanzi": "你是越南人吗？", "examplePinyin": "nǐ shì Yuè nán rén ma?", "exampleVi": "Bạn là người Việt Nam phải không?",
                "slots": {
                    "promptVi": "Hỏi xem bạn mới có phải người Trung Quốc không:",
                    "choices": [
                        {"hanzi": "中国", "pinyin": "Zhōng guó", "vi": "Trung Quốc"},
                        {"hanzi": "越南", "pinyin": "Yuè nán", "vi": "Việt Nam"},
                        {"hanzi": "同学", "pinyin": "tóng xué", "vi": "bạn học"},
                    ],
                    "answerHanzi": "中国",
                },
            },
            {
                "id": "p-t2-3", "frame": "很高兴___你！", "pinyin": "hěn gāo xìng ___ nǐ!", "meaningVi": "Rất vui được ___ bạn!",
                "exampleHanzi": "很高兴认识你！", "examplePinyin": "hěn gāo xìng rèn shi nǐ!", "exampleVi": "Rất vui được quen biết bạn!",
                "slots": {
                    "promptVi": "Hoàn thành câu 'Rất vui được quen biết bạn!':",
                    "choices": [
                        {"hanzi": "认识", "pinyin": "rèn shi", "vi": "quen biết"},
                        {"hanzi": "名字", "pinyin": "míng zi", "vi": "tên"},
                        {"hanzi": "中国", "pinyin": "Zhōng guó", "vi": "Trung Quốc"},
                    ],
                    "answerHanzi": "认识",
                },
            },
        ],
        "dialogue": [
            {"speaker": "Linh", "voiceRole": "female", "hanzi": "你好！请问你叫什么名字？", "pinyin": "nǐ hǎo! qǐng wèn nǐ jiào shén me míng zi?", "vi": "Xin chào! Xin hỏi bạn tên là gì?", "mode": "npc"},
            {
                "speaker": "Bao", "voiceRole": "male", "hanzi": "你好！我叫Bao，你呢？", "pinyin": "nǐ hǎo! wǒ jiào Bao, nǐ ne?", "vi": "Xin chào! Mình tên là Bao, còn bạn?",
                "mode": "choice", "goalLabel": "Giới thiệu tên",
                "choices": [
                    {"hanzi": "你好！我叫Bao，你呢？", "pinyin": "nǐ hǎo! wǒ jiào Bao, nǐ ne?", "vi": "Xin chào! Mình tên là Bao, còn bạn?", "correct": True},
                    {"hanzi": "你叫Bao。", "pinyin": "nǐ jiào Bao.", "vi": "Bạn tên là Bao.", "correct": False},
                    {"hanzi": "再见，谢谢。", "pinyin": "zài jiàn, xiè xie.", "vi": "Tạm biệt, cảm ơn.", "correct": False},
                ],
            },
            {"speaker": "Linh", "voiceRole": "female", "hanzi": "我叫小玲。很高兴认识你！", "pinyin": "wǒ jiào Xiǎo Líng. hěn gāo xìng rèn shi nǐ!", "vi": "Mình tên là Tiểu Linh. Rất vui được quen bạn!", "mode": "npc"},
            {"speaker": "Bao", "voiceRole": "male", "hanzi": "我也很高兴认识你！", "pinyin": "wǒ yě hěn gāo xìng rèn shi nǐ!", "vi": "Mình cũng rất vui được quen bạn!", "mode": "tiles", "goalLabel": "Đáp lại lời làm quen", "tilePrompt": ["我也", "很", "高兴", "认识", "你"]},
            {"speaker": "Linh", "voiceRole": "female", "hanzi": "你是中国人吗？", "pinyin": "nǐ shì Zhōng guó rén ma?", "vi": "Bạn là người Trung Quốc phải không?", "mode": "npc"},
            {"speaker": "Bao", "voiceRole": "male", "hanzi": "不是，我是越南人。", "pinyin": "bú shì, wǒ shì Yuè nán rén.", "vi": "Không phải, mình là người Việt Nam.", "mode": "pinyin", "goalLabel": "Nói quốc tịch", "acceptedPinyin": ["bushi woshi yuenanren", "bushiwoshiyuenanren", "bú shì wǒ shì yuè nán rén", "不是，我是越南人"]},
        ],
        "exercises": [
            {
                "id": "ex-t2-1", "kind": "meaning-choice", "promptVi": "Câu 「很高兴认识你！」 có nghĩa là gì?",
                "hanziPrompt": "很高兴认识你！", "pinyinPrompt": "hěn gāo xìng rèn shi nǐ!",
                "options": [
                    {"label": "Rất vui được quen biết bạn!", "value": "Rất vui được quen biết bạn!"},
                    {"label": "Bạn tên là gì?", "value": "Bạn tên là gì?"},
                    {"label": "Mình là người Việt Nam.", "value": "Mình là người Việt Nam."},
                    {"label": "Cảm ơn bạn rất nhiều.", "value": "Cảm ơn bạn rất nhiều."},
                ],
                "answer": "Rất vui được quen biết bạn!",
            },
            {
                "id": "ex-t2-2", "kind": "hanzi-choice", "promptVi": "Nghe và chọn chữ Hán có nghĩa 'quen biết'",
                "audioText": "认识",
                "options": [
                    {"label": "认识", "value": "认识"},
                    {"label": "名字", "value": "名字"},
                    {"label": "同学", "value": "同学"},
                    {"label": "越南", "value": "越南"},
                ],
                "answer": "认识",
            },
            {
                "id": "ex-t2-3", "kind": "match-pairs", "promptVi": "Ghép nhanh 4 cặp từ giới thiệu bản thân:",
                "pairs": [
                    {"hanzi": "名字", "pinyin": "míng zi", "vi": "Tên"},
                    {"hanzi": "越南", "pinyin": "Yuè nán", "vi": "Việt Nam"},
                    {"hanzi": "中国", "pinyin": "Zhōng guó", "vi": "Trung Quốc"},
                    {"hanzi": "同学", "pinyin": "tóng xué", "vi": "Bạn học"},
                ],
                "answer": "matched",
            },
            {
                "id": "ex-t2-4", "kind": "fill-blank", "promptVi": "Điền từ đúng: 「你___什么名字？」",
                "hanziPrompt": "你___什么名字？", "pinyinPrompt": "nǐ ___ shén me míng zi?",
                "options": [
                    {"label": "叫", "value": "叫"},
                    {"label": "是", "value": "是"},
                    {"label": "认识", "value": "认识"},
                    {"label": "好", "value": "好"},
                ],
                "answer": "叫",
                "explainVi": "Dùng 叫 (jiào) để hỏi tên: 你叫什么名字？",
            },
            {
                "id": "ex-t2-5", "kind": "sentence-tiles", "promptVi": "Ghép câu: 'Mình là người Việt Nam.'",
                "tiles": ["人", "越南", "我", "是"],
                "answer": "我是越南人",
                "explainVi": "Trật tự chuẩn: 我 (tôi) + 是 (là) + 越南人 (người Việt Nam).",
            },
            {
                "id": "ex-t2-6", "kind": "meaning-choice", "promptVi": "Câu 「王老师是中国人，她是我的老师。」 nghĩa là gì?",
                "hanziPrompt": "王老师是中国人，她是我的老师。", "pinyinPrompt": "Wáng lǎo shī shì Zhōng guó rén, tā shì wǒ de lǎo shī.",
                "options": [
                    {"label": "Cô Vương là người Trung Quốc, cô ấy là giáo viên của mình.", "value": "Cô Vương là người Trung Quốc, cô ấy là giáo viên của mình."},
                    {"label": "Cô Vương là bạn học người Việt Nam của mình.", "value": "Cô Vương là bạn học người Việt Nam của mình."},
                    {"label": "Mình không quen biết cô Vương.", "value": "Mình không quen biết cô Vương."},
                    {"label": "Cô Vương tên là Tiểu Linh.", "value": "Cô Vương tên là Tiểu Linh."},
                ],
                "answer": "Cô Vương là người Trung Quốc, cô ấy là giáo viên của mình.",
            },
        ],
        "roleplay": [
            {
                "npcHanzi": "你好！请问你叫什么名字？", "npcPinyin": "nǐ hǎo! qǐng wèn nǐ jiào shén me míng zi?", "npcVi": "Xin chào! Xin hỏi bạn tên là gì?",
                "promptVi": "Chào lại và giới thiệu tên mình là Bao:",
                "options": [
                    {"hanzi": "你好！我叫Bao。", "pinyin": "nǐ hǎo! wǒ jiào Bao.", "vi": "Xin chào! Mình tên là Bao.", "correct": True},
                    {"hanzi": "不客气！", "pinyin": "bú kè qi!", "vi": "Không có gì!", "correct": False},
                    {"hanzi": "明天见！", "pinyin": "míng tiān jiàn!", "vi": "Hẹn gặp ngày mai!", "correct": False},
                ],
                "expectedHanzi": "你好！我叫Bao。",
            },
            {
                "npcHanzi": "你是哪国人？", "npcPinyin": "nǐ shì nǎ guó rén?", "npcVi": "Bạn là người nước nào?",
                "promptVi": "Trả lời mình là người Việt Nam:",
                "options": [
                    {"hanzi": "我是越南人。", "pinyin": "wǒ shì Yuè nán rén.", "vi": "Mình là người Việt Nam.", "correct": True},
                    {"hanzi": "我叫越南。", "pinyin": "wǒ jiào Yuè nán.", "vi": "Mình tên là Việt Nam.", "correct": False},
                    {"hanzi": "老师好。", "pinyin": "lǎo shī hǎo.", "vi": "Em chào cô.", "correct": False},
                ],
                "expectedHanzi": "我是越南人。",
            },
            {
                "npcHanzi": "很高兴认识你，新同学！", "npcPinyin": "hěn gāo xìng rèn shi nǐ, xīn tóng xué!", "npcVi": "Rất vui được quen bạn, bạn học mới!",
                "promptVi": "Đáp lại niềm nở rằng mình cũng rất vui:",
                "options": [
                    {"hanzi": "我也很高兴认识你！", "pinyin": "wǒ yě hěn gāo xìng rèn shi nǐ!", "vi": "Mình cũng rất vui được quen bạn!", "correct": True},
                    {"hanzi": "对不起！", "pinyin": "duì bu qǐ!", "vi": "Xin lỗi!", "correct": False},
                    {"hanzi": "不是中国人。", "pinyin": "bú shì Zhōng guó rén.", "vi": "Không phải người Trung Quốc.", "correct": False},
                ],
                "expectedHanzi": "我也很高兴认识你！",
            },
        ],
        "writing": [
            {"char": "叫", "pinyin": "jiào", "meaningVi": "tên là, gọi", "radical": "口", "radicalNoteVi": "Bộ khẩu (口) chỉ hoạt động của miệng khi gọi tên.", "lookalikes": [{"hanzi": "叫", "pinyin": "jiào", "vi": "gọi"}, {"hanzi": "吃", "pinyin": "chī", "vi": "ăn"}, {"hanzi": "听", "pinyin": "tīng", "vi": "nghe"}, {"hanzi": "叹", "pinyin": "tàn", "vi": "thở dài"}]},
            {"char": "名", "pinyin": "míng", "meaningVi": "tên", "radical": "口", "radicalNoteVi": "Chiều tối (夕) phải gọi tên bằng miệng (口) để nhận ra nhau.", "lookalikes": [{"hanzi": "名", "pinyin": "míng", "vi": "tên"}, {"hanzi": "各", "pinyin": "gè", "vi": "mỗi"}, {"hanzi": "多", "pinyin": "duō", "vi": "nhiều"}, {"hanzi": "夕", "pinyin": "xī", "vi": "chiều tối"}]},
            {"char": "字", "pinyin": "zì", "meaningVi": "chữ viết", "radical": "子", "radicalNoteVi": "Đứa trẻ (子) ngồi học chữ dưới mái nhà (宀).", "lookalikes": [{"hanzi": "字", "pinyin": "zì", "vi": "chữ"}, {"hanzi": "学", "pinyin": "xué", "vi": "học"}, {"hanzi": "子", "pinyin": "zǐ", "vi": "con"}, {"hanzi": "安", "pinyin": "ān", "vi": "an lành"}]},
        ],
    },
    {
        "topicId": 3,
        "title": "Số đếm, tuổi & ngày tháng",
        "subtitle": "Hỏi tuổi, nói ngày tháng và chúc mừng sinh nhật",
        "storyTagVi": "Ngày 2 · Sinh nhật sắp tới của Linh",
        "connectsFromVi": "Tiếp nối Bài 2: Giới thiệu bản thân",
        "storyContextVi": "Quen thân sau Bài 2, Bao hỏi tuổi Tiểu Linh thì bất ngờ biết tuần sau chính là sinh nhật của bạn ấy!",
        "bridgeFromPrevVi": "Đã biết tên và quốc tịch ở Bài 2 — nay học thêm cách hỏi tuổi, ngày tháng và chúc sinh nhật nhé!",
        "bridgeToNextVi": "Để chuẩn bị tiệc sinh nhật cho Linh, sang Bài 4 Bao sẽ kể về gia đình và giới thiệu bạn thân Tiểu Minh!",
        "recapWordIds": ["叫", "名字", "同学"],
        "cultureTipVi": "Trong tiếng Trung, thứ tự ngày tháng luôn đi từ LỚN đến NHỎ: Năm (年) → Tháng (月) → Ngày (号/日). Ví dụ: 2026年5月18号 (ngày 18 tháng 5 năm 2026)!",
        "grammarSpotlight": {
            "title": "Thứ tự ngày tháng (Năm → Tháng → Ngày) & Hỏi tuổi",
            "formula": "___年 ___月 ___号  |  你今年多大？ / 你几岁？",
            "explainVi": "Khi nói ngày tháng, luôn đặt đơn vị lớn trước, nhỏ sau (ngược với tiếng Việt). Khi hỏi tuổi: 几岁 (jǐ suì) thường hỏi trẻ nhỏ, còn 多大 (duō dà) lịch sự dùng cho bạn bè/thanh niên.",
            "vsVietnameseVi": "Tiếng Việt nói 'ngày 18 tháng 5', tiếng Trung đảo ngược thành '5月18号' (tháng 5 ngày 18).",
            "commonMistakeVi": "Nhầm 18号5月 theo kiểu Việt — phải luôn đặt 月 (tháng) trước 号 (ngày)!",
            "examples": [
                {"hanzi": "今天是五月十八号。", "pinyin": "jīn tiān shì wǔ yuè shí bā hào.", "vi": "Hôm nay là ngày 18 tháng 5."},
                {"hanzi": "我今年二十岁。", "pinyin": "wǒ jīn nián èr shí suì.", "vi": "Năm nay mình 20 tuổi."},
            ],
        },
        "words": [
            {
                "hanzi": "几", "pinyin": "jǐ", "meaningVi": "mấy (hỏi số nhỏ dưới 10)", "pos": "Đại từ",
                "radical": "几", "literalVi": "Từ hỏi số lượng nhỏ",
                "mnemonic": "Chỉ có 2 nét cong như cái ghế đẩu — dùng để hỏi 'mấy?'.",
                "usageNoteVi": "Dùng trong 几月 (tháng mấy), 几号 (ngày mấy), 几岁 (mấy tuổi).",
                "examples": [
                    {"hanzi": "今天几月几号？", "pinyin": "jīn tiān jǐ yuè jǐ hào?", "vi": "Hôm nay ngày mấy tháng mấy?"},
                    {"hanzi": "你妹妹今年几岁？", "pinyin": "nǐ mèi mei jīn nián jǐ suì?", "vi": "Em gái bạn năm nay mấy tuổi?"},
                ],
            },
            {
                "hanzi": "岁", "pinyin": "suì", "meaningVi": "tuổi", "pos": "Lượng từ",
                "radical": "山", "literalVi": "Núi (山) bên trên — từng năm tháng lớn lên vững vàng",
                "mnemonic": "Mỗi năm thêm một tuổi (岁) cao lớn như ngọn núi (山)!",
                "usageNoteVi": "Đặt trực tiếp sau số: 二十岁 (20 tuổi), KHÔNG cần động từ 是 (nói 我二十岁, không nói 我是二十岁).",
                "examples": [
                    {"hanzi": "小玲今年二十岁。", "pinyin": "Xiǎo Líng jīn nián èr shí suì.", "vi": "Tiểu Linh năm nay 20 tuổi."},
                    {"hanzi": "你今年几岁了？", "pinyin": "nǐ jīn nián jǐ suì le?", "vi": "Năm nay bạn mấy tuổi rồi?"},
                ],
            },
            {
                "hanzi": "今年", "pinyin": "jīn nián", "meaningVi": "năm nay", "pos": "Danh từ",
                "radical": "人", "literalVi": "今 (hiện tại) + 年 (năm)",
                "mnemonic": "今 (nay) + 年 (năm) = năm nay. Tương tự: 去年 (năm ngoái), 明年 (năm sau).",
                "usageNoteVi": "Đặt trước hoặc sau chủ ngữ đều được: 今年我二十岁 hoặc 我今年二十岁.",
                "examples": [
                    {"hanzi": "我今年二十一岁。", "pinyin": "wǒ jīn nián èr shí yī suì.", "vi": "Năm nay mình 21 tuổi."},
                    {"hanzi": "今年我在中国学中文。", "pinyin": "jīn nián wǒ zài Zhōng guó xué Zhōng wén.", "vi": "Năm nay mình học tiếng Trung ở Trung Quốc."},
                ],
            },
            {
                "hanzi": "年", "pinyin": "nián", "meaningVi": "năm", "pos": "Danh từ",
                "radical": "干", "literalVi": "Một mùa vụ thu hoạch trọn vẹn = 1 năm",
                "mnemonic": "Năm (年) trong tiếng Trung đọc từng chữ số: 2026年 đọc èr líng èr liù nián!",
                "usageNoteVi": "Không đọc hai nghìn không trăm... mà đọc từng số một trước chữ 年.",
                "examples": [
                    {"hanzi": "祝你新年快乐！", "pinyin": "zhù nǐ xīn nián kuài lè!", "vi": "Chúc bạn năm mới vui vẻ!"},
                    {"hanzi": "今年是二零二六年。", "pinyin": "jīn nián shì èr líng èr liù nián.", "vi": "Năm nay là năm 2026."},
                ],
            },
            {
                "hanzi": "月", "pinyin": "yuè", "meaningVi": "tháng, mặt trăng", "pos": "Danh từ",
                "radical": "月", "literalVi": "Hình vầng trăng khuyết — một chu kỳ trăng là 1 tháng",
                "mnemonic": "Hình vầng trăng cong có 2 vạch ngang ở giữa: 一月 (tháng 1) đến 十二月 (tháng 12).",
                "usageNoteVi": "Số + 月 = tên tháng (五月 = tháng 5). Lưu ý: '5 tháng' (khoảng thời gian) lại là 五个月!",
                "examples": [
                    {"hanzi": "我的生日是五月。", "pinyin": "wǒ de shēng rì shì wǔ yuè.", "vi": "Sinh nhật mình vào tháng 5."},
                    {"hanzi": "现在是十月。", "pinyin": "xiàn zài shì shí yuè.", "vi": "Bây giờ là tháng 10."},
                ],
            },
            {
                "hanzi": "号", "pinyin": "hào", "meaningVi": "ngày (trong tháng), số hiệu", "pos": "Danh từ",
                "radical": "口", "literalVi": "Kêu/đánh số trong văn nói",
                "mnemonic": "Văn nói dùng 号 (五月十号), còn văn viết trang trọng dùng 日 (五月十日).",
                "usageNoteVi": "Cũng dùng để hỏi số phòng, số điện thoại.",
                "examples": [
                    {"hanzi": "今天是六月十八号。", "pinyin": "jīn tiān shì liù yuè shí bā hào.", "vi": "Hôm nay là ngày 18 tháng 6."},
                    {"hanzi": "十月一号是节日。", "pinyin": "shí yuè yī hào shì jié rì.", "vi": "Ngày 1 tháng 10 là ngày lễ."},
                ],
            },
            {
                "hanzi": "生日", "pinyin": "shēng rì", "meaningVi": "sinh nhật", "pos": "Danh từ",
                "radical": "生", "literalVi": "生 (sinh ra) + 日 (ngày)",
                "mnemonic": "生 (mầm cây nhú lên = sinh ra) + 日 (mặt trời/ngày) = ngày sinh nhật!",
                "usageNoteVi": "Chúc sinh nhật: 生日快乐！(Shēngrì kuàilè!).",
                "examples": [
                    {"hanzi": "明天是小玲的生日！", "pinyin": "míng tiān shì Xiǎo Líng de shēng rì!", "vi": "Ngày mai là sinh nhật của Tiểu Linh!"},
                    {"hanzi": "你的生日是几月几号？", "pinyin": "nǐ de shēng rì shì jǐ yuè jǐ hào?", "vi": "Sinh nhật của bạn là ngày mấy tháng mấy?"},
                ],
            },
            {
                "hanzi": "快乐", "pinyin": "kuài lè", "meaningVi": "vui vẻ, hạnh phúc", "pos": "Tính từ",
                "radical": "忄", "literalVi": "快 (thoải mái, bộ tâm 忄) + 乐 (vui sướng)",
                "mnemonic": "Trái tim (忄) nhẹ nhàng vui sướng (乐) — chuyên dùng trong các lời chúc!",
                "usageNoteVi": "Hay đi với dịp lễ: 生日快乐 (sinh nhật vui vẻ), 新年快乐 (năm mới vui vẻ).",
                "examples": [
                    {"hanzi": "祝你生日快乐！", "pinyin": "zhù nǐ shēng rì kuài lè!", "vi": "Chúc bạn sinh nhật vui vẻ!"},
                    {"hanzi": "希望你每天都快乐！", "pinyin": "xī wàng nǐ měi tiān dōu kuài lè!", "vi": "Mong bạn mỗi ngày đều vui vẻ!"},
                ],
            },
        ],
        "patterns": [
            {
                "id": "p-t3-1", "frame": "你今年几___？", "pinyin": "nǐ jīn nián jǐ ___?", "meaningVi": "Năm nay bạn mấy tuổi?",
                "exampleHanzi": "你今年几岁？", "examplePinyin": "nǐ jīn nián jǐ suì?", "exampleVi": "Năm nay bạn mấy tuổi?",
                "slots": {
                    "promptVi": "Chọn từ để hỏi tuổi:",
                    "choices": [
                        {"hanzi": "岁", "pinyin": "suì", "vi": "tuổi"},
                        {"hanzi": "月", "pinyin": "yuè", "vi": "tháng"},
                        {"hanzi": "号", "pinyin": "hào", "vi": "ngày"},
                    ],
                    "answerHanzi": "岁",
                },
            },
            {
                "id": "p-t3-2", "frame": "今天是几___几号？", "pinyin": "jīn tiān shì jǐ ___ jǐ hào?", "meaningVi": "Hôm nay là ngày mấy tháng mấy?",
                "exampleHanzi": "今天是几月几号？", "examplePinyin": "jīn tiān shì jǐ yuè jǐ hào?", "exampleVi": "Hôm nay là ngày mấy tháng mấy?",
                "slots": {
                    "promptVi": "Điền đơn vị đứng trước 号 (ngày):",
                    "choices": [
                        {"hanzi": "月", "pinyin": "yuè", "vi": "tháng"},
                        {"hanzi": "岁", "pinyin": "suì", "vi": "tuổi"},
                        {"hanzi": "快乐", "pinyin": "kuài lè", "vi": "vui vẻ"},
                    ],
                    "answerHanzi": "月",
                },
            },
            {
                "id": "p-t3-3", "frame": "祝你___快乐！", "pinyin": "zhù nǐ ___ kuài lè!", "meaningVi": "Chúc bạn ___ vui vẻ!",
                "exampleHanzi": "祝你生日快乐！", "examplePinyin": "zhù nǐ shēng rì kuài lè!", "exampleVi": "Chúc bạn sinh nhật vui vẻ!",
                "slots": {
                    "promptVi": "Chọn từ để chúc Tiểu Linh sinh nhật vui vẻ:",
                    "choices": [
                        {"hanzi": "生日", "pinyin": "shēng rì", "vi": "sinh nhật"},
                        {"hanzi": "今年", "pinyin": "jīn nián", "vi": "năm nay"},
                        {"hanzi": "名字", "pinyin": "míng zi", "vi": "tên"},
                    ],
                    "answerHanzi": "生日",
                },
            },
        ],
        "dialogue": [
            {"speaker": "Bao", "voiceRole": "male", "hanzi": "小玲，今天几月几号？", "pinyin": "Xiǎo Líng, jīn tiān jǐ yuè jǐ hào?", "vi": "Tiểu Linh ơi, hôm nay ngày mấy tháng mấy thế?", "mode": "npc"},
            {"speaker": "Linh", "voiceRole": "female", "hanzi": "今天是五月九号。", "pinyin": "jīn tiān shì wǔ yuè jiǔ hào.", "vi": "Hôm nay là ngày 9 tháng 5.", "mode": "npc"},
            {
                "speaker": "Bao", "voiceRole": "male", "hanzi": "你的生日是几月几号？", "pinyin": "nǐ de shēng rì shì jǐ yuè jǐ hào?", "vi": "Sinh nhật của bạn là ngày mấy tháng mấy?",
                "mode": "choice", "goalLabel": "Hỏi ngày sinh nhật",
                "choices": [
                    {"hanzi": "你的生日是几月几号？", "pinyin": "nǐ de shēng rì shì jǐ yuè jǐ hào?", "vi": "Sinh nhật của bạn là ngày mấy tháng mấy?", "correct": True},
                    {"hanzi": "你叫什么名字？", "pinyin": "nǐ jiào shén me míng zi?", "vi": "Bạn tên gì?", "correct": False},
                    {"hanzi": "我是越南人。", "pinyin": "wǒ shì Yuè nán rén.", "vi": "Mình là người Việt Nam.", "correct": False},
                ],
            },
            {"speaker": "Linh", "voiceRole": "female", "hanzi": "明天五月十号是我的生日！我今年二十岁了。", "pinyin": "míng tiān wǔ yuè shí hào shì wǒ de shēng rì! wǒ jīn nián èr shí suì le.", "vi": "Ngày mai 10 tháng 5 là sinh nhật mình! Năm nay mình 20 tuổi rồi.", "mode": "npc"},
            {"speaker": "Bao", "voiceRole": "male", "hanzi": "祝你生日快乐！", "pinyin": "zhù nǐ shēng rì kuài lè!", "vi": "Chúc bạn sinh nhật vui vẻ!", "mode": "tiles", "goalLabel": "Chúc mừng sinh nhật", "tilePrompt": ["祝你", "生日", "快乐"]},
            {"speaker": "Linh", "voiceRole": "female", "hanzi": "谢谢你，Bao！明天一起玩吧！", "pinyin": "xiè xie nǐ, Bao! míng tiān yì qǐ wán ba!", "vi": "Cảm ơn Bao nhé! Mai đi chơi cùng nhau nào!", "mode": "npc"},
        ],
        "exercises": [
            {
                "id": "ex-t3-1", "kind": "meaning-choice", "promptVi": "「五月十八号」 là ngày nào?",
                "hanziPrompt": "五月十八号", "pinyinPrompt": "wǔ yuè shí bā hào",
                "options": [
                    {"label": "Ngày 18 tháng 5", "value": "Ngày 18 tháng 5"},
                    {"label": "Ngày 5 tháng 18", "value": "Ngày 5 tháng 18"},
                    {"label": "Ngày 8 tháng 5", "value": "Ngày 8 tháng 5"},
                    {"label": "Năm 18 tuổi", "value": "Năm 18 tuổi"},
                ],
                "answer": "Ngày 18 tháng 5",
                "explainVi": "Tiếng Trung nói tháng (五月) trước, ngày (十八号) sau!",
            },
            {
                "id": "ex-t3-2", "kind": "hanzi-choice", "promptVi": "Nghe và chọn chữ Hán có nghĩa 'sinh nhật'",
                "audioText": "生日",
                "options": [
                    {"label": "生日", "value": "生日"},
                    {"label": "今年", "value": "今年"},
                    {"label": "快乐", "value": "快乐"},
                    {"label": "几岁", "value": "几岁"},
                ],
                "answer": "生日",
            },
            {
                "id": "ex-t3-3", "kind": "match-pairs", "promptVi": "Ghép nhanh 4 cặp từ ngày tháng & tuổi:",
                "pairs": [
                    {"hanzi": "今年", "pinyin": "jīn nián", "vi": "Năm nay"},
                    {"hanzi": "月", "pinyin": "yuè", "vi": "Tháng"},
                    {"hanzi": "岁", "pinyin": "suì", "vi": "Tuổi"},
                    {"hanzi": "快乐", "pinyin": "kuài lè", "vi": "Vui vẻ"},
                ],
                "answer": "matched",
            },
            {
                "id": "ex-t3-4", "kind": "fill-blank", "promptVi": "Điền từ đúng: 「我今年二十___。」 (Năm nay mình 20 tuổi.)",
                "hanziPrompt": "我今年二十___。", "pinyinPrompt": "wǒ jīn nián èr shí ___.",
                "options": [
                    {"label": "岁", "value": "岁"},
                    {"label": "号", "value": "号"},
                    {"label": "月", "value": "月"},
                    {"label": "年", "value": "年"},
                ],
                "answer": "岁",
            },
            {
                "id": "ex-t3-5", "kind": "sentence-tiles", "promptVi": "Ghép câu: 'Hôm nay là sinh nhật của mình.'",
                "tiles": ["生日", "我的", "今天", "是"],
                "answer": "今天是我的生日",
            },
            {
                "id": "ex-t3-6", "kind": "meaning-choice", "promptVi": "Câu 「祝你生日快乐！」 dùng khi nào?",
                "hanziPrompt": "祝你生日快乐！", "pinyinPrompt": "zhù nǐ shēng rì kuài lè!",
                "options": [
                    {"label": "Chúc mừng sinh nhật bạn", "value": "Chúc mừng sinh nhật bạn"},
                    {"label": "Hỏi xem hôm nay là thứ mấy", "value": "Hỏi xem hôm nay là thứ mấy"},
                    {"label": "Xin lỗi vì đến muộn", "value": "Xin lỗi vì đến muộn"},
                    {"label": "Hỏi tên bạn mới", "value": "Hỏi tên bạn mới"},
                ],
                "answer": "Chúc mừng sinh nhật bạn",
            },
        ],
        "roleplay": [
            {
                "npcHanzi": "今天几月几号？", "npcPinyin": "jīn tiān jǐ yuè jǐ hào?", "npcVi": "Hôm nay ngày mấy tháng mấy?",
                "promptVi": "Trả lời hôm nay là ngày 10 tháng 5:",
                "options": [
                    {"hanzi": "今天是五月十号。", "pinyin": "jīn tiān shì wǔ yuè shí hào.", "vi": "Hôm nay là ngày 10 tháng 5.", "correct": True},
                    {"hanzi": "我今年十岁。", "pinyin": "wǒ jīn nián shí suì.", "vi": "Năm nay mình 10 tuổi.", "correct": False},
                    {"hanzi": "谢谢你。", "pinyin": "xiè xie nǐ.", "vi": "Cảm ơn bạn.", "correct": False},
                ],
                "expectedHanzi": "今天是五月十号。",
            },
            {
                "npcHanzi": "今天是我的生日！", "npcPinyin": "jīn tiān shì wǒ de shēng rì!", "npcVi": "Hôm nay là sinh nhật mình!",
                "promptVi": "Gửi lời chúc mừng sinh nhật vui vẻ:",
                "options": [
                    {"hanzi": "祝你生日快乐！", "pinyin": "zhù nǐ shēng rì kuài lè!", "vi": "Chúc bạn sinh nhật vui vẻ!", "correct": True},
                    {"hanzi": "对不起！", "pinyin": "duì bu qǐ!", "vi": "Xin lỗi!", "correct": False},
                    {"hanzi": "我是越南人。", "pinyin": "wǒ shì Yuè nán rén.", "vi": "Mình là người Việt Nam.", "correct": False},
                ],
                "expectedHanzi": "祝你生日快乐！",
            },
            {
                "npcHanzi": "你今年多大？", "npcPinyin": "nǐ jīn nián duō dà?", "npcVi": "Năm nay bạn bao nhiêu tuổi?",
                "promptVi": "Trả lời năm nay mình 20 tuổi:",
                "options": [
                    {"hanzi": "我今年二十岁。", "pinyin": "wǒ jīn nián èr shí suì.", "vi": "Năm nay mình 20 tuổi.", "correct": True},
                    {"hanzi": "我叫二十岁。", "pinyin": "wǒ jiào èr shí suì.", "vi": "Mình tên là 20 tuổi.", "correct": False},
                    {"hanzi": "再见！", "pinyin": "zài jiàn!", "vi": "Tạm biệt!", "correct": False},
                ],
                "expectedHanzi": "我今年二十岁。",
            },
        ],
        "writing": [
            {"char": "岁", "pinyin": "suì", "meaningVi": "tuổi", "radical": "山", "radicalNoteVi": "Bộ sơn (山) phía trên — lớn lên vững vàng từng năm.", "lookalikes": [{"hanzi": "岁", "pinyin": "suì", "vi": "tuổi"}, {"hanzi": "山", "pinyin": "shān", "vi": "núi"}, {"hanzi": "多", "pinyin": "duō", "vi": "nhiều"}, {"hanzi": "夕", "pinyin": "xī", "vi": "chiều tối"}]},
            {"char": "年", "pinyin": "nián", "meaningVi": "năm", "radical": "干", "radicalNoteVi": "Hình bông lúa thu hoạch mỗi năm một mùa.", "lookalikes": [{"hanzi": "年", "pinyin": "nián", "vi": "năm"}, {"hanzi": "午", "pinyin": "wǔ", "vi": "trưa"}, {"hanzi": "牛", "pinyin": "niú", "vi": "bò"}, {"hanzi": "半", "pinyin": "bàn", "vi": "nửa"}]},
            {"char": "月", "pinyin": "yuè", "meaningVi": "tháng, trăng", "radical": "月", "radicalNoteVi": "Bộ nguyệt (月) — hình vầng trăng khuyết.", "lookalikes": [{"hanzi": "月", "pinyin": "yuè", "vi": "tháng"}, {"hanzi": "日", "pinyin": "rì", "vi": "ngày"}, {"hanzi": "目", "pinyin": "mù", "vi": "mắt"}, {"hanzi": "用", "pinyin": "yòng", "vi": "dùng"}]},
        ],
    },
    {
        "topicId": 4,
        "title": "Gia đình & bạn bè",
        "subtitle": "Kể về người thân trong nhà và bạn thân Tiểu Minh",
        "storyTagVi": "Ngày 3 · Khoe ảnh gia đình cùng Linh",
        "connectsFromVi": "Tiếp nối Bài 3: Số đếm, tuổi & sinh nhật",
        "storyContextVi": "Khi xem ảnh sinh nhật (Bài 3), Bao hào hứng giới thiệu gia đình 4 người của mình và cậu bạn thân Tiểu Minh cho Linh biết!",
        "bridgeFromPrevVi": "Ở Bài 3 bạn đã biết đếm số và nói tuổi — hôm nay ghép vào để nói 'Nhà mình có mấy người' và kể về từng thành viên nhé!",
        "bridgeToNextVi": "Kể xong về Tiểu Minh, sang Bài 5 Bao sẽ học cách xem giờ và hẹn cả nhóm gặp nhau!",
        "recapWordIds": ["今年", "岁", "生日"],
        "cultureTipVi": "Khi đếm số người trong gia đình, người Trung Quốc dùng lượng từ 「口」(kǒu = miệng ăn): 我家有四口人 (Nhà mình có 4 người), mang ý nghĩa cả nhà cùng quây quần bên mâm cơm!",
        "grammarSpotlight": {
            "title": "Sở hữu 「的」 & Câu tồn tại 「我家有…口人」",
            "formula": "我家有 + Số + 口人  |  Chủ sở hữu + 的 + Người/Vật",
            "explainVi": "Dùng 有 (yǒu = có) để nói số người trong nhà. Với người thân ruột thịt (爸爸, 妈妈, 哥哥), người Trung Quốc thường lược bỏ 的 cho thân mật: 我爸爸, 我家.",
            "vsVietnameseVi": "Khác tiếng Việt: tiếng Việt nói 'mẹ của tôi' (Mẹ + Tôi), tiếng Trung đặt 'Tôi' lên trước: 我(的)妈妈!",
            "commonMistakeVi": "Quên lượng từ 口 hoặc 个: phải nói 四口人 / 两个朋友, không nói 四人 / 二朋友 (và nhớ dùng 两 chứ không dùng 二 trước lượng từ!).",
            "examples": [
                {"hanzi": "我家有四口人。", "pinyin": "wǒ jiā yǒu sì kǒu rén.", "vi": "Nhà mình có 4 người."},
                {"hanzi": "小明是我的好朋友。", "pinyin": "Xiǎo Míng shì wǒ de hǎo péng you.", "vi": "Tiểu Minh là bạn thân của mình."},
            ],
        },
        "words": [
            {
                "hanzi": "家", "pinyin": "jiā", "meaningVi": "nhà, gia đình", "pos": "Danh từ",
                "radical": "宀", "literalVi": "Mái nhà (宀) che chở cuộc sống ấm no (豕)",
                "mnemonic": "Dưới mái nhà (宀) có gia đình ấm áp quây quần!",
                "usageNoteVi": "回家 (huí jiā = về nhà), 在家 (zài jiā = ở nhà), 我家 (nhà mình).",
                "examples": [
                    {"hanzi": "我家有四口人。", "pinyin": "wǒ jiā yǒu sì kǒu rén.", "vi": "Nhà mình có 4 người."},
                    {"hanzi": "我很爱我的家。", "pinyin": "wǒ hěn ài wǒ de jiā.", "vi": "Mình rất yêu gia đình mình."},
                ],
            },
            {
                "hanzi": "爸爸", "pinyin": "bà ba", "meaningVi": "bố, ba", "pos": "Danh từ",
                "radical": "父", "literalVi": "Bộ phụ (父) chỉ người cha + âm đọc 巴",
                "mnemonic": "Bộ 父 ở trên giống đôi tay mạnh mẽ của bố che chở gia đình.",
                "usageNoteVi": "Chữ thứ hai đọc thanh nhẹ (bà ba).",
                "examples": [
                    {"hanzi": "我爸爸今年五十岁。", "pinyin": "wǒ bà ba jīn nián wǔ shí suì.", "vi": "Bố mình năm nay 50 tuổi."},
                    {"hanzi": "爸爸喜欢喝中国茶。", "pinyin": "bà ba xǐ huan hē Zhōng guó chá.", "vi": "Bố thích uống trà Trung Quốc."},
                ],
            },
            {
                "hanzi": "妈妈", "pinyin": "mā ma", "meaningVi": "mẹ, má", "pos": "Danh từ",
                "radical": "女", "literalVi": "Bộ nữ (女) + thanh phù 马 (mǎ)",
                "mnemonic": "Bên trái là người phụ nữ (女), bên phải gợi âm đọc 'ma' (马)!",
                "usageNoteVi": "Chữ thứ hai đọc thanh nhẹ (mā ma). Bố mẹ nói chung là 爸爸妈妈 hoặc 父母.",
                "examples": [
                    {"hanzi": "我妈妈很喜欢做饭。", "pinyin": "wǒ mā ma hěn xǐ huan zuò fàn.", "vi": "Mẹ mình rất thích nấu ăn."},
                    {"hanzi": "妈妈，生日快乐！", "pinyin": "mā ma, shēng rì kuài lè!", "vi": "Mẹ ơi, chúc mẹ sinh nhật vui vẻ!"},
                ],
            },
            {
                "hanzi": "哥哥", "pinyin": "gē ge", "meaningVi": "anh trai", "pos": "Danh từ",
                "radical": "口", "literalVi": "Hai chữ 可 xếp chồng lên nhau",
                "mnemonic": "Anh trai lúc nào cũng nói 'được, để anh lo!' (可 + 可 = 哥).",
                "usageNoteVi": "Chữ thứ hai đọc thanh nhẹ (gē ge). Em trai là 弟弟 (dì di).",
                "examples": [
                    {"hanzi": "我有一个哥哥。", "pinyin": "wǒ yǒu yí gè gē ge.", "vi": "Mình có một người anh trai."},
                    {"hanzi": "哥哥在北京工作。", "pinyin": "gē ge zài Běi jīng gōng zuò.", "vi": "Anh trai làm việc ở Bắc Kinh."},
                ],
            },
            {
                "hanzi": "姐姐", "pinyin": "jiě jie", "meaningVi": "chị gái", "pos": "Danh từ",
                "radical": "女", "literalVi": "Bộ nữ (女) + 且",
                "mnemonic": "Có bộ nữ (女) chỉ người phụ nữ dịu dàng — chị gái!",
                "usageNoteVi": "Em gái là 妹妹 (mèi mei). Tất cả đều có bộ 女 ở bên trái!",
                "examples": [
                    {"hanzi": "我姐姐很可爱。", "pinyin": "wǒ jiě jie hěn kě ài.", "vi": "Chị gái mình rất dễ thương."},
                    {"hanzi": "姐姐今年二十五岁。", "pinyin": "jiě jie jīn nián èr shí wǔ suì.", "vi": "Chị gái năm nay 25 tuổi."},
                ],
            },
            {
                "hanzi": "朋友", "pinyin": "péng you", "meaningVi": "bạn bè", "pos": "Danh từ",
                "radical": "月", "literalVi": "朋 (hai vầng trăng sóng đôi) + 友 (hai bàn tay nắm lấy nhau)",
                "mnemonic": "朋 có hai chữ 月 đi cùng nhau — bạn bè luôn đồng hành!",
                "usageNoteVi": "好朋友 = bạn thân, 中国朋友 = bạn người Trung Quốc.",
                "examples": [
                    {"hanzi": "小明是我的好朋友。", "pinyin": "Xiǎo Míng shì wǒ de hǎo péng you.", "vi": "Tiểu Minh là bạn thân của mình."},
                    {"hanzi": "我有很多中国朋友。", "pinyin": "wǒ yǒu hěn duō Zhōng guó péng you.", "vi": "Mình có rất nhiều bạn Trung Quốc."},
                ],
            },
            {
                "hanzi": "有", "pinyin": "yǒu", "meaningVi": "có", "pos": "Động từ",
                "radical": "月", "literalVi": "Bàn tay cầm nắm thứ gì đó",
                "mnemonic": "Bàn tay đưa ra giữ lấy — nghĩa là 'có'. Phủ định luôn là 没有 (không có)!",
                "usageNoteVi": "TUYỆT ĐỐI không nói 不有 — phủ định của 有 luôn là 没有 (méi yǒu)!",
                "examples": [
                    {"hanzi": "你家有几口人？", "pinyin": "nǐ jiā yǒu jǐ kǒu rén?", "vi": "Nhà bạn có mấy người?"},
                    {"hanzi": "我没有哥哥，我有一个姐姐。", "pinyin": "wǒ méi yǒu gē ge, wǒ yǒu yí gè jiě jie.", "vi": "Mình không có anh trai, mình có một chị gái."},
                ],
            },
            {
                "hanzi": "爱", "pinyin": "ài", "meaningVi": "yêu, thích", "pos": "Động từ",
                "radical": "爫", "literalVi": "Bàn tay che chở người bạn (友) dưới mái ấm",
                "mnemonic": "Chữ 爱 chứa hình bàn tay nâng niu người thân yêu!",
                "usageNoteVi": "Dùng cho tình yêu gia đình, bạn bè, hay sở thích mãnh liệt (我爱学中文).",
                "examples": [
                    {"hanzi": "我爱爸爸和妈妈。", "pinyin": "wǒ ài bà ba hé mā ma.", "vi": "Mình yêu bố và mẹ."},
                    {"hanzi": "Bao很爱学习中文。", "pinyin": "Bao hěn ài xué xí Zhōng wén.", "vi": "Bao rất yêu việc học tiếng Trung."},
                ],
            },
        ],
        "patterns": [
            {
                "id": "p-t4-1", "frame": "我家有___口人。", "pinyin": "wǒ jiā yǒu ___ kǒu rén.", "meaningVi": "Nhà mình có ___ người.",
                "exampleHanzi": "我家有四口人。", "examplePinyin": "wǒ jiā yǒu sì kǒu rén.", "exampleVi": "Nhà mình có 4 người.",
                "slots": {
                    "promptVi": "Điền từ chỉ số lượng để nói 'Nhà mình có 4 người':",
                    "choices": [
                        {"hanzi": "四", "pinyin": "sì", "vi": "bốn"},
                        {"hanzi": "几", "pinyin": "jǐ", "vi": "mấy (hỏi)"},
                        {"hanzi": "岁", "pinyin": "suì", "vi": "tuổi"},
                    ],
                    "answerHanzi": "四",
                },
            },
            {
                "id": "p-t4-2", "frame": "我没有___。", "pinyin": "wǒ méi yǒu ___.", "meaningVi": "Mình không có ___.",
                "exampleHanzi": "我没有哥哥。", "examplePinyin": "wǒ méi yǒu gē ge.", "exampleVi": "Mình không có anh trai.",
                "slots": {
                    "promptVi": "Nói 'Mình không có anh trai':",
                    "choices": [
                        {"hanzi": "哥哥", "pinyin": "gē ge", "vi": "anh trai"},
                        {"hanzi": "姐姐", "pinyin": "jiě jie", "vi": "chị gái"},
                        {"hanzi": "朋友", "pinyin": "péng you", "vi": "bạn bè"},
                    ],
                    "answerHanzi": "哥哥",
                },
            },
            {
                "id": "p-t4-3", "frame": "这是我的好___。", "pinyin": "zhè shì wǒ de hǎo ___.", "meaningVi": "Đây là ___ tốt của mình.",
                "exampleHanzi": "这是我的好朋友。", "examplePinyin": "zhè shì wǒ de hǎo péng you.", "exampleVi": "Đây là bạn thân của mình.",
                "slots": {
                    "promptVi": "Giới thiệu Tiểu Minh là bạn thân của Bao:",
                    "choices": [
                        {"hanzi": "朋友", "pinyin": "péng you", "vi": "bạn bè"},
                        {"hanzi": "家", "pinyin": "jiā", "vi": "gia đình"},
                        {"hanzi": "爸爸", "pinyin": "bà ba", "vi": "bố"},
                    ],
                    "answerHanzi": "朋友",
                },
            },
        ],
        "dialogue": [
            {"speaker": "Linh", "voiceRole": "female", "hanzi": "Bao，你家有几口人？", "pinyin": "Bao, nǐ jiā yǒu jǐ kǒu rén?", "vi": "Bao ơi, nhà bạn có mấy người?", "mode": "npc"},
            {
                "speaker": "Bao", "voiceRole": "male", "hanzi": "我家有四口人：爸爸、妈妈、姐姐和我。", "pinyin": "wǒ jiā yǒu sì kǒu rén: bà ba, mā ma, jiě jie hé wǒ.", "vi": "Nhà mình có 4 người: bố, mẹ, chị gái và mình.",
                "mode": "choice", "goalLabel": "Kể thành viên gia đình",
                "choices": [
                    {"hanzi": "我家有四口人：爸爸、妈妈、姐姐和我。", "pinyin": "wǒ jiā yǒu sì kǒu rén: bà ba, mā ma, jiě jie hé wǒ.", "vi": "Nhà mình có 4 người: bố, mẹ, chị gái và mình.", "correct": True},
                    {"hanzi": "我今年四岁。", "pinyin": "wǒ jīn nián sì suì.", "vi": "Năm nay mình 4 tuổi.", "correct": False},
                    {"hanzi": "我是四月人。", "pinyin": "wǒ shì sì yuè rén.", "vi": "Mình là người tháng 4.", "correct": False},
                ],
            },
            {"speaker": "Linh", "voiceRole": "female", "hanzi": "你有哥哥吗？", "pinyin": "nǐ yǒu gē ge ma?", "vi": "Bạn có anh trai không?", "mode": "npc"},
            {"speaker": "Bao", "voiceRole": "male", "hanzi": "我没有哥哥。", "pinyin": "wǒ méi yǒu gē ge.", "vi": "Mình không có anh trai.", "mode": "tiles", "goalLabel": "Trả lời phủ định với 没有", "tilePrompt": ["我", "没有", "哥哥"]},
            {"speaker": "Linh", "voiceRole": "female", "hanzi": "照片里这个男生是谁？", "pinyin": "zhào piàn lǐ zhè gè nán shēng shì shéi?", "vi": "Bạn nam trong ảnh này là ai thế?", "mode": "npc"},
            {"speaker": "Bao", "voiceRole": "male", "hanzi": "他叫小明，是我的好朋友！", "pinyin": "tā jiào Xiǎo Míng, shì wǒ de hǎo péng you!", "vi": "Cậu ấy tên Tiểu Minh, là bạn thân của mình!", "mode": "pinyin", "goalLabel": "Giới thiệu bạn thân", "acceptedPinyin": ["ta jiao xiaoming shi wode hao pengyou", "tajiaoxiaomingshiwodehaopengyou", "他叫小明，是我的好朋友", "他是我的好朋友"]},
        ],
        "exercises": [
            {
                "id": "ex-t4-1", "kind": "meaning-choice", "promptVi": "「姐姐」 có nghĩa là gì?",
                "hanziPrompt": "姐姐", "pinyinPrompt": "jiě jie",
                "options": [
                    {"label": "Chị gái", "value": "Chị gái"},
                    {"label": "Anh trai", "value": "Anh trai"},
                    {"label": "Mẹ", "value": "Mẹ"},
                    {"label": "Bạn thân", "value": "Bạn thân"},
                ],
                "answer": "Chị gái",
            },
            {
                "id": "ex-t4-2", "kind": "hanzi-choice", "promptVi": "Nghe và chọn chữ Hán có nghĩa 'bạn bè'",
                "audioText": "朋友",
                "options": [
                    {"label": "朋友", "value": "朋友"},
                    {"label": "哥哥", "value": "哥哥"},
                    {"label": "爸爸", "value": "爸爸"},
                    {"label": "家人", "value": "家人"},
                ],
                "answer": "朋友",
            },
            {
                "id": "ex-t4-3", "kind": "match-pairs", "promptVi": "Ghép 4 cặp từ gia đình:",
                "pairs": [
                    {"hanzi": "爸爸", "pinyin": "bà ba", "vi": "Bố"},
                    {"hanzi": "妈妈", "pinyin": "mā ma", "vi": "Mẹ"},
                    {"hanzi": "哥哥", "pinyin": "gē ge", "vi": "Anh trai"},
                    {"hanzi": "家", "pinyin": "jiā", "vi": "Gia đình"},
                ],
                "answer": "matched",
            },
            {
                "id": "ex-t4-4", "kind": "fill-blank", "promptVi": "Phủ định của 有 là gì? 「我___哥哥。」",
                "hanziPrompt": "我___哥哥。", "pinyinPrompt": "wǒ ___ gē ge.",
                "options": [
                    {"label": "没有", "value": "没有"},
                    {"label": "不有", "value": "不有"},
                    {"label": "不是", "value": "不是"},
                    {"label": "不叫", "value": "不叫"},
                ],
                "answer": "没有",
                "explainVi": "Nhớ quy tắc vàng: phủ định của 有 luôn là 没有, không bao giờ nói 不有!",
            },
            {
                "id": "ex-t4-5", "kind": "sentence-tiles", "promptVi": "Ghép câu: 'Tiểu Minh là bạn thân của mình.'",
                "tiles": ["好朋友", "小明", "我的", "是"],
                "answer": "小明是我的好朋友",
            },
            {
                "id": "ex-t4-6", "kind": "meaning-choice", "promptVi": "Câu 「我家有四口人，我爱我的家。」 nghĩa là gì?",
                "hanziPrompt": "我家有四口人，我爱我的家。", "pinyinPrompt": "wǒ jiā yǒu sì kǒu rén, wǒ ài wǒ de jiā.",
                "options": [
                    {"label": "Nhà mình có 4 người, mình yêu gia đình mình.", "value": "Nhà mình có 4 người, mình yêu gia đình mình."},
                    {"label": "Nhà mình có 4 người bạn thân.", "value": "Nhà mình có 4 người bạn thân."},
                    {"label": "Mình có 4 người anh trai.", "value": "Mình có 4 người anh trai."},
                    {"label": "Hôm nay là ngày 4 tháng 4.", "value": "Hôm nay là ngày 4 tháng 4."},
                ],
                "answer": "Nhà mình có 4 người, mình yêu gia đình mình.",
            },
        ],
        "roleplay": [
            {
                "npcHanzi": "你家有几口人？", "npcPinyin": "nǐ jiā yǒu jǐ kǒu rén?", "npcVi": "Nhà bạn có mấy người?",
                "promptVi": "Trả lời nhà mình có 4 người:",
                "options": [
                    {"hanzi": "我家有四口人。", "pinyin": "wǒ jiā yǒu sì kǒu rén.", "vi": "Nhà mình có 4 người.", "correct": True},
                    {"hanzi": "我今年四岁。", "pinyin": "wǒ jīn nián sì suì.", "vi": "Năm nay mình 4 tuổi.", "correct": False},
                    {"hanzi": "不客气。", "pinyin": "bú kè qi.", "vi": "Không có gì.", "correct": False},
                ],
                "expectedHanzi": "我家有四口人。",
            },
            {
                "npcHanzi": "你有姐姐吗？", "npcPinyin": "nǐ yǒu jiě jie ma?", "npcVi": "Bạn có chị gái không?",
                "promptVi": "Trả lời mình có một chị gái:",
                "options": [
                    {"hanzi": "有，我有一个姐姐。", "pinyin": "yǒu, wǒ yǒu yí gè jiě jie.", "vi": "Có, mình có một chị gái.", "correct": True},
                    {"hanzi": "我叫姐姐。", "pinyin": "wǒ jiào jiě jie.", "vi": "Mình tên là chị gái.", "correct": False},
                    {"hanzi": "祝你生日快乐！", "pinyin": "zhù nǐ shēng rì kuài lè!", "vi": "Chúc mừng sinh nhật!", "correct": False},
                ],
                "expectedHanzi": "有，我有一个姐姐。",
            },
            {
                "npcHanzi": "小明是你的同学吗？", "npcPinyin": "Xiǎo Míng shì nǐ de tóng xué ma?", "npcVi": "Tiểu Minh là bạn học của bạn à?",
                "promptVi": "Đáp cậu ấy là bạn thân của mình:",
                "options": [
                    {"hanzi": "对，他是我的好朋友！", "pinyin": "duì, tā shì wǒ de hǎo péng you!", "vi": "Đúng rồi, cậu ấy là bạn thân của mình!", "correct": True},
                    {"hanzi": "我没有时间。", "pinyin": "wǒ méi yǒu shí jiān.", "vi": "Mình không có thời gian.", "correct": False},
                    {"hanzi": "再见！", "pinyin": "zài jiàn!", "vi": "Tạm biệt!", "correct": False},
                ],
                "expectedHanzi": "对，他是我的好朋友！",
            },
        ],
        "writing": [
            {"char": "家", "pinyin": "jiā", "meaningVi": "nhà, gia đình", "radical": "宀", "radicalNoteVi": "Bộ miên (宀) là mái nhà che chở cho cả gia đình.", "lookalikes": [{"hanzi": "家", "pinyin": "jiā", "vi": "nhà"}, {"hanzi": "室", "pinyin": "shì", "vi": "phòng"}, {"hanzi": "安", "pinyin": "ān", "vi": "an lành"}, {"hanzi": "字", "pinyin": "zì", "vi": "chữ"}]},
            {"char": "爸", "pinyin": "bà", "meaningVi": "bố, ba", "radical": "父", "radicalNoteVi": "Bộ phụ (父) ở trên chỉ cha, phần 巴 ở dưới gợi âm đọc.", "lookalikes": [{"hanzi": "爸", "pinyin": "bà", "vi": "bố"}, {"hanzi": "吧", "pinyin": "ba", "vi": "nhé"}, {"hanzi": "把", "pinyin": "bǎ", "vi": "cầm/đem"}, {"hanzi": "爷", "pinyin": "yé", "vi": "ông"}]},
            {"char": "妈", "pinyin": "mā", "meaningVi": "mẹ, má", "radical": "女", "radicalNoteVi": "Bộ nữ (女) chỉ phụ nữ, ghép chữ 马 gợi âm đọc mā.", "lookalikes": [{"hanzi": "妈", "pinyin": "mā", "vi": "mẹ"}, {"hanzi": "吗", "pinyin": "ma", "vi": "không?"}, {"hanzi": "姐", "pinyin": "jiě", "vi": "chị"}, {"hanzi": "好", "pinyin": "hǎo", "vi": "tốt"}]},
        ],
    },
    {
        "topicId": 5,
        "title": "Thời gian & hẹn gặp",
        "subtitle": "Hỏi mấy giờ, nói sáng/chiều/tối và đặt lịch hẹn bạn",
        "storyTagVi": "Ngày 4 · Chốt giờ đi uống trà sữa",
        "connectsFromVi": "Tiếp nối Bài 4: Gia đình & bạn bè",
        "storyContextVi": "Muốn rủ cả Linh lẫn cậu bạn thân Tiểu Minh (Bài 4) đi chơi sau giờ học, Bao cần biết hỏi giờ và chốt lịch hẹn chính xác!",
        "bridgeFromPrevVi": "Đã quen Linh và Tiểu Minh ở Bài 4 — giờ cùng học cách hỏi giờ và hẹn gặp nhau lúc 3 giờ chiều nhé!",
        "bridgeToNextVi": "Chốt lịch hẹn xong rồi! Sang Bài 6 cả nhóm kéo nhau tới quán trà sữa phố cổ gọi món ngon!",
        "recapWordIds": ["朋友", "同学", "家"],
        "cultureTipVi": "Trong tiếng Trung, trạng ngữ thời gian (今天, 明天, 下午三点) luôn đứng TRƯỚC động từ (VD: 我下午三点去, không nói 我去下午三点 như tiếng Việt!).",
        "grammarSpotlight": {
            "title": "Vị trí thời gian trong câu & Cách nói giờ",
            "formula": "Chủ ngữ + [Thời gian] + Động từ  |  ___点 ___分 (___ giờ ___ phút)",
            "explainVi": "Giờ dùng 点 (diǎn), phút dùng 分 (fēn), rưỡi dùng 半 (bàn). Lưu ý 2 giờ luôn nói 两点 (liǎng diǎn), không nói 二点!",
            "vsVietnameseVi": "Tiếng Việt đặt thời gian cuối câu ('Tôi đi lúc 3 giờ'), còn tiếng Trung đặt TRƯỚC động từ ('我三点去').",
            "commonMistakeVi": "Nói 二点 thay vì 两点, hoặc để 明天/三点 ra cuối câu!",
            "examples": [
                {"hanzi": "现在下午三点半。", "pinyin": "xiàn zài xià wǔ sān diǎn bàn.", "vi": "Bây giờ là 3 giờ rưỡi chiều."},
                {"hanzi": "我们明天下午两点见！", "pinyin": "wǒ men míng tiān xià wǔ liǎng diǎn jiàn!", "vi": "Chúng mình hẹn gặp 2 giờ chiều mai nhé!"},
            ],
        },
        "words": [
            {
                "hanzi": "今天", "pinyin": "jīn tiān", "meaningVi": "hôm nay", "pos": "Danh từ",
                "radical": "人", "literalVi": "今 (hiện tại) + 天 (ngày/trời)",
                "mnemonic": "今 (nay) + 天 (ngày) = hôm nay. So với 今年 (năm nay) ở Bài 3!",
                "usageNoteVi": "Đứng đầu câu hoặc ngay sau chủ ngữ: 今天我有课 / 我今天有课.",
                "examples": [
                    {"hanzi": "你今天有时间吗？", "pinyin": "nǐ jīn tiān yǒu shí jiān ma?", "vi": "Hôm nay bạn có thời gian không?"},
                    {"hanzi": "今天天气很好！", "pinyin": "jīn tiān tiān qì hěn hǎo!", "vi": "Thời tiết hôm nay rất đẹp!"},
                ],
            },
            {
                "hanzi": "明天", "pinyin": "míng tiān", "meaningVi": "ngày mai", "pos": "Danh từ",
                "radical": "日", "literalVi": "明 (mặt trời 日 + mặt trăng 月 = sáng rõ) + 天 (ngày)",
                "mnemonic": "Mặt trời (日) lặn rồi trăng (月) lại qua là sang ngày mai (明天)!",
                "usageNoteVi": "Hôm qua là 昨天 (zuó tiān), hôm nay 今天, ngày mai 明天.",
                "examples": [
                    {"hanzi": "我们明天见！", "pinyin": "wǒ men míng tiān jiàn!", "vi": "Hẹn gặp nhau ngày mai nhé!"},
                    {"hanzi": "明天下午我们去喝奶茶吧。", "pinyin": "míng tiān xià wǔ wǒ men qù hē nǎi chá ba.", "vi": "Chiều mai chúng mình đi uống trà sữa nhé."},
                ],
            },
            {
                "hanzi": "现在", "pinyin": "xiàn zài", "meaningVi": "bây giờ, hiện tại", "pos": "Danh từ",
                "radical": "王", "literalVi": "现 (hiện ra) + 在 (đang ở)",
                "mnemonic": "Điều đang hiện (现) ngay tại (在) lúc này chính là 'bây giờ'!",
                "usageNoteVi": "Hỏi giờ cực chuẩn: 现在几点？(Bây giờ mấy giờ rồi?).",
                "examples": [
                    {"hanzi": "请问，现在几点？", "pinyin": "qǐng wèn, xiàn zài jǐ diǎn?", "vi": "Xin hỏi, bây giờ là mấy giờ?"},
                    {"hanzi": "我现在在学校。", "pinyin": "wǒ xiàn zài zài xué xiào.", "vi": "Bây giờ mình đang ở trường."},
                ],
            },
            {
                "hanzi": "点", "pinyin": "diǎn", "meaningVi": "giờ (trên đồng hồ)", "pos": "Lượng từ",
                "radical": "灬", "literalVi": "Điểm mốc chỉ giờ",
                "mnemonic": "4 chấm lửa (灬) ở dưới như chấm giờ trên mặt đồng hồ.",
                "usageNoteVi": "2 giờ là 两点 (KHÔNG nói 二点!). 3 giờ rưỡi là 三点半.",
                "examples": [
                    {"hanzi": "现在两点十分。", "pinyin": "xiàn zài liǎng diǎn shí fēn.", "vi": "Bây giờ là 2 giờ 10 phút."},
                    {"hanzi": "我们下午三点见。", "pinyin": "wǒ men xià wǔ sān diǎn jiàn.", "vi": "Chúng mình gặp lúc 3 giờ chiều nhé."},
                ],
            },
            {
                "hanzi": "分钟", "pinyin": "fēn zhōng", "meaningVi": "phút (khoảng thời gian)", "pos": "Danh từ",
                "radical": "刀", "literalVi": "分 (chia nhỏ) + 钟 (đồng hồ)",
                "mnemonic": "Con dao (刀) chia (分) một giờ trên đồng hồ (钟) thành 60 phút!",
                "usageNoteVi": "Đọc giờ trên đồng hồ nói 分 (三点十分); đếm độ dài thời gian nói 分钟 (等十分钟 = đợi 10 phút).",
                "examples": [
                    {"hanzi": "请等我五分钟！", "pinyin": "qǐng děng wǒ wǔ fēn zhōng!", "vi": "Đợi mình 5 phút nhé!"},
                    {"hanzi": "走路只要十分钟。", "pinyin": "zǒu lù zhǐ yào shí fēn zhōng.", "vi": "Đi bộ chỉ mất 10 phút thôi."},
                ],
            },
            {
                "hanzi": "下午", "pinyin": "xià wǔ", "meaningVi": "buổi chiều", "pos": "Danh từ",
                "radical": "一", "literalVi": "下 (sau) + 午 (buổi trưa)",
                "mnemonic": "Trước trưa là 上午 (buổi sáng), giữa trưa là 中午, sau trưa là 下午 (buổi chiều)!",
                "usageNoteVi": "Luôn đặt buổi (上午/下午/晚上) TRƯỚC số giờ: 下午三点.",
                "examples": [
                    {"hanzi": "今天下午你有空吗？", "pinyin": "jīn tiān xià wǔ nǐ yǒu kòng ma?", "vi": "Chiều nay bạn có rảnh không?"},
                    {"hanzi": "下午四点我们下课。", "pinyin": "xià wǔ sì diǎn wǒ men xià kè.", "vi": "4 giờ chiều chúng mình tan học."},
                ],
            },
            {
                "hanzi": "晚上", "pinyin": "wǎn shang", "meaningVi": "buổi tối", "pos": "Danh từ",
                "radical": "日", "literalVi": "晚 (muộn/tối, bộ nhật 日) + 上",
                "mnemonic": "Bộ nhật (日) mặt trời đã lặn muộn — trời tối rồi!",
                "usageNoteVi": "Chào buổi tối: 晚上好！(Wǎn shang hǎo!).",
                "examples": [
                    {"hanzi": "晚上好！你吃饭了吗？", "pinyin": "wǎn shang hǎo! nǐ chī fàn le ma?", "vi": "Chào buổi tối! Bạn ăn cơm chưa?"},
                    {"hanzi": "今天晚上七点见！", "pinyin": "jīn tiān wǎn shang qī diǎn jiàn!", "vi": "Tối nay 7 giờ gặp nhé!"},
                ],
            },
            {
                "hanzi": "时间", "pinyin": "shí jiān", "meaningVi": "thời gian", "pos": "Danh từ",
                "radical": "日", "literalVi": "时 (giờ, bộ nhật 日) + 间 (khoảng giữa)",
                "mnemonic": "Ánh nắng (日) lọt qua khe cửa (门 + 日 = 间) đánh dấu dòng chảy thời gian!",
                "usageNoteVi": "有时间 (có thời gian), 没有时间 (không có thời gian).",
                "examples": [
                    {"hanzi": "明天下午我有时间。", "pinyin": "míng tiān xià wǔ wǒ yǒu shí jiān.", "vi": "Chiều mai mình có thời gian."},
                    {"hanzi": "不好意思，我现在没有时间。", "pinyin": "bù hǎo yì si, wǒ xiàn zài méi yǒu shí jiān.", "vi": "Ngại quá, bây giờ mình không có thời gian."},
                ],
            },
        ],
        "patterns": [
            {
                "id": "p-t5-1", "frame": "现在几___？", "pinyin": "xiàn zài jǐ ___?", "meaningVi": "Bây giờ là mấy giờ?",
                "exampleHanzi": "现在几点？", "examplePinyin": "xiàn zài jǐ diǎn?", "exampleVi": "Bây giờ mấy giờ rồi?",
                "slots": {
                    "promptVi": "Điền từ để hỏi mấy giờ:",
                    "choices": [
                        {"hanzi": "点", "pinyin": "diǎn", "vi": "giờ"},
                        {"hanzi": "岁", "pinyin": "suì", "vi": "tuổi"},
                        {"hanzi": "号", "pinyin": "hào", "vi": "ngày"},
                    ],
                    "answerHanzi": "点",
                },
            },
            {
                "id": "p-t5-2", "frame": "你明天___有时间吗？", "pinyin": "nǐ míng tiān ___ yǒu shí jiān ma?", "meaningVi": "Buổi ___ ngày mai bạn có thời gian không?",
                "exampleHanzi": "你明天下午有时间吗？", "examplePinyin": "nǐ míng tiān xià wǔ yǒu shí jiān ma?", "exampleVi": "Chiều mai bạn có thời gian không?",
                "slots": {
                    "promptVi": "Hỏi xem chiều mai bạn có rảnh không:",
                    "choices": [
                        {"hanzi": "下午", "pinyin": "xià wǔ", "vi": "buổi chiều"},
                        {"hanzi": "分钟", "pinyin": "fēn zhōng", "vi": "phút"},
                        {"hanzi": "现在", "pinyin": "xiàn zài", "vi": "bây giờ"},
                    ],
                    "answerHanzi": "下午",
                },
            },
            {
                "id": "p-t5-3", "frame": "我们下午___点见！", "pinyin": "wǒ men xià wǔ ___ diǎn jiàn!", "meaningVi": "Chúng mình gặp lúc ___ giờ chiều nhé!",
                "exampleHanzi": "我们下午两点见！", "examplePinyin": "wǒ men xià wǔ liǎng diǎn jiàn!", "exampleVi": "Chúng mình gặp lúc 2 giờ chiều nhé!",
                "slots": {
                    "promptVi": "Cách nói ĐÚNG của '2 giờ' là từ nào?",
                    "choices": [
                        {"hanzi": "两", "pinyin": "liǎng", "vi": "hai (dùng cho giờ/lượng từ)"},
                        {"hanzi": "二", "pinyin": "èr", "vi": "số hai (không dùng với 点)"},
                        {"hanzi": "几", "pinyin": "jǐ", "vi": "mấy"},
                    ],
                    "answerHanzi": "两",
                },
            },
        ],
        "dialogue": [
            {"speaker": "Bao", "voiceRole": "male", "hanzi": "小玲，现在几点了？", "pinyin": "Xiǎo Líng, xiàn zài jǐ diǎn le?", "vi": "Tiểu Linh ơi, bây giờ mấy giờ rồi?", "mode": "npc"},
            {"speaker": "Linh", "voiceRole": "female", "hanzi": "现在下午两点半。", "pinyin": "xiàn zài xià wǔ liǎng diǎn bàn.", "vi": "Bây giờ là 2 giờ rưỡi chiều.", "mode": "npc"},
            {
                "speaker": "Bao", "voiceRole": "male", "hanzi": "你今天晚上有时间吗？", "pinyin": "nǐ jīn tiān wǎn shang yǒu shí jiān ma?", "vi": "Tối nay bạn có thời gian không?",
                "mode": "choice", "goalLabel": "Hỏi lịch rảnh",
                "choices": [
                    {"hanzi": "你今天晚上有时间吗？", "pinyin": "nǐ jīn tiān wǎn shang yǒu shí jiān ma?", "vi": "Tối nay bạn có thời gian không?", "correct": True},
                    {"hanzi": "你家有几口人？", "pinyin": "nǐ jiā yǒu jǐ kǒu rén?", "vi": "Nhà bạn có mấy người?", "correct": False},
                    {"hanzi": "现在三分钟。", "pinyin": "xiàn zài sān fēn zhōng.", "vi": "Bây giờ là 3 phút.", "correct": False},
                ],
            },
            {"speaker": "Linh", "voiceRole": "female", "hanzi": "有啊！小明也一起去吗？", "pinyin": "yǒu a! Xiǎo Míng yě yì qǐ qù ma?", "vi": "Có chứ! Tiểu Minh cũng đi cùng à?", "mode": "npc"},
            {"speaker": "Bao", "voiceRole": "male", "hanzi": "我们下午四点见！", "pinyin": "wǒ men xià wǔ sì diǎn jiàn!", "vi": "Chúng mình gặp lúc 4 giờ chiều nhé!", "mode": "tiles", "goalLabel": "Chốt giờ hẹn", "tilePrompt": ["我们", "下午", "四点", "见"]},
            {"speaker": "Linh", "voiceRole": "female", "hanzi": "好，四点见！", "pinyin": "hǎo, sì diǎn jiàn!", "vi": "Được, 4 giờ gặp nhé!", "mode": "npc"},
        ],
        "exercises": [
            {
                "id": "ex-t5-1", "kind": "meaning-choice", "promptVi": "「现在下午两点半」 là mấy giờ?",
                "hanziPrompt": "现在下午两点半", "pinyinPrompt": "xiàn zài xià wǔ liǎng diǎn bàn",
                "options": [
                    {"label": "Bây giờ là 2 giờ 30 chiều", "value": "Bây giờ là 2 giờ 30 chiều"},
                    {"label": "Bây giờ là 2 giờ sáng", "value": "Bây giờ là 2 giờ sáng"},
                    {"label": "Ngày mai gặp lúc 2 giờ", "value": "Ngày mai gặp lúc 2 giờ"},
                    {"label": "Đợi 2 phút nữa", "value": "Đợi 2 phút nữa"},
                ],
                "answer": "Bây giờ là 2 giờ 30 chiều",
            },
            {
                "id": "ex-t5-2", "kind": "hanzi-choice", "promptVi": "Nghe và chọn chữ Hán có nghĩa 'thời gian'",
                "audioText": "时间",
                "options": [
                    {"label": "时间", "value": "时间"},
                    {"label": "分钟", "value": "分钟"},
                    {"label": "现在", "value": "现在"},
                    {"label": "明天", "value": "明天"},
                ],
                "answer": "时间",
            },
            {
                "id": "ex-t5-3", "kind": "match-pairs", "promptVi": "Ghép 4 cặp từ thời gian:",
                "pairs": [
                    {"hanzi": "今天", "pinyin": "jīn tiān", "vi": "Hôm nay"},
                    {"hanzi": "明天", "pinyin": "míng tiān", "vi": "Ngày mai"},
                    {"hanzi": "下午", "pinyin": "xià wǔ", "vi": "Buổi chiều"},
                    {"hanzi": "晚上", "pinyin": "wǎn shang", "vi": "Buổi tối"},
                ],
                "answer": "matched",
            },
            {
                "id": "ex-t5-4", "kind": "fill-blank", "promptVi": "Điền từ đúng: 「请等我五___！」 (Đợi mình 5 phút nhé!)",
                "hanziPrompt": "请等我五___！", "pinyinPrompt": "qǐng děng wǒ wǔ ___!",
                "options": [
                    {"label": "分钟", "value": "分钟"},
                    {"label": "点", "value": "点"},
                    {"label": "岁", "value": "岁"},
                    {"label": "号", "value": "号"},
                ],
                "answer": "分钟",
            },
            {
                "id": "ex-t5-5", "kind": "sentence-tiles", "promptVi": "Ghép câu: 'Chiều mai mình có thời gian.'",
                "tiles": ["有时间", "明天", "我", "下午"],
                "answer": "我明天下午有时间",
                "explainVi": "Thời gian (明天下午) đứng trước động từ (有时间).",
            },
            {
                "id": "ex-t5-6", "kind": "meaning-choice", "promptVi": "Câu 「我们明天晚上七点见！」 nghĩa là gì?",
                "hanziPrompt": "我们明天晚上七点见！", "pinyinPrompt": "wǒ men míng tiān wǎn shang qī diǎn jiàn!",
                "options": [
                    {"label": "Chúng mình gặp nhau lúc 7 giờ tối mai nhé!", "value": "Chúng mình gặp nhau lúc 7 giờ tối mai nhé!"},
                    {"label": "Hôm nay 7 giờ sáng mình có lớp.", "value": "Hôm nay 7 giờ sáng mình có lớp."},
                    {"label": "Bây giờ là 7 giờ tối rồi.", "value": "Bây giờ là 7 giờ tối rồi."},
                    {"label": "Đợi mình 7 phút nhé!", "value": "Đợi mình 7 phút nhé!"},
                ],
                "answer": "Chúng mình gặp nhau lúc 7 giờ tối mai nhé!",
            },
        ],
        "roleplay": [
            {
                "npcHanzi": "请问，现在几点了？", "npcPinyin": "qǐng wèn, xiàn zài jǐ diǎn le?", "npcVi": "Xin hỏi, bây giờ mấy giờ rồi?",
                "promptVi": "Trả lời bây giờ là 3 giờ chiều:",
                "options": [
                    {"hanzi": "现在下午三点。", "pinyin": "xiàn zài xià wǔ sān diǎn.", "vi": "Bây giờ là 3 giờ chiều.", "correct": True},
                    {"hanzi": "今天五月三号。", "pinyin": "jīn tiān wǔ yuè sān hào.", "vi": "Hôm nay ngày 3 tháng 5.", "correct": False},
                    {"hanzi": "三分钟。", "pinyin": "sān fēn zhōng.", "vi": "3 phút.", "correct": False},
                ],
                "expectedHanzi": "现在下午三点。",
            },
            {
                "npcHanzi": "你明天下午有时间吗？", "npcPinyin": "nǐ míng tiān xià wǔ yǒu shí jiān ma?", "npcVi": "Chiều mai bạn có thời gian không?",
                "promptVi": "Trả lời có và hẹn 4 giờ gặp:",
                "options": [
                    {"hanzi": "有时间！我们四点见！", "pinyin": "yǒu shí jiān! wǒ men sì diǎn jiàn!", "vi": "Có chứ! Chúng mình gặp lúc 4 giờ nhé!", "correct": True},
                    {"hanzi": "没有哥哥。", "pinyin": "méi yǒu gē ge.", "vi": "Không có anh trai.", "correct": False},
                    {"hanzi": "我叫Bao。", "pinyin": "wǒ jiào Bao.", "vi": "Mình tên là Bao.", "correct": False},
                ],
                "expectedHanzi": "有时间！我们四点见！",
            },
            {
                "npcHanzi": "我已经到了，你在哪儿？", "npcPinyin": "wǒ yǐ jīng dào le, nǐ zài nǎr?", "npcVi": "Mình tới rồi, bạn ở đâu thế?",
                "promptVi": "Nhờ bạn đợi mình 5 phút:",
                "options": [
                    {"hanzi": "对不起，请等我五分钟！", "pinyin": "duì bu qǐ, qǐng děng wǒ wǔ fēn zhōng!", "vi": "Xin lỗi, đợi mình 5 phút nhé!", "correct": True},
                    {"hanzi": "祝你生日快乐！", "pinyin": "zhù nǐ shēng rì kuài lè!", "vi": "Chúc mừng sinh nhật!", "correct": False},
                    {"hanzi": "不客气！", "pinyin": "bú kè qi!", "vi": "Không có gì!", "correct": False},
                ],
                "expectedHanzi": "对不起，请等我五分钟！",
            },
        ],
        "writing": [
            {"char": "今", "pinyin": "jīn", "meaningVi": "nay, hiện tại", "radical": "人", "radicalNoteVi": "Mái che (人) giữ lấy khoảnh khắc hiện tại.", "lookalikes": [{"hanzi": "今", "pinyin": "jīn", "vi": "nay"}, {"hanzi": "令", "pinyin": "lìng", "vi": "lệnh"}, {"hanzi": "念", "pinyin": "niàn", "vi": "đọc/nhớ"}, {"hanzi": "合", "pinyin": "hé", "vi": "hợp"}]},
            {"char": "天", "pinyin": "tiān", "meaningVi": "ngày, trời", "radical": "大", "radicalNoteVi": "Trên đầu chữ 大 (lớn/người) là bầu trời (一).", "lookalikes": [{"hanzi": "天", "pinyin": "tiān", "vi": "trời/ngày"}, {"hanzi": "大", "pinyin": "dà", "vi": "to lớn"}, {"hanzi": "夫", "pinyin": "fū", "vi": "chồng"}, {"hanzi": "太", "pinyin": "tài", "vi": "quá"}]},
            {"char": "明", "pinyin": "míng", "meaningVi": "sáng, ngày mai", "radical": "日", "radicalNoteVi": "Mặt trời (日) và mặt trăng (月) cùng tỏa sáng.", "lookalikes": [{"hanzi": "明", "pinyin": "míng", "vi": "sáng/mai"}, {"hanzi": "朋", "pinyin": "péng", "vi": "bạn"}, {"hanzi": "时", "pinyin": "shí", "vi": "giờ"}, {"hanzi": "晚", "pinyin": "wǎn", "vi": "tối"}]},
        ],
    },
    {
        "topicId": 6,
        "title": "Ăn uống: gọi món, trà sữa & cà phê",
        "subtitle": "Gọi đồ uống đúng gu ít đường, nóng/đá và gọi tính tiền",
        "storyTagVi": "Ngày 4 · Quán trà sữa phố cổ",
        "connectsFromVi": "Tiếp nối Bài 5: Thời gian & hẹn gặp",
        "storyContextVi": "Đúng 4 giờ chiều như đã hẹn (Bài 5), Bao, Linh và Tiểu Minh ghé quán trà sữa nổi tiếng ở phố cổ để thưởng thức đồ uống!",
        "bridgeFromPrevVi": "Đã hẹn đúng giờ ở Bài 5 — giờ bước vào quán, tự tin gọi một ly trà sữa ít đường và một ly cà phê nóng nhé!",
        "bridgeToNextVi": "Uống trà sữa no nê rồi, sang Bài 7 Bao sẽ sang khu chợ kế bên hỏi giá và mua quà lưu niệm!",
        "recapWordIds": ["今天", "下午", "朋友"],
        "cultureTipVi": "Ở quán trà sữa Trung Quốc, nhớ 4 cụm thần thánh: 少糖 (ít đường), 无糖 (không đường), 少冰 (ít đá), 去冰 (không đá). Khi thanh toán chỉ cần hô 「买单！」(Mǎidān!).",
        "grammarSpotlight": {
            "title": "Gọi món với 「我要…」 & Lượng từ đồ uống 「杯」",
            "formula": "我要 + Số + 杯 + (热/冰) + Đồ uống",
            "explainVi": "我要 (wǒ yào = cho mình…) dùng cực phổ biến khi gọi món. Lượng từ cho ly/cốc là 杯 (bēi). 2 ly nói 两杯 (không nói 二杯!).",
            "vsVietnameseVi": "Tính từ (热 nóng / 冰 đá) đứng TRƯỚC danh từ đồ uống: 热咖啡 (cà phê nóng), ngược với tiếng Việt!",
            "commonMistakeVi": "Nói 咖啡热 thay vì 热咖啡, hoặc 二杯 thay vì 两杯.",
            "examples": [
                {"hanzi": "我要一杯热奶茶，少糖。", "pinyin": "wǒ yào yì bēi rè nǎi chá, shǎo táng.", "vi": "Cho mình một ly trà sữa nóng, ít đường."},
                {"hanzi": "请问，你们想喝什么？", "pinyin": "qǐng wèn, nǐ men xiǎng hē shén me?", "vi": "Xin hỏi các bạn muốn uống gì ạ?"},
            ],
        },
        "words": [
            {
                "hanzi": "喝", "pinyin": "hē", "meaningVi": "uống", "pos": "Động từ",
                "radical": "口", "literalVi": "Bộ khẩu (口) — dùng miệng để uống",
                "mnemonic": "Bên trái có cái miệng (口) — ăn (吃) và uống (喝) đều có bộ khẩu!",
                "usageNoteVi": "喝茶 (uống trà), 喝水 (uống nước), 喝奶茶 (uống trà sữa).",
                "examples": [
                    {"hanzi": "我想喝一杯热茶。", "pinyin": "wǒ xiǎng hē yì bēi rè chá.", "vi": "Mình muốn uống một ly trà nóng."},
                    {"hanzi": "你喜欢喝咖啡吗？", "pinyin": "nǐ xǐ huan hē kā fēi ma?", "vi": "Bạn có thích uống cà phê không?"},
                ],
            },
            {
                "hanzi": "吃", "pinyin": "chī", "meaningVi": "ăn", "pos": "Động từ",
                "radical": "口", "literalVi": "Bộ khẩu (口) + 乞 — mở miệng ăn",
                "mnemonic": "Chỉ có 6 nét rất gọn, có bộ khẩu (口) ở bên trái.",
                "usageNoteVi": "吃饭 (ăn cơm), 好吃 (hǎo chī = ngon miệng — dùng cho đồ ăn; còn đồ uống ngon là 好喝 hǎo hē!).",
                "examples": [
                    {"hanzi": "这个蛋糕很好吃！", "pinyin": "zhè gè dàn gāo hěn hǎo chī!", "vi": "Chiếc bánh ngọt này ngon quá!"},
                    {"hanzi": "我们一起去吃饭吧。", "pinyin": "wǒ men yì qǐ qù chī fàn ba.", "vi": "Chúng mình cùng đi ăn cơm nhé."},
                ],
            },
            {
                "hanzi": "奶茶", "pinyin": "nǎi chá", "meaningVi": "trà sữa", "pos": "Danh từ",
                "radical": "女", "literalVi": "奶 (sữa) + 茶 (trà)",
                "mnemonic": "奶 (sữa) + 茶 (trà — có bộ thảo 艹 là lá trà!) = món trà sữa quốc dân!",
                "usageNoteVi": "Trà sữa trân châu là 珍珠奶茶 (zhēnzhū nǎichá).",
                "examples": [
                    {"hanzi": "这家的奶茶很好喝！", "pinyin": "zhè jiā de nǎi chá hěn hǎo hē!", "vi": "Trà sữa quán này uống rất ngon!"},
                    {"hanzi": "我要一杯少糖奶茶。", "pinyin": "wǒ yào yì bēi shǎo táng nǎi chá.", "vi": "Cho mình một ly trà sữa ít đường."},
                ],
            },
            {
                "hanzi": "咖啡", "pinyin": "kā fēi", "meaningVi": "cà phê", "pos": "Danh từ",
                "radical": "口", "literalVi": "Từ phiên âm từ 'coffee', cả hai chữ đều có bộ khẩu (口)",
                "mnemonic": "Hai cái miệng (口 + 口) cùng nhâm nhi ly cà phê thơm lừng!",
                "usageNoteVi": "Cà phê đá: 冰咖啡 (bīng kāfēi). Cà phê sữa: 拿铁 (nátiě).",
                "examples": [
                    {"hanzi": "小明想要一杯冰咖啡。", "pinyin": "Xiǎo Míng xiǎng yào yì bēi bīng kā fēi.", "vi": "Tiểu Minh muốn một ly cà phê đá."},
                    {"hanzi": "早上我常常喝咖啡。", "pinyin": "zǎo shang wǒ cháng cháng hē kā fēi.", "vi": "Buổi sáng mình thường uống cà phê."},
                ],
            },
            {
                "hanzi": "杯", "pinyin": "bēi", "meaningVi": "ly, cốc (lượng từ)", "pos": "Lượng từ",
                "radical": "木", "literalVi": "Bộ mộc (木) — xưa cốc làm bằng gỗ",
                "mnemonic": "Cái cốc (杯) đựng đồ uống: 一杯茶, 两杯奶茶.",
                "usageNoteVi": "Danh từ cái cốc gọi là 杯子 (bēi zi).",
                "examples": [
                    {"hanzi": "请给我两杯热茶。", "pinyin": "qǐng gěi wǒ liǎng bēi rè chá.", "vi": "Làm ơn cho mình hai ly trà nóng."},
                    {"hanzi": "一杯奶茶多少钱？", "pinyin": "yì bēi nǎi chá duō shao qián?", "vi": "Một ly trà sữa bao nhiêu tiền?"},
                ],
            },
            {
                "hanzi": "少糖", "pinyin": "shǎo táng", "meaningVi": "ít đường", "pos": "Cụm giao tiếp",
                "radical": "小", "literalVi": "少 (ít) + 糖 (đường, bộ mễ 米)",
                "mnemonic": "少 (ít) + 糖 (đường ngọt) — câu thần chú khi gọi trà sữa!",
                "usageNoteVi": "Tương tự: 少冰 (ít đá), 去冰 (không đá), 半糖 (50% đường).",
                "examples": [
                    {"hanzi": "这杯奶茶要少糖，少冰。", "pinyin": "zhè bēi nǎi chá yào shǎo táng, shǎo bīng.", "vi": "Ly trà sữa này lấy ít đường, ít đá nhé."},
                    {"hanzi": "我喜欢喝少糖的奶茶。", "pinyin": "wǒ xǐ huan hē shǎo táng de nǎi chá.", "vi": "Mình thích uống trà sữa ít đường."},
                ],
            },
            {
                "hanzi": "热", "pinyin": "rè", "meaningVi": "nóng", "pos": "Tính từ",
                "radical": "灬", "literalVi": "4 chấm lửa (灬) ở dưới — nóng bốc khói!",
                "mnemonic": "Thấy 4 chấm lửa (灬) bên dưới là biết ngay rất nóng (热)!",
                "usageNoteVi": "Dùng cho cả đồ ăn/uống (热茶) và thời tiết (天气很热 — chuẩn bị cho Bài 10!).",
                "examples": [
                    {"hanzi": "我要一杯热咖啡。", "pinyin": "wǒ yào yì bēi rè kā fēi.", "vi": "Cho mình một ly cà phê nóng."},
                    {"hanzi": "这杯茶很热，小心一点。", "pinyin": "zhè bēi chá hěn rè, xiǎo xīn yì diǎn.", "vi": "Ly trà này nóng lắm, cẩn thận một chút nhé."},
                ],
            },
            {
                "hanzi": "买单", "pinyin": "mǎi dān", "meaningVi": "tính tiền, thanh toán", "pos": "Động từ",
                "radical": "乙", "literalVi": "买 (mua/trả) + 单 (hóa đơn)",
                "mnemonic": "Gọi nhân viên trả tiền hóa đơn (单) là 买单!",
                "usageNoteVi": "Nói lịch sự: 服务员，买单！(Nhân viên ơi, tính tiền ạ!).",
                "examples": [
                    {"hanzi": "你好，请问在哪儿买单？", "pinyin": "nǐ hǎo, qǐng wèn zài nǎr mǎi dān?", "vi": "Xin chào, cho hỏi tính tiền ở đâu ạ?"},
                    {"hanzi": "今天我来买单吧！", "pinyin": "jīn tiān wǒ lái mǎi dān ba!", "vi": "Hôm nay để mình mời tính tiền nhé!"},
                ],
            },
        ],
        "patterns": [
            {
                "id": "p-t6-1", "frame": "我要一杯___。", "pinyin": "wǒ yào yì bēi ___.", "meaningVi": "Cho mình một ly ___.",
                "exampleHanzi": "我要一杯奶茶。", "examplePinyin": "wǒ yào yì bēi nǎi chá.", "exampleVi": "Cho mình một ly trà sữa.",
                "slots": {
                    "promptVi": "Gọi một ly trà sữa:",
                    "choices": [
                        {"hanzi": "奶茶", "pinyin": "nǎi chá", "vi": "trà sữa"},
                        {"hanzi": "买单", "pinyin": "mǎi dān", "vi": "tính tiền"},
                        {"hanzi": "时间", "pinyin": "shí jiān", "vi": "thời gian"},
                    ],
                    "answerHanzi": "奶茶",
                },
            },
            {
                "id": "p-t6-2", "frame": "请给我两___热咖啡。", "pinyin": "qǐng gěi wǒ liǎng ___ rè kā fēi.", "meaningVi": "Cho mình hai ___ cà phê nóng.",
                "exampleHanzi": "请给我两杯热咖啡。", "examplePinyin": "qǐng gěi wǒ liǎng bēi rè kā fēi.", "exampleVi": "Cho mình hai ly cà phê nóng.",
                "slots": {
                    "promptVi": "Chọn lượng từ đúng cho đồ uống:",
                    "choices": [
                        {"hanzi": "杯", "pinyin": "bēi", "vi": "ly / cốc"},
                        {"hanzi": "岁", "pinyin": "suì", "vi": "tuổi"},
                        {"hanzi": "口", "pinyin": "kǒu", "vi": "miệng (người trong nhà)"},
                    ],
                    "answerHanzi": "杯",
                },
            },
            {
                "id": "p-t6-3", "frame": "这杯奶茶要___，谢谢！", "pinyin": "zhè bēi nǎi chá yào ___, xiè xie!", "meaningVi": "Ly trà sữa này lấy ___, cảm ơn!",
                "exampleHanzi": "这杯奶茶要少糖，谢谢！", "examplePinyin": "zhè bēi nǎi chá yào shǎo táng, xiè xie!", "exampleVi": "Ly trà sữa này lấy ít đường, cảm ơn!",
                "slots": {
                    "promptVi": "Yêu cầu pha ít đường:",
                    "choices": [
                        {"hanzi": "少糖", "pinyin": "shǎo táng", "vi": "ít đường"},
                        {"hanzi": "买单", "pinyin": "mǎi dān", "vi": "tính tiền"},
                        {"hanzi": "吃饭", "pinyin": "chī fàn", "vi": "ăn cơm"},
                    ],
                    "answerHanzi": "少糖",
                },
            },
        ],
        "dialogue": [
            {"speaker": "Nhân viên", "voiceRole": "female", "hanzi": "欢迎光临！请问想喝点什么？", "pinyin": "huān yíng guāng lín! qǐng wèn xiǎng hē diǎn shén me?", "vi": "Chào mừng quý khách! Xin hỏi bạn muốn uống gì ạ?", "mode": "npc"},
            {
                "speaker": "Bao", "voiceRole": "male", "hanzi": "我要一杯热奶茶，少糖。", "pinyin": "wǒ yào yì bēi rè nǎi chá, shǎo táng.", "vi": "Cho mình một ly trà sữa nóng, ít đường.",
                "mode": "choice", "goalLabel": "Gọi trà sữa đúng gu",
                "choices": [
                    {"hanzi": "我要一杯热奶茶，少糖。", "pinyin": "wǒ yào yì bēi rè nǎi chá, shǎo táng.", "vi": "Cho mình một ly trà sữa nóng, ít đường.", "correct": True},
                    {"hanzi": "我今年二十岁。", "pinyin": "wǒ jīn nián èr shí suì.", "vi": "Năm nay mình 20 tuổi.", "correct": False},
                    {"hanzi": "现在下午四点。", "pinyin": "xiàn zài xià wǔ sì diǎn.", "vi": "Bây giờ là 4 giờ chiều.", "correct": False},
                ],
            },
            {"speaker": "Nhân viên", "voiceRole": "female", "hanzi": "好的！你的朋友要喝什么？", "pinyin": "hǎo de! nǐ de péng you yào hē shén me?", "vi": "Vâng ạ! Bạn của bạn muốn uống gì?", "mode": "npc"},
            {"speaker": "Bao", "voiceRole": "male", "hanzi": "她要一杯冰咖啡。", "pinyin": "tā yào yì bēi bīng kā fēi.", "vi": "Bạn ấy lấy một ly cà phê đá.", "mode": "tiles", "goalLabel": "Gọi thêm cho Linh", "tilePrompt": ["她要", "一杯", "冰", "咖啡"]},
            {"speaker": "Nhân viên", "voiceRole": "female", "hanzi": "好的，请稍等五分钟！", "pinyin": "hǎo de, qǐng shāo děng wǔ fēn zhōng!", "vi": "Vâng, xin đợi 5 phút ạ!", "mode": "npc"},
            {"speaker": "Bao", "voiceRole": "male", "hanzi": "谢谢，现在买单！", "pinyin": "xiè xie, xiàn zài mǎi dān!", "vi": "Cảm ơn, giờ mình tính tiền nhé!", "mode": "pinyin", "goalLabel": "Gọi tính tiền", "acceptedPinyin": ["xiexie xianzai maidan", "maidan", "mǎi dān", "谢谢，现在买单", "买单"]},
        ],
        "exercises": [
            {
                "id": "ex-t6-1", "kind": "meaning-choice", "promptVi": "「少糖」 có nghĩa là gì?",
                "hanziPrompt": "少糖", "pinyinPrompt": "shǎo táng",
                "options": [
                    {"label": "Ít đường", "value": "Ít đường"},
                    {"label": "Nhiều đá", "value": "Nhiều đá"},
                    {"label": "Tính tiền", "value": "Tính tiền"},
                    {"label": "Trà nóng", "value": "Trà nóng"},
                ],
                "answer": "Ít đường",
            },
            {
                "id": "ex-t6-2", "kind": "hanzi-choice", "promptVi": "Nghe và chọn chữ Hán có nghĩa 'trà sữa'",
                "audioText": "奶茶",
                "options": [
                    {"label": "奶茶", "value": "奶茶"},
                    {"label": "咖啡", "value": "咖啡"},
                    {"label": "买单", "value": "买单"},
                    {"label": "热茶", "value": "热茶"},
                ],
                "answer": "奶茶",
            },
            {
                "id": "ex-t6-3", "kind": "match-pairs", "promptVi": "Ghép 4 cặp từ ở quán đồ uống:",
                "pairs": [
                    {"hanzi": "喝", "pinyin": "hē", "vi": "Uống"},
                    {"hanzi": "咖啡", "pinyin": "kā fēi", "vi": "Cà phê"},
                    {"hanzi": "热", "pinyin": "rè", "vi": "Nóng"},
                    {"hanzi": "买单", "pinyin": "mǎi dān", "vi": "Tính tiền"},
                ],
                "answer": "matched",
            },
            {
                "id": "ex-t6-4", "kind": "fill-blank", "promptVi": "Điền lượng từ: 「我想喝两___热奶茶。」",
                "hanziPrompt": "我想喝两___热奶茶。", "pinyinPrompt": "wǒ xiǎng hē liǎng ___ rè nǎi chá.",
                "options": [
                    {"label": "杯", "value": "杯"},
                    {"label": "点", "value": "点"},
                    {"label": "口", "value": "口"},
                    {"label": "个", "value": "个"},
                ],
                "answer": "杯",
            },
            {
                "id": "ex-t6-5", "kind": "sentence-tiles", "promptVi": "Ghép câu: 'Cho mình một ly trà sữa nóng.'",
                "tiles": ["奶茶", "一杯", "我要", "热"],
                "answer": "我要一杯热奶茶",
            },
            {
                "id": "ex-t6-6", "kind": "meaning-choice", "promptVi": "Đồ uống ngon khen 「好喝」, thế đồ ăn ngon khen gì?",
                "hanziPrompt": "很好吃", "pinyinPrompt": "hěn hǎo chī",
                "options": [
                    {"label": "Rất ngon (dùng cho đồ ăn)", "value": "Rất ngon (dùng cho đồ ăn)"},
                    {"label": "Rất nóng", "value": "Rất nóng"},
                    {"label": "Rất ít đường", "value": "Rất ít đường"},
                    {"label": "Rất đắt", "value": "Rất đắt"},
                ],
                "answer": "Rất ngon (dùng cho đồ ăn)",
            },
        ],
        "roleplay": [
            {
                "npcHanzi": "你好，请问想喝什么？", "npcPinyin": "nǐ hǎo, qǐng wèn xiǎng hē shén me?", "npcVi": "Xin chào, bạn muốn uống gì ạ?",
                "promptVi": "Gọi một ly trà sữa ít đường:",
                "options": [
                    {"hanzi": "我要一杯奶茶，少糖。", "pinyin": "wǒ yào yì bēi nǎi chá, shǎo táng.", "vi": "Cho mình một ly trà sữa, ít đường.", "correct": True},
                    {"hanzi": "对不起，没关系。", "pinyin": "duì bu qǐ, méi guān xi.", "vi": "Xin lỗi, không sao đâu.", "correct": False},
                    {"hanzi": "明天见！", "pinyin": "míng tiān jiàn!", "vi": "Hẹn gặp ngày mai!", "correct": False},
                ],
                "expectedHanzi": "我要一杯奶茶，少糖。",
            },
            {
                "npcHanzi": "要热的还是冰的？", "npcPinyin": "yào rè de hái shi bīng de?", "npcVi": "Bạn lấy nóng hay đá ạ?",
                "promptVi": "Chọn loại nóng và cảm ơn:",
                "options": [
                    {"hanzi": "要热的，谢谢！", "pinyin": "yào rè de, xiè xie!", "vi": "Lấy nóng nhé, cảm ơn!", "correct": True},
                    {"hanzi": "我叫Bao。", "pinyin": "wǒ jiào Bao.", "vi": "Mình tên là Bao.", "correct": False},
                    {"hanzi": "四口人。", "pinyin": "sì kǒu rén.", "vi": "4 người.", "correct": False},
                ],
                "expectedHanzi": "要热的，谢谢！",
            },
            {
                "npcHanzi": "请问还需要别的吗？", "npcPinyin": "qǐng wèn hái xū yào bié de ma?", "npcVi": "Xin hỏi bạn có cần thêm gì nữa không?",
                "promptVi": "Nói không cần và gọi tính tiền:",
                "options": [
                    {"hanzi": "不用了，谢谢，买单！", "pinyin": "bú yòng le, xiè xie, mǎi dān!", "vi": "Không cần nữa, cảm ơn, tính tiền nhé!", "correct": True},
                    {"hanzi": "祝你生日快乐！", "pinyin": "zhù nǐ shēng rì kuài lè!", "vi": "Chúc sinh nhật vui vẻ!", "correct": False},
                    {"hanzi": "现在两点。", "pinyin": "xiàn zài liǎng diǎn.", "vi": "Bây giờ là 2 giờ.", "correct": False},
                ],
                "expectedHanzi": "不用了，谢谢，买单！",
            },
        ],
        "writing": [
            {"char": "喝", "pinyin": "hē", "meaningVi": "uống", "radical": "口", "radicalNoteVi": "Bộ khẩu (口) ở bên trái chỉ hành động uống bằng miệng.", "lookalikes": [{"hanzi": "喝", "pinyin": "hē", "vi": "uống"}, {"hanzi": "渴", "pinyin": "kě", "vi": "khát"}, {"hanzi": "吃", "pinyin": "chī", "vi": "ăn"}, {"hanzi": "叫", "pinyin": "jiào", "vi": "gọi"}]},
            {"char": "茶", "pinyin": "chá", "meaningVi": "trà", "radical": "艹", "radicalNoteVi": "Bộ thảo (艹) chỉ cây cỏ, giữa là người (人), dưới là cây (木): người hái lá trà.", "lookalikes": [{"hanzi": "茶", "pinyin": "chá", "vi": "trà"}, {"hanzi": "草", "pinyin": "cǎo", "vi": "cỏ"}, {"hanzi": "花", "pinyin": "huā", "vi": "hoa"}, {"hanzi": "菜", "pinyin": "cài", "vi": "rau/món"}]},
            {"char": "杯", "pinyin": "bēi", "meaningVi": "ly, cốc", "radical": "木", "radicalNoteVi": "Bộ mộc (木) chỉ cái cốc xưa làm bằng gỗ.", "lookalikes": [{"hanzi": "杯", "pinyin": "bēi", "vi": "cốc"}, {"hanzi": "不", "pinyin": "bù", "vi": "không"}, {"hanzi": "林", "pinyin": "lín", "vi": "rừng"}, {"hanzi": "本", "pinyin": "běn", "vi": "quyển"}]},
        ],
    },
    {
        "topicId": 7,
        "title": "Mua sắm & mặc cả",
        "subtitle": "Hỏi giá tiền, chê đắt/khen rẻ và trả giá vui vẻ ở chợ phố cổ",
        "storyTagVi": "Ngày 5 · Chọn quà ở chợ phố cổ",
        "connectsFromVi": "Tiếp nối Bài 6: Ăn uống & tính tiền",
        "storyContextVi": "Rời quán trà sữa (Bài 6), Bao ghé khu chợ nhỏ kế bên để mua chiếc móc khóa gấu trúc làm quà sinh nhật cho Tiểu Linh!",
        "bridgeFromPrevVi": "Ở Bài 6 bạn đã gọi 「买单」(tính tiền) — giờ học cách hỏi giá 「多少钱」, chê đắt và trả giá thật khéo nhé!",
        "bridgeToNextVi": "Mua quà xong rồi! Sang Bài 8 Bao sẽ hỏi đường ra ga tàu điện ngầm để mang quà về nhà!",
        "recapWordIds": ["买单", "奶茶", "杯"],
        "cultureTipVi": "Trong văn nói, người Trung Quốc dùng 「块」(kuài = tệ) thay cho 「元」(yuán). Khi mặc cả ở chợ đêm, câu thần chú thân thiện là 「太贵了，便宜一点儿吧！」(Đắt quá, bớt chút đi ạ!).",
        "grammarSpotlight": {
            "title": "Hỏi giá 「多少钱？」 & Cảm thán 「太 + Tính từ + 了！」",
            "formula": "Danh từ + 多少钱？  |  太 + 贵/便宜 + 了！",
            "explainVi": "多少 (duō shao) dùng để hỏi số lớn (như giá tiền). Cấu trúc 太…了 (quá… rồi!) cực hữu ích để cảm thán: 太贵了 (đắt quá!), 太好了 (tuyệt quá!).",
            "vsVietnameseVi": "Tiếng Việt nói 'đắt quá' (Tính từ + Quá), tiếng Trung bọc tính từ ở giữa 太 và 了: 太贵了!",
            "commonMistakeVi": "Nói 这个多少块？ khi hỏi giá — cách chuẩn tự nhiên nhất luôn là 「这个多少钱？」!",
            "examples": [
                {"hanzi": "请问，这个多少钱？", "pinyin": "qǐng wèn, zhè gè duō shao qián?", "vi": "Xin hỏi, cái này bao nhiêu tiền ạ?"},
                {"hanzi": "三十块太贵了，便宜一点儿吧！", "pinyin": "sān shí kuài tài guì le, pián yi yì diǎnr ba!", "vi": "30 tệ đắt quá, rẻ hơn một chút đi ạ!"},
            ],
        },
        "words": [
            {
                "hanzi": "买", "pinyin": "mǎi", "meaningVi": "mua", "pos": "Động từ",
                "radical": "乙", "literalVi": "Bỏ tiền để mang về",
                "mnemonic": "买 (mua) không có dấu thập ở trên; 卖 (bán) có dấu 十 (thêm đồ mang ra bán)!",
                "usageNoteVi": "Cẩn thận phân biệt 买 (mǎi - thanh 3: mua) và 卖 (mài - thanh 4: bán)!",
                "examples": [
                    {"hanzi": "我想买一个礼物。", "pinyin": "wǒ xiǎng mǎi yí gè lǐ wù.", "vi": "Mình muốn mua một món quà."},
                    {"hanzi": "你要买什么东西？", "pinyin": "nǐ yào mǎi shén me dōng xi?", "vi": "Bạn muốn mua đồ gì thế?"},
                ],
            },
            {
                "hanzi": "东西", "pinyin": "dōng xi", "meaningVi": "đồ đạc, thứ, món đồ", "pos": "Danh từ",
                "radical": "一", "literalVi": "东 (đông) + 西 (tây) — xưa đi chợ Đông chợ Tây mua đồ!",
                "mnemonic": "Chợ Đông (东) và chợ Tây (西) bán đủ mọi món đồ — gọi chung là 东西!",
                "usageNoteVi": "Khi nghĩa là 'đồ đạc', chữ 西 đọc thanh nhẹ (dōng xi).",
                "examples": [
                    {"hanzi": "这里的东西很便宜。", "pinyin": "zhè lǐ de dōng xi hěn pián yi.", "vi": "Đồ ở đây rất rẻ."},
                    {"hanzi": "我去买点东西。", "pinyin": "wǒ qù mǎi diǎn dōng xi.", "vi": "Mình đi mua chút đồ."},
                ],
            },
            {
                "hanzi": "钱", "pinyin": "qián", "meaningVi": "tiền", "pos": "Danh từ",
                "radical": "钅", "literalVi": "Bộ kim (钅) — xưa tiền đúc bằng kim loại",
                "mnemonic": "Bên trái có bộ kim loại (钅) — đồng xu kim loại chính là tiền!",
                "usageNoteVi": "多少钱 (bao nhiêu tiền), 零钱 (tiền lẻ).",
                "examples": [
                    {"hanzi": "一杯奶茶多少钱？", "pinyin": "yì bēi nǎi chá duō shao qián?", "vi": "Một ly trà sữa bao nhiêu tiền?"},
                    {"hanzi": "这个包八十块钱。", "pinyin": "zhè gè bāo bā shí kuài qián.", "vi": "Chiếc túi này 80 tệ."},
                ],
            },
            {
                "hanzi": "块", "pinyin": "kuài", "meaningVi": "tệ, đồng (đơn vị tiền văn nói)", "pos": "Lượng từ",
                "radical": "土", "literalVi": "Miếng / đồng tiền trong giao tiếp hằng ngày",
                "mnemonic": "Đếm tiền Trung Quốc hằng ngày cứ dùng 块: 十块 (10 tệ), 二十块 (20 tệ)!",
                "usageNoteVi": "Có thể nói 二十块 hoặc 二十块钱. Trên biển giá in sẽ ghi 元 (yuán).",
                "examples": [
                    {"hanzi": "这个杯子十五块钱。", "pinyin": "zhè gè bēi zi shí wǔ kuài qián.", "vi": "Chiếc cốc này 15 tệ."},
                    {"hanzi": "二十块可以吗？", "pinyin": "èr shí kuài kě yǐ ma?", "vi": "20 tệ có được không ạ?"},
                ],
            },
            {
                "hanzi": "多少", "pinyin": "duō shao", "meaningVi": "bao nhiêu", "pos": "Đại từ",
                "radical": "夕", "literalVi": "多 (nhiều) + 少 (ít) = bao nhiêu?",
                "mnemonic": "Ghép hai từ trái nghĩa 'nhiều' (多) và 'ít' (少) thành câu hỏi 'bao nhiêu?'!",
                "usageNoteVi": "多少 dùng khi đoán số > 10 (như giá tiền), còn 几 dùng cho số nhỏ < 10.",
                "examples": [
                    {"hanzi": "请问，这个多少钱？", "pinyin": "qǐng wèn, zhè gè duō shao qián?", "vi": "Xin hỏi, cái này bao nhiêu tiền?"},
                    {"hanzi": "你们班有多少同学？", "pinyin": "nǐ men bān yǒu duō shao tóng xué?", "vi": "Lớp bạn có bao nhiêu học sinh?"},
                ],
            },
            {
                "hanzi": "便宜", "pinyin": "pián yi", "meaningVi": "rẻ", "pos": "Tính từ",
                "radical": "亻", "literalVi": "Giá cả phải chăng, dễ chịu",
                "mnemonic": "Đừng đọc biàn nhé! Khi nghĩa là 'rẻ', chữ 便 đọc là pián (pián yi)!",
                "usageNoteVi": "便宜一点儿 (rẻ hơn một chút) — câu mặc cả cực hiệu quả.",
                "examples": [
                    {"hanzi": "可以便宜一点儿吗？", "pinyin": "kě yǐ pián yi yì diǎnr ma?", "vi": "Có thể rẻ hơn một chút không ạ?"},
                    {"hanzi": "这个很便宜，我买了！", "pinyin": "zhè gè hěn pián yi, wǒ mǎi le!", "vi": "Cái này rẻ lắm, mình mua luôn!"},
                ],
            },
            {
                "hanzi": "贵", "pinyin": "guì", "meaningVi": "đắt, quý", "pos": "Tính từ",
                "radical": "贝", "literalVi": "Bộ bối (贝 - vỏ sò/tiền bạc) ở dưới",
                "mnemonic": "Món đồ tốn nhiều vỏ sò tiền bạc (贝) thì rất đắt (贵)!",
                "usageNoteVi": "Hay đi với 太…了: 太贵了！(Đắt quá!).",
                "examples": [
                    {"hanzi": "五十块太贵了！", "pinyin": "wǔ shí kuài tài guì le!", "vi": "50 tệ đắt quá!"},
                    {"hanzi": "这个不贵，很好看。", "pinyin": "zhè gè bú guì, hěn hǎo kàn.", "vi": "Cái này không đắt, rất đẹp nữa."},
                ],
            },
            {
                "hanzi": "这个", "pinyin": "zhè gè", "meaningVi": "cái này", "pos": "Đại từ",
                "radical": "辶", "literalVi": "这 (này) + 个 (cái)",
                "mnemonic": "Chỉ tay gần là 这个 (cái này), chỉ tay xa là 那个 (cái kia)!",
                "usageNoteVi": "Rất tiện khi đi chợ chưa biết tên món đồ: chỉ tay và hỏi 这个多少钱？",
                "examples": [
                    {"hanzi": "我要买这个。", "pinyin": "wǒ yào mǎi zhè gè.", "vi": "Mình muốn mua cái này."},
                    {"hanzi": "这个比那个便宜。", "pinyin": "zhè gè bǐ nà gè pián yi.", "vi": "Cái này rẻ hơn cái kia."},
                ],
            },
        ],
        "patterns": [
            {
                "id": "p-t7-1", "frame": "请问，这个多少___？", "pinyin": "qǐng wèn, zhè gè duō shao ___?", "meaningVi": "Xin hỏi, cái này bao nhiêu tiền?",
                "exampleHanzi": "请问，这个多少钱？", "examplePinyin": "qǐng wèn, zhè gè duō shao qián?", "exampleVi": "Xin hỏi, cái này bao nhiêu tiền?",
                "slots": {
                    "promptVi": "Điền từ chuẩn để hỏi giá tiền:",
                    "choices": [
                        {"hanzi": "钱", "pinyin": "qián", "vi": "tiền"},
                        {"hanzi": "块", "pinyin": "kuài", "vi": "tệ (không đi sau 多少)"},
                        {"hanzi": "岁", "pinyin": "suì", "vi": "tuổi"},
                    ],
                    "answerHanzi": "钱",
                },
            },
            {
                "id": "p-t7-2", "frame": "太___了，便宜一点儿吧！", "pinyin": "tài ___ le, pián yi yì diǎnr ba!", "meaningVi": "___ quá rồi, rẻ hơn một chút đi ạ!",
                "exampleHanzi": "太贵了，便宜一点儿吧！", "examplePinyin": "tài guì le, pián yi yì diǎnr ba!", "exampleVi": "Đắt quá rồi, rẻ hơn chút đi ạ!",
                "slots": {
                    "promptVi": "Chọn tính từ để chê đắt khi mặc cả:",
                    "choices": [
                        {"hanzi": "贵", "pinyin": "guì", "vi": "đắt"},
                        {"hanzi": "便宜", "pinyin": "pián yi", "vi": "rẻ"},
                        {"hanzi": "热", "pinyin": "rè", "vi": "nóng"},
                    ],
                    "answerHanzi": "贵",
                },
            },
            {
                "id": "p-t7-3", "frame": "这个杯子二十___。", "pinyin": "zhè gè bēi zi èr shí ___.", "meaningVi": "Chiếc cốc này 20 tệ.",
                "exampleHanzi": "这个杯子二十块。", "examplePinyin": "zhè gè bēi zi èr shí kuài.", "exampleVi": "Chiếc cốc này 20 tệ.",
                "slots": {
                    "promptVi": "Chọn đơn vị tiền tệ trong văn nói:",
                    "choices": [
                        {"hanzi": "块", "pinyin": "kuài", "vi": "tệ / đồng"},
                        {"hanzi": "杯", "pinyin": "bēi", "vi": "ly / cốc"},
                        {"hanzi": "点", "pinyin": "diǎn", "vi": "giờ"},
                    ],
                    "answerHanzi": "块",
                },
            },
        ],
        "dialogue": [
            {"speaker": "Chủ tiệm", "voiceRole": "female", "hanzi": "你好！你想买什么东西？", "pinyin": "nǐ hǎo! nǐ xiǎng mǎi shén me dōng xi?", "vi": "Xin chào! Bạn muốn mua đồ gì thế?", "mode": "npc"},
            {
                "speaker": "Bao", "voiceRole": "male", "hanzi": "请问，这个杯子多少钱？", "pinyin": "qǐng wèn, zhè gè bēi zi duō shao qián?", "vi": "Xin hỏi, chiếc cốc này bao nhiêu tiền ạ?",
                "mode": "choice", "goalLabel": "Hỏi giá món đồ",
                "choices": [
                    {"hanzi": "请问，这个杯子多少钱？", "pinyin": "qǐng wèn, zhè gè bēi zi duō shao qián?", "vi": "Xin hỏi, chiếc cốc này bao nhiêu tiền ạ?", "correct": True},
                    {"hanzi": "请问，现在几点？", "pinyin": "qǐng wèn, xiàn zài jǐ diǎn?", "vi": "Xin hỏi bây giờ mấy giờ?", "correct": False},
                    {"hanzi": "我要一杯奶茶。", "pinyin": "wǒ yào yì bēi nǎi chá.", "vi": "Cho mình một ly trà sữa.", "correct": False},
                ],
            },
            {"speaker": "Chủ tiệm", "voiceRole": "female", "hanzi": "这个杯子四十块钱。", "pinyin": "zhè gè bēi zi sì shí kuài qián.", "vi": "Chiếc cốc này 40 tệ.", "mode": "npc"},
            {"speaker": "Bao", "voiceRole": "male", "hanzi": "太贵了，便宜一点儿吧！", "pinyin": "tài guì le, pián yi yì diǎnr ba!", "vi": "Đắt quá rồi, rẻ hơn một chút đi ạ!", "mode": "tiles", "goalLabel": "Mặc cả nhẹ nhàng", "tilePrompt": ["太贵了", "便宜", "一点儿", "吧"]},
            {"speaker": "Chủ tiệm", "voiceRole": "female", "hanzi": "好吧，给你三十块！", "pinyin": "hǎo ba, gěi nǐ sān shí kuài!", "vi": "Được thôi, để bạn 30 tệ nhé!", "mode": "npc"},
            {"speaker": "Bao", "voiceRole": "male", "hanzi": "好的，我买这个！谢谢！", "pinyin": "hǎo de, wǒ mǎi zhè gè! xiè xie!", "vi": "Vâng, mình mua cái này! Cảm ơn ạ!", "mode": "pinyin", "goalLabel": "Chốt mua hàng", "acceptedPinyin": ["haode womai zhege xiexie", "womaizhege", "wǒ mǎi zhè gè", "我买这个", "好的，我买这个！谢谢！"]},
        ],
        "exercises": [
            {
                "id": "ex-t7-1", "kind": "meaning-choice", "promptVi": "「太贵了」 có nghĩa là gì?",
                "hanziPrompt": "太贵了", "pinyinPrompt": "tài guì le",
                "options": [
                    {"label": "Đắt quá rồi!", "value": "Đắt quá rồi!"},
                    {"label": "Rẻ quá rồi!", "value": "Rẻ quá rồi!"},
                    {"label": "Nóng quá rồi!", "value": "Nóng quá rồi!"},
                    {"label": "Nhiều đồ quá!", "value": "Nhiều đồ quá!"},
                ],
                "answer": "Đắt quá rồi!",
            },
            {
                "id": "ex-t7-2", "kind": "hanzi-choice", "promptVi": "Nghe và chọn chữ Hán có nghĩa 'rẻ'",
                "audioText": "便宜",
                "options": [
                    {"label": "便宜", "value": "便宜"},
                    {"label": "东西", "value": "东西"},
                    {"label": "多少", "value": "多少"},
                    {"label": "买单", "value": "买单"},
                ],
                "answer": "便宜",
            },
            {
                "id": "ex-t7-3", "kind": "match-pairs", "promptVi": "Ghép 4 cặp từ mua sắm:",
                "pairs": [
                    {"hanzi": "买", "pinyin": "mǎi", "vi": "Mua"},
                    {"hanzi": "东西", "pinyin": "dōng xi", "vi": "Đồ đạc"},
                    {"hanzi": "钱", "pinyin": "qián", "vi": "Tiền"},
                    {"hanzi": "贵", "pinyin": "guì", "vi": "Đắt"},
                ],
                "answer": "matched",
            },
            {
                "id": "ex-t7-4", "kind": "fill-blank", "promptVi": "Hỏi giá chuẩn nhất: 「这个___钱？」",
                "hanziPrompt": "这个___钱？", "pinyinPrompt": "zhè gè ___ qián?",
                "options": [
                    {"label": "多少", "value": "多少"},
                    {"label": "怎么", "value": "怎么"},
                    {"label": "什么", "value": "什么"},
                    {"label": "便宜", "value": "便宜"},
                ],
                "answer": "多少",
            },
            {
                "id": "ex-t7-5", "kind": "sentence-tiles", "promptVi": "Ghép câu: 'Cái này bao nhiêu tiền?'",
                "tiles": ["钱", "这个", "多少"],
                "answer": "这个多少钱",
            },
            {
                "id": "ex-t7-6", "kind": "meaning-choice", "promptVi": "Câu 「这里的东西不贵，很便宜。」 nghĩa là gì?",
                "hanziPrompt": "这里的东西不贵，很便宜。", "pinyinPrompt": "zhè lǐ de dōng xi bú guì, hěn pián yi.",
                "options": [
                    {"label": "Đồ ở đây không đắt, rất rẻ.", "value": "Đồ ở đây không đắt, rất rẻ."},
                    {"label": "Đồ ở đây rất đắt, không rẻ chút nào.", "value": "Đồ ở đây rất đắt, không rẻ chút nào."},
                    {"label": "Ở đây không bán đồ ăn.", "value": "Ở đây không bán đồ ăn."},
                    {"label": "Mình muốn mua hai chiếc cốc.", "value": "Mình muốn mua hai chiếc cốc."},
                ],
                "answer": "Đồ ở đây không đắt, rất rẻ.",
            },
        ],
        "roleplay": [
            {
                "npcHanzi": "你好，请问想看点什么？", "npcPinyin": "nǐ hǎo, qǐng wèn xiǎng kàn diǎn shén me?", "npcVi": "Xin chào, bạn muốn xem gì ạ?",
                "promptVi": "Chỉ chiếc cốc xinh và hỏi giá tiền:",
                "options": [
                    {"hanzi": "请问，这个多少钱？", "pinyin": "qǐng wèn, zhè gè duō shao qián?", "vi": "Xin hỏi, cái này bao nhiêu tiền ạ?", "correct": True},
                    {"hanzi": "请问，你叫什么名字？", "pinyin": "qǐng wèn, nǐ jiào shén me míng zi?", "vi": "Xin hỏi bạn tên gì?", "correct": False},
                    {"hanzi": "我要两杯茶。", "pinyin": "wǒ yào liǎng bēi chá.", "vi": "Cho mình hai ly trà.", "correct": False},
                ],
                "expectedHanzi": "请问，这个多少钱？",
            },
            {
                "npcHanzi": "这个五十块钱。", "npcPinyin": "zhè gè wǔ shí kuài qián.", "npcVi": "Cái này 50 tệ.",
                "promptVi": "Chê đắt và xin bớt chút:",
                "options": [
                    {"hanzi": "太贵了，便宜一点儿吧！", "pinyin": "tài guì le, pián yi yì diǎnr ba!", "vi": "Đắt quá rồi, rẻ hơn một chút đi ạ!", "correct": True},
                    {"hanzi": "没关系！", "pinyin": "méi guān xi!", "vi": "Không sao đâu!", "correct": False},
                    {"hanzi": "不客气！", "pinyin": "bú kè qi!", "vi": "Không có gì!", "correct": False},
                ],
                "expectedHanzi": "太贵了，便宜一点儿吧！",
            },
            {
                "npcHanzi": "好，三十五块给你！", "npcPinyin": "hǎo, sān shí wǔ kuài gěi nǐ!", "npcVi": "Được rồi, để bạn 35 tệ nhé!",
                "promptVi": "Đồng ý mua và cảm ơn:",
                "options": [
                    {"hanzi": "好的，我买这个，谢谢！", "pinyin": "hǎo de, wǒ mǎi zhè gè, xiè xie!", "vi": "Vâng, mình mua cái này, cảm ơn!", "correct": True},
                    {"hanzi": "对不起，我来晚了。", "pinyin": "duì bu qǐ, wǒ lái wǎn le.", "vi": "Xin lỗi mình đến muộn.", "correct": False},
                    {"hanzi": "我是越南人。", "pinyin": "wǒ shì Yuè nán rén.", "vi": "Mình là người Việt Nam.", "correct": False},
                ],
                "expectedHanzi": "好的，我买这个，谢谢！",
            },
        ],
        "writing": [
            {"char": "买", "pinyin": "mǎi", "meaningVi": "mua", "radical": "乙", "radicalNoteVi": "Nét gập trên cùng và chữ 头 — đi mua đồ về.", "lookalikes": [{"hanzi": "买", "pinyin": "mǎi", "vi": "mua"}, {"hanzi": "卖", "pinyin": "mài", "vi": "bán"}, {"hanzi": "头", "pinyin": "tóu", "vi": "đầu"}, {"hanzi": "实", "pinyin": "shí", "vi": "thật"}]},
            {"char": "东", "pinyin": "dōng", "meaningVi": "đông (trong 东西)", "radical": "一", "radicalNoteVi": "Mặt trời mọc sau hàng cây ở hướng Đông.", "lookalikes": [{"hanzi": "东", "pinyin": "dōng", "vi": "đông"}, {"hanzi": "车", "pinyin": "chē", "vi": "xe"}, {"hanzi": "乐", "pinyin": "lè", "vi": "vui"}, {"hanzi": "练", "pinyin": "liàn", "vi": "luyện"}]},
            {"char": "西", "pinyin": "xī", "meaningVi": "tây (trong 东西)", "radical": "西", "radicalNoteVi": "Hình tổ chim lúc mặt trời lặn về hướng Tây.", "lookalikes": [{"hanzi": "西", "pinyin": "xī", "vi": "tây"}, {"hanzi": "四", "pinyin": "sì", "vi": "bốn"}, {"hanzi": "要", "pinyin": "yào", "vi": "muốn"}, {"hanzi": "面", "pinyin": "miàn", "vi": "mặt"}]},
        ],
    },
    {
        "topicId": 8,
        "title": "Hỏi đường & đi lại",
        "subtitle": "Hỏi đường ra ga tàu điện ngầm, rẽ trái/phải và đi lại tự tin",
        "storyTagVi": "Ngày 5 · Tìm đường ra ga tàu điện ngầm",
        "connectsFromVi": "Tiếp nối Bài 7: Mua sắm ở chợ phố cổ",
        "storyContextVi": "Tay xách quà vừa mua ở chợ (Bài 7), trời đã tối nên Bao hỏi người qua đường lối ra ga tàu điện ngầm gần nhất để về nhà!",
        "bridgeFromPrevVi": "Xong màn mua sắm cực vui ở Bài 7 — bài cuối Chặng 1 này sẽ giúp bạn tự tin hỏi đường và đi tàu điện ngầm ở Trung Quốc!",
        "bridgeToNextVi": "Chúc mừng sắp xong Chặng 1! Hãy đọc Chương 1 truyện dài kỳ và làm Kiểm tra Chặng 1 để bước vào Chặng 2 — Đời sống nhé!",
        "recapWordIds": ["买", "东西", "谢谢"],
        "cultureTipVi": "Khi hỏi đường ở Trung Quốc, mở lời bằng 「请问，去___怎么走？」(Xin hỏi, đi đến ___ đi như thế nào?) luôn nhận được chỉ dẫn nhiệt tình. Hướng trái là 左 (zuǒ), phải là 右 (yòu)!",
        "grammarSpotlight": {
            "title": "Hỏi đường 「去 + Địa điểm + 怎么走？」 & Chỉ hướng",
            "formula": "请问，去 + [Địa điểm] + 怎么走？  |  往左/右走 (đi về bên trái/phải)",
            "explainVi": "怎么 (zěn me = thế nào) đặt trước động từ 走 (đi) tạo thành 'đi thế nào?'. Vị trí dùng 在: 地铁站在右边 (Ga tàu điện ngầm ở bên phải).",
            "vsVietnameseVi": "Đặt địa điểm ngay sau 去 rồi mới tới 怎么走 (VD: 去地铁站怎么走？).",
            "commonMistakeVi": "Nói 去车站走 (thiếu 怎么) hoặc quên 怎么 trước 走!",
            "examples": [
                {"hanzi": "请问，去地铁站怎么走？", "pinyin": "qǐng wèn, qù dì tiě zhàn zěn me zǒu?", "vi": "Xin hỏi, đi ra ga tàu điện ngầm đi đường nào ạ?"},
                {"hanzi": "往前走，车站就在左边。", "pinyin": "wǎng qián zǒu, chē zhàn jiù zài zuǒ bian.", "vi": "Đi thẳng về trước, nhà ga ở ngay bên trái."},
            ],
        },
        "words": [
            {
                "hanzi": "去", "pinyin": "qù", "meaningVi": "đi (đến nơi nào đó)", "pos": "Động từ",
                "radical": "厶", "literalVi": "Rời khỏi điểm đang đứng để đi tới nơi khác",
                "mnemonic": "Phân biệt: 去 (đi ra xa khỏi người nói) ↔ 来 (lái = đi lại gần người nói).",
                "usageNoteVi": "去 + Địa điểm: 去学校 (đi học), 去车站 (ra nhà ga).",
                "examples": [
                    {"hanzi": "我想去地铁站。", "pinyin": "wǒ xiǎng qù dì tiě zhàn.", "vi": "Mình muốn đi ra ga tàu điện ngầm."},
                    {"hanzi": "明天我们去公园吧！", "pinyin": "míng tiān wǒ men qù gōng yuán ba!", "vi": "Ngày mai chúng mình đi công viên nhé!"},
                ],
            },
            {
                "hanzi": "怎么", "pinyin": "zěn me", "meaningVi": "như thế nào, sao vậy", "pos": "Đại từ",
                "radical": "心", "literalVi": "Từ hỏi cách thức thực hiện hành động",
                "mnemonic": "Có bộ tâm (心) suy nghĩ cách làm: 怎么走 (đi thế nào), 怎么说 (nói thế nào).",
                "usageNoteVi": "Luôn đứng TRƯỚC động từ: 怎么走, 怎么写 (viết thế nào).",
                "examples": [
                    {"hanzi": "请问，去车站怎么走？", "pinyin": "qǐng wèn, qù chē zhàn zěn me zǒu?", "vi": "Xin hỏi, đi đến bến xe đi thế nào ạ?"},
                    {"hanzi": "这个字怎么读？", "pinyin": "zhè gè zì zěn me dú?", "vi": "Chữ này đọc thế nào?"},
                ],
            },
            {
                "hanzi": "走", "pinyin": "zǒu", "meaningVi": "đi bộ, bước đi", "pos": "Động từ",
                "radical": "走", "literalVi": "Hình người đang sải bước trên mặt đất (土)",
                "mnemonic": "Bộ tẩu (走) chính là biểu tượng của bước chân đi bộ!",
                "usageNoteVi": "走路 (đi bộ), 往前走 (đi thẳng), 往左走 (rẽ sang trái).",
                "examples": [
                    {"hanzi": "一直往前走五分钟。", "pinyin": "yì zhí wǎng qián zǒu wǔ fēn zhōng.", "vi": "Đi thẳng về phía trước 5 phút."},
                    {"hanzi": "我们走路去吧，很近！", "pinyin": "wǒ men zǒu lù qù ba, hěn jìn!", "vi": "Chúng mình đi bộ tới nhé, gần lắm!"},
                ],
            },
            {
                "hanzi": "车站", "pinyin": "chē zhàn", "meaningVi": "bến xe, nhà ga", "pos": "Danh từ",
                "radical": "车", "literalVi": "车 (xe) + 站 (trạm dừng)",
                "mnemonic": "Nơi các chiếc xe (车) đứng dừng (站) đón khách chính là bến xe/nhà ga!",
                "usageNoteVi": "火车站 (ga tàu hỏa), 公交车站 (trạm xe buýt).",
                "examples": [
                    {"hanzi": "车站离这里不远。", "pinyin": "chē zhàn lí zhè lǐ bù yuǎn.", "vi": "Nhà ga cách đây không xa."},
                    {"hanzi": "请问，车站在哪里？", "pinyin": "qǐng wèn, chē zhàn zài nǎ lǐ?", "vi": "Xin hỏi, bến xe ở đâu ạ?"},
                ],
            },
            {
                "hanzi": "地铁", "pinyin": "dì tiě", "meaningVi": "tàu điện ngầm", "pos": "Danh từ",
                "radical": "土", "literalVi": "地 (lòng đất) + 铁 (đường sắt)",
                "mnemonic": "Đường sắt (铁) chạy dưới lòng đất (地) = tàu điện ngầm!",
                "usageNoteVi": "坐地铁 (zuò dìtiě = đi tàu điện ngầm), 地铁站 (ga tàu điện ngầm).",
                "examples": [
                    {"hanzi": "我每天坐地铁去学校。", "pinyin": "wǒ měi tiān zuò dì tiě qù xué xiào.", "vi": "Mỗi ngày mình đi tàu điện ngầm tới trường."},
                    {"hanzi": "地铁站就在前面！", "pinyin": "dì tiě zhàn jiù zài qián miàn!", "vi": "Ga tàu điện ngầm ở ngay phía trước!"},
                ],
            },
            {
                "hanzi": "左边", "pinyin": "zuǒ bian", "meaningVi": "bên trái", "pos": "Danh từ",
                "radical": "工", "literalVi": "左 (trái — có chữ 工) + 边 (bên/phía)",
                "mnemonic": "Mẹo nhớ không bao giờ nhầm: 左 (trái) có chữ 工 (công), 右 (phải) có chữ 口 (miệng — tay phải cầm đũa đưa vào miệng!).",
                "usageNoteVi": "Chữ 边 đọc thanh nhẹ (zuǒ bian).",
                "examples": [
                    {"hanzi": "地铁站在左边。", "pinyin": "dì tiě zhàn zài zuǒ bian.", "vi": "Ga tàu điện ngầm ở bên trái."},
                    {"hanzi": "往左边走两分钟就到了。", "pinyin": "wǎng zuǒ bian zǒu liǎng fēn zhōng jiù dào le.", "vi": "Đi về bên trái 2 phút là tới rồi."},
                ],
            },
            {
                "hanzi": "右边", "pinyin": "yòu bian", "meaningVi": "bên phải", "pos": "Danh từ",
                "radical": "口", "literalVi": "右 (phải — có bộ khẩu 口) + 边 (bên/phía)",
                "mnemonic": "Tay phải (右) cầm đũa đưa thức ăn vào miệng (口)!",
                "usageNoteVi": "Ở bên phải: 在右边.",
                "examples": [
                    {"hanzi": "奶茶店在右边。", "pinyin": "nǎi chá diàn zài yòu bian.", "vi": "Quán trà sữa ở bên phải."},
                    {"hanzi": "我的右边是小玲。", "pinyin": "wǒ de yòu bian shì Xiǎo Líng.", "vi": "Bên phải mình là Tiểu Linh."},
                ],
            },
            {
                "hanzi": "远", "pinyin": "yuǎn", "meaningVi": "xa", "pos": "Tính từ",
                "radical": "辶", "literalVi": "Bộ xước (辶) — con đường bước đi dài xa",
                "mnemonic": "Thấy bộ xước (辶) là liên quan đến đường sá di chuyển! Trái nghĩa là 近 (jìn = gần).",
                "usageNoteVi": "不远 (không xa), 离这里很远 (cách đây rất xa).",
                "examples": [
                    {"hanzi": "地铁站离这里远吗？", "pinyin": "dì tiě zhàn lí zhè lǐ yuǎn ma?", "vi": "Ga tàu điện ngầm cách đây có xa không?"},
                    {"hanzi": "不远，走五分钟就到。", "pinyin": "bù yuǎn, zǒu wǔ fēn zhōng jiù dào.", "vi": "Không xa đâu, đi bộ 5 phút là tới."},
                ],
            },
        ],
        "patterns": [
            {
                "id": "p-t8-1", "frame": "请问，去___怎么走？", "pinyin": "qǐng wèn, qù ___ zěn me zǒu?", "meaningVi": "Xin hỏi, đi đến ___ đi thế nào ạ?",
                "exampleHanzi": "请问，去地铁站怎么走？", "examplePinyin": "qǐng wèn, qù dì tiě zhàn zěn me zǒu?", "exampleVi": "Xin hỏi, đi ra ga tàu điện ngầm đi đường nào ạ?",
                "slots": {
                    "promptVi": "Điền địa điểm để hỏi đường ra nhà ga:",
                    "choices": [
                        {"hanzi": "车站", "pinyin": "chē zhàn", "vi": "nhà ga / bến xe"},
                        {"hanzi": "怎么", "pinyin": "zěn me", "vi": "thế nào"},
                        {"hanzi": "便宜", "pinyin": "pián yi", "vi": "rẻ"},
                    ],
                    "answerHanzi": "车站",
                },
            },
            {
                "id": "p-t8-2", "frame": "地铁站在___。", "pinyin": "dì tiě zhàn zài ___.", "meaningVi": "Ga tàu điện ngầm ở ___.",
                "exampleHanzi": "地铁站在右边。", "examplePinyin": "dì tiě zhàn zài yòu bian.", "exampleVi": "Ga tàu điện ngầm ở bên phải.",
                "slots": {
                    "promptVi": "Chỉ rằng ga tàu ở bên trái:",
                    "choices": [
                        {"hanzi": "左边", "pinyin": "zuǒ bian", "vi": "bên trái"},
                        {"hanzi": "右边", "pinyin": "yòu bian", "vi": "bên phải"},
                        {"hanzi": "走", "pinyin": "zǒu", "vi": "đi bộ"},
                    ],
                    "answerHanzi": "左边",
                },
            },
            {
                "id": "p-t8-3", "frame": "车站离这里___吗？", "pinyin": "chē zhàn lí zhè lǐ ___ ma?", "meaningVi": "Nhà ga cách đây có ___ không?",
                "exampleHanzi": "车站离这里远吗？", "examplePinyin": "chē zhàn lí zhè lǐ yuǎn ma?", "exampleVi": "Nhà ga cách đây có xa không?",
                "slots": {
                    "promptVi": "Hỏi xem nhà ga cách đây có xa không:",
                    "choices": [
                        {"hanzi": "远", "pinyin": "yuǎn", "vi": "xa"},
                        {"hanzi": "贵", "pinyin": "guì", "vi": "đắt"},
                        {"hanzi": "岁", "pinyin": "suì", "vi": "tuổi"},
                    ],
                    "answerHanzi": "远",
                },
            },
        ],
        "dialogue": [
            {"speaker": "Bao", "voiceRole": "male", "hanzi": "你好！请问，去地铁站怎么走？", "pinyin": "nǐ hǎo! qǐng wèn, qù dì tiě zhàn zěn me zǒu?", "vi": "Xin chào! Xin hỏi, đi ra ga tàu điện ngầm đi đường nào ạ?", "mode": "npc"},
            {"speaker": "Bác bán hàng", "voiceRole": "formal", "hanzi": "一直往前走，然后在左边。", "pinyin": "yì zhí wǎng qián zǒu, rán hòu zài zuǒ bian.", "vi": "Đi thẳng về phía trước, rồi ở bên trái nhé.", "mode": "npc"},
            {
                "speaker": "Bao", "voiceRole": "male", "hanzi": "离这里远吗？", "pinyin": "lí zhè lǐ yuǎn ma?", "vi": "Cách đây có xa không ạ?",
                "mode": "choice", "goalLabel": "Hỏi khoảng cách",
                "choices": [
                    {"hanzi": "离这里远吗？", "pinyin": "lí zhè lǐ yuǎn ma?", "vi": "Cách đây có xa không ạ?", "correct": True},
                    {"hanzi": "这个多少钱？", "pinyin": "zhè gè duō shao qián?", "vi": "Cái này bao nhiêu tiền?", "correct": False},
                    {"hanzi": "你叫什么名字？", "pinyin": "nǐ jiào shén me míng zi?", "vi": "Bạn tên gì?", "correct": False},
                ],
            },
            {"speaker": "Bác bán hàng", "voiceRole": "formal", "hanzi": "不远！走路五分钟就到了。", "pinyin": "bù yuǎn! zǒu lù wǔ fēn zhōng jiù dào le.", "vi": "Không xa đâu! Đi bộ 5 phút là tới rồi.", "mode": "npc"},
            {"speaker": "Bao", "voiceRole": "male", "hanzi": "太好了，谢谢您！", "pinyin": "tài hǎo le, xiè xie nín!", "vi": "Tuyệt quá, cháu cảm ơn bác ạ!", "mode": "tiles", "goalLabel": "Cảm ơn người chỉ đường", "tilePrompt": ["太好了", "谢谢", "您"]},
            {"speaker": "Bác bán hàng", "voiceRole": "formal", "hanzi": "不客气，慢走！", "pinyin": "bú kè qi, màn zǒu!", "vi": "Không có gì, đi cẩn thận nhé!", "mode": "npc"},
        ],
        "exercises": [
            {
                "id": "ex-t8-1", "kind": "meaning-choice", "promptVi": "「地铁站」 có nghĩa là gì?",
                "hanziPrompt": "地铁站", "pinyinPrompt": "dì tiě zhàn",
                "options": [
                    {"label": "Ga tàu điện ngầm", "value": "Ga tàu điện ngầm"},
                    {"label": "Quán trà sữa", "value": "Quán trà sữa"},
                    {"label": "Phòng học", "value": "Phòng học"},
                    {"label": "Cửa hàng quà tặng", "value": "Cửa hàng quà tặng"},
                ],
                "answer": "Ga tàu điện ngầm",
            },
            {
                "id": "ex-t8-2", "kind": "hanzi-choice", "promptVi": "Nghe và chọn chữ Hán có nghĩa 'bên phải'",
                "audioText": "右边",
                "options": [
                    {"label": "右边", "value": "右边"},
                    {"label": "左边", "value": "左边"},
                    {"label": "车站", "value": "车站"},
                    {"label": "地铁", "value": "地铁"},
                ],
                "answer": "右边",
            },
            {
                "id": "ex-t8-3", "kind": "match-pairs", "promptVi": "Ghép 4 cặp từ hỏi đường:",
                "pairs": [
                    {"hanzi": "去", "pinyin": "qù", "vi": "Đi"},
                    {"hanzi": "走", "pinyin": "zǒu", "vi": "Đi bộ"},
                    {"hanzi": "左边", "pinyin": "zuǒ bian", "vi": "Bên trái"},
                    {"hanzi": "远", "pinyin": "yuǎn", "vi": "Xa"},
                ],
                "answer": "matched",
            },
            {
                "id": "ex-t8-4", "kind": "fill-blank", "promptVi": "Hỏi đường chuẩn: 「请问，去车站___走？」",
                "hanziPrompt": "请问，去车站___走？", "pinyinPrompt": "qǐng wèn, qù chē zhàn ___ zǒu?",
                "options": [
                    {"label": "怎么", "value": "怎么"},
                    {"label": "多少", "value": "多少"},
                    {"label": "什么", "value": "什么"},
                    {"label": "几", "value": "几"},
                ],
                "answer": "怎么",
            },
            {
                "id": "ex-t8-5", "kind": "sentence-tiles", "promptVi": "Ghép câu: 'Đi đến nhà ga đi thế nào?'",
                "tiles": ["怎么走", "车站", "去"],
                "answer": "去车站怎么走",
                "explainVi": "Mẫu hỏi đường chuẩn: 去 + [Địa điểm] + 怎么走？",
            },
            {
                "id": "ex-t8-6", "kind": "meaning-choice", "promptVi": "Câu 「不远，走路五分钟就到了。」 nghĩa là gì?",
                "hanziPrompt": "不远，走路五分钟就到了。", "pinyinPrompt": "bù yuǎn, zǒu lù wǔ fēn zhōng jiù dào le.",
                "options": [
                    {"label": "Không xa đâu, đi bộ 5 phút là tới rồi.", "value": "Không xa đâu, đi bộ 5 phút là tới rồi."},
                    {"label": "Xa lắm, phải đi 5 tiếng mới tới.", "value": "Xa lắm, phải đi 5 tiếng mới tới."},
                    {"label": "Ga tàu nằm ở bên phải.", "value": "Ga tàu nằm ở bên phải."},
                    {"label": "Vé tàu điện ngầm giá 5 tệ.", "value": "Vé tàu điện ngầm giá 5 tệ."},
                ],
                "answer": "Không xa đâu, đi bộ 5 phút là tới rồi.",
            },
        ],
        "roleplay": [
            {
                "npcHanzi": "你好，请问需要帮忙吗？", "npcPinyin": "nǐ hǎo, qǐng wèn xū yào bāng máng ma?", "npcVi": "Xin chào, bạn có cần giúp gì không?",
                "promptVi": "Hỏi đường ra ga tàu điện ngầm:",
                "options": [
                    {"hanzi": "请问，去地铁站怎么走？", "pinyin": "qǐng wèn, qù dì tiě zhàn zěn me zǒu?", "vi": "Xin hỏi, đi ra ga tàu điện ngầm đi đường nào ạ?", "correct": True},
                    {"hanzi": "地铁站多少钱？", "pinyin": "dì tiě zhàn duō shao qián?", "vi": "Ga tàu điện ngầm bao nhiêu tiền?", "correct": False},
                    {"hanzi": "我要一杯地铁。", "pinyin": "wǒ yào yì bēi dì tiě.", "vi": "Cho mình một ly tàu điện ngầm.", "correct": False},
                ],
                "expectedHanzi": "请问，去地铁站怎么走？",
            },
            {
                "npcHanzi": "往前走，地铁站就在右边！", "npcPinyin": "wǎng qián zǒu, dì tiě zhàn jiù zài yòu bian!", "npcVi": "Đi thẳng về trước, ga tàu ở ngay bên phải!",
                "promptVi": "Hỏi xem cách đây có xa không:",
                "options": [
                    {"hanzi": "离这里远吗？", "pinyin": "lí zhè lǐ yuǎn ma?", "vi": "Cách đây có xa không ạ?", "correct": True},
                    {"hanzi": "现在几点？", "pinyin": "xiàn zài jǐ diǎn?", "vi": "Bây giờ mấy giờ?", "correct": False},
                    {"hanzi": "你几岁？", "pinyin": "nǐ jǐ suì?", "vi": "Bạn mấy tuổi?", "correct": False},
                ],
                "expectedHanzi": "离这里远吗？",
            },
            {
                "npcHanzi": "不远，走三分钟就到！", "npcPinyin": "bù yuǎn, zǒu sān fēn zhōng jiù dào!", "npcVi": "Không xa đâu, đi bộ 3 phút là tới!",
                "promptVi": "Cảm ơn và chào tạm biệt:",
                "options": [
                    {"hanzi": "太好了，谢谢您，再见！", "pinyin": "tài hǎo le, xiè xie nín, zài jiàn!", "vi": "Tuyệt quá, cảm ơn bác, tạm biệt ạ!", "correct": True},
                    {"hanzi": "太贵了！", "pinyin": "tài guì le!", "vi": "Đắt quá!", "correct": False},
                    {"hanzi": "对不起！", "pinyin": "duì bu qǐ!", "vi": "Xin lỗi!", "correct": False},
                ],
                "expectedHanzi": "太好了，谢谢您，再见！",
            },
        ],
        "writing": [
            {"char": "去", "pinyin": "qù", "meaningVi": "đi", "radical": "厶", "radicalNoteVi": "Đứng trên mặt đất (土) bước ra đi (厶).", "lookalikes": [{"hanzi": "去", "pinyin": "qù", "vi": "đi"}, {"hanzi": "土", "pinyin": "tǔ", "vi": "đất"}, {"hanzi": "云", "pinyin": "yún", "vi": "mây"}, {"hanzi": "法", "pinyin": "fǎ", "vi": "cách"}]},
            {"char": "路", "pinyin": "lù", "meaningVi": "con đường", "radical": "足", "radicalNoteVi": "Bộ túc (足) chỉ bàn chân bước trên con đường.", "lookalikes": [{"hanzi": "路", "pinyin": "lù", "vi": "đường"}, {"hanzi": "足", "pinyin": "zú", "vi": "chân"}, {"hanzi": "跑", "pinyin": "pǎo", "vi": "chạy"}, {"hanzi": "各", "pinyin": "gè", "vi": "mỗi"}]},
            {"char": "车", "pinyin": "chē", "meaningVi": "xe cộ", "radical": "车", "radicalNoteVi": "Hình chiếc xe nhìn từ trên xuống có trục và hai bánh.", "lookalikes": [{"hanzi": "车", "pinyin": "chē", "vi": "xe"}, {"hanzi": "东", "pinyin": "dōng", "vi": "đông"}, {"hanzi": "连", "pinyin": "lián", "vi": "nối"}, {"hanzi": "军", "pinyin": "jūn", "vi": "quân"}]},
        ],
    },
]
