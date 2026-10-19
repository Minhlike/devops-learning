import csv
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

import verify

HERE = Path(__file__).resolve().parent


class IncidentArithmetic(unittest.TestCase):
    def test_canary_comparison(self):
        with (HERE / "observations.csv").open(encoding="utf-8", newline="") as stream:
            rows = [r for r in csv.DictReader(stream) if r["window"] == "10:00-10:05"]
        self.assertEqual(sum(int(r["valid"]) for r in rows), 1000)
        self.assertEqual(sum(int(r["wrong_amount"]) for r in rows), 31)
        self.assertEqual(verify.audit()["all_wrong_ratio"], Fraction(31, 1000))
        self.assertEqual(verify.audit()["v1_wrong_ratio"], Fraction(1, 900))
        self.assertEqual(verify.audit()["v2_wrong_ratio"], Fraction(3, 10))
        self.assertEqual(verify.audit()["v2_traffic_share"], Fraction(1, 10))
        self.assertTrue(verify.audit()["v2_samples_100x_low"])
        self.assertEqual(verify.audit()["wrong_v2_requests"], 30)
        self.assertIsNone(verify.audit()["distinct_affected_records"])
        self.assertFalse(verify.audit()["post_mitigation_verified"])

    def test_pending_step_cannot_be_marked_verified_without_evidence(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            for item in ("observations.csv", "request_evidence.csv", "timeline.csv",
                         "manuscript.md", "answers.md", "visual.md"):
                (root / item).write_bytes((HERE / item).read_bytes())
            timeline = root / "timeline.csv"
            timeline.write_text(timeline.read_text(encoding="utf-8").replace(
                "10:16,Cần thử request mới qua v1 và xác minh không còn v2 writer; chưa có kết quả,verification needed",
                "10:16,Cần thử request mới qua v1 và xác minh không còn v2 writer; chưa có kết quả,verified fictional observation"),
                encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "no request-level fixture"):
                verify.audit(root)

    def test_wrong_requests_cannot_become_distinct_records(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            for item in ("observations.csv", "request_evidence.csv", "timeline.csv",
                         "manuscript.md", "answers.md", "visual.md"):
                (root / item).write_bytes((HERE / item).read_bytes())
            timeline = root / "timeline.csv"
            timeline.write_text(timeline.read_text(encoding="utf-8").replace(
                "30 request v2 sai", "30 bản ghi v2 sai"), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "distinct records"):
                verify.audit(root)

    def test_pending_prose_cannot_claim_verified_request(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            for item in ("observations.csv", "request_evidence.csv", "timeline.csv",
                         "manuscript.md", "answers.md", "visual.md"):
                (root / item).write_bytes((HERE / item).read_bytes())
            manuscript = root / "manuscript.md"
            manuscript.write_text(manuscript.read_text(encoding="utf-8").replace(
                "Mốc 10:16 là **phép hậu kiểm cần làm**",
                "Mốc 10:16 đã xác minh request mới phục hồi"), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "cannot be described as verified"):
                verify.audit(root)


if __name__ == "__main__":
    unittest.main()
