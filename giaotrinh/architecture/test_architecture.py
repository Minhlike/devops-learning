"""Regression contracts for the proposed knowledge graph and full legacy map."""

import csv
import json
import re
import unittest
from collections import Counter
from pathlib import Path

import compile_architecture as architecture


class ArchitectureContracts(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parent
        self.tree = json.loads((self.root / "knowledge_tree.json").read_text(encoding="utf-8"))
        with (self.root / "legacy_migration.csv").open(encoding="utf-8", newline="") as file:
            self.rows = list(csv.DictReader(file))

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
        self.assertEqual(len(entries), len({ident for ident, _ in entries}))
        valid = {part["id"] for part in self.tree["parts"]}
        valid.update(lesson["id"] for part in self.tree["parts"] for ch in part["chapters"]
                     for lesson in ch["lessons"])
        for ident, target in entries:
            self.assertIn(target, valid, ident)
        self.assertIn("P0", storyboard)
        self.assertIn("P2", storyboard)


if __name__ == "__main__":
    unittest.main()
