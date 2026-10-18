# Cẩm nang ngành DevOps

Đây là bản thảo có cấu trúc của một giáo trình đang biên soạn. `Cam_nang_devops.candidate.pdf` chỉ là bản đọc thử cho mốc đầu; tên phát hành `Cam_nang_devops.pdf` chỉ được dùng khi toàn bộ mục lục đã có nội dung, lời giải, kiểm toán nguồn và kiểm tra hình học PDF.

## Quy tắc xuất bản

- `chapters/*.md`, `examples/*` và `answers.md` là nguồn nội dung. `book_plan.md` ghi kiến trúc sách và phân định nội dung đã học với phần mở rộng. `references.md` và `source_map.json` chỉ phục vụ kiểm chứng biên tập; không xuất hiện trong PDF.
- Viết từ cơ chế và quan hệ tiên quyết. Thuật ngữ tiếng Việt tự nhiên, tên API và giao thức giữ nguyên. Không bịa output, benchmark, số liệu hay hành vi theo phiên bản.
- Mỗi hình phải trả lời một câu hỏi kỹ thuật, có nguồn tạo trong thư mục này, kiểm tra nhãn, cạnh, nhánh lỗi và bố cục. Không mượn hình hoặc font từ repo Go.
- Bài tập ở cuối chương, đáp án ở cuối sách. Không áp cấu trúc bài tập cố định. Nội dung chỉ có trong roadmap được ghi là kế hoạch, không được gọi là đã học.
- PDF không chứa mã nguồn tham khảo, chú thích nguồn, URL tham khảo, danh mục hoặc phụ lục nguồn. URL thuộc ví dụ kỹ thuật vẫn là nội dung hợp lệ. Bộ dựng và kiểm thử kiểm tra ranh giới này ở văn bản, bookmark, metadata và hyperlink.
- Kiểm toán nội dung trước khi xuất bản: nguồn chính thức cho khẳng định dễ đổi, đối chiếu lab khi mô tả kết quả thực tế, rà soát bản thảo và hình. PDF cần A4, font nhúng, không tràn lề, bookmark, số trang, liên kết và render kiểm tra trang đại diện.
- Chỉ xuất bản theo mốc có nội dung đủ ý nghĩa. Khi build lỗi, giữ nguyên PDF đang phát hành. Không coi candidate là bản hoàn chỉnh.

## Dựng bản đọc thử

Chạy `python giaotrinh/scripts/build.py` từ gốc repo. Cần Python với `reportlab` và `pymupdf`; Times New Roman và Consolas phải có trên máy dựng. Font được tham chiếu từ hệ điều hành, không đưa vào Git. Lệnh dựng chỉ ghi trong `giaotrinh/`.

## Trạng thái mốc 1

Đã có kiến trúc sách, khảo sát roadmap S01–S66 và chỉ mục học/lab hiện có, bộ benchmark được xác minh, mười chương nền tảng và lời giải. Chương 2 có ví dụ tính toán được gắn nhãn giả định; Chương 3 có unit minh họa; Chương 4 lần theo một kết nối IPv4/TCP qua gateway và NAT; Chương 5 theo yêu cầu từ DNS tới proxy/upstream với trace HTTP hai chặng; Chương 6 giải thích Git bằng object, index và commit graph có conflict; Chương 7 dùng thử nghiệm cô lập để phân tích backup báo thành công giả và sửa đường lỗi Bash; Chương 8 so sánh Python và Go qua một chuỗi tác vụ giả có status lỗi, timeout và trạng thái từng phần; Chương 9 theo một artifact từ commit tới triển khai và phục hồi, có sự cố dữ liệu giả định để phân biệt rollback ứng dụng với sửa dữ liệu; Chương 10 phân biệt namespace, cgroup và image qua dữ liệu chẩn đoán giả định có thể tính lại. Chưa có nội dung cho các chương còn lại; PDF hiện là candidate, chưa được phát hành dưới tên cuối.
