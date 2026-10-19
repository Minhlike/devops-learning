# Cây tri thức đề xuất — Cẩm nang ngành DevOps

**Trạng thái:** đề xuất A1 để Reviewer nghiệm thu; chưa thay bản thảo hoặc PDF.
**Cách đọc:** ID ổn định; cạnh `A → B` nghĩa học A trước B. `reviewed_draft` chỉ nói bản thảo đã qua review milestone, không xác nhận mọi claim hay lab. `needs_extension` là bài chưa có mục cũ trực tiếp; `planned_new` cần biên soạn và nguồn mới.
**Chủ chứng cứ:** `evidence_ownership.csv` gán một primary lesson cho từng claim/ví dụ/cặp đề–đáp án; `legacy_content_units.csv` gán chủ đoạn ở mục split; `legacy_migration.csv` ghi liên kết cũ–mới. Nguồn liệt kê trong JSON chỉ đến từ claim thuộc bài, không là xác nhận ngữ nghĩa mới.
**Phạm vi đã chốt:** Go là CLI DevOps nhỏ; UDP/IPv6/MTU ở mức chẩn đoán nền; AWS-first với nguyên lý cloud-neutral; capstone theo `capstone_contract.md` có bản local không phí.

Tổng: 15 Phần, 58 Chương, 178 Bài/Mục. Cấu trúc phản ánh ranh giới cơ chế và tiên quyết, không phải quota.

## Đồ thị tiên quyết đọc nhanh

Bản đầy đủ ở `knowledge_tree.json`: 244 cạnh bắt buộc, 8 cạnh hữu ích và 8 đường đào sâu. Chỉ cạnh bắt buộc tạo trật tự học; mọi cạnh đi từ bài xuất hiện trước tới bài xuất hiện sau. Các chuỗi minh họa dưới đây có thể bỏ qua nút trung gian; cạnh chính xác nằm trong JSON.

- `P01.C02.L03` (process/FD) → `P07.C01.L01` (namespace) → `P07.C03.L01` (container là lần chạy).
- `P03.C02.L03` (đường TCP/NAT) → `P08.C02.L01` (VPC route) → `P11.C04.L02` (Service dataplane áp dụng mạng gốc).
- `P04.C01.L03` (commit/ref) → `P06.C01.L01` (build input) → `P07.C02.L02` (OCI digest).
- `P11.C01.L02` (controller) + `P11.C03.L01` (CPU request/placement) + `P11.C03.L03` (resource metric) → `P11.C06.L01` (HPA); P12 Prometheus không là điều kiện vào.
- `P08.C04.L03` (data lifecycle) → `P09.C01.L01` (resource) → `P09.C02.L01` (state) → `P09.C04.L01` (replacement/data risk).
- `P12.C02.L03` (dashboard/missing data) → `P13.C01.L01` (SLI denominator) → `P13.C02.L01` (incident triage).

## P01 — Máy tính và tiến trình

**Câu hỏi:** Một dòng mã trở thành công việc có thể quan sát bằng cách nào?
**Mô hình:** Chương trình, tiến trình, luồng và tài nguyên là các thực thể khác nhau; thời gian là tổng của chạy, chờ và phối hợp.
**Tiên quyết:** Không; chỉ cần đọc được một đoạn mã và phép chia đơn vị.
**Ranh giới:** Chưa quản trị Linux hoặc container; chỉ dựng mô hình phần cứng và hệ điều hành.
**Năng lực ra:** Lần theo một lần chạy từ artifact tới PID, trạng thái và kết quả.
**Ngộ nhận cần sửa:** Tệp thực thi đang có trên đĩa tức là tiến trình đã đổi phiên bản.
**Chuyển tiếp:** Cho Linux, container, chẩn đoán hiệu năng và service lifecycle.

### P01.C01 — Công việc, thời gian và đường đi dữ liệu [mixed]

- **Đích học:** Phân tích một request thành tính toán, chờ và tác dụng phụ.
- **Mô hình nối bài:** CPU time, wall time và dữ liệu đi qua bộ nhớ/I/O không hoán đổi được.
- **Tiên quyết bắt buộc:** Không.
- **Ranh giới:** Linux counter cụ thể ở P02.C03.
- **Ngộ nhận:** CPU thấp chứng minh request không bị nghẽn.
- **Cách dạy:** Dùng timeline giả định rồi đặt phép đo phân biệt giả thuyết.
- **Đánh giá:** Tính lower bound latency và nêu đại lượng còn thiếu.
- **Nối tới:** P01.C02, P02.C03, P12.C01.
- **Nguồn cũ:** Ch02.
- **Cây bài:**
  - `P01.C01.L01` **Máy thực thi** [needs_extension; 0 mục cũ; 0 claim] — lõi logic, bộ nhớ, thiết bị và đồng hồ
  - `P01.C01.L02` **Đường thời gian** [needs_extension; 1 mục cũ; 0 claim] — running, runnable, blocked, wall time và CPU time
  - `P01.C01.L03` **Dữ liệu đi qua I/O** [needs_extension; 0 mục cũ; 0 claim] — buffer, cache, thiết bị và ranh giới bền vững

### P01.C02 — Chương trình, tiến trình và ranh giới nhân [reviewed_draft]

- **Đích học:** Lần theo một bản build đến hai tiến trình và kết quả từng nhánh.
- **Mô hình nối bài:** Tệp, process image, PID, descriptor và exit status là các đối tượng khác vòng đời.
- **Tiên quyết bắt buộc:** P01.C01.L02.
- **Ranh giới:** Quyền đường dẫn chi tiết ở P02.C02; service manager ở P02.C04.
- **Ngộ nhận:** Thay binary trên đĩa thay process đang chạy.
- **Cách dạy:** Đọc trace fork/execve thành công và lỗi, rồi đối chiếu trạng thái cha/con.
- **Đánh giá:** Dự đoán PID, return value, descriptor và hậu trạng thái.
- **Nối tới:** P02.C01, P02.C04, P03.C01, P05.C01, P05.C02, P07.C01.
- **Nguồn cũ:** Ch01.
- **Cây bài:**
  - `P01.C02.L01` **Ba dạng ứng dụng** [reviewed_draft; 1 mục cũ; 1 claim] — source, executable và process instance
  - `P01.C02.L02` **Tạo và thay process** [reviewed_draft; 1 mục cũ; 5 claim] — fork, execve, wait, exit và copy-on-write
  - `P01.C02.L03` **Descriptor và identity** [reviewed_draft; 3 mục cũ; 1 claim] — open file description, UID/GID và giới hạn

## P02 — Linux và vận hành máy chủ

**Câu hỏi:** Nhân cho phép, giới hạn và duy trì một dịch vụ như thế nào?
**Mô hình:** Lời gọi hệ thống đi qua định danh, namespace tên, quyền, tài nguyên rồi tới supervisor; mỗi ranh giới có bằng chứng riêng.
**Tiên quyết:** P01: tiến trình, địa chỉ ảo, CPU time và file descriptor.
**Ranh giới:** Không dạy OCI image hoặc Kubernetes; chỉ cơ chế và vận hành host.
**Năng lực ra:** Phân biệt lỗi quyền, I/O, quota, tiến trình và readiness trên host.
**Ngộ nhận cần sửa:** systemctl active nghĩa là ứng dụng đã sẵn sàng phục vụ.
**Chuyển tiếp:** Cho Docker runtime, Ansible, Kubernetes node và điều tra sự cố.

### P02.C01 — Syscall, đường dẫn và hệ thống tệp [reviewed_draft]

- **Đích học:** Giải thích tại sao cùng tên file có thể trỏ đối tượng khác.
- **Mô hình nối bài:** VFS phân giải từng thành phần đường dẫn rồi trả descriptor gắn đối tượng mở.
- **Tiên quyết bắt buộc:** P01.C02.L03.
- **Ranh giới:** Không dạy image layer hay cloud object store.
- **Ngộ nhận:** Tên file, inode và descriptor là một.
- **Cách dạy:** Lần theo openat, rename, symlink và lỗi EACCES/ENOENT.
- **Đánh giá:** Giải thích log vẫn ghi vào file đã đổi tên và điều kiện fsync.
- **Nối tới:** P02.C02, P02.C03, P02.C05, P04.C01, P05.C01, P07.C03, P08.C04.
- **Nguồn cũ:** Ch01, Ch02, Ch03.
- **Cây bài:**
  - `P02.C01.L01` **Vào nhân** [reviewed_draft; 2 mục cũ; 1 claim] — syscall, wrapper, errno và thao tác thật
  - `P02.C01.L02` **Phân giải tên** [reviewed_draft; 1 mục cũ; 1 claim] — directory traversal, inode, hard/symlink
  - `P02.C01.L03` **Ghi và bền vững** [reviewed_draft; 1 mục cũ; 2 claim] — page cache, rename, fsync file/thư mục

### P02.C02 — Danh tính và quyền Linux [reviewed_draft]

- **Đích học:** Chẩn đoán một lần mở file bị từ chối qua mọi thư mục cha.
- **Mô hình nối bài:** UID/GID, mode và chính sách bảo vệ được xét tại thao tác cụ thể.
- **Tiên quyết bắt buộc:** P02.C01.L02.
- **Ranh giới:** AWS IAM và K8s RBAC có scope khác.
- **Ngộ nhận:** Chỉ cần chmod file đích là đọc được.
- **Cách dạy:** Đọc đường dẫn, identity, group và kết quả syscall trước khi sửa.
- **Đánh giá:** Giải thích 0640 file dưới thư mục 0700 và sửa tối thiểu.
- **Nối tới:** P02.C04, P08.C01.
- **Nguồn cũ:** Ch01, Ch03.
- **Cây bài:**
  - `P02.C02.L01` **Danh tính tiến trình** [reviewed_draft; 1 mục cũ; 1 claim] — real/effective ID, group và capability ở mức giới thiệu
  - `P02.C02.L02` **Bước đi qua thư mục** [reviewed_draft; 1 mục cũ; 1 claim] — execute/search permission, owner/group/mode, ACL khi có
  - `P02.C02.L03` **Điều tra và sửa** [needs_extension; 0 mục cũ; 0 claim] — đúng UID, đường dẫn, least privilege, không chmod 777

### P02.C03 — Tài nguyên và chẩn đoán hiệu năng Linux [reviewed_draft]

- **Đích học:** Phân biệt CPU runnable/quota, memory reclaim và I/O wait bằng counter.
- **Mô hình nối bài:** Đọc hiệu hai mẫu trong cùng cửa sổ rồi gắn với latency, không suy từ một snapshot.
- **Tiên quyết bắt buộc:** P01.C01.L03, P02.C01.L03.
- **Ranh giới:** cgroup v2 controller đầy đủ ở P07.C01; Prometheus ở P12.
- **Ngộ nhận:** RAM cache luôn là lãng phí; throttled cycles là CPU utilization.
- **Cách dạy:** Dùng bộ số Ch2 và phản biện các nguyên nhân cạnh tranh.
- **Đánh giá:** Tính core từ usage_usec và PSI, nêu giới hạn nhân quả.
- **Nối tới:** P07.C01, P11.C03, P13.C04.
- **Nguồn cũ:** Ch02, Ch10.
- **Cây bài:**
  - `P02.C03.L01` **CPU và scheduler** [reviewed_draft; 2 mục cũ; 1 claim] — runnable, usage, quota và PSI
  - `P02.C03.L02` **Memory** [reviewed_draft; 1 mục cũ; 1 claim] — virtual/resident, reclaim, page cache, OOM
  - `P02.C03.L03` **I/O và độ bền** [reviewed_draft; 1 mục cũ; 0 claim] — dirty/writeback, fsync và thiết bị
  - `P02.C03.L04` **Điều tra đa tín hiệu** [reviewed_draft; 1 mục cũ; 3 claim] — lấy hiệu counter CPU, memory, I/O cùng cửa sổ, đối chiếu latency và phép đo thiếu

### P02.C04 — systemd và vòng đời dịch vụ [reviewed_draft]

