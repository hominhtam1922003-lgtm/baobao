# Recon Map — BaoBao (`replica/recon.md`)

## Scope
- **Sản phẩm:** Web app tĩnh PWA học tiếng Trung giao tiếp + đọc hiểu cho người trẻ Việt Nam ("BaoBao").
- **Nền tảng:** Trình duyệt laptop (1280px–1920px) và đáp ứng Safari iPhone (<768px).
- **Lát cắt ĐỢT 1:** Đủ app shell, offline PWA, IndexedDB 4 bảng, và cả 8 màn hình hoạt động trên dữ liệu thật Chặng 1 (trọng tâm mẫu trọn gói Chủ đề 1 & Chủ đề 6).

## Sources
| Nguồn | Giá trị cung cấp |
|---|---|
| Yêu cầu sản phẩm trong prompt | Đầy đủ đặc tả 8 màn hình, khuôn 4 kỹ năng, bảng màu PHẦN 6.1, luật cứng PHẦN 8 |
| `drkameleon/complete-hsk-vocabulary` (MIT) | Xương sống từ vựng cấp độ, bộ thủ, tần suất, pinyin |
| `cc-cedict` (`cedict_ts.u8`, CC BY-SA 4.0) | Từ điển tra cứu đối chiếu pinyin & nghĩa Anh |
| `downloads.tatoeba.org` (CC BY 2.0 FR) | Câu ví dụ `cmn` có liên kết `vie`/`eng` |
| `skishore/makemeahanzi` + `hanzi-writer-data` (LGPL/Arphic/MIT) | Thứ tự nét chữ & phân rã bộ thủ |

## Screen Inventory

| ID | Màn hình | Route | Mục đích | Thành phần chính | Trạng thái |
|---|---|---|---|---|---|
| S01 | Bản đồ bài học ("Đường du hành của Bao") | `#/` | Điều hướng 4 chặng / 28 chủ đề, mở bài học, xem mục tiêu ngày | Sidebar/Tab bar, Topbar chips, Banner chặng + nút Sổ tay + Tải sẵn chặng, Đường zigzag nút Ø72px, Popover bài học, Cột phải "Hôm nay" + Truyện dở | loading, filled, locked, active, completed, offline-cached, mobile |
| S02 | Học từ + mẫu câu | `#/lesson/:lessonId` (type `giao-tiep`) | Dạy 4–6 từ mới + 1–2 mẫu câu qua 7 bước 7–10 phút | Focus header (progress + ✕), SRS warmup, Thẻ từ 64px + loa + gợi nhớ bộ thủ, Bong bóng câu mẫu + popup tra từ, Bài tập 3 chạm & ghép thẻ, Đóng vai 3 câu, Tổng kết +XP | loading, warmup, card, drill, roleplay, feedback-ok, feedback-err, summary, mobile |
| S03 | Hội thoại giao tiếp | `#/dialogue/:lessonId` | Luyện phản xạ hội thoại 6–10 lượt + shadowing tự nghe lại | Focus header, Thanh mục tiêu hội thoại, Chat `#FFF1F3` (NPC trái / Bao phải), Pinyin ẩn/hiện, Nhập liệu 3 cấp (chọn -> sắp thẻ -> gõ pinyin), Ghi âm shadowing, Confetti cục bộ, Tổng kết | loading, npc-turn, choice-turn, tiles-turn, pinyin-turn, shadowing, completed, mobile |
| S04 | Đọc hiểu | `#/reading/:readingId` | Đọc truyện theo cấp độ với tra từ tại chỗ & nghe karaoke | Focus header 1200px, Segmented control pinyin (3 chế độ), Trang truyện 21px/1.9, Popup tra từ tại chỗ, Panel phải sticky (Từ mới + % đã biết + tiến độ + Bao gợi ý 1 lần), Nghe cả bài karaoke, Câu hỏi cuối bài + Lưu tất cả từ mới | loading, reading, word-popover, karaoke-playing, quiz-answered, empty, mobile |
| S05 | Luyện nghe | `#/listening/:lessonId` | Luyện nghe 5–7 phút theo độ khó tăng dần | Focus header, Trình phát tròn Ø180px `#8F82C8` + Bao tai nghe + sóng âm, 3 pill tốc độ (`0.75×` chậm thật / `1×` / `1.25×`), Lặp 1 câu, Tua `←/→`, 6 dạng bài (nghĩa -> chữ -> ghép ô -> điền khuyết -> hội thoại -> chính tả), Phát chậm tự động khi sai | loading, playing, paused, slow-replay, dictation, summary, error-audio, mobile |
| S06 | Viết chữ | `#/writing/:lessonId` | Học bộ thủ & viết từng nét bằng Hanzi Writer | Focus header, Canvas 480×480px lưới `米字格` lip cam, Nút Xem nét, Nút 3 mức (tô -> mẫu mờ -> trí nhớ), Panel phải 360px (chữ 48px + tiến độ nét + chip bộ thủ mở thẻ giải thích), Mini-quiz 4 chữ gần giống | loading, trace, ghost, memory, stroke-error, char-complete, lookalike-quiz, summary, mobile |
| S07 | Ôn tập flashcard (SRS) | `#/review` | Ôn thẻ FSRS 3 mặt tách biệt với câu ví dụ đầy đủ | App shell, 4 chip lọc + số thẻ chờ, Thẻ 640×360px lật 3D 300ms, Mặt trước (chữ/audio/câu khuyết), Mặt sau (pinyin + nghĩa + câu mẫu + loa), 4 nút FSRS (`1`–`4`) kèm khoảng lặp, Bao ăn mừng mỗi 10 thẻ, Tổng kết + Ôn thêm 5 thẻ yếu | loading, empty-due, front, flipped, streak-10, summary, mobile |
| S08 | Hồ sơ + Streak | `#/profile` | Quản lý danh tính Bao, streak, mục tiêu, thành tích, cài đặt & sao lưu | App shell, Lưới 3 cột clay card: Danh tính + Tủ đồ Bao, Lịch streak + 2 Đóng băng, Mục tiêu ngày 5/10/20p, Huy hiệu thành tích, 4 thanh kỹ năng, Cài đặt + Xuất/Nhập JSON + Về ứng dụng (credit giấy phép) | filled, freeze-used, import-confirm, import-error, credits-modal, mobile |

