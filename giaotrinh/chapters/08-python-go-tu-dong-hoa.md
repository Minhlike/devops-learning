# Chương 8. Python và Go: điều phối tác vụ, giữ đúng ranh giới lỗi

Chương 7 cho thấy một pipeline Bash có thể che mã lỗi của bước sao lưu. Chuyển cùng việc ấy sang Python hoặc Go không tự sửa sai: chương trình vẫn có thể nhận lỗi rồi bỏ qua và in thông báo thành công. Khác biệt hữu ích nằm ở cách biểu diễn đối số, kết quả, thời hạn và trạng thái của từng bước. Ta sẽ điều phối ba bước nhỏ: kiểm tra điều kiện, áp dụng thay đổi giả, xác minh kết quả. Không bước nào chạm hệ thống thật; helper chỉ ghi vào thư mục tạm được đánh dấu cho demo.

## 8.1. Khi nào giữ Bash, khi nào dùng Python hoặc Go?

Bash phù hợp cho vài lệnh tuyến tính trên một máy, với đầu vào nhỏ và hợp đồng lỗi rõ. Khi phải giữ trạng thái qua nhiều bước, đọc cấu hình có cấu trúc, kiểm tra dữ liệu, phân loại lỗi và kiểm thử nhánh phục hồi, Python thường cho mã dễ đọc hơn. Thư viện chuẩn của Python đã có subprocess, xử lý tệp, JSON và kiểm thử; đổi ngôn ngữ chỉ để gọi một lệnh đơn lẻ không mang lại an toàn. Go phù hợp khi cần một chương trình biên dịch triển khai trên nhiều máy, kiểu dữ liệu và luồng lỗi tường minh, hoặc nhiều tác vụ I/O đồng thời với cancellation chung. Một binary Go vẫn phụ thuộc hệ điều hành, kiến trúc, tùy chọn build và có thể phụ thuộc thư viện động; “một file” không có nghĩa chạy được ở mọi nơi. Python cần interpreter và môi trường package tương thích. Quyết định dựa trên độ phức tạp trạng thái, môi trường triển khai, năng lực nhóm và chi phí vận hành, không dựa trên nhãn “ngôn ngữ DevOps”.

Trong cả ba ngôn ngữ, chương trình điều phối không đồng nhất với tác vụ nó khởi chạy. Một lệnh con có thể chạy xong và trả status khác 0; không khởi chạy được; bị timeout; hoặc trả 0 nhưng kết quả nghiệp vụ sai. Từng trạng thái cần chính sách riêng. Exit status là quan sát từ tiến trình con, còn “triển khai thành công” là kết luận sau khi kiểm tra hậu điều kiện. Không ghép hai ý ấy thành một biến boolean duy nhất.

## 8.2. Đối số, cấu hình và môi trường thực thi

Python `subprocess.run` nhận danh sách đối số; Go `exec.CommandContext` nhận tên chương trình cùng từng đối số. Hai API này mặc định không gọi shell. Giá trị như `"a; rm -rf ..."` đi thành một đối số, không thành lệnh thứ hai. Điều đó chặn một kiểu shell injection tại ranh giới này, nhưng utility con vẫn có thể hiểu dấu gạch đầu như tùy chọn, đọc file cấu hình độc hại hoặc tự gọi shell. Nếu cố dùng `shell=True` hay `sh -c` với chuỗi ghép từ đầu vào, ranh giới parsing của Chương 7 trở lại. Dùng argv tách rời, xác nhận giá trị theo schema và hợp đồng của chương trình con, chọn đường dẫn executable đáng tin, rồi dùng dấu kết thúc tùy chọn khi utility hỗ trợ.

