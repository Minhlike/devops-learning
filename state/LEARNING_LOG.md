# LEARNING LOG

## [2026-07-30] Session 1: Onboarding & Diagnostic Test
- Khởi tạo quy trình Persistent Memory Protocol và cấu hình trạng thái tại `D:\Devops\state\`.
- Học viên hoàn thành 34 câu hỏi kiểm tra đầu vào (Diagnostic Test). Kết quả: 18.5/34 câu.

## [2026-07-31] Session 1: WSL2 Setup, Linux CLI Basics & First Git Push
- Xử lý lỗi hỏng đĩa ảo WSL cũ bằng cách chuyển sang `Ubuntu-24.04` thành công.
- Thực hành thao tác Terminal Linux cơ bản, sinh SSH key Ed25519, commit & push thành công kho Git `Minhlike/devops-learning`.

## [2026-07-31] Session 2: Linux Filesystem Hierarchy & Advanced CLI Commands
- Trả lời đúng 100% phần Ôn tập Recall.
- Khám phá các thư mục gốc `/etc`, `/var/log`, `/proc`. Sử dụng Pipe `|` lọc dữ liệu CPU/RAM.
- Dựng cấu trúc thư mục ứng dụng 3-tier sản xuất (`mkdir -p`, `touch`, `cp`, `mv`, `rm -rf`).
- Commit và push thành công bài lab `lab-02-structure` lên GitHub.

## [2026-08-01] Session 3: Linux File Permissions & User/Group Management
- Trả lời đúng 100% bài kiểm tra kiến thức cũ.
- Nắm vững 3 đối tượng (User, Group, Others), 3 quyền (r=4, w=2, x=1) và mã Octal `755`, `644`, `600`.
- Phân biệt sự khác biệt cơ bản giữa phân quyền đĩa native ext4 (Linux) và đĩa Windows mount (`/mnt/d/`).
- Tự tay kích hoạt quyền thực thi và khắc phục thành công lỗi `-bash: ./test.sh: Permission denied`.
- Giải quyết bài lab Failure Injection: Khắc phục sự cố lộ quyền SSH Private Key bằng `chmod 600` chuẩn xác ngay lần thử đầu tiên.
- Commit và push bài lab `lab-03-permissons` lên GitHub `Minhlike/devops-learning`.
