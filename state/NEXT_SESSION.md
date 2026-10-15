# NEXT SESSION PLAN

- **Buổi học tiếp theo:** BUỔI 43 — Helm Fundamentals (Tiến hành trực tiếp theo Roadmap, không bị chặn bởi sự cố S40).
- **Trạng thái Tiền đề (Prerequisites & State Confirmation):**
  - Buổi 42 (Kubernetes Gateway API & Application Exposure) đã **HOÀN THÀNH (COMPLETED — LEARNING & ASSESSMENT PASS: 7,7/10)** ngày 15/10/2026. Local HTTP routing PASS, Gateway External LoadBalancer provisioning UNRESOLVED (bảo lưu tồn đọng).
  - Buổi 41 (Kubernetes Storage: Volumes, emptyDir, PV, PVC, StorageClass, StatefulSet, PostgreSQL 16 Persistence) đã **HOÀN THÀNH (COMPLETED / PASS)** ngày 15/10/2026.
  - Buổi 40 (Kubernetes Resources, Scheduling & Scaling) tiếp tục giữ trạng thái **IN PROGRESS / PARTIALLY VERIFIED** do tồn đọng sự cố HPA CPU: `<unknown>/50%`. Cụm Kind `s40` và `s41` được giữ nguyên tài nguyên; sự cố S40 được quản lý như một backlog incident độc lập, không cản trở việc bắt đầu S43.
  - Lộ trình Roadmap chính thức: Tiếp tục 2 buổi Kubernetes & Helm (**S43 Helm, S44 K8s Troubleshooting & Defense**) trước khi bước sang Observability (**S45 Prometheus, S46 Grafana**).

---

