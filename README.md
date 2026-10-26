# DevOps Engineering Learning System

Hệ thống quản lý học tập, thực hành và lưu trữ mã nguồn thực chiến DevOps từ cơ bản đến nâng cao (Linux, Networking, Docker, CI/CD, AWS Cloud, Terraform IaC, Ansible Automation, Kubernetes Orchestration, Observability & DevSecOps).

Repository được chuẩn hóa theo kiến trúc tự chứa (self-contained), gọn nhẹ, tối ưu cho việc tự học, ôn tập, phục dựng môi trường và sẵn sàng cho các AI Agent tiếp quản.

---

## 1. Cổng Thông tin & Điều hướng Nhanh

| Mục tiêu | Tài liệu Nguồn sự thật | Mô tả |
| :--- | :--- | :--- |
| **Dành cho AI Agent** | [`AGENTS.md`](AGENTS.md) | Bản đồ điều hướng, trật tự đọc nguồn sự thật và quy tắc vận hành cho AI. |
| **Tiến độ Thực tế** | [`state/CURRENT_PHASE.md`](state/CURRENT_PHASE.md) | Trạng thái hiện tại đã được nghiệm thu bằng bằng chứng thực tế. |
| **Kế hoạch Buổi Tiếp theo** | [`state/NEXT_SESSION.md`](state/NEXT_SESSION.md) | Chi tiết mục tiêu, chuẩn bị môi trường và nội dung buổi học kế tiếp. |
| **Lộ trình Chuẩn hóa** | [`docs/ROADMAP.md`](docs/ROADMAP.md) | Lộ trình đào tạo 66 buổi (S01 – S66), phân chia theo 12 giai đoạn. |
| **Chỉ mục Bài học** | [`docs/SESSION_INDEX.md`](docs/SESSION_INDEX.md) | Tra cứu nhanh 34+ bài lab theo mã buổi (`S14`, `S41`), công nghệ, lỗi kỹ thuật. |
| **Chính sách Đánh giá** | [`docs/ASSESSMENT_POLICY.md`](docs/ASSESSMENT_POLICY.md) | Chuẩn kiểm tra mới (7 trắc nghiệm + 2 tự luận cuối buổi, áp dụng từ S42). |
| **Quy chuẩn Sư phạm** | [`docs/LEARNING_PROTOCOL.md`](docs/LEARNING_PROTOCOL.md) | Nguyên tắc giảng dạy đan xen, nhịp học chuẩn, quản trị tải nhận thức. |
| **Bản đồ Chuyển đổi** | [`docs/MIGRATION_MAP.md`](docs/MIGRATION_MAP.md) | Ánh xạ đường dẫn cũ (`linux-labs/`, `scripting-labs/`) sang cấu trúc chuẩn `labs/sXX/`. |
| **Cẩm nang Repository** | [`docs/REPOSITORY_GUIDE.md`](docs/REPOSITORY_GUIDE.md) | Hướng dẫn cấu trúc, quy ước đóng góp, quy trình CI/CD và vệ sinh secret. |
| **Tài liệu Tham khảo** | [`docs/reference/`](docs/reference/) | Bộ Cheatsheet Linux & DevOps (Markdown, HTML, PDF). |

---

## 2. Trạng thái Đào tạo Hiện tại

