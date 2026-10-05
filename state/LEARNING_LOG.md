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

## [2026-09-04] Session 17: Docker Capstone Project & Container Registry Deployment
- Hoàn thành dự án Capstone Phase 4 xây dựng ứng dụng Flask API đếm lượt truy cập (`POST /visits`, `GET /visits`) kết nối PostgreSQL 17 database.
- Đóng gói ứng dụng bằng Dockerfile (`python:3.12-slim`, Gunicorn 2 workers) và cấu hình `.dockerignore`.
- Thiết lập hệ thống đa dịch vụ qua `compose.yaml`: `app` + `db`, Docker DNS nội bộ, `healthcheck` pg_isready, `depends_on: service_healthy`, resource limits (`0.50` CPU, `256m` RAM), `restart: unless-stopped` và port publish `8087:8000`.
- Kiểm tra bảo mật: file `.env` chứa mật khẩu bị chặn bởi `.gitignore`, duy trì file mẫu `.env.example`.
- Kiểm thử chức năng API và chứng minh Data Persistence: thực hiện `docker compose down` xoá container nhưng named volume `db-data` được giữ nguyên; khi dựng lại stack dữ liệu lượt truy cập vẫn nguyên vẹn.
- Đăng nhập Docker Hub (`minhhociot`), đánh tag `minhhociot/docker-capstone:v1`, push image lên Docker Hub và ghi nhận digest `sha256:6823167bb94c7ac57320f69a886e50ebecf53139fd03d8ab8059d9649410b0bc`.
- Xoá image local, cập nhật `compose.yaml` từ `build: ./app` sang `image: minhhociot/docker-capstone:v1` và pull/deploy thành công trực tiếp từ Docker Hub Registry.
- Xác minh qua `docker inspect` khớp `Image` và `RepoDigest` với registry.
- Kết quả: **ĐẠT BUỔI 17 (HOÀN THÀNH PHASE 4)**.

## [2026-09-08] Session 18: CI/CD Fundamentals with GitHub Actions
- Bắt đầu Phase 5: CI/CD Automation & GitHub Actions.
- Xây dựng Flask API microservice (`app.py`, Gunicorn 2 workers, endpoint `/`, `/health`) và viết bộ kiểm thử tự động bằng Flask test client (`test_app.py`).
- Tích hợp công cụ Linter hiện đại Ruff (Astral/Rust) tối ưu tốc độ quét mã nguồn tĩnh và chuẩn hóa PEP 8.
- Soạn thảo GitHub Actions Workflow (`.github/workflows/ci.yml`), quản lý 2 jobs tuần tự (`test` và `build-and-push`) kết nối qua quan hệ phụ thuộc `needs: test` (cơ chế Fail-Fast).
- Cấu hình an toàn GitHub Repository Secrets (`DOCKER_HUB_USERNAME` và `DOCKER_HUB_TOKEN`) để runner đăng nhập Docker Hub an toàn, không để lộ credential.
- Sử dụng bộ Docker GitHub Actions (`setup-buildx-action`, `login-action`, `build-push-action`) tự động hóa đóng gói container và push lên Docker Hub Registry với tag kép `:latest` và `:${{ github.sha }}`.
- Kéo trực tiếp image `minhhociot/devops-lab18:latest` từ Docker Hub về máy local qua WSL, chạy container và xác minh `curl /health` phản hồi `healthy`.
- Thực hành chuỗi Failure Injections và chẩn đoán sự cố:
  1. Lỗi Linter Ruff `I001`: Thiếu dòng trống ngăn cách standard library và local import $\rightarrow$ sửa theo chuẩn PEP 8.
  2. Lỗi logic test: Cố tình đổi mong đợi `version` thành `2.0.0` $\rightarrow$ Runner bắt AssertionError, pipeline đỏ tại step `Run unit tests` và dừng khẩn cấp trước khi build Docker.
  3. Lỗi xác thực Registry: Khắc phục lỗi `401 Unauthorized` do thiếu/sai Secret token Docker Hub, áp dụng tính năng `Re-run jobs` mà không cần commit rác.
  4. Lỗi Build Context: Xử lý lỗi `open Dockerfile: no such file or directory` do nhầm vị trí file `Dockerfile`.
- Merge toàn bộ code nhánh `feature/lab-18-ci-cd` vào nhánh `main` và push thành công lên GitHub.
- Kết quả: **ĐẠT BUỔI 18 (XUẤT SẮC)**.

## [2026-09-09] Session 19: Advanced GitHub Actions & Multi-Stage CI/CD Workflows
- Tiếp tục Phase 5: CI/CD Automation & GitHub Actions.
- Nâng cấp CI workflow từ single-job sang Matrix Build: Chạy song song unit test trên 3 runtime Python 3.10, 3.11, 3.12 sử dụng `strategy.matrix` và tắt `fail-fast` (`fail-fast: false`) để thu thập đầy đủ kết quả của mọi phiên bản độc lập.
- Tối ưu hóa thời gian chạy pipeline bằng cơ chế Caching dependencies với `actions/setup-python` (`cache: "pip"`, `cache-dependency-path: labs/lab-18-ci-cd/app/requirements.txt`).
- Tích hợp kiểm thử độ bao phủ mã nguồn với `coverage>=7.6.0`: Thực thi `coverage run`, xuất báo cáo định dạng `coverage.xml` và thiết lập Quality Gate `--fail-under=80` (Coverage < 80% thì CI tự động đánh FAIL).
- Lưu trữ và upload báo cáo coverage thành CI Artifacts riêng biệt cho từng phiên bản (`coverage-python-3.10`, `coverage-python-3.11`, `coverage-python-3.12`) qua `actions/upload-artifact@v4`.
- Phân định ranh giới CI vs CD an toàn: Cấu hình job `build-and-push` chỉ chạy khi có sự kiện push vào nhánh `main` (`github.event_name == 'push' && github.ref == 'refs/heads/main'`), nhánh feature chỉ chạy test/lint/coverage, không deploy image.
- Tạo nhánh tính năng `feature/lab-19-matrix-ci` và mở Pull Request #1 vào `main`.
- Thiết lập GitHub Branch Ruleset bảo vệ nhánh `main`: Chặn force push, bắt buộc Pull Request và yêu cầu 3 status checks bắt buộc (`Test - Python 3.10`, `Test - Python 3.11`, `Test - Python 3.12`) phải pass mới được merge.
- Thực hành Failure Injection: Cố tình nâng ngưỡng coverage lên 101% (`--fail-under=101`) khiến CI bị đỏ và GitHub khóa chặn nút merge PR #1; sau khi khôi phục threshold về 80%, CI xanh trở lại và mở khóa merge.
- Merge thành công PR #1 vào `main` (merge commit `68bb478`).
- Xác minh sau merge trên `main`: Matrix test 3.10/3.11/3.12 đều PASS, upload artifact PASS, job `build-and-push` tự động kích hoạt thực hiện Docker Buildx, Docker Hub login và push image thành công.
- Kết quả: **ĐẠT BUỔI 19 (XUẤT SẮC)**.

## [2026-09-09] Session 20: Deployment Environments, Approval Gates & Rollback
- Hoàn thành Buổi 20 trong Phase 5: CI/CD Automation & GitHub Actions.
- Thiết lập hệ thống GitHub Environments đa tầng gồm `staging` và `production` trên repository GitHub.
- Cấu hình Deployment Protection Rules cho môi trường `production`: Thiết lập Required Reviewers (yêu cầu phê duyệt thủ công từ reviewer chỉ định trước khi job deploy được phép chạy).
- Xây dựng kiến trúc CD Pipeline phân tầng hoàn chỉnh:
  1. `test` (Matrix Python 3.10, 3.11, 3.12, Linting Ruff, Coverage Gate 80%).
  2. `build-and-push` (Chỉ kích hoạt trên `main`, đóng gói Docker image và push lên Docker Hub).
  3. `deploy-staging` (Deploy tự động lên môi trường staging sau khi build thành công).
  4. `staging-smoke-test` (Tự động kiểm tra tính khả dụng của endpoint `/health` trên staging).
  5. `deploy-production` (Gán `environment: production`, tự động dừng lại chờ manual approval của reviewer; chỉ chạy khi staging smoke test PASS).
  6. `production-smoke-test` (Kiểm tra sức khỏe dịch vụ trên production).
  7. `promote-stable` (Sau khi production smoke test PASS, tiến hành promote Docker image gán thêm tag `stable`).
- Kiểm soát phạm vi triển khai theo nhánh: Các nhánh tính năng (feature branches) chỉ thực thi các job CI kiểm thử, tuyệt đối không kích hoạt deploy lên staging hay production.
- Áp dụng nguyên lý Artifact Immutability: Chuyển đổi toàn bộ quá trình đóng gói và deploy sang image tag bất biến dựa trên Git commit SHA (`${{ github.sha }}`) thay vì phụ thuộc vào tag mutable `latest`.
- Triển khai cơ chế Image Promotion: Khẳng định tính ổn định của bản release bằng việc gắn tag `stable` cho container image chỉ sau khi nó đã vượt qua toàn bộ các bài kiểm tra thực tế trên production.
- Tích hợp tính năng Manual Workflow Trigger: Bổ sung sự kiện `workflow_dispatch` với input `rollback` (kiểu boolean, mặc định false) cho phép người vận hành kích hoạt quy trình khẩn cấp trực tiếp từ GitHub Actions UI.
- Thiết kế và kiểm chứng quy trình Rollback khẩn cấp (`rollback-production`):
  - Khi kích hoạt với `rollback=true`, pipeline thông minh bỏ qua toàn bộ các bước `test`, `build-and-push`, `staging` và chỉ chạy duy nhất job `rollback-production`.
  - Job rollback vẫn tuân thủ Environment Protection Rules của `production` (đảm bảo tính kiểm soát truy cập và audit trail).
  - Kéo phiên bản an toàn đã được chứng nhận (`:stable`), khởi chạy, thực hiện smoke test `/health` xác minh khôi phục và dọn dẹp tài nguyên.
- Kiểm chứng thực tế trên GitHub Actions UI:
  - Kích hoạt Manual Rollback thành công trên run #28 (SUCCESS), xác minh các job không liên quan đều ở trạng thái `skipped`.
- Kết quả: **ĐẠT BUỔI 20 (XUẤT SẮC)**.

## [2026-09-10] Session 21: DevSecOps Security Scanning, Automated Releases & Phase 5 Capstone
- Hoàn thành Buổi 21 và chính thức tốt nghiệp PHASE 5: CI/CD Automation & GitHub Actions.
- Tích hợp công cụ Static Application Security Testing (SAST) với Bandit (`bandit -r app -ll`) để phân tích mã nguồn tĩnh, phát hiện sớm các rủi ro bảo mật trong Python code.
- Thực hành Failure Injection với Bandit: Bandit phát hiện cảnh báo bảo mật B104 (Hardcoded bind all interfaces `0.0.0.0`) trong khối `app.run()` phục vụ môi trường development; đã tiến hành tái cấu trúc, loại bỏ hoàn toàn dev server khỏi mã nguồn production và chuyển sang chạy thuần Gunicorn WSGI.
- Tích hợp Secret Detection với Gitleaks GitHub Action (`gitleaks-action`):
  - Cấu hình bắt buộc `fetch-depth: 0` để Gitleaks quét toàn bộ lịch sử Git commit thay vì chỉ quét commit nông gần nhất.
  - Thực hành Failure Injection với Gitleaks: Thử commit secret giả lập, nhận diện bài học cốt lõi rằng việc tạo commit mới để xóa file chứa secret KHÔNG loại bỏ được secret khỏi repository do Git lưu vết bất biến; đã thực hiện quy trình remediation viết lại lịch sử commit (commit amend/rebase) và force push an toàn bằng `--force-with-lease`.
- Tích hợp Container Vulnerability Scanning với Aqua Security Trivy (`aquasecurity/trivy-action`):
  - Tự động quét Docker image ngay sau khi build và TRƯỚC KHI đẩy lên Docker Hub Registry.
  - Cấu hình chốt chặn an ninh nghiêm ngặt: Thiết lập `--severity HIGH,CRITICAL` và `--exit-code 1` để tự động ngắt pipeline lập tức nếu phát hiện lỗ hổng nghiêm trọng trong base image hoặc application dependencies.
- Vận hành và chuẩn hóa luồng CI/CD + DevSecOps hoàn chỉnh trên nhánh `main`:
  1. `test`: Chạy song song Matrix Test (Python 3.10, 3.11, 3.12) kết hợp Ruff Linter, Coverage Gate (>=80%), Bandit SAST và Gitleaks secret detection.
  2. `build-and-push`: Đóng gói Docker image với commit SHA tag bất biến (`${{ github.sha }}`).
  3. `trivy-scan`: Quét lỗ hổng container image; chỉ khi vượt qua bài kiểm tra bảo mật mới push image lên Docker Hub.
  4. `deploy-staging` & `staging-smoke-test`: Triển khai tự động lên môi trường staging và chạy smoke test `/health`.
  5. `deploy-production`: Chốt chặn an toàn với Environment Protection Rules, yêu cầu manual approval từ reviewer chỉ định.
  6. `production-smoke-test`: Xác minh endpoint `/health` trên production.
  7. `promote-stable`: Gán thêm tag `:stable` cho image sau khi vượt qua smoke test production.
  8. `rollback-production`: Sẵn sàng kích hoạt khẩn cấp qua `workflow_dispatch` kéo `:stable` phục hồi khi có sự cố.
