# Kiểm tra bản PDF chính sau biên tập Phần XI — 2026-10-24

## Phạm vi và nội dung

- Cây xuất bản giữ **15 Phần, 58 Chương, 178 Bài**; bài tập và lời giải ở cuối sách dùng tiêu đề tiếng Việt cho người đọc. Manifest và các mã nội bộ nằm ngoài PDF.
- Hồ sơ migration giữ 88 mục, 216 đoạn, 267 claim, 23 ví dụ và 79 cặp bài tập–đáp án cũ. URL của ID nguồn cũ được khóa. Kiểm thử migration cho phép đúng một sửa chữa đã kiểm chứng: ví dụ CPU ở chương 18 là 24 giây trên **mỗi** instance, tổng 48 giây trong 120 giây, tức 0,4 lõi.
- Tệp chính `Cam_nang_devops.pdf` và candidate là cùng byte; SHA-256: `47f170d94de48dd0327c3bbd75b178dafc3d982ad97bbe2166af91701335cbe4`.
- Cả 24 bài của Phần XI được biên tập văn phong; hash trong manifest và hồ sơ biên tập đã đồng bộ. Cơ chế, YAML, số liệu, phép tính và neo chứng cứ được giữ trong bản thảo.

## PDF và điều hướng

- **270 trang A4**, **310 bookmark**, 148 liên kết nội bộ, 0 liên kết ngoài. PDF trích xuất 697.325 ký tự, không có ký tự Unicode thay thế.
- Times New Roman Regular/Bold và Consolas được nhúng. Bộ dựng có thêm Arial Bold cho thành phần thiết kế và Helvetica cho thành phần PDF hệ thống.
- Mục lục in trình bày Phần và Chương với số trang đối chiếu bookmark. Bookmark có cấp Bài. Bộ kiểm tra xác nhận nhãn, thứ tự, đích trang và vị trí mở Chương; bài tập có mặt cả ở đề và lời giải.
- 18 hình khoa học dạng vector có caption và panel riêng. Bộ kiểm tra xác nhận mỗi hình và caption xuất hiện đúng một lần, không cắt panel. Hồ sơ hình và dữ liệu nguồn ở ngoài PDF.
- Kiểm tra nguồn tham khảo ở văn bản, bookmark, metadata và hyperlink: **0 rò nguồn**. URL thuộc ví dụ kỹ thuật vẫn được giữ khi cần. Footer không còn nhãn “BẢN ĐỌC THỬ”.

## Kiểm thử và kiểm tra hình ảnh

- `python -X utf8 -m unittest discover -s giaotrinh/tests -q`: **44 test OK, 1 SKIP** do không có Go toolchain trong PATH. Không có FAIL.
- `python -X utf8 -m giaotrinh.scripts.build`: `CANDIDATE_OK pages=270 bookmarks=310 source_leaks=0`. Kiểm tra hình học của bộ dựng xác nhận A4, font nhúng, các khối chữ trong vùng an toàn và đích mục lục/bookmark.
- Đã render **36 trang Phần XI (143–178)**, xem 3 contact sheet bao phủ đủ dải trang này và xem chi tiết các trang 144, 149, 158, 174, 178; trang 144 được render lại sau khi sửa footer. Không thấy hình, code, chữ bị cắt hoặc tràn lề trong phạm vi ảnh đã xem. Các phần khác không được render lại ở lượt biên tập này; audit hình học vẫn kiểm mọi trang PDF.
- Đã mở lại và chạy cùng bộ kiểm tra trên tệp chính sau khi sao chép từ candidate; hash hai tệp trùng nhau.

## Giới hạn thực nghiệm

- **SKIP:** Chưa chạy ví dụ Go trên máy QA này.
- **UNKNOWN:** Không tạo tài nguyên AWS, cluster Kubernetes, Docker Engine hay hệ thống production để xác nhận các tình huống giả định. Kiểm tra cấu trúc claim và neo nguồn không chứng minh độc lập ngữ nghĩa của mọi claim.
- Báo cáo này nêu các phép kiểm đã chạy cho bản PDF chính. Nó không tự thay thế phản biện học thuật hoặc nghiệm thu xuất bản độc lập.
