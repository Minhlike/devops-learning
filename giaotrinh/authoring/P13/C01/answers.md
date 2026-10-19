# Đáp án P13.C01 — nằm ngoài bản thảo render

**C13.1.** Không. Tổng 11 dòng là 11.000 valid và 129 bad; summary nói giờ cuối 12.000/189, nên thiếu 1.000 valid/60 bad chứ không có bằng chứng lỗi đã hết. Trước tiên kiểm scrape/target, thời điểm sample, counter reset và đối chiếu log/edge từ đúng population. Đánh dấu SLI ngắn hạn `UNKNOWN`, giữ nguyên đánh giá rủi ro canary và không tăng traffic cho tới khi phép đo hoặc tín hiệu độc lập đủ tin cậy. Không dùng dòng vắng như 0 bad. Monthly summary cũng cần provenance: nếu được cập nhật từ một đường dữ liệu khác, nó không tự sửa được khoảng mù năm phút.

**C13.2.** Tổng 19 bad/1.000 valid = 1,9%; phép tính `(1%+10%)/2=5,5%` trao trọng số 50/50 dù A nhận 90% lưu lượng. SLO 99% cho phép `0,01×1.000=10` bad, nên đã vượt 9 bad. Không đổi SLO hay loại B khỏi population sau khi nhìn số.

**C13.3.** Năm phút có `60/1.000=0,06`; burn `0,06/0,001=60`, vượt 14,4. Nếu giờ có 100/12.000 = 0,008333…; burn `8,333…`, không vượt 14,4, nên điều kiện AND không page dù năm phút xấu. Cần dữ liệu 6h và 30m cùng population mới xét nhánh kia; một mẫu 1h không tái tạo được hai cửa sổ ấy. Ngay cả khi page, nguyên nhân và độ tin cậy đo vẫn phải kiểm tra.