- **Đích học:** Tách start thành công khỏi listener, readiness và dữ liệu đúng.
- **Mô hình nối bài:** Unit dựng dependency/order và giám sát main process; ứng dụng có hợp đồng health riêng.
- **Tiên quyết bắt buộc:** P01.C02.L02, P02.C02.L03.
- **Ranh giới:** K8s probes ở P11.C02.
- **Ngộ nhận:** After= kéo dependency hoặc network.target bảo đảm IP đã sẵn.
- **Cách dạy:** Giải phẫu atlas.service và hai đường lỗi ExecStart/config.
- **Đánh giá:** Phân biệt Type=exec, After/Wants/Requires, active và request thật.
- **Nối tới:** P02.C05, P08.C03, P10.C01.
- **Nguồn cũ:** Ch01, Ch03.
- **Cây bài:**
  - `P02.C04.L01` **Unit graph** [reviewed_draft; 2 mục cũ; 2 claim] — After, Wants, Requires, network-online
  - `P02.C04.L02` **Process lifecycle** [reviewed_draft; 1 mục cũ; 3 claim] — Type, ExecStart, signal, restart
  - `P02.C04.L03` **Quan sát dịch vụ** [reviewed_draft; 2 mục cũ; 0 claim] — MainPID, journal, socket, readiness và hậu điều kiện

### P02.C05 — Vận hành host và phục hồi có kiểm chứng [planned_new]

- **Đích học:** Đặt thay đổi cấu hình, log rotation và backup vào quy trình có hậu điều kiện.
- **Mô hình nối bài:** Độ an toàn nằm ở thứ tự và khả năng phục hồi dữ liệu, không ở lệnh đơn lẻ.
- **Tiên quyết bắt buộc:** P02.C01.L03, P02.C04.L03.
- **Ranh giới:** Runbook sự cố đa dịch vụ ở P13.C02.
- **Ngộ nhận:** Tạo archive thành công chứng minh restore được.
- **Cách dạy:** Đi từ một lỗi host tới quyết định dừng, backup, sửa và kiểm tra.
- **Đánh giá:** Thiết kế phép thử restore và giới hạn dữ liệu chưa được bảo đảm.
- **Nối tới:** P05.C03, P06.C04.
- **Nguồn cũ:** Ch02, Ch03, Ch07.
- **Cây bài:**
  - `P02.C05.L01` **Thay đổi host** [planned_new; 0 mục cũ; 0 claim] — dịch vụ, quyền, config và cửa sổ bảo trì
  - `P02.C05.L02` **Dữ liệu host** [planned_new; 0 mục cũ; 0 claim] — backup nhất quán, restore thử và log rotation
  - `P02.C05.L03` **Phục hồi** [planned_new; 0 mục cũ; 0 claim] — chứng cứ trước/sau, rollback config, request và dữ liệu

## P03 — Mạng và giao thức ứng dụng

**Câu hỏi:** Một request đi từ tên tới byte phản hồi qua những ranh giới nào?
**Mô hình:** Mỗi tầng chọn một đích hoặc hợp đồng: route/neighbor, kết nối, bảo mật phiên, ngữ nghĩa HTTP và proxy.
**Tiên quyết:** P01 tiến trình/socket; P02 service listener trên host. Mạng namespace được giới thiệu sau ở P07.
**Ranh giới:** VPC, CNI và Gateway API chỉ áp dụng lại cơ chế, không dạy lại TCP từ đầu.
**Năng lực ra:** Khoanh chặng hỏng bằng quan sát từ đúng phía client và server.
**Ngộ nhận cần sửa:** Một status hoặc TCP established tự nó chỉ ra nguyên nhân gốc.
**Chuyển tiếp:** Cho cloud network, container publishing, Service/Gateway và tracing.

### P03.C01 — Địa chỉ, subnet và đường đi gói IP [mixed]

- **Đích học:** Từ đích IP tìm route và địa chỉ chặng kế tiếp.
- **Mô hình nối bài:** Prefix quyết định on-link; routing chọn next hop; neighbor resolution tìm địa chỉ link cục bộ.
- **Tiên quyết bắt buộc:** P01.C02.L03.
- **Ranh giới:** TCP state ở chương sau; VPC route ở P08.
- **Ngộ nhận:** ARP hỏi MAC của server ở mạng xa.
- **Cách dạy:** Vẽ từng hop và xác nhận bằng route get từ đúng namespace.
- **Đánh giá:** Chọn next hop cho route /24 và /0, nêu điều policy routing thay đổi.
- **Nối tới:** P03.C02, P07.C01, P08.C02, P11.C04.
- **Nguồn cũ:** Ch04.
- **Cây bài:**
  - `P03.C01.L01` **Định danh logic** [reviewed_draft; 1 mục cũ; 1 claim] — IPv4/IPv6, prefix, subnet và địa chỉ nguồn
  - `P03.C01.L02` **Chọn chặng** [reviewed_draft; 1 mục cũ; 2 claim] — longest prefix, policy route, source address
  - `P03.C01.L03` **Đóng frame** [reviewed_draft; 1 mục cũ; 1 claim] — ARP/IPv6 Neighbor Discovery, link address, hop và đường về
  - `P03.C01.L04` **Kích thước đường** [planned_new; 0 mục cũ; 0 claim] — MTU, fragmentation và Path MTU Discovery, triệu chứng black hole

### P03.C02 — Transport, TCP, UDP và NAT [mixed]

- **Đích học:** Lần theo SYN, seq/ack, retransmission, datagram UDP và dịch tuple hai chiều.
- **Mô hình nối bài:** TCP endpoint giữ luồng byte; UDP giữ datagram và không tự bảo đảm giao hàng; NAT giữ ánh xạ packet độc lập với socket ứng dụng.
- **Tiên quyết bắt buộc:** P03.C01.L03.
- **Ranh giới:** TLS/HTTP ở P03.C03; không mở rộng thành giáo trình định tuyến chuyên sâu.
- **Ngộ nhận:** TCP established chứng minh HTTP hoạt động; UDP timeout chứng minh server không nhận gói.
- **Cách dạy:** Dùng trace số RFC 9293, datagram DNS/QUIC cơ sở và tình huống đường về mất.
- **Đánh giá:** Tính ACK cộng dồn, kiểm mapping NAPT và nêu chứng cứ phân biệt UDP loss.
- **Nối tới:** P03.C03, P08.C02, P11.C04.
- **Nguồn cũ:** Ch04.
- **Cây bài:**
  - `P03.C02.L01` **Bắt tay và byte stream** [reviewed_draft; 1 mục cũ; 3 claim] — SYN, seq, ack, retransmission
  - `P03.C02.L02` **Socket và lỗi** [reviewed_draft; 2 mục cũ; 3 claim] — LISTEN, connect, ECONNREFUSED, timeout
  - `P03.C02.L03` **NAT và đối xứng đường** [reviewed_draft; 1 mục cũ; 2 claim] — tuple, state timeout, return path
  - `P03.C02.L04` **UDP có điều kiện** [planned_new; 0 mục cũ; 0 claim] — datagram, port, checksum, timeout, DNS/QUIC và quan sát hai phía

### P03.C03 — Tên, TLS và ngữ nghĩa HTTP [reviewed_draft]

- **Đích học:** Tách lỗi DNS, TCP, chứng chỉ và HTTP bằng dữ kiện tối thiểu.
- **Mô hình nối bài:** Tên chọn địa chỉ; TLS xác minh peer; HTTP đặt phương thức, header, status và body.
- **Tiên quyết bắt buộc:** P03.C02.L02, P03.C02.L04.
- **Ranh giới:** Proxy hop ở P03.C04; cloud DNS ở P08.
- **Ngộ nhận:** DNS trả IP nghĩa là service chạy; 502 luôn do upstream chết.
- **Cách dạy:** Lần theo request client với SNI/Host và kết quả từng tầng.
- **Đánh giá:** Định ranh giới xa nhất đã vượt qua cho mỗi lỗi.
- **Nối tới:** P03.C04, P08.C01, P14.C01.
- **Nguồn cũ:** Ch05.
- **Cây bài:**
  - `P03.C03.L01` **DNS và cache** [reviewed_draft; 1 mục cũ; 3 claim] — stub, recursive, authoritative, TTL, A/AAAA, UDP/TCP transport
  - `P03.C03.L02` **TLS** [reviewed_draft; 1 mục cũ; 3 claim] — SNI, chứng chỉ, tên, trust, timeout
  - `P03.C03.L03` **HTTP** [reviewed_draft; 1 mục cũ; 2 claim] — request/response, Host, method, status, cache và body

### P03.C04 — Reverse proxy và điều tra request hai chặng [reviewed_draft]

- **Đích học:** Xác định ai sinh status và chặng nào timeout.
- **Mô hình nối bài:** Proxy kết thúc một chặng rồi là client của chặng khác; forwarded headers cần trust boundary.
- **Tiên quyết bắt buộc:** P03.C03.L03.
- **Ranh giới:** Gateway API ở P11.C07.
- **Ngộ nhận:** Một mã 504 xác nhận upstream không chạy.
- **Cách dạy:** Đọc http_two_hop.txt, sau đó chèn timeout ở từng chặng.
- **Đánh giá:** Chứng minh Host/Content-Length, TLS boundary và nơi tạo response.
- **Nối tới:** P06.C03, P07.C04, P11.C07, P12.C03.
- **Nguồn cũ:** Ch05.
- **Cây bài:**
  - `P03.C04.L01` **Chọn upstream** [reviewed_draft; 1 mục cũ; 1 claim] — virtual host, route, pool, cache
  - `P03.C04.L02` **Hai chặng** [reviewed_draft; 1 mục cũ; 2 claim] — client–proxy và proxy–upstream, header chuyển tiếp
  - `P03.C04.L03` **Đường lỗi** [reviewed_draft; 3 mục cũ; 2 claim] — 502/504, retry an toàn, log và hậu điều kiện

## P04 — Git và lịch sử thay đổi

**Câu hỏi:** Làm sao biết, tích hợp và khôi phục đúng thay đổi đã chia sẻ?
**Mô hình:** Blob/tree/commit là đồ thị bất biến; ref, index và working tree là trạng thái có thể dịch.
**Tiên quyết:** P01: file và process; không cần cloud.
**Ranh giới:** Pipeline và release ở P06 dùng commit, không lặp object model.
**Năng lực ra:** Giải conflict và chọn merge/rebase/revert dựa trên đồ thị.
**Ngộ nhận cần sửa:** Branch là bản sao thư mục, reset là rollback an toàn cho nhánh chung.
**Chuyển tiếp:** Cho identity của artifact, CI và supply chain.

### P04.C01 — Git object, index và ref [reviewed_draft]

- **Đích học:** Dự đoán byte nào sẽ nằm trong commit kế tiếp.
- **Mô hình nối bài:** Blob/tree/commit là snapshot có cha; HEAD/ref/index/working tree là ba lớp trạng thái.
- **Tiên quyết bắt buộc:** P02.C01.L02.
- **Ranh giới:** CI dùng commit ID ở P06.
- **Ngộ nhận:** git add là liên kết sống tới file đang sửa.
- **Cách dạy:** Đọc object graph và tình huống staged 2000/working 3000.
- **Đánh giá:** Tính tree của commit và chứng cứ diff staged.
- **Nối tới:** P04.C02, P06.C01, P09.C01, P11.C08, P14.C03.
- **Nguồn cũ:** Ch06.
- **Cây bài:**
  - `P04.C01.L01` **Object graph** [reviewed_draft; 1 mục cũ; 2 claim] — blob, tree, commit, SHA
  - `P04.C01.L02` **Trạng thái cục bộ** [reviewed_draft; 1 mục cũ; 2 claim] — HEAD, ref, index, working tree
  - `P04.C01.L03` **Danh tính thay đổi** [needs_extension; 0 mục cũ; 0 claim] — tag, branch, remote, object reachability

### P04.C02 — Tích hợp và sửa lịch sử [reviewed_draft]

