# DevOps Learning Roadmap (S34 – S66)

## 1. Tổng quan Lộ trình Chuẩn hóa

Lộ trình học tập chuẩn hóa được thống nhất từ Buổi 34 đến Buổi 66, định hướng trang bị năng lực thực chiến cho vị trí DevOps Intern / Fresher / Junior DevOps.

---

## 2. Chi tiết Lộ trình theo Giai đoạn

### Phase 8 — Configuration Management & System Automation (S34 – S36)
- **S34:** Ansible Roles & Modular Playbooks — **COMPLETED**
- **S35:** Advanced Inventory & Multi-Host Automation — **COMPLETED**
- **S36:** Ansible Deployment Strategy, Tags, Vault & Secrets — **COMPLETED**

### Phase 9 — Container Orchestration with Kubernetes & Helm (S37 – S44)
- **S37:** Kubernetes Fundamentals: Cluster, Pod, Deployment — **COMPLETED**
- **S38:** Kubernetes Service & Networking — **COMPLETED**
- **S39:** Kubernetes ConfigMap, Secret, Environment & Probes — **COMPLETED**
- **S40:** Kubernetes Resources, Scheduling & Scaling — **IN PROGRESS / PARTIALLY VERIFIED** (Resources, QoS, Scheduling PASS; tồn đọng sự cố HPA CPU `<unknown>/50%` được điều tra độc lập, cluster `s40` giữ nguyên)
- **S41:** Kubernetes Storage (Volumes, emptyDir, PV, PVC, StorageClass, StatefulSet, PostgreSQL 16 Persistence) — **COMPLETED / PASS** (15/10/2026)
- **S42:** Ingress & Application Exposure — **NEXT SESSION**
- **S43:** Helm Fundamentals (Charts, Values, Templates, Release Lifecycle)
- **S44:** Kubernetes Troubleshooting & Defense (Cluster & Workload Recovery)

> **Mốc quan trọng (Milestone):** Còn đúng 3 buổi (**S42, S43, S44**) thuộc mảng Kubernetes & Helm trước khi chuyển tiếp sang mảng Observability. Không chèn thêm các buổi Kubernetes phát sinh.

### Phase 10 — Observability & Site Reliability Engineering (S45 – S50)
- **S45:** Prometheus Fundamentals & Metrics (Metrics collection, PromQL, Exporters, Pull model)
- **S46:** Grafana & Practical Dashboards (Visualization, Panels, Dashboard as Code, Querying)
- **S47:** Logging & Centralized Logs (Log aggregation, Fluentbit/Loki, LogQL, Log shipping)
- **S48:** Alerting (Alertmanager, Alerting rules, Routing, Grouping, Inhibit rules, Notification channels)
- **S49:** SLI, SLO & Error Budget (Service Level Indicators/Objectives, Error Budget calculation, Burn rate)
- **S50:** Incident Response & Runbooks (Incident Lifecycle, Troubleshooting runbooks, Blameless Postmortem)

> **Mốc quan trọng (Milestone):** **S45** bắt đầu học Prometheus. **S46** bắt đầu học Grafana. Không tự ý dời Prometheus hoặc Grafana sang buổi khác.

### Phase 11 — DevSecOps & Security Automation (S51 – S55)
- **S51:** Container & Image Security Scanning (Trivy, Grype, Base image hardening, Distroless)
- **S52:** Kubernetes Security & Hardening (RBAC, ServiceAccounts, Least privilege, NetworkPolicies)
- **S53:** Pod Security Standards & Admission Controllers (PSS/PSA, OPA/Kyverno enforcement)
- **S54:** Secrets Management in Kubernetes (HashiCorp Vault / External Secrets Operator)
- **S55:** CI/CD Security Pipeline Integration (SAST, DAST, Secret scanning, Dependency check)

### Phase 12 — Capstone Projects & Job Readiness (S56 – S66)
- **S56 – S60:** Production-Grade DevOps Capstone (End-to-End GitOps, Kubernetes Cluster, CI/CD, Observability stack)
- **S61 – S63:** Multi-Environment Infrastructure & Disaster Recovery / High Availability Simulation
- **S64 – S66:** Portfolio Review, Technical Interview Preparation, CV & Career Coaching (DevOps Fresher/Junior)
