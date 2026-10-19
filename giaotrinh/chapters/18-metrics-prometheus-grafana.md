# Chương 18. Prometheus và Grafana: từ phép đo tới kết luận

Ở Chương 16, HPA dùng CPU utilization tính từ CPU usage và request. Đó chỉ là một tín hiệu điều khiển. Người vận hành cần biết phép đo được tạo ở đâu, có tới nơi lưu trữ không, câu truy vấn biến mẫu rời rạc thành đại lượng nào và lúc nào dữ liệu không còn đủ để kết luận. Một biểu đồ đẹp không sửa được một lần scrape thất bại hay một nhãn sai.

## 18.1. Một mẫu số đi qua những ranh giới nào?

Ứng dụng hoặc exporter đo một sự kiện rồi giữ giá trị theo tên metric và tập nhãn. Target công bố snapshot qua HTTP; Prometheus chọn target bằng cấu hình hoặc service discovery, định kỳ scrape endpoint và gắn timestamp cho mẫu nhận được. Metric `up` do Prometheus tạo cho kết quả scrape: 1 khi scrape thành công, 0 khi thất bại với target vẫn còn trong danh sách. `up=1` chỉ xác nhận việc lấy metric, không chứng minh request nghiệp vụ qua Gateway thành công. Target bị loại khỏi discovery là trường hợp khác với target còn được theo dõi nhưng `up=0`.

Mỗi tổ hợp tên metric và giá trị nhãn tạo một time series. Gauge có thể tăng hoặc giảm theo trạng thái hiện tại, như số request đang chạy. Counter cộng dồn và có thể về giá trị nhỏ khi tiến trình khởi động lại; không lấy một giá trị counter đơn lẻ làm tốc độ. Classic histogram gồm các bucket tích lũy theo ngưỡng `le`, `_sum` và `_count`. Một request nằm trong mọi bucket có ngưỡng lớn hơn hoặc bằng thời gian của nó; bucket `+Inf` phải bằng `_count`. Summary có thể xuất quantile do client tính; không thể cộng trực tiếp các quantile của nhiều target để có quantile toàn hệ thống. Chương này chỉ tính p95 từ classic histogram, không trộn với native histogram.

Prometheus lưu mẫu thành các chuỗi thời gian trên đĩa cục bộ với write-ahead log và block; thời hạn lưu do cấu hình retention chi phối. Retention không biến dữ liệu thành backup: lỗi đĩa hoặc xóa TSDB vẫn cần kế hoạch sao lưu/độ sẵn sàng riêng. Recording rule định kỳ lưu kết quả biểu thức thành chuỗi mới để giảm chi phí truy vấn lặp lại; alerting rule đánh giá điều kiện và chuyển cảnh báo sang trạng thái chờ/phát theo `for`. Rule cũng chịu ảnh hưởng của dữ liệu thiếu và thứ tự đánh giá, không xác nhận nguyên nhân gốc. Grafana truy vấn Prometheus qua data source rồi vẽ panel; nó không phải nguồn gốc của phép đo.

Chọn nhãn để phân nhóm hữu ích như `service`, `route`, `status_class`; tránh `request_id` hoặc user ID thay đổi theo từng request. Nếu 50.000 request tạo 50.000 giá trị `request_id` cho một metric, riêng chiều nhãn đó có thể tạo khoảng 50.000 chuỗi thay vì vài chuỗi theo status; nhân thêm instance, method và bucket còn tăng số chuỗi, bộ nhớ và chi phí truy vấn. Đây là phép đếm tổ hợp giả định, không phải benchmark Prometheus. Không đưa secret hay định danh người dùng vào nhãn chỉ để lọc dashboard.

## 18.2. Cửa sổ, tốc độ và tỷ lệ lỗi

