# Hợp đồng cấu trúc trình bày cho A2

Tài liệu này quy định **thứ bậc và ngữ nghĩa**, không bắt A1 sửa renderer hoặc PDF hiện tại. A2 có thể thay đổi kích cỡ/màu sau thử in, nhưng không được làm phẳng cây tri thức, mất traceability hoặc đưa nguồn tham khảo vào PDF.

## Một bản ghi nội dung, nhiều cách trình bày

`knowledge_tree.json` định danh `BOOK → Pxx → Pxx.Cyy → Pxx.Cyy.Lzz`. ID không phụ thuộc số trang hay tên tệp, không tái sử dụng sau khi đã công bố. Bài/Mục là đơn vị cơ chế và đánh giá; có thể có heading phụ cho ví dụ, đường lỗi hoặc chứng minh nhưng không tạo ID mới chỉ vì trang dài. Khi A2 tách tiếp, giữ ID cũ cho nội dung cốt lõi và cấp ID mới cho phần phát sinh; lập migration diff, không đổi anchor âm thầm. Số in sách (Phần I, Chương 1, 1.1) là nhãn hiển thị được sinh từ thứ tự đã duyệt, tách khỏi ID ổn định.

## Cấp Phần

Mỗi Phần mở ở trang mới, có một trang mở riêng: số/tên Phần, câu hỏi trung tâm, mô hình tư duy, 2–4 ranh giới với Phần trước/sau và sơ đồ hành trình ngắn. Có thể dùng minh họa nghệ thuật gốc theo V35–V37 hoặc hình khái niệm khác khi thật sự giúp định vị; không dùng ảnh stock hoặc hình sinh ra để lấp trống. Trang mở không có claim kỹ thuật không kiểm chứng. Chương đầu theo sau trang mở; không để trang mở và nửa Chương chung một trang. Running header của phần thân gồm tên Phần rút gọn ở trang chẵn và tên Chương ở trang lẻ; trang mở/cover không mang header đó.

## Cấp Chương và Bài/Mục

Chương bắt đầu có chủ đích, có số/tên, nhãn Phần, câu hỏi chủ đạo và một đoạn nêu tình huống hoặc cơ chế kết nối các bài; không cần ép mọi Chương vào một template cố định. Tên bài phân cấp rõ với heading cấp 2, ví dụ/điều tra là heading cấp 3 không mang số nếu chỉ là cách dạy. Không để một heading cuối trang mà không có ít nhất hai dòng nội dung cùng nó; giữ caption với hình/bảng và giữ một đoạn ngắn giải thích ý nghĩa trước hoặc sau. Cho phép chương dài liên tục nếu mạch tốt; không tạo trang trắng hoặc section break chỉ để đều độ dài.

| Đối tượng | Hợp đồng ngữ nghĩa và dàn trang |
| --- | --- |
| Văn xuôi | Mỗi đoạn một ý, định nghĩa xuất hiện trước lần suy luận đầu; dẫn tới ID bài gốc khi áp dụng lại. Phân biệt quan sát, giả định, suy luận và quyết định. |
| Code | Có ngôn ngữ/phiên bản hoặc điều kiện chạy khi cần, nguồn file của ví dụ; không cắt dòng làm đổi token. Đo code width trước dựng; nếu quá rộng, đổi cách trình bày hoặc tách đoạn có chú thích, không thu font vô hạn. |
| Terminal transcript | Ghi input, output thật, môi trường và điều kiện; dữ liệu giả định đặt nhãn rõ. Prompt và output khác kiểu chữ; secret được che nhưng không làm mất ý nghĩa kiểm chứng. |
| Công thức và phép tính | Định nghĩa biến, đơn vị, cửa sổ đo, giả định; số làm tròn tách khỏi giá trị tính. Khi có dữ liệu CSV, kiểm tra bằng test và biểu đồ từ dữ liệu ấy. |
| Sơ đồ/hình kỹ thuật | Số `Hình <chương in>.<thứ tự>`; caption nêu câu hỏi/kết luận và điều kiện. Có alt text; bản nguồn vector và ID Vxx ở manifest biên tập ngoài PDF. Không dùng mũi tên trang trí. |
| Biểu đồ từ dữ liệu | Trục, đơn vị, nguồn dataset và giả định trong caption; không nối qua missing sample như đã đo 0. Dữ liệu và mã dựng được giữ ngoài PDF. |
| Bảng đối chiếu | Cột là tiêu chí đo/điều kiện, hàng là phương án; ghi rõ “không áp dụng/chưa kiểm” thay ô trống mơ hồ. Tránh bảng dài vỡ hàng hoặc quá rộng. |
| Tình huống lỗi | Nêu trạng thái đầu, thay đổi, quan sát thật/giả định, nhánh cạnh tranh, phép kiểm và giới hạn. Không tiết lộ lời giải trước khi người học thử suy luận. |
| Bài tập và kết luận | Cuối Chương có câu hỏi suy luận trên dữ kiện, không áp quota. Kết luận kỹ thuật chỉ tóm quan hệ/giới hạn đã chứng minh, không thêm claim mới. |