Đường dẫn làm việc, `PATH`, biến môi trường, locale, quyền và tài nguyên của tiến trình con ảnh hưởng kết quả. Python `env=None` và Go `Cmd.Env=nil` cho con kế thừa môi trường hiện tại; điều này tiện trong demo nhưng có thể chuyển cả credential hoặc cấu hình ngoài dự kiến. Bí mật trong argv có thể lộ qua danh sách tiến trình hoặc log; bí mật trong environment cũng không phải két an toàn tuyệt đối. Đừng in nguyên command, exception, environment hoặc output khi chúng có thể chứa secret. Chỉ ghi mã bước, loại lỗi và request ID đã lọc; cấp secret qua cơ chế quản lý riêng với quyền tối thiểu. Trong ví dụ, output con bị bỏ đi vì ta đã biết helper nhỏ và chỉ cần status; công cụ thật cần log giới hạn kích thước, che dữ liệu nhạy cảm và đủ chứng cứ chẩn đoán.

## 8.3. Một lỗi được quan sát qua Python và Go

Helper sau là tác vụ giả. Nó chỉ hoạt động khi thư mục đích có file `.demo-only`. `apply_fail` ghi `partial` rồi trả 7. `apply_slow` ghi `partial`, ngủ lâu hơn hạn 0,3 giây, rồi mới định ghi `ready`. `verify` chỉ trả 0 nếu trạng thái là `ready`. Như vậy một lỗi hoặc timeout có thể để lại dấu vết của tác dụng phụ trước khi tiến trình con dừng. Không suy từ timeout rằng không có gì đã xảy ra.

{{code:examples/orchestration_probe.py}}

Chương trình Python gọi cùng helper theo thứ tự `precheck → apply → verify`. `subprocess.run` với `check=False` trả `CompletedProcess` khi con kết thúc bình thường, kể cả status 7 hoặc 8; người gọi phải đọc `returncode`. Nếu hết thời gian, API kết thúc và chờ tiến trình con trực tiếp rồi ném `TimeoutExpired`; nếu không khởi chạy được hoặc lời gọi I/O lỗi, có thể ném `OSError`. Trong demo, `124` và `125` chỉ là nhãn do chương trình điều phối tự chọn, không phải exit status do helper trả. Nhánh `bad` ghi nhận lỗi nhưng vẫn chạy bước sau và in `DEPLOY_OK`; nhánh `checked` dừng khác 0 ngay ở lỗi đầu. Cả hai nhánh cố ý để lại `partial` để người học thấy kết luận sai và giới hạn của việc dừng sớm.

{{code:examples/orchestrate_python.py}}

Go dùng `exec.CommandContext` để liên kết lệnh con với deadline. `Run` trả `nil` khi lệnh chạy và kết thúc thành công; status khác 0 thường cho `*exec.ExitError`, còn lỗi tìm executable hoặc I/O là loại lỗi khác. Khi context hết hạn, `CommandContext` mặc định yêu cầu kill tiến trình con trực tiếp; `ctx.Err()` giúp nhận biết deadline trong ví dụ. Mã phải kiểm tra `err`, không được chỉ ghi log rồi bỏ qua. Nhánh `bad` dưới đây mắc đúng lỗi quyết định đó; nhánh `checked` dừng. `io.Discard` giữ output con ngoài log demo, không phải mẫu quan sát phù hợp cho mọi dịch vụ.

{{code:examples/orchestrate_go.go}}

Trong phép thử có kiểm soát trên Python 3.12 và Go 1.27.1, cả hai bản điều phối đều cho cùng bốn loại kết quả: chế độ `ok` in `DEPLOY_OK` và thoát 0; `bad fail` in `DEPLOY_OK` dù `apply` trả 7 và `verify` trả 8; `checked fail` thoát 1 ở `apply`; `checked slow` thoát 1 vì timeout. Sau các nhánh lỗi, file trạng thái vẫn là `partial`. Đây là output được đo cho chương trình demo, không phải dự đoán cho một quy trình triển khai thật. Thứ tự và tốc độ khởi tạo tiến trình có thể làm hạn 0,3 giây quá ngắn trên máy rất chậm; muốn kiểm thử ổn định hơn cần đồng bộ điểm bắt đầu hoặc tăng khoảng cách giữa thời gian tác vụ và deadline.

## 8.4. Timeout, cancellation và thất bại từng phần

