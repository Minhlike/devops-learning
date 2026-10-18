# Nguồn và benchmark đã xác minh

Ngày truy cập: 18-10-2026. Các đường dẫn là nguồn tham khảo, không phải quyền sao chép văn bản hoặc hình ảnh.

| Mã | Loại | Nguồn, phiên bản | Vai trò |
| --- | --- | --- | --- |
| B1 | Benchmark chương trình | ACM/IEEE-CS/AAAI, CS2023 Final Report, bản được các hội nghề nghiệp phê chuẩn năm 2024: https://csed.acm.org/ | Soát độ bao phủ kiến trúc máy, hệ điều hành, mạng, hệ phân tán, bảo mật và kỹ nghệ phần mềm; không gọi là chuẩn DevOps |
| B2 | Benchmark sư phạm | Remzi H. Arpaci-Dusseau, Andrea C. Arpaci-Dusseau, *Operating Systems: Three Easy Pieces*, v1.10, 11-2023: https://pages.cs.wisc.edu/~remzi/OSTEP/ | Học cách dựng mô hình tiến trình, ảo hóa, đồng thời, lưu trữ từ nguyên lý; liên kết đến sách thay vì sao chép |
| B3 | Benchmark nghề nghiệp | Google, *Site Reliability Engineering* (bản gốc 2016, https://sre.google/sre-book/preface/) và *The Site Reliability Workbook* (2018, https://sre.google/workbook/preface/) | Khung suy nghĩ về độ tin cậy, SLO và vận hành; không coi ví dụ Google là mặc định cho mọi tổ chức |
| R1 | Tài liệu kỹ thuật | Linux man-pages 6.19, `fork(2)`: https://man7.org/linux/man-pages/man2/fork.2.html | Tiến trình con, copy-on-write, kế thừa tài nguyên |
| R2 | Tài liệu kỹ thuật | Linux man-pages, `execve(2)`: https://man7.org/linux/man-pages/man2/execve.2.html | Thay process image và quy tắc file descriptor |
| R3 | Tài liệu kỹ thuật | Linux man-pages, `open(2)`: https://man7.org/linux/man-pages/man2/open.2.html | Phân biệt file descriptor với open file description |
| R4 | Tài liệu kỹ thuật | Linux man-pages, `namespaces(7)`: https://man7.org/linux/man-pages/man7/namespaces.7.html | Ranh giới hiển thị tài nguyên của tiến trình |

Nguồn B1–B3 dùng để kiểm tra cấu trúc và mức sâu. R1–R4 hỗ trợ các phát biểu cơ chế của chương 1. Những phần về công nghệ khác chỉ được gắn nguồn chính thức khi biên soạn chương tương ứng; chưa ngầm coi toàn bộ roadmap là đã kiểm chứng kỹ thuật.
