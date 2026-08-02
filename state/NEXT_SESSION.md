# NEXT SESSION PLAN

- **Buổi học tiếp theo:** BUỔI 5 — PHASE 1: Quản lý Tài nguyên (Resource Management), Tự động hóa Cron & Log Rotation.
- **Mục tiêu:**
  1. Giám sát chuyên sâu tài nguyên CPU, Memory, Swap, Disk và Load Average (`top`, `htop`, `df -h`, `du -sh`, `free -m`).
  2. Phân tích nguyên nhân sự cố đĩa bị đầy (Disk Full) và tiến trình ngốn CPU / Memory.
  3. Lập lịch tự động hóa công việc với Cron Job (`crontab -e`, cú pháp 5 dấu sao `* * * * *`).
  4. Quản lý xoay vòng file log ứng dụng với `logrotate` để tránh tràn đĩa cứng.
  5. Giải quyết bài lab sự cố đĩa đầy và tạo Cron Job tự động kiểm tra disk space.
