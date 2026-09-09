# MISTAKE LOG

## [2026-07-31] Lỗi gõ sai tên Remote trong Git (`origion` thay vì `origin`)
- **Ngày:** 2026-07-31
- **Bối cảnh:** Kết nối Git repository local lên GitHub.
- **Triệu chứng:** `fatal: 'origin' does not appear to be a git repository` khi gõ `git push -u origin main`.
- **Nguyên nhân gốc:** Gõ thừa chữ `i` trong câu lệnh `git remote add origion ...`.
- **Cách sửa:** Chạy `git remote rename origion origin`.

## [2026-08-01] Sự cố xóa nhầm file `/etc/nginx/nginx.conf` khi sửa lỗi Nginx
- **Ngày:** 2026-08-01
- **Bối cảnh:** Thực hành bài lab Incident Response Nginx config sai syntax.
- **Triệu chứng:** `open() "/etc/nginx/nginx.conf" failed (2: No such file or directory)`.
- **Nguyên nhân gốc:** Gõ nhầm lệnh `sudo rm /etc/nginx/nginx.conf` thay vì xóa file lỗi `/etc/nginx/conf.d/broken.conf`.
- **Cách sửa:** Xóa file lỗi `broken.conf` và dùng `sudo apt purge -y nginx nginx-common nginx-core` rồi `sudo apt install -y nginx` để ép buộc apt tải lại file config mặc định.

## [2026-08-02] Lỗi gõ nhầm tên thư mục trong Shell Script (`lab-5-resources` vs `lab-05-resources`)
- **Ngày:** 2026-08-02
- **Bối cảnh:** Viết script `check_disk.sh` tự động ghi log đĩa.
- **Triệu chứng:** `./check_disk.sh: line 3: /mnt/d/.../lab-5-resources/disk_audit.log: No such file or directory`.
- **Nguyên nhân gốc:** Gõ thiếu chữ số `0` trong tên thư mục (`lab-5-resources` thay vì `lab-05-resources`).
- **Cách sửa:** Đọc lại tên thư mục chính xác bằng `pwd` và sửa lại câu lệnh echo trong script.

## [2026-08-07] Lỗi cú pháp Nginx Reverse Proxy `invalid number of arguments in "proxy_pass"`
- **Ngày:** 2026-08-07
- **Bối cảnh:** Cấu hình Nginx Reverse Proxy chuyển tiếp request Port 8080 sang Python Backend Port 8000.
- **Triệu chứng:** `invalid number of arguments in "proxy_pass" directive in /etc/nginx/conf.d/reverse_proxy.conf:6`.
- **Nguyên nhân gốc:** Thừa/thiếu khoảng trắng khi chèn lệnh proxy_pass bằng bash redirection script.
- **Cách sửa:** Tạo lại file cấu hình tối giản với cú pháp chuẩn `proxy_pass http://127.0.0.1:8000;`.

## [2026-08-08] Lỗi `merge: feature/port-8080 - not something we can merge` khi quên tạo branch
- **Ngày:** 2026-08-08
- **Bối cảnh:** Thực hành bài lab Git Merge Conflict.
- **Triệu chứng:** `merge: feature/port-8080 - not something we can merge`.
- **Nguyên nhân gốc:** Bỏ qua lệnh tạo nhánh `git checkout -b feature/port-8080` nên branch này chưa tồn tại trong Git.
- **Cách kiểm tra:** Dùng lệnh `git branch` để xem danh sách các nhánh hiện có.
- **Cách sửa:** Chạy `git checkout -b feature/port-8080` để tạo nhánh trước khi sửa code và commit.

## [2026-08-24] Bash tạo file literal `BACKUP_FILE` do thiếu `$`
- **Ngày:** 2026-08-24
- **Bối cảnh:** Lab 12 — viết `backup_app.sh`.
- **Triệu chứng:** Xuất hiện file thật tên `BACKUP_FILE` ở thư mục hiện tại dù script thông báo đường dẫn `backups/app-<timestamp>.tar.gz`.
- **Nguyên nhân gốc:** Viết `tar -czf "BACKUP_FILE" ...` thay vì `tar -czf "$BACKUP_FILE" ...`.
- **Cách sửa:** Dùng `$BACKUP_FILE` để Bash thực hiện variable expansion và quote biến bằng `"$BACKUP_FILE"`.

