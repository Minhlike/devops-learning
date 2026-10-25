"""Build and audit a limited DevOps textbook candidate; never publish final here."""

from __future__ import annotations

import html
import hashlib
import json
import csv
import re
from pathlib import Path

import pymupdf
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    BaseDocTemplate, Flowable, Frame, PageBreak, PageTemplate, Paragraph,
    Preformatted, Spacer, LongTable, TableStyle, KeepTogether,
)
from reportlab.platypus.tableofcontents import TableOfContents
try:
    from .p13_publication import figure_story
    from .science_figures import FIGURES, figure_story as mechanism_figure_story
except ImportError:  # direct execution: python giaotrinh/scripts/build.py
    from p13_publication import figure_story
    from science_figures import FIGURES, figure_story as mechanism_figure_story


ROOT = Path(__file__).resolve().parents[1]
COVER_ART = ROOT / "assets" / "cover_datacenter_bw.png"
READER_TITLES = json.loads((ROOT / "manuscript" / "reader_titles.json").read_text(encoding="utf-8"))
EXERCISE_TITLES = json.loads((ROOT / "manuscript" / "exercise_titles.json").read_text(encoding="utf-8"))
OUTPUT = ROOT / "Cam_nang_devops.candidate.pdf"
NEXT = ROOT / "Cam_nang_devops.candidate.next.pdf"
FONT_DIR = Path("C:/Windows/Fonts")
PAGE_W, PAGE_H = A4
LEFT = RIGHT = 62
TOP = 65
BOTTOM = 62
URL_RE = re.compile(r"https?://[^\s|)]+")
MARKER_RE = re.compile(r"\[[A-Z]{1,3}\d+\]")
SOURCE_HEADING_RE = re.compile(
    r"(?i)\b(?:nguồn chương|tài liệu tham khảo|danh mục tài liệu|bibliography|references)\b"
)
REFERENCE_SIGNATURE_RE = re.compile(
    r"(?i)\b(?:RFC\s+\d{3,5}|Linux man-pages 6\.19|Operating Systems: Three Easy Pieces|source_map\.json|docs\.kernel\.org|man7\.org)\b"
)
XREF_RE = re.compile(r"\{\{xref:(P\d{2}(?:\.C\d{2})?(?:\.L\d{2})?)\}\}")
LEGACY_XREF_RE = re.compile(
    r"(?i)\b(?:chương\s+\d+(?:[–-]\d+)?|mục\s+\d+\.\d+(?:[–-]\d+)?|"
    r"bài\s+\d+\.\d+|hình\s+(?:\d+|[IVX]+)\.\d+(?:\.\d+)?|"
    r"bảng\s+\d+(?:\.\d+)?|phần\s+[IVX]+)\b"
)


def register_fonts() -> None:
    fonts = {
        "Body": "times.ttf",
        "BodyBold": "timesbd.ttf",
        "CoverBold": "arialbd.ttf",
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
        "h3": ParagraphStyle("h3", fontName="BodyBold", fontSize=11.8,
                             leading=16, spaceBefore=13, spaceAfter=9,
                             leftIndent=7, rightIndent=7, borderPadding=5,
                             backColor=colors.HexColor("#eeeeee"),
                             keepWithNext=True),
        "body": ParagraphStyle("body", fontName="Body", fontSize=11.7,
                               leading=16.8, alignment=TA_LEFT, spaceAfter=6.5),
        "p13body": ParagraphStyle("p13body", fontName="Body", fontSize=11.7,
                                  leading=17, alignment=TA_LEFT, spaceAfter=6.5),
        "answerbody": ParagraphStyle("answerbody", fontName="Body", fontSize=10.8,
                                     leading=15.5, alignment=TA_LEFT, spaceAfter=4,
                                     allowOrphans=0, allowWidows=0),
        "toc": ParagraphStyle("toc-title", fontName="BodyBold", fontSize=19,
                              leading=24, spaceAfter=20),
        "tocentry": ParagraphStyle("toc-entry", fontName="BodyBold", fontSize=10,
                                   leading=11, leftIndent=8, firstLineIndent=-8,
                                   keepWithNext=True),
        "tocchapter": ParagraphStyle("toc-chapter", fontName="Body", fontSize=9.5,
                                     leading=11, leftIndent=22, firstLineIndent=-8),
        "toclesson": ParagraphStyle("toc-lesson", fontName="Body", fontSize=9,
                                    leading=11, leftIndent=38, firstLineIndent=-8),
        "part_deck": ParagraphStyle("part-deck", fontName="BodyBold", fontSize=19,
                                    leading=25, alignment=TA_CENTER, spaceAfter=10),
        "part_intro": ParagraphStyle("part-intro", fontName="Body", fontSize=12,
                                     leading=19, spaceAfter=15),
        "part_route": ParagraphStyle("part-route", fontName="Body", fontSize=11,
                                     leading=15, textColor=colors.HexColor("#222222")),
        "exercise": ParagraphStyle("exercise", fontName="BodyBold", fontSize=11.5,
                                   leading=16, spaceBefore=12, spaceAfter=7,
                                   keepWithNext=True),
        "caption": ParagraphStyle("caption", fontName="Body", fontSize=9,
                                  leading=12, spaceBefore=4),
        "p13code": ParagraphStyle("p13code", fontName="Mono", fontSize=8,
                                  leading=11, leftIndent=6, rightIndent=6,
                                  backColor=colors.HexColor("#f5f5f5"),
                                  spaceBefore=5, spaceAfter=10),
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
                 styles: dict[str, ParagraphStyle], include_in_toc: bool = True):
        super().__init__(html.escape(text), styles[f"h{level}"])
        self.heading_text = text
        self.level = level
        self.bookmark_key = key
        self.include_in_toc = include_in_toc


