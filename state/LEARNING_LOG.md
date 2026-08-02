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

## [2026-08-01] Session 4: Linux Process & Service Management & Masterclass Syntax
- Trả lời đúng 100% bài kiểm tra kiến thức cũ.
- Thực hành tra cứu PID và tiêu diệt tiến trình bị treo bằng `kill -9`.
- Cài đặt, vận hành Web Server Nginx bằng `apt` và `systemctl`. Test HTTP OK bằng `curl -I`.
- Thực hành sự cố Incident Response: Đọc log bằng `journalctl -u nginx` và `nginx -t`.
- Xử lý thành công sự cố khôi phục Nginx bằng `apt purge` và `apt install`.
- Tổ chức phiên Masterclass giải mã Ngữ pháp cú pháp Linux CLI (Command, Options/Flags, Arguments, I/O Redirection, Pipes).
- Đóng gói và xuất bộ tài liệu **Cheat Sheet Linux & DevOps Cốt lõi** dạng PDF (`LINUX_DEVOPS_CHEATSHEET.pdf`) và Markdown (`LINUX_DEVOPS_CHEATSHEET.md`).
- Kết thúc Buổi 4.
