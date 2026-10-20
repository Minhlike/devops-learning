# Kiểm toán bản PDF candidate — 2026-10-20

## Phạm vi và trạng thái

- Cây xuất bản: **15 Phần, 58 Chương, 178 Bài**. Manifest ở phase `complete_scientific_candidate`; 178/178 bài có văn bản và trạng thái `reviewed`.
- Hồ sơ biên tập: 53 bài trong `manuscript/wave2_evidence.json`, 12 bài Phần XIII trong `authoring/P13/`, 113 bài kế thừa trong `manuscript/editorial_evidence.json`. `source_map.json` giữ 267 claim ở trạng thái `verified`; bộ dựng kiểm tra neo, hash nội dung, ID/URL nguồn và nguồn rò. Trạng thái hồ sơ không thay cho việc tự đọc và kiểm chứng ngữ nghĩa mọi mệnh đề.
- Bảo toàn migration: 88 mục, 216 đoạn, 267 claim, 23 ví dụ và 79 cặp bài tập–đáp án cũ theo ledger. Các câu được tách sang bài khác không còn lặp trong đoạn chủ sở hữu ban đầu; ca âm kiểm tra lỗi này.

## PDF cuối

- Tệp: `Cam_nang_devops.candidate.pdf`
- SHA-256: `38f942c2bfd8f2d91f8230eaa4eb98debb010a9cfc7d000bf165dffe9beded43`
- 193 trang, tất cả khổ A4; 310 bookmark; Times New Roman Regular/Bold và Consolas được nhúng. Có 502 liên kết nội bộ, **0** liên kết ngoài.
- Trích xuất 494.499 ký tự không có ký tự thay thế Unicode; không có mã citation, mục nguồn hay bibliography. Một URL `https://api.example.test/orders/42` là dữ liệu ví dụ kỹ thuật, không phải tài liệu tham khảo.
- Bộ dựng báo `CANDIDATE_OK pages=193 bookmarks=310 source_leaks=0`. Lệnh hồi quy `python -m unittest discover -s giaotrinh/tests -q`: **36 test, 35 PASS, 1 SKIP** (Go toolchain unavailable).

## Kiểm tra hình ảnh

Đã render **toàn bộ 193 trang** của PDF cuối, rà 13 contact sheet. Đã xem chi tiết các trang 13, 14, 23, 34, 41, 54, 55, 74, 95, 106, 112, 114, 115, 122, 127, 132, 136–138, 144, 148, 151 và 153, gồm sơ đồ, bảng, trace, code, công thức và các trang đổi bố cục. Nhãn sơ đồ Terraform trang 95 từng chạm đường nối; đã sửa trong nguồn vector, dựng lại và xem ảnh trang 95. Không thấy cắt chữ, tràn lề, mất caption hoặc lỗi Unicode trong những ảnh đã rà. Contact sheet chỉ phát hiện lỗi bố cục nhìn thấy ở độ thu nhỏ; kiểm tra chi tiết tập trung vào các trang có mật độ và thành phần phức tạp.

## Giới hạn và quyết định

- **SKIP:** Ví dụ Go chưa chạy ở môi trường QA này vì thiếu toolchain; các ca Python và phép kiểm tự động còn lại đã chạy.
- **UNKNOWN ngoài phạm vi chạy hiện tại:** Không tạo tài nguyên AWS, cluster Kubernetes, Docker Engine hay host production để chứng minh các ví dụ giả định. Các ví dụ gắn nhãn giả định trong sách không được mô tả là log hoặc phép đo production.
- **Nguồn khoa học:** Biên bản neo theo claim và các review trước hỗ trợ nội dung; kiểm toán tự động không chứng minh toàn bộ 267 claim đúng về ngữ nghĩa trong mọi phiên bản và môi trường. Đây là giới hạn của nghiệm thu độc lập, cần giữ khi quyết định phát hành chính thức.
- **Quyết định:** Nội dung và bản PDF candidate đã hoàn thành theo hợp đồng tự động và QA hình ảnh ở trên. Chưa phát hành bản chính thức, chưa merge và chưa tự phê duyệt xuất bản.
