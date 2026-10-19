# Hợp đồng đầu ra capstone — P15.C03

**Trạng thái:** quyết định phạm vi của Reviewer ngày 19-10-2026; đây là đặc tả cho A2, chưa phải kết quả thực nghiệm. Bài tập có bản **cục bộ, không tốn phí** (container/Kind hoặc process và filesystem tạm tùy công cụ sẵn có). AWS là nhánh mở rộng có điều kiện, tuyệt đối không là điều kiện để đạt capstone và không tạo tài nguyên có phí tự động.

## Đối tượng và chuỗi công việc

Một dịch vụ API nhỏ có ít nhất một thao tác ghi và đọc lại bản ghi bền vững. Một thay đổi từ commit `S1` sang `S2` làm thay đổi artifact và một ranh giới vận hành đã biết. `change_id` theo đợt thay đổi từ commit, build, triển khai đến sự cố và quyết định phục hồi; mỗi lần triển khai hoặc rollback có `deployment_revision` riêng. Mỗi request thử có `request_id` riêng, chỉ xuất hiện từ lúc phát request và trong telemetry liên quan. Ledger nối request về revision đang phục vụ bằng log, trace hoặc bản ghi tương quan có thời điểm; không gán một request ID cho build hoặc dùng chung một ID cho mọi request. Không mượn output giả định của các chương trước làm kết quả chạy thật.

| Bài | Đầu ra phải nộp | Phép kiểm bắt buộc | Tiêu chuẩn đạt |
| --- | --- | --- | --- |
| `P15.C03.L01` Chuẩn bị | `change_id`, commit/ref, dependency lock, artifact digest, cấu hình/IaC được duyệt, sơ đồ đường request và trust boundary, bản sao dữ liệu trước thay đổi. | Tính lại digest từ byte; kiểm config/schema và dữ liệu đọc được; ghi phiên bản tool, thời điểm, host/namespace. | Artifact có identity bất biến và bản sao có phép thử restore nhỏ; thiếu một mắt xích thì chưa deploy. |
| `P15.C03.L02` Thực thi | Manifest/plan diff, test gate, `deployment_revision`, rollout record, các request ghi và đọc lại với `request_id` riêng, metric/log/trace tương quan. | So expected/actual ở từng chặng DNS/TCP/TLS/HTTP hoặc đường cục bộ tương đương; đối chiếu request ID với revision đang phục vụ; kiểm readiness riêng với request và dữ liệu. | Bản mới phục vụ đúng request, có bằng chứng dữ liệu, không chỉ status xanh. |
| `P15.C03.L03` Sự cố và phục hồi | Một lỗi được tiêm trong phạm vi fixture, quyết định stop/rollback gắn `change_id`, revision trước/sau và request kiểm tra mới, hậu trạng thái của artifact, data, quyền. | Chạy ca âm tái lập; trước hành động lưu evidence; sau hành động kiểm artifact đang chạy, bản ghi cũ/mới và khả năng đọc. | Rollback ứng dụng không được ghi là phục hồi dữ liệu; restore có kiểm nội dung và giới hạn RPO/RTO đo từ timeline. |
| `P15.C03.L04` Kiểm toán | `evidence_ledger` có đường dẫn, hash, thời điểm, môi trường, `change_id`, từng `deployment_revision`, các `request_id` tương ứng, kết quả PASS/FAIL/SKIP, giải thích thiếu dữ liệu, SLI numerator/denominator và quyết định vận hành. | Reviewer lấy mẫu tái chạy phép tính SLO/digest, mở từng artifact, đối chiếu quan hệ change–revision–request và kiểm tra các mục SKIP. | Không có PASS không có bằng chứng; mọi FAIL có stop rule hoặc mitigation đã thử; giới hạn sản xuất ghi rõ. |

## Bằng chứng tối thiểu và phép thử âm

Ledger phải có chuỗi thay đổi `change_id → commit → build input → digest → deployment_revision → running instance`; với **mỗi** request, ghi `request_id → revision đang phục vụ → data record → telemetry`. Sự cố, rollback hoặc restore nối về `change_id` và revision trước/sau; request hậu kiểm có ID mới. Quan hệ request–revision phải có bằng chứng tương quan và thời điểm, không suy chỉ từ tag hay trạng thái Ready. Với từng mắt xích ghi nguồn thật (file, log, command output, timestamp, checksum) hoặc `SKIP` kèm nguyên nhân. A2 thiết kế ít nhất ba ca âm: artifact/tag sai digest; triển khai Ready nhưng request ghi/đọc sai; rollback app thành công nhưng dữ liệu/schema không tương thích. Một ca về thiếu quyền hoặc secret bị lộ phải có quan sát và biện pháp giảm thiểu, không đưa secret thật vào ledger.

Một phép đo SLI phải khai báo population, cửa sổ, numerator, denominator và loại request bị loại. SLO/burn phải tính được từ dataset nộp kèm. Metric/log/trace thiếu do pipeline lỗi là `UNKNOWN`, không là healthy. Tải và cost được ghi theo đơn vị, giả định, Region/ngày nếu có AWS; bản local dùng tài nguyên máy đo được và không suy thành hóa đơn cloud.

## Điều kiện SKIP và dừng

- **SKIP hợp lệ:** Docker/Kind/Go/Terraform/Ansible hoặc OTel backend không khả dụng; quyền mạng/filesystem không cho phép; AWS chưa cấp ngân sách. Ghi bài bị ảnh hưởng, bằng chứng kiểm môi trường và thay bằng fixture cục bộ tương đương nếu còn chứng minh được năng lực. SKIP không biến thành PASS.
- **Dừng ngay:** thao tác có thể chạm dữ liệu/lab thật; plan có `replace/destroy` chưa có backup và duyệt; canary vượt ngưỡng SLO đã định; permission/secret sai; restore thử không đạt; evidence ledger thiếu identity artifact hoặc không xác định được hậu trạng thái dữ liệu.
- **Không đạt capstone:** chỉ có sơ đồ production; chỉ `kubectl apply`/`helm upgrade`/CI xanh; không có phép thử request và dữ liệu; không thể tái lập claim SLO hoặc rollback; ghi output giả định như đã chạy thật.

Reviewer duyệt rubric, ngưỡng SLO và blast radius của fixture trước khi A2 triển khai. Bản cục bộ là đường học chính; một nhánh AWS hoặc multi-cloud chỉ được thêm nếu có nguồn phiên bản và chi phí/quyền rõ, không thay hợp đồng chứng cứ trên.
