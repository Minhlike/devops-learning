# NEXT SESSION PLAN

- **Buổi học tiếp theo:** BUỔI 18 — BẮT ĐẦU PHASE 5: CI/CD Automation & GitHub Actions (CI/CD Fundamentals).
- **Mục tiêu Buổi 18:**
  1. Hiểu khái niệm CI (Continuous Integration) & CD (Continuous Deployment) trong quy trình DevOps hiện đại.
  2. Nắm vững cấu trúc GitHub Actions Workflow (`.github/workflows/*.yml`): `name`, `on` (triggers: push, pull_request), `jobs`, `steps`, `uses`, `run`.
  3. Cấu hình Workflow chạy tự động unit test và linter cho ứng dụng Python/Bash khi push code.
  4. Quản lý GitHub Repository Secrets & Variables an toàn (`secrets.DOCKER_HUB_PASSWORD`, `secrets.DOCKER_HUB_USERNAME`).
  5. Tự động hóa build Docker image và push lên Docker Hub từ GitHub Actions Runner khi merge vào `main`.
  6. Failure Injection: CI pipeline bị đỏ do linter/test failure, secret credential bị thiếu/sai làm fail push registry.
