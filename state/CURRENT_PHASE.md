# CURRENT LEARNING PHASE

- **Current Phase:** PHASE 2 — Mạng Máy Tính Dành Cho DevOps
- **Current Status:** Hoàn thành Buổi 8 (HTTP/HTTPS Deep-Dive, DNS Resolution, cURL Advanced & 502 Bad Gateway Incident). Chuẩn bị Buổi 9 (Network Packet Capture `tcpdump`, Network Architecture Diagramming & Bài kiểm tra cuối Phase 2).
- **Current Week:** Tuần 2
- **Completed Outputs:**
  1. Nắm vững bản chất các mã trạng thái HTTP (2xx, 3xx, 4xx, 5xx), phân biệt sự khác nhau giữa 502 Bad Gateway và 504 Gateway Timeout.
  2. Tra cứu bản ghi A Record, CNAME, NS Record của DNS bằng công cụ `dig`.
  3. Soi quá trình bắt tay TCP, TLS Handshake và Request/Response Headers bằng `curl -v`.
  4. Thực hành sự cố Failure Injection 8.2: Phát hiện lỗi `HTTP 502 Bad Gateway` khi Backend Python bị tắt, đọc chính xác log `connect() failed (111: Connection refused)` từ `/var/log/nginx/error.log` và khôi phục dịch vụ về `200 OK`.
  5. Viết script `check_http_status.sh`, commit và push bài lab `lab-08-http-dns` lên GitHub `Minhlike/devops-learning`.
