# Bản đồ kiến thức Phần IV (hồ sơ biên tập, không render)

Ngày lập: 2026-10-25. Ví dụ xuyên suốt là kho giả định `atlas`, tệp `app.conf`, nhánh `main` và `feature/retry`. Các chữ B, C, D, M là nhãn sư phạm, không phải object ID thực. Nguồn G1–G9 là các tài liệu Git đã khóa trong `source_map.json`; cần đối chiếu thí nghiệm cục bộ cho những thao tác có trạng thái.

| Bài / đơn vị | Mức | Bản chất và tiên quyết | Ngộ nhận cần phá | Vị trí / phép kiểm hoặc hình / nguồn |
|---|---|---|---|---|
| L01 blob | CORE | Object lưu byte nội dung; đã biết file từ P02 | Blob chứa tên file | § byte → blob; `cat-file`, V44; G1 |
| L01 tree entry | CORE | Tên, mode, ID trỏ blob/tree; cần blob | File path nằm trong blob | § tree; `ls-tree`, V44; G1 |
| L01 mode | SUPPORTING | Mode trong entry mô tả loại/quyền thực thi; cần tree | Git giữ đầy đủ ACL của host | § tree; so `ls-tree`; G1 |
| L01 commit | CORE | Root tree, parent, metadata tạo object mới; cần tree | Commit là thư mục vật lý | § commit; `cat-file`; G1 |
| L01 snapshot/parent | CORE | Snapshot là nội dung, cha nối lịch sử; cần commit | Git chỉ lưu diff tuyến tính | § DAG; V44; G1 |
| L01 băm/object format | CORE | Hash của header loại, độ dài và nội dung; cần object | Hash chứng minh tác giả/an toàn | § ID; `hash-object`; G1,G8 |
| L01 đổi byte/tên/mode | CORE | Byte đổi blob; tên/mode đổi tree; commit mới đổi do tree/cha | Rename là object độc lập | § ba commit; `ls-tree`, V44; G1 |
| L01 rename inference | SUPPORTING | Diff so snapshot và suy luận tương đồng | Có sự kiện rename lưu riêng | § so diff; G3 |
| L01 ID rút gọn, tính xác thực | REFERENCE | Prefix phân biệt cục bộ; author metadata chưa là chứng thực | SHA ngắn hay tên tác giả là bằng chứng tuyệt đối | § giới hạn; G1,G3 |
| L02 working tree | CORE | Byte hiện ở đĩa; cần object snapshot | File đang mở là commit | § ba lớp, V45; G3 |
| L02 index | CORE | Tree dự kiến cho commit sau, có path/mode/stage | Index chỉ là danh sách tên | § ba lớp, V45; G3 |
| L02 HEAD/branch | CORE | Commit đang checkout qua ref thường; cần L01 | HEAD luôn là hash trực tiếp | § ba lớp, V45; G2 |
| L02 add/commit | CORE | Add chụp byte lúc đó; commit lấy index và đẩy ref | Lưu file sau add tự cập nhật index | § 1000/2000/3000; V45; G3 |
| L02 status/diff | CORE | status phân loại; diff so index–worktree; cached so HEAD–index | Một diff nói hết cả ba lớp | § quan sát; `show :path`; G3 |
| L02 tracked/untracked | SUPPORTING | Index/HEAD quyết định tracked; untracked chưa trong snapshot | Mọi file ở thư mục sẽ được commit | § quan sát; `status`; G3 |
| L02 add -p | CORE | Có thể đưa riêng hunk vào index | Test working tree chứng minh staged snapshot | § kiểm partial stage; G3 |
| L02 unstage/restore | SUPPORTING | Bỏ stage khác bỏ sửa trên đĩa | `restore` luôn không mất dữ liệu | § sửa nhầm; status/diff; G11 |
| L02 secret trong index | CORE | Byte staged sống độc lập với byte trên đĩa | Xóa secret khỏi file đủ để an toàn | § sự cố; `diff --cached`; G3 |
| L03 commit identity | CORE | ID xác định object, ref là tên có thể dời; cần L01 | Branch/tag/hash là cùng loại | § nhãn và object, V46; G1,G2 |
| L03 symbolic/detached HEAD | CORE | HEAD thường trỏ branch; detached trực tiếp trỏ commit | Commit ở detached HEAD tự theo branch | § hai chế độ; `symbolic-ref`; G2,G3 |
| L03 branch/tag | SUPPORTING | Branch dời; lightweight tag trỏ object, annotated tag là object riêng | Tag là bằng chứng build đã kiểm | § nhãn phát hành, V46; G2 |
| L03 remote-tracking/fetch | CORE | `origin/main` là ref local cập nhật khi fetch | Đọc origin/main là đọc server hiện tại | § hai bản sao; V46; G3 |
| L03 ancestry/merge base | CORE | Parent tạo quan hệ tổ tiên; cần commit DAG | SHA mới hơn nghĩa là con | § A→B→C→D; `merge-base`; G3 |
| L03 reachability/reflog | SUPPORTING | Ref dẫn đến object; reflog ghi lịch sử cập nhật ref có hạn | Reset xóa object ngay; reflog là backup | § nhánh thử; `reflog`; G3 |
| L03 source/artifact | SUPPORTING | Commit ID không phải digest binary; cần CI nền tảng | Cùng commit luôn ra cùng binary | § ranh giới phát hành; G2 |
| L04 divergence/fast-forward | CORE | FF khi tip đích là tổ tiên tip nguồn | Merge luôn tạo commit | § B/D/C; V47; G4 |
| L04 merge base/three-way | CORE | So base, ours, theirs để hợp nội dung | Chỉ so hai đầu nhánh là đủ | § dòng timeout; V47; G4 |
| L04 index stage 1/2/3 | CORE | Bản base/HEAD/MERGE_HEAD ở path xung đột | Marker là toàn bộ dữ liệu conflict | § ba stage; `ls-files -u`, V47; G4,G9 |
| L04 HEAD/MERGE_HEAD | SUPPORTING | HEAD ở D, MERGE_HEAD ghi C khi merge dở | Git đã tạo M ngay lúc conflict | § dừng merge; G4 |
| L04 marker/ours/theirs | CORE | Trình bày hai phía theo merge hiện tại; quyết định theo hợp đồng | Chọn ours mặc nhiên đúng | § giải xung đột; V47; G4 |
| L04 semantic conflict | CORE | Merge sạch chữ có thể sai hành vi | Không marker nghĩa là đúng nghiệp vụ | § retry/timeout; phép test; G4 |
| L04 resolve/abort | CORE | Stage bản giải rồi commit M hai cha; abort có điều kiện | Abort chắc chắn khôi phục mọi sửa dở | § hậu điều kiện; `diff --cached`; G4 |
| L05 replay/ID mới | CORE | Rebase phát lại patch trên D thành C′; parent đổi ID | Rebase sửa C tại chỗ | § trước/sau; V09; G5 |
| L05 rebase nhiều commit | CORE | C1′ rồi C2′, từng bước có thể dừng | Một lần resolve bảo đảm chuỗi đúng | § hai commit; `log --graph`; G5 |
| L05 ours/theirs khi rebase | CORE | Ours là phía đã rebase trên upstream, theirs là commit phát lại | Ours luôn là nhánh feature cũ | § conflict; `ls-files -u`; G5 |
| L05 continue/abort | SUPPORTING | Continue sau stage; abort quay trạng thái rebase trước | Continue là cổng chất lượng | § kiểm đồ thị và test; G5 |
| L05 shared history/force | CORE | Đẩy C′ thay C gây lệch bản sao; lease kiểm ref kỳ vọng | Force-with-lease tự bảo đảm cộng tác an toàn | § chính sách nhánh; G5,G10 |
| L05 merge/rebase choice | CORE | Merge giữ hai tuyến, rebase đổi identity; cần L04 | Đồ thị thẳng luôn tốt hơn | § tình huống; V09; G4,G5 |
| L06 revert thường | CORE | Tạo commit đảo hiệu ứng trong bối cảnh hiện tại | Xóa commit lỗi khỏi lịch sử | § lỗi đã push; V48; G6 |
| L06 revert merge/mainline | CORE | Chọn parent để xác định delta đảo; cần M hai cha | `-m 1` đưa kho về B | § M/D/C; V48; G6 |
| L06 reset modes | CORE | Soft dời ref; mixed thêm index; hard thêm worktree | Mọi reset đều xóa file như nhau | § bảng trạng thái bằng văn xuôi; V48; G7 |
| L06 path restore | SUPPORTING | Sửa một path/index khác dời branch | Dùng reset branch để unstage một file | § thao tác hẹp; G7 |
| L06 reflog/recovery | SUPPORTING | Có thể tìm tip trước khi ref dời, nếu entry/object còn | Reflog thay backup | § nhánh thử; `reflog`; G3,G7 |
| L06 hậu điều kiện/deploy | CORE | Git sửa source history, không đảo dữ liệu/tác dụng phụ ở runtime | Revert là rollback production | § kiểm chứng; G6 |

## Quyết định tài sản hình

Đã tìm ảnh kỹ thuật ở [Pro Git](https://git-scm.com/book/en/v2), Wikimedia Commons và FreeSVG. Hình Pro Git theo CC BY-NC-SA 3.0 gây ràng buộc phi thương mại; nhiều hình Wikimedia phù hợp chung theo CC BY-SA 4.0 đòi ghi công/share-alike; hình rebase CC0 ở FreeSVG không trùng trạng thái B–D–C và không biểu diễn index của ví dụ. Vì PDF hiện giữ quy tắc không có credit/nguồn tham khảo, tôi không đưa tài sản bên ngoài vào sách nếu không đáp ứng nghĩa vụ giấy phép hoặc sai cơ chế. V09 được giữ; các hình mới là vector gốc tạo từ mã ReportLab trong repository, không sao chép hình tìm thấy, và có thể sửa nhãn/cạnh ở mã nguồn. Hồ sơ nguồn, giấy phép và giới hạn từng hình nằm ở `figure_evidence.json`.
