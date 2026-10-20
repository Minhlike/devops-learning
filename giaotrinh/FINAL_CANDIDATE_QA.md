# Kiểm toán bản PDF candidate — 2026-10-20

## Phạm vi và trạng thái

- Cây xuất bản: **15 Phần, 58 Chương, 178 Bài**. Manifest ở phase `complete_scientific_candidate`; 178/178 bài có văn bản và trạng thái `reviewed`.
- Hồ sơ biên tập: 53 bài trong `manuscript/wave2_evidence.json`, 12 bài Phần XIII trong `authoring/P13/`, 113 bài kế thừa trong `manuscript/editorial_evidence.json`. `source_map.json` giữ 267 claim ở trạng thái `verified`; bộ dựng kiểm tra neo, hash nội dung, ID/URL nguồn và nguồn rò. Trạng thái hồ sơ không thay cho việc tự đọc và kiểm chứng ngữ nghĩa mọi mệnh đề.
- Bảo toàn migration: 88 mục, 216 đoạn, 267 claim, 23 ví dụ và 79 cặp bài tập–đáp án cũ theo ledger. Các câu được tách sang bài khác không còn lặp trong đoạn chủ sở hữu ban đầu; ca âm kiểm tra lỗi này.

## PDF cuối

- Tệp: `Cam_nang_devops.candidate.pdf`
- SHA-256: `8610751ee1281692a996a3ebe5eb3f9c9bd43f1b983956381fc3986307bb2f47`
- 188 trang, tất cả khổ A4; 310 bookmark; Times New Roman Regular/Bold và Consolas được nhúng. Có 146 liên kết nội bộ, **0** liên kết ngoài.
- Trích xuất 464.619 ký tự không có ký tự thay thế Unicode; không có mã citation, mục nguồn hay bibliography. Một URL `https://api.example.test/orders/42` là dữ liệu ví dụ kỹ thuật, không phải tài liệu tham khảo.
- Mục lục in có hai cấp Phần–Chương, đánh số La Mã/toàn sách để đọc, không còn mã `Pxx.Cyy.Lzz` hay 178 Bài chen trong mục lục. Bookmark vẫn đủ ba cấp Phần–Chương–Bài, tên và trang đích được so khớp với cây xuất bản. Nhãn đọc riêng trong `manuscript/reader_titles.json`; ID/URL nguồn và ID migration không đổi. Kiểm thử âm chèn mã nội bộ vào mục lục phải báo lỗi.
- Bộ dựng báo `CANDIDATE_OK pages=188 bookmarks=310 source_leaks=0`. Lệnh hồi quy `python -m unittest discover -s giaotrinh/tests -q`: **37 test, 36 PASS, 1 SKIP** (Go toolchain unavailable).

## Kiểm tra hình ảnh

Đã render **toàn bộ 188 trang** của PDF mới, rà 12 contact sheet và xem chi tiết hai trang mục lục 2–3 ở độ phân giải in. Các trang 2–3 có phân cấp Phần in đậm, Chương thụt vào, số trang và dấu dẫn rõ; trang 3 có nhãn “Mục lục · tiếp”. Không thấy mã nội bộ, dòng bị cắt hay mục lục dư một trang gần trống. Đã rà contact sheet của toàn bộ phần thân, lời giải, hình, bảng và mã; không thấy tràn lề rõ ở độ thu nhỏ. Những trang nội dung đã được xem chi tiết ở vòng QA trước không được tái kiểm từng trang trong vòng sửa mục lục này; thay đổi hiện tại tác động đến nhãn heading và phân trang.

## Giới hạn và quyết định

- **SKIP:** Ví dụ Go chưa chạy ở môi trường QA này vì thiếu toolchain; các ca Python và phép kiểm tự động còn lại đã chạy.
- **UNKNOWN ngoài phạm vi chạy hiện tại:** Không tạo tài nguyên AWS, cluster Kubernetes, Docker Engine hay host production để chứng minh các ví dụ giả định. Các ví dụ gắn nhãn giả định trong sách không được mô tả là log hoặc phép đo production.
- **Nguồn khoa học:** Biên bản neo theo claim và các review trước hỗ trợ nội dung; kiểm toán tự động không chứng minh toàn bộ 267 claim đúng về ngữ nghĩa trong mọi phiên bản và môi trường. Đây là giới hạn của nghiệm thu độc lập, cần giữ khi quyết định phát hành chính thức.
- **Quyết định:** Lỗi mục lục người đọc phản ánh đã được sửa và có ca kiểm thử ngăn tái diễn. PDF vẫn là candidate; chưa phát hành bản chính thức, chưa merge và chưa tự phê duyệt xuất bản.
