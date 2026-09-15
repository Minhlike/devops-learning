# NEXT SESSION PLAN

- **Buổi học tiếp theo:** BUỔI 26 — PHASE 6: AWS Load Balancing & Auto Scaling.
- **Mục tiêu Buổi 26:**
  1. Phân biệt Vertical Scaling (Scale Up/Down - nâng cấp cấu hình máy chủ) vs Horizontal Scaling (Scale Out/In - tăng giảm số lượng máy chủ).
  2. Hiểu bản chất và vai trò của Load Balancer: Đóng vai trò Reverse Proxy phân phối lưu lượng truy cập đồng đều, tránh điểm nghẽn (Single Point of Failure).
  3. Cấu hình Application Load Balancer (ALB), Target Group và Health Checks định kỳ kiểm tra tình trạng máy chủ.
  4. Quản trị Auto Scaling Group (ASG) kết hợp Launch Template: Định nghĩa cấu hình máy chủ chuẩn (AMI, instance type, user data) để tự động sinh instance.
  5. Cấu hình dung lượng nhóm máy chủ: Desired Capacity, Min Capacity và Max Capacity.
  6. Cơ chế tự phục hồi (Self-Healing): Khi một instance bị lỗi hoặc chết, ASG phát hiện qua health check và tự động spawn instance mới thay thế.
  7. Thực hành Failure Injection: Cố tình terminate một EC2 instance và quan sát trực tiếp hành vi của ASG tự động tạo máy chủ mới để duy trì Desired Capacity.
  8. Giới thiệu chỉ số giám sát cơ bản với Amazon CloudWatch Metrics (CPUUtilization, HealthyHostCount).
  9. Vận hành nguyên tắc Cost Safety nghiêm ngặt và dọn dẹp sạch toàn bộ tài nguyên (ALB, Target Group, ASG, Launch Template) sau bài lab.
- **Yêu cầu phương pháp giảng dạy S26:**
  - Áp dụng nguyên tắc **Architecture-First**: Trình bày kiến trúc và mục tiêu trước, giải thích rõ ràng "chúng ta đang xây cái gì và tại sao cần từng resource" trước khi thao tác.
  - Tối ưu hóa câu lệnh, giảm bớt chuỗi CLI rườm rà không cần thiết so với S25 để tập trung sâu vào mental model và hiểu bản chất hệ thống.






