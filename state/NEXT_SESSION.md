# NEXT SESSION PLAN

- **Buổi học tiếp theo:** TIẾP TỤC BUỔI 36 — Ansible Deployment Strategy, Tags, Vault & Secrets (Phần 2: Deployment Strategies & Rolling Updates).
- **Trạng thái:**
  - Buổi 35 (Advanced Inventory & Multi-Host Automation): Đã HOÀN THÀNH (COMPLETED) ngày 2026-10-02.
  - Buổi 36 (Deployment Strategy, Tags, Vault & Secrets): Đang thực hiện (IN PROGRESS - Phần 1 hoàn thành ngày 2026-10-04, chưa hoàn thành phần Rolling Deployment).
  - **Lưu ý Roadmap:** Tuyệt đối giữ nguyên roadmap, KHÔNG chuyển sang S37 Kubernetes cho tới khi S36 được hoàn thành toàn diện và nghiệm thu đạt chuẩn.

- **Nội dung S36 ĐÃ HOÀN THÀNH (Phần 1):**
  - Quản trị task với `tags`, thực thi có chọn lọc bằng `--tags` và loại trừ bằng `--skip-tags`.
  - Khởi tạo và mã hóa tệp tin chứa bí mật bằng `ansible-vault encrypt`.
  - Nạp tệp tin biến đã mã hóa qua `vars_files: - vars/vault.yml`.
  - Bảo mật secret at rest vs runtime, ngăn chặn lộ log với `no_log: true` và phân quyền tệp tin `mode: "0600"`.
  - Failure Injection sai mật khẩu Vault khi giải mã.
  - Kiểm định tự động trạng thái hệ thống bằng `ansible.builtin.stat` + `ansible.builtin.assert`.
  - Idempotency PASS (`changed=0`), Technical Defense PASS (Timed Defense ghi nhận VOID / không chấm do đề test ngoài phạm vi đã dạy).
  - Active Recall 7/7 và Cleanup PASS.

- **Nội dung Kỹ thuật Trọng tâm Cần Hoàn thành Tiếp tục ở Buổi 36 (Phần 2):**
  1. **Chiến lược Triển khai Cuốn chiếu (Rolling Deployment):**
     - `serial`: Điều khiển số lượng hoặc tỷ lệ phần trăm managed nodes được cập nhật trong từng đợt (`serial: 1`, `serial: 2`, `serial: "50%"`).
     - `max_fail_percentage`: Ngưỡng phần trăm lỗi tối đa cho phép trong một đợt trước khi dừng toàn bộ playbook để bảo vệ hệ thống.
     - `any_errors_fatal: true`: Dừng ngay lập tức toàn bộ quá trình triển khai khi có bất kỳ node nào gặp lỗi ở đợt hiện tại.
  2. **Ủy quyền Tác vụ (Task Delegation):**
     - `delegate_to`: Chuyển quyền thực thi task lên host khác (ví dụ: rút/nạp node khỏi load balancer hoặc thông báo monitoring).
  3. **Thao tác Vault CLI Nâng cao:**
     - `ansible-vault decrypt` (giải mã tệp tin), `ansible-vault view` (xem nội dung mã hóa), `ansible-vault edit` (chỉnh sửa trực tiếp file mã hóa).
  4. **Failure Injection trong Rolling Deployment:**
     - Mô phỏng node đầu tiên gặp sự cố, kiểm chứng cơ chế `serial` kết hợp `any_errors_fatal` ngăn chặn việc triển khai tiếp lên các node còn lại.
  5. **Thử thách Defense Mode Toàn diện Cuối Buổi 36:**
     - Kịch bản tổng hợp cả Rolling Deployment, Task Delegation và Quản trị Bí mật được bấm giờ countdown chuẩn mực sau khi học đủ kiến thức.

- **Quy chuẩn Phương pháp Giảng dạy & Vận hành S36:**
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