- **Đích học:** Giải conflict mà vẫn giữ ý nghĩa thay đổi và lịch sử chia sẻ.
- **Mô hình nối bài:** Merge tạo nút hai cha; rebase tái tạo commit; revert thêm lịch sử, reset dịch ref.
- **Tiên quyết bắt buộc:** P04.C01.L03.
- **Ranh giới:** Rollout/rollback artifact ở P06.
- **Ngộ nhận:** Chọn ours/theirs theo tên branch là đủ xác định đúng mã.
- **Cách dạy:** Tái hiện graph B-D/C, index stage 1/2/3 rồi kiểm thử kết quả.
- **Đánh giá:** Vẽ đồ thị sau merge/rebase/revert và quyết định an toàn cho nhánh chung.
- **Nối tới:** P06.C02.
- **Nguồn cũ:** Ch06.
- **Cây bài:**
  - `P04.C02.L01` **Merge** [reviewed_draft; 1 mục cũ; 2 claim] — merge base, conflict stages, hai cha
  - `P04.C02.L02` **Rebase** [reviewed_draft; 1 mục cũ; 1 claim] — commit mới, xung đột và lịch sử chia sẻ
  - `P04.C02.L03` **Phục hồi** [reviewed_draft; 2 mục cũ; 2 claim] — revert, reset, reflog có giới hạn, kiểm thử

## P05 — Tự động hóa hệ thống

**Câu hỏi:** Một chuỗi tác vụ báo đúng thất bại và có thể chạy lại thế nào?
**Mô hình:** Parser, argv, status, deadline và tác dụng phụ qua nhiều tiến trình là các hợp đồng khác nhau.
**Tiên quyết:** P01 process/exit; P02 quyền/file; P04 trạng thái thay đổi.
**Ranh giới:** Không thay Ansible/Terraform bằng script tùy tiện; dạy hợp đồng lỗi nền tảng.
**Năng lực ra:** Viết và kiểm tra đường thành công, lỗi, timeout và trạng thái từng phần.
**Ngộ nhận cần sửa:** set -e hoặc một exit 0 bảo đảm workflow thành công.
**Chuyển tiếp:** Cho CI jobs, IaC automation, incident runbook.

### P05.C01 — Bash và ngữ nghĩa lỗi của shell [reviewed_draft]

- **Đích học:** Dự đoán argv, output và exit status trước khi chạy script.
- **Mô hình nối bài:** Shell parse trước, expand sau; redirection/pipeline/conditional thay nguồn status quan sát.
- **Tiên quyết bắt buộc:** P01.C02.L03, P02.C01.L01.
- **Ranh giới:** Python/Go orchestration ở P05.C02.
- **Ngộ nhận:** set -euo pipefail tự biến script thành giao dịch.
- **Cách dạy:** Tái hiện script backup lỗi trên thư mục tạm và giải thích từng nhánh.
- **Đánh giá:** Dự đoán false success, quoting, pipefail và trap.
- **Nối tới:** P05.C02.
- **Nguồn cũ:** Ch07.
- **Cây bài:**
  - `P05.C01.L01` **Parsing** [reviewed_draft; 1 mục cũ; 3 claim] — quote, expansion, splitting, globbing
  - `P05.C01.L02` **I/O và status** [reviewed_draft; 1 mục cũ; 3 claim] — descriptor, redirect, pipe, PIPESTATUS
  - `P05.C01.L03` **Control flow** [reviewed_draft; 2 mục cũ; 3 claim] — errexit exception, signal, trap, cleanup

### P05.C02 — Python và Go điều phối tiến trình [reviewed_draft]

- **Đích học:** Đọc/viết CLI DevOps nhỏ bằng Python hoặc Go, xử lý argv, lỗi, timeout và test nhánh.
- **Mô hình nối bài:** Parent quan sát startup và task deadline khác nhau; cancellation không rollback tác dụng phụ.
- **Tiên quyết bắt buộc:** P05.C01.L03, P01.C02.L02.
- **Ranh giới:** Đóng gói artifact ở P06; không dạy Go như một giáo trình ngôn ngữ riêng.
- **Ngộ nhận:** Không dùng shell thì input tự an toàn; timeout đã dừng dịch vụ từ xa.
- **Cách dạy:** Đọc ba chương trình orchestration và kiểm thử success/fail/slow.
- **Đánh giá:** Phân biệt START_ERROR, EXIT 7, TIMEOUT, partial state và dependency môi trường.
- **Nối tới:** P05.C03.
- **Nguồn cũ:** Ch08.
- **Cây bài:**
  - `P05.C02.L01` **Chọn ngôn ngữ** [reviewed_draft; 2 mục cũ; 1 claim] — Bash đủ dùng vs Python/Go CLI nhỏ, module/dependency
  - `P05.C02.L02` **Subprocess** [reviewed_draft; 2 mục cũ; 4 claim] — argv, env, status, Python exception/Go error, startup readiness, test nhánh
  - `P05.C02.L03` **Timeout** [reviewed_draft; 2 mục cũ; 3 claim] — communicate, context cancellation/CommandContext, child/grandchild và cleanup

### P05.C03 — Workflow an toàn và chạy lại [mixed]

- **Đích học:** Thiết kế tác vụ nhiều bước có nhận diện partial failure.
- **Mô hình nối bài:** Mỗi bước phải có tiền/hậu điều kiện, idempotency key và chính sách retry theo tác dụng phụ.
- **Tiên quyết bắt buộc:** P05.C02.L03, P02.C05.L03.
- **Ranh giới:** CI gate ở P06; Ansible idempotency ở P10.
- **Ngộ nhận:** Lặp vô hạn hoặc xóa partial state làm hệ thống chắc chắn hội tụ.
- **Cách dạy:** Điều tra backup/deploy báo thành công giả, rồi thiết kế mô hình trạng thái.
- **Đánh giá:** Viết bảng trạng thái và phép thử chạy lại khi lỗi/timeout.
- **Nối tới:** P06.C01, P10.C02.
- **Nguồn cũ:** Ch07, Ch08.
- **Cây bài:**
  - `P05.C03.L01` **Hợp đồng bước** [needs_extension; 2 mục cũ; 2 claim] — input, output, error class, secret
  - `P05.C03.L02` **Retry** [needs_extension; 1 mục cũ; 0 claim] — idempotency, deduplication, backoff, concurrency
  - `P05.C03.L03` **Phục hồi** [needs_extension; 2 mục cũ; 3 claim] — durable marker, compensation, cleanup và chứng minh hậu điều kiện

## P06 — Build, kiểm thử và phát hành

**Câu hỏi:** Một commit trở thành artifact đang phục vụ người dùng bằng chứng cứ nào?
**Mô hình:** Source, build inputs, artifact digest, test gate, deployment state và dữ liệu là các vòng đời tách biệt.
**Tiên quyết:** P04 commit/ref; P05 status và retry; P03 request/readiness.
**Ranh giới:** Không triển khai chi tiết Kubernetes rollout ở đây; giữ mô hình phát hành độc lập nền tảng.
**Năng lực ra:** Thiết kế cổng kiểm thử, rollout, dừng và hậu điều kiện rollback.
**Ngộ nhận cần sửa:** Rollback binary tự đảo migration hay tác dụng phụ dữ liệu.
**Chuyển tiếp:** Cho Docker image, Helm release, SRE change risk và supply chain.

### P06.C01 — Build và danh tính artifact [reviewed_draft]

- **Đích học:** Chứng minh production chạy đúng byte đã qua kiểm thử.
- **Mô hình nối bài:** Commit là source snapshot; toolchain/dependency/build flags tạo artifact; digest nhận diện byte.
- **Tiên quyết bắt buộc:** P04.C01.L03, P05.C03.L01.
- **Ranh giới:** OCI manifest chuyên sâu ở P07.C02.
- **Ngộ nhận:** Cùng commit luôn tạo cùng binary.
- **Cách dạy:** Truy vết c83→H83, c84→H84 và một lần rebuild khác byte.
- **Đánh giá:** Đề xuất provenance tối thiểu và phép build đối chiếu.
- **Nối tới:** P06.C02, P07.C02.
- **Nguồn cũ:** Ch09.
- **Cây bài:**
  - `P06.C01.L01` **Đầu vào build** [reviewed_draft; 2 mục cũ; 2 claim] — source, dependency, compiler, môi trường
  - `P06.C01.L02` **Artifact** [reviewed_draft; 1 mục cũ; 2 claim] — digest, tag, immutable promotion
  - `P06.C01.L03` **Tái lập** [needs_extension; 0 mục cũ; 0 claim] — so byte độc lập, giới hạn cache và timestamp

### P06.C02 — Test gates và CI/CD [mixed]

- **Đích học:** Thiết kế test kiểm đúng ranh giới của thay đổi và quyền release.
- **Mô hình nối bài:** CI phản hồi trên commit; CD quảng bá một artifact đã xét qua policy theo môi trường.
- **Tiên quyết bắt buộc:** P06.C01.L03, P04.C02.L03.
- **Ranh giới:** Bảo mật supply chain chi tiết ở P14.C03.
- **Ngộ nhận:** Unit test và readiness xanh xác nhận hành vi tiền bạc của đơn hàng.
- **Cách dạy:** Đọc gate bỏ sót amount_cents; bổ sung phép kiểm nghiệp vụ.
- **Đánh giá:** Lập ma trận unit/integration/contract/production smoke và quyền phê duyệt.
- **Nối tới:** P06.C03, P09.C04, P14.C03.
- **Nguồn cũ:** Ch09.
- **Cây bài:**
  - `P06.C02.L01` **CI vs CD** [needs_extension; 1 mục cũ; 1 claim] — build, test, delivery, deployment
  - `P06.C02.L02` **Test model** [needs_extension; 0 mục cũ; 0 claim] — pyramid, contract, data fixtures, false confidence
  - `P06.C02.L03` **Gate** [needs_extension; 1 mục cũ; 1 claim] — secret, approval, concurrency và evidence

### P06.C03 — Rollout và quyết định dừng [reviewed_draft]

- **Đích học:** Chọn rolling, blue-green hay canary theo năng lực và khả năng quan sát.
- **Mô hình nối bài:** Traffic chuyển dần tới artifact mới; quan sát đại diện quyết định tiếp tục hoặc dừng.
- **Tiên quyết bắt buộc:** P06.C02.L03, P03.C04.L03.
- **Ranh giới:** Deployment controller ở P11.C02.
- **Ngộ nhận:** Canary nhỏ luôn đủ thống kê hoặc green probe bằng green user journey.
- **Cách dạy:** Dựng timeline H83/H84 theo version, lưu lượng và error budget.
- **Đánh giá:** Chọn chiến lược dưới giới hạn thêm một Pod và đặt stop rule.
- **Nối tới:** P06.C04, P08.C03, P10.C03, P11.C01, P13.C01.
- **Nguồn cũ:** Ch09.
- **Cây bài:**
  - `P06.C03.L01` **Chiến lược** [reviewed_draft; 1 mục cũ; 4 claim] — rolling, blue-green, canary
  - `P06.C03.L02` **Readiness** [reviewed_draft; 1 mục cũ; 1 claim] — process vs dependency vs request
  - `P06.C03.L03` **Điều phối** [needs_extension; 0 mục cũ; 0 claim] — serial release, approval, rollback trigger

### P06.C04 — Rollback và tương thích dữ liệu [reviewed_draft]

- **Đích học:** Chứng minh hậu điều kiện sau khi lùi ứng dụng.
- **Mô hình nối bài:** Binary/image có thể lùi, schema và tác dụng phụ đã ghi thường cần phục hồi riêng.
- **Tiên quyết bắt buộc:** P06.C03.L03, P02.C05.L02.
- **Ranh giới:** DR hệ thống ở P13.C03.
- **Ngộ nhận:** Một lệnh rollback đảo dữ liệu.
- **Cách dạy:** Phân tích amount_cents và 41 đơn, tách ứng dụng/dữ liệu/ngoại tác.
- **Đánh giá:** Nêu điều kiện expand-contract schema và kế hoạch phục hồi có thử.
- **Nối tới:** P09.C02, P11.C08, P13.C02, P13.C03.
- **Nguồn cũ:** Ch09.
- **Cây bài:**
  - `P06.C04.L01` **Dữ liệu qua bản phát hành** [reviewed_draft; 2 mục cũ; 2 claim] — migration, back/forward compatibility
  - `P06.C04.L02` **Partial deployment** [reviewed_draft; 1 mục cũ; 1 claim] — identity hiện chạy, request và dữ liệu
  - `P06.C04.L03` **Phục hồi** [reviewed_draft; 1 mục cũ; 1 claim] — snapshot, compensating action, hậu điều kiện

