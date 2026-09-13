# NEXT SESSION PLAN

- **Buổi học tiếp theo:** BUỔI 24 — PHASE 6: AWS Storage & IAM Role for EC2.
- **Mục tiêu Buổi 24:**
  1. Nắm vững nền tảng Amazon S3 (Simple Storage Service): Khái niệm Bucket, Object, Prefix (giả lập thư mục), Storage Class và tính độc lập Region.
  2. Nắm vững nền tảng Amazon Elastic Block Store (EBS): Phân loại Volume (gp3, io2), Snapshot, cơ chế đính kèm/tháo gỡ (Attach/Detach) và gắn kết Availability Zone.
  3. So sánh chuyên sâu các loại hình lưu trữ trên AWS: Instance Store (Ephemerality/Hiệu năng cao) vs EBS (Block Storage/Persistence) vs S3 (Object Storage/Scale vô hạn/REST API).
  4. Tạo S3 Bucket thực hành với tiêu chí Cost Safety: Cấu hình bucket duy nhất toàn cầu, bật mã hóa SSE-S3 mặc định và chặn truy cập công khai (Block Public Access).
  5. Thiết kế và khởi tạo IAM Role dành riêng cho máy chủ EC2:
     - Soạn thảo Trust Policy cho phép dịch vụ `ec2.amazonaws.com` assume role qua `sts:AssumeRole`.
     - Soạn thảo Permission Policy cấp quyền đọc hạn chế (`s3:GetObject`, `s3:ListBucket`) trên S3 bucket bài lab.
     - Tạo IAM Instance Profile để gắn Role vào máy chủ EC2.
  6. Triển khai kiến trúc bảo mật không lưu trữ Credentials: Cấu hình cho EC2 tự động truy xuất temporary credentials qua Instance Metadata Service (IMDSv2) để đọc object từ S3, tuyệt đối KHÔNG lưu static Access Key trong file `.env` hay config máy chủ.
  7. Thực hành Failure Injection: Truy vấn S3 từ EC2 khi chưa attach IAM Role $\rightarrow$ bắt lỗi `AccessDenied` / `403 Forbidden`; đính kèm Instance Profile $\rightarrow$ truy vấn S3 thành công tức thì.
  8. Dọn dẹp tài nguyên (Cleanup) triệt để sau lab: Xóa object và delete S3 bucket, terminate EC2 instance và xóa IAM Role/Instance Profile nhằm duy trì chi phí $0.




