# Test Plan — BaoBao ĐỢT 1 (`replica/test-plan.md`)

| ID | Luồng | Kịch bản kiểm thử | Kết quả kỳ vọng |
|---|---|---|---|
| F01-H1 | Bản đồ -> Học từ | Mở `#/`, bấm nút Chủ đề 1 Giao tiếp -> BẮT ĐẦU -> hoàn thành S02 | 0 lỗi console, chữ Hán 64px, nút loa phát MP3 cục bộ, +XP lưu IndexedDB |
| F02-H1 | Đọc hiểu | Mở `#/reading/r-t1`, chuyển 3 chế độ pinyin, bấm từ mở popup, trả lời 3 câu | Popup hiện nghĩa Việt + loa; lưu SRS thành công |
| F03-H1 | Hội thoại | Mở `#/dialogue/t1-giao-tiep`, hoàn thành mục tiêu hội thoại | Hiện danh sách mục tiêu mint, đủ 3 cấp chọn/ghép/pinyin |
| F04-H1 | Luyện nghe | Mở `#/listening/t1-nghe`, bật 0.75× và phát | Nạp file MP3 chậm `-25%` cục bộ, không lỗi 404 |
| F05-H1 | Viết chữ | Mở `#/writing/t1-viet`, bấm Xem nét, mở giải thích bộ thủ | Nạp `strokes/<char>.json` cục bộ (0 request CDN ngoài) |
| F06-H1 | Ôn tập SRS | Mở `#/review`, bấm lật thẻ, chấm nút `[3] Good` | Lật 3D mượt, cập nhật `due` trong IndexedDB |
| F07-E1 | Offline | Sau khi tải trang trên preview, bật Offline -> tải lại & chuyển qua các màn | Shell, JSON, strokes và audio đã cache vẫn chạy không lỗi |
| F08-N1 | Nhập JSON hỏng | Trên `#/profile`, kiểm tra Xuất JSON và kiểm tra từ chối JSON hỏng | Đã kiểm chứng tự động qua `progressBackup.test.ts` |
| UI-M1 | Mobile 390px | Kiểm tra `#/` và `#/reading/r-t1` ở 390×844 | Sidebar ẩn, hiện bottom tab bar 5 mục, không tràn ngang |
