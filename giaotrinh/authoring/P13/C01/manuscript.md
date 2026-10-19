# P13.C01 — SLI, SLO và ngân sách lỗi

**Bản thảo nội dung A1; dữ liệu dưới đây là giả định để học, không phải phép đo production.**

## P13.C01.L01 — Định nghĩa phép đo từ trải nghiệm

Một API trả HTTP 200 có thể vẫn gây mất tiền nếu giá trị đơn hàng sai; ngược lại HTTP 503 ở một tác vụ nền không thuộc hành trình mua hàng có thể không làm hỏng thao tác khách hàng đang quan tâm. Vì thế trước khi chọn biểu đồ, ta viết hợp đồng sự kiện: ai là người dùng, hành động nào quan trọng, điểm đo ở client, edge hay server, và cách xử lý timeout, retry, cache, request trùng, bot, dữ liệu lỗi. **SLI** là phép đo có định nghĩa đó, không phải tên của một metric có sẵn. Availability thường là tỷ lệ thao tác hợp lệ thành công; latency là tỷ lệ thao tác hợp lệ hoàn tất dưới ngưỡng thời gian. Error rate là phần bù của một SLI nhị phân nếu định nghĩa “bad” bao trùm mọi trường hợp không good. Throughput đo lượng công việc trên đơn vị thời gian; nó mô tả tải, không tự là chất lượng phục vụ.

Với request-based SLI, tập `valid` gồm các lần thử thuộc phạm vi đã công bố; `good` là tập con thỏa cả kết quả nghiệp vụ và ngưỡng thời gian nếu SLI gộp hai điều kiện. `bad = valid - good`. Tỷ lệ good là `good/valid`, có đơn vị 1; không cộng các tỷ lệ của từng Pod rồi chia đều khi lưu lượng khác nhau. Chỉ loại request có lý do sản phẩm rõ (ví dụ endpoint nội bộ hoặc đầu vào bị từ chối đúng theo hợp đồng), ghi riêng số bị loại. Timeout phía client sau khi request rời máy thường phải được tính là bad nếu SLI hứa đáp ứng cho lần thử ấy, ngay cả khi server không có log; đo chỉ ở server có thể làm mẫu số co lại trong lúc mạng hỏng. Retry chỉ là good của một *lần thử* nếu SLI đo lần thử; nếu SLI đo một hành trình người dùng, phải gom các lần thử thành một thao tác và công bố quy tắc gom. Không đổi mẫu số sau sự cố để làm SLI đẹp hơn.

Time-based SLI chia lịch thành các khoảng đo (chẳng hạn phút) và xét phút nào thỏa điều kiện phục vụ. Nó hữu ích khi mục tiêu là thời gian sẵn sàng, nhưng một phút có một request được cân ngang phút có mười nghìn request. Request-based SLI cân theo số thao tác, nên phản ánh tác động tại đỉnh tải tốt hơn nhưng im lặng khi không có request. Hai cách không đổi chéo bằng một phép nhân tùy tiện; nếu dùng probe tổng hợp, giữ nó thành luồng đo riêng và nói rõ phần hành vi người dùng mà probe không kiểm được.

## P13.C01.L02 — Mục tiêu, cửa sổ và ngân sách

**SLO** là mục tiêu định lượng áp lên SLI, population và cửa sổ: ví dụ “ít nhất 99,9% request checkout hợp lệ trong 30 ngày gần nhất trả kết quả đúng trong 500 ms, đo tại edge”. **SLA** là thỏa thuận với bên nhận dịch vụ có hậu quả khi vi phạm; chỉ có SLO nội bộ chưa tự thành SLA. SLO cũng không chứng minh mỗi request đúng: một mục tiêu 99,9% vẫn cho phép một phần thao tác lỗi. Rolling 30 ngày tại thời điểm `t` dùng `(t−30 ngày, t]` và dịch mỗi khi đánh giá; tháng lịch cố định đóng ở ranh giới tháng. Cùng số lượng bad nhưng budget còn lại có thể khác vì population, cửa sổ và lượng request khác. Cần chốt múi giờ, độ trễ nạp dữ liệu và quy tắc event sát biên trước khi so số liệu.

Với SLO dạng tỷ lệ `S` và `V` valid events trong cửa sổ, ngân sách lý thuyết là `B=(1−S)×V` bad events; đã dùng `E=V−G`, còn `B−E`. Nếu `B` không nguyên, chính sách làm tròn phải được định nghĩa trước, không tự nâng trần để nới mục tiêu. Với một cửa sổ có ít lưu lượng, tỷ lệ có phương sai lớn: một bad trong 10 request là 10% lỗi, không đủ để suy cả hệ thống hỏng liên tục. Với SLO theo thời gian, ngân sách là `(1−S)×độ dài cửa sổ` theo đơn vị thời gian, không lấy số request làm mẫu số. Với latency SLI, bad là request quá ngưỡng (hoặc timeout theo hợp đồng), không lấy trung bình các p95 rời rạc làm phần trăm good toàn hệ thống.

