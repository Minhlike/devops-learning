"""Editable monochrome mechanism diagrams for the textbook's causal models.

The labels and edges are source, not screenshots; ReportLab keeps them as PDF
vector objects. Each diagram is deliberately scoped to one lesson claim.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from reportlab.lib import colors
from reportlab.platypus import Flowable, KeepTogether, Paragraph

INK = colors.HexColor("#242424")
MID = colors.HexColor("#777777")
LIGHT = colors.HexColor("#f0f0f0")
ROOT = Path(__file__).resolve().parents[1]

FIGURES = {
    "V02": ("Hình I.2.1 — fork/execve/wait: PID giả định; nhánh thành công và lỗi là hai lần chạy khác nhau.", 236),
    "V03": ("Hình II.1.1 — Đổi tên thay mục thư mục; descriptor đang mở vẫn tới cùng inode.", 228),
    "V07": ("Hình III.2.1 — TCP: sequence đếm byte, ACK cộng dồn; số liệu giả định.", 242),
    "V09": ("Hình IV.2.1 — Cùng nhánh ban đầu, merge thêm commit hai cha; rebase tạo commit mới.", 224),
    "V10": ("Hình V.1.1 — Trạng thái pipeline không mặc nhiên là trạng thái của tar.", 218),
    "V12": ("Hình VI.1.1 — Từ commit đến tiến trình phục vụ: mỗi cổng giữ một bằng chứng riêng.", 230),
    "V16": ("Hình VII.3.1 — Vòng đời image, writable layer và nơi lưu độc lập; dữ liệu giả định.", 238),
    "V18": ("Hình VIII.2.1 — Đường tới S3 và STS khác nhau; DNS, mạng và IAM là các ranh giới riêng.", 234),
    "V20": ("Hình IX.2.1 — Terraform: cấu hình, state và API thực có thể lệch nhau; CPU là dữ kiện giả định.", 220),
    "V22": ("Hình X.2.1 — Handler chỉ chạy khi task phù hợp báo changed; các lượt là tình huống giả định.", 222),
    "V23": ("Hình XI.1.1 — Vòng điều khiển Kubernetes và đường request tách biệt.", 226),
    "V29": ("Hình XII.3.1 — Năm span trên một trục 420 ms; số liệu từ fixture trace và log.", 244),
    "V33": ("Hình XIV.3.1 — Chứng cứ nguồn, build và deploy: chữ ký không chứng minh chất lượng ứng dụng.", 232),
    "V43": ("Hình XV.3.1 — Ledger capstone: mỗi hậu điều kiện cần phép kiểm và trạng thái riêng.", 248),
    "V44": ("Hình IV.1.1 — Commit trỏ tree; tree giữ tên và mode, blob chỉ giữ byte.", 246),
    "V45": ("Hình IV.1.2 — Ba ảnh của app.conf sau hai lần sửa nhưng chỉ một lần stage; số liệu giả định.", 225),
    "V46": ("Hình IV.1.3 — Ref là tên cục bộ có thể dời; quan hệ parent thuộc commit.", 225),
    "V47": ("Hình IV.2.2 — Fast-forward dời ref; nhánh phân kỳ cần hợp ba phía và giải conflict.", 242),
    "V48": ("Hình IV.2.3 — Revert thêm commit đảo tác động; reset dời ref và tùy mode đổi index, worktree.", 238),
}


class MechanismFigure(Flowable):
    def __init__(self, figure_id: str, styles: dict):
        super().__init__()
        if figure_id not in FIGURES:
            raise ValueError(f"Unknown mechanism figure: {figure_id}")
        self.figure_id = figure_id
        caption, self.panel_height = FIGURES[figure_id]
        self.caption = Paragraph(caption, styles["caption"])
        self.width = 471
        _, caption_height = self.caption.wrap(self.width, 80)
        self.height = self.panel_height + caption_height + 10

    def line(self, x1, y1, x2, y2, arrow=False, dashed=False):
        c = self.canv
        c.setStrokeColor(INK)
        c.setLineWidth(0.8)
        c.setDash(3, 2) if dashed else c.setDash()
        c.line(x1, y1, x2, y2)
        c.setDash()
        if arrow:
            angle = math.atan2(y2 - y1, x2 - x1)
            for offset in (-0.52, 0.52):
                c.line(x2, y2, x2 - 6 * math.cos(angle + offset),
                       y2 - 6 * math.sin(angle + offset))

    def box(self, x, y, w, h, label, small=None, fill=False):
        c = self.canv
        c.setStrokeColor(INK)
        c.setFillColor(LIGHT if fill else colors.white)
        c.rect(x, y, w, h, fill=1, stroke=1)
        c.setFillColor(INK)
        c.setFont("BodyBold", 9.2)
        c.drawCentredString(x + w / 2, y + h / 2 + (3 if small else -3), label)
        if small:
            c.setFont("Body", 7.8)
            c.drawCentredString(x + w / 2, y + h / 2 - 10, small)

    def text(self, x, y, value, size=8, bold=False):
        self.canv.setFillColor(INK)
        self.canv.setFont("BodyBold" if bold else "Body", size)
        self.canv.drawString(x, y, value)

    def draw(self):
        c = self.canv
        c.saveState()
        y0 = self.height - self.panel_height
        c.setStrokeColor(MID)
        c.setLineWidth(0.5)
        c.rect(0, y0, self.width, self.panel_height, fill=0, stroke=1)
        getattr(self, f"draw_{self.figure_id}")(y0)
        self.text(self.width - 31, y0 + self.panel_height - 17, self.figure_id, 7)
        self.caption.drawOn(c, 0, 2)
        c.restoreState()

    def draw_V02(self, y0):
        self.text(15, y0 + 216, "Một lần fork thành công", 10, True)
        self.box(166, y0 + 171, 140, 30, "fork()", fill=True)
        self.line(198, y0 + 171, 112, y0 + 152)
        self.line(274, y0 + 171, 360, y0 + 152)
        self.box(17, y0 + 117, 190, 35, "CHA · PID 4200", "fork trả 4201")
        self.box(264, y0 + 117, 190, 35, "CON · PID 4201", "fork trả 0")
        self.line(360, y0 + 117, 360, y0 + 105)
        self.box(264, y0 + 70, 190, 35, "execve()", "PID vẫn là 4201", fill=True)
        self.text(268, y0 + 55, "OK: image mới; không trở về", 8)
        self.text(268, y0 + 43, "Lỗi: -1 / exception; có thể exit 127", 8)
        self.line(111, y0 + 117, 111, y0 + 58)
        self.box(17, y0 + 24, 190, 34, "waitpid(4201)", "nhận status 0 hoặc 127")
        self.text(15, y0 + 10, "fork lỗi: cha nhận -1, không có tiến trình con để wait.", 8)

    def draw_V03(self, y0):
        self.text(15, y0 + 207, "Trước rename: hai đường tham chiếu cùng đối tượng", 10, True)
        self.box(15, y0 + 148, 132, 36, "Tên cũ", "/srv/log/current")
        self.box(170, y0 + 148, 132, 36, "Mục thư mục", "entry → inode 42", fill=True)
        self.box(325, y0 + 148, 132, 36, "inode 42", "nội dung + metadata")
        self.line(147, y0 + 166, 170, y0 + 166, arrow=True)
        self.line(302, y0 + 166, 325, y0 + 166, arrow=True)
        self.box(15, y0 + 86, 132, 36, "FD 7 · process", "đã mở trước rename")
        self.box(170, y0 + 86, 132, 36, "Open file desc.", "offset + flags", fill=True)
        self.line(147, y0 + 104, 170, y0 + 104, arrow=True)
        self.line(302, y0 + 104, 390, y0 + 148, arrow=True)
        self.line(10, y0 + 69, 461, y0 + 69)
        self.text(15, y0 + 49, "Sau rename: entry mang tên mới; FD 7 vẫn tới inode 42.", 9, True)
        self.text(15, y0 + 32, "Hard link: entry khác → cùng inode; symlink: nội dung là đường dẫn.", 8)
        self.text(15, y0 + 14, "Quyền tìm kiếm thư mục vẫn cần khi mở bằng tên mới.", 8)

    def draw_V09(self, y0):
        self.text(15, y0 + 201, "MERGE", 10, True)
        self.text(257, y0 + 201, "REBASE", 10, True)
        for x, y, label in ((34, 145, "B"), (110, 173, "D"), (110, 112, "C"),
                            (195, 145, "M"), (276, 145, "B"), (355, 173, "D"),
                            (433, 173, "C′")):
            self.canv.circle(x, y0 + y, 13, stroke=1, fill=0)
            self.text(x - 5, y0 + y - 3, label, 9, True)
        for a, b in (((47,145),(96,173)),((47,145),(96,112)),((123,173),(182,145)),
                     ((123,112),(182,145)),((289,145),(342,173)),((368,173),(420,173))):
            self.line(a[0], y0+a[1], b[0], y0+b[1], arrow=True)
        self.text(17, y0 + 75, "M có hai cha D và C; giữ nguyên commit C.", 8.5)
        self.text(257, y0 + 75, "C′ có cha D và ID mới; C không đổi.", 8.5)
        self.line(10, y0 + 58, 461, y0 + 58)
        self.text(15, y0 + 37, "Cả hai cách đều cần giải conflict và chạy kiểm thử trên kết quả.", 8.5)
        self.text(15, y0 + 19, "Đồ thị giả định: B là merge base, main đi B→D, feature đi B→C.", 8)

    def draw_V44(self, y0):
        self.text(15, y0 + 225, "C1: cùng byte có thể được nhiều tên tham chiếu", 10, True)
        self.box(15, y0 + 164, 114, 40, "commit C1", "tree T1; parent A", fill=True)
        self.box(179, y0 + 164, 114, 40, "tree T1", "100644 app.conf → B1")
        self.box(343, y0 + 164, 114, 40, "blob B1", "byte: port=8080")
        self.line(129, y0 + 184, 179, y0 + 184, arrow=True)
        self.line(293, y0 + 184, 343, y0 + 184, arrow=True)
        self.box(15, y0 + 91, 114, 40, "commit C2", "tree T2; parent C1", fill=True)
        self.box(179, y0 + 91, 114, 40, "tree T2", "100644 service.conf → B1")
        self.line(71, y0 + 131, 71, y0 + 164, arrow=True)
        self.line(129, y0 + 111, 179, y0 + 111, arrow=True)
        self.line(293, y0 + 111, 391, y0 + 164, arrow=True)
        self.text(15, y0 + 69, "Đổi tên: B1 giữ byte; tên entry đổi nên tree và commit đổi.", 8.5)
        self.line(10, y0 + 51, 461, y0 + 51)
        self.text(15, y0 + 33, "Sửa port=9090 sau đó: blob B2, tree T3, commit C3.", 8.5)
        self.text(15, y0 + 16, "Các ký hiệu B/T/C là nhãn mô hình, không phải SHA quan sát.", 8)

    def draw_V45(self, y0):
        self.text(15, y0 + 205, "Cùng app.conf ở ba thời điểm · timeout_ms", 10, True)
        for x, label in ((17, "HEAD"), (169, "Index"), (321, "Working tree")):
            self.text(x, y0 + 177, label, 9, True)
        rows = (("B: chưa sửa", "1000", "1000", "1000"),
                ("sửa, add", "1000", "2000", "2000"),
                ("sửa tiếp", "1000", "2000", "3000"))
        for i, (name, head, index, work) in enumerate(rows):
            y = y0 + 140 - i * 44
            self.text(17, y + 27, name, 7.7)
            for x, value in ((105, head), (218, index), (370, work)):
                self.box(x, y, 82, 27, value, fill=i == 2 and x == 218)
        self.line(10, y0 + 34, 461, y0 + 34)
        self.text(15, y0 + 17, "Commit sau hàng cuối lấy 2000 từ index; 3000 còn trên đĩa.", 8.5)

    def draw_V46(self, y0):
        self.text(15, y0 + 203, "Tên ref → object; parent ← commit trước", 10, True)
        self.box(15, y0 + 146, 97, 38, "tag v1.4", "ref → B")
        self.box(126, y0 + 146, 110, 38, "origin/main", "ref local → C")
        self.box(252, y0 + 146, 93, 38, "main", "ref → D", fill=True)
        self.box(361, y0 + 146, 94, 38, "HEAD", "symbolic → main", fill=True)
        self.line(361, y0 + 165, 345, y0 + 165, arrow=True)
        for x, label in ((32, "B"), (188, "C"), (344, "D")):
            self.box(x, y0 + 82, 79, 32, label)
        self.line(63, y0 + 146, 71, y0 + 114, arrow=True)
        self.line(181, y0 + 146, 227, y0 + 114, arrow=True)
        self.line(298, y0 + 146, 383, y0 + 114, arrow=True)
        self.line(344, y0 + 98, 267, y0 + 98, arrow=True)
        self.line(188, y0 + 98, 111, y0 + 98, arrow=True)
        self.text(15, y0 + 58, "D → C → B là quan hệ parent; origin/main chỉ là bản ghi sau fetch.", 8.3)
        self.line(10, y0 + 42, 461, y0 + 42)
        self.text(15, y0 + 23, "Tag minh họa trỏ B; các ref có thể cùng hoặc khác đích.", 8.2)

    def draw_V47(self, y0):
        self.text(15, y0 + 220, "FAST-FORWARD", 9.5, True)
        self.text(249, y0 + 220, "PHÂN KỲ + CONFLICT", 9.5, True)
        self.box(17, y0 + 166, 52, 30, "B")
        self.box(138, y0 + 166, 52, 30, "C")
        self.line(69, y0 + 181, 138, y0 + 181, arrow=True)
        self.text(17, y0 + 148, "main: B → C; không cần M", 8)
        self.box(256, y0 + 166, 52, 30, "B")
        self.box(353, y0 + 188, 52, 30, "D")
        self.box(353, y0 + 143, 52, 30, "C")
        self.line(308, y0 + 181, 353, y0 + 203, arrow=True)
        self.line(308, y0 + 181, 353, y0 + 158, arrow=True)
        self.text(249, y0 + 125, "B là base; D/C cùng sửa timeout.", 8)
        self.line(10, y0 + 111, 461, y0 + 111)
        self.text(15, y0 + 91, "Index khi merge dừng ở app.conf:", 8.5, True)
        for x, label, small in ((17, "stage 1", "B: 1000"),
                                (168, "stage 2", "D: 3000"),
                                (319, "stage 3", "C: 2000")):
            self.box(x, y0 + 38, 135, 39, label, small, fill=x == 168)
        self.text(15, y0 + 18, "Giải thành 2500 là quyết định giả định; stage rồi test trước M.", 8)

    def draw_V48(self, y0):
        self.text(15, y0 + 217, "SAU M ĐÃ CÔNG BỐ", 9.5, True)
        self.box(16, y0 + 164, 99, 36, "D", "cha 1 của M")
        self.box(182, y0 + 164, 99, 36, "M", "main hiện tại")
        self.box(349, y0 + 164, 107, 36, "R", "revert mới", fill=True)
        self.line(115, y0 + 182, 182, y0 + 182, arrow=True)
        self.line(281, y0 + 182, 349, y0 + 182, arrow=True)
        self.text(17, y0 + 143, "Revert: main → R; M vẫn ở lịch sử.", 8.5)
        self.line(10, y0 + 128, 461, y0 + 128)
        self.text(15, y0 + 108, "Reset M → D dịch ref; tác động lên ba lớp:", 8.5, True)
        for y, mode, state in ((84, "soft", "index và worktree giữ bản M"),
                               (61, "mixed", "index về D; worktree giữ M"),
                               (38, "hard", "index và worktree về D")):
            self.text(22, y0 + y, mode, 8.5, True)
            self.text(100, y0 + y, state, 8.5)
        self.text(15, y0 + 14, "Cả hai không tự đảo dữ liệu hay bản chạy ở production.", 8)

    def draw_V10(self, y0):
        self.text(15, y0 + 197, "Một pipeline Bash bị hiểu nhầm", 10, True)
        self.box(15, y0 + 137, 125, 45, "tar", "exit 2; stderr")
        self.box(177, y0 + 137, 125, 45, "tee", "exit 0; in log", fill=True)
        self.box(337, y0 + 137, 120, 45, "pipeline", "mặc định: exit 0")
        self.line(140, y0 + 159, 177, y0 + 159, arrow=True)
        self.line(302, y0 + 159, 337, y0 + 159, arrow=True)
        self.text(21, y0 + 119, "2>&1 đưa stderr của tar vào pipe; tee nhận được lỗi.", 8.5)
        self.line(10, y0 + 101, 461, y0 + 101)
        self.box(15, y0 + 42, 205, 42, "Không pipefail", "set -e thấy 0 → BACKUP_OK")
        self.box(248, y0 + 42, 208, 42, "Có pipefail", "pipeline thấy 2 → dừng lỗi", fill=True)
        self.text(15, y0 + 19, "Vẫn phải kiểm archive và hậu điều kiện; pipefail không chứng minh backup tốt.", 8)

    def draw_V12(self, y0):
        self.text(15, y0 + 209, "Một thay đổi chỉ an toàn khi nối được các định danh", 10, True)
        nodes = [(14, "Commit c84", "source"), (128, "Inputs", "toolchain / deps"),
                 (242, "Artifact H84", "digest"), (356, "Test gate", "đúng H84")]
        for x, title, small in nodes:
            self.box(x, y0 + 143, 101, 42, title, small, fill=x in (242, 356))
        for x in (115, 229, 343): self.line(x, y0 + 164, x + 13, y0 + 164, arrow=True)
        self.box(51, y0 + 65, 164, 47, "Release record", "chọn H84; approval")
        self.box(258, y0 + 65, 164, 47, "Instance phục vụ", "imageID H84; request", fill=True)
        self.line(407, y0 + 143, 133, y0 + 112, arrow=True)
        self.line(215, y0 + 89, 258, y0 + 89, arrow=True)
        self.text(15, y0 + 40, "Tag là nhãn có thể đổi; digest gắn với byte artifact đã kiểm.", 8.5)
        self.text(15, y0 + 21, "Deploy xong ≠ Ready; kiểm revision và request ở đường phục vụ.", 8.5)

    def draw_V16(self, y0):
        self.text(15, y0 + 215, "Tạo lại container từ image mới · dữ liệu giả định", 10, True)
        self.box(14, y0 + 158, 136, 43, "Image H1 → H2", "artifact bất biến")
        self.box(167, y0 + 158, 136, 43, "Container A → B", "writable layer mới", fill=True)
        self.box(320, y0 + 158, 137, 43, "App path", "/var/lib/orders")
        self.line(150, y0 + 179, 167, y0 + 179, arrow=True)
        self.line(303, y0 + 179, 320, y0 + 179, arrow=True)
        self.text(15, y0 + 139, "Một trong ba nơi lưu, tùy cấu hình mount:", 8.5, True)
        self.box(15, y0 + 83, 136, 43, "Writable A", "mất khi xóa A")
        self.box(168, y0 + 83, 136, 43, "Named volume", "vẫn gắn lại được", fill=True)
        self.box(321, y0 + 83, 136, 43, "Bind mount", "đường dẫn host")
        self.line(389, y0 + 158, 389, y0 + 132)
        self.line(83, y0 + 132, 389, y0 + 132)
        for x in (83,236,389): self.line(x, y0 + 132, x, y0 + 126, arrow=True)
        self.line(10, y0 + 65, 461, y0 + 65)
        self.text(15, y0 + 45, "Project khác có thể chọn tên volume khác; volume cũ chưa bị xóa.", 8)
        self.text(15, y0 + 29, "Stopped/removed khác xóa volume; down mặc định không xóa named volume.", 8)
        self.text(15, y0 + 13, "Persist không phải backup: cần snapshot/restore kiểm chứng riêng.", 8)

    def draw_V18(self, y0):
        self.text(15, y0 + 212, "Private EC2: cùng nguồn, hai đích dịch vụ khác nhau", 10, True)
        self.box(15, y0 + 153, 104, 38, "EC2 private", "DNS chọn đích")
        self.box(156, y0 + 153, 137, 38, "DNS result", "IP / tên dịch vụ", fill=True)
        self.box(330, y0 + 153, 127, 38, "Route table", "subnet association")
        self.line(119, y0 + 172, 156, y0 + 172, arrow=True)
        self.line(293, y0 + 172, 330, y0 + 172, arrow=True)
        self.box(14, y0 + 77, 210, 45, "S3 gateway endpoint", "prefix route → S3 cùng Region", fill=True)
        self.box(248, y0 + 77, 209, 45, "STS regional endpoint", "cần đường riêng: NAT/IGW hoặc interface")
        self.line(368, y0 + 153, 120, y0 + 122, arrow=True)
        self.line(401, y0 + 153, 352, y0 + 122, arrow=True)
        self.line(10, y0 + 60, 461, y0 + 60)
        self.text(15, y0 + 40, "SG tại ENI và NACL tại subnet phải cho phép gói đi/về.", 8)
        self.text(15, y0 + 24, "Sau TCP/HTTP: IAM xét principal, action, resource, context riêng.", 8)
        self.text(15, y0 + 9, "Timeout trước HTTP không phải bằng chứng AccessDenied.", 8)

    def draw_V07(self, y0):
        self.text(15, y0 + 220, "CLIENT", 9, True)
        self.text(379, y0 + 220, "SERVER", 9, True)
        self.line(73, y0 + 207, 73, y0 + 43, dashed=True)
        self.line(397, y0 + 207, 397, y0 + 43, dashed=True)
        rows = [
            (195, True, "SYN · seq 1000"),
            (165, False, "SYN-ACK · seq 5000, ack 1001"),
            (135, True, "ACK · seq 1001, ack 5001"),
            (105, True, "DATA · seq 1001–1004 (4 byte)"),
            (75, False, "ACK 1005 · gói ACK giả định bị mất"),
            (45, True, "RETRANSMIT · cùng byte 1001–1004"),
        ]
        for y, outbound, label in rows:
            yy = y0 + y
            self.line(75 if outbound else 395, yy, 395 if outbound else 75, yy, arrow=True)
            self.text(110, yy + 5, label, 8)
        self.text(15, y0 + 18, "Server ACK lại 1005: đã nhận liên tục đến byte 1004.", 8)
        self.text(15, y0 + 7, "ACK mất không có nghĩa ứng dụng nhận dữ liệu hai lần.", 8)

    def draw_V20(self, y0):
        self.text(15, y0 + 199, "Ba thực thể tại cùng một thời điểm", 10, True)
        self.box(18, y0 + 125, 132, 48, "HCL · A: CPU 2", "desired configuration", fill=True)
        self.box(170, y0 + 125, 132, 48, "STATE: CPU 2", "binding → i-demo-01", fill=True)
        self.box(322, y0 + 125, 132, 48, "API · B: CPU 4", "real infrastructure", fill=True)
        self.line(84, y0 + 125, 175, y0 + 66, arrow=True)
        self.line(236, y0 + 125, 236, y0 + 66, arrow=True)
        self.line(388, y0 + 125, 295, y0 + 66, arrow=True)
        self.box(103, y0 + 32, 270, 34, "provider read / refresh / plan", "so A, state mới và B; có thể đề xuất thay", fill=False)
        self.text(15, y0 + 12, "Plan không khóa API và không bảo đảm apply thành công.", 8)

    def draw_V22(self, y0):
        self.text(15, y0 + 202, "Cùng playbook trên fixture POSIX · tình huống giả định", 10, True)
        columns = (20, 120, 236, 348)
        for x, label in zip(columns, ("Lượt", "file: mode 0750", "template", "handler")):
            self.text(x, y0 + 176, label, 8, True)
        rows = (
            ("1 · tạo mới", "changed", "changed → notify", "chạy 1 lần"),
            ("2 · chạy lại", "ok", "ok", "không chạy"),
            ("Drift quyền", "changed", "ok", "không chạy"),
            ("Drift config", "ok", "changed → notify", "chạy 1 lần"),
        )
        for index, row in enumerate(rows):
            y = y0 + 146 - index * 30
            if index % 2 == 0:
                self.canv.setFillColor(LIGHT)
                self.canv.rect(12, y - 9, 447, 28, fill=1, stroke=0)
            for x, value in zip(columns, row): self.text(x, y, value, 8)
            self.line(12, y - 10, 459, y - 10)
        self.text(15, y0 + 18, "check mode chỉ dự báo thay đổi; apply thật và request vẫn cần hậu kiểm.", 8)

    def draw_V29(self, y0):
        with (ROOT / "examples" / "trace-ch19.csv").open(encoding="utf-8", newline="") as stream:
            spans = list(csv.DictReader(stream))
        logs = json.loads((ROOT / "examples" / "logs-ch19.json").read_text(encoding="utf-8"))
        if [(s["alias"], int(s["start_ms"]), int(s["end_ms"])) for s in spans] != [
            ("G", 0, 420), ("A", 12, 405), ("D", 30, 280),
            ("U1", 285, 335), ("U2", 345, 385),
        ] or [int(x["time"][20:23]) for x in logs] != [30, 335, 405]:
            raise ValueError("Fixture trace/log thay đổi; phải kiểm lại hình V29")
        self.text(15, y0 + 224, "Cùng request req-17 · trục thời gian 0–420 ms", 10, True)
        x0, scale = 96, 345 / 420
        for tick in (0, 100, 200, 300, 420):
            x = x0 + tick * scale
            self.line(x, y0 + 43, x, y0 + 199, dashed=True)
            self.text(x - 8, y0 + 31, str(tick), 7)
        for index, span in enumerate(spans):
            y = y0 + 182 - index * 28
            start, end = int(span["start_ms"]), int(span["end_ms"])
            self.text(17, y + 5, span["alias"] + " " + span["stage"], 8)
            self.canv.setFillColor(LIGHT if index % 2 else colors.white)
            self.canv.setStrokeColor(INK)
            self.canv.rect(x0 + start * scale, y, (end-start)*scale, 16, fill=1, stroke=1)
            if span["status"] == "ERROR":
                self.text(x0 + start*scale + 3, y + 4, "ERROR", 7, True)
        for point in (30, 335, 405):
            self.canv.setFillColor(INK)
            self.canv.circle(x0 + point * scale, y0 + 48, 2.8, fill=1, stroke=0)
        self.text(15, y0 + 12, "Log: 30 / 335 / 405 ms; HTTP 200 cuối. Span lồng nhau không cộng duration.", 7.8)

    def draw_V33(self, y0):
        self.text(15, y0 + 211, "Đường chứng cứ qua ba ranh giới", 10, True)
        self.box(15, y0 + 148, 135, 40, "Nguồn", "commit + dependency lock")
        self.box(168, y0 + 148, 135, 40, "Build", "input + SBOM", fill=True)
        self.box(321, y0 + 148, 135, 40, "Artifact", "image digest H84")
        self.line(150, y0 + 168, 168, y0 + 168, arrow=True)
        self.line(303, y0 + 168, 321, y0 + 168, arrow=True)
        self.box(15, y0 + 78, 135, 40, "Attestation", "subject = H84")
        self.box(168, y0 + 78, 135, 40, "Verifier", "key + subject", fill=True)
        self.box(321, y0 + 78, 135, 40, "Admission", "spec dùng H84")
        self.line(389, y0 + 148, 83, y0 + 118, arrow=True)
        self.line(150, y0 + 98, 168, y0 + 98, arrow=True)
        self.line(303, y0 + 98, 321, y0 + 98, arrow=True)
        self.line(10, y0 + 60, 461, y0 + 60)
        self.text(15, y0 + 41, "Verifier kiểm chữ ký và digest; admission xét request theo policy.", 8)
        self.text(15, y0 + 25, "Pod thực, request và dữ liệu cần hậu kiểm sau admission.", 8)
        self.text(15, y0 + 10, "Chữ ký không chứng minh test đã đủ hoặc mã không có lỗi.", 8)

    def draw_V43(self, y0):
        self.text(15, y0 + 228, "Một thay đổi · mỗi hàng có chứng cứ và quy tắc dừng", 10, True)
        headers = ("Bước", "Artifact/ID", "Phép kiểm", "Trạng thái")
        xs = (17, 113, 236, 383)
        for x, label in zip(xs, headers): self.text(x, y0 + 202, label, 8, True)
        rows = (
            ("Build", "commit → digest", "tính lại SHA-256", "CHƯA ĐO"),
            ("Deploy", "revision → imageID", "Pod + request", "CHƯA ĐO"),
            ("Quyền", "role + secret ID", "ca âm/ca dương", "CHƯA ĐO"),
            ("Quan sát", "request_id", "metric/log/trace", "CHƯA ĐO"),
            ("Sự cố", "injection ID", "stop / rollback", "CHƯA ĐO"),
            ("Dữ liệu", "backup ID", "restore + SLI", "CHƯA ĐO"),
        )
        for index, row in enumerate(rows):
            y = y0 + 177 - index * 26
            if index % 2 == 0:
                self.canv.setFillColor(LIGHT)
                self.canv.rect(12, y - 8, 447, 25, fill=1, stroke=0)
            for x, value in zip(xs, row): self.text(x, y, value, 7.8)
            self.line(12, y - 9, 459, y - 9)
        self.text(15, y0 + 14, "Thiếu identity, restore hoặc hậu trạng thái dữ liệu → DỪNG; SKIP có lý do.", 7.8)

    def draw_V23(self, y0):
        self.text(15, y0 + 206, "ĐƯỜNG ĐIỀU KHIỂN", 9, True)
        self.box(14, y0 + 159, 103, 32, "Người dùng", "apply spec")
        self.box(174, y0 + 159, 126, 32, "API server + etcd", "lưu object spec/status", fill=True)
        self.line(117, y0 + 175, 174, y0 + 175, arrow=True)
        self.line(237, y0 + 159, 237, y0 + 143)
        self.line(65, y0 + 143, 408, y0 + 143)
        self.box(14, y0 + 101, 103, 29, "Controller", "ReplicaSet / Pod")
        self.box(184, y0 + 101, 103, 29, "Scheduler", "node binding")
        self.box(344, y0 + 101, 118, 29, "Kubelet + runtime", "chạy Pod trên node")
        for x in (65, 237, 408):
            self.line(x, y0 + 143, x, y0 + 130, arrow=True)
        self.text(15, y0 + 86, "Ba tác nhân đọc/ghi object qua API; status trở về API bất đồng bộ.", 8)
        self.line(10, y0 + 73, 461, y0 + 73)
        self.text(15, y0 + 54, "ĐƯỜNG DỮ LIỆU", 9, True)
        self.box(15, y0 + 16, 120, 27, "Client request")
        self.box(175, y0 + 16, 120, 27, "Service endpoint")
        self.box(335, y0 + 16, 120, 27, "Pod Ready")
        self.line(135, y0 + 29, 175, y0 + 29, arrow=True)
        self.line(295, y0 + 29, 335, y0 + 29, arrow=True)
        self.text(15, y0 + 5, "apply thành công ≠ Pod Ready ≠ request thành công", 8)


def figure_story(figure_id: str, styles: dict):
    return KeepTogether([MechanismFigure(figure_id, styles)])
