# Bản đồ trực quan hóa cho A2

**Quy tắc chọn:** chỉ trực quan hóa khi vị trí, thứ tự, trạng thái, quan hệ nhân quả hoặc số liệu khó đọc hơn trong văn xuôi. Đây là 43 ứng viên: 29 sơ đồ kỹ thuật/luồng/trạng thái, 7 biểu đồ định lượng từ dữ liệu, 4 bảng hoặc bảng kết hợp sơ đồ, 3 minh họa mở Phần có thể bỏ. Đây là danh sách có hợp đồng kiểm chứng, **không phải quota**. `P0` cần trước khi di chuyển khối tương ứng; `P1` cần trước khi nghiệm thu Phần; `P2` là phương án nghệ thuật/đào sâu có thể bỏ nếu không giúp hiểu. Hình kỹ thuật xuất SVG/vector có source chỉnh được; đồ thị từ dữ liệu phải lưu dữ liệu và mã dựng; ảnh thực chỉ từ thí nghiệm được phép có metadata; nghệ thuật không được mang claim kỹ thuật. Không dùng ASCII art làm hình xuất bản. Các `source_map`/URL chỉ ở hồ sơ A2, không vào PDF.

## Máy, Linux và mạng

### V01 · `P01.C01.L02` · CPU time và wall time
- **Hỏi / dạng:** vì sao CPU thấp mà request chậm? Timeline định lượng từ ví dụ Ch2.5, không phải ảnh máy thật.
- **Bắt buộc:** cùng trục 60 giây, phần running/runnable/blocked, CPU time và wall latency; chỉ cộng các đoạn không chồng lấn, đánh dấu khoảng chưa đo. Mũi tên “chờ” là quan sát, không tự gán I/O.
- **Kiểm / sai lệch:** `chapters/02#2.1,#2.5`, bảng và lời giải C2.4; sai nếu biến PSI 2%/30% thành % CPU. **Medium:** biểu đồ từ dữ liệu giả định, vector. **P0:** là mô hình chẩn đoán đầu sách.

### V02 · `P01.C02.L02` · fork/execve/wait
- **Hỏi / dạng:** PID, giá trị trả về và đường lỗi khác nhau thế nào? Sequence/state diagram hai nhánh cha/con.
- **Bắt buộc:** fork cha nhận child PID, con nhận 0, lỗi cha −1; execve thành công không trả về, lỗi trả −1/exception; wait/exit 0 hoặc 127; giữ PID của con sau execve. Nhánh thành công và lỗi không đồng thời trên cùng một lần chạy.
- **Kiểm / sai lệch:** `examples/fork_exec.py`, `source_map` Ch1.2, man-pages fork/execve; sai nếu vẽ exec tạo process mới. **Medium:** SVG. **P0:** chặn ngộ nhận gốc.

### V03 · `P02.C01.L02` · path, inode và descriptor
- **Hỏi / dạng:** vì sao log cũ vẫn nhận byte sau rename? Sơ đồ đối tượng với hai ảnh thời gian.
- **Bắt buộc:** pathname→directory entry→inode; FD của process→open file description→inode; rename đổi entry, không làm FD mở trỏ sang tên mới; phân biệt hard/symlink.
- **Kiểm / sai lệch:** Ch1.3, Ch3.2, R3/R8 trong `source_map`; sai nếu đặt FD trực tiếp bằng tên tệp. **Medium:** SVG. **P0:** nối cơ chế host và container mount.

### V04 · `P02.C02.L02` · kiểm quyền khi đi qua đường dẫn
- **Hỏi / dạng:** file `0640 root:atlas` vẫn đọc lỗi vì sao? Flowchart từng thư mục.
- **Bắt buộc:** UID/GID tiến trình, quyền search ở `/`, `/srv`, `/srv/atlas`, quyền read trên file, nhánh EACCES tại thư mục 0700; phân biệt quyền file với quyền directory.
- **Kiểm / sai lệch:** Ch3.2/C3.1 và nguồn path resolution; sai nếu chỉ nhìn bit file đích. **Medium:** SVG. **P0:** dễ gây sửa quyền quá mức.

