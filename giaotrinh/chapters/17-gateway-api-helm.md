# Chương 17. Gateway API và Helm: bản phát hành gặp đường đi của request

Chương 15–16 cho thấy object được API nhận, Pod được đặt và Service có endpoint vẫn là những sự kiện khác nhau. Khi người dùng ở ngoài cluster gửi request, còn có ranh giới định tuyến vào cluster. Helm giúp tạo và cập nhật một nhóm object theo bản phát hành; Gateway API khai báo nơi lưu lượng đi vào và cách chọn backend. Helm không phải bộ định tuyến, còn Gateway API không tự chạy proxy. Để một request thành công, bản phát hành, controller Gateway, dataplane, Service, Pod và ứng dụng phải cùng thỏa điều kiện tại thời điểm thử.

## 17.1. Từ GatewayClass tới HTTPRoute

Gateway API là nhóm API mở rộng: cluster cần CRD tương ứng và một triển khai controller hỗ trợ phiên bản, loại Route và tính năng đang dùng. `GatewayClass` là object phạm vi cluster, chỉ ra `controllerName` của triển khai. Quản trị viên có thể chuẩn bị class; tên class trong bản khai báo không làm controller xuất hiện. `Gateway` là object có namespace, chọn class và khai báo các `listener`: cổng, protocol, hostname, chính sách Route được phép gắn, và khi cần thì cấu hình TLS. Controller được chọn có thể tạo load balancer mới, sửa proxy hiện có hoặc lập trình hệ thống mạng khác; API không quy định một proxy cố định cho mọi triển khai.

`HTTPRoute` mô tả một hay nhiều luật HTTP. `parentRefs` chọn Gateway, có thể chỉ rõ listener qua `sectionName`; Gateway listener cũng phải cho phép Route gắn vào. `hostnames` và `matches.path` thu hẹp request phù hợp, còn `backendRefs` chỉ nơi gửi tiếp, thường là Service cùng namespace và cổng Service. Địa chỉ DNS của client phải tới địa chỉ thực của Gateway; HTTP `Host` hoặc TLS SNI phải phù hợp với listener và Route. Có Route đúng mà DNS trỏ tới một proxy cũ thì request vẫn không đi qua nó. Có Gateway nhận request mà không có Route phù hợp thì phản hồi có thể là 404 do dataplane; cần kiểm tra status, request và cấu hình triển khai trước khi quy nguyên nhân từ mã HTTP.

Quan hệ gắn Route có hai phía: Route gọi tên parent, còn listener giới hạn loại Route và namespace qua `allowedRoutes`. Mặc định thông dụng là chỉ Route cùng namespace; trong ví dụ dưới đây `from: Same` được viết tường minh. Nếu Route ở namespace khác, Gateway có thể cho phép namespace bằng `allowedRoutes`, nhưng điều đó không tự cho Route quyền trỏ tới Service ở namespace thứ ba. Tham chiếu chéo namespace tới backend hoặc TLS Secret cần `ReferenceGrant` tại namespace chứa object đích, với nguồn và đích được khai báo cụ thể. Trường hợp Route ở namespace khác gắn Gateway là ngoại lệ của cơ chế ReferenceGrant và do `allowedRoutes` điều khiển. Không mở `allowedRoutes: All` hoặc tạo grant rộng chỉ để làm mất lỗi cấu hình; quyền gắn Route là quyền chiếm một phần bề mặt lưu lượng.

Với HTTPS termination, listener của Gateway dùng TLS Secret để bắt tay với client; sau điểm giải mã, HTTPRoute có thể so hostname/path và chuyển request tới backend. Secret thường ở cùng namespace với Gateway; tham chiếu Secret ở namespace khác cần grant phù hợp và hỗ trợ từ triển khai. SNI, chứng chỉ, tên host và nơi chấm dứt TLS phải được xét cùng nhau. TLS ở Gateway không mặc nhiên mã hóa chặng Gateway → Service/Pod. Ví dụ chart dưới đây cố ý chỉ dùng HTTP để không giả vờ có chứng chỉ hoặc bảo đảm bảo mật của chặng bên trong; muốn dùng trong hệ thống thật phải thiết kế TLS và ranh giới tin cậy riêng.

## 17.2. Status là bằng chứng của controller, không phải phép thử request

`GatewayClass.status.conditions` cho biết class có được triển khai chấp nhận hay không. Trên Gateway, đọc `Accepted`, `Programmed`, status của từng listener và địa chỉ được cấp nếu có. `Accepted=True` nghĩa cấu hình được controller nhận ở mức tương ứng; `Programmed=True` nói controller đã lập trình cấu hình xuống dataplane theo hợp đồng của nó, không chứng minh DNS, firewall, TLS hay Pod phía sau hoạt động. Trên HTTPRoute, đọc `status.parents` đúng parent/controller, điều kiện `Accepted` và `ResolvedRefs`; `ResolvedRefs=False` có thể chỉ backend hoặc tham chiếu khác không tồn tại hay không được phép. Một Route có nhiều parent có thể được parent này nhận nhưng parent kia từ chối. Luôn so `observedGeneration` trong condition với `metadata.generation` trước khi dùng status để đánh giá bản spec mới.

