# Lab S44 — Kubernetes Troubleshooting & Defense

Thư mục lưu trữ các kịch bản manifest mô phỏng, cô lập và khắc phục sự cố Kubernetes thực tế của Buổi 44: chẩn đoán theo bằng chứng (Evidence-Based Diagnostics), phân loại trạng thái lỗi Pod, tài nguyên và mạng dịch vụ.

## 1. Danh mục Manifests Mô phỏng Sự cố

| Tệp Manifest | Dạng sự cố mô phỏng | Bằng chứng chẩn đoán | Biện pháp khắc phục |
| :--- | :--- | :--- | :--- |
| `crashloop.yaml` | `CrashLoopBackOff` | `kubectl describe pod` -> `Last State: Terminated (exit code != 0)`, `kubectl logs -p` | Điều chỉnh command/args tiến trình PID 1, bổ sung dependency hoặc fix mã thoát |
| `readiness.yaml` | `ReadinessProbe Failed` | Pod trạng thái `Running` nhưng `0/1 Ready`; `kubectl get endpointslices` không có endpoint | Khắc phục endpoint sức khỏe nghiệp vụ của ứng dụng; kiểm tra đúng path và port probe |
| `liveness.yaml` | `LivenessProbe Failed` | Kubelet kill và restart container liên tục (`RestartCount` tăng dần); Events báo probe timeout/404 | Điều chỉnh tham số `initialDelaySeconds`, `timeoutSeconds` hoặc sửa deadlock logic |
| `oom.yaml` | `OOMKilled` (Exit Code 137) | `kubectl describe pod` -> `Reason: OOMKilled`, `Exit Code: 137` do nhân Linux kích hoạt OOM Killer | Cân đối nâng `limits.memory` hoặc tối ưu bộ nhớ heap/cấp phát mã nguồn |
| `insufficient-memory.yaml` | `Pending / FailedScheduling` | Pod kẹt `Pending`, Events báo: `0/1 nodes are available: 1 Insufficient memory` | Hạ `requests.memory` về mức node đáp ứng được hoặc scale worker node |
| `service-debug.yaml` | Service Routing Mismatch | Service trả Connection refused / 404, EndpointSlice rỗng (`0 endpoints`) | Căn chỉnh `spec.selector` của Service khớp chính xác `metadata.labels` của Pod |

## 2. Quy trình Chẩn đoán theo Bằng chứng (4 Bước)

```text
[B1: Khảo sát tổng quan]   kubectl get pods -o wide -n <ns>
          │
[B2: Đọc sự kiện runtime]  kubectl describe pod <name> -n <ns> (xem Events & Last State)
          │
[B3: Truy vết log ứng dụng] kubectl logs <name> [-c <container>] [-p] -n <ns>
          │
[B4: Kiểm tra tầng mạng]    kubectl get endpointslices,services -n <ns>
```

## 3. Quy chuẩn 4 Câu hỏi Định vị Hạ tầng

Mỗi đối tượng điều tra đều được đối soát qua 4 chiều:
1. **Thành phần thật:** Tiến trình OS, file socket, bản ghi etcd, hay iptables rule?
2. **Nơi thực thi:** Host, WSL, Control Plane, Worker Node, hay Container cgroup?
3. **Thành phần quản lý:** Kubelet, containerd, kube-scheduler, kube-controller-manager?
4. **Liên hệ thực tiễn:** Tương đương với gì trong Linux systemd, Docker hay mạng truyền thống?
