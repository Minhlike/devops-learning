# CURRENT LEARNING PHASE

- **Current Phase:** PHASE 1 — Linux nền tảng và quản trị hệ thống
- **Current Status:** Hoàn thành Buổi 4 (Process & Service Management). Chuẩn bị Buổi 5 (Resource Management, Package & System Logs: CPU, RAM, Swap, Disk, Load Average, cron, logrotate).
- **Current Week:** Tuần 1
- **Completed Outputs:**
  1. Sử dụng thành thạo `ps aux`, `grep` để tìm PID và tiêu diệt tiến trình bị treo bằng `kill -9`.
  2. Cài đặt và vận hành Nginx Web Server bằng `apt` và `systemctl`.
  3. Kiểm tra phản hồi HTTP bằng `curl -I http://localhost`.
  4. Sử dụng `journalctl -u nginx` và `nginx -t` để chẩn đoán nguyên nhân sự cố cấu hình bị sai cú pháp.
  5. Nắm vững kỹ thuật khôi phục file cấu hình hệ thống bằng `apt purge` và `apt install`.
  6. Viết script `check_service.sh` kiểm tra trạng thái dịch vụ và push bài lab `lab-04-services` lên GitHub.
