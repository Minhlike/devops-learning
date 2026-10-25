# Bản thảo xuất bản theo cây kiến thức

`architecture/knowledge_tree.json` là thứ tự xuất bản của 15 Phần, 59 Chương và 186 Bài. `manifest.json` lưu ID, parent, tiên quyết, trạng thái biên tập, đường dẫn, SHA-256, đơn vị cũ, claim, ví dụ, bài tập và đáp án. Renderer chỉ lấy bài có nội dung từ cây Phần → Chương → Bài; 19 chương cũ là tư liệu đối chứng, không phải cấu trúc xuất bản.

Tại bản này, 186/186 bài có văn bản và được gắn trạng thái `reviewed`: 53 bài có hồ sơ `wave2_evidence.json`, 12 bài Phần XIII có hồ sơ `authoring/P13/`, 113 bài kế thừa có biên bản neo theo nội dung trong `editorial_evidence.json`, và tám bài P15.C04 có hồ sơ nguồn riêng `P15/C04/source_map.json`. Các biên bản ghi rõ nguồn, điểm tựa và giới hạn của những claim đã chọn; kiểm tra tự động chỉ xác nhận tính toàn vẹn của hồ sơ, không chứng minh mọi mệnh đề khoa học đều đúng.

`scripts/migrate_manuscript.py` và ledger trong `architecture/` bảo vệ 88 mục, 216 đoạn split, 267 claim, 23 ví dụ và 79 cặp bài tập–đáp án cũ. `editorial_override=true` ngăn script migration ghi đè bài đã được nâng trạng thái hoặc sửa có chủ đích. `verification=reviewed_baseline_migration` chỉ xác nhận cấu trúc và định danh, chưa nâng nội dung lên `reviewed`. 27 claim và 12 cặp bài tập–đáp án Phần XIII được kiểm riêng trong `authoring/P13/`.

Nguồn và biên bản hỗ trợ claim chỉ ở `source_map.json`, `source_ids.lock.json`, `wave2_evidence.json`, `editorial_evidence.json`, `P15/C04/source_map.json` và các hồ sơ tác giả nằm ngoài PDF. Renderer và kiểm thử chặn URL, mã trích dẫn, bookmark hoặc metadata nguồn tham khảo lọt vào PDF. Các bài có dữ liệu giả định ghi rõ giới hạn của phép tính; kiểm thử không thay thế thử nghiệm trên cluster, cloud hoặc host production.

Để chấp nhận bản phát hành, cần chạy lại toàn bộ regression và kiểm tra hình ảnh mọi trang của candidate cuối. Các ca âm hiện bảo vệ thiếu bài, sai parent, mất claim/ví dụ/đáp án, đổi hash, sai đích bookmark, rò nguồn, mất hình/caption và câu claim bị lặp khi chia bài. Kết quả build xanh chỉ xác nhận hợp đồng tự động đã kiểm; không tự cấp quyền xuất bản. Hồ sơ `qa/P15_C04_QA.md` ghi riêng kiểm tra của chương mới.
