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
- Trực tiếp đọc chỉ số dung lượng đĩa `df -h`, bộ nhớ RAM `free -h` và `uptime`.
- Giải quyết bài lab Failure Injection: Dùng `du -sh * | sort -rh` khoanh vùng và tiêu diệt file log rác phình to 200MB.
- Thiết lập Cron Job (`crontab`) tự động hóa kiểm tra ổ đĩa mỗi phút và kiểm chứng thành công.
- Commit và push bài lab `lab-05-resources` lên GitHub.

## [2026-08-07] Session 6: Phase 1 Failure Injection Exam & Graduation
- Học viên hoàn thành Bài kiểm tra Cuối Phase 1: Xử lý độc lập 3 sự cố đồng thời.
- Viết Báo cáo Sự cố Incident Postmortem Report đầu tiên tại `docs/postmortem-phase1.md`.
- Kết quả Đánh giá Phase 1: **100 / 100 điểm** (ĐẠT VỮNG PHASE 1).

## [2026-08-07] Session 7: Phase 2 Networking Fundamentals & Nginx Reverse Proxy
- Soi Card mạng `lo`, `eth0`, IP Private `172.19.132.120/20` bằng `ip a`, giám sát Port `sudo ss -tulpn`.
- Cấu hình Nginx làm Reverse Proxy tiếp nhận Request Port 8080 và chuyển tiếp (`proxy_pass`) tới Python Backend Port 8000.
- Commit và push bài lab `lab-07-networking` lên GitHub.

## [2026-08-08] Session 8: HTTP Status Codes, DNS Resolution & 502 Bad Gateway Incident
- Soi chi tiết Request/Response Headers bằng `curl -v http://localhost`. Tra cứu DNS bằng `dig google.com +short`.
- Giải quyết thành công sự cố Failure Injection 8.2: Phát hiện lỗi `HTTP 502 Bad Gateway` do Backend Python bị sụp, đọc log `Connection refused` từ `/var/log/nginx/error.log` và khôi phục dịch vụ về `200 OK`.
- Commit và push bài lab `lab-08-http-dns` lên GitHub.

## [2026-08-08] Session 9: Packet Capture tcpdump, Mermaid Architecture Diagram & Phase 2 Graduation
- Bắt và giải mã trực tiếp các gói tin TCP 3-Way Handshake (SYN / SYN-ACK / ACK) bằng `sudo tcpdump -i lo port 80`.
- Tạo Sơ đồ Kiến trúc Mermaid tại `docs/architecture-phase2.md` và Báo cáo Postmortem tại `docs/postmortem-phase2.md`.
- Kết quả Đánh giá Phase 2: **100 / 100 điểm** (ĐẠT VỮNG PHASE 2).

## [2026-08-08] Session 10: Advanced Git Workflow, .gitignore, Merge Conflict & Tagging
- Cấu hình `.gitignore` chặn rò rỉ Secret `.env`, log rác `*.log` và cache `__pycache__/`.
- Thực hành bài lab Failure Injection 10.2: Tự kích hoạt đụng độ `CONFLICT (content): Merge conflict in app_setting.txt` và tự xử lý conflict bằng CLI.
- Đánh nhãn phiên bản Semantic Versioning `v1.0.0` và push tag lên GitHub.

## [2026-08-10] Session 11: Bash Scripting Fundamentals, Variables, Conditionals & Exit Codes
- Trả lời đúng 100% bài kiểm tra kiến thức cũ.
- Tự tay viết Pseudocode (Mã giả) chuẩn logic lập trình trước khi viết mã nguồn Bash.
- Lập trình thành công script `check_endpoint.sh` tự động kiểm tra mã phản hồi HTTP và trích xuất Exit Code `$?` (0 vs 1).
- Thực hành bài lab Failure Injection 11.2: Sử dụng cờ `set -e` để chặn trôi lỗi trong Bash script cho Pipeline CI/CD.
- Commit và push bài lab `lab-11-bash` lên GitHub `Minhlike/devops-learning`.

## [2026-08-24] Session 12: Bash Advanced Automation, Log Parsing & Safe Cleanup
- Viết và kiểm thử `backup_app.sh` tự động tạo archive `.tar.gz` với timestamp.
- Dùng Functions, `return`, `exit`, `if` và kiểm thử cả success path lẫn failure path.
- Phát hiện hiện tượng `tar` thất bại nhưng script vẫn báo thành công do lệnh `echo` cuối trả Exit Code `0`; sửa bằng kiểm tra trực tiếp exit status của `tar`.
- Viết `parse_log.sh` dùng `grep -c`, command substitution `$()`, vòng lặp `for` xử lý nhiều log và `while read -r` đọc log từng dòng.
- Viết `clean_old_backups.sh` tìm/xóa file `.tar.gz` cũ hơn 7 ngày bằng `find -mtime +7`.
- Hoàn thành Failure Injection chống xóa nhầm file khi `BACKUP_DIR` bị cấu hình sai.
- Tự sửa lỗi Bash `missing ']'` và troubleshoot lỗi thiếu `$` khiến `BACKUP_FILE` bị hiểu thành chuỗi literal.
- Kết quả: **ĐẠT BUỔI 12**.

