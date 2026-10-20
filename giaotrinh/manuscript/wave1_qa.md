# Kiểm toán candidate chuyển cấu trúc — Đợt 1

Candidate: `giaotrinh/Cam_nang_devops.candidate.pdf`
SHA-256: `58c031d3851fd2de0b0c70a535b096f2e6a2f4f9aca4a76d68eb1fa8043d6cdd`

- 160 trang A4; 248 bookmarks gồm 13 Phần, 50 Chương, 136 Bài và mục đáp án. Mục lục in theo cùng thứ tự với bookmarks; kiểm thử đối chiếu đích bookmark với trang thật.
- Times New Roman Regular/Bold và Consolas được nhúng; 0 URI action; bộ kiểm nguồn không phát hiện mã trích dẫn, URL tham khảo, bibliography trong văn bản, bookmark hoặc metadata.
- Renderer kiểm tra bề rộng code, bảng và bounding box văn bản. Bốn hình Phần XIII còn đủ caption và vector; phép thử âm xóa cả hình lẫn caption cuối gây FAIL.
- Đã rasterize toàn bộ 160 trang thành 10 contact sheet, đọc lần lượt các sheet; không thấy trang trắng, mất khối hoặc tràn rõ ở kích thước tổng quan. Kiểm tra thêm 12 trang ở độ phân giải 1,5×, gồm mục lục, code, bảng, hình và đáp án. Chưa chứng nhận typography ở kích thước in trên mọi trang; đây không phải Publication PASS.
- Hồi quy: 28 test `giaotrinh/tests` PASS, 1 SKIP do thiếu Go toolchain; 8 test kiến trúc PASS; 3 test hợp đồng Phần XIII PASS; 10 test fixture toán Phần XIII PASS. Không coi trường hợp Go SKIP là đã thực thi.
- Bảo toàn migration: 88 mục, 216 đơn vị split, 267 claim, 23 ví dụ, 79 cặp đề–đáp án cũ; Phần XIII có 12 bài, 12 cặp đề–đáp án, 27 claim trong ledger riêng. Mã bài tập cũ được giữ trong manifest; 79 mã in sách mới gắn ID bài học và không trùng 12 mã Phần XIII.

Tồn đọng: 41 bài chưa biên soạn, một mảnh `P14.C02.L02` chưa render, Phần XIV/XV và các bài mới cần viết; 11 bài có văn xuôi biên tập mới cần đối chiếu nguồn theo từng claim; kiểm toán ngữ nghĩa toàn sách và thiết kế hình theo storyboard thuộc các đợt tiếp theo. Không phát hành chính thức từ candidate này.
