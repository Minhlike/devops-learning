# CURRENT LEARNING PHASE

- **Current Phase:** PHASE 6 — AWS Cloud Infrastructure
- **Current Status:** Hoàn thành Buổi 24 — AWS Storage & IAM Role for EC2. Chuẩn bị Buổi 25 — AWS RDS & Managed Database Fundamentals.
- **Current Week:** Tuần 6
- **Completed Outputs:**
  1. **Buổi 13 — Python Fundamentals for DevOps Automation:**
     - Sử dụng `pathlib` với `exists()`, `is_file()`, `read_text()`, `glob()` xử lý đường dẫn an toàn.
     - Đọc và phân tích log tìm chuỗi `ERROR` và mã HTTP `500`.
     - Tổng hợp báo cáo dạng `dict` và xuất file JSON bằng `json.dump()` (`health_report.json`).
     - Tương tác với HĐH qua `subprocess.run()`, đọc `stdout`, `stderr`, kiểm tra `returncode` và điều khiển mã thoát bằng `sys.exit()`.
     - Thực hành Failure Injection: thiếu file log, lệnh trả returncode non-zero, executable không tồn tại.
     - Viết và hoàn thiện `health_report.py` và `health_report.json`.
     - Kết quả: **ĐẠT BUỔI 13**.
  2. **Buổi 14 — Docker Fundamentals:**
     - Cài đặt và vận hành Docker Engine native trên Ubuntu 24.04 WSL.
     - Phân biệt khái niệm cốt lõi Image vs Container.
     - Thành thạo bộ lệnh container: `run`, `start`, `stop`, `exec`, `rm`.
     - Hiểu bản chất PID 1 và vòng đời container (Container Lifecycle).
     - Phân biệt Writable Layer vs xoá/tạo lại container; sử dụng Named Volumes cho Data Persistence.
     - Cấu hình Port Publishing `HOST_PORT:CONTAINER_PORT`.
     - Nắm vững Bridge Network, hiện tượng Localhost Isolation trong container, tạo User-defined Network và Docker DNS theo Container Name.
     - Viết `Dockerfile`, hiểu Build Context, Image Layers + Cache, đánh tag/versioning `my-web:v1/v2`.
     - Cấu hình `.gitignore` và `.dockerignore` loại bỏ file rác.
     - Xử lý các dạng lỗi Failure Injection: Build-time failure, container start failure (Created), application crash (Exited + ExitCode).
     - Giám sát và chẩn đoán container với `docker logs`, `inspect`, `top`.
     - Phân biệt cơ chế `CMD` vs `ENTRYPOINT`.
     - Kết quả: **ĐẠT BUỔI 14**.
  3. **Buổi 15 — Docker Compose & Multi-Container Application:**
     - Nắm vững khái niệm Docker Compose cơ bản và quản lý multi-container ứng dụng đa dịch vụ.
     - Cấu hình `compose.yaml`: `services`, `build`, `image`, `ports`, `environment`, `volumes`, `networks`.
     - Xây dựng mô hình ứng dụng Flask app + PostgreSQL database.
     - Cấu hình Compose Network và cơ chế Docker DNS phân giải theo Service Name (`db`).
     - Thiết lập cơ chế `healthcheck` trên DB và điều kiện phụ thuộc `depends_on` với `condition: service_healthy`.
     - Gắn Named Volume cho PostgreSQL duy trì dữ liệu bền vững qua các lần restart.
     - Phân biệt rõ `docker compose down` (giữ volume) vs `docker compose down -v` (xóa volume làm mất dữ liệu DB).
     - Quản lý biến môi trường an toàn bằng `.env` và mẫu `.env.example`, đảm bảo `.env` được bảo vệ bởi `.gitignore`.
     - Sử dụng `docker compose config` kiểm tra cú pháp YAML.
     - Thực hành Failure Injections: Sai `DB_HOST` (DNS resolution failure), sai `DB_PASSWORD` (PostgreSQL authentication failure), `docker compose down -v` gây mất dữ liệu DB.
     - Phục hồi stack ứng dụng hoàn chỉnh: `app` Up, `db` healthy, `curl http://localhost:8086` trả `"status":"ok"`.
     - Kết quả: **ĐẠT BUỔI 15**.
  4. **Buổi 16 — Advanced Docker Compose & Production Operations:**
     - Chuyển đổi Flask development server sang Production WSGI Server Gunicorn (Master + 2 Workers).
     - Thực hành Failure Injection: kill một worker process, Gunicorn master tự động spawn worker mới duy trì khả năng phục vụ.
     - Hiểu bản chất PID 1 trong container và tầm quan trọng của Process Management.
     - Thêm chính sách tự phục hồi `restart: unless-stopped` trong `compose.yaml`.
     - Thực hành Failure Injection: kill Gunicorn PID 1, Docker Engine tự động restart container và xác minh `RestartCount` tăng.
     - Tạo Flask endpoint `/health` và cấu hình Docker `healthcheck` cho ứng dụng.
     - Hiểu rõ nguyên lý `Up != Healthy`.
     - Thực hành Failure Injection cấu hình sai healthcheck URL: container vẫn `Up` nhưng Docker status báo `unhealthy`; hiểu rằng status `unhealthy` không tự động kích hoạt `restart` policy.
     - Khôi phục healthcheck URL chính xác đưa status trở lại `healthy`.
     - Thiết lập Resource Limits: `cpus: "0.50"`, `mem_limit: 256m`, `memswap_limit: 256m`.
     - Xác minh CPU limit bằng `docker stats`: CPU hog process bị throttle ở mức ~50%.
     - Xác minh Memory limit: process test cấp phát 300 MiB bị OOM kill, exit code `137`, `OOMKilled=true`; Gunicorn master vẫn sống nên container không bị restart.
     - Thực hành Graceful Shutdown với `docker compose stop app`: Gunicorn nhận SIGTERM, workers exit sạch sẽ, master shutdown, container kết thúc với `Exited (0)`.
     - Start lại app và kiểm tra `/health` phản hồi `healthy`.
     - Kết quả: **ĐẠT BUỔI 16**.
  5. **Buổi 17 — Docker Capstone Project & Container Registry Deployment:**
     - Xây dựng Flask API Capstone hoàn chỉnh với các endpoints: `GET /`, `GET /health`, `GET /visits`, `POST /visits`.
     - Sử dụng Gunicorn (2 workers), PostgreSQL `postgres:17-alpine` (hostname `db`, port `5432`, named volume `db-data`).
     - Soạn thảo `Dockerfile` tối ưu dựa trên `python:3.12-slim` và `.dockerignore`.
     - Cấu hình `compose.yaml`: `app` + `db`, Docker DNS, `healthcheck`, `depends_on: service_healthy`, `restart: unless-stopped`, resource limits (CPU `0.50`, mem `256m`, memswap `256m`), host publish `8087:8000`.
     - Kiểm tra bảo mật `.env` local bị `.gitignore` tuyệt đối, tạo `.env.example`.
     - Kiểm tra hoạt động ứng dụng: `GET /`, `GET /health`, `POST /visits` tăng counter `0 -> 1 -> 2`.
     - Chứng minh Data Persistence: `docker compose down` xoá container nhưng named volume `db-data` còn nguyên; khi dựng lại stack counter vẫn bằng 2.
     - Đăng nhập Docker Hub (`minhhociot`), đánh tag `minhhociot/docker-capstone:v1`, push image lên Docker Hub (digest `sha256:6823167bb94c7ac57320f69a886e50ebecf53139fd03d8ab8059d9649410b0bc`).
     - Thực hành xoá image local, pull image từ Docker Hub và cập nhật `compose.yaml` chuyển từ `build: ./app` sang `image: minhhociot/docker-capstone:v1`.
     - Deploy thành công trực tiếp từ registry image; `docker inspect` xác nhận `Image=minhhociot/docker-capstone:v1` và `RepoDigest` khớp digest registry.
     - Kết quả: **ĐẠT BUỔI 17 (HOÀN THÀNH CAPSTONE PHASE 4)**.
  6. **Buổi 18 — CI/CD Fundamentals with GitHub Actions:**
     - Xây dựng Flask API microservice (`app.py`, Gunicorn 2 workers, endpoint `/`, `/health`).
     - Thiết lập Unit Test với Flask Test Client (`test_app.py`) kiểm tra HTTP status code 200 và dữ liệu JSON response.
     - Tích hợp công cụ Linter hiện đại Ruff (Rust) tối ưu tốc độ quét mã nguồn tĩnh và chuẩn hóa quy chuẩn PEP 8.
     - Soạn thảo GitHub Actions Workflow (`.github/workflows/ci.yml`) đa job (`test` và `build-and-push`) kết nối qua quan hệ phụ thuộc `needs: test`.
     - Quản lý an toàn GitHub Repository Secrets: `DOCKER_HUB_USERNAME` và `DOCKER_HUB_TOKEN` chống rò rỉ credential ra log.
     - Tự động hóa build Docker image từ runner cloud và push lên Docker Hub Registry với tag kép `:latest` và `:${{ github.sha }}`.
     - Kéo image `minhhociot/devops-lab18:latest` từ Docker Hub về máy local qua WSL và kiểm thử endpoint `/health` trả về `healthy`.
     - Hoàn thành chuỗi Failure Injections: sửa lỗi linter `I001`, bắt lỗi logic test `1.0.0 != 2.0.0`, khắc phục sự cố xác thực Registry 401 Unauthorized, và xử lý lỗi thiếu `Dockerfile` trong build context.
     - Kết quả: **ĐẠT BUỔI 18 (XUẤT SẮC)**.
  7. **Buổi 19 — Advanced GitHub Actions & Multi-Stage CI/CD Workflows:**
     - Nâng cấp CI Pipeline lên Matrix Build chạy song song trên 3 phiên bản Python: 3.10, 3.11, 3.12 sử dụng `strategy.matrix` và `fail-fast: false`.
     - Cả 3 matrix jobs chạy độc lập và đều PASS thành công.
     - Tối ưu hóa pipeline với Pip Dependency Caching qua `actions/setup-python` (`cache: "pip"`, `cache-dependency-path: labs/lab-18-ci-cd/app/requirements.txt`).
     - Tích hợp kiểm tra độ bao phủ mã nguồn với `coverage>=7.6.0`, `coverage run`, `coverage report` và xuất báo cáo `coverage.xml`.
     - Thiết lập Quality Gate tự động: Chặn pipeline nếu Test Coverage dưới 80% (`--fail-under=80`).
     - Upload báo cáo coverage thành CI Artifacts riêng biệt cho từng phiên bản Python (`coverage-python-3.10`, `3.11`, `3.12`) qua `actions/upload-artifact@v4`.
     - Bảo vệ deployment: Cấu hình điều kiện chỉ chạy job `build-and-push` khi có sự kiện push vào nhánh `main`. Nhánh feature chỉ chạy test/lint/coverage, không push Docker image.
     - Tạo feature branch `feature/lab-19-matrix-ci` và mở Pull Request #1 vào `main`.
     - Thiết lập GitHub Ruleset bảo vệ nhánh `main`: Bắt buộc Pull Request, chặn force push, yêu cầu 3 status checks Matrix Test (Python 3.10, 3.11, 3.12) pass mới cho merge.
     - Thực hành Failure Injection: Cố tình nâng threshold coverage lên 101% khiến CI báo đỏ và PR bị chặn bởi required checks. Khôi phục về 80% CI xanh trở lại.
     - Merge PR #1 thành công vào `main` (commit `68bb478`).
     - Sau merge: Matrix tests, upload artifact và job `build-and-push` (Docker Buildx, Docker Hub login, push image) đều chạy thành công trên `main`.
     - Kết quả: **ĐẠT BUỔI 19 (XUẤT SẮC)**.
  8. **Buổi 20 — Deployment Environments, Approval Gates & Rollback:**
     - Thiết lập GitHub Environments đa tầng: `staging` và `production`.
     - Cấu hình Deployment Protection Rules: Thiết lập Required Reviewers / manual approval gate bảo vệ môi trường `production`.
     - Xây dựng luồng pipeline tự động phân tầng: `test matrix` $\rightarrow$ `build-and-push` $\rightarrow$ `deploy-staging` $\rightarrow$ `smoke test staging` $\rightarrow$ `deploy-production`.
     - Bảo vệ an toàn nhánh: Nhánh feature chỉ kích hoạt test matrix, không deploy lên staging/production.
     - Tự động hóa sau merge `main`: Staging tự động deploy và smoke test PASS; Production dừng lại chờ review thủ công và chỉ deploy sau khi được phê duyệt (Approval).
     - Áp dụng nguyên lý Artifact Immutability: Sử dụng image tag bất biến `${{ github.sha }}` cho toàn bộ chu trình deploy thay vì phụ thuộc vào tag mutable `latest`.
     - Triển khai cơ chế Image Promotion: Sau khi production smoke test `/health` thành công, image được gắn thêm tag `stable` đại diện cho bản phát hành tốt nhất hiện tại.
     - Tích hợp Trigger thủ công `workflow_dispatch` với input boolean `rollback` để kích hoạt kịch bản khôi phục thảm họa.
     - Thiết kế job `rollback-production`: Chỉ chạy khi `rollback=true`, vẫn tuân thủ Environment Protection Rules của `production`, kéo image `:stable`, chạy smoke test `/health` và dọn dẹp container.
     - Thực hành Manual Rollback thật trên GitHub Actions UI (Run #28: SUCCESS), kiểm chứng toàn bộ các job build/test/staging được bỏ qua (skipped) đúng thiết kế khi kích hoạt rollback.
     - Kết quả: **ĐẠT BUỔI 20 (XUẤT SẮC)**.
  9. **Buổi 21 — DevSecOps Security Scanning, Automated Releases & Phase 5 Capstone:**
     - Tích hợp công cụ SAST Bandit quét mã nguồn Python tĩnh vào CI Pipeline nhằm phát hiện các lỗ hổng bảo mật ứng dụng.
     - Thực hành Failure Injection với Bandit: Bandit phát hiện binding Flask development server `app.run(host='0.0.0.0')` tiềm ẩn rủi ro lộ lọt port; đã tiến hành gỡ bỏ code dev thừa, chuyển quyền chạy hoàn toàn cho Gunicorn WSGI server.
     - Tích hợp Gitleaks GitHub Action quét bảo mật toàn bộ lịch sử commit (`fetch-depth: 0`).
     - Thực hành Failure Injection với Gitleaks: Thấu hiểu sâu sắc nguyên lý bảo mật rằng xóa file chứa secret bằng một commit mới là không đủ; secret vẫn tồn tại vĩnh viễn trong Git history; đã khắc phục bằng cách rewrite commit history và loại bỏ secret triệt để.
     - Tích hợp Aqua Security Trivy vào CI/CD: Quét lỗ hổng bảo mật (CVE) của Docker image trước khi đẩy lên registry, cấu hình chốt chặn nghiêm ngặt ngắt pipeline nếu phát hiện lỗ hổng mức `HIGH,CRITICAL` (`--severity HIGH,CRITICAL --exit-code 1`).
     - Hoàn thiện luồng CI/CD + DevSecOps hoàn chỉnh trên nhánh `main`:
       `Matrix Test (Python 3.10, 3.11, 3.12)` + `Ruff Lint` + `Coverage Gate 80%` + `Bandit SAST` + `Gitleaks`
       $\rightarrow$ `Docker Build`
       $\rightarrow$ `Trivy CVE Scanning`
       $\rightarrow$ `Docker Hub Push (Immutable SHA Tag)`
       $\rightarrow$ `Staging Deploy & Smoke Test (/health)`
       $\rightarrow$ `Production Manual Approval Gate (Required Reviewers)`
       $\rightarrow$ `Production Deploy & Smoke Test (/health)`
       $\rightarrow$ `Image Promotion (:stable tag)`
       $\rightarrow$ `Rollback Disaster Readiness`.
     - Mở và merge thành công PR #6 tích hợp toàn diện các DevSecOps security gates vào repository.
     - Tích hợp Google Release Please (`google-github-actions/release-please-action`) theo mô hình manifest mode (`release-please-config.json`, `.release-please-manifest.json`).
     - Cấu hình phân quyền GitHub Actions cho phép tự động tạo và phê duyệt Pull Request (`Settings` $\rightarrow$ `Actions` $\rightarrow$ `General` $\rightarrow$ `Allow GitHub Actions to create and approve pull requests`).
     - Tự động hóa Semantic Versioning & Conventional Commits: Merge thành công Release PR #8 (`chore(main): release 1.1.0`).
     - Tự động sinh `CHANGELOG.md`, cập nhật file `version.txt` và tự động gắn Git tag / xuất bản GitHub Release `v1.1.0`.
     - Kết quả: **ĐẠT BUỔI 21 — HOÀN THÀNH PHASE 5 (TỐT NGHIỆP XUẤT SẮC)**.
  10. **Buổi 22 — AWS Foundations, IAM, CLI & Cost Safety:**
      - Nắm vững kiến trúc hạ tầng toàn cầu của AWS: Phân biệt Region, Availability Zone (AZ) và Data Center; hiểu Shared Responsibility Model giữa AWS (Security OF the Cloud) và khách hàng (Security IN the Cloud).
      - Thiết lập an toàn tài khoản tối cao: Kích hoạt Root MFA (Hardware/Virtual Authenticator), không dùng root user cho tác vụ hàng ngày.
      - Cấu hình quản trị chi phí và ngân sách: Tạo AWS Zero-Spend Budget với cảnh báo chi phí tức thì qua email khi phát sinh vượt ngưỡng $0.01.
      - Xây dựng hệ thống IAM theo nguyên tắc Least Privilege:
        - Tạo IAM User `minh-devops` không cấp direct policy.
        - Tạo IAM Group `devops-lab`.
        - Soạn thảo Customer-managed Policy `DevOpsLabReadOnly` phân quyền chi tiết đọc tài nguyên EC2 metadata và S3.
        - Hiểu cơ chế implicit deny (mọi hành động không được Explicit Allow thì mặc định bị Deny).
      - Phân biệt rõ IAM Role, Trust Policy (ai được phép assume role) và Permission Policy (role được làm gì).
      - Cài đặt và vận hành AWS CLI v2 trên Ubuntu 24.04 WSL, cấu hình region mặc định `ap-southeast-1` (Singapore).
      - Xác thực CLI an toàn qua `aws login` với Temporary Credentials ngắn hạn (STS token), kiên quyết không tạo static long-term Access Key.
      - Kiểm thử và xác minh quyền qua CLI:
        - `aws ec2 describe-regions` và `aws ec2 describe-availability-zones` thành công.
        - `aws s3api list-buckets` (`ListAllMyBuckets`) thành công.
      - Thực hành Failure Injection: Chạy `aws ec2 describe-instances` bị chặn với lỗi `UnauthorizedOperation` chính xác theo thiết kế Least Privilege do policy chỉ cho phép xem regions/AZs, không cho phép xem instances.
      - Chẩn đoán và xử lý sự cố (Troubleshooting): Sửa lỗi liên kết symlink `~/.aws` giữa Windows và WSL; khắc phục phiên xác thực hết hạn (`expired aws login session`) bằng quy trình re-authenticate.
      - Kết quả: **ĐẠT BUỔI 22 (XUẤT SẮC)**.
  11. **Buổi 23 — AWS EC2 & VPC Fundamentals:**
      - Hiểu sâu sắc bản chất mạng VPC (Virtual Private Cloud), Subnet và mối quan hệ ràng buộc: Mỗi Subnet nằm trọn vẹn trong một Availability Zone (AZ) duy nhất.
      - Khảo sát và phân tích Default VPC tại region `ap-southeast-1` (Singapore), kiểm tra các default subnets phân bổ qua 3 AZ (`ap-southeast-1a`, `ap-southeast-1b`, `ap-southeast-1c`).
      - Nắm vững vai trò của Internet Gateway (IGW) và Route Table trong việc định tuyến Public Subnet; xác minh route mặc định `0.0.0.0/0` trỏ ra Internet Gateway.
      - Phân tích cơ chế hoạt động của Security Group: Tường lửa ảo cấp độ máy chủ có tính chất stateful (tự động cho phép traffic phản hồi mà không cần mở outbound tương ứng).
      - Thiết lập Security Group độc lập `web-sg`, tuân thủ nguyên tắc Least Privilege: Chỉ mở inbound rule cho giao thức TCP port 80 từ mọi nguồn (`0.0.0.0/0`), không mở SSH công khai không cần thiết.
      - Phân biệt Amazon Machine Image (AMI) và Instance Types; lựa chọn image chuẩn `Amazon Linux 2023` và instance type `t3.micro` (2 vCPU, 1 GiB RAM) tối ưu chi phí trong Free Tier.
      - Tự động hóa triển khai hạ tầng EC2 bằng AWS CLI (`aws ec2 run-instances`):
        - Sử dụng User Data script (`user-data.sh`) để tự động cài đặt `nginx`, tạo trang HTML tùy biến (`Hello from AWS EC2 - DevOps Learning - Session 23`) và enable systemd service ngay khi máy chủ khởi động lần đầu.
        - Gán Public IPv4 tự động và kiểm thử website thật ngoài Internet bằng lệnh `curl http://<PUBLIC_IP>` trả về HTTP 200 kèm nội dung chính xác.
      - Thực hành Failure Injection kiểm chứng Stateful Firewall:
        - Thu hồi (revoke) rule TCP/80 trong Security Group $\rightarrow$ lệnh `curl` tới Public IP bị treo timeout ngay lập tức.
        - Khôi phục (authorize) lại rule TCP/80 $\rightarrow$ website lập tức phản hồi thông suốt trở lại mà không cần khởi động lại dịch vụ web hay máy chủ.
      - Tuân thủ nghiêm ngặt nguyên tắc Cost Safety & Resource Cleanup:
        - Terminate EC2 instance ngay sau khi hoàn thành lab.
        - Xóa Security Group `web-sg`.
        - Xác minh Public IPv4 được giải phóng hoàn toàn về pool của AWS, tránh phát sinh chi phí IPv4 theo giờ.
      - Bảo vệ an toàn quyền hạn (Least Privilege):
        - Thu hồi toàn bộ quyền ghi tạm thời đã cấp cho user để làm lab.
        - Kiểm chứng bằng kỹ thuật `--dry-run` và lệnh `CreateSecurityGroup`: AWS API trả về lỗi `UnauthorizedOperation` chính xác theo thiết kế ban đầu.
      - Kết quả: **ĐẠT BUỔI 23 (XUẤT SẮC)**.
  12. **Buổi 24 — AWS Storage & IAM Role for EC2:**
      - Nắm vững mô hình phân loại lưu trữ tổng quát trên AWS: Block Storage (EBS), Object Storage (S3) và Ephemeral Local Storage (Instance Store); hiểu rõ lý do thư mục dữ liệu PostgreSQL phù hợp với Block Storage/EBS hơn Object Storage do yêu cầu đọc ghi ngẫu nhiên (random read/write), POSIX compliance và độ trễ thấp.
      - Quản trị dịch vụ lưu trữ đối tượng Amazon S3:
        - Tạo S3 bucket lab tại region `ap-southeast-1`.
        - Hiểu sâu sắc cấu trúc Bucket, Object, Key và Prefix (phân cấp thư mục logic); phân biệt rõ S3 là Object Storage qua API/HTTPS chứ không phải filesystem hay mounted disk.
        - Thực thi thành thạo các tác vụ `PutObject`, `ListObjectsV2`, `GetObject`.
        - Kiểm tra cơ chế mã hóa lưu trữ mặc định Server-Side Encryption (SSE-S3 AES256).
        - Phân tách rạch ròi giữa bucket-level permissions (`s3:ListBucket`) và object-level permissions (`s3:GetObject`, `s3:PutObject`); cấu hình scope Resource chính xác theo ARN (`arn:aws:s3:::bucket` vs `arn:aws:s3:::bucket/*`).
        - Thực hành Failure Injection S3: Thu hồi quyền `s3:CreateBucket` $\rightarrow$ API lập tức trả về `AccessDenied`.
      - Thiết kế và triển khai IAM Role cho máy chủ EC2 (`S24-EC2-S3-Role`):
        - Cấu hình Trust Policy: Cho phép principal `ec2.amazonaws.com` thực hiện `sts:AssumeRole`.
        - Cấu hình Permission Policy: Giới hạn nghiêm ngặt chỉ cấp `s3:ListBucket` và `s3:GetObject` trên S3 bucket bài lab.
        - Tạo Instance Profile làm cầu nối đính kèm IAM Role vào máy chủ EC2.
        - Phân biệt bản chất `iam:PassRole` (ủy quyền cho EC2 nhận Role) và `sts:AssumeRole` (hành động assume danh tính của EC2); scope `iam:PassRole` chính xác về ARN của S24 Role.
      - Thực hành Failure Injection kiểm chứng IAM Role cho EC2:
        - Khởi tạo EC2 không gán IAM Role $\rightarrow$ AWS CLI trong instance báo lỗi `Unable to locate credentials`.
        - Đính kèm Instance Profile vào EC2 đang chạy (live attachment) $\rightarrow$ EC2 tự động nhận temporary credentials thông qua Instance Metadata Service (IMDS).
        - Thực thi `GetObject` thành công ghi nhận nội dung `S24_SUCCESS: EC2 READ S3`, chứng minh máy chủ đọc S3 an toàn tuyệt đối mà không cần tạo hay lưu trữ long-term Access Key.
      - Quản trị ổ đĩa lưu trữ khối Amazon Elastic Block Store (EBS):
        - Khảo sát Root EBS Volume: `gp3`, 8 GiB, gắn liền Availability Zone `ap-southeast-1a`, cấu hình `DeleteOnTermination=True`.
        - Nắm vững nguyên tắc vật lý: EBS Volume chỉ có thể attach vào EC2 instance nằm trong cùng Availability Zone (AZ).
        - Tạo bổ sung 1 GiB gp3 encrypted volume, gắn (attach) thành công vào EC2 instance; phân biệt rõ việc attach ở tầng hạ tầng ảo hóa AWS chưa đồng nghĩa với việc định dạng filesystem (`mkfs`) hay mount vào thư mục trong Linux OS.
        - Tạo EBS Snapshot kiểm chứng giải pháp sao lưu point-in-time cấp block-level; thực hành detach và delete EBS volume, xóa snapshot an toàn.
      - Vận hành nguyên tắc Cost Safety & Resource Deprovisioning:
        - Terminate toàn bộ EC2 instances bài lab.
        - Xóa sạch EBS lab volume và EBS snapshot.
        - Dọn sạch S3 objects và xóa S3 bucket.
        - Xóa IAM Instance Profile, IAM Role và inline policy liên quan.
        - Thu hồi toàn bộ quyền ghi tạm thời, giữ quyền `ec2:DescribeVolumes` trong policy `EC2ReadOnly`.
        - Kiểm chứng bằng dry-run `CreateVolume` trả về `UnauthorizedOperation` chính xác theo thiết kế.
      - Kết quả: **ĐẠT BUỔI 24 (XUẤT SẮC)**.




