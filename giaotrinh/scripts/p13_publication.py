"""Render the reviewed P13 manuscript and its CSV-backed vector figures.

Only manuscript/answers enter the book. The claim ledger and status files stay
outside the PDF. Every figure calls the chapter's fixture audit before drawing.
"""

from __future__ import annotations

import csv
import html
import re
import runpy
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Flowable, KeepTogether, Paragraph, Preformatted, Spacer, Table, TableStyle

PART = Path(__file__).resolve().parents[1] / "authoring" / "P13"
INK = colors.HexColor("#202020")
MID = colors.HexColor("#777777")
LIGHT = colors.HexColor("#ececec")


def fixture(chapter: str):
    folder = PART / chapter
    result = runpy.run_path(str(folder / "verify.py"))["audit"]()
    with (folder / ("load.csv" if chapter == "C04" else "timeline.csv" if chapter in {"C02", "C03"} else "five_minute.csv")).open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return result, rows


def markup(value: str) -> str:
    value = re.sub(r"P13\.C(\d{2})\.L(\d{2})", lambda m: f"Bài XIII.{int(m[1])}.{int(m[2])}", value)
    value = re.sub(r"P13\.C(\d{2})", lambda m: f"Chương XIII.{int(m[1])}", value)
    value = html.escape(value)
    value = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"`([^`]+)`", r'<font name="Mono">\1</font>', value)
    return value