## Mục lục, bookmark và tham chiếu

Mục lục PDF có ít nhất Phần và Chương; Bài/Mục xuất hiện trong mục lục mở rộng hoặc bookmark cấp 3 khi mật độ không gây quá tải. Bookmark không dựa duy nhất vào số lượng: mỗi đích phải là trang bắt đầu đúng heading, đúng thứ bậc và thứ tự. Cross-reference trong bản thảo là ID ổn định; renderer đổi thành số Chương/Bài/Hình và trang sau khi pagination ổn. Link nội bộ nếu có phải tới đích hợp lệ. Không để “xem Chương 16” cũ sau migration mà không biết đó là scheduling, storage hay HPA.

Đánh số hình/bảng theo Chương để thêm hình không làm lệch toàn sách; ID kỹ thuật Vxx độc lập với số in. Caption đặt cùng trang hoặc ngay dưới hình; nếu hình lớn buộc tách trang, dành trang hình riêng và chỉ dẫn ở văn bản. Tránh hình bị co quá nhỏ để giữ caption. Danh mục hình có thể có nếu giúp tra cứu, nhưng **không có danh mục nguồn/bibliography** trong PDF. Các nguồn, phiên bản, ngày kiểm chứng và claim anchor vẫn ở `source_map.json`, `source_ids.lock.json`, `references.md` hoặc hồ sơ A2 ngoài render. URL thực sự thuộc ví dụ kỹ thuật vẫn được phép theo hợp đồng hiện hành.

Lời giải đặt cuối sách, sau toàn bộ nội dung và trước phụ lục tra cứu nếu Reviewer chọn. Mã câu hỏi ổn định trong migration; khi A2 đổi số in, duy trì ánh xạ old ID→new ID và test để không thất lạc 79 cặp hiện có. Lời giải không cần lặp trọn đề; phải chỉ rõ dữ kiện dùng, phép suy luận, giới hạn và phép kiểm thực tế khi thích hợp. Bài tập thuộc một Chương chính; nếu bài gốc liên quan nhiều Chương, chỉ đặt một lần rồi cross-reference.

## Khổ trang và kiểm chứng A2

Giữ A4, Times New Roman cho văn xuôi/heading và monospace nhúng cho code theo hợp đồng hiện tại cho đến khi Reviewer duyệt thay đổi typography. Trang mới phải có lề an toàn, không clipped text, code/table width được đo, Unicode tiếng Việt đọc được, bookmark trỏ đúng, source-free PDF ở text, metadata, outline và URI. PDF candidate được dựng từ nguồn A2, không đè bản phát hành. QA gồm audit cấu trúc tự động, trích xuất text đại diện và **render/quan sát từng trang** ở cỡ in; một build PASS không phải publication PASS. Nếu A2 chưa tạo hình hoặc renderer chưa hỗ trợ đối tượng, ghi SKIP/tồn đọng và không giả vờ đối tượng đã có.