## [2026-08-24] `tar` thất bại nhưng script vẫn trả Exit Code 0
- **Ngày:** 2026-08-24
- **Bối cảnh:** Failure Injection khi thư mục `backups/` không tồn tại.
- **Triệu chứng:** `tar` báo `Cannot open` và status 2 nhưng script vẫn in `Backup thanh cong`; `echo $?` trả `0`.
- **Nguyên nhân gốc:** Sau lệnh `tar` thất bại, `echo` vẫn chạy thành công và trở thành command cuối cùng của script.
- **Cách sửa:** Kiểm tra trực tiếp `if tar ...; then ... else ... fi` và trả `return/exit` phù hợp.

## [2026-08-24] Nhầm phạm vi biến giữa Shell cha và Script
- **Ngày:** 2026-08-24
- **Bối cảnh:** Failure Injection cho `clean_old_backups.sh`.
- **Triệu chứng:** Chạy `BACKUP_DIR="."` trong terminal nhưng script vẫn sử dụng `backups`.
- **Nguyên nhân gốc:** Script tự gán lại `BACKUP_DIR="backups"` trong process Bash mới nên giá trị của shell bên ngoài không được sử dụng.
- **Cách sửa:** Sửa trực tiếp biến khi test hoặc thiết kế script nhận giá trị bên ngoài bằng `BACKUP_DIR="${BACKUP_DIR:-backups}"`.

## [2026-08-29] Python FileNotFoundError do sai đường dẫn tương đối
- **Ngày:** 2026-08-29
- **Bối cảnh:** Lab 13 — Python Automation & Log Parsing (`health_report.py`).
- **Triệu chứng:** `FileNotFoundError: [Errno 2] No such file or directory` khi đọc log.
- **Nguyên nhân gốc:** Dùng đường dẫn tương đối cứng mà không kiểm tra bằng `pathlib.Path.exists()`.
- **Cách sửa:** Sử dụng `pathlib.Path` và kiểm tra `if not path.exists(): sys.exit(1)` trước khi mở file.

## [2026-08-29] Container không kết nối DB do nhầm Localhost Isolation
- **Ngày:** 2026-08-29
- **Bối cảnh:** Lab 14 — Docker Fundamentals & Networking.
- **Triệu chứng:** App container báo `Connection refused` khi cố kết nối DB tại `127.0.0.1`.
- **Nguyên nhân gốc:** Mỗi container có `localhost` (`127.0.0.1`) hoàn toàn cô lập; `localhost` bên trong container không trỏ ra Host OS hay container DB.
- **Cách sửa:** Đưa 2 container vào chung một User-defined Network và dùng Docker DNS trỏ tới tên container DB.

## [2026-08-30] Các lỗi cú pháp và vận hành trong Lab 15 Docker Compose
- **Ngày:** 2026-08-30
- **Bối cảnh:** Lab 15 — Docker Compose Multi-Container Application.
- **Danh sách lỗi & bài học:**
  - `wget -q0-` thay vì `wget -qO-` (nhầm số 0 với chữ O in hoa).
  - `port:` thay vì `ports:` (sai keyword trong `compose.yaml`).
  - Sai indentation `depends_on` (lỗi cú pháp YAML).
  - PyPI tải rất chậm khi build dependency (`pip install`).
  - Thiếu `DB_PORT` trong cấu hình môi trường kết nối database.
  - Typo `appdp` thay vì `appdb` trong tên database.
  - `psql -s appdb` thay vì `psql -d appdb` (sai flag psql).
  - Failure Injection sai DB hostname (`DB_HOST`): Gây lỗi DNS resolution failure làm App không tìm thấy DB container.
  - Failure Injection sai DB password (`DB_PASSWORD`): Gây lỗi PostgreSQL authentication failure.
  - `docker compose down -v`: Xóa sạch named volume và làm mất dữ liệu database.