class Figure(Flowable):
    """Black and white PDF vector figure with an inseparable caption."""

    def __init__(self, chapter: str, caption: str, styles: dict, width: float = 471):
        super().__init__()
        self.chapter = chapter
        self.width = width
        self.panel_height = 265 if chapter == "C01" else 254
        self.height = self.panel_height
        self.caption = Paragraph(markup(caption), styles["caption"])
        _, caption_h = self.caption.wrap(width, 100)
        self.height += caption_h + 10

    def draw(self):
        c = self.canv
        c.saveState()
        c.setStrokeColor(INK)
        c.setFillColor(INK)
        c.setLineWidth(0.75)
        c.rect(0, self.height - self.panel_height, self.width,
               self.panel_height, stroke=1, fill=0)
        getattr(self, f"draw_{self.chapter}")(c, self.height - self.panel_height)
        self.caption.drawOn(c, 0, 2)
        c.restoreState()

    @staticmethod
    def label(c, x, y, value, size=9, bold=False):
        c.setFont("BodyBold" if bold else "Body", size)
        c.drawString(x, y, str(value))

    def draw_C01(self, c, y0):
        data, rows = fixture("C01")
        if (data["remaining"], data["burn_1h"], data["burn_5m"]) != (300, 15.75, 60):
            raise ValueError("V30 fixture changed without editorial review")
        c.saveState()
        c.translate(0, 11)
        self.label(c, 15, y0 + 232, "V30  |  SLO 99,9%  |  cửa sổ 30 ngày (fixture)", 10, True)
        self.label(c, 15, y0 + 202, "Ngân sách: 1.000 bad events", 9)
        c.setFillColor(LIGHT); c.rect(15, y0 + 177, 440, 18, fill=1, stroke=0)
        c.setFillColor(INK); c.rect(15, y0 + 177, 440 * 700 / 1000, 18, fill=1, stroke=0)
        c.setFillColor(colors.white); self.label(c, 20, y0 + 182, "Đã dùng 700", 9, True)
        c.setFillColor(INK); self.label(c, 15 + 440 * .7 + 8, y0 + 182, "Còn 300", 9, True)
        self.label(c, 15, y0 + 154, "Burn rate (lần ngân sách bình quân)", 9)
        scale = 6.5
        for i, (name, value) in enumerate((("1 giờ", float(data["burn_1h"])), ("5 phút", float(data["burn_5m"])))):
            yy = y0 + 129 - i * 40
            self.label(c, 15, yy + 7, name)
            c.setFillColor(LIGHT); c.rect(75, yy, 380, 20, fill=1, stroke=0)
            c.setFillColor(INK); c.rect(75, yy, min(value * scale, 380), 20, fill=1, stroke=0)
            c.setFillColor(colors.white if value > 10 else INK)
            self.label(c, 81, yy + 5, f"{value:g}×", 9, True)
            c.setFillColor(INK)
        threshold_x = 75 + 14.4 * scale
        c.setDash(3, 2); c.line(threshold_x, y0 + 86, threshold_x, y0 + 149); c.setDash()
        self.label(c, threshold_x + 4, y0 + 69, "ngưỡng 14,4×", 8)
        c.restoreState()
        self.label(c, 15, y0 + 58, f"12 cửa sổ: {sum(int(r['valid']) for r in rows):,} valid / {sum(int(r['bad']) for r in rows)} bad; mất mẫu = UNKNOWN", 8)
        self.label(c, 15, y0 + 47, "bad events / cửa sổ 5 phút (kết thúc phút)", 8)
        for i, row in enumerate(rows):
            x = 22 + i * 36
            bad = int(row["bad"])
            h = max(1, bad * .37)
            c.setFillColor(INK)
            c.rect(x, y0 + 18, 22, h, fill=1, stroke=0)
            self.label(c, x + 2, y0 + 7, row["minute_end"], 7)
        self.label(c, 445, y0 + 20, "60", 7)

    def draw_C02(self, c, y0):
        data, rows = fixture("C02")
        if (data["wrong_v2_requests"], data["distinct_affected_records"], data["post_mitigation_verified"]) != (30, None, False):
            raise ValueError("incident epistemic state changed")
        self.label(c, 15, y0 + 241, "Incident timeline | fixture, không phải production", 10, True)
        status_names = {"fixture observation": "QUAN SÁT", "fixture assumption": "GIẢ ĐỊNH", "proposed response": "ĐỀ XUẤT", "proposed mitigation": "ĐỀ XUẤT", "verification needed": "CẦN XÁC MINH", "reconciliation needed": "CẦN ĐỐI SOÁT"}
        for i, row in enumerate(rows):
            yy = y0 + 217 - i * 22
            c.setStrokeColor(LIGHT); c.line(15, yy - 5, 455, yy - 5); c.setStrokeColor(INK)
            self.label(c, 17, yy, row["time"], 8, True)
            self.label(c, 62, yy, status_names[row["epistemic_status"]], 7.5, True)
            text = row["event"]
            # Two bounded lines preserve the full event, without clipping the figure.
            words = text.split(); lines = [""]
            for word in words:
                candidate = (lines[-1] + " " + word).strip()
                if pdfmetrics.stringWidth(candidate, "Body", 7.5) > 270:
                    lines.append(word)
                else:
                    lines[-1] = candidate
            if len(lines) > 2:
                raise ValueError(f"timeline event too wide: {text}")
            for j, line in enumerate(lines):
                self.label(c, 176, yy - j * 8, line, 7.5)
        self.label(c, 15, y0 + 13, "31/1.000 request sai; số order phân biệt UNKNOWN; hậu kiểm 10:16 chưa chạy.", 8)

    def draw_C03(self, c, y0):
        data, rows = fixture("C03")
        if (data["rpo_minutes"], data["rto_minutes"]) != (8, 37):
            raise ValueError("V31 recovery fixture changed")
        self.label(c, 15, y0 + 231, "V31  |  Chuỗi phục hồi theo mốc thời gian giả định", 10, True)
        x0, x1 = 40, 430
        c.line(x0, y0 + 125, x1, y0 + 125)
        times = {"09:00": 0, "09:52": 52, "10:00": 60, "10:04": 64, "10:08": 68, "10:27": 87, "10:37": 97}
        for row in rows:
            x = x0 + times[row["at"]] / 97 * (x1 - x0)
            c.line(x, y0 + 119, x, y0 + 131)
            if row["event"] in {"base_backup", "last_recoverable_commit", "failure", "replay_finished", "service_verified"}:
                self.label(c, x - 14, y0 + (137 if row["event"] in {"base_backup", "failure", "service_verified"} else 105), row["at"], 8, True)
        self.label(c, 20, y0 + 190, "Base backup 09:00 + WAL liên tục đến 09:52", 9)
        self.label(c, 20, y0 + 170, "Sự cố 10:00; replay xong 10:27; ứng dụng xác minh 10:37", 9)
        self.label(c, 20, y0 + 72, "RPO = 10:00 - 09:52 = 8 phút (mục tiêu ≤15)", 9, True)
        self.label(c, 20, y0 + 54, "RTO = 10:37 - 10:00 = 37 phút (mục tiêu ≤45)", 9, True)
        self.label(c, 20, y0 + 30, "O-104/O-105 sau 09:52: cần đối soát; không gọi là không mất dữ liệu.", 8)

    def draw_C04(self, c, y0):
        data, rows = fixture("C04")
        if data["C_outstanding_growth"] != 2400:
            raise ValueError("capacity fixture changed")
        self.label(c, 15, y0 + 232, "Capacity | offered, completed và latency theo pha 60 giây", 10, True)
        self.label(c, 17, y0 + 202, "req/s", 8)
        c.line(66, y0 + 125, 66, y0 + 185)
        for value in (0, 100, 200):
            yy = y0 + 125 + value * .25
            c.line(62, yy, 69, yy)
            self.label(c, 37 if value else 55, yy - 3, value, 7.5)
        labels = ("A", "B", "C")
        for i, row in enumerate(rows):
            x = 85 + i * 128
            self.label(c, x + 28, y0 + 202, labels[i], 9, True)
            offered = int(row["offered_rps"]); completed = int(row["completed_rps"])
            c.setFillColor(LIGHT); c.rect(x, y0 + 125, 22, offered * .25, fill=1, stroke=1)
            c.setFillColor(INK); c.rect(x + 27, y0 + 125, 22, completed * .25, fill=1, stroke=0)
            self.label(c, x, y0 + 110, f"{offered}/{completed}", 8)
            self.label(c, x - 6, y0 + 83, f"p95 {int(row['p95_latency_ms'])} ms", 8)
            self.label(c, x - 6, y0 + 64, f"DB {int(row['db_wait_p95_ms'])} ms", 8)
        c.setFillColor(INK)
        self.label(c, 17, y0 + 38, "C: (220 - 180) req/s × 60 s = 2.400 request chưa hoàn tất", 9, True)
        self.label(c, 17, y0 + 20, "Cột nhạt: offered; cột đậm: completed. Không đo riêng queue length.", 8)


