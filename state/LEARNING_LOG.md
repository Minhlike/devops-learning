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





