# P13.C04 — Hiệu năng, capacity và thử giới hạn

**Mọi số liệu trong `load.csv` là fixture tính toán giả định, không phải benchmark đã chạy.** Mô hình trung tâm: request đến, chờ, dùng tài nguyên rồi hoàn tất hoặc bị từ chối; capacity là mức tải giữ được SLO và khả năng phục hồi với biên an toàn đã kiểm, không phải một giá trị CPU.

## P13.C04.L01 — Workload: thời gian, số request và số việc cùng tồn tại

Một request có **latency** từ điểm người dùng bắt đầu đo tới kết quả họ nhận; một service có **throughput** là số request hoàn tất mỗi giây, còn **arrival/offered rate** là số request đi vào mỗi giây. Khi hàng đợi tăng, hai rate này khác nhau. **Concurrency** là số request đang ở trong hệ thống, gồm đang chờ và đang phục vụ; utilization là phần tài nguyên bận theo một định nghĩa quan sát cụ thể. Một CPU 70% không cho biết thread đang đợi DB, khóa, đĩa, network hay một shard nóng. Cần đo cùng cửa sổ và cùng population; trung bình latency có thể ổn dù p95/p99 vi phạm mục tiêu của một nhóm người dùng.

Trong fixture, mỗi pha dài 60 giây và không có retry, reject hay timeout ẩn. Pha A nhận và hoàn tất 100 request/s, latency trung bình 0,120 s, p95 0,180 s. Pha B nhận và hoàn tất 160 request/s, trung bình 0,250 s, p95 0,520 s. Nếu hai pha đã ổn định và số vào bằng số ra, Little's Law cho số request trung bình trong hệ thống **L = λW**: A là 100 request/s × 0,120 s = 12 request; B là 160 × 0,250 = 40 request. `L` không phải số thread hay CPU core; nó gồm cả chờ. Cùng định nghĩa “vào hệ thống” và “rời hệ thống” phải áp cho λ, W và L. Từ hai con số này không suy được phân bố độ trễ hay bottleneck; dữ liệu p95 và counter tài nguyên vẫn cần thiết.

Pha C nhận 220/s nhưng chỉ hoàn tất 180/s trong 60 giây. Nếu không từ chối, timeout, hủy hoặc retry ẩn và cùng ranh giới đo, **số request chưa hoàn tất** tăng `(220−180)×60 = 2.400 request`. `outstanding_delta` là chênh lệch tổng request đang chờ **và** đang xử lý, không phải phép đo riêng độ dài queue. Hệ thống chưa ổn định: không lấy 220×0,550 để gọi là concurrency trung bình theo Little's Law; 0,550 s chỉ đo trên nhóm đã hoàn tất và bỏ lại các request chưa hoàn tất. Ngay cả 180×0,550 cũng không tự cho tổng request đang có khi outstanding thay đổi. Phải đo riêng độ dài queue đầu/cuối, số in-flight, drop, timeout và retry; nếu một counter thiếu, số 2.400 chỉ là hệ quả **có điều kiện** của fixture.

## P13.C04.L02 — Từ dấu hiệu bão hòa đến quyết định capacity

Ở A→B, CPU giả định tăng 45%→65% nhưng p95 từ 180→520 ms; DB wait p95 từ 40→110 ms. Ở C, CPU chỉ 70% trong khi DB wait p95 300 ms, p95 request 1.800 ms và số chưa hoàn tất tăng. Tương quan cho thấy cần kiểm tra DB/connection pool và queue trước khi thêm replica; không chứng minh DB là root cause vì client mix, lock, hot key hoặc đo sai cũng có thể tạo dấu hiệu giống vậy. CPU phải được đọc kèm quota/throttling, per-core skew, run queue và thời gian chờ I/O. Memory phải phân biệt RSS/page cache, reclaim, OOM và GC; I/O cần độ trễ, queue depth, throughput; network cần loss/retransmit, RTT và connection errors. Một graph CPU thấp là một observation, không phải chứng thư còn capacity.

