# Chương 6. Git là đồ thị lịch sử, không phải thư mục sao lưu

Khi hai người cùng sửa một dịch vụ, câu hỏi không chỉ là “tệp cuối cùng trông ra sao” mà còn là thay đổi nào đã được ghi, thay đổi nào chưa, và hai dòng phát triển có chung tổ tiên nào. Git lưu các snapshot có liên kết cha–con. Hiểu liên kết ấy giúp ta chọn cách tích hợp, đọc conflict và phục hồi sự cố mà không làm mất lịch sử của đồng đội. Các ký tự `A`, `B`, `C` trong chương là nhãn tượng trưng cho commit, không phải SHA thật; tình huống là mô hình giả định, không phải log của repo này.

## 6.1. Từ nội dung tệp tới commit có cha

Một blob chứa nội dung tệp, không chứa tên tệp. Một tree ghép tên, mode và định danh object của blob hoặc tree con thành snapshot thư mục. Commit trỏ tới một tree gốc, ghi tác giả, người tạo commit, thông điệp và không hoặc nhiều commit cha. Vì vậy đổi tên tệp có thể đổi tree mà blob nội dung vẫn giữ nguyên; hai commit khác nhau có thể trỏ tới cùng snapshot tệp nhưng khác cha hoặc metadata. Git lưu lịch sử bằng các quan hệ này, không phải bằng cách chép nguyên một thư mục có nhãn thời gian cho mỗi commit.

Định danh object là giá trị băm của loại, độ dài và nội dung object theo định dạng kho đang dùng. Nhiều kho dùng SHA-1; Git cũng hỗ trợ kho SHA-256. Vì commit chứa định danh tree và cha, thay nội dung một tệp làm đổi blob, tree chứa nó và các commit mới đi qua thay đổi ấy. Định danh cho phép kiểm tra tính nhất quán nội dung trong kho; nó không tự chứng minh ai là tác giả hay rằng mã an toàn. Tên branch và tên file không nằm trong blob. Để tự đối chiếu mô hình trên một kho được phép đọc, `git cat-file -p HEAD` cho thấy trường tree và parent của commit; `git ls-tree HEAD` cho thấy các mục ở tree gốc. Một SHA rút gọn chỉ là cách viết đủ phân biệt trong kho hiện tại, không phải một loại object khác.

## 6.2. Ba trạng thái cần phân biệt trước khi commit

Working tree là những tệp đang thấy và sửa bằng trình biên tập. Index là snapshot dự kiến cho commit kế tiếp; `git add` chép nội dung hiện tại của đường dẫn vào index tại thời điểm chạy. `HEAD` thường là tham chiếu tượng trưng tới branch đang checkout, còn branch ref trỏ tới một commit. Khi tạo commit, Git ghi tree từ index, đặt commit mới có cha là commit tại `HEAD`, rồi dịch ref của branch hiện tại sang commit mới. Sửa tệp sau `git add` không tự cập nhật index; commit có thể chứa bản cũ trong khi working tree vẫn có sửa đổi mới.

Giả sử `timeout_ms` trong commit hiện tại là `1000`. Ta sửa working tree thành `2000`, stage, rồi sửa tiếp thành `3000`. Lúc ấy `HEAD` giữ `1000`, index giữ `2000`, working tree giữ `3000`. `git diff --cached` so `HEAD` với index, còn `git diff` mặc định so index với working tree. Nếu commit ngay, snapshot mới ghi `2000`; muốn ghi `3000` phải stage lại và kiểm tra diff. Đây là lý do `git status` và diff trước commit có giá trị hơn lời khẳng định “tôi đã lưu file”. Tệp chưa được theo dõi chưa tự có trong index.

## 6.3. Branch là ref; merge là kết quả của hai dòng lịch sử