## [2026-08-29] Session 13: Python Fundamentals for DevOps Automation
- Viết và hoàn thiện `read_log.py`, `health_report.py`, `check_command.py`.
- Sử dụng `pathlib` (`exists()`, `is_file()`, `read_text()`, `glob()`) thao tác file và kiểm tra đường dẫn an toàn.
- Đọc và phân tích file log tự động lọc chuỗi `ERROR` và mã HTTP `500`.
- Xuất báo cáo cấu trúc JSON qua `dict` và `json.dump()` (`health_report.json`).
- Tương tác hệ thống bằng `subprocess.run()`, xử lý `stdout`, `stderr`, kiểm tra `returncode` và điều khiển mã thoát bằng `sys.exit()`.
- Thực hành Failure Injection: log file bị thiếu, non-zero return code, executable không tồn tại.
- Kết quả: **ĐẠT BUỔI 13**.

## [2026-08-29] Session 14: Docker Fundamentals
- Cài đặt và vận hành Docker Engine native trên Ubuntu 24.04 WSL.
- Phân biệt bản chất Image vs Container, quản lý PID 1 và vòng đời container (`run`, `start`, `stop`, `exec`, `rm`).
- Phân biệt Writable Layer vs xoá/tạo lại container; sử dụng Named Volumes cho Data Persistence.
- Cấu hình Port Publishing `HOST_PORT:CONTAINER_PORT`.
- Nắm vững Bridge Network, hiện tượng Localhost Isolation trong container, tạo User-defined Network và Docker DNS theo Container Name.
- Soạn thảo `Dockerfile`, hiểu Build Context, Image Layers + Cache, versioning `my-web:v1/v2`.
- Cấu hình `.dockerignore` loại bỏ file rác.
- Thực hành Failure Injections: Build-time failure, container start failure (Created), application crash (Exited + ExitCode).
- Chẩn đoán lỗi bằng `docker logs`, `inspect`, `top`.
- Phân biệt cơ chế `CMD` vs `ENTRYPOINT`.
- Kết quả: **ĐẠT BUỔI 14**.

## [2026-08-30] Session 15: Docker Compose & Multi-Container Application
- Thực hành xây dựng và vận hành hệ thống đa container Flask App + PostgreSQL Database bằng Docker Compose (`compose.yaml`).
- Cấu hình Compose Network nội bộ và kiểm chứng cơ chế Docker DNS tự động phân giải IP theo Service Name (`db`).
- Thiết lập `healthcheck` trên container PostgreSQL (`pg_isready`) và sử dụng `depends_on` với `condition: service_healthy` giúp Flask app chờ DB khởi tạo xong mới kết nối.
- Cấu hình Named Volume cho PostgreSQL đảm bảo dữ liệu ghi vào DB không bị mất khi restart hay `docker compose down`.
- Thực hành Failure Injection `docker compose down -v` và hiểu hậu quả của cờ `-v` làm xóa sạch volume dữ liệu.
- Quản lý biến môi trường an toàn với file `.env` và file mẫu `.env.example`; kiểm tra bảo mật đảm bảo `.env` bị chặn bởi `.gitignore`.
- Sử dụng `docker compose config` kiểm tra cú pháp file YAML.
- Thực hành Failure Injections: cấu hình sai `DB_HOST` (gây lỗi DNS resolution), sai `DB_PASSWORD` (gây lỗi PostgreSQL authentication).
- Khắc phục sự cố và phục hồi thành công stack: `app` Up (Port 8086), `db` healthy, `curl http://localhost:8086` trả về `{"database":"...","status":"ok"}`.
- Kết quả: **ĐẠT BUỔI 15**.

## [2026-08-31] Session 16: Advanced Docker Compose & Production Operations
- Nâng cấp ứng dụng Flask từ Development Server sang Production WSGI Server Gunicorn (1 Master + 2 Workers).
- Thực hành Failure Injection kill worker process: Gunicorn master tự động phát hiện và spawn worker mới duy trì tính khả dụng.
- Thêm `restart: unless-stopped` trong `compose.yaml`; kill PID 1 Gunicorn và xác minh Docker tự restart container với `RestartCount` tăng.
- Xây dựng endpoint `/health` và cấu hình Docker `healthcheck` cho container app.
- Phân biệt sâu sắc nguyên lý `Up != Healthy`: cố tình cấu hình sai URL healthcheck khiến container giữ trạng thái `Up` nhưng báo `unhealthy`, hiểu rằng `unhealthy` không tự động kích hoạt `restart` policy.
- Khôi phục URL healthcheck chính xác đưa container về trạng thái `healthy`.
- Cấu hình giới hạn tài nguyên: `cpus: "0.50"`, `mem_limit: 256m`, `memswap_limit: 256m`.
- Kiểm chứng CPU limit bằng `docker stats` (CPU hog bị throttle ở mức 50%) và Memory limit (process xin cấp phát 300 MiB bị OOM kill với exit code 137 và `OOMKilled=true`).
- Kiểm chứng Gunicorn master không bị chết khi worker con bị OOM kill, giúp container giữ tính ổn định.
- Thực hành Graceful Shutdown bằng `docker compose stop app`: Gunicorn master nhận SIGTERM, giải phóng workers và shutdown an toàn với `Exited (0)`.
- Kết quả: **ĐẠT BUỔI 16**.
