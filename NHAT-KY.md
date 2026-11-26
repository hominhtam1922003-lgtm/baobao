# Nhật ký dự án BaoBao

| Thời gian | Việc | Kết quả đo thật | Commit |
|---|---|---|---|
| 2026-11-26 12:10 | Khởi tạo repo local, GEMINI.md, NHAT-KY.md, .gitignore | 4 file gốc; remote `origin` trỏ `hominhtam1922003-lgtm/baobao` (chưa tạo trên GitHub) | `fc1513d` |
| 2026-11-26 12:12 | Viết SPEC, PLAN, recon, architecture, design tokens | 8 file; `contrast.py` đạt 22/22 cặp PASS/AA/AAA (0 lỗi) | `afa2cf4` |
| 2026-11-26 12:14 | Dựng khung Vite + TS, font tự host, SVG Bao/icon, Pages workflow | `npm.cmd run build` pass (21 file, `dist/` = 5.39 MB) | `c69c69e` |
| 2026-11-26 12:19 | Pipeline dữ liệu mở (`tools/`), TDD `level_checker.py`, `docs/DATA.md` | HSK 11.470 · CEDICT 125.474 · Tatoeba 89.325 cmn (667 cmn-vie, 66.225 cmn-eng) · MMAH 9.574; HSK1-3=1.207 từ; `pytest` 5/5 pass | `10fd783` |
| 2026-11-26 12:19 | Dịch vụ lõi TS (`srsEngine`, `db`, `progressBackup`, `contentLoader`, `audioPlayer`, `recorder`, `pwa`) | `vitest` 6/6 pass, `tsc --noEmit` 0 lỗi | `22b98ad` |
| 2026-11-26 12:25 | Nội dung Chặng 1 + mẫu Chủ đề 1 & 6 + nét chữ + audio MP3 | 129 từ (96 câu Tatoeba cmn-vie), 8 bài, 2 bài đọc; level check 6/6 pass (0 loại); 518 file nét; 365/365 MP3 (5,22 MB) | `4ee51f2` |
| 2026-11-26 12:26 | App shell, SW offline & đủ 8 màn hình S01–S08 | `npm.cmd run build` pass (`dist/` = 12,26 MB, JS = 193,49 kB) | `11d5223` |
| 2026-11-26 12:39 | Kiểm thử `replica-test` + `code-review` 2 trục + `security-audit` & sửa lỗi B01–B06 | `pytest` 5/5, `vitest` 6/6, `tsc` 0 lỗi, `build` 910 file (`12,26 MB`), browser QA 8 màn + 390px pass (`376/376` SW cache, 0 console/network error, 0 secret/HSK in `src/`) | `11b68c0` |
| 2026-11-26 13:28 | Quét `security-audit`, push `origin/main`, deploy GitHub Pages & kiểm thử bản live | `security-audit` 0 secret/0 file nhạy cảm trên 951 file tracked + full `git log`; Actions run `45768111814` `success`; browser QA live `https://hominhtam1922003-lgtm.github.io/baobao/` (S01 Map, S02 Topic 1, S06 Writing `/baobao/strokes/` 44 SVG paths, S08 Profile) đạt HTTP 200, 0 console error, 0 HTTP 4xx/5xx, 0 `"HSK"` | `pending` |
