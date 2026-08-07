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
- **Cách kiểm tra:** Chạy `sudo nginx -t` đọc chính xác số dòng bị lỗi.
- **Cách sửa:** Tạo lại file cấu hình tối giản với cú pháp chuẩn `proxy_pass http://127.0.0.1:8000;`.
