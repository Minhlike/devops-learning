# Bàn giao có kiểm soát cho A2

**Trạng thái:** `AWAITING_ARCHITECTURE_REVIEW`. Không khởi động A2 trước khi Reviewer duyệt `knowledge_tree.md`, đồ thị và ranh giới. A1 chỉ lập thiết kế; PDF 109 trang hiện là candidate cũ, không được gọi là đầu ra kiến trúc mới.

## Đọc trước khi sửa

1. `giaotrinh/architecture/knowledge_tree.md` để hiểu hành trình, `knowledge_tree.json` để lấy ID/prerequisite.
2. `architecture_rationale.md`, `coverage_matrix.md`, `visual_storyboard.md`, `publication_structure.md` để giữ lý do và hình thức đã được duyệt.
3. `legacy_migration.csv` để biết từng mục cũ và quy tắc split; `legacy_content_units.csv` để định vị đủ 216 đoạn ở mục split (kèm hash và chỉ dẫn trích claim khỏi đoạn hỗn hợp); `evidence_ownership.csv` để tra chủ bài của từng claim/ví dụ/cặp đề–đáp án; `source_map.json`/`source_ids.lock.json` để khóa nguồn; `references.md` chỉ làm hồ sơ ngoài PDF.
4. `chapters/01-*.md` … `19-*.md`, `examples/`, `answers.md`, `scripts/build.py`, tests. Không suy từ tên bài rằng claim đã được kiểm chứng ngữ nghĩa.
5. `capstone_contract.md` cho đầu ra, phép kiểm, SKIP và stop rule; `docs/ROADMAP.md`, `docs/SESSION_INDEX.md`, `state/CURRENT_PHASE.md` ở chế độ chỉ đọc để phân biệt người học đã làm với nội dung sách đã viết. S40/HPA và Gateway trên Kind có tồn đọng; không dựng output giả.

**Bốn ranh giới migration đã chốt:** P03.C01.L01 chỉ có bản thảo IPv4/prefix và P03.C01.L03 chỉ có ARP/Ethernet; phần IPv6 addressing và Neighbor Discovery là `needs_extension`, cần biên soạn và kiểm nguồn riêng. Sáu lesson có đoạn cũ nhưng không có claim nguồn trực tiếp mang `source_research_needed=true` dù còn `reviewed_draft`; không mượn nguồn bài kề. Ở P11.C07 Gateway API, A2 dùng YAML resource thuần hoặc manifest đã render kèm đầu vào render và chỉ giảng schema/status; hai tệp `gateway-helm/templates/gateway.yaml` và `httproute.yaml` cùng `values.yaml` thuộc P11.C08 Helm, nơi mới dạy `.Release`/`.Values`. Không đặt nguyên Go template vào bài Gateway hoặc tạo required edge Gateway→Helm. Trong capstone, `change_id` theo đợt thay đổi; từng `deployment_revision` định danh một lần triển khai; mỗi request có `request_id` riêng và bằng chứng nối về revision phục vụ.

## Thứ tự tái biên soạn

| Đợt | Đầu vào / hành động có thể rollback | Cổng nghiệm thu trước đợt sau |
| --- | --- | --- |
| 0. Khóa baseline | Ghi SHA 19 chương, answers, examples, source_map, lock, candidate PDF; xuất bảng 88 mục, 216 đoạn split và ledger 267 claim/23 ví dụ/79 cặp đề–đáp án. Định nghĩa ID/tệp đích và renderer hợp đồng trước khi đổi. | Reviewer duyệt cây, ranh giới Phần, 3 loại cạnh, 43 visual objects là ứng viên chứ không quota; ledger đủ chủ sở hữu và quy tắc split. |
| 1. Nền máy/Linux/mạng/Git | Chuyển từng mục từ Ch1–6 qua P01–P04; ưu tiên V01–V09 chỉ khi nội dung dùng. Giữ trace fork/TCP/HTTP và lời giải. | Source anchors remap theo mục mới; câu hỏi/đáp án còn đủ; test các phép tính; PDF candidate A4 và visual review. |
| 2. Automation/delivery/container | Ch7–11 qua P05–P07. Tách pipeline failure, artifact identity, OCI image/runtime/data. Giữ file ví dụ, môi trường tạm và nhãn giả định. | Re-run script backup/orchestration có điều kiện; Go SKIP ghi rõ; không xóa volume/lab thật; kiểm 41 bản ghi là tình huống giả định. |
| 3. Cloud/Terraform/Ansible | Ch12–14 qua P08–P10; bổ sung các mục planned_new với nguồn phiên bản. Không tạo AWS resource tính phí. | HCL validate nếu có CLI; Ansible fixture trên POSIX filesystem nếu có; source ID cũ không đổi; không tuyên bố plan/apply giả là output thật. |
| 4. Kubernetes/observability | Ch15–19 qua P11–P12; thứ tự resource metric→HPA→Prometheus; Gateway và Helm tách. Kiểm tra V23–V29 và các sự cố giả định. | Apply/Ready/Available, Bound/Mount, sampled/stored phân biệt đúng; CSV p95 và trace vẫn tính đúng; cluster/OTel runtime thiếu thì SKIP trung thực. |
| 5. SRE/security/production | Viết P13–P15 từ nguồn chính thức, dataset có thể kiểm, kịch bản có stop rule; không mượn output từ roadmap. | Reviewer chuyên môn kiểm SLO denominator, DR restore, policy evaluation, provenance, chi phí theo Region/ngày, capstone evidence. |
| 6. Đóng gói candidate | A2 triển khai hierarchy, hình vector/biểu đồ và PDF candidate mới theo `publication_structure.md`. | Automated tests + visual từng trang, source-free, link/bookmark đích, font/A4; chỉ Reviewer mới cấp publication approval. |

