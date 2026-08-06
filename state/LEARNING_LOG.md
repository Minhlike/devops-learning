# LEARNING LOG

## [2026-07-30] Session 1: Onboarding & Diagnostic Test
- Khởi tạo quy trình Persistent Memory Protocol và cấu hình trạng thái tại `D:\Devops\state\`.
- Học viên hoàn thành 34 câu hỏi kiểm tra đầu vào (Diagnostic Test). Kết quả: 18.5/34 câu.

## [2026-07-31] Session 1: WSL2 Setup, Linux CLI Basics & First Git Push
- Xử lý lỗi hỏng đĩa ảo WSL cũ bằng cách chuyển sang `Ubuntu-24.04` thành công.
- Thực hành thao tác Terminal Linux cơ bản, sinh SSH key Ed25519, commit & push thành công kho Git `Minhlike/devops-learning`.

## [2026-07-31] Session 2: Linux Filesystem Hierarchy & Advanced CLI Commands
- Trả lời đúng 100% phần Ôn tập Recall. Khám phá `/etc`, `/var/log`, `/proc`, dùng Pipe `|`.
- Dựng cấu trúc thư mục ứng dụng 3-tier sản xuất, commit và push thành công bài lab `lab-02-structure` lên GitHub.

## [2026-08-01] Session 3: Linux File Permissions & User/Group Management
- Trả lời đúng 100% bài kiểm tra kiến thức cũ. Nắm vững phân quyền (u, g, o), (r=4, w=2, x=1) và con số Octal `755`, `644`, `600`.
- Khắc phục lỗi `Permission Denied` (`chmod +x`) và sự cố SSH Private Key (`chmod 600`).
- Commit và push bài lab `lab-03-permissons` lên GitHub.

## [2026-08-01] Session 4: Linux Process & Service Management (systemd, Nginx, Journalctl)
- Thực hành tra cứu PID và tiêu diệt tiến trình `kill -9`. Cài đặt Nginx Web Server.
- Thực hành Incident Response Nginx config sai syntax. Xử lý sự cố khôi phục Nginx bằng `apt purge` và `apt install`.
- Tổ chức phiên Masterclass Syntax Linux CLI và xuất bản tài liệu PDF Cheat Sheet `LINUX_DEVOPS_CHEATSHEET.pdf`.

## [2026-08-02] Session 5: Resource Monitoring, Disk Full Incident & Cron Automation
- Trả lời đúng 100% bài kiểm tra kiến thức cũ.
- Thực hành đọc chỉ số dung lượng đĩa `df -h`, bộ nhớ RAM `free -h` và chỉ số `uptime` (Load Average).
- Giải quyết bài lab Failure Injection: Dùng `du -sh * | sort -rh` khoanh vùng và tiêu diệt file log rác phình to 200MB.
- Tự phát hiện và sửa lỗi gõ nhầm đường dẫn trong script `check_disk.sh` (`lab-5-resources` vs `lab-05-resources`).
- Thiết lập Cron Job (`crontab`) tự động hóa kiểm tra ổ đĩa mỗi phút và kiểm chứng thành công.
- Nắm vững khái niệm Log Rotation (`logrotate`, `rotate`, `compress`).
- Commit và push bài lab `lab-05-resources` lên GitHub `Minhlike/devops-learning`.
