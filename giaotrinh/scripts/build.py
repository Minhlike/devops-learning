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
from reportlab.platypus import (
    BaseDocTemplate, Flowable, Frame, PageBreak, PageTemplate, Paragraph,
    Preformatted, Spacer, LongTable, TableStyle, KeepTogether,
)
from reportlab.platypus.tableofcontents import TableOfContents
try:
    from .p13_publication import figure_story
except ImportError:  # direct execution: python giaotrinh/scripts/build.py
    from p13_publication import figure_story


ROOT = Path(__file__).resolve().parents[1]
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
        "h3": ParagraphStyle("h3", fontName="BodyBold", fontSize=11.8,
                             leading=16, spaceBefore=12, spaceAfter=7,
                             keepWithNext=True),
        "body": ParagraphStyle("body", fontName="Body", fontSize=11.7,
                               leading=17.5, alignment=TA_LEFT, spaceAfter=7.5),
        "p13body": ParagraphStyle("p13body", fontName="Body", fontSize=11.7,
                                  leading=17, alignment=TA_LEFT, spaceAfter=6.5),
        "answerbody": ParagraphStyle("answerbody", fontName="Body", fontSize=10.8,
                                     leading=15.5, alignment=TA_LEFT, spaceAfter=6),
        "toc": ParagraphStyle("toc-title", fontName="BodyBold", fontSize=19,
                              leading=24, spaceAfter=20),
        "tocentry": ParagraphStyle("toc-entry", fontName="Body", fontSize=10,
                                   leading=11, leftIndent=8, firstLineIndent=-8),
        "tocchapter": ParagraphStyle("toc-chapter", fontName="Body", fontSize=9.5,
                                     leading=11, leftIndent=22, firstLineIndent=-8),
        "toclesson": ParagraphStyle("toc-lesson", fontName="Body", fontSize=9,
                                    leading=11, leftIndent=38, firstLineIndent=-8),
        "part_deck": ParagraphStyle("part-deck", fontName="BodyBold", fontSize=19,
                                    leading=25, alignment=TA_CENTER, spaceAfter=10),
        "part_intro": ParagraphStyle("part-intro", fontName="Body", fontSize=12,
                                     leading=19, spaceAfter=15),
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


