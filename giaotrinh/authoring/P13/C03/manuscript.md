# P13.C03 — Backup, DR và phục hồi dữ liệu

**Toàn bộ thời điểm, đơn hàng và kết quả trong chương là fixture giả định. Chưa chạy restore PostgreSQL hay diễn tập trên hệ thống thật.** Mô hình trung tâm: chỉ một bản sao có thể khôi phục, đủ nhất quán và nằm ngoài miền lỗi cần chống mới có giá trị đối với mục tiêu phục hồi.

## P13.C03.L01 — Mục tiêu phục hồi gắn với thời gian và miền lỗi

Khi ứng dụng mất kết nối database, khởi động lại Pod có thể khôi phục process nhưng không tái tạo một đơn hàng đã bị xóa. **High availability** giữ dịch vụ tiếp tục phục vụ khi một thành phần hỏng, thường nhờ bản sao hoặc chuyển vai; **disaster recovery** khôi phục sau biến cố vượt khả năng HA. Replication đưa thay đổi tới bản sao để giảm gián đoạn, đồng thời có thể sao cả thao tác xóa sai hoặc dữ liệu hỏng. Backup là một điểm dữ liệu có thể chọn để phục hồi; nhãn “backup thành công” chỉ nói đã tạo được bản sao theo một quy trình, chưa chứng minh đọc lại đúng nội dung. Snapshot là cách ghi trạng thái ở một thời điểm, nhưng tính nhất quán phụ thuộc tầng tạo snapshot và ứng dụng. Những cơ chế này bổ sung cho nhau; không suy ra backup từ số replica hay từ việc storage tuyên bố durable.

Mục tiêu giả định là **RPO không quá 15 phút**, **RTO không quá 45 phút**. RPO đo khoảng từ thời điểm mất khả năng ghi lúc 10:00 lùi đến commit cuối cùng thực sự khôi phục được. RTO đo từ 10:00 đến lúc đường nghiệp vụ đọc **và ghi** được kiểm chứng, không dừng ở thông báo “database started”. Nếu chỉ đọc được một trang health check, chưa đạt hậu điều kiện. Kịch bản dùng base backup nhất quán lúc 09:00 và chuỗi WAL đã lưu liên tục đến commit 09:52. Sự cố lúc 10:00; phát hiện 10:04, bắt đầu restore 10:08, replay xong 10:27, xác minh dữ liệu và ghi/đọc ứng dụng xong 10:37. Theo fixture, RPO thực tế là 8 phút, RTO thực tế là 37 phút. Đây là phép tính từ timeline, không phải bảo đảm RPO/RTO cho mọi lần sự cố. Nếu WAL thực sự thiếu một đoạn trước 09:52, recovery point phải lùi hoặc restore thất bại; không được ghi 09:52 chỉ vì dashboard archive xanh.

Miền lỗi quyết định bản sao nào còn sống. Hai file trên cùng volume không bảo vệ khi volume mất; replica đồng bộ cùng account và quyền xóa không bảo vệ trước một lệnh xóa lan truyền. Bản sao phục hồi cần được kiểm tra ở miền lỗi tách biệt theo rủi ro đang xét, với chính sách quyền, phiên bản, thời hạn lưu và khóa giải mã còn dùng được. “Offsite” không tự động nghĩa là độc lập trước credential bị chiếm; cần thử kịch bản mất quyền, mất key và xóa nhầm bên cạnh lỗi máy.

## P13.C03.L02 — Bản sao nhất quán và chuỗi phục hồi

Một snapshot filesystem có thể **crash-consistent**: các byte giống lúc máy tắt đột ngột, database phải replay log và vẫn có thể phát hiện giao dịch chưa commit. Nó không mặc nhiên **application-consistent**: ví dụ hai hệ thống cùng ghi một đơn, một snapshot chụp sau DB commit nhưng trước khi đối soát message có thể giữ hai phía ở hai thời điểm khác nhau. Một base backup PostgreSQL hợp lệ cộng WAL liên tục cho phép khôi phục đến điểm mong muốn trong phần WAL còn có; việc sao chép riêng data directory của database đang chạy mà không theo quy trình backup không thay thế cơ chế ấy. Nếu cần nhất quán xuyên database, object store và queue, phải xác định invariant nghiệp vụ và cách đối soát hoặc đóng băng ghi; một snapshot từng hệ thống không tự tạo giao dịch liên hệ thống.

