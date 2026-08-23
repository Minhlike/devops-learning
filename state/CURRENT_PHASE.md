# CURRENT LEARNING PHASE

- **Current Phase:** PHASE 3 — Git, Bash Scripting & Python cho DevOps
- **Current Status:** Hoàn thành Buổi 12 — Bash Advanced Automation: Functions, `for/while`, Automated Backup, Log Parser, Safe Cleanup & Failure Injection. Chuẩn bị Buổi 13 — Python Fundamentals for DevOps.
- **Current Week:** Tuần 3
- **Completed Outputs:**
  1. Hoàn thành `backup_app.sh`: tạo backup `.tar.gz` tự động với timestamp.
  2. Tổ chức Bash script bằng Functions; phân biệt `return` trong function và `exit` của toàn script.
  3. Kiểm tra success/failure path bằng Exit Code `0` và khác `0`.
  4. Viết `parse_log.sh` dùng `grep`, command substitution `$()` để đếm `ERROR` và HTTP `500`.
  5. Dùng vòng lặp `for` để xử lý nhiều file log và `while read -r` để xử lý log từng dòng.
  6. Viết `clean_old_backups.sh` dùng `find`, `-mtime +7`, `-print`, `-delete`.
  7. Hoàn thành Failure Injection chống cleanup sai đường dẫn bằng safety guard trước thao tác destructive.
  8. Troubleshoot lỗi variable expansion, cú pháp `[` `]`, exit status và phạm vi biến Shell/Script.