`monthly.csv` là **toàn bộ dữ liệu giả định** của rolling 30 ngày tại một thời điểm: 988.000 valid/511 bad trước giờ cuối, 12.000 valid/189 bad ở giờ cuối. Tổng `V=1.000.000`, `E=700`, `G=999.300`, SLI `99,93%`. Với `S=99,9%`, `B=1.000` bad và còn `300` bad. Phần giờ cuối khớp 12 dòng năm phút trong `five_minute.csv`; con số này chứng minh phép tính trên fixture, không cho biết lưu lượng tháng sau. Nếu có request hoàn toàn mất khỏi instrumentation, các con số vẫn có thể đẹp một cách sai lệch.

## P13.C01.L03 — Tốc độ tiêu ngân sách và quyết định

Trong một cửa sổ ngắn, `error_ratio = bad/valid`. **Burn rate** của SLO request-based là `error_ratio/(1−S)`, không có đơn vị. Burn 1 nghĩa tỷ lệ lỗi hiện tại bằng phần lỗi được phép bình quân; nó không nói budget hiện đã cạn. Giờ cuối trong fixture có `189/12.000 = 1,575%` lỗi, burn `15,75`; năm phút cuối có `60/1.000 = 6%`, burn `60`. Cảnh báo 1 giờ/5 phút với ngưỡng burn `14,4` sẽ thỏa cả hai phía (`15,75 > 14,4` và `60 > 14,4`). Đây là một tín hiệu can thiệp nhanh, **không phải** bằng chứng duy nhất của nguyên nhân hay xác suất tháng sẽ vi phạm SLO. Công thức “burn × độ dài cửa sổ / 30 ngày” ước lượng tỷ lệ ngân sách thời gian bị tiêu nếu traffic và error ratio đại diện, ổn định; với request budget và traffic biến thiên, phải dùng bad events thật trên toàn population thay cho ước lượng thời gian ấy.

Ví dụ PromQL sau giả sử ứng dụng xuất hai counter riêng `sli_valid_total` và `sli_bad_total`, cùng nhãn `service` và `route`, counter bad tăng đúng một lần cho mỗi valid bad. Đây là **mẫu biểu thức chưa chạy trên Prometheus**, không phải output thật:

```promql
(
  sum(rate(sli_bad_total{service="checkout",route="write"}[1h]))
  /
  sum(rate(sli_valid_total{service="checkout",route="write"}[1h]))
  > (14.4 * 0.001)
)
and
(
  sum(rate(sli_bad_total{service="checkout",route="write"}[5m]))
  /
  sum(rate(sli_valid_total{service="checkout",route="write"}[5m]))
  > (14.4 * 0.001)
)
```

`rate()` phải áp trên từng counter trước `sum` để nhận ra reset từng instance. Hai cửa sổ dài/ngắn cùng vượt ngưỡng giúp xác nhận lỗi còn đang tiếp diễn và giảm thời gian alert treo sau khi hồi phục. Trên Prometheus thật, cửa sổ phải có đủ sample, vector matching/labels phải đúng, mẫu số dương và target phải còn được scrape; thiếu chuỗi hoặc mất scrape là trạng thái đo **unknown**, không là lỗi bằng 0. Cần cảnh báo độc lập cho tính đầy đủ telemetry và kiểm từ phía client. Không tính trung bình tỷ lệ của các replica; lấy tổng tốc độ bad chia tổng tốc độ valid cùng population. SLO 6h/30m là một nhánh alert khác, không được kết luận từ fixture chỉ có 1h.

Một page burn nhanh và chỉ còn 300 bad làm việc mở rộng canary không hợp lý cho tới khi phân biệt lỗi thật và lỗi đo. Người trực có thể dừng tăng traffic, so request/dữ liệu theo release, giảm tác động bằng rollback hoặc flag nếu hậu điều kiện đã biết. Quyết định tạm dừng release là chính sách sản phẩm/SRE đã thống nhất, không phải tính năng tự động của phương trình. Khi ít lưu lượng, một bad có thể tạo burn rất lớn; đánh giá giá trị giao dịch, probe riêng, số sự kiện và độ tin cậy dữ liệu trước khi đánh thức cả đội. Khi không có valid event, tỷ lệ không xác định chứ không bằng 100% good.

### Bài tập C13.1

Trong fixture 30 ngày, giả sử chỉ giữ 11 dòng đầu của `five_minute.csv` vì dòng cuối chưa được scrape, nhưng monthly summary vẫn được dashboard giữ nguyên. Có được báo “không còn burn” hay không? Hãy nêu phép đối chiếu, trạng thái đo và quyết định trước khi tiếp tục canary.

### Bài tập C13.2

Một API có hai replica: A xử lý 900 valid/9 bad, B xử lý 100 valid/10 bad trong cùng cửa sổ. Tính tỷ lệ lỗi toàn dịch vụ và giải thích vì sao trung bình cộng 1% và 10% là sai. Nếu SLO 99%, còn ngân sách trong cửa sổ 1.000 valid là bao nhiêu bad?

### Bài tập C13.3

Với năm phút cuối trong fixture, tính burn và so ngưỡng 14,4. Nếu 1 giờ trước đó chỉ có 12.000 valid/100 bad (thay cho 189), alert hai cửa sổ có page không? Giải thích vì sao không thể tự suy nhánh 6h/30m.