def _blocks(path: Path, styles: dict, heading_factory, chapter: int, answer: bool = False):
    text = path.read_text(encoding="utf-8")
    if re.search(r"https?://|\[(?:R|B|SRE|DR|INC|PERF)\d+\]", text):
        raise ValueError(f"source leak in {path}")
    story = []
    paragraph = []
    code = []
    in_code = False

    def flush():
        nonlocal paragraph
        if paragraph:
            content = " ".join(s.strip() for s in paragraph)
            story.append(Paragraph(markup(content), styles["answerbody"] if answer else styles["p13body"]))
            paragraph = []

    for line in text.splitlines() + [""]:
        if line.startswith("```"):
            flush()
            if in_code:
                for code_line in code:
                    if pdfmetrics.stringWidth(code_line, "Mono", 8.0) > 453:
                        raise ValueError(f"code too wide in {path}: {code_line}")
                code_style = styles["p13code"]
                story.append(Preformatted("\n".join(code), code_style))
                code = []
            in_code = not in_code
            continue
        if in_code:
            code.append(line)
            continue
        if not line.strip():
            flush()
            continue
        if line.startswith("## P13.C") and not answer:
            flush()
            m = re.match(r"## P13\.C(\d{2})\.L(\d{2}) — (.*)", line)
            if not m or int(m[1]) != chapter:
                raise ValueError(f"invalid lesson heading: {line}")
            lesson = int(m[2])
            story.append(heading_factory(f"Bài XIII.{chapter}.{lesson} — {m[3]}", 3,
                                         f"P13.C{chapter:02d}.L{lesson:02d}", styles))
            continue
        if line.startswith("### Bài tập "):
            flush()
            story.append(Paragraph(markup(line[4:]), styles["exercise"]))
            continue
        if line.startswith("# "):
            flush()  # Chapter title comes from the locked architecture, not manuscript heading.
            continue
        paragraph.append(line)
    if in_code:
        raise ValueError(f"unclosed code fence in {path}")
    return story