## P07 — Container và OCI

**Câu hỏi:** Image trở thành tiến trình cô lập ra sao, và dữ liệu sống ở đâu?
**Mô hình:** Namespace đổi góc nhìn, cgroup điều tiết tài nguyên; image là artifact, container là lần chạy, mount tách vòng đời dữ liệu.
**Tiên quyết:** P01 process/memory; P02 Linux permissions/resource; P03 network; P06 artifact.
**Ranh giới:** Không coi Compose là scheduler nhiều node; Kubernetes ở P11.
**Năng lực ra:** Lần theo image digest, PID, mount và dữ liệu qua recreate.
**Ngộ nhận cần sửa:** Container là VM nhỏ hoặc volume tự được backup.
**Chuyển tiếp:** Cho cloud native workload, Kubernetes runtime/storage và image security.

### P07.C01 — Namespace, cgroup v2 và runtime boundary [reviewed_draft]

- **Đích học:** Chỉ ra cơ chế nào đổi góc nhìn, cơ chế nào giới hạn CPU/RAM.
- **Mô hình nối bài:** PID/net/mount/user namespace là view; cgroup là accounting/control; runtime đặt process vào cả hai.
- **Tiên quyết bắt buộc:** P01.C02.L03, P02.C03.L03, P03.C01.L03.
- **Ranh giới:** Image artifact ở chương sau.
- **Ngộ nhận:** PID 1 trong container là PID 1 host; 80/100 throttled là 80% utilization.
- **Cách dạy:** Lần theo NSpid, netns, cpu.stat, memory.events.local có cửa sổ.
- **Đánh giá:** Phân biệt OOM, quota và lỗi config qua counter/log.
- **Nối tới:** P07.C02, P11.C01, P11.C03.
- **Nguồn cũ:** Ch10, Ch02.
- **Cây bài:**
  - `P07.C01.L01` **Tạo/tham gia** [reviewed_draft; 1 mục cũ; 5 claim] — clone, unshare, setns, fork/exec, quyền
  - `P07.C01.L02` **View** [reviewed_draft; 1 mục cũ; 3 claim] — PID/net/mount/user và quan sát host/container
  - `P07.C01.L03` **Limit** [reviewed_draft; 4 mục cũ; 7 claim] — cpu.max, memory.max, OOM và pressure

### P07.C02 — OCI image, build và registry [reviewed_draft]

- **Đích học:** Lần từ Dockerfile tới manifest/digest và byte đã pull.
- **Mô hình nối bài:** Image gồm config và layer theo descriptor; registry phân phối theo tag biến đổi hoặc digest.
- **Tiên quyết bắt buộc:** P06.C01.L03, P07.C01.L03.
- **Ranh giới:** Supply chain ký/provenance ở P14.C03.
- **Ngộ nhận:** Tag v2 là artifact bất biến; xóa secret ở layer sau xóa mọi dấu vết.
- **Cách dạy:** Giải phẫu build context, cache, digest và image cục bộ khác registry.
- **Đánh giá:** Chứng minh digest đang chạy thay vì chỉ đọc tag.
- **Nối tới:** P07.C03, P14.C03.
- **Nguồn cũ:** Ch10, Ch11.
- **Cây bài:**
  - `P07.C02.L01` **Build** [reviewed_draft; 1 mục cũ; 1 claim] — context, Dockerfile, layer cache, secret mount
  - `P07.C02.L02` **OCI** [reviewed_draft; 2 mục cũ; 3 claim] — config, manifest/index, descriptor và digest
  - `P07.C02.L03` **Distribution** [reviewed_draft; 1 mục cũ; 1 claim] — push/pull, tag, platform và kiểm byte

### P07.C03 — Container lifecycle và dữ liệu [reviewed_draft]

- **Đích học:** Dự đoán dữ liệu sau stop, recreate, remove, mount và đổi image.
- **Mô hình nối bài:** Container là run instance có writable layer; volume/bind là dữ liệu ở vòng đời độc lập.
- **Tiên quyết bắt buộc:** P07.C02.L03, P02.C01.L03.
- **Ranh giới:** K8s PV/PVC ở P11.C05.
- **Ngộ nhận:** Container đang running nghĩa là app Ready; volume tự có backup.
- **Cách dạy:** Theo 41 bản ghi qua A/B/D và xác định mount destination/volume identity.
- **Đánh giá:** Phân biệt khả năng khôi phục khi container dừng và khi đã xóa.
- **Nối tới:** P07.C04, P11.C02, P11.C05.
- **Nguồn cũ:** Ch10, Ch11.
- **Cây bài:**
  - `P07.C03.L01` **Lần chạy** [reviewed_draft; 3 mục cũ; 2 claim] — create, start, stop, exit, health
  - `P07.C03.L02` **Filesystem** [reviewed_draft; 1 mục cũ; 0 claim] — read-only layers, writable layer, whiteout
  - `P07.C03.L03` **Mount** [reviewed_draft; 2 mục cũ; 3 claim] — volume, bind, ownership, backup và restore

### P07.C04 — Compose và ứng dụng nhiều service [reviewed_draft]

- **Đích học:** Phân biệt cấu hình project với trạng thái service/volume thực tế.
- **Mô hình nối bài:** Compose gom service/network/mount trên một Engine; depends_on và health không chứng minh giao dịch nghiệp vụ.
- **Tiên quyết bắt buộc:** P07.C03.L03, P03.C04.L02.
- **Ranh giới:** Scheduler nhiều node ở P11.
- **Ngộ nhận:** Đổi project name xóa dữ liệu volume cũ.
- **Cách dạy:** Đọc compose-data.yaml, đổi tên project và kiểm tra volume identity.
- **Đánh giá:** Thiết kế thao tác down/up không xóa dữ liệu và phép restore.
- **Nối tới:** Tổng hợp cuối sách.
- **Nguồn cũ:** Ch11.
- **Cây bài:**
  - `P07.C04.L01` **Mô hình project** [reviewed_draft; 1 mục cũ; 2 claim] — services, network, DNS, port
  - `P07.C04.L02` **Khởi động** [reviewed_draft; 1 mục cũ; 2 claim] — dependency, healthcheck, restart và giới hạn
  - `P07.C04.L03` **Dữ liệu** [reviewed_draft; 2 mục cũ; 2 claim] — named/external volume, bind, recreate và cleanup

## P08 — Cloud và AWS

**Câu hỏi:** Một request qua ranh giới danh tính, mạng, tính toán và dữ liệu của cloud ra sao?
**Mô hình:** Identity policy và đường mạng là hai bộ lọc độc lập; compute và storage có vòng đời, miền lỗi, chi phí khác nhau.
**Tiên quyết:** P02 host; P03 route/TLS/HTTP; P06 release; P07 artifact.
**Ranh giới:** Terraform mô tả thay đổi cloud ở P09; không học HCL trong phần này.
**Năng lực ra:** Phân biệt timeout, AccessDenied, lỗi target và mất dữ liệu bằng bằng chứng.
**Ngộ nhận cần sửa:** Role gắn EC2 tự tạo đường tới AWS API; replication đồng nghĩa backup.
**Chuyển tiếp:** Cho IaC, DR, reliability và cloud security.

### P08.C01 — AWS identity và IAM evaluation [reviewed_draft]

- **Đích học:** Lần theo principal từ EC2 tới S3/STS và quyết định Allow/Deny.
- **Mô hình nối bài:** Trust nhận role; temporary credentials định danh session; policy evaluation áp dụng theo request/resource/context.
- **Tiên quyết bắt buộc:** P02.C02.L03, P03.C03.L02.
- **Ranh giới:** Cloud network ở P08.C02; threat model liên miền ở P14.
- **Ngộ nhận:** Role attached đồng nghĩa mọi API đều được phép.
- **Cách dạy:** Đọc policy JSON giả định, explicit Deny và request ARN/action.
- **Đánh giá:** Phân biệt authn/authorization/route khi gặp AccessDenied.
- **Nối tới:** P08.C02, P14.C01.
- **Nguồn cũ:** Ch12.
- **Cây bài:**
  - `P08.C01.L01` **Danh tính** [reviewed_draft; 1 mục cũ; 2 claim] — user, role, session, trust, IMDS, STS
  - `P08.C01.L02` **Quyết định** [reviewed_draft; 1 mục cũ; 2 claim] — Allow, explicit Deny, boundaries/SCP/resource policy theo scope
  - `P08.C01.L03` **Điều tra** [reviewed_draft; 1 mục cũ; 1 claim] — principal, action, resource, context và audit event

### P08.C02 — VPC, subnet và đường đi AWS [reviewed_draft]

- **Đích học:** Chứng minh private workload có hoặc không có đường tới S3/STS.
- **Mô hình nối bài:** Route quyết định target; SG stateful và NACL stateless lọc gói; endpoint thay loại đường, không cấp quyền IAM.
- **Tiên quyết bắt buộc:** P03.C02.L03, P03.C01.L04, P08.C01.L03.
- **Ranh giới:** K8s Service/Gateway ở P11 dùng control plane khác.
- **Ngộ nhận:** Private subnet có NAT Gateway thì mọi AWS API đều dùng cùng đường an toàn.
- **Cách dạy:** Tách timeout DNS/route/SG/NACL/endpoint theo vị trí nguồn.
- **Đánh giá:** Vẽ đường request đi và về qua ALB, IGW, NAT/endpoint.
- **Nối tới:** P08.C03, P14.C04.
- **Nguồn cũ:** Ch12, Ch04.
- **Cây bài:**
  - `P08.C02.L01` **Topology** [reviewed_draft; 1 mục cũ; 3 claim] — VPC, subnet/AZ, route table, IGW, NAT
  - `P08.C02.L02` **Chính sách gói** [reviewed_draft; 1 mục cũ; 2 claim] — SG, NACL, state và ephemeral port
  - `P08.C02.L03` **Private access** [reviewed_draft; 2 mục cũ; 5 claim] — gateway/interface endpoint, DNS, route và điều kiện

### P08.C03 — EC2, load balancer và miền lỗi [mixed]

- **Đích học:** Phân biệt instance running, target healthy và request nghiệp vụ đúng.
- **Mô hình nối bài:** Compute instance, ENI, ALB target và AZ chịu vòng đời/health khác nhau.
- **Tiên quyết bắt buộc:** P08.C02.L03, P02.C04.L03, P06.C03.L02.
- **Ranh giới:** Autoscaling/cloud cost ở P15.C02.
- **Ngộ nhận:** ALB /health 200 chứng minh endpoint đọc S3 tốt.
- **Cách dạy:** Theo client→ALB→private EC2→dependency và mỗi phép health.
- **Đánh giá:** Đặt phép kiểm trước/sau failover một AZ.
- **Nối tới:** P08.C04.
- **Nguồn cũ:** Ch12.
- **Cây bài:**
  - `P08.C03.L01` **Compute** [needs_extension; 1 mục cũ; 0 claim] — instance, image, boot, instance profile
  - `P08.C03.L02` **Traffic** [needs_extension; 1 mục cũ; 0 claim] — ALB listener, target group, health và timeout
  - `P08.C03.L03` **Failure domain** [needs_extension; 0 mục cũ; 0 claim] — AZ, capacity, replace và state ngoài instance

### P08.C04 — Block, file và object storage [reviewed_draft]

