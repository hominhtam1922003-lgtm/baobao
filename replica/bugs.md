# Bug Report — BaoBao ĐỢT 1 (`replica/bugs.md`)

| ID | Mức độ | Màn hình / File | Mô tả & Tái hiện | Nguyên nhân & Cách sửa | Trạng thái |
|---|---|---|---|---|---|
| B01 | S1 | `vite.config.ts` | `vite preview` chạy ở `/` thay vì `/baobao/` nên browser mở `http://localhost:4173/baobao/` bị 404 script JS | Kiểm tra `process.argv.includes('preview')` để dùng `base = '/baobao/'` cả khi preview lẫn build | Fixed |
| B02 | S1 | `src/screens/DialogueScreen.ts` | Vào `#/dialogue/t1-giao-tiep` dừng ở lượt NPC 1/6, không hiện nút lựa chọn trả lời cho Bao | Tự động mở các lượt `npc` dẫn đầu cho tới lượt nhập liệu đầu tiên của Bao; thêm thu hồi `URL.revokeObjectURL` và dừng recorder khi thoát | Fixed |
| B03 | S2 | `src/screens/ReadingScreen.ts` | `calc(21px * var(--hanzi-scale))` tụt xuống `19.32px` (< 20px) khi chọn cỡ chữ nhỏ (`0.92`) + bấm lại đáp án cộng lặp +25 XP | Bọc `max(20px, calc(21px * var(--hanzi-scale)))` và gắn cờ `awardedReadingXp` | Fixed |
| B04 | S2 | `src/screens/ReviewScreen.ts` | Lật thẻ thay toàn bộ `body.innerHTML` làm mất hiệu ứng xoay 3D 300ms | Chỉ toggle class `.is-flipped` và cập nhật vùng nút chấm bên dưới | Fixed |
| B05 | S2 | `src/services/progressBackup.ts`, `src/router.ts` | `validateBackup` chưa kiểm tra kiểu số cho `progress`; `router` chưa escape `err.message` | Kiểm tra `Number.isFinite` từng trường số của `progress` (huỷ transaction nếu sai) và bọc `escapeHtml` | Fixed |
| B06 | S3 | `src/components/AppShell.ts`, `src/screens/ProfileScreen.ts`, `src/services/srsEngine.ts` | Nhãn tab mobile `"nghe"` viết thường; vòng mục tiêu dùng tổng XP thay vì XP hôm nay; Đóng băng streak chưa tính lại `streak`; credits chứa chuỗi "HSK" | Đặt `mobileLabel` rõ ràng (`Nghe`), thêm `dailyXp`/`getTodayXp`, chuyển `useStreakFreeze`/`equipAccessory` về `srsEngine.ts`, đổi nhãn credit sang `drkameleon` (MIT) | Fixed |
