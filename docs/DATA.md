# Nguồn dữ liệu & Giấy phép (`docs/DATA.md`)

Tất cả dữ liệu mở được tải bởi [`tools/fetch_data.py`](../tools/fetch_data.py) và lưu cục bộ trong `data-src/` (không commit file nặng lên Git). Giao diện người học chỉ đọc JSON đã xử lý trong `content/` và tài nguyên tĩnh trong `public/`.

## 1. Bốn bộ dữ liệu mở (đã tải & kiểm chứng số lượng thật)

| Bộ dữ liệu | URL nguồn | Giấy phép | Số lượng đo thật | Vai trò trong BaoBao |
|---|---|---|---|---|
| Từ vựng HSK (`complete.json`) | `https://raw.githubusercontent.com/drkameleon/complete-hsk-vocabulary/main/complete.json` | MIT | **11.470** mục | Xương sống cấp độ + thứ tự từ vựng (nội bộ, không hiển thị nhãn HSK trong UI) |
| CC-CEDICT (`cedict_ts.u8`) | `https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.txt.gz` | CC BY-SA 4.0 | **125.474** mục | Tra pinyin/nghĩa Anh bổ sung, tách từ kiểm cấp độ và đối chiếu 5% bản dịch |
| Tatoeba (`cmn` + `vie` + `eng` + `links`) | `https://downloads.tatoeba.org/exports/` (`cmn_sentences.tsv.bz2`, `vie_sentences.tsv.bz2`, `eng_sentences.tsv.bz2`, `links.tar.bz2`) | CC BY 2.0 FR | **89.325** câu `cmn`, **33.328** câu `vie`, **2.041.577** câu `eng`; **667** cặp liên kết trực tiếp `cmn–vie`, **66.225** cặp `cmn–eng` | Câu ví dụ thật (ưu tiên câu có bản dịch Việt sẵn; KHÔNG dùng audio Tatoeba) |
| Make Me A Hanzi + `hanzi-writer-data` | `https://raw.githubusercontent.com/skishore/makemeahanzi/master/` (`dictionary.txt`, `graphics.txt`) + npm `hanzi-writer-data` | `dictionary.txt`: LGPL v3+; `graphics.txt` / `hanzi-writer-data`: Arphic Public License | **9.574** chữ (`dictionary`), **9.574** chữ (`graphics`) | Thứ tự nét chữ (`public/strokes/`) và phân rã bộ thủ (`content/radicals.json`) |

## 2. Cách ánh xạ cấp độ từ `complete.json`

`complete.json` trộn nhiều nhãn (`old-1..6`, `new-1..7`, `newest-1..7`). Đo đếm thực tế trên `complete.json`:
- `new-1`: 506 · `new-2`: 750 · `new-3`: 953 (tổng dải `new-1..3` = **2.209** mục)
- `newest-1`: 294 · `newest-2`: 197 · `newest-3`: 487 (tổng dải `newest-1..3` = **978** mục)

Quy tắc ánh xạ trong `tools/prepare_stage1.py`:
- Chọn tất cả mục có ít nhất một nhãn thuộc `new-1..3` hoặc `newest-1..3` làm kho từ vựng cấp 1–3.
- Cấp nội bộ `level` gán theo cấp nhỏ nhất trong `newest-*` (nếu có), ngược lại theo `new-*` (giá trị `1`, `2`, hoặc `3`).
- Giao diện người học chia theo **4 chặng / 28 chủ đề** và tuyệt đối không nhắc đến "HSK".

## 3. Audio tự sinh offline

- Công cụ: Python `edge-tts` với các giọng `zh-CN-XiaoxiaoNeural` (`+0%`), `zh-CN-XiaoyiNeural`, `zh-CN-YunxiNeural`, `zh-CN-YunyangNeural`, đọc truyện `zh-CN-XiaoxiaoNeural` (`-10%`, vì `zh-CN-XiaohanNeural` không còn khả dụng trên `edge-tts`), và bản chậm `-25%` cho bài nghe.
- Không dùng audio của Tatoeba và không gọi API TTS lúc người học sử dụng ứng dụng.
