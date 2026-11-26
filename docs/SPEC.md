# BaoBao — Đặc tả sản phẩm & kỹ thuật (`docs/SPEC.md`)

## Problem Statement

Người trẻ Việt Nam muốn học tiếng Trung tập trung vào giao tiếp đời sống và đọc hiểu (kèm nghe và viết thử nhận diện chữ) thường gặp hai rào cản: các ứng dụng phổ biến ép người học qua cơ chế Hearts/Energy phạt sai lầm, bảng xếp hạng gây áp lực, hoặc phụ thuộc mạng/tài khoản/server; đồng thời tài liệu học tiếng Trung tiếng Việt rời rạc giữa từ vựng, hội thoại, bài đọc có kiểm soát cấp độ, luyện nghe chậm thật và luyện viết từng nét.

## Solution

BaoBao là web app tĩnh (PWA offline hoàn toàn sau lần tải đầu, phát hành trên GitHub Pages), không tài khoản, không API key hay TTS lúc người học sử dụng, đồng hành cùng linh vật gấu trúc tròn tên Bao. Mỗi phiên học kéo dài 7–10 phút, nạp 4–6 từ mới qua bốn kỹ năng Giao tiếp, Đọc hiểu, Nghe và Viết nhận diện chữ, kết hợp ôn tập lặp lại ngắt quãng FSRS (`ts-fsrs`) lưu cục bộ trong IndexedDB kèm sao lưu JSON.

## User Stories

