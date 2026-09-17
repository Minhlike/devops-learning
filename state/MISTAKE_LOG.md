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

## [2026-09-10] Bài học về DevSecOps Security Scanning, Git History Remediation và Release Please Automation
- **Ngày:** 2026-09-10
- **Bối cảnh:** Lab 21 — Tích hợp Bandit SAST, Gitleaks Secret Detection, Trivy Container Scanning và Google Release Please.
- **Bài học rút ra (Lessons):**
  - **Fake secret không kích hoạt scanner do sai pattern hoặc entropy:** Khi tạo chuỗi secret giả lập để test Failure Injection cho Gitleaks, chuỗi thử nghiệm ban đầu không khớp regex pattern chuẩn hoặc không đủ entropy ngẫu nhiên của các nhà cung cấp (AWS, GitHub, Stripe, Docker Token) khiến Gitleaks bỏ qua. Để kiểm thử chính xác, cần sử dụng chuỗi có format nhận diện rõ ràng (ví dụ pattern token thực tế hoặc format chuẩn của Gitleaks test).
  - **Secret đã commit vào Git history không thể xóa sạch bằng commit mới:** Việc tạo một commit mới để xóa file hoặc xóa dòng chứa secret chỉ loại bỏ nó trên working directory và commit mới nhất; toàn bộ commit cũ trong lịch sử Git vẫn lưu giữ nguyên vẹn secret đó. Bất kỳ ai clone repo đều có thể trích xuất lại secret. Cách xử lý triệt để duy nhất là rewrite Git history (dùng `git commit --amend`, rebase hoặc git filter-repo) để xóa vết hoàn toàn, sau đó push cập nhật an toàn bằng `git push --force-with-lease`.
  - **Vị trí file cấu hình Release Please:** Ban đầu các file cấu hình `release-please-config.json`, `.release-please-manifest.json`, `version.txt` và `CHANGELOG.md` bị đặt nhầm vào `.github/workflows/` thay vì đặt tại thư mục gốc (root) của repository. Release Please action mặc định tìm kiếm manifest và config ở root directory trừ khi được cấu hình path tùy chỉnh.
  - **Lỗi xung đột cấu hình Manifest Mode trong Release Please:** Khi sử dụng mô hình manifest-driven release, việc truyền đồng thời cờ `release-type` trực tiếp trong file workflow action gây xung đột cấu hình (Release Please báo lỗi vì cấu hình component và release-type đã được quy định bên trong `release-please-config.json`). Cách khắc phục là loại bỏ tham số `release-type` inline và để action đọc cấu hình manifest/config files một cách đồng bộ.
  - **GitHub chặn GitHub Actions tự tạo Pull Request theo mặc định:** Release Please chạy thành công nhưng không tạo được Release PR do cơ chế bảo mật mặc định của GitHub ngăn cản `GITHUB_TOKEN` tạo hoặc phê duyệt Pull Request. Cần kích hoạt thủ công quyền này trong giao diện repository: `Settings` $\rightarrow$ `Actions` $\rightarrow$ `General` $\rightarrow$ tích chọn `Allow GitHub Actions to create and approve pull requests`.
  - **Đặc điểm của CHANGELOG.md trong lần chạy đầu tiên của Release Please:** Bản Changelog phát hành đầu tiên của `v1.1.0` có độ dài lớn do repository trước đó đã có sẵn tag `v1.0.0` từ Phase 2 và tích lũy toàn bộ commit history từ Buổi 10 đến Buổi 21. Kể từ bản release này trở đi, mọi Pull Request và Release tiếp theo sẽ tính toán chênh lệch (incremental) một cách ngắn gọn, chính xác theo từng release cycle.

