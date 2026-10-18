"""Build and audit a limited DevOps textbook candidate; never publish final here."""

from __future__ import annotations

import html
import hashlib
import re
from pathlib import Path

import pymupdf
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Flowable, Frame, PageBreak, PageTemplate, Paragraph,
    Spacer,
)
from reportlab.platypus.tableofcontents import TableOfContents


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "Cam_nang_devops.candidate.pdf"
FONT_DIR = Path("C:/Windows/Fonts")
PAGE_W, PAGE_H = A4
LEFT = RIGHT = 62
TOP = 65
BOTTOM = 62
URL_RE = re.compile(r"https?://[^\s]+")


def register_fonts() -> None:
    fonts = {
        "Body": "times.ttf",
        "BodyBold": "timesbd.ttf",
        "Mono": "consola.ttf",
    }
    for name, filename in fonts.items():
        path = FONT_DIR / filename
        if not path.is_file():
            raise FileNotFoundError(f"Font hệ điều hành không có: {path}")
        pdfmetrics.registerFont(TTFont(name, str(path)))
    pdfmetrics.registerFontFamily("Body", normal="Body", bold="BodyBold")


def style() -> dict[str, ParagraphStyle]:
    return {
        "title": ParagraphStyle("title", fontName="BodyBold", fontSize=31,
                                leading=38, alignment=TA_CENTER, textColor=colors.black),
        "subtitle": ParagraphStyle("subtitle", fontName="Body", fontSize=14,
                                   leading=20, alignment=TA_CENTER),
        "h1": ParagraphStyle("h1", fontName="BodyBold", fontSize=18,
                             leading=23, spaceBefore=17, spaceAfter=12,
                             keepWithNext=True),
        "h2": ParagraphStyle("h2", fontName="BodyBold", fontSize=13.5,
                             leading=18, spaceBefore=14, spaceAfter=8,
                             keepWithNext=True),
        "body": ParagraphStyle("body", fontName="Body", fontSize=11.7,
                               leading=18, alignment=TA_LEFT, spaceAfter=9),
        "toc": ParagraphStyle("toc-title", fontName="BodyBold", fontSize=19,
                              leading=24, spaceAfter=20),
        "tocentry": ParagraphStyle("toc-entry", fontName="Body", fontSize=11.5,
                                   leading=16, leftIndent=8, firstLineIndent=-8),
        "source": ParagraphStyle("source", fontName="Body", fontSize=10.5,
                                 leading=15, spaceAfter=7),
    }


class Heading(Paragraph):
    def __init__(self, text: str, level: int, key: str,
                 styles: dict[str, ParagraphStyle]):
        super().__init__(html.escape(text), styles[f"h{level}"])
        self.heading_text = text
        self.level = level
        self.bookmark_key = key


