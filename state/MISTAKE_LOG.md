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