Python `run(timeout=...)` bao cả thời gian giao tiếp với con sau khi nó được tạo, nhưng khởi tạo tiến trình trên một số nền tảng có thể chưa bị ngắt ngay đúng deadline. Go `CommandContext` gắn context cho command và mặc định kill process khi context kết thúc; nó không tự rollback file đã ghi. Cả hai ví dụ chỉ quản lý tiến trình con trực tiếp. Nếu con khởi chạy cháu, giữ pipe mở hoặc gọi một API từ xa đã nhận yêu cầu, hết hạn ở phía điều phối không chứng minh mọi tác vụ bên ngoài đã dừng. Với Go, việc chờ pipe đóng và cách hủy có thể cần `WaitDelay` hoặc quy ước shutdown riêng; với Python, một process group có thể cần quản lý riêng. Không mặc định kill toàn bộ cây tiến trình bằng một lời gọi.

Sau lỗi, phải xác định trạng thái bền vững hiện tại rồi mới quyết định thử lại, tiếp tục hay quay lui. Retry một thao tác ghi có thể nhân đôi tác dụng nếu lần đầu đã hoàn tất ở hệ thống đích nhưng phản hồi bị mất, như tình huống HTTP ở Chương 5. Chỉ retry khi thao tác idempotent theo hợp đồng, hoặc có khóa chống lặp và khả năng truy kết quả cũ; dùng số lần và tổng thời gian hữu hạn. `finally` của Python và `defer` của Go phù hợp giải phóng tài nguyên cục bộ, nhưng không thay giao dịch hay rollback phân tán; `os.Exit` trong Go còn bỏ qua các `defer` đang chờ ở cùng tiến trình. Việc xóa file `partial` mù quáng có thể che trạng thái cần điều tra hoặc xóa công việc hợp lệ của lượt khác. Demo dừng và giữ dấu vết, không tự tuyên bố đã khôi phục.

## 8.5. Đóng gói và kiểm chứng trước khi chạy ở nơi khác

Hai ví dụ chỉ dùng thư viện chuẩn. Với Python, ghi rõ phiên bản interpreter, tạo virtual environment cho package của dự án và khóa dependency theo công cụ đóng gói đã chọn; virtual environment là thứ tái tạo được, không nên coi thư mục của nó là artifact có thể di chuyển nguyên vẹn giữa máy. Với Go, module ghi yêu cầu ở `go.mod`, checksum dependency được quản lý ở `go.sum`; cần ghi cả phiên bản toolchain, target OS/architecture và cờ build khi muốn tái tạo binary. Không đưa secret vào package hoặc Git. Test nên chạy trong thư mục tạm có dấu hiệu nhận diện, xác minh cả status lẫn trạng thái cuối, rồi xóa đúng thư mục ấy sau khi đối chiếu. Với thay đổi thật, thêm kiểm thử hậu điều kiện từ góc nhìn người dùng, quan sát rollback và quyền thao tác; kết quả demo chỉ chứng minh các nhánh được thử trong môi trường thử.

## Bài tập

C8.1. Với `orchestrate_python.py bad fail`, dự đoán thứ tự các bước, status của helper ở từng bước, output cuối và nội dung `state.txt`. Vì sao `check=False` tự nó không phải lỗi, nhưng bỏ qua `returncode` là lỗi? Chế độ `checked` khác ở đâu?

C8.2. Với `orchestrate_go.go checked slow`, `ctx.Err()` và `err` cho biết những gì? Vì sao file vẫn có thể chứa `partial` dù điều phối đã thoát 1? Nêu điều gì không thể kết luận về tiến trình cháu hoặc dịch vụ từ xa.

C8.3. Một tên môi trường do người dùng nhập là `prod; echo LEAK`. So sánh truyền nó như một phần tử argv với ghép vào chuỗi `sh -c`. Vì sao argv tách rời vẫn phải kiểm tra schema và quy tắc tùy chọn của utility? Nêu một nơi có thể làm lộ secret dù không dùng shell.

C8.4. Sau timeout, người vận hành định retry vô hạn bước ghi và xóa `partial` trước mỗi lần. Phân tích rủi ro nhân đôi, mất chứng cứ và chạy đồng thời; đề xuất điều kiện tối thiểu để thử lại, cùng phép kiểm chứng hậu điều kiện. Khi nào Bash vẫn là lựa chọn hợp lý cho một tác vụ tương tự?
