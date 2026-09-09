# NEXT SESSION PLAN

- **Buổi học tiếp theo:** BUỔI 20 — PHASE 5: Production-Ready CD & Release Automation (Environments, Semantic Release & Rollback).
- **Mục tiêu Buổi 20:**
  1. GitHub Environments & Deployment Gates: Cấu hình môi trường `staging` và `production` trên GitHub, thiết lập Environment Protection Rules (Required Reviewers manual approval trước khi deploy lên `production`).
  2. Release Tagging & Semantic Versioning Automation: Tự động hóa tạo GitHub Release và gắn Semantic Version tag (`v1.0.0`, `v1.0.1`) cho Docker image khi tạo Git tag hoặc merge vào `main`.
  3. Continuous Deployment Simulation: CD pipeline tự động deploy container lên môi trường host mục tiêu (qua SSH runner / Docker Compose) và chạy kiểm tra tự động Healthcheck sau deploy (`curl http://.../health`).
  4. Automated Rollback Strategy: Xây dựng kịch bản rollback tự động về image tag ổn định trước đó khi Healthcheck sau deploy bị thất bại (`failure()` condition).
  5. Failure Injection: Deploy một bản build lỗi cố tình làm sập endpoint `/health` $\rightarrow$ CD pipeline phát hiện và tự động kích hoạt rollback đưa hệ thống về phiên bản lành mạnh gần nhất.
