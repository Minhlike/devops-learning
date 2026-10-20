# Bản thảo xuất bản theo cây kiến thức

`architecture/knowledge_tree.json` quyết định thứ tự Phần → Chương → Bài. `manifest.json` lưu ID ổn định, parent, tiên quyết, trạng thái, tệp nội dung, hash, đơn vị cũ, claim, ví dụ, bài tập và đáp án. Renderer chỉ đưa bài `migrated_draft` hoặc `reviewed` có nội dung vào PDF candidate. Chương và Phần chưa có bài đủ nội dung không được dựng thành trang giả.

Đợt 1 đã đưa nội dung từ 19 chương cũ vào 137 tệp bài học. Trong đó 136 bài là draft có nội dung; một mảnh `P14.C02.L02` được bảo toàn ngoài PDF để chờ biên soạn Phần XIV. Còn 41 bài chưa có nội dung. Candidate hiện trình bày 13 Phần, 50 Chương, 136 Bài trên 160 trang, cùng 79 cặp đề–đáp án cũ và 12 cặp Phần XIII. Đây là mốc chuyển cấu trúc, **không phải sách hoàn chỉnh 15/58/178 hoặc Publication PASS**.

`scripts/migrate_manuscript.py` chuyển nội dung theo `legacy_migration.csv`, kiểm hash của 216 đoạn split và giữ nguồn cũ làm đối chứng. Các đoạn chứa claim của nhiều bài được giữ nguyên ở chủ đoạn; câu chứa claim còn được trích sang chủ claim theo ledger. Những câu trích này cần biên tập liên kết ngữ cảnh ở đợt sau. `editorial_override=true` bảo vệ 11 bài đã được viết nối hoặc viết mới trong đợt này; script từ chối ghi đè khi hash thay đổi ngoài manifest.

`verification=reviewed_baseline_migration` chỉ nghĩa là đơn vị cũ đã được đối chiếu cấu trúc và định danh với ledger; không xác nhận toàn bộ phát biểu trong bài đã được kiểm chứng ngữ nghĩa mới. `verification=editorial_synthesis_pending_source_review` đánh dấu 11 bài có phần văn xuôi mới cần đối chiếu nguồn trước khi đổi sang trạng thái `reviewed`. Bản đồ nguồn và 27 claim Phần XIII vẫn tách ngoài PDF. Không thêm URL tham khảo vào sách.

Kiểm thử Đợt 1 bảo vệ 88 mục, 216 đoạn split, 267 claim, 23 ví dụ, 79 cặp cũ, 12 cặp Phần XIII, parent, tệp, hash, thứ tự bookmark và đích trang. Các ca âm cố ý làm thiếu bài, sai parent, mất claim/ví dụ/đáp án, đổi hash và chuyển bookmark sang trang khác. PDF candidate cần build lại sau mỗi thay đổi nội dung; không coi một lần build thành công là nghiệm thu nội dung hay dàn trang ở kích thước in.
