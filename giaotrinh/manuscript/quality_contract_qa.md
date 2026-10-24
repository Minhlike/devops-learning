# Đánh giá nội bộ theo Quality Contract — 2026-10-23

## Phạm vi và cách chấm

Đã đọc trực tiếp nội dung **178/178 bài**, đối chiếu câu hỏi–đáp án ở `manifest.json`, và kiểm từng bài theo sáu điều kiện cấp Bài trong Quality Contract. Đã cho điểm **58/58 chương** theo A/B/C/D/E/F, thang 0–4 và trọng số 20/25/20/15/10/10. Bảng ghi bằng chứng đại diện của từng chương; số bài của chương tra theo ID trong `architecture/knowledge_tree.json` và `manuscript/manifest.json`. `reviewed` trong manifest, một test xanh, hoặc độ dài văn bản không được dùng làm bằng chứng chất lượng. Điểm là đánh giá biên tập nội bộ, không là nghiệm thu nguồn từng claim hay nghiệm thu xuất bản.

Quy ước điểm: A=3 ở mọi chương vì đã có bản đồ nguồn và đối chiếu chọn lọc nhưng chưa kiểm toán ngữ nghĩa độc lập mọi claim; F=3 vì thứ tự học, hình và ví dụ đã có nhưng ảnh render của candidate hiện tại chưa được xem toàn bộ. B=4 chỉ khi chương giải thích quan hệ nhân quả và trạng thái; C=4 khi có phép tính, mã/fixture hoặc tình huống có đầu vào, hậu kiểm và ca biên đủ để người học tự đối chiếu; D=4 khi bài buộc phân biệt giả thuyết, phép quan sát và giới hạn kết luận. C=3 vẫn đáp ứng khả năng tự áp dụng trong phạm vi bài, thường vì chưa có môi trường thực nghiệm thật. Không cộng điểm cho một output chưa chạy.

**Sau sửa:** 178 bài đã đọc, 178 bài đã kiểm điều kiện cấp Bài, 178 bài đạt ở lượt chấm nội bộ; 58 chương được chấm điểm, 58 chương đạt ngưỡng 85/100 và A/B/C/D ≥3. Ba bài được nâng cấp thực chất trong lượt này: `P08.C01.L01`, `P09.C01.L01` (bài tập và đáp án), `P10.C01.L01`. **Bài còn yếu theo những điều kiện đã chấm: không phát hiện.** Kết luận này không bao gồm chứng nhận thực nghiệm trên AWS/Kubernetes hoặc kiểm toán thị giác toàn bộ PDF.

## Điểm theo chương

