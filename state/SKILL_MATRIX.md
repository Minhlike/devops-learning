# SKILL MATRIX

| Skill Area | Specific Skill | Status | Last Verified Date | Evidence / Notes |
| :--- | :--- | :--- | :--- | :--- |
| OS & Computer | Hardware & OS Basics | Làm được độc lập | 2026-07-31 | Diagnostic test + Cài đặt WSL2 Ubuntu 24.04 thành công |
| OS & Computer | Filesystem Mounting (`/mnt/d`) | Làm được độc lập | 2026-07-31 | Lab 1: Truy cập `/mnt/d/Devops`, chạy `pwd`, `ls -la` |
| OS & Computer | Case Sensitivity (ext4 vs NTFS) | Làm được độc lập | 2026-07-31 | Failure Injection 1: Thử `cat` file hoa/thường trên ext4 và NTFS |
| Linux Terminal | Basic Navigation & Commands | Làm được độc lập | 2026-07-31 | Dùng thạo `cd`, `pwd`, `ls -la`, `cat`, `echo`, `rm` |
| Linux Terminal | Filesystem Hierarchy (`/etc`, `/var`, `/proc`)| Làm được độc lập | 2026-07-31 | Lab 2.1: Đọc `/proc/cpuinfo`, `/proc/meminfo`, `/var/log`, `/etc` |
| Linux Terminal | File Management (`mkdir -p`, `cp`, `mv`, `rm -rf`) | Làm được độc lập | 2026-07-31 | Lab 2.2: Dựng cấu trúc thư mục production 3-tier, sửa dư thừa, backup |
| Linux Terminal | File Permissions (`chmod`, octal 755, 644, 600) | Troubleshoot được | 2026-08-01 | Lab 3.2 & 3.3: Sửa lỗi Permission Denied (`chmod +x`) & SSH Key (`chmod 600`) |
| Linux System Admin| User, Group, `sudo`, `chown` | Làm được độc lập | 2026-08-01 | Nắm bản chất root, sudo và đổi owner |
| Linux System Admin| Process Management (`ps`, PID, `kill -9`) | Làm được độc lập | 2026-08-01 | Lab 4.1: Tra cứu PID và tiêu diệt tiến trình `sleep 1000` |
| Linux System Admin| Service Management (`systemctl`, Nginx) | Làm được độc lập | 2026-08-01 | Lab 4.2: Cài đặt, start, status Nginx và test `curl -I` |
| Linux System Admin| Resource Monitoring (`df -h`, `free -m`, `uptime`)| Làm được độc lập | 2026-08-02 | Lab 5.1: Đọc dung lượng đĩa, RAM và Load Average |
| Linux System Admin| Disk Full Troubleshooting (`du -sh * | sort -rh`)| Troubleshoot được | 2026-08-02 | Incident 5.2: Khoanh vùng và tiêu diệt file log rác phình to 200MB |
| Automation & Script| Cron Job Automation (`crontab`) | Làm được độc lập | 2026-08-02 | Lab 5.4: Lập lịch cron `* * * * *` tự động chạy script kiểm tra đĩa |
| Troubleshooting | Systemd & Journalctl Log Analysis | Troubleshoot được | 2026-08-01 | Incident 4.3: Đọc log `journalctl` & `nginx -t`, xử lý lỗi config & khôi phục bằng `apt purge` |
| Troubleshooting | Multi-Incident Exam & Postmortem Report | Troubleshoot được | 2026-08-07 | Phase 1 Exam: Sửa 3 lỗi đồng thời & viết Postmortem Report trên GitHub |
| Version Control| Git Config & SSH Key | Làm được độc lập | 2026-07-31 | Sinh SSH key Ed25519, add GitHub, test `ssh -T` thành công |
| Version Control| Git Local & Remote (init, commit, push) | Làm được độc lập | 2026-08-07 | Commit & push thành công bài exam và postmortem report lên GitHub |
| Technical English| Reading Documentation | Làm được độc lập | 2026-07-30 | Diagnostic Test (Tốt) |
