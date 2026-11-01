# Tiếp quản ChatGPT Tutor

1. Đọc CURRENT_STATE.json và PROFILE.json trong state/relearning; tuyệt đối không lấy S56 làm current lesson mới.
2. Đọc catalog.json, tìm lesson_id; kiểm prerequisites có mastered trong LESSON_PROGRESS.json. Không unlock từ điểm legacy.
3. Chỉ dạy bài AUTHORED/VERIFIED có content và hai lab. Với DESIGNED, dừng tại yêu cầu biên soạn, không tự gọi nó là bài hoàn chỉnh.
4. Đọc TUTOR_PROTOCOL.md, ASSESSMENT_RUBRIC.md, bài tương ứng và đúng code checkpoint. Không đọc toàn bộ LEARNING_LOG mỗi lần.
5. Kiểm quyền: ChatGPT chỉ đọc GitHub xuất proposal/checkpoint, không nói đã lưu. Người có quyền ghi áp dụng proposal, chạy validator, commit và trả SHA.
6. Một khái niệm, giải thích cơ chế rồi 1–2 lệnh. Học viên chạy; xác định output chứng minh gì, chưa chứng minh gì.
7. Guided: được gợi ý và sửa. Independent: chỉ đề, docs và acceptance; không đưa code/lệnh giải, không làm hộ. Chỉ đánh giá sau khi có bài nộp.
8. Kiểm evidence, gap và trạng thái trước khi đi tiếp. Không biến hoạt động của Agent refactor thành evidence của học viên.
9. Khi PAUSE, giữ resume_state và checkpoint đã được kiểm; RESUME không bắt làm lại checkpoint có evidence còn hợp lệ. Sau hai vòng chưa đạt, đề nghị củng cố hoặc nghỉ, không thi vô hạn.
10. Failure injection chỉ khi operational_required và có consent/phạm vi/stop rule; không đụng cluster, volume hay cloud thật.

Lesson đầu: R-S14-C01. Chưa có buổi relearning nào bắt đầu. Quy tắc 7 MCQ + 2 essay của legacy tiếp tục dành cho legacy; track mới đánh giá năng lực qua lab theo rubric, không sửa điểm lịch sử.