- **Đích học:** Chọn EBS/EFS/S3 theo cách truy cập và vòng đời dữ liệu.
- **Mô hình nối bài:** Block là volume AZ, shared file là filesystem có miền lỗi riêng, object là API; durability khác availability và backup.
- **Tiên quyết bắt buộc:** P08.C03.L03, P02.C01.L03.
- **Ranh giới:** K8s storage ở P11.C05; DR ở P13.C03.
- **Ngộ nhận:** Replication mặc định là backup hoặc EBS attach xuyên AZ.
- **Cách dạy:** Đối chiếu AZ hỏng và object bị xóa nhầm.
- **Đánh giá:** Đề xuất thử restore cho từng dạng dữ liệu, không suy từ SLA chung.
- **Nối tới:** P09.C01, P09.C04, P11.C05, P13.C03, P15.C02.
- **Nguồn cũ:** Ch12, Ch11.
- **Cây bài:**
  - `P08.C04.L01` **Block** [reviewed_draft; 1 mục cũ; 2 claim] — EBS attach, snapshot, delete_on_termination
  - `P08.C04.L02` **File** [reviewed_draft; 1 mục cũ; 1 claim] — EFS mount, đồng thời, quyền
  - `P08.C04.L03` **Object** [reviewed_draft; 1 mục cũ; 2 claim] — S3 API, versioning, lifecycle, restore và chi phí

## P09 — Terraform và trạng thái hạ tầng

**Câu hỏi:** Cấu hình, state và hạ tầng thực lệch nhau thì quyết định thay đổi thế nào?
**Mô hình:** Provider dựng DAG rồi đọc state/API và thực hiện các tác vụ có thể thất bại từng phần; state là ánh xạ nhạy cảm.
**Tiên quyết:** P04 Git; P06 change gate; P08 resource/IAM/network/data.
**Ranh giới:** Ansible hội tụ file bên trong máy ở P10, không được nhập nhằng với Terraform state.
**Năng lực ra:** Đọc plan/replacement và phục hồi state hoặc object an toàn.
**Ngộ nhận cần sửa:** Plan là giao dịch hoặc lock khóa cả console/cloud API.
**Chuyển tiếp:** Cho vận hành production, drift control và change approval.

### P09.C01 — HCL, provider và dependency DAG [reviewed_draft]

- **Đích học:** Đọc tài nguyên, data source và cạnh implicit/explicit trong plan.
- **Mô hình nối bài:** Provider là chương trình/API boundary; references tạo DAG; depends_on chỉ thêm cạnh thực.
- **Tiên quyết bắt buộc:** P08.C04.L03, P04.C01.L03.
- **Ranh giới:** State/backend ở chương sau.
- **Ngộ nhận:** Thứ tự các block trong file là thứ tự apply.
- **Cách dạy:** Đọc main.tf terraform_data và vẽ đồ thị trước khi chạy.
- **Đánh giá:** Tìm cạnh tham chiếu và nhận diện cạnh depends_on dư.
- **Nối tới:** P09.C02.
- **Nguồn cũ:** Ch13.
- **Cây bài:**
  - `P09.C01.L01` **Ngôn ngữ** [reviewed_draft; 1 mục cũ; 1 claim] — variable, resource, data, output, expression
  - `P09.C01.L02` **Provider** [reviewed_draft; 1 mục cũ; 0 claim] — schema, CRUD, version pin
  - `P09.C01.L03` **DAG** [reviewed_draft; 1 mục cũ; 3 claim] — implicit refs, depends_on, cycle và parallelism

### P09.C02 — Plan, state và backend [reviewed_draft]

- **Đích học:** Giải thích tại sao một plan có thể thất bại giữa chừng và state nhạy cảm.
- **Mô hình nối bài:** Configuration, state snapshot và API reality là ba thực thể; lock chỉ bảo vệ một state phù hợp.
- **Tiên quyết bắt buộc:** P09.C01.L03, P06.C04.L03.
- **Ranh giới:** Import/refactor ở chương sau.
- **Ngộ nhận:** Plan là giao dịch; sensitive flag mã hóa state.
- **Cách dạy:** Lần theo partial apply và remote write failure.
- **Đánh giá:** Liệt kê object thực/state/config và bước đối chiếu trước retry.
- **Nối tới:** P09.C03, P10.C01, P14.C02.
- **Nguồn cũ:** Ch13.
- **Cây bài:**
  - `P09.C02.L01` **Ba trạng thái** [reviewed_draft; 1 mục cũ; 1 claim] — config, state binding, real object
  - `P09.C02.L02` **Plan/apply** [reviewed_draft; 1 mục cũ; 4 claim] — refresh, unknown value, provider failure
  - `P09.C02.L03` **Backend** [reviewed_draft; 1 mục cũ; 3 claim] — locking, versioning, access, encryption, restore

### P09.C03 — Drift, import và refactor [mixed]

- **Đích học:** Phân biệt thay đổi ngoài Terraform với đổi địa chỉ cấu hình.
- **Mô hình nối bài:** Drift được thấy khi provider refresh được; import/moved block sửa ánh xạ, không tự sửa dữ liệu.
- **Tiên quyết bắt buộc:** P09.C02.L03.
- **Ranh giới:** Approval rollout ở P09.C04.
- **Ngộ nhận:** ignore_changes là cách chữa drift an toàn mọi lúc.
- **Cách dạy:** Điều tra B trên console so với HCL A và state cũ.
- **Đánh giá:** Chọn import, moved, sửa HCL hoặc phục hồi với điều kiện cụ thể.
- **Nối tới:** P09.C04.
- **Nguồn cũ:** Ch13.
- **Cây bài:**
  - `P09.C03.L01` **Drift** [needs_extension; 1 mục cũ; 1 claim] — refresh, -refresh=false, refresh-only
  - `P09.C03.L02` **Ánh xạ** [needs_extension; 0 mục cũ; 0 claim] — import, moved, state mv có kiểm soát
  - `P09.C03.L03` **Refactor** [needs_extension; 0 mục cũ; 0 claim] — count/for_each/module address và chống destroy

### P09.C04 — Thay đổi hạ tầng có dữ liệu [reviewed_draft]

- **Đích học:** Quyết định dừng khi plan đề xuất replace instance chứa dữ liệu.
- **Mô hình nối bài:** Plan là dự báo có điều kiện; backup và hậu điều kiện độc lập quyết định quyền apply.
- **Tiên quyết bắt buộc:** P09.C03.L03, P08.C04.L03, P06.C02.L03.
- **Ranh giới:** Không tạo AWS resource thật để dạy nếu không được cấp phép.
- **Ngộ nhận:** Có state lock nghĩa là console không gây race.
- **Cách dạy:** Đọc user_data_replace_on_change và root EBS delete_on_termination.
- **Đánh giá:** Viết preflight, stop rule, apply sequencing và recovery plan.
- **Nối tới:** Tổng hợp cuối sách.
- **Nguồn cũ:** Ch13.
- **Cây bài:**
  - `P09.C04.L01` **Replacement** [reviewed_draft; 1 mục cũ; 2 claim] — ForceNew/provider schema và data risk
  - `P09.C04.L02` **Điều phối** [needs_extension; 0 mục cũ; 0 claim] — approval, lock, concurrent actor, saved plan
  - `P09.C04.L03` **Hậu kiểm** [reviewed_draft; 1 mục cũ; 0 claim] — ID object, dữ liệu, request, state backup và rollback

## P10 — Ansible và hội tụ cấu hình

**Câu hỏi:** Làm sao áp trạng thái mong muốn lên các máy đang tồn tại mà không gây restart thừa?
**Mô hình:** Inventory chọn host, module quan sát rồi đổi trạng thái, handler hoãn tác động; kết quả theo từng host không phải giao dịch.
**Tiên quyết:** P02 Linux quyền/systemd; P05 idempotency/status; P09 ranh giới IaC.
**Ranh giới:** Không tạo VPC/EC2 mới ở đây; không xem changed là health check.
**Năng lực ra:** Chứng minh hai lượt hội tụ và xử lý drift, lỗi từng phần.
**Ngộ nhận cần sửa:** Mọi shell task idempotent và check mode bảo đảm apply thật.
**Chuyển tiếp:** Cho fleet operations, release orchestration và secrets.

### P10.C01 — Inventory và đường điều khiển Ansible [reviewed_draft]

- **Đích học:** Chỉ ra ai kết nối tới ai, bằng quyền nào và biến nào được dùng.
- **Mô hình nối bài:** Control node đọc inventory/play rồi thực thi module trên managed node theo connection/become.
- **Tiên quyết bắt buộc:** P02.C04.L03, P09.C02.L01.
- **Ranh giới:** Không thay Terraform bằng các lệnh tạo hạ tầng trong task.
- **Ngộ nhận:** SSH thành công tức là ứng dụng đã healthy.
- **Cách dạy:** Phân tích localhost fixture rồi mở rộng thành inventory hai host giả định.
- **Đánh giá:** Chứng minh host pattern, variable precedence và quyền thực thi.
- **Nối tới:** P10.C02.
- **Nguồn cũ:** Ch14.
- **Cây bài:**
  - `P10.C01.L01` **Topology** [reviewed_draft; 1 mục cũ; 2 claim] — inventory, host/group, SSH/local
  - `P10.C01.L02` **Đơn vị chạy** [reviewed_draft; 1 mục cũ; 1 claim] — play, task, module, facts
  - `P10.C01.L03` **Quyền/biến** [reviewed_draft; 1 mục cũ; 1 claim] — become, precedence, secret boundary

### P10.C02 — Hội tụ, handler và thất bại từng host [reviewed_draft]

- **Đích học:** Chứng minh lượt đầu changed, lượt hai ok và drift sửa đúng phạm vi.
- **Mô hình nối bài:** Module quan sát trạng thái; handler chỉ chạy khi được notify; failure từng host không rollback máy khác.
- **Tiên quyết bắt buộc:** P10.C01.L03, P05.C03.L03.
- **Ranh giới:** Service readiness ở P02; rollout fleet ở P10.C03.
- **Ngộ nhận:** changed=0 là dịch vụ khỏe; check mode giống apply thật.
- **Cách dạy:** Chạy playbook trên POSIX fixture và tạo drift quyền/nội dung.
- **Đánh giá:** Đọc recap, marker handler, mode và request độc lập.
- **Nối tới:** P10.C03.
- **Nguồn cũ:** Ch14.
- **Cây bài:**
  - `P10.C02.L01` **Idempotency** [reviewed_draft; 2 mục cũ; 4 claim] — ok/changed/failed và module contract
  - `P10.C02.L02` **Handler** [reviewed_draft; 2 mục cũ; 3 claim] — notify, thứ tự, restart đúng lúc
  - `P10.C02.L03` **Failure** [reviewed_draft; 2 mục cũ; 3 claim] — check/diff, partial host, hậu điều kiện

### P10.C03 — Vai trò, secrets và triển khai theo đợt [planned_new]

- **Đích học:** Tổ chức cấu hình nhiều host với blast radius kiểm soát được.
- **Mô hình nối bài:** Role đóng gói task/default/template; rolling serial và vault giảm rủi ro nhưng không tự bảo đảm health.
- **Tiên quyết bắt buộc:** P10.C02.L03, P06.C03.L03.
- **Ranh giới:** K8s deployment strategy ở P11 dùng controller khác.
- **Ngộ nhận:** Vault trong repo là đủ bảo mật secret lâu dài.
- **Cách dạy:** Thiết kế sửa config trên host thử, kiểm request rồi tới host còn lại.
- **Đánh giá:** Đề xuất rollback khi một host restart lỗi và bảo toàn secret.
- **Nối tới:** Tổng hợp cuối sách.
- **Nguồn cũ:** Ch14.
- **Cây bài:**
  - `P10.C03.L01` **Tái sử dụng** [planned_new; 1 mục cũ; 1 claim] — role, defaults/vars, tags
  - `P10.C03.L02` **Phân đợt** [planned_new; 1 mục cũ; 2 claim] — serial, max_fail_percentage, handler và health
  - `P10.C03.L03` **Secret** [planned_new; 0 mục cũ; 0 claim] — Vault, key custody, log redaction, rotation

## P11 — Kubernetes và cloud native

