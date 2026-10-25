"""PDF checks for source-editable mechanism diagrams and part openers."""

import json
import unittest

import pymupdf

from giaotrinh.scripts import build


class ScienceFigureContract(unittest.TestCase):
    def test_new_figure_evidence_has_one_owner_and_locked_source_ids(self):
        ledger = json.loads((build.ROOT / "manuscript" / "figure_evidence.json").read_text(encoding="utf-8"))
        tree, manifest = build.load_manuscript()
        self.assertEqual(len(ledger["figures"]), 15)
        storyboard = (build.ROOT / ledger["storyboard"]).read_text(encoding="utf-8")
        for figure_id, row in ledger["figures"].items():
            with self.subTest(figure=figure_id):
                self.assertIn(figure_id, build.FIGURES)
                self.assertIn("### " + figure_id, storyboard)
                owner = manifest["lessons"][row["lesson_id"]]
                self.assertTrue(row["source_ids"])
                self.assertLessEqual(set(row["source_ids"]), set(owner["source_ids"]))
                self.assertTrue(row["claim"] and row["limits"])
                self.assertIn("{{figure:" + figure_id + "}}",
                              (build.ROOT / owner["content"]).read_text(encoding="utf-8"))

    def test_scientific_panels_cover_the_visual_gaps(self):
        concepts = {
            "V03": ("Hình II.1.1", "Open file desc.", "inode 42"),
            "V09": ("Hình IV.2.1", "MERGE", "REBASE"),
            "V10": ("Hình V.1.1", "tar", "pipefail"),
            "V12": ("Hình VI.1.1", "Artifact H84", "Test gate"),
            "V16": ("Hình VII.3.1", "Named volume", "Writable A"),
            "V18": ("Hình VIII.2.1", "S3 gateway endpoint", "STS regional endpoint"),
            "V22": ("Hình X.2.1", "Drift quyền", "handler"),
            "V29": ("Hình XII.3.1", "gateway", "upstream_1"),
            "V33": ("Hình XIV.3.1", "Attestation", "Verifier"),
            "V43": ("Hình XV.3.1", "commit", "restore"),
            "V44": ("Hình IV.1.1", "tree T1", "blob B1"),
            "V45": ("Hình IV.1.2", "Index", "3000"),
            "V46": ("Hình IV.1.3", "origin/main", "tag v1.4"),
            "V47": ("Hình IV.2.2", "stage 1", "stage 3"),
            "V48": ("Hình IV.2.3", "revert mới", "mixed"),
        }
        self.assertEqual(len(build.FIGURES), 19)
        with pymupdf.open(build.OUTPUT) as doc:
            for figure_id, (caption, *terms) in concepts.items():
                with self.subTest(figure=figure_id):
                    pages = [page for page in doc if caption in page.get_text()]
                    self.assertEqual(len(pages), 1)
                    page = pages[0]
                    caption_rect = page.search_for(caption)[0]
                    panels = [drawing["rect"] for drawing in page.get_drawings()
                              if drawing["rect"].width >= 450 and drawing["rect"].height >= 200
                              and 0 <= caption_rect.y0 - drawing["rect"].y1 <= 30]
                    self.assertEqual(len(panels), 1)
                    panel_text = page.get_text(clip=panels[0])
                    for term in terms:
                        self.assertIn(term, panel_text)

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

    def test_capstone_figure_and_caption_cannot_both_disappear(self):
        with pymupdf.open(build.OUTPUT) as doc:
            page = next(page for page in doc if "Hình XV.3.1" in page.get_text())
            caption = page.search_for("Hình XV.3.1")[0]
            panel = next(drawing["rect"] for drawing in page.get_drawings()
                         if drawing["rect"].width >= 450 and drawing["rect"].height >= 200
                         and 0 <= caption.y0 - drawing["rect"].y1 <= 30)
            page.add_redact_annot(panel)
            page.add_redact_annot(caption)
            page.apply_redactions(graphics=1)
            with self.assertRaisesRegex(RuntimeError, "Thiếu hoặc lặp hình cơ chế V43"):
                build.audit_document(doc)


if __name__ == "__main__":
    unittest.main()
