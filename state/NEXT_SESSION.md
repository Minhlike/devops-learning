# NEXT SESSION PLAN

- **Buổi học tiếp theo:** BUỔI 30 — Terraform Variables, Outputs, Dependencies & Multi-Resource Provisioning on AWS.
- **Mục tiêu Buổi 30:**
  1. Quản trị Input Variables (`variables.tf`):
     - Khai báo biến đầu vào với kiểu dữ liệu cơ bản và phức hợp: `string`, `number`, `bool`, `list`, `map`, `object`.
     - Thiết lập giá trị mặc định (`default`), mô tả (`description`) và các ràng buộc xác thực (`validation`).
  2. Thứ tự ưu tiên nạp biến trong Terraform (Variable Definition Precedence):
     - Thực hành nạp biến qua file `terraform.tfvars`, `*.auto.tfvars`, biến môi trường `TF_VAR_*` và cờ dòng lệnh `-var`.
  3. Quản trị Local Values (`locals.tf`):
     - Tái sử dụng biểu thức phức tạp, chuẩn hóa quy chuẩn đặt tên tài nguyên (naming conventions) và gắn thẻ chung (common tags).
  4. Quản trị Output Values (`outputs.tf`):
     - Trích xuất và hiển thị các thuộc tính quan trọng của hạ tầng sau khi triển khai; sử dụng cờ `sensitive = true` để bảo vệ dữ liệu nhạy cảm.
  5. Quản lý phụ thuộc giữa các tài nguyên (Resource Dependencies & Graph):
     - Phụ thuộc ngầm định (Implicit Dependency): Tham chiếu trực tiếp thuộc tính từ resource này sang resource khác (ví dụ: gán subnet ID, security group ID vào EC2).
     - Phụ thuộc tường minh (Explicit Dependency): Sử dụng khối `depends_on` cho các trường hợp không có tham chiếu trực tiếp.
  6. Triển khai hạ tầng mạng và tính toán đa tài nguyên trên AWS bằng Terraform:
     - Tự động hóa provisioning: VPC, Public Subnet, Internet Gateway, Route Table, Security Group (mở port 80/443), và EC2 instance (`t3.micro`, Amazon Linux 2023) đính kèm Nginx User Data script.
  7. Sử dụng Data Sources mở rộng:
     - Tự động tra cứu AMI Amazon Linux mới nhất qua `data "aws_ami"` thay vì hard-code AMI ID tĩnh.
  8. Tổng quan về Remote State & State Locking:
     - Phân tích rủi ro khi lưu state ở local; nguyên lý lưu trữ state từ xa trên Amazon S3 và cơ chế khóa trạng thái (State Locking) với Amazon DynamoDB để hỗ trợ làm việc nhóm.
  9. Thực hành Failure Injection & Troubleshooting:
     - Cố tình tạo phụ thuộc vòng (circular dependency) hoặc truyền sai kiểu biến để kiểm chứng thông báo lỗi của Terraform.
  10. Vận hành nguyên tắc Cost Safety nghiêm ngặt và dọn dẹp sạch toàn bộ tài nguyên qua `terraform destroy`.
- **Yêu cầu phương pháp giảng dạy S30:**
  - Tiếp tục duy trì nguyên tắc **Architecture-First**: Phác thảo sơ đồ liên kết giữa các tài nguyên trước khi viết mã nguồn HCL.
  - Hướng dẫn chi tiết cấu trúc thư mục module hóa (`providers.tf`, `variables.tf`, `locals.tf`, `main.tf`, `outputs.tf`, `terraform.tfvars`).










