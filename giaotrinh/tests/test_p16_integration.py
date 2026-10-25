"""Publication migration and artifact identity contracts for Part XVI."""

import copy
import json
import re
import unittest

from giaotrinh.scripts import build


class Part16Integration(unittest.TestCase):
    def test_architecture_migration_and_exercise_ownership(self):
        tree, manifest = build.load_manuscript()
        self.assertEqual((len(tree["parts"]),
                          sum(len(p["chapters"]) for p in tree["parts"]),
                          len(manifest["lessons"])), (16, 64, 202))
        chapters = tree["parts"][-1]["chapters"]
        self.assertEqual([len(ch["lessons"]) for ch in chapters], [4] * 6)
        self.assertTrue(all(ch["id"].startswith("P16.C") for ch in chapters))
        self.assertFalse(any(k.startswith("P15.C04") for k in manifest["lessons"]))
        mapping = json.loads((build.ROOT / "architecture/p15_c04_to_p16.json")
                             .read_text(encoding="utf-8"))["lesson_map"]
        archived = json.loads((build.ROOT / "architecture/history_p15_c04/manifest_rows.json")
                              .read_text(encoding="utf-8"))["lessons"]
        self.assertEqual(set(mapping), set(archived))
        for old_id, entry in mapping.items():
            row = manifest["lessons"][entry["primary"]]
            self.assertEqual(row["qa"][0]["question"], archived[old_id]["qa"][0]["question"])
            self.assertEqual(row["qa"][0]["answer"], archived[old_id]["qa"][0]["answer"])
        for ch in chapters:
            for lesson in ch["lessons"]:
                row = manifest["lessons"][lesson["id"]]
                self.assertEqual(len(row["qa"]), 1)
                self.assertEqual(row["status"], "reviewed")
                self.assertEqual(row["verification"], "author_verified_p16")
                self.assertTrue((build.ROOT / row["content"]).is_file())

    def test_source_and_figure_owners_fail_closed(self):
        _, manifest = build.load_manuscript()
        data = json.loads((build.ROOT / "manuscript/P16/source_map.json")
                          .read_text(encoding="utf-8"))
        broken = copy.deepcopy(data)
        broken["claims"][0]["anchor"] = "neo không tồn tại"
        with self.assertRaisesRegex(ValueError, "mất neo"):
            build.check_p16_evidence(manifest, broken)
        broken = copy.deepcopy(data)
        broken["sources"]["R9"] = broken["sources"].pop("TC-01")
        with self.assertRaisesRegex(ValueError, "tái sử dụng"):
            build.check_p16_evidence(manifest, broken)
        broken = copy.deepcopy(data)
        broken["sources"]["TC-01"]["url"] = "https://example.invalid/changed"
        with self.assertRaisesRegex(ValueError, "đổi ID hoặc URL"):
            build.check_p16_evidence(manifest, broken)
        all_bodies = [(build.ROOT / row["content"]).read_text(encoding="utf-8")
                      for lid, row in manifest["lessons"].items() if lid.startswith("P16.")]
        for fid in (f"V{i}" for i in range(49, 67)):
            self.assertEqual(sum(body.count("{{figure:" + fid + "}}")
                                 for body in all_bodies), 1, fid)

    def test_build_once_and_digest_deploy_contract(self):
        root = build.ROOT / "examples/orders_toolchain"
        workflow = (root / "ci.yml").read_text(encoding="utf-8")
        verify, publish = workflow.split("  publish:", 1)
        self.assertEqual(len(re.findall(r"(?m)^\s+docker build ", verify)), 1)
        self.assertNotIn("docker build ", publish)
        self.assertIn("docker save", verify)
        self.assertIn("docker load", publish)
        self.assertIn("image-id.txt", publish)
        deploy = (root / "deploy.compose.yaml").read_text(encoding="utf-8")
        self.assertIn("@sha256", deploy)
        self.assertNotIn("build:", deploy)
        lab = (root / "local_pipeline.py").read_text(encoding="utf-8")
        for token in ('"pull"', "runtime_image_ref", "record_before_failure",
                      "independent_restore", "registry_manifest_digest"):
            self.assertIn(token, lab)


if __name__ == "__main__":
    unittest.main()
