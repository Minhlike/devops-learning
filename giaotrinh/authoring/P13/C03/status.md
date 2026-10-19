# Kiểm chứng và tồn đọng P13.C03

- PASS — Claim cơ chế PostgreSQL 17 và định nghĩa mục tiêu recovery được đối chiếu nguồn gốc trong `claims.csv` ngày 2026-10-19.
- PASS — Phép tính RPO/RTO và phân loại order theo recovery point kiểm bằng `verify.py` và test độc lập.
- SKIP — Không tạo backup, replay WAL, chạy `pg_verifybackup`, ghi thử ứng dụng hay thao tác dữ liệu thật. Timeline và order đều là fixture giả định.
- UNKNOWN — RPO/RTO production, độ dài WAL chain thực, khả năng giải mã, tính nhất quán xuyên hệ thống và mức mất dữ liệu thực trong một sự cố.
