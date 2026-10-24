# INCIDENT POSTMORTEM REPORT - PHASE 1 EXAM
- **Ngày xảy ra sự cố:** 2026-08-07
- **Người xử lý (On-Call Engineer):** Minh (DevOps Candidate)
- **Mức độ nghiêm trọng:** High (Dịch cụ Web Ngingx sụp đổ & Tràn dung lượng đĩa)
## 1. Triệu trứng (SYMPTOMS)
- Nginx Web Server bị ngưng hoạt động ('failed /inactive').
- File log ứng dụng 'app_crash.log' phình to chiếm 150 MB dung lượng đĩa.
## 2. NGUYÊN NHÂN GỐC (ROOT CAUSE)
1. **Lỗi Nginx Config:** Dòng cấu hình sai cú pháp 'invalid_ingix_directive_exam;' trong file '/etc/ngĩn/còn.d/exam_fault.còn:1'.
2. **Lỗi Dung lượng Đĩa:"" File log rác 'app_crash.log' phình to chiếm bộ nhớ đĩa.
## 3. QUÁ TRÌNH KHẮC PHỤC (REMEDIATION STEPS)
1. Dùng 'sudo nginx -t' xác định chính xác file lỗi bash


cat << 'EOF' > docs/postmortem-phase1.md
# INCIDENT POSTMORTEM REPORT — PHASE 1 EXAM
- **Ngày xảy ra sự cố:** 2026-08-07
- **Người xử lý (On-Call Engineer):** Minh (DevOps Candidate)
- **Mức độ nghiêm trọng:** High (Dịch vụ Web Nginx sụp đổ & Tràn dung lượng đĩa)
## 1. TRIỆU CHỨNG (SYMPTOMS)
- Nginx Web Server bị ngưng hoạt động (`failed / inactive`).
- File log ứng dụng `app_crash.log` phình to chiếm 150MB dung lượng đĩa.
## 2. NGUYÊN NHÂN GỐC (ROOT CAUSE)
1. **Lỗi Nginx Config:** Dòng cấu hình sai cú pháp `invalid_nginx_directive_exam;` trong file `/etc/nginx/conf.d/exam_fault.conf:1`.
2. **Lỗi Dung lượng Đĩa:** File log rác `app_crash.log` phình to chiếm bộ nhớ đĩa.
## 3. QUÁ TRÌNH KHẮC PHỤC (REMEDIATION STEPS)
1. Dùng `sudo nginx -t` xác định chính xác file lỗi `/etc/nginx/conf.d/exam_fault.conf`.

2. **Lỗi Dung lượng Đĩa:** File log rác `app_crash.log` phình to chiếm bộ nhớ đĩa.
3. Kiểm tra lại cú pháp bằng `sudo nginx -t` và restart dịch vụ bằng `sudo systemctl restart nginx`.
4. Dùng `du -sh *` khoanh vùng file log rác `app_crash.log` và xóa bằng `rm app_crash.log`.
5. Kích hoạt và kiểm tra script khôi phục `./recover.sh`.
## 4. BIỆN PHÁP PHÒNG TRÁNH (PREVENTATIVE ACTIONS)
- Thêm bước kiểm tra cú pháp `sudo nginx -t` vào pipeline CI/CD trước khi reload/restart Nginx trên Production.
- Cấu hình `logrotate` nén và xóa log tự động để chống đĩa bị đầy.