### V05 · `P02.C04.L01` · unit graph và readiness
- **Hỏi / dạng:** `After=network.target` bảo đảm gì? DAG dependency/order và timeline start.
- **Bắt buộc:** After chỉ thứ tự nếu cả hai unit được đưa vào giao dịch; Wants/Requires kéo dependency với cường độ khác; network.target khác network-online.target; `Type=exec` kiểm exec, HTTP readiness là bước khác.
- **Kiểm / sai lệch:** `examples/atlas.service`, Ch3.3, systemd.unit/special v257 trong source_map; sai nếu vẽ After như kết nối mạng sẵn IP. **Medium:** SVG. **P0:** phòng ngộ nhận vận hành.

### V06 · `P03.C01.L03` · route và neighbor từng hop
- **Hỏi / dạng:** client gửi tới MAC nào khi server ngoài subnet? Sơ đồ packet/link qua gateway.
- **Bắt buộc:** 10.20.1.10/24, next hop 10.20.1.1, đích IP 198.51.100.20 giữ qua hop trước NAT, MAC của next hop, route /24 so /0, mũi tên chiều về riêng.
- **Kiểm / sai lệch:** Ch4.1–4.2, C4.1–C4.2; sai nếu ARP trực tiếp địa chỉ server ở mạng xa. **Medium:** SVG. **P0:** tiên quyết VPC và CNI.

### V07 · `P03.C02.L01` · TCP sequence/ACK
- **Hỏi / dạng:** vì sao SYN tiêu thụ một số và ACK dữ liệu là 1005? Sequence diagram có số.
- **Bắt buộc:** SYN seq=1000→ack=1001, bốn byte seq=1001–1004→ack=1005, ACK mất rồi retransmit cùng byte, receiver ACK cộng dồn 1005; label rõ dữ liệu giả định.
- **Kiểm / sai lệch:** Ch4.3/C4.6, RFC 9293 trong source_map; sai nếu ACK đếm gói thay byte hoặc app nhận hai lần. **Medium:** SVG. **P0:** văn xuôi khó truyền trạng thái.

### V08 · `P03.C04.L02` · HTTP client–proxy–upstream
- **Hỏi / dạng:** ai xử lý TLS và ai sinh status? Sequence diagram hai chặng.
- **Bắt buộc:** DNS/TCP/TLS tới proxy, request GET Host công khai, proxy request Host nội bộ và X-Forwarded-* do proxy kiểm soát, upstream 200 + Content-Length=9, nhánh timeout proxy 504; biên trust header.
- **Kiểm / sai lệch:** `examples/http_two_hop.txt`, Ch5.3; sai nếu thể hiện TLS client chạy xuyên proxy tới upstream trong ví dụ. **Medium:** SVG. **P0:** làm rõ ranh giới an toàn.

## Thay đổi, automation và phát hành

### V09 · `P04.C02.L02` · merge/rebase trên cùng ba commit
- **Hỏi / dạng:** vì sao hai cách cho history khác nhau? Hai commit DAG đặt cạnh nhau.
- **Bắt buộc:** B là merge base, main B→D, feature B→C; merge M có D/C làm hai cha; rebase tạo C′ trên D với ID mới; conflict marker không quyết định đúng giá trị.
- **Kiểm / sai lệch:** Ch6.3–6.5, C6.2–C6.4; sai nếu vẽ C bị sửa tại chỗ. **Medium:** SVG. **P0:** đồ thị là nội dung, không trang trí.

### V44 · `P04.C01.L01` · object graph của atlas
- **Hỏi / dạng:** đổi tên nhưng không đổi byte làm đổi object nào? Vector gốc trong `scripts/science_figures.py`.
- **Bắt buộc:** C1→T1→B1 và C2→T2→cùng B1; tên ở tree, không ở blob; nhãn là giả định.
- **Kiểm / sai lệch:** G1/G3/G8; sai nếu vẽ rename là object riêng. **Tài sản:** mã gốc của repository, không lấy hình bên ngoài.

### V45 · `P04.C01.L02` · HEAD, index và working tree
- **Hỏi / dạng:** sau một lần add và lần sửa tiếp, commit lấy 2000 hay 3000?
- **Bắt buộc:** ba thời điểm của timeout_ms; HEAD 1000, index 2000, working tree 3000 ở trạng thái cuối.
- **Kiểm / sai lệch:** G2/G3; sai nếu mũi tên add khiến working tree 3000 tự cập nhật index. **Tài sản:** vector gốc.

