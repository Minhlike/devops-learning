# NEXT SESSION PLAN

- **Buổi tiếp theo:** S54 — Kubernetes Security Basics.
- **Trạng thái gần nhất:** S53 — CI/CD Security **COMPLETED — 9,75/10** ngày 26/10/2026.
- **Tiến độ:** 53/66 buổi (80,3%). Phase 10 COMPLETED; Phase 11 IN PROGRESS.
- **Kết quả đã nghiệm thu:** S49 10/10; S50 9/10; S51 10/10; S52 9,5/10; S53 9,75/10.
- **Roadmap chính thức:** S51 Container & Dependency Security; S52 IaC Security; S53 CI/CD Security; S54 Kubernetes Security Basics; S55 Software Supply Chain Security.

## Tổng kết S49–S53

- **S49 — SLI, SLO & Error Budget (10/10):** Prometheus/Podinfo HTTP metrics; HTTP 2xx SLI đạt 100% trong cửa sổ quan sát 30 phút; RPS 5 phút khoảng 0,2337; Burn Rate 5 phút bằng 0. SLO 99,9% là mục tiêu giả định. Không suy rộng kết quả cửa sổ ngắn hoặc retention 8 giờ thành SLO 30 ngày.
- **S50 — Incident Response & Runbooks (9/10):** Thực hành Incident Response, Triage, Severity, Mitigation, Recovery, Runbooks và Blameless Postmortem; kiểm tra Deployment, Service, EndpointSlice, Prometheus, Loki; hai endpoint Podinfo `ready=true`, HTTP 200; quan sát revisions 3 và 4. Không ghi nhận incident/postmortem thực tế chưa có bằng chứng.
- **S51 — Container & Dependency Security (10/10):** Trivy 0.76.1, Grype, Podinfo image scanning, CVE/Severity/SCA, base image risk và patch strategy. Security Gate `grype --only-fixed --fail-on critical` trả `CI_GATE_EXIT=2`. Không thay đổi Deployment đang chạy. Grype, Distroless và Security Gate là nội dung bổ sung; không đổi tên/phạm vi buổi.
- **S52 — IaC Security (9,5/10):** Ubuntu Server `lab-server`; Terraform 1.17.0, Checkov 3.3.30. SSH ingress `0.0.0.0/0` được giới hạn thành `/32` (Checkov PASS); S3 public-read ACL được sửa và bật Block Public Access (5/5 PASS); IAM wildcard được giới hạn thành `s3:GetObject` trên bucket cụ thể (9/9 PASS); S3 Versioning `CKV_AWS_21` PASS. Full scan 24 PASS/7 FAIL trước khi sửa Versioning; baseline gate 9 PASS/0 FAIL; negative gate exit 1; recovery gate exit 0. Không ghi nhận AWS deployment thật hoặc toàn bộ cảnh báo ngoài baseline đã được sửa.
- **S53 — CI/CD Security (9,75/10):** Workflow mẫu `permissions: write-all` đổi thành `contents: read`; học rủi ro `pull_request`/`pull_request_target`. Bandit 1.9.4 phát hiện B602 HIGH; sửa dùng `subprocess.run([...], check=True)` không shell. Full SAST còn 3 LOW; gate exit 0. pip-audit 2.10.1 phát hiện 10 vulnerability matches với `requests==2.19.1`; nâng `2.34.2`, direct scan `--no-deps` không phát hiện. Gitleaks 8.16.0 bắt token giả (exit 1), sau khi xóa exit 0; combined gate exit 0.

## Giới hạn bằng chứng S53 cần giữ

- Workflow GitHub Actions chưa chạy thực tế; required status checks chưa được xác minh.
- pip-audit dùng `--no-deps`, chưa quét toàn bộ dependency tree.
- Ba cảnh báo Bandit LOW vẫn còn.
- Gitleaks chỉ quét working files trong lab, chưa kiểm tra Git history.
- YAML workflow mới được kiểm tra cấu trúc cục bộ; không tạo kết quả CI giả.

## Chuẩn bị S54 — Kubernetes Security Basics

- Theo roadmap: RBAC, ServiceAccount, SecurityContext và NetworkPolicy.
- Giải thích lý thuyết, cơ chế và cú pháp trước từng phần thực hành; phân biệt Windows, WSL và Ubuntu Server.
- Kiểm tra context/namespace và trạng thái hiện tại trước thao tác; làm theo checkpoint nhỏ và xác minh output thật.
- Chỉ một bài nghiệm thu cuối buổi gồm 7 câu trắc nghiệm và 2 câu tự luận trong phạm vi nội dung đã học.
- Không đưa credentials, private key, kubeconfig quản trị hoặc Kubernetes Secret thật vào Git; không thay đổi tài nguyên đang chạy ngoài phạm vi đã thống nhất.

**S55:** Software Supply Chain Security — UPCOMING (SBOM, provenance, digest, image signing).