def roman(number: int) -> str:
    symbols = ((10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"))
    result = ""
    for value, symbol in symbols:
        while number >= value:
            result += symbol
            number -= value
    return result


def publication_labels(tree: dict) -> tuple[dict[str, int], dict[str, str]]:
    """Keep stable architecture IDs separate from the labels printed for readers."""
    chapter_numbers: dict[str, int] = {}
    labels: dict[str, str] = {}
    valid = {"parts": set(), "chapters": set(), "lessons": set()}
    for part_index, part in enumerate(tree["parts"], 1):
        valid["parts"].add(part["id"])
        labels[part["id"]] = f"PHẦN {roman(part_index)} — {READER_TITLES['parts'].get(part['id'], part['title'])}"
        for chapter in part["chapters"]:
            chapter_id = chapter["id"]
            valid["chapters"].add(chapter_id)
            number = len(chapter_numbers) + 1
            chapter_numbers[chapter_id] = number
            labels[chapter_id] = f"Chương {number} — {READER_TITLES['chapters'][chapter_id]}"
            for lesson_index, lesson in enumerate(chapter["lessons"], 1):
                lesson_id = lesson["id"]
                valid["lessons"].add(lesson_id)
                title = READER_TITLES["lessons"].get(lesson_id, lesson["title"])
                labels[lesson_id] = f"Bài {number}.{lesson_index} — {title}"
    for kind, ids in valid.items():
        overrides = READER_TITLES[kind]
        if not set(overrides) <= ids or any(not value.strip() for value in overrides.values()):
            raise ValueError(f"Nhãn hiển thị {kind} sai ID hoặc rỗng")
    if set(READER_TITLES["chapters"]) != valid["chapters"]:
        raise ValueError("Thiếu nhãn Chương dành cho người đọc")
    return chapter_numbers, labels


def publication_exercises(tree: dict, manifest: dict) -> dict[str, str]:
    """Number exercises for readers without changing their stable ledger IDs."""
    expected_ids = {qa["publication_id"] for row in manifest["lessons"].values() for qa in row["qa"]}
    if set(EXERCISE_TITLES) != expected_ids or any(not value.strip() for value in EXERCISE_TITLES.values()):
        raise ValueError("Tên bài tập dành cho người đọc thiếu, thừa hoặc rỗng")
    chapter_numbers, _ = publication_labels(tree)
    labels: dict[str, str] = {}
    for part in tree["parts"]:
        for chapter in part["chapters"]:
            number = chapter_numbers[chapter["id"]]
            exercise_number = 0
            for lesson in chapter["lessons"]:
                for qa in manifest["lessons"][lesson["id"]]["qa"]:
                    exercise_number += 1
                    identifier = qa["publication_id"]
                    if identifier in labels:
                        raise ValueError(f"Trùng mã bài tập nội bộ: {identifier}")
                    labels[identifier] = f"Bài tập {number}.{exercise_number} — {EXERCISE_TITLES[identifier]}"
    return labels


class PartPlate(Flowable):
    """A quiet monochrome part opener generated from the approved chapter tree."""

    def __init__(self, part: dict, chapters: list, styles: dict[str, ParagraphStyle],
                 labels: dict[str, str]):
        super().__init__()
        self.part = part
        self.chapters = chapters
        self.styles = styles
        self.labels = labels
        self.width = PAGE_W - LEFT - RIGHT
        self.height = max(315, 140 + 43 * len(chapters))

    def draw(self):
        c = self.canv
        c.saveState()
        ink = colors.HexColor("#222222")
        gray = colors.HexColor("#777777")
        c.setFillColor(ink)
        c.rect(0, self.height - 9, self.width, 9, fill=1, stroke=0)
        c.setFont("BodyBold", 55)
        c.drawString(9, self.height - 81, roman(int(self.part['id'][1:])))
        c.setStrokeColor(gray)
        c.setLineWidth(0.6)
        c.line(104, self.height - 65, self.width, self.height - 65)
        c.setFont("BodyBold", 10)
        c.drawString(110, self.height - 53, "LỘ TRÌNH PHẦN")
        y = self.height - 112
        for index, (chapter, _) in enumerate(self.chapters, 1):
            c.setFillColor(ink)
            c.circle(18, y + 6, 3.2, fill=1, stroke=0)
            c.setStrokeColor(gray)
            if index < len(self.chapters):
                c.line(18, y + 3, 18, y - 35)
            label = self.labels[chapter["id"]]
            paragraph = Paragraph(paragraph_markup(label), self.styles["part_route"])
            _, ph = paragraph.wrap(self.width - 44, 50)
            paragraph.drawOn(c, 34, y - ph + 10)
            y -= max(43, ph + 14)
        c.setStrokeColor(gray)
        c.line(0, 5, self.width, 5)
        c.restoreState()


class CoverPage(Flowable):
    """Minimal white cover with live type and a monochrome photograph."""

    def __init__(self):
        super().__init__()
        self.width = PAGE_W - LEFT - RIGHT
        self.height = PAGE_H - TOP - BOTTOM - 2

    def draw(self):
        c = self.canv
        c.saveState()
        draw_cover_photo(c, self.width - 225, 0, 225, self.height)
        c.setFillColor(colors.black)
        c.setFont("CoverBold", 30)
        c.drawString(0, 450, "CẨM NANG")
        c.drawString(0, 411, "NGÀNH")
        c.setFont("CoverBold", 42)
        c.drawString(0, 352, "DEVOPS")
        c.restoreState()


def draw_cover_photo(canvas, x: float, y: float, width: float, height: float) -> None:
    """Crop at render time without altering the source photograph."""
    if not COVER_ART.is_file():
        raise FileNotFoundError(f"Thiếu ảnh bìa: {COVER_ART}")
    image = ImageReader(str(COVER_ART))
    image_width, image_height = image.getSize()
    scaled_width = height * image_width / image_height
    canvas.saveState()
    clip = canvas.beginPath()
    clip.rect(x, y, width, height)
    canvas.clipPath(clip, stroke=0, fill=0)
    canvas.drawImage(image, x - (scaled_width - width) / 2, y,
                     width=scaled_width, height=height)
    canvas.restoreState()


class BackCoverPage(CoverPage):
    """Reader-facing back cover, without status text or page furniture."""

    def draw(self):
        c = self.canv
        c._back_cover = True
        c.saveState()
        draw_cover_photo(c, 0, 0, 225, self.height)
        x = 250
        c.setFillColor(colors.black)
        c.setFont("CoverBold", 17)
        c.drawString(x, 493, "HIỂU HỆ THỐNG.")
        c.drawString(x, 466, "VẬN HÀNH")
        c.drawString(x, 439, "CÓ CHỨNG CỨ.")
        c.setFont("Body", 12)
        for line, y in (
            ("Từ mã nguồn đến hạ tầng,", 359),
            ("triển khai, quan sát và phục hồi,", 340),
            ("cuốn sách đi từ cơ chế đến", 321),
            ("quyết định vận hành có thể kiểm chứng.", 302),
        ):
            c.drawString(x, y, line)
        c.restoreState()


class Book(BaseDocTemplate):
    def __init__(self, path: Path):
        super().__init__(str(path), pagesize=A4, leftMargin=LEFT,
                         rightMargin=RIGHT, topMargin=TOP, bottomMargin=BOTTOM,
                         title="Cẩm nang ngành DevOps")
        frame = Frame(LEFT, BOTTOM, PAGE_W - LEFT - RIGHT,
                      PAGE_H - TOP - BOTTOM, leftPadding=0, rightPadding=0,
                      topPadding=0, bottomPadding=0)
        self.running_part = None
        self.running_chapter = None
        self.part_opening_page = None
        self.addPageTemplates(PageTemplate(id="normal", frames=[frame],
                                           onPageEnd=self.page_decoration))

    def beforeDocument(self):
        # multiBuild renders the TOC more than once using the same template.
        # Running heads must never inherit the final section of an earlier pass.
        self.running_part = None
        self.running_chapter = None
        self.part_opening_page = None

    @staticmethod
    def page_decoration(canvas, doc):
        if doc.page == 1 or getattr(canvas, "_back_cover", False):
            return
        canvas.saveState()
        if not doc.running_part and doc.page > 2:
            canvas.setFont("BodyBold", 8.5)
            canvas.drawString(LEFT, PAGE_H - 39, "MỤC LỤC · TIẾP")
            canvas.setStrokeColor(colors.HexColor("#999999"))
            canvas.line(LEFT, PAGE_H - 47, PAGE_W - RIGHT, PAGE_H - 47)
        if doc.running_part and doc.page != doc.part_opening_page:
            canvas.setFont("BodyBold", 8.5)
            canvas.drawString(LEFT, PAGE_H - 39, "CẨM NANG NGÀNH DEVOPS")
            canvas.setFont("Body", 8.5)
            section = doc.running_chapter or doc.running_part
            canvas.drawRightString(PAGE_W - RIGHT, PAGE_H - 39, section)
            canvas.setStrokeColor(colors.HexColor("#999999"))
            canvas.line(LEFT, PAGE_H - 47, PAGE_W - RIGHT, PAGE_H - 47)
        canvas.setStrokeColor(colors.HexColor("#999999"))
        canvas.setLineWidth(0.4)
        canvas.line(LEFT, 45, PAGE_W - RIGHT, 45)
        canvas.setFont("Body", 9)
        canvas.drawString(LEFT, 32, "CẨM NANG NGÀNH DEVOPS")
        canvas.drawRightString(PAGE_W - RIGHT, 32, str(doc.page))
        canvas.restoreState()

    def afterFlowable(self, flowable: Flowable):
        if not isinstance(flowable, Heading):
            return
        if flowable.level == 1 and flowable.bookmark_key.startswith("P"):
            self.running_part = flowable.heading_text.split(" — ", 1)[0]
            self.running_chapter = None
            self.part_opening_page = self.page
        elif flowable.bookmark_key == "answers":
            self.running_part = "LỜI GIẢI"
            self.running_chapter = None
            self.part_opening_page = None
        elif flowable.level == 2 and flowable.bookmark_key.endswith(".answers"):
            # Several answer groups can share one page; a page-end callback
            # must not label the whole page with its final group.
            self.running_chapter = None
        elif flowable.level == 2 and flowable.bookmark_key.startswith("P"):
            self.running_chapter = flowable.heading_text.split(" — ", 1)[0]
        key = flowable.bookmark_key
        self.canv.bookmarkPage(key)
        self.canv.addOutlineEntry(flowable.heading_text, key,
                                  level=flowable.level - 1, closed=False)
        if flowable.include_in_toc:
            self.notify("TOCEntry", (flowable.level - 1,
                                      flowable.heading_text, self.page, key))


def short_reference(target: str, labels: dict[str, str]) -> str:
    if target not in labels:
        raise ValueError(f"Tham chiếu không có đích: {target}")
    short = labels[target].split(" — ", 1)[0]
    return "Phần " + short[5:] if short.startswith("PHẦN ") else short


def expand_references(text: str, labels: dict[str, str]) -> str:
    result = XREF_RE.sub(lambda match: short_reference(match.group(1), labels), text)
    if "{{xref:" in result:
        raise ValueError(f"Tham chiếu sai cú pháp: {result[:120]}")
    return result


def validate_cross_references(tree: dict, manifest: dict,
                              contract: dict | None = None) -> int:
    """Pin each semantic destination to its source so a valid but wrong ID fails."""
    if contract is None:
        contract = json.loads((ROOT / "manuscript" / "cross_references.json").read_text(encoding="utf-8"))
    if contract.get("schema_version") != 1:
        raise ValueError("Hợp đồng tham chiếu thiếu phiên bản")
    _, labels = publication_labels(tree)
    found: dict[str, list[str]] = {}
    for lid, row in manifest["lessons"].items():
        body = (ROOT / row["content"]).read_text(encoding="utf-8")
        source = f"lesson:{lid}"
        targets = XREF_RE.findall(body)
        if "{{xref:" in XREF_RE.sub("", body):
            raise ValueError(f"Tham chiếu sai cú pháp trong {source}")
        if targets:
            found[source] = targets
        if LEGACY_XREF_RE.search(body):
            raise ValueError(f"Tham chiếu số cũ còn trong {source}")
        for qa in row["qa"]:
            for field in ("question", "answer"):
                source = f"qa:{qa['publication_id']}:{field}"
                body = qa[field]
                targets = XREF_RE.findall(body)
                if "{{xref:" in XREF_RE.sub("", body):
                    raise ValueError(f"Tham chiếu sai cú pháp trong {source}")
                if targets:
                    found[source] = targets
                if LEGACY_XREF_RE.search(body):
                    raise ValueError(f"Tham chiếu số cũ còn trong {source}")
    expected = contract["sources"]
    if found != expected:
        raise ValueError(f"Tham chiếu sai đích hoặc sai chủ đề: {set(found) ^ set(expected)}")
    for source, targets in found.items():
        for target in targets:
            if target not in labels:
                raise ValueError(f"Tham chiếu không có đích: {source} -> {target}")
    return sum(map(len, found.values()))


def reference_contexts(manifest: dict, labels: dict[str, str]):
    """Text around each rendered reference, for rejecting a stale PDF."""
    for lid, row in manifest["lessons"].items():
        bodies = [(lid, (ROOT / row["content"]).read_text(encoding="utf-8"))]
        bodies.extend((qa["publication_id"] + ":" + field, qa[field])
                      for qa in row["qa"] for field in ("question", "answer"))
        for source, body in bodies:
            for match in XREF_RE.finditer(body):
                preceding_break = body.rfind("\n\n", 0, match.start())
                paragraph_start = 0 if preceding_break < 0 else preceding_break + 2
                paragraph_end = body.find("\n\n", match.end())
                if paragraph_end < 0:
                    paragraph_end = len(body)
                paragraph = body[paragraph_start:paragraph_end]
                expanded = expand_references(paragraph, labels)
                start = len(expand_references(body[paragraph_start:match.start()], labels))
                end = start + len(short_reference(match.group(1), labels))
                excerpt = expanded[max(0, start - 24):end + 24]
                plain = re.sub(r"[`*]", "", excerpt)
                yield source, re.sub(r"\s+", " ", plain)


def paragraph_markup(text: str, labels: dict[str, str] | None = None) -> str:
    if labels is not None:
        text = expand_references(text, labels)
    elif "{{xref:" in text:
        raise ValueError("Thiếu cây nhãn để dựng tham chiếu")
    escaped = html.escape(text)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escaped)
    escaped = re.sub(r"`([^`]+)`", r'<font name="Mono">\1</font>', escaped)
    return escaped


def reference_urls() -> set[str]:
    registry = json.loads((ROOT / "source_map.json").read_text(encoding="utf-8"))
    markdown = (ROOT / "references.md").read_text(encoding="utf-8")
    urls = {source["url"] for source in registry["sources"].values()}
    urls.update(match.group(0).rstrip(".,;") for match in URL_RE.finditer(markdown))
    for ledger in sorted((ROOT / "authoring" / "P13").glob("C*/claims.csv")):
        with ledger.open(encoding="utf-8", newline="") as stream:
            urls.update(row["source_url"] for row in csv.DictReader(stream))
    wave2 = json.loads((ROOT / "manuscript" / "wave2_evidence.json").read_text(encoding="utf-8"))
    urls.update(source["url"] for source in wave2["sources"].values())
    toolchain = json.loads((ROOT / "manuscript" / "P16" / "source_map.json").read_text(encoding="utf-8"))
    urls.update(source["url"] for source in toolchain["sources"].values())
    return urls


def check_source_map(registry: dict | None = None) -> None:
    if registry is None:
        registry = json.loads((ROOT / "source_map.json").read_text(encoding="utf-8"))
    sources = registry["sources"]
    locked = json.loads((ROOT / "source_ids.lock.json").read_text(encoding="utf-8"))["urls"]
    if set(sources) != set(locked):
        raise ValueError("Mã nguồn và source_ids.lock.json không khớp")
    for source_id, source in sources.items():
        if source.get("url") != locked[source_id]:
            raise ValueError(f"Định danh nguồn đã đổi URL: {source_id}")
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


def read_markdown(path: Path, styles: dict[str, ParagraphStyle],
                  exercise_labels: dict[str, str] | None = None,
                  xref_labels: dict[str, str] | None = None) -> list[Flowable]:
    if not path.is_file():
        raise FileNotFoundError(path)
    raw = path.read_text(encoding="utf-8")
    # Fence bodies may contain blank lines. Keep them as one render unit.
    chunks = re.split(r"(?ms)(^```[^\n]*\n.*?^```\s*$)", raw.strip())
    blocks = [piece for chunk in chunks for piece in
              ([chunk] if chunk.startswith("```") else re.split(r"\n\s*\n", chunk)) if piece.strip()]
    issues = source_free_issues(raw)
    if issues:
        raise ValueError(f"Nguồn tham khảo lọt vào bản thảo PDF {path}: {issues}")
    story: list[Flowable] = []
    for index, block in enumerate(blocks):
        block = block.strip()
        key = "section-" + hashlib.sha1(f"{path.name}:{index}".encode("utf-8")).hexdigest()[:12]
        if block.startswith("{{figure:") and block.endswith("}}"):
            figure_id = block[9:-2]
            story.append(figure_story(figure_id, styles) if figure_id.startswith("P13.C")
                         else mechanism_figure_story(figure_id, styles))
        elif block.startswith("```"):
            lines = block.splitlines()
            if len(lines) < 2 or not lines[-1].startswith("```"):
                raise ValueError(f"Code fence chưa đóng: {path}")
            code_lines = lines[1:-1]
            for line in code_lines:
                if pdfmetrics.stringWidth(line, "Mono", 8) > PAGE_W - LEFT - RIGHT - 18:
                    raise ValueError(f"Dòng code quá rộng: {path}: {line}")
            for start in range(0, len(code_lines), 42):
                story.append(Preformatted("\n".join(code_lines[start:start + 42]), styles["p13code"]))
        elif block.startswith("### Bài tập "):
            heading, _, rest = block.partition("\n")
            identifier = heading[len("### Bài tập "):].strip()
            if exercise_labels is not None:
                if identifier not in exercise_labels:
                    raise ValueError(f"Bài tập trong bản thảo chưa có tên đọc: {identifier}")
                heading = exercise_labels[identifier]
            else:
                heading = heading[4:]
            story.append(Paragraph(paragraph_markup(heading), styles["exercise"]))
            if rest.strip():
                story.append(Paragraph(paragraph_markup(" ".join(rest.splitlines()), xref_labels), styles["body"]))
        elif block.startswith("# "):
            story.append(Heading(block[2:].strip(), 1, key, styles))
        elif block.startswith("## "):
            story.append(Heading(block[3:].strip(), 2, key, styles,
                                 include_in_toc=path.name != "answers.md"))
        elif block.startswith("{{code:") and block.endswith("}}"):
            code_path = (ROOT / block[7:-2]).resolve()
            if not code_path.is_relative_to(ROOT / "examples") or not code_path.is_file():
                raise ValueError(f"Code example ngoài phạm vi hoặc thiếu: {code_path}")
            code = code_path.read_text(encoding="utf-8").rstrip()
            for line in code.splitlines():
                if pdfmetrics.stringWidth(line, "Mono", 8.7) > PAGE_W - LEFT - RIGHT - 18:
                    raise ValueError(f"Dòng code quá rộng: {code_path}: {line}")
            # A single oversize Preformatted can be clipped without a build error.
            # Keep each chunk within the printable height and allow page breaks.
            lines = code.splitlines()
            for start in range(0, len(lines), 42):
                story.append(KeepTogether([
                    Preformatted("\n".join(lines[start:start + 42]), styles["code"])
                ]))
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
            story.append(Paragraph(paragraph_markup(paragraph, xref_labels), styles["body"]))
    return story


def load_manuscript(tree: dict | None = None, manifest: dict | None = None) -> tuple[dict, dict]:
    if tree is None:
        tree = json.loads((ROOT / "architecture" / "knowledge_tree.json").read_text(encoding="utf-8"))
    if manifest is None:
        manifest = json.loads((ROOT / "manuscript" / "manifest.json").read_text(encoding="utf-8"))
    lessons = {}
    chapter_ids = set()
    part_ids = set()
    for part in tree["parts"]:
        if part["id"] in part_ids:
            raise ValueError(f"Trùng Phần: {part['id']}")
        part_ids.add(part["id"])
        for chapter in part["chapters"]:
            cid = chapter["id"]
            if cid in chapter_ids or chapter["part"] != part["id"] or not cid.startswith(part["id"] + "."):
                raise ValueError(f"Chương trùng hoặc sai parent: {cid}")
            chapter_ids.add(cid)
            for lesson in chapter["lessons"]:
                lid = lesson["id"]
                if lid in lessons or lesson["parent"] != cid or not lid.startswith(cid + "."):
                    raise ValueError(f"Bài trùng hoặc sai parent: {lid}")
                lessons[lid] = lesson
    if len(part_ids) != 16 or len(chapter_ids) != 64 or len(lessons) != 202:
        raise ValueError("Cây kiến thức không còn đủ 16/64/202")
    if "P15.C04" in chapter_ids or any(lid.startswith("P15.C04.") for lid in lessons):
        raise ValueError("Chương cũ P15.C04 còn trong bản xuất bản")
    if set(manifest["lessons"]) != set(lessons):
        raise ValueError("Manifest thiếu hoặc thừa bài so với cây đã duyệt")
    for lid, row in manifest["lessons"].items():
        if row["parent"] != lessons[lid]["parent"] or row["prerequisites"] != lessons[lid]["prerequisites"]:
            raise ValueError(f"Metadata parent hoặc tiên quyết sai: {lid}")
        if row["status"] not in ("migrated_draft", "migration_fragment", "pending_authorship", "reviewed"):
            raise ValueError(f"Trạng thái bài sai: {lid}")
        if row["status"] == "reviewed" and row["verification"] not in (
            "source_reviewed_wave2", "reviewed_p13_publication_contract",
            "reviewed_editorial_evidence", "author_verified_p16",
        ):
            raise ValueError(f"Bài được đánh dấu reviewed nhưng thiếu hợp đồng kiểm chứng: {lid}")
        if row["verification"] == "reviewed_p13_publication_contract" and not lid.startswith("P13."):
            raise ValueError(f"Hợp đồng Phần XIII gắn sai bài: {lid}")
        if row["content"]:
            path = (ROOT / row["content"]).resolve()
            if not path.is_relative_to(ROOT / "manuscript") or not path.is_file():
                raise ValueError(f"Bài trỏ sai tệp: {lid}")
            digest = hashlib.sha256(path.read_text(encoding="utf-8").strip().encode("utf-8")).hexdigest()
            if digest != row["sha256"]:
                raise ValueError(f"Bài đã đổi mà manifest chưa duyệt: {lid}")
            if row["status"] in ("migrated_draft", "reviewed") and len(path.read_text(encoding="utf-8").split()) < 100:
                raise ValueError(f"Bài quá ngắn để tuyên bố có nội dung: {lid}")
        elif row["status"] != "pending_authorship":
            raise ValueError(f"Bài hoàn thành nhưng thiếu nội dung: {lid}")
    check_migration_evidence(manifest)
    check_wave2_evidence(manifest)
    check_editorial_evidence(manifest)
    check_p16_evidence(manifest)
    return tree, manifest


def check_p16_evidence(manifest: dict, data: dict | None = None) -> None:
    """Keep final-part sources separate from the frozen legacy map."""
    if data is None:
        data = json.loads((ROOT / "manuscript/P16/source_map.json").read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or not data.get("checked_on"):
        raise ValueError("P16 thiếu ngày hoặc schema nguồn")
    sources = data["sources"]
    old = json.loads((ROOT / "source_ids.lock.json").read_text(encoding="utf-8"))["urls"]
    if set(sources) & set(old):
        raise ValueError("P16 tái sử dụng mã nguồn cũ")
    historical = json.loads((ROOT / "architecture/history_p15_c04/source_map.json").read_text(encoding="utf-8"))["sources"]
    locked = json.loads((ROOT / "manuscript/P16/source_ids.lock.json").read_text(encoding="utf-8"))["urls"]
    if {sid: source["url"] for sid, source in sources.items()} != locked:
        raise ValueError("P16 đổi ID hoặc URL nguồn đã khóa")
    if any(sources.get(sid, {}).get("url") != source["url"]
           for sid, source in historical.items()):
        raise ValueError("P16 đổi nguồn lịch sử TC-01..TC-09")
    for sid, source in sources.items():
        if not all(source.get(key) for key in ("url", "version", "evidence", "scope")):
            raise ValueError(f"Nguồn P16 thiếu metadata: {sid}")
    claims_by_lesson: dict[str, list[dict]] = {}
    for claim in data["claims"]:
        lid = claim["lesson"]
        if lid not in manifest["lessons"] or not lid.startswith("P16.C"):
            raise ValueError(f"Claim P16 sai bài: {lid}")
        body = (ROOT / manifest["lessons"][lid]["content"]).read_text(encoding="utf-8")
        if not claim.get("anchor") or claim["anchor"] not in body:
            raise ValueError(f"Claim P16 mất neo: {lid}")
        if not claim.get("sources") or not set(claim["sources"]) <= set(sources):
            raise ValueError(f"Claim P16 thiếu nguồn: {lid}")
        if not claim.get("verification"):
            raise ValueError(f"Claim P16 thiếu phạm vi đối chiếu: {lid}")
        claims_by_lesson.setdefault(lid, []).append(claim)
    for lid, row in manifest["lessons"].items():
        if not lid.startswith("P16.C"):
            continue
        if row["status"] != "reviewed" or row["verification"] != "author_verified_p16":
            raise ValueError(f"Bài P16 thiếu trạng thái tác giả kiểm: {lid}")
        actual = sorted({sid for claim in claims_by_lesson.get(lid, []) for sid in claim["sources"]})
        if row["source_ids"] != actual:
            raise ValueError(f"Nguồn P16 sai bài: {lid}")


def check_migration_evidence(manifest: dict) -> None:
    with (ROOT / "architecture" / "evidence_ownership.csv").open(
            encoding="utf-8-sig", newline="") as stream:
        evidence = list(csv.DictReader(stream))
    if len(evidence) != 369 or len({row["old_id"] for row in evidence}) != 369:
        raise ValueError("Ledger claim/ví dụ/bài tập không đủ hoặc trùng")
    evidence_by_id = {row["old_id"]: row for row in evidence}
    expected = {lid: {"claim_ids": [], "examples": [], "qa": []}
                for lid in manifest["lessons"]}
    for row in evidence:
        owner = row["primary_lesson_id"]
        if owner not in expected:
            raise ValueError(f"Chủ chứng cứ ngoài cây: {owner}")
        kind = row["kind"]
        field = {"claim": "claim_ids", "example": "examples", "exercise_answer": "qa"}[kind]
        expected[owner][field].append(row["old_id"])
        if kind in ("claim", "example"):
            path = manifest["lessons"][owner]["content"]
            body = (ROOT / path).read_text(encoding="utf-8") if path else ""
            anchor = row["old_anchor_or_title"] if kind == "claim" else "{{code:" + row["old_id"] + "}}"
            if anchor not in body:
                raise ValueError(f"Mất claim hoặc ví dụ tại chủ bài: {row['old_id']}")
    # A split claim belongs in its selected lesson exactly once. Keeping the
    # original sentence in the paragraph owner makes migration duplicate prose.
    with (ROOT / "architecture" / "legacy_content_units.csv").open(
            encoding="utf-8-sig", newline="") as stream:
        for unit in csv.DictReader(stream):
            primary = manifest["lessons"][unit["primary_lesson_id"]]
            body = (ROOT / primary["content"]).read_text(encoding="utf-8")
            for moved in json.loads(unit["extract_to_other_owners"]):
                match = evidence_by_id[moved["old_id"]]
                if match["old_anchor_or_title"] in body:
                    raise ValueError(f"Claim đã tách vẫn lặp ở bài gốc: {moved['old_id']}")
    for lid, expected_row in expected.items():
        actual = manifest["lessons"][lid]
        for field in ("claim_ids", "examples"):
            if actual[field] != expected_row[field]:
                raise ValueError(f"Mất hoặc đổi chủ {field}: {lid}")
        old_qa = [] if lid.startswith("P13.") else [item["id"] for item in actual["qa"]
                                                   if item["id"] in expected_row["qa"]]
        if old_qa != expected_row["qa"]:
            raise ValueError(f"Mất cặp đề đáp án: {lid}")
    p13_qa = [qa["id"] for lid, row in manifest["lessons"].items()
              if lid.startswith("P13.") for qa in row["qa"]]
    if sorted(p13_qa) != sorted(f"C13.{i}" for i in range(1, 13)):
        raise ValueError("Mất bài tập hoặc đáp án Phần XIII")
    published_ids = [qa.get("publication_id") for row in manifest["lessons"].values() for qa in row["qa"]]
    if len(published_ids) < 91 or any(not identifier for identifier in published_ids) or len(set(published_ids)) != len(published_ids):
        raise ValueError("Mã bài tập xuất bản thiếu hoặc trùng")


def check_wave2_evidence(manifest: dict, ledger: dict | None = None) -> None:
    if ledger is None:
        ledger = json.loads((ROOT / "manuscript" / "wave2_evidence.json").read_text(encoding="utf-8"))
    if ledger.get("schema_version") != 1 or not ledger.get("checked_on"):
        raise ValueError("Ledger Đợt 2 thiếu phiên bản hoặc ngày kiểm")
    locked = json.loads((ROOT / "manuscript" / "wave2_source_ids.lock.json").read_text(
        encoding="utf-8"))["urls"]
    if {sid: source.get("url") for sid, source in ledger["sources"].items()} != locked:
        raise ValueError("Nguồn Đợt 2 đã đổi ID hoặc URL khóa")
    old_sources = json.loads((ROOT / "source_map.json").read_text(encoding="utf-8"))["sources"]
    sources = dict(old_sources)
    for sid, source in ledger["sources"].items():
        if sid in sources or not all(source.get(k) for k in ("type", "version", "url")):
            raise ValueError(f"Nguồn Đợt 2 trùng mã hoặc thiếu metadata: {sid}")
        sources[sid] = source
    for lid, evidence in ledger["lessons"].items():
        if lid not in manifest["lessons"]:
            raise ValueError(f"Ledger Đợt 2 trỏ ngoài cây: {lid}")
        row = manifest["lessons"][lid]
        if row["status"] != "reviewed" or row["verification"] != "source_reviewed_wave2":
            raise ValueError(f"Bài Đợt 2 chưa có trạng thái kiểm chứng phù hợp: {lid}")
        body = (ROOT / row["content"]).read_text(encoding="utf-8")
        if not evidence.get("claims") or not evidence.get("qa"):
            raise ValueError(f"Bài Đợt 2 thiếu claim hoặc bài tập: {lid}")
        for claim in evidence["claims"]:
            if not claim.get("anchor") or claim["anchor"] not in body:
                raise ValueError(f"Claim Đợt 2 không neo vào bài: {lid}")
            if not claim.get("sources") or any(sid not in sources for sid in claim["sources"]):
                raise ValueError(f"Claim Đợt 2 thiếu nguồn: {lid}")
            if not all(claim.get(k) for k in ("source_location", "support", "limits")):
                raise ValueError(f"Claim Đợt 2 thiếu biên bản ngữ nghĩa: {lid}")
        if row["qa"][-len(evidence["qa"]):] != evidence["qa"]:
            raise ValueError(f"Bài tập Đợt 2 không khớp ledger: {lid}")
        if row["source_ids"] != sorted({sid for claim in evidence["claims"]
                                         for sid in claim["sources"]}):
            raise ValueError(f"Nguồn bài Đợt 2 không khớp ledger: {lid}")
    for lid, row in manifest["lessons"].items():
        if row["verification"] == "source_reviewed_wave2" and lid not in ledger["lessons"]:
            raise ValueError(f"Bài Đợt 2 thiếu ledger: {lid}")


def check_editorial_evidence(manifest: dict, ledger: dict | None = None) -> None:
    """Require an anchored, versioned review before graduating inherited prose."""
    if ledger is None:
        ledger = json.loads((ROOT / "manuscript" / "editorial_evidence.json").read_text(
            encoding="utf-8"))
    if ledger.get("schema_version") != 1 or not ledger.get("checked_on"):
        raise ValueError("Biên bản biên tập thiếu phiên bản hoặc ngày kiểm")
    old = json.loads((ROOT / "source_map.json").read_text(encoding="utf-8"))["sources"]
    wave2 = json.loads((ROOT / "manuscript" / "wave2_evidence.json").read_text(
        encoding="utf-8"))["sources"]
    sources = old | wave2
    for lid, review in ledger.get("lessons", {}).items():
        if lid not in manifest["lessons"]:
            raise ValueError(f"Biên bản biên tập trỏ ngoài cây: {lid}")
        row = manifest["lessons"][lid]
        if row["status"] != "reviewed" or row["verification"] != "reviewed_editorial_evidence":
            raise ValueError(f"Bài biên tập chưa có trạng thái kiểm chứng: {lid}")
        if review.get("content_sha256") != row["sha256"]:
            raise ValueError(f"Biên bản biên tập không khớp nội dung: {lid}")
        body = (ROOT / row["content"]).read_text(encoding="utf-8")
        checks = review.get("checks")
        if not isinstance(checks, list) or not checks or not review.get("editorial_decision"):
            raise ValueError(f"Biên bản biên tập thiếu đánh giá: {lid}")
        used = set()
        for check in checks:
            if check.get("anchor") not in body or not all(
                check.get(key) for key in ("kind", "support", "limits")):
                raise ValueError(f"Biên bản biên tập thiếu neo hoặc biên: {lid}")
            cited = check.get("sources", [])
            if check["kind"] == "documented" and not cited:
                raise ValueError(f"Claim tài liệu thiếu nguồn: {lid}")
            if check["kind"] not in ("documented", "derived", "inference"):
                raise ValueError(f"Loại bằng chứng không hợp lệ: {lid}")
            if any(sid not in sources for sid in cited):
                raise ValueError(f"Biên bản biên tập dùng nguồn không khai báo: {lid}")
            if cited and not check.get("source_location"):
                raise ValueError(f"Biên bản biên tập thiếu vị trí nguồn: {lid}")
            used.update(cited)
        if used != set(row["source_ids"]):
            raise ValueError(f"Nguồn bài không khớp biên bản biên tập: {lid}")
    for lid, row in manifest["lessons"].items():
        if row["verification"] == "reviewed_editorial_evidence" and lid not in ledger.get("lessons", {}):
            raise ValueError(f"Bài đã duyệt thiếu biên bản biên tập: {lid}")


def published_lessons(tree: dict, manifest: dict):
    for part in tree["parts"]:
        chapters = []
        for chapter in part["chapters"]:
            content = [lesson for lesson in chapter["lessons"] if
                       manifest["lessons"][lesson["id"]]["status"] in ("migrated_draft", "reviewed")]
            if content:
                chapters.append((chapter, content))
        if chapters:
            yield part, chapters


def build() -> None:
    check_source_map()
    register_fonts()
    tree, manifest = load_manuscript()
    chapter_numbers, labels = publication_labels(tree)
    validate_cross_references(tree, manifest)
    exercise_labels = publication_exercises(tree, manifest)
    publication = list(published_lessons(tree, manifest))
    count = sum(len(lessons) for _, chapters in publication for _, lessons in chapters)
    if count < 100:
        raise RuntimeError("Migration candidate thiếu phần lớn nội dung cũ")
    styles = style()
    toc = TableOfContents()
    toc.levelStyles = [styles["tocentry"], styles["tocchapter"]]
    story: list[Flowable] = [
        CoverPage(),
        PageBreak(),
        Paragraph("MỤC LỤC", styles["toc"]),
        toc,
        PageBreak(),
    ]
    for part, chapters in publication:
        story.append(Heading(labels[part["id"]], 1, part["id"], styles))
        story.append(Spacer(1, 28))
        story.append(Paragraph(paragraph_markup(part["central_question"]), styles["part_deck"]))
        story.append(Paragraph(paragraph_markup(part["mental_model"]), styles["part_intro"]))
        story.append(PartPlate(part, chapters, styles, labels))
        story.append(PageBreak())
        for chapter_index, (chapter, lessons) in enumerate(chapters):
            if chapter_index:
                story.append(PageBreak())
            story.append(Heading(labels[chapter["id"]], 2, chapter["id"], styles))
            story.append(Paragraph(paragraph_markup(chapter["objective"]), styles["body"]))
            for lesson in lessons:
                lid = lesson["id"]
                story.append(Heading(labels[lid], 3, lid, styles, include_in_toc=False))
                story.extend(read_markdown(ROOT / manifest["lessons"][lid]["content"], styles,
                                           exercise_labels, labels))
                for qa in manifest["lessons"][lid]["qa"]:
                    if lid.startswith("P13."):
                        continue  # Reviewed P13 questions are already inside the lesson.
                    story.append(Paragraph(paragraph_markup(exercise_labels[qa["publication_id"]]),
                                           styles["exercise"]))
                    story.append(Paragraph(paragraph_markup(qa["question"], labels), styles["body"]))
        story.append(PageBreak())
    story.append(Heading("Lời giải bài tập", 1, "answers", styles))
    for part, chapters in publication:
        for chapter, lessons in chapters:
            entries = [(lid["id"], qa) for lid in lessons for qa in manifest["lessons"][lid["id"]]["qa"]]
            if not entries:
                continue
            story.append(Heading(f"Đáp án chương {chapter_numbers[chapter['id']]} — {READER_TITLES['chapters'][chapter['id']]}", 2,
                                 f"{chapter['id']}.answers", styles, include_in_toc=False))
            for _, qa in entries:
                label = exercise_labels[qa["publication_id"]]
                story.append(Paragraph(f"<b>{html.escape(label)}</b><br/>{paragraph_markup(qa['answer'], labels)}",
                                       styles["answerbody"]))
    story.extend((PageBreak(), BackCoverPage()))
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
    normalized_text = re.sub(r"\s+", " ", text)
    cover_text = doc[0].get_text()
    if not all(word in cover_text for word in ("CẨM NANG", "NGÀNH", "DEVOPS")):
        raise RuntimeError("Tiêu đề bìa thiếu hoặc không trích xuất được")
    if "VẬN HÀNH" not in doc[-1].get_text() or "BẢN ĐỌC THỬ" in doc[-1].get_text():
        raise RuntimeError("Bìa sau thiếu hoặc còn thông tin quản lý nội bộ")
    if any(word in cover_text.casefold() for word in
           ("bản thảo", "candidate", "bản đọc thử", "chưa phải", "/178")):
        raise RuntimeError("Thông tin nội bộ lọt lên bìa")
    for phrase in ("CẨM NANG", "MỤC LỤC", "Lời giải"):
        if phrase not in text:
            raise RuntimeError(f"Thiếu nội dung PDF: {phrase}")
    tree, manifest = load_manuscript()
    _, labels = publication_labels(tree)
    exercise_labels = publication_exercises(tree, manifest)
    expected = []
    for part, chapters in published_lessons(tree, manifest):
        expected.append((1, labels[part["id"]]))
        for chapter, lessons in chapters:
            expected.append((2, labels[chapter["id"]]))
            expected.extend((3, labels[lesson["id"]]) for lesson in lessons)
            for lesson in lessons:
                for qa in manifest["lessons"][lesson["id"]]["qa"]:
                    display = exercise_labels[qa["publication_id"]]
                    if normalized_text.count(display) != 2:
                        raise RuntimeError(f"Thiếu bài tập hoặc lời giải: {display}")
    if re.search(r"\bP\d{2}\.C\d{2}\.L\d{2}\.Q\d{2}\b|\bC13\.\d+\b", text):
        raise RuntimeError("Mã bài tập nội bộ lọt vào PDF")
    for source, context in reference_contexts(manifest, labels):
        if context not in normalized_text:
            raise RuntimeError(f"Tham chiếu chưa cập nhật trong PDF: {source}: {context}")
    for figure in ("Hình XIII.1.1", "Hình XIII.2.1", "Hình XIII.3.1", "Hình XIII.4.1"):
        if figure not in text:
            raise RuntimeError(f"Thiếu hình đã duyệt: {figure}")
    for figure_id, (caption, _) in FIGURES.items():
        owners = [lid for lid, row in manifest["lessons"].items()
                  if f"{{{{figure:{figure_id}}}}}" in (ROOT / row["content"]).read_text(encoding="utf-8")]
        if len(owners) != 1 or len(re.findall(rf"\b{re.escape(figure_id)}\b", text)) != 1:
            raise RuntimeError(f"Thiếu hoặc lặp hình cơ chế {figure_id}")
        label = caption.split(" — ", 1)[0]
        pages = [page for page in doc if label in page.get_text()]
        if len(pages) != 1:
            raise RuntimeError(f"Thiếu hoặc lặp caption hình {figure_id}")
        caption_rect = pages[0].search_for(label)[0]
        panels = [drawing["rect"] for drawing in pages[0].get_drawings()
                  if drawing["rect"].width >= 450 and drawing["rect"].height >= 200
                  and 0 <= caption_rect.y0 - drawing["rect"].y1 <= 30]
        if len(panels) != 1:
            raise RuntimeError(f"Thiếu panel vector hình {figure_id}")
    toc_entries = doc.get_toc()
    actual = [(level, title) for level, title, _ in toc_entries[:len(expected)]]
    if actual != expected:
        raise RuntimeError(f"Sai nhãn/cấp/thứ tự bookmark: {actual[:8]} != {expected[:8]}")
    for level, title, page in toc_entries[:len(expected)]:
        page_text = re.sub(r"\s+", " ", doc[page - 1].get_text()) if 1 <= page <= len(doc) else ""
        if page < 3 or page > len(doc) or re.sub(r"\s+", " ", title) not in page_text:
            raise RuntimeError(f"Bookmark trỏ sai trang: {title} -> {page}")
        if level == 2 and title.startswith("Chương "):
            locations = doc[page - 1].search_for(title)
            if len(locations) != 1 or locations[0].y0 > 100:
                raise RuntimeError(f"Chương không mở rõ ở đầu trang: {title} -> {page}")
    for index, (level, title, page) in enumerate(toc_entries[:len(expected) - 1]):
        if level == 2 and toc_entries[index + 1][2] != page:
            raise RuntimeError(f"Tiêu đề Chương bị tách khỏi Bài đầu: {title}")
    first_part_page = toc_entries[0][2]
    printed_toc = "\n".join(doc[index].get_text() for index in range(1, first_part_page - 1))
    if re.search(r"\bP\d{2}(?:\.C\d{2})?(?:\.L\d{2})?\b", printed_toc):
        raise RuntimeError("Mục lục in lộ mã kiến trúc nội bộ")
    if "Bài 1.1" in printed_toc or labels[tree["parts"][0]["chapters"][0]["lessons"][0]["id"]] in printed_toc:
        raise RuntimeError("Mục lục in quá dày: đã đưa Bài vào danh sách Phần–Chương")
    for level, label in expected:
        if level <= 2 and label not in printed_toc:
            raise RuntimeError(f"Mục lục in thiếu nhãn: {label}")
    printed_entries = [(level, title, page) for level, title, page in toc_entries
                       if level <= 2 and not title.startswith("Đáp án chương")]
    if not any(title == "Lời giải bài tập" for _, title, _ in printed_entries):
        raise RuntimeError("Mục lục in thiếu Lời giải bài tập")
    toc_pages = [(doc[index], doc[index].get_text("words"))
                 for index in range(1, first_part_page - 1)]
    for _, title, destination in printed_entries:
        matched = 0
        for page, words in toc_pages:
            for rect in page.search_for(title):
                if any(word[4] == str(destination) and word[0] > PAGE_W - RIGHT - 45
                       and abs(word[1] - rect.y0) < 14 for word in words):
                    matched += 1
        if matched != 1:
            raise RuntimeError(f"Số trang mục lục in sai: {title} -> {destination}")
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
