# Independent — bàn giao một instance mới

Tạo một instance OrderOps health độc lập với guided, chọn tên và cổng loopback còn trống. Chứng minh nó dùng cùng image đã build, trả HTTP đúng và không bị ảnh hưởng khi instance guided được dừng với sự cho phép. Không dùng lệnh xóa hàng loạt, không đụng workload cũ.

Chỉ tra Docker Running containers: https://docs.docker.com/engine/containers/run/ . Không có lời giải hoặc chuỗi lệnh ở đây; Tutor không làm hộ.

Acceptance: bằng chứng image/runtime identity, trạng thái process, port mapping, HTTP và diễn giải khác biệt stop/remove/image. Nộp output có exit code và giới hạn điều đã kiểm. Nếu không được phép dừng guided, nêu giới hạn và xin bài biến thể an toàn; không bịa kết quả. Assessment chưa bắt đầu.
