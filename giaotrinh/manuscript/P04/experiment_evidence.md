# Bằng chứng thí nghiệm Git Phần IV (ngoài PDF)

Ngày 2026-10-25, Git `2.51.2.windows.1`. Chỉ chạy trong `D:\Devops\giaotrinh\.p04-git-fixture-20261025`, kho tạm tự tạo với danh tính commit `p04@example.invalid`; đã xác nhận đường dẫn thuộc `giaotrinh/` và dọn sạch sau thí nghiệm. Các SHA dưới đây thuộc fixture đã dọn, không phải repository sách. Số timeout là dữ liệu giả định để thử cơ chế Git, không phải cấu hình production.

| Phép kiểm | Quan sát thực tế | Phạm vi kết luận |
|---|---|---|
| C1 `app.conf` → C2 `service.conf`, byte/mode giữ nguyên | Blob ID giống nhau, root tree ID khác, commit ID khác | Xác nhận mô hình object cho ca đổi tên thuần túy; không suy mọi rename đều giữ blob. |
| Sau stage `2000` rồi sửa đĩa thành `3000` | `git show HEAD:setting.txt` = `1000`; `git show :setting.txt` = `2000`; file trên đĩa = `3000` | Commit lấy index, không lấy bản sửa mới nhất trên đĩa. |
| Merge `main` D với feature C | Git trả exit 1 vì conflict; stage 1/2/3 lần lượt `timeout_ms=1000/3000/2000`; HEAD ở D, MERGE_HEAD ở C | Xác nhận vị trí ba bản cho conflict sửa cùng dòng; một số loại conflict khác có thể thiếu stage. |
| Resolve `2500`, add rồi commit M | M=`f0017177`, cha thứ nhất D=`e7c9405e`, cha thứ hai C=`f4fb4385` | `2500` do người thử chọn, không phải Git tự suy đúng nghiệp vụ. |
| Rebase C lên D, resolve `2500` | Dừng ở conflict cùng ba giá trị; commit mới C′=`788f8a06` khác C, parent là D, nội dung cuối `2500` | Xác nhận object mới và parent mới cho một commit; chưa kiểm mọi tùy chọn rebase. |
| Revert merge M với `-m 1` | Commit revert mới có parent M; `app.conf` trở lại `timeout_ms=3000` | Chỉ kiểm một merge chưa có commit sau; không chứng minh rollback runtime. |
| Reset M về D | Soft: HEAD/index/đĩa=`3000/2500/2500`; mixed=`3000/3000/2500`; hard=`3000/3000/3000` | Kiểm ba mode trong fixture sạch ban đầu; không thử file untracked cản trở. |

Sau `reset --soft`, Git đã từ chối `switch replay` vì thay đổi cục bộ của fixture sẽ bị ghi đè. Người thử đưa riêng fixture về trạng thái sạch trước khi tiếp tục; đây là bằng chứng cho điều kiện an toàn khi chuyển nhánh, không phải lỗi của sách. Không có lệnh nào trên repository học tập, branch chia sẻ hoặc dữ liệu lab.