def part_story(styles: dict, heading_factory):
    result = []
    chapter_names = (
        "SLI, SLO và Error Budget", "Incident Response và Postmortem",
        "Backup và Disaster Recovery", "Performance và Capacity Planning",
    )
    result.append(heading_factory("PHẦN XIII — SRE VÀ PHỤC HỒI", 1, "P13", styles))
    result.append(Spacer(1, 42))
    result.append(Paragraph("Từ tín hiệu phục vụ tới quyết định phục hồi", styles["part_deck"]))
    result.append(Spacer(1, 35))
    for line in (
        "Câu hỏi trung tâm: Khi hệ thống trả lời sai, chậm hoặc mất dữ liệu, ta biết điều gì, còn thiếu bằng chứng nào và khi nào được tuyên bố đã phục hồi?",
        "Mô hình: định nghĩa phép đo → xác nhận tác động → giới hạn thiệt hại → khôi phục dữ liệu và phục vụ → thử sức chịu tải.",
        "Ranh giới: metric không tự nói nguyên nhân; rollback ứng dụng không sửa dữ liệu; một bản backup chưa được thử restore không chứng minh khả năng phục hồi.",
    ):
        result.append(Paragraph(markup(line), styles["part_intro"]))
    from reportlab.platypus import PageBreak
    result.append(PageBreak())
    for n, name in enumerate(chapter_names, 1):
        folder = PART / f"C{n:02d}"
        result.append(heading_factory(f"Chương XIII.{n} — {name}", 2, f"P13.C{n:02d}", styles))
        blocks = _blocks(folder / "manuscript.md", styles, heading_factory, n)
        # Figure follows its primary lesson; text keeps exact reviewed order.
        inserted = False
        for i, block in enumerate(blocks):
            if hasattr(block, "bookmark_key") and block.bookmark_key == f"P13.C{n:02d}.L03" and not inserted:
                caption = (
                    "Hình XIII.1.1 — V30: 700 bad đã dùng và 300 còn lại; burn 1h/5m từ dữ liệu giả định.",
                    "Hình XIII.2.1 — Trạng thái bằng chứng trong incident; 10:16 còn cần xác minh.",
                    "Hình XIII.3.1 — V31: WAL, điểm khôi phục và hậu kiểm ứng dụng; RPO/RTO giả định.",
                    "Hình XIII.4.1 — Tải A/B/C: offered và completed; chênh lệch C là tổng outstanding.",
                )[n - 1]
                lead = (
                    "Hình XIII.1.1 đặt ngân sách lỗi cạnh hai cửa sổ burn và 12 khoảng dữ liệu thực có trong fixture.",
                    "Hình XIII.2.1 giữ riêng quan sát, giả định, đề xuất và hậu kiểm còn thiếu.",
                    "Hình XIII.3.1 tách mốc replay database khỏi mốc ứng dụng được xác minh.",
                    "Hình XIII.4.1 đối chiếu tốc độ đến, tốc độ hoàn tất và độ trễ theo cùng pha tải.",
                )[n - 1]
                result.append(KeepTogether([
                    Paragraph(markup(lead), styles["caption"]),
                    Figure(f"C{n:02d}", caption, styles),
                ]))
                inserted = True
            result.append(block)
        if not inserted:
            raise ValueError(f"missing figure insertion point C{n:02d}")
        result.append(PageBreak())
    return result


def answer_story(styles: dict, heading_factory):
    result = [heading_factory("Lời giải Phần XIII", 1, "P13.answers", styles)]
    for n in range(1, 5):
        result.append(heading_factory(f"Chương XIII.{n} — đáp án", 2, f"P13.C{n:02d}.answers", styles))
        result.extend(_blocks(PART / f"C{n:02d}" / "answers.md", styles, heading_factory, n, answer=True))
    return result