| Chương | A/B/C/D/E/F | Điểm | Bằng chứng năng lực đại diện |
|---|---|---:|---|
| P01.C01 | 3/4/4/4/3/3 | 90 | P01.C01.L01: tính wall/CPU time và phản chứng tối ưu CPU |
| P01.C02 | 3/4/4/4/3/3 | 90 | P01.C02.L02: lần theo fork/exec và nhánh lỗi; L03 kiểm descriptor mở |
| P02.C01 | 3/4/3/4/3/3 | 85 | P02.C01.L03: đối chiếu đường dẫn, ghi và bền vững qua sự cố |
| P02.C02 | 3/4/3/4/3/3 | 85 | P02.C02.L03: quyền tìm kiếm trên đường dẫn trước quyền tệp |
| P02.C03 | 3/4/4/4/3/3 | 90 | P02.C03.L03: CPU, PSI, I/O và giới hạn phép đo latency |
| P02.C04 | 3/4/3/4/3/3 | 85 | P02.C04.L03: trạng thái systemd, ordering và readiness |
| P02.C05 | 3/4/3/4/4/3 | 87.5 | P02.C05.L02: hash backup khác tính nhất quán/restore |
| P03.C01 | 3/4/4/4/3/3 | 90 | P03.C01.L04: MTU/PMTU và payload tính theo byte |
| P03.C02 | 3/4/4/4/3/3 | 90 | P03.C02.L03: tuple NAT, ACK và đường phản hồi |
| P03.C03 | 3/4/4/4/3/3 | 90 | P03.C03.L02: phân biệt DNS, TLS và HTTP theo trace |
| P03.C04 | 3/4/4/4/3/3 | 90 | P03.C04.L02: request hai chặng, nơi sinh status, timeout |
| P04.C01 | 3/4/4/3/3/3 | 86.25 | P04.C01.L02: suy HEAD/index/working tree từ ba giá trị |
| P04.C02 | 3/4/4/4/3/3 | 90 | P04.C02.L02: conflict và kết quả merge/rebase trên DAG |
| P05.C01 | 3/4/4/4/3/3 | 90 | P05.C01.L02: backup báo thành công giả và đường lỗi shell |
| P05.C02 | 3/4/4/4/3/3 | 90 | P05.C02.L02: subprocess, timeout và trạng thái partial |
| P05.C03 | 3/4/4/4/4/3 | 92.5 | P05.C03.L03: idempotency, cleanup và hậu điều kiện chạy lại |
| P06.C01 | 3/4/3/4/3/3 | 85 | P06.C01.L03: digest artifact sau build và giới hạn test cũ |
| P06.C02 | 3/4/4/4/3/3 | 90 | P06.C02.L02: gate CI/CD đối chiếu đúng artifact triển khai |
| P06.C03 | 3/4/4/4/4/3 | 92.5 | P06.C03.L03: canary, stop rule và traffic theo revision |
| P06.C04 | 3/4/3/4/4/3 | 87.5 | P06.C04.L02: rollback binary không đảo schema/dữ liệu |
| P07.C01 | 3/4/4/4/3/3 | 90 | P07.C01.L03: cgroup CPU throttle khác utilization |
| P07.C02 | 3/4/3/4/3/3 | 85 | P07.C02.L02: cache graph, digest và gói cũ dù job xanh |
| P07.C03 | 3/4/4/4/3/3 | 90 | P07.C03.L02: writable layer, bind mount và volume |
| P07.C04 | 3/4/4/4/4/3 | 92.5 | P07.C04.L03: đổi project/image và nhận diện volume thật |
| P08.C01 | 3/4/4/4/3/3 | 90 | P08.C01.L01: ba nhánh credential/TCP/AccessDenied; L02 đọc policy |
| P08.C02 | 3/4/3/4/3/3 | 85 | P08.C02.L02: chiều về cổng ephemeral qua NACL |
| P08.C03 | 3/4/4/4/3/3 | 90 | P08.C03.L02: ALB healthy, S3 timeout rồi AccessDenied |
| P08.C04 | 3/4/3/4/4/3 | 87.5 | P08.C04.L01: root/data EBS và recovery point khác RTO |
| P09.C01 | 3/4/4/3/3/3 | 86.25 | P09.C01.L01: cạnh suy diễn/tường minh và policy readiness |
| P09.C02 | 3/4/3/4/3/3 | 85 | P09.C02.L03: API timeout cộng lỗi ghi state sau partial apply |
| P09.C03 | 3/4/4/4/3/3 | 90 | P09.C03.L03: moved block, import và plan không destroy |
| P09.C04 | 3/4/3/4/4/3 | 87.5 | P09.C04.L03: replacement của instance giữ 41 đơn |
| P10.C01 | 3/4/4/3/3/3 | 86.25 | P10.C01.L01: inventory ba host, giới hạn canary, unreachable |
| P10.C02 | 3/4/4/4/3/3 | 90 | P10.C02.L02: changed/handler và lượt hội tụ thứ hai |
| P10.C03 | 3/4/3/4/4/3 | 87.5 | P10.C03.L01: variable precedence; L03 xoay K0/K1 từng host |
| P11.C01 | 3/4/3/4/3/3 | 85 | P11.C01.L02: API → ReplicaSet → Pod → scheduler → kubelet |
| P11.C02 | 3/4/4/4/3/3 | 90 | P11.C02.L03: surge/unavailable và Ready khác Available |
| P11.C03 | 3/4/4/4/3/3 | 90 | P11.C03.L03: CPU counter, request và mẫu thiếu |
| P11.C04 | 3/4/3/4/3/3 | 85 | P11.C04.L02: Service/EndpointSlice và policy theo đường gói |
| P11.C05 | 3/4/3/4/4/3 | 87.5 | P11.C05.L02: PVC Bound khác CSI attach/mount và backup |
| P11.C06 | 3/4/4/4/3/3 | 90 | P11.C06.L01: CPU utilization theo request, metric HPA |
| P11.C07 | 3/4/4/4/3/3 | 90 | P11.C07.L03: Gateway Accepted/ResolvedRefs và client request |
| P11.C08 | 3/4/4/4/4/3 | 92.5 | P11.C08.L03: Helm revision, Host đổi và rollback dữ liệu |
| P12.C01 | 3/4/4/4/3/3 | 90 | P12.C01.L02: cardinality 800.000 chuỗi theo giả định |
| P12.C02 | 3/4/4/4/3/3 | 90 | P12.C02.L03: PromQL, rate/window và nhãn phép đo |
| P12.C03 | 3/4/3/4/3/3 | 85 | P12.C03.L02: trace sampling và giới hạn kết luận |
| P12.C04 | 3/4/4/4/3/3 | 90 | P12.C04.L02: alert path từ target tới người trực |
| P13.C01 | 3/4/4/4/3/3 | 90 | P13.C01.L03: weighted SLI và multi-window burn |
| P13.C02 | 3/4/4/4/3/3 | 90 | P13.C02.L02: 30 request sai khác số order, mitigation chưa verified |
| P13.C03 | 3/4/3/4/4/3 | 87.5 | P13.C03.L01: RPO 8 phút, RTO 37 phút và WAL chain |
| P13.C04 | 3/4/4/4/3/3 | 90 | P13.C04.L03: Little's Law trong cửa sổ không ổn định |
| P14.C01 | 3/4/3/4/3/3 | 85 | P14.C01.L01: object authorization, user 7/8, ca âm |
| P14.C02 | 3/4/3/4/4/3 | 87.5 | P14.C02.L02: secret trong image layer và thu hồi token |
| P14.C03 | 3/4/4/4/3/3 | 90 | P14.C03.L02: provenance/attestation phải khớp digest đích |
| P14.C04 | 3/4/3/4/3/3 | 85 | P14.C04.L02: SA/RBAC khác UID, token và runtime control |
| P15.C01 | 3/4/4/4/3/3 | 90 | P15.C01.L02: request → revision → database → readback |
| P15.C02 | 3/4/4/4/4/3 | 92.5 | P15.C02.L02: 5.840p/3.160p và chi phí chưa tính |
| P15.C03 | 3/4/4/4/4/3 | 92.5 | P15.C03.L04: capstone release, incident, restore, ca âm |

