# NEXT SESSION PLAN

- **Buổi học tiếp theo:** BUỔI 35 — Advanced Inventory & Multi-Host Automation.
- **Trạng thái:** S34 đã HOÀN THÀNH (COMPLETED) ngày 2026-10-02. S35 là buổi học kế tiếp theo lộ trình.
- **Mục tiêu Kỹ thuật Buổi 35:**
  - Nâng cấp Ansible Inventory từ single host/localhost sang kiến trúc Multi-Host và Dynamic/Advanced Grouping.
  - Quản lý cấu trúc `inventory/` đa file hoặc chia nhóm logic (`[web]`, `[db]`, `[loadbalancer]`, parent-child groups `[all:children]`).
  - Quản trị biến môi trường theo nhóm (`group_vars/`) và theo host (`host_vars/`).
  - Tự động hóa điều khiển song song (`forks`, `serial` execution) và rolling updates an toàn.
  - Tích hợp kỹ năng role đã xây dựng từ S34 để triển khai đồng bộ trên nhiều target hosts.

- **Nội dung Khởi động Đầu Buổi 35 (Thời lượng: 10–15 phút):**
  - **Mục tiêu:** Củng cố nhanh kiến trúc role và nguyên lý phân tầng biến trước khi mở rộng quy mô multi-host.
  - **Trọng tâm Review:**
    1. Cấu trúc thư mục role chuẩn và chức năng từng phân tầng (`tasks`, `handlers`, `templates`, `defaults`, `vars`, `meta`).
    2. Độ ưu tiên biến: `defaults/main.yml` vs `vars/main.yml` vs `vars:` tại playbook call site.
    3. Tránh hidden dependency trong role bằng cách thiết lập fallback an toàn trong `defaults`.
    4. Kỹ thuật `flush_handlers` và kiểm chứng Idempotency (`changed=0`).

- **Quy chuẩn Phương pháp Giảng dạy & Vận hành S35:**
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










