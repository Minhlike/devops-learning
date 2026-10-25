# NEXT SESSION PLAN

- **Buổi tiếp theo:** S52 — Kubernetes Security & Hardening.
- **Trạng thái gần nhất:** S51 — Container & Image Security Scanning **COMPLETED — 10/10** ngày 25/10/2026.
- **Tiến độ:** 51/66 buổi hoàn thành (77,3%). Phase 10 hoàn tất; Phase 11 đang triển khai.
- **Chuỗi kết quả đã nghiệm thu:** S47 9.8/10; S48 10/10; S49 10/10; S50 9/10; S51 10/10.
- **S51 đã thực hành:** Trivy 0.76.1, Grype, quét image Podinfo, phân tích CVE và Security Gate trả exit code 2.
- **Tồn đọng độc lập:** S40 HPA CPU `<unknown>/50%` chưa xác định root cause; S42 Gateway LoadBalancer `AddressNotAssigned` trong Kind; S46 failure injection No Data không thực hiện theo yêu cầu người học. Không suy diễn kết quả hoặc biến các tồn đọng này thành điều kiện cho S52.

## Chuẩn triển khai S52

- Bắt đầu bằng lý thuyết cần thiết về RBAC, ServiceAccounts, nguyên tắc least privilege và NetworkPolicies; giải thích cơ chế và cú pháp trước từng phần thực hành.
- Phân biệt rõ Windows, WSL và Ubuntu Server; kiểm tra context/namespace và trạng thái hiện tại trước khi thao tác.
- Đi theo từng checkpoint nhỏ, đọc output thật trước khi kết luận; chỉ thực hiện Failure Injection/Troubleshooting nếu nằm trong phạm vi đã thống nhất.
- Chỉ tổ chức một bài nghiệm thu cuối buổi gồm 7 câu trắc nghiệm và 2 câu tự luận, dựa trên nội dung đã dạy và thực hành.
- Không đưa credentials, private key, kubeconfig quản trị hoặc Kubernetes Secret thực tế vào Git; không xóa cluster hay tài nguyên đang chạy khi chưa được yêu cầu.

**S53:** Pod Security Standards & Admission Controllers — UPCOMING.
