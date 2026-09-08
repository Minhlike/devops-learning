# NEXT SESSION PLAN

- **Buổi học tiếp theo:** BUỔI 19 — PHASE 5: Advanced GitHub Actions & Multi-Stage CI/CD Workflows.
- **Mục tiêu Buổi 19:**
  1. Matrix Builds: Chạy song song unit test trên nhiều phiên bản Python (Python 3.10, 3.11, 3.12) và OS matrix (`ubuntu-latest`, `windows-latest` nếu cần).
  2. Caching Dependencies: Tối ưu thời gian chạy pipeline bằng cơ chế Cache (`actions/cache` / `setup-python cache: 'pip'`) để không phải tải lại thư viện mỗi lần push.
  3. Artifacts & Test Coverage: Xuất báo cáo độ bao phủ mã nguồn (`pytest-cov` / `coverage`) và upload test artifact lưu trữ trên GitHub Actions UI (`actions/upload-artifact`).
  4. Branch Protection Rules & Pull Request Checks: Cấu hình bắt buộc Status Check (CI phải xanh mới cho phép merge vào `main`).
  5. Failure Injection: Broken dependency version trong Matrix, test coverage sụt giảm dưới ngưỡng quy định (Threshold Gate Failure).
