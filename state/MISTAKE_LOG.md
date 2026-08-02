# MISTAKE LOG

## [2026-07-31] Lỗi gõ sai tên Remote trong Git (`origion` thay vì `origin`)
- **Ngày:** 2026-07-31
- **Bối cảnh:** Kết nối Git repository local lên GitHub.
- **Triệu chứng:** `fatal: 'origin' does not appear to be a git repository` khi gõ `git push -u origin main`.
- **Giả thuyết ban đầu:** Chưa tạo remote hoặc chưa add remote.
- **Nguyên nhân gốc:** Gõ thừa chữ `i` trong câu lệnh `git remote add origion ...`.
- **Cách kiểm tra:** Chạy lệnh `git remote -v` để liệt kê danh sách tên Remote đang có.
- **Cách sửa:** Chạy `git remote rename origion origin`.
- **Cách phòng tránh:** Sử dụng lệnh `git remote -v` để kiểm tra lại trước khi thực hiện `git push`.

## [2026-08-01] Sự cố xóa nhầm file `/etc/nginx/nginx.conf` khi sửa lỗi Nginx
- **Ngày:** 2026-08-01
- **Bối cảnh:** Thực hành bài lab Incident Response Nginx config sai syntax.
- **Triệu chứng:** `open() "/etc/nginx/nginx.conf" failed (2: No such file or directory)`.
- **Giả thuyết ban đầu:** Nginx bị mất file cấu hình chính.
- **Nguyên nhân gốc:** Gõ nhầm lệnh `sudo rm /etc/nginx/nginx.conf` thay vì xóa file lỗi `/etc/nginx/conf.d/broken.conf`.
- **Cách kiểm tra:** Chạy `sudo nginx -t` thấy báo thiếu file `/etc/nginx/nginx.conf`.
- **Cách sửa:** Xóa file lỗi `broken.conf` và dùng `sudo apt purge -y nginx nginx-common nginx-core` rồi `sudo apt install -y nginx` để ép buộc apt tải lại file config mặc định.
- **Cách phòng tránh:** Đọc kỹ đường dẫn file trước khi thực hiện lệnh `rm`, đặc biệt là trong thư mục hệ thống `/etc/`.