### V46 · `P04.C01.L03` · ref và parent
- **Hỏi / dạng:** tên nào là ref cục bộ và tên nào là object bất biến?
- **Bắt buộc:** HEAD tượng trưng qua main tới D; origin/main ở C; tag ở B; parent D→C→B.
- **Kiểm / sai lệch:** G2/G3; sai nếu origin/main là truy vấn server thời gian thực. **Tài sản:** vector gốc.

### V47 · `P04.C02.L01` · fast-forward, phân kỳ và ba stage
- **Hỏi / dạng:** vì sao B→C có thể dời ref, nhưng B→D và B→C dừng conflict?
- **Bắt buộc:** B/D/C; index stage 1=1000, 2=3000, 3=2000; 2500 là quyết định giả định cần test.
- **Kiểm / sai lệch:** G4/G9; không suy mọi loại conflict có đủ ba stage. **Tài sản:** vector gốc.

### V48 · `P04.C02.L03` · revert và reset
- **Hỏi / dạng:** thao tác nào giữ M trên lịch sử chung, thao tác nào dời main về D?
- **Bắt buộc:** D→M→R cho revert; soft/mixed/hard khác nhau ở index và worktree; runtime nằm ngoài hình.
- **Kiểm / sai lệch:** G6/G7; sai nếu hình gợi Git tự hoàn nguyên dữ liệu production. **Tài sản:** vector gốc.

### V10 · `P05.C01.L02` · pipeline báo thành công giả
- **Hỏi / dạng:** `tar` lỗi nhưng shell in BACKUP_OK ra sao? Sơ đồ luồng FD và status.
- **Bắt buộc:** tar stderr→tee qua `2>&1`, tar=2, tee=0, pipeline=0 khi không pipefail, `set -e` không thoát; bên cạnh là nhánh checked với kiểm tar/list/không ghi đè.
- **Kiểm / sai lệch:** `backup_false_success.sh`, `backup_checked.sh`, Ch7.5; sai nếu tô status của pipeline bằng status tar. **Medium:** SVG. **P0:** lỗi an toàn dữ liệu.

### V11 · `P05.C02.L03` · startup vs task deadline
- **Hỏi / dạng:** vì sao deadline 0,5s chỉ bắt đầu sau READY? State machine Python/Go.
- **Bắt buộc:** spawn→READY (limit 10s)→go→task limit 0,5s→OK/EXIT 7/TIMEOUT; partial file tồn tại sau fail/timeout; cancellation chỉ quản child trực tiếp, không rollback.
- **Kiểm / sai lệch:** ba ví dụ orchestration và test tương ứng; sai nếu gộp START_TIMEOUT với task TIMEOUT. **Medium:** SVG. **P0:** tránh dạy sai khi máy khởi động chậm.

### V12 · `P06.C01.L02` · source đến artifact đang chạy
- **Hỏi / dạng:** làm sao chứng minh production chạy đúng bản đã test? Provenance chain.
- **Bắt buộc:** commit c83/c84, toolchain/dependency, artifact A83/A84 và digest H83/H84, test gate, release record, instance đang phục vụ; tag là nhãn có thể đổi.
- **Kiểm / sai lệch:** Ch9.1–9.2, C9.1; sai nếu một mũi tên commit→prod bỏ qua build inputs hoặc deploy. **Medium:** SVG. **P0:** xương sống sách.

### V13 · `P06.C03.L03` · rolling/blue-green/canary
- **Hỏi / dạng:** chiến lược nào phù hợp ngân sách thêm một Pod và ngưỡng dừng? Ba timeline lưu lượng/năng lực.
- **Bắt buộc:** số replica cũ/mới, % traffic, đầu vào test, điểm đo, stop/rollback, công suất tối đa; trục thời gian và data compatibility; số liệu giả định tách khỏi đo thực.
- **Kiểm / sai lệch:** Ch9.3–9.4, C9.3; sai nếu canary nhỏ được vẽ như bảo đảm phát hiện mọi lỗi. **Medium:** vector từ dữ liệu tình huống. **P1:** so sánh cần cùng tiêu chí.

## Container, cloud, IaC và cấu hình

### V14 · `P07.C01.L03` · namespace khác cgroup
- **Hỏi / dạng:** view và limit nằm ở đâu của cùng tiến trình? Sơ đồ cấu trúc host/process.
- **Bắt buộc:** host PID 3142/NSpid 1, net namespace riêng/loopback, cgroup tree `cpu.max` và `memory.max`, runtime đặt process vào cả hai, `clone/unshare/setns` có nhánh PID đặc biệt.
- **Kiểm / sai lệch:** Ch10.1–10.4, kernel cgroup v2 và namespace docs trong source_map; sai nếu vẽ image như cơ chế cô lập. **Medium:** SVG. **P0:** ranh giới gốc container.