Xét commit `B` có `timeout_ms=1000`. Nhánh `main` đi từ `B` tới `D`, đặt `timeout_ms=3000` để giảm timeout sai ở cổng vào. Nhánh `feature/retry` đi từ `B` tới `C`, đặt cùng dòng thành `timeout_ms=2000` để thử retry. Đồ thị trước tích hợp là `A → B → D` trên `main` và `B → C` trên `feature/retry`; `B` là tổ tiên chung gần nhất. Tên branch chỉ là ref có thể dịch chuyển; `D` và `C` là hai object commit vẫn còn nguyên khi ref đổi.

Nếu `main` vẫn ở `B`, tích hợp `C` có thể fast-forward: chỉ dịch ref `main` tới `C`, không tạo commit hai cha. Ở đây `main` đã tới `D`, nên fast-forward không đủ. Merge ba phía so snapshot ở `B`, `D` và `C`. Cả hai phía thay cùng dòng theo hai cách nên Git không thể chọn đúng ý định nghiệp vụ; nó dừng với conflict. Trước khi người vận hành giải quyết, `HEAD` vẫn là `D`, `MERGE_HEAD` ghi phía `C`, index có thể giữ ba stage cho tệp xung đột: stage 1 là bản ở `B`, stage 2 là phía `HEAD`/`D`, stage 3 là phía `MERGE_HEAD`/`C`. Dấu `<<<<<<<`, `=======`, `>>>>>>>` trong working tree chỉ là trình bày vùng chưa giải quyết, không phải cấu hình được phép đưa vào production.

Quyết định đúng không thể suy từ câu “lấy ours” hay “lấy theirs”. Nhóm phải kiểm tra hợp đồng timeout và retry. Giả sử kiểm thử cho thấy upstream cần ngưỡng `2500` và retry chỉ dành cho thao tác idempotent. Người tích hợp viết `timeout_ms=2500`, cập nhật kiểm thử liên quan, rồi stage tệp đã giải quyết. Khi đó index có bản thường thay cho ba stage xung đột; `git diff --cached` cho thấy snapshot sắp ghi, và `git ls-files -u` không còn mục chưa giải quyết. Chạy kiểm thử cấu hình và hành vi retry trên kết quả cuối, xem diff để bảo đảm không còn marker; chỉ sau đó tạo merge commit `M` với hai cha theo thứ tự `D` và `C`. Ref `main` dịch tới `M`, còn ref `feature/retry` vẫn ở `C` nếu chưa xóa. Nếu chưa hiểu cách giải, `git merge --abort` có thể đưa merge về trước khi bắt đầu, nhưng với thay đổi chưa commit trước merge không nên mặc định rằng mọi thứ luôn khôi phục hoàn hảo; hãy bắt đầu từ working tree sạch.

## 6.4. Rebase thay gốc bằng commit mới

Thay vì merge, trên nhánh feature chưa chia sẻ có thể rebase `C` lên `D`: Git lấy thay đổi mà `C` đưa vào so với `B`, thử áp dụng lên `D`, rồi tạo commit mới `C′` có cha là `D`. Vì `D` đã sửa cùng dòng, rebase cũng có thể dừng để con người giải conflict. Sau khi giải và tiếp tục, ref feature trỏ tới `C′`; `C` cũ không bị sửa tại chỗ. Ngay cả khi snapshot cuối cùng giống kết quả merge, đồ thị khác: `A → B → D → C′` là một đường, trong khi merge tạo `M` có hai cha `D` và `C`. Giá trị băm của `C′` khác `C` vì nội dung commit, đặc biệt parent, khác.

Rebase thuận tiện để sắp xếp các commit của chính mình trước khi công bố. Nếu người khác đã dựa vào `C` trên một branch dùng chung, đẩy lịch sử rebase lên sẽ buộc ref từ xa rời đường cũ và làm bản sao của họ lệch nhau; cần phối hợp rõ trước mọi lần viết lại lịch sử đã chia sẻ. Với nhánh tình huống này đã có người cùng dùng, chọn merge để giữ cả `C` và `D` trong lịch sử công khai. Cả merge lẫn rebase chỉ xử lý cách ghép lịch sử và nội dung; không tự chứng minh bản `timeout_ms=2500` đúng. Chạy lại phép kiểm chứng trên snapshot tích hợp là điều bắt buộc.