## [2026-09-12] Sự cố và Bài học về AWS IAM, CLI Authentication và Symlink Configuration
- **Ngày:** 2026-09-12
- **Bối cảnh:** Lab 22 — Thiết lập môi trường AWS Foundations, cấu hình AWS CLI v2 trên WSL, quản lý quyền hạn IAM và xác thực phiên.
- **Sự cố & Bài học rút ra (Lessons):**
  - **Sự cố đứt gãy Symlink thư mục `~/.aws` trên WSL:** Khi tạo symlink trỏ từ thư mục `~/.aws` trong Ubuntu WSL sang thư mục cấu hình AWS trên Windows (`/mnt/c/Users/.../.aws`), quyền truy cập file (file permissions) và đường dẫn mount có thể khiến AWS CLI trên Linux không đọc hoặc không ghi được cache token phiên (`credentials`/`sso cache`). Khắc phục bằng cách đảm bảo symlink trỏ đúng path hợp lệ hoặc duy trì thư mục `~/.aws` độc lập bên trong filesystem ext4 của WSL với quyền `chmod 600/700` chuẩn bảo mật Linux.
  - **Phiên làm việc AWS CLI hết hạn (`ExpiredToken / Token has expired`):** Khi sử dụng phương thức đăng nhập an toàn `aws login` tạo Temporary Credentials ngắn hạn qua AWS STS, token sẽ tự động hết hạn sau khoảng thời gian quy định (thường từ 1 đến 12 giờ). Khi thực thi lệnh CLI bị chặn với lỗi token hết hạn, người vận hành cần thực hiện re-authenticate (`aws login` hoặc `aws sso login`) thay vì nhầm lẫn rằng quyền hạn IAM bị thu hồi.
  - **Failure Injection chứng minh sức mạnh của nguyên tắc Implicit Deny:** Việc thực thi `aws ec2 describe-instances` bị từ chối với lỗi `ClientError: An error occurred (UnauthorizedOperation) when calling the DescribeInstances operation` là minh chứng rõ ràng nhất cho kiến trúc Zero Trust / Least Privilege. IAM không cần câu lệnh Explicit Deny; chỉ cần hành động không nằm trong danh sách `Action` của Policy được gán, AWS sẽ tự động từ chối.
  - **Kiên quyết loại bỏ Long-term Access Keys trên máy local:** Việc tạo static `aws_access_key_id` và `aws_secret_access_key` lưu trong file plain text `~/.aws/credentials` mang rủi ro bảo mật cực lớn nếu máy tính bị tấn công hoặc vô tình commit vào Git. Việc chuẩn hóa quy trình sử dụng Temporary Credentials qua `aws login` giúp triệt tiêu hoàn toàn rủi ro lộ lọt credential vĩnh viễn.

## [2026-09-12] Sự cố và Bài học về AWS EC2, Security Group Stateful Firewall và Cost Lifecycle
- **Ngày:** 2026-09-12
- **Bối cảnh:** Lab 23 — Khảo sát VPC/Subnet, khởi tạo EC2 qua CLI với User Data, kiểm thử Security Group và dọn dẹp tài nguyên.
- **Sự cố & Bài học rút ra (Lessons):**
  - **Triệu chứng Timeout khi Security Group chặn traffic vs Connection Refused:** Khi thu hồi (revoke) rule TCP/80 trong bài Failure Injection, lệnh `curl` tới Public IP bị rơi vào trạng thái treo và timeout (không nhận được phản hồi). Điều này chứng minh Security Group hoạt động như một packet filter ở tầng ảo hóa hypervisor: gói tin bị âm thầm loại bỏ (drop silently) mà không gửi gói TCP RST về cho client. Khác với trường hợp Nginx bị tắt (OS trả về `Connection refused` ngay lập tức).
  - **Lỗi `DependencyViolation` khi xóa Security Group trước khi EC2 Terminated:** Khi cố gắng xóa Security Group `web-sg` ngay sau lệnh `terminate-instances`, AWS API trả về lỗi `DependencyViolation` do instance vẫn đang ở trạng thái `shutting-down` và network interface (ENI) chưa được tháo gỡ (detach). Cần sử dụng lệnh `aws ec2 wait instance-terminated` để đảm bảo máy chủ đã hủy hoàn toàn trước khi xóa Security Group.
  - **Bẫy chi phí giữa Stop vs Terminate và Public IPv4:** Dừng máy chủ (`stop-instances`) chỉ dừng tính phí compute (vCPU/RAM), nhưng AWS vẫn tiếp tục tính phí cho root EBS storage volume và địa chỉ Public IPv4 gán cho instance. Để duy trì nguyên tắc Zero-Spend / Cost Safety tuyệt đối trong môi trường học tập, bắt buộc phải `terminate-instances` để tự động hủy toàn bộ EBS volume gắn kèm và giải phóng Public IPv4 về lại AWS pool.
  - **Vệ sinh đặc quyền (Privilege Hygiene) và kiểm thử với `--dry-run`:** Việc cấp tạm quyền ghi để làm lab cần tuân thủ quy trình thu hồi ngay sau khi dọn dẹp tài nguyên. Cờ `--dry-run` của AWS CLI là công cụ kiểm thử phân quyền vô cùng đắc lực: cho phép xác minh quyền hạn IAM mà không thực sự tạo hay xóa tài nguyên, tránh gây rủi ro sai sót trong môi trường cloud.