Dữ liệu CSV dưới đây là ví dụ tính toán giả định, không phải output scrape trên cluster. Hai instance `a` và `b` được lấy mẫu ở giây 0, 60, 120, 180; trong ví dụ, tên instance được gắn khi scrape thay cho địa chỉ target mặc định. `ok` và `err` là hai counter HTTP; bốn cột `le_*` là bucket tích lũy của thời gian request tính bằng giây; `cpu_s` là CPU time tích lũy. Để số dễ tự kiểm, từng phút mỗi instance xử lý 54 request 2xx và 6 request 5xx; số đếm bucket tăng 20, 45, 58, 60. Mọi request của bảng thuộc một trong hai status class và đi vào histogram. Trong vận hành, hãy xác nhận phạm vi instrument trước khi lấy histogram count làm mẫu số HTTP.

{{code:examples/metrics-ch18.csv}}

Tại giây 180, biểu thức `rate(http_requests_total[3m])` dùng mẫu trong khoảng `(0,180]`, tức giây 60, 120, 180 theo quy tắc range selector. Trên chuỗi đều và không reset này, `rate` của 5xx ở mỗi instance là `(23−11)/120 = 0,1` và `(28−16)/120 = 0,1` request/giây. Cộng theo instance cho 0,2 lỗi/giây. Tương tự tổng request mỗi instance là `(280−160)/120 = 1` request/giây, cả hai là 2 request/giây; tỷ lệ lỗi bằng 0,2/2 = 10%. `increase(counter[3m])` là `rate` nhân 180 giây, có thể cho số lẻ vì Prometheus ngoại suy tới biên cửa sổ. Không đọc nó như hiệu thô 120 giây giữa hai mẫu đầu/cuối. Nếu cần kiểm phép đếm thô của cả 0→180, tổng lỗi tăng 36 trên tổng request tăng 360, cũng là 10% trong bộ dữ liệu tuyến tính này.

Trong hệ có nhãn `job="atlas"` được gắn lúc scrape, các biểu thức sau gom theo status và instance sau khi tính tốc độ riêng từng chuỗi:

{{code:examples/metrics-ch18.promql}}

Phép cộng trước `rate` là sai khi hai tiến trình reset counter khác lúc: reset của một instance có thể bị tổng của instance khác che khuất. `rate` và `increase` nhận biết bước giảm counter như reset trong phạm vi mẫu, nhưng không thể cứu cửa sổ quá ít mẫu hoặc instrument sai. Khi chọn status class, tử số và mẫu số phải cùng service, route, loại request và cửa sổ; một truy vấn thiếu nhãn lọc có thể cho tỷ lệ số học đúng mà sai đối tượng.

## 18.3. Histogram và một p95 có giới hạn

Ở `(0,180]`, tổng tốc độ bucket của hai instance lần lượt là 0,667; 1,5; 1,933; 2 request/giây cho ngưỡng 0,1; 0,5; 1; `+Inf`. Vì p95 của 2 request/giây nằm tại 1,9 request/giây, nó thuộc bucket `(0,5;1]`. Với giả định nội suy đều trong bucket của `histogram_quantile`, kết quả là `0,5 + (1,9−1,5)/(1,933…−1,5) × 0,5 ≈ 0,962 giây`. Có thể kiểm bằng 120 giây quan sát: tổng 240 request, 180 ở ≤0,5 giây và 232 ở ≤1 giây; vị trí 228 cho `0,5+(228−180)/(232−180)×0,5 = 0,9615` giây. Đây là ước lượng từ ranh giới bucket, không phải p95 chính xác của từng request; bucket rộng làm sai số nội suy lớn. Giữ `le` khi `sum` bucket; bỏ nó làm mất biên để tính quantile.

CPU time tăng 24 giây trên hai instance trong 120 giây mẫu, tức 0,4 lõi trung bình; con số ấy không loại trừ chờ I/O, lock, backend, mạng hoặc một nhóm request chậm. p95 tăng cùng lúc CPU bình thường là dấu hiệu cần điều tra latency theo route và upstream; không được gán nguyên nhân chỉ bằng hai đường biểu đồ.

Snapshot exposition giả định của target `a` ở giây 180 dưới đây có cú pháp metric, bucket và count nhất quán với dòng `a` cuối CSV. Endpoint ứng dụng không tự xuất nhãn `instance` hoặc `job`: Prometheus gắn chúng theo target khi scrape; `up` cũng do Prometheus tạo. Snapshot không có các mẫu quá khứ nên riêng nó không thể trả lời truy vấn `rate`.