## [2026-08-31] Bài học kinh nghiệm & Sự cố trong Lab 16 Advanced Docker Compose
- **Ngày:** 2026-08-31
- **Bối cảnh:** Lab 16 — Advanced Docker Compose & Production Operations.
- **Danh sách bài học & giải pháp:**
  - Image `python:3.12-slim` không có binary `ps`: Phải đọc tiến trình trực tiếp qua hệ thống file ảo `/proc`.
  - Shell Builtin `kill`: Lệnh `docker compose exec app kill ...` không chạy vì `kill` là shell builtin; phải dùng `sh -c 'kill ...'`.
  - TTY cho Heredoc: Heredoc với `docker compose exec` cần cờ `-T` để tắt TTY (`docker compose exec -T app sh -c ...`).
  - Memory Swap limit: Ban đầu test cấp phát 300 MiB không bị OOM vì `MemorySwap` mặc định cho phép tổng 512 MiB; phải cấu hình `memswap_limit: 256m` để kích hoạt OOM Killer chuẩn xác.
  - Cơ chế Healthcheck: Trạng thái `unhealthy` của healthcheck không tự động kích hoạt restart policy của Docker.
  - Reset RestartCount: Chỉ số `RestartCount` sẽ reset về `0` khi Compose recreate một container mới.

