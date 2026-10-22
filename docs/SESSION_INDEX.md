# CHỈ MỤC BÀI HỌC DEVOPS (SESSION INDEX)

> **Mục đích:** Bảng tra cứu nhanh toàn diện phục vụ việc tìm kiếm theo mã buổi (`S14`, `S40`, `S41`), theo công nghệ (`Linux`, `Docker`, `Terraform`, `Ansible`, `Kubernetes`, `PostgreSQL`), hoặc theo tình huống sự cố.
> **Nguồn chi tiết:** Chi tiết từng buổi được lưu trữ đầy đủ tại [`state/LEARNING_LOG.md`](../state/LEARNING_LOG.md) và [`state/MISTAKE_LOG.md`](../state/MISTAKE_LOG.md).

---

## 1. Giai đoạn 1 & 2 — Linux, Networking & Scripting (S01 – S13)

| Mã | Chủ đề | Trạng thái | Thư mục Lab / Nguồn | Kỹ năng Cốt lõi | Tình huống Lỗi & Bằng chứng |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **S01** | Onboarding & Linux CLI Basics | **COMPLETED** | `docs/reference/` | WSL2, Linux CLI, pipe, redirect, Git commit & push | Cấu hình SSH key & GitHub authentication |
| **S02** | Linux Filesystem Hierarchy | **COMPLETED** | [`labs/s02-linux-filesystem/`](../labs/s02-linux-filesystem/) | `/etc`, `/var`, `/tmp`, `find`, `grep`, `tar` | File structure, backup, grep log patterns |
| **S03** | Linux Permissions & Users | **COMPLETED** | [`labs/s03-linux-permissions/`](../labs/s03-linux-permissions/) | `chmod 755`, `chown`, user & group, octal notation | Lỗi Permission Denied khi chạy script không có `+x` |
| **S04** | Process & Service Management | **COMPLETED** | [`labs/s04-linux-services/`](../labs/s04-linux-services/) | `systemctl`, `journalctl`, Nginx service, kill, signal | Dịch vụ bị stop đột ngột; phục hồi systemd unit |
| **S05** | Resource Monitoring & Cron | **COMPLETED** | [`labs/s05-resource-monitoring/`](../labs/s05-resource-monitoring/) | `df`, `du`, `top`, `free`, cron automation, log audit | Sự cố Disk Full do log phình to; tự động dọn dẹp |
| **S06** | Phase 1 Exam & Recovery | **COMPLETED** | [`labs/s06-phase1-exam/`](../labs/s06-phase1-exam/) | Khắc phục sự cố tổng hợp Phase 1, postmortem | Sập web do permission + disk full; script `recover.sh` |
| **S07** | Linux Networking Fundamentals | **COMPLETED** | [`labs/s07-linux-networking/`](../labs/s07-linux-networking/) | `ip`, `netstat`, `ss`, curl, Nginx reverse proxy | Cổng bị chiếm dụng (Address already in use) |
| **S08** | HTTP Status Codes & DNS | **COMPLETED** | [`labs/s08-http-dns/`](../labs/s08-http-dns/) | HTTP 200/404/502, `/etc/hosts`, `dig`, DNS resolution | Sự cố 502 Bad Gateway khi upstream app bị tắt |
| **S09** | Phase 2 Exam & Architecture | **COMPLETED** | [`labs/s09-phase2-exam/`](../labs/s09-phase2-exam/) | Packet capture `tcpdump`, Mermaid diagram, audit | Phân tích gói tin HTTP/DNS, postmortem Phase 2 |
| **S10** | Advanced Git Workflows | **COMPLETED** | [`labs/s10-git-advanced/`](../labs/s10-git-advanced/) | Git branching, merge conflicts, `.gitignore`, Git tags | Xung đột merge conflict giữa hai feature branches |
| **S11** | Bash Scripting Fundamentals | **COMPLETED** | [`labs/s11-bash-scripting/`](../labs/s11-bash-scripting/) | Bash variables, if/else, exit codes, healthcheck script | Script kiểm tra endpoint HTTP và trả exit code chuẩn |
| **S12** | Bash Advanced Automation | **COMPLETED** | [`labs/s12-bash-automation/`](../labs/s12-bash-automation/) | Log parsing (`awk`, `sort`, `uniq`), safe backup/rotation | Xoay vòng backup và dọn file cũ quá 7 ngày |
| **S13** | Python Automation for DevOps | **COMPLETED** | [`labs/s13-python-devops/`](../labs/s13-python-devops/) | `pathlib`, `subprocess`, JSON reporting, log parsing | Xử lý lỗi command failure và xuất `health_report.json` |

