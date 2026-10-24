# NEXT SESSION PLAN

- **Buổi tiếp theo:** S49 — SLI, SLO & Error Budget.
- **Trạng thái:** NEXT / THEORY INTRODUCED. Đã giới thiệu SLI, SLO, Error Budget và ví dụ mục tiêu SLO 99.9%; chưa thực hiện lab, truy vấn metric thực tế, tính Error Budget/Burn Rate hoặc nghiệm thu.
- **Chuỗi kết quả đã nghiệm thu:** S43 9.3/10; S44 9.6/10; S45 9.7/10; S46 9.8/10; S47 9.8/10; S48 10/10 — đều COMPLETED.
- **S47:** COMPLETED — 9.8/10 — PASS ngày 24/10/2026. Loki Monolithic + Fluent Bit DaemonSet gom log Podinfo namespace `staging`; Loki API trả 4 log và Grafana Explore hiển thị log tương ứng. Loki dùng local-path single-node, chưa HA/backup; Fluent Bit buffer chưa persistent. Cấu hình được lưu trong [`labs/s47-centralized-logging/`](../labs/s47-centralized-logging/).
- **S48:** COMPLETED — 10/10 — PASS ngày 24/10/2026. Đã xác minh alert Pending → Firing, Alertmanager active, routing/grouping, silence, inhibition và webhook HTTP 200. Rule/receiver thử nghiệm đã cleanup; Prometheus trả `[]`, Alertmanager config CLEAN, webhook listener đã dừng. Cấu hình có thể truy xuất lưu tại [`labs/s48-alerting/`](../labs/s48-alerting/); file webhook listener và cấu hình endpoint nguyên bản không lấy được do SSH tới Ubuntu Server timeout, không dựng file thay thế.
- **Tồn đọng độc lập:** S40 HPA CPU `<unknown>/50%` chưa rõ root cause; S42 Gateway LoadBalancer `AddressNotAssigned` trong Kind; S46 failure injection No Data đã được người học yêu cầu bỏ. Các nội dung này không chặn S49.

## Kế hoạch S49

1. Giới thiệu lại cơ chế SLI, SLO, Error Budget và Burn Rate trước khi thao tác; giải thích PromQL và nơi chạy từng lệnh trên Windows, WSL hoặc Ubuntu Server.
2. Khảo sát các HTTP metrics thực sự đang có trong Prometheus; chọn SLI từ dữ liệu quan sát được, không giả định tên metric hoặc kết quả.
3. Xây dựng truy vấn PromQL cho tỷ lệ request thành công, đối chiếu với mục tiêu SLO ví dụ 99.9%, rồi tính Error Budget và Burn Rate trên cửa sổ thời gian có dữ liệu.
4. Thực hành theo checkpoint nhỏ, đọc output thật và giải thích kết quả trước khi kết luận.
5. Tổ chức duy nhất một bài nghiệm thu cuối buổi gồm 7 câu trắc nghiệm và 2 câu tự luận; không kiểm tra lại ngoài yêu cầu của người học.

**S50:** Incident Response & Runbooks — UPCOMING.
