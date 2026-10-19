# Kiểm chứng và tồn đọng P13.C04

- PASS — Công thức Little's Law với điều kiện trạng thái ổn định, thử tải và hành vi overload đã đối chiếu nguồn gốc trong `claims.csv` ngày 2026-10-19.
- PASS — Số L=12/40, backlog +2.400 và forecast 200/s được kiểm bằng `verify.py` và test độc lập trên fixture.
- SKIP — Chưa chạy load/stress/soak test, không có đo CPU, DB hay p95 thật. Các giá trị A/B/C chỉ minh họa giả định.
- UNKNOWN — Bottleneck thật, mức peak an toàn ở 200/s, error rate tại peak, biên mất replica và chi phí vận hành.
