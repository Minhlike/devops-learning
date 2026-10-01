# NEXT SESSION PLAN

- **Buổi học tiếp theo:** BUỔI 34 — Cần xác minh chủ đề chi tiết theo roadmap (Đề xuất định hướng logic tiếp theo: Ansible Roles, Modular Playbooks & Multi-Host Automation hoặc Ansible AWS Integration).
- **Lưu ý Roadmap:** Source of truth hiện tại (`STUDENT_PROFILE.md`) chỉ định nghĩa mục tiêu giai đoạn cấp cao (Phase 7-8: IaC Terraform/Ansible) mà chưa cố định tiêu đề cụ thể cho S34. Do đó, tiêu đề và phạm vi kỹ thuật chi tiết của S34 cần được người hướng dẫn / học viên thống nhất trước khi triển khai, không tự ý sáng tác nội dung ngoài lộ trình.

- **Nội dung Khởi động Bắt buộc Đầu Buổi 34 (Thời lượng: 15–20 phút):**
  - **Mục tiêu:** Củng cố sâu bản chất và khắc phục triệt để lỗ hổng tiếp thu của Buổi 33 trước khi tiếp cận kiến thức mới.
  - **5 Chuyên đề Review Sâu:**
    1. **Handlers & Event-Driven Notification:**
       - Bản chất điều kiện kích hoạt: Chỉ chạy khi task có `changed: true`.
       - Cơ chế gom (batch execution): Mặc định chỉ chạy một lần duy nhất ở cuối play dù có nhiều task cùng notify.
       - Kỹ thuật điều khiển luồng: Ứng dụng `ansible.builtin.meta: flush_handlers` để ép reload dịch vụ ngay lập tức khi cần tránh race condition.
    2. **Task Telemetry & Variable Registration (`register`):**
       - Cơ chế hoạt động: Lưu toàn bộ kết quả thực thi của task (stdout, stderr, rc, changed...) vào biến.
       - Cách truy xuất: Sử dụng biến đăng ký (`<var_name>.stdout`, `<var_name>.rc`) để làm dữ liệu đầu vào hoặc điều kiện rẽ nhánh cho các task sau.
    3. **Custom Business Failure Criteria (`failed_when`):**
       - Bản chất: Ghi đè cơ chế bắt lỗi mặc định dựa trên exit code (`rc != 0`).
       - Ứng dụng thực tế: Đánh dấu task thất bại dựa trên logic nghiệp vụ (ví dụ: HTTP status code trả về khác 200 dù lệnh `curl` có exit code 0).
    4. **Structured Error Handling (`block`, `rescue`, `always`):**
       - Phân tầng xử lý: `block` chứa tác vụ chính cần thực thi; `rescue` tự động kích hoạt khi có lỗi xảy ra trong block; `always` luôn được thực thi dù block thành công hay thất bại.
       - Ứng dụng: Đảm bảo dọn dẹp tài nguyên tạm thời hoặc phục hồi trạng thái khi gặp sự cố bất ngờ.
    5. **Safe Web Server Deployment Pipeline:**
       - Nhận diện rủi ro: Ghi file cấu hình lỗi trực tiếp vào thư mục dịch vụ đang chạy làm hỏng service trên disk.
       - Luồng triển khai 5 bước chuẩn hóa:
         1. Render candidate file ra thư mục tạm (`/tmp`).
         2. Tạo file cấu hình test độc lập.
         3. Validate cú pháp an toàn (`nginx -t -c`).
         4. Copy atomic candidate file vào thư mục chính thức (`/etc/nginx/conf.d/`) với `remote_src: true` chỉ khi validation PASS.
         5. Trigger handler reload dịch vụ.

- **Nội dung Kỹ thuật Dự kiến Buổi 34 (Sau khi hoàn tất 15-20 phút Review):**
  - Tiếp tục phát triển kỹ năng Ansible theo định hướng module hóa và tự động hóa nâng cao (chờ xác nhận chính thức từ roadmap).

- **Quy chuẩn Phương pháp Giảng dạy & Vận hành S34:**
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










