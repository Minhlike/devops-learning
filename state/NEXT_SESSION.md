# NEXT SESSION PLAN

- **Buổi học tiếp theo:** BUỔI 21 — PHASE 5: DevSecOps Security Scanning, Automated GitHub Releases & Phase 5 Capstone.
- **Mục tiêu Buổi 21:**
  1. Container Vulnerability Scanning with Trivy: Tích hợp Aqua Security Trivy vào pipeline để quét lỗ hổng bảo mật (CVE) của Docker image trước khi push lên Docker Hub, thiết lập chốt chặn an ninh với mức độ cảnh báo HIGH/CRITICAL (`--severity HIGH,CRITICAL --exit-code 1`).
  2. Secret Leak Detection with Gitleaks: Tích hợp Gitleaks GitHub Action quét commit history nhằm ngăn chặn nguy cơ vô tình commit lộ lọt secret, API keys, private tokens hay credentials vào repo.
  3. Static Application Security Testing (SAST) with Bandit: Tích hợp công cụ Bandit quét mã nguồn Python tĩnh, phát hiện các điểm yếu bảo mật phổ biến (hardcoded secrets, unsafe deserialization, insecure configs).
  4. Automated Semantic Versioning & GitHub Releases: Tự động hóa đánh tag Semantic Versioning (`v1.1.0`, `v1.2.0`) và tự động xuất bản GitHub Release kèm Release Notes/Changelog dựa trên Conventional Commits khi merge vào nhánh `main`.
  5. Phase 5 Capstone Project: Tổng kết và vận hành hoàn chỉnh chu trình DevSecOps CI/CD End-to-End: PR $\rightarrow$ Linter/Matrix/Coverage/SAST/Gitleaks $\rightarrow$ Merge Main $\rightarrow$ Docker Build & Trivy Scan $\rightarrow$ Push SHA $\rightarrow$ Staging Deploy & Smoke Test $\rightarrow$ Manual Production Gate Approval $\rightarrow$ Production Deploy & Smoke Test $\rightarrow$ Image Promotion `:stable` $\rightarrow$ Rollback Readiness $\rightarrow$ Tốt nghiệp Phase 5 sẵn sàng tiến vào Phase 6 (AWS Cloud Infrastructure).