## [2026-09-13] Sự cố và Bài học về Automation Timing, IAM Role vs PassRole và Block Storage Attach
- **Ngày:** 2026-09-13
- **Bối cảnh:** Lab 24 — Quản trị AWS Storage (S3, EBS, Snapshot), cấu hình IAM Role cho EC2 và tự động hóa qua User Data.
- **Sự cố & Bài học rút ra (Lessons):**
  - **Sự cố Timeout trong User Data do Retry Window quá ngắn:**
    - *Triệu chứng:* Script User Data kiểm tra quyền đọc S3 ban đầu thiết lập vòng lặp thử lại 30 lần x 10 giây (tổng cộng 5 phút). Do quá trình attach IAM Instance Profile thủ công diễn ra sau khi máy chủ đã khởi động, script chạy hết 30 lần trước khi Role được gắn thành công, kết thúc với thông điệp lỗi `S24_FAILED`.
    - *Chẩn đoán:* Xác định chính xác nguyên nhân gốc (root cause) thông qua console log hệ thống (`aws ec2 get-console-output`).
    - *Khắc phục:* Mở rộng retry window lên 120 lần x 10 giây (20 phút) và bổ sung log chi tiết có thể quan sát được (observable logs). Khi chạy lại, EC2 bắt được temporary credentials ngay sau khi gắn role và hoàn thành thành công với `S24_SUCCESS`.
    - *Bài học:* Mọi kịch bản tự động hóa phụ thuộc vào tính đồng nhất sau cùng (eventual consistency) hoặc độ trễ thao tác giữa các thành phần cloud phân tán đều cần có Retry Window đủ rộng và cơ chế ghi log tường minh.
  - **Phân biệt rạch ròi giữa AWS Block Device Attach và Linux OS Mount:**
    - Việc gọi API `aws ec2 attach-volume` chỉ đưa volume vào danh sách thiết bị phần cứng ảo hóa của máy chủ (hiện diện dưới dạng block device như `/dev/xvdf` hoặc `/dev/nvme1n1`).
    - Hệ điều hành Linux bên trong EC2 hoàn toàn chưa thể sử dụng nếu chưa thực hiện các bước: kiểm tra filesystem (`lsblk -f`), định dạng hệ thống tệp tin (`mkfs -t ext4`) và gắn kết vào cây thư mục (`mount /dev/... /mnt/...`).
  - **Phân biệt `sts:AssumeRole` và `iam:PassRole`:**
    - `sts:AssumeRole`: Là hành động của chủ thể (ở đây là máy chủ EC2 thông qua service principal `ec2.amazonaws.com`) thực hiện lấy danh tính tạm thời từ IAM Role thông qua Trust Policy.
    - `iam:PassRole`: Là quyền hạn của người dùng hoặc tiến trình khởi tạo máy chủ (User/CLI) cho phép "chuyển giao" Role đó cho tài nguyên EC2. Cần scope quyền `iam:PassRole` chính xác về ARN của Role cần cấp thay vì dùng `*` để tránh nguy cơ leo thang đặc quyền (Privilege Escalation).