Mỗi đợt là một commit/nhóm commit nhỏ chỉ trong `giaotrinh/`, có manifest old→new và khả năng quay lại commit trước. Không di chuyển hàng loạt rồi sửa lỗi sau. Khi chuyển một mục: sao nội dung đã được review → so câu/claim/đề–đáp án/ví dụ → kiểm nguồn hỗ trợ trong ngữ cảnh mới → viết thêm phần thiếu với nhãn bằng chứng → chạy test → render/visual. Khi thay hình hoặc bảng, giữ dữ liệu nguồn, số và alt text; không dùng số trang cũ làm ID.

## Rủi ro và điều kiện dừng

- **Nguồn đổi danh tính:** 197 URL hiện khóa; thêm ID mới, không tái dùng ID hay đổi URL. Dừng nếu claim anchor bị mất hoặc validator chỉ “thấy anchor” nhưng ngữ nghĩa chưa đối chiếu.
- **Lặp tri thức:** một định nghĩa gốc có một bài chủ sở hữu, bài ứng dụng chỉ tóm 1–2 câu và cross-reference. Dừng nếu A2 viết lại nguyên cơ chế TCP trong VPC hoặc Prometheus trong HPA.
- **Sai thứ tự:** test DAG/ID trước render. Dừng nếu một bài dùng metric/scheduler/permission chưa xuất hiện, trừ phần giới thiệu tại chỗ đã ghi là `helpful`.
- **Mất bằng chứng:** giữ mọi 88 mục, 216 đoạn thuộc mục split, 267 claim, 23 ví dụ và 79 cặp đề–đáp án; dùng cả ba ledger migration/content/evidence. Dừng nếu một đoạn không có primary lesson, source IDs lệch nguồn gốc hoặc claim được copy sang nhiều bài như hai bản chính. Claimless lesson và phần IPv6/ND phải có hồ sơ nghiên cứu nguồn trực tiếp trước khi coi là đã kiểm chứng.
- **Hình sai kỹ thuật:** Reviewer xem cạnh, đơn vị, nhánh lỗi, caption và dataset của từng Vxx; không dùng hình minh họa nghệ thuật thay chứng cứ kỹ thuật.
- **Thí nghiệm nguy hiểm:** lab, state học tập, cluster, cloud account và volume thật nằm ngoài phạm vi migration; không chạm. Dùng fixture/thư mục tạm, ghi SKIP khi thiếu toolchain/quyền.
- **Publication:** source-free tuyệt đối trong PDF; build xanh không thay visual QA. Không phát hành chính thức, merge hoặc kích hoạt A2 tự động.

## Quyết định Reviewer cần chốt

1. Nghiệm thu lại phạm vi 15 Phần/58 Chương/178 Bài, đặc biệt chủ claim/ví dụ/bài tập, sáu status `needs_extension` và nguồn chỉ theo claim gán thực.
2. Duyệt quy tắc split của 59 mục nhiều đích, đặc biệt 75 đoạn không có anchor và 27 đoạn trộn nhiều owner; duyệt sáu visual bổ sung V38–V43 theo rủi ro thực, không theo quota. Quyết định về Go, UDP/IPv6/MTU và AWS-first đã được phản ánh trong cây.
3. Duyệt rubric `capstone_contract.md`: phiên local không phí, quan hệ change–revision–request, phép kiểm âm/dương, SLO denominator, stop rule, và điều kiện SKIP; chỉnh ngưỡng cụ thể khi A2 có fixture/dataset.
4. Chốt thứ tự lời giải và phụ lục, cùng tiêu chuẩn visual pass cho bản in. Trang mở nghệ thuật V35–V37 là tùy chọn sau khi technical visuals đạt.

**Điều kiện A2-ready:** Reviewer xác nhận cây/graph, migration không bỏ sót, storyboard đúng câu hỏi kỹ thuật, hợp đồng publication rõ và các quyết định trên được ghi. Trước thời điểm đó, trạng thái là **chưa bàn giao thực thi**.
