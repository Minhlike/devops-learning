# Bàn giao bản thảo A1 — Phần XIII

Phạm vi này chứa **bản thảo khoa học**, dữ liệu giả định và hồ sơ chứng cứ cho Phần XIII theo 12 lesson ID trong `architecture/knowledge_tree.json`. Chưa đưa vào renderer/PDF. `claims.csv` ở từng chương chỉ dành cho Reviewer và A2; tuyệt đối không ghép vào nội dung sách. Các file `status.md` phân biệt PASS của kiểm toán nguồn/số học với SKIP thực nghiệm.

| Chương | Bản thảo và bài | Dữ liệu/kiểm toán | Đầu vào hình |
| --- | --- | --- | --- |
| P13.C01, L01–L03 | `C01/manuscript.md`, `C01/answers.md` (C13.1–3) | `monthly.csv`, `five_minute.csv`, `verify.py`, `test_math.py`, 8 claim | `C01/visual.md` → V30 |
| P13.C02, L01–L03 | `C02/manuscript.md`, `C02/answers.md` (C13.4–6) | `observations.csv`, `request_evidence.csv`, `timeline.csv`, `verify.py`, `test_math.py`, 7 claim | `C02/visual.md` → timeline tùy chọn |
| P13.C03, L01–L03 | `C03/manuscript.md`, `C03/answers.md` (C13.7–9) | `timeline.csv`, `orders.csv`, `verify.py`, `test_math.py`, 6 claim | `C03/visual.md` → V31 |
| P13.C04, L01–L03 | `C04/manuscript.md`, `C04/answers.md` (C13.10–12) | `load.csv`, `verify.py`, `test_math.py`, 6 claim | `C04/visual.md` → biểu đồ/bảng tùy chọn |

## Ranh giới tích hợp

- A2 đặt từng mục `## P13.Cxx.Lyy` vào bài cùng ID. Bài tập có chủ sở hữu chính xác dưới đây; đáp án hiện ở file riêng để đưa về cuối sách. Không sao chép `claims.csv`, `status.md` hay URL vào PDF.

| Lesson chủ | Bài tập |
| --- | --- |
| P13.C01.L01 | C13.2 |
| P13.C01.L03 | C13.1, C13.3 |
| P13.C02.L01 | C13.4 |
| P13.C02.L02 | C13.5, C13.6 |
| P13.C03.L01 | C13.7 |
| P13.C03.L02 | C13.8 |
| P13.C03.L03 | C13.9 |
| P13.C04.L01 | C13.10 |
| P13.C04.L02 | C13.11 |
| P13.C04.L03 | C13.12 |

- C01 kế thừa kỹ thuật metric/PromQL từ P12 và chỉ xây SLI/SLO/burn; C02 dùng kết quả quan sát để điều phối incident, không dạy lại cách thu log/trace; C03 xét DR ở mức dữ liệu và nghiệp vụ, không thay bài storage Kubernetes/cloud; C04 dùng counter tài nguyên như bằng chứng để thử capacity, không dạy lại kernel/cgroup.
- Toàn bộ fixture là dữ liệu giả định có thể kiểm lại bằng code; các script không chạm mạng, database, cluster hay tài nguyên cloud. Không có kết quả production hoặc cam kết capacity/RPO/RTO thực tế.
- Ledger claim ghi nguồn, vị trí, phiên bản URL (nếu tài liệu có version), ngày kiểm, phạm vi hỗ trợ và giới hạn. PASS của ledger là đối chiếu tài liệu cho claim đó, không thay thế review khoa học toàn bản thảo. Reviewer cần xem lại nguồn trước khi A2 hợp nhất vào source map chính; ID nguồn khóa của 19 chương không thay đổi.
- V30/V31 là **yêu cầu kỹ thuật đầu vào**; A2 tự tạo SVG/bảng sau khi kiểm nhãn, phép tính, alt text, caption và trạng thái giả định. Không xem mô tả hình là một hình đã nghiệm thu.

## Kiểm toán trước tích hợp

Chạy `python -m unittest discover -s giaotrinh/authoring/P13 -p test_contract.py -v`, rồi chạy `test_math.py` trong từng thư mục C01–C04 và `verify.py` tương ứng. Các test kiểm cấu trúc, nguồn tách rời và phép tính fixture; **không** chạy restore, incident, load test hay thay đổi ứng dụng thật. Đọc `status.md` từng chương để quyết định thêm thử nghiệm nào trước khi phát hành. Giữ nguyên kiến trúc và bản PDF hiện tại cho đến khi Reviewer duyệt và A2 nhận bàn giao.