- Mở và merge thành công Pull Request #6 tích hợp toàn bộ các DevSecOps security gates.
- Tích hợp Google Release Please (`google-github-actions/release-please-action`):
  - Cấu hình manifest-driven release mode thông qua file `release-please-config.json` và `.release-please-manifest.json` tại thư mục gốc repository.
  - Cấu hình phân quyền bảo mật cho GitHub Actions Runner: Bật quyền `Allow GitHub Actions to create and approve pull requests` trong repository Settings.
  - Tự động hóa Semantic Versioning & Conventional Commits: Dựa trên các commit format `feat:`, `fix:`, `chore:`, Release Please tự động phân tích và mở Pull Request #8 (`chore(main): release 1.1.0`).
  - Merge thành công Release PR #8: Release Please tự động sinh file `CHANGELOG.md`, cập nhật `version.txt` lên `1.1.0`, tạo Git tag `v1.1.0` và xuất bản GitHub Release `v1.1.0` chính thức.
- Kết quả: **ĐẠT BUỔI 21 — HOÀN THÀNH TOÀN DIỆN VÀ TỐT NGHIỆP PHASE 5 (XUẤT SẮC)**.

## [2026-09-12] Session 22: AWS Foundations, IAM, CLI & Cost Safety
- Chính thức khởi động PHASE 6: AWS Cloud Infrastructure.
- Nghiên cứu nền tảng hạ tầng toàn cầu của AWS:
  - Phân biệt bản chất giữa AWS Region (khu vực địa lý độc lập), Availability Zone (AZ - một hoặc nhiều trung tâm dữ liệu tách biệt về điện, mạng và lũ lụt nhưng kết nối độ trễ cực thấp) và Data Center.
  - Phân tích sâu Shared Responsibility Model: AWS chịu trách nhiệm về "Security OF the Cloud" (hạ tầng vật lý, server, mạng quang, hypervisor), khách hàng chịu trách nhiệm về "Security IN the Cloud" (dữ liệu khách hàng, quản lý danh tính IAM, cấu hình hệ điều hành, firewall security groups và mã hóa).
- Thiết lập chốt chặn an toàn tài khoản AWS (Root Account Hardening):
  - Kích hoạt Multi-Factor Authentication (MFA) bảo vệ tài khoản root.
  - Khóa chặt tài khoản root, kiên quyết không tạo Access Key cho root và không sử dụng root cho các công việc vận hành hàng ngày.
- Quản trị an toàn chi phí với AWS Zero-Spend Budget:
  - Tạo AWS Budget với hạn mức chi phí $0.01 kèm cảnh báo tức thì qua email khi có bất kỳ chi phí nào phát sinh, đảm bảo môi trường học tập luôn an toàn chi phí tuyệt đối.
- Thiết kế hệ thống quản trị danh tính và truy cập (IAM) theo chuẩn Least Privilege:
  - Khởi tạo IAM User `minh-devops` không gán trực tiếp policy (No Direct Attached Policies).
  - Khởi tạo IAM Group `devops-lab` và gán user `minh-devops` vào nhóm.
  - Soạn thảo Customer-managed Policy `DevOpsLabReadOnly`: Cấp quyền đọc metadata khu vực EC2 (`ec2:DescribeRegions`, `ec2:DescribeAvailabilityZones`) và danh sách S3 bucket (`s3:ListAllMyBuckets`).
  - Thấu hiểu nguyên lý Implicit Deny: Mọi hành động không được cấp quyền Explicit Allow thì mặc định sẽ bị Deny.
- Phân biệt kiến trúc IAM Role:
  - Nắm vững cấu trúc Role gồm Trust Policy (ai/dịch vụ nào được phép assume role qua `sts:AssumeRole`) và Permission Policy (role đó được phép thao tác những tài nguyên nào sau khi assume).
- Vận hành AWS CLI v2 trên môi trường Ubuntu 24.04 WSL:
  - Cài đặt và cấu hình AWS CLI v2, đặt region mặc định là `ap-southeast-1` (Singapore).
  - Triển khai phương thức xác thực an toàn: Sử dụng `aws login` với Temporary Credentials ngắn hạn (STS token), hoàn toàn không tạo hay lưu trữ static long-term Access Key trên máy tính cá nhân.
  - Kiểm thử tương tác tài nguyên qua CLI:
    - Chạy `aws ec2 describe-regions` và `aws ec2 describe-availability-zones` thành công.
    - Chạy `aws s3api list-buckets` thành công.
- Thực hành Failure Injection kiểm chứng Least Privilege:
  - Cố tình thực thi câu lệnh `aws ec2 describe-instances`.
  - Kết quả: AWS API phản hồi lỗi `ClientError (UnauthorizedOperation)` đúng như thiết kế kiến trúc bảo mật, chứng minh policy chỉ cho phép xem metadata hạ tầng mà không cho phép truy cập danh sách máy chủ compute.
- Xử lý sự cố kỹ thuật (Troubleshooting):
  - Khắc phục lỗi đường dẫn và quyền hạn khi đồng bộ symlink cấu hình `~/.aws` giữa Windows host và Ubuntu WSL.
  - Nhận diện và xử lý phiên làm việc hết hạn (`expired aws login session`), thiết lập quy trình refresh token/login nhanh chóng.
- Kết quả: **ĐẠT BUỔI 22 (XUẤT SẮC)**.

## [2026-09-12] Session 23: AWS EC2 & VPC Fundamentals
- Tiếp tục PHASE 6: AWS Cloud Infrastructure.
- Khảo sát kiến trúc mạng AWS VPC và Subnet:
  - Phân tích Default VPC tại region `ap-southeast-1` (CIDR `172.31.0.0/16`).
  - Kiểm tra các default subnets và nắm vững nguyên lý vật lý: mỗi subnet nằm trọn vẹn trong một Availability Zone cụ thể (`ap-southeast-1a`, `ap-southeast-1b`, `ap-southeast-1c`).
  - Phân tích cơ chế Internet Gateway (IGW) và Route Table: xác minh route `0.0.0.0/0` trỏ tới Internet Gateway cho phép các tài nguyên trong Public Subnet kết nối hai chiều với Internet.
- Phân tích và cấu hình Security Group (Tường lửa ảo cấp máy chủ):
  - Hiểu rõ cơ chế Stateful: Khi cho phép traffic đi vào (inbound), traffic phản hồi (outbound response) tự động được cho phép mà không cần quy tắc outbound tương ứng.
  - Tạo Security Group riêng biệt `web-sg` chỉ mở cổng TCP 80 (`0.0.0.0/0`), không mở SSH công khai, tuân thủ nghiêm ngặt nguyên tắc Least Privilege.
- Khởi tạo và tự động hóa triển khai máy chủ EC2 (Bootstrapping via User Data):
  - Lựa chọn AMI Amazon Linux 2023 (`al2023-ami-...`) kết hợp instance type `t3.micro` (Free Tier eligible).
  - Sử dụng AWS CLI (`aws ec2 run-instances`) cùng file script `user-data.sh` truyền vào base64 để tự động hóa toàn bộ quá trình: cập nhật hệ thống, cài đặt Nginx (`dnf install -y nginx`), tạo file trang chủ HTML (`Hello from AWS EC2 - DevOps Learning - Session 23`) và kích hoạt service (`systemctl enable --now nginx`).
  - Kiểm tra và xác minh qua Public IPv4: Sử dụng `curl http://<PUBLIC_IP>` truy cập thành công từ máy local, nhận mã HTTP 200 và nội dung HTML đúng như kịch bản.
- Thực hành Failure Injection kiểm chứng tính chất Stateful Firewall:
  - Thu hồi (revoke) rule cho phép cổng 80 (`aws ec2 revoke-security-group-ingress`) $\rightarrow$ lệnh `curl` tới Public IP bị treo timeout ngay lập tức, chứng minh gói tin bị drop tại tầng Security Group trước khi vào OS.
  - Khôi phục (authorize) rule cổng 80 $\rightarrow$ website ngay lập tức phản hồi thông suốt trở lại mà không cần can thiệp vào máy chủ hay restart Nginx.
- Vận hành nguyên tắc Cost Safety & Resource Cleanup triệt để:
  - Thực thi `aws ec2 terminate-instances` xóa hoàn toàn máy chủ EC2 sau khi hoàn tất bài lab.
  - Xóa Security Group `web-sg` sau khi instance đã terminated hoàn toàn.
  - Xác minh Public IPv4 được tự động thu hồi và giải phóng về pool của AWS, ngăn chặn chi phí phát sinh cho IPv4 công cộng.
- Quản lý vòng đời đặc quyền (Privilege Hygiene) & Least Privilege:
  - Thu hồi toàn bộ các quyền ghi tạm thời (EC2 write permissions) đã cấp cho IAM User phục vụ bài lab.
  - Kiểm chứng bằng cờ `--dry-run` và lệnh `aws ec2 create-security-group`: AWS API trả về lỗi `UnauthorizedOperation` chính xác theo thiết kế ban đầu, đưa tài khoản về trạng thái an toàn tuyệt đối.
- Kết quả: **ĐẠT BUỔI 23 (XUẤT SẮC)**.

## [2026-09-13] Session 24: AWS Storage & IAM Role for EC2
- Tiếp tục PHASE 6: AWS Cloud Infrastructure.
- Phân tích toàn diện mô hình lưu trữ trên đám mây AWS:
  - So sánh Block Storage (Amazon EBS) vs Object Storage (Amazon S3) vs Ephemeral Local Storage (EC2 Instance Store).
  - Thấu hiểu tính phù hợp kiến trúc: Thư mục dữ liệu PostgreSQL (`PGDATA`) đòi hỏi đọc/ghi ngẫu nhiên (random I/O), độ trễ micro-giây và tương thích POSIX nên bắt buộc triển khai trên Block Storage/EBS thay vì Object Storage/S3.
- Quản trị dịch vụ lưu trữ đối tượng Amazon S3:
  - Tạo S3 bucket lab tại region `ap-southeast-1`.
  - Phân tích cấu trúc dữ liệu: Bucket, Object, Key và Prefix; nắm vững nguyên lý S3 là hệ thống lưu trữ đối tượng dạng Flat Namespace truy cập qua HTTPS REST API chứ không phải mounted filesystem.
  - Vận hành thành thạo bộ lệnh CLI: `PutObject`, `ListObjectsV2`, `GetObject`.
  - Kiểm tra tính năng Server-Side Encryption mặc định SSE-S3 sử dụng thuật toán mã hóa AES256.
  - Phân định rõ ràng phạm vi quyền hạn: Tách biệt quyền mức bucket (`s3:ListBucket` trên `arn:aws:s3:::bucket`) và quyền mức object (`s3:GetObject` trên `arn:aws:s3:::bucket/*`).
  - Thực hành Failure Injection S3: Cố tình loại bỏ quyền `s3:CreateBucket` khỏi policy $\rightarrow$ API phản hồi ngay lập tức `AccessDenied`.
- Thiết kế và triển khai cơ chế IAM Role & Instance Profile cho EC2:
  - Khởi tạo IAM Role `S24-EC2-S3-Role` với Trust Policy cho phép `ec2.amazonaws.com` gọi `sts:AssumeRole`.
  - Soạn thảo Permission Policy theo chuẩn Least Privilege: Chỉ cấp quyền `s3:ListBucket` và `s3:GetObject` duy nhất trên bucket bài lab.
  - Tạo Instance Profile đính kèm Role vào máy chủ EC2; hiểu rõ sự khác biệt giữa `sts:AssumeRole` (danh tính EC2 assume role) và `iam:PassRole` (quyền của người dùng ủy quyền chuyển giao role cho EC2).
- Thực hành Failure Injection kiểm chứng cơ chế xác thực IAM Role:
  - Khởi tạo EC2 instance không có IAM Role $\rightarrow$ AWS CLI trong instance báo lỗi `Unable to locate credentials`.
  - Thực hiện live-attach Instance Profile vào instance đang chạy $\rightarrow$ máy chủ tự động truy xuất temporary credentials qua IMDSv2.
  - Chạy `GetObject` tải file thành công ghi nhận chuỗi `S24_SUCCESS: EC2 READ S3`, loại bỏ triệt để việc lưu trữ long-term Access Key trên máy chủ.
- Quản trị ổ đĩa lưu trữ khối Amazon Elastic Block Store (EBS):
  - Khảo sát Root EBS Volume (gp3, 8 GiB, `ap-southeast-1a`, `DeleteOnTermination=True`).
  - Kiểm chứng ràng buộc vật lý: EBS Volume và EC2 Instance bắt buộc phải nằm trong cùng một Availability Zone (AZ).
  - Tạo volume bổ sung 1 GiB gp3 có mã hóa (Encrypted) và gắn (attach) vào EC2 instance; phân tích sự khác nhau giữa việc attach block device ở tầng ảo hóa và việc format filesystem/mount trong Linux.
  - Tạo EBS Snapshot kiểm chứng giải pháp sao lưu dữ liệu point-in-time; thực hành detach và delete EBS volume, xóa snapshot an toàn.
