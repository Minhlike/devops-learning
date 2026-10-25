# Kiểm tra PDF sau tái biên soạn Phần IV — 2026-10-25

## Phạm vi nội dung

- Baseline `621b17d19f62798abf0ac2069d7476716f735f6c`. Viết lại phần thân 6/6 bài `P04.C01.L01–L03` và `P04.C02.L01–L03`; giữ nguyên cây 15 Phần, 58 Chương, 178 Bài và bìa đã duyệt. Không sửa nội dung bài ngoài P04.
- Bản đồ ngoài PDF ở `manuscript/P04/knowledge_map.md` gồm 44 đơn vị: 32 CORE, 11 SUPPORTING, 1 REFERENCE. Các bài lần lượt tăng 622→977, 546→843, 417→903, 396→812, 611→794, 430→1388 từ (tổng 3.022→5.717). Phần tăng tập trung vào object graph, ba lớp HEAD/index/worktree, ref, merge stages, rebase và hậu điều kiện phục hồi; không dùng số từ làm bằng chứng chất lượng thay cho việc đọc nội dung.
- Giữ các claim và QA ID cũ; cập nhật hash manifest, editorial evidence và một neo wave2 của detached HEAD. Nguồn G1–G9 giữ URL; thêm G10 (Git push 2.52.0) và G11 (Git restore 2.51.0) vào source map/lock, ngoài đường render.
- V09 được giữ. Thêm vector gốc V44–V48 từ `scripts/science_figures.py`, lần lượt cho object graph, ba lớp trạng thái, ref, fast-forward/merge stages và revert/reset. Không lấy tài sản Internet vào PDF: Pro Git có điều kiện CC BY-NC-SA; hình tìm ở Wikimedia thường đòi attribution/share-alike; hình CC0 tìm được không khớp đồ thị B–D–C. Hồ sơ nguồn/giấy phép và giới hạn từng hình ở `manuscript/figure_evidence.json`.

## Thí nghiệm và kiểm thử

- Git `2.51.2.windows.1` trong fixture tạm: đổi tên giữ blob nhưng đổi root tree; HEAD/index/worktree = 1000/2000/3000; merge conflict cho stage 1/2/3 = 1000/3000/2000; M có parent D/C; rebase tạo C′ khác C với parent D; revert `-m 1` đưa nội dung ví dụ về 3000; reset soft/mixed/hard cho các hậu trạng thái dự đoán. Chi tiết và giới hạn ở `manuscript/P04/experiment_evidence.md`. Fixture đã được xóa sau khi xác nhận đúng đường dẫn.
- Full regression sau bản thảo và hình đầu tiên: 44 test, 43 PASS, 1 SKIP (thiếu Go toolchain), 0 FAIL. Sau chỉnh sửa cuối ở L03, dựng lại PDF và chạy ba phép kiểm tập trung: bảo toàn migration, văn bản reviewed đến PDF, và panel/caption hình; 3 PASS. Kiểm riêng hợp đồng nguồn hình sau khi thu hẹp nguồn V09/V45/V48: 1 PASS. Tổng kiểm tập trung sau lượt full: 4 PASS, 0 FAIL. Bộ dựng/audit cuối báo `CANDIDATE_OK`.
- PDF chính và candidate giống byte, SHA-256 `9282c9881cc5b66b25f006b99a43de5f99be16c4ddc906bbfcea47a6cbea589e`. 269 trang A4, 310 bookmark, 693.392 ký tự text trích xuất, `source_leaks=0`; Times New Roman Regular/Bold và Consolas nhúng. Không có thay đổi bìa hoặc renderer dàn trang chung.
- Đã render và xem contact sheet trang 47–60 của Phần IV; xem chi tiết trang 48, 50, 52, 54, 56, 58–59 gồm mọi hình mới, V09 và trang chuyển chương. Trang 59 ban đầu chỉ còn bài tập; đã bổ sung ca suy luận phục hồi có giá trị và dựng lại, nay bài tập nằm cùng trang nội dung. Không thấy chữ, nhãn hình hay caption bị cắt; audit PDF kiểm vùng chữ an toàn trên toàn file.

## Giới hạn

- Giá trị timeout, đồ thị ký hiệu và quyết định `2500` trong sách là ví dụ giả định; fixture chỉ chứng minh cơ chế Git trên một máy Windows, không chứng minh cấu hình ứng dụng đúng ở production.
- Không chạy lại Go do thiếu toolchain. Không xem chi tiết mọi trang ngoài Phần IV trong lượt này; kết quả không cấp Publication PASS cho toàn sách. Hồ sơ nguồn kiểm từng claim mới trọng yếu, không khẳng định mọi câu trong 178 bài đã được kiểm toán độc lập.
