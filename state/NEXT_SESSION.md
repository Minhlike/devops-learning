# NEXT SESSION PLAN

- **Buổi học tiếp theo:** BUỔI 37 — Kubernetes Fundamentals: Cluster, Pod, Deployment.
- **Trạng thái:** Buổi 36 (Ansible Tags, Vault & Secrets Management) đã HOÀN THÀNH (COMPLETED) ngày 2026-10-04. S37 là buổi học kế tiếp theo lộ trình (bước chuyển sang mảng Container Orchestration).
- **Mục tiêu Kỹ thuật Buổi 37:**
  - **Tổng quan Kiến trúc Kubernetes (K8s Architecture):**
    - Control Plane: API Server, etcd, kube-scheduler, kube-controller-manager.
    - Worker Node: kubelet, kube-proxy, Container Runtime (containerd).
  - **Thiết lập Môi trường Kubernetes Cục bộ (Local Cluster):**
    - Khởi tạo và kiểm tra trạng thái cụm K8s với Minikube (hoặc Kind/K3s) trên WSL2 Ubuntu.
    - Làm quen và thành thạo bộ lệnh CLI cơ bản `kubectl`: `cluster-info`, `get nodes`, `describe node`.
  - **Khái niệm Pod & Vòng đời Pod:**
    - Hiểu Pod là đơn vị triển khai nhỏ nhất trong Kubernetes.
    - Viết manifest YAML Pod đầu tiên (`apiVersion: v1`, `kind: Pod`, `spec.containers`).
    - Thao tác: `kubectl apply`, `kubectl get pods`, `kubectl describe pod`, `kubectl logs`, `kubectl exec`.
  - **Quản trị Deployment & Tự phục hồi (Self-Healing):**
    - Khái niệm Deployment & ReplicaSet.
    - Viết manifest `kind: Deployment`, quản lý số lượng bản sao (`replicas: 2`).
    - Kiểm chứng cơ chế Self-Healing: Xóa 1 Pod, quan sát Kubernetes tự động khởi tạo Pod mới để duy trì desired state.
    - Khái niệm Rolling Update và Scaling Pods theo yêu cầu.
  - **Phân biệt Mô hình Vận hành:**
    - So sánh Docker Compose (single host) vs Kubernetes (multi-host cluster orchestration).

- **Nội dung Khởi động Đầu Buổi 37 (Thời lượng: 10–15 phút):**
  - **Mục tiêu:** Kết nối logic từ Docker (đóng gói) $\rightarrow$ Ansible (quản trị máy chủ) $\rightarrow$ Kubernetes (điều phối cụm container).
  - **Trọng tâm Review:**
    1. Vòng đời container và cổng mạng (Port binding) từ nền tảng Docker.
    2. Nguyên lý Desired State và Idempotency (tương đồng giữa Terraform/Ansible và Kubernetes Controller).
    3. Nguyên tắc bảo vệ Secrets (chuẩn bị cho Kubernetes Secrets/ConfigMaps).

- **Quy chuẩn Phương pháp Giảng dạy & Vận hành S37:**
  - **Hiển thị tiến độ phiên:** Mỗi phản hồi trong session học phải hiển thị ngắn gọn tiến độ toàn buổi: phần đã xong, phần hiện tại, phần còn lại.
  - **Lab là trung tâm:** Lab là phần trung tâm của session; tuyệt đối không biến buổi học thành chuỗi hỏi–đáp lý thuyết suông.
  - **Nhịp chuẩn triển khai:** Lý thuyết cần thiết $\rightarrow$ Guided Lab nhỏ $\rightarrow$ học viên chạy $\rightarrow$ đọc output thật $\rightarrow$ giải thích output $\rightarrow$ mini-check khi thực sự cần $\rightarrow$ tăng dần mức tự làm $\rightarrow$ Failure Injection $\rightarrow$ Troubleshooting $\rightarrow$ Defense $\rightarrow$ Active Recall $\rightarrow$ Cleanup.
  - **Mini-check có trọng tâm:** Mini-check chỉ dùng tại các điểm kiến thức quan trọng, không hỏi máy móc sau mọi đoạn giải thích.
  - **Cấu trúc 4 bước cho từng khái niệm:** `Nó là gì` $\rightarrow$ `Vì sao cần nó` $\rightarrow$ `Nó hoạt động thế nào` $\rightarrow$ `Ví dụ thực tế trong doanh nghiệp`.
  - **Chỉ định đường dẫn file:** Trước khi sửa hoặc tạo file, luôn ghi rõ: `File cần sửa: /đường/dẫn/tuyệt/đối/chính/xác`.
  - **Phân phối lệnh vừa phải:** Số lượng lệnh mỗi lượt phải vừa phải; trước mỗi lệnh phải giải thích ngắn gọn mục đích; không xả hàng loạt lệnh cùng lúc.
  - **Khởi động phiên & Cloud Verification:** Khi bắt đầu ngày học/session lab mới, thực hiện block khởi động WSL/AWS đã thống nhất và kiểm tra `aws sts get-caller-identity` trước khi thao tác cloud.
  - **Tiêu chuẩn năng lực thực tế (Mastery):** Không nhầm lẫn việc học viên trả lời đúng hoặc chạy được lab là đã nắm vững kiến thức; việc nắm vững phải được chứng minh qua thực hành độc lập, xử lý sự cố (troubleshooting) và Defense.
  - **Kiểm soát tải nhận thức:** Giảm tốc độ giảng dạy, tinh gọn số lượng khái niệm mới để đảm bảo người học nắm vững bản chất thay vì chỉ chạy lướt qua lệnh lab.
  - **Quy chuẩn Defense Mode:** Chuẩn bị đủ kiến thức trước khi test, kịch bản chỉ xoay quanh nội dung đã học, bấm giờ countdown thật, không đưa gợi ý (hints) trong quá trình xử lý, có rubric và xác minh minh bạch.
  - **Đồng bộ Active Recall:** Câu hỏi Active Recall cuối buổi chỉ kiểm tra đúng phạm vi và độ sâu đã được truyền đạt trong buổi học.
  - **Bảo tồn Roadmap (S34–S66):** Không tự ý thay đổi roadmap cấp session từ S34–S66; nếu repo chưa có tài liệu roadmap này thì bổ sung tài liệu roadmap từ handoff đang hoạt động, bảo đảm không xung đột với tiến độ trong state.
  - **Ranh giới Git giữa buổi:** Không cập nhật và push lên GitHub giữa chừng trong buổi học trừ khi học viên yêu cầu.










