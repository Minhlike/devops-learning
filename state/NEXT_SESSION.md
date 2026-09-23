# NEXT SESSION PLAN

- **Buổi học tiếp theo (Next Logical Session):** BUỔI 32 — Terraform Meta-Arguments, Lifecycle, for_each/count, Import & Safe Refactoring
- **Mục tiêu Buổi 32:**
  1. Terraform Meta-Arguments: `count` vs `for_each`:
     - Phân tích sâu sắc sự khác biệt giữa `count` (dựa trên mảng index) và `for_each` (dựa trên set/map keys).
     - Rủi ro của `count`: Vấn đề index shift khi xóa hoặc chèn phần tử ở giữa danh sách khiến Terraform tái tạo (recreate) hàng loạt tài nguyên ngoài ý muốn.
     - Ứng dụng `for_each` để tạo tài nguyên theo danh mục định danh ổn định.
  2. Quản trị vòng đời tài nguyên nâng cao (Resource Lifecycle Rules):
     - `create_before_destroy`: Tạo tài nguyên mới trước khi hủy tài nguyên cũ, hạn chế tối đa thời gian downtime.
     - `prevent_destroy`: Chốt chặn an toàn ngăn chặn việc vô tình phá hủy các tài nguyên quan trọng (database, storage bucket).
     - `ignore_changes`: Bỏ qua các thay đổi drift trên những thuộc tính cụ thể do bên ngoài hoặc autoscaling can thiệp.
     - `replace_triggered_by`: Kích hoạt tái tạo tài nguyên khi một tài nguyên phụ thuộc khác bị thay đổi.
  3. Quản trị tài nguyên hiện hữu với Terraform Import:
     - Nhập tài nguyên đã có sẵn trên AWS (tạo qua console/CLI) vào Terraform state mà không làm gián đoạn hệ thống.
     - Thực hành khối lệnh `import {}` chuẩn trong Terraform modern và lệnh `terraform plan -generate-config-out`.
  4. Safe Refactoring & State Surgery (`moved {}` & `terraform state mv`):
     - Tái cấu trúc mã nguồn: Đổi tên resource block hoặc di chuyển resource từ root module vào bên trong child module.
     - Sử dụng khối `moved {}` để Terraform tự động cập nhật state address mà không destroy/recreate tài nguyên thực tế ngoài cloud.
  5. Cấu hình khối lặp động (Dynamic Blocks):
     - Tối ưu hóa các khối lặp lồng nhau (nested blocks) như Security Group rules hoặc VPC tags bằng biểu thức `dynamic`.
  6. Thực hành Failure Injection & Troubleshooting:
     - Giả lập lỗi index shift với `count`.
     - Kiểm chứng cơ chế bảo vệ của `prevent_destroy` khi thực thi lệnh destroy.
  7. Thử thách Defense Mode (Áp lực thời gian):
     - Kịch bản sự cố thực tế chỉ xoay quanh nội dung đã học.
     - Bộ đếm thời gian (Countdown) thực tế, không gợi ý (no hints).
     - Rubric đánh giá rõ ràng và xác minh kỹ thuật minh bạch.
  8. Vận hành nguyên tắc Cost Safety & Resource Deprovisioning:
     - `terraform destroy` toàn bộ tài nguyên bài lab, kiểm tra state list trống và dọn dẹp an toàn.
- **Yêu cầu phương pháp giảng dạy S32:**
  - Trước MỌI lệnh sửa file, bắt buộc ghi rõ: `File cần sửa: <exact path>`.
  - Không dồn quá nhiều lệnh liên tiếp mà không giải thích bản chất kỹ thuật.
  - Giữ vững phong cách: `Theory` $\rightarrow$ `Guided Action` $\rightarrow$ `Explain Result` $\rightarrow$ `Check Question`.
  - Duy trì tôn chỉ: Lab-first nhưng không phải command-only.










