# Bộ nhớ có thể kiểm toán

Bốn lớp: PROFILE.json (bền vững), LESSON_PROGRESS.json (năng lực), CURRENT_STATE.json + SESSION_CHECKPOINT.md (phiên đang học), EVIDENCE_LOG.jsonl + artifacts được chọn (bằng chứng). Legacy vẫn tại state/*.md và labs/. LEGACY_BASELINE.json khóa byte local lúc tiếp quản, gồm cả lịch sử chưa commit; đó không phải tuyên bố chúng đã có trên remote.

Evidence bắt buộc id, lesson_id, actor, at (ISO8601 có timezone), environment, kind, verification, reference, sha256, verifier, limits. verification phân biệt student_reported/guided_verified/independent_verified/troubleshooting_verified/not_verified. Reference nằm trong repo, không secret; ghi transcript rút gọn đủ kiểm, không cần log khổng lồ. Hash sai làm evidence mất hiệu lực. Actor và verifier phải được kiểm bằng người chịu trách nhiệm; validator không xác thực danh tính con người.

Cập nhật: xuất proposal chứa base SHA, track, lesson, trạng thái trước/sau, evidence và next_action. Người ghi đối chiếu base SHA, gọi transition(), chạy validate.py và commit; chỉ khi có SHA mới nói đã lưu. Nếu hai proposal đụng cùng checkpoint, không last-write-wins: giữ cả hai và hòa giải evidence. Rollback bằng commit sửa hoặc revert được review, không reset history. schema_version=1; schema version lạ phải dừng và migration có backup.

Ôn tập: sau independent pass đề nghị ngày +7; nếu lặp lỗi, đề nghị +2; sau lần recall đủ bằng chứng, +21. Ngày là lịch đề xuất, không tự đổi mastered hay tạo chứng cứ. Mỗi gap ghi lỗi, mô hình nhầm, bằng chứng và bài củng cố. Read-only Tutor xuất JSON proposal và checkpoint cho người có quyền áp dụng, không tự nói đã ghi nhớ GitHub.