1. Là người học, tôi muốn mở một đường link GitHub Pages trên laptop hoặc Safari iPhone mà không cần đăng ký hay đăng nhập, để bắt đầu học ngay lập tức.
2. Là người học, tôi muốn thấy bản đồ "Đường du hành của Bao" chia 4 chặng / 28 chủ đề theo đường cong zigzag, để biết rõ mình đang đứng đâu và còn gì phía trước.
3. Là người học, tôi muốn thấy mỗi nút bài hiển thị rõ trạng thái (đã xong có vương miện, đang học dở có vòng tiến độ, bài hiện tại nảy nhẹ kèm Bao, chưa mở có ổ khoá), để chọn đúng bài tiếp theo.
4. Là người học, tôi muốn bấm vào nút bài trên bản đồ để xem popover tên bài, kỹ năng luyện, XP và nút "BẮT ĐẦU", để chuẩn bị trước khi vào học.
5. Là người học, tôi muốn mở "Sổ tay" ngay trên banner mỗi chặng, để xem tóm tắt ngữ pháp ngắn gọn của chặng đó.
6. Là người học, tôi muốn bấm "Tải sẵn chặng này" trên bản đồ, để cache toàn bộ dữ liệu và audio của chặng phục vụ học khi mất mạng.
7. Là người học, tôi muốn xem thẻ "Hôm nay" ở cột phải bản đồ (vòng mục tiêu ngày, số thẻ đến hạn ôn, thẻ truyện đang đọc dở), để quản lý thói quen hằng ngày.
8. Là người học, tôi muốn học mỗi buổi giao tiếp 7–10 phút gồm khởi động 3–5 thẻ SRS, 4–6 từ mới, 1–2 mẫu câu khung, hội thoại mẫu, luyện tập tương tác, thử thách đóng vai 3 câu và tổng kết XP, để nắm chắc bài trong một lượt ngắn.
9. Là người học, tôi muốn không bao giờ bị mất tim (Hearts/Energy) hay bị khoá lượt khi trả lời sai, để thoải mái thử sai và học lại.
10. Là người học, tôi muốn xem thẻ từ mới có chữ Hán lớn 64px, pinyin 20px, nghĩa Việt, nút loa phát MP3 và minh hoạ gợi nhớ bộ thủ, để ghi nhớ mặt chữ và âm thanh cùng lúc.
11. Là người học, tôi muốn bấm vào bất kỳ từ nào trong câu ví dụ hoặc bài đọc để mở popup tra nghĩa Việt, pinyin, loa và nút "+ Ôn tập" mà không rời màn hình đang học.
12. Là người học, tôi muốn thực hành hội thoại đóng vai Bao trong khung chat với độ khó tăng dần (chọn 1/3 câu -> sắp xếp thẻ từ -> gõ pinyin hoặc chọn từ gợi ý) và thanh mục tiêu hội thoại, để luyện phản xạ giao tiếp.
13. Là người học, tôi muốn thu âm giọng mình đọc theo lượt nhân vật (shadowing) và tự nghe lại mà không bị chấm điểm AI, để tự rèn ngữ điệu một cách tự nhiên.
14. Là người học, tôi muốn đọc bài đọc hiểu trình bày như trang truyện trên laptop (chữ Hán 21px, line-height 1.9) với segmented control 3 chế độ pinyin (tất cả / chỉ từ mới / tắt), để chuyển dần từ phụ thuộc pinyin sang đọc mặt chữ.
15. Là người học, tôi muốn bài đọc đánh dấu từ mới bằng nền vàng nhạt `#FFF3B0`, từ yếu bằng gạch chấm mint dưới chân, kèm chức năng "Nghe cả bài" chạy highlight theo câu và câu hỏi kiểm tra cuối bài, để vừa đọc vừa nghe hiểu trọn vẹn.
16. Là người học, tôi muốn lưu tất cả từ mới của bài đọc vào hàng đợi SRS chỉ với một nút bấm sau khi đọc xong, để không bỏ sót từ vựng.
17. Là người học, tôi muốn luyện nghe qua trình phát tròn có vòng sóng âm, chọn tốc độ 0.75× (dùng file audio chậm tổng hợp sẵn), 1×, 1.25×, lặp lại 1 câu và tua qua lại câu bằng phím mũi tên, để nghe rõ thanh điệu và nối âm.
18. Là người học, tôi muốn bài nghe đi từ dễ đến khó (chọn nghĩa -> chọn chữ Hán -> ghép ô chữ theo audio -> điền từ thiếu -> nghe hội thoại trả lời -> chép chính tả rút gọn theo từng từ) và tự phát lại bản chậm khi sai, để tự sửa lỗi nghe.
19. Là người học, tôi muốn luyện viết từng chữ Hán theo bộ thủ trước, qua 3 mức (tô theo nét mờ -> viết có mẫu mờ -> viết từ trí nhớ) trên ô lưới mễ tự `米字格` với chấm nét thời gian thực (dữ liệu nét lưu cục bộ), để nhận diện mặt chữ vững chắc.
20. Là người học, tôi muốn xem hoạt hình thứ tự nét ("Xem nét"), bấm chip bộ thủ để hiểu cấu tạo chữ, và làm mini-quiz 4 chữ gần giống sau mỗi chữ viết xong, để phân biệt các chữ dễ nhầm.
21. Là người học, tôi muốn ôn tập flashcard theo thuật toán FSRS có lọc theo 4 nhóm (Đến hạn hôm nay / Từ yếu / Từ trong truyện / Chữ viết yếu), lật thẻ 3D bằng phím Space và chấm 4 mức (Again / Hard / Good / Easy) kèm khoảng lặp dự kiến, để tối ưu trí nhớ dài hạn.
22. Là người học, tôi muốn mặt sau thẻ flashcard luôn hiển thị câu ví dụ nguyên vẹn kèm audio, và thẻ SRS tách riêng 3 mặt (từ vựng / câu / chữ viết), để nhớ từ trong ngữ cảnh thật.
23. Là người học, tôi muốn theo dõi hồ sơ gồm tủ đồ của Bao mở khoá bằng XP, lịch streak tháng, 2 lá chắn Đóng băng streak, mục tiêu ngày 5/10/20 phút, huy hiệu thành tích và 4 thanh kỹ năng, để có động lực bền bỉ.
24. Là người học, tôi muốn chỉnh pinyin mặc định, âm thanh phản hồi, reduced motion, 3 mức cỡ chữ Hán, xem trang credit giấy phép dữ liệu và Xuất/Nhập toàn bộ tiến độ ra file JSON (có xác nhận và tự sao lưu bản cũ trước khi ghi đè), để giữ an toàn dữ liệu cá nhân.
25. Là người học, tôi muốn dùng phím tắt laptop (`Space`, `1`–`4`, `Enter`, `←`/`→`) xuyên suốt các màn học, để thao tác nhanh bằng bàn phím.

## Implementation Decisions

