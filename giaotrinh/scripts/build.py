"""Build and audit a limited DevOps textbook candidate; never publish final here."""

from __future__ import annotations

import html
import hashlib
import json
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
    Preformatted, Spacer, LongTable, TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "Cam_nang_devops.candidate.pdf"
NEXT = ROOT / "Cam_nang_devops.candidate.next.pdf"
FONT_DIR = Path("C:/Windows/Fonts")
PAGE_W, PAGE_H = A4
LEFT = RIGHT = 62
TOP = 65
BOTTOM = 62
URL_RE = re.compile(r"https?://[^\s|)]+")
MARKER_RE = re.compile(r"\[(?:R|B|K|P|S)\d+\]")
SOURCE_HEADING_RE = re.compile(
    r"(?i)\b(?:nguồn chương|tài liệu tham khảo|danh mục tài liệu|bibliography|references)\b"
)
REFERENCE_SIGNATURE_RE = re.compile(
    r"(?i)\b(?:Linux man-pages 6\.19|Operating Systems: Three Easy Pieces|source_map\.json|docs\.kernel\.org|man7\.org)\b"
)


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
                               leading=17.5, alignment=TA_LEFT, spaceAfter=7.5),
        "toc": ParagraphStyle("toc-title", fontName="BodyBold", fontSize=19,
                              leading=24, spaceAfter=20),
        "tocentry": ParagraphStyle("toc-entry", fontName="Body", fontSize=11.5,
                                   leading=16, leftIndent=8, firstLineIndent=-8),
        "code": ParagraphStyle("code", fontName="Mono", fontSize=8.7,
                               leading=12.3, leftIndent=9, rightIndent=9,
                               backColor=colors.HexColor("#f5f5f5"),
                               spaceBefore=5, spaceAfter=11),
        "cell": ParagraphStyle("cell", fontName="Body", fontSize=9.5,
                               leading=12.5),
        "cellhead": ParagraphStyle("cellhead", fontName="BodyBold", fontSize=9.5,
                                   leading=12.5),
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
                         title="Cẩm nang ngành DevOps — bản đọc thử phần nền tảng",
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
    return escaped


def reference_urls() -> set[str]:
    registry = json.loads((ROOT / "source_map.json").read_text(encoding="utf-8"))
    markdown = (ROOT / "references.md").read_text(encoding="utf-8")
    urls = {source["url"] for source in registry["sources"].values()}
    urls.update(match.group(0).rstrip(".,;") for match in URL_RE.finditer(markdown))
    return urls


def check_source_map(registry: dict | None = None) -> None:
    if registry is None:
        registry = json.loads((ROOT / "source_map.json").read_text(encoding="utf-8"))
    sources = registry["sources"]
    if not registry.get("checked_on") or not registry.get("claims"):
        raise ValueError("Source map thiếu ngày kiểm chứng hoặc claim")
    for source in sources.values():
        if not all(source.get(key) for key in ("type", "version", "url")):
            raise ValueError(f"Source map thiếu metadata: {source}")
        if re.search(r"(?i)\b(?:latest|online)\b", source["version"]):
            raise ValueError(f"Nguồn chưa khóa phiên bản: {source}")
    for claim in registry["claims"]:
        path = (ROOT / claim["chapter"]).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            raise ValueError(f"Claim trỏ ngoài bản thảo: {claim}")
        if not claim.get("section") or not claim.get("evidence"):
            raise ValueError(f"Claim thiếu vị trí hoặc loại chứng cứ: {claim}")
        if not claim.get("sources") or any(source not in sources for source in claim["sources"]):
            raise ValueError(f"Claim thiếu nguồn hợp lệ: {claim}")
        if not all(claim.get(key) for key in ("source_location", "support", "limits")):
            raise ValueError(f"Claim thiếu biên bản đối chiếu ngữ nghĩa: {claim}")
        if claim.get("review_status") != "verified":
            raise ValueError(f"Claim chưa được đối chiếu nguồn: {claim}")
        chapter_text = path.read_text(encoding="utf-8")
        section = re.search(
            rf"(?ms)^## {re.escape(claim['section'])}\. .*?(?=^## |\Z)",
            chapter_text,
        )
        if not section:
            raise ValueError(f"Claim trỏ tới mục không có thật: {claim}")
        if claim["anchor"] not in section.group(0):
            raise ValueError(f"Claim không nằm trong mục đã khai báo: {claim['anchor']}")


