# NEXT SESSION PLAN

- **Buổi học tiếp theo:** BUỔI 27 — PHASE 6: AWS DNS, Route 53 & HTTPS/TLS Fundamentals.
- **Mục tiêu Buổi 27:**
  1. Hiểu nền tảng hệ thống phân giải tên miền (DNS): Bản chất DNS, Domain Name, Root Servers, TLD, Authoritative Name Servers, DNS Query Resolution Flow.
  2. Nắm vững dịch vụ Amazon Route 53: Public Hosted Zones vs Private Hosted Zones.
  3. Phân biệt và thực hành các loại bản ghi DNS cốt lõi:
     - Record `A` (IPv4 address).
     - Record `CNAME` (Canonical Name - trỏ domain tới domain).
     - Record `Alias` (Tính năng độc quyền của Route 53: Trỏ trực tiếp domain apex tới AWS resources như ALB mà không bị giới hạn như CNAME).
  4. Hiểu các chính sách định tuyến Route 53 Routing Policies: Simple Routing, Weighted Routing, Latency-based Routing, Failover Routing và Health Checks.
  5. Bảo mật truyền thông với HTTPS/TLS & AWS Certificate Manager (ACM):
     - Hiểu nguyên lý mã hóa đối xứng, bất đối xứng, chứng chỉ SSL/TLS và CA (Certificate Authority).
     - Đăng ký và xác thực SSL/TLS Certificate miễn phí qua ACM (DNS Validation qua Route 53).
  6. Tích hợp HTTPS vào Application Load Balancer:
     - Cấu hình HTTPS Listener (Cổng 443) gắn SSL Certificate từ ACM.
     - Thiết lập HTTP to HTTPS Redirection (Tự động chuyển hướng toàn bộ traffic HTTP cổng 80 sang HTTPS cổng 443).
     - Đạt được luồng bảo mật End-to-End: Người dùng truy cập domain với HTTPS bảo mật hoàn toàn.
  7. Thực hành Failure Injection: Truy cập HTTP và kiểm chứng hành vi redirect 301 sang HTTPS; kiểm tra bảo mật certificate bằng `curl -v` hoặc trình duyệt.
  8. Vận hành nguyên tắc Cost Safety nghiêm ngặt và dọn dẹp sạch toàn bộ tài nguyên (Route 53 records/hosted zone, ACM certificates, ALB listeners) sau bài lab.
- **Yêu cầu phương pháp giảng dạy S27:**
  - Tiếp tục duy trì nguyên tắc **Architecture-First**: Giải thích sơ đồ luồng phân giải DNS và luồng bắt tay TLS (TLS Handshake) trước khi bắt tay cấu hình tài nguyên.
  - Hướng dẫn chi tiết, rõ ràng từng bước, tối ưu lệnh CLI và đảm bảo không phát sinh chi phí ngoài ý muốn.







