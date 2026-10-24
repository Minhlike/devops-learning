# NEXT SESSION PLAN

- **Buổi học hiện tại / tiếp tục:** BUỔI 46 — Grafana & Practical Dashboards (Hoàn thiện các hạng mục còn lại & Nghiệm thu chính thức).
- **Trạng thái Tiền đề (Prerequisites & State Confirmation):**
  - Buổi 43 (Helm Fundamentals) đã **HOÀN THÀNH (COMPLETED — 9,3/10)** ngày 19/10/2026.
  - Buổi 44 (Kubernetes Troubleshooting & Defense) đã **HOÀN THÀNH (COMPLETED — 9,6/10)** ngày 21/10/2026; mốc tốt nghiệp Phase 9.
  - Buổi 45 (Prometheus Fundamentals & Metrics Collection) đã **HOÀN THÀNH (COMPLETED — 9,7/10)** ngày 21/10/2026.
  - Buổi 46 (Grafana & Practical Dashboards) đang ở trạng thái **IN PROGRESS (22/10/2026)**; hạ tầng VMware K3s và 3 panel cơ bản đã được xác minh thành công.
  - Sự cố tồn đọng độc lập: Buổi 40 HPA CPU `<unknown>/50%` và Buổi 42 Gateway LoadBalancer `AddressNotAssigned` tiếp tục được bảo lưu.
  - Phân định môi trường: Máy ảo VMware Ubuntu Server 26.04.1 (`192.168.210.100`) chạy K3s dành riêng cho S46+; độc lập với cụm Kind `s41` trên WSL2.

---

## 1. 12 QUY CHUẨN GIẢNG DẠY BẮT BUỘC (MANDATORY RULES)

1. **Giảng dạy từ nguyên lý:** Luôn giải thích trực giác, cơ chế hoạt động và kiến trúc hệ thống trước khi thực hành.
2. **Minh bạch câu lệnh:** Mỗi lệnh Linux/Kubernetes/Helm phải được giải thích rõ cú pháp, tham số quan trọng, tác dụng, môi trường thực thi, kết quả mong đợi và rủi ro.
3. **Phân định rõ môi trường thực thi:** Luôn phân biệt rạch ròi giữa Windows CMD/PowerShell, WSL Ubuntu và Ubuntu Server qua SSH; tuyệt đối không trộn lẫn cú pháp.
4. **Không nhồi nhét mã nguồn:** Tuyệt đối không đưa hàng loạt lệnh dài hoặc YAML lớn để học viên sao chép mù quáng mà không hiểu.
5. **Soạn thảo qua công cụ chuẩn (VS Code):** Hướng dẫn học viên dùng VS Code để tạo/sửa file YAML; không ép dùng heredoc trong terminal.
6. **Lab sát thực tế DevOps/SRE:** Bài lab phải có sự cố, điều tra nguyên nhân gốc, đọc logs/events/metrics, sửa lỗi, xác minh và rollback. Tránh tutorial hell.
7. **Phân đoạn theo mốc lớn (Milestone-based):** Chia bài học theo mốc lớn, có mục tiêu, vị trí hiện tại và tiêu chí hoàn thành; không chia vụn vặt vô nghĩa.
8. **Yêu cầu bằng chứng tại Checkpoint:** Không đòi hỏi nộp ảnh/output sau từng thao tác nhỏ; chỉ yêu cầu bằng chứng tại các checkpoint quan trọng.
9. **Duy nhất một bài kiểm tra cuối buổi:** Đúng 7 câu trắc nghiệm + 2 câu tự luận, nội dung nằm trong buổi học. Không gợi ý trước đáp án, không kiểm tra lặp lại khi đã đạt.
10. **Ngôn ngữ chuẩn xác, có chiều sâu:** Viết bằng tiếng Việt tự nhiên, chuẩn xác, có chiều sâu kỹ thuật; không sáo rỗng, không nhồi thuật ngữ tiếng Anh bừa bãi.
11. **Ghi nhận Checkpoint khi tạm dừng:** Ghi nhận chính xác checkpoint và công việc còn lại để tiếp tục liền mạch, không bắt học viên làm lại từ đầu.
12. **Tối ưu tài nguyên máy tính:** Tôn trọng tài nguyên laptop; ưu tiên giải pháp gọn nhẹ, không cài thêm thành phần không cần thiết.

---

## 2. Các Hạng mục Tiếp tục Thực hiện của Buổi 46

1. **Checkpoint Đã hoàn thành (Ngày 22/10/2026):**
   - VM Ubuntu Server 26.04.1 (192.168.210.100), LVM mở rộng, SSH Hardening, tắt swap.
   - Cụm K3s v1.36.5+k3s1 node Ready, Helm v4.3.1.
   - Release Podinfo v6.15.0, 2 replicas, NodePort 31198 (namespace staging); rolling update và rollback thành công (rev 4).
   - Prometheus server PVC 2Gi local-path, scrape config tự động phát hiện Podinfo (`UP=1`).
   - Grafana PVC 1Gi local-path, kết nối Data Source `Prometheus-S46`.
   - Dashboard `S46 — K3s Podinfo Monitoring` với 3 Panel:
     - Panel 1: *Successful Scrape Targets* (`sum(up{job="podinfo"})`)
     - Panel 2: *Scrape Status by Pod* (`up{job="podinfo"}`)
     - Panel 3: *HTTP Requests per Second* (`sum(rate(http_requests_total{job="podinfo"}[1m]))`)

2. **Nhiệm vụ Còn lại Cần Hoàn thiện:**
   - **Thêm Panel 4: HTTP Latency P95:**
     - Query PromQL: `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{job="podinfo"}[1m])) by (le))`
     - Cấu hình format đơn vị giây (seconds/milliseconds), trực quan hóa phân vị trễ của ứng dụng dưới tải.
   - **Thực nghiệm Sự cố Ứng dụng & Hiện tượng No Data:**
     - Tận dụng endpoints `/faults` của Podinfo hoặc scale Deployment về 0 replicas.
     - Quan sát biến động trên Grafana: Panel Scrape Status chuyển sang 0 (Down), panel RPS rớt về 0 hoặc hiển thị No Data.
     - Khôi phục ứng dụng và chứng minh hệ thống phục hồi metric tự động.
   - **Bài kiểm tra Chuẩn hóa Cuối Buổi S46:**
     - Duy nhất 1 bài kiểm tra: 7 câu trắc nghiệm + 2 câu tự luận (về PromQL Histogram, Grafana Dashboards as Code, Alerting concepts).
     - Đánh giá và ghi nhận điểm số chính thức.
   - **Nghiệm thu S46 & Chuyển tiếp S47:**
     - Cập nhật hồ sơ hoàn thành S46 khi đạt điểm pass.
     - Chuẩn bị Buổi 47: Centralized Logging (Fluentbit / Loki / Promtail).
