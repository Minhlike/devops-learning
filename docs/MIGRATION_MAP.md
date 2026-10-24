# BẢN ĐỒ CHUYỂN ĐỔI ĐƯỜNG DẪN (MIGRATION MAP)

> **Mục đích:** Tài liệu nguồn sự thật lưu vết toàn bộ các thay đổi tái cấu trúc thư mục từ hệ thống phân tán (`linux-labs/`, `scripting-labs/`, `labs/`) sang cấu trúc chuẩn hóa thống nhất (`labs/sXX-<name>/`) ngày 15/10/2026.
> **Cách sử dụng:** Cả người học và AI Agent có thể tra cứu bảng này để xác định vị trí file trước đây hoặc truy vấn lịch sử commit của từng file bằng lệnh `git log --follow -- <new_path>`.

---

## 1. Bảng Ánh xạ Cấu trúc Toàn diện (Path Mapping Table)

| STT | Buổi | Đường dẫn Cũ (Legacy Path) | Đường dẫn Mới (Standardized Path) | Loại Thao tác | Mô tả & Vai trò |
| :---: | :---: | :--- | :--- | :---: | :--- |
| **01** | Root | `generate_pdf.py` | `tools/generate_pdf.py` | `git mv` | Script sinh cheatsheet PDF tự động (ReportLab) |
| **02** | Root | `LINUX_DEVOPS_CHEATSHEET.md` | `docs/reference/LINUX_DEVOPS_CHEATSHEET.md` | `git mv` | Bản Markdown nguồn của Linux Cheatsheet |
| **03** | Root | `LINUX_DEVOPS_CHEATSHEET.html` | `docs/reference/LINUX_DEVOPS_CHEATSHEET.html` | `git mv` | Bản HTML xuất bản của Linux Cheatsheet |
| **04** | Root | `LINUX_DEVOPS_CHEATSHEET.pdf` | `docs/reference/LINUX_DEVOPS_CHEATSHEET.pdf` | `git mv` | Bản PDF xuất bản của Linux Cheatsheet |
| **05** | Root | `PERSISTENT_MEMORY_PROTOCOL.md` | `docs/LEARNING_PROTOCOL.md` | `git mv` | Quy chuẩn phương pháp giảng dạy & vận hành phiên |
| **06** | S02 | `linux-labs/lab-02-structure/` | `labs/s02-linux-filesystem/` | `git mv` | Linux Filesystem Hierarchy & CLI Commands |
| **07** | S03 | `linux-labs/lab-03-permissons/` | `labs/s03-linux-permissions/` | `git mv` | File Permissions, chmod 755 & chown (Sửa lỗi chính tả) |
| **08** | S04 | `linux-labs/lab-04-services/` | `labs/s04-linux-services/` | `git mv` | Process & Service Management (systemd, journalctl) |
| **09** | S05 | `linux-labs/lab-05-resources/` | `labs/s05-resource-monitoring/` | `git mv` | Resource Monitoring, Disk Audit & Cron Automation |
| **10** | S06 | `linux-labs/phase-1-exam/` | `labs/s06-phase1-exam/` | `git mv` | Phase 1 Failure Injection Exam & Postmortem |
| **11** | S07 | `linux-labs/lab-07-networking/` | `labs/s07-linux-networking/` | `git mv` | Linux Networking & Nginx Reverse Proxy |
| **12** | S08 | `linux-labs/lab-08-http-dns/` | `labs/s08-http-dns/` | `git mv` | HTTP Status Codes, DNS & 502 Bad Gateway Incident |
| **13** | S09 | `linux-labs/phase-2-exam/` | `labs/s09-phase2-exam/` | `git mv` | Phase 2 Graduation Exam, Architecture & Postmortem |
| **14** | S10 | `scripting-labs/lab-10-git-advanced/` | `labs/s10-git-advanced/` | `git mv` | Advanced Git Workflow, Merge Conflict & Tags |
| **15** | S11 | `scripting-labs/lab-11-bash/` | `labs/s11-bash-scripting/` | `git mv` | Bash Scripting Fundamentals & HTTP Healthcheck |
| **16** | S12 | `labs/lab-12-bash-advanced/` | `labs/s12-bash-automation/` | `git mv` | Bash Automation, Log Parsing & Safe Backup/Cleanup |
| **17** | S13 | `labs/lab-13-python-devops/` | `labs/s13-python-devops/` | `git mv` | Python Automation, Subprocess & Health Report |
| **18** | S14 | `labs/lab-14-docker-fundamentals/` | `labs/s14-docker-fundamentals/` | `git mv` | Dockerfile, Container Lifecycle & .dockerignore |
| **19** | S15 | `labs/lab-15-docker-compose/` | `labs/s15-docker-compose/` | `git mv` | Docker Compose Multi-Container (Web + Redis) |
| **20** | S16 | `labs/lab-16-advanced-compose/` | `labs/s16-advanced-compose/` | `git mv` | Advanced Compose, Resource Limits & Healthchecks |
| **21** | S17 | `labs/lab-17-docker-capstone/` | `labs/s17-docker-capstone/` | `git mv` | Docker Production Capstone & Multi-Stage Builds |
| **22** | S18 | `labs/lab-18-ci-cd/` | `labs/s18-ci-cd/` | `git mv` | GitHub Actions CI/CD Pipeline (Cập nhật cả ci.yml) |
| **23** | S23 | `labs/lab-23-aws-ec2/` | `labs/s23-aws-ec2/` | `git mv` | AWS EC2 Launch & User Data Automation |
| **24** | S24 | `labs/lab-24-aws-storage/` | `labs/s24-aws-storage/` | `git mv` | AWS S3, EBS Volume & EC2 IAM Roles |
| **25** | S25 | `labs/lab-25-aws-rds/` | `labs/s25-aws-rds/` | `git mv` | AWS RDS PostgreSQL & Private Security Group |
| **26** | S26 | `labs/lab-26-aws-alb-asg/` | `labs/s26-aws-alb-asg/` | `git mv` | AWS Application Load Balancer & Auto Scaling Group |
| **27** | S29 | `labs/lab-29-terraform-aws/` | `labs/s29-terraform-aws/` | `git mv` | Terraform AWS Infrastructure as Code Foundations |
| **28** | S30 | `labs/lab-30-terraform-multi-resource/` | `labs/s30-terraform-multi-resource/` | Move & Stage | Terraform VPC, Subnet, EC2 & Variables |
| **29** | S31 | `labs/lab-31-terraform-remote-state/` | `labs/s31-terraform-remote-state/` | Move & Stage | Terraform S3 Remote Backend, Locking & Modules |
| **30** | S32 | `labs/lab-32-terraform-advanced/` | `labs/s32-terraform-advanced/` | Move & Stage | Terraform count, for_each, dynamic & Import |
| **31** | S33 | `labs/lab-33-ansible-fundamentals/` | `labs/s33-ansible-fundamentals/` | Move & Stage | Ansible Playbooks, Idempotency & Jinja2 Templates |
| **32** | S34 | `labs/lab-34-ansible-roles/` | `labs/s34-ansible-roles/` | Move & Stage | Ansible Roles, Handlers & Reusable Playbooks |
| **33** | S35 | `labs/lab-35-ansible-multihost/` | `labs/s35-ansible-multihost/` | Move & Stage | Ansible Multi-Host, Group Vars & Docker Nodes |
| **34** | S36 | `labs/lab-36-ansible-tags-vault/` | `labs/s36-ansible-tags-vault/` | Move & Stage | Ansible Tags, Selective Run & Ansible Vault Secrets |
| **35** | S37 | `labs/lab-37-kubernetes-fundamentals/` | `labs/s37-kubernetes-fundamentals/` | Move & Stage | Kubernetes Kind Cluster, Pods & Deployments |
| **36** | S38 | `labs/lab-38-kubernetes-service-networking/` | `labs/s38-kubernetes-service-networking/` | Move & Stage | Kubernetes ClusterIP, NodePort & EndpointSlice |
| **37** | S39 | `labs/lab-39-kubernetes-config-secret-probes/` | `labs/s39-kubernetes-config/` | `git mv` | Kubernetes ConfigMap, Secret & Probes |
| **38** | S40 | `labs/lab-40-kubernetes-resources-scheduling-scaling/` | `labs/s40-kubernetes-resources/` | `git mv` | Kubernetes Resources, QoS, Taints & Scaling |
| **39** | S41 | `labs/lab-41-kubernetes-storage/` | `labs/s41-kubernetes-storage/` | `git mv` | Kubernetes Storage (emptyDir, PV/PVC, StatefulSet) |

