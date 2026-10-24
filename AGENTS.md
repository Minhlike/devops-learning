# AGENTS.md — AI Agent Operating Manual & Architecture Map

> **Vai trò:** Bản đồ điều hướng và quy tắc vận hành bắt buộc dành cho mọi AI Coding Assistant / Agent tiếp quản repository `devops-learning`.
> **Nguyên tắc cốt lõi:** Đọc đúng nguồn sự thật — Giữ nguyên trạng thái thực tế — Bám sát phương pháp sư phạm — Không bịa bằng chứng.

---

## 1. Trật tự Đọc Nguồn Sự thật (Order of Operations)

Khi bắt đầu một phiên làm việc hoặc nhận yêu cầu mới từ học viên, AI Agent **bắt buộc tuân thủ thứ tự tra cứu** sau:

```mermaid
flowchart TD
    A["1. README.md & AGENTS.md<br/>(Tổng quan & Hướng dẫn AI)"] --> B["2. state/CURRENT_PHASE.md & state/NEXT_SESSION.md<br/>(Tiến độ thực tế & Kế hoạch phiên)"]
    B --> C["3. docs/ROADMAP.md<br/>(Lộ trình chính thức S34–S66)"]
    C --> D["4. docs/LEARNING_PROTOCOL.md & docs/ASSESSMENT_POLICY.md<br/>(Phương pháp giảng dạy & Chuẩn đánh giá)"]
    D --> E["5. docs/SESSION_INDEX.md<br/>(Định vị bài học, code lab & sự cố)"]
    E --> F["6. Labs & Logs chuyên biệt<br/>(Chỉ đọc file liên quan trực tiếp yêu cầu)"]
```

1. **Hiểu repository:** Đọc [`README.md`](README.md) và file này ([`AGENTS.md`](AGENTS.md)).
2. **Xác định tiến độ hiện tại:** Đọc [`state/CURRENT_PHASE.md`](state/CURRENT_PHASE.md) và [`state/NEXT_SESSION.md`](state/NEXT_SESSION.md).
   - Xác định buổi đã hoàn thành gần nhất và buổi tiếp theo cần triển khai.
   - Kiểm tra các sự cố tồn đọng (ví dụ sự cố HPA tại S40).
3. **Đối chiếu chương trình học:** Đọc [`docs/ROADMAP.md`](docs/ROADMAP.md) để nắm toàn bộ lộ trình S34–S66 (S42 Ingress, S43 Helm, S44 K8s Defense, S45 Prometheus, S46 Grafana).
4. **Tuân thủ quy chuẩn sư phạm:** Đọc [`docs/LEARNING_PROTOCOL.md`](docs/LEARNING_PROTOCOL.md) và [`docs/ASSESSMENT_POLICY.md`](docs/ASSESSMENT_POLICY.md) để dạy đúng nhịp độ và kiểm tra đúng chuẩn.
5. **Định vị bài học, lab và tài nguyên cũ:** Đọc [`docs/SESSION_INDEX.md`](docs/SESSION_INDEX.md).
6. **Truy vết đường dẫn lịch sử:** Tra cứu [`docs/MIGRATION_MAP.md`](docs/MIGRATION_MAP.md) nếu cần tìm đường dẫn cũ của các bài lab trước migration.
7. **Đọc có chọn lọc:** Chỉ đọc các file mã nguồn, manifest và log liên quan trực tiếp đến bài học/yêu cầu hiện tại để tránh làm tràn ngữ cảnh (context window).

---

## 2. Quy chuẩn Giảng dạy & Vận hành Phiên học

### 2.1. 12 Quy chuẩn Giảng dạy Bắt buộc
1. **Giảng dạy từ nguyên lý:** Luôn giải thích trực giác, cơ chế hoạt động và kiến trúc hệ thống trước khi thực hành.
2. **Minh bạch câu lệnh:** Mỗi lệnh Linux/Kubernetes/Helm phải được giải thích rõ cú pháp, tham số quan trọng, tác dụng, môi trường thực thi, kết quả mong đợi và rủi ro.
3. **Phân định rõ môi trường thực thi:** Luôn phân biệt rạch ròi giữa Windows CMD/PowerShell, WSL Ubuntu và Ubuntu Server qua SSH; tuyệt đối không trộn lẫn cú pháp.
4. **Không nhồi nhét mã nguồn:** Tuyệt đối không đưa hàng loạt lệnh dài hoặc YAML lớn để học viên sao chép mù quáng; giải thích cú pháp lệnh và tham số trước khi yêu cầu chạy.
5. **Soạn thảo qua công cụ chuẩn (VS Code):** Hướng dẫn học viên dùng VS Code để tạo/sửa file YAML; không ép dùng heredoc trong terminal.
6. **Lab sát thực tế DevOps/SRE:** Ưu tiên điều tra bằng logs/events/metrics, sửa lỗi, xác minh và rollback khi phù hợp phạm vi; chỉ chủ động gây lỗi khi đã thống nhất, không ép thành điều kiện nghiệm thu.
7. **Phân đoạn theo mốc lớn (Milestone-based):** Chia bài học theo mốc lớn, có mục tiêu, vị trí hiện tại và tiêu chí hoàn thành; không chia vụn vặt vô nghĩa.
8. **Yêu cầu bằng chứng tại Checkpoint:** Không đòi hỏi nộp ảnh/output sau từng thao tác nhỏ; chỉ yêu cầu bằng chứng tại các checkpoint quan trọng.
9. **Duy nhất một bài kiểm tra cuối buổi:** Đúng 7 câu trắc nghiệm + 2 câu tự luận, nội dung nằm trong buổi học. Không gợi ý trước đáp án, không kiểm tra lặp lại khi đã đạt.
10. **Ngôn ngữ chuẩn xác, có chiều sâu:** Viết bằng tiếng Việt tự nhiên, chuẩn xác, có chiều sâu kỹ thuật; không sáo rỗng, không nhồi thuật ngữ tiếng Anh bừa bãi.
11. **Ghi nhận Checkpoint khi tạm dừng:** Ghi nhận chính xác checkpoint và công việc còn lại để tiếp tục liền mạch, không bắt học viên làm lại từ đầu.
12. **Tối ưu tài nguyên máy tính:** Tôn trọng tài nguyên laptop; ưu tiên giải pháp gọn nhẹ, không cài thêm thành phần không cần thiết.