def source_free_issues(text: str) -> list[str]:
    issues: list[str] = []
    text = text.replace("\u00ad", "-").replace("\u00a0", " ")
    if MARKER_RE.search(text):
        issues.append("citation marker")
    if SOURCE_HEADING_RE.search(text):
        issues.append("source heading")
    if REFERENCE_SIGNATURE_RE.search(text):
        issues.append("reference signature")
    compact = re.sub(r"\s+", "", text)
    for url in reference_urls():
        if url in compact:
            issues.append(f"reference URL: {url}")
    return issues


def read_markdown(path: Path, styles: dict[str, ParagraphStyle]) -> list[Flowable]:
    if not path.is_file():
        raise FileNotFoundError(path)
    blocks = re.split(r"\n\s*\n", path.read_text(encoding="utf-8").strip())
    issues = source_free_issues(path.read_text(encoding="utf-8"))
    if issues:
        raise ValueError(f"Nguồn tham khảo lọt vào bản thảo PDF {path}: {issues}")
    story: list[Flowable] = []
    for index, block in enumerate(blocks):
        block = block.strip()
        key = "section-" + hashlib.sha1(f"{path.name}:{index}".encode("utf-8")).hexdigest()[:12]
        if block.startswith("# "):
            story.append(Heading(block[2:].strip(), 1, key, styles))
        elif block.startswith("## "):
            story.append(Heading(block[3:].strip(), 2, key, styles))
        elif block.startswith("{{code:") and block.endswith("}}"):
            code_path = (ROOT / block[7:-2]).resolve()
            if not code_path.is_relative_to(ROOT / "examples") or not code_path.is_file():
                raise ValueError(f"Code example ngoài phạm vi hoặc thiếu: {code_path}")
            code = code_path.read_text(encoding="utf-8").rstrip()
            for line in code.splitlines():
                if pdfmetrics.stringWidth(line, "Mono", 8.7) > PAGE_W - LEFT - RIGHT - 18:
                    raise ValueError(f"Dòng code quá rộng: {code_path}: {line}")
            story.append(Preformatted(code, styles["code"]))
        elif block.startswith("|"):
            lines = block.splitlines()
            if len(lines) < 3 or not re.fullmatch(r"\|[\s:|-]+\|", lines[1]):
                raise ValueError(f"Bảng Markdown không hợp lệ: {path}")
            rows = [[part.strip() for part in line.strip().strip("|").split("|")]
                    for line in [lines[0], *lines[2:]]]
            columns = len(rows[0])
            if columns != 3 or any(len(row) != columns for row in rows):
                raise ValueError(f"Bảng này cần đúng ba cột: {path}")
            cells = [[Paragraph(paragraph_markup(item),
                                styles["cellhead"] if row_index == 0 else styles["cell"])
                      for item in row]
                     for row_index, row in enumerate(rows)]
            table = LongTable(cells, colWidths=[251, 110, 110], repeatRows=1,
                              hAlign="LEFT")
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eeeeee")),
                ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black),
                ("LINEBELOW", (0, 1), (-1, -1), 0.2, colors.HexColor("#dddddd")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]))
            story.append(table)
            story.append(Spacer(1, 10))
        else:
            if block.startswith("-"):
                raise ValueError(f"Chưa hỗ trợ bảng hoặc list trong PDF: {path}")
            paragraph = " ".join(line.strip() for line in block.splitlines())
            story.append(Paragraph(paragraph_markup(paragraph), styles["body"]))
    return story


