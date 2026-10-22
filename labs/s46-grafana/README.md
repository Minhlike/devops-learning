# Lab S46 — Grafana & Practical Dashboards (K3s Staging)

Thư mục cấu hình cho Buổi 46: Trực quan hóa dữ liệu giám sát với Grafana, tích hợp Prometheus Data Source và xây dựng Dashboard theo dõi ứng dụng thực tế trên cụm K3s (máy ảo VMware Ubuntu Server 26.04.1).

## 1. Môi trường Thực thi & Kiến trúc Hạ tầng

- **Máy chủ ảo (VMware):** Ubuntu Server 26.04.1 LTS, IP cố định `192.168.210.100`.
- **Hạ tầng hệ thống:** LVM mở rộng, SSH Hardening (khóa xác thực SSH key, bảo mật port), swapoff hoàn toàn.
- **Cụm Kubernetes:** K3s `v1.36.5+k3s1` (Control plane/worker tích hợp), StorageClass `local-path`, Metrics Server sẵn sàng.
- **Công cụ quản lý gói:** Helm CLI v4.3.1.
- **Phân định rõ ràng:** Môi trường K3s VMware phục vụ chuỗi bài Observability từ S46, hoàn toàn độc lập với cụm Kind `s41` trên WSL2.

## 2. Cấu trúc Thành phần Lab (`labs/s46-grafana/`)

```text
labs/s46-grafana/
├── podinfo/
│   └── podinfo-values.yaml     # Release Podinfo v6.15.0, 2 replicas, NodePort 31198 (namespace staging)
├── prometheus/
│   └── prometheus-values.yaml  # Prometheus server (PVC 2Gi local-path, scrape config tự động phát hiện Podinfo)
├── grafana/
│   └── grafana-values.yaml     # Grafana instance (PVC 1Gi local-path, kết nối Prometheus-S46 datasource)
└── README.md                   # Tài liệu tiến độ và hướng dẫn bài lab
```

## 3. Tiến độ Triển khai Hiện tại (22/10/2026)

- [x] **Hạ tầng OS & K3s:** Dựng VM, SSH, LVM, tắt swap, bootstrap cụm K3s node Ready.
- [x] **Podinfo Staging:** Triển khai Helm release Podinfo, 2 replicas, NodePort 31198; thực hành Rolling Update và Rollback thành công (Revision 4).
- [x] **Prometheus Scrape:** Triển khai Prometheus server với PVC 2 GiB `local-path`; cấu hình `kubernetes_sd_configs` lọc pod `podinfo-.*` cổng `9797`; xác minh 2 targets đều đạt `UP=1`.
- [x] **Grafana & Data Source:** Triển khai Grafana PVC 1 GiB; kết nối thành công Data Source `Prometheus-S46`.
- [x] **Dashboard Panels (3/4 hoàn tất):**
  1. `Successful Scrape Targets`: `sum(up{job="podinfo"})`
  2. `Scrape Status by Pod`: `up{job="podinfo"}`
  3. `HTTP Requests per Second`: `sum(rate(http_requests_total{job="podinfo"}[1m]))`
- [ ] **Công việc còn lại:**
  1. Xây dựng Panel đo HTTP Latency P95: `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[1m])) by (le))`.
  2. Thực nghiệm kịch bản sự cố (Fault injection: delay/error/unhealthy trên Podinfo) và quan sát hiện tượng No Data / Target Down.
  3. Tổ chức bài kiểm tra chuẩn hóa cuối buổi S46 (7 trắc nghiệm + 2 tự luận) và nghiệm thu chính thức.