Trong fixture `orders.csv`, O-101 đến O-103 commit chậm nhất 09:52 và còn ở bản khôi phục. O-104 lúc 09:53 và O-105 lúc 09:59 không có trong recovery point; chúng nằm trong khoảng mất dữ liệu 8 phút đã chấp nhận theo RPO, nhưng vẫn cần đối chiếu nguồn giao dịch bên ngoài để xử lý. Một bản sao khác đến 09:59 có thể ít mất hơn, nhưng chỉ chọn được nếu kiểm tra tính toàn vẹn, thứ tự log và miền lỗi. Không đổi điểm khôi phục chỉ dựa vào timestamp của file hoặc “latest” trên UI.

Retention xác định ta có thể quay về bao xa trước một lỗi xóa âm thầm được phát hiện muộn. Versioning hoặc bản sao khó sửa giúp giữ một phiên bản cũ, nhưng không loại rủi ro hết hạn retention, phá khóa mã hóa hoặc cấu hình cho cùng principal được xóa mọi phiên bản. Cần ghi danh mục backup, checksum hoặc kiểm tính toàn vẹn tương đương, chain WAL, phiên bản schema, key và quyền đọc. Hash khớp cho file chỉ xác nhận byte được so khớp; nó không chứng minh giao dịch nghiệp vụ đúng hoặc ứng dụng dùng được.

## P13.C03.L03 — Diễn tập restore và điều kiện dừng

Runbook bắt đầu bằng **dừng thao tác phá dữ liệu**: cô lập writer và job ghi, khóa quyền xóa trên bản sao, giữ ảnh hiện trạng và log trước khi thử restore. Nếu chưa xác định được backup chain, khóa giải mã, recovery target hoặc người phê duyệt ghi đè, dừng trước bước thay production. Diễn tập trên môi trường tạm độc lập: liệt kê base backup và WAL, kiểm tính liên tục, dựng một instance sạch, replay đến commit 09:52, kiểm tra trạng thái database, các order ID và tổng tiền. Sau đó thử bằng tài khoản ứng dụng một phép đọc và ghi có thể hoàn tác, đối soát message/queue, xác nhận route tới instance đúng và chỉ mới cân nhắc mở traffic. Nếu bài kiểm gây thay đổi dữ liệu, dùng fixture độc lập rồi dọn theo chính sách của môi trường thử; không chạy thử trực tiếp trên bản sao duy nhất.

Ở 10:27 chỉ có kết quả replay; 10:37 mới có hậu điều kiện ứng dụng. Báo người chịu trách nhiệm dữ liệu rằng O-104/O-105 chưa có trong điểm khôi phục và cần quy trình tái tạo/đền bù, tránh tuyên bố “không mất dữ liệu”. Nếu client đã nhận xác nhận ghi sau 09:52, phải đối soát với nguồn ngoài DB để không tự phát hành trùng đơn. Khi chỉ có binary/app phục hồi còn nội dung sai, incident vẫn mở. Sau diễn tập, lưu thời điểm, hash, phiên bản, query kiểm tra, sai lệch, quyền đã dùng, thời gian từng bước và kết luận theo từng mục tiêu. Một lần PASS trong môi trường nhỏ không bảo đảm thời gian restore khi dữ liệu lớn hơn hoặc miền lỗi khác; lặp diễn tập với kích thước và điều kiện gần thực tế, không dùng nhãn PASS vĩnh viễn.

### Bài tập C13.7

Từ `timeline.csv`, tính RPO/RTO thực tế và đánh giá hai mục tiêu. Nếu dashboard chỉ ghi “restore xong” lúc 10:27, vì sao không thể dùng 27 phút làm RTO? Nếu thiếu WAL 09:45–09:46, có còn chứng minh được recovery point 09:52 không?

### Bài tập C13.8

Đối chiếu `orders.csv`: đơn nào chắc chắn hiện diện ở recovery point, đơn nào cần đối soát bên ngoài? Một kỹ sư đề xuất chuyển sang replica cùng account rồi xóa bản chính để tiết kiệm thời gian. Nêu ít nhất ba điều kiện cần xác minh trước bất kỳ thao tác hủy dữ liệu nào.

### Bài tập C13.9

Thiết kế hậu kiểm cho một restore: phân biệt kiểm byte, kiểm database, kiểm ứng dụng và kiểm nghiệp vụ. Nêu một tình huống mà checksum PASS nhưng vẫn chưa được mở ghi production.