### V15 · `P07.C02.L02` · OCI manifest, layer, config và digest
- **Hỏi / dạng:** tag/digest trỏ tới byte nào? Sơ đồ directed object graph.
- **Bắt buộc:** tag→manifest/index→config + layer descriptors; digest trên từng object, platform variant, build context/cache và đường pull. Cache hit không chứng minh source mới đã vào image.
- **Kiểm / sai lệch:** Ch11.1, OCI image spec v1.1.1 và Docker docs; sai nếu tag được vẽ như hash bất biến. **Medium:** SVG. **P0:** nối artifact với container.

### V16 · `P07.C03.L03` · dữ liệu qua recreate
- **Hỏi / dạng:** 41 bản ghi ở đâu khi đổi image/project? Sơ đồ ba vòng đời.
- **Bắt buộc:** container A writable layer, container B mới, volume độc lập, bind mount host path, Compose project volume name; trạng thái stopped/removed và nhánh có/không backup.
- **Kiểm / sai lệch:** Ch11.2–11.4, `compose-data.yaml`, Docker volume docs; sai nếu vẽ `down` mặc định xóa named volume hoặc volume là backup. **Medium:** SVG. **P0:** mất dữ liệu.

### V17 · `P08.C01.L02` · IAM evaluation theo request
- **Hỏi / dạng:** vì sao role có Allow vẫn AccessDenied? Decision flow có scope.
- **Bắt buộc:** principal/session, action/resource/context, identity/resource policy, explicit Deny, boundary/SCP nếu áp dụng; ranh giới network trước policy; thiếu bằng chứng policy khác ghi “chưa xác minh”.
- **Kiểm / sai lệch:** Ch12.1/C12.2 và AWS IAM docs nguồn Ch12; sai nếu đánh đồng role trust với permission hoặc Deny chỉ xét sau Allow. **Medium:** SVG. **P0:** chẩn đoán chính xác.

### V18 · `P08.C02.L03` · private subnet tới S3/STS
- **Hỏi / dạng:** route nào đủ và endpoint nào không giúp STS? Hai path packet.
- **Bắt buộc:** private EC2, route table, S3 gateway endpoint association, NAT/IGW nếu có, SG/NACL, S3 vs STS đích khác; điểm DNS và IAM quyết định riêng.
- **Kiểm / sai lệch:** Ch12.2–12.4; sai nếu vẽ S3 gateway endpoint như đường chung tới STS. **Medium:** SVG. **P0:** hai ranh giới lỗi của tình huống.

### V19 · `P08.C04.L03` · block/file/object và miền lỗi
- **Hỏi / dạng:** loại lưu trữ nào còn dữ liệu sau mất AZ hoặc xóa nhầm? Bảng có điều kiện.
- **Bắt buộc:** API truy cập, AZ/Region scope, attach/mount, durability vs availability, versioning/snapshot/restore thử; giá không ghi số tĩnh.
- **Kiểm / sai lệch:** Ch12.3/C12.3, AWS docs theo Region; sai nếu “Regional” thành “không cần backup”. **Medium:** bảng vector. **P1:** so sánh có nhiều trục.

### V20 · `P09.C02.L01` · ba thực thể Terraform
- **Hỏi / dạng:** plan thấy gì sau sửa console? Tam giác trạng thái theo thời gian.
- **Bắt buộc:** HCL A, state binding ID+i-demo-01, API thực B; refresh có/không, provider read và plan replace; không có mũi tên “plan khóa API”.
- **Kiểm / sai lệch:** Ch13.2–13.4 và Terraform state docs; sai nếu state vẽ là hạ tầng thực. **Medium:** SVG. **P0:** mô hình Terraform.

### V21 · `P09.C04.L03` · partial apply/recovery
- **Hỏi / dạng:** API timeout và state write lỗi để lại gì? State machine có nhánh không biết.
- **Bắt buộc:** network/volume tạo xong, instance API timeout không xác định, backend write failure, lock, tra API bằng ID/tag, import/repair, plan mới và hậu điều kiện; tô riêng “unknown”.
- **Kiểm / sai lệch:** Ch13.3/C13.3; sai nếu timeout được vẽ là “không tạo resource”. **Medium:** SVG. **P0:** an toàn state/data.