## Những sửa đổi so với bản ngay trước lượt chấm

- `P10.C01.L01`: từ mô tả inventory/SSH bằng văn xuôi sang inventory INI ba host, phép giao `app ∩ canary`, phân biệt alias với địa chỉ, và giải thích vì sao `unreachable` không là hội tụ. Có câu hỏi–đáp án yêu cầu chọn tập máy và hậu kiểm từng host.
- `P08.C01.L01`: từ mô tả role/profile sang trace ba nhánh credential, kết nối TCP và phản hồi `AccessDenied`; câu hỏi–đáp án mới buộc chọn phép kiểm đúng lớp và nêu điều chưa thể kết luận.
- `P09.C01.L01`: từ câu hỏi “khi nào dùng depends_on?” với đáp án một câu sang tình huống hai biểu thức HCL, cạnh DAG, độ trễ hiệu lực policy, đọc plan và kiểm request dương/âm sau apply. Văn bản bài học và kiến trúc chương không đổi.

## Candidate gắn với hồ sơ này

- Tệp: `giaotrinh/Cam_nang_devops.candidate.pdf`.
- SHA-256: `21A97465829361AA58B261E0F6B7844B29C2822F8B621319F693B12CA9588AD6`.
- 248 trang A4, 310 bookmark; font Times New Roman/Consolas và Arial Bold cho bìa được nhúng; 0 URI action ngoài theo phép đọc cấu trúc PDF.
- Bộ dựng báo `source_leaks=0`; điều đó không thay cho việc đọc mọi trang hoặc kiểm chứng ngữ nghĩa 267 claim.
- Candidate được dựng từ bản thảo sau ba sửa đổi nêu trên, với bìa trước/sau trắng, chữ đen và ảnh máy chủ đen trắng. Đã xem ảnh render hai bìa; hồ sơ QA này không tham gia render. Đây là bản candidate, **không có Publication PASS**.

## Kiểm chứng đã chạy trong lượt này

- Dựng PDF: PASS (`CANDIDATE_OK`, 248 trang, 310 bookmark, `source_leaks=0`). Đọc cấu trúc riêng: 248/248 trang kích thước A4 khoảng 595×842 pt, 0 URI action ngoài, có Times New Roman Regular/Bold, Consolas và Arial Bold.
- Bìa: đã xem ảnh render trang đầu và cuối; chỉ có tiêu đề sách ở bìa trước, không có số trang hoặc trạng thái nội bộ trên hai bìa. Kiểm thử `test_pdf_contract.py`: 7 PASS, 0 FAIL, 0 SKIP.
- Regression toàn bộ: 44 ca được chạy; ban đầu 42 PASS, 1 FAIL do hai ID nguồn mới bị đưa nhầm vào `frozen_ids` lịch sử, 1 SKIP vì thiếu Go toolchain. Đã bỏ hai ID mới khỏi `frozen_ids`, giữ URL mới trong registry, và chạy lại đúng ca lỗi: PASS. Vậy **0 FAIL còn mở trong các ca đã chạy**; toàn bộ suite chưa chạy lại sau chỉnh sửa hẹp này.
- `git diff --check`: PASS. Kiểm độc lập 58 dòng điểm cho 58 ID chương, công thức trọng số và điểm thấp nhất 85: PASS.

## Giới hạn và việc còn phải kiểm độc lập

- Chưa xem ảnh render của toàn bộ 248 trang ở lượt này; typography và ngắt trang ruột sách chưa được nghiệm thu độc lập.
- Chưa chạy lại toàn bộ ví dụ cần AWS, Docker Engine hoặc Kubernetes cluster; ví dụ giả định trong sách được giữ đúng nhãn.
- Chưa kiểm toán ngữ nghĩa độc lập từng claim trong source map. A=3 phản ánh giới hạn ấy; anchor tồn tại không chứng minh nguồn hỗ trợ mọi diễn giải.
- Điểm là biên tập nội bộ của bản thảo này. Nếu kiểm toán nguồn hoặc quan sát trang phát hiện lỗi, phải hạ điểm chương liên quan và sửa trước khi xét xuất bản.
