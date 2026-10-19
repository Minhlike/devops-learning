# Kiểm chứng và tồn đọng P13.C01

- PASS — Claim nền về SLI/SLO/SLA, event ratio, error budget và multi-window burn đã đối chiếu nguồn gốc trong `claims.csv` (ngày 2026-10-19). Đây là kiểm chứng phạm vi phát biểu, không xác nhận một SLO của hệ thống thật.
- PASS — Fixture giả định, phép tính số học và bài tập được kiểm độc lập bằng `verify.py` và bộ test P13.
- SKIP — Chưa có metric `sli_*` hoặc Prometheus instance; PromQL được so với cú pháp tài liệu chính thức, chưa chạy query trên dữ liệu sống. A2 phải xác nhận label, scrape interval, target và alert routing trên fixture trước khi gọi là thực nghiệm.
- UNKNOWN — SLI client-side, traffic thật, đặc điểm request nghiệp vụ và chính sách release của tổ chức. Cần dữ liệu/duyệt riêng khi áp dụng.
