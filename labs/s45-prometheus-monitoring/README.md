# Lab S45 — Prometheus Fundamentals & Metrics Collection

Thư mục cấu hình và bài thực hành Buổi 45: Hệ thống giám sát Prometheus, thu thập metrics theo mô hình Pull, PromQL cơ bản và đo lường tài nguyên workload Kubernetes.

## 1. Cấu trúc Thư mục Lab

```text
labs/s45-prometheus-monitoring/
├── prometheus-values.yaml      # Cấu hình Helm triển khai Prometheus lightweight (tắt thành phần thừa, tối ưu RAM)
├── cpu-demo.yaml               # Pod tạo tải CPU 3 pha (IDLE -> STRESS -> RECOVERY) phục vụ truy vấn PromQL
└── README.md                   # Tài liệu hướng dẫn và ghi nhận bài lab
```

## 2. Các Khái niệm & Kỹ năng Trọng tâm

- **Mô hình Pull Model:** Prometheus chủ động gửi HTTP GET request định kỳ (`scrape_interval: 15s`) đến endpoint `/metrics` của target.
- **TSDB (Time Series Database):** Dữ liệu chuỗi thời gian được lưu dưới dạng metric name, tập nhãn (labels `key=value`), timestamp và numeric value.
- **4 Kiểu Metric Chuẩn:**
  1. `Counter`: Chỉ tăng hoặc reset về 0 (ví dụ `http_requests_total`).
  2. `Gauge`: Tăng giảm tự do (ví dụ `node_memory_Active_bytes`, CPU usage).
  3. `Histogram`: Đếm số lượng mẫu rơi vào các bucket định sẵn (`_bucket`, `_sum`, `_count`).
  4. `Summary`: Tương tự histogram nhưng tính sẵn quantile ở phía client.
- **Truy vấn PromQL Cơ bản:**
  - Kiểm tra trạng thái target: `up{job="prometheus"}`
  - Tính tốc độ tăng: `rate(container_cpu_usage_seconds_total[1m])`
  - Nhóm theo nhãn: `sum by (pod) (rate(container_cpu_usage_seconds_total[1m]))`

## 3. Triển khai & Kiểm thử

```bash
# Triển khai Prometheus server lightweight bằng Helm
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/prometheus -n s45 --create-namespace -f prometheus-values.yaml

# Khởi tạo workload sinh tải CPU
kubectl apply -f cpu-demo.yaml -n s45

# Port-forward giao diện web Prometheus
kubectl port-forward svc/prometheus-server 9090:80 -n s45
```
