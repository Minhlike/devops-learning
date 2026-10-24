# Kiểm tra bản PDF sau tái biên tập 15 bài Phần XI — 2026-10-25

## Phạm vi và chứng cứ nội dung

- Baseline `1ca48a3bc35e1dd8f5bbef2f4d5ed8454acda099`. Viết lại phần thân 15/15 bài ở `P11.C03`, `C05`, `C06`, `C07`, `C08`; không thay nội dung `P11.C01/C02/C04` hoặc Phần khác.
- Tổng 15 bài: 10.116 → 7.617 từ. Phần giảm là các đoạn nhắc lại; diff cho thấy cơ chế, tình huống và kết luận đều được viết lại. Giữ nguyên ID, 35 neo claim migration, 50 neo editorial, marker code/xref và dữ kiện tính toán. Hợp đồng liên kết chéo được kiểm tra khi dựng.
- Bản thảo vẫn có 15 Phần, 58 Chương, 178 Bài. Nguồn tham khảo chỉ nằm ngoài PDF; không thêm URL/ID nguồn vào bài.

## PDF và kiểm thử

- `Cam_nang_devops.pdf` và `Cam_nang_devops.candidate.pdf` giống byte, SHA-256 `6aefcb35d0f3b601acad1b6d71d971cc48c182d1fef402b612a427ab140025eb`.
- 263 trang A4, 310 bookmark, 0 URI action ngoài, 678.444 ký tự text trích xuất. Times New Roman Regular/Bold và Consolas được nhúng; audit bộ dựng báo `source_leaks=0` trên cả hai PDF.
- Bộ hồi quy: 44 test OK, 1 SKIP (Go toolchain không có trong PATH), 0 FAIL. Bộ dựng và audit đã chạy trên bản thảo cuối.
- Đã render và xem contact sheet toàn bộ trang 151–173 của PDF cuối, xem chi tiết trang 153–154 và trang có code Helm/đoạn kết. Không thấy text, code, công thức bị cắt hoặc tràn; trang lẻ một dòng cuối Chương 38 đã được loại bỏ. Trang kết Chương 42 và 43 còn khoảng trắng do quy tắc mở chương mới ở trang riêng; không thấy mất nội dung.

## Giới hạn

- Các timeline, metric, địa chỉ và revision trong năm chương là ví dụ giả định. Không chạy Kubernetes cluster, CSI driver, Gateway controller hoặc Helm release thật trong lượt biên tập này.
- Chưa kiểm toán độc lập mọi phát biểu của toàn sách hoặc tất cả trang ngoài 151–173. Kết quả này không cấp Publication PASS cho toàn bộ cuốn sách.
