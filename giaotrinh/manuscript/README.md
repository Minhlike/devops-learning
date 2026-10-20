# Bản thảo xuất bản theo cây kiến thức

`architecture/knowledge_tree.json` là thứ tự khóa của 15 Phần, 58 Chương và 178 Bài. `manifest.json` lưu ID, parent, tiên quyết, trạng thái biên tập, đường dẫn, SHA-256, đơn vị cũ, claim, ví dụ, bài tập và đáp án. Renderer chỉ lấy bài có nội dung từ cây Phần → Chương → Bài; 19 chương cũ là tư liệu đối chứng, không phải cấu trúc xuất bản.

Tại HEAD này, 178/178 bài có văn bản và đã vào `Cam_nang_devops.candidate.pdf`. Có 80 bài `reviewed`: 53 bài được đối chiếu trong `wave2_evidence.json`, 12 bài Phần XIII đã qua hồ sơ `authoring/P13/`, và 15 bài kế thừa Phần I–II được đối chiếu trong `editorial_evidence.json`. Còn 98 bài `migrated_draft`: nội dung cũ đã được bảo toàn và một số bài đã được biên tập thêm, nhưng trạng thái này **chưa xác nhận kiểm toán ngữ nghĩa đầy đủ theo bài**. Vì vậy PDF vẫn là candidate; không được diễn giải số 178/178 như Publication PASS.

`scripts/migrate_manuscript.py` và ledger trong `architecture/` bảo vệ 88 mục, 216 đoạn split, 267 claim, 23 ví dụ và 79 cặp bài tập–đáp án cũ. `editorial_override=true` ngăn script migration ghi đè bài đã được nâng trạng thái hoặc sửa có chủ đích. `verification=reviewed_baseline_migration` chỉ xác nhận cấu trúc và định danh, chưa nâng nội dung lên `reviewed`. 27 claim và 12 cặp bài tập–đáp án Phần XIII được kiểm riêng trong `authoring/P13/`.

Nguồn và biên bản hỗ trợ claim chỉ ở `source_map.json`, `source_ids.lock.json`, `wave2_evidence.json`, `editorial_evidence.json` và các hồ sơ tác giả nằm ngoài PDF. Renderer và kiểm thử chặn URL, mã trích dẫn, bookmark hoặc metadata nguồn tham khảo lọt vào PDF. Các bài có dữ liệu giả định ghi rõ giới hạn của phép tính; kiểm thử không thay thế thử nghiệm trên cluster, cloud hoặc host production.

Để chấp nhận bản phát hành, cần kiểm toán ngữ nghĩa và biên tập nốt 98 bài `migrated_draft`, chạy lại toàn bộ regression và kiểm tra hình ảnh mọi trang của candidate cuối. Các ca âm hiện bảo vệ thiếu bài, sai parent, mất claim/ví dụ/đáp án, đổi hash, sai đích bookmark, rò nguồn và mất hình/caption. Kết quả build xanh chỉ xác nhận hợp đồng tự động đã kiểm; không tự cấp quyền xuất bản.
