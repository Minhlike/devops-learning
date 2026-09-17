# NEXT SESSION PLAN

- **Buổi học tiếp theo:** BUỔI 28 — PHASE 6: AWS CloudWatch Monitoring, Metrics, Logs & Alarms.
- **Mục tiêu Buổi 28:**
  1. Nắm vững nền tảng giám sát hệ thống trên AWS với Amazon CloudWatch:
     - Phân biệt 4 trụ cột chính: Metrics, Logs, Alarms và Dashboards.
     - Hiểu kiến trúc thu thập dữ liệu giám sát và luồng luân chuyển dữ liệu của AWS.
  2. Quản trị CloudWatch Metrics:
     - Khảo sát các chỉ số cơ bản của EC2 (CPUUtilization, NetworkIn, NetworkOut, StatusCheckFailed).
     - Khảo sát các chỉ số của Application Load Balancer & Target Group (RequestCount, TargetResponseTime, HTTPCode_Target_2XX_Count, HealthyHostCount, UnHealthyHostCount).
     - Phân biệt Standard Monitoring (chu kỳ 5 phút) vs Detailed Monitoring (chu kỳ 1 phút).
  3. Quản trị CloudWatch Alarms:
     - Thiết lập cấu hình ngưỡng cảnh báo (Metric, Threshold, Evaluation Periods, Datapoints to Alarm).
     - Quản lý các trạng thái vòng đời của Alarm: `OK`, `ALARM`, `INSUFFICIENT_DATA`.
     - Tích hợp Amazon SNS (Simple Notification Service) để tự động gửi thông báo qua email khi alarm chuyển sang trạng thái cảnh báo.
  4. Quản trị CloudWatch Logs:
     - Nắm vững cấu trúc phân cấp: Log Groups, Log Streams, Log Events và Log Retention Policies.
     - Cài đặt và cấu hình CloudWatch Unified Agent trên EC2 để thu thập log hệ điều hành (`/var/log/messages`) và web server log (`/var/log/nginx/access.log`, `error.log`).
     - Sử dụng CloudWatch Logs Insights để viết truy vấn và phân tích log sự cố theo thời gian thực.
  5. Thiết lập CloudWatch Dashboard:
     - Xây dựng bảng điều khiển trực quan hiển thị sức khỏe tổng thể của ứng dụng (EC2 + ALB + Target Group).
  6. Thực hành Failure Injection:
     - Giả lập tải CPU cao hoặc làm sập web server trên EC2 để kích hoạt CloudWatch Alarm chuyển sang trạng thái `ALARM`.
     - Xác nhận nhận email thông báo qua SNS và phân tích nguyên nhân sự cố thông qua CloudWatch Logs Insights.
  7. Vận hành nguyên tắc Cost Safety nghiêm ngặt và dọn dẹp sạch toàn bộ tài nguyên (CloudWatch Alarms, Dashboard, Log Groups, SNS Topics, EC2) sau bài lab.
- **Yêu cầu phương pháp giảng dạy S28:**
  - Tiếp tục duy trì nguyên tắc **Architecture-First**: Phân tích sơ đồ kiến trúc giám sát tổng thể trước khi cấu hình cụ thể từng dịch vụ.
  - Sử dụng ngôn ngữ kỹ thuật chuẩn xác, giải thích cặn kẽ bản chất và tránh các thuật ngữ mang tính tuyệt đối.








