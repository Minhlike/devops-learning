"""Regression tests for evidence separation and the generated PDF."""

import copy
import json
import tempfile
import unittest
from pathlib import Path

import pymupdf

from giaotrinh.scripts import build


class SourceFreePdfTests(unittest.TestCase):
    def test_candidate_and_claim_map(self):
        build.check_source_map()
        with pymupdf.open(build.OUTPUT) as doc:
            self.assertEqual(build.source_free_pdf_issues(doc), [])
            self.assertGreaterEqual(len(doc), 8)

    def make_pdf(self, root: Path, *, body="", title="", bookmark="", link="") -> Path:
        path = root / "probe.pdf"
        doc = pymupdf.open()
        page = doc.new_page()
        page.insert_font(fontname="TNR", fontfile=str(build.FONT_DIR / "times.ttf"))
        page.insert_text((72, 72), body or "Technical example", fontname="TNR")
        if title:
            doc.set_metadata({"title": title})
        if bookmark:
            doc.set_toc([[1, bookmark, 1]])
        if link:
            page.insert_link({"kind": pymupdf.LINK_URI,
                              "from": pymupdf.Rect(70, 60, 300, 90), "uri": link})
        doc.save(path)
        doc.close()
        return path

    def test_reference_leaks_in_each_pdf_surface_are_rejected(self):
        reference = "https://man7.org/linux/man-pages/man2/fork.2.html"
        with tempfile.TemporaryDirectory(dir=build.ROOT) as temp:
            root = Path(temp)
            cases = [
                {"body": "An inline marker [R1]"},
                {"body": "An inline marker [S1]"},
                {"body": "An inline marker [N4]"},
                {"body": "An inline marker [D1]"},
                {"body": "An inline marker [T1]"},
                {"body": "Nguồn chương"},
                {"body": "Linux man-pages 6.19"},
                {"body": "RFC 9293"},
                {"body": reference},
                {"title": "Bibliography [B2]"},
                {"bookmark": "Tài liệu tham khảo"},
                {"link": reference},
            ]
            for case in cases:
                with self.subTest(case=case):
                    path = self.make_pdf(root, **case)
                    with pymupdf.open(path) as doc:
                        self.assertTrue(build.source_free_pdf_issues(doc))
                    path.unlink()

    def test_technical_example_url_is_allowed(self):
        url = "https://api.example.test/health"
        with tempfile.TemporaryDirectory(dir=build.ROOT) as temp:
            path = self.make_pdf(Path(temp), body=url, link=url)
            with pymupdf.open(path) as doc:
                self.assertEqual(build.source_free_pdf_issues(doc), [])

    def test_unreviewed_claim_with_real_anchor_is_rejected(self):
        registry = json.loads((build.ROOT / "source_map.json").read_text(encoding="utf-8"))
        altered = copy.deepcopy(registry)
        altered["claims"][0]["review_status"] = "pending"
        with self.assertRaisesRegex(ValueError, "chưa được đối chiếu"):
            build.check_source_map(altered)
        altered = copy.deepcopy(registry)
        altered["claims"][0]["support"] = ""
        with self.assertRaisesRegex(ValueError, "biên bản đối chiếu"):
            build.check_source_map(altered)
        altered = copy.deepcopy(registry)
        altered["sources"]["K1"]["version"] = "latest"
        with self.assertRaisesRegex(ValueError, "chưa khóa phiên bản"):
            build.check_source_map(altered)
        altered = copy.deepcopy(registry)
        altered["claims"][0]["section"] = "1.2"
        with self.assertRaisesRegex(ValueError, "không nằm trong mục"):
            build.check_source_map(altered)


if __name__ == "__main__":
    unittest.main()