**Câu hỏi:** Khai báo biến thành Pod sẵn sàng phục vụ nhờ những vòng điều khiển nào?
**Mô hình:** API lưu spec, controller/scheduler/kubelet/dataplane hội tụ bất đồng bộ; status, endpoint và request là các chứng cứ khác nhau.
**Tiên quyết:** P02 Linux; P03 mạng; P07 container; P08 cloud; P06 release.
**Ranh giới:** Prometheus chuyên sâu ở P12; trước HPA chỉ dạy CPU time/request/resource metrics tối thiểu.
**Năng lực ra:** Chẩn đoán apply xanh nhưng request hỏng qua object, node, network, storage và dữ liệu.
**Ngộ nhận cần sửa:** Running/Bound/Programmed hoặc helm upgrade xanh đồng nghĩa người dùng thành công.
**Chuyển tiếp:** Cho observability, SRE và Kubernetes security.

### P11.C01 — API, etcd và reconciliation [reviewed_draft]

- **Đích học:** Theo một spec từ apply tới các controller và node.
- **Mô hình nối bài:** API server lưu object; controller quan sát rồi thu hẹp sai lệch; status là ảnh chụp bất đồng bộ.
- **Tiên quyết bắt buộc:** P07.C01.L03, P06.C03.L02.
- **Ranh giới:** Scheduler, Service và storage có chương riêng.
- **Ngộ nhận:** Apply thành công là workload chạy; resourceVersion là đồng hồ toàn cục.
- **Cách dạy:** Điều tra chuỗi Deployment→ReplicaSet→Pod với generation/status.
- **Đánh giá:** Đọc owner, selector, observedGeneration và giới hạn của snapshot.
- **Nối tới:** P11.C02, P11.C06, P11.C07, P12.C03, P14.C01.
- **Nguồn cũ:** Ch15.
- **Cây bài:**
  - `P11.C01.L01` **Control plane** [reviewed_draft; 1 mục cũ; 3 claim] — API/admission, etcd, controller manager
  - `P11.C01.L02` **Reconciliation** [reviewed_draft; 1 mục cũ; 2 claim] — spec/status, watch, retry, generation
  - `P11.C01.L03` **Node boundary** [reviewed_draft; 1 mục cũ; 2 claim] — scheduler, kubelet, runtime và đường dữ liệu

### P11.C02 — Pod, Deployment và readiness [reviewed_draft]

- **Đích học:** Phân biệt Running, Ready, Available và rollout complete.
- **Mô hình nối bài:** Pod là run unit; ReplicaSet giữ số; Deployment quản bản thay thế, probe xác định chấp nhận lưu lượng.
- **Tiên quyết bắt buộc:** P11.C01.L03, P07.C03.L01.
- **Ranh giới:** Service endpoint ở P11.C04.
- **Ngộ nhận:** Restart tự phục hồi dữ liệu trong emptyDir.
- **Cách dạy:** Sửa readiness sai trong k8s-ch15-incident.yaml rồi kiểm status từng cấp.
- **Đánh giá:** Chỉ ra vì sao Available không chứng minh request nghiệp vụ.
- **Nối tới:** P11.C03, P11.C04, P11.C05, P11.C08.
- **Nguồn cũ:** Ch15, Ch09.
- **Cây bài:**
  - `P11.C02.L01` **Workload objects** [reviewed_draft; 1 mục cũ; 3 claim] — Pod, ReplicaSet, Deployment, owner/selector
  - `P11.C02.L02` **Probe** [reviewed_draft; 2 mục cũ; 1 claim] — startup, liveness, readiness và failure mode
  - `P11.C02.L03` **Rollout** [reviewed_draft; 2 mục cũ; 2 claim] — revision, surge/unavailable, progress deadline và dừng

### P11.C03 — Scheduler và ngân sách tài nguyên [reviewed_draft]

- **Đích học:** Giải thích Pending vì requests/taint dù CPU tức thời thấp.
- **Mô hình nối bài:** Filter/score dùng allocatable, requests và ràng buộc; cgroup limit có thể gây throttle sau khi chạy.
- **Tiên quyết bắt buộc:** P11.C02.L01, P02.C03.L03, P07.C01.L03.
- **Ranh giới:** HPA ở P11.C06; metrics server tối thiểu ở bài 3.
- **Ngộ nhận:** kubectl top 10% giúp scheduler bỏ qua requests.
- **Cách dạy:** Tính node A/B và đối chiếu FailedScheduling, cpu.stat.
- **Đánh giá:** Chọn node khả thi và nêu rủi ro sửa request/limit.
- **Nối tới:** P11.C06, P12.C01.
- **Nguồn cũ:** Ch16, Ch10, Ch02.
- **Cây bài:**
  - `P11.C03.L01` **Placement** [reviewed_draft; 2 mục cũ; 3 claim] — requests, allocatable, taint/toleration, affinity
  - `P11.C03.L02` **Runtime budget** [reviewed_draft; 1 mục cũ; 4 claim] — CPU/memory limits, QoS, OOM/throttle
  - `P11.C03.L03` **Resource metric tối thiểu** [reviewed_draft; 1 mục cũ; 2 claim] — CPU time per window, metrics.k8s.io, timestamp/missing sample

### P11.C04 — Service, EndpointSlice và NetworkPolicy [reviewed_draft]

- **Đích học:** Lần theo tên Service tới Pod socket và policy chặn.
- **Mô hình nối bài:** DNS chỉ trả tên; selector tạo endpoint; node dataplane và policy xử lý packet.
- **Tiên quyết bắt buộc:** P11.C02.L02, P03.C02.L03, P03.C01.L04.
- **Ranh giới:** Gateway edge ở P11.C07.
- **Ngộ nhận:** Service có IP nghĩa là có backend; Pod Ready đảm bảo mọi namespace nối được.
- **Cách dạy:** Chẩn đoán typo app=atals cùng probe sai và một client khác namespace.
- **Đánh giá:** Xác định chặng DNS/selector/endpoint/port/policy/call.
- **Nối tới:** P11.C07, P14.C04.
- **Nguồn cũ:** Ch15, Ch16.
- **Cây bài:**
  - `P11.C04.L01` **Discovery** [reviewed_draft; 2 mục cũ; 3 claim] — DNS, Service selector, EndpointSlice
  - `P11.C04.L02` **Dataplane** [reviewed_draft; 1 mục cũ; 1 claim] — ClusterIP, kube-proxy/CNI theo triển khai, targetPort/MTU
  - `P11.C04.L03` **Policy** [reviewed_draft; 2 mục cũ; 1 claim] — ingress/egress, scope và thử từ đúng nguồn

### P11.C05 — PVC, CSI và dữ liệu workload [reviewed_draft]

- **Đích học:** Phân biệt PVC Bound với volume mount và dữ liệu phục hồi được.
- **Mô hình nối bài:** Binding, provision, attach/mount, quyền và backup là các bước khác nhau.
- **Tiên quyết bắt buộc:** P11.C02.L01, P08.C04.L03, P07.C03.L03.
- **Ranh giới:** DR ở P13.C03.
- **Ngộ nhận:** RWO nghĩa chỉ một Pod; StatefulSet tự backup.
- **Cách dạy:** Điều tra FailedMount, reclaim policy và Pod replacement.
- **Đánh giá:** Đề xuất hậu điều kiện dữ liệu trước khi thay Pod.
- **Nối tới:** P13.C03.
- **Nguồn cũ:** Ch15, Ch16.
- **Cây bài:**
  - `P11.C05.L01` **Tài nguyên** [reviewed_draft; 1 mục cũ; 3 claim] — PV, PVC, StorageClass, access mode
  - `P11.C05.L02` **Thực thi** [reviewed_draft; 2 mục cũ; 1 claim] — CSI, topology, attach/mount, permissions
  - `P11.C05.L03` **Vòng đời** [reviewed_draft; 2 mục cũ; 2 claim] — StatefulSet identity, reclaim, backup/restore

### P11.C06 — HPA và điều khiển mở rộng [reviewed_draft]

- **Đích học:** Tính replica từ CPU utilization khi biết request và chất lượng metric.
- **Mô hình nối bài:** Controller dùng sampled resource metric và CPU request làm mẫu số, rồi chịu tolerance/stabilization và khả năng scheduler.
- **Tiên quyết bắt buộc:** P11.C01.L02, P11.C03.L03, P11.C03.L01.
- **Ranh giới:** Prometheus/PromQL sâu ở P12, không phải tiên quyết.
- **Ngộ nhận:** HPA có desiredReplicas lớn hơn nghĩa user latency giảm ngay.
- **Cách dạy:** Tính ví dụ 300m/450m/150m trên request 500m rồi kiểm Pending.
- **Đánh giá:** Nêu quyết định cơ sở và các lý do status cuối có thể khác.
- **Nối tới:** Tổng hợp cuối sách.
- **Nguồn cũ:** Ch16.
- **Cây bài:**
  - `P11.C06.L01` **Phép đo** [reviewed_draft; 1 mục cũ; 1 claim] — usage, request, missing/stale metric
  - `P11.C06.L02` **Vòng tính** [reviewed_draft; 1 mục cũ; 3 claim] — average utilization, ceil, bounds/tolerance
  - `P11.C06.L03` **Hội tụ** [reviewed_draft; 1 mục cũ; 0 claim] — scale target, scheduler, readiness, latency và giới hạn

### P11.C07 — Gateway API và ranh giới request ngoài cluster [reviewed_draft]

- **Đích học:** Phân biệt controller conditions với đường request của client.
- **Mô hình nối bài:** GatewayClass/controller, listener, Route, Service và DNS/Host/SNI phải cùng khớp theo generation.
- **Tiên quyết bắt buộc:** P11.C04.L03, P03.C04.L03, P11.C01.L02.
- **Ranh giới:** Helm chỉ đóng gói cấu hình ở P11.C08.
- **Ngộ nhận:** Programmed=True chứng minh DNS/TLS/Pod phục vụ.
- **Cách dạy:** Điều tra revision đổi hostname nhưng DNS chưa đổi.
- **Đánh giá:** Xác nhận Accepted/ResolvedRefs, quyền cross-namespace và request từ client.
- **Nối tới:** Tổng hợp cuối sách.
- **Nguồn cũ:** Ch17.
- **Cây bài:**
  - `P11.C07.L01` **API objects** [reviewed_draft; 2 mục cũ; 5 claim] — GatewayClass, Gateway, listener, HTTPRoute
  - `P11.C07.L02` **Attachment** [reviewed_draft; 3 mục cũ; 3 claim] — allowedRoutes, parentRefs, ReferenceGrant và status
  - `P11.C07.L03` **Request path** [reviewed_draft; 2 mục cũ; 1 claim] — DNS, Host/SNI, dataplane, Service và lỗi

### P11.C08 — Helm chart và vòng đời release [reviewed_draft]

- **Đích học:** Theo chart/values đến manifest/revision rồi phân biệt với trạng thái thật.
- **Mô hình nối bài:** Render là đầu vào API; release history giữ manifest/config, rollback tạo revision chứ không đảo dữ liệu.
- **Tiên quyết bắt buộc:** P11.C02.L03, P06.C04.L03, P04.C01.L03.
- **Ranh giới:** Gateway API chỉ là ví dụ chart hiện có, không là tiên quyết Helm.
- **Ngộ nhận:** helm template chạy xong chứng minh CRD/controller tồn tại.
- **Cách dạy:** Đọc chart atlas-gateway, upgrade/rollback giả định và kiểm request.
- **Đánh giá:** Đề xuất hậu điều kiện cho revision, object, endpoint, dữ liệu.
- **Nối tới:** P15.C01.
- **Nguồn cũ:** Ch17.
- **Cây bài:**
  - `P11.C08.L01` **Chart** [reviewed_draft; 2 mục cũ; 3 claim] — metadata, template, values, dependency
  - `P11.C08.L02` **Release** [reviewed_draft; 1 mục cũ; 1 claim] — install, upgrade, wait, history và revision
  - `P11.C08.L03` **Rollback** [reviewed_draft; 2 mục cũ; 3 claim] — manifest, owner, data compatibility và request

## P12 — Observability và telemetry

