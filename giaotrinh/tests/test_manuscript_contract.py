"""Regression gates for the Wave 1 migration into the approved knowledge tree."""

import copy
import csv
import json
import re
import unittest
from collections import Counter
from pathlib import Path

import pymupdf

from giaotrinh.scripts import build
from giaotrinh.scripts.migrate_manuscript import sections

ROOT = build.ROOT
ARCH = ROOT / "architecture"


def ledger(name):
    with (ARCH / name).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


class ManuscriptContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tree, cls.manifest = build.load_manuscript()

    def test_all_ids_have_exact_parent_and_no_fake_completed_lesson(self):
        self.assertEqual(len(self.tree["parts"]), 15)
        self.assertEqual(sum(len(p["chapters"]) for p in self.tree["parts"]), 58)
        self.assertEqual(len(self.manifest["lessons"]), 178)
        wave2 = json.loads((ROOT / "manuscript" / "wave2_evidence.json").read_text(encoding="utf-8"))
        reviewed = len(wave2["lessons"])
        synthesis_ids = {
            "P06.C02.L02", "P06.C03.L03", "P06.C04.L02", "P08.C02.L02",
            "P09.C01.L01", "P09.C04.L02", "P10.C01.L02", "P10.C01.L03",
            "P11.C06.L01", "P12.C01.L01", "P12.C04.L03",
        }
        self.assertTrue(synthesis_ids <= set(wave2["lessons"]))
        self.assertEqual(Counter(x["status"] for x in self.manifest["lessons"].values()),
                         Counter({"migrated_draft": 136 - len(synthesis_ids),
                                  "reviewed": reviewed}))
        self.assertEqual(sum(len(ls) for _, chapters in build.published_lessons(self.tree, self.manifest)
                             for _, ls in chapters), 136 - len(synthesis_ids) + reviewed)

    def test_legacy_sections_and_split_paragraphs_are_preserved(self):
        migration = [r for r in ledger("legacy_migration.csv") if r["action"] != "move_rekey_after_review"]
        units = ledger("legacy_content_units.csv")
        self.assertEqual((len(migration), len(units)), (88, 216))
        for row in migration:
            old, section = row["old_location"].split("#")
            original = sections(ROOT / old)[1][section]
            owner = self.manifest["lessons"][row["primary_text_owner"]]
            self.assertIn(row["old_location"], owner["legacy_units"] +
                          [u["old_location"].split(":")[0] for u in units
                           if u["primary_lesson_id"] == row["primary_text_owner"]])
            if row["action"] != "split":
                self.assertIn(original, (ROOT / owner["content"]).read_text(encoding="utf-8"))
        for unit in units:
            old, rest = unit["old_location"].split("#")
            section, ordinal = rest.split(":")
            paragraph = re.split(r"\n\s*\n", sections(ROOT / old)[1][section])[int(ordinal.split("-")[1]) - 1]
            owner = self.manifest["lessons"][unit["primary_lesson_id"]]
            self.assertIn(unit["old_id"], owner["legacy_units"])
            self.assertIn(paragraph, (ROOT / owner["content"]).read_text(encoding="utf-8"))

    def test_claims_examples_and_question_answer_pairs_have_one_owner(self):
        evidence = ledger("evidence_ownership.csv")
        self.assertEqual(Counter(r["kind"] for r in evidence),
                         Counter({"claim": 267, "example": 23, "exercise_answer": 79}))
        self.assertEqual(len({r["old_id"] for r in evidence}), 369)
        for row in evidence:
            owner = self.manifest["lessons"][row["primary_lesson_id"]]
            manuscript = (ROOT / owner["content"]).read_text(encoding="utf-8")
            if row["kind"] == "claim":
                self.assertIn(row["old_id"], owner["claim_ids"])
                self.assertIn(row["old_anchor_or_title"], manuscript)
            elif row["kind"] == "example":
                self.assertIn(row["old_id"], owner["examples"])
                self.assertIn("{{code:" + row["old_id"] + "}}", manuscript)
            else:
                self.assertEqual(sum(q["id"] == row["old_id"] for q in owner["qa"]), 1)
        wave2 = json.loads((ROOT / "manuscript" / "wave2_evidence.json").read_text(encoding="utf-8"))
        expected_count = 91 + sum(len(x["qa"]) for x in wave2["lessons"].values())
        self.assertEqual(sum(len(x["qa"]) for x in self.manifest["lessons"].values()), expected_count)
        publication_ids = [qa["publication_id"] for x in self.manifest["lessons"].values() for qa in x["qa"]]
        self.assertEqual(len(set(publication_ids)), expected_count)
        p13_claims = 0
        for i in range(1, 5):
            with (ROOT / "authoring" / "P13" / f"C{i:02d}" / "claims.csv").open(
                    encoding="utf-8", newline="") as stream:
                p13_claims += len(list(csv.DictReader(stream)))
        self.assertEqual(p13_claims, 27)

    def test_missing_lesson_and_wrong_parent_fail_closed(self):
        broken = copy.deepcopy(self.manifest)
        del broken["lessons"]["P01.C02.L01"]
        with self.assertRaisesRegex(ValueError, "Manifest thiếu"):
            build.load_manuscript(self.tree, broken)
        broken = copy.deepcopy(self.manifest)
        broken["lessons"]["P01.C02.L01"]["parent"] = "P09.C01"
        with self.assertRaisesRegex(ValueError, "parent"):
            build.load_manuscript(self.tree, broken)

    def test_claimed_complete_without_content_fails_closed(self):
        broken = copy.deepcopy(self.manifest)
        broken["lessons"]["P01.C02.L01"]["content"] = None
        with self.assertRaisesRegex(ValueError, "thiếu nội dung"):
            build.load_manuscript(self.tree, broken)
        broken = copy.deepcopy(self.manifest)
        broken["lessons"]["P01.C02.L01"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "manifest chưa duyệt"):
            build.load_manuscript(self.tree, broken)

    def test_missing_claim_example_and_answer_fail_closed(self):
        broken = copy.deepcopy(self.manifest)
        broken["lessons"]["P01.C02.L01"]["claim_ids"].clear()
        with self.assertRaisesRegex(ValueError, "Mất hoặc đổi chủ claim_ids"):
            build.load_manuscript(self.tree, broken)
        broken = copy.deepcopy(self.manifest)
        broken["lessons"]["P01.C02.L02"]["examples"].clear()
        with self.assertRaisesRegex(ValueError, "Mất hoặc đổi chủ examples"):
            build.load_manuscript(self.tree, broken)
        broken = copy.deepcopy(self.manifest)
        broken["lessons"]["P01.C02.L01"]["qa"].clear()
        with self.assertRaisesRegex(ValueError, "Mất cặp đề đáp án"):
            build.load_manuscript(self.tree, broken)
        broken = copy.deepcopy(self.manifest)
        broken["lessons"]["P01.C02.L01"]["qa"][0]["publication_id"] = "C13.1"
        with self.assertRaisesRegex(ValueError, "Mã bài tập xuất bản"):
            build.load_manuscript(self.tree, broken)

    def test_wave2_lesson_and_qa_cannot_silently_drop(self):
        broken = copy.deepcopy(self.manifest)
        broken["lessons"]["P01.C01.L01"]["status"] = "pending_authorship"
        with self.assertRaisesRegex(ValueError, "trạng thái kiểm chứng"):
            build.load_manuscript(self.tree, broken)
        broken = copy.deepcopy(self.manifest)
        broken["lessons"]["P01.C01.L03"]["qa"].clear()
        with self.assertRaisesRegex(ValueError, "Bài tập Đợt 2"):
            build.load_manuscript(self.tree, broken)

    def test_wave2_source_id_url_is_immutable(self):
        ledger = json.loads((ROOT / "manuscript" / "wave2_evidence.json").read_text(encoding="utf-8"))
        ledger["sources"]["W2-CLK"]["url"] = "https://example.invalid/changed"
        with self.assertRaisesRegex(ValueError, "đổi ID hoặc URL khóa"):
            build.check_wave2_evidence(self.manifest, ledger)

    def test_bookmark_same_count_but_wrong_destination_fails(self):
        with pymupdf.open(build.OUTPUT) as doc:
            toc = doc.get_toc()
            index = next(i for i, item in enumerate(toc) if item[1].startswith("Bài P01.C02.L02"))
            page = toc[index][2]
            wrong = next(p for p in range(page + 1, len(doc) + 1)
                         if toc[index][1] not in doc[p - 1].get_text())
            toc[index][2] = wrong
            doc.set_toc(toc)
            self.assertEqual(len(doc.get_toc()), len(toc))
            with self.assertRaisesRegex(RuntimeError, "Bookmark trỏ sai trang"):
                build.audit_document(doc)


if __name__ == "__main__":
    unittest.main()
