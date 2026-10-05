# NEXT SESSION PLAN

- **Buổi học tiếp theo:** BUỔI 39 — Kubernetes ConfigMap, Secret, Environment & Probes.
- **Trạng thái:** Buổi 38 (Kubernetes Service & Networking) đã HOÀN THÀNH (COMPLETED) ngày 2026-10-05. S39 là buổi học kế tiếp theo lộ trình (quản trị cấu hình, dữ liệu mật và cơ chế giám sát sức khỏe container).
- **Mục tiêu Kỹ thuật Buổi 39:**
  - **Quản trị Cấu hình Ứng dụng với ConfigMap:**
    - Khái niệm tách biệt code và cấu hình (The Twelve-Factor App).
    - Tạo ConfigMap từ literal values, file và directory.
    - Truyền ConfigMap vào Pod: biến môi trường đơn lẻ (`valueFrom.configMapKeyRef`), toàn bộ cấu hình qua env (`envFrom.configMapRef`), và mount dưới dạng Volume (`volumes` / `volumeMounts`).
  - **Quản trị Dữ liệu Mật với Kubernetes Secrets:**
    - Khái niệm Secrets loại Opaque.
    - So sánh cơ chế bảo mật: Base64 encoding của K8s Secret vs Ansible Vault encryption (mã hóa at rest thực sự) và các giải pháp Vault tập trung.
    - Truyền Secret vào Pod an toàn qua environment variables và file volume mounts.
    - Thực hành bảo mật: Thiết lập phân quyền tệp tin mount `defaultMode: 0400 / 0600`.
  - **Giám sát Sức khỏe & Vòng đời Ứng dụng với Container Probes:**
    - Cơ chế tự phục hồi nâng cao: Kubelet probe container.
    - Liveness Probe: Phát hiện deadlock / treo ứng dụng -> tự động restart container.
    - Readiness Probe: Kiểm tra ứng dụng sẵn sàng nhận traffic -> kết nối/ngắt kết nối khỏi Service EndpointSlice (liên kết trực tiếp kiến thức S38).
    - Startup Probe: Hỗ trợ ứng dụng khởi động chậm, tránh bị Liveness giết sớm.
    - Ba cơ chế kiểm tra probe: HTTP GET, TCP Socket, Exec command.
    - Cấu hình tham số: `initialDelaySeconds`, `periodSeconds`, `timeoutSeconds`, `failureThreshold`, `successThreshold`.

- **Nội dung Khởi động Đầu Buổi 39 (Thời lượng: 10–15 phút):**
  - **Mục tiêu:** Kết nối logic từ Service & EndpointSlice (S38) $\rightarrow$ Readiness Probe & Service traffic routing $\rightarrow$ Quản trị Config/Secret an toàn.
  - **Trọng tâm Review:**
    1. Cơ chế hoạt động của Service Selector và cách EndpointSlice thu nạp/loại bỏ Pod IP backend.
    2. Vì sao Pod IP không ổn định nhưng Service mang lại địa chỉ truy cập ổn định.
    3. Điểm khác biệt cốt lõi giữa base64 encoding (Kubernetes Secret) và AES-256 encryption (Ansible Vault từ S36).

- **Quy chuẩn Phương pháp Giảng dạy & Vận hành S39:**
  - **Hiển thị tiến độ phiên:** Mỗi phản hồi trong session học phải hiển thị ngắn gọn tiến độ toàn buổi: phần đã xong, phần hiện tại, phần còn lại.
  - **Lab là trung tâm:** Lab là phần trung tâm của session; tuyệt đối không biến buổi học thành chuỗi hỏi–đáp lý thuyết suông.
  - **Nhịp chuẩn triển khai:** Lý thuyết cần thiết $\rightarrow$ Guided Lab nhỏ $\rightarrow$ học viên chạy $\rightarrow$ đọc output thật $\rightarrow$ giải thích output $\rightarrow$ mini-check khi thực sự cần $\rightarrow$ tăng dần mức tự làm $\rightarrow$ Failure Injection $\rightarrow$ Troubleshooting $\rightarrow$ Defense $\rightarrow$ Active Recall $\rightarrow$ Cleanup.
  - **Mini-check có trọng tâm:** Mini-check chỉ dùng tại các điểm kiến thức quan trọng, không hỏi máy móc sau mọi đoạn giải thích.
  - **Cấu trúc 4 bước cho từng khái niệm:** `Nó là gì` $\rightarrow$ `Vì sao cần nó` $\rightarrow$ `Nó hoạt động thế nào` $\rightarrow$ `Ví dụ thực tế trong doanh nghiệp`.
  - **Chỉ định đường dẫn file:** Trước khi sửa hoặc tạo file, luôn ghi rõ: `File cần sửa: /đường/dẫn/tuyệt/đối/chính/xác`.
  - **Phân phối lệnh vừa phải:** Số lượng lệnh mỗi lượt phải vừa phải; trước mỗi lệnh phải giải thích ngắn gọn mục đích; không xả hàng loạt lệnh cùng lúc.
  - **Khởi động phiên:** Khi bắt đầu ngày học/session lab mới, thực hiện block khởi động WSL và kiểm tra trạng thái Docker daemon / Kind cluster.
  - **Tiêu chuẩn năng lực thực tế (Mastery):** Không nhầm lẫn việc học viên trả lời đúng hoặc chạy được lab là đã nắm vững kiến thức; việc nắm vững phải được chứng minh qua thực hành độc lập, xử lý sự cố (troubleshooting) và Defense.
  - **Kiểm soát tải nhận thức:** Giảm tốc độ giảng dạy, tinh gọn số lượng khái niệm mới để đảm bảo người học nắm vững bản chất thay vì chỉ chạy lướt qua lệnh lab.
  - **Quy chuẩn Defense Mode:** Chuẩn bị đủ kiến thức trước khi test, kịch bản chỉ xoay quanh nội dung đã học, bấm giờ countdown thật (nếu có timed defense), không đưa gợi ý (hints) trong quá trình xử lý, có rubric và xác minh minh bạch; phân biệt rõ Technical Defense PASS vs Timed Defense PASS.
  - **Đồng bộ Active Recall:** Câu hỏi Active Recall cuối buổi chỉ kiểm tra đúng phạm vi và độ sâu đã được truyền đạt trong buổi học.
  - **Bảo tồn Roadmap (S34–S66):** Không tự ý thay đổi roadmap cấp session từ S34–S66; nếu repo chưa có tài liệu roadmap này thì bổ sung tài liệu roadmap từ handoff đang hoạt động, bảo đảm không xung đột với tiến độ trong state.
  - **Ranh giới Git giữa buổi:** Không cập nhật và push lên GitHub giữa chừng trong buổi học trừ khi học viên yêu cầu.










