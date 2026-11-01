# Kiểm chứng V2 ngày 2026-11-01

Phạm vi bàn giao là nền tảng khóa học và hai lesson đầu theo phương án khối lượng lớn ở mục43 yêu cầu. Chưa hoàn thiện nội dung toàn bộ S14–S48.

| Hạng mục | Kết quả | Giới hạn |
|---|---|---|
| Curriculum | 35 buổi, 70 lesson, dependency graph không chu kỳ | 2 AUTHORED, 68 DESIGNED; không dùng designed card làm bài học |
| Học liệu mở đầu | 2 bài lý thuyết, 2 Guided, 2 Independent | Chưa chạy lab Docker, không learner mastery |
| Validator/tests | 13/13 PASS | Kiểm cấu trúc và gate, không xác thực danh tính người nộp |
| Python reporting | 3/3 PASS | CSV fixture, không query PostgreSQL hoặc benchmark |
| Java Maven/HTTP | NOT RUN | Java17 có; Maven không có trong PATH; không tự cài toolchain |
| Go tests | NOT RUN | Go không có trong PATH |
| Docker Compose/stack | NOT RUN | Chưa có stack business implementation; không tác động Engine/WSL/cluster |
| Sơ đồ | 13 tệp PlantUML có source, state edges khớp code | Chỉ kiểm file/envelope, chưa PlantUML syntax/render hoặc review độc lập |
| Legacy | 274 hash delivery baseline hợp lệ | Initial snapshot và main mới được phân biệt trong AUDIT; S56 chưa có output |
| Chứng chỉ | NOT_MAPPED | Chưa kiểm blueprint, không tuyên bố exam readiness |

Sơ đồ: context, containers, components, create-order, order-state, vm-deployment, kubernetes-deployment, data-model, cicd, observability, tutor-learning-process, tutor-state-machine, tutor-interaction-sequence. C4 dùng PlantUML standard library, UML activity có swimlanes/decision/loop, ERD dùng Crow's Foot. Đích thiết kế được ghi DESIGNED để không nhầm với code health-only hiện tại. Không cần BPMN bổ sung khi quy trình hiện tại đã dùng UML activity.

Các test âm đã chạy: duplicate ID, prerequisite thiếu, cycle, mastered không evidence, docs thiếu, state sai, file thiếu, evidence sai owner/không xác minh, schema version lạ, catalog/progress lệch, unlock quá sớm, resume sai và shortcut trạng thái. Đọc hash không thay cho nghiệm thu lab. Không có evidence học viên mới được tạo trong pha refactor.

Backlog có thứ tự và acceptance ở BACKLOG.md. Điểm tiếp quản: TEACHER_START_HERE.md → R-S14-C01, chỉ bắt đầu khi học viên yêu cầu và môi trường thực hành sẵn sàng. Git delivery không merge main. Bản sao byte và stash bảo toàn ban đầu vẫn ở máy, không commit file thô hay secret.
