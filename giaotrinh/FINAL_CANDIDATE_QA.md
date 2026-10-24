# Kiểm tra bản PDF chính sau tái biên tập Phần VI — 2026-10-25

## Phạm vi và toàn vẹn bản thảo

- Baseline: `c7e91d56ed5fcff3cdbfdf7445b30ba522acdb34`. Biên tập xuyên suốt 9 bài `P06.C02.L01–L03`, `P06.C03.L01–L03`, `P06.C04.L01–L03`. Không sửa nội dung P06.C01, P02, P03, P11 hoặc Phần khác.
- Cây xuất bản giữ 15 Phần, 58 Chương, 178 Bài. Tổng độ dài 9 bài từ 4.567 lên 4.604 từ; thay đổi nằm trong cơ chế, tình huống, chuyển tiếp và kết luận, không chỉ lời mở.
- 22 neo trong hồ sơ editorial/wave2 và các claim migration thuộc 9 bài còn nguyên. Không mất marker hình, code, tham chiếu chéo; không sửa câu hỏi/đáp án, source ID hoặc URL đã khóa. Hash trong manifest và editorial evidence đồng bộ.
- Đối chiếu chọn lọc hành vi Deployment, probe với Kubernetes documentation và phân biệt approval/concurrency với GitHub Actions documentation. Đây không phải kiểm toán độc lập mọi claim của sách.

## PDF và kiểm thử

- `Cam_nang_devops.pdf` và candidate giống byte; SHA-256: `578572a9583ce547b32c96ff1bc9993934ffb9dde465632df2f832deb4fdccee`.
- 267 trang A4, 310 bookmark, 0 URI action ngoài, 690.652 ký tự văn bản trích xuất. Times New Roman Regular/Bold và Consolas nhúng; audit của bộ dựng báo `source_leaks=0` trên candidate và PDF chính.
- `python -X utf8 -m unittest discover -s giaotrinh/tests -q`: 44 test OK, 1 SKIP do không có Go toolchain trong PATH, 0 FAIL.
- Đã render và xem đủ trang 75–84, gồm 9 trang thuộc ba chương vừa sửa và trang ranh giới Phần VII. Không thấy chữ, code, hình, đầu trang hoặc ngắt trang bị cắt/tràn. Các trang khác không được render lại trong lượt biên tập này; audit hình học vẫn chạy trên toàn PDF.

## Giới hạn

- Các case `orders-api`, `H83/H84`, race `R1/R2` và các số liệu canary là fixture giả định, không phải log hoặc benchmark production.
- Không chạy rollout cluster, hệ CI thật, migration database hoặc đối soát thanh toán trong lượt biên tập văn phong. Go test SKIP. Lượt QA này không cấp Publication PASS cho toàn sách.