- **Kiến trúc tĩnh hoàn toàn:** Vite + TypeScript thuần, không framework UI nặng, không backend, không tài khoản, không API key runtime. Mọi route chạy qua hash router để tương thích trực tiếp với subpath GitHub Pages (`/baobao/`).
- **Quản lý nội dung theo chặng:** Tách dữ liệu JSON tại `content/stage-N/` (`words.json`, `lessons.json`, `readings.json`) và `content/radicals.json`, chỉ tải chặng đang học. Dữ liệu nét chữ từ `hanzi-writer-data` trích riêng các chữ có trong giáo trình vào `public/strokes/<char>.json` và truyền `charDataLoader` cục bộ cho `hanzi-writer` để không gọi CDN ngoài.
- **Audio đóng gói tĩnh:** Toàn bộ file MP3 được sinh trước bằng Python `edge-tts` vào `public/audio/` đặt tên theo hash nội dung; bài Nghe có bản `-25%` riêng cho tốc độ `0.75×`. Trình duyệt chỉ phát `<audio>` tĩnh và âm thanh phản hồi UI tổng hợp bằng Web Audio API.
- **Thuật toán ôn tập & lưu trữ cục bộ:** Dùng `ts-fsrs` với cấu hình cố định (`request_retention: 0.9`, `maximum_interval: 365`, `enable_fuzz: true`, learning steps `1m`/`10m`, relearning `10m`), tách thẻ theo 3 mặt (`vocab` | `sentence` | `writing`). Dữ liệu lưu trong IndexedDB qua `idb` với đúng 4 object stores (`cards`, `reviewLog`, `progress`, `settings`), mọi bản ghi tiến độ có `updatedAt`. Gọi `navigator.storage.persist()` khi bắt đầu học lần đầu.
- **PWA Offline:** `manifest.webmanifest` + Service Worker `sw.js` dùng chiến lược cache-first theo phiên bản và nhận thông điệp `CACHE_STAGE` để cache chủ động tài nguyên của từng chặng.
- **Pipeline dữ liệu offline (`tools/`):** Tách từ và kiểm soát cấp độ (`level_checker.py`) đối chiếu vốn từ tích luỹ + từ mới chú thích trên toàn bộ hội thoại, bài đọc, câu nghe trước khi đưa vào `content/`. Phần dịch và sinh nội dung dùng SDK `google-genai` (model `gemini-4-hydrogen`) đọc `GEMINI_API_KEY` từ biến môi trường lúc chạy `tools/`, không bao giờ ghi key vào repo.
- **Hệ thống giao diện:** Khung 1200px nền `#FFFBF3`, sidebar 240px (ẩn khi vào bài học; <768px chuyển bottom tab bar 5 mục), tối đa 2 màu loại bài trên 1 màn, cỡ chữ Hán sàn ≥ 20px, tuyệt đối không nhắc từ "HSK" trên UI, không dark mode ở bản đầu.

## Testing Decisions

Kiểm thử hành vi qua public boundary (seams), không test chi tiết nội bộ, giá trị kỳ vọng lấy từ nguồn độc lập (không tự tính lại theo logic code):

1. **`levelChecker` (`tools/level_checker.py`):** Đầu vào là văn bản tiếng Trung, tập từ được phép, tập từ mới chú thích, từ điển tách từ và ngưỡng tối đa từ lạ; đầu ra là kết quả đạt/loại, tỷ lệ từ ngoài vốn và danh sách từ chưa chú thích / chưa lặp đủ số lần. Bắt lỗi giáo trình vượt cấp.
2. **`srsEngine` (`src/services/srsEngine.ts`):** Đầu vào là thao tác tạo thẻ theo mặt (`vocab`/`sentence`/`writing`), chấm điểm (`Again`/`Hard`/`Good`/`Easy`) và lọc hàng đợi; đầu ra là trạng thái thẻ `ts-fsrs` độc lập từng mặt, khoảng lặp dự kiến và danh sách lọc đúng. Bắt lỗi sai lịch ôn hoặc lẫn mặt thẻ.
3. **`progressBackup` (`src/services/progressBackup.ts`):** Đầu vào là dữ liệu 4 bảng IndexedDB và file JSON nhập vào (hợp lệ hoặc hỏng cấu trúc); đầu ra là bản xuất đủ 4 bảng, bản tự sao lưu trước khi ghi đè khi hợp lệ, và từ chối sạch không mất dữ liệu cũ khi file nhập hỏng. Bắt lỗi mất tiến độ người học.

## Out of Scope

- Đăng nhập, tài khoản đám mây, đồng bộ server, leaderboard, bạn bè.
- Cơ chế Hearts/Energy, paywall hoặc mua hàng trong ứng dụng.
- Chấm điểm phát âm bằng AI hoặc Web Speech API.
- Dark mode ở phiên bản đầu.
- Sử dụng audio của Tatoeba hoặc nội dung từ ứng dụng thương mại.

## Further Notes

- Trong ĐỢT 1, khi chưa có `GEMINI_API_KEY` và repo GitHub public chưa tạo trên remote, pipeline vẫn hoàn chỉnh script sẵn sàng và Chủ đề 1 + Chủ đề 6 được biên soạn mẫu trọn gói đạt chuẩn kiểm cấp độ cùng audio thật từ `edge-tts`. Mọi mục phụ thuộc bước ngoài máy đều ghi rõ trạng thái `CHƯA KIỂM ĐƯỢC` cho tới khi hoàn tất điều kiện.
