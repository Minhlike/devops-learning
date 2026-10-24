# Kiểm tra bản PDF chính sau tái biên tập Phần XI — 2026-10-24

## Phạm vi và nội dung

- Cây xuất bản giữ **15 Phần, 58 Chương, 178 Bài**. Chỉ nội dung 9 bài `P11.C01.L01–L03`, `P11.C02.L01–L03`, `P11.C04.L01–L03` được tái biên tập trong lượt này; 15 bài còn lại của P11 và các Phần khác không đổi.
- Chín bài được viết lại cả phần giải thích cơ chế, tình huống và kết luận, không chỉ thay lời dẫn. Tổng văn bản của chín bài giảm từ 5.547 xuống 4.982 từ sau khi bỏ đoạn lặp. Claim anchors, liên kết nội bộ, hình V23 và YAML minh họa còn nguyên; hash trong manifest và hồ sơ biên tập đã đồng bộ.
- Hồ sơ migration giữ 88 mục, 216 đoạn, 267 claim, 23 ví dụ và 79 cặp bài tập–đáp án cũ. URL của ID nguồn cũ được khóa. Kiểm thử migration cho phép một sửa chữa đã kiểm chứng trước đây: ví dụ CPU ở chương 18 là 24 giây trên **mỗi** instance, tổng 48 giây trong 120 giây, tức 0,4 lõi.

## PDF và điều hướng

- Tệp chính `Cam_nang_devops.pdf` và candidate cùng byte; SHA-256: `ca195fa715798fc25d3fef2cdb0abce1b6ab940b96b2612e1363fb56e3cfc68a`.
- **269 trang A4**, **310 bookmark**, 148 liên kết nội bộ, 0 liên kết ngoài. PDF trích xuất 694.198 ký tự, không có ký tự Unicode thay thế theo audit của bộ dựng.
- Times New Roman Regular/Bold và Consolas được nhúng; Arial Bold phục vụ thành phần thiết kế và Helvetica phục vụ thành phần PDF hệ thống.
- Mục lục in có Phần và Chương, bookmark có cấp Bài; audit kiểm tra nhãn, thứ tự, đích trang và vị trí mở Chương. Mười tám hình khoa học dạng vector có caption và panel riêng; audit kiểm tra mỗi hình và caption đúng một lần, không cắt panel.
- Kiểm tra văn bản, bookmark, metadata và hyperlink: **0 rò nguồn tham khảo**. URL thuộc ví dụ kỹ thuật vẫn được giữ khi cần.

## Kiểm thử và kiểm tra hình ảnh

- `python -X utf8 -m unittest discover -s giaotrinh/tests -q`: **44 test OK, 1 SKIP** do không có Go toolchain trong PATH. Không có FAIL. Kiểm thử migration của chín bài đã tái biên tập bảo toàn claim anchors thay vì đòi giữ nguyên văn từng đoạn cũ.
- `python -X utf8 -m giaotrinh.scripts.build`: `CANDIDATE_OK pages=269 bookmarks=310 source_leaks=0`. Chạy lại `audit()` trên PDF chính sau khi cập nhật: PASS.
- Đã render **35/35 trang Phần XI (143–177)** và xem ba contact sheet bao phủ cả dải. Đã xem riêng các trang 146 (sơ đồ V23), 149–150 (YAML), 158–159 (Service/NetworkPolicy). Không thấy hình, code hoặc chữ bị cắt hay tràn lề trong phạm vi ảnh đã xem. Những phần khác không được render lại ở lượt biên tập này; audit hình học vẫn kiểm toàn bộ PDF.

## Giới hạn thực nghiệm

- **SKIP:** Chưa chạy ví dụ Go trên máy QA này.
- **UNKNOWN:** Không tạo cluster Kubernetes hay hệ thống production để chạy lại các tình huống giả định. Kiểm tra cấu trúc claim và neo nguồn không chứng minh độc lập ngữ nghĩa của mọi claim.
- Báo cáo này ghi các phép kiểm đã thực hiện cho PDF hiện tại; chưa phải Publication PASS hoặc phản biện học thuật độc lập cho toàn sách.
