# CURRENT LEARNING PHASE

- **Current Phase:** PHASE 1 — Linux nền tảng và quản trị hệ thống
- **Current Status:** Hoàn thành Buổi 5 (Resource Management, Disk Full Incident, Cron Automation & Log Rotation). Chuẩn bị Buổi 6 (Package Management, Log Rotation thực hành & Bài kiểm tra cuối Phase 1).
- **Current Week:** Tuần 1
- **Completed Outputs:**
  1. Giám sát chuyên sâu dung lượng đĩa `df -h`, bộ nhớ RAM `free -h` và chỉ số `uptime` (Load Average).
  2. Xử lý thành công bài lab Failure Injection: Dùng `du -sh * | sort -rh` khoanh vùng và tiêu diệt file log rác phình to 200MB.
  3. Viết script `check_disk.sh` ghi nhận thời gian và trạng thái đĩa.
  4. Lập lịch tự động hóa Cron Job (`crontab`) chạy script mỗi phút thành công.
  5. Nắm vững khái niệm Log Rotation (`logrotate`, `rotate`, `compress`).
  6. Commit và push bài lab `lab-05-resources` lên GitHub `Minhlike/devops-learning`.
