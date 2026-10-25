"""Bounded contracts for the new synthesis chapter and its source separation."""

import copy
import json
import re
import statistics
import unittest
from pathlib import Path

from giaotrinh.scripts import build


class ToolchainChapterTests(unittest.TestCase):
    def test_chapter_has_eight_substantial_lessons_and_scoped_sources(self):
        tree, manifest = build.load_manuscript()
        chapter = tree["parts"][-1]["chapters"][-1]
        self.assertEqual(chapter["id"], "P15.C04")
        self.assertEqual(len(chapter["lessons"]), 8)
        content = []
        for lesson in chapter["lessons"]:
            row = manifest["lessons"][lesson["id"]]
            content.append((build.ROOT / row["content"]).read_text(encoding="utf-8"))
            self.assertEqual(len(row["qa"]), 1)
        words = sum(len(re.sub(r"(?s)```.*?```", "", body).split()) for body in content)
        chapter_words = []
        for folder in (build.ROOT / "manuscript").glob("P*/C*"):
            if folder.name == "C04" and folder.parent.name == "P15":
                continue
            chapter_words.append(sum(len(re.sub(r"(?s)```.*?```", "", path.read_text(encoding="utf-8")).split())
                                     for path in folder.glob("L*.md")))
        self.assertGreaterEqual(words, 4.9 * statistics.median(chapter_words))
        self.assertTrue(all(sum(body.count(f"{{{{figure:{fid}}}}}") for body in content) == 1
                            for fid in ("V49", "V50", "V51", "V52")))

    def test_missing_claim_anchor_and_reused_source_id_fail(self):
        _, manifest = build.load_manuscript()
        data = json.loads((build.ROOT / "manuscript/P15/C04/source_map.json").read_text(encoding="utf-8"))
        broken = copy.deepcopy(data)
        broken["claims"][0]["anchor"] = "không có neo này"
        with self.assertRaisesRegex(ValueError, "mất neo"):
            build.check_p15_c04_evidence(manifest, broken)
        broken = copy.deepcopy(data)
        broken["sources"]["R9"] = broken["sources"].pop("TC-01")
        with self.assertRaisesRegex(ValueError, "tái sử dụng"):
            build.check_p15_c04_evidence(manifest, broken)


if __name__ == "__main__":
    unittest.main()
