# Cẩm nang ngành DevOps

Đây là bản thảo có cấu trúc của một giáo trình đang biên soạn. `Cam_nang_devops.candidate.pdf` chỉ là bản đọc thử cho mốc đầu; tên phát hành `Cam_nang_devops.pdf` chỉ được dùng khi toàn bộ mục lục đã có nội dung, lời giải, kiểm toán nguồn và kiểm tra hình học PDF.

## Quy tắc xuất bản

- `chapters/*.md` và `answers.md` là nguồn nội dung. `book_plan.md` ghi kiến trúc sách và phân định nội dung đã học với phần mở rộng. `references.md` ghi nguồn, loại nguồn, phiên bản và ngày truy cập.
- Viết từ cơ chế và quan hệ tiên quyết. Thuật ngữ tiếng Việt tự nhiên, tên API và giao thức giữ nguyên. Không bịa output, benchmark, số liệu hay hành vi theo phiên bản.
- Mỗi hình phải trả lời một câu hỏi kỹ thuật, có nguồn tạo trong thư mục này, kiểm tra nhãn, cạnh, nhánh lỗi và bố cục. Không mượn hình hoặc font từ repo Go.
- Bài tập ở cuối chương, đáp án ở cuối sách. Không áp cấu trúc bài tập cố định. Nội dung chỉ có trong roadmap được ghi là kế hoạch, không được gọi là đã học.
- Kiểm toán nội dung trước khi xuất bản: nguồn chính thức cho khẳng định dễ đổi, đối chiếu lab khi mô tả kết quả thực tế, rà soát bản thảo và hình. PDF cần A4, font nhúng, không tràn lề, bookmark, số trang, liên kết và render kiểm tra trang đại diện.
- Chỉ xuất bản theo mốc có nội dung đủ ý nghĩa. Khi build lỗi, giữ nguyên PDF đang phát hành. Không coi candidate là bản hoàn chỉnh.

## Dựng bản đọc thử

Chạy `python giaotrinh/scripts/build.py` từ gốc repo. Cần Python với `reportlab` và `pymupdf`; Times New Roman và Consolas phải có trên máy dựng. Font được tham chiếu từ hệ điều hành, không đưa vào Git. Lệnh dựng chỉ ghi trong `giaotrinh/`.

## Trạng thái mốc 1

Đã có kiến trúc sách, khảo sát roadmap S01–S66 và chỉ mục học/lab hiện có, bộ benchmark được xác minh, một chương nền tảng và lời giải. Chưa có nội dung cho các chương còn lại; PDF hiện là candidate, chưa được phát hành dưới tên cuối.
