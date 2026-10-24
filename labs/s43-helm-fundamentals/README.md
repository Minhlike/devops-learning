# Lab S43 — Helm Fundamentals

Thư mục lưu trữ mã nguồn Helm Chart và kịch bản thực hành của Buổi 43: Đóng gói ứng dụng Kubernetes, quản lý cấu hình bằng values/templates, vòng đời Helm Release và Failure Injection Rollback.

## 1. Cấu trúc Chart (`s43-hello`)

```text
labs/s43-helm-fundamentals/
└── s43-hello/
    ├── Chart.yaml                  # Metadata khai báo chart (name, version, appVersion)
    ├── values.yaml                 # Tham số cấu hình mặc định (message, replicas, image, port)
    └── templates/                  # Manifest templates render qua Go template engine
        ├── configmap.yaml          # ConfigMap settings
        ├── deployment.yaml         # Deployment với readiness probe
        └── service.yaml            # ClusterIP Service kết nối Pods
```

## 2. Các Lệnh Thực hành & Kiểm thử Chuẩn

### Kiểm tra cú pháp (Lint)
```bash
helm lint labs/s43-helm-fundamentals/s43-hello
```

### Render Manifest cục bộ (Template)
```bash
helm template s43-demo labs/s43-helm-fundamentals/s43-hello
helm template s43-demo labs/s43-helm-fundamentals/s43-hello --set replicaCount=2 --set message="Override Test"
```

### Triển khai & Cập nhật Release
```bash
# Cài đặt release vào namespace s43
helm install s43-demo labs/s43-helm-fundamentals/s43-hello -n s43 --create-namespace

# Nâng cấp release
helm upgrade s43-demo labs/s43-helm-fundamentals/s43-hello -n s43 --set replicaCount=2

# Xem lịch sử revisions
helm history s43-demo -n s43

# Rollback về revision trước khi gặp sự cố
helm rollback s43-demo 1 -n s43
```

## 3. Tình huống Lỗi Thực hành (Failure Injection)

1. **Sai vị trí file template:** Đặt `configmap.yaml` ở thư mục gốc chart → Helm bỏ qua không render. Khắc phục: chuyển vào `templates/`.
2. **Nâng cấp với Image không tồn tại:** `helm upgrade ... --set image.tag=bad-image-tag-does-not-exist` → Pod mới rơi vào `ImagePullBackOff`. Kubernetes `RollingUpdate` giữ nguyên Pod cũ đang chạy (Zero Downtime).
3. **Rollback khôi phục:** Sử dụng `helm rollback s43-demo <rev> -n s43` đưa hệ thống trở lại trạng thái lành mạnh ngay lập tức.