---

## 2. Giai đoạn 3 & 4 — Docker, Compose & CI/CD (S14 – S21)

| Mã | Chủ đề | Trạng thái | Thư mục Lab / Nguồn | Kỹ năng Cốt lõi | Tình huống Lỗi & Bằng chứng |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **S14** | Docker Fundamentals | **COMPLETED** | [`labs/s14-docker-fundamentals/`](../labs/s14-docker-fundamentals/) | Dockerfile, image layers, port binding, `.dockerignore` | Loại trừ file rác `big.tmp` khỏi Docker build context |
| **S15** | Docker Compose Multi-Container | **COMPLETED** | [`labs/s15-docker-compose/`](../labs/s15-docker-compose/) | Compose YAML, service linking, volume mount, Redis | Web app Flask kết nối Redis cache qua service name |
| **S16** | Advanced Docker Compose | **COMPLETED** | [`labs/s16-advanced-compose/`](../labs/s16-advanced-compose/) | Resource limits (CPU/RAM), healthcheck, depends_on | Container bị restart do healthcheck fail |
| **S17** | Docker Production Capstone | **COMPLETED** | [`labs/s17-docker-capstone/`](../labs/s17-docker-capstone/) | Multi-stage build, Non-root user, minimal base image | Thu nhỏ image từ 1GB xuống 80MB, bảo mật container |
| **S18** | CI/CD with GitHub Actions | **COMPLETED** | [`labs/s18-ci-cd/`](../labs/s18-ci-cd/) | Workflow YAML, matrix test, pip cache, coverage report | Test suite unittest 2/2 PASS, coverage đạt 96% |
| **S19** | Multi-Stage CI/CD Workflows | **COMPLETED** | [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) | Branch protection ruleset, required checks | Khóa nút merge khi coverage < 80% hoặc tests fail |
| **S20** | CD Environments & Rollback | **COMPLETED** | [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) | Manual approval gates, Staging buffer, `:stable` tag | Rollback khẩn cấp kéo image `:stable` qua dispatch |
| **S21** | DevSecOps & Automated Release | **COMPLETED** | [`.github/workflows/`](../.github/workflows/) | Bandit SAST, Gitleaks secret scan, Google Release Please | Tự động sinh `CHANGELOG.md` và tag release `v1.2.0` |

---

## 3. Giai đoạn 5 & 6 — AWS Cloud Infrastructure (S22 – S28)

| Mã | Chủ đề | Trạng thái | Thư mục Lab / Nguồn | Kỹ năng Cốt lõi | Tình huống Lỗi & Bằng chứng |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **S22** | AWS Foundations & IAM | **COMPLETED** | Cloud Practice | IAM Roles, Least Privilege, AWS CLI v2, STS tokens | Phân biệt implicit deny vs explicit deny |
| **S23** | AWS EC2 & VPC | **COMPLETED** | [`labs/s23-aws-ec2/`](../labs/s23-aws-ec2/) | EC2 launch, User Data bootstrap, Security Group | Stateful firewall: Timeout khi revoke port 80 |
| **S24** | AWS Storage (S3 & EBS) | **COMPLETED** | [`labs/s24-aws-storage/`](../labs/s24-aws-storage/) | S3 bucket policy, EBS attach & mkfs, IAM Instance Profile | User Data retry window khi attach IAM Role trễ |
| **S25** | AWS RDS PostgreSQL | **COMPLETED** | [`labs/s25-aws-rds/`](../labs/s25-aws-rds/) | Managed PostgreSQL, Security Group Referencing | Kết nối private an toàn, bảo vệ snapshot thủ công |
| **S26** | AWS ALB & Auto Scaling Group | **COMPLETED** | [`labs/s26-aws-alb-asg/`](../labs/s26-aws-alb-asg/) | Application Load Balancer, Target Group, Multi-AZ ASG | Self-healing: EC2 bị terminate, ASG tự launch mới |
| **S27** | AWS Route 53 & TLS | **COMPLETED** | Cloud Practice | DNS Hosted Zone, A/CNAME record, ACM certificate | TLS termination tại ALB, HTTPS redirect |
| **S28** | AWS CloudWatch Observability | **COMPLETED** | Cloud Practice | CloudWatch Agent, RAM metric, Alarm, SNS, Logs Insights | Báo động RAM vượt 45%, phân tích access log 404 |