**Câu hỏi:** Dữ liệu quan sát được tạo, vận chuyển và diễn giải có giới hạn nào?
**Mô hình:** Metric tổng hợp, log sự kiện và trace đường request là các phép chiếu có sai lệch lấy mẫu, mất dữ liệu và khác thời gian.
**Tiên quyết:** P03 request; P05 status; P11 workload; P01 CPU time.
**Ranh giới:** SLO/incident response ở P13 dùng tín hiệu đã được kiểm định ở đây.
**Năng lực ra:** Tính rate/p95, tìm request, đánh giá thiếu dữ liệu và hỏng pipeline quan sát.
**Ngộ nhận cần sửa:** Dashboard xanh hoặc thiếu span chứng minh hệ thống khỏe hoặc thao tác không chạy.
**Chuyển tiếp:** Cho SLI/SLO, alerting, incident và cost of telemetry.

### P12.C01 — Phép đo, nhãn và chuỗi thời gian [reviewed_draft]

- **Đích học:** Định nghĩa phép đo và rủi ro sai lệch trước khi xem dashboard.
- **Mô hình nối bài:** Instrument/exporter phát metric; scrape/sampling tạo chuỗi hữu hạn theo nhãn và thời gian.
- **Tiên quyết bắt buộc:** P01.C01.L02, P11.C03.L03.
- **Ranh giới:** HPA chỉ dùng resource metric cơ sở đã học; đây là mô hình quan sát sâu.
- **Ngộ nhận:** Một mẫu cao/thấp chứng minh tải hoặc root cause.
- **Cách dạy:** Đọc metrics-ch18.prom và đổi request_id thành nhãn để tính cardinality.
- **Đánh giá:** Phân biệt counter/gauge/histogram, reset và mẫu bị thiếu.
- **Nối tới:** P12.C02.
- **Nguồn cũ:** Ch18.
- **Cây bài:**
  - `P12.C01.L01` **Đo** [reviewed_draft; 1 mục cũ; 2 claim] — counter, gauge, histogram, units
  - `P12.C01.L02` **Tập hợp** [reviewed_draft; 1 mục cũ; 2 claim] — labels, cardinality, identity
  - `P12.C01.L03` **Thu thập** [reviewed_draft; 1 mục cũ; 3 claim] — scrape, target discovery, up và cửa sổ

### P12.C02 — Prometheus, PromQL và Grafana [reviewed_draft]

- **Đích học:** Tính rate, tỷ lệ lỗi và p95 có giới hạn từ mẫu thật/giả định.
- **Mô hình nối bài:** Query biến chuỗi có cửa sổ thành ước lượng; panel chỉ là phép chiếu có filter/time range.
- **Tiên quyết bắt buộc:** P12.C01.L03.
- **Ranh giới:** SLI/SLO ở P13.
- **Ngộ nhận:** Trung bình p95 của Pod là p95 toàn dịch vụ.
- **Cách dạy:** Tính CSV Ch18 rồi thay một target bằng up=0.
- **Đánh giá:** Sửa query rate(sum()) và nêu bias do mất scrape.
- **Nối tới:** P12.C04, P13.C01, P13.C04.
- **Nguồn cũ:** Ch18.
- **Cây bài:**
  - `P12.C02.L01` **PromQL** [reviewed_draft; 2 mục cũ; 4 claim] — rate/increase, aggregation, reset
  - `P12.C02.L02` **Histogram** [reviewed_draft; 1 mục cũ; 2 claim] — bucket cumulative, quantile interpolation
  - `P12.C02.L03` **Dashboard** [reviewed_draft; 2 mục cũ; 3 claim] — selector, step, data source và missing series

### P12.C03 — Logs, traces và OpenTelemetry [reviewed_draft]

- **Đích học:** Nối log và span của một request, kể cả khi một nhánh timeout nhưng cuối trả 200.
- **Mô hình nối bài:** Trace mô tả quan hệ parent/child; log mô tả sự kiện; SDK/Collector/backend có đường lỗi riêng.
- **Tiên quyết bắt buộc:** P03.C04.L03, P11.C01.L02.
- **Ranh giới:** Grafana dashboard không là điều kiện để hiểu propagation; alert policy ở P12.C04.
- **Ngộ nhận:** Cộng mọi span duration ra client latency; sampled=01 bảo đảm trace được lưu.
- **Cách dạy:** Dùng trace-ch19.csv và logs-ch19.json để tính và chẩn đoán missing span.
- **Đánh giá:** Xác định 420 ms end-to-end, chỗ thiếu span và giới hạn kết luận.
- **Nối tới:** P12.C04, P13.C02, P14.C02.
- **Nguồn cũ:** Ch19.
- **Cây bài:**
  - `P12.C03.L01` **Log** [reviewed_draft; 2 mục cũ; 3 claim] — timestamp/severity/context/PII
  - `P12.C03.L02` **Trace** [reviewed_draft; 2 mục cũ; 8 claim] — span parent, W3C traceparent, sampling
  - `P12.C03.L03` **Pipeline** [reviewed_draft; 3 mục cũ; 8 claim] — OTel API/SDK, OTLP, Collector queue/retry/backend

### P12.C04 — Alerting và sức khỏe pipeline quan sát [planned_new]

- **Đích học:** Tạo tín hiệu hành động thay vì báo động từ một dashboard.
- **Mô hình nối bài:** Rule evaluation, routing và telemetry pipeline đều có độ trễ, mất dữ liệu và quyền truy cập riêng.
- **Tiên quyết bắt buộc:** P12.C02.L03, P12.C03.L03.
- **Ranh giới:** Burn-rate SLO policy ở P13.C01.
- **Ngộ nhận:** No data luôn là healthy; alert sent tức là người trực đã nhận và hiểu.
- **Cách dạy:** Failure injection mất scrape/queue đầy/alert route sai.
- **Đánh giá:** Viết test alert rule, no-data policy và đường nhận thông báo.
- **Nối tới:** Tổng hợp cuối sách.
- **Nguồn cũ:** Ch18, Ch19.
- **Cây bài:**
  - `P12.C04.L01` **Rule** [planned_new; 2 mục cũ; 1 claim] — threshold, duration, missing data
  - `P12.C04.L02` **Routing** [planned_new; 0 mục cũ; 0 claim] — group, inhibit, silences, escalation
  - `P12.C04.L03` **Pipeline** [planned_new; 1 mục cũ; 0 claim] — export failure, queue/drop, retention và telemetry cost

## P13 — SRE và phục hồi

**Câu hỏi:** Độ tin cậy được định nghĩa, bảo vệ và khôi phục ra sao?
**Mô hình:** SLI/SLO định nghĩa tác động người dùng; response dùng chứng cứ, DR dùng bản sao có thử khôi phục, capacity dùng tải và giới hạn.
**Tiên quyết:** P06 release; P08 data/availability; P11 control loops; P12 telemetry.
**Ranh giới:** Các cơ chế backup/rollout được dùng làm quyết định vận hành, không giảng lại API sản phẩm.
**Năng lực ra:** Lập error budget, điều phối sự cố và chứng minh phục hồi dữ liệu/nghiệp vụ.
**Ngộ nhận cần sửa:** HA, replication và rollback đều là backup; postmortem là tìm người sai.
**Chuyển tiếp:** Cho thiết kế production và đánh giá rủi ro bảo mật.

### P13.C01 — SLI, SLO và error budget [planned_new]

- **Đích học:** Chọn phép đo gần trải nghiệm người dùng và tính burn rate.
- **Mô hình nối bài:** SLI là tử/mẫu có phạm vi; SLO đặt ngưỡng; error budget cho biết rủi ro thay đổi còn chấp nhận.
- **Tiên quyết bắt buộc:** P12.C02.L03, P06.C03.L03.
- **Ranh giới:** Alert rule mechanics ở P12.C04; không lặp PromQL nền.
- **Ngộ nhận:** SLO 99.9% nghĩa không bao giờ được lỗi.
- **Cách dạy:** Tính ngân sách theo request và so client/server measurement.
- **Đánh giá:** Phản biện một SLI loại bỏ request thất bại do target biến mất.
- **Nối tới:** P13.C02, P13.C04.
- **Nguồn cũ:** Cần biên soạn mới.
- **Cây bài:**
  - `P13.C01.L01` **SLI** [planned_new; 0 mục cũ; 0 claim] — good/total events, latency, availability, exclusion
  - `P13.C01.L02` **SLO** [planned_new; 0 mục cũ; 0 claim] — window, target, budget
  - `P13.C01.L03` **Burn** [planned_new; 0 mục cũ; 0 claim] — rate, multi-window alert, change policy

### P13.C02 — Incident response và postmortem [planned_new]

- **Đích học:** Tổ chức phát hiện, phân vai, giảm tác động và học từ sự cố.
- **Mô hình nối bài:** Incident là chuỗi quyết định dưới thông tin thiếu; timeline/bằng chứng và communication giảm lỗi thứ cấp.
- **Tiên quyết bắt buộc:** P13.C01.L03, P12.C03.L03, P06.C04.L03.
- **Ranh giới:** DR chi tiết ở P13.C03.
- **Ngộ nhận:** Postmortem là tìm cá nhân chịu lỗi; root cause luôn đơn nhất.
- **Cách dạy:** Điều tra request chậm qua metric/log/trace và change timeline.
- **Đánh giá:** Lập runbook với trigger, stop, verification và mốc thông báo.
- **Nối tới:** P15.C03.
- **Nguồn cũ:** Ch09, Ch19.
- **Cây bài:**
  - `P13.C02.L01` **Phản ứng** [planned_new; 0 mục cũ; 0 claim] — detect, triage, severity, incident command
  - `P13.C02.L02` **Giảm tác động** [planned_new; 0 mục cũ; 0 claim] — rollback/isolation, evidence preservation, status updates
  - `P13.C02.L03` **Học lại** [planned_new; 0 mục cũ; 0 claim] — timeline, contributing factors, action ownership

### P13.C03 — Backup, DR và phục hồi dữ liệu [planned_new]

- **Đích học:** Phân biệt availability, durability, RPO, RTO và restore kiểm chứng.
- **Mô hình nối bài:** Bản sao nhất quán độc lập miền lỗi mới cho phép khôi phục; replication thường sao lỗi/xóa theo.
- **Tiên quyết bắt buộc:** P08.C04.L03, P11.C05.L03, P06.C04.L03.
- **Ranh giới:** Cloud storage API chi tiết ở P08.
- **Ngộ nhận:** Multi-AZ hoặc PVC Bound chứng minh restore được.
- **Cách dạy:** Diễn tập mất AZ và xóa object, kiểm manifest dữ liệu trước/sau.
- **Đánh giá:** Đề xuất RPO/RTO thực tế và phép thử restore.
- **Nối tới:** P15.C01.
- **Nguồn cũ:** Ch11, Ch12, Ch13, Ch16.
- **Cây bài:**
  - `P13.C03.L01` **Mục tiêu** [planned_new; 0 mục cũ; 0 claim] — RPO, RTO, failure domain
  - `P13.C03.L02` **Bản sao** [planned_new; 0 mục cũ; 0 claim] — snapshot, versioning, immutable/offsite, secret/key
  - `P13.C03.L03` **Diễn tập** [planned_new; 0 mục cũ; 0 claim] — restore, checksum, application consistency và request

### P13.C04 — Hiệu năng, capacity và thử giới hạn [planned_new]

- **Đích học:** Phân biệt nghẽn CPU, I/O, hàng đợi và giới hạn dữ liệu khi tải tăng.
- **Mô hình nối bài:** Demand, service time, concurrency và queue làm tail latency khác trung bình; capacity là quyết định theo SLO.
- **Tiên quyết bắt buộc:** P02.C03.L03, P12.C02.L02, P13.C01.L03.
- **Ranh giới:** Cost strategy ở P15.C02.
- **Ngộ nhận:** Thêm replica luôn giảm latency hoặc failure injection production là vô hại.
- **Cách dạy:** Đặt thí nghiệm tải có baseline, stop rule và đo hậu trạng thái.
- **Đánh giá:** Chọn chỉ số để chứng minh bottleneck rồi dự báo headroom.
- **Nối tới:** P15.C02.
- **Nguồn cũ:** Ch02, Ch16, Ch18.
- **Cây bài:**
  - `P13.C04.L01` **Workload** [planned_new; 1 mục cũ; 0 claim] — arrival rate, service time, concurrency
  - `P13.C04.L02` **Capacity** [planned_new; 0 mục cũ; 0 claim] — queueing, saturation, autoscale lag
  - `P13.C04.L03` **Experiment** [planned_new; 0 mục cũ; 0 claim] — load test, fault injection, blast radius, recovery

