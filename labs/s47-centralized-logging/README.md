# S47 — Logging & Centralized Logs

**Trạng thái:** COMPLETED — PASS — **9.8/10**
**Ngày nghiệm thu:** 24/10/2026

## Kiến trúc và phạm vi đã thực hành

- Hạ tầng K3s một node trên Ubuntu Server trong VMware; giữ nguyên Prometheus và Grafana từ S46.
- Loki Helm chart `19.2.0` / app `3.7.9`, chế độ Monolithic, StatefulSet `1/1`, PVC `2Gi` qua `local-path`.
- Fluent Bit Helm chart `0.58.3` / app `5.1.3`, DaemonSet đọc container logs của Podinfo namespace `staging` và gửi chúng đến `s47-loki.monitoring.svc.cluster.local:3100`.
- Thực hành LogQL, truy vấn log và `count_over_time`; thêm Loki datasource vào Grafana.

## Bằng chứng và kết quả

- Loki API truy vấn thành công và trả về 4 bản ghi log Podinfo.
- Grafana Explore hiển thị các log tương ứng; truy vấn `count_over_time` được kiểm chứng.
- Prometheus/Grafana từ S46 được bảo toàn.
- Nghiệm thu duy nhất cuối buổi: 7/7 câu trắc nghiệm, tự luận 2.8/3; tổng **9.8/10 — PASS**. Không thi lại.

## Giới hạn đã ghi nhận

- `local-path` chỉ lưu trên một node; cấu hình này chưa có HA hoặc backup.
- Fluent Bit sử dụng buffer không có lưu trữ bền vững.

## Cấu hình

- [`loki-values.yaml`](loki-values.yaml): Loki Monolithic, PVC và giới hạn tài nguyên.
- [`fluent-bit-values.yaml`](fluent-bit-values.yaml): tail log Podinfo staging và output Loki.

Đây là cấu hình lab đã có trong workspace. Không kèm ảnh chụp hoặc log dump; kết quả được ghi theo dữ liệu nghiệm thu đã cung cấp.
