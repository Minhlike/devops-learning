"""Check draft ownership against the locked architecture and source-free render text."""
import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ARCH = ROOT.parents[1] / "architecture" / "knowledge_tree.json"


class Part13Contract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data = json.loads(ARCH.read_text(encoding="utf-8"))
        part = next(part for part in data["parts"] if part["id"] == "P13")
        cls.chapters = part["chapters"]

    def test_exact_approved_lessons(self):
        self.assertEqual(len(self.chapters), 4)
        for chapter in self.chapters:
            folder = ROOT / chapter["id"].split(".")[-1]
            draft = (folder / "manuscript.md").read_text(encoding="utf-8")
            headings = re.findall(r"^## (P13\.C\d{2}\.L\d{2})\b", draft, re.M)
            self.assertEqual(headings, [lesson["id"] for lesson in chapter["lessons"]])

    def test_exercises_and_answer_ownership(self):
        ids = []
        for chapter in self.chapters:
            folder = ROOT / chapter["id"].split(".")[-1]
            draft = (folder / "manuscript.md").read_text(encoding="utf-8")
            answers = (folder / "answers.md").read_text(encoding="utf-8")
            exercises = re.findall(r"^### Bài tập (C13\.\d+)\b", draft, re.M)
            solved = re.findall(r"^\*\*(C13\.\d+)\.\*\*", answers, re.M)
            self.assertEqual(exercises, solved)
            self.assertEqual(len(exercises), 3)
            ids.extend(exercises)
        self.assertEqual(ids, [f"C13.{i}" for i in range(1, 13)])

    def test_claims_separate_and_render_text_source_free(self):
        for chapter in self.chapters:
            folder = ROOT / chapter["id"].split(".")[-1]
            draft = (folder / "manuscript.md").read_text(encoding="utf-8")
            answers = (folder / "answers.md").read_text(encoding="utf-8")
            for render_text in (draft, answers):
                self.assertNotRegex(render_text, r"https?://|\[(?:R|B|SRE|DR|INC|PERF)\d+\]")
            with (folder / "claims.csv").open(encoding="utf-8", newline="") as stream:
                claims = list(csv.DictReader(stream))
            self.assertTrue(claims)
            lessons = {x["id"] for x in chapter["lessons"]}
            for claim in claims:
                self.assertIn(claim["lesson_id"], lessons)
                self.assertTrue(claim["source_url"].startswith("https://"))
                self.assertTrue(all(claim[k].strip() for k in ("claim", "source_location", "checked_date", "support", "limit")))
                self.assertIn(claim["status"], {"PASS", "SKIP", "UNKNOWN"})


if __name__ == "__main__":
    unittest.main()
