# Quy trình có thẩm quyền cho track relearning

Thứ tự: state hiện tại → catalog/prerequisites → content → guided → independent → evidence → acceptance. Các quy tắc legacy trong docs/LEARNING_PROTOCOL.md và docs/ASSESSMENT_POLICY.md không được dùng để xóa lịch sử hoặc ép kỳ thi 9 câu vào từng lesson mới.

Giải thích một mô hình, yêu cầu học viên dự đoán và giải thích ngắn; feedback này không phải kỳ thi chính thức mới. Chỉ sang lab sau khi mô hình đủ rõ. Tutor được dùng worked example trong guided, giảm hỗ trợ dần; independent đổi điều kiện và không có đáp án trong repo học viên. Một self-report không thay được output khi acceptance đòi thực nghiệm.

State machine chính thức: tools/relearning/validate.py (STATES, TRANSITIONS); UML phản ánh cùng cạnh. paused lưu trạng thái trước; resume chỉ tới trạng thái đó. needs_remediation trở về checkpoint thích hợp, không xóa evidence đã hợp lệ. acceptance chỉ được mastered khi guided + independent có evidence xác minh và prerequisites đạt. operational_required=false không ép tạo sự cố.

Dừng khi có nguy cơ mất dữ liệu, tài nguyên không thuộc lab mới, cloud có phí chưa được phép hoặc thiếu quyền. Lưu gap và đề xuất bước tiếp theo. Không chạy block WSL/AWS startup legacy trong refactor này.