class Book(BaseDocTemplate):
    def __init__(self, path: Path):
        super().__init__(str(path), pagesize=A4, leftMargin=LEFT,
                         rightMargin=RIGHT, topMargin=TOP, bottomMargin=BOTTOM,
                         title="Cẩm nang ngành DevOps — bản đọc thử chương 1",
                         author="Dự án devops-learning")
        frame = Frame(LEFT, BOTTOM, PAGE_W - LEFT - RIGHT,
                      PAGE_H - TOP - BOTTOM, leftPadding=0, rightPadding=0,
                      topPadding=0, bottomPadding=0)
        self.addPageTemplates(PageTemplate(id="normal", frames=[frame],
                                           onPage=self.page_decoration))

    @staticmethod
    def page_decoration(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#999999"))
        canvas.setLineWidth(0.4)
        canvas.line(LEFT, 45, PAGE_W - RIGHT, 45)
        canvas.setFont("Body", 9)
        canvas.drawString(LEFT, 32, "CẨM NANG NGÀNH DEVOPS · BẢN ĐỌC THỬ")
        canvas.drawRightString(PAGE_W - RIGHT, 32, str(doc.page))
        canvas.restoreState()

    def afterFlowable(self, flowable: Flowable):
        if not isinstance(flowable, Heading):
            return
        key = flowable.bookmark_key
        self.canv.bookmarkPage(key)
        self.canv.addOutlineEntry(flowable.heading_text, key,
                                  level=flowable.level - 1, closed=False)
        self.notify("TOCEntry", (flowable.level - 1,
                                  flowable.heading_text, self.page, key))


def paragraph_markup(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r'<font name="Mono">\1</font>', escaped)
    escaped = URL_RE.sub(lambda m: f'<link href="{m.group(0)}" color="#222222">'
                                 f'{m.group(0)}</link>', escaped)
    return escaped


def read_markdown(path: Path, styles: dict[str, ParagraphStyle]) -> list[Flowable]:
    if not path.is_file():
        raise FileNotFoundError(path)
    blocks = re.split(r"\n\s*\n", path.read_text(encoding="utf-8").strip())
    story: list[Flowable] = []
    for index, block in enumerate(blocks):
        block = block.strip()
        key = "section-" + hashlib.sha1(f"{path.name}:{index}".encode("utf-8")).hexdigest()[:12]
        if block.startswith("# "):
            story.append(Heading(block[2:].strip(), 1, key, styles))
        elif block.startswith("## "):
            story.append(Heading(block[3:].strip(), 2, key, styles))
        else:
            if block.startswith("|") or block.startswith("-"):
                raise ValueError(f"Chưa hỗ trợ bảng hoặc list trong PDF: {path}")
            paragraph = " ".join(line.strip() for line in block.splitlines())
            pstyle = styles["source"] if paragraph.startswith("[") else styles["body"]
            story.append(Paragraph(paragraph_markup(paragraph), pstyle))
    return story


def build() -> None:
    register_fonts()
    styles = style()
    toc = TableOfContents()
    toc.levelStyles = [styles["tocentry"], styles["tocentry"]]
    story: list[Flowable] = [
        Spacer(1, 170),
        Paragraph("CẨM NANG<br/>NGÀNH DEVOPS", styles["title"]),
        Spacer(1, 26),
        Paragraph("Giáo trình kỹ thuật · bản đọc thử Chương 1", styles["subtitle"]),
        Spacer(1, 10),
        Paragraph("Chưa phải bản phát hành hoàn chỉnh", styles["subtitle"]),
        PageBreak(),
        Paragraph("MỤC LỤC", styles["toc"]),
        toc,
        PageBreak(),
    ]
    story.extend(read_markdown(ROOT / "chapters" / "01-tu-chuong-trinh-den-tien-trinh.md", styles))
    story.append(PageBreak())
    story.extend(read_markdown(ROOT / "answers.md", styles))
    Book(OUTPUT).multiBuild(story)
    audit(OUTPUT)


def audit(path: Path) -> None:
    doc = pymupdf.open(path)
    if len(doc) < 5:
        raise RuntimeError("Candidate quá ngắn so với nội dung bản thảo")
    text = "\n".join(page.get_text() for page in doc)
    for phrase in ("CẨM NANG", "MỤC LỤC", "Từ chương trình đến tiến trình",
                   "C1.1.", "Lời giải", "Chưa phải bản phát hành"):
        if phrase not in text:
            raise RuntimeError(f"Thiếu nội dung PDF: {phrase}")
    toc_entries = doc.get_toc()
    if len(toc_entries) < 7:
        raise RuntimeError("Bookmark chưa đủ")
    if toc_entries[0][2] != 3 or any(a[2] > b[2] for a, b in zip(toc_entries, toc_entries[1:])):
        raise RuntimeError(f"Bookmark trỏ sai trang hoặc sai thứ tự: {toc_entries}")
    url_count = 0
    for number, page in enumerate(doc, 1):
        if abs(page.rect.width - PAGE_W) > 0.1 or abs(page.rect.height - PAGE_H) > 0.1:
            raise RuntimeError(f"Trang {number} không đúng A4")
        for block in page.get_text("dict")["blocks"]:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    x0, y0, x1, y1 = span["bbox"]
                    if x0 < 25 or x1 > PAGE_W - 25 or y0 < 20 or y1 > PAGE_H - 20:
                        raise RuntimeError(f"Text ra ngoài vùng an toàn trang {number}: {span['text']}")
        url_count += sum(1 for link in page.get_links() if link["kind"] == pymupdf.LINK_URI)
    font_names = {font[3] for page in doc for font in page.get_fonts(full=True)}
    if not any("TimesNewRoman" in name.replace(" ", "") for name in font_names):
        raise RuntimeError(f"Times New Roman chưa được nhúng: {font_names}")
    if url_count < 4:
        raise RuntimeError("Thiếu hyperlink tới nguồn")
    print(f"CANDIDATE_OK pages={len(doc)} bookmarks={len(doc.get_toc())} links={url_count}")
    print(f"FONTS {sorted(font_names)}")
    print(f"OUTPUT {path}")


if __name__ == "__main__":
    build()
