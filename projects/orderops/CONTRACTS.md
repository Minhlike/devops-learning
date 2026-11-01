# Hợp đồng đích — DESIGNED, chưa triển khai business checkpoint

Java sở hữu products/orders/order_items và order_outbox. POST /orders nhận Idempotency-Key, product_id, quantity; transaction kiểm tồn, ghi order + event; cùng key/payload trả order cũ, khác payload trả409; validation400, không có quyền403, phụ thuộc chưa sẵn sàng503. Không trả thành công trước commit. GET /orders/{id} trả404 nếu thiếu. Error có code/request_id, không log secret/body nhạy cảm. Dùng decimal currency và currency code, không float tiền. Các endpoint này chưa có trong health scaffold.

OrderCreated v1: event_id UUID, order_id UUID, occurred_at timezone UTC, schema_version=1, request_id. Không chứa email/token. API transaction ghi outbox cùng dữ liệu, nên không có cửa sổ commit đơn nhưng quên ghi ý định publish. Go role chỉ SELECT/UPDATE outbox và ghi processed_events; không UPDATE orders. Claim lease và SKIP LOCKED chỉ giải concurrency, không bảo đảm exactly-once effect.

Worker chết sau effect trước ack sẽ nhận lặp; durable effect/idempotency ở cùng transaction hoặc provider key mới bảo vệ được. Message at-least-once, retry bounded exponential backoff+jitter và dead letter/owner; context timeout dừng chờ nhưng không đảo transaction đã commit. Ack chỉ sau durable hậu điều kiện. Test bắt buộc crash trước/sau commit và duplicate event; chưa triển khai nên NOT RUN.

Python đọc CSV snapshot được API/export role read-only cung cấp với watermark/at; ghi báo cáo vào output mới, không sửa DB. Rerun cùng snapshot phải cùng nội dung; publication dùng atomic replace sau validation, không ghi chồng báo cáo đang đọc dở. Tác vụ lỗi trả nonzero; duplicate order ID là input error, không cộng hai lần. Hiện summarize đã kiểm input; atomic file publisher còn backlog.

DB PostgreSQL18: Java runtime không superuser; migration role riêng; reporter SELECT trên view được phép; worker quyền hẹp. Secret từ môi trường/file được quản trị, không vào image/Git. Readiness kiểm phụ thuộc thiết yếu; liveness chỉ process; nghiệp vụ phải POST/GET/đối soát. API chết: edge báo lỗi, worker vẫn xử lý outbox cũ. DB mất: API/worker fail trong deadline, không success giả. Schema lệch: gate kiểm compatibility, rollback code không tự rollback dữ liệu.

Mỗi request có request_id, revision và instance trong log. Metrics đếm error/latency theo route/status, không request_id label. Worker event_id ở log, retry counter thấp cardinality. Report có snapshot ID và row count. Trace là mở rộng sau khi kiểm correlation tối thiểu. Deploy ba chương trình riêng chỉ khi có nhu cầu; không cần broker ở checkpoint đầu.
