# S48 — Alerting

**Trạng thái:** COMPLETED — PASS — **10/10**
**Ngày nghiệm thu:** 24/10/2026

## Kiến trúc

S48 mở Alertmanager trong Helm release Prometheus `s46-prometheus` (chart Prometheus `29.36.1`) trên cụm K3s đã dùng cho S46–S47. Alertmanager chạy StatefulSet `1/1`, Pod `2/2`, PVC `256Mi` qua `local-path`. Prometheus discovery nhận diện endpoint Alertmanager active.

Prometheus phát alert rules; Alertmanager xử lý trạng thái, receiver, routing, grouping, silence, inhibition và gửi notification HTTP webhook. Các overlay cấu hình tham khảo nằm trong thư mục này; baseline Prometheus được lưu tại [`../s46-grafana/prometheus/prometheus-values.yaml`](../s46-grafana/prometheus/prometheus-values.yaml).

## Các bước đã nghiệm thu

1. Phát hiện `alertmanager.enabled: false` trong Helm values và bổ sung Alertmanager.
2. Xác minh StatefulSet/Pod/PVC và Prometheus discovery endpoint active.
3. Tạo `S48TrainingAlert` với biểu thức `vector(1)`, `for: 1m`; quan sát `Pending → Firing` và trạng thái active trên Alertmanager.
4. Thực hành receiver `s48-lab`, routing theo nhãn `session`, grouping theo `session`, tạo Silence và xác minh `state: suppressed` cùng `silencedBy` ID.
5. Tạo `S48ParentAlert`, kiểm chứng inhibition: alert con `suppressed` và `inhibitedBy` có ID.
6. Kiểm chứng HTTP webhook notification: `S48ParentAlert` lúc 13:29:48 và `S48TrainingAlert` lúc 13:31:14 được gửi đến receiver `s48-lab`, HTTP 200.
7. Troubleshoot Helm upgrade đã cập nhật ConfigMap nhưng tiến trình chưa reload cấu hình; dùng `kubectl rollout restart` cho workload liên quan rồi xác minh lại.
8. Cleanup rules, receiver, routing, inhibition và webhook thử nghiệm; giữ Alertmanager, các dịch vụ monitoring và PVC.

Lần gửi alert con gần thời điểm Alertmanager restart không được xem là bằng chứng inhibition thất bại. Trạng thái sau đó xác nhận alert con `suppressed` với `inhibitedBy` có giá trị.

## Kết quả cuối và đánh giá

Sau cleanup, Prometheus `/api/v1/rules?type=alert` trả `[]`, kiểm tra cấu hình Alertmanager báo `CLEAN`, và webhook listener đã dừng. Không còn alerting rule thử nghiệm.

Bài nghiệm thu duy nhất: 7/7 trắc nghiệm; tự luận câu 8 đạt 1.5/1.5 và câu 9 đạt 1.5/1.5; tổng **10/10 — PASS**. Không thi lại.

## Cấu hình có trong repository

- [`alertmanager-values.yaml`](alertmanager-values.yaml): bật Alertmanager, PVC và resources.
- [`s48-rule-values.yaml`](s48-rule-values.yaml): rule huấn luyện `vector(1)`.
- [`s48-routing-values.yaml`](s48-routing-values.yaml): routing/grouping/inhibition tham khảo.

File cấu hình baseline, notification webhook và webhook listener nguyên bản nằm trên Ubuntu Server nhưng không truy xuất được trong phiên cập nhật này do SSH tới `192.168.210.100` timeout. Các file trên là cấu hình thực có sẵn tại workspace; không tạo file listener hoặc endpoint thay thế và không ghi credentials. Bằng chứng trên là kết quả nghiệm thu được cung cấp, không có ảnh chụp hay log dump được thêm vào repository.