---

## 4. Giai đoạn 7 & 8 — Infrastructure as Code & Ansible (S29 – S36)

| Mã | Chủ đề | Trạng thái | Thư mục Lab / Nguồn | Kỹ năng Cốt lõi | Tình huống Lỗi & Bằng chứng |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **S29** | Terraform AWS Foundations | **COMPLETED** | [`labs/s29-terraform-aws/`](../labs/s29-terraform-aws/) | HCL syntax, provider, state, init/plan/apply/destroy | Idempotency: chạy lại apply không sinh thay đổi |
| **S30** | Terraform Multi-Resource | **COMPLETED** | [`labs/s30-terraform-multi-resource/`](../labs/s30-terraform-multi-resource/) | VPC, Subnets, EC2, locals, variables, outputs | Cấu hình tham số hóa hạ tầng, tags động |
| **S31** | Terraform Remote State | **COMPLETED** | [`labs/s31-terraform-remote-state/`](../labs/s31-terraform-remote-state/) | S3 Backend, State Locking, Reusable modules | Bootstrap pattern: bucket phải tạo trước khi backend dùng |
| **S32** | Terraform Advanced Refactoring | **COMPLETED** | [`labs/s32-terraform-advanced/`](../labs/s32-terraform-advanced/) | `count` vs `for_each`, `lifecycle`, `import`, dynamic blocks | Index shift bug của count; import hạ tầng có sẵn |
| **S33** | Ansible Fundamentals | **COMPLETED** | [`labs/s33-ansible-fundamentals/`](../labs/s33-ansible-fundamentals/) | Inventory, playbooks, handlers, Jinja2 templates | Idempotency: lần chạy 2 `changed=0`, quản lý Nginx |
| **S34** | Ansible Roles & Modularity | **COMPLETED** | [`labs/s34-ansible-roles/`](../labs/s34-ansible-roles/) | Role structure (tasks, handlers, templates, defaults, vars) | Phân biệt defaults vs vars; xử lý hidden dependency |
| **S35** | Ansible Multi-Host Automation | **COMPLETED** | [`labs/s35-ansible-multihost/`](../labs/s35-ansible-multihost/) | Inventory groups, `group_vars`, `host_vars`, patterns | Phân biệt node UNREACHABLE vs task FAILED |
| **S36** | Ansible Tags & Vault Secrets | **COMPLETED** | [`labs/s36-ansible-tags-vault/`](../labs/s36-ansible-tags-vault/) | Tags (`--tags`), Ansible Vault AES256, `no_log: true` | Bảo vệ secret lúc nghỉ (at-rest) và lúc chạy (runtime) |

---

## 5. Giai đoạn 9 — Container Orchestration with Kubernetes (S37 – S44)