## P14 — Security và DevSecOps

**Câu hỏi:** Mối đe dọa đi qua identity, artifact, secret và runtime thế nào?
**Mô hình:** Đặt trust boundary và tài sản trước công cụ; giảm quyền, chứng minh provenance, kiểm soát secret và đo hiệu lực policy.
**Tiên quyết:** P03 TLS; P04 Git; P06 build; P07 image; P08 IAM; P11 Kubernetes; P13 incident.
**Ranh giới:** IAM AWS nền tảng ở P08; đây là phân tích đe dọa liên miền và kiểm soát.
**Năng lực ra:** Dựng threat model và bằng chứng về quyền, dữ liệu, artifact và policy.
**Ngộ nhận cần sửa:** Một scanner xanh hoặc một bản ký đủ chứng minh ứng dụng an toàn.
**Chuyển tiếp:** Cho duyệt kiến trúc production và response sự cố bảo mật.

### P14.C01 — Threat model và quyền tối thiểu [planned_new]

- **Đích học:** Nhận diện tài sản, actor, trust boundary và đường lạm dụng.
- **Mô hình nối bài:** Mọi quyền là quan hệ principal/action/resource/context; defense có giả định và bypass riêng.
- **Tiên quyết bắt buộc:** P08.C01.L03, P03.C03.L02, P11.C01.L01.
- **Ranh giới:** Chi tiết IAM syntax ở P08, RBAC cụ thể ở P14.C04.
- **Ngộ nhận:** Ẩn endpoint hoặc dùng private subnet là đủ kiểm soát truy cập.
- **Cách dạy:** Vẽ luồng request và đánh dấu nơi xác thực/ủy quyền.
- **Đánh giá:** Viết threat scenario và phép thử denial/allow theo least privilege.
- **Nối tới:** P14.C02.
- **Nguồn cũ:** Ch12.
- **Cây bài:**
  - `P14.C01.L01` **Bề mặt** [planned_new; 0 mục cũ; 0 claim] — asset, actor, entrypoint, data flow
  - `P14.C01.L02` **Quyền** [planned_new; 0 mục cũ; 0 claim] — principal, role, policy evaluation, separation
  - `P14.C01.L03` **Bằng chứng** [planned_new; 0 mục cũ; 0 claim] — audit log, negative test, review và thay đổi

### P14.C02 — Secret và bảo vệ dữ liệu [planned_new]

- **Đích học:** Lần theo secret từ tạo tới sử dụng, log, rotation và thu hồi.
- **Mô hình nối bài:** Secret nằm trong nhiều bản sao: repo, CI, state, environment, memory, telemetry, backup.
- **Tiên quyết bắt buộc:** P14.C01.L03, P09.C02.L03, P12.C03.L01.
- **Ranh giới:** Không đồng nhất mã hóa-at-rest với quản lý vòng đời khóa.
- **Ngộ nhận:** Mã hóa state là đủ khi secret còn trong log.
- **Cách dạy:** Threat-model một token đi qua pipeline và Terraform/Ansible/K8s.
- **Đánh giá:** Đề xuất redaction, scope, rotation và bằng chứng không rò.
- **Nối tới:** Tổng hợp cuối sách.
- **Nguồn cũ:** Ch08, Ch11, Ch13, Ch14, Ch19.
- **Cây bài:**
  - `P14.C02.L01` **Vòng đời** [planned_new; 0 mục cũ; 0 claim] — issuance, storage, use, rotate, revoke
  - `P14.C02.L02` **Bề mặt lộ** [planned_new; 2 mục cũ; 1 claim] — CI log, env, state, image layer, trace
  - `P14.C02.L03` **Kiểm soát** [planned_new; 0 mục cũ; 0 claim] — KMS/Vault, encryption, access audit, recovery

### P14.C03 — Software supply chain [planned_new]

- **Đích học:** Truy vết source→dependency→build→image→deploy không đánh tráo artifact.
- **Mô hình nối bài:** Digest, provenance, SBOM, signature và policy là bằng chứng có phạm vi, không thay kiểm thử runtime.
- **Tiên quyết bắt buộc:** P06.C02.L03, P07.C02.L03, P04.C01.L03.
- **Ranh giới:** Kubernetes admission ở P14.C04.
- **Ngộ nhận:** Scanner xanh hoặc chữ ký hợp lệ chứng minh image không có lỗi.
- **Cách dạy:** Kiểm một artifact có dependency đổi ngầm và tag bị dịch.
- **Đánh giá:** Chỉ ra chuỗi bằng chứng và điểm còn chưa xác minh.
- **Nối tới:** P14.C04, P15.C03.
- **Nguồn cũ:** Ch09, Ch11.
- **Cây bài:**
  - `P14.C03.L01` **Nguồn** [planned_new; 0 mục cũ; 0 claim] — dependency pin, SBOM, license/vulnerability
  - `P14.C03.L02` **Build** [planned_new; 0 mục cũ; 0 claim] — isolation, provenance, attestation, signing
  - `P14.C03.L03` **Deploy** [planned_new; 0 mục cũ; 0 claim] — digest verify, admission policy, revocation

### P14.C04 — Cloud/Kubernetes runtime hardening [planned_new]

- **Đích học:** Đặt ranh giới quyền và mạng trên workload thật.
- **Mô hình nối bài:** Policy admission, ServiceAccount/RBAC, security context, NetworkPolicy và cloud identity chặn các đường khác nhau.
- **Tiên quyết bắt buộc:** P14.C03.L03, P11.C04.L03, P08.C02.L03.
- **Ranh giới:** Không lặp cơ chế scheduler hay API controller.
- **Ngộ nhận:** Pod chạy non-root thì không thể đọc secret hoặc đi ra internet.
- **Cách dạy:** Dựng chuỗi tấn công từ image tới API/data và thử policy âm.
- **Đánh giá:** Lập ma trận kiểm soát và giới hạn thực thi của plugin/provider.
- **Nối tới:** P15.C01.
- **Nguồn cũ:** Ch15, Ch16, Ch17.
- **Cây bài:**
  - `P14.C04.L01` **Admission** [planned_new; 0 mục cũ; 0 claim] — PSS/policy engine và image policy
  - `P14.C04.L02` **Runtime** [planned_new; 0 mục cũ; 0 claim] — SA/RBAC, securityContext, seccomp, volume
  - `P14.C04.L03` **Network/cloud** [planned_new; 0 mục cũ; 0 claim] — NetworkPolicy, workload identity, SG và audit

## P15 — Thiết kế và vận hành production

**Câu hỏi:** Làm sao ghép các cơ chế thành hệ thống đáng tin, đo được và có chi phí hợp lý?
**Mô hình:** Luồng request, dữ liệu và control plane phải cùng được vẽ với miền lỗi, ngân sách, chủ sở hữu và kế hoạch phục hồi.
**Tiên quyết:** P01–P14; dùng sau khi có SLO, threat model, IaC và bằng chứng vận hành.
**Ranh giới:** Không thêm công nghệ mới làm mục tiêu; tích hợp và phản biện đánh đổi.
**Năng lực ra:** Bảo vệ một kiến trúc, canary, DR và cost plan trước tình huống thay đổi tải/lỗi.
**Ngộ nhận cần sửa:** Nhiều lớp công cụ tự động đem lại độ tin cậy mà không cần kiểm chứng đầu cuối.
**Chuyển tiếp:** Kết thúc sách bằng capstone có bằng chứng, giới hạn và quyết định vận hành.

### P15.C01 — Thiết kế một dịch vụ production [planned_new]

- **Đích học:** Bảo vệ đường request, dữ liệu và control plane trong một kiến trúc.
- **Mô hình nối bài:** Mỗi thành phần có owner, failure domain, SLO, trust boundary và phương án giảm tác động.
- **Tiên quyết bắt buộc:** P13.C03.L03, P14.C04.L03, P11.C08.L03.
- **Ranh giới:** Không dạy lại cú pháp Terraform/Helm.
- **Ngộ nhận:** Một sơ đồ thành phần đẹp tự chứng minh hệ thống chịu lỗi.
- **Cách dạy:** Thiết kế rồi đi qua ba sự cố đối nghịch: mất AZ, cert lỗi, deploy hỏng.
- **Đánh giá:** Lập bảng tradeoff với bằng chứng cho từng control.
- **Nối tới:** P15.C02.
- **Nguồn cũ:** Cần biên soạn mới.
- **Cây bài:**
  - `P15.C01.L01` **Yêu cầu** [planned_new; 0 mục cũ; 0 claim] — traffic, dữ liệu, compliance, budget
  - `P15.C01.L02` **Kiến trúc** [planned_new; 0 mục cũ; 0 claim] — edge, compute, data, network và control plane
  - `P15.C01.L03` **Đánh giá** [planned_new; 0 mục cũ; 0 claim] — failure domain, runbook, ownership, test plan

### P15.C02 — Mở rộng và tối ưu chi phí có ràng buộc [planned_new]

- **Đích học:** Chọn năng lực đủ SLO trong giới hạn tiền và vận hành.
- **Mô hình nối bài:** Capacity, autoscale lag, redundancy và telemetry/egress/storage retention đều tiêu ngân sách.
- **Tiên quyết bắt buộc:** P15.C01.L03, P13.C04.L03, P08.C04.L03.
- **Ranh giới:** Không bịa bảng giá; dùng biến và công thức có Region/time.
- **Ngộ nhận:** Giảm chi phí bằng cách tắt backup hoặc giảm replica luôn tối ưu.
- **Cách dạy:** So ba phương án từ số liệu workload, nêu dữ liệu giá cần cập nhật.
- **Đánh giá:** Tính điểm hòa vốn và rủi ro mất SLO/DR.
- **Nối tới:** P15.C03.
- **Nguồn cũ:** Cần biên soạn mới.
- **Cây bài:**
  - `P15.C02.L01` **Mô hình tải** [planned_new; 0 mục cũ; 0 claim] — peak, headroom, burst, queue
  - `P15.C02.L02` **Mô hình tiền** [planned_new; 0 mục cũ; 0 claim] — compute, storage, data transfer, observability
  - `P15.C02.L03` **Quyết định** [planned_new; 0 mục cũ; 0 claim] — cost per outcome, stop rule, kiểm số liệu giá

### P15.C03 — Capstone: thay đổi, sự cố và phục hồi [planned_new]

- **Đích học:** Chứng minh toàn hành trình từ commit đến phục hồi bằng artifact và phép đo.
- **Mô hình nối bài:** Một change record nối source, build, IaC, rollout, telemetry, incident và dữ liệu.
- **Tiên quyết bắt buộc:** P15.C02.L03, P13.C02.L03, P14.C03.L03.
- **Ranh giới:** Không coi mô phỏng là production certification.
- **Ngộ nhận:** Mọi test xanh loại bỏ nhu cầu quan sát người dùng.
- **Cách dạy:** Đưa cùng một dịch vụ qua rollout, failure injection giới hạn, restore và review.
- **Đánh giá:** Nộp evidence ledger, kết quả âm/dương, giới hạn và quyết định vận hành.
- **Nối tới:** Tổng hợp cuối sách.
- **Nguồn cũ:** Cần biên soạn mới.
- **Cây bài:**
  - `P15.C03.L01` **Chuẩn bị** [planned_new; 0 mục cũ; 0 claim] — source/digest, policy, state, backup, SLO
  - `P15.C03.L02` **Thực thi** [planned_new; 0 mục cũ; 0 claim] — deploy, metric/log/trace, stop/rollback
  - `P15.C03.L03` **Bảo vệ** [planned_new; 0 mục cũ; 0 claim] — restore, security check, postmortem và chi phí
  - `P15.C03.L04` **Kiểm toán** [planned_new; 0 mục cũ; 0 claim] — evidence ledger, phép kiểm âm/dương, SKIP, stop rule và quyết định vận hành