- Tuân thủ nghiêm ngặt nguyên tắc Cost Safety & Resource Deprovisioning:
  - Terminate toàn bộ máy chủ EC2 bài lab.
  - Xóa sạch EBS volume bổ sung và EBS snapshot.
  - Dọn sạch S3 objects và xóa bucket.
  - Xóa IAM Role, Instance Profile và inline policy.
  - Thu hồi toàn bộ quyền ghi tạm thời, giữ quyền `ec2:DescribeVolumes` trong policy `EC2ReadOnly`.
  - Kiểm chứng bằng kỹ thuật dry-run `CreateVolume` trả về `UnauthorizedOperation` chính xác theo thiết kế.
- Kết quả: **ĐẠT BUỔI 24 (XUẤT SẮC)**.

## [2026-09-15] Session 25: AWS RDS & Managed Database Fundamentals
- Tiếp tục PHASE 6: AWS Cloud Infrastructure.
- Phân tích sâu sắc kiến trúc cơ sở dữ liệu trên đám mây AWS:
  - So sánh chi tiết Database tự quản trên EC2 (Self-Managed) vs Amazon RDS (Managed Database): Trade-offs về việc tự quản lý OS/Database Engine, patching định kỳ, automated backup, point-in-time recovery, Multi-AZ high availability và tối ưu hóa chi phí vận hành.
  - Nắm vững các thành phần kiến trúc cốt lõi của RDS: DB Instance class (`db.t4g.micro`), database engine (PostgreSQL 17.11), storage (gp3 20 GiB, encrypted bằng KMS key mặc định).
  - Phân tích bản chất RDS Endpoint: Điểm truy cập DNS hostname ổn định mang tính trừu tượng hóa cao, giúp ứng dụng không bị ảnh hưởng khi địa chỉ IP underlying của database thay đổi sau bảo trì hoặc failover.
- Khởi tạo và cấu hình cơ sở dữ liệu Amazon RDS PostgreSQL:
  - Tạo DB Subnet Group gồm 2 Availability Zones (`ap-southeast-1a`, `ap-southeast-1b`) xác định phạm vi cấp phát mạng cho database; thiết lập `PubliclyAccessible=False` cô lập hoàn toàn database khỏi Internet.
  - Phân biệt từ nền tảng giữa High Availability (Multi-AZ synchronous replication với automatic failover cho thảm họa) vs Read Scaling (Read Replica asynchronous phục vụ phân tải truy vấn đọc).
- Thiết kế bảo mật mạng phân tầng với Security Group Referencing:
  - Tạo riêng biệt Security Group `app-sg` cho EC2 application layer và `rds-sg` cho RDS database layer.
  - Thực hành Failure Injection: EC2 cùng nằm trong VPC nhưng `rds-sg` chưa mở cổng TCP/5432 $\rightarrow$ kết nối bị chặn hoàn toàn (connection timeout).
  - Khắc phục theo chuẩn Least Privilege: Thêm rule cho phép TCP/5432 trên `rds-sg` với source là `app-sg` (Security Group Referencing thay vì mở dải IP CIDR hay `0.0.0.0/0`) $\rightarrow$ kết nối thông suốt.
  - Dùng công cụ `pg_isready` từ EC2 kiểm chứng PostgreSQL thực sự chấp nhận kết nối (accepting connections) qua mạng private nội bộ mà không cần đi qua Internet Gateway.
- Kiểm chứng vòng đời sao lưu dữ liệu (Automated Backups vs Manual Snapshots):
  - Phân tích sự khác biệt: Automated Backup bị ràng buộc bởi retention window và tự động bị hủy theo DB (khi dùng `--delete-automated-backups`), trong khi Manual Snapshot tồn tại vĩnh viễn và độc lập với vòng đời của DB instance.
  - Tạo manual snapshot; xóa DB instance và kiểm chứng manual snapshot vẫn tồn tại độc lập nguyên vẹn.
- Vận hành nguyên tắc Cost Safety & Resource Deprovisioning:
  - Dọn sạch toàn bộ EC2, RDS DB instance, manual snapshot, Security Groups (`app-sg`, `rds-sg`) và DB Subnet Group.
  - Thu hồi quyền `S25TemporaryLabManagement` và quyền `CreateServiceLinkedRole`; giữ lại service-linked role hệ thống `AWSServiceRoleForRDS`.
  - Kiểm tra AWS Billing xác nhận chi phí ước tính thực tế chỉ phát sinh khoảng ~$0.01 tại thời điểm kiểm tra.
- Kết quả: **ĐẠT BUỔI 25 (XUẤT SẮC)**.

## [2026-09-16] Session 26: AWS Load Balancing & Auto Scaling
- Tiếp tục PHASE 6: AWS Cloud Infrastructure.
- Nắm vững các khái niệm mở rộng và tính sẵn sàng cao (High Availability):
  - Phân biệt Vertical Scaling (Scale Up/Down - thay đổi kích thước CPU/RAM máy chủ) vs Horizontal Scaling (Scale Out/In - thay đổi số lượng máy chủ).
  - Nhận diện rủi ro Single Point of Failure (SPOF): Một máy chủ đơn lẻ chết sẽ làm sập toàn bộ dịch vụ; giải pháp là phân tán tải qua nhiều máy chủ và đa Availability Zone.
  - Hiểu vai trò của Application Load Balancer (ALB): Reverse Proxy hoạt động ở tầng ứng dụng Layer 7, tiếp nhận request từ client và định tuyến thông minh tới các backend targets.
  - Phân tích vai trò của Target Group và cơ chế Active Health Check: Giám sát định kỳ endpoint `/health` để tự động gỡ bỏ máy chủ lỗi khỏi bảng định tuyến.
  - Hiểu Launch Template là bản thiết kế (blueprint) chuẩn hóa cho phép tái tạo cấu hình máy chủ giống hệt nhau (AMI, type, script user-data) bất kỳ lúc nào.
  - Phân biệt rõ: ALB quản lý và định tuyến request; ASG quản trị và đảm bảo số lượng máy chủ chạy (Desired, Min, Max Capacity).
- Xây dựng kiến trúc cân bằng tải và bảo mật phân tầng:
  - Thiết lập luồng bảo mật nghiêm ngặt: `Internet` $\rightarrow$ `ALB SG` $\rightarrow$ `Web SG` $\rightarrow$ `EC2`.
  - Cấu hình `Web SG` chỉ cho phép lưu lượng TCP/80 đến từ `ALB SG` (Security Group Referencing), chặn hoàn toàn kết nối trực tiếp từ Internet vào máy chủ EC2.
  - Khởi tạo ALB, HTTP Listener (cổng 80), Target Group với health check path `/health`.
  - Khởi tạo Launch Template với cấu hình Amazon Linux 2023, `t3.micro`, Nginx user-data.
  - Khởi tạo Auto Scaling Group với `Min=2`, `Desired=2`, `Max=4`, phân bổ đều trên 2 Subnets thuộc `ap-southeast-1a` và `ap-southeast-1b`.
  - Kiểm tra qua ALB DNS Endpoint: Các request gửi bằng `curl` được phân phối luân phiên đồng đều tới 2 EC2 instances ở 2 AZs khác nhau.
- Thực hành Failure Injection & Kiểm chứng Khả năng Tự phục hồi (Self-Healing):
  - Cố tình `terminate` 1 máy chủ EC2 đang hoạt động $\rightarrow$ instance chuyển sang `shutting-down`.
  - ASG phát hiện trạng thái `Unhealthy`, báo hiệu cho Target Group.
  - ALB kích hoạt Connection Draining, ngừng gửi request mới tới instance đang dừng nhưng duy trì hoàn thành các request đang dở dang.
  - Kiểm thử 10/10 requests liên tục trong thời gian sự cố: Toàn bộ đều trả về HTTP 200 thành công nhờ máy chủ khỏe mạnh còn lại gánh tải.
  - ASG tự động kích hoạt Scaling Activity, dùng Launch Template khởi tạo 1 máy chủ mới thay thế; máy chủ mới pass health check và đưa cụm trở lại 2 healthy instances trên 2 AZs mà không cần sự can thiệp thủ công của con người.
- Vận hành nguyên tắc Cost Safety & Resource Deprovisioning:
  - Hạ `Desired`/`Min` của ASG về 0, quan sát quá trình `WaitingForELBConnectionDraining`.
  - Xóa tuần tự ASG, ALB Listener, Application Load Balancer, Target Group, Launch Template và các Security Groups.
  - Thu hồi toàn bộ quyền IAM ghi tạm thời (`S26TemporaryLoadBalancingLab`, `S26CreateRequiredServiceLinkedRoles`), giữ lại các quyền đọc an toàn và service-linked roles hệ thống.
- Kết quả: **ĐẠT BUỔI 26 (XUẤT SẮC)**.

## [2026-09-17] Session 27: AWS DNS, Route 53 & HTTPS/TLS Fundamentals
- Tiếp tục PHASE 6: AWS Cloud Infrastructure.
- Nắm vững các khái niệm nền tảng về DNS và quản lý định tuyến:
  - Phân biệt vai trò của Recursive DNS Resolver (máy chủ phân giải trung gian nhận truy vấn từ client/browser và truy lùng câu trả lời) vs Authoritative DNS Server (máy chủ nắm giữ bản ghi gốc chính thức của tên miền).
  - Hiểu cơ chế ủy quyền Name Server (NS delegation) và vai trò của Time to Live (TTL) trong việc lưu bộ đệm (DNS cache) tại các resolver trung gian.
  - Ủy nhiệm subdomain `aws.orianawren.com` từ DNS quản lý trên Cloudflare sang Amazon Route 53 bằng cách tạo các bản ghi NS tương ứng; sử dụng `dig` để truy vấn trực tiếp và xác thực việc delegation hoàn tất.
- Quản lý chứng chỉ số với AWS Certificate Manager (ACM):
  - Yêu cầu cấp phát chứng chỉ SSL/TLS công khai miễn phí cho FQDN `s27.aws.orianawren.com`.
  - Thực hiện xác thực danh tính tên miền bằng phương thức DNS Validation: Tạo bản ghi CNAME bí mật trong Route 53 Hosted Zone để ACM tự động xác thực và chuyển chứng chỉ sang trạng thái `ISSUED`.
- Thiết kế hạ tầng cân bằng tải HTTPS và bảo mật phân tầng:
  - Khởi tạo EC2 instance chạy Amazon Linux 2023, tự động cấu hình Nginx với endpoint `/health` qua User Data script.
  - Áp dụng mô hình bảo mật Security Group nhiều lớp: `Internet` $\rightarrow$ `ALB SG` (mở cổng TCP 80 và 443) $\rightarrow$ `EC2 SG` (chỉ cho phép cổng 80 có source từ `ALB SG` qua cơ chế Security Group Referencing).
  - Khởi tạo Target Group gắn health check `/health` và tạo Application Load Balancer (ALB) đa AZ.
  - Cấu hình HTTP Listener (cổng 80) tự động redirect 301 sang giao thức HTTPS cổng 443.
  - Cấu hình HTTPS Listener (cổng 443) đính kèm ACM Certificate và forward lưu lượng an toàn tới Target Group.
  - Tạo bản ghi Route 53 Alias `A` cho `s27.aws.orianawren.com` trỏ tới ALB DNS endpoint.
- Kiểm thử và xác minh giao thức TLS:
  - Dùng `curl -v https://s27.aws.orianawren.com/health` kiểm chứng luồng HTTPS: Kết nối thành công qua TLS 1.3, ALPN đàm phán giao thức HTTP/2, xác nhận chuỗi chứng chỉ hợp lệ (certificate verify OK) và nhận mã HTTP 200 từ Nginx backend.
- Thực hành Failure Injection & Phân biệt các khái niệm bảo mật cốt lõi:
  - Truy cập trực tiếp qua hostname mặc định của ALB (`https://<alb-id>...elb.amazonaws.com`) $\rightarrow$ ghi nhận lỗi Certificate Hostname Mismatch (`SSL: no alternative certificate subject name matches target host name`).
  - Phân tích và làm rõ: TLS encryption (mã hóa luồng dữ liệu) khác với Certificate Hostname Authentication (xác thực danh tính máy chủ với hostname người dùng yêu cầu). Lỗi hostname mismatch có thể đơn thuần do cấu hình sai URL truy cập chứ không đồng nghĩa chắc chắn có tấn công Man-in-the-Middle (MITM).
  - Nhận diện kiến trúc TLS Termination tại ALB: ALB chịu trách nhiệm giải mã TLS; chặng backend giữa `ALB` và `EC2` trong bài lab này là HTTP thông thường (unencrypted).
