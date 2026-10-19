# P13.C02 — Ứng cứu sự cố và học từ bằng chứng

**Tình huống, log tóm tắt và số liệu trong chương là fixture giả định, không phải kết quả chạy production.**

## P13.C02.L01 — Phát hiện, điều phối và phân loại tác động

Một alert chỉ là tín hiệu được một quy tắc phát ra. Một incident bắt đầu khi có tác động hoặc rủi ro đủ để cần phối hợp ứng cứu; incident có thể được khai báo từ cuộc gọi khách hàng dù alert im lặng. **Impact** mô tả ai bị ảnh hưởng, hành động nào hỏng, bao nhiêu sự kiện và trong bao lâu. **Severity** là mức tác động đã xác định theo chính sách tổ chức; **priority** là thứ tự xử lý có thể thay đổi vì thời gian, nghĩa vụ pháp lý hoặc rủi ro tiếp diễn. Không gán P1 chỉ vì một biểu đồ màu đỏ. Ngược lại, sai số tiền đã lưu là lý do hợp lý để đề xuất P1 dù HTTP 5xx bằng 0; người trực vẫn phải đối chiếu tiêu chí P1 thực tế của tổ chức.

Fixture `observations.csv` theo cùng một cửa sổ năm phút: v1 phục vụ 900 request, 1 số tiền sai; v2 phục vụ 100 request, 30 số tiền sai. Cả hai có `http_5xx=0`. Nếu SLI chỉ đếm status thành công thì sẽ báo 100% good, trong khi phép đối soát nghiệp vụ cho thấy 31/1.000 request sai, tức 3,1%. Trước canary, v1 ở cửa sổ trước có 1/900 sai; đây là baseline nhỏ, không chứng minh v1 hoàn hảo. Tỷ lệ v2 sai 30%, v1 khoảng 0,111% cùng thời điểm. Ta mới có một tương quan mạnh với release, chưa có root cause. Việc tập v2 là 10% lưu lượng cần kiểm chứng phân tuyến thực tế, không chỉ cấu hình cân bằng tải.

Tại 10:07, trong bài toán giả định, người trực tuyên bố incident và mở một tài liệu trạng thái sống: tác động đã biết, phần chưa biết, giả thuyết, người phụ trách, thời điểm cập nhật tiếp theo. Incident commander (IC) giữ mục tiêu và quyền điều phối; Ops lead thực hiện thay đổi kỹ thuật trong phạm vi được giao; Communications lead báo đều cho khách hàng và các nhóm liên quan, nêu điều đã xác minh, điều đang điều tra và mốc cập nhật. Nếu chỉ có một người, họ có thể tạm kiêm vai nhưng phải ưu tiên gọi hỗ trợ khi đồng thời vừa đổi hệ thống vừa báo cáo trở nên không an toàn. Escalation không phải chuyển trách nhiệm cho “ai đó”: nêu rõ cần quyền gì, quyết định nào, thời hạn nào. Nhật ký chung ghi cả thử nghiệm thất bại và lý do dừng để người sau không lặp thao tác nguy hiểm.

## P13.C02.L02 — Cạnh tranh giả thuyết, giảm tác động, xác nhận phục vụ

Từ `request_evidence.csv`, hai request v2 mang 4.100 và 5.900 cents được lưu thành 41 và 59 cents, nhưng đều trả HTTP 200; request v1 cùng đầu vào 4.100 giữ 4.100. DB time 42–49 ms và p95 toàn cửa sổ 180–190 ms không cho thấy tăng chậm lớn, nhưng vài mẫu không đủ loại bỏ mọi vấn đề database. Giữ bốn giả thuyết: DNS/edge đưa sai đích; DB làm chậm hoặc ghi sai; adapter v2 đổi đơn vị; feature flag chỉ áp cho nhóm canary. DNS sai toàn service khó giải thích khác biệt cùng edge giữa v1/v2, nhưng cần so địa chỉ và revision trên chính request. DB chậm không giải thích nhân 1/100 nhất quán; vẫn có thể có lỗi ghi logic ở tầng DB. Feature flag và adapter đều còn khả dĩ cho tới khi so config, diff và tái hiện cặp input–output trong fixture độc lập. Một diff **giả định** `store(amount_cents)` → `store(amount_cents // 100)` khớp hai mẫu v2; đây là bằng chứng cơ chế của tình huống, không là log/code production đã quan sát. Cần kiểm tra toàn bộ 30 bản ghi theo release/request ID trước khi khẳng định phạm vi tác động.

