# Kiến trúc tri thức

Sách đi từ mô hình máy tính đến vận hành một dịch vụ có người dùng thật. Chương không tương ứng một buổi học. `Đã học` nghĩa là có dấu vết trong roadmap và chỉ mục buổi học hiện hành; không có nghĩa là mọi chi tiết của chương đã được chứng minh trong lab. `Mở rộng` là phần biên soạn vượt ra ngoài lộ trình. S40 là nội dung học dở, với HPA chưa xác minh; S43–S66 là kế hoạch, không phải thành tích.

| Phần | Chương dự kiến | Tiên quyết | Liên hệ repo | Trạng thái nguồn |
| --- | --- | --- | --- | --- |
| I. Máy và hệ điều hành | 1. Từ chương trình đến tiến trình; 2. CPU, bộ nhớ và I/O; 3. Nhân Linux, file, quyền và systemd | Không | S01–S06 | Ch1 đang biên soạn; phần còn lại mở rộng |
| II. Truyền thông | 4. Địa chỉ, định tuyến và TCP; 5. DNS, HTTP, TLS và reverse proxy | I | S07–S09, S27 | Đã học cơ bản, mở rộng giao thức |
| III. Thay đổi có kiểm soát | 6. Git như đồ thị lịch sử; 7. Bash và ranh giới lỗi; 8. Python, Go cho tự động hóa nhỏ; 9. Build, test, phát hành và rollback | I–II | S10–S13, S18–S21 | Go ứng dụng và lý thuyết phát hành mở rộng |
| IV. Môi trường chạy | 10. Namespace, cgroup và container; 11. Image, registry, Compose và dữ liệu | I–III | S14–S17 | Cơ chế kernel mở rộng |
| V. Hạ tầng và đám mây | 12. Hạ tầng AWS, IAM, mạng và lưu trữ; 13. Terraform: đồ thị phụ thuộc và state; 14. Ansible: hội tụ cấu hình | I–IV | S22–S36 | Đã học các lab, phân tích cơ chế mở rộng |
| VI. Điều phối | 15. Kubernetes: desired state và reconciliation; 16. Mạng, storage, scheduling và tài nguyên; 17. Gateway API và Helm | I–V | S37–S44 | S40 một phần; S43–S44 chưa học |
| VII. Đo và điều hành | 18. Metrics, Prometheus, Grafana; 19. Logs, traces và OpenTelemetry; 20. SLI, SLO và error budget; 21. Incident response và phục hồi | I–VI | S45–S50 chỉ là roadmap | Mở rộng, chưa học |
| VIII. Tin cậy và an toàn | 22. Threat model, IAM, secrets; 23. Supply chain, ký và provenance; 24. Kiến trúc production, năng lực, chi phí, DR | I–VII | S51–S66 chỉ là roadmap | Mở rộng, chưa học |

Các phần phụ lục cuối sách sẽ gồm bảng thuật ngữ, nguồn tham khảo theo chương và lời giải có mã câu hỏi. Thứ tự này theo phụ thuộc khái niệm: không thể giải thích giới hạn container nếu chưa có tiến trình và tài nguyên; không thể hiểu HPA nếu chưa hiểu metric và vòng điều hòa; không thể bàn rollback nếu chưa có artifact bất biến và mô hình triển khai.

## Dấu vết khảo sát repo

Đối chiếu ngày 18-10-2026 trên nhánh gốc `refactor/learning-repository-architecture`: `docs/ROADMAP.md` liệt kê S01–S66; `docs/SESSION_INDEX.md` định vị lab và sự cố từ S01 tới S42; `state/CURRENT_PHASE.md` và `state/NEXT_SESSION.md` ghi S42 hoàn thành, S43 tiếp theo, S40/HPA còn mở. Các lab theo chủ đề nằm trong `labs/s02-*` đến `labs/s42-*`, không liên tục vì có buổi lý thuyết hoặc hoạt động cloud. `state/LEARNING_LOG.md` và `state/MISTAKE_LOG.md` là hồ sơ trải nghiệm, chỉ dùng khi viết đoạn cụ thể có thể đối chiếu. Không đưa log hoặc kết quả đo chưa xác minh vào chính văn.
