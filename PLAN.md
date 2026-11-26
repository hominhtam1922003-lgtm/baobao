# Kế hoạch triển khai BaoBao (`PLAN.md`)

## ĐỢT 1 — Khung + dữ liệu mẫu trọn gói (đang thực hiện, dừng duyệt cuối đợt)
1. Khởi tạo repo, `GEMINI.md`, `NHAT-KY.md`, GitHub Actions deploy Pages, bộ khung thiết kế (`tokens.json`, `tokens.css`, SVG Bao & icon).
2. Xây pipeline `tools/`: tải 4 bộ dữ liệu mở (`docs/DATA.md`), kiểm cấp độ TDD (`level_checker.py`), chuẩn bị từ vựng Chặng 1, script Gemini (`translate_vi.py`, `generate_content.py`), trích nét chữ (`extract_strokes.py`), sinh audio offline (`generate_audio.py`).
3. Hoàn thiện nội dung mẫu trọn gói cho **Chủ đề 1 (Chào hỏi & tạm biệt)** và **Chủ đề 6 (Ăn uống: gọi món, trà sữa & cà phê)** đủ 4 kỹ năng + nét chữ + audio MP3 thật (kèm bản chậm −25%).
4. Xây lõi dịch vụ TDD (`srsEngine`, `db`, `progressBackup`, `contentLoader`, `audioPlayer`, `recorder`) và đủ 8 màn hình dùng được trên nội dung mẫu, chạy offline PWA.
5. Kiểm thử (`pytest`, `vitest`, `tsc`, `build`, `replica-test`, `code-review`, `security-audit`), ghi số đo thật và dừng báo cáo chờ duyệt.

## ĐỢT 2 — Đủ giáo trình (sau khi ĐỢT 1 được duyệt)
1. Chạy dịch Việt + kiểm mẫu 5% đối chiếu CC-CEDICT cho toàn bộ vốn từ HSK 3.0 cấp 1–3.
2. Sinh + chạy `level_checker.py` cho đủ 28 chủ đề (4 loại bài/chủ đề), 4 chương truyện dài kỳ, 4 bài kiểm tra cuối chặng.
3. Sinh đủ audio MP3 + trích đủ `public/strokes/` cho toàn giáo trình, đo và ghi tỷ lệ đạt/loại.
4. Hoàn thiện tủ đồ của Bao, lưới huy hiệu thành tích, logic Đóng băng streak, phím tắt đầy đủ trên toàn app.

## ĐỢT 3 — Hoàn thiện & tối ưu phát hành (sau khi ĐỢT 2 được duyệt)
1. Rà soát toàn bộ ứng dụng theo checklist PHẦN 8.
2. Tối ưu dung lượng bản build GitHub Pages (đo tổng MB thật).
3. Kiểm thử kịch bản lỗi: mất mạng giữa bài, nhập file JSON tiến độ hỏng, trình duyệt Safari iPhone, độ phân giải 1280px và 1920px.
4. Viết `README.md` hướng dẫn sử dụng và cách chạy `tools/` tái tạo dữ liệu.
