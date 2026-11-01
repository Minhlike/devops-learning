# Backlog có điều kiện nghiệm thu

P0: biên soạn 68 đơn vị DESIGNED còn lại; mỗi bài cần lý thuyết theo mô hình riêng, guided/independent không lộ đáp án, docs theo phiên bản, operational scenario khi cần. Bắt đầu S15 volume/network, rồi S16 resource/probe, S17 artifact. Không dùng các dòng catalog thay cho bài học.

P0: chạy Java Maven tests và hai lab S14 trên môi trường mới được học viên cho phép. Chưa có Maven/Go trong PATH; không sửa hệ thống để giả lập PASS. Khóa digest base image trước bài artifact; hiện Dockerfile dùng tag công khai cho bước đầu, không là reproducible build.

P1: Java business checkpoint: PostgreSQL transaction + idempotency + outbox migration; Go worker claim/ack/idempotent effect với failure tests; Python snapshot export/read-only role. Hiện code mới là checkpoint nền, không phải hệ thống đặt hàng hoàn chỉnh.

P1: render/parse PlantUML bằng tool đã kiểm trong workspace và review notation/semantics; hiện chỉ kiểm cấu trúc tệp, chưa syntax/render PASS. Mapping blueprint CKA/Terraform/AWS còn NOT_MAPPED; phải kiểm nguồn chính thức, ngày/version và phạm vi trước công bố.

P2: thêm CI validator ở workflow chỉ read permission, PR vào main sau review; tuyệt đối không sửa workflow legacy có deploy như một phần refactor này.
