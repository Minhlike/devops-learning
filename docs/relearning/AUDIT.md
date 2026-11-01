# Audit baseline 2026-11-01

Git root D:/Devops, origin Minhlike/devops-learning; HEAD lúc tiếp quản 393ec63ef48d771e1ab9f7aa54d03c24bdee217d. Bảy tệp local sửa chưa commit: README, ROADMAP, SESSION_INDEX, CURRENT_PHASE, LEARNING_LOG, NEXT_SESSION, SKILL_MATRIX. Không diễn giải chúng thành dữ liệu remote đã xác minh. File hashes trong LEGACY_BASELINE.json giữ trạng thái local thật, đặc biệt 55/66 và S56 checkpoint chờ output.

- docs/LEARNING_PROTOCOL.md / Session startup dựa vào MCP memory và yêu cầu Defense; docs/ASSESSMENT_POLICY.md / Quy chuẩn cuối buổi quy định 7 MCQ +2 essay. Quy tắc này có scope legacy; relearning dùng evidence theo lab. Không sửa điểm cũ.
- docs/LEARNING_PROTOCOL.md / Environment & Cloud Verification có startup WSL/AWS; pha refactor không cần và không được chạy block đó.
- state/CURRENT_PHASE.md / Current Status và state/NEXT_SESSION.md / S56 lặp thông tin; một Tutor mới cần entrypoint gọn. V2 dùng current JSON + catalog, giữ nguyên legacy.
- docs/ROADMAP.md / S15 ghi Flask+Redis, state/CURRENT_PHASE.md / Buổi15 ghi Flask+PostgreSQL. Giữ bất nhất lịch sử, không tự viết lại; dùng OrderOps riêng cho học lại.
- state/CURRENT_PHASE.md và ROADMAP / S40 giữ HPA unknown; S42 Kind Gateway LB chưa giải quyết. Không gọi số buổi hoàn thành tổng thể là tất cả sự cố đã đóng.
- .github/workflows/ci.yml / test tập trung labs/s18-ci-cd Python; chưa có test ba ngôn ngữ. Không sửa workflow có deploy trong pha này. Kiểm V2 chạy cục bộ, CI V2 còn backlog.
- state/LEARNING_LOG.md là chi tiết lịch sử dài; không bắt Tutor đọc hết để tiếp quản một checkpoint. Chưa có structured evidence ledger riêng cho học lại trước V2.

Đã kiểm kê labs, workflows, profile, skill matrix, mistake log và repository guide. Không có cơ sở chấm mọi lab cũ yếu hoặc xóa kết quả cũ. Không truy vấn hạ tầng thật. Textbook giaotrinh/ ngoài phạm vi lần này.

Git delivery: fetch xác nhận main 5b2265ef2b77e639ef0d3b7300fd2306ec63da2e, vẫn 55/66 và S56. Nhánh delivery refactor/devops-learning-v2-main lấy main làm nền, không mang lịch sử giaotrinh. Snapshot ban đầu giữ ở LEGACY_INITIAL_BASELINE.json và Git stash preserve-local-before-v2-main-base; bản sao byte local ở tmp/relearning-preservation (không commit). Main có bổ sung mới ở LEARNING_PROTOCOL/MISTAKE_LOG; dùng bản main mới hơn, giữ bản trước trong snapshot, không xóa lịch sử. LEGACY_BASELINE.json là hash nền delivery, 274 tệp.
