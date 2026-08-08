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
| Networking | IP Address, CIDR Notation (`/20`, `/24`), Interfaces | Làm được độc lập | 2026-08-07 | Lab 7.1: Đọc thông số card `lo`, `eth0`, IP `172.19.132.120/20` từ `ip a` |
| Networking | Port Inspection (`ss -tulpn`, TCP/UDP) | Troubleshoot được | 2026-08-07 | Incident 7.2: Tìm PID `1252` ngốn Port 8080 và giải phóng bằng `kill -9` |
| Networking | Nginx Reverse Proxy & `proxy_pass` | Làm được độc lập | 2026-08-07 | Lab 7.3: Cấu hình Nginx reverse proxy Port 8080 sang Python Backend 8000 |
| Networking | HTTP Status Codes, Headers & `curl -v` | Làm được độc lập | 2026-08-08 | Lab 8.1: Soi chi tiết Request/Response Headers bằng `curl -v` |
| Networking | DNS Records & Resolution (`dig`, `bind9-dnsutils`) | Làm được độc lập | 2026-08-08 | Lab 8.1: Tra cứu A Record và DNS `google.com` bằng `dig` |
| Networking | Network Packet Capture (`tcpdump`) | Làm được độc lập | 2026-08-08 | Lab 9.1: Bắt gói tin TCP 3-Way Handshake SYN/SYN-ACK/ACK bằng `tcpdump` |
| Architecture | Mermaid Architecture Diagramming | Làm được độc lập | 2026-08-08 | Phase 2 Exam: Vẽ sơ đồ luồng Request End-to-End tại `docs/architecture-phase2.md` |
| Troubleshooting | HTTP 502 Bad Gateway Incident Response | Troubleshoot được | 2026-08-08 | Incident 8.2 & Exam Phase 2: Đọc log `Connection refused` và sửa lỗi 502 |
| Troubleshooting | Multi-Incident Exam & Postmortem Report | Troubleshoot được | 2026-08-08 | Phase 2 Exam: Sửa lỗi mạng, vẽ sơ đồ Mermaid & viết Postmortem Report trên GitHub |
| Version Control| Git Config & SSH Key | Làm được độc lập | 2026-07-31 | Sinh SSH key Ed25519, add GitHub, test `ssh -T` thành công |
| Version Control| Git Local & Remote (init, commit, push) | Làm được độc lập | 2026-08-08 | Commit & push thành công bài exam và postmortem report Phase 2 lên GitHub |
| Technical English| Reading Documentation | Làm được độc lập | 2026-07-30 | Diagnostic Test (Tốt) |
