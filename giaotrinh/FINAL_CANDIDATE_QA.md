# Kiểm toán PDF candidate — 2026-10-21

## Phạm vi

- Cây xuất bản: **15 Phần, 58 Chương, 178 Bài**; cả 178 bài có văn bản và trạng thái `reviewed`.
- Hồ sơ migration giữ 88 mục, 216 đoạn, 267 claim, 23 ví dụ và 79 cặp bài tập–đáp án cũ. Khóa ID/URL nguồn không thay đổi.
- 144 bài tập và lời giải dùng cùng số và tiêu đề tiếng Việt dành cho người đọc; ID nội bộ chỉ còn trong manifest và hồ sơ ngoài PDF.

## PDF và điều hướng

- Tệp: `Cam_nang_devops.candidate.pdf`.
- SHA-256: `08f0700dbe5548b43613faa2cb35ca1e0823647e8a32d48615fa69ed230cc3de`.
- **208 trang A4**, **310 bookmark**, 148 liên kết nội bộ, 0 liên kết ngoài. Times New Roman Regular/Bold và Consolas được nhúng. Có thêm Helvetica cho thành phần PDF hệ thống; nội dung sách dùng các font đã quy định.
- Trích xuất 478.389 ký tự, không có ký tự Unicode thay thế. Bộ dựng báo `CANDIDATE_OK pages=208 bookmarks=310 source_leaks=0`.
- Mục lục in liệt kê 15 Phần, 58 Chương và **Lời giải bài tập** với số trang đối chiếu được với bookmark. Bookmark vẫn có cấp Bài; mục lục in giữ hai cấp để người đọc quét nhanh. Tất cả tiêu đề Chương bắt đầu gần đầu trang và running header mang số Chương tương ứng.
- 43 tham chiếu chéo ở 28 vị trí bản thảo dùng ID ngữ nghĩa và được renderer tạo nhãn đọc từ cây xuất bản. Bộ dựng từ chối tham chiếu số chương cũ, ID không tồn tại hoặc ID lệch hợp đồng; ca âm kiểm tra trỏ sang chủ đề sai, thiếu đích và số trang mục lục sai.
- 14 hình cơ chế dạng vector từ `scripts/science_figures.py`, trong đó 10 hình mới có hồ sơ claim, chủ sở hữu, nguồn và giới hạn ở `manuscript/figure_evidence.json`. Cùng với 4 hình Phần XIII, PDF có 18 hình khoa học. Mỗi Phần trước đây không có hình đã được xem xét và thêm một hình có vai trò giải thích cơ chế hoặc suy luận vận hành. Không có quota hình.
- Chương Helm có tiêu đề đọc “Gói Helm (Helm chart) và vòng đời bản phát hành”; cấu trúc tri thức và ID khóa không đổi.

## Kiểm thử và QA hình ảnh

- `python -m unittest discover -s giaotrinh/tests -q`: **43 test, 42 PASS, 1 SKIP** (thiếu Go toolchain). Kiểm thử bao gồm ca âm về tham chiếu, trang mục lục, hình/caption, source leak và hợp đồng bản thảo.
- Đã render **toàn bộ 208 trang** từ PDF cuối và rà 13 contact sheet. Xem chi tiết mục lục trang 2–3, trang bài tập 7, các trang hình/bảng/code tiêu biểu 13, 45, 49, 63, 80, 88, 110, 145, 173, 186; các trang hình bị tác động bởi lần sửa cuối đã được render và xem lại riêng. Contact sheet không bộc lộ tràn lề hoặc hình bị cắt; phép kiểm tự động còn đối chiếu chiều rộng mã, bảng và kích thước trang.
- Một số trang chỉ có bài tập cuối Chương và nhiều chỗ trống, ví dụ trang 7, 34, 40, 83, 89, 103, 115. Đây là hệ quả của việc mở Chương tiếp theo trên trang mới; vẫn là giới hạn biên tập cần cân nhắc ở vòng duyệt bản in, không được mô tả là bố cục đã hoàn hảo.

## Giới hạn và quyết định

- **SKIP:** Ví dụ Go chưa được thực thi ở môi trường QA này.
- **UNKNOWN:** Không chạy AWS, Kubernetes, Docker Engine hoặc host production để xác nhận các tình huống giả định. Validator đối chiếu neo và hồ sơ chứng cứ nhưng không chứng minh độc lập mọi claim kỹ thuật đúng về ngữ nghĩa.
- PDF là **candidate**. Báo cáo này xác nhận các phép kiểm đã chạy và những trang đã xem, không cấp `Publication PASS`, không phát hành chính thức và không merge.