---

## 2. Các Thay đổi Phụ thuộc Đã Khắc phục (Dependency Updates)

1. **GitHub Actions CI/CD Workflow (`.github/workflows/ci.yml`):**
   - Đã cập nhật 7 tham chiếu đường dẫn từ `labs/lab-18-ci-cd/` thành `labs/s18-ci-cd/`.
   - Các vị trí: `cache-dependency-path`, `pip install`, `ruff check`, `bandit -r`, `working-directory`, `upload-artifact (coverage.xml)`, và `Docker build context`.
   - Kiểm chứng kỹ thuật: Ruff PASS, Bandit PASS, Unittest 2/2 PASS, Code Coverage 96% (vượt ngưỡng yêu cầu 80%).
2. **Script Đo lường Hệ thống (`labs/s05-resource-monitoring/check_disk.sh`):**
   - Đã thay thế đường dẫn tuyệt đối cũ `/mnt/d/Devops/linux-labs/lab-05-resources/disk_audit.log` bằng đường dẫn tương đối an toàn `$(dirname "$0")/disk_audit.log`, hỗ trợ hoạt động trơn tru trên mọi môi trường.
3. **Script Xuất bản Tài liệu (`tools/generate_pdf.py`):**
   - Đã thay thế đường dẫn tuyệt đối `/mnt/d/Devops/LINUX_DEVOPS_CHEATSHEET.pdf` bằng tính toán động `os.path.join(repo_root, "docs", "reference", "LINUX_DEVOPS_CHEATSHEET.pdf")`.
   - Kiểm chứng kỹ thuật: Chạy lệnh `python tools/generate_pdf.py` xuất bản thành công bản PDF tại đích mới.

---

## 3. Cách Truy vấn Lịch sử Git Sau Migration

Khi cần đối chiếu code cũ hoặc xem lịch sử commit của bất kỳ bài lab nào đã đổi tên:

```bash
# 1. Xem lịch sử thay đổi qua các lần đổi tên của một file:
git log --follow -p -- labs/s18-ci-cd/app/app.py

# 2. Xem commit đổi tên cụ thể:
git log --oneline --follow -- labs/s03-linux-permissions/deploy.sh

# 3. Xem nội dung file trước thời điểm refactor:
git show HEAD~1:linux-labs/lab-03-permissons/deploy.sh
```
