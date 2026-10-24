# Kiểm tra bản PDF chính sau tái biên tập Phần III — 2026-10-24

## Phạm vi nội dung

- Baseline: `fb2ee8b0306171b9035653f08ce334c514fb2a12`. Biên tập xuyên suốt 10 bài `P03.C02.L01–L04`, `P03.C03.L01–L03`, `P03.C04.L01–L03`; không sửa nội dung P03.C01, P02, P11 hay Phần khác.
- Cây xuất bản vẫn gồm 15 Phần, 58 Chương, 178 Bài. Văn bản 10 bài từ 5.996 xuống 5.436 từ sau khi bỏ lặp; trace TCP, tuple NAT, cache 30/70 giây, timeout 1.500/2.000 ms, ví dụ HTTP hai chặng, bài tập, hình/code và tham chiếu chéo được giữ đúng nghĩa.
- Đã so 31 neo biên tập và mọi marker `figure`, `code`, `xref` của 10 bài với bản gốc. Hash manifest và editorial evidence đã đồng bộ. Không đổi ID/URL nguồn đã khóa.
- Đối chiếu chọn lọc các cơ chế với RFC 9293 (TCP), RFC 8446 (TLS 1.3), RFC 9110 (HTTP semantics), RFC 9111 (HTTP cache), RFC 3022 (NAPT) và RFC 2308 (DNS negative cache). Không coi việc neo tồn tại là bằng chứng mọi claim của sách đã được xác minh độc lập.

## PDF và kiểm thử

- `Cam_nang_devops.pdf` và candidate giống byte; SHA-256: `339d0693b10fa81e13b61ac5445f137e26012b0a5cae5006fdff5de7ae9f53bf`.
- 267 trang A4, 310 bookmark, 0 URI action ngoài, 690.618 ký tự văn bản trích xuất. Bộ dựng báo `source_leaks=0`; Times New Roman Regular/Bold và Consolas nhúng. Chạy `audit()` trên cả candidate và PDF chính: PASS.
- `python -X utf8 -m unittest discover -s giaotrinh/tests -q`: 44 test OK, 1 SKIP do Go toolchain không có trong PATH, 0 FAIL.
- Đã render và xem đủ 13 trang 35–47 (ba chương sửa và trang ranh giới phần kế tiếp); kiểm tra hình TCP ở trang 36, HTTP trace ở trang 44, ngắt trang và lề. Không thấy chữ/code/hình bị cắt hoặc tràn. Các trang khác không được render lại trong lượt này; audit hình học vẫn chạy trên toàn PDF.

## Giới hạn

- Các tình huống client, gateway, proxy và upstream trong bài là dữ liệu giả định; không được báo như packet capture hay log production đã đo.
- Không thực thi lab mạng có namespace, TLS endpoint hay reverse proxy trong lượt biên tập văn phong. Kiểm thử Go SKIP. Không cấp Publication PASS cho toàn sách từ lượt QA này.
