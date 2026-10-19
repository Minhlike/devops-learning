"""Compile and audit the editorial architecture; never renders the textbook PDF.

The compact chapter declarations below are the editable source for the tree and
machine-readable graph. Run from any working directory with Python 3.12+.
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent

# Part records: ID, title, governing question, mental model, true prerequisites,
# boundary, exit capability, misconception, transfer to later parts.
PARTS = [
    ("P01", "Máy tính và tiến trình", "Một dòng mã trở thành công việc có thể quan sát bằng cách nào?", "Chương trình, tiến trình, luồng và tài nguyên là các thực thể khác nhau; thời gian là tổng của chạy, chờ và phối hợp.", "Không; chỉ cần đọc được một đoạn mã và phép chia đơn vị.", "Chưa quản trị Linux hoặc container; chỉ dựng mô hình phần cứng và hệ điều hành.", "Lần theo một lần chạy từ artifact tới PID, trạng thái và kết quả.", "Tệp thực thi đang có trên đĩa tức là tiến trình đã đổi phiên bản.", "Cho Linux, container, chẩn đoán hiệu năng và service lifecycle."),
    ("P02", "Linux và vận hành máy chủ", "Nhân cho phép, giới hạn và duy trì một dịch vụ như thế nào?", "Lời gọi hệ thống đi qua định danh, namespace tên, quyền, tài nguyên rồi tới supervisor; mỗi ranh giới có bằng chứng riêng.", "P01: tiến trình, địa chỉ ảo, CPU time và file descriptor.", "Không dạy OCI image hoặc Kubernetes; chỉ cơ chế và vận hành host.", "Phân biệt lỗi quyền, I/O, quota, tiến trình và readiness trên host.", "systemctl active nghĩa là ứng dụng đã sẵn sàng phục vụ.", "Cho Docker runtime, Ansible, Kubernetes node và điều tra sự cố."),
    ("P03", "Mạng và giao thức ứng dụng", "Một request đi từ tên tới byte phản hồi qua những ranh giới nào?", "Mỗi tầng chọn một đích hoặc hợp đồng: route/neighbor, kết nối, bảo mật phiên, ngữ nghĩa HTTP và proxy.", "P01 tiến trình/socket; P02 service listener trên host. Mạng namespace được giới thiệu sau ở P07.", "VPC, CNI và Gateway API chỉ áp dụng lại cơ chế, không dạy lại TCP từ đầu.", "Khoanh chặng hỏng bằng quan sát từ đúng phía client và server.", "Một status hoặc TCP established tự nó chỉ ra nguyên nhân gốc.", "Cho cloud network, container publishing, Service/Gateway và tracing."),
    ("P04", "Git và lịch sử thay đổi", "Làm sao biết, tích hợp và khôi phục đúng thay đổi đã chia sẻ?", "Blob/tree/commit là đồ thị bất biến; ref, index và working tree là trạng thái có thể dịch.", "P01: file và process; không cần cloud.", "Pipeline và release ở P06 dùng commit, không lặp object model.", "Giải conflict và chọn merge/rebase/revert dựa trên đồ thị.", "Branch là bản sao thư mục, reset là rollback an toàn cho nhánh chung.", "Cho identity của artifact, CI và supply chain."),
    ("P05", "Tự động hóa hệ thống", "Một chuỗi tác vụ báo đúng thất bại và có thể chạy lại thế nào?", "Parser, argv, status, deadline và tác dụng phụ qua nhiều tiến trình là các hợp đồng khác nhau.", "P01 process/exit; P02 quyền/file; P04 trạng thái thay đổi.", "Không thay Ansible/Terraform bằng script tùy tiện; dạy hợp đồng lỗi nền tảng.", "Viết và kiểm tra đường thành công, lỗi, timeout và trạng thái từng phần.", "set -e hoặc một exit 0 bảo đảm workflow thành công.", "Cho CI jobs, IaC automation, incident runbook."),
    ("P06", "Build, kiểm thử và phát hành", "Một commit trở thành artifact đang phục vụ người dùng bằng chứng cứ nào?", "Source, build inputs, artifact digest, test gate, deployment state và dữ liệu là các vòng đời tách biệt.", "P04 commit/ref; P05 status và retry; P03 request/readiness.", "Không triển khai chi tiết Kubernetes rollout ở đây; giữ mô hình phát hành độc lập nền tảng.", "Thiết kế cổng kiểm thử, rollout, dừng và hậu điều kiện rollback.", "Rollback binary tự đảo migration hay tác dụng phụ dữ liệu.", "Cho Docker image, Helm release, SRE change risk và supply chain."),
    ("P07", "Container và OCI", "Image trở thành tiến trình cô lập ra sao, và dữ liệu sống ở đâu?", "Namespace đổi góc nhìn, cgroup điều tiết tài nguyên; image là artifact, container là lần chạy, mount tách vòng đời dữ liệu.", "P01 process/memory; P02 Linux permissions/resource; P03 network; P06 artifact.", "Không coi Compose là scheduler nhiều node; Kubernetes ở P11.", "Lần theo image digest, PID, mount và dữ liệu qua recreate.", "Container là VM nhỏ hoặc volume tự được backup.", "Cho cloud native workload, Kubernetes runtime/storage và image security."),
    ("P08", "Cloud và AWS", "Một request qua ranh giới danh tính, mạng, tính toán và dữ liệu của cloud ra sao?", "Identity policy và đường mạng là hai bộ lọc độc lập; compute và storage có vòng đời, miền lỗi, chi phí khác nhau.", "P02 host; P03 route/TLS/HTTP; P06 release; P07 artifact.", "Terraform mô tả thay đổi cloud ở P09; không học HCL trong phần này.", "Phân biệt timeout, AccessDenied, lỗi target và mất dữ liệu bằng bằng chứng.", "Role gắn EC2 tự tạo đường tới AWS API; replication đồng nghĩa backup.", "Cho IaC, DR, reliability và cloud security."),
    ("P09", "Terraform và trạng thái hạ tầng", "Cấu hình, state và hạ tầng thực lệch nhau thì quyết định thay đổi thế nào?", "Provider dựng DAG rồi đọc state/API và thực hiện các tác vụ có thể thất bại từng phần; state là ánh xạ nhạy cảm.", "P04 Git; P06 change gate; P08 resource/IAM/network/data.", "Ansible hội tụ file bên trong máy ở P10, không được nhập nhằng với Terraform state.", "Đọc plan/replacement và phục hồi state hoặc object an toàn.", "Plan là giao dịch hoặc lock khóa cả console/cloud API.", "Cho vận hành production, drift control và change approval."),
    ("P10", "Ansible và hội tụ cấu hình", "Làm sao áp trạng thái mong muốn lên các máy đang tồn tại mà không gây restart thừa?", "Inventory chọn host, module quan sát rồi đổi trạng thái, handler hoãn tác động; kết quả theo từng host không phải giao dịch.", "P02 Linux quyền/systemd; P05 idempotency/status; P09 ranh giới IaC.", "Không tạo VPC/EC2 mới ở đây; không xem changed là health check.", "Chứng minh hai lượt hội tụ và xử lý drift, lỗi từng phần.", "Mọi shell task idempotent và check mode bảo đảm apply thật.", "Cho fleet operations, release orchestration và secrets."),
    ("P11", "Kubernetes và cloud native", "Khai báo biến thành Pod sẵn sàng phục vụ nhờ những vòng điều khiển nào?", "API lưu spec, controller/scheduler/kubelet/dataplane hội tụ bất đồng bộ; status, endpoint và request là các chứng cứ khác nhau.", "P02 Linux; P03 mạng; P07 container; P08 cloud; P06 release.", "Prometheus chuyên sâu ở P12; trước HPA chỉ dạy CPU time/request/resource metrics tối thiểu.", "Chẩn đoán apply xanh nhưng request hỏng qua object, node, network, storage và dữ liệu.", "Running/Bound/Programmed hoặc helm upgrade xanh đồng nghĩa người dùng thành công.", "Cho observability, SRE và Kubernetes security."),
    ("P12", "Observability và telemetry", "Dữ liệu quan sát được tạo, vận chuyển và diễn giải có giới hạn nào?", "Metric tổng hợp, log sự kiện và trace đường request là các phép chiếu có sai lệch lấy mẫu, mất dữ liệu và khác thời gian.", "P03 request; P05 status; P11 workload; P01 CPU time.", "SLO/incident response ở P13 dùng tín hiệu đã được kiểm định ở đây.", "Tính rate/p95, tìm request, đánh giá thiếu dữ liệu và hỏng pipeline quan sát.", "Dashboard xanh hoặc thiếu span chứng minh hệ thống khỏe hoặc thao tác không chạy.", "Cho SLI/SLO, alerting, incident và cost of telemetry."),
    ("P13", "SRE và phục hồi", "Độ tin cậy được định nghĩa, bảo vệ và khôi phục ra sao?", "SLI/SLO định nghĩa tác động người dùng; response dùng chứng cứ, DR dùng bản sao có thử khôi phục, capacity dùng tải và giới hạn.", "P06 release; P08 data/availability; P11 control loops; P12 telemetry.", "Các cơ chế backup/rollout được dùng làm quyết định vận hành, không giảng lại API sản phẩm.", "Lập error budget, điều phối sự cố và chứng minh phục hồi dữ liệu/nghiệp vụ.", "HA, replication và rollback đều là backup; postmortem là tìm người sai.", "Cho thiết kế production và đánh giá rủi ro bảo mật."),
    ("P14", "Security và DevSecOps", "Mối đe dọa đi qua identity, artifact, secret và runtime thế nào?", "Đặt trust boundary và tài sản trước công cụ; giảm quyền, chứng minh provenance, kiểm soát secret và đo hiệu lực policy.", "P03 TLS; P04 Git; P06 build; P07 image; P08 IAM; P11 Kubernetes; P13 incident.", "IAM AWS nền tảng ở P08; đây là phân tích đe dọa liên miền và kiểm soát.", "Dựng threat model và bằng chứng về quyền, dữ liệu, artifact và policy.", "Một scanner xanh hoặc một bản ký đủ chứng minh ứng dụng an toàn.", "Cho duyệt kiến trúc production và response sự cố bảo mật."),
    ("P15", "Thiết kế và vận hành production", "Làm sao ghép các cơ chế thành hệ thống đáng tin, đo được và có chi phí hợp lý?", "Luồng request, dữ liệu và control plane phải cùng được vẽ với miền lỗi, ngân sách, chủ sở hữu và kế hoạch phục hồi.", "P01–P14; dùng sau khi có SLO, threat model, IaC và bằng chứng vận hành.", "Không thêm công nghệ mới làm mục tiêu; tích hợp và phản biện đánh đổi.", "Bảo vệ một kiến trúc, canary, DR và cost plan trước tình huống thay đổi tải/lỗi.", "Nhiều lớp công cụ tự động đem lại độ tin cậy mà không cần kiểm chứng đầu cuối.", "Kết thúc sách bằng capstone có bằng chứng, giới hạn và quyết định vận hành."),
]

CHAPTERS: list[dict] = []


def add(part: str, title: str, goal: str, model: str, required: str,
        boundary: str, misconception: str, method: str, assessment: str,
        lessons: str, legacy: str = "", status: str = "planned_new",
        helpful: str = "", extension: str = "") -> None:
    number = sum(ch["part"] == part for ch in CHAPTERS) + 1
    cid = f"{part}.C{number:02d}"
    parsed = []
    for i, entry in enumerate(lessons.split("; "), 1):
        name, concepts = entry.split("~", 1)
        parsed.append({"id": f"{cid}.L{i:02d}", "parent": cid,
                       "title": name, "core": concepts,
                       "status": status if status != "mixed" else "needs_extension"})
    CHAPTERS.append({"id": cid, "part": part, "title": title,
                     "objective": goal, "mental_model": model,
                     "required": required.split() if required else [],
                     "helpful": helpful.split() if helpful else [],
                     "extension": extension.split() if extension else [],
                     "boundary": boundary, "misconception": misconception,
                     "teaching_strategy": method, "assessment": assessment,
                     "lessons": parsed, "legacy_chapters": legacy.split() if legacy else [],
                     "status": status})


# P01 — machine model, then the executable/process distinction.
add("P01", "Công việc, thời gian và đường đi dữ liệu", "Phân tích một request thành tính toán, chờ và tác dụng phụ.", "CPU time, wall time và dữ liệu đi qua bộ nhớ/I/O không hoán đổi được.", "", "Linux counter cụ thể ở P02.C03.", "CPU thấp chứng minh request không bị nghẽn.", "Dùng timeline giả định rồi đặt phép đo phân biệt giả thuyết.", "Tính lower bound latency và nêu đại lượng còn thiếu.", "Máy thực thi~lõi logic, bộ nhớ, thiết bị và đồng hồ; Đường thời gian~running, runnable, blocked, wall time và CPU time; Dữ liệu đi qua I/O~buffer, cache, thiết bị và ranh giới bền vững", "02", "mixed")
add("P01", "Chương trình, tiến trình và ranh giới nhân", "Lần theo một bản build đến hai tiến trình và kết quả từng nhánh.", "Tệp, process image, PID, descriptor và exit status là các đối tượng khác vòng đời.", "P01.C01.L02", "Quyền đường dẫn chi tiết ở P02.C02; service manager ở P02.C04.", "Thay binary trên đĩa thay process đang chạy.", "Đọc trace fork/execve thành công và lỗi, rồi đối chiếu trạng thái cha/con.", "Dự đoán PID, return value, descriptor và hậu trạng thái.", "Ba dạng ứng dụng~source, executable và process instance; Tạo và thay process~fork, execve, wait, exit và copy-on-write; Descriptor và identity~open file description, UID/GID và giới hạn", "01", "reviewed_draft")

# P02 — Linux is a system of mechanisms, not one survey chapter.
add("P02", "Syscall, đường dẫn và hệ thống tệp", "Giải thích tại sao cùng tên file có thể trỏ đối tượng khác.", "VFS phân giải từng thành phần đường dẫn rồi trả descriptor gắn đối tượng mở.", "P01.C02.L03", "Không dạy image layer hay cloud object store.", "Tên file, inode và descriptor là một.", "Lần theo openat, rename, symlink và lỗi EACCES/ENOENT.", "Giải thích log vẫn ghi vào file đã đổi tên và điều kiện fsync.", "Vào nhân~syscall, wrapper, errno và thao tác thật; Phân giải tên~directory traversal, inode, hard/symlink; Ghi và bền vững~page cache, rename, fsync file/thư mục", "01 02 03", "reviewed_draft")
add("P02", "Danh tính và quyền Linux", "Chẩn đoán một lần mở file bị từ chối qua mọi thư mục cha.", "UID/GID, mode và chính sách bảo vệ được xét tại thao tác cụ thể.", "P02.C01.L02", "AWS IAM và K8s RBAC có scope khác.", "Chỉ cần chmod file đích là đọc được.", "Đọc đường dẫn, identity, group và kết quả syscall trước khi sửa.", "Giải thích 0640 file dưới thư mục 0700 và sửa tối thiểu.", "Danh tính tiến trình~real/effective ID, group và capability ở mức giới thiệu; Bước đi qua thư mục~execute/search permission, owner/group/mode, ACL khi có; Điều tra và sửa~đúng UID, đường dẫn, least privilege, không chmod 777", "01 03", "reviewed_draft")
add("P02", "Tài nguyên và chẩn đoán hiệu năng Linux", "Phân biệt CPU runnable/quota, memory reclaim và I/O wait bằng counter.", "Đọc hiệu hai mẫu trong cùng cửa sổ rồi gắn với latency, không suy từ một snapshot.", "P01.C01.L03 P02.C01.L03", "cgroup v2 controller đầy đủ ở P07.C01; Prometheus ở P12.", "RAM cache luôn là lãng phí; throttled cycles là CPU utilization.", "Dùng bộ số Ch2 và phản biện các nguyên nhân cạnh tranh.", "Tính core từ usage_usec và PSI, nêu giới hạn nhân quả.", "CPU và scheduler~runnable, usage, quota và PSI; Memory~virtual/resident, reclaim, page cache, OOM; I/O và chẩn đoán~dirty/writeback, fsync, latency cửa sổ, counter đối chiếu", "02 10", "reviewed_draft")
add("P02", "systemd và vòng đời dịch vụ", "Tách start thành công khỏi listener, readiness và dữ liệu đúng.", "Unit dựng dependency/order và giám sát main process; ứng dụng có hợp đồng health riêng.", "P01.C02.L02 P02.C02.L03", "K8s probes ở P11.C02.", "After= kéo dependency hoặc network.target bảo đảm IP đã sẵn.", "Giải phẫu atlas.service và hai đường lỗi ExecStart/config.", "Phân biệt Type=exec, After/Wants/Requires, active và request thật.", "Unit graph~After, Wants, Requires, network-online; Process lifecycle~Type, ExecStart, signal, restart; Quan sát dịch vụ~MainPID, journal, socket, readiness và hậu điều kiện", "01 03", "reviewed_draft")
add("P02", "Vận hành host và phục hồi có kiểm chứng", "Đặt thay đổi cấu hình, log rotation và backup vào quy trình có hậu điều kiện.", "Độ an toàn nằm ở thứ tự và khả năng phục hồi dữ liệu, không ở lệnh đơn lẻ.", "P02.C01.L03 P02.C04.L03", "Runbook sự cố đa dịch vụ ở P13.C02.", "Tạo archive thành công chứng minh restore được.", "Đi từ một lỗi host tới quyết định dừng, backup, sửa và kiểm tra.", "Thiết kế phép thử restore và giới hạn dữ liệu chưa được bảo đảm.", "Thay đổi host~dịch vụ, quyền, config và cửa sổ bảo trì; Dữ liệu host~backup nhất quán, restore thử và log rotation; Phục hồi~chứng cứ trước/sau, rollback config, request và dữ liệu", "02 03 07", "planned_new")

# P03 — link/routing, transport, application and proxy are separate reasoning tasks.
add("P03", "Địa chỉ, subnet và đường đi gói IP", "Từ đích IP tìm route và địa chỉ chặng kế tiếp.", "Prefix quyết định on-link; routing chọn next hop; neighbor resolution tìm địa chỉ link cục bộ.", "P01.C02.L03", "TCP state ở chương sau; VPC route ở P08.", "ARP hỏi MAC của server ở mạng xa.", "Vẽ từng hop và xác nhận bằng route get từ đúng namespace.", "Chọn next hop cho route /24 và /0, nêu điều policy routing thay đổi.", "Định danh logic~IP, prefix, subnet; Chọn chặng~longest prefix, policy route, source address; Đóng frame~ARP/neighbor, link address, hop và đường về", "04", "reviewed_draft")
add("P03", "TCP, NAT và trạng thái kết nối", "Lần theo SYN, seq/ack, retransmission và dịch tuple hai chiều.", "TCP endpoint giữ luồng byte; NAT giữ ánh xạ packet độc lập với socket ứng dụng.", "P03.C01.L03", "TLS/HTTP ở P03.C03.", "TCP established chứng minh HTTP hoạt động; 80% retransmit là 80% tải.", "Dùng trace số RFC 9293 và tình huống SYN-ACK mất chiều về.", "Tính ACK cộng dồn và kiểm tra mapping NAPT khi đường về đổi.", "Bắt tay và byte stream~SYN, seq, ack, retransmission; Socket và lỗi~LISTEN, connect, ECONNREFUSED, timeout; NAT và đối xứng đường~tuple, state timeout, return path", "04", "reviewed_draft")
add("P03", "Tên, TLS và ngữ nghĩa HTTP", "Tách lỗi DNS, TCP, chứng chỉ và HTTP bằng dữ kiện tối thiểu.", "Tên chọn địa chỉ; TLS xác minh peer; HTTP đặt phương thức, header, status và body.", "P03.C02.L02", "Proxy hop ở P03.C04; cloud DNS ở P08.", "DNS trả IP nghĩa là service chạy; 502 luôn do upstream chết.", "Lần theo request client với SNI/Host và kết quả từng tầng.", "Định ranh giới xa nhất đã vượt qua cho mỗi lỗi.", "DNS và cache~stub, recursive, authoritative, TTL, A/AAAA; TLS~SNI, chứng chỉ, tên, trust, timeout; HTTP~request/response, Host, method, status, cache và body", "05", "reviewed_draft")
add("P03", "Reverse proxy và điều tra request hai chặng", "Xác định ai sinh status và chặng nào timeout.", "Proxy kết thúc một chặng rồi là client của chặng khác; forwarded headers cần trust boundary.", "P03.C03.L03", "Gateway API ở P11.C07.", "Một mã 504 xác nhận upstream không chạy.", "Đọc http_two_hop.txt, sau đó chèn timeout ở từng chặng.", "Chứng minh Host/Content-Length, TLS boundary và nơi tạo response.", "Chọn upstream~virtual host, route, pool, cache; Hai chặng~client–proxy và proxy–upstream, header chuyển tiếp; Đường lỗi~502/504, retry an toàn, log và hậu điều kiện", "05", "reviewed_draft")

# P04 — version-control mechanics before CI identity.
add("P04", "Git object, index và ref", "Dự đoán byte nào sẽ nằm trong commit kế tiếp.", "Blob/tree/commit là snapshot có cha; HEAD/ref/index/working tree là ba lớp trạng thái.", "P02.C01.L02", "CI dùng commit ID ở P06.", "git add là liên kết sống tới file đang sửa.", "Đọc object graph và tình huống staged 2000/working 3000.", "Tính tree của commit và chứng cứ diff staged.", "Object graph~blob, tree, commit, SHA; Trạng thái cục bộ~HEAD, ref, index, working tree; Danh tính thay đổi~tag, branch, remote, object reachability", "06", "reviewed_draft")
add("P04", "Tích hợp và sửa lịch sử", "Giải conflict mà vẫn giữ ý nghĩa thay đổi và lịch sử chia sẻ.", "Merge tạo nút hai cha; rebase tái tạo commit; revert thêm lịch sử, reset dịch ref.", "P04.C01.L03", "Rollout/rollback artifact ở P06.", "Chọn ours/theirs theo tên branch là đủ xác định đúng mã.", "Tái hiện graph B-D/C, index stage 1/2/3 rồi kiểm thử kết quả.", "Vẽ đồ thị sau merge/rebase/revert và quyết định an toàn cho nhánh chung.", "Merge~merge base, conflict stages, hai cha; Rebase~commit mới, xung đột và lịch sử chia sẻ; Phục hồi~revert, reset, reflog có giới hạn, kiểm thử", "06", "reviewed_draft")

# P05 — syntax, process orchestration, then multi-step safety.
add("P05", "Bash và ngữ nghĩa lỗi của shell", "Dự đoán argv, output và exit status trước khi chạy script.", "Shell parse trước, expand sau; redirection/pipeline/conditional thay nguồn status quan sát.", "P01.C02.L03 P02.C01.L01", "Python/Go orchestration ở P05.C02.", "set -euo pipefail tự biến script thành giao dịch.", "Tái hiện script backup lỗi trên thư mục tạm và giải thích từng nhánh.", "Dự đoán false success, quoting, pipefail và trap.", "Parsing~quote, expansion, splitting, globbing; I/O và status~descriptor, redirect, pipe, PIPESTATUS; Control flow~errexit exception, signal, trap, cleanup", "07", "reviewed_draft")
add("P05", "Python và Go điều phối tiến trình", "So sánh xử lý argv, timeout và kết quả con theo hai runtime.", "Parent quan sát startup và task deadline khác nhau; cancellation không rollback tác dụng phụ.", "P05.C01.L03 P01.C02.L02", "Đóng gói artifact ở P06.", "Không dùng shell thì input tự an toàn; timeout đã dừng dịch vụ từ xa.", "Đọc ba chương trình orchestration và kiểm thử success/fail/slow.", "Phân biệt START_ERROR, EXIT 7, TIMEOUT và partial state.", "Chọn ngôn ngữ~Bash đủ dùng vs Python/Go; Subprocess~argv, env, status, startup readiness; Timeout~communicate, CommandContext, child/grandchild và cleanup", "08", "reviewed_draft")
add("P05", "Workflow an toàn và chạy lại", "Thiết kế tác vụ nhiều bước có nhận diện partial failure.", "Mỗi bước phải có tiền/hậu điều kiện, idempotency key và chính sách retry theo tác dụng phụ.", "P05.C02.L03 P02.C05.L03", "CI gate ở P06; Ansible idempotency ở P10.", "Lặp vô hạn hoặc xóa partial state làm hệ thống chắc chắn hội tụ.", "Điều tra backup/deploy báo thành công giả, rồi thiết kế mô hình trạng thái.", "Viết bảng trạng thái và phép thử chạy lại khi lỗi/timeout.", "Hợp đồng bước~input, output, error class, secret; Retry~idempotency, deduplication, backoff, concurrency; Phục hồi~durable marker, compensation, cleanup và chứng minh hậu điều kiện", "07 08", "mixed")

# P06 — artifact and rollout independent of a particular orchestrator.
add("P06", "Build và danh tính artifact", "Chứng minh production chạy đúng byte đã qua kiểm thử.", "Commit là source snapshot; toolchain/dependency/build flags tạo artifact; digest nhận diện byte.", "P04.C01.L03 P05.C03.L01", "OCI manifest chuyên sâu ở P07.C02.", "Cùng commit luôn tạo cùng binary.", "Truy vết c83→H83, c84→H84 và một lần rebuild khác byte.", "Đề xuất provenance tối thiểu và phép build đối chiếu.", "Đầu vào build~source, dependency, compiler, môi trường; Artifact~digest, tag, immutable promotion; Tái lập~so byte độc lập, giới hạn cache và timestamp", "09", "reviewed_draft")
add("P06", "Test gates và CI/CD", "Thiết kế test kiểm đúng ranh giới của thay đổi và quyền release.", "CI phản hồi trên commit; CD quảng bá một artifact đã xét qua policy theo môi trường.", "P06.C01.L03 P04.C02.L03", "Bảo mật supply chain chi tiết ở P14.C03.", "Unit test và readiness xanh xác nhận hành vi tiền bạc của đơn hàng.", "Đọc gate bỏ sót amount_cents; bổ sung phép kiểm nghiệp vụ.", "Lập ma trận unit/integration/contract/production smoke và quyền phê duyệt.", "CI vs CD~build, test, delivery, deployment; Test model~pyramid, contract, data fixtures, false confidence; Gate~secret, approval, concurrency và evidence", "09", "mixed")
add("P06", "Rollout và quyết định dừng", "Chọn rolling, blue-green hay canary theo năng lực và khả năng quan sát.", "Traffic chuyển dần tới artifact mới; quan sát đại diện quyết định tiếp tục hoặc dừng.", "P06.C02.L03 P03.C04.L03", "Deployment controller ở P11.C02.", "Canary nhỏ luôn đủ thống kê hoặc green probe bằng green user journey.", "Dựng timeline H83/H84 theo version, lưu lượng và error budget.", "Chọn chiến lược dưới giới hạn thêm một Pod và đặt stop rule.", "Chiến lược~rolling, blue-green, canary; Readiness~process vs dependency vs request; Điều phối~serial release, approval, rollback trigger", "09", "reviewed_draft")
add("P06", "Rollback và tương thích dữ liệu", "Chứng minh hậu điều kiện sau khi lùi ứng dụng.", "Binary/image có thể lùi, schema và tác dụng phụ đã ghi thường cần phục hồi riêng.", "P06.C03.L03 P02.C05.L02", "DR hệ thống ở P13.C03.", "Một lệnh rollback đảo dữ liệu.", "Phân tích amount_cents và 41 đơn, tách ứng dụng/dữ liệu/ngoại tác.", "Nêu điều kiện expand-contract schema và kế hoạch phục hồi có thử.", "Dữ liệu qua bản phát hành~migration, back/forward compatibility; Partial deployment~identity hiện chạy, request và dữ liệu; Phục hồi~snapshot, compensating action, hậu điều kiện", "09", "reviewed_draft")

# P07 — distinguish kernel isolation, image, run instance and composition.
add("P07", "Namespace, cgroup v2 và runtime boundary", "Chỉ ra cơ chế nào đổi góc nhìn, cơ chế nào giới hạn CPU/RAM.", "PID/net/mount/user namespace là view; cgroup là accounting/control; runtime đặt process vào cả hai.", "P01.C02.L03 P02.C03.L03 P03.C01.L03", "Image artifact ở chương sau.", "PID 1 trong container là PID 1 host; 80/100 throttled là 80% utilization.", "Lần theo NSpid, netns, cpu.stat, memory.events.local có cửa sổ.", "Phân biệt OOM, quota và lỗi config qua counter/log.", "Tạo/tham gia~clone, unshare, setns, fork/exec, quyền; View~PID/net/mount/user và quan sát host/container; Limit~cpu.max, memory.max, OOM và pressure", "10 02", "reviewed_draft")
add("P07", "OCI image, build và registry", "Lần từ Dockerfile tới manifest/digest và byte đã pull.", "Image gồm config và layer theo descriptor; registry phân phối theo tag biến đổi hoặc digest.", "P06.C01.L03 P07.C01.L03", "Supply chain ký/provenance ở P14.C03.", "Tag v2 là artifact bất biến; xóa secret ở layer sau xóa mọi dấu vết.", "Giải phẫu build context, cache, digest và image cục bộ khác registry.", "Chứng minh digest đang chạy thay vì chỉ đọc tag.", "Build~context, Dockerfile, layer cache, secret mount; OCI~config, manifest/index, descriptor và digest; Distribution~push/pull, tag, platform và kiểm byte", "10 11", "reviewed_draft")
add("P07", "Container lifecycle và dữ liệu", "Dự đoán dữ liệu sau stop, recreate, remove, mount và đổi image.", "Container là run instance có writable layer; volume/bind là dữ liệu ở vòng đời độc lập.", "P07.C02.L03 P02.C01.L03", "K8s PV/PVC ở P11.C05.", "Container đang running nghĩa là app Ready; volume tự có backup.", "Theo 41 bản ghi qua A/B/D và xác định mount destination/volume identity.", "Phân biệt khả năng khôi phục khi container dừng và khi đã xóa.", "Lần chạy~create, start, stop, exit, health; Filesystem~read-only layers, writable layer, whiteout; Mount~volume, bind, ownership, backup và restore", "10 11", "reviewed_draft")
add("P07", "Compose và ứng dụng nhiều service", "Phân biệt cấu hình project với trạng thái service/volume thực tế.", "Compose gom service/network/mount trên một Engine; depends_on và health không chứng minh giao dịch nghiệp vụ.", "P07.C03.L03 P03.C04.L02", "Scheduler nhiều node ở P11.", "Đổi project name xóa dữ liệu volume cũ.", "Đọc compose-data.yaml, đổi tên project và kiểm tra volume identity.", "Thiết kế thao tác down/up không xóa dữ liệu và phép restore.", "Mô hình project~services, network, DNS, port; Khởi động~dependency, healthcheck, restart và giới hạn; Dữ liệu~named/external volume, bind, recreate và cleanup", "11", "reviewed_draft")

# P08 — identity/network/compute/data are independent cloud boundaries.
add("P08", "AWS identity và IAM evaluation", "Lần theo principal từ EC2 tới S3/STS và quyết định Allow/Deny.", "Trust nhận role; temporary credentials định danh session; policy evaluation áp dụng theo request/resource/context.", "P02.C02.L03 P03.C03.L02", "Cloud network ở P08.C02; threat model liên miền ở P14.", "Role attached đồng nghĩa mọi API đều được phép.", "Đọc policy JSON giả định, explicit Deny và request ARN/action.", "Phân biệt authn/authorization/route khi gặp AccessDenied.", "Danh tính~user, role, session, trust, IMDS, STS; Quyết định~Allow, explicit Deny, boundaries/SCP/resource policy theo scope; Điều tra~principal, action, resource, context và audit event", "12", "reviewed_draft")
add("P08", "VPC, subnet và đường đi AWS", "Chứng minh private workload có hoặc không có đường tới S3/STS.", "Route quyết định target; SG stateful và NACL stateless lọc gói; endpoint thay loại đường, không cấp quyền IAM.", "P03.C02.L03 P08.C01.L03", "K8s Service/Gateway ở P11 dùng control plane khác.", "Private subnet có NAT Gateway thì mọi AWS API đều dùng cùng đường an toàn.", "Tách timeout DNS/route/SG/NACL/endpoint theo vị trí nguồn.", "Vẽ đường request đi và về qua ALB, IGW, NAT/endpoint.", "Topology~VPC, subnet/AZ, route table, IGW, NAT; Chính sách gói~SG, NACL, state và ephemeral port; Private access~gateway/interface endpoint, DNS, route và điều kiện", "12 04", "reviewed_draft")
add("P08", "EC2, load balancer và miền lỗi", "Phân biệt instance running, target healthy và request nghiệp vụ đúng.", "Compute instance, ENI, ALB target và AZ chịu vòng đời/health khác nhau.", "P08.C02.L03 P02.C04.L03 P06.C03.L02", "Autoscaling/cloud cost ở P15.C02.", "ALB /health 200 chứng minh endpoint đọc S3 tốt.", "Theo client→ALB→private EC2→dependency và mỗi phép health.", "Đặt phép kiểm trước/sau failover một AZ.", "Compute~instance, image, boot, instance profile; Traffic~ALB listener, target group, health và timeout; Failure domain~AZ, capacity, replace và state ngoài instance", "12", "mixed")
add("P08", "Block, file và object storage", "Chọn EBS/EFS/S3 theo cách truy cập và vòng đời dữ liệu.", "Block là volume AZ, shared file là filesystem có miền lỗi riêng, object là API; durability khác availability và backup.", "P08.C03.L03 P02.C01.L03", "K8s storage ở P11.C05; DR ở P13.C03.", "Replication mặc định là backup hoặc EBS attach xuyên AZ.", "Đối chiếu AZ hỏng và object bị xóa nhầm.", "Đề xuất thử restore cho từng dạng dữ liệu, không suy từ SLA chung.", "Block~EBS attach, snapshot, delete_on_termination; File~EFS mount, đồng thời, quyền; Object~S3 API, versioning, lifecycle, restore và chi phí", "12 11", "reviewed_draft")

# P09 — configuration/state/reality stays visible across four chapters.
add("P09", "HCL, provider và dependency DAG", "Đọc tài nguyên, data source và cạnh implicit/explicit trong plan.", "Provider là chương trình/API boundary; references tạo DAG; depends_on chỉ thêm cạnh thực.", "P08.C04.L03 P04.C01.L03", "State/backend ở chương sau.", "Thứ tự các block trong file là thứ tự apply.", "Đọc main.tf terraform_data và vẽ đồ thị trước khi chạy.", "Tìm cạnh tham chiếu và nhận diện cạnh depends_on dư.", "Ngôn ngữ~variable, resource, data, output, expression; Provider~schema, CRUD, version pin; DAG~implicit refs, depends_on, cycle và parallelism", "13", "reviewed_draft")
add("P09", "Plan, state và backend", "Giải thích tại sao một plan có thể thất bại giữa chừng và state nhạy cảm.", "Configuration, state snapshot và API reality là ba thực thể; lock chỉ bảo vệ một state phù hợp.", "P09.C01.L03 P06.C04.L03", "Import/refactor ở chương sau.", "Plan là giao dịch; sensitive flag mã hóa state.", "Lần theo partial apply và remote write failure.", "Liệt kê object thực/state/config và bước đối chiếu trước retry.", "Ba trạng thái~config, state binding, real object; Plan/apply~refresh, unknown value, provider failure; Backend~locking, versioning, access, encryption, restore", "13", "reviewed_draft")
add("P09", "Drift, import và refactor", "Phân biệt thay đổi ngoài Terraform với đổi địa chỉ cấu hình.", "Drift được thấy khi provider refresh được; import/moved block sửa ánh xạ, không tự sửa dữ liệu.", "P09.C02.L03", "Approval rollout ở P09.C04.", "ignore_changes là cách chữa drift an toàn mọi lúc.", "Điều tra B trên console so với HCL A và state cũ.", "Chọn import, moved, sửa HCL hoặc phục hồi với điều kiện cụ thể.", "Drift~refresh, -refresh=false, refresh-only; Ánh xạ~import, moved, state mv có kiểm soát; Refactor~count/for_each/module address và chống destroy", "13", "mixed")
add("P09", "Thay đổi hạ tầng có dữ liệu", "Quyết định dừng khi plan đề xuất replace instance chứa dữ liệu.", "Plan là dự báo có điều kiện; backup và hậu điều kiện độc lập quyết định quyền apply.", "P09.C03.L03 P08.C04.L03 P06.C02.L03", "Không tạo AWS resource thật để dạy nếu không được cấp phép.", "Có state lock nghĩa là console không gây race.", "Đọc user_data_replace_on_change và root EBS delete_on_termination.", "Viết preflight, stop rule, apply sequencing và recovery plan.", "Replacement~ForceNew/provider schema và data risk; Điều phối~approval, lock, concurrent actor, saved plan; Hậu kiểm~ID object, dữ liệu, request, state backup và rollback", "13", "reviewed_draft")

# P10 — configuration convergence after infrastructure ownership.
add("P10", "Inventory và đường điều khiển Ansible", "Chỉ ra ai kết nối tới ai, bằng quyền nào và biến nào được dùng.", "Control node đọc inventory/play rồi thực thi module trên managed node theo connection/become.", "P02.C04.L03 P09.C02.L01", "Không thay Terraform bằng các lệnh tạo hạ tầng trong task.", "SSH thành công tức là ứng dụng đã healthy.", "Phân tích localhost fixture rồi mở rộng thành inventory hai host giả định.", "Chứng minh host pattern, variable precedence và quyền thực thi.", "Topology~inventory, host/group, SSH/local; Đơn vị chạy~play, task, module, facts; Quyền/biến~become, precedence, secret boundary", "14", "reviewed_draft")
add("P10", "Hội tụ, handler và thất bại từng host", "Chứng minh lượt đầu changed, lượt hai ok và drift sửa đúng phạm vi.", "Module quan sát trạng thái; handler chỉ chạy khi được notify; failure từng host không rollback máy khác.", "P10.C01.L03 P05.C03.L03", "Service readiness ở P02; rollout fleet ở P10.C03.", "changed=0 là dịch vụ khỏe; check mode giống apply thật.", "Chạy playbook trên POSIX fixture và tạo drift quyền/nội dung.", "Đọc recap, marker handler, mode và request độc lập.", "Idempotency~ok/changed/failed và module contract; Handler~notify, thứ tự, restart đúng lúc; Failure~check/diff, partial host, hậu điều kiện", "14", "reviewed_draft")
add("P10", "Vai trò, secrets và triển khai theo đợt", "Tổ chức cấu hình nhiều host với blast radius kiểm soát được.", "Role đóng gói task/default/template; rolling serial và vault giảm rủi ro nhưng không tự bảo đảm health.", "P10.C02.L03 P06.C03.L03", "K8s deployment strategy ở P11 dùng controller khác.", "Vault trong repo là đủ bảo mật secret lâu dài.", "Thiết kế sửa config trên host thử, kiểm request rồi tới host còn lại.", "Đề xuất rollback khi một host restart lỗi và bảo toàn secret.", "Tái sử dụng~role, defaults/vars, tags; Phân đợt~serial, max_fail_percentage, handler và health; Secret~Vault, key custody, log redaction, rotation", "14", "planned_new")

# P11 — controllers, workloads, resources, network, data, autoscaling, edge, packaging.
add("P11", "API, etcd và reconciliation", "Theo một spec từ apply tới các controller và node.", "API server lưu object; controller quan sát rồi thu hẹp sai lệch; status là ảnh chụp bất đồng bộ.", "P07.C01.L03 P06.C03.L02", "Scheduler, Service và storage có chương riêng.", "Apply thành công là workload chạy; resourceVersion là đồng hồ toàn cục.", "Điều tra chuỗi Deployment→ReplicaSet→Pod với generation/status.", "Đọc owner, selector, observedGeneration và giới hạn của snapshot.", "Control plane~API/admission, etcd, controller manager; Reconciliation~spec/status, watch, retry, generation; Node boundary~scheduler, kubelet, runtime và đường dữ liệu", "15", "reviewed_draft")
add("P11", "Pod, Deployment và readiness", "Phân biệt Running, Ready, Available và rollout complete.", "Pod là run unit; ReplicaSet giữ số; Deployment quản bản thay thế, probe xác định chấp nhận lưu lượng.", "P11.C01.L03 P07.C03.L01", "Service endpoint ở P11.C04.", "Restart tự phục hồi dữ liệu trong emptyDir.", "Sửa readiness sai trong k8s-ch15-incident.yaml rồi kiểm status từng cấp.", "Chỉ ra vì sao Available không chứng minh request nghiệp vụ.", "Workload objects~Pod, ReplicaSet, Deployment, owner/selector; Probe~startup, liveness, readiness và failure mode; Rollout~revision, surge/unavailable, progress deadline và dừng", "15 09", "reviewed_draft")
add("P11", "Scheduler và ngân sách tài nguyên", "Giải thích Pending vì requests/taint dù CPU tức thời thấp.", "Filter/score dùng allocatable, requests và ràng buộc; cgroup limit có thể gây throttle sau khi chạy.", "P11.C02.L01 P02.C03.L03 P07.C01.L03", "HPA ở P11.C06; metrics server tối thiểu ở bài 3.", "kubectl top 10% giúp scheduler bỏ qua requests.", "Tính node A/B và đối chiếu FailedScheduling, cpu.stat.", "Chọn node khả thi và nêu rủi ro sửa request/limit.", "Placement~requests, allocatable, taint/toleration, affinity; Runtime budget~CPU/memory limits, QoS, OOM/throttle; Resource metric tối thiểu~CPU time per window, metrics.k8s.io, timestamp/missing sample", "16 10 02", "reviewed_draft")
add("P11", "Service, EndpointSlice và NetworkPolicy", "Lần theo tên Service tới Pod socket và policy chặn.", "DNS chỉ trả tên; selector tạo endpoint; node dataplane và policy xử lý packet.", "P11.C02.L02 P03.C02.L03", "Gateway edge ở P11.C07.", "Service có IP nghĩa là có backend; Pod Ready đảm bảo mọi namespace nối được.", "Chẩn đoán typo app=atals cùng probe sai và một client khác namespace.", "Xác định chặng DNS/selector/endpoint/port/policy/call.", "Discovery~DNS, Service selector, EndpointSlice; Dataplane~ClusterIP, kube-proxy/CNI theo triển khai, targetPort; Policy~ingress/egress, scope và thử từ đúng nguồn", "15 16", "reviewed_draft")
add("P11", "PVC, CSI và dữ liệu workload", "Phân biệt PVC Bound với volume mount và dữ liệu phục hồi được.", "Binding, provision, attach/mount, quyền và backup là các bước khác nhau.", "P11.C02.L01 P08.C04.L03 P07.C03.L03", "DR ở P13.C03.", "RWO nghĩa chỉ một Pod; StatefulSet tự backup.", "Điều tra FailedMount, reclaim policy và Pod replacement.", "Đề xuất hậu điều kiện dữ liệu trước khi thay Pod.", "Tài nguyên~PV, PVC, StorageClass, access mode; Thực thi~CSI, topology, attach/mount, permissions; Vòng đời~StatefulSet identity, reclaim, backup/restore", "15 16", "reviewed_draft")
add("P11", "HPA và điều khiển mở rộng", "Tính replica từ CPU utilization khi biết request và chất lượng metric.", "Controller dùng sampled resource metric và CPU request làm mẫu số, rồi chịu tolerance/stabilization và khả năng scheduler.", "P11.C01.L02 P11.C03.L03 P11.C03.L01", "Prometheus/PromQL sâu ở P12, không phải tiên quyết.", "HPA có desiredReplicas lớn hơn nghĩa user latency giảm ngay.", "Tính ví dụ 300m/450m/150m trên request 500m rồi kiểm Pending.", "Nêu quyết định cơ sở và các lý do status cuối có thể khác.", "Phép đo~usage, request, missing/stale metric; Vòng tính~average utilization, ceil, bounds/tolerance; Hội tụ~scale target, scheduler, readiness, latency và giới hạn", "16", "reviewed_draft")
add("P11", "Gateway API và ranh giới request ngoài cluster", "Phân biệt controller conditions với đường request của client.", "GatewayClass/controller, listener, Route, Service và DNS/Host/SNI phải cùng khớp theo generation.", "P11.C04.L03 P03.C04.L03 P11.C01.L02", "Helm chỉ đóng gói cấu hình ở P11.C08.", "Programmed=True chứng minh DNS/TLS/Pod phục vụ.", "Điều tra revision đổi hostname nhưng DNS chưa đổi.", "Xác nhận Accepted/ResolvedRefs, quyền cross-namespace và request từ client.", "API objects~GatewayClass, Gateway, listener, HTTPRoute; Attachment~allowedRoutes, parentRefs, ReferenceGrant và status; Request path~DNS, Host/SNI, dataplane, Service và lỗi", "17", "reviewed_draft")
add("P11", "Helm chart và vòng đời release", "Theo chart/values đến manifest/revision rồi phân biệt với trạng thái thật.", "Render là đầu vào API; release history giữ manifest/config, rollback tạo revision chứ không đảo dữ liệu.", "P11.C07.L03 P06.C04.L03 P04.C01.L03", "Không biến chart thành nguồn sự thật cho mọi object ngoài release.", "helm template chạy xong chứng minh CRD/controller tồn tại.", "Đọc chart atlas-gateway, upgrade/rollback giả định và kiểm request.", "Đề xuất hậu điều kiện cho revision, object, endpoint, dữ liệu.", "Chart~metadata, template, values, dependency; Release~install, upgrade, wait, history và revision; Rollback~manifest, owner, data compatibility và request", "17", "reviewed_draft")

# P12 — metrics before logs/traces, telemetry reliability before SLO use.
add("P12", "Phép đo, nhãn và chuỗi thời gian", "Định nghĩa phép đo và rủi ro sai lệch trước khi xem dashboard.", "Instrument/exporter phát metric; scrape/sampling tạo chuỗi hữu hạn theo nhãn và thời gian.", "P01.C01.L02 P11.C03.L03", "HPA chỉ dùng resource metric cơ sở đã học; đây là mô hình quan sát sâu.", "Một mẫu cao/thấp chứng minh tải hoặc root cause.", "Đọc metrics-ch18.prom và đổi request_id thành nhãn để tính cardinality.", "Phân biệt counter/gauge/histogram, reset và mẫu bị thiếu.", "Đo~counter, gauge, histogram, units; Tập hợp~labels, cardinality, identity; Thu thập~scrape, target discovery, up và cửa sổ", "18", "reviewed_draft")
add("P12", "Prometheus, PromQL và Grafana", "Tính rate, tỷ lệ lỗi và p95 có giới hạn từ mẫu thật/giả định.", "Query biến chuỗi có cửa sổ thành ước lượng; panel chỉ là phép chiếu có filter/time range.", "P12.C01.L03", "SLI/SLO ở P13.", "Trung bình p95 của Pod là p95 toàn dịch vụ.", "Tính CSV Ch18 rồi thay một target bằng up=0.", "Sửa query rate(sum()) và nêu bias do mất scrape.", "PromQL~rate/increase, aggregation, reset; Histogram~bucket cumulative, quantile interpolation; Dashboard~selector, step, data source và missing series", "18", "reviewed_draft")
add("P12", "Logs, traces và OpenTelemetry", "Nối log và span của một request, kể cả khi một nhánh timeout nhưng cuối trả 200.", "Trace mô tả quan hệ parent/child; log mô tả sự kiện; SDK/Collector/backend có đường lỗi riêng.", "P12.C02.L03 P03.C04.L03 P11.C01.L02", "Alert policy ở P12.C04; không bắt buộc chạy Collector thật ở bài này.", "Cộng mọi span duration ra client latency; sampled=01 bảo đảm trace được lưu.", "Dùng trace-ch19.csv và logs-ch19.json để tính và chẩn đoán missing span.", "Xác định 420 ms end-to-end, chỗ thiếu span và giới hạn kết luận.", "Log~timestamp/severity/context/PII; Trace~span parent, W3C traceparent, sampling; Pipeline~OTel API/SDK, OTLP, Collector queue/retry/backend", "19", "reviewed_draft")
add("P12", "Alerting và sức khỏe pipeline quan sát", "Tạo tín hiệu hành động thay vì báo động từ một dashboard.", "Rule evaluation, routing và telemetry pipeline đều có độ trễ, mất dữ liệu và quyền truy cập riêng.", "P12.C02.L03 P12.C03.L03", "Burn-rate SLO policy ở P13.C01.", "No data luôn là healthy; alert sent tức là người trực đã nhận và hiểu.", "Failure injection mất scrape/queue đầy/alert route sai.", "Viết test alert rule, no-data policy và đường nhận thông báo.", "Rule~threshold, duration, missing data; Routing~group, inhibit, silences, escalation; Pipeline~export failure, queue/drop, retention và telemetry cost", "18 19", "planned_new")

# P13 — operational decisions consume P12 evidence.
add("P13", "SLI, SLO và error budget", "Chọn phép đo gần trải nghiệm người dùng và tính burn rate.", "SLI là tử/mẫu có phạm vi; SLO đặt ngưỡng; error budget cho biết rủi ro thay đổi còn chấp nhận.", "P12.C02.L03 P06.C03.L03", "Alert rule mechanics ở P12.C04; không lặp PromQL nền.", "SLO 99.9% nghĩa không bao giờ được lỗi.", "Tính ngân sách theo request và so client/server measurement.", "Phản biện một SLI loại bỏ request thất bại do target biến mất.", "SLI~good/total events, latency, availability, exclusion; SLO~window, target, budget; Burn~rate, multi-window alert, change policy", "", "planned_new")
add("P13", "Incident response và postmortem", "Tổ chức phát hiện, phân vai, giảm tác động và học từ sự cố.", "Incident là chuỗi quyết định dưới thông tin thiếu; timeline/bằng chứng và communication giảm lỗi thứ cấp.", "P13.C01.L03 P12.C03.L03 P06.C04.L03", "DR chi tiết ở P13.C03.", "Postmortem là tìm cá nhân chịu lỗi; root cause luôn đơn nhất.", "Điều tra request chậm qua metric/log/trace và change timeline.", "Lập runbook với trigger, stop, verification và mốc thông báo.", "Phản ứng~detect, triage, severity, incident command; Giảm tác động~rollback/isolation, evidence preservation, status updates; Học lại~timeline, contributing factors, action ownership", "09 19", "planned_new")
add("P13", "Backup, DR và phục hồi dữ liệu", "Phân biệt availability, durability, RPO, RTO và restore kiểm chứng.", "Bản sao nhất quán độc lập miền lỗi mới cho phép khôi phục; replication thường sao lỗi/xóa theo.", "P08.C04.L03 P11.C05.L03 P06.C04.L03", "Cloud storage API chi tiết ở P08.", "Multi-AZ hoặc PVC Bound chứng minh restore được.", "Diễn tập mất AZ và xóa object, kiểm manifest dữ liệu trước/sau.", "Đề xuất RPO/RTO thực tế và phép thử restore.", "Mục tiêu~RPO, RTO, failure domain; Bản sao~snapshot, versioning, immutable/offsite, secret/key; Diễn tập~restore, checksum, application consistency và request", "11 12 13 16", "planned_new")
add("P13", "Hiệu năng, capacity và thử giới hạn", "Phân biệt nghẽn CPU, I/O, hàng đợi và giới hạn dữ liệu khi tải tăng.", "Demand, service time, concurrency và queue làm tail latency khác trung bình; capacity là quyết định theo SLO.", "P02.C03.L03 P12.C02.L02 P13.C01.L03", "Cost strategy ở P15.C02.", "Thêm replica luôn giảm latency hoặc failure injection production là vô hại.", "Đặt thí nghiệm tải có baseline, stop rule và đo hậu trạng thái.", "Chọn chỉ số để chứng minh bottleneck rồi dự báo headroom.", "Workload~arrival rate, service time, concurrency; Capacity~queueing, saturation, autoscale lag; Experiment~load test, fault injection, blast radius, recovery", "02 16 18", "planned_new")

# P14 — security is a coherent analysis of trust boundaries across the stack.
add("P14", "Threat model và quyền tối thiểu", "Nhận diện tài sản, actor, trust boundary và đường lạm dụng.", "Mọi quyền là quan hệ principal/action/resource/context; defense có giả định và bypass riêng.", "P08.C01.L03 P03.C03.L02 P11.C01.L01", "Chi tiết IAM syntax ở P08, RBAC cụ thể ở P14.C04.", "Ẩn endpoint hoặc dùng private subnet là đủ kiểm soát truy cập.", "Vẽ luồng request và đánh dấu nơi xác thực/ủy quyền.", "Viết threat scenario và phép thử denial/allow theo least privilege.", "Bề mặt~asset, actor, entrypoint, data flow; Quyền~principal, role, policy evaluation, separation; Bằng chứng~audit log, negative test, review và thay đổi", "12", "planned_new")
add("P14", "Secret và bảo vệ dữ liệu", "Lần theo secret từ tạo tới sử dụng, log, rotation và thu hồi.", "Secret nằm trong nhiều bản sao: repo, CI, state, environment, memory, telemetry, backup.", "P14.C01.L03 P09.C02.L03 P12.C03.L01", "Không đồng nhất mã hóa-at-rest với quản lý vòng đời khóa.", "Mã hóa state là đủ khi secret còn trong log.", "Threat-model một token đi qua pipeline và Terraform/Ansible/K8s.", "Đề xuất redaction, scope, rotation và bằng chứng không rò.", "Vòng đời~issuance, storage, use, rotate, revoke; Bề mặt lộ~CI log, env, state, image layer, trace; Kiểm soát~KMS/Vault, encryption, access audit, recovery", "08 11 13 14 19", "planned_new")
add("P14", "Software supply chain", "Truy vết source→dependency→build→image→deploy không đánh tráo artifact.", "Digest, provenance, SBOM, signature và policy là bằng chứng có phạm vi, không thay kiểm thử runtime.", "P06.C02.L03 P07.C02.L03 P04.C01.L03", "Kubernetes admission ở P14.C04.", "Scanner xanh hoặc chữ ký hợp lệ chứng minh image không có lỗi.", "Kiểm một artifact có dependency đổi ngầm và tag bị dịch.", "Chỉ ra chuỗi bằng chứng và điểm còn chưa xác minh.", "Nguồn~dependency pin, SBOM, license/vulnerability; Build~isolation, provenance, attestation, signing; Deploy~digest verify, admission policy, revocation", "09 11", "planned_new")
add("P14", "Cloud/Kubernetes runtime hardening", "Đặt ranh giới quyền và mạng trên workload thật.", "Policy admission, ServiceAccount/RBAC, security context, NetworkPolicy và cloud identity chặn các đường khác nhau.", "P14.C03.L03 P11.C04.L03 P08.C02.L03", "Không lặp cơ chế scheduler hay API controller.", "Pod chạy non-root thì không thể đọc secret hoặc đi ra internet.", "Dựng chuỗi tấn công từ image tới API/data và thử policy âm.", "Lập ma trận kiểm soát và giới hạn thực thi của plugin/provider.", "Admission~PSS/policy engine và image policy; Runtime~SA/RBAC, securityContext, seccomp, volume; Network/cloud~NetworkPolicy, workload identity, SG và audit", "15 16 17", "planned_new")

# P15 — synthesis and professional judgment, not another product catalogue.
add("P15", "Thiết kế một dịch vụ production", "Bảo vệ đường request, dữ liệu và control plane trong một kiến trúc.", "Mỗi thành phần có owner, failure domain, SLO, trust boundary và phương án giảm tác động.", "P13.C03.L03 P14.C04.L03 P11.C08.L03", "Không dạy lại cú pháp Terraform/Helm.", "Một sơ đồ thành phần đẹp tự chứng minh hệ thống chịu lỗi.", "Thiết kế rồi đi qua ba sự cố đối nghịch: mất AZ, cert lỗi, deploy hỏng.", "Lập bảng tradeoff với bằng chứng cho từng control.", "Yêu cầu~traffic, dữ liệu, compliance, budget; Kiến trúc~edge, compute, data, network và control plane; Đánh giá~failure domain, runbook, ownership, test plan", "", "planned_new")
add("P15", "Mở rộng và tối ưu chi phí có ràng buộc", "Chọn năng lực đủ SLO trong giới hạn tiền và vận hành.", "Capacity, autoscale lag, redundancy và telemetry/egress/storage retention đều tiêu ngân sách.", "P15.C01.L03 P13.C04.L03 P08.C04.L03", "Không bịa bảng giá; dùng biến và công thức có Region/time.", "Giảm chi phí bằng cách tắt backup hoặc giảm replica luôn tối ưu.", "So ba phương án từ số liệu workload, nêu dữ liệu giá cần cập nhật.", "Tính điểm hòa vốn và rủi ro mất SLO/DR.", "Mô hình tải~peak, headroom, burst, queue; Mô hình tiền~compute, storage, data transfer, observability; Quyết định~cost per outcome, stop rule, kiểm số liệu giá", "", "planned_new")
add("P15", "Capstone: thay đổi, sự cố và phục hồi", "Chứng minh toàn hành trình từ commit đến phục hồi bằng artifact và phép đo.", "Một change record nối source, build, IaC, rollout, telemetry, incident và dữ liệu.", "P15.C02.L03 P13.C02.L03 P14.C03.L03", "Không coi mô phỏng là production certification.", "Mọi test xanh loại bỏ nhu cầu quan sát người dùng.", "Đưa cùng một dịch vụ qua rollout, failure injection giới hạn, restore và review.", "Nộp evidence ledger, kết quả âm/dương, giới hạn và quyết định vận hành.", "Chuẩn bị~source/digest, policy, state, backup, SLO; Thực thi~deploy, metric/log/trace, stop/rollback; Bảo vệ~restore, security check, postmortem và chi phí", "", "planned_new")

# Optional edges are deliberately sparse. They are not hidden requirements.
OPTIONAL_LINKS = {
    "P01.C01": {"extension": "P02.C03.L01"},
    "P03.C02": {"extension": "P12.C03.L02"},
    "P03.C04": {"helpful": "P02.C04.L03"},
    "P05.C02": {"helpful": "P04.C01.L02"},
    "P06.C03": {"helpful": "P05.C03.L02"},
    "P07.C02": {"extension": "P14.C03.L01"},
    "P08.C04": {"extension": "P13.C03.L01"},
    "P09.C02": {"extension": "P14.C02.L02"},
    "P11.C01": {"extension": "P11.C06.L02"},
    "P11.C06": {"helpful": "P02.C03.L01"},
    "P12.C03": {"helpful": "P11.C07.L03", "extension": "P13.C02.L01"},
    "P13.C01": {"helpful": "P12.C04.L01"},
    "P14.C03": {"extension": "P15.C03.L01"},
}
for chapter in CHAPTERS:
    for kind, value in OPTIONAL_LINKS.get(chapter["id"], {}).items():
        chapter[kind] = value.split()


# Explicit old-section -> new-lesson map. A split has more than one target.
# Every old section is checked against the real Markdown before compilation.
SECTION_MAP = {
    "01": ["P01.C02.L01", "P01.C02.L02", "P01.C02.L03 P02.C01.L01", "P02.C02.L01", "P02.C04.L01", "P01.C02.L03 P02.C04.L03"],
    "02": ["P01.C01.L02 P02.C03.L01", "P01.C02.L03 P02.C03.L02", "P02.C01.L03 P02.C03.L03", "P02.C03.L01 P07.C01.L03", "P02.C03.L03 P13.C04.L01"],
    "03": ["P02.C01.L01", "P02.C01.L02 P02.C02.L02", "P02.C04.L01 P02.C04.L02", "P02.C04.L03"],
    "04": ["P03.C01.L01", "P03.C01.L02 P03.C01.L03", "P03.C02.L01 P03.C02.L02", "P03.C02.L03", "P03.C02.L02 P03.C04.L03"],
    "05": ["P03.C03.L01", "P03.C03.L02", "P03.C03.L03 P03.C04.L01 P03.C04.L02", "P03.C04.L03"],
    "06": ["P04.C01.L01", "P04.C01.L02", "P04.C02.L01", "P04.C02.L02", "P04.C02.L03", "P04.C02.L03"],
    "07": ["P05.C01.L01", "P05.C01.L02", "P05.C01.L03", "P05.C01.L03 P05.C03.L02", "P05.C03.L01 P05.C03.L03"],
    "08": ["P05.C02.L01", "P05.C02.L02 P14.C02.L02", "P05.C02.L02 P05.C03.L01", "P05.C02.L03 P05.C03.L03", "P05.C02.L01 P06.C01.L01"],
    "09": ["P06.C01.L01 P06.C01.L02", "P06.C02.L01 P06.C02.L03", "P06.C03.L01 P06.C03.L02", "P06.C04.L01 P06.C04.L03"],
    "10": ["P07.C01.L01 P07.C01.L02", "P07.C01.L03", "P07.C02.L02 P07.C03.L01", "P07.C01.L03 P07.C03.L01"],
    "11": ["P07.C02.L01 P07.C02.L03", "P07.C03.L01 P07.C03.L02 P07.C03.L03", "P07.C04.L01 P07.C04.L02 P07.C04.L03", "P07.C03.L03 P07.C04.L03"],
    "12": ["P08.C01.L01 P08.C01.L02", "P08.C02.L01 P08.C02.L02 P08.C02.L03", "P08.C03.L01 P08.C04.L01 P08.C04.L02 P08.C04.L03", "P08.C01.L03 P08.C02.L03 P08.C03.L02"],
    "13": ["P09.C01.L01 P09.C01.L02 P09.C01.L03", "P09.C02.L01 P09.C02.L02", "P09.C02.L03", "P09.C03.L01 P09.C04.L01 P09.C04.L03"],
    "14": ["P10.C01.L01 P10.C01.L02 P10.C01.L03", "P10.C02.L01 P10.C02.L02 P10.C02.L03", "P10.C02.L01 P10.C02.L02", "P10.C02.L03 P10.C03.L02"],
    "15": ["P11.C01.L01 P11.C01.L03", "P11.C01.L02 P11.C02.L01", "P11.C02.L02 P11.C04.L01", "P11.C02.L03 P11.C05.L03"],
    "16": ["P11.C03.L01", "P11.C03.L02 P07.C01.L03", "P11.C04.L01 P11.C04.L02 P11.C04.L03", "P11.C05.L01 P11.C05.L02", "P11.C03.L03 P11.C06.L01 P11.C06.L02", "P11.C03.L01 P11.C04.L03 P11.C05.L02 P11.C06.L03"],
    "17": ["P11.C07.L01 P11.C07.L02", "P11.C07.L02 P11.C07.L03", "P11.C08.L01 P11.C08.L02 P11.C08.L03", "P11.C07.L01 P11.C08.L01", "P11.C07.L03 P11.C08.L03"],
    "18": ["P12.C01.L01 P12.C01.L02 P12.C01.L03", "P12.C02.L01", "P12.C02.L02", "P12.C02.L03 P12.C04.L01"],
    "19": ["P12.C03.L01", "P12.C03.L02", "P12.C03.L03", "P12.C03.L02 P12.C03.L03", "P12.C03.L03 P12.C04.L03 P14.C02.L02"],
}

# Editorial preservation notes are intentionally specific: the migration row
# must tell A2 what validated mechanism/result is at risk, not just echo a title.
PRESERVE = {
    "01": ["Source/executable/process khác vòng đời; execve giữ PID", "fork cha/con/lỗi và execve success/failure; ví dụ Linux", "FD, open file description, offset và rename log", "UID/GID kiểm quyền từng thao tác, không suy từ process sống", "Exit status, signal, service readiness không đồng nhất", "Chẩn đoán artifact→PID→socket→request"],
    "02": ["Running/runnable/blocked và CPU time khác wall time", "Virtual address, resident memory, cấp phát trễ", "Page cache, writeback, rename/fsync và độ bền", "Cgroup quota/limit tác động latency khác nhau", "Bộ số giả định 60s; 0,30/0,32 lõi, PSI 2%/30% và giới hạn suy luận"],
    "03": ["openat đi qua syscall rồi trả FD/errno", "Inode, symlink, quyền search ở từng thư mục", "Type=exec; After/Wants/Requires; network.target không là readiness", "systemd-analyze, journal, MainPID và phép thử HTTP sau start"],
    "04": ["IP/prefix và địa chỉ logic; đích ví dụ 198.51.100.20", "Longest prefix, next hop 10.20.1.1 và ARP chặng gần", "TCP SYN/seq/ack byte và retransmission đúng số", "NAPT tuple 10.20.1.10→203.0.113.5 và đường về", "ECONNREFUSED với listener 127.0.0.1, giả thuyết cạnh tranh"],
    "05": ["DNS cache, A/AAAA và điểm nhìn của client", "TCP established khác TLS identity/SNI/cert", "HTTP hai chặng Host/X-Forwarded-*/Content-Length=9/status", "Phân biệt DNS/TCP/TLS/502/504 bằng ranh giới chứng cứ"],
    "06": ["Blob/tree/commit, parent và content hash", "HEAD/index/working tree; stage 2000 rồi sửa 3000", "Merge graph B-D/C, stage 1/2/3, M hai cha", "Rebase sinh C′ và rủi ro commit đã chia sẻ", "Revert thêm commit; reset dịch ref, mainline merge", "Kiểm diff, graph, test trước push"],
    "07": ["Bash parse rồi expand; quote, split, glob", "Redirection FD order và pipeline status", "set -e bị bỏ qua ở ngữ cảnh điều kiện", "Trap/signal/SIGKILL và giới hạn cleanup", "Backup lỗi BACKUP_OK exit 0; bản sửa không overwrite và restore thử"],
    "08": ["Điều kiện chọn Bash/Python/Go theo trạng thái và triển khai", "Argv tách shell nhưng vẫn có option/secret risk", "READY tách startup khỏi task timeout; bad vs checked", "Cancellation không rollback file partial hoặc tiến trình cháu", "Python env/dependency và Go module/toolchain/platform"],
    "09": ["Commit c83/c84 khác artifact digest H83/H84", "CI/CD, gate, approval, dữ liệu test bỏ sót amount_cents", "Running khác Ready; rolling/blue-green/canary và stop rule", "41 đơn, rollback app không đảo schema/side effects"],
    "10": ["PID/net namespace, NSpid 3142 1, clone/unshare/setns", "cpu.max 0,5 lõi; memory.max/oom/oom_kill phân biệt", "OCI image không tự tạo namespace/cgroup", "4,7 triệu µs/10s=0,47 lõi; 80/100 throttle không là utilization"],
    "11": ["Manifest/layer/config/digest/tag, cache và secret layer", "Stop/recreate/remove, writable layer khác volume/bind", "Compose project/network/health/port và giới hạn một Engine", "41 bản ghi có thể mất hoặc còn tùy mount/volume identity"],
    "12": ["Role trust vs permission; STS/IMDS; explicit Deny", "VPC route/IGW/NAT/S3 gateway endpoint/SG/NACL", "EC2/EBS AZ, EFS/S3 khác API; redundancy không backup", "Timeout do endpoint route rồi AccessDenied do Deny"],
    "13": ["terraform_data HCL; resource/data/provider/DAG", "Config/state/API reality, refresh và plan không giao dịch", "Backend lock/version/access và secret trong state", "B console drift, replacement, root EBS 41 đơn và stop-before-apply"],
    "14": ["Inventory/control/managed/SSH/module/become khác Terraform", "Idempotent/changed/ok/failed; check/diff không bảo đảm apply", "Local playbook, mode 0750, template notify và marker handler", "Hai host restart/quyền sai có thể gián đoạn dù play xanh"],
    "15": ["API/etcd/controller/scheduler/kubelet/runtime trách nhiệm riêng", "spec/status/generation/resourceVersion, owner vs selector", "Probe /ready sai và selector app=atals là hai lỗi độc lập", "Eventual convergence, Pod mới không giữ emptyDir"],
    "16": ["Scheduler request/allocatable/taint, không dùng usage 10%", "CPU request/limit/throttling; memory OOM phân biệt", "DNS→Service→EndpointSlice→Pod socket/policy", "PVC Bound khác CSI attach/mount/backup", "300/450/150m trên request 500m; cơ sở HPA ceil=4", "Pending/FailedMount/network/HPA là bốn ranh giới chứng cứ"],
    "17": ["GatewayClass/controller/listener/Route/ReferenceGrant", "Accepted/ResolvedRefs/Programmed và observedGeneration", "Helm chart/values/manifest/revision, rollback không đảo data", "Chart atlas-gateway tạo Gateway/Route cho Service có sẵn", "Revision 4→5 đổi host khi DNS cũ; status khác request"],
    "18": ["Metric scrape/up/cardinality và nhãn request_id nguy hiểm", "CSV counters, rate/increase/ratio và cửa sổ", "Histogram cumulative buckets; p95 giả định 0,9615s", "up=0 và missing series làm dashboard giảm lỗi giả"],
    "19": ["Log timestamp/severity/context/PII, ID request/trace", "Span parent/event/status, W3C traceparent và sampling", "OTel API/SDK→OTLP→Collector→backend có queue/retry/drop", "Trace G=420ms, tổng span=1153ms, timeout rồi HTTP 200", "Thiếu span không chứng minh không chạy; bảo vệ secret/PII"],
}

EXERCISE_DEFAULT = {
    "01": "P01.C02", "02": "P02.C03", "03": "P02.C04", "04": "P03.C02",
    "05": "P03.C04", "06": "P04.C02", "07": "P05.C01", "08": "P05.C02",
    "09": "P06.C03", "10": "P07.C01", "11": "P07.C03", "12": "P08.C02",
    "13": "P09.C03", "14": "P10.C02", "15": "P11.C02", "16": "P11.C03",
    "17": "P11.C07", "18": "P12.C02", "19": "P12.C03",
}
EXERCISE_OVERRIDES = {
    "C1.1": "P01.C02", "C1.2": "P02.C01", "C1.3": "P01.C02",
    "C2.3": "P02.C01", "C4.1": "P03.C01", "C4.2": "P03.C01",
    "C5.1": "P03.C03", "C5.2": "P03.C03", "C6.1": "P04.C01",
    "C7.4": "P05.C03", "C8.3": "P05.C03", "C8.4": "P05.C03",
    "C9.1": "P06.C01", "C9.2": "P06.C02", "C9.4": "P06.C04",
    "C10.4": "P07.C03", "C11.1": "P07.C02", "C11.3": "P07.C04",
    "C12.2": "P08.C01", "C12.3": "P08.C04", "C12.4": "P08.C03",
    "C13.1": "P09.C01", "C13.2": "P09.C04", "C13.3": "P09.C02",
    "C14.4": "P10.C03", "C15.1": "P11.C01", "C15.2": "P11.C04",
    "C15.4": "P11.C05", "C16.2": "P11.C05", "C16.3": "P11.C04",
    "C16.4": "P11.C06", "C16.5": "P11.C06", "C17.4": "P11.C08",
    "C18.3": "P12.C01", "C19.4": "P12.C04",
}


def old_sections(path: Path) -> list[tuple[str, str, str]]:
    text = path.read_text(encoding="utf-8")
    blocks = re.split(r"(?m)^## ", text)[1:]
    result = []
    for block in blocks:
        heading, _, body = block.partition("\n")
        match = re.match(r"(\d+\.\d+)\.\s+(.*)", heading)
        if match:
            result.append((match.group(1), match.group(2).strip(), body))
    return result


def make_migration(claims: list[dict]) -> list[dict]:
    rows = []
    covered_claims = 0
    embedded_examples: set[str] = set()
    answers = (ROOT / "answers.md").read_text(encoding="utf-8")
    old_files = sorted((ROOT / "chapters").glob("[0-9][0-9]-*.md"))
    if len(old_files) != 19 or set(SECTION_MAP) != {p.name[:2] for p in old_files}:
        raise ValueError("Expected exactly the 19 baseline chapters")
    for path in old_files:
        old_id = path.name[:2]
        sections = old_sections(path)
        destinations = SECTION_MAP[old_id]
        if len(sections) != len(destinations) or len(sections) != len(PRESERVE[old_id]):
            raise ValueError(f"Section migration missing for {path.name}: {len(sections)} != {len(destinations)}")
        for (section, title, body), dest, preserve in zip(sections, destinations, PRESERVE[old_id]):
            targets = dest.split()
            section_claims = [c for c in claims if c["chapter"] == f"chapters/{path.name}" and c["section"] == section]
            covered_claims += len(section_claims)
            example_paths = re.findall(r"\{\{code:([^}]+)\}\}", body)
            embedded_examples.update(example_paths)
            for example in example_paths:
                if not (ROOT / example).is_file():
                    raise ValueError(f"Missing legacy example: {example}")
            old_cross = sorted(set(re.findall(r"Chương\s+(\d+)", body)))
            rows.append({
                "old_location": f"chapters/{path.name}#{section}", "old_title": title,
                "new_ids": ";".join(targets),
                "action": "split" if len(targets) > 1 else ("move_and_extend" if old_id in {"02", "09", "12", "13", "15", "16", "17", "18", "19"} else "move"),
                "reason": "Tách các cơ chế có tiên quyết hoặc bằng chứng khác nhau" if len(targets) > 1 else "Đặt cơ chế vào hệ thống kiến thức có chủ đề và tiên quyết rõ",
                "verified_content_to_preserve": preserve,
                "source_claim_anchors": json.dumps([c["anchor"] for c in section_claims], ensure_ascii=False),
                "source_ids": ";".join(sorted({sid for c in section_claims for sid in c["sources"]})),
                "examples": ";".join(example_paths), "exercise_answer_ids": "",
                "cross_references_to_rewrite": ";".join(f"Chương {n}" for n in old_cross),
                "evidence_status": "reviewed_draft; structural source map, not blanket semantic proof",
            })
        exercise_ids = re.findall(r"(?m)^C(\d+)\.(\d+)\.\s", path.read_text(encoding="utf-8"))
        for number, item in exercise_ids:
            qid = f"C{number}.{item}"
            if number != str(int(old_id)) or not re.search(rf"(?m)^\s*{re.escape(qid)}\.", answers):
                raise ValueError(f"Missing matching exercise/answer: {qid}")
            target = EXERCISE_OVERRIDES.get(qid, EXERCISE_DEFAULT[old_id])
            rows.append({
                "old_location": f"chapters/{path.name}#{qid}", "old_title": "Bài tập và lời giải " + qid,
                "new_ids": target, "action": "move_rekey_after_review",
                "reason": "Giữ cặp đề–đáp án; đổi mã in sách sau khi cấu trúc mới ổn định",
                "verified_content_to_preserve": "Giữ nguyên dữ kiện, nhánh lỗi và giới hạn kết luận của bài và lời giải",
                "source_claim_anchors": "[]", "source_ids": "", "examples": "",
                "exercise_answer_ids": qid,
                "cross_references_to_rewrite": f"answers.md#{qid}; old exercise ID {qid}",
                "evidence_status": "reviewed_draft; preserve question-answer pair",
            })
    all_examples = {str(p.relative_to(ROOT)).replace("\\", "/") for p in (ROOT / "examples").rglob("*") if p.is_file()}
    if embedded_examples != all_examples:
        raise ValueError(f"Unmapped example files: {sorted(all_examples - embedded_examples)}")
    if covered_claims != len(claims):
        raise ValueError(f"Unmapped source claims: {covered_claims}/{len(claims)}")
    return rows


def compile_tree() -> tuple[dict, str]:
    part_ids = [p[0] for p in PARTS]
    if len(set(part_ids)) != len(part_ids):
        raise ValueError("Duplicate part ID")
    chapter_ids = [c["id"] for c in CHAPTERS]
    lesson_ids = [l["id"] for c in CHAPTERS for l in c["lessons"]]
    if len(set(chapter_ids)) != len(chapter_ids) or len(set(lesson_ids)) != len(lesson_ids):
        raise ValueError("Duplicate chapter/lesson ID")
    index = {lid: i for i, lid in enumerate(lesson_ids)}
    edges = []
    for chapter in CHAPTERS:
        for i, lesson in enumerate(chapter["lessons"]):
            required = chapter["required"] if i == 0 else [chapter["lessons"][i-1]["id"]]
            lesson["prerequisites"] = {"required": required, "helpful": chapter["helpful"] if i == 0 else [],
                                       "extension": []}
            for kind in ("required", "helpful"):
                for source in lesson["prerequisites"][kind]:
                    if source not in index or index[source] >= index[lesson["id"]]:
                        raise ValueError(f"Missing or forward {kind} dependency: {source} -> {lesson['id']}")
                    edges.append({"from": source, "to": lesson["id"], "kind": kind})
        for target in chapter["extension"]:
            source = chapter["lessons"][-1]["id"]
            if target not in index or index[source] >= index[target]:
                raise ValueError(f"Invalid extension edge: {source} -> {target}")
            edges.append({"from": source, "to": target, "kind": "extension"})
    # Required edges always point forward in the canonical teaching order; this proves acyclicity.
    if len({(e["from"], e["to"], e["kind"]) for e in edges}) != len(edges):
        raise ValueError("Duplicate graph edge")
    consumers: dict[str, set[str]] = defaultdict(set)
    for e in edges:
        if e["kind"] == "required":
            consumers[e["from"].split(".L")[0]].add(e["to"].split(".L")[0])
    claims = json.loads((ROOT / "source_map.json").read_text(encoding="utf-8"))["claims"]
    for c in CHAPTERS:
        c["prepares_for"] = sorted(consumers[c["id"]] - {c["id"]})
        c["source_ids_to_recheck"] = sorted({sid for claim in claims
            if claim["chapter"].split("/")[-1][:2] in c["legacy_chapters"] for sid in claim["sources"]})
        c["learning_outcomes"] = [c["objective"], c["assessment"]]
    parts = []
    for pid, title, question, model, prereq, boundary, ability, misconception, transfer in PARTS:
        members = [c for c in CHAPTERS if c["part"] == pid]
        if len(members) < 2:
            raise ValueError(f"Part must be a real knowledge system: {pid}")
        parts.append({"id": pid, "parent": "BOOK", "title": title,
                      "central_question": question, "mental_model": model,
                      "prerequisites": prereq, "boundary": boundary,
                      "exit_capability": ability, "misconception": misconception,
                      "transfer": transfer, "chapters": members})
    tree = {"schema_version": 1, "book": {"id": "BOOK", "title": "Cẩm nang ngành DevOps",
            "status": "architecture_proposal_not_approved", "source_baseline": "8bdce2dd0f5e72bc0e7c9f3c61a947722ed0a144"},
            "parts": parts, "dependency_edges": edges,
            "dependency_semantics": {"required": "Phải học nguồn trước đích để hiểu cơ chế; tạo thứ tự chính.",
                                     "helpful": "Có ích nhưng được giới thiệu ngắn tại chỗ nếu chưa học.",
                                     "extension": "Đường đào sâu sau bài hiện tại, không là cổng vào bắt buộc."}}
    lines = ["# Cây tri thức đề xuất — Cẩm nang ngành DevOps", "",
             "**Trạng thái:** đề xuất A1 để Reviewer nghiệm thu; chưa thay bản thảo hoặc PDF.",
             "**Cách đọc:** ID ổn định; cạnh `A → B` nghĩa học A trước B. `reviewed_draft` chỉ nói bản thảo đã qua review milestone, không xác nhận mọi claim hay lab. Nội dung mới mang `planned_new`.", "",
             f"Tổng: {len(parts)} Phần, {len(CHAPTERS)} Chương, {len(lesson_ids)} Bài/Mục. Cấu trúc phản ánh ranh giới cơ chế và tiên quyết, không phải quota.", ""]
    kinds = Counter(edge["kind"] for edge in edges)
    lines += ["## Đồ thị tiên quyết đọc nhanh", "",
              f"Bản đầy đủ ở `knowledge_tree.json`: {kinds['required']} cạnh bắt buộc, {kinds['helpful']} cạnh hữu ích và {kinds['extension']} đường đào sâu. Chỉ cạnh bắt buộc tạo trật tự học; mọi cạnh đi từ bài xuất hiện trước tới bài xuất hiện sau. Các chuỗi minh họa dưới đây có thể bỏ qua nút trung gian; cạnh chính xác nằm trong JSON.", "",
              "- `P01.C02.L03` (process/FD) → `P07.C01.L01` (namespace) → `P07.C03.L01` (container là lần chạy).",
              "- `P03.C02.L03` (đường TCP/NAT) → `P08.C02.L01` (VPC route) → `P11.C04.L02` (Service dataplane áp dụng mạng gốc).",
              "- `P04.C01.L03` (commit/ref) → `P06.C01.L01` (build input) → `P07.C02.L02` (OCI digest).",
              "- `P11.C01.L02` (controller) + `P11.C03.L01` (CPU request/placement) + `P11.C03.L03` (resource metric) → `P11.C06.L01` (HPA); P12 Prometheus không là điều kiện vào.",
              "- `P08.C04.L03` (data lifecycle) → `P09.C01.L01` (resource) → `P09.C02.L01` (state) → `P09.C04.L01` (replacement/data risk).",
              "- `P12.C02.L03` (dashboard/missing data) → `P13.C01.L01` (SLI denominator) → `P13.C02.L01` (incident triage).", ""]
    for part in parts:
        lines += [f"## {part['id']} — {part['title']}", "",
                  f"**Câu hỏi:** {part['central_question']}",
                  f"**Mô hình:** {part['mental_model']}",
                  f"**Tiên quyết:** {part['prerequisites']}",
                  f"**Ranh giới:** {part['boundary']}",
                  f"**Năng lực ra:** {part['exit_capability']}",
                  f"**Ngộ nhận cần sửa:** {part['misconception']}",
                  f"**Chuyển tiếp:** {part['transfer']}", ""]
        for ch in part["chapters"]:
            lines += [f"### {ch['id']} — {ch['title']} [{ch['status']}]", "",
                      f"- **Đích học:** {ch['objective']}",
                      f"- **Mô hình nối bài:** {ch['mental_model']}",
                      f"- **Tiên quyết bắt buộc:** {', '.join(ch['required']) or 'Không'}.",
                      f"- **Ranh giới:** {ch['boundary']}",
                      f"- **Ngộ nhận:** {ch['misconception']}",
                      f"- **Cách dạy:** {ch['teaching_strategy']}",
                      f"- **Đánh giá:** {ch['assessment']}",
                      f"- **Nối tới:** {', '.join(ch['prepares_for']) or 'Tổng hợp cuối sách'}.",
                      f"- **Nguồn cũ:** {', '.join('Ch' + x for x in ch['legacy_chapters']) or 'Cần biên soạn mới'}.",
                      "- **Cây bài:**"]
            for lesson in ch["lessons"]:
                lines.append(f"  - `{lesson['id']}` **{lesson['title']}** — {lesson['core']}")
            lines.append("")
    return tree, "\n".join(lines).rstrip() + "\n"


def main() -> None:
    tree, markdown = compile_tree()
    rows = make_migration(json.loads((ROOT / "source_map.json").read_text(encoding="utf-8"))["claims"])
    ids = {l["id"] for part in tree["parts"] for ch in part["chapters"] for l in ch["lessons"]}
    cids = {ch["id"] for part in tree["parts"] for ch in part["chapters"]}
    for row in rows:
        for target in row["new_ids"].split(";"):
            if target not in ids | cids:
                raise ValueError(f"Migration points to unknown target: {target}")
    (OUT / "knowledge_tree.json").write_text(json.dumps(tree, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "knowledge_tree.md").write_text(markdown, encoding="utf-8")
    with (OUT / "legacy_migration.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"ARCHITECTURE_OK parts={len(tree['parts'])} chapters={len(cids)} lessons={len(ids)} "
          f"required_edges={sum(e['kind']=='required' for e in tree['dependency_edges'])} "
          f"migration_rows={len(rows)} sections={sum('#C' not in r['old_location'] for r in rows)} "
          f"exercise_answers={sum(bool(r['exercise_answer_ids']) for r in rows)}")


if __name__ == "__main__":
    main()
