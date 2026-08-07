# CURRENT LEARNING PHASE

- **Current Phase:** PHASE 2 — Mạng Máy Tính Dành Cho DevOps
- **Current Status:** Hoàn thành Buổi 7 (Networking Fundamentals, IP/CIDR, Port Troubleshooting & Nginx Reverse Proxy). Chuẩn bị Buổi 8 (HTTP/HTTPS Deep-Dive, DNS Resolution, cURL Advanced & Firewall Configuration).
- **Current Week:** Tuần 2
- **Completed Outputs:**
  1. Nắm vững bản chất địa chỉ IPv4, Subnet Mask, Ký hiệu CIDR (`/20`, `/24`) và phân biệt IP Public vs Private.
  2. Sử dụng công cụ `ip a`, `ping -c 4` kiểm tra Card mạng (`lo`, `eth0`) và thông mạng Internet.
  3. Thành thạo công cụ `sudo ss -tulpn` kiểm tra các Cổng (Port) đang lắng nghe trên server.
  4. Thực hành bài lab Failure Injection 7.2: Khoanh vùng và tiêu diệt tiến trình chiếm dụng Port 8080 bằng `kill -9`.
  5. Cấu hình Nginx làm Reverse Proxy tiếp nhận HTTP Request ở Port 8080 và chuyển tiếp (`proxy_pass`) tới ứng dụng Python Backend ở Port 8000.
  6. Viết script `check_ports.sh`, commit và push bài lab `lab-07-networking` lên GitHub `Minhlike/devops-learning`.