Ingress vẫn là API Kubernetes đang tồn tại và vẫn được controller tương ứng triển khai; Gateway API mở rộng mô hình vai trò Gateway/Route và cho phép chia quyền cấu hình rõ hơn. Không đổi một Ingress thành Gateway chỉ bằng cách đổi `kind`. Cần kiểm tra loại Route, tính năng được controller cụ thể hỗ trợ, đối tượng TLS và cách dataplane nhận lưu lượng. Cả Ingress lẫn Gateway đều cần một controller thực thi; sự tồn tại của object trong API server chỉ xác nhận bản khai báo được lưu.

## 17.3. Helm đi từ chart tới revision, không theo dõi sức khỏe nghiệp vụ

Một chart là gói đầu vào. `Chart.yaml` chứa tên và version của chart, `values.yaml` đặt giá trị mặc định, còn `templates/` là mẫu được Helm render bằng Go template và values cuối cùng. Giá trị do người dùng truyền qua `-f` hoặc `--set` có thể ghi đè mặc định; `--reuse-values` khi upgrade có thể kéo theo một giá trị cũ mà người sửa chart tưởng đã bỏ. `helm lint` kiểm tra chart ở mức tĩnh; `helm template` cho thấy YAML render từ release name, namespace và values đã chọn mà không cần cluster. Bản YAML ấy chưa được API server chấp nhận, chưa có CRD/controller và chưa thể nói request sẽ đi đâu.

Khi `helm install` tạo release, Helm gửi manifest đã render đến API server và ghi lại lịch sử release. `helm upgrade` render lại với chart/values mới và tạo revision tiếp theo; `helm history` và `helm get manifest` giúp phân biệt revision đã ghi với cấu hình đang có trong cluster. Chart version, `appVersion`, revision và image digest là bốn danh tính khác nhau; một revision mới có thể chỉ đổi hostname, không thay image. `helm rollback` tạo một revision mới dựa trên revision cũ, rồi cập nhật các object Helm quản lý; nó không quay ngược cơ sở dữ liệu, request đã xử lý, dữ liệu trên volume hay thay đổi bên ngoài chart. `helm uninstall` bỏ các object trong phạm vi release theo quy tắc Helm, không phải lệnh dọn mọi dữ liệu liên quan. Giá trị, template và manifest có thể được giữ trong release metadata, thường là Kubernetes Secret của Helm 3; Secret không phải nơi an toàn để ghi credential vào chart/values rồi đưa output `helm template` hoặc `helm get` lên log công khai.

`--wait` có thể chờ một số điều kiện Ready của tài nguyên Kubernetes trong thời hạn cấu hình, nhưng không thay thế request đại diện qua Gateway, kiểm tra dữ liệu hay xác nhận backend nghiệp vụ. Một chart render đúng vẫn có thể fail khi API server không có CRD hoặc cấm quyền; một upgrade được ghi nhận vẫn có thể để controller Gateway từ chối Route hay Pod chưa Ready. Vì vậy cần giữ riêng bốn ảnh chụp: chart/values đã chọn, manifest của revision, trạng thái object hiện tại và phản hồi từ đúng client.

## 17.4. Ví dụ tối giản: chart sở hữu cửa vào, ứng dụng đã có Service

Chart `atlas-gateway` chỉ tạo Gateway và HTTPRoute trong namespace của release; nó trỏ tới Service `atlas:80` đã có từ Chương 15. Đây là ví dụ cấu hình, chưa có kết quả chạy trên cluster. Trước khi thử, quản trị viên phải có Gateway API CRD, `GatewayClass` tên `example-gateway` do một controller thật quản lý, namespace `demo`, Service `atlas` và backend Ready. Chữ `example-gateway` không phải tên class mặc định của Kubernetes. Manifest Chương 15 không đặt namespace; nếu thử nó trong cluster cô lập đã được phép, chạy `kubectl -n demo apply -f` với đường dẫn tệp đó, sau khi đã hiểu hai lỗi cố ý và sửa trên bản sao thử nghiệm. Đừng áp manifest lỗi lên workload đang phục vụ.

`Chart.yaml` và `values.yaml` định nghĩa đầu vào, không chứa credential:

{{code:examples/gateway-helm/Chart.yaml}}

{{code:examples/gateway-helm/values.yaml}}

Gateway tạo listener HTTP cổng 80, giới hạn Route cùng namespace. Namespace lấy từ release để tên Gateway và Route không bị tách nhầm.

{{code:examples/gateway-helm/templates/gateway.yaml}}

HTTPRoute gắn đúng listener qua `parentRefs`, so hostname và chuyển path bắt đầu bằng `/` tới cổng Service. `backendRefs.port` là cổng Service, không phải `targetPort` của Pod:

{{code:examples/gateway-helm/templates/httproute.yaml}}

