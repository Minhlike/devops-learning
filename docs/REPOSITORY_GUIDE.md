# CẨM NANG KIẾN TRÚC REPOSITORY (REPOSITORY GUIDE)

> **Mục tiêu:** Hướng dẫn toàn diện về cấu trúc tổ chức, quy ước đặt tên, quy trình vận hành và kiểm thử dành cho kỹ sư DevOps và người học khi tham gia phát triển repository `devops-learning`.

---

## 1. Cấu trúc Thư mục Chuẩn hóa (Repository Layout)

```text
devops-learning/
│
├── README.md                          # Tổng quan dự án & cổng thông tin chính
├── AGENTS.md                          # Bản đồ điều hướng & quy chuẩn vận hành cho AI Agent
├── .gitignore                         # Bộ lọc loại trừ rác, cache, secret và file nhạy cảm
│
├── .github/
│   └── workflows/
│       ├── ci.yml                     # Pipeline CI/CD tự động (Test Python 3.10-3.12, Gitleaks, Build)
│       └── release-please.yml         # Tự động hóa tạo release PR & cập nhật CHANGELOG.md
│
├── state/                             # Nguồn sự thật lưu trữ hồ sơ học tập và tiến độ
│   ├── CURRENT_PHASE.md               # Trạng thái hiện tại đã kiểm chứng
│   ├── NEXT_SESSION.md                # Kế hoạch chi tiết cho buổi học kế tiếp
│   ├── SKILL_MATRIX.md                # Ma trận kỹ năng & mức độ làm chủ thực tế
│   ├── LEARNING_LOG.md                # Nhật ký học tập chi tiết theo từng buổi
│   ├── MISTAKE_LOG.md                 # Hồ sơ phân tích lỗi kỹ thuật & bài học kinh nghiệm
│   └── STUDENT_PROFILE.md             # Hồ sơ năng lực, mục tiêu nghề nghiệp & sở thích học
│
├── docs/                              # Hệ thống tài liệu kiến trúc, quy chuẩn & tra cứu
│   ├── ROADMAP.md                     # Lộ trình chuẩn hóa từ S34 đến S66
│   ├── ASSESSMENT_POLICY.md           # Chính sách kiểm tra mới (7 trắc nghiệm + 2 tự luận từ S42)
│   ├── LEARNING_PROTOCOL.md           # Quy chuẩn sư phạm, nhịp học & nguyên tắc tương tác
│   ├── SESSION_INDEX.md               # Chỉ mục tra cứu nhanh theo mã buổi, công nghệ, sự cố
│   ├── MIGRATION_MAP.md               # Bản đồ chuyển đổi đường dẫn legacy -> chuẩn hóa
│   ├── REPOSITORY_GUIDE.md            # Tài liệu cẩm nang kiến trúc repository này
│   └── reference/                     # Tài liệu tham khảo, cheatsheet (Markdown, HTML, PDF)
│
├── labs/                              # Cổng duy nhất chứa toàn bộ các bài thực hành (S02 -> S41+)
│   ├── s02-linux-filesystem/
│   ├── s03-linux-permissions/
│   ├── ...
│   ├── s18-ci-cd/                     # Source app Flask phục vụ pipeline CI/CD
│   ├── ...
│   ├── s39-kubernetes-config/
│   ├── s40-kubernetes-resources/
│   └── s41-kubernetes-storage/
│
└── tools/                             # Công cụ & kịch bản bổ trợ vận hành
    └── generate_pdf.py                # Script sinh tài liệu cheatsheet PDF tự động (ReportLab)
```

---

## 2. Quy ước Đặt tên & Tổ chức Bài Lab (Lab Conventions)

1. **Thư mục bài lab:** Đặt trực tiếp dưới `labs/` với tiền tố buổi học: `sXX-<kebab-case-name>`.
   - Ví dụ: `s41-kubernetes-storage`, `s42-ingress-routing`.
2. **Không phân mảnh thừa:** Mỗi buổi học chỉ cần đúng một thư mục chính. Chỉ tạo thư mục con khi công nghệ bắt buộc (ví dụ `app/` cho mã nguồn ứng dụng, `roles/` cho Ansible role, `templates/` cho Jinja2).
3. **Mã nguồn tối thiểu nhưng tự chứa:** Mỗi thư mục lab phải chứa đủ manifest, code, file cấu hình mẫu để có thể đọc hiểu và tái hiện lại bài thực hành bất kỳ lúc nào.
4. **Bảo toàn dữ liệu fixture:** Các file log mẫu phục vụ bài học (ví dụ `access.log`, `disk_audit.log`) được đưa vào whitelist của `.gitignore` để lưu trữ trong Git.

---

## 3. Quy chuẩn Bảo mật & Vệ sinh Mã nguồn (Security Hygiene)

- **Tuyệt đối không commit Private Key:** Các file khóa SSH (`*_key`, `*.pem`, `*.key`) được tự động chặn bởi `.gitignore`.
- **Tuyệt đối không commit Secret nhạy cảm:**
  - File `.env` chứa mật khẩu thật được chặn bởi `.gitignore`. Chỉ commit `.env.example`.
  - Manifest Kubernetes Secret chỉ chứa dữ liệu giả định/an toàn cho lab, hoặc được tạo trực tiếp trên cluster qua lệnh CLI mà không lưu vào Git.
- **Không commit Runtime Artifacts:**
  - Thư mục provider Terraform (`.terraform/`), file trạng thái local (`*.tfstate`), và plan (`*.tfplan`) hoàn toàn bị loại trừ khỏi Git để giữ dung lượng repository siêu nhẹ.
  - Python bytecode (`__pycache__/`, `*.pyc`) và cache build được tự động bỏ qua.
- **Tự động quét Secrets:** Mọi Pull Request đều được quét tự động bởi Gitleaks thông qua job `secret-scan` trong GitHub Actions.

---

## 4. Quy trình Tạo Bài Lab Mới (Ví dụ Buổi 42 — Ingress)

Khi bắt đầu buổi học mới:
1. Đọc [`state/NEXT_SESSION.md`](../state/NEXT_SESSION.md) để nắm mục tiêu và kế hoạch.
2. Tạo thư mục lab mới: `labs/s42-ingress-application-exposure/`.
3. Triển khai các manifest: `ingress.yaml`, `service.yaml`, `deployment.yaml`.
4. Sau khi hoàn thành bài lab và vượt qua bài kiểm tra cuối buổi (7 trắc nghiệm + 2 tự luận), cập nhật hồ sơ tại `state/` và commit lên Git theo quy chuẩn branch.
