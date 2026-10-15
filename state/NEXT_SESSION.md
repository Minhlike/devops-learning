# NEXT SESSION PLAN

- **Buổi học tiếp theo:** BUỔI 42 — Ingress & Application Exposure (Tiến hành trực tiếp theo Roadmap, không bị chặn bởi sự cố S40).
- **Trạng thái Tiền đề (Prerequisites & State Confirmation):**
  - Buổi 41 (Kubernetes Storage: Volumes, emptyDir, PV, PVC, StorageClass, StatefulSet, PostgreSQL 16 Persistence) đã **HOÀN THÀNH (COMPLETED / PASS)** ngày 15/10/2026.
  - Buổi 40 (Kubernetes Resources, Scheduling & Scaling) tiếp tục giữ trạng thái **IN PROGRESS / PARTIALLY VERIFIED** do tồn đọng sự cố HPA CPU: `<unknown>/50%`. Cụm Kind `s40` và `s41` được giữ nguyên tài nguyên; sự cố S40 được quản lý như một backlog incident độc lập, không cản trở việc bắt đầu S42.
  - Lộ trình Roadmap chính thức: Tiếp tục 3 buổi Kubernetes (**S42 Ingress, S43 Helm, S44 K8s Defense**) trước khi bước sang Observability (**S45 Prometheus, S46 Grafana**).

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

## 2. Kế hoạch Nội dung Buổi 42 (Ingress & Application Exposure)

- **Mục tiêu:** Nắm vững cơ chế tiếp nhận và định tuyến lưu lượng HTTP/HTTPS từ bên ngoài cụm Kubernetes vào các dịch vụ nội bộ (Services) ở Lớp 7 (Application Layer).
- **Môi trường & Công cụ:**
  - WSL Ubuntu, Docker daemon, Kind cluster hoặc cấu hình Kind port mapping (extraPortMappings 80/443).
  - Ingress Controller (Ingress NGINX Controller for Kind).
  - `kubectl`, `curl`.
- **Nội dung Lab Trọng tâm:**
  1. Phân biệt ClusterIP vs NodePort vs LoadBalancer vs Ingress (L4 vs L7 Routing).
  2. Cài đặt và cấu hình Ingress NGINX Controller trên Kind cluster.
  3. Khởi tạo Ingress Resource định tuyến theo Host-based (`foo.local`, `bar.local`).
  4. Khởi tạo Ingress Resource định tuyến theo Path-based (`/api`, `/web`).
  5. Default Backend và xử lý mã lỗi HTTP 404/503.
  6. Failure Injection & Troubleshooting: Sai Service name, sai target port, controller ingress class (`spec.ingressClassName: nginx`).
  7. Bài kiểm tra cuối buổi chuẩn hóa: 7 câu trắc nghiệm + 2 câu tự luận về Ingress.

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
