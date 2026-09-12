# NEXT SESSION PLAN

- **Buổi học tiếp theo:** BUỔI 23 — PHASE 6: AWS EC2 & VPC Fundamentals.
- **Mục tiêu Buổi 23:**
  1. Nắm vững vòng đời của máy chủ EC2 (EC2 Instance Lifecycle): Pending, Running, Stopping, Stopped, Terminated; hiểu cơ chế thanh toán và rủi ro chi phí giữa Stop vs Terminate (EBS volume tiếp tục tính phí khi instance stopped).
  2. Phân loại Amazon Machine Image (AMI): AWS Managed AMI (Amazon Linux 2023, Ubuntu Server), Custom AMI và Marketplace.
  3. Lựa chọn Instance Types phù hợp: Hiểu naming convention (ví dụ `t4g.nano`, `t3.micro`), tối ưu theo nhu cầu CPU/RAM/Network và tận dụng AWS Free Tier.
  4. Quản trị tường lửa mạng máy chủ với Security Group: Bản chất stateful của Security Group, cấu hình Inbound Rules (chỉ mở SSH port 22 và HTTP port 80 cho CIDR cần thiết) và Outbound Rules.
  5. Xây dựng mạng riêng ảo AWS VPC Fundamentals:
     - Tạo VPC với CIDR block chuẩn (ví dụ `10.0.0.0/16`).
     - Tạo Public Subnet gắn liền với Availability Zone cụ thể.
     - Tạo và gắn Internet Gateway (IGW) vào VPC.
     - Cấu hình Route Table điều hướng traffic ra Internet (`0.0.0.0/0` $\rightarrow$ IGW).
  6. Triển khai một EC2 instance nhỏ trong Public Subnet: Gắn SSH Key Pair, Public IP, cài đặt web server đơn giản (Nginx) bằng User Data script.
  7. Thực hành Cost Safety nghiêm ngặt: Kiểm tra trạng thái tài nguyên, thiết lập thói quen cleanup hoặc terminate instance sau khi hoàn thành lab để duy trì chi phí $0.



