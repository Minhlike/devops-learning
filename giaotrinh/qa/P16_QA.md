# Phần XVI — hồ sơ candidate để Reviewer kiểm toán

Ngày kiểm: 2026-10-25. Baseline: `ea099b719a008b9c5035414b3574651e4f8cae42`. Commit chứa bản thảo và PDF: `4825aa3b54412ccc5f7b2ca3e671dd04fa261d05`.

## Phạm vi và migration

- Cây xuất bản: 16 Phần, 64 Chương, 202 Bài; P16 gồm 6 Chương, 24 Bài. P15.C04 không còn trong cây/manifest. Tám bài cũ và nguồn được giữ tại `architecture/history_p15_c04/`, ánh xạ tại `architecture/p15_c04_to_p16.json`.
- Bài cũ L01→P16.C01.L01, L02→C02.L01, L03→C04.L01, L04→C03.L01, L05→C03.L04, L06→C05.L01, L07→C04.L02, L08→C06.L01; mỗi nhánh được mở rộng trong mapping. Tám câu hỏi cũ giữ nội dung với ID mới; 16 câu hỏi mới có đáp án cuối sách.
- Phần XVI có khoảng 30 nghìn từ theo hai cách đếm: 29.992 từ tách bằng khoảng trắng hoặc 30.258 đơn vị theo biểu thức `\b\w+\b` (tính cả mã và nhãn). Sáu chương lần lượt có 5.834, 5.360, 4.914, 4.709, 4.186 và 5.255 đơn vị theo phép đếm sau. Số từ là thông tin dung lượng, không là bằng chứng chất lượng.
- Nội dung mới làm rõ luồng request/data/change, hợp đồng trên cạnh công cụ, build một artifact, idempotency trong transaction, registry digest, runtime identity, phục hồi dữ liệu độc lập, lựa chọn stack có điều kiện và bài tổng hợp thư viện chưa có stack cho sẵn.

## Hình và nguồn

- V49–V52 chuyển chủ sở hữu sang P16; V53–V66 là hình vector gốc mới. Cả 18 hình P16 được vẽ bằng `scripts/science_figures.py`, không nhập ảnh bên ngoài hay tài sản có watermark. Repository chưa có tệp LICENSE; hồ sơ này không tự cấp giấy phép tái sử dụng bên ngoài.
- `manuscript/P16/source_map.json` có 14 nguồn TC-01–TC-14 và 11 claim anchors. TC-01–TC-09 giữ URL cũ qua `source_ids.lock.json`; nguồn mới là tài liệu chính thức Python, SQLite, Docker và GitHub theo phạm vi ghi trong map. Validator chỉ chứng minh anchor/ID/URL hợp lệ về cấu trúc; đối chiếu ngữ nghĩa đã thực hiện với các cơ chế trọng yếu, chưa là kiểm toán độc lập mọi câu của 24 bài. Nguồn không đi vào PDF.

## Chứng cứ thực thi

Ledger sạch tại `qa/p16_runs/p16-20261025-083937-1825/evidence.json`, chạy trên Docker cục bộ từ commit `4825aa3b54412ccc5f7b2ca3e671dd04fa261d05`:

| Chặng | Trạng thái | Bằng chứng chính |
| --- | --- | --- |
| Source → unit test → build một lần | PASS | commit thật; build input SHA-256 `3808a5020f3897ba28cdfa30dc5a540d785f522e3e402efd1f53b3d3b892fbbf`; candidate image ID `sha256:ca62bcbb80533936039b595345cee14677ee25886f65190e81fbc7ddbcee4e2a` |
| Candidate smoke → local OCI registry | PASS | tạo/đọc đơn và retry cùng key; push log ghi manifest digest `sha256:ca62bcbb80533936039b595345cee14677ee25886f65190e81fbc7ddbcee4e2a` |
| Pull digest → Compose deploy | PASS | pull và inspect runtime cùng image ID; Config.Image chứa tham chiếu `@sha256` |
| Request → instance → record → log | PASS | request `smoke-fe7205c1256f462f` tạo order `51c0a16c3017431ebfb9ddbb2a5df606`; record có origin revision/instance; log chứa request ID và order ID |
| Failure → recovery → restore | PASS | health/ready 200 nhưng POST 503 khi bật lỗi nghiệp vụ; sau recreate record không đổi; backup API, restore vào volume độc lập và đọc lại cùng record |
| GitHub Actions/GHCR/remote deploy | SKIP | workflow chỉ là mẫu cho repository sandbox; không có run remote hay credential production |

Image ID và registry digest trùng trong lần chạy single-platform này; không coi chúng luôn là một loại định danh. Registry cục bộ không TLS/auth; Docker Engine có quyền mạnh trên host. Base image chưa ghim digest, không có SBOM, ký artifact, attestation độc lập hay thử mất cả host. Các container/volume mang tiền tố `p16-20261025-083937-1825` còn trên máy thử để Reviewer đối chiếu; không đụng tới tài nguyên lab cũ. Các giới hạn ấy ngăn suy rộng kết quả lab thành bảo đảm production.

## Kiểm thử và PDF

- `architecture/test_architecture.py`: 8 PASS. `unittest discover -s giaotrinh/tests`: 47 ca, 46 PASS, 1 SKIP (Go toolchain không có). Pipeline local chạy lại 5 ca API trước build; các nhánh success, retry, payload conflict và cạnh tranh dùng database tạm. Không sửa labs/state/tài nguyên cloud.
- Candidate và PDF chính cùng SHA-256 `BA297A6F698968692F2B001317E0C320F96F55B1E8714DFCEBA21F61F21EA854`; 331 trang A4, 347 bookmark, Times New Roman/Consolas nhúng và không có URI nguồn. Build audit xác nhận nguồn không rò vào text/bookmark/metadata/link; các ca âm bảo vệ bookmark sai, hình/caption mất, nguồn rò và metadata sai.
- Đã render và xem contact sheet các trang 245–303 (toàn Phần XVI), 304–330 (lời giải bị dời trang) và trang mục lục 3. Đã mở lớn các trang 245, 247, 261, 268, 279, 284, 290, 299, 330 để rà sơ đồ, mã và lời giải. Contact sheet ở `qa/p16_visual/contact-1.png` đến `contact-5.png`. Không thấy hình cắt, chữ tràn hoặc nhãn thiếu ở phạm vi đã xem; trang cuối một số chương còn khoảng trắng do chương sau mở trang mới. Chưa rà độc lập từng câu của toàn sách hoặc thử trên máy in thật.

## Trạng thái

Candidate và PDF chính đã đồng bộ về byte để Reviewer đọc. Đây là hồ sơ tác giả, không phải Publication PASS hoặc Editorial PASS. Reviewer cần kiểm toán độc lập ngữ nghĩa nguồn, chất lượng sư phạm 24 bài, hình, pipeline local và các trang in trước khi nghiệm thu.
