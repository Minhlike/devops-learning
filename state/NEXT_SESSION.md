# NEXT SESSION PLAN

- **Buổi hiện tại:** S56 — Production-Grade DevOps Capstone, IN PROGRESS — Checkpoint 1: Infrastructure Baseline; chờ output kiểm kê.
- **Buổi hoàn thành gần nhất:** S55 — Software Supply Chain Security **COMPLETED — 9,75/10 — PASS** ngày 26/10/2026.
- **Tiến độ:** 55/66 buổi (83,3%). Phase 10 COMPLETED; Phase 11 COMPLETED (5/5); Phase 12 IN PROGRESS.
- **Kết quả đã nghiệm thu:** S49 10/10; S50 9/10; S51 10/10; S52 9,5/10; S53 9,75/10; S54 10/10; S55 9,75/10.
- **Roadmap chính thức:** Phase 11 S51–S55 COMPLETED; Phase 12 S56–S60 Production-Grade DevOps Capstone, hiện tại là S56.

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

## Bàn giao S54 — Kubernetes Security Basics

- **Kết quả:** COMPLETED — 10/10 — PASS (7/7 trắc nghiệm, 3/3 tự luận), ngày 26/10/2026.
- **RBAC:** Trong namespace `s54-rbac-lab`, `pod-reader` ServiceAccount nhận quyền `get/list/watch` trên Pods qua `pod-viewer` Role và RoleBinding. Trước binding `list pods=no`, sau binding `yes`; `get secrets=no`, `delete pods=no`; quyền list ở `staging` và `monitoring` đều `no`.
- **ServiceAccount:** Pod `s54-identity-test` gọi Kubernetes API trực tiếp; `LIST_PODS_HTTP=200`, `GET_SECRET_HTTP=403`.
- **SecurityContext:** Pod `s54-hardened` 1/1 Running; UID/GID 10001/10001, root filesystem ghi bị từ chối, token không mount, `CapEff=0`, `NoNewPrivs=1`, Seccomp 2.
- **NetworkPolicy:** Baseline HTTP 200; default deny làm HTTP 000/exit 7; selective allow TCP/80 cho nhãn được duyệt phục hồi HTTP 200/exit 0; client không có nhãn tiếp tục HTTP 000/exit 7.
- **Giới hạn:** Thử nghiệm trong namespace lab riêng; không khẳng định production cluster đã harden toàn diện. Chưa có bằng chứng cleanup tài nguyên lab.

## Bàn giao S55 — Software Supply Chain Security

- **Kết quả:** COMPLETED — 9,75/10 — PASS (7/7 trắc nghiệm, 2,75/3 tự luận), ngày 26/10/2026.
- **Digest/SBOM:** Hai Pod chạy `ghcr.io/stefanprodan/podinfo:6.15.0` có cùng imageID `sha256:ec73780a8425f59ea49f5bc8cdff0d598805a224fbaa1f86c67a244f250fa9da`. Trivy 0.76.1 tạo CycloneDX 1.7 cho Alpine 3.24.1, 123 components, exit 0; lệnh SBOM không bật vulnerability scan.
- **Provenance:** Skopeo đọc OCI index amd64/arm64 cùng hai attestation; AMD64 manifest `sha256:72611294759dc6b304d1f3efa2d4b1de212ce422866244f31bc29f731e3b2079`. Attestation có SPDX SBOM và SLSA Provenance v1; blob integrity PASS; provenance ghi BuildKit/GitHub Actions run `33408245072`, source Podinfo revision `dd507173b7b75b2312a36cabe0de5f09c1ce69c8`, 3 dependencies.
- **Image signing:** Cosign APT 2.6.2 không tìm artifact bằng `cosign tree`; Cosign v3.1.4 chính thức được binary-verify (exit 0), xác minh chữ ký Podinfo (exit 0), signer identity release workflow của tag 6.15.0 và issuer GitHub Actions. Certificate chain và transparency log được xác minh offline.
- **Giới hạn:** Chưa xác minh độc lập chữ ký/danh tính phát hành của provenance; không kết luận toàn bộ build đã audit hoặc image không có CVE/backdoor/zero-day; chưa có admission policy bắt buộc verify signature. Không đưa binary, layer, SBOM hay provenance local lên GitHub.

## S56 — Production-Grade DevOps Capstone (CURRENT SESSION)

- **Trạng thái:** IN PROGRESS — Checkpoint 1: Infrastructure Baseline; chưa có output và chưa nghiệm thu. Giữ tiến độ ở 55/66 (83,3%); S57–S66 chưa học.
- **Định hướng:** Tái sử dụng Flask + PostgreSQL từ S17; kế thừa unit test, CI/CD và Security Gates từ S18; triển khai ứng dụng trên K3s và GitOps; tích hợp Prometheus, Grafana, Loki, Alerting; thiết kế health checks, rollback, backup và runbooks. Tối ưu cho VM đơn node, không tuyên bố HA thực tế.
- **Đã giao kiểm kê, đang chờ output:** `nproc`, `free -h`, `df -h /`, `sudo k3s kubectl get deploy,sts -A`.
- **Checkpoint tiếp theo:** Đọc output thật để xác lập baseline tài nguyên và workload trước khi chọn quy mô thiết kế. Không tự điền CPU/RAM/disk/workload hoặc xác nhận checkpoint hoàn tất.
- **Khung Phase 12 giữ nguyên:** S56–S60 Production-Grade DevOps Capstone; S61–S63 Multi-Environment Infrastructure, Disaster Recovery, High Availability Simulation; S64–S66 Portfolio Review, Technical Interview Preparation, CV & Career Coaching.
