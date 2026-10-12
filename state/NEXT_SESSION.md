# NEXT SESSION PLAN

- **Buổi học tiếp theo:** HOÀN TẤT BUỔI 40 — Khắc phục Sự cố HPA Autoscaling & Cleanup Cụm S40 (Chuẩn bị chuyển tiếp S41 theo Roadmap).
- **Trạng thái:**
  - Buổi 39 (Kubernetes ConfigMap, Secret, Environment & Probes) đã **HOÀN THÀNH (COMPLETED - Technical Defense PASS, Active Recall 7/7)** ngày 2026-10-06.
  - Buổi 40 (Kubernetes Resources, Scheduling & Scaling) đang ở trạng thái **IN PROGRESS / PARTIALLY VERIFIED**: Đã hoàn thành Resources (requests/limits), OOMKilled, CPU Throttling, 3 QoS classes, nodeSelector, Taints & Tolerations, Manual Scaling, Technical Defense PASS và Active Recall 7/7 PASS ngày 12/10/2026.
  - Tồn đọng quan trọng: Sự cố HPA `s40-scaling-hpa` hiển thị `CPU: <unknown>/50%` chưa xác định được root cause; chưa kiểm chứng được hành vi scale-up/scale-down tự động; chưa thực hiện cleanup cluster S40.
- **Mục tiêu Ưu tiên Hàng đầu Đầu Phiên Kế tiếp:**
  1. **Khảo sát Hiện trường Cluster S40:**
     - Kiểm tra trạng thái các node (`kubectl get nodes`) và các Pod trong namespace `default` (`s40-scaling`) và `kube-system` (`metrics-server`).
     - Xác minh trạng thái API metrics: `kubectl top pods`, `kubectl get --raw /apis/metrics.k8s.io/v1beta1/pods`.
  2. **Điều tra Nguyên nhân Gốc rễ (Root Cause Analysis) Sự cố HPA `<unknown>/50%`:**
     - Kiểm tra log của `metrics-server`: Chẩn đoán nguyên nhân gây restart 17 lần, liveness timeout, `SandboxChanged` và `Error exit=2`.
     - Kiểm tra log của `kube-controller-manager` (container trong Kind control-plane) để đọc trực tiếp lỗi khi controller scrape metrics từ metrics-server cho HPA.
     - Kiểm tra cấu hình cờ khởi động của Metrics Server trên Kind (xác minh `--kubelet-insecure-tls`, `--kubelet-preferred-address-types=InternalIP`).
  3. **Khắc phục và Kiểm chứng Chu trình Horizontal Pod Autoscaling (HPA):**
     - Đưa HPA `s40-scaling-hpa` về trạng thái đọc được metrics hợp lệ (thay vì `<unknown>/50%`).
     - Sinh tải CPU cao lên Deployment `s40-scaling` và quan sát HPA tự động scale tăng replicas (từ 1 lên 2–5 Pods).
     - Ngắt tải CPU, quan sát chu kỳ ổn định (cooldown / stabilization window) và HPA tự động scale giảm về `minReplicas: 1`.
  4. **Thực hiện Quy trình Cleanup An toàn Buổi 40:**
     - Xóa các tài nguyên lab S40 (Deployment, Pods, HPA, Metrics Server).
     - Xóa cụm Kind `s40` (`kind delete cluster --name s40`), xác minh `kind get clusters` và `docker ps -a` sạch hoàn toàn.
     - Lưu trữ toàn bộ manifest YAML trong `labs/lab-40-kubernetes-resources-scheduling-scaling` làm bằng chứng.
  5. **Nghiệm thu Buổi 40 & Chuyển tiếp Roadmap:**
     - Sau khi khắc phục thành công sự cố HPA và hoàn thành Cleanup, chính thức cập nhật S40 sang trạng thái **COMPLETED**.
     - Chuyển tiếp sang buổi học tiếp theo theo đúng lộ trình Roadmap: **BUỔI 41 — Kubernetes Ingress Controller & Routing**.

- **Quy chuẩn Phương pháp Giảng dạy & Vận hành Phiên:**
  - **Hiển thị tiến độ phiên:** Mỗi phản hồi trong session học phải hiển thị ngắn gọn tiến độ toàn buổi: phần đã xong, phần hiện tại, phần còn lại.
  - **Lab là trung tâm:** Lab là phần trung tâm của session; tuyệt đối không biến buổi học thành chuỗi hỏi–đáp lý thuyết suông.
  - **Nhịp chuẩn triển khai:** Lý thuyết cần thiết $\rightarrow$ Guided Lab nhỏ $\rightarrow$ học viên chạy $\rightarrow$ đọc output thật $\rightarrow$ giải thích output $\rightarrow$ mini-check khi thực sự cần $\rightarrow$ tăng dần mức tự làm $\rightarrow$ Failure Injection $\rightarrow$ Troubleshooting $\rightarrow$ Defense $\rightarrow$ Active Recall $\rightarrow$ Cleanup.
  - **Mini-check có trọng tâm:** Mini-check chỉ dùng tại các điểm kiến thức quan trọng, không hỏi máy móc sau mọi đoạn giải thích.
  - **Cấu trúc 4 bước cho từng khái niệm:** `Nó là gì` $\rightarrow$ `Vì sao cần nó` $\rightarrow$ `Nó hoạt động thế nào` $\rightarrow$ `Ví dụ thực tế trong doanh nghiệp`.
  - **Chỉ định đường dẫn file:** Trước khi sửa hoặc tạo file, luôn ghi rõ: `File cần sửa: /đường/dẫn/tuyệt/đối/chính/xác`.
  - **Phân phối lệnh vừa phải:** Số lượng lệnh mỗi lượt phải vừa phải; trước mỗi lệnh phải giải thích ngắn gọn mục đích; không xả hàng loạt lệnh cùng lúc.
  - **Khởi động phiên:** Khi bắt đầu ngày học/session lab mới, thực hiện block khởi động WSL và kiểm tra trạng thái Docker daemon / Kind cluster `s40`.
  - **Tiêu chuẩn năng lực thực tế (Mastery):** Không nhầm lẫn việc học viên trả lời đúng hoặc chạy được lab là đã nắm vững kiến thức; việc nắm vững phải được chứng minh qua thực hành độc lập, xử lý sự cố (troubleshooting) và Defense.
  - **Kiểm soát tải nhận thức:** Giảm tốc độ giảng dạy, tinh gọn số lượng khái niệm mới để đảm bảo người học nắm vững bản chất thay vì chỉ chạy lướt qua lệnh lab.
  - **Quy chuẩn Defense Mode:** Chuẩn bị đủ kiến thức trước khi test, kịch bản chỉ xoay quanh nội dung đã học, bấm giờ countdown thật (nếu có timed defense), không đưa gợi ý (hints) trong quá trình xử lý, có rubric và xác minh minh bạch; phân biệt rõ Technical Defense PASS vs Timed Defense PASS.
  - **Đồng bộ Active Recall:** Câu hỏi Active Recall cuối buổi chỉ kiểm tra đúng phạm vi và độ sâu đã được truyền đạt trong buổi học.
  - **Bảo tồn Roadmap (S34–S66):** Không tự ý thay đổi roadmap cấp session từ S34–S66; nếu repo chưa có tài liệu roadmap này thì bổ sung tài liệu roadmap từ handoff đang hoạt động, bảo đảm không xung đột với tiến độ trong state.
  - **Ranh giới Git giữa buổi:** Không cập nhật và push lên GitHub giữa chừng trong buổi học trừ khi học viên yêu cầu.
