# BaoBao — Luật dự án (GEMINI.md)

Ưu tiên Serena để đọc code, Context Mode cho mọi đầu ra dài.

## Luật cứng (PHẦN 8 — VI PHẠM = LÀM LẠI)

1. Không Hearts/Energy, không leaderboard, không paywall giả. Không dark mode ở bản đầu.
2. Không nội dung bản quyền từ app/web thương mại; chỉ 4 bộ dữ liệu mở ở PHẦN 3 + nội dung AI sinh qua pipeline có script kiểm cấp độ. Không dùng audio Tatoeba.
3. Không chấm điểm phát âm bằng AI/Web Speech ở bản này — luyện nói chỉ là shadowing thu âm nghe lại.
4. Không API key trong repo, không gọi API lúc người học dùng app (kể cả TTS) — mọi thứ sinh offline lúc dựng nội dung.
5. Chữ Hán không bao giờ dưới 20px ở màn học; pinyin không to/đậm hơn chữ Hán; 1 màn tối đa 2 màu loại bài.
6. Số báo cáo = số đo thật; chưa kiểm bằng bản Pages thật thì ghi "CHƯA KIỂM ĐƯỢC", không suy đoán là đạt.
7. Xong việc nào commit + push việc đó, ghi NHAT-KY. Hết đợt thì dừng chờ duyệt, không tự chạy qua đợt.
8. Giao diện người học: tiếng Việt là chính; không nhắc "HSK" trong UI (chỉ dùng nội bộ cho cấp độ dữ liệu).

## Bắt buộc dùng Skill đã cài (PHẦN 0B)

| Lúc nào | Skill bắt buộc | Để làm gì |
|---|---|---|
| Ngay khi bắt đầu dự án | `to-spec` | Chuyển prompt này thành spec + PLAN.md trong repo trước khi code |
| Đầu ĐỢT 1, theo đúng thứ tự | `replica-recon` → `replica-architect` → `replica-design` | Khảo sát nguồn dữ liệu/thư viện → chốt kiến trúc → chốt design system theo PHẦN 5–6 |
| Khi thi công từng việc | `replica-build` | Thi công bám spec + design đã chốt |
| Trước khi viết logic khó (script kiểm cấp độ, FSRS, tách từ) | `tdd` | Viết test trước, code sau — logic sai ở đây là hỏng cả giáo trình |
| Khi viết `tools/` gọi Gemini API | `gemini-api-dev` | Dùng đúng API + kỹ thuật hiện hành, tránh lỗi quota/format |
| Cuối mỗi đợt, trước khi báo cáo | `replica-test` + `code-review` | Tự test + tự review, sửa hết lỗi tìm được rồi mới báo |
| Trước mỗi lần push lên repo PUBLIC | `security-audit` | Quét rò rỉ API key/secret toàn bộ cây — repo public, lộ key là cháy |
| Mọi báo cáo cho user | `caveman` | Trả lời cụt, tiết kiệm token |
| Xuyên suốt | Serena MCP + Context Mode MCP | Đọc code theo symbol + nén đầu ra tool — 2 nguồn ngốn token lớn nhất |

## Môi trường Windows trên máy này
- `git`: `C:\Users\Administrator\AppData\Local\GitHubDesktop\app-3.7.0\resources\app\git\cmd\git.exe`
- `npm` / `npx`: dùng `npm.cmd` và `npx.cmd` (PowerShell chặn `.ps1`)
- `python`: dùng `tools\.venv\Scripts\python.exe` (tạo từ `uv venv tools/.venv --python 3.12`)