- Vận hành nguyên tắc Cost Safety & Resource Deprovisioning:
  - Dọn sạch toàn bộ tài nguyên: Xóa Alias record, ALB, Target Group, EC2 instance, ACM certificate, Security Groups, ACM validation CNAME record, xóa bản ghi NS delegation trên Cloudflare và xóa Route 53 Hosted Zone.
  - Ghi nhận hiện tượng lưu cache DNS: Recursive resolver có thể vẫn lưu trữ và trả về thông tin NS delegation cũ cho tới khi TTL hết hiệu lực, ngay cả khi authoritative configuration đã bị hủy bỏ.
- Kết quả: **ĐẠT BUỔI 27 (XUẤT SẮC)**.

## [2026-09-20] Session 28: AWS CloudWatch Monitoring, Metrics, Logs & Alarms
- Tiếp tục PHASE 6: AWS Cloud Infrastructure.
- Nắm vững kiến trúc và mô hình tư duy (Mental Model) của hệ thống giám sát trên AWS:
  - Phân biệt 5 thành phần trụ cột:
    - Metrics: Dữ liệu số theo chuỗi thời gian (time-series data) phản ánh tình trạng tài nguyên.
    - Logs: Dữ liệu sự kiện/bằng chứng chi tiết có ngữ cảnh (event-driven records).
    - Alarms: Đánh giá điều kiện/ngưỡng trên dữ liệu giám sát để kích hoạt các hành động phản hồi.
    - SNS (Simple Notification Service): Kênh phân phối thông báo (notification delivery), không tự phát hiện sự cố.
    - Dashboard: Trực quan hóa và tổng hợp tín hiệu đo lường, không tự kết luận toàn bộ hệ thống đang hoạt động tốt (healthy).
- Xây dựng hạ tầng bài lab và quản trị máy chủ qua AWS Systems Manager:
  - Khởi tạo EC2 Amazon Linux 2023 (`t3.micro`).
  - Sử dụng AWS Systems Manager Session Manager để kết nối terminal an toàn, không mở cổng hay dùng SSH public.
  - Cài đặt Nginx và xác minh dịch vụ phản hồi HTTP 200 từ localhost và Public IPv4.
  - Giữ nguyên chế độ EC2 Basic Monitoring (chu kỳ 5 phút), không bật Detailed Monitoring trong lab.
- Cấu hình Amazon CloudWatch Unified Agent và thu thập In-Guest Telemetry:
  - Tạo và gán IAM Role `S28CloudWatchAgentRole` cho EC2, tuân thủ nghiêm ngặt nguyên tắc không lưu trữ static long-term Access Key trên máy chủ.
  - Cài đặt CloudWatch Agent, cấu hình đẩy metric bộ nhớ `mem_used_percent` vào custom namespace `CWAgent`.
  - Thiết lập `metrics_collection_interval = 60` giây và dimension theo `InstanceId`.
- Thực hành Failure Injection kiểm chứng Telemetry Memory:
  - Quan sát mức tiêu thụ RAM baseline của hệ thống ở mức ~25%.
  - Khởi chạy tiến trình Python cấp phát và giữ thêm ~300 MiB RAM, đẩy `mem_used_percent` lên ~55%; sau khi process kết thúc, mức sử dụng RAM hạ dần về baseline.
  - Phân biệt rõ: Agent Collection Interval (chu kỳ agent thu thập và đẩy mẫu lên CloudWatch) vs CloudWatch Period (cửa sổ thời gian CloudWatch gom dữ liệu để tính toán statistic).
  - Thấu hiểu rằng thống kê `Average` với Period 5 phút sẽ làm mượt (smooth) các đột biến ngắn hạn hơn so với Period 1 phút.
- Thiết lập CloudWatch Alarm và tích hợp Amazon SNS:
  - Cấu hình Alarm `S28-High-Memory` trên metric `mem_used_percent` (Statistic: `Average`, Period: 1 minute, Threshold: `> 45%`, Datapoints to alarm: `1 out of 1`).
  - Quan sát và ghi nhận trực tiếp vòng đời chuyển đổi trạng thái: `OK` $\rightarrow$ `ALARM` $\rightarrow$ `OK`.
  - Tạo SNS Topic `s28-cloudwatch-alerts`, hoàn tất bước xác nhận (Confirm) email subscription trước khi test cảnh báo.
  - Nhận email cảnh báo tự động thành công khi Alarm chuyển sang trạng thái `ALARM`.
- Thu thập và phân tích nhật ký với CloudWatch Logs & Logs Insights:
  - Cấu hình CloudWatch Agent thu thập hai log stream: `/var/log/nginx/access.log` $\rightarrow$ Log Group `/s28/nginx/access` và `/var/log/nginx/error.log` $\rightarrow$ Log Group `/s28/nginx/error`.
  - Thiết lập Log Retention Policy ở mức 3 ngày để tối ưu hóa chi phí lưu trữ.
  - Thực hành Failure Injection tạo lỗi client: Gửi request `GET /this-page-does-not-exist` sinh mã HTTP 404.
  - Sử dụng CloudWatch Logs Insights viết truy vấn lọc các bản ghi lỗi 404, bóc tách log với lệnh `parse` thành các trường `method`, `path`, `protocol`, `status` và tổng hợp thống kê bằng `stats count(*) as requests by status`.
- Xây dựng CloudWatch Observability Dashboard:
  - Tạo dashboard `S28-Observability` với widget `CPUUtilization` (namespace `AWS/EC2`) và `mem_used_percent` (namespace `CWAgent`).
  - Ghi nhận nguyên tắc: Dashboard chỉ trực quan hóa các tín hiệu đo lường được chọn, không tự chứng minh toàn bộ hệ thống đang hoạt động bình thường.
- Hoàn thành Active Recall và tiếp thu hiệu chỉnh kỹ thuật:
  - Trả lời đạt 7/7 câu hỏi kiểm tra kiến thức cuối buổi.
  - Hiệu chỉnh kỹ thuật: Memory là in-guest/OS-level telemetry không nằm trong bộ EC2 default metrics (chứ không phải do hypervisor không có quyền vì privacy); không đồng nhất Period với collection interval và không xem việc tăng Period là tự giảm chi phí lưu trữ metric.
- Vận hành nguyên tắc Cost Safety & Resource Deprovisioning:
  - Thực hiện checklist dọn dẹp tài nguyên bài lab: Xóa CloudWatch Alarm `S28-High-Memory`, Dashboard `S28-Observability`, 2 Log Groups (`/s28/nginx/access`, `/s28/nginx/error`), SNS Topic `s28-cloudwatch-alerts` và email subscription, EC2 instance, Security Group và IAM Role `S28CloudWatchAgentRole`.
- Kết quả: **ĐẠT BUỔI 28**.

## [2026-09-21] Session 29: Infrastructure as Code Fundamentals with Terraform on AWS
- Tiếp tục lộ trình kỹ thuật: Khởi động Infrastructure as Code (IaC) với HashiCorp Terraform trên nền tảng AWS.
- Nắm vững kiến trúc và mô hình tư duy Declarative Infrastructure as Code:
  - Declarative (khai báo): Mô tả trạng thái mong muốn (Desired State) trong file cấu hình `.tf`, Terraform tự tính toán các bước thực thi để đưa hạ tầng thực tế về trạng thái đó, khác biệt với tư duy Imperative (mệnh lệnh) của Shell Scripting.
  - Providers: Plugin trung gian (`hashicorp/aws`) chịu trách nhiệm dịch cú pháp HCL thành các lệnh gọi AWS API tương ứng.
  - State (`terraform.tfstate`): Nguồn chân lý (Source of Truth) lưu trữ ánh xạ giữa resource định nghĩa trong code và ID/thuộc tính của resource thực tế ngoài cloud.
  - Core Workflow: Chu trình chuẩn mực `Author` $\rightarrow$ `Init` $\rightarrow$ `Plan` $\rightarrow$ `Apply` $\rightarrow$ `State` $\rightarrow$ `Update` $\rightarrow$ `Destroy`.
  - Idempotency (tính lũy thừa): Khả năng chạy lại cùng một configuration nhiều lần mà không tạo ra các tác dụng phụ hay thay đổi ngoài ý muốn nếu hạ tầng đã khớp code.
  - Configuration Drift: Hiện tượng sai lệch giữa tài nguyên thực tế ngoài AWS và định nghĩa trong mã nguồn Terraform (thường do ai đó sửa tay qua AWS Console/CLI).
  - Update-in-place: Cơ chế cập nhật trực tiếp các thuộc tính của tài nguyên tại chỗ mà không cần phải hủy bỏ (destroy) và tái tạo lại (recreate).
  - Saved Execution Plan (`terraform plan -out=s29.tfplan`): Kỹ thuật xuất bản kế hoạch thực thi ra file nhị phân để đảm bảo `apply` đúng chính xác những gì đã review, ngăn chặn race condition.
  - Git Hygiene & An toàn bí mật: Không bao giờ hard-code AWS access key/secret trong file cấu hình, sử dụng AWS Credential Chain (`AWS_PROFILE=devops-lab`, `AWS_REGION=ap-southeast-1`); giữ `.terraform.lock.hcl` trong Git để cố định phiên bản provider; cấu hình `.gitignore` loại bỏ `.terraform/`, `*.tfstate`, `*.tfstate.*`, `*.tfvars`, `*.tfplan`.
- Môi trường & Cấu hình Terraform:
  - Môi trường: Windows 11 + WSL2 Ubuntu 24.04, Terraform v1.16.3, AWS Region `ap-southeast-1`, IAM User `minh-devops`, AWS CLI profile `devops-lab`.
  - Xác thực an toàn qua `aws login --remote --profile devops-lab --region ap-southeast-1`, tuyệt đối không dùng Root User cho Terraform.
  - Soạn thảo `providers.tf`: Khai báo `required_version >= 1.16.0`, provider `hashicorp/aws`.
  - Soạn thảo `main.tf`: Khai báo data sources `aws_caller_identity.current`, `aws_region.current`; resource `aws_s3_bucket.lab` với `bucket_prefix = "s29-terraform-lab-"` và tags (`Name = s29-terraform-lab`, `Session = S29`, `ManagedBy = Terraform`); outputs: `aws_account_id`, `aws_arn`, `aws_region`.
- Thực hành Lab & Đối soát Drift:
  1. `terraform init`: Tải và cài đặt provider plugin AWS vào `.terraform/`, sinh file lock `.terraform.lock.hcl`.
  2. `terraform fmt` & `terraform validate`: Chuẩn hóa định dạng code và kiểm tra tính hợp lệ về mặt cú pháp.
  3. `terraform plan`: Phân tích trạng thái hiện tại và tạo execution plan thêm mới 1 resource.
  4. `terraform plan -out=s29.tfplan`: Lưu execution plan ra file.
  5. `terraform apply s29.tfplan`: Thực thi áp dụng kế hoạch đã lưu, khởi tạo thành công S3 bucket `s29-terraform-lab-cfde5b5df619082b66ff5228cd` tại `ap-southeast-1`.
  6. `terraform state list` & `terraform state show aws_s3_bucket.lab`: Khảo sát metadata lưu trong state file.
  7. `terraform output`: Kiểm tra các giá trị caller identity, ARN và region được trích xuất.
  8. Update tag `ManagedBy`: Chỉnh sửa code, chạy `terraform apply` quan sát hành vi update-in-place thành công.
  9. Tạo drift thủ công bằng AWS CLI: Sửa tag `ManagedBy = Manual` trực tiếp ngoài cloud.
  10. `terraform plan`: Phát hiện chính xác drift (`ManagedBy: "Manual" -> "Terraform"`).
  11. `terraform apply`: Tự động đối soát (reconcile) đưa tag ngoài cloud trở lại đúng giá trị trong code.
  12. `terraform plan` lần cuối: Xác nhận hạ tầng đồng nhất tuyệt đối (`No changes. Your infrastructure matches the configuration.`).
  13. `terraform destroy`: Hủy bỏ hoàn toàn S3 bucket được quản lý bởi Terraform.
  14. `terraform state list`: Xác nhận danh sách resource trong state trống rỗng sau khi destroy.
- Failure Injection & Xử lý Sự cố:
  - Lần apply đầu tiên thất bại với lỗi `AccessDenied` do user `minh-devops` chưa được cấp quyền `s3:CreateBucket`.
  - Hiểu sâu sắc sự khác biệt giữa Authentication (đăng nhập thành công) $\ne$ Authorization (được phép thực hiện hành động).
  - Khắc phục bằng cách gắn inline policy tạm thời `S29TerraformS3Lab` cấp quyền `s3:*` nhưng giới hạn phạm vi chặt chẽ (scoped) về ARN của bucket bài lab (`arn:aws:s3:::s29-terraform-lab-*`). Kiên quyết không dùng root user hoặc AdministratorAccess để né lỗi phân quyền.
  - Lỗi bộ gõ tiếng Việt Telex: Gõ chuỗi xác nhận "yes" bị bộ gõ chèn ký tự/diacritic khiến Terraform hiểu nhầm là chuỗi khác và tự động hủy ("Apply cancelled"); khắc phục bằng cách chuyển bộ gõ sang English input.
  - Terminal VS Code bị đóng băng do tính năng flow-control (XOFF) khi vô tình bấm `Ctrl+S`; sử dụng `Ctrl+Q` (XON) để giải phóng luồng I/O.
