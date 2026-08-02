# BỘ CHEAT SHEET LINUX & DEVOPS CỐT LÕI (PRACTICAL CHEAT SHEET)

## 1. CẤU TRÚC NGỮ PHÁP CÚ PHÁP LINUX (COMMAND LINE ANATOMY)

**Công thức chung:**
```text
Command  [-Options/Flags]  [Arguments]
(Động từ) (Trạng từ bổ nghĩa) (Đối tượng tác động)
```

- **Command**: File chương trình thực thi (binary tại `/bin`, `/usr/bin`).
- **`-` (Cờ ngắn 1 ký tự)**: Ví dụ `-l`, `-a`, `-r`, `-f`. Có thể gộp: `ls -la`, `rm -rf`.
- **`--` (Cờ dài từ đầy đủ)**: Ví dụ `--help`, `--version`, `--no-pager`.
- **`>`**: Ghi đè stdout vào file (xóa sạch nội dung cũ).
- **`>>`**: Ghi nối tiếp stdout vào cuối file (giữ nội dung cũ).
- **`|` (Pipe)**: Chuyển stdout của lệnh trái làm stdin cho lệnh phải.

---

## 2. CÂY HỆ THỐNG FILE LINUX (FILESYSTEM HIERARCHY)

| Thư mục | Khái niệm & Vai trò cốt lõi |
| :--- | :--- |
| `/` | **Root Directory**: Thư mục gốc tối cao của hệ thống. |
| `/home` | Thư mục cá nhân của người dùng (ví dụ `/home/minh123`). |
| `/etc` | Nơi chứa toàn bộ **FILE CẤU HÌNH** của HĐH và ứng dụng (Nginx, SSH...). |
| `/var` | Nơi chứa **DỮ LIỆU BIẾN ĐỔI** (Log hệ thống `/var/log`, cache, DB). |
| `/proc` | Thư mục ảo chứa thông tin phần cứng CPU/RAM & Process trực tiếp từ RAM. |
| `/tmp` | Thư mục chứa file tạm thời (tự động xóa khi reboot). |
| `/mnt/d` | Nơi WSL2 mount ổ đĩa D: của Windows vào Linux. |

---

## 3. THAO TÁC FILE & THƯ MỤC CƠ BẢN

```bash
pwd                                  # In đường dẫn thư mục hiện tại
cd /đường/dẫn                        # Di chuyển tới thư mục (cd .. lùi 1 cấp, cd ~ về home)
ls -la                               # In chi tiết tất cả file/thư mục (kể cả file ẩn .)
mkdir -p folder1/folder2             # Tạo chuỗi thư mục lồng nhau
touch filename.txt                   # Tạo file rỗng mới
cp -r nguồn đích                     # Sao chép file/folder (cờ -r cho folder)
mv nguồn đích                        # Di chuyển HOẶC đổi tên file/folder
rm -rf folder_name                   # Xóa đệ quy folder/file ép buộc không hỏi
cat filename                         # In toàn bộ nội dung file ra màn hình
head -n 10 filename                  # Xem 10 dòng đầu tiên của file
tail -n 20 filename                  # Xem 20 dòng cuối cùng của file
grep "từ_khóa" filename              # Tìm kiếm dòng chứa từ khóa
```

---

## 4. PHÂN QUYỀN & QUẢN LÝ USER (`chmod`, `chown`, `sudo`)

**Bảng điểm Octal:** Read (`r`=4), Write (`w`=2), Execute (`x`=1).
- **User (u)** | **Group (g)** | **Others (o)**

| Mã số | Chuỗi chữ | Ý nghĩa & Trường hợp sử dụng |
| :---: | :---: | :--- |
| **`755`** | `rwxr-xr-x` | Mặc định cho Thư mục & Script thực thi (Owner toàn quyền, Group/Others chỉ đọc/chạy). |
| **`644`** | `rw-r--r--` | Mặc định cho File dữ liệu thường (Owner đọc/ghi, Group/Others chỉ đọc). |
| **`600`** | `rw-------` | Bắt buộc cho **SSH Private Key** (Chỉ Owner đọc/ghi, cấm tuyệt đối người khác). |

```bash
chmod +x script.sh                   # Cấp quyền thực thi cho file script
chmod 600 ~/.ssh/id_ed25519          # Phân quyền chuẩn bảo mật cho SSH Private Key
sudo chown root:root filename        # Đổi người sở hữu file sang user root
```

---

## 5. QUẢN LÝ TIẾN TRÌNH & DỊCH VỤ (PROCESS & SYSTEMD)

```bash
ps aux | grep tên_tiến_trình          # Tìm PID (Process ID) của tiến trình đang chạy
kill -9 <PID>                        # Ép buộc dừng ngay lập tức tiến trình bị treo
top / htop                           # Màn hình giám sát CPU/RAM realtime
sudo systemctl status nginx          # Xem trạng thái dịch vụ Nginx
sudo systemctl start|stop|restart nginx # Khởi chạy / Dừng / Khởi động lại dịch vụ
sudo systemctl enable nginx          # Cho phép dịch vụ tự bật khi khởi động máy
sudo journalctl -u nginx -n 50 --no-pager # Xem 50 dòng log mới nhất của Nginx
sudo nginx -t                        # Kiểm tra cú pháp file cấu hình Nginx
```

---

## 6. QUẢN LÝ GÓI & SỬA SỰ CỐ (APT & INCIDENT RECOVERY)

```bash
sudo apt update && sudo apt install -y package_name # Cập nhật danh sách & cài đặt gói
sudo apt purge -y package_name                      # Xóa sạch gói + XÓA TOÀN BỘ FILE CONFIG TRONG /etc/
curl -I http://localhost                            # Kiểm tra Header phản hồi HTTP Server
```

---

## 7. GIT & GITHUB CƠ BẢN DÀNH CHO DEVOPS

```bash
ssh-keygen -t ed25519 -C "email@example.com" # Sinh SSH Key chuẩn Ed25519
ssh -T git@github.com                        # Kiểm tra kết nối SSH tới GitHub
git init                                     # Khởi tạo kho Git local
git branch -M main                           # Đổi tên nhánh mặc định thành main
git status                                   # Kiểm tra trạng thái làm việc
git add .                                    # Đưa tất cả file mới/sửa vào Staging Area
git commit -m "feat: mô tả công việc"        # Chụp ảnh lưu trữ commit
git remote add origin git@github.com:User/Repo.git # Kết nối remote GitHub
git remote -v                                # Kiểm tra đường dẫn Remote hiện có
git remote rename origion origin             # Sửa lỗi gõ nhầm tên Remote
git push -u origin main                      # Đẩy commit lên nhánh main trên GitHub
```
