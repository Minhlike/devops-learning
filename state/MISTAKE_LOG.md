# MISTAKE LOG

## [2026-07-31] Lỗi gõ sai tên Remote trong Git (`origion` thay vì `origin`)
- **Ngày:** 2026-07-31
- **Bối cảnh:** Kết nối Git repository local lên GitHub.
- **Triệu chứng:** `fatal: 'origin' does not appear to be a git repository` khi gõ `git push -u origin main`.
- **Nguyên nhân gốc:** Gõ thừa chữ `i` trong câu lệnh `git remote add origion ...`.
- **Cách sửa:** Chạy `git remote rename origion origin`.

## [2026-08-01] Sự cố xóa nhầm file `/etc/nginx/nginx.conf` khi sửa lỗi Nginx
- **Ngày:** 2026-08-01
- **Bối cảnh:** Thực hành bài lab Incident Response Nginx config sai syntax.
- **Triệu chứng:** `open() "/etc/nginx/nginx.conf" failed (2: No such file or directory)`.
- **Nguyên nhân gốc:** Gõ nhầm lệnh `sudo rm /etc/nginx/nginx.conf` thay vì xóa file lỗi `/etc/nginx/conf.d/broken.conf`.
- **Cách sửa:** Xóa file lỗi `broken.conf` và dùng `sudo apt purge -y nginx nginx-common nginx-core` rồi `sudo apt install -y nginx` để ép buộc apt tải lại file config mặc định.

## [2026-08-02] Lỗi gõ nhầm tên thư mục trong Shell Script (`lab-5-resources` vs `lab-05-resources`)
- **Ngày:** 2026-08-02
- **Bối cảnh:** Viết script `check_disk.sh` tự động ghi log đĩa.
- **Triệu chứng:** `./check_disk.sh: line 3: /mnt/d/.../lab-5-resources/disk_audit.log: No such file or directory`.
- **Nguyên nhân gốc:** Gõ thiếu chữ số `0` trong tên thư mục (`lab-5-resources` thay vì `lab-05-resources`).
- **Cách sửa:** Đọc lại tên thư mục chính xác bằng `pwd` và sửa lại câu lệnh echo trong script.

## [2026-08-07] Lỗi cú pháp Nginx Reverse Proxy `invalid number of arguments in "proxy_pass"`
- **Ngày:** 2026-08-07
- **Bối cảnh:** Cấu hình Nginx Reverse Proxy chuyển tiếp request Port 8080 sang Python Backend Port 8000.
- **Triệu chứng:** `invalid number of arguments in "proxy_pass" directive in /etc/nginx/conf.d/reverse_proxy.conf:6`.
- **Nguyên nhân gốc:** Thừa/thiếu khoảng trắng khi chèn lệnh proxy_pass bằng bash redirection script.
- **Cách sửa:** Tạo lại file cấu hình tối giản với cú pháp chuẩn `proxy_pass http://127.0.0.1:8000;`.

## [2026-08-08] Lỗi `merge: feature/port-8080 - not something we can merge` khi quên tạo branch
- **Ngày:** 2026-08-08
- **Bối cảnh:** Thực hành bài lab Git Merge Conflict.
- **Triệu chứng:** `merge: feature/port-8080 - not something we can merge`.
- **Nguyên nhân gốc:** Bỏ qua lệnh tạo nhánh `git checkout -b feature/port-8080` nên branch này chưa tồn tại trong Git.
- **Cách kiểm tra:** Dùng lệnh `git branch` để xem danh sách các nhánh hiện có.
- **Cách sửa:** Chạy `git checkout -b feature/port-8080` để tạo nhánh trước khi sửa code và commit.

## [2026-08-24] Bash tạo file literal `BACKUP_FILE` do thiếu `$`
- **Ngày:** 2026-08-24
- **Bối cảnh:** Lab 12 — viết `backup_app.sh`.
- **Triệu chứng:** Xuất hiện file thật tên `BACKUP_FILE` ở thư mục hiện tại dù script thông báo đường dẫn `backups/app-<timestamp>.tar.gz`.
- **Nguyên nhân gốc:** Viết `tar -czf "BACKUP_FILE" ...` thay vì `tar -czf "$BACKUP_FILE" ...`.
- **Cách sửa:** Dùng `$BACKUP_FILE` để Bash thực hiện variable expansion và quote biến bằng `"$BACKUP_FILE"`.

## [2026-08-24] `tar` thất bại nhưng script vẫn trả Exit Code 0
- **Ngày:** 2026-08-24
- **Bối cảnh:** Failure Injection khi thư mục `backups/` không tồn tại.
- **Triệu chứng:** `tar` báo `Cannot open` và status 2 nhưng script vẫn in `Backup thanh cong`; `echo $?` trả `0`.
- **Nguyên nhân gốc:** Sau lệnh `tar` thất bại, `echo` vẫn chạy thành công và trở thành command cuối cùng của script.
- **Cách sửa:** Kiểm tra trực tiếp `if tar ...; then ... else ... fi` và trả `return/exit` phù hợp.

## [2026-08-24] Nhầm phạm vi biến giữa Shell cha và Script
- **Ngày:** 2026-08-24
- **Bối cảnh:** Failure Injection cho `clean_old_backups.sh`.
- **Triệu chứng:** Chạy `BACKUP_DIR="."` trong terminal nhưng script vẫn sử dụng `backups`.
- **Nguyên nhân gốc:** Script tự gán lại `BACKUP_DIR="backups"` trong process Bash mới nên giá trị của shell bên ngoài không được sử dụng.
- **Cách sửa:** Sửa trực tiếp biến khi test hoặc thiết kế script nhận giá trị bên ngoài bằng `BACKUP_DIR="${BACKUP_DIR:-backups}"`.
