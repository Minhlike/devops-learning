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
| Automation & Script| Bash Scripting, Variables & Quoting | Làm được độc lập | 2026-08-10 | Lab 11.1: Viết script `check_endpoint.sh` tự động kiểm tra mã HTTP |
| Automation & Script| Exit Codes (`$?`) & CI/CD `set -e` Safety | Troubleshoot được | 2026-08-10 | Lab 11.2: Kiểm soát Exit Code 0 vs 1 và dùng `set -e` chặn trôi lỗi |
| Automation & Script| Bash Functions, `return` & Control Flow | Troubleshoot được | 2026-08-24 | Lab 12: `check_backup_dir`, `backup_app`; xử lý success/failure path |
| Automation & Script| Bash Loops (`for`, `while read`) | Troubleshoot được | 2026-08-24 | Lab 12: Parse nhiều file log bằng `for`; đọc từng dòng bằng `while read -r` |
| Automation & Script| Log Parsing (`grep`, `$()`) | Troubleshoot được | 2026-08-24 | `parse_log.sh`: đếm ERROR/HTTP 500 và xử lý hàng loạt file log |
| Automation & Script| Automated Backup (`tar`, timestamp) | Troubleshoot được | 2026-08-24 | `backup_app.sh`: backup timestamp, validation và kiểm tra exit status của `tar` |
| Automation & Script| Safe File Cleanup (`find`, `-mtime`, safety guard) | Troubleshoot được | 2026-08-24 | `clean_old_backups.sh`: cleanup >7 ngày và Failure Injection chống sai path |
| Automation & Script| Python File & Log Handling (`pathlib`, `glob`) | Làm được độc lập | 2026-08-29 | Lab 13: `read_log.py`, `health_report.py`, lọc ERROR và HTTP 500 |
| Automation & Script| Python JSON Reporting (`dict`, `json.dump`) | Làm được độc lập | 2026-08-29 | Lab 13: Tổng hợp dict và xuất file `health_report.json` |
| Automation & Script| Python System Commands (`subprocess.run`, `sys.exit`) | Troubleshoot được | 2026-08-29 | Lab 13: `check_command.py`, xử lý returncode non-zero & missing executable |
| Containers & Cloud| Docker Engine & WSL Integration | Làm được độc lập | 2026-08-29 | Lab 14: Cài đặt và vận hành Docker Engine native trên Ubuntu 24.04 WSL |
| Containers & Cloud| Container Lifecycle (`run`, `start`, `stop`, `exec`, `rm`, PID 1) | Làm được độc lập | 2026-08-29 | Lab 14: Quản lý vòng đời container và PID 1 |
| Containers & Cloud| Docker Storage & Persistence (Named Volumes) | Làm được độc lập | 2026-08-29 | Lab 14: Writable layer vs Named Volumes duy trì dữ liệu bền vững |
| Containers & Cloud| Docker Networking & Port Publishing | Troubleshoot được | 2026-08-29 | Lab 14: Port publishing `HOST:CONTAINER`, Bridge network & Docker DNS |
| Containers & Cloud| Dockerfile Building & Versioning (`.dockerignore`) | Làm được độc lập | 2026-08-29 | Lab 14: Build context, layers cache, `my-web:v1/v2`, `CMD` vs `ENTRYPOINT` |
| Containers & Cloud| Docker Troubleshooting (`logs`, `inspect`, `top`, Failure Injections)| Troubleshoot được | 2026-08-29 | Lab 14: Chẩn đoán lỗi build-time, status Created/Exited + ExitCode |
| Containers & Cloud| Docker Compose Fundamentals (`compose.yaml`, `services`, `build`) | Làm được độc lập | 2026-08-30 | Lab 15: Định nghĩa Flask App + PostgreSQL trong `compose.yaml` |
| Containers & Cloud| Docker Compose Networking & Service-Name DNS | Làm được độc lập | 2026-08-30 | Lab 15: Phân giải hostname theo Service Name (`db`) trong Compose Network |
| Containers & Cloud| Docker Healthcheck & `depends_on` (service_healthy) | Troubleshoot được | 2026-08-30 | Lab 15: Cấu hình `healthcheck` pg_isready và `depends_on` chờ DB ready |
| Containers & Cloud| Docker Compose Volume Persistence & Data Safety | Troubleshoot được | 2026-08-30 | Lab 15: Named volume persistence, phân biệt `down` vs `down -v` gây mất data |
| Containers & Cloud| Secrets & Environment Variable Management (`.env`, `.gitignore`)| Làm được độc lập | 2026-08-30 | Lab 15: Quản lý biến môi trường bằng `.env`, tạo `.env.example`, gitignore `.env` |
| Containers & Cloud| Multi-Container Troubleshooting & Failure Injections | Troubleshoot được | 2026-08-30 | Lab 15: Sửa lỗi DNS resolution (`DB_HOST`), DB auth (`DB_PASSWORD`), syntax YAML |
| Containers & Cloud| Production WSGI & Process Supervision (Gunicorn Worker Management) | Làm được độc lập | 2026-08-31 | Lab 16: Gunicorn master + 2 workers, tự spawn worker mới khi process bị kill |
| Containers & Cloud| Container PID 1 & Auto-Restart Policies (`restart: unless-stopped`) | Troubleshoot được | 2026-08-31 | Lab 16: Kill PID 1, Docker tự restart container, xác minh RestartCount tăng |
| Containers & Cloud| Advanced Container Healthchecks & Status Monitoring (`Up` vs `Healthy`) | Troubleshoot được | 2026-08-31 | Lab 16: Endpoint `/health`, phân biệt Up vs Healthy, unhealthy không trigger restart |
| Containers & Cloud| Container Resource Limits & OOM Killer (`cpus`, `mem_limit`, `memswap_limit`)| Troubleshoot được | 2026-08-31 | Lab 16: CPU throttle ~50%, OOM kill 300MiB process, exit code 137, OOMKilled=true |
| Containers & Cloud| Graceful Shutdown & Signal Handling (`SIGTERM`, `Exited (0)`) | Làm được độc lập | 2026-08-31 | Lab 16: `docker compose stop app`, Gunicorn bắt SIGTERM, shutdown sạch sẻ |
| Containers & Cloud| Container Registry Operations (Docker Hub Login, Tag, Push, Pull) | Làm được độc lập | 2026-09-04 | Lab 17: Push image `minhhociot/docker-capstone:v1` lên Docker Hub & pull deploy |
| Containers & Cloud| Image Immutability & Registry Digest Verification | Làm được độc lập | 2026-09-04 | Lab 17: Kiểm tra digest `sha256:6823...` qua `docker inspect` và RepoDigest |
| Containers & Cloud| Docker Compose Image Deployment (Decoupled Build & Deploy) | Làm được độc lập | 2026-09-04 | Lab 17: Chuyển `compose.yaml` từ `build: ./app` sang `image: registry/repo:tag` |
| Containers & Cloud| End-to-End Docker Capstone Architecture (App + DB + Persistence + Health) | Mastery | 2026-09-04 | Lab 17: Capstone Flask API + PostgreSQL + Volume persistence + Healthchecks |
| Networking | IP Address, CIDR Notation (`/20`, `/24`), Interfaces | Làm được độc lập | 2026-08-07 | Lab 7.1: Đọc thông số card `lo`, `eth0`, IP `172.19.132.120/20` từ `ip a` |
| Networking | Port Inspection (`ss -tulpn`, TCP/UDP) | Troubleshoot được | 2026-08-07 | Incident 7.2: Tìm PID `1252` ngốn Port 8080 và giải phóng bằng `kill -9` |
| Networking | Nginx Reverse Proxy & `proxy_pass` | Làm được độc lập | 2026-08-07 | Lab 7.3: Cấu hình Nginx reverse proxy Port 8080 sang Python Backend 8000 |
| Networking | HTTP Status Codes, Headers & `curl -v` | Làm được độc lập | 2026-08-08 | Lab 8.1: Soi chi tiết Request/Response Headers bằng `curl -v` |
| Networking | DNS Records & Resolution (`dig`, `bind9-dnsutils`) | Làm được độc lập | 2026-08-08 | Lab 8.1: Tra cứu A Record và DNS `google.com` bằng `dig` |
| Networking | Network Packet Capture (`tcpdump`) | Làm được độc lập | 2026-08-08 | Lab 9.1: Bắt gói tin TCP 3-Way Handshake SYN/SYN-ACK/ACK bằng `tcpdump` |
| Architecture | Mermaid Architecture Diagramming | Làm được độc lập | 2026-08-08 | Phase 2 Exam: Vẽ sơ đồ luồng Request End-to-End tại `docs/architecture-phase2.md` |
| Version Control| Feature Branching & `.gitignore` | Làm được độc lập | 2026-08-08 | Lab 10.1: Cấu hình `.gitignore` bảo vệ `.env`, tạo branch `feature/port-8080` |
| Version Control| Git Merge Conflict Resolution | Troubleshoot được | 2026-08-08 | Lab 10.2: Đọc dải đụng độ `< = >`, tự sửa conflict và commit merge |
| Version Control| Semantic Versioning & Release Tags (`git tag`)| Làm được độc lập | 2026-08-08 | Đánh tag `v1.0.0` và push thành công lên GitHub `Minhlike/devops-learning` |
| Troubleshooting | HTTP 502 Bad Gateway Incident Response | Troubleshoot được | 2026-08-08 | Incident 8.2 & Exam Phase 2: Đọc log `Connection refused` và sửa lỗi 502 |
| Technical English| Reading Documentation | Làm được độc lập | 2026-07-30 | Diagnostic Test (Tốt) |
| CI/CD & Automation | GitHub Actions Workflow Syntax (`name`, `on`, `jobs`, `steps`, `uses`, `run`) | Làm được độc lập | 2026-09-08 | Lab 18: Viết `.github/workflows/ci.yml` chuẩn cú pháp YAML |
| CI/CD & Automation | Multi-Job Pipeline & Dependencies (`needs: test`) | Làm được độc lập | 2026-09-08 | Lab 18: Cấu hình `build-and-push` phụ thuộc kết quả `test` (Fail-Fast) |
| CI/CD & Automation | Modern Python Linting (`ruff check`) | Làm được độc lập | 2026-09-08 | Lab 18: Tích hợp Ruff (Rust) quét mã nguồn tĩnh và chuẩn PEP 8 |
| CI/CD & Automation | GitHub Repository Secrets Management (`DOCKER_HUB_*`) | Làm được độc lập | 2026-09-08 | Lab 18: Quản lý và bảo vệ an toàn Docker Hub Personal Access Token |
| CI/CD & Automation | Automated Docker Build & Registry Push (`docker/build-push-action`) | Làm được độc lập | 2026-09-08 | Lab 18: Tự động build và push `minhhociot/devops-lab18` với tag kép `:latest` & `:${{ github.sha }}` |
| CI/CD & Automation | CI/CD Failure Injections & Log Diagnostics | Troubleshoot được | 2026-09-08 | Lab 18: Xử lý lỗi Ruff `I001`, AssertionError, Registry 401, Dockerfile missing |
| CI/CD & Automation | GitHub Actions Matrix Strategy (`strategy.matrix`) | Làm được độc lập | 2026-09-09 | Lab 19: Chạy song song test trên Python 3.10, 3.11, 3.12 |
| CI/CD & Automation | Python Multi-Version Compatibility Testing | Làm được độc lập | 2026-09-09 | Lab 19: Xác minh tương thích app trên nhiều runtime Python độc lập |
| CI/CD & Automation | Matrix Execution & Fail-Fast Control (`fail-fast: false`) | Làm được độc lập | 2026-09-09 | Lab 19: Giữ các job matrix khác tiếp tục chạy khi 1 job bị fail |
| CI/CD & Automation | pip Dependency Caching (`actions/setup-python`) | Làm được độc lập | 2026-09-09 | Lab 19: Cache package pip theo hash file requirements.txt tối ưu CI time |
| CI/CD & Automation | Test Coverage & Quality Gate (`coverage --fail-under=80`) | Làm được độc lập | 2026-09-09 | Lab 19: Tự động chặn CI nếu độ bao phủ mã nguồn dưới ngưỡng 80% |
| CI/CD & Automation | GitHub Actions Artifacts (`actions/upload-artifact@v4`) | Làm được độc lập | 2026-09-09 | Lab 19: Đóng gói và lưu trữ báo cáo coverage xml cho từng matrix job |
| CI/CD & Automation | GitHub Branch Rulesets & Branch Protection | Làm được độc lập | 2026-09-09 | Lab 19: Thiết lập ruleset bảo vệ main, chặn force push, yêu cầu PR |
| CI/CD & Automation | Required Status Checks & Pull Request CI Gate | Làm được độc lập | 2026-09-09 | Lab 19: Bắt buộc 3 checks Matrix test pass mới cho phép merge PR #1 |
| CI/CD & Automation | Conditional Deployment by Branch (`github.ref`, `event_name`) | Làm được độc lập | 2026-09-09 | Lab 19: Chỉ kích hoạt build-and-push khi push vào main, feature chỉ CI |
| CI/CD & Automation | CI Failure Injection & Threshold Gate Recovery | Troubleshoot được | 2026-09-09 | Lab 19: Inject lỗi threshold 101% chặn merge PR, khôi phục 80% mở khóa CI |
| CI/CD & Automation | GitHub Deployment Environments (`staging`, `production`) | Làm được độc lập | 2026-09-09 | Lab 20: Thiết lập và phân tách cấu hình môi trường staging và production |
| CI/CD & Automation | Deployment Protection Rules & Manual Approval Gate | Làm được độc lập | 2026-09-09 | Lab 20: Cấu hình Required Reviewers chặn production chờ phê duyệt thủ công |
| CI/CD & Automation | Multi-Stage Deployment Pipeline (Staging $\rightarrow$ Production) | Làm được độc lập | 2026-09-09 | Lab 20: Chuỗi pipeline test matrix $\rightarrow$ build $\rightarrow$ staging $\rightarrow$ prod |
| CI/CD & Automation | Post-Deployment Automated Smoke Testing (`curl /health`) | Làm được độc lập | 2026-09-09 | Lab 20: Tự động kiểm tra endpoint `/health` sau khi deploy từng môi trường |
| CI/CD & Automation | Immutable Artifact Tagging (`${{ github.sha }}`) | Làm được độc lập | 2026-09-09 | Lab 20: Dùng commit SHA bất biến cho image tag, tránh rủi ro của tag `latest` |
| CI/CD & Automation | Container Image Promotion (`:stable` tag) | Làm được độc lập | 2026-09-09 | Lab 20: Promote image đạt chuẩn production smoke test thành tag `stable` |
| CI/CD & Automation | Manual Workflow Trigger (`workflow_dispatch`) | Làm được độc lập | 2026-09-09 | Lab 20: Kích hoạt pipeline thủ công trên GitHub UI với input boolean `rollback` |
| CI/CD & Automation | Production Rollback Automation & Disaster Recovery | Troubleshoot được | 2026-09-09 | Lab 20: Rollback kéo image `:stable`, smoke test và dọn dẹp (Run #28 SUCCESS) |
| CI/CD & Automation | Conditional Job Skip & Workflow Branching Control | Làm được độc lập | 2026-09-09 | Lab 20: Phân luồng điều kiện bỏ qua build/staging khi rollback=true |
| CI/CD & Automation | Python SAST Security Scanning (`bandit`) | Troubleshoot được | 2026-09-10 | Lab 21: Quét mã tĩnh Bandit phát hiện và loại bỏ insecure host binding 0.0.0.0 |
| CI/CD & Automation | Secret Detection with Gitleaks (`gitleaks-action`) | Làm được độc lập | 2026-09-10 | Lab 21: Quét toàn bộ Git history (`fetch-depth: 0`) phát hiện secret leak |
| Version Control | Git History Secret Remediation | Troubleshoot được | 2026-09-10 | Lab 21: Loại bỏ secret khỏi Git history bằng commit rewrite và force-with-lease |
| CI/CD & Automation | Docker Image CVE Scanning with Trivy (`aquasecurity/trivy-action`) | Làm được độc lập | 2026-09-10 | Lab 21: Quét lỗ hổng container trước khi push, chặn HIGH/CRITICAL với exit-code 1 |
| CI/CD & Automation | DevSecOps Multi-Stage Security Gates | Làm được độc lập | 2026-09-10 | Lab 21: Tích hợp chốt chặn SAST, Secret và Container Vulnerabilities vào CI/CD |
| CI/CD & Automation | Conventional Commits Specification | Làm được độc lập | 2026-09-10 | Lab 21: Chuẩn hóa commit format (`feat:`, `fix:`, `chore:`) phục vụ automation |
| CI/CD & Automation | Automated Semantic Versioning (SemVer) | Làm được độc lập | 2026-09-10 | Lab 21: Tự động tính toán bump version (`1.0.0` $\rightarrow$ `1.1.0`) từ commit history |
| CI/CD & Automation | Automated Release Management (`google-github-actions/release-please-action`) | Làm được độc lập | 2026-09-10 | Lab 21: Tích hợp Release Please manifest mode, tự động tạo Release PR #8 |
| CI/CD & Automation | GitHub Release, Tag & Changelog Automation | Làm được độc lập | 2026-09-10 | Lab 21: Tự động sinh CHANGELOG.md, cập nhật version.txt, tạo tag/release `v1.1.0` |
| CI/CD & Automation | End-to-End CI/CD + Security + Deployment Pipeline | Làm được độc lập | 2026-09-10 | Lab 21: Vận hành toàn diện luồng Test $\rightarrow$ Security Gates $\rightarrow$ Build $\rightarrow$ Trivy $\rightarrow$ Registry $\rightarrow$ Staging $\rightarrow$ Manual Approval $\rightarrow$ Prod $\rightarrow$ Release |


