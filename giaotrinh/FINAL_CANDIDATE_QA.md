# Kiểm tra bản PDF chính sau tái biên tập Phần II — 2026-10-24

## Phạm vi và nội dung

- Cây xuất bản giữ **15 Phần, 58 Chương, 178 Bài**. Lượt này chỉ tái biên tập 10 bài `P02.C03.L01–L04`, `P02.C04.L01–L03` và `P02.C05.L01–L03`. Nội dung P11, P02.C01–C02 và các Phần khác không đổi.
- Cả phần thân của 10 bài được viết lại theo mạch chẩn đoán và phục hồi. Từ ngữ giảm từ 6.067 xuống 5.800 sau khi gộp diễn giải lặp. Bảng số liệu C03, unit Atlas, ví dụ O-7/outbox, bài tập, các neo claim và liên kết chéo vẫn còn. Hash của 10 bài trong manifest và hồ sơ biên tập đã đồng bộ.
- Hồ sơ migration vẫn giữ ánh xạ 88 mục, 216 đoạn và 267 claim. Kiểm thử migration cho phép 10 bài được tái biên tập bảo toàn claim anchors thay vì yêu cầu giữ nguyên từng đoạn văn cũ. ID và URL nguồn đã khóa không đổi.
- Các cơ chế dễ nhầm được giữ tách biệt: wall time / CPU time / PSI / iowait; virtual memory / page cache / reclaim / OOM; unit start / process alive / service readiness; ghi tệp / `fsync` / backup nhất quán / restore kiểm chứng. Ví dụ tính toán và sự cố được ghi rõ là giả định.

## PDF và điều hướng

- `Cam_nang_devops.pdf` và candidate cùng byte; SHA-256: `c9d12e8bff74acd2eee289eb5059533cebbd39c2faeab15ab03cdebeadfa8380`.
- **268 trang A4**, **310 bookmark**, 148 liên kết nội bộ, 0 liên kết ngoài. Văn bản trích xuất có 693.269 ký tự; audit bộ dựng không thấy ký tự Unicode thay thế.
- Times New Roman Regular/Bold và Consolas được nhúng; Arial Bold phục vụ thiết kế và Helvetica phục vụ thành phần PDF hệ thống. Audit kiểm mục lục, bookmark, đích trang, vùng in và 18 hình vector/caption.
- Kiểm văn bản, bookmark, metadata và hyperlink: **0 rò nguồn tham khảo**. URL thuộc ví dụ kỹ thuật vẫn được giữ khi cần.

## Kiểm thử và trang in

- `python -X utf8 -m unittest discover -s giaotrinh/tests -q`: **44 test OK, 1 SKIP** do không có Go toolchain trong PATH; 0 FAIL.
- `python -X utf8 -m giaotrinh.scripts.build`: `CANDIDATE_OK pages=268 bookmarks=310 source_leaks=0`. Chạy lại `audit()` trên PDF chính sau khi cập nhật: PASS. Candidate và bản chính có cùng SHA-256.
- Đã render và xem contact sheet của **11/11 trang bị ảnh hưởng (19–29)**; mở chi tiết trang 22 (bảng và bài tập), 23 (unit), 29 (phục hồi và bài tập). Không thấy chữ, bảng hay code bị cắt hoặc tràn vùng in. Hai câu hỏi từng bị đẩy sang trang gần trống đã trở lại trang 22 và 29. Các Phần khác không được render lại trong lượt này; audit hình học vẫn kiểm toàn PDF.

## Giới hạn thực nghiệm

- **SKIP:** Ví dụ Go chưa chạy trên máy QA này.
- **UNKNOWN:** Không thực thi các tình huống systemd, I/O hay restore PostgreSQL trên host Linux cô lập trong lượt biên tập này; dữ liệu giả định không được trình bày như log thật. Đối chiếu tài liệu Linux kernel, Linux man-pages và systemd chỉ kiểm các cơ chế được biên tập, không thay phản biện độc lập cho mọi claim của sách.
- Báo cáo này không cấp Publication PASS cho toàn sách.