### V22 · `P10.C02.L02` · Ansible task/handler theo lượt
- **Hỏi / dạng:** drift quyền và drift template kích hoạt gì? Timeline hai lượt + hai drift.
- **Bắt buộc:** file module changed/ok, template notify, handler chạy một lần khi config đổi, permission-only không notify, check mode khác apply, mode 0750 trên POSIX fixture.
- **Kiểm / sai lệch:** Ch14.2–14.4, playbook và kiểm thử POSIX có điều kiện; sai nếu `changed=0` đồng nghĩa ứng dụng healthy. **Medium:** SVG từ recap thật nếu có, nếu không đánh dấu giả định. **P0:** hội tụ.

## Kubernetes, telemetry, SRE và security

### V23 · `P11.C01.L02` · vòng reconciliation
- **Hỏi / dạng:** apply thành công nhưng Pod chưa phục vụ do đâu? Sơ đồ vòng điều khiển + đường dữ liệu riêng.
- **Bắt buộc:** user→API/auth/admission→etcd spec; controller→ReplicaSet→Pod; scheduler→node; kubelet/runtime→container; status/observedGeneration đi ngược; request client nằm ở đường khác.
- **Kiểm / sai lệch:** Ch15.1–15.4, Kubernetes components; sai nếu API server được vẽ là nơi chạy Pod hoặc apply=Ready. **Medium:** SVG. **P0:** mô hình điều phối.

### V24 · `P11.C04.L02` · Service selector đến endpoint
- **Hỏi / dạng:** sửa probe rồi vì sao Service còn lỗi? Luồng object/data với trạng thái.
- **Bắt buộc:** Pod `app=atlas`, Service selector typo `app=atals`, Ready=False→True, EndpointSlice trống rồi có endpoint, port 80→8080, thử từ đúng client và NetworkPolicy.
- **Kiểm / sai lệch:** Ch15.3/16.3, `k8s-ch15-incident.yaml`; sai nếu ownerReferences bị vẽ như selector. **Medium:** SVG. **P0:** lỗi hai nguyên nhân.

### V25 · `P11.C05.L02` · PVC đến dữ liệu
- **Hỏi / dạng:** `Bound` chưa phải mount/backup thế nào? State chart.
- **Bắt buộc:** claim→StorageClass/provisioner→PV bound→CSI attach/mount→filesystem permission→read/write→backup/restore; nhánh FailedMount và reclaim policy.
- **Kiểm / sai lệch:** Ch16.4/C16.2, Kubernetes storage docs; sai nếu RWO nghĩa một Pod hoặc bound nghĩa dữ liệu an toàn. **Medium:** SVG. **P0:** an toàn dữ liệu.

### V26 · `P11.C06.L02` · HPA từ CPU request
- **Hỏi / dạng:** ba Pod có 300/450/150m, request 500m, target 50% thì cơ sở ra mấy Pod? Bảng tính và vòng feedback.
- **Bắt buộc:** utilization 60/90/30%, avg 60%, ratio 1,2, ceil(3×1,2)=4, giới hạn 2–5; metric timestamp/missing, tolerance, scheduler, readiness sau scale.
- **Kiểm / sai lệch:** Ch16.5/C16.4; sai nếu lấy CPU limit làm mẫu số hoặc 4 replica là kết quả chắc chắn. **Medium:** bảng + SVG/vector. **P0:** bảo đảm thứ tự tiên quyết.

### V27 · `P11.C07.L02` · Route attachment/status
- **Hỏi / dạng:** Accepted/ResolvedRefs/Programmed khác request thế nào? Sơ đồ object và condition.
- **Bắt buộc:** GatewayClass controller, Gateway listener `allowedRoutes`, HTTPRoute parentRef, cross-namespace ReferenceGrant cho backend riêng, Service endpoint, DNS/Host/SNI, observedGeneration.
- **Kiểm / sai lệch:** Ch17.1–17.5, chart `gateway-helm`; sai nếu Grant ở namespace Gateway tự mở listener. **Medium:** SVG. **P1:** nhiều quan hệ quyền độc lập.

