# OrderOps — checkpoints, không phải stack production sẵn có

Hiện thực hiện tại: Java health endpoint cho S14; Python CSV reporting có unit tests; Go worker lifecycle và dedupe trong bộ nhớ có test source. Không có REST API Python. Worker chưa có persistence và không hứa idempotency sau restart. PostgreSQL/outbox ở mức DESIGNED trong CONTRACTS.md; không gọi thiết kế ấy là code đã triển khai.

Java: JDK17 LTS; Maven3.9.x khi có môi trường; chạy `mvn test` rồi `mvn package` tại services/order-api. Dockerfile chỉ COPY jar, không tự tải Maven vào host. Unit test health chưa kiểm HTTP integration. Python: tại services/reporting chạy `python -m unittest -v`; Go: tại services/event-worker chạy `go test ./...` khi có Go1.26+. Không cài toolchain hoặc khởi động Docker/WSL trong refactor.

Checkpoint kế: Java DTO/validation → PostgreSQL transaction/migration/idempotency → outbox trong transaction → Go claim/ack với durable processed_events → Python read-only snapshot. Chỉ giới thiệu checkpoint cần thiết cho từng lesson. Không để sẵn lời giải independent lab.