## [2026-09-15] Bài học về Phương pháp tiếp cận Cloud Architecture, Bảo mật RDS Security Group và Quản lý Snapshot
- **Ngày:** 2026-09-15
- **Bối cảnh:** Lab 25 — Khảo sát và triển khai cơ sở dữ liệu Amazon RDS PostgreSQL, kết nối private từ EC2 và quản lý sao lưu snapshot.
- **Sự cố & Bài học rút ra (Lessons):**
  - **Bài học phương pháp luận (Teaching & Learning Mental Model):**
    - *Vấn đề:* Buổi học ban đầu quá tập trung vào các chuỗi lệnh CLI phức tạp kéo dài khiến người học bị quá tải chi tiết cú pháp và đánh mất bức tranh toàn cảnh (mental model) về kiến trúc hệ thống.
    - *Cải tiến:* Kể từ các buổi học tiếp theo, luôn áp dụng nguyên tắc **Architecture-First**: Phác thảo sơ đồ kiến trúc và nêu rõ mục tiêu tổng thể trước, giải thích bản chất và vai trò của từng resource ("chúng ta đang xây dựng thành phần gì và tại sao hệ thống cần nó") trước khi bắt tay vào gõ lệnh. Đồng thời gom toàn bộ quy trình dọn dẹp (Cleanup) thành một phase độc lập ở cuối buổi thay vì để việc dọn dẹp xen lẫn làm loãng nội dung học chính.
  - **Bảo mật mạng RDS với Source Security Group (Least Privilege):**
    - Tuyệt đối không bao giờ dùng dải IP CIDR của máy chủ (vì IP có thể thay đổi khi relaunch/reboot) hoặc `0.0.0.0/0` để mở cổng kết nối database.
    - Thay vào đó, sử dụng tính năng **Security Group Referencing**: Cấu hình rule inbound trên `rds-sg` với source trực tiếp là `app-sg`. Mọi instance được gán `app-sg` sẽ tự động có quyền kết nối vào RDS một cách bảo mật và linh hoạt nhất.
  - **Phân biệt vòng đời Automated Backup vs Manual Snapshot:**
    - Automated Backup của RDS bị giới hạn bởi thời gian lưu trữ (retention period) và mặc định sẽ bị xóa bỏ cùng với DB instance nếu truyền cờ `--delete-automated-backups`.
    - Manual Snapshot là bản chụp độc lập do người dùng chủ động tạo ra, sẽ tiếp tục tồn tại vĩnh viễn ngay cả khi DB instance gốc đã bị xóa bỏ hoàn toàn. Do đó, cần kiểm tra và xóa cả manual snapshot sau khi hoàn thành lab để tránh phát sinh chi phí lưu trữ ngoài ý muốn.