{{code:examples/metrics-ch18.prom}}

## 18.4. Một dashboard gặp dữ liệu thiếu

Tình huống giả định: sau một thay đổi nhãn, dashboard báo p95 tăng, CPU giữ quanh 0,4 lõi, target `b` có `up=0` ở giây 240 và số series tăng nhanh. Trước hết khóa cùng data source, time range, step, filter `service/route` và múi giờ trong Grafana; panel vẽ `rate(...[3m])` ở các mốc đánh giá khác nhau sẽ nhìn những cửa sổ khác nhau. Xem Explore hoặc truy vấn thô để so số mẫu, nhãn và series tham gia, rồi kiểm tra target discovery, endpoint `/metrics`, kết quả scrape và log exporter. Nếu `b` vẫn được discovery và scrape lỗi, `up{instance="b"}=0`; sau failed scrape, series do `b` xuất có thể stale và biến mất khỏi instant vector. Range vector có thể còn mẫu cũ một thời gian. Tỷ lệ lỗi hoặc p95 chỉ từ `a` có thể trông tốt lên dù người dùng của `b` vẫn lỗi. Không biến “không có mẫu” thành 0 request hay 0 latency.

Song song, xem metric/label nào tạo nhiều tổ hợp mới; nếu có `request_id`, bỏ nhãn ấy ở điểm instrument, giới hạn nhãn được phép và đánh giá ngân sách chuỗi trước khi triển khai lại. Sau đó xác minh cả hai target scrape được, số series ổn định và request nghiệp vụ qua đúng Route; xem latency/error theo route và so với log/trace của upstream để tìm nguyên nhân p95. Tăng retention hay đổi panel không sửa được explosion ở nguồn. Grafana hiển thị câu trả lời của truy vấn cho cửa sổ đã chọn, nên một panel “No data” là tín hiệu kiểm tra scrape, selector và range, không phải bằng chứng dịch vụ khỏe hoặc chết.

Với alert, tách “không lấy được metric” (`up`, target discovery/absence) khỏi “ứng dụng có lỗi” (tỷ lệ 5xx và lưu lượng tối thiểu). Recording rule có thể lưu tốc độ đã tổng hợp theo service/route, nhưng tên và nhãn của rule phải giữ đúng phạm vi; nếu mất target, kết quả tổng hợp cũng thiếu. Một alert p95 nên có điều kiện lưu lượng và chất lượng dữ liệu, ngưỡng theo SLO đã xác định, thời gian `for` phù hợp; ví dụ này không ấn định SLO cho hệ thật.

## Bài tập

C18.1. Từ CSV, tại giây 180 hãy tính rate 5xx, tổng rate, tỷ lệ lỗi, CPU trung bình và p95 classic histogram cho hai instance. Nêu vì sao `increase(...[3m])` không nhất thiết bằng hiệu thô giữa mẫu đầu và cuối trong cửa sổ.

C18.2. Ở giây 240, `up{instance="b"}=0` nhưng panel lỗi 5xx giảm. Liệt kê các phép kiểm để phân biệt dịch vụ `b` hồi phục, `b` không được scrape và truy vấn bị lọc nhãn; chỉ rõ điều chưa thể kết luận từ `up`.

C18.3. Một thay đổi thêm `request_id` vào metric HTTP và Grafana báo chậm. Tính bậc số chuỗi nếu có 50.000 ID khác nhau, hai instance, hai status class và bốn bucket; đề xuất nhãn thay thế và cách kiểm chứng sau sửa. Giả sử mọi tổ hợp đều xuất hiện; giải thích vì sao tích này chỉ là ước lượng trần theo giả định.

C18.4. Một kỹ sư tính `rate(sum(http_requests_total)[3m:])` rồi lấy trung bình `p95` của hai Pod. Nêu hai lỗi cơ chế và truy vấn/quan sát phù hợp hơn. Nếu một Pod mất scrape, giới hạn của kết quả mới là gì?
