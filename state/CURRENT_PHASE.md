# CURRENT LEARNING PHASE

- **Current Phase:** PHASE 4 — Docker, Containers & Application Deployment (ĐÃ HOÀN THÀNH XUẤT SẮC BÀI CAPSTONE)
- **Next Phase:** PHASE 5 — CI/CD Automation & GitHub Actions (BẮT ĐẦU BUỔI 18)
- **Current Week:** Tuần 5
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
