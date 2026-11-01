# Review secret-scan PR #37

Ngày 2026-11-01; base `817ad0da74e5fac644c713f7e591815ac4ce2135`; CI gốc run `41324061054`, Gitleaks 8.24.3.

## Phân loại 12 phát hiện

Hai manifest LEGACY_BASELINE và LEGACY_INITIAL_BASELINE có cùng sáu dòng bị rule generic-api-key bắt. Cả 12 giá trị là chuỗi hexadecimal SHA-256 64 ký tự, tính lại từ tệp local đều khớp; không phải credential. Không có real secret trong 12 giá trị bị báo. Chi tiết từng fingerprint/path/line nằm trong gitleaks-findings.json, không lưu nội dung khóa hoặc log CI thô.

| Dòng mỗi manifest | Đối tượng được checksum | Kết luận |
|---|---|---|
|86|SSH private key local s35_key|Checksum metadata, false positive; khóa thật không được Git track|
|87|SSH public key s35_key.pub|Checksum metadata, false positive; public key được track|
|109,110|Hai Pod manifest dùng Secret|Checksum metadata, false positive; không miễn quét nội dung YAML|
|112|Secret fixture YAML|Checksum metadata, false positive; không xác nhận credential bên trong là production hay còn hiệu lực|
|156|access.log fixture|Checksum metadata, false positive|

Kiểm SSH: private key gốc và bản sao byte trong tmp/relearning-preservation được Git ignore; git log --all trên đúng các private-key paths không có commit. Public key có lịch sử Git là điều bình thường. Không mở kết nối SSH tới host nào. Khóa local dạng OpenSSH không mã hóa bằng passphrase; ACL kế thừa cho Authenticated Users quyền Modify và BUILTIN Users quyền ReadAndExecute. OpenSSH từ chối load vì quyền quá rộng, nên đối chiếu private/public bằng ssh-keygen là NOT RUN, không được gọi là mismatch. Đây là rủi ro bảo vệ secret tại máy; chủ máy cần quyết định thu hẹp ACL/di chuyển hoặc rotate nếu có khả năng truy cập trái phép. Task này không sửa khóa, ACL hoặc lịch sử lab. Bản backup local cũng nhạy cảm và không được đưa vào Git.

## Khắc phục hẹp

Bản sửa ban đầu của `.gitleaksignore` có 12 fingerprint `commit:file:rule:line` chính xác từ log, không có allowlist path, rule hay regex tổng quát. Giữ nguyên nội dung hai manifest và đủ 274 checksum trong từng tệp; không cần thay định dạng hoặc nới validator. Secret thật ở tệp nguồn, phát hiện khác hoặc commit mới không được miễn theo ngoại lệ này.

Tái hiện bằng binary 8.24.3 đã xác minh checksum: bỏ tạm ignore rồi quét đúng commit range của CI gốc cho 12 phát hiện/exit2; bật ignore cho 0 phát hiện/exit0. Fixture âm trong Git repo tạm bên dưới D:/Devops tạo chuỗi ngẫu nhiên không phải credential tại cùng manifest path và dòng86 nhưng commit mới: Gitleaks vẫn phát hiện generic-api-key, exit2. Fixture/log/report thô chỉ ở tmp, không commit. Phạm vi scan tái hiện là lịch sử PR; không tuyên bố toàn bộ mọi ref của repository đã sạch.

## Kiểm chứng thực tế

- 16 local tests gốc PASS (13 validator +3 reporting). Thêm 3 test bảo vệ đúng 12 ngoại lệ, 274 checksum/55/66/S56, và private-key Git exclusion: PASS. validate.py PASS trên 274 hash delivery baseline.
- Maven3.9.11 + Java17 hiện có: `test package` BUILD SUCCESS; unit test Java 1 PASS. Chạy jar thật bind127.0.0.1/port0, GET /health HTTP200/body OK; kết thúc đúng tiến trình do phép thử tạo. Không Docker/VM/cloud/production deploy.
- Go1.27.3 portable: `go test ./...` PASS (2 test lifecycle/replay). Đây chưa là worker PostgreSQL/outbox integration.
- PlantUML1.2026.9: checkonly toàn13 tệp PASS sau sửa ba multiline note thành block note. Đây là syntax PASS, chưa là review độc lập semantics/render.
- Công cụ tải từ release chính thức Gitleaks/PlantUML/Go và Maven Central, kiểm SHA-256 hoặc SHA-512 trước khi chạy, lưu trong tmp/security-tools; Maven repo và Go cache cũng dưới D:/Devops. Không chỉnh PATH/toolchain hệ thống. Chi tiết checksum ở security-tool-downloads.json.
- NOT RUN: Docker lab, PostgreSQL integration, private/public SSH comparison do ACL; không tác động VMware/WSL/Kubernetes/AWS.

CI gốc đã thất bại giữ nguyên trong lịch sử. CI mới được yêu cầu chạy riêng trên commit sửa; kết quả phải đối chiếu run/head SHA thực tế, không suy từ local PASS. Workflow CI/CD đã bị chủ repo tắt trước task; chỉ bật tạm để dispatch kiểm thử với rollback=false rồi trả về disabled. Các job push/deploy yêu cầu push main sẽ không chạy trong dispatch này. Không merge PR.

## Phát hiện bổ sung khi CI quét mọi nhánh

Run41328665737 tại commit5fd48f2: ba Python job PASS, secret-scan FAIL với 2 phát hiện ở commit giáo trình cũ53d5d8f, evidence.json dòng19 và36. workflow_dispatch không có log-opts diff nên quét lịch sử rộng, khác range PR ở run gốc. Hai field idempotency_key là order-prefixed UUID4 do smoke.py tự sinh để kiểm retry, không phải bearer token/API credential; đã đối chiếu producer code và contract. Không hiển thị giá trị. Chúng được ghi riêng ở additional-gitleaks-findings.json và thêm đúng2 fingerprint lịch sử, tổng14 ngoại lệ. Không sửa hồ sơ giáo trình, không tắt rule/path và không giới hạn scan để che lỗi. Run FAIL này giữ nguyên lịch sử; cần một CI mới chứng minh quét rộng thành công.
