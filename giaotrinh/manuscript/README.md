# Bản thảo xuất bản theo cây kiến thức

`architecture/knowledge_tree.json` là thứ tự xuất bản của 16 Phần, 64 Chương và 202 Bài. `manifest.json` lưu ID, parent, tiên quyết, trạng thái biên tập, đường dẫn, SHA-256, đơn vị cũ, claim, ví dụ, bài tập và đáp án. Renderer chỉ lấy bài có nội dung từ cây Phần → Chương → Bài; 19 chương cũ là tư liệu đối chứng, không phải cấu trúc xuất bản.

Tại bản này, 202/202 bài có văn bản: 178 bài trước P15.C04 giữ hồ sơ hiện có; 24 bài Phần XVI có hồ sơ riêng `P16/source_map.json` và `P16/qa.json`. Tám bài P15.C04 cũ được lưu trong `architecture/history_p15_c04/`, không bị xóa khỏi lịch sử. Các biên bản ghi rõ nguồn, điểm tựa và giới hạn của claim đã chọn; kiểm tra tự động chỉ xác nhận tính toàn vẹn của hồ sơ, không chứng minh mọi mệnh đề khoa học đều đúng.

`scripts/migrate_manuscript.py` và ledger trong `architecture/` bảo vệ 88 mục, 216 đoạn split, 267 claim, 23 ví dụ và 79 cặp bài tập–đáp án cũ. `editorial_override=true` ngăn script migration ghi đè bài đã được nâng trạng thái hoặc sửa có chủ đích. `verification=reviewed_baseline_migration` chỉ xác nhận cấu trúc và định danh, chưa nâng nội dung lên `reviewed`. 27 claim và 12 cặp bài tập–đáp án Phần XIII được kiểm riêng trong `authoring/P13/`.

Nguồn và biên bản hỗ trợ claim chỉ ở `source_map.json`, `source_ids.lock.json`, `wave2_evidence.json`, `editorial_evidence.json`, `P16/source_map.json` và các hồ sơ tác giả nằm ngoài PDF. ID/URL TC-01–TC-09 cũ được giữ nguyên; nguồn mới dùng ID tiếp theo và lock riêng. Renderer và kiểm thử chặn URL, mã trích dẫn, bookmark hoặc metadata nguồn tham khảo lọt vào PDF. Các bài có dữ liệu giả định ghi rõ giới hạn của phép tính; kiểm thử không thay thế thử nghiệm trên cluster, cloud hoặc host production.

Để chấp nhận bản phát hành, cần chạy lại regression và kiểm tra hình ảnh candidate cuối. Các ca âm bảo vệ thiếu bài, sai parent, mất claim/ví dụ/đáp án, đổi hash, sai đích bookmark, rò nguồn và mất hình/caption. Kết quả build xanh chỉ xác nhận hợp đồng tự động đã kiểm; không tự cấp quyền xuất bản. Hồ sơ `qa/P16_QA.md` ghi riêng kiểm tra của Phần XVI.