def build() -> None:
    check_source_map()
    register_fonts()
    chapters = sorted((ROOT / "chapters").glob("[0-9][0-9]-*.md"))
    if not chapters:
        raise RuntimeError("Không có chương bản thảo")
    styles = style()
    toc = TableOfContents()
    toc.levelStyles = [styles["tocentry"], styles["tocentry"]]
    story: list[Flowable] = [
        Spacer(1, 170),
        Paragraph("CẨM NANG<br/>NGÀNH DEVOPS", styles["title"]),
        Spacer(1, 26),
        Paragraph(f"Giáo trình kỹ thuật · bản đọc thử {len(chapters)} chương", styles["subtitle"]),
        Spacer(1, 10),
        Paragraph("Chưa phải bản phát hành hoàn chỉnh", styles["subtitle"]),
        PageBreak(),
        Paragraph("MỤC LỤC", styles["toc"]),
        toc,
        PageBreak(),
    ]
    for chapter in chapters:
        story.extend(read_markdown(chapter, styles))
        story.append(PageBreak())
    story.extend(read_markdown(ROOT / "answers.md", styles))
    try:
        Book(NEXT).multiBuild(story)
        audit(NEXT)
        NEXT.replace(OUTPUT)
        print(f"OUTPUT {OUTPUT}")
    finally:
        NEXT.unlink(missing_ok=True)


def source_free_pdf_issues(doc: pymupdf.Document) -> list[str]:
    text_parts = [page.get_text(sort=True) for page in doc]
    text_parts.extend(item[1] for item in doc.get_toc())
    text_parts.extend(str(value) for value in doc.metadata.values() if value)
    issues = source_free_issues("\n".join(text_parts))
    references = {url.rstrip("/") for url in reference_urls()}
    for page_number, page in enumerate(doc, 1):
        for link in page.get_links():
            if link["kind"] == pymupdf.LINK_URI and link.get("uri", "").rstrip("/") in references:
                issues.append(f"reference hyperlink on page {page_number}")
    return issues


def audit(path: Path) -> None:
    with pymupdf.open(path) as doc:
        audit_document(doc)


def audit_document(doc: pymupdf.Document) -> None:
    if len(doc) < 8:
        raise RuntimeError("Candidate quá ngắn so với nội dung bản thảo")
    text = "\n".join(page.get_text() for page in doc)
    for phrase in ("CẨM NANG", "MỤC LỤC", "Từ chương trình đến tiến trình",
                   "C1.1.", "C2.1.", "C3.1.", "Lời giải", "Chưa phải bản phát hành"):
        if phrase not in text:
            raise RuntimeError(f"Thiếu nội dung PDF: {phrase}")
    toc_entries = doc.get_toc()
    if len(toc_entries) < 7:
        raise RuntimeError("Bookmark chưa đủ")
    if toc_entries[0][2] != 3 or any(a[2] > b[2] for a, b in zip(toc_entries, toc_entries[1:])):
        raise RuntimeError(f"Bookmark trỏ sai trang hoặc sai thứ tự: {toc_entries}")
    issues = source_free_pdf_issues(doc)
    if issues:
        raise RuntimeError(f"Nguồn tham khảo lọt vào PDF: {issues}")
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
    fonts = {font[0]: font[3] for page in doc for font in page.get_fonts(full=True)}
    font_names = set(fonts.values())
    if not any("TimesNewRoman" in name.replace(" ", "") for name in font_names):
        raise RuntimeError(f"Times New Roman chưa được nhúng: {font_names}")
    for xref, name in fonts.items():
        if ("TimesNewRoman" in name or "Consolas" in name) and not doc.extract_font(xref)[3]:
            raise RuntimeError(f"Font chưa được nhúng: {name}")
    pages = len(doc)
    bookmarks = len(toc_entries)
    print(f"CANDIDATE_OK pages={pages} bookmarks={bookmarks} source_leaks=0")
    print(f"FONTS {sorted(font_names)}")


if __name__ == "__main__":
    build()
