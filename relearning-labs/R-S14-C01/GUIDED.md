# Guided — hai lần chạy từ một image

Môi trường: shell Linux đã có Docker Engine được học viên cho phép sử dụng. Không khởi động WSL/Engine tự động. File nguồn Windows: D:\Devops\projects\orderops\services\order-api\Dockerfile; trong WSL là /mnt/d/Devops/projects/orderops/services/order-api. Chỉ dùng tên mới orderops-r-s14-a/b và port loopback 18081/18082 sau khi kiểm chúng chưa bị chiếm. Không xóa tài nguyên cùng tên nếu đã tồn tại.

Chuẩn bị có điều kiện: tại thư mục order-api, JDK17 và Maven>=3.6.3, `mvn test` rồi `mvn package`. Nếu thiếu Maven hoặc tải dependency bị chặn, checkpoint blocked, không ghi test PASS. Tutor giải thích jar là đầu ra và target/order-api.jar phải tồn tại. Đây là các bước chuẩn bị guided, mỗi lượt chỉ đưa 1–2 lệnh.

1. Từ thư mục trên, chạy `docker build -t orderops-health:s14 .`. Quan sát COPY có đúng jar; build fail thì chưa có candidate.
2. Chạy `docker run -d --name orderops-r-s14-a -p 127.0.0.1:18081:8080 orderops-health:s14`. Giải thích -d, tên mới và host:container; EXPOSE không thay -p.
3. Kiểm `docker inspect orderops-r-s14-a` rồi `curl --fail http://127.0.0.1:18081/health`. Kỳ vọng có process Running và body OK, nhưng chỉ kết luận sau output thật. Ghi .Image, State và NetworkSettings.Ports.
4. Tạo B từ cùng image ở port18082 sau khi Tutor giải thích thay đổi này; stop A rồi quan sát B và image vẫn còn. Không dùng prune/down -v. Cleanup chỉ sau học viên yêu cầu, đúng tên do buổi này tạo, không volume.

Evidence: lệnh, exit code, image ID A/B, trạng thái A trước/sau stop, HTTP A/B và giải thích. Nếu HTTP fail: phân biệt lỗi bind host, app exited và route; đọc logs container mới trước khi sửa. Không gây sự cố ngoài phạm vi. Recovery: start lại đúng A nếu nó chỉ bị stop; không build lại rồi gọi là cùng đối tượng. Refactor chưa chạy Docker lab này: NOT RUN.