Capacity forecast bắt đầu từ nhu cầu và hậu điều kiện. Nếu peak hiện tại là 160 request/s và dự báo tăng 25%, peak mới là **200 request/s**. Fixture chỉ có pha B ổn định 160/s; pha C 220/s có số request chưa hoàn tất tăng. Vì vậy không thể nội suy rằng 200/s đạt SLO hoặc suy ra cần đúng 1,25 lần số replica. Nếu SLO giả định là p95 ≤600 ms và error rate <0,1% tại peak, B qua được điều kiện latency trong fixture, nhưng chưa có số liệu error rate và độ dài chạy nên cả SLO chưa được chứng minh. C cần stop vì số chưa hoàn tất tăng và p95. Biên an toàn phải xét mất một instance, rollout, autoscaler trễ, burst, skew tenant và shared dependency. Tăng replica có chi phí và có thể đẩy thêm tải vào DB; đặt queue hữu hạn và shed tải có kiểm soát có thể giữ phần request được phục vụ đúng hạn, nhưng sẽ ảnh hưởng availability SLI. Quyết định cần xem cả ngân sách lỗi P13.C01 và chi phí, không tối ưu p95 bằng cách lặng lẽ bỏ request khỏi mẫu số.

## P13.C04.L03 — Thiết kế thí nghiệm để biết giới hạn

Một **load test** chạy mức tải gần dự báo để kiểm SLO; **stress test** tăng vượt vùng dự kiến để tìm ngưỡng bão hòa và hành vi từ chối; **soak test** giữ tải đủ lâu để lộ leak, tích queue, hết connection/disk hay drift chậm. Tên test không tự chứng minh kết quả: dữ liệu phải có traffic mix, kích thước payload, think time hoặc arrival model, trạng thái cache, phiên bản artifact, topology, warm-up, thời lượng và điểm đo phía client. Một máy phát tải bão hòa có thể tạo số liệu giả; đo cả generator. Histogram p95 phải giữ population và bucket phù hợp; không lấy trung bình p95 giữa các pod như p95 toàn fleet.

Đề xuất thí nghiệm **chưa chạy** cho peak 200/s: dùng môi trường cô lập với cấu hình và dữ liệu đại diện nhưng không chứa dữ liệu khách hàng; kiểm baseline 160/s, tăng từng bậc 180→200→220/s và giữ mỗi bậc đủ lâu để thấy queue đầu/cuối. Ghi offered, accepted, completed, rejected, timed-out, retries, latency client p50/p95/p99, in-flight, queue, CPU quota/throttle, memory/GC, disk/network và DB wait theo cùng cửa sổ. Stop ngay nếu p95 vượt 600 ms hai cửa sổ liên tiếp, backlog tăng quá giới hạn định trước, dữ liệu sai, hoặc generator bão hòa; giữ khả năng phục hồi trước khi tăng tiếp. Sau giảm tải, xác nhận queue rút, request mới đúng và không có job nền tiếp tục gây tải. Chỉ khi dữ liệu thật đạt hậu điều kiện và thử thêm mất một replica mới chốt mức capacity. Không failure-inject production để “cho chắc” nếu chưa định blast radius và đường quay lui.

### Bài tập C13.10

Từ A và B tính concurrency trung bình theo Little's Law. Ở C tính mức tăng số request chưa hoàn tất trong 60 giây, rồi giải thích vì sao 220×0,550 không là concurrency đã chứng minh. Có thể kết luận riêng độ dài queue tăng bao nhiêu không? Nêu hai counter có thể bác bỏ giả định của phép tính.

### Bài tập C13.11

Một người nói “CPU 70% nên chỉ cần thêm 25% replica để chịu peak 200/s”. Dựa vào dữ liệu A–C, chỉ ra ba lỗ hổng trong suy luận, một giả thuyết bottleneck và phép đo có thể bác bỏ nó. Kết luận có được triển khai 200/s chưa?

### Bài tập C13.12

Thiết kế một phép thử capacity cho peak 200/s với tiêu chí dừng, hậu kiểm và thông tin cần ghi để tái lập. Phân biệt load, stress và soak; nêu một ví dụ khi kết quả PASS ở môi trường thử vẫn chưa đủ để công bố production capacity.
