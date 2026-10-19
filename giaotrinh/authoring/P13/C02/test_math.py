import csv
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


if __name__ == "__main__":
    unittest.main()