## [2026-09-16] Sự cố và Bài học về ALB, Auto Scaling Group và Connection Draining
- **Ngày:** 2026-09-16
- **Bối cảnh:** Lab 26 — Khởi tạo Application Load Balancer, Launch Template, Auto Scaling Group đa AZ, kiểm thử Self-Healing và dọn dẹp tài nguyên.
- **Sự cố & Bài học rút ra (Lessons):**
  - **Lỗi `ServiceLinkedRoleFailure` khi tạo Auto Scaling Group:**
    - *Triệu chứng:* Lệnh `aws autoscaling create-auto-scaling-group` thất bại với lỗi `ServiceLinkedRoleFailure: Failed to create or use a service linked role for auto scaling`.
    - *Nguyên nhân:* Service-linked role `AWSServiceRoleForAutoScaling` vừa mới được tạo nhưng do độ trễ truyền bá (eventual consistency) trong hệ thống phân tán IAM của AWS, quyền hạn chưa kịp sẵn sàng trên toàn bộ endpoint của dịch vụ Auto Scaling.
    - *Cách khắc phục:* Đợi một khoảng thời gian ngắn (propagation window ~15-30 giây) và thử lại lệnh tạo ASG.
    - *Bài học:* Khi tạo mới IAM Role hoặc Service-Linked Role, luôn dự phòng khoảng thời gian trễ nhất định trước khi gọi các dịch vụ phụ thuộc vào role đó.
  - **Lỗi thiếu quyền `ec2:RunInstances` trong S26 Temporary Policy:**
    - *Triệu chứng:* Auto Scaling Group được tạo nhưng không thể khởi tạo các EC2 instances từ Launch Template; kiểm tra `DescribeScalingActivities` thấy hoạt động scale bị Failed do thiếu quyền.
    - *Nguyên nhân:* Policy tạm thời ban đầu của lab cấp quyền cho các API ASG và ELB nhưng thiếu quyền `ec2:RunInstances` và các quyền EC2 tài nguyên liên quan khi ASG thực thi launch instance.
    - *Cách khắc phục:* Bổ sung quyền `ec2:RunInstances`, `ec2:CreateSecurityGroup`, `ec2:CreateTags`... vào policy tạm thời để ASG có đầy đủ quyền thao tác với EC2.
  - **Lỗi thiếu quyền `ec2:DescribeAccountAttributes` khi tạo Load Balancer:**
    - *Triệu chứng:* Lệnh `aws elbv2 create-load-balancer` bị từ chối với lỗi `AccessDenied` / `UnauthorizedOperation`.
    - *Nguyên nhân:* Khi tạo ALB, dịch vụ Elastic Load Balancing ngầm gọi API `ec2:DescribeAccountAttributes` để kiểm tra các thiết lập VPC mặc định và giới hạn tài nguyên của tài khoản AWS.
    - *Cách khắc phục:* Bổ sung quyền `ec2:DescribeAccountAttributes` vào chính sách IAM đọc của lab.
  - **Lỗi `ScalingActivityInProgress` khi xóa Auto Scaling Group:**
    - *Triệu chứng:* Lệnh `aws autoscaling delete-auto-scaling-group` trả về lỗi thông báo đang có hoạt động scaling diễn ra và không cho phép xóa ngay.
    - *Nguyên nhân:* Khi hạ capacity về 0 hoặc khi instances đang trong giai đoạn `WaitingForELBConnectionDraining` (Connection Draining), ASG đang tiến hành thu hồi tài nguyên và chờ Target Group giải phóng kết nối an toàn.
    - *Cách khắc phục:* Chờ đợi scaling activity hoàn tất (hoặc truyền cờ `--force-delete` nếu cần thiết sau khi đã verify hạ capacity) trước khi thực hiện xóa ASG.
  - **Bài học phương pháp luận (Teaching & Execution Mental Model):**
    - Tiếp tục phát huy hiệu quả của phương pháp **Architecture-First**: Phân tích sơ đồ kiến trúc luồng dữ liệu (`Internet` $\rightarrow$ `ALB SG` $\rightarrow$ `Web SG` $\rightarrow$ `EC2`), giải thích cặn kẽ bản chất và vai trò của từng thành phần trước khi thực thi CLI giúp người học nắm chắc tư duy hệ thống và tự tin xử lý sự cố.