### V28 · `P12.C02.L02` · histogram và missing scrape
- **Hỏi / dạng:** p95 0,9615s được ước lượng ra sao và khi `b` mất scrape thì gì sai? Biểu đồ bucket từ CSV + lớp missing.
- **Bắt buộc:** cumulative buckets 80/180/232/240 trên 120s, vị trí 228, nội suy 0,5–1s; dấu không có dữ liệu của b tại 240, không nối tuyến như giá trị 0; ghi rõ giả định.
- **Kiểm / sai lệch:** `metrics-ch18.csv`, C18.1–C18.4; sai nếu diễn giải p95 là percentile chính xác của request raw hoặc `up=0` là app chết. **Medium:** đồ thị dựng từ CSV, vector. **P0:** số liệu là nội dung.

### V29 · `P12.C03.L02` · trace và log trên cùng trục
- **Hỏi / dạng:** vì sao năm span cộng 1153ms nhưng client mất 420ms? Gantt/span tree kết hợp log marker.
- **Bắt buộc:** G 0–420, A 12–405, D 30–280, U1 285–335 ERROR, U2 345–385, log tại 30/335/405; khoảng trống và retry 10ms; HTTP 200 cuối; không suy DB server 250ms.
- **Kiểm / sai lệch:** `trace-ch19.csv`, `logs-ch19.json`, test trace; sai nếu cộng duration lồng nhau hoặc vẽ log severity thành span status. **Medium:** chart từ CSV/JSON, vector. **P0:** cơ chế trực quan hơn văn xuôi.

