# NEXT SESSION PLAN

- **Buổi học tiếp theo:** BUỔI 15 — PHASE 4: Docker Compose & Multi-Container Application.
- **Mục tiêu Buổi 15:**
  1. Hiểu khái niệm Docker Compose là gì và tại sao dùng Docker Compose thay vì chạy nhiều câu lệnh `docker run` thủ công.
  2. Nắm vững cú pháp YAML cơ bản (indentation, key-value, lists).
  3. Cấu hình các khối dịch vụ chính trong `docker-compose.yml`: `services`, `build`, `image`, `ports`, `environment`, `volumes`, `networks`.
  4. Triển khai mô hình ứng dụng đa container (Multi-Container App): App + Database (PostgreSQL / MySQL / Redis).
  5. Nắm vững cơ chế Service-Name DNS giữa các container trong cùng Compose Network.
  6. Gắn Database Persistent Volume để đảm bảo dữ liệu DB không bị mất khi container restart/down.
  7. Quản lý biến môi trường (Environment Variables) và Secrets an toàn.
  8. Thành thạo các lệnh quản lý Compose: `docker compose up -d`, `docker compose ps`, `docker compose logs`, `docker compose exec`, `docker compose down`.
  9. Failure Injection: Database down, sai hostname kết nối, sai credential (username/password), và xung đột cổng (Port conflict).