- Hoàn thành Active Recall cuối buổi:
  - Trả lời đạt 7/7 câu hỏi ôn tập về plan vs apply, vai trò terraform.tfstate, drift, update-in-place, bucket_prefix, bảo mật credentials, và phạm vi quản lý của terraform destroy.
- Vận hành nguyên tắc Cost Safety & Resource Deprovisioning:
  - S3 bucket bài lab đã được `terraform destroy` thành công.
  - Kiểm tra `terraform state list` sau cleanup: Không còn output.
  - Xóa hoàn toàn inline IAM policy tạm thời `S29TerraformS3Lab`.
  - Không còn tài nguyên AWS nào của S29 bị lưu lại chạy ngầm.
- Kết quả: **ĐẠT BUỔI 29**.

## [2026-09-23] Session 31: Terraform Remote State, S3 State Locking & Reusable Modules
- Tiếp tục lộ trình kỹ thuật: Quản trị Remote State, S3 State Locking và cấu trúc Reusable Modules với HashiCorp Terraform trên AWS.
- Môi trường & Không gian làm việc:
  - Workspace: `/mnt/d/Devops/labs/lab-31-terraform-remote-state`
  - Hệ điều hành: Windows 11 + WSL2 Ubuntu 24.04, Terraform v1.16.3, AWS Region `ap-southeast-1`.
  - IAM User: `minh-devops`, AWS CLI profile `devops-lab`.
- Phân biệt kiến trúc cốt lõi:
  - Git: Nơi lưu trữ và chia sẻ mã nguồn khai báo hạ tầng Terraform (`.tf`).
  - Remote Backend: Hạ tầng lưu trữ tập trung file trạng thái thực tế (`terraform.tfstate`), cho phép team/CI cùng nhìn thấy một nguồn chân lý.
  - State Locking: Cơ chế khóa trạng thái nhằm ngăn chặn race condition và concurrent state operations (nhiều tiến trình apply/plan đồng thời gây corrupt state).
- Mô hình Bootstrap Pattern cho Terraform Backend:
  - Khởi tạo thư mục `bootstrap/` sử dụng local state để tạo S3 backend bucket trước (`s31-terraform-state-*`).
  - Thấu hiểu bản chất: Backend bucket phải tồn tại và sẵn sàng hoạt động trước khi cấu hình remote backend của thư mục `app/` có thể trỏ vào sử dụng.
- Cấu hình chuẩn hóa và an toàn S3 Backend Bucket:
  - S3 bucket prefix: `s31-terraform-state-*` tại region `ap-southeast-1`.
  - Bật S3 Bucket Versioning (`versioning_configuration { status = "Enabled" }`).
  - Khóa toàn bộ truy cập công khai (`aws_s3_bucket_public_access_block` bật tất cả 4 thiết lập chặn public access).
  - Kích hoạt mã hóa lưu trữ SSE-S3 AES256.
- Quản trị IAM Least Privilege & Failure Injection:
  - Lần apply đầu tiên của bootstrap thất bại chính xác tại API `s3:CreateBucket` do user `minh-devops` thiếu quyền ghi S3.
  - Cấp inline policy tạm thời `S31TerraformStateLab` giới hạn nghiêm ngặt phạm vi tài nguyên (scoped) chỉ trên bucket `s31-terraform-state-*` và `s31-terraform-state-*/*`.
  - Xóa bỏ hoàn toàn inline policy này ở cuối session theo quy trình Privilege Hygiene.
- Di chuyển State lên Remote Backend (Remote-State Migration):
  - Khởi tạo tài nguyên `terraform_data.demo` với local state ban đầu (`terraform.tfstate`).
  - Kích hoạt S3 backend qua file cấu hình `backend.hcl` với key `s31/app/terraform.tfstate`.
  - Thực thi di chuyển state: `terraform init -migrate-state -backend-config=backend.hcl`.
  - Kiểm tra `terraform state list`: Resource `terraform_data.demo` vẫn hiện diện nguyên vẹn sau migration, chứng minh Terraform đã chuyển dịch toàn bộ metadata state lên remote backend mà không tái tạo (recreate) tài nguyên.
- Kiểm chứng S3 Versioning & Mental Model Phục hồi State:
  - Chỉnh sửa thuộc tính của `terraform_data.demo`, chạy `terraform apply` để ghi state mới lên S3.
  - Quan sát S3 object versions: State cũ chuyển sang `IsLatest=false`, state mới có `IsLatest=true` kèm VersionId mới.
  - Mental Model chuẩn xác: S3 Versioning là cơ chế bảo vệ phục hồi state khi xảy ra lỗi ghi đè hoặc hỏng file; việc restore state từ version cũ chỉ phục hồi bộ nhớ mapping của Terraform, hoàn toàn không đồng nghĩa với việc tự động rollback hạ tầng thực tế ngoài cloud.
- Kiểm chứng Native S3 State Locking (`use_lockfile = true`):
  - Sử dụng tính năng S3 Native Locking (`use_lockfile = true`), KHÔNG dùng DynamoDB (DynamoDB locking là kiến thức cũ/deprecated đối với workflow này).
  - Kiểm thử tranh chấp khóa (Locking Concurrency):
    - Terminal A: Kích hoạt apply giữ lock thông qua `terraform_data.lock_holder` kết hợp `local-exec sleep`.
    - Terminal B: Chạy `terraform plan -lock-timeout=3s`.
    - Kết quả: Terminal B bị chặn đứng với thông báo lỗi `Error acquiring the state lock` và mã lỗi HTTP S3 `412 PreconditionFailed` trên file `.tflock`.
    - Lock info hiển thị rõ định danh tiến trình và `OperationTypeApply`.
    - Sau khi Terminal A hoàn tất và nhả lock, Terminal B thực thi lại `terraform plan` thành công và trả về `No changes`.
- Thiết kế và Tái sử dụng Child Modules (Reusable Modules):
  - Xây dựng Child Module chuẩn mực tại `app/modules/message/` gồm:
    - `variables.tf`: Khai báo input variables cho module.
    - `main.tf`: Khai báo logic tài nguyên của module (`terraform_data.this`).
    - `outputs.tf`: Xuất output từ module ra ngoài.
  - Root module gọi cùng một source module hai lần độc lập:
    - `module.message_app`
    - `module.message_ops`
  - Quản lý phân cấp không gian địa chỉ state:
    - `terraform_data.demo`
    - `terraform_data.lock_holder`
    - `module.message_app.terraform_data.this`
    - `module.message_ops.terraform_data.this`.
  - Kiểm tra và xuất thành công module outputs: `app_module_data` và `ops_module_data`.
- Active Recall cuối buổi & Hiệu chỉnh Mental Model:
  - Nắm vững kiến thức: Remote State vs Locking, Bootstrap Pattern, Versioning, Module Addresses, Module Inputs/Outputs.
  - Hiệu chỉnh nhận thức quan trọng: Chuyển đổi dứt điểm từ mental model cũ `S3 + DynamoDB locking` sang S3 Native Locking `.tflock`.
  - Hiệu chỉnh bản chất của State: State là bộ nhớ/mapping của Terraform để liên kết cấu hình code với đối tượng thực tế, không phải là bản sao tuyệt đối của thực tế ("reality").
- Thử thách Defense Mode (Thời lượng quy định: 10 phút):
  - Kịch bản sự cố injected:
    - Backend key bị đổi từ `s31/app/terraform.tfstate` thành `s31/defense/terraform.tfstate`.
    - Child module output `data` bị đổi tên thành `payload`.
  - Kết quả xử lý sự cố:
    - Technical Recovery: **PASS** (`terraform validate`: PASS; `terraform plan`: `No changes`; `terraform state list`: đủ 4 addresses; module outputs hiển thị chính xác; không destroy/recreate tài nguyên để chữa lỗi; root-cause reasoning sau Defense: PASS).
    - Time Requirement: **FAIL** (thời gian xử lý thực tế 19m26s, vượt ngưỡng quy định 9m26s).
    - Đánh giá tổng hợp Defense Mode: Technical PASS / Timed FAIL.
- Vận hành nguyên tắc Cost Safety & Resource Deprovisioning:
  - `terraform destroy` toàn bộ tài nguyên trong thư mục `app/`.
  - Xóa sạch toàn bộ versioned objects và delete markers trong S3 bucket backend.
  - `terraform destroy` xóa sạch S3 bucket trong thư mục `bootstrap/`.
  - Xóa hoàn toàn Temporary Inline IAM Policy `S31TerraformStateLab`.
  - Không còn tài nguyên AWS nào của S31 bị lưu lại chạy ngầm.
- Kết quả: **ĐẠT BUỔI 31 (Technical PASS / Timed FAIL Defense Mode)**.

## [2026-09-24] Session 32: Terraform Meta-Arguments, Lifecycle, Import & Safe Refactoring
- Tiếp tục lộ trình kỹ thuật: Quản trị vòng đời tài nguyên, kỹ thuật Meta-Arguments, Modern Config-Driven Import và Safe Refactoring với HashiCorp Terraform.
- Môi trường & Không gian làm việc:
  - Workspace chính: `D:\Devops\labs\lab-32-terraform-advanced`
  - WSL: `/mnt/d/Devops/labs/lab-32-terraform-advanced`
  - Hệ điều hành: Windows 11 + Ubuntu 24.04 WSL2, Terraform v1.16.3.
- Thực hành Meta-Arguments: `count` vs `for_each`:
  - `count-demo`:
    - Khởi tạo 3 instances (`api`, `worker`, `scheduler`) với address theo numeric index (`[0]`, `[1]`, `[2]`).
    - Thực hành xóa phần tử `worker` ở giữa danh sách.
    - Plan/Apply thực tế: `0 added, 1 changed, 1 destroyed`. Tài nguyên `scheduler` bị dịch chuyển index từ `[2]` sang `[1]`.
    - Mental Model: `count` định danh theo chỉ mục số nguyên (numeric index). Xóa hoặc chèn phần tử ở giữa list sẽ gây hiện tượng Index Shift, kéo theo việc cập nhật hoặc thay thế hàng loạt tài nguyên phía sau.
  - `foreach-demo`:
    - Khởi tạo cùng danh sách với `for_each`, định danh theo stable key: `terraform_data.service["api"]`, `terraform_data.service["worker"]`, `terraform_data.service["scheduler"]`.
    - Xóa `worker`: Kết quả `0 added, 0 changed, 1 destroyed`. Hai service `api` và `scheduler` giữ nguyên bản sắc định danh.
    - Mental Model: `for_each` gán định danh tài nguyên theo key ổn định (string key), là lựa chọn tối ưu khi tài nguyên có tên hoặc ID tự nhiên cố định.
- Quản trị Vòng đời Tài nguyên (Resource Lifecycle Rules):
  - Workspace: `lab-32-terraform-advanced/lifecycle-demo`.
  - Thực hành 4 quy tắc: `create_before_destroy`, `prevent_destroy`, `ignore_changes`, `replace_triggered_by`.
  - `prevent_destroy`: Kiểm chứng `terraform destroy` bị chặn đứng với thông báo lỗi: `Error: Instance cannot be destroyed.`. Hiểu rõ đây là lớp bảo vệ tại tầng client Terraform CLI, không ngăn cản việc xóa trực tiếp ngoài Cloud Console/API/Docker CLI.
  - `ignore_changes`: State giữ `value-v1`, chỉnh sửa code thành `value-v2`. `terraform plan` báo `No changes`. Hiểu rõ cơ chế hữu ích khi thuộc tính do hệ thống khác quản trị, nhưng lạm dụng sẽ che giấu drift hạ tầng.
  - `replace_triggered_by`: Khi tài nguyên nguồn thay đổi, tài nguyên phụ thuộc bị buộc phải thay thế. Phân biệt chuẩn xác: `depends_on` định nghĩa thứ tự thực thi (ordering), còn `replace_triggered_by` thiết lập điều kiện kích hoạt thay thế tài nguyên.
- Quản trị Import Tài nguyên Hiện hữu (Modern Config-Driven Import):
  - Workspace: `lab-32-terraform-advanced/import-demo`.
  - Khởi tạo Docker container ngoài Terraform: `name: s32-import-demo`, port `8088 -> 80`, ID `1b423fff7695853972214aea38992f97393d6c67bf536a1d6de220b351aaac93`.
  - Khai báo khối `import {}` và sinh file cấu hình tự động: `terraform plan -generate-config-out=generated.tf`.
  - Phân tích rủi ro: Plan lần đầu báo `1 to import, 1 to add, 0 to change, 1 to destroy` do `generated.tf` sinh ra thuộc tính `env` mặc định buộc replacement. Kiên quyết không apply plan phá hủy này.
  - Tinh chỉnh `generated.tf` với `env = []`: Plan an toàn trở thành `1 to import, 0 to add, 1 to change, 0 to destroy`.
  - Thực thi Apply: `Resources: 1 imported, 0 added, 1 changed, 0 destroyed`. Container được đưa vào quản lý tại `docker_container.imported`. Docker ID được bảo toàn 100%.
  - Mental Model: `generated.tf` chỉ là bản nháp khởi đầu, bắt buộc phải review kỹ lưỡng execution plan; import tạo ánh xạ giữa tài nguyên đang chạy ngoài đời thực và Terraform state chứ không phải tạo lại tài nguyên.
