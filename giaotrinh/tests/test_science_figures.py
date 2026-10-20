"""PDF checks for source-editable mechanism diagrams and part openers."""

import unittest

import pymupdf

from giaotrinh.scripts import build


class ScienceFigureContract(unittest.TestCase):
    def test_all_part_openers_have_their_route(self):
        with pymupdf.open(build.OUTPUT) as doc:
            part_pages = [page for level, _, page in doc.get_toc() if level == 1][:15]
            self.assertEqual(len(part_pages), 15)
            for number in part_pages:
                self.assertIn("LỘ TRÌNH PHẦN", doc[number - 1].get_text())

    def test_missing_panel_and_caption_fails(self):
        with pymupdf.open(build.OUTPUT) as doc:
            page = next(page for page in doc if "Hình I.2.1" in page.get_text())
            caption = page.search_for("Hình I.2.1")[0]
            panel = next(drawing["rect"] for drawing in page.get_drawings()
                         if drawing["rect"].width >= 450 and drawing["rect"].height >= 200)
            page.add_redact_annot(panel)
            page.add_redact_annot(caption)
            page.apply_redactions(graphics=1)
            with self.assertRaisesRegex(RuntimeError, "Thiếu hoặc lặp hình cơ chế V02"):
                build.audit_document(doc)

    def test_caption_without_panel_fails(self):
        with pymupdf.open(build.OUTPUT) as doc:
            page = next(page for page in doc if "Hình III.2.1" in page.get_text())
            panel = next(drawing["rect"] for drawing in page.get_drawings()
                         if drawing["rect"].width >= 450 and drawing["rect"].height >= 200)
            page.add_redact_annot(panel)
            page.apply_redactions(graphics=1)
            with self.assertRaisesRegex(RuntimeError, "Thiếu hoặc lặp hình cơ chế V07"):
                build.audit_document(doc)


if __name__ == "__main__":
    unittest.main()