### V30 · `P13.C01.L03` · error budget và burn
- **Hỏi / dạng:** khi nào rollout phải dừng? Biểu đồ từ kịch bản dữ liệu mới, không dùng “số thật” giả.
- **Bắt buộc:** good/total request, SLO window, budget cho phép, tiêu thụ theo thời gian, multi-window burn và no-data; trục và denominator minh bạch.
- **Kiểm / sai lệch:** A2 tạo dataset có phép tính kiểm bằng script; đối chiếu [Google SRE SLO](https://sre.google/sre-book/service-level-objectives/). Sai nếu tính trung bình tỷ lệ không trọng số. **Medium:** data chart. **P1:** chỉ tạo khi có dataset kiểm toán.

### V31 · `P13.C03.L03` · RPO/RTO và restore
- **Hỏi / dạng:** sau mất AZ/xóa nhầm, thời điểm nào dữ liệu và request được phục hồi? Timeline hai đồng hồ.
- **Bắt buộc:** last consistent backup, failure time, detection, restore, validation, traffic resume; RPO vs RTO; replication có thể sao lỗi/xóa; nhánh key/secret mất.
- **Kiểm / sai lệch:** Ch12.3 cùng tài liệu DR được A2 ghim; sai nếu snapshot tồn tại nghĩa restore thành công. **Medium:** SVG/data timeline. **P1:** phục hồi là quá trình.

### V32 · `P14.C01.L02` · trust boundary và policy
- **Hỏi / dạng:** ai có quyền gọi gì trên đường client→cluster→cloud data? Data-flow threat diagram.
- **Bắt buộc:** client identity, proxy, Pod ServiceAccount, STS role session, S3 action/resource, secret store, log/trace pipeline; phân biệt trust boundary, network path và authorization decision.
- **Kiểm / sai lệch:** Ch12 IAM, Ch17 Gateway, Ch19 telemetry; A2 phải xác minh policy cụ thể. Sai nếu một firewall được vẽ như quyết định IAM. **Medium:** SVG. **P1:** hợp nhất kiểm soát chéo.

### V33 · `P14.C03.L03` · supply-chain evidence chain
- **Hỏi / dạng:** chữ ký chứng minh điều gì và chưa chứng minh điều gì? Directed evidence graph.
- **Bắt buộc:** source commit, dependency lock, build inputs, SBOM, provenance/attestation, image digest, signature verifier, deployment admission, runtime behavior; cạnh ghi rõ ai xác minh.
- **Kiểm / sai lệch:** P06 artifact model, OCI spec, tiêu chuẩn provenance được A2 ghim phiên bản; sai nếu signature được vẽ như test chất lượng mã. **Medium:** SVG. **P1:** chuẩn bị security.

### V34 · `P15.C02.L03` · chi phí và SLO
- **Hỏi / dạng:** phương án nào vừa đủ tải/SLO với giá thấp hơn? Đường biên đánh đổi từ dữ liệu có Region/time.
- **Bắt buộc:** peak, headroom, replica, storage backup/retention, egress, telemetry; công thức chi phí, trục đơn vị, giả định giá có ngày/Region; vùng không đạt SLO/DR.
- **Kiểm / sai lệch:** A2 tạo dữ liệu và nguồn giá chính thức theo ngày; sai nếu một giá cố định được trình bày như phổ quát. **Medium:** chart từ dữ liệu. **P1:** không biến cost thành khẩu hiệu.

## Bổ sung tại sáu cơ chế khó, theo kiểm toán A1

### V38 · `P02.C03.L04` · Chẩn đoán CPU, memory và I/O trên cùng cửa sổ
- **Hỏi / dạng:** cùng lúc latency tăng, tín hiệu nào phân biệt quota, reclaim và nghẽn thiết bị? Biểu đồ nhiều làn từ dữ liệu giả định Ch2.5, kèm bảng counter trước/sau.
- **Bắt buộc:** cửa sổ 60 giây; usage_usec đổi ra core, nr_throttled, memory.events high/oom, io.pressure some, số request và p95; mỗi làn ghi đơn vị, timestamp, số đo vắng mặt. Chỉ gắn nguyên nhân sau khi có phép quan sát phân biệt và đối chiếu request.
- **Kiểm / sai lệch:** Ch2.5, C2.4, Linux cgroup v2/PSI; sai nếu dùng 80/100 chu kỳ throttle làm 80% CPU hoặc gọi PSI là thời gian I/O của một request. **Medium:** biểu đồ từ dataset giả định có mã tính, vector. **P0:** là bài suy luận đa tín hiệu, văn xuôi dễ che cửa sổ đo.

### V39 · `P09.C01.L03` · DAG Terraform và thứ tự không được bảo đảm
- **Hỏi / dạng:** reference và depends_on tạo cạnh nào, hai resource không có cạnh có thể chạy song song ra sao? DAG có nhãn nguồn cạnh.
- **Bắt buộc:** resource/data/provider node từ `examples/terraform-graph/main.tf`; cạnh suy diễn bằng tham chiếu tách màu/ký hiệu với cạnh khai báo; một cặp không có cạnh, một chu trình bị từ chối; chú thích graph là thứ tự ràng buộc, không phải giao dịch.
- **Kiểm / sai lệch:** HCL Ch13.1, tài liệu [Terraform dependency graph](https://developer.hashicorp.com/terraform/internals/graph); sai nếu vẽ mọi block theo thứ tự tệp hoặc `depends_on` tạo rollback. **Medium:** SVG chỉnh được. **P0:** DAG là mô hình trung tâm của chương.

### V40 · `P09.C03.L02` · Drift, import và moved address
- **Hỏi / dạng:** đổi object ngoài Terraform khác đổi địa chỉ resource trong cấu hình thế nào? Ba snapshot config/state/API và hai nhánh thao tác.
- **Bắt buộc:** ID object thực giữ nguyên khi moved/import đúng; địa chỉ state trước/sau; drift B trên API không tự chữa bằng moved; plan replace/destroy là nhánh dừng để kiểm dữ liệu. Ghi rõ thao tác nào cần backup/lock và hậu kiểm.
- **Kiểm / sai lệch:** Ch13.2–13.4 và [Terraform refactoring](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring); sai nếu import được vẽ là tạo object mới hoặc moved là sửa drift của API. **Medium:** SVG + bảng trạng thái nhỏ. **P0:** ngăn xóa nhầm resource giữ dữ liệu.

### V41 · `P11.C03.L01` · Scheduler lọc node trước khi xét CPU tức thời
- **Hỏi / dạng:** Pod request 500m có thể lên A/B không khi A còn 300m, B còn 600m nhưng có taint? Bảng điều kiện + flow filter.
- **Bắt buộc:** A/B allocatable trừ requests đã cấp, toleration, kết quả filter, reason FailedScheduling; CPU usage 10% đặt ở cột quan sát khác và không quyết định fit. Chỉ sau placement mới diễn giải CPU limit/throttle ở L02.
- **Kiểm / sai lệch:** Ch16.1/C16.1, Kubernetes scheduling docs; sai nếu xem usage thấp là chỗ trống hoặc toleration là đảm bảo được xếp lên B. **Medium:** bảng vector và flow ngắn. **P0:** hai ranh giới placement/runtime dễ lẫn.

### V42 · `P11.C08.L03` · Helm revision và trạng thái ứng dụng
- **Hỏi / dạng:** `helm rollback` đã tạo revision mới nhưng dữ liệu/schema và request ở đâu? State machine ba trục.
- **Bắt buộc:** revision 6→7→8 sau rollback, chart/values/manifest trên từng revision; API object/controller status, endpoint/request và schema/41 đơn là ba dải riêng; nhánh rollback manifest thành công nhưng app không tương thích dữ liệu. Gateway chỉ là ví dụ chart hiện có, không là tiên quyết Helm.
- **Kiểm / sai lệch:** Ch17.3–17.5/C17.4 và [Helm rollback](https://docs.helm.sh/docs/helm/helm_rollback/); sai nếu mũi tên rollback tự đảo migration. **Medium:** SVG state timeline. **P0:** release identity khác hậu điều kiện.

### V43 · `P15.C03.L04` · Evidence ledger capstone
- **Hỏi / dạng:** thay đổi đã đủ chứng cứ để phục vụ và phục hồi chưa? Ma trận bước–artifact–phép kiểm–kết quả–stop rule, nối bằng một request ID.
- **Bắt buộc:** commit/digest, triển khai dịch vụ có dữ liệu, request path, IAM/secret, metric/log/trace, failure injection cục bộ, stop/rollback, restore dữ liệu, SLI/SLO và SKIP có lý do. Mỗi hàng dẫn tới tệp/log/dataset tái lập; không điền PASS cho thử nghiệm chưa chạy.
- **Kiểm / sai lệch:** `capstone_contract.md`, test/dataset A2 sẽ tạo và Reviewer kiểm; sai nếu một sơ đồ production hoặc status xanh được xem là đủ evidence. **Medium:** bảng vector dùng mã evidence ID; hồ sơ kiểm ngoài PDF, không chèn URL nguồn vào sách. **P0:** hợp đồng đầu ra, không phải hình trang trí.

## Trang mở Phần và hình mang tính khái niệm

### V35 · `P07` · lớp và vòng đời
- **Hỏi / dạng:** gợi cảm nhận về nhiều lớp độc lập trước khi vào cơ chế. Minh họa phác họa 3D đen trắng: một hộp có lớp trong suốt và vật thể dữ liệu đứng riêng, **không** gắn nhãn khoa học/mũi tên.
- **Kiểm / sai lệch:** A2 so với V14–V16 để không gợi ý container là VM hoặc dữ liệu luôn nằm trong image. **Medium:** minh họa nghệ thuật gốc; không dùng ảnh stock. **P2:** chỉ giữ nếu giúp định vị Phần.

### V36 · `P11` · vòng phản hồi
- **Hỏi / dạng:** gợi một hệ thống luôn điều chỉnh chứ không hoàn tất tức thời. Minh họa đen trắng dạng cấu trúc đang tự cân bằng, tách rõ khỏi V23 có claim kỹ thuật.
- **Kiểm / sai lệch:** không vẽ API server điều khiển trực tiếp process, không dùng ảnh làm bằng chứng. **Medium:** minh họa nghệ thuật gốc. **P2:** bản sắc sách, không thay sơ đồ cơ chế.

### V37 · `P15` · tuyến đường và dữ liệu
- **Hỏi / dạng:** khép hành trình từ request tới phục hồi. Minh họa khái niệm đơn sắc có ba lớp request, data, operator; không chép dashboard hoặc logo sản phẩm.
- **Kiểm / sai lệch:** A2 đánh giá tại trang mở Phần; bỏ nếu làm giảm sự rõ ràng của V30–V34. **Medium:** nghệ thuật gốc. **P2:** nhịp thị giác cuối sách.

## Quy trình nghiệm thu hình của A2

Mỗi đối tượng cần `visual_id`, lesson ID, source gốc hoặc dataset, file nguồn chỉnh được, bản SVG/ảnh export, mô tả alt text, caption trả lời câu hỏi, và biên bản kiểm từng nhãn/cạnh/đơn vị/nhánh lỗi. Dữ liệu đo thật phải ghi môi trường, phiên bản, thời gian và cách chạy; số liệu giả định phải có nhãn ngay ở caption. Reviewer kiểm một hình theo câu hỏi kỹ thuật của nó, không chỉ theo độ đẹp. Đếm hình chỉ để quản lý phạm vi, không là KPI.
