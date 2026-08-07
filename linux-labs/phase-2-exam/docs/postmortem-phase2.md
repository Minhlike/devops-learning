# INCIDENT POSTMORTEM REPORT — PHASE 2 NETWORKING EXAM

- **Ngày xảy ra sự cố:** 2026-08-08
- **Người xử lý (On-Call Engineer):** Minh (DevOps Candidate)
- **Mức độ nghiêm trọng:** High (Dịch vụ Web Nginx trả về lỗi HTTP 502 Bad Gateway)

## 1. TRIỆU CHỨNG (SYMPTOMS)
- Người dùng truy cập `http://localhost:8080` nhận được mã lỗi `HTTP 502 Bad Gateway`.

## 2. NGUYÊN NHÂN GỐC (ROOT CAUSE)
1. Cấu hình Nginx `/etc/nginx/conf.d/exam_phase2.conf` bị trỏ nhầm `proxy_pass` sang Port 8005.
2. Tiến trình Python Backend ở Port 8000 bị ngắt ngầm.

## 3. QUÁ TRÌNH KHẮC PHỤC (REMEDIATION STEPS)
1. Đọc log `/var/log/nginx/error.log` phát hiện Nginx không nối được tới IP `127.0.0.1:8005`.
2. Sửa lại `proxy_pass` trong `/etc/nginx/conf.d/exam_phase2.conf` về đúng port `8000`.
3. Reload Nginx bằng `sudo systemctl reload nginx`.
4. Bật lại ứng dụng Python backend ở Port 8000 (`python3 -m http.server 8000 &`).
5. Dùng `curl -I http://localhost:8080` xác nhận khôi phục thành công `HTTP 200 OK`.

## 4. BIỆN PHÁP PHÒNG TRÁNH (PREVENTATIVE ACTIONS)
- Tự động hóa kiểm tra Port đang lắng nghe bằng script `check_ports.sh` trước khi deploy.
- Sử dụng `systemctl` hoặc Docker để tự động restart ứng dụng Backend nếu bị crash.