Đường giảm tác động chọn theo ranh giới dữ liệu. Tại 10:09 giữ digest, manifest, config flag, log/trace, phân tuyến và snapshot dữ liệu; hạn chế truy cập bản sao có thông tin khách hàng. Tại 10:12 dừng **đường ghi mới của v2**, đưa traffic về v1 rồi xác nhận không còn worker/queue consumer v2; chỉ rollback routing mà bỏ qua job nền là chưa đủ. Nếu lỗi nằm sau một flag độc lập, tắt flag có thể nhanh hơn, nhưng phải chứng minh phiên v2 không còn ghi sai. Failover sang vùng khác sẽ vô ích nếu cùng binary/config sai hoặc dữ liệu đã được sao chép; nó chỉ phù hợp nếu failure domain được chứng minh độc lập. Traffic shifting, rollback, flag và failover là các lựa chọn có tiền điều kiện/hậu điều kiện, không phải bốn nút “chữa lỗi” tương đương.

Sau 10:16, một request ghi/đọc mới qua v1 trả số tiền đúng; cần lấy mẫu từ nhiều client/route và kiểm tra digest cùng revision đang phục vụ. Đó là bằng chứng **đường request mới** phục vụ lại, chưa phải phục hồi dữ liệu cũ. Lúc 10:22 mới khoanh được 30 bản ghi nghi sai từ v2; chưa có evidence sửa/đối soát đủ 30. Trạng thái incident vì vậy là *giảm tác động, phục hồi một phần*, không được kết thúc chỉ vì dashboard 5xx và CPU xanh. Một SLI nghiệp vụ đúng phải tiếp tục báo phần bad đã xảy ra; chính sách SLO xác định khi nào mở lại release, không được xóa dữ liệu lịch sử để “reset” ngân sách.

## P13.C02.L03 — Timeline, nguyên nhân đóng góp và hành động sau sự cố

Timeline trong `timeline.csv` tách observation, giả định, đề xuất thao tác và verification còn cần làm. Cùng một câu “rollback xong” có thể có ba timestamp: lệnh hoàn tất, request mới đúng, dữ liệu cũ được sửa. Postmortem không ép ba mốc đó thành một. Khi điều tra sau giảm tác động, hỏi vì sao một thay đổi đổi đơn vị lọt qua: phép thử nào thiếu, canary gate chỉ nhìn status nào, telemetry có dấu hiệu gì nhưng không có cảnh báo, ai có quyền nâng traffic, và dữ liệu nào đáng lẽ được đối soát trước khi ghi. Giả thuyết root cause là adapter v2 đổi cents thành đơn vị nhỏ hơn; cần tái hiện trên input cụ thể và so cả diff/config trước khi ghi là xác nhận. Các điều kiện đóng góp có thể gồm test chỉ xác nhận 200, thiếu SLI số tiền, không có stop rule cho canary 10%; đó là lỗ hổng hệ thống cần khắc phục, không là lời buộc tội cá nhân.

Action item phải có chủ sở hữu, thời hạn và phép kiểm: (1) test âm cho 4.100 cents và kiểm dữ liệu lưu; (2) canary gate tính tỷ lệ sai nghiệp vụ theo release với mẫu số và missing-data policy; (3) runbook chặn mọi v2 writer và đối soát toàn bộ order ID; (4) diễn tập rollback app **và** kiểm sửa dữ liệu. “Cẩn thận hơn” không kiểm chứng được. Incident chỉ được đóng khi người phụ trách dữ liệu xác nhận phạm vi bản ghi, kế hoạch/sửa chữa, hậu điều kiện và thông báo cho người bị ảnh hưởng theo quy trình. Một postmortem không phải tài liệu để tìm người chịu lỗi; nó là hồ sơ bằng chứng và các thay đổi giảm xác suất hoặc tác động của lần sau.

### Bài tập C13.4

Tính tỷ lệ sai của v1, v2 và toàn canary window. Một người kết luận “DB chậm là root cause” vì có vài request chậm; người khác kết luận “DNS sai” vì khách hàng báo lỗi. Dữ liệu nào chống lại hai kết luận ấy, dữ liệu nào còn thiếu? Hãy đề xuất thứ tự ba phép kiểm ít gây tác động nhất.

### Bài tập C13.5

Sau 10:16, dashboard HTTP 5xx về 0, v1 ghi đơn mới đúng, nhưng 30 bản ghi v2 vẫn chờ đối soát. IC có được đánh dấu incident `resolved` và mở lại v2 không? Phân biệt mitigation, phục hồi request mới, khôi phục dữ liệu và các điều kiện cho từng quyết định.

### Bài tập C13.6

So sánh rollback ứng dụng, tắt feature flag và failover trong fixture. Nêu tiền điều kiện và một hậu điều kiện có thể đo cho mỗi lựa chọn; nếu dữ kiện thiếu thì ghi rõ không thể chọn an toàn.