## User Flows

- **F01 Khởi động & học bài giao tiếp đầu tiên:** `S01 (chọn bài) -> Popover -> BẮT ĐẦU -> S02 (7 bước) -> Tổng kết -> S01 (nút chuyển trạng thái xong + XP/streak cập nhật)` (happy path: ~12 chạm/phím).
- **F02 Đọc hiểu & tra từ tại chỗ:** `S01 / Sidebar Đọc -> S04 -> Đổi chế độ pinyin -> Bấm từ mở popup -> Lưu SRS -> Nghe cả bài -> Trả lời 3–5 câu -> Lưu tất cả từ mới`.
- **F03 Hội thoại & shadowing:** `S01 / S02 gợi ý -> S03 -> Hoàn thành mục tiêu hội thoại -> Thu âm shadowing & nghe lại -> Lưu câu hay`.
- **F04 Luyện nghe & chép chính tả:** `S01 / Sidebar Nghe -> S05 -> Nghe tốc độ 1×/0.75× -> Làm bài tăng tiến -> Sai tự phát chậm -> Hoàn thành`.
- **F05 Viết chữ theo bộ thủ:** `S01 / Sidebar Viết -> S06 -> Bấm chip bộ thủ -> Viết 3 mức -> Mini-quiz 4 chữ -> Tổng kết`.
- **F06 Ôn tập FSRS hàng ngày:** `S01 thẻ Hôm nay / Sidebar Ôn tập -> S07 -> Chọn lọc -> Space lật thẻ -> Phím 1–4 chấm FSRS -> Tổng kết`.
- **F07 Tải sẵn chặng & học offline:** `S01 bấm "Tải sẵn chặng này" -> SW cache JSON + audio + strokes -> Tắt mạng -> Mở lại app & học đủ 4 kỹ năng`.
- **F08 Sao lưu & khôi phục tiến độ:** `S08 -> Xuất JSON -> Lưu file -> Nhập JSON -> Hộp thoại xác nhận -> Tự sao lưu bản cũ -> Ghi đè / báo lỗi nếu file hỏng`.

## Repeated Components

- `AppShell` (Sidebar 240px desktop / Bottom Tab Bar 5 mục <768px, Topbar với 3 chip Streak/XP/Goal)
- `LessonHeader` (Focus mode bar: nút ✕, thanh tiến độ mượt, bộ đếm)
- `PressableButton` (variants: `primary`, `secondary`, `ghost`, `lesson-color`, `fsrs-rating`; lip 4px lún khi `:active`)
- `ClayCard` (bo 20–28px, bóng clay mềm)
- `WordPopup` (tra nghĩa, pinyin, loa, nút "+ Ôn tập")
- `AudioButton` (nút loa tròn rung khi phát + trạng thái loading/playing/error)
- `BaoMascot` (SVG linh vật theo biểu cảm + phụ kiện tủ đồ)
- `FeedbackBanner` (panel trượt lên dưới đáy: mint khi đúng, hồng nhạt khi sai)
- `SegmentedControl` (chọn chế độ pinyin / tốc độ nghe / bộ lọc)
- `Modal` (Sổ tay ngữ pháp, Chi tiết bộ thủ, Xác nhận nhập dữ liệu, Về ứng dụng)

## Inferred Client Data Model

- `Word`: `{id, hanzi, pinyin, meaningVi, radical, level, mnemonic?, examples: [{hanzi, pinyin, vi, audio}]}`
- `Lesson`: `{id, stage, topicId, title, type, newWords, patterns, dialogue?, exercises, roleplay?, xp}`
- `Reading`: `{id, stage, topicId, title, mode: 'fluent'|'study', knownRatio, paragraphs, newWords, questions, audioFull, audioSentences}`
- `SrsCardRecord` (IndexedDB `cards`): `{key: "${itemId}::${facet}", itemId, facet: 'vocab'|'sentence'|'writing', hanzi, pinyin, meaningVi, example?, audio?, card: Card (ts-fsrs), updatedAt}`
- `ReviewLogRecord` (IndexedDB `reviewLog`): `{id?, key, rating, state, reviewedAt, elapsedMs}`
- `ProgressRecord` (IndexedDB `progress`): `{id, xp, streak, bestStreak, freezesLeft, activeDates[], completedLessons[], lessonProgress{}, storyBookmarks{}, unlockedAccessories[], badges[], skillXp: {giaoTiep, doc, nghe, viet}, updatedAt}`
- `SettingsRecord` (IndexedDB `settings`): `{id: 'user', learnerName, dailyGoalMinutes: 5|10|20, pinyinMode: 'all'|'new'|'off', sfxEnabled, reducedMotion, hanziSize: 'sm'|'md'|'lg', updatedAt}`

## Cannot Be Cloned / Out of Scope

- Nội dung từ app/web thương mại (`skip`), audio Tatoeba (`skip`), chấm điểm phát âm bằng AI (`skip`), đồng bộ tài khoản đám mây (`skip`).

## Size Estimate

- Toàn dự án 3 đợt: `L` (giáo trình 28 chủ đề + 8 màn tương tác + pipeline offline). Đợt 1 là lát cắt dọc hoàn chỉnh cho Chặng 1 (Chủ đề 1 & 6).