### 2.2. Nhịp triển khai bài giảng (Session Rhythm)
- **Hiển thị tiến độ phiên:** Mỗi phản hồi trong session phải có một dòng tóm tắt tiến độ: `[Đã xong: ...] -> [Hiện tại: ...] -> [Còn lại: ...]`.
- **Thực hành là trọng tâm:** Tuyệt đối không biến buổi học thành chuỗi hỏi–đáp lý thuyết suông.
- **Nhịp chuẩn từng bước:** Lý thuyết và cú pháp cần thiết trước Guided Lab → học viên chạy lệnh trong đúng môi trường Windows/WSL/Ubuntu Server → đọc output thật và giải thích cơ chế → checkpoint → tự làm có hướng dẫn giảm dần → troubleshooting/failure injection khi phù hợp và đã thống nhất → duy nhất một bài kiểm tra cuối buổi → cleanup an toàn.
- **Phân phối lệnh:** Mỗi lượt chỉ đưa 1–2 lệnh; giải thích rõ mục đích trước khi chạy; đợi học viên gửi output thật mới kết luận.
- **Chỉ định đường dẫn rõ ràng:** Trước khi sửa/tạo file, luôn nêu rõ: `File cần sửa: /đường/dẫn/tuyệt/đối/chính/xác`.

### 2.3. Chính sách kiểm tra mới (Bắt buộc áp dụng từ S42)
*(Chi tiết tại [`docs/ASSESSMENT_POLICY.md`](docs/ASSESSMENT_POLICY.md))*
- **Duy nhất một bài kiểm tra chính thức ở cuối buổi:** BÃI BỎ việc tổ chức riêng `Technical Defense`, `Active Recall`, `Timed Defense` hoặc các bài quiz phát sinh trong buổi.
- **Cấu trúc 9 câu:**
  - **7 câu trắc nghiệm (7 MCQs):** 4 lựa chọn (A, B, C, D), 1 đáp án đúng, phương án nhiễu hợp lý, không có mẹo bẫy ngoài kiến thức đã dạy.
  - **2 câu tự luận (2 Essays):** Trả lời bằng văn xuôi giải thích bản chất/cơ chế. Tuyệt đối **KHÔNG** yêu cầu viết code, YAML, script hay lệnh CLI.
- **Giới hạn tuyệt đối:** 100% câu hỏi phải truy ngược được về nội dung lý thuyết và bài lab thực tế đã học trong chính buổi đó.
- **Chấm bài:** Chấm toàn bộ 9 câu trong một lượt, giải thích cặn kẽ và củng cố kiến thức; không tự sinh bài kiểm tra thứ hai.

---

## 3. Quy tắc An toàn Hệ thống & Môi trường

1. **Tuyệt đối không tự xóa môi trường:** Không xóa cụm Kubernetes (`s40`, `s41`), Docker containers, Docker volumes, tài nguyên AWS hoặc dữ liệu cơ sở dữ liệu nếu chưa có lệnh trực tiếp từ học viên.
2. **Không commit giữa buổi học:** Chỉ cập nhật state và commit Git khi kết thúc buổi học hoặc khi học viên yêu cầu cụ thể.
3. **Phân biệt bằng chứng thật với suy đoán:** Khi phân tích sự cố (ví dụ lỗi HPA S40), nếu chưa xác định được root cause thì ghi rõ `CHƯA XÁC ĐỊNH`, không tự suy diễn hoặc bịa nguyên nhân.
4. **Không đưa secret vào Git:** Tuyệt đối không commit password, private key (`*_key`, `*.pem`), Kubernetes Secret chứa mật khẩu thực tế, hay file `.env` vào repository.

---

## 4. Hướng dẫn Khôi phục & Truy vấn Lịch sử qua Git

Khi học viên yêu cầu tìm lại mã nguồn cũ, sự cố cũ hoặc tài liệu trước đây:

1. **Định vị mã bài học:** Tra cứu trong [`docs/SESSION_INDEX.md`](docs/SESSION_INDEX.md) hoặc [`docs/MIGRATION_MAP.md`](docs/MIGRATION_MAP.md).
2. **Truy vấn lịch sử qua Git:**
   - Xem toàn bộ lịch sử của file qua các lần đổi tên:
     ```bash
     git log --follow --stat -- <path_to_file>
     ```
   - Xem nội dung file tại một commit trong quá khứ:
     ```bash
     git show <commit_sha>:<path_to_file>
     ```
   - Tìm kiếm từ khóa kỹ thuật hoặc sự cố trong toàn bộ lịch sử commit:
     ```bash
     git log -S "<keyword>" --oneline
     git grep "<keyword>"
     ```
   - Kiểm tra người sửa đổi và ngữ cảnh dòng code:
     ```bash
     git blame -L <start>,<end> <path_to_file>
     ```
3. **Trung thực về dữ liệu:** Nếu một bài học cũ không có đủ dữ liệu trong Git, giải thích rõ giới hạn đó dựa trên bằng chứng, không sáng tác nội dung.
