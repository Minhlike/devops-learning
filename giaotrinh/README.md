# Cẩm nang ngành DevOps

`Cam_nang_devops.pdf` là bản PDF chính của giáo trình. Bản thảo xuất bản nằm trong `manuscript/`, theo cây 16 Phần, 64 Chương và 202 Bài. `Cam_nang_devops.candidate.pdf` là tệp dựng trước khi chốt bản chính; hồ sơ Phần XVI nằm trong `qa/P16_QA.md`. `FINAL_CANDIDATE_QA.md` ghi lại một đợt kiểm tra trước đó.

## Quy tắc xuất bản

- `manuscript/` là nguồn xuất bản theo cây Phần → Chương → Bài; `architecture/` giữ kiến trúc tri thức đã duyệt. `chapters/*.md`, `examples/*` và `answers.md` lưu nội dung nền và ví dụ cũ. `references.md`, `source_map.json` và `source_ids.lock.json` chỉ phục vụ kiểm chứng biên tập; không xuất hiện trong PDF. ID nguồn đã dùng giữ nguyên URL; nguồn mới phải thêm ID mới vào bản đồ và lock.
- Viết từ cơ chế và quan hệ tiên quyết. Thuật ngữ tiếng Việt tự nhiên, tên API và giao thức giữ nguyên. Không bịa output, benchmark, số liệu hay hành vi theo phiên bản.
- Mỗi hình phải trả lời một câu hỏi kỹ thuật, có nguồn tạo trong thư mục này, kiểm tra nhãn, cạnh, nhánh lỗi và bố cục. Không mượn hình hoặc font từ repo Go.
- Bài tập có tiêu đề đọc được và lời giải ở cuối sách. Không áp cấu trúc bài tập cố định. Nội dung chỉ có trong roadmap được ghi là kế hoạch, không được gọi là đã học.
- PDF không chứa mã nguồn tham khảo, chú thích nguồn, URL tham khảo, danh mục hoặc phụ lục nguồn. URL thuộc ví dụ kỹ thuật vẫn là nội dung hợp lệ. Bộ dựng và kiểm thử kiểm tra ranh giới này ở văn bản, bookmark, metadata và hyperlink.
- Kiểm toán nội dung trước khi xuất bản: nguồn chính thức cho khẳng định dễ đổi, đối chiếu lab khi mô tả kết quả thực tế, rà soát bản thảo và hình. PDF cần A4, font nhúng, không tràn lề, bookmark, số trang, liên kết và render kiểm tra trang đại diện.
- Chỉ thay bản PDF chính sau khi candidate vượt kiểm thử và kiểm tra trang in. Khi build lỗi, giữ nguyên PDF đang phát hành.

## Dựng PDF candidate

Chạy `python -X utf8 -m giaotrinh.scripts.build` từ gốc repo. Cần Python với `reportlab` và `pymupdf`; Times New Roman và Consolas phải có trên máy dựng. Font được tham chiếu từ hệ điều hành, không đưa vào Git. Lệnh dựng chỉ ghi candidate trong `giaotrinh/`; việc chốt bản chính cần đối chiếu PDF sau khi dựng.

## Trạng thái bản chính

Phần XVI độc lập gồm sáu chương và 24 bài về kiến trúc dự án, hợp đồng giữa công cụ, phát hành một artifact, lựa chọn stack, an toàn vận hành và phương pháp thiết kế dự án mới. Tám bài P15.C04 cũ cùng metadata được lưu trong `architecture/history_p15_c04/` để truy vết, không còn trong cây xuất bản. PDF chính chỉ được thay từ candidate sau khi kiểm tra cấu trúc và trang bị ảnh hưởng; hồ sơ QA ghi rõ phạm vi rà ảnh và giới hạn thực nghiệm. Sự tồn tại của PDF không thay thế đối chiếu khoa học độc lập.