## 6.5. Revert thêm lịch sử; reset dịch vị trí

Nếu một commit thường đã công bố gây lỗi, `git revert` tạo commit mới đảo tác động của commit được chọn trên trạng thái hiện tại. Commit lỗi vẫn có trong đồ thị, người khác có thể lấy commit đảo chiều bằng cách đồng bộ bình thường; revert cũng có thể xung đột nếu mã đã thay đổi thêm. Muốn revert chính merge commit `M` của ví dụ, phải chỉ định parent làm dòng chính: `git revert -m 1 M` xem `D` là mainline rồi đảo thay đổi mà merge đưa vào so với `D`. Cần xem diff và kiểm thử vì thao tác này không có nghĩa “quay toàn bộ repo về B”, và về sau merge lại cùng nhánh có thể không tự mang lại các thay đổi đã bị đảo.

`git reset <commit>` ở dạng dịch `HEAD` đặt ref branch hiện tại về commit được chọn; chế độ `--soft`, mặc định `--mixed`, và `--hard` lần lượt ảnh hưởng khác nhau tới index và working tree. `--hard` còn có thể bỏ thay đổi local chưa commit ở các tệp được theo dõi. Dịch ref `main` từ `M` về `D` sẽ làm lịch sử branch công bố không còn đi qua `M`, dù object có thể còn tạm được tham chiếu ở nơi khác. Vì thế reset là công cụ sửa lịch sử cục bộ khi đã hiểu trạng thái; nó không thay revert trên nhánh đã chia sẻ. Khôi phục một tệp trong working tree hoặc bỏ stage là tác vụ khác với dịch branch ref; đừng dùng một lệnh dịch lịch sử để chữa nhầm một file đang sửa.

## 6.6. Đọc chứng cứ trước khi chọn hành động

Khi nhận một conflict thật, trước hết xác định branch đang checkout, working tree có sạch trước khi tích hợp không, và hai commit đầu nhánh cùng merge base. Sau đó đọc ba phiên bản của tệp, xác định mỗi thay đổi phục vụ yêu cầu nào; conflict marker chỉ cho vị trí chồng lấn, không cho quyết định đúng. Kiểm tra diff đã stage và đồ thị cha sau commit, chạy test trên snapshot vừa tích hợp, rồi mới chia sẻ. Nếu test thất bại, phân biệt lỗi từ code đã commit với sửa đổi chỉ còn trong working tree; một `git status` sạch không thay thế kiểm thử. Nếu cần hủy ảnh hưởng trên branch chung, chuẩn bị một revert có review; nếu cần thử lại một merge đang dở, kiểm tra trạng thái trước khi abort. Sự an toàn đến từ việc biết ref, index và working tree nào đang thay đổi ở mỗi bước.

## Bài tập

C6.1. Commit `B` chứa `timeout_ms=1000`. Sau `git add` bản `2000`, người học sửa working tree thành `3000` nhưng chưa stage lại. `HEAD`, index và working tree lần lượt giữ gì? Commit ngay sẽ ghi giá trị nào và phép so sánh nào chứng minh điều đó?

C6.2. Trên đồ thị `A → B → D` của `main` và `B → C` của feature, vì sao không thể fast-forward `main` tới `C` mà giữ `D`? Nếu giải conflict rồi merge thành `M`, nêu hai cha và trạng thái các branch ref. Index có gì khi conflict đang dở?

C6.3. Nếu rebase `C` lên `D` và giải cùng conflict, đồ thị mới và định danh commit feature thay đổi ra sao? Vì sao phương án này cần cân nhắc khác khi `C` đã được chia sẻ? Hai cách tích hợp có tự xác nhận timeout mới là đúng không?

C6.4. Merge commit `M` đã lên branch chung rồi gây lỗi. So sánh mục tiêu và hậu quả của revert `M` với reset `main` về `D`; vì sao revert merge cần chọn mainline? Cần kiểm chứng gì trước khi push?