- Tái cấu trúc An toàn (Safe Refactoring as Code):
  - Workspace: `lab-32-terraform-advanced/refactor-demo`.
  - Đổi tên `terraform_data.server_old` sang `server_app` trong code mà chưa khai báo `moved`: Plan báo phá hủy và tạo mới (`1 to add, 1 to destroy`).
  - Thêm khối khai báo:
    ```hcl
    moved {
      from = terraform_data.server_old
      to   = terraform_data.server_app
    }
    ```
  - Kết quả: Plan sạch hoàn toàn (`0 to add, 0 to change, 0 to destroy`), state cập nhật thành `terraform_data.server_app`.
  - Thực hành lệnh trực tiếp `terraform state mv` (`server_app -> server_final`): Do code vẫn là `server_app` nên plan lập tức bị lệch (`1 add, 1 destroy`). Sau đó sửa state về lại `server_app` để plan sạch.
  - Mental Model: `moved {}` là giải pháp tái cấu trúc dạng khai báo (declarative refactor-as-code), commit và review được qua Git/CI, cực kỳ an toàn cho đội ngũ làm việc chung; `terraform state mv` là thao tác thủ công trực tiếp lên state file, dễ gây lệch pha giữa code và state.
- Cấu hình Khối lặp Động (Dynamic Blocks):
  - Workspace: `lab-32-terraform-advanced/dynamic-demo`.
  - Sử dụng `local.port_mappings` kết hợp `dynamic "ports"` sinh hai khối nested blocks lồng nhau (`18091 -> 80`, `18092 -> 80`).
  - `terraform validate`: PASS; `terraform plan`: `2 to add` (chỉ plan đối soát cú pháp, không apply).
  - Mental Model: `count`/`for_each` sinh nhiều instances của một resource; `dynamic` sinh nhiều nested blocks bên trong một resource. Không lạm dụng dynamic nếu một vài block cố định viết trực tiếp dễ đọc hơn.
- Failure Injection S32:
  - Kiểm chứng lỗi Index Shift của `count` và cơ chế chặn destroy của `prevent_destroy` trực tiếp trong lab.
- Thử thách Defense Mode (Bắt đầu 20:03:28 UTC+7 ngày 2026-09-24):
  - Yêu cầu: Đổi `docker_container.imported` sang `docker_container.web`, không xóa/tạo lại container, chuyển 2 ports blocks sang dynamic block dùng local, cập nhật import block, bắt buộc dùng `moved {}`.
  - Học viên tự thực hiện: Cấu hình `local.container_ports`, `dynamic "ports"`, khối `moved {}`, cập nhật target import.
  - Kết quả: Plan/Apply `0 added, 0 changed, 0 destroyed`, state chuyển sang `docker_container.web`, Docker ID giữ nguyên `1b423fff7695...`.
  - Thời gian xử lý: 19 phút 49 giây.
  - Đánh giá: Technical Defense **PASS**; Timed requirement (10m) **FAIL**.
- Hoàn thành Active Recall & Cleanup:
  - Đạt 7/7 câu hỏi ôn tập cuối buổi.
  - Dọn dẹp tài nguyên: `import-demo` destroy 1 resource (container xóa sạch); `lifecycle-demo` gỡ `prevent_destroy` rồi destroy 5 resources; các demo khác state sạch; không tạo tài nguyên AWS, chi phí $0.
- Kết quả: **ĐẠT BUỔI 32 (Technical PASS / Timed FAIL Defense Mode)**.

## [2026-10-01] Session 33: Ansible Fundamentals & Safe Configuration Management
- Tiếp tục lộ trình kỹ thuật: Khởi động mảng Quản trị Cấu hình (Configuration Management) với Ansible trên môi trường Linux Ubuntu 24.04 WSL.
- Ngày học: 2026-09-28 và tiếp tục hoàn thành ngày 2026-10-01.
- Môi trường & Không gian làm việc:
  - Workspace: `D:\Devops\labs\lab-33-ansible-fundamentals`
  - WSL: `/mnt/d/Devops/labs/lab-33-ansible-fundamentals`
  - Phiên bản: Ubuntu 24.04 WSL, `ansible-core 2.16.3`, Python 3.12.3.
  - Nginx đã tồn tại sẵn trên máy trước bài lab; không xem việc cài Nginx là tài nguyên mới do S33 tạo ra.
- Phân biệt Kiến trúc Terraform vs Ansible:
  - Terraform: Tập trung vào cấp phát hạ tầng (Infrastructure Provisioning).
  - Ansible: Tập trung vào quản trị cấu hình hệ thống, cài đặt phần mềm và duy trì trạng thái OS (Configuration Management).
  - Kiến trúc Agentless: Ansible không cần cài agent ngầm trên managed node, điều khiển thông qua cơ chế kết nối (SSH cho remote host, local connection cho localhost).
- Thiết lập Inventory & Ad-hoc Command:
  - Soạn thảo `inventory.ini` với nhóm `[local]` chứa `localhost ansible_connection=local`.
  - Thực thi ad-hoc command: `ansible -i inventory.ini all -m ping`.
  - Kết quả: `SUCCESS`, `changed=false`, `ping=pong`.
  - Mental Model: `ansible.builtin.ping` không phải lệnh ping mạng ICMP mà là kiểm tra khả năng Ansible kết nối và thực thi module/Python trên target host.
- Playbook & Kiểm chứng Tính Lũy Thừa (Idempotency):
  - Viết playbook đầu tiên dùng `ansible.builtin.copy` tạo file `/tmp/ansible-demo.txt`.
  - Lần chạy 1: `changed=1` (file được tạo mới).
  - Lần chạy 2: `changed=0` (nội dung file đã khớp desired state, không có thay đổi dư thừa).
  - Mental Model: Idempotency đảm bảo chạy lại playbook nhiều lần vẫn duy trì cùng một trạng thái ổn định mà không gây tác dụng phụ.
- Quản trị Biến và Xử lý Từ khóa Bảo lưu (Reserved Variables):
  - Ban đầu đặt tên biến là `environment` -> kết quả render bị rỗng `Environment: []`.
  - Phát hiện `environment` là từ khóa dành riêng (reserved keyword) của Ansible dùng để thiết lập biến môi trường cho task; đổi tên thành `app_environment`.
  - Cấu hình vars: `app_name: demo-app`, `app_environment: dev`. Kết quả hiển thị chính xác.
  - Tách biến ra file riêng `vars.yml`; refactor lại playbook và chạy kiểm tra ghi nhận `changed=0`.
- Cơ chế Handlers & Event-Driven Notification:
  - Nắm vững nguyên lý: Task chỉ trigger `notify` khi có trạng thái `changed=true`; nếu `changed=false`, handler sẽ bị bỏ qua.
  - Nhiều task notify cùng một handler thì handler mặc định chỉ chạy một lần duy nhất ở cuối play.
  - Thực hành: Đổi môi trường từ `dev` sang `staging` khiến task template thay đổi (`changed=1`), handler reload được kích hoạt thành công.
- Cấu hình Động với Jinja2 Template:
  - Chuyển từ copy file tĩnh sang `ansible.builtin.template` với file nguồn `templates/app.conf.j2` (`{{ app_name }}`, `{{ app_environment }}`).
  - Xử lý lỗi thực hành: Playbook trỏ nhầm tên file (`app_info.j2` vs `app.conf.j2`), đã đọc lỗi và sửa lại đúng đường dẫn. Khi template render trùng khớp file hiện tại, task báo `changed=0`.
- Thu thập Facts Hệ thống & Điều kiện Hóa Tác vụ (`when`):
  - Bật `gather_facts: true`. Facts thực tế thu thập: distribution `Ubuntu`, version `24.04`, release `noble`, OS family `Debian`.
  - Áp dụng điều kiện: `when: ansible_facts['distribution'] == "Ubuntu"`. Task Ubuntu chạy thành công, task dành cho Amazon Linux được bỏ qua (`skipped=1`).
- Quản trị Đặc quyền & Dịch vụ (`become`, `apt`, `service`):
  - Kích hoạt đặc quyền root với `become: true` (`--ask-become-pass`).
  - Module `apt`: Đảm bảo Nginx có trạng thái `state=present` (do Nginx đã có từ trước nên task báo `ok`, `changed=0`).
  - Module `service`: Đảm bảo Nginx `state: started` và `enabled: true` (hệ thống đã active và enabled từ trước nên task báo `ok`, `changed=0`).
- Triển khai Cấu hình Nginx & Failure Injection Lần 1 (Unsafe Pattern):
  - Tạo `templates/nginx-demo.conf.j2` với `listen 8081;`, deploy vào `/etc/nginx/conf.d/ansible-demo.conf`, notify `Reload Nginx`.
  - Lần đầu: template thay đổi -> handler reload chạy -> `curl localhost:8081` trả về `Managed by Ansible - staging`. Lần hai chạy lại: `changed=0`.
  - Failure Injection 1 (Unsafe deployment): Cố tình sửa template thành `listen abc;` và ghi thẳng vào `/etc/nginx/conf.d/`. Lệnh kiểm tra `nginx -t` thất bại. Sau khi session tạm dừng và mở lại vào ngày 2026-10-01, lệnh `sudo nginx -t` vẫn FAILED và curl 8081 không kết nối được -> chứng minh sự nguy hiểm khi file cấu hình hỏng đã nằm trực tiếp trên disk của dịch vụ.
  - Phục hồi thủ công: Sửa lại `listen 8081;`, `nginx -t` PASS, restart Nginx và curl thông suốt trở lại.
- Thiết kế Quy trình Triển khai An toàn (Safe Nginx Deployment Pipeline):
  - Nâng cấp playbook thành pipeline triển khai chuẩn:
    1. Render candidate file ra thư mục tạm: `/tmp/ansible-nginx-demo.conf`.
    2. Tạo file cấu hình test độc lập: `/tmp/ansible-nginx-test.conf`.
    3. Kiểm tra cú pháp an toàn: `nginx -t -c /tmp/ansible-nginx-test.conf`.
    4. Chỉ khi bước kiểm tra cú pháp PASS mới copy candidate vào `/etc/nginx/conf.d/ansible-demo.conf` (sử dụng `remote_src: true`).
    5. Kích hoạt notify `Reload Nginx`.
  - Failure Injection 2: Cố tình cấu hình template sai (`listen abc;`). Candidate `/tmp` bị lỗi cú pháp -> bước `nginx -t -c` FAILED ngắt playbook ngay lập tức -> task copy và handler reload bị chặn đứng -> file thật `/etc/nginx/conf.d/` vẫn giữ nguyên `listen 8081;` và curl 8081 vẫn phản hồi bình thường!
  - Sau đó phục hồi template về `listen 8081;`, pipeline chạy thông suốt.
- Đăng ký Biến & Điều kiện Lỗi Nghiệp vụ (`register`, `failed_when`):
  - Dùng `register: nginx_status` lưu kết quả lệnh `systemctl is-active nginx`, sử dụng thuộc tính `nginx_status.stdout == "active"` làm điều kiện kiểm tra.
  - Health check HTTP: Dùng `curl -s -o /dev/null -w "%{http_code}" http://localhost:8081`, lưu vào biến `http_check`, cấu hình `changed_when: false` và `failed_when: http_check.stdout != "200"`.
  - Failure Injection: Đổi tạm thành `failed_when: http_check.stdout != "201"`. Dù lệnh curl có exit code 0 (`rc=0`) nhưng do output trả về "200", Ansible đánh giá task FAILED chính xác theo điều kiện logic nghiệp vụ. Khôi phục lại về "200".
- Xử lý Ngoại lệ Có Cấu trúc (`block`, `rescue`, `always`):
  - Thử nghiệm khối `block` thực thi lệnh `/bin/false` (gây lỗi rc=1) -> task chuyển hướng sang khối `rescue` ("Da phat hien loi va chuyen sang rescue.") -> khối `always` luôn được thực thi dù thành công hay thất bại.
- Thử thách Defense Mode (Bắt đầu 17:40:26 UTC+7 ngày 2026-10-01):
  - Mục tiêu: Chuyển port Nginx từ 8081 sang 8082 thông qua `vars.yml` (`app_port: 8082`), duy trì safe pipeline, reload dịch vụ và kiểm tra HTTP 200.
  - Điểm sáng tạo của học viên: Tự thêm task `ansible.builtin.meta: flush_handlers` để ép Reload Nginx chạy ngay lập tức trước bước kiểm tra HTTP health check, loại bỏ hoàn toàn race condition kiểm tra port mới khi Nginx chưa kịp nạp cấu hình mới.
  - Kết quả Defense:
    - Run 1: `ok=18, changed=3, failed=0, rescued=1` (`nginx -t` pass, `curl :8082` pass).
    - Run 2: `ok=17, changed=0` -> Idempotency PASS.
    - Thời gian xử lý: 13 phút 40 giây.
    - Đánh giá: Technical Defense **PASS**, Safe Deployment **PASS**, Idempotency **PASS**, Timed requirement (10m) **FAIL**.
