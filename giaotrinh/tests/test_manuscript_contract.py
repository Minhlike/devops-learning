"""Regression gates for the Wave 1 migration into the approved knowledge tree."""

import copy
import csv
import json
import re
import unittest
from collections import Counter
from pathlib import Path
from unittest.mock import patch

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
        editorial = json.loads((ROOT / "manuscript" / "editorial_evidence.json").read_text(encoding="utf-8"))
        reviewed = len(wave2["lessons"])
        synthesis_ids = {
            "P06.C02.L02", "P06.C03.L03", "P06.C04.L02", "P08.C02.L02",
            "P09.C01.L01", "P09.C04.L02", "P10.C01.L02", "P10.C01.L03",
            "P11.C06.L01", "P12.C01.L01", "P12.C04.L03",
        }
        self.assertTrue(synthesis_ids <= set(wave2["lessons"]))
        p13_reviewed = {lid for lid, row in self.manifest["lessons"].items()
                        if lid.startswith("P13.") and row["status"] == "reviewed" and
                        row["verification"] == "reviewed_p13_publication_contract"}
        self.assertEqual(len(p13_reviewed), 12)
        reviewed_ids = set(wave2["lessons"]) | p13_reviewed | set(editorial["lessons"])
        self.assertEqual(self.manifest["phase"], "complete_scientific_candidate")
        self.assertEqual(len(reviewed_ids), 178)
        self.assertEqual({lid for lid, row in self.manifest["lessons"].items()
                          if row["status"] == "reviewed"}, reviewed_ids)
        self.assertEqual(Counter(x["status"] for x in self.manifest["lessons"].values()),
                         Counter({"migrated_draft": 178 - len(reviewed_ids),
                                  "reviewed": len(reviewed_ids)}))
        self.assertEqual(sum(len(ls) for _, chapters in build.published_lessons(self.tree, self.manifest)
                             for _, ls in chapters), 178)

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
            migrated = (ROOT / owner["content"]).read_text(encoding="utf-8")
            extracted = json.loads(unit["extract_to_other_owners"])
            if extracted:
                evidence = {row["old_id"]: row for row in ledger("evidence_ownership.csv")}
                sentences = set()
                for claim in extracted:
                    anchor = evidence[claim["old_id"]]["old_anchor_or_title"]
                    position = paragraph.index(anchor)
                    previous = max(paragraph.rfind(". ", 0, position),
                                   paragraph.rfind("? ", 0, position),
                                   paragraph.rfind("! ", 0, position))
                    start = 0 if previous < 0 else previous + 2
                    endings = [index for index in (paragraph.find(". ", position),
                               paragraph.find("? ", position), paragraph.find("! ", position))
                               if index >= 0]
                    end = min(endings) + 1 if endings else len(paragraph)
                    sentence = paragraph[start:end]
                    sentences.add(sentence)
                    target = self.manifest["lessons"][claim["owner"]]
                    target_body = (ROOT / target["content"]).read_text(encoding="utf-8")
                    self.assertIn(anchor, target_body)
                    self.assertNotIn(anchor, migrated)
                    if claim["old_id"] not in ("CLM-ea54a2dace4146ac",
                                               "CLM-fc44f951fc7f37a7",
                                               "CLM-4694812c6561c96f",
                                               "CLM-04bb47b429753cbe"):
                        self.assertEqual(target_body.count(sentence), 1)
                for sentence in sentences:
                    paragraph = paragraph.replace(sentence + " ", "", 1) if sentence + " " in paragraph else (
                        paragraph.replace(" " + sentence, "", 1) if " " + sentence in paragraph else
                        paragraph.replace(sentence, "", 1))
            self.assertIn(" ".join(paragraph.split()), " ".join(migrated.split()))

    def test_each_lesson_first_and_last_prose_reaches_candidate(self):
        with pymupdf.open(build.OUTPUT) as doc:
            pdf_text = " ".join(" ".join(page.get_text().split()) for page in doc)
        for lid, row in self.manifest["lessons"].items():
            manuscript = (ROOT / row["content"]).read_text(encoding="utf-8")
            paragraphs = []
            for block in re.split(r"\n\s*\n", manuscript):
                block = block.strip()
                if not block or block.startswith(("{{", "```", "#", "|")):
                    continue
                plain = " ".join(re.sub(r"[`*]", "", block).split())
                if len(plain) > 70:
                    paragraphs.append(plain)
            self.assertTrue(paragraphs, lid)
            for paragraph in (paragraphs[0], paragraphs[-1]):
                self.assertIn(paragraph[:65], pdf_text, lid)

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

    def test_editorial_review_cannot_outlive_or_misattribute_evidence(self):
        review = json.loads((ROOT / "manuscript" / "editorial_evidence.json").read_text(
            encoding="utf-8"))
        broken = copy.deepcopy(review)
        del broken["lessons"]["P01.C02.L03"]
        with self.assertRaisesRegex(ValueError, "thiếu biên bản biên tập"):
            build.check_editorial_evidence(self.manifest, broken)
        broken = copy.deepcopy(review)
        broken["lessons"]["P01.C02.L03"]["checks"][0]["anchor"] = "not in manuscript"
        with self.assertRaisesRegex(ValueError, "thiếu neo hoặc biên"):
            build.check_editorial_evidence(self.manifest, broken)
        broken = copy.deepcopy(review)
        broken["lessons"]["P01.C02.L03"]["checks"][0]["sources"] = ["R1"]
        with self.assertRaisesRegex(ValueError, "Nguồn bài không khớp"):
            build.check_editorial_evidence(self.manifest, broken)
        broken_manifest = copy.deepcopy(self.manifest)
        broken_manifest["lessons"]["P01.C02.L01"]["verification"] = "reviewed_baseline_migration"
        with self.assertRaisesRegex(ValueError, "thiếu hợp đồng kiểm chứng"):
            build.load_manuscript(self.tree, broken_manifest)

    def test_migrated_claim_cannot_reappear_in_paragraph_owner(self):
        lid = "P03.C02.L01"
        target = (ROOT / self.manifest["lessons"][lid]["content"]).resolve()
        original_read = Path.read_text
        duplicate = " `ss -ltn` trên đúng network namespace"

        def injected_read(path, *args, **kwargs):
            value = original_read(path, *args, **kwargs)
            return value + duplicate if path.resolve() == target else value

        with patch.object(Path, "read_text", injected_read):
            with self.assertRaisesRegex(ValueError, "Claim đã tách vẫn lặp"):
                build.check_migration_evidence(self.manifest)

    def test_bookmark_same_count_but_wrong_destination_fails(self):
        with pymupdf.open(build.OUTPUT) as doc:
            toc = doc.get_toc()
            index = next(i for i, item in enumerate(toc) if item[1].startswith("Bài 2.2 —"))
            page = toc[index][2]
            wrong = next(p for p in range(page + 1, len(doc) + 1)
                         if toc[index][1] not in doc[p - 1].get_text())
            toc[index][2] = wrong
            doc.set_toc(toc)
            self.assertEqual(len(doc.get_toc()), len(toc))
            with self.assertRaisesRegex(RuntimeError, "Bookmark trỏ sai trang"):
                build.audit_document(doc)

    def test_reader_toc_keeps_internal_ids_out(self):
        _, labels = build.publication_labels(self.tree)
        self.assertEqual(labels["P01"], "PHẦN I — Máy tính và tiến trình")
        self.assertEqual(labels["P01.C01"], "Chương 1 — Công việc, thời gian và đường đi dữ liệu")
        self.assertEqual(labels["P01.C01.L01"], "Bài 1.1 — Máy thực thi")
        with pymupdf.open(build.OUTPUT) as doc:
            printed_toc = "\n".join(doc[i].get_text() for i in range(1, doc.get_toc()[0][2] - 1))
            self.assertIn(labels["P01.C01"], printed_toc)
            self.assertNotIn(labels["P01.C01.L01"], printed_toc)
            self.assertNotRegex(printed_toc, r"\bP\d{2}\.C\d{2}")
            doc[1].insert_text((72, 800), "P01.C01.L01", fontsize=8)
            with self.assertRaisesRegex(RuntimeError, "Mục lục in lộ mã"):
                build.audit_document(doc)

    def test_reader_exercise_names_cover_every_question_and_answer(self):
        labels = build.publication_exercises(self.tree, self.manifest)
        self.assertEqual(len(labels), 144)
        self.assertEqual(labels["P07.C04.L03.Q01"],
                         "Bài tập 24.2 — Dữ liệu khi đổi image và tên project")
        self.assertTrue(labels["C13.1"].startswith("Bài tập 48.1 —"))
        with pymupdf.open(build.OUTPUT) as doc:
            text = "\n".join(page.get_text() for page in doc)
            normalized = re.sub(r"\s+", " ", text)
            self.assertTrue(all(normalized.count(label) == 2 for label in labels.values()))
            self.assertNotRegex(text, r"\bP\d{2}\.C\d{2}\.L\d{2}\.Q\d{2}\b|\bC13\.\d+\b")
            doc[1].insert_text((72, 800), "P07.C04.L03.Q01", fontsize=8)
            with self.assertRaisesRegex(RuntimeError, "Mã bài tập nội bộ"):
                build.audit_document(doc)

        with patch.dict(build.EXERCISE_TITLES, {"P07.C04.L03.Q01": ""}):
            with self.assertRaisesRegex(ValueError, "Tên bài tập"):
                build.publication_exercises(self.tree, self.manifest)


if __name__ == "__main__":
    unittest.main()
