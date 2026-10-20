"""Editable monochrome mechanism diagrams for the four foundational models.

The labels and edges are source, not screenshots; ReportLab keeps them as PDF
vector objects. Each diagram is deliberately scoped to one lesson claim.
"""

from __future__ import annotations

import math

from reportlab.lib import colors
from reportlab.platypus import Flowable, KeepTogether, Paragraph

INK = colors.HexColor("#242424")
MID = colors.HexColor("#777777")
LIGHT = colors.HexColor("#f0f0f0")

FIGURES = {
    "V02": ("Hình I.2.1 — fork/execve/wait: PID giả định; nhánh thành công và lỗi là hai lần chạy khác nhau.", 236),
    "V07": ("Hình III.2.1 — TCP: sequence đếm byte, ACK cộng dồn; số liệu giả định.", 242),
    "V20": ("Hình IX.2.1 — Terraform: cấu hình, state và API thực có thể lệch nhau; CPU là dữ kiện giả định.", 220),
    "V23": ("Hình XI.1.1 — Vòng điều khiển Kubernetes và đường request tách biệt.", 226),
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
