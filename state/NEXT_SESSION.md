# NEXT SESSION PLAN

- **Buổi học tiếp theo:** BUỔI 25 — PHASE 6: AWS RDS & Managed Database Fundamentals.
- **Mục tiêu Buổi 25:**
  1. So sánh kiến trúc Database tự vận hành trên EC2 vs Dịch vụ cơ sở dữ liệu được quản lý hoàn toàn (AWS Managed Database - Amazon RDS): Trade-offs về quản trị, patching, backup, HA và chi phí.
  2. Nắm vững kiến trúc cốt lõi của Amazon RDS: DB Instance class, Database Engine (PostgreSQL/MySQL), Storage types (gp3/io2), IOPS, Storage Auto-scaling và cơ chế phân giải DNS Endpoint.
  3. Cấu hình mạng riêng tư và bảo mật cho RDS:
     - Tạo DB Subnet Group bao phủ ít nhất 2 Availability Zones trong VPC theo chuẩn AWS Best Practice.
     - Thiết lập Security Group chuyên biệt cho Database: Chỉ cho phép traffic cổng DB (ví dụ TCP 5432) từ Security Group của EC2/Application layer, tuyệt đối không mở ra Internet (`0.0.0.0/0`).
  4. Phân biệt chuyên sâu High Availability (HA) vs Read Scaling:
     - Multi-AZ Deployment: Cơ chế đồng bộ dữ liệu (Synchronous replication), tự động chuyển đổi dự phòng (Automatic failover) nhằm đảm bảo tính sẵn sàng cao (High Availability).
     - Read Replica: Cơ chế bất đồng bộ (Asynchronous replication), tăng tải đọc (Read scaling) và giảm áp lực cho Primary DB.
  5. Cơ chế sao lưu và bảo trì: Automated Backups, Transaction Logs (PITR - Point-in-Time Recovery), Manual DB Snapshots và Maintenance Windows.
  6. Kiểm thử kết nối ứng dụng/EC2 tới RDS qua Private Networking: Truy cập cơ sở dữ liệu từ EC2 instance thông qua Private IP/Endpoint nội bộ.
  7. Thực hành Failure Injection: Cố tình cấu hình sai Database Security Group hoặc chặn Network Connectivity $\rightarrow$ ứng dụng báo lỗi Connection Timeout; điều chỉnh lại Security Group $\rightarrow$ kết nối thông suốt.
  8. Vận hành nguyên tắc Cost Safety nghiêm ngặt: Lựa chọn `db.t3.micro`/`db.t4g.micro` Single-AZ trong Free Tier, vô hiệu hóa Multi-AZ khi làm lab, và thực hiện xóa DB instance (kèm disable final snapshot hoặc xóa snapshot sau đó) để duy trì chi phí $0.