Trên máy có Helm 3, `helm lint` và `helm template atlas-edge ./examples/gateway-helm --namespace demo` kiểm tra chart và cho manifest dự kiến. Thử ghi đè hostname bằng một values file thử nghiệm rồi so bản render; kiểm tra `metadata.namespace=demo`, `atlas-edge-web`, tên listener `http`, host và backend. Không dùng render cục bộ như bằng chứng API/CRD/controller chấp nhận. Nếu triển khai trong cluster được cho phép, cần kiểm tra GatewayClass đã Accepted, Gateway/listener đã Programmed, HTTPRoute parent Accepted/ResolvedRefs, địa chỉ Gateway, DNS trỏ đúng địa chỉ và request có `Host: atlas.example.test` từ một client xác định. Không tự cài CRD, controller hay tạo Gateway ngoài môi trường được giao chỉ để chứng minh ví dụ sách.

## 17.5. Sự cố giả định: upgrade xanh, bên ngoài vẫn lỗi

Giả sử revision 4 của release `atlas-edge` dùng host `atlas.example.test` và Service `atlas:80`; một request kiểm thử qua địa chỉ Gateway đã thành công. Revision 5 được tạo bằng `helm upgrade` với file values mới đặt `hostname: api.example.test`. Lệnh hoàn tất và hai object mới tồn tại, nhưng DNS của khách hàng vẫn đưa `atlas.example.test` tới đúng Gateway. Đây là dữ liệu giả định, không phải log Helm, kubectl hoặc proxy đã chạy. So chart và values được dùng cho revision 5 với `helm get manifest` của revision đó: cả listener lẫn Route nay chọn `api.example.test`. Request mang Host cũ không khớp cấu hình mới, nên một phản hồi 404 tại Gateway là giả thuyết mạnh; vẫn phải xác định chính gateway nào đã trả mã và điều kiện listener/Route ở generation mới. Sửa values cho đúng host và upgrade có kiểm tra, hoặc rollback sang revision đã biết rồi xác nhận request cũ; chỉ nhìn chữ `deployed` của Helm không đủ.

Nếu host và attachment đều đúng nhưng nhận 503, lần tiếp theo là `backendRefs` → Service/port → EndpointSlice có endpoint Ready → Pod readiness → ứng dụng. Trong nhiều triển khai, không có backend khỏe có thể hiện thành 503, nhưng mã ấy không tự định danh lỗi: proxy khác, policy, timeout kết nối backend hoặc ứng dụng cũng có thể góp phần. `ResolvedRefs=False` gợi ý Service/Secret sai tên, sai namespace hoặc thiếu grant; `Accepted=False` trên Route gợi ý Route chưa attach, `Programmed=False` trên Gateway gợi ý controller/dataplane chưa hoàn tất. Nếu tất cả condition đều hiện True nhưng request timeout, kiểm tra địa chỉ và DNS, đường client → Gateway, firewall, listener thực tế, rồi thử từ vị trí gần backend để tách chặng lỗi. Một status True có `observedGeneration` cũ không được dùng để minh oan revision 5.

Khi rollback, ghi rõ revision đích, manifest cũ, các object live trước/sau và thời điểm lưu lượng chuyển. Nếu revision 5 kèm migration schema hay đã ghi dữ liệu vào backend, đổi Route về host cũ không khôi phục dữ liệu. Hậu điều kiện cần có request từ client ở đúng hostname/SNI và path, response mong đợi, EndpointSlice còn backend Ready, và kiểm tra dữ liệu nếu ứng dụng có ghi. Đây là phép xác nhận một lần tại thời điểm đo, không phải bảo đảm lâu dài.

## Bài tập

C17.1. Chart đã render Gateway và HTTPRoute hợp lệ về YAML, nhưng GatewayClass chưa tồn tại. Dự đoán thứ tự bằng chứng cần đọc trước khi chẩn đoán 404 từ client. Điều gì chưa thể kết luận từ `helm template`?

C17.2. HTTPRoute ở namespace `app` trỏ tới Gateway ở namespace `edge`, listener chỉ cho Route cùng namespace. Một kỹ sư thêm ReferenceGrant ở `edge` cho Route này. Vì sao Route có thể vẫn không attach? Nếu Route còn trỏ Service ở namespace `data`, cần cơ chế quyền nào khác?

C17.3. Sau upgrade, `HTTPRoute.status.parents` cho parent đúng có `Accepted=True`, `ResolvedRefs=False`, còn Service dự kiến không có trong namespace của Route. Suy luận nhánh lỗi hợp lý và phép kiểm tra tiếp; vì sao không nên chỉ tăng timeout?

C17.4. Revision 7 đổi hostname và image, đồng thời ứng dụng ghi dữ liệu theo schema mới. `helm rollback` về revision 6 hoàn tất. Nêu ba hậu điều kiện độc lập phải chứng minh trước khi nói dịch vụ đã phục hồi.

C17.5. Người dùng báo timeout nhưng Gateway `Programmed=True` ở generation mới, HTTPRoute Accepted/ResolvedRefs True và Service có endpoint Ready. Hãy thiết kế phép thử phân biệt đường client tới Gateway, Gateway tới Pod và lỗi ứng dụng; chỉ rõ giới hạn của mỗi condition.
