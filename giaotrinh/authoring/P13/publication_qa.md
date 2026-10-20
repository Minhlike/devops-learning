# PDF candidate tích hợp Phần XIII — biên bản QA

Ngày kiểm: 2026-10-20. Đây là **candidate để Reviewer kiểm toán**, không phải PDF phát hành.

- Baseline `d29a740`: 109 trang, 146 bookmark. Candidate: 125 trang A4, 168 bookmark.
- SHA-256 candidate: `6e2a3bbaf4e2368749511d672d93aa2420a7d57883a690e808498a76fc10c22e`.
- Phần XIII mở trang 96. C01 trang 97–99; C02 trang 100–103; C03 trang 104–106; C04 trang 107–109. Lời giải 12 bài tập C13.1–C13.12 ở trang 124–125. Mục lục cấp Phần/Chương/Bài ở trang 5.
- Hình vector PDF: V30/ngân sách và 12 cửa sổ trang 98; incident timeline trang 102; V31/RPO–RTO trang 105; capacity A/B/C trang 108. Mỗi hình có caption, câu dẫn và dữ liệu lấy từ CSV đã qua `verify.py`. Phần XIII không thêm bảng riêng vì bản thảo đã diễn giải số liệu bằng hình và văn bản.
- 27 claim mới vẫn ở 4 ledger `claims.csv` ngoài PDF. Source map cũ giữ 197 ID URL và 267 claim. Bộ dựng kiểm thêm URL từ ledger P13 để ngăn rò nguồn trong text, bookmark, metadata và link tham khảo.
- Bộ dựng kiểm font Times New Roman/Consolas nhúng, A4, vùng an toàn text, 19 chương/79 lời giải cũ, 12 bài/đề/đáp án mới, đích bookmark, caption và đối chiếu từng đoạn văn xuôi bản thảo với PDF.
- `qa_p13_pdf.py` rasterize toàn bộ 125 trang, lưu 16 trang Phần XIII/lời giải ở ảnh 1,4× để xem. Đã xem từng trang này và mục lục trang 2–5; không thấy hình/caption bị cắt, chữ tràn lề hay heading mồ côi trong phạm vi đó. Các trang cũ còn lại được kiểm tự động, chưa được xem từng trang bằng mắt ở lần tích hợp này.
- Giới hạn: fixture là số liệu giả định; không chạy incident, restore, load test hay hệ thống production. Việc rasterize không thay kiểm toán xuất bản độc lập của Reviewer.