## [2026-09-04] Lỗi cú pháp và bài học kinh nghiệm trong Lab 17 Docker Capstone
- **Ngày:** 2026-09-04
- **Bối cảnh:** Lab 17 — Docker Capstone Project & Container Registry Deployment.
- **Danh sách lỗi & cú pháp:**
  - Dockerfile thiếu `\` ở chuỗi `RUN apt-get`.
  - Dockerfile từng viết `COPY app.py` thiếu destination `.`.
  - Python từng typo: `flash` / `Flash` thay vì `flask` / `Flask`.
  - Biến môi trường: `DB_POST` thay vì `DB_PORT`.
  - Lỗi Python DB: `add_visit` từng thiếu `fetchone()` và `commit()`.
  - Cú pháp YAML `compose.yaml`: dùng `&{DB_NAME}` thay vì `${DB_NAME}`.
  - Typo healthcheck: `retires` thay vì `retries`.
  - Typo environment: `environments` thay vì `environment`.
  - Khối app environment từng thiếu `DB_USER`.
  - Lỗi CLI: gõ `docker compose volume ls` nhưng lệnh đúng phải là `docker volume ls`.
- **Bài học rút ra (Lessons):**
  - `py_compile` chỉ kiểm tra cú pháp syntax, không bắt được các lỗi import, name error hoặc lỗi runtime.
  - `docker compose config` là bước validate quan trọng trước khi deployment.
  - Thao tác `tag` không copy/duplicate image, chỉ tạo thêm tên trỏ cùng Image ID.
  - Container Registry cho phép các máy khác pull/deploy image mà không cần mã nguồn local.
  - Vòng đời Volume (Volume Lifecycle) hoàn toàn độc lập với vòng đời Container (Container Lifecycle).

## [2026-09-08] Lỗi Linter Ruff I001 (Import Block Formatting) trong CI Runner
- **Ngày:** 2026-09-08
- **Bối cảnh:** Lab 18 — CI/CD Pipeline với GitHub Actions & Ruff Linter.
- **Triệu chứng:** Pipeline bị đỏ tại step `Lint with Ruff` với thông báo `I001 [*] Import block is un-sorted or un-formatted`.
- **Nguyên nhân gốc:** Không có dòng trống ngăn cách giữa standard library (`import unittest`) và local import (`from app import app`) theo chuẩn PEP 8.
- **Cách sửa:** Thêm 1 dòng trống phân cách giữa 2 nhóm import trong `test_app.py`.

## [2026-09-08] Lỗi 401 Unauthorized khi GitHub Actions đăng nhập Docker Hub
- **Ngày:** 2026-09-08
- **Bối cảnh:** Lab 18 — Cấu hình CD Job push image lên Docker Hub.
- **Triệu chứng:** `Error response from daemon: Get "https://registry-1.docker.io/v2/": unauthorized: incorrect username or password`.
- **Nguyên nhân gốc:** Docker Hub Token hoặc Username trong GitHub Repository Secrets bị thiếu, sai hoặc dính khoảng trắng khi copy-paste.
- **Cách sửa:** Tạo Personal Access Token mới trên Docker Hub (quyền Read & Write), cập nhật lại secret `DOCKER_HUB_TOKEN` trên GitHub Settings và dùng tính năng `Re-run jobs` mà không cần tạo commit rác.

## [2026-09-08] Docker Buildx lỗi "open Dockerfile: no such file or directory"
- **Ngày:** 2026-09-08
- **Bối cảnh:** Lab 18 — Build Docker Image trong GitHub Actions runner.
- **Triệu chứng:** `buildx failed with: ERROR: failed to build: failed to solve: failed to read dockerfile: open Dockerfile: no such file or directory`.
- **Nguyên nhân gốc:** File `Dockerfile` bị đặt nhầm vị trí (nằm trong `app/Dockerfile` hoặc thư mục `Dockerfile/`) thay vì nằm ngay tại context root `labs/lab-18-ci-cd/Dockerfile`.
- **Cách sửa:** Dùng lệnh `mv labs/lab-18-ci-cd/app/Dockerfile labs/lab-18-ci-cd/Dockerfile` đưa file ra đúng thư mục gốc của lab rồi commit.
- **Bài học rút ra (Lessons):**
  - Cơ chế Fail-Fast: Step trước fail (Exit Code $\neq 0$) thì các step và job phụ thuộc phía sau bị hủy ngay lập tức, tiết kiệm chi phí tính toán.
  - Phân biệt Linter vs Test: Linter bắt vi phạm quy chuẩn và cấu trúc tĩnh; Unittest kiểm tra tính đúng đắn của logic nghiệp vụ tại runtime.
  - Phân trang Linux (`less`): Bấm `q` để thoát pager khi xem `git diff` hoặc `git log`.
  - Re-run Jobs: Khi lỗi thuộc về Secret hoặc hạ tầng bên ngoài, dùng `Re-run failed jobs` thay vì tạo commit rỗng.

## [2026-09-09] Lỗi Unittest Discovery Pattern ('*_test.py' vs 'test_*.py')
- **Ngày:** 2026-09-09
- **Bối cảnh:** Lab 19 — Cấu hình lệnh chạy test trong GitHub Actions workflow.
- **Triệu chứng:** Unittest không tìm thấy bất kỳ test case nào (Ran 0 tests in 0.000s).
- **Nguyên nhân gốc:** Đặt sai pattern discovery là `'*_test.py'` trong khi file test đặt tên theo quy ước `test_app.py`.
- **Cách sửa:** Đổi pattern thành `'test_*.py'` trong câu lệnh `python -m unittest discover -s app -p 'test_*.py'`.

## [2026-09-09] Lỗi thụt lề cú pháp YAML dưới khối lệnh đa dòng 'run: |'
- **Ngày:** 2026-09-09
- **Bối cảnh:** Lab 19 — Soạn thảo các step chạy shell script trong file workflow `.github/workflows/ci.yml`.
- **Triệu chứng:** GitHub Actions báo lỗi parsing YAML workflow file (`mapping values are not allowed in this context` hoặc step không thực thi đúng).
- **Nguyên nhân gốc:** Thụt lề không đồng nhất giữa các dòng lệnh con bên dưới khối `run: |`. Trong YAML, khoảng trắng (whitespace indentation) mang ý nghĩa phân cấp cú pháp bắt buộc.
- **Cách sửa:** Căn lề thụt đầu dòng thẳng hàng (chuẩn 2 spaces) cho toàn bộ các dòng shell script nằm trong khối `run: |`.

## [2026-09-09] Runner thiếu binary 'coverage' do quên khai báo trong requirements.txt
- **Ngày:** 2026-09-09
- **Bối cảnh:** Lab 19 — Tích hợp bước đo lường độ bao phủ mã nguồn (Coverage Gate).
- **Triệu chứng:** Step chạy coverage báo lỗi `/bin/bash: line ...: coverage: command not found`.
- **Nguyên nhân gốc:** Thư viện `coverage` chưa được thêm vào `requirements.txt`, nên bước `pip install -r requirements.txt` không cài đặt công cụ này lên môi trường runner.
- **Cách sửa:** Thêm `coverage>=7.6.0` vào `labs/lab-18-ci-cd/app/requirements.txt`.

## [2026-09-09] Bài học về cơ chế Conditional Job Execution và Branch Protection
- **Ngày:** 2026-09-09
- **Bối cảnh:** Lab 19 — Quản lý vòng đời CI/CD với Branch Rulesets và Pull Request.
- **Bài học rút ra (Lessons):**
  - **Job Skipped là hành vi thiết kế đúng:** Job `build-and-push` bị chuyển trạng thái `skipped` khi push trên feature branch là do điều kiện `if: github.event_name == 'push' && github.ref == 'refs/heads/main'`. Đây là hành vi bảo vệ hạ tầng đúng, không phải lỗi pipeline.
  - **Xác thực Branch Protection bằng Failure Injection:** Việc cố tình nâng threshold `--fail-under=101` đã chứng minh trực quan cách GitHub Ruleset và Required Status Checks khóa chặt nút merge PR, ngăn chặn hoàn toàn mã nguồn lỗi lọt vào nhánh `main`.

## [2026-09-09] Bài học về Production CD, Approval Gates, Image Immutability và Rollback Strategy
- **Ngày:** 2026-09-09
- **Bối cảnh:** Lab 20 — Thiết lập Pipeline CD đa môi trường, cổng phê duyệt thủ công và quy trình Rollback khẩn cấp.
- **Bài học rút ra (Lessons):**
  - **Môi trường Staging là lớp đệm (Buffer Zone) bắt buộc:** Không bao giờ deploy trực tiếp lên production ngay sau khi build. Staging cho phép chạy smoke test kiểm thử toàn diện container trong môi trường tương đồng production, phát hiện lỗi cấu hình runtime, port mapping hay crashloop trước khi ảnh hưởng người dùng thật.
  - **Manual Approval Gate là chốt chặn an toàn:** Cấu hình Required Reviewers trên GitHub Environment `production` ngăn chặn việc deploy tự động ngoài ý muốn sau khi merge PR. Đội ngũ kỹ thuật có thời gian đánh giá kết quả staging và chủ động lựa chọn thời điểm release an toàn.
  - **Tag SHA Bất biến (Immutability) loại bỏ rủi ro của tag 'latest':** Tag `latest` có tính biến động (mutable), có thể bị ghi đè bất kỳ lúc nào khiến việc tái hiện sự cố hoặc rollback trở nên mơ hồ. Sử dụng tag `${{ github.sha }}` đảm bảo tính xác định tuyệt đối (deterministic) giữa mã nguồn Git và Docker image artifact.
  - **Chiến lược Image Promotion an toàn:** Chỉ gắn tag `:stable` cho Docker image sau khi đã vượt qua bài smoke test thực tế trên production. Không bao giờ rebuild image từ mã nguồn khi promote để tránh rủi ro trôi phiên bản dependencies.
  - **Quy trình Rollback phải được chuẩn bị sẵn (Pre-engineered):** Khi xảy ra thảm họa production, việc revert git commit và chờ build lại từ đầu tốn rất nhiều thời gian (MTTR cao). Một job rollback chuyên dụng kích hoạt qua `workflow_dispatch` kéo ngay image `:stable` đã được chứng nhận giúp hạ thời gian phục hồi xuống dưới 1 phút.
  - **Bảo toàn Environment Protection Rules trong Rollback:** Job rollback vẫn phải khai báo `environment: production` để lưu vết audit log và đảm bảo chỉ những reviewer có thẩm quyền mới được phê duyệt kích hoạt rollback.
  - **Phân nhánh điều kiện chặt chẽ (Conditional Job Execution):** Sử dụng biểu thức điều kiện `if` rõ ràng ở từng job để tách biệt rạch ròi giữa luồng triển khai định kỳ (`rollback != 'true'`) và luồng khôi phục khẩn cấp (`rollback == 'true'`), đảm bảo không chạy thừa các job test/build khi cần cứu hộ hệ thống.