| Mã | Chủ đề | Trạng thái | Thư mục Lab / Nguồn | Kỹ năng Cốt lõi | Tình huống Lỗi & Bằng chứng |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **S37** | Kubernetes Fundamentals | **COMPLETED** | [`labs/s37-kubernetes-fundamentals/`](../labs/s37-kubernetes-fundamentals/) | Kind 3-node cluster, Pods, Deployments, self-healing | Sự cố cgroup v1 làm sập kubelet; fix bằng cgroup v2 |
| **S38** | Kubernetes Service & Networking | **COMPLETED** | [`labs/s38-kubernetes-service-networking/`](../labs/s38-kubernetes-service-networking/) | ClusterIP, NodePort, CoreDNS, EndpointSlice | Lệch selector khiến EndpointSlice rỗng (0 endpoints) |
| **S39** | Kubernetes Config & Probes | **COMPLETED** | [`labs/s39-kubernetes-config/`](../labs/s39-kubernetes-config/) | ConfigMap, Secret `0400`, Startup/Readiness/Liveness | Readiness 404 gỡ Pod khỏi service; Liveness restart |
| **S40** | Kubernetes Resources & Scaling | **PARTIALLY VERIFIED** | [`labs/s40-kubernetes-resources/`](../labs/s40-kubernetes-resources/) | `requests/limits`, OOMKilled exit 137, QoS, Taints/Tolerations | **Incident tồn đọng:** HPA báo `CPU: <unknown>/50%` |
| **S41** | Kubernetes Storage & Persistence | **COMPLETED / PASS** | [`labs/s41-kubernetes-storage/`](../labs/s41-kubernetes-storage/) | emptyDir, PV/PVC dynamic, StatefulSet, PostgreSQL 16 | Dữ liệu SQL bảo toàn sau khi Pod DB bị xóa và tái tạo |
| **S42** | Kubernetes Gateway API & Application Exposure | **COMPLETED** | [`labs/s42-kubernetes-gateway-api/`](../labs/s42-kubernetes-gateway-api/) | Gateway API, Envoy Gateway, GatewayClass, HTTPRoute, Host/Path routing | Đạt 7,7/10; AddressNotAssigned bảo lưu; 503 recovery |
| **S43** | Helm Fundamentals | **COMPLETED** | [`labs/s43-helm-fundamentals/`](../labs/s43-helm-fundamentals/) | Helm 3, Chart structure, Go templates, values, release lifecycle | Đạt 9,3/10; rolling upgrade bảo toàn traffic khi helm fail; rollback |
| **S44** | K8s Troubleshooting & Defense | **COMPLETED** | [`labs/s44-kubernetes-troubleshooting/`](../labs/s44-kubernetes-troubleshooting/) | Chẩn đoán theo bằng chứng, CrashLoopBackOff, Probes, OOMKilled, Service selector | Đạt 9,6/10; 4 câu hỏi hạ tầng; 7 MCQ + 2 Essay; tốt nghiệp Phase 9 |

---

## 6. Giai đoạn 10 — Observability & Site Reliability Engineering (S45 – S50)

| Mã | Chủ đề | Trạng thái | Thư mục Lab / Nguồn | Kỹ năng Cốt lõi | Tình huống Lỗi & Bằng chứng |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **S45** | Prometheus Fundamentals | **COMPLETED** | [`labs/s45-prometheus-monitoring/`](../labs/s45-prometheus-monitoring/) | Mô hình Pull, TSDB, 4 kiểu metric, PromQL (rate, sum by), scrape configs | Đạt 9,7/10; tạo tải CPU 3 pha & trực quan hóa PromQL; target UP=1 |
| **S46** | Grafana & Practical Dashboards | **IN PROGRESS** | [`labs/s46-grafana/`](../labs/s46-grafana/) | VMware Ubuntu Server, K3s, Podinfo rolling/rollback, Prometheus SD, Grafana | Đang học (22/10/2026); xong 3 panel; còn P95, No Data & bài kiểm tra |
| **S47** | Logging & Centralized Logs | **UPCOMING** | Lộ trình chuẩn | Fluentbit, Loki, LogQL, Log shipping | Chuẩn bị triển khai sau S46 |
| **S48** | Alerting & Notifications | **UPCOMING** | Lộ trình chuẩn | Alertmanager, Alerting rules, Routing, Notification channels | Lộ trình Phase 10 |
| **S49** | SLI, SLO & Error Budget | **UPCOMING** | Lộ trình chuẩn | Định lượng độ tin cậy dịch vụ & Error budget burn rate | Lộ trình Phase 10 |
| **S50** | Incident Response & Runbooks | **UPCOMING** | Lộ trình chuẩn | Runbooks, quy trình điều tra & Blameless Postmortem | Mốc kết thúc Phase 10 |

---

## 7. Giai đoạn 11 & 12 — Lộ trình Kế tiếp (S51 – S66)

- **S51 – S55:** DevSecOps (Trivy, RBAC, PSS/PSA, HashiCorp Vault)
- **S56 – S66:** Capstone Projects & Job Readiness