- Active Recall & Tiếp thu Phản hồi Giảng dạy (Teaching-Quality Process Note):
  - Học viên trả lời đúng 7/7 câu hỏi về inventory, idempotency, template vs copy, notify/handler, register/stdout, failed_when, và safe deployment pipeline.
  - Phản hồi phương pháp giảng dạy: Học viên ghi nhận trải nghiệm học chưa hài lòng (bài giảng lướt nhiều khái niệm chỉ đủ để chạy lab, câu hỏi recall lại yêu cầu giải thích sâu hơn nhiều so với phần được dạy, dồn quá nhiều concept trong một buổi).
  - Đánh giá năng lực: Ghi nhận "answers correct, reinforcement required" (không ngộ nhận 7/7 là đã mastery toàn bộ S33).
  - Quy chuẩn cải tiến từ S34:
    - Mỗi khái niệm giảng dạy theo cấu trúc chuẩn: Là gì -> Vì sao cần -> Cơ chế hoạt động -> Ví dụ thực tế.
    - Mini-check kiểm tra ngay sau từng phần.
    - Câu hỏi recall cuối buổi bám sát mức độ đã giảng dạy.
    - Giảm tải số lượng khái niệm mới mỗi buổi.
    - Dành 15-20 phút đầu Buổi 34 review củng cố sâu 5 nội dung trọng tâm của S33 (handlers, register, failed_when, block/rescue/always, safe deployment pipeline).
- Vận hành Dọn dẹp Tài nguyên (Cleanup):
  - Xóa sạch `/etc/nginx/conf.d/ansible-demo.conf`, `/tmp/ansible-nginx-demo.conf`, `/tmp/ansible-nginx-test.conf`, `/tmp/ansible-demo.txt`.
  - Xác nhận file cấu hình đã xóa và curl 8082 báo `Failed to connect`. Nginx được giữ nguyên vì đã có sẵn từ trước lab. Không có tài nguyên cloud phát sinh chi phí.
- Kết quả: **ĐẠT BUỔI 33 (Technical PASS / Timed FAIL Defense Mode; Reinforcement Required for Core Concepts)**.

## [2026-10-02] Session 34: Ansible Roles & Modular Playbooks
- Tiếp tục lộ trình Configuration Management: Nâng cấp kiến trúc playbook từ dạng monolithic (toàn bộ task/handler/template gom vào một file) sang cấu trúc Role-Based Modular Architecture.
- Ngày học: 2026-10-02.
- Môi trường & Không gian làm việc:
  - Workspace: `D:\Devops\labs\lab-34-ansible-roles`
  - WSL: `/mnt/d/Devops/labs/lab-34-ansible-roles`
  - Phiên bản: Ubuntu 24.04 WSL, `ansible-core 2.16.3`, Python 3.12.3, Nginx service.
- Refactor Kiến trúc Monolithic sang Role `nginx`:
  - Khởi tạo cấu trúc thư mục role chuẩn bằng `ansible-galaxy init roles/nginx` (hoặc khởi tạo thủ công).
  - Phân tách các thành phần chức năng:
    - `roles/nginx/tasks/main.yml`: Chứa toàn bộ chuỗi tác vụ triển khai (render candidate `/tmp`, validate `nginx -t -c`, copy atomic vào `/etc/nginx/conf.d/`, verify service và telemetry).
    - `roles/nginx/handlers/main.yml`: Chứa handler `Reload Nginx`.
    - `roles/nginx/templates/nginx-demo.conf.j2`: Chứa template Jinja2 động.
    - `roles/nginx/defaults/main.yml`: Định nghĩa các biến mặc định (`app_port: 8082`, `app_environment: staging`).
    - `roles/nginx/vars/main.yml`: Chứa các biến nội bộ role không muốn bị ghi đè.
    - `roles/nginx/meta/main.yml`: Khai báo metadata và dependencies của role.
- Quản trị Thứ bậc Ưu tiên Biến (Variable Precedence):
  - Phân tích sự khác biệt cốt lõi giữa `defaults/main.yml` và `vars/main.yml`:
    - `defaults`: Mức ưu tiên thấp nhất trong 22 cấp độ biến của Ansible, sinh ra để làm fallback an toàn và dễ dàng bị override bởi playbook/inventory.
    - `vars`: Mức ưu tiên rất cao (mức 16/22), dùng cho các biến cố định nội bộ của role mà người gọi không nên can thiệp.
- Cơ chế Triệu gọi Role (`roles:` vs `include_role`):
  - Khai báo tĩnh qua khối `roles:` ở cấp play: nạp role và thực thi tuần tự trước các task trong `tasks:`.
  - Hiểu cơ chế nạp động qua module `ansible.builtin.include_role`: cho phép nạp role có điều kiện (`when`), lặp qua role (`loop`), hoặc gọi lồng nhau linh hoạt tại runtime.
- Phát hiện & Khắc phục Phụ thuộc Ngầm (Hidden Dependency Isolation):
  - Triệu chứng: Template `nginx-demo.conf.j2` sử dụng biến `app_environment`. Nếu playbook bên ngoài không định nghĩa biến này, role sẽ bị vỡ.
  - Giải pháp: Khai báo fallback `app_environment: staging` trong `roles/nginx/defaults/main.yml`. Role trở nên khép kín, tự trị (autonomous) và an toàn tuyệt đối khi được tái sử dụng trong các playbook khác.
- Kiểm chứng Tính Lũy Thừa (Idempotency):
  - Chạy lại playbook lần 2: Toàn bộ task kiểm tra candidate, validate, copy, và handler đều báo `ok` hoặc không thay đổi (`changed=0`).
- Thực hành Failure Injection:
  - Cố tình đặt sai tên role hoặc sai đường dẫn role trong playbook: Ansible parser lập tức ngắt lệnh với `ERROR! the role '...' was not found in ...`.
  - Phân tích cơ chế Ansible tìm kiếm role tại thư mục `./roles/` tương đối với playbook hoặc qua biến cấu hình `roles_path`.
- Thử thách Defense Mode (Bắt đầu 04:28 UTC+7 ngày 2026-10-02):
  - Nhiệm vụ: Viết `playbook-defense.yml` tái sử dụng role `nginx` deploy trên port mới 8084, duy trì safe deployment pipeline, reload Nginx và xác minh HTTP 200.
  - Triển khai:
    - Gọi role `nginx` kèm biến override `vars: app_port: 8084`.
    - Apply playbook: Nginx validate cú pháp thành công, flush handlers reload dịch vụ.
    - HTTP health check: `curl http://localhost:8084` phản hồi HTTP 200.
    - Idempotency test: Chạy lại lượt 2 ghi nhận `changed=0`.
  - Kết quả Defense:
    - Technical Defense: **PASS**.
    - Safe Deployment & Idempotency: **PASS**.
    - Timed Requirement: **PASS** (Hoàn thành trong ~4 phút 02 giây / 10 phút hạn mức — Đạt chuẩn xuất sắc cả kỹ thuật và thời gian).
- Active Recall & Ôn tập:
  - Trả lời xuất sắc 7/7 câu hỏi về cấu trúc role, precedence của `defaults` vs `vars`, `roles:` vs `include_role`, hidden dependency, idempotency và quy trình troubleshooting.
- Dọn dẹp Tài nguyên (Cleanup PASS):
  - Thu hồi các file cấu hình port thử nghiệm trong `/etc/nginx/conf.d/` và file tạm trong `/tmp/`. Dịch vụ Nginx giữ nguyên ở trạng thái gốc, không tạo tài nguyên cloud, chi phí $0.
- Kết quả: **ĐẠT BUỔI 34 (Technical PASS / Timed PASS Defense Mode: ~4m02s)**.

## [2026-10-02] Session 35: Advanced Inventory & Multi-Host Automation
- Tiến độ lộ trình: Nâng cấp kiến trúc quản trị tự động hóa từ single host / localhost sang môi trường Multi-Host phân tán.
- Ngày học: 2026-10-02.
- Môi trường & Không gian làm việc:
  - Workspace: `D:\Devops\labs\lab-35-ansible-multihost`
  - WSL: `/mnt/d/Devops/labs/lab-35-ansible-multihost`
  - Managed Nodes: 2 Docker containers chạy Ubuntu SSH server (`web1` port 2221, `web2` port 2222), xác thực qua SSH key (`s35_key`).
- Dựng Môi trường Multi-Node Cục bộ với Docker & OpenSSH:
  - Viết `Dockerfile` tích hợp OpenSSH Server, tạo user `ansible` có quyền sudo không cần mật khẩu, cấu hình public key `s35_key.pub`.
  - Khởi chạy 2 container `web1` và `web2` với port mapping `2221:22` và `2222:22`.
- Thiết kế Cấu trúc Inventory Phân cấp Nâng cao:
  - Soạn thảo `inventory.ini`:
    - Nhóm hosts `[web]` gồm `web1 ansible_host=127.0.0.1 ansible_port=2221` và `web2 ansible_host=127.0.0.1 ansible_port=2222`.
    - Nhóm biến chung `[web:vars]`: `ansible_user=ansible`, `ansible_ssh_private_key_file=/home/minh123/.ssh/s35_key`, `ansible_python_interpreter=/usr/bin/python3`, và `ansible_ssh_common_args='-o StrictHostKeyChecking=accept-new'`.
- Quản trị Biến Phân tầng (`group_vars` vs `host_vars`):
  - Tạo `group_vars/web.yml`: Định nghĩa cấu hình chung cho cả nhóm (`http_port: 8080`, `app_env: staging`).
  - Tạo `host_vars/web2.yml`: Định nghĩa cấu hình ghi đè đặc thù cho máy 2 (`http_port: 8085`).
  - Xác minh quy tắc Variable Precedence: `host_vars` có mức ưu tiên cao hơn `group_vars`; khi chạy `playbook-vars.yml`, `web1` nhận port 8080 còn `web2` nhận port 8085 chính xác theo thiết kế.
- Kiểm tra Kết nối Đa máy & Điều hướng Host:
  - Chạy ad-hoc ping: `ansible -i inventory.ini all -m ping` nhận `SUCCESS` đồng thời trên cả `web1` và `web2`.
  - Sử dụng Host Patterns và `--limit`: Chạy `--limit web1` chỉ tác động lên máy `web1` mà không ảnh hưởng tới `web2`.
- Triển khai Cấu hình Đa máy & Kiểm chứng Lũy thừa (Idempotency):
  - Chạy `playbook-multihost.yml` triển khai Jinja2 template cho cả cụm: Lần đầu `changed=1`, lần hai chạy lại đạt `changed=0` trên cả 2 nodes.
- Thực hành Failure Injection & Phân biệt Bản chất Lỗi:
  - Dừng container `web2` (`docker stop web2`), chạy playbook kiểm tra:
    - `web2` báo lỗi `UNREACHABLE` (Connection refused trên port 2222).
    - `web1` vẫn tiếp tục thực thi thành công (`ok`, `SUCCESS`).
  - Phân tích sâu sự khác biệt:
    - `UNREACHABLE`: Lỗi tầng transport / hạ tầng mạng / SSH, Ansible lập tức loại bỏ node đó khỏi toàn bộ play.
    - `FAILED`: Kết nối thành công nhưng task thực thi bị lỗi hoặc vi phạm điều kiện logic nghiệp vụ.
- Thử thách Defense Mode (Hạn mức 10 phút):
  - Nhiệm vụ: Viết `playbook-defense.yml` triển khai file cấu hình multi-host với port override, kiểm tra trạng thái và xác minh tính lũy thừa.
  - Kết quả Defense:
    - Technical Defense: **PASS**.
    - Idempotency: **PASS** (`changed=0`).
    - Timed Requirement: **PASS** (Hoàn thành trong ~5 phút 34 giây / 10 phút hạn mức).
- Active Recall & Ôn tập:
  - Trả lời đúng 7/7 câu hỏi về multi-host inventory, group_vars vs host_vars precedence, --limit, idempotency, UNREACHABLE vs FAILED.
- Dọn dẹp Tài nguyên (Cleanup PASS):
  - Dừng và gỡ bỏ các container Docker `web1`, `web2`, xóa các file tạm.
- Kết quả: **ĐẠT BUỔI 35 (COMPLETED - Technical PASS / Timed PASS Defense Mode: ~5m34s)**.

## [2026-10-04] Session 36: Ansible Tags, Vault & Secrets Management
- Tiếp tục lộ trình Configuration Management: Hoàn thành chuyên đề về kỹ thuật gắn nhãn tác vụ (Tags), mã hóa và quản trị dữ liệu mật (Vault & Secrets) và kiểm định bảo mật hệ thống.
- Ngày học: 2026-10-03 và hoàn thành ngày 2026-10-04.
- Môi trường & Không gian làm việc:
  - Workspace: `D:\Devops\labs\lab-36-ansible-tags-vault`
  - WSL: `/mnt/d/Devops/labs/lab-36-ansible-tags-vault`
  - Ansible Core 2.16.3, Python 3.12.3.