## [2026-09-17] Sự cố và Bài học về DNS Resolution, ACM Certificate, TLS Termination và Ngữ nghĩa An ninh Mạng
- **Ngày:** 2026-09-17
- **Bối cảnh:** Lab 27 — Cấu hình DNS Delegation, Route 53 Hosted Zone, ACM Certificate, ALB HTTPS Listener và kiểm thử TLS.
- **Sự cố & Bài học rút ra (Lessons):**
  - **Mô hình truy vấn DNS: Trình duyệt không hỏi trực tiếp Authoritative DNS Server:**
    - *Hiểu lầm phổ biến:* Cho rằng trình duyệt người dùng trực tiếp gửi query tới Route 53 Name Server.
    - *Thực tế chuẩn xác:* Trình duyệt máy khách gửi truy vấn tới Recursive DNS Resolver (ví dụ resolver của ISP hoặc public resolver như 1.1.1.1, 8.8.8.8). Recursive resolver mới là đối tượng thực hiện lần theo hệ thống phân cấp (Root $\rightarrow$ TLD $\rightarrow$ Authoritative Server) và lưu đệm (cache) kết quả theo giá trị TTL.
  - **Phân định ranh giới giữa ALB và AWS WAF (Không nhầm lẫn chức năng bảo mật):**
    - *Hiểu lầm phổ biến:* Cho rằng Application Load Balancer mặc định có sẵn khả năng lọc mã độc, chặn tấn công SQLi, XSS hoặc lọc payload HTTP độc hại.
    - *Thực tế chuẩn xác:* ALB chỉ là bộ cân bằng tải tầng ứng dụng (Layer 7 reverse proxy). Khả năng thanh lọc gói tin, ngăn chặn mã độc và lọc payload web nằm ở dịch vụ tường lửa ứng dụng web riêng biệt là **AWS WAF** (Web Application Firewall) khi được liên kết với ALB.
  - **Phân biệt vai trò của ACM và giao thức TLS trong mã hóa đường truyền:**
    - *Hiểu lầm phổ biến:* Nói rằng "ACM thực hiện mã hóa dữ liệu".
    - *Thực tế chuẩn xác:* ACM (AWS Certificate Manager) là dịch vụ quản lý vòng đời chứng chỉ (cấp phát, lưu trữ, tự động gia hạn). Bản thân giao thức TLS kết hợp cùng phần mềm máy chủ/ALB mới là thành phần trực tiếp thực hiện quá trình bắt tay (TLS Handshake) và mã hóa lưu lượng mạng.
  - **Bản chất của TLS Termination tại ALB và luồng lưu lượng backend:**
    - *Lưu ý quan trọng:* Trong mô hình TLS Termination tại ALB của bài lab này, lưu lượng được mã hóa HTTPS giữa Client và ALB. Chặng kết nối nội bộ từ ALB đến EC2 instances qua Target Group sử dụng giao thức HTTP thông thường (unencrypted). Không được gọi toàn bộ luồng traffic từ đầu đến cuối là "được mã hóa" mà cần nêu rõ ranh giới termination.
  - **Bản chất của lỗi Certificate Hostname Mismatch trong Failure Injection:**
    - *Hiểu lầm:* Xem lỗi hostname mismatch là bằng chứng khẳng định đang bị tấn công Man-in-the-Middle (MITM).
    - *Thực tế chuẩn xác:* Hostname mismatch đơn giản là kết quả khi client kiểm tra trường Subject Alternative Name (SAN) trong chứng chỉ do server gửi về không trùng khớp với hostname mà client gửi yêu cầu (ở đây là dùng ALB default hostname truy cập vào chứng chỉ cấp cho `s27.aws.orianawren.com`). Đây thường là lỗi cấu hình (misconfiguration) thay vì chắc chắn có kẻ tấn công can thiệp.
  - **Tránh sử dụng các thuật ngữ an ninh mang tính tuyệt đối:**
    - *Nguyên tắc thuật ngữ:* Trong tài liệu kỹ thuật và thiết kế hệ thống, tránh sử dụng các từ mang tính khẳng định tuyệt đối như "bảo mật tối đa" hay "ngăn chặn hoàn toàn". Cần sử dụng các mô tả chính xác về mặt kỹ thuật (ví dụ: "áp dụng mô hình Least Privilege", "hạn chế bề mặt tấn công", "phân tầng kiểm soát truy cập").
  - **Đặc tính lưu đệm của Recursive DNS và độ trễ khi dọn dẹp tài nguyên:**
    - Khi xóa bỏ bản ghi hoặc hủy ủy quyền trên Authoritative Server (Cloudflare / Route 53), các Recursive Resolver trên Internet vẫn có thể tiếp tục phân giải bản ghi cũ cho đến khi TTL hết hạn. Cần tính toán thời gian TTL caching trong quá trình lập kế hoạch migration hoặc rollback hệ thống DNS.








