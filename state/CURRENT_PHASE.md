# CURRENT LEARNING PHASE

- **Current Phase:** PHASE 4 — Docker, Containers & Application Deployment
- **Current Status:** Hoàn thành Buổi 13 (Python Fundamentals for DevOps Automation) và Buổi 14 (Docker Fundamentals). Chuẩn bị Buổi 15 — Docker Compose & Multi-Container Application.
- **Current Week:** Tuần 4
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
