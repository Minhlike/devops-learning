# NEXT SESSION PLAN

- **Buổi học tiếp theo:** BUỔI 47 — Logging & Centralized Logs (Fluent Bit/Loki).
- **Trạng thái phiên gần nhất:** S46 Grafana Monitoring **COMPLETED — 9.8/10 — PASS**, nghiệm thu ngày 24/10/2026; không tổ chức kiểm tra lại.
- **Chuỗi điểm đã nghiệm thu:** S43 9.3/10; S44 9.6/10; S45 9.7/10; S46 9.8/10.
- **Lab S46:** [`labs/s46-grafana/`](../labs/s46-grafana/) chứa cấu hình Podinfo, Prometheus và Grafana. Dashboard `S46 — K3s Podinfo Monitoring` có 4 panel: Successful Scrape Targets, Scrape Status by Pod, HTTP Requests per Second, HTTP Latency P95.
- **Đánh giá S46:** 7/7 trắc nghiệm (7 điểm), tự luận 2.8/3; tổng 9.8/10. Đã thực hành khắc phục truy cập Grafana liên quan SSH Tunnel và `kubectl port-forward`.
- **Giới hạn ghi nhận:** Bài thực nghiệm chủ động gây lỗi ứng dụng/No Data được người học yêu cầu bỏ. Không ghi nhận đã thực hiện, không tạo bằng chứng giả, không phải điều kiện nghiệm thu.
- **Tồn đọng độc lập:** S40 HPA CPU `<unknown>/50%` chưa xác định root cause; S42 Gateway External LoadBalancer `AddressNotAssigned` trong Kind. Không để các tồn đọng này chặn S47.

## 1. Quy chuẩn giảng dạy

- Dạy lý thuyết, cơ chế và cú pháp lệnh trước khi thực hành từng khái niệm.
- Phân biệt rõ thao tác trên Windows, WSL và Ubuntu Server từ xa; chỉ rõ môi trường chạy lệnh.
- Đi theo trình tự, từng bước nhỏ; có checkpoint hợp lý, đọc và giải thích output thật trước khi kết luận.
- Failure Injection/Troubleshooting chỉ thực hiện khi phù hợp phạm vi và được thống nhất; không tự biến thành điều kiện nghiệm thu bổ sung.
- Chỉ có một bài kiểm tra cuối buổi gồm 7 câu trắc nghiệm và 2 câu tự luận, giới hạn trong kiến thức đã dạy và lab đã làm. Chấm một lượt; không tự tổ chức thi lại.

## 2. Chuẩn bị S47 — Logging & Centralized Logs

- **Mục tiêu dự kiến:** Tìm hiểu luồng thu thập, chuyển tiếp, lưu trữ và truy vấn log tập trung với Fluent Bit/Loki theo Roadmap.
- **Trước khi chốt lab:** Đọc cấu hình và trạng thái mới nhất của môi trường; chọn lab nhỏ, kiểm chứng được bằng output thật, không làm thay đổi tài nguyên đang chạy ngoài phạm vi đã thống nhất.
- **Nhịp triển khai:** Lý thuyết cần thiết → Guided Lab nhỏ → học viên chạy → đọc và giải thích output → checkpoint → troubleshooting phù hợp → bài kiểm tra cuối buổi (7 MCQ + 2 essays).
- **An toàn:** Không xóa cluster, volume, database hay tài nguyên cloud nếu chưa có yêu cầu trực tiếp. Không đưa credentials, private key, Secret thực tế hoặc kubeconfig quản trị vào Git.
