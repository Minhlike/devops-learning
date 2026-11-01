# Guided — quan sát một lần stop

Prerequisite: R-S14-C01 mastered; image OrderOps đã có, quyền dùng Engine được xác nhận. Dùng container mới orderops-r-s14-signal; file D:\Devops\projects\orderops\services\order-api\Dockerfile. Không đụng A/B nếu chúng đang giữ evidence independent.

Tutor đưa từng bước 1–2 lệnh. Đầu tiên chạy container mới trên loopback port18083 còn trống từ orderops-health:s14. Kiểm `docker top orderops-r-s14-signal` và `docker inspect orderops-r-s14-signal` để quan sát process chính/command. Không suy PID trên host bằng1; PID namespace và host có góc nhìn khác.

Sau khi học viên dự đoán và đồng ý dừng đúng fixture mới, chạy `docker stop --timeout 15 orderops-r-s14-signal`. Tiếp theo đọc `docker inspect orderops-r-s14-signal` và logs; ghi StartedAt, FinishedAt, ExitCode, OOMKilled, command và ý nghĩa trong phạm vi output.

Kỳ vọng State chuyển exited; không bịa exact log hay thời gian. Với health-only fixture, chưa có request dài để chứng minh drain. Nếu timeout/137, điều tra log và signal path; không tự gắn nhãn OOM. Khôi phục bằng start đúng fixture khi cần, xác nhận /health. Không dùng kill/prune. Evidence gồm OS/Engine version, process, state trước/sau và giới hạn suy luận. NOT RUN trong refactor.