- **Giai đoạn Hiện tại:** Phase 11 — DevSecOps; Phase 10 — Observability & SRE đã COMPLETED.
- **Buổi Hoàn thành Gần nhất:** **Buổi 53 — CI/CD Security** (COMPLETED — 9,75/10 — Ngày 26/10/2026).
- **Buổi Tiếp theo:** **Buổi 54 — Kubernetes Security Basics**.
- **Kết quả gần nhất:** S43 9.3/10, S44 9.6/10, S45 9.7/10, S46 9.8/10, S47 9.8/10, S48 10/10, S49 10/10, S50 9/10, S51 10/10, S52 9,5/10, S53 9,75/10 — đều COMPLETED.
- **Tiến độ:** Hoàn thành **53/66 buổi (80,3%)**. Phase 10 hoàn tất; Phase 11 đang triển khai.
- **Sự cố Tồn đọng Độc lập:** Buổi 40 (Kubernetes Resources & Scaling) tiếp tục giữ trạng thái **IN PROGRESS / PARTIALLY VERIFIED** do sự cố HPA CPU: `<unknown>/50%` đang nằm trong backlog điều tra riêng biệt, cụm Kind `s40` và `s41` được duy trì nguyên vẹn; Gateway External LoadBalancer provisioning của S42 là tồn đọng UNRESOLVED do môi trường Kind không có LoadBalancer controller.
- **Hạ tầng Mới Vận hành:** Cụm K3s `v1.36.5` trên máy ảo VMware Ubuntu Server 26.04.1 (`192.168.210.100`) phục vụ chuyên đề Observability (S46+), hoạt động song song và độc lập với cụm Kind trên WSL2.

---

## 3. Cấu trúc Thư mục Thực hành (`labs/`)

Toàn bộ các bài thực hành đã được hợp nhất về thư mục duy nhất `labs/` với quy ước định danh `sXX-<kebab-case>`:

- `labs/s02-linux-filesystem` đến `labs/s09-phase2-exam`: Nền tảng Linux, Services, Permissions, Networking & HTTP/DNS.
- `labs/s10-git-advanced` đến `labs/s13-python-devops`: Git nâng cao, Bash Automation & Python DevOps.
- `labs/s14-docker-fundamentals` đến `labs/s17-docker-capstone`: Dockerfile, Multi-Container Compose, Capstone Project.
- `labs/s18-ci-cd`: GitHub Actions Pipeline (Test Matrix Python 3.10–3.12, Gitleaks, Bandit, Coverage 96%).
- `labs/s23-aws-ec2` đến `labs/s26-aws-alb-asg`: AWS Cloud Infrastructure (EC2, S3/EBS, RDS PostgreSQL, ALB & ASG).
- `labs/s29-terraform-aws` đến `labs/s32-terraform-advanced`: Infrastructure as Code (Terraform VPC, S3 Remote State, Modules, Refactoring).
- `labs/s33-ansible-fundamentals` đến `labs/s36-ansible-tags-vault`: Configuration Management (Ansible Roles, Multi-Host, Ansible Vault).
- `labs/s37-kubernetes-fundamentals` đến `labs/s48-alerting`: Kubernetes Orchestration, Gateway API, Helm, Cluster Troubleshooting, Prometheus, Grafana, Loki/Fluent Bit và Alertmanager.

---

## 4. Công nghệ Sử dụng (Tech Stack)

- **Hệ điều hành & Môi trường:** Ubuntu 24.04 trên WSL2, Ubuntu Server 26.04.1 trên VMware, Windows 11.
- **Ngôn ngữ & Tự động hóa:** Bash Shell, Python 3.12, Jinja2, HCL, YAML, PromQL.
- **Container & Điều phối:** Docker Engine, Docker Compose, Kubernetes (v1.37), Kind (v0.33), K3s (v1.36.5), kubectl, Helm (v4.3).
- **Giám sát & Độ tin cậy (Observability):** Prometheus (Pull model, TSDB, Service Discovery), Grafana (Dashboards, Data Sources).
- **CI/CD & DevSecOps:** GitHub Actions, Gitleaks, Ruff, Bandit, Coverage.py, Google Release Please.
- **Hạ tầng & Đám mây:** AWS (IAM, EC2, S3, EBS, RDS, ALB, ASG, CloudWatch, Route 53), HashiCorp Terraform.
- **Quản trị Cấu hình:** Ansible, Ansible Vault.
- **Lưu trữ & Cơ sở dữ liệu:** PostgreSQL 16, Redis 7, Kubernetes PersistentVolume & StatefulSet.