class Book(BaseDocTemplate):
    def __init__(self, path: Path):
        super().__init__(str(path), pagesize=A4, leftMargin=LEFT,
                         rightMargin=RIGHT, topMargin=TOP, bottomMargin=BOTTOM,
                         title="Cẩm nang ngành DevOps — bản thảo candidate",
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
        if flowable.include_in_toc:
            self.notify("TOCEntry", (flowable.level - 1,
                                      flowable.heading_text, self.page, key))


def paragraph_markup(text: str) -> str:
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


def read_markdown(path: Path, styles: dict[str, ParagraphStyle]) -> list[Flowable]:
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
            story.append(figure_story(block[9:-2], styles))
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
            story.append(Paragraph(paragraph_markup(heading[4:]), styles["exercise"]))
            if rest.strip():
                story.append(Paragraph(paragraph_markup(" ".join(rest.splitlines())), styles["body"]))
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
            story.append(Paragraph(paragraph_markup(paragraph), styles["body"]))
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
    if len(part_ids) != 15 or len(chapter_ids) != 58 or len(lessons) != 178:
        raise ValueError("Cây kiến thức không còn đủ 15/58/178")
    if set(manifest["lessons"]) != set(lessons):
        raise ValueError("Manifest thiếu hoặc thừa bài so với cây đã duyệt")
    for lid, row in manifest["lessons"].items():
        if row["parent"] != lessons[lid]["parent"] or row["prerequisites"] != lessons[lid]["prerequisites"]:
            raise ValueError(f"Metadata parent hoặc tiên quyết sai: {lid}")
        if row["status"] not in ("migrated_draft", "migration_fragment", "pending_authorship", "reviewed"):
            raise ValueError(f"Trạng thái bài sai: {lid}")
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
    return tree, manifest


def check_migration_evidence(manifest: dict) -> None:
    with (ROOT / "architecture" / "evidence_ownership.csv").open(
            encoding="utf-8-sig", newline="") as stream:
        evidence = list(csv.DictReader(stream))
    if len(evidence) != 369 or len({row["old_id"] for row in evidence}) != 369:
        raise ValueError("Ledger claim/ví dụ/bài tập không đủ hoặc trùng")
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
    publication = list(published_lessons(tree, manifest))
    count = sum(len(lessons) for _, chapters in publication for _, lessons in chapters)
    if count < 100:
        raise RuntimeError("Migration candidate thiếu phần lớn nội dung cũ")
    styles = style()
    toc = TableOfContents()
    toc.levelStyles = [styles["tocentry"], styles["tocchapter"], styles["toclesson"]]
    story: list[Flowable] = [
        Spacer(1, 170),
        Paragraph("CẨM NANG<br/>NGÀNH DEVOPS", styles["title"]),
        Spacer(1, 26),
        Paragraph(f"Bản thảo tích hợp Đợt 2 · {count}/178 bài có nội dung", styles["subtitle"]),
        Spacer(1, 10),
        Paragraph("Chưa phải bản phát hành hoàn chỉnh", styles["subtitle"]),
        PageBreak(),
        Paragraph("MỤC LỤC", styles["toc"]),
        toc,
        PageBreak(),
    ]
    for part, chapters in publication:
        story.append(Heading(f"PHẦN {int(part['id'][1:]):02d} — {part['title']}", 1, part["id"], styles))
        story.append(Spacer(1, 28))
        story.append(Paragraph(paragraph_markup(part["central_question"]), styles["part_deck"]))
        story.append(Paragraph(paragraph_markup(part["mental_model"]), styles["part_intro"]))
        story.append(PageBreak())
        for chapter, lessons in chapters:
            story.append(Heading(f"Chương {chapter['id']} — {chapter['title']}", 2, chapter["id"], styles))
            story.append(Paragraph(paragraph_markup(chapter["objective"]), styles["body"]))
            for lesson in lessons:
                lid = lesson["id"]
                story.append(Heading(f"Bài {lid} — {lesson['title']}", 3, lid, styles))
                story.extend(read_markdown(ROOT / manifest["lessons"][lid]["content"], styles))
                for qa in manifest["lessons"][lid]["qa"]:
                    if lid.startswith("P13."):
                        continue  # Reviewed P13 questions are already inside the lesson.
                    story.append(Paragraph(paragraph_markup(f"Bài tập {qa['publication_id']}"), styles["exercise"]))
                    story.append(Paragraph(paragraph_markup(qa["question"]), styles["body"]))
            story.append(PageBreak())
    story.append(Heading("Lời giải", 1, "answers", styles, include_in_toc=False))
    for part, chapters in publication:
        for chapter, lessons in chapters:
            entries = [(lid["id"], qa) for lid in lessons for qa in manifest["lessons"][lid["id"]]["qa"]]
            if not entries:
                continue
            story.append(Heading(f"Đáp án {chapter['id']} — {chapter['title']}", 2,
                                 f"{chapter['id']}.answers", styles, include_in_toc=False))
            for _, qa in entries:
                story.append(Paragraph(paragraph_markup(qa["publication_id"] + ". " + qa["answer"]), styles["answerbody"]))
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
    for phrase in ("CẨM NANG", "MỤC LỤC", "Lời giải", "Chưa phải bản phát hành"):
        if phrase not in text:
            raise RuntimeError(f"Thiếu nội dung PDF: {phrase}")
    tree, manifest = load_manuscript()
    expected = []
    for part, chapters in published_lessons(tree, manifest):
        expected.append((1, part["id"]))
        for chapter, lessons in chapters:
            expected.append((2, chapter["id"]))
            expected.extend((3, lesson["id"]) for lesson in lessons)
            for lesson in lessons:
                for qa in manifest["lessons"][lesson["id"]]["qa"]:
                    if qa["publication_id"] not in text:
                        raise RuntimeError(f"Thiếu bài tập/đáp án {qa['publication_id']}")
    for figure in ("Hình XIII.1.1", "Hình XIII.2.1", "Hình XIII.3.1", "Hình XIII.4.1"):
        if figure not in text:
            raise RuntimeError(f"Thiếu hình đã duyệt: {figure}")
    toc_entries = doc.get_toc()
    actual = [(level, ("P" + title.split(" — ", 1)[0].split()[-1]
                       if level == 1 and title.startswith("PHẦN ") else
                       title.split(" — ", 1)[0].split()[-1]))
              for level, title, _ in toc_entries[:len(expected)]]
    if actual != expected:
        raise RuntimeError(f"Sai cấp/thứ tự bookmark: {actual[:8]} != {expected[:8]}")
    for level, title, page in toc_entries[:len(expected)]:
        if page < 3 or page > len(doc) or title not in doc[page - 1].get_text():
            raise RuntimeError(f"Bookmark trỏ sai trang: {title} -> {page}")
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
