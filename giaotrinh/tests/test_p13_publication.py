"""Publication gates for the reviewed P13 content and its candidate PDF."""

import csv
import json
import re
import sys
import unittest
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build import audit, source_free_pdf_issues  # noqa: E402

PART = ROOT / "authoring" / "P13"
PDF = ROOT / "Cam_nang_devops.candidate.pdf"


class PublicationPart13(unittest.TestCase):
    def test_reviewed_input_is_complete(self):
        tree = json.loads((ROOT / "architecture" / "knowledge_tree.json").read_text(encoding="utf-8"))
        part = next(p for p in tree["parts"] if p["id"] == "P13")
        self.assertEqual(len(part["chapters"]), 4)
        claims = 0
        for chapter in part["chapters"]:
            folder = PART / chapter["id"].split(".")[-1]
            draft = (folder / "manuscript.md").read_text(encoding="utf-8")
            answers = (folder / "answers.md").read_text(encoding="utf-8")
            self.assertEqual(re.findall(r"^## (P13\.C\d{2}\.L\d{2})", draft, re.M),
                             [lesson["id"] for lesson in chapter["lessons"]])
            self.assertEqual(re.findall(r"^### Bài tập (C13\.\d+)", draft, re.M),
                             re.findall(r"^\*\*(C13\.\d+)\.\*\*", answers, re.M))
            with (folder / "claims.csv").open(encoding="utf-8", newline="") as stream:
                rows = list(csv.DictReader(stream))
            self.assertTrue(all(row["status"] == "PASS" and row["source_url"].startswith("https://")
                                for row in rows))
            claims += len(rows)
        self.assertEqual(claims, 27)

    def test_candidate_has_exact_hierarchy_and_answer_pairs(self):
        self.assertTrue(PDF.is_file() and PDF.stat().st_size > 100_000,
                        "PDF candidate missing or unreadable")
        with pymupdf.open(PDF) as doc:
            audit(PDF)
            toc = doc.get_toc()
            part = next(item for item in toc if item[1].startswith("PHẦN 13"))
            self.assertEqual(part[0], 1)
            chapters = [item for item in toc if item[0] == 2 and
                        re.match(r"Chương P13\.C0[1-4] — (?!đáp án)", item[1])]
            self.assertEqual(len(chapters), 4)
            lessons = [item for item in toc if item[0] == 3 and item[1].startswith("Bài P13.")]
            self.assertEqual(len(lessons), 12)
            self.assertEqual([item[2] for item in chapters], sorted(item[2] for item in chapters))
            for item in [part, *chapters, *lessons]:
                page_text = doc[item[2] - 1].get_text()
                self.assertIn(item[1], page_text, f"bookmark points away from heading: {item}")
            full = "\n".join(page.get_text() for page in doc)
            legacy_chapters = sorted((ROOT / "chapters").glob("[0-9][0-9]-*.md"))
            self.assertEqual(len(legacy_chapters), 19)
            self.assertFalse(any(item[1].startswith("Chương 1. ") for item in toc),
                             "legacy chapters must not be standalone publication units")
            legacy_answers = re.findall(r"(?m)^(C\d+\.\d+)\.\s",
                                        (ROOT / "answers.md").read_text(encoding="utf-8"))
            self.assertEqual(len(legacy_answers), 79)
            manifest = json.loads((ROOT / "manuscript" / "manifest.json").read_text(encoding="utf-8"))
            publication_ids = [qa["publication_id"] for lid, row in manifest["lessons"].items()
                               if not lid.startswith("P13.") for qa in row["qa"]]
            old_question_ids = set(legacy_answers)
            migrated_ids = [qa["id"] for lid, row in manifest["lessons"].items()
                            if not lid.startswith("P13.") for qa in row["qa"]
                            if qa["id"] in old_question_ids]
            self.assertEqual(set(migrated_ids), old_question_ids)
            self.assertEqual(len(migrated_ids), 79)
            self.assertEqual(len(set(publication_ids)), len(publication_ids))
            for answer_id in publication_ids:
                self.assertRegex(full, rf"(?m)^{re.escape(answer_id)}\. ")
            self.assertIn("Lời giải", full)
            for i in range(1, 13):
                self.assertIn(f"Bài tập C13.{i}", full)
                self.assertRegex(full, rf"(?m)^C13\.{i}\. ")
            for caption in ("Hình XIII.1.1", "Hình XIII.2.1", "Hình XIII.3.1", "Hình XIII.4.1"):
                pages = [page for page in doc if caption in page.get_text()]
                self.assertEqual(len(pages), 1)
                self.assertGreater(len(pages[0].get_drawings()), 6,
                                   f"figure {caption} has no vector drawing")
            self.assertFalse(source_free_pdf_issues(doc))

    def test_missing_figure_and_caption_fails(self):
        """A blank caption count must not bypass the publication contract."""
        with pymupdf.open(PDF) as original:
            writer = pymupdf.open()
            # Copy all pages except the one carrying the final figure. Both its
            # vector and caption disappear; the gate must still fail.
            missing = next(i for i, page in enumerate(original) if "Hình XIII.4.1" in page.get_text())
            writer.insert_pdf(original, from_page=0, to_page=missing - 1)
            writer.insert_pdf(original, from_page=missing + 1, to_page=len(original) - 1)
            with self.assertRaisesRegex(RuntimeError, "Hình XIII.4.1"):
                from build import audit_document
                audit_document(writer)

    def test_every_reviewed_prose_block_reaches_pdf(self):
        with pymupdf.open(PDF) as doc:
            pdf_text = re.sub(r"\s+", " ", "\n".join(page.get_text() for page in doc))
        checked = 0
        for n in range(1, 5):
            for filename in ("manuscript.md", "answers.md"):
                draft = (PART / f"C{n:02d}" / filename).read_text(encoding="utf-8")
                for block in re.split(r"\n\s*\n", draft):
                    block = block.strip()
                    if not block or block.startswith(("#", "```")):
                        continue
                    if block.startswith("**C13."):
                        # The answer heading and its reasoning share one block.
                        block = re.sub(r"^\*\*C13\.\d+\.\*\*\s*", "", block)
                    plain = block.replace("**", "").replace("`", "")
                    plain = re.sub(r"P13\.C(\d{2})\.L(\d{2})",
                                   lambda m: f"Bài XIII.{int(m[1])}.{int(m[2])}", plain)
                    plain = re.sub(r"P13\.C(\d{2})", lambda m: f"Chương XIII.{int(m[1])}", plain)
                    plain = re.sub(r"\s+", " ", plain)
                    for excerpt in (plain[:42], plain[-42:]):
                        self.assertIn(excerpt, pdf_text, f"missing prose in {filename} C{n:02d}: {excerpt}")
                    checked += 1
        self.assertGreater(checked, 30)

    def test_part13_reference_url_is_rejected_from_pdf_metadata(self):
        with (PART / "C01" / "claims.csv").open(encoding="utf-8", newline="") as stream:
            url = next(csv.DictReader(stream))["source_url"]
        with pymupdf.open() as probe:
            probe.new_page()
            probe.set_metadata({"title": url})
            self.assertTrue(source_free_pdf_issues(probe))


if __name__ == "__main__":
    unittest.main()
