# Kiểm toán bản PDF candidate — 2026-10-21

## Phạm vi và trạng thái

- Cây xuất bản: **15 Phần, 58 Chương, 178 Bài**. Manifest ở phase `complete_scientific_candidate`; 178/178 bài có văn bản và trạng thái `reviewed`.
- Hồ sơ biên tập: 53 bài trong `manuscript/wave2_evidence.json`, 12 bài Phần XIII trong `authoring/P13/`, 113 bài kế thừa trong `manuscript/editorial_evidence.json`. `source_map.json` giữ 267 claim ở trạng thái `verified`; bộ dựng kiểm tra neo, hash nội dung, ID/URL nguồn và nguồn rò. Trạng thái hồ sơ không thay cho việc tự đọc và kiểm chứng ngữ nghĩa mọi mệnh đề.
- Bảo toàn migration: 88 mục, 216 đoạn, 267 claim, 23 ví dụ và 79 cặp bài tập–đáp án cũ theo ledger. Các câu được tách sang bài khác không còn lặp trong đoạn chủ sở hữu ban đầu; ca âm kiểm tra lỗi này.

## PDF cuối

- Tệp: `Cam_nang_devops.candidate.pdf`
- SHA-256: `2353746ffc8834485dfef5149d33fc031b35da67a3032c2bb0156ba33ea3c021`
- 191 trang, tất cả khổ A4; 310 bookmark; Times New Roman Regular/Bold và Consolas được nhúng. Có 146 liên kết nội bộ, **0** liên kết ngoài.
- Trích xuất 472.730 ký tự không có ký tự thay thế Unicode; không có mã citation, mục nguồn hay bibliography. Một URL `https://api.example.test/orders/42` là dữ liệu ví dụ kỹ thuật, không phải tài liệu tham khảo.
- Mục lục in có hai cấp Phần–Chương, đánh số La Mã/toàn sách để đọc, không còn mã `Pxx.Cyy.Lzz` hay 178 Bài chen trong mục lục. Bookmark vẫn đủ ba cấp Phần–Chương–Bài, tên và trang đích được so khớp với cây xuất bản. Nhãn đọc riêng trong `manuscript/reader_titles.json`; ID/URL nguồn và ID migration không đổi. Kiểm thử âm chèn mã nội bộ vào mục lục phải báo lỗi.
- Đủ **144/144 bài tập** có số theo Chương và tên ngắn mô tả đúng câu hỏi, ví dụ “Bài tập 24.2 — Dữ liệu khi đổi image và tên project”. Tên xuất hiện giống nhau ở câu hỏi và lời giải; mã `Pxx.Cyy.Lzz.Qnn` và `C13.x` chỉ còn trong manifest và hồ sơ ngoài PDF. `manuscript/exercise_titles.json` bắt buộc phủ đủ mọi câu; kiểm thử âm xác nhận thiếu tên hoặc mã nội bộ lọt vào PDF đều thất bại.
- Bộ dựng báo `CANDIDATE_OK pages=191 bookmarks=310 source_leaks=0`. Lệnh hồi quy `python -m unittest discover -s giaotrinh/tests -q`: **38 test, 37 PASS, 1 SKIP** (Go toolchain unavailable).

## Kiểm tra hình ảnh

Đã render **toàn bộ 191 trang** của PDF mới và rà 12 contact sheet. Xem chi tiết trang 76 (bài tập người dùng chỉ ra), trang 179 (lời giải tương ứng), trang 140 và 187 (bài tập/lời giải Phần XIII). Nhãn bài tập rõ, câu hỏi không bị cắt, đáp án đối chiếu được theo cùng số/tên. Header của phần lời giải đã được đổi thành “LỜI GIẢI” để trang chứa nhiều chương không mang sai số chương ở đầu trang. Contact sheet không cho thấy lỗi tràn lề rõ; kiểm tra chữ nhỏ và công thức chi tiết vẫn giới hạn ở những trang đã xem riêng.

## Giới hạn và quyết định

- **SKIP:** Ví dụ Go chưa chạy ở môi trường QA này vì thiếu toolchain; các ca Python và phép kiểm tự động còn lại đã chạy.
- **UNKNOWN ngoài phạm vi chạy hiện tại:** Không tạo tài nguyên AWS, cluster Kubernetes, Docker Engine hay host production để chứng minh các ví dụ giả định. Các ví dụ gắn nhãn giả định trong sách không được mô tả là log hoặc phép đo production.
- **Nguồn khoa học:** Biên bản neo theo claim và các review trước hỗ trợ nội dung; kiểm toán tự động không chứng minh toàn bộ 267 claim đúng về ngữ nghĩa trong mọi phiên bản và môi trường. Đây là giới hạn của nghiệm thu độc lập, cần giữ khi quyết định phát hành chính thức.
- **Quyết định:** Lỗi nhãn bài tập người đọc phản ánh đã được sửa trên toàn bộ câu hỏi và lời giải, có kiểm thử ngăn tái diễn. PDF vẫn là candidate; chưa phát hành bản chính thức, chưa merge và chưa tự phê duyệt xuất bản.
