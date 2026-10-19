# NEXT SESSION PLAN

- **Buổi học tiếp theo:** BUỔI 44 — Kubernetes Troubleshooting & Defense (Mốc kết thúc Phase 9 trước khi sang Observability S45 Prometheus & S46 Grafana).
- **Trạng thái Tiền đề (Prerequisites & State Confirmation):**
  - Buổi 43 (Helm Fundamentals: Chart Anatomy, Values Override, Install, Upgrade, Rollback, RollingUpdate Resilience) đã **HOÀN THÀNH (COMPLETED — LEARNING & ASSESSMENT PASS: 9,3/10)** ngày 19/10/2026.
  - Buổi 42 (Kubernetes Gateway API & Application Exposure) đã **HOÀN THÀNH (COMPLETED / PASS: 7,7/10)** ngày 15/10/2026; tồn đọng Gateway External LoadBalancer provisioning (`AddressNotAssigned`) tiếp tục được bảo lưu.
  - Buổi 41 (Kubernetes Storage: Volumes, PV, PVC, StorageClass, StatefulSet, PostgreSQL 16) đã **HOÀN THÀNH (COMPLETED / PASS)**; dữ liệu PostgreSQL và PVC được bảo toàn nguyên vẹn.
  - Buổi 40 (Kubernetes Resources, Scheduling & Scaling) tiếp tục giữ trạng thái **IN PROGRESS / PARTIALLY VERIFIED** do sự cố HPA CPU: `<unknown>/50%` nằm trong backlog độc lập. Cụm Kind `s40` và `s41` được giữ nguyên tài nguyên.
  - Lộ trình Roadmap chính thức: Hoàn thành buổi Kubernetes cuối cùng (**S44 K8s Troubleshooting & Defense**) trước khi bước sang Observability (**S45 Prometheus, S46 Grafana**).

---

## 1. YÊU CẦU SƯ PHẠM MỚI (BẮT BUỘC ÁP DỤNG TỪ BUỔI 44)
*(Học viên yêu cầu: Mọi thuật ngữ hạ tầng phải được gắn với đối tượng vật lý hoặc logic thực tế)*

Mỗi khi giới thiệu một khái niệm hoặc thuật ngữ mới, Agent bắt buộc giải thích theo 4 câu hỏi định vị:
1. **Nó đại diện cho thành phần gì trong hệ thống thật?** (Tiến trình OS, file trên đĩa, bản ghi etcd, network socket, v.v.).
2. **Nó nằm/chạy ở đâu?** (Máy vật lý host, máy ảo WSL, Worker Node, Control Plane Node, Pod, Container, hay chỉ là tài nguyên logic trên Kubernetes API Server).
3. **Thành phần nào tạo ra, quản lý và giám sát nó?** (kubelet, kube-scheduler, kube-controller-manager, containerd, kernel cgroups, kube-proxy, v.v.).
4. **Nó liên hệ với những thành phần đã học như thế nào?** (Đối chiếu với Linux process, systemd service, Docker container, Compose network, AWS EC2, v.v.).

**Nguyên tắc triển khai:**
- Luôn phân biệt rạch ròi **cấu hình logic** (YAML manifest, desired state) với **tài nguyên vật lý/runtime** (actual state, RAM/CPU cấp phát, cgroup, iptables/eBPF rules).
- Dạy từng khái niệm nhỏ kết hợp lab có mục tiêu; tuyệt đối không đưa chuỗi lệnh dài khi chưa giải thích cơ chế.
- Lệnh terminal trình bày thành từng khối riêng, có mục đích rõ ràng; đợi học viên chạy và đọc output thật.
- File YAML được tạo/chỉnh sửa với đường dẫn tuyệt đối rõ ràng: `File cần sửa: /đường/dẫn/tuyệt/đối`.
- **Duy nhất một bài kiểm tra cuối buổi:** 7 câu trắc nghiệm khách quan + 2 câu tự luận bản chất/cơ chế. Không phát sinh bài kiểm tra phụ.

---

## 2. Kế hoạch Nội dung Buổi 44 (Kubernetes Troubleshooting & Defense)

- **Mục tiêu:** Nắm vững phương pháp luận và công cụ chẩn đoán sự cố theo bằng chứng (Evidence-Based Troubleshooting) trên cụm Kubernetes; tự tin khoanh vùng và khắc phục các lớp sự cố phổ biến từ Pod, Workload đến Mạng và Tài nguyên mà không dùng thao tác restart mù quáng.
- **Môi trường & Công cụ:**
  - WSL2 Ubuntu 24.04, Docker daemon, cụm Kind `s41` (hoặc dựng kịch bản kiểm thử độc lập).
  - `kubectl` (`describe`, `logs`, `events`, `get -o wide`, `exec`), `crictl`, `curl`.
- **Nội dung Lab Trọng tâm:**
  1. **Quy trình Chẩn đoán theo Bằng chứng (Diagnostics Workflow):**
     - Luồng: `kubectl get pods` $\rightarrow$ `kubectl describe pod <name>` (đọc Events) $\rightarrow$ `kubectl logs <name> [-p]` $\rightarrow$ `kubectl get events --sort-by=.metadata.creationTimestamp`.
  2. **Nhóm sự cố Khởi tạo Pod (Pod Lifecycle & Image):**
     - `ImagePullBackOff` / `ErrImagePull`: Sai repository, tag không tồn tại, thiếu ImagePullSecrets.
     - `CreateContainerConfigError` / `CreateContainerError`: Sai tên ConfigMap/Secret key, volume mount thất bại.
  3. **Nhóm sự cố Ứng dụng & Tiến trình (Application Crashes):**
     - `CrashLoopBackOff`: Lệnh CMD/args sai, thiếu biến môi trường bắt buộc, process PID 1 thoát với exit code non-zero. Phân tích `lastState` và cờ `--previous`.
     - Phân biệt rõ `CrashLoopBackOff` vs `ImagePullBackOff` vs `ReadinessProbe Failed`.
  4. **Nhóm sự cố Tài nguyên Hệ thống (Resource Constraints):**
     - `OOMKilled` (Exit code 137): Container vượt ngưỡng `limits.memory`; phân biệt với lỗi thiếu RAM node.
     - `Pending` / `FailedScheduling`: Requests vượt quá sức chứa node (`Insufficient cpu/memory`), không khớp `nodeSelector`, hoặc bị chặn bởi `Taints` thiếu `Tolerations`.
  5. **Nhóm sự cố Giám sát Sức khỏe (Health Check Probes):**
     - Readiness Probe thất bại: Pod Running nhưng NotReady (`0/1 Ready`), EndpointSlice tự động gỡ Pod khỏi traffic; phân biệt với Liveness Probe thất bại khiến container restart liên tục.
  6. **Nhóm sự cố Mạng Dịch vụ & Phân giải Tên miền (Networking & DNS):**
     - Service không định tuyến được: Lệch `selector` với Pod `labels` dẫn đến EndpointSlice trống (0 endpoints); lệch cổng `targetPort` so với containerPort.
     - Phân giải CoreDNS: Khắc phục sự cố Pod không resolve được service name nội bộ.
  7. **Thử thách Troubleshooting Defense Tổng hợp:**
     - Người học tiếp nhận kịch bản cụm bị lỗi đa tầng, tự thực hiện các bước điều tra theo bằng chứng, xác định root cause chính xác và áp dụng biện pháp sửa chữa tối thiểu.
  8. **Bài kiểm tra cuối buổi chuẩn hóa:** 7 câu trắc nghiệm + 2 câu tự luận (chỉ trong phạm vi các sự cố và cơ chế đã thực hành).
