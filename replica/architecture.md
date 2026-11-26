# Architecture — BaoBao (`replica/architecture.md`)

## Stack (Static Web App + Offline Content Pipeline)

| Tầng | Lựa chọn | Lý do |
|---|---|---|
| Build & Runtime | Vite + TypeScript thuần (không framework UI nặng) | Bundle nhỏ, kiểm soát DOM/animation/focus trực tiếp, xuất static chuẩn GitHub Pages |
| Styling | CSS custom properties (`tokens.css`) + CSS thuần | Bám sát lip 4px, clay shadow, responsive `<768px`, không phụ thuộc thư viện CSS nặng |
| Fonts | Self-hosted `@fontsource/baloo-2` + `@fontsource/noto-sans-sc` (subset kiểm soát MB) | Đảm bảo hiển thị tiếng Việt & chữ Hán đẹp ngay cả khi mất mạng hoàn toàn |
| Viết chữ | `hanzi-writer` + dữ liệu trích tại `public/strokes/` | Chấm từng nét thời gian thực hoàn toàn offline qua custom `charDataLoader` |
| SRS | `ts-fsrs` (`request_retention: 0.9`, `maximum_interval: 365`, `enable_fuzz: true`) | Thuật toán FSRS chuẩn, bước học `1m`/`10m`, tái học `10m`, tách 3 mặt thẻ |
| Lưu trữ | IndexedDB qua `idb` (4 bảng: `cards`, `reviewLog`, `progress`, `settings`) | Bền vững offline, `navigator.storage.persist()`, xuất/nhập JSON toàn bộ |
| Hiệu ứng | `canvas-confetti` | Ăn mừng cục bộ và hoàn thành chặng/streak (tôn trọng `prefers-reduced-motion`) |
| Pipeline Offline (`tools/`) | Python 3.12 (`uv`), `edge-tts`, `pypinyin`, `google-genai`, `pytest` | Tải 4 bộ mở, tách từ kiểm cấp độ, dịch Việt, sinh MP3 thường + chậm −25% trước build |
| Hosting | GitHub Pages qua GitHub Actions (`base: '/baobao/'` khi build) | Phát hành static miễn phí qua 1 link duy nhất |

## IndexedDB Schema (`baobao-db` v1)

1. `cards` (keyPath: `key` = `${itemId}::${facet}`): `{ key, itemId, facet, hanzi, pinyin, meaningVi, example?, audio?, card, createdAt, updatedAt }` — index theo `facet`, `due` (`card.due`).
2. `reviewLog` (keyPath: `id`, autoIncrement): `{ id, key, facet, rating, state, reviewedAt, elapsedMs }` — index theo `key`, `reviewedAt`.
3. `progress` (keyPath: `id`): bản ghi `'main'` chứa `{ id: 'main', xp, streak, bestStreak, freezesLeft, activeDates, completedLessons, lessonProgress, storyBookmarks, unlockedAccessories, badges, skillXp, updatedAt }`.
4. `settings` (keyPath: `id`): bản ghi `'user'` chứa `{ id: 'user', learnerName, dailyGoalMinutes, pinyinMode, sfxEnabled, reducedMotion, hanziSize, updatedAt }`.

## Static Content Contracts (`content/stage-N/`)

- `content/curriculum.json`: danh mục 4 chặng, 28 chủ đề, ghi chú ngữ pháp "Sổ tay" theo chặng, tóm tắt truyện dài kỳ.
- `content/radicals.json`: bảng bộ thủ + chữ cùng bộ trích từ Make Me A Hanzi `dictionary.txt`.
- `content/stage-1/words.json`: mảng `Word[]` của Chặng 1.
- `content/stage-1/lessons.json`: mảng `Lesson[]` của Chặng 1 (`giao-tiep`, `nghe`, `viet`, `doc` link sang `readings.json`).
- `content/stage-1/readings.json`: mảng `Reading[]` của Chặng 1.
- Mọi fetch qua helper dùng `import.meta.env.BASE_URL` để chạy khớp cả dev (`/`) và Pages (`/baobao/`).

## Offline & Error Boundaries

- `public/sw.js` dùng `CACHE_VERSION` rõ ràng: cache-first cho app shell, `content/`, `strokes/`, `audio/`. Hỗ trợ `postMessage({ type: 'CACHE_STAGE', urls })` để tải chủ động toàn bộ tài nguyên của chặng.
- Nhập file sao lưu JSON: kiểm tra schema bắt buộc 4 bảng trước khi chạm IndexedDB; tạo bản sao lưu tạm `baobao-auto-backup` trong `localStorage` hoặc snapshot bộ nhớ trước khi ghi đè; nếu hỏng cấu trúc thì huỷ sạch và báo lỗi cụ thể.

## Build Order (ĐỢT 1)

1. `tokens.json` / `tokens.css` (đạt 0 lỗi WCAG AA qua `contrast.py`) -> Vite shell + `#/design`.
2. Pipeline `tools/` + TDD `level_checker.py` -> tải 4 bộ dữ liệu -> xuất Chặng 1 + mẫu Chủ đề 1 & 6 + strokes + audio MP3.
3. Lõi dịch vụ TDD: `srsEngine.ts`, `db.ts`, `progressBackup.ts`, `contentLoader.ts`, `audioPlayer.ts`, `recorder.ts`.
4. App shell + SW + lần lượt 8 màn hình S01–S08 -> kiểm thử `replica-test` + `code-review` + `security-audit`.
