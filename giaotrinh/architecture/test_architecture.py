"""Regression contracts for the proposed knowledge graph and full legacy map."""

import csv
import hashlib
import json
import re
import unittest
from collections import Counter
from copy import deepcopy
from pathlib import Path

import compile_architecture as architecture


class ArchitectureContracts(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parent
        self.tree = json.loads((self.root / "knowledge_tree.json").read_text(encoding="utf-8"))
        with (self.root / "legacy_migration.csv").open(encoding="utf-8", newline="") as file:
            self.rows = list(csv.DictReader(file))
        with (self.root / "evidence_ownership.csv").open(encoding="utf-8", newline="") as file:
            self.ownership = list(csv.DictReader(file))
        with (self.root / "legacy_content_units.csv").open(encoding="utf-8", newline="") as file:
            self.content_units = list(csv.DictReader(file))

    def test_generated_tree_matches_editable_declarations(self):
        fresh, markdown = architecture.compile_tree()
        self.assertEqual(self.tree, fresh)
        self.assertEqual((self.root / "knowledge_tree.md").read_text(encoding="utf-8"), markdown)
        parts = self.tree["parts"]
        self.assertTrue(all(len(part["chapters"]) >= 2 for part in parts))
        self.assertTrue({"Linux", "Container", "Terraform"}.issubset(
            {word for part in parts for word in part["title"].split()}))

    def test_required_graph_is_acyclic_and_all_three_edge_kinds_exist(self):
        lessons = [lesson for part in self.tree["parts"] for ch in part["chapters"]
                   for lesson in ch["lessons"]]
        position = {lesson["id"]: i for i, lesson in enumerate(lessons)}
        self.assertEqual(len(position), len(lessons))
        kinds = Counter(edge["kind"] for edge in self.tree["dependency_edges"])
        self.assertTrue(all(kinds[kind] for kind in ("required", "helpful", "extension")))
        for edge in self.tree["dependency_edges"]:
            self.assertIn(edge["from"], position)
            self.assertIn(edge["to"], position)
            self.assertLess(position[edge["from"]], position[edge["to"]])
        # Specifically: HPA has CPU request/resource metrics and controller, not full Prometheus.
        hpa = next(ch for part in self.tree["parts"] for ch in part["chapters"]
                   if ch["id"] == "P11.C06")
        self.assertIn("P11.C03.L03", hpa["required"])
        self.assertIn("P11.C01.L02", hpa["required"])
        self.assertFalse(any(ref.startswith("P12") for ref in hpa["required"]))
        helm = next(ch for part in self.tree["parts"] for ch in part["chapters"] if ch["id"] == "P11.C08")
        trace = next(ch for part in self.tree["parts"] for ch in part["chapters"] if ch["id"] == "P12.C03")
        self.assertNotIn("P11.C07.L03", helm["required"])
        self.assertIn("P11.C07.L03", helm["helpful"])
        self.assertNotIn("P12.C02.L03", trace["required"])
        self.assertIn("P12.C02.L03", trace["helpful"])

    def test_migration_preserves_every_section_question_answer_example_and_claim(self):
        claims = json.loads((architecture.ROOT / "source_map.json").read_text(encoding="utf-8"))["claims"]
        fresh_rows = architecture.make_migration(claims)
        self.assertEqual(self.rows, fresh_rows)
        old_files = sorted((architecture.ROOT / "chapters").glob("[0-9][0-9]-*.md"))
        self.assertEqual({p.name[:2] for p in old_files}, architecture.SECTION_MAP.keys())
        self.assertEqual(sum("#C" not in row["old_location"] for row in self.rows),
                         sum(len(architecture.old_sections(p)) for p in old_files))
        self.assertEqual(sum(bool(row["exercise_answer_ids"]) for row in self.rows),
                         len(re.findall(r"(?m)^C\d+\.\d+\.\s", (architecture.ROOT / "answers.md").read_text(encoding="utf-8"))))
        covered = Counter((row["old_location"].split("#")[0], row["old_location"].split("#")[1], anchor)
                          for row in self.rows for anchor in json.loads(row["source_claim_anchors"]))
        expected = Counter((claim["chapter"], claim["section"], claim["anchor"]) for claim in claims)
        self.assertEqual(covered, expected)
        owned = Counter(row["kind"] for row in self.ownership)
        self.assertEqual(owned, {"claim": 267, "example": 23, "exercise_answer": 79})
        architecture.validate_ownership(self.ownership, claims)
        architecture.validate_content_units(self.content_units, claims, self.ownership)
        by_id = {row["old_id"]: row for row in self.ownership}
        units_by_id = {row["old_id"]: row for row in self.content_units}
        self.assertEqual(len(self.content_units), 216)
        for row in self.rows:
            if row["exercise_answer_ids"]:
                self.assertEqual(row["new_ids"], by_id[row["exercise_answer_ids"]]["primary_lesson_id"])
            else:
                for claim_id in filter(None, row["claim_ids"].split(";")):
                    self.assertIn(by_id[claim_id]["primary_lesson_id"], row["new_ids"].split(";"))
                for unit_id in filter(None, row["content_unit_ids"].split(";")):
                    self.assertIn(units_by_id[unit_id]["primary_lesson_id"], row["new_ids"].split(";"))

    def test_source_scope_status_and_reviewed_coverage(self):
        source_map = json.loads((architecture.ROOT / "source_map.json").read_text(encoding="utf-8"))
        locked = json.loads((architecture.ROOT / "source_ids.lock.json").read_text(encoding="utf-8"))["urls"]
        self.assertEqual(hashlib.sha256((architecture.ROOT / "source_map.json").read_bytes()).hexdigest(),
                         architecture.SOURCE_MAP_SHA256)
        self.assertTrue(all(source_map["sources"][sid]["url"] == url for sid, url in locked.items()))
        claims_by_lesson = {}
        for row in self.ownership:
            if row["kind"] == "claim":
                claims_by_lesson.setdefault(row["primary_lesson_id"], []).append(row)
        for part in self.tree["parts"]:
            for chapter in part["chapters"]:
                exact = set()
                for lesson in chapter["lessons"]:
                    expected_sources = {sid for row in claims_by_lesson.get(lesson["id"], [])
                                        for sid in row["original_source_ids"].split(";") if sid}
                    self.assertEqual(set(lesson["source_ids_to_recheck"]), expected_sources)
                    self.assertFalse(lesson["status"] == "reviewed_draft" and not lesson["legacy_sections"])
                    exact.update(expected_sources)
                self.assertEqual(set(chapter["source_ids_to_recheck"]), exact)
                if not exact:
                    self.assertEqual(chapter["source_ids_to_recheck"], [])
                    self.assertTrue(chapter["source_research_needed"])

    def test_reviewer_microfix_boundaries_and_negative_cases(self):
        capstone = (self.root / "capstone_contract.md").read_text(encoding="utf-8")
        architecture.validate_microfix_contracts(self.tree, self.ownership, capstone)

        def lesson(tree, lid):
            return next(l for p in tree["parts"] for c in p["chapters"]
                        for l in c["lessons"] if l["id"] == lid)

        for lid in architecture.PARTIAL_NETWORK_SCOPE:
            tampered = deepcopy(self.tree)
            lesson(tampered, lid)["status"] = "reviewed_draft"
            with self.subTest(ipv6_lesson=lid), self.assertRaisesRegex(ValueError, "IPv6/ND"):
                architecture.validate_microfix_contracts(tampered, self.ownership, capstone)

        for lid in architecture.CLAIMLESS_REVIEWED_LESSONS:
            tampered = deepcopy(self.tree)
            lesson(tampered, lid)["source_research_needed"] = False
            with self.subTest(claimless_lesson=lid), self.assertRaisesRegex(ValueError, "direct source"):
                architecture.validate_microfix_contracts(tampered, self.ownership, capstone)
        tampered = deepcopy(self.tree)
        lesson(tampered, "P09.C01.L02")["source_ids_to_recheck"] = ["R9"]
        with self.assertRaisesRegex(ValueError, "direct source"):
            architecture.validate_microfix_contracts(tampered, self.ownership, capstone)

        for name in ("templates/gateway.yaml", "templates/httproute.yaml"):
            tampered = [dict(row) for row in self.ownership]
            row = next(row for row in tampered if row["old_id"] == "examples/gateway-helm/" + name)
            row["primary_lesson_id"] = "P11.C07.L01"
            with self.subTest(template=name), self.assertRaisesRegex(ValueError, "before Helm"):
                architecture.validate_microfix_contracts(self.tree, tampered, capstone)

        reverted = capstone.replace("Mỗi request thử có `request_id` riêng",
                                     "Cùng một `request_id` dùng cho mọi request")
        with self.assertRaisesRegex(ValueError, "conflates change"):
            architecture.validate_microfix_contracts(self.tree, self.ownership, reverted)

    def test_negative_wrong_claim_example_exercise_or_source_fails(self):
        claims = json.loads((architecture.ROOT / "source_map.json").read_text(encoding="utf-8"))["claims"]
        for kind, field, replacement in (
            ("claim", "primary_lesson_id", "P15.C03.L04"),
            ("example", "primary_lesson_id", "P15.C03.L04"),
            ("exercise_answer", "primary_lesson_id", "P15.C03.L04"),
            ("claim", "original_source_ids", "R9"),
        ):
            tampered = [dict(row) for row in self.ownership]
            record = next(row for row in tampered if row["kind"] == kind)
            record[field] = replacement
            with self.subTest(kind=kind, field=field), self.assertRaisesRegex(ValueError, "Ownership mismatch"):
                architecture.validate_ownership(tampered, claims)
        tampered_units = [dict(row) for row in self.content_units]
        tampered_units[0]["primary_lesson_id"] = "P15.C03.L04"
        with self.assertRaisesRegex(ValueError, "Content-unit ownership mismatch"):
            architecture.validate_content_units(tampered_units, claims, self.ownership)

    def test_negative_missing_section_or_forward_prerequisite_fails(self):
        saved_map = architecture.SECTION_MAP["01"]
        architecture.SECTION_MAP["01"] = saved_map[:-1]
        try:
            with self.assertRaisesRegex(ValueError, "Section migration missing"):
                architecture.make_migration([])
        finally:
            architecture.SECTION_MAP["01"] = saved_map
        saved_required = architecture.CHAPTERS[0]["required"]
        architecture.CHAPTERS[0]["required"] = ["P15.C03.L03"]
        try:
            with self.assertRaisesRegex(ValueError, "forward required dependency"):
                architecture.compile_tree()
        finally:
            architecture.CHAPTERS[0]["required"] = saved_required

    def test_visual_ids_are_unique_and_point_into_tree(self):
        storyboard = (self.root / "visual_storyboard.md").read_text(encoding="utf-8")
        entries = re.findall(r"(?m)^### (V\d+) · `([^`]+)`", storyboard)
        self.assertEqual({ident for ident, _ in entries},
                         {f"V{i:02d}" for i in range(1, 44)})
        self.assertIn("43 ứng viên", storyboard)
        valid = {part["id"] for part in self.tree["parts"]}
        valid.update(lesson["id"] for part in self.tree["parts"] for ch in part["chapters"]
                     for lesson in ch["lessons"])
        for ident, target in entries:
            self.assertIn(target, valid, ident)
        self.assertEqual({ident: target for ident, target in entries if int(ident[1:]) >= 38}, {
            "V38": "P02.C03.L04", "V39": "P09.C01.L03", "V40": "P09.C03.L02",
            "V41": "P11.C03.L01", "V42": "P11.C08.L03", "V43": "P15.C03.L04",
        })
        self.assertIn("P0", storyboard)
        self.assertIn("P2", storyboard)


if __name__ == "__main__":
    unittest.main()
