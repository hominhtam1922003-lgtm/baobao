# BaoBao Component Specs (`replica/design/components.md`)

1. **PressableButton**
   - Variants: `primary` (accent + lip), `comm` (`--comm` / `--comm-lip`), `read` (`--read` / `--read-lip`), `listen` (`--listen-lip` text `#FFF`), `write` (`--write` / `--write-lip`), `review` (`--review` / `--review-lip`), `vocab` (`--vocab` / `--vocab-lip`), `secondary` (`--surface` + `--border` lip), `ghost`.
   - Sizes: `sm` (36px), `md` (44px), `lg` (52px).
   - Depth & Active: `box-shadow: 0 var(--lip-h) 0 var(--btn-lip)`; `:active:not(:disabled)` dịch `translateY(4px)` và `box-shadow: 0 0 0 var(--btn-lip)`.
   - States: default, hover, active, focus-visible (3px outline `--vocab`), disabled (`--locked`), loading.
   - A11y: `<button type="button">`, nhãn tiếng Việt rõ ràng, chỉ rõ phím tắt nếu có.

2. **ClayCard**
   - Radius: `20px`–`24px` (`28px` cho flashcard), nền `--surface`, viền `1.5px solid --border`, `box-shadow: var(--shadow-clay)`.
   - Không trộn shadow material mờ nhiều tầng.

3. **LessonNode (Đường du hành của Bao)**
   - Size: `Ø72px` tròn, icon sticker viền trắng 2px ở giữa.
   - States: `done` (màu loại bài + vương miện nhỏ), `in-progress` (vòng SVG tiến độ quanh nút), `current` (`scale(1.15)` + nảy nhẹ + Bao đứng cạnh với bong bóng thoại), `locked` (`--locked` + ổ khoá).

4. **SegmentedControl**
   - Pill container `--bg` bo `999px` viền `--border`; nút con bo `999px`, active nền `--surface` + viền mảnh. Dùng cho 3 chế độ pinyin và tốc độ nghe.

5. **WordToken & WordPopup**
   - Token bấm được trong câu mẫu / bài đọc: cỡ chữ Hán `>= 20px` (`21px / 1.9` trong bài đọc), từ mới tô nền `--reading-hl`, từ yếu gạch chấm `--read-lip`.
   - Popup bo `16px`, hiển thị chữ Hán, pinyin (nhỏ hơn & `--ink-pinyin`), nghĩa Việt, nút loa + nút "+ Ôn tập".

6. **FeedbackBanner**
   - Trượt từ đáy màn học (`200ms`): đúng = `--ok-bg` + `--ok-accent`; sai = `--err-bg` + `--err-accent` (tuyệt đối không đỏ chói, không rung lắc phạt).

7. **AppShell & Navigation**
   - Desktop (`>= 768px`): sidebar cố định `240px` + vùng nội dung căn giữa tối đa `1200px` với topbar (tiêu đề + 3 chip streak / XP hôm nay / vòng mục tiêu).
   - Trong bài học (`S02`–`S06`): ẩn sidebar, hiện thanh tập trung tối đa `880px` (riêng `S04` Đọc dùng `1200px`).
   - Mobile (`< 768px`): bottom tab bar 5 mục (Bản đồ, Đọc, Nghe, Viết, Ôn tập); Hồ sơ mở qua chip avatar trên topbar.