## 1. CHÍNH SÁCH KIỂM TRA MỚI (BẮT BUỘC ÁP DỤNG TỪ BUỔI 42)
*(Tuân thủ tuyệt đối quy định tại [docs/ASSESSMENT_POLICY.md](file:///D:/Devops/docs/ASSESSMENT_POLICY.md))*

1. **Duy nhất một bài kiểm tra cuối buổi:** Mỗi buổi học chỉ tổ chức đúng MỘT bài kiểm tra chính thức ở cuối buổi sau khi đã hoàn thành 100% phần lý thuyết và bài lab thực hành.
2. **Cấu trúc bài kiểm tra 9 câu:**
   - **PHẦN A — 7 câu trắc nghiệm (7 MCQs):** 4 lựa chọn (A, B, C, D), đúng 1 đáp án chính xác, phân bố ngẫu nhiên, phương án nhiễu hợp lý, không gợi ý lộ liễu, không dùng khái niệm chưa học để đánh đố.
   - **PHẦN B — 2 câu tự luận (2 Essays):** Trả lời bằng đoạn văn giải thích bản chất/cơ chế vận hành. Tuyệt đối **KHÔNG** bắt viết YAML, code, script, lệnh CLI hay thiết kế kiến trúc vượt phạm vi bài học.
3. **Bãi bỏ hoàn toàn các hình thức kiểm tra cũ:** Kể từ S42, **BÃI BỎ** việc tổ chức riêng `Technical Defense`, `Active Recall`, `Timed Defense` hoặc các bài quiz phát sinh trong buổi.
4. **Giới hạn phạm vi kiến thức (Scope Integrity):** 100% câu hỏi phải truy ngược được về nội dung lý thuyết và bài lab thực tế đã học trong chính buổi đó. Nghiêm cấm hỏi kiến thức ngoài lề hoặc câu hỏi phỏng vấn Senior.
5. **Quy trình chấm bài:** Chấm một lượt cả 9 câu sau khi học viên nộp bài; công bố đáp án và giải thích minh bạch; không tự sinh bài kiểm tra thứ hai hay ép kiểm tra lại.

---

## 2. Kế hoạch Nội dung Buổi 43 (Helm Fundamentals)

- **Mục tiêu:** Nắm vững nguyên lý và vận hành Helm Package Manager để đóng gói, cấu hình tham số hóa và quản trị vòng đời ứng dụng Kubernetes (install, upgrade, rollback) một cách chuẩn hóa.
- **Môi trường & Công cụ:**
  - WSL2 Ubuntu 24.04, Docker daemon, Kind cluster (`s41` hoặc cụm mới nếu cần).
  - Helm CLI v3, `kubectl`.
- **Nội dung Lab Trọng tâm:**
  1. Vì sao nhiều Kubernetes YAML rời rạc trở nên khó quản lý (YAML sprawl, thiếu versioning, khó quản lý đa môi trường).
  2. Kiến trúc Helm: Chart, Release, Repository; phân biệt Helm client vs Kubernetes API Server.
  3. Cấu trúc Chart chuẩn: `Chart.yaml`, `values.yaml`, `templates/`, `charts/`, `.helmignore`.
  4. Templating cơ bản: `{{ .Values... }}`, `{{ .Release.Name }}`, built-in objects, template helpers.
  5. Vòng đời Release: `helm install`, `helm upgrade`, `helm rollback`, `helm list`, `helm history`, `helm uninstall`, `helm status`.
  6. Quản lý cấu hình đa môi trường bằng values override (`-f values-prod.yaml`, `--set`).
  7. Failure Injection & Rollback: Cố tình cấu hình sai template hoặc values gây rollout fail $\rightarrow$ sử dụng `helm rollback` để khôi phục về release ổn định trước đó một cách an toàn.
  8. Bài kiểm tra cuối buổi chuẩn hóa: 7 câu trắc nghiệm + 2 câu tự luận về Helm (chỉ trong phạm vi lý thuyết và lab đã thực hành).

---

## 3. Quy chuẩn Phương pháp Giảng dạy & Vận hành Phiên

- **Hiển thị tiến độ phiên:** Mỗi phản hồi trong session học phải hiển thị ngắn gọn tiến độ toàn buổi: phần đã xong, phần hiện tại, phần còn lại.
- **Lab là trung tâm:** Thực hành chiếm phần lớn thời lượng; không biến buổi học thành chuỗi hỏi–đáp lý thuyết suông.
- **Nhịp chuẩn triển khai:** Lý thuyết cần thiết $\rightarrow$ Guided Lab nhỏ $\rightarrow$ học viên chạy $\rightarrow$ đọc output thật $\rightarrow$ giải thích output $\rightarrow$ mini-check khi thực sự cần $\rightarrow$ tăng dần mức tự làm $\rightarrow$ Failure Injection $\rightarrow$ Troubleshooting $\rightarrow$ Bài kiểm tra cuối buổi (7 trắc nghiệm + 2 tự luận) $\rightarrow$ Cleanup.
- **Mini-check có trọng tâm:** Mini-check chỉ dùng tại các điểm kiến thức quan trọng, không hỏi máy móc sau mọi đoạn giải thích.
- **Cấu trúc 4 bước cho từng khái niệm:** `Nó là gì` $\rightarrow$ `Vì sao cần nó` $\rightarrow$ `Nó hoạt động thế nào` $\rightarrow$ `Ví dụ thực tế trong doanh nghiệp`.
- **Chỉ định đường dẫn file:** Trước khi sửa hoặc tạo file, luôn ghi rõ: `File cần sửa: /đường/dẫn/tuyệt/đối/chính/xác`.
- **Phân phối lệnh vừa phải:** Số lượng lệnh mỗi lượt phải vừa phải; trước mỗi lệnh phải giải thích ngắn gọn mục đích; không xả hàng loạt lệnh cùng lúc.
- **Khởi động phiên:** Khi bắt đầu ngày học/session lab mới, thực hiện block khởi động WSL và kiểm tra trạng thái Docker daemon / Kind cluster.
- **Kiểm soát tải nhận thức:** Giảm tốc độ giảng dạy, tinh gọn số lượng khái niệm mới để đảm bảo người học nắm vững bản chất thay vì chỉ chạy lướt qua lệnh lab.
- **Ranh giới Git giữa buổi:** Không cập nhật và push lên GitHub giữa chừng trong buổi học trừ khi học viên yêu cầu.
