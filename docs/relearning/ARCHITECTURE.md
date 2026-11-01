# Kiến trúc theo nhu cầu

Đọc projects/orderops/CONTRACTS.md và architecture.json. Java là nguồn ghi nghiệp vụ; Python batch không tạo API thứ hai; Go là consumer độc lập khi async xuất hiện. C4 đích khác implementation hiện tại: health-only scaffold chưa có DB/event path. Không bật các thành phần đích trước khi đến lesson tương ứng.

| Phương án | Khi hợp lý | Chi phí/rủi ro và trigger đổi |
|---|---|---|
| Siêu nhỏ: Linux/systemd/Nginx/PostgreSQL | Một nhóm, thay đổi ít, chấp nhận mất host theo RTO | Không cần Docker/worker/batch riêng nếu chưa có nhu cầu; backup ngoài host, quyền và restore vẫn bắt buộc. Đổi khi cần isolation/release độc lập |
| Nhỏ: VM/Compose | Cần đóng gói runtime và nhiều tiến trình | Một host là failure domain chung; không gọi HA. Đổi khi headroom hoặc RTO không đáp ứng |
| Vừa: multi-host/managed DB/LB/Terraform/Ansible | Nhiều môi trường, thay đổi hạ tầng lặp lại | Chi phí managed/egress/IAM; thử failover, schema và quyền. Không mặc định Kubernetes |
| Lớn: Kubernetes/platform/GitOps | Nhiều workload/đội và policy đủ biện minh | Phải sở hữu control plane, storage, CNI, upgrade, observability; managed không miễn vận hành |

Không dùng headcount làm tiêu chí duy nhất: đo load, change rate, data-loss tolerance, năng lực trực, blast radius và tổng chi phí. AWS lab phải có Region/account identity/ước lượng giá theo nguồn hiện tại, resource ownership và stop rule; pha refactor chỉ thiết kế, không tạo tài nguyên.