- Quản trị Tác vụ với Ansible Tags (`tags`):
  - Khai báo nhãn `tags: [deploy]`, `tags: [secret]`, `tags: [verify]` trên từng task.
  - Thực thi chọn lọc với `--tags`: Chỉ chạy các task được gắn tag mong muốn (ví dụ `--tags deploy`).
  - Loại trừ task với `--skip-tags`: Bỏ qua các task nặng hoặc nhạy cảm khi debug.
- Mã hóa Bí mật với Ansible Vault cơ bản:
  - Khởi tạo file biến chứa mật khẩu `vars/vault.yml` (`db_user: db_admin`, `db_password: SuperSecretPassword123!`).
  - Mã hóa tệp tin bằng lệnh `ansible-vault encrypt vars/vault.yml` với mật khẩu an toàn.
  - Kiểm tra tệp tin trên disk: Nội dung đã chuyển thành định dạng mã hóa `$ANSIBLE_VAULT;1.1;AES256`.
- Tích hợp Tệp tin Biến Mã hóa (`vars_files`):
  - Khai báo `vars_files: - vars/vault.yml` trong playbook.
  - Thực thi playbook kèm cờ giải mã `--ask-vault-pass` (hoặc `--vault-password-file`).
- Quản trị An toàn Bí mật (Secret at Rest vs Runtime):
  - Bảo vệ at rest: File mã hóa an toàn trên disk và an toàn khi commit lên Git.
  - Bảo vệ runtime & Chống rò rỉ log: Bắt buộc sử dụng `no_log: true` trên mọi task thao tác trực tiếp với secret để ngăn Ansible in giá trị biến ra console output hoặc ghi vào file log hệ thống.
  - Phân quyền tệp tin bí mật trên filesystem máy đích: Luôn gán `mode: "0600"` (chỉ owner có quyền đọc/ghi, chặn toàn bộ group và others).
- Failure Injection:
  - Cố tình nhập sai mật khẩu Vault khi chạy `ansible-playbook`: Ansible lập tức ngắt lệnh với lỗi xác thực mật mã (`Decryption failed`), không thể đọc biến mật.
- Kiểm định Tự động với Assertion:
  - Sử dụng `ansible.builtin.stat` kết hợp `ansible.builtin.assert` kiểm tra tự động sự tồn tại của file và kiểm chứng chính xác `stat.mode == "0600"`.
- Kiểm chứng Tính Lũy Thừa (Idempotency):
  - Chạy lại playbook lần 2: Đạt `changed=0`.
- Thử thách Defense S36:
  - Technical Defense: **PASS** (Viết `playbook-defense.yml` kết hợp tags deploy/secret/verify, vars_files mã hóa vault, no_log: true, mode 0600 và stat+assert kiểm định).
- Active Recall & Dọn dẹp:
  - Trả lời chính xác 7/7 câu hỏi về tags, vault encrypt, no_log, 0600 và stat/assert.
  - Dọn dẹp an toàn các file tạm trên disk (`/tmp/s36-defense-*.txt`), Cleanup PASS.
- Kết quả: **ĐẠT BUỔI 36 (COMPLETED - Technical PASS Defense Mode)**.

## [2026-10-04] Session 37: Kubernetes Fundamentals: Cluster, Pod, Deployment
- Tiến độ lộ trình: Bước chuyển sang mảng Container Orchestration với Kubernetes, thiết lập cụm cục bộ, vòng đời Pod và quản trị Deployment tự phục hồi.
- Ngày học: 2026-10-04.
- Môi trường & Không gian làm việc:
  - Workspace: `D:\Devops\labs\lab-37-kubernetes-fundamentals`
  - WSL: `/mnt/d/Devops/labs/lab-37-kubernetes-fundamentals`
  - Công cụ: `kubectl v1.37.0`, `kind v0.33.0`, WSL2 Ubuntu 24.04, Docker Engine 28.0.1.
- Dựng cụm Kubernetes cục bộ với Kind:
  - Cấu hình topology cụm `s37` qua `kind-config.yaml` gồm 1 Control-Plane (`s37-control-plane`) và 2 Worker nodes (`s37-worker`, `s37-worker2`).
- Xử lý sự cố hạ tầng Bootstrap cụm (Troubleshoot Cluster Bootstrap Failure):
  - Kubelet fail bootstrap khi khởi động container node, kiểm tra log phát hiện cờ kiểm tra kernel: `failCgroupV1=true`.
  - Chẩn đoán nguyên nhân: Kubernetes 1.37 yêu cầu cgroup v2, trong khi WSL2, Docker daemon và kind node container đều đang chạy cgroup v1.
  - Xử lý: Cập nhật cấu hình `.wslconfig` trên host Windows để kích hoạt cgroup v2 cho WSL2 (`systemd=true`), khởi động lại WSL và Docker.
  - Xác minh thành công: WSL hiển thị `cgroup2fs` và Docker đạt `CgroupVersion=2`.
  - Khởi tạo lại cụm bằng `kind create cluster --config kind-config.yaml --name s37`: Cả 3 node đều đạt trạng thái `Ready`.
- Kiến trúc nền tảng Kubernetes:
  - Nắm vững và thực hành tương tác với Control Plane (API Server, etcd, Scheduler, Controller Manager) và Worker Node (kubelet, containerd).
- Triển khai Standalone Pod:
  - Viết manifest khai báo `pod-nginx.yaml` (`apiVersion: v1`, `kind: Pod`).
  - Vận hành thành thạo bộ lệnh `kubectl`: `apply`, `get`, `describe`, `logs`, `exec`.
  - Quan sát kube-scheduler tự động đặt Pod lên worker node.
  - Phân tích chuỗi sự kiện vòng đời (Events): `Scheduled` -> `Pulling` -> `Pulled` -> `Created` -> `Started`.
  - Chứng minh tính chất phù du (Ephemeral): Khi xóa standalone Pod bằng `kubectl delete pod`, Pod bị hủy hoàn toàn và không được tự động tạo lại.
- Quản trị Deployment & Tính tự phục hồi (Self-Healing):
  - Viết manifest `deployment-nginx.yaml` với `replicas: 3`.
  - Phân tích cấu trúc phân cấp: `Deployment` -> `ReplicaSet` -> `Pods`.
  - Kiểm tra quan hệ sở hữu (`ownerReferences`): Pod trỏ owner về ReplicaSet; ReplicaSet trỏ owner về Deployment.
  - Failure Injection: Xóa 1 Pod thuộc ReplicaSet, ReplicaSet controller lập tức phát hiện lệch desired state và khởi tạo Pod mới thay thế (Self-healing PASS).
  - Điều chỉnh quy mô (Scaling): Dùng `kubectl scale` nâng 3 -> 5 replicas; sau đó re-apply manifest `replicas: 3`, quan sát Declarative Reconciliation tự động thu hồi 2 Pod dư thừa để đưa hệ thống về đúng 3 Pods.
- Xử lý sự cố cú pháp Manifest (YAML Troubleshooting):
  - Bắt lỗi cú pháp thụt lề: `spec.template.spec.containers: Required value` do đặt sai cấp indentation trong spec template; chẩn đoán và sửa đúng cấu trúc YAML.
- Đánh giá năng lực & Defense Mode:
  - Checkpoint: 6/6 PASS.
  - Defense Mode S37: Tự viết `deployment-defense.yaml` (`s37-defense`, 2 replicas), xóa 1 Pod, quan sát Pod mới được ReplicaSet tạo và Deployment trở lại 2/2 Ready. Đạt **Technical PASS** (không chấm giờ).
  - Active Recall: 5/5 PASS.
  - Dọn dẹp tài nguyên (Cleanup PASS): Cụm cluster `s37` đã được xóa sạch sau buổi học (`kind delete cluster --name s37`), manifest YAML được lưu trữ tại `labs/lab-37-kubernetes-fundamentals` làm bằng chứng.
- Kết quả: **ĐẠT BUỔI 37 (COMPLETED - Technical PASS Defense Mode)**.

## [2026-10-05] Session 38: Kubernetes Service & Networking
- Tiếp tục lộ trình Container Orchestration: Tìm hiểu cơ chế mạng dịch vụ trong Kubernetes, giải quyết bài toán Pod IP phù du bằng Service, phân giải DNS nội bộ, định tuyến ClusterIP và NodePort.
- Ngày học: 2026-10-05.
- Môi trường & Không gian làm việc:
  - Workspace: `D:\Devops\labs\lab-38-kubernetes-service-networking`
  - WSL: `/mnt/d/Devops/labs/lab-38-kubernetes-service-networking`
  - Cluster: Cụm Kind riêng biệt `s38` (1 Control-Plane + 2 Worker nodes).
- Khởi tạo cụm và Backend Deployment:
  - Dựng cụm kind `s38` với 1 Control-Plane và 2 Worker nodes, kiểm tra cả 3 nodes đều `Ready`.
  - Triển khai backend Deployment Nginx 3 replicas mang nhãn `app: s38-backend`.
  - Nhận thức vấn đề: Địa chỉ Pod IP có tính chất phù du (thay đổi khi recreate/reschedule); ứng dụng client không thể kết nối trực tiếp qua Pod IP mà cần một tầng trừu tượng ổn định là Kubernetes Service.
- Cấu hình ClusterIP Service & Label Selector:
  - Khởi tạo Service loại `ClusterIP` (`s38-service`) sử dụng `selector: app: s38-backend`.
  - Khám phá `EndpointSlice`: Trên Kubernetes v1.37, EndpointSlice thay thế Endpoints legacy để theo dõi danh sách IP backend có khả năng mở rộng cao; xác nhận EndpointSlice tự động thu nạp 3 IP của 3 backend Pods.
- Khám phá Dịch vụ & Phân giải Tên miền Nội bộ (Service Discovery / CoreDNS):
  - Khởi tạo client Pod BusyBox (`s38-client`).
  - Gửi HTTP request tới DNS service name nội bộ (`http://s38-service:8080`), nhận phản hồi trang chào Nginx thành công.
- Phân biệt Rạch ròi Cổng Mạng:
  - Ánh xạ rõ ràng qua manifest: `port: 8080` (cổng dịch vụ mở trên ClusterIP/NodePort) vs `targetPort: 80` (cổng thực tế mà container Nginx trong Pod lắng nghe).
- Mở rộng Truy cập với NodePort Service:
  - Nâng cấp Service sang kiểu `NodePort` với `port: 8080`, `targetPort: 80`, `nodePort: 30080`.
  - Kiểm tra truy cập đa node: Gửi curl tới IP của node worker 1 (`172.22.0.3:30080`) và node worker 2 (`172.22.0.2:30080`), cả hai đều trả về Nginx thành công nhờ cơ chế chuyển tiếp traffic của kube-proxy.
  - Nắm vững khái niệm LoadBalancer ở tầng cloud provider; hiểu lý do không giả lập cloud LB trong môi trường Kind local.
- Thực hành Failure Injection & Quy trình Xử lý Sự cố Mạng:
  - Cố tình sửa selector của Service thành `app: s38-backend-broken`.
  - Quan sát triệu chứng: Service object vẫn tồn tại bình thường nhưng `EndpointSlice` bị xóa sạch (0 endpoints), request tới NodePort lập tức bị từ chối/timeout.
  - Khắc phục sự cố: Đối chiếu selector của Service với labels của Pods và EndpointSlice; sửa selector về đúng `app: s38-backend` -> EndpointSlice lập tức phục hồi 3 backend IP -> traffic thông suốt trở lại.
  - Xử lý sự cố Pod phase: Client Pod chuyển sang trạng thái `Completed/Succeeded` do lệnh `sleep 3600` đã chạy hết thời gian; chẩn đoán chính xác đây là hành vi kết thúc bình thường của tiến trình Linux, không phải lỗi mạng hay crash, tạo lại client Pod với `sleep 86400`.
- Thử thách Defense S38:
  - Tự viết ClusterIP Service `s38-defense-service` với selector `app: s38-backend`, map `port: 8081` -> `targetPort: 80`.
  - Kiểm tra EndpointSlice ghi nhận đủ 3 endpoints backend.
  - Gửi request từ `s38-client` qua DNS `curl http://s38-defense-service:8081` nhận trang chào Nginx thành công.
  - Kết quả Defense: Đạt **Technical PASS** (không chấm giờ).
- Đánh giá Năng lực: Trả lời chính xác 6/6 câu hỏi Active Recall.
- Dọn dẹp Tài nguyên (Cleanup PASS):
  - Đã xác minh bằng chứng: Lệnh `kind delete cluster --name s38` đã được thực thi; `kind get clusters` và `docker ps -a` xác nhận cụm s38 và các container đã được dọn sạch hoàn toàn; lưu trữ manifest YAML tại `labs/lab-38-kubernetes-service-networking` làm bằng chứng.
- Kết quả: **ĐẠT BUỔI 38 (COMPLETED - Technical PASS Defense Mode)**.











