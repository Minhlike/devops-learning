"""Independent arithmetic checks for the illustrative C01 fixture."""
import csv
import unittest
from fractions import Fraction
from pathlib import Path

import verify

HERE = Path(__file__).resolve().parent


class SloArithmetic(unittest.TestCase):
    def test_monthly_population_and_budget(self):
        with (HERE / "monthly.csv").open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))
        valid = sum(int(row["valid"]) for row in rows)
        bad = sum(int(row["bad"]) for row in rows)
        self.assertEqual((valid, bad), (1_000_000, 700))
        self.assertEqual(Fraction(valid - bad, valid), Fraction(9993, 10000))
        self.assertEqual(Fraction(1, 1000) * valid - bad, 300)
        self.assertEqual(verify.audit()["remaining"], 300)

    def test_windows_and_multiwindow_gate(self):
        with (HERE / "five_minute.csv").open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))
        last_hour = Fraction(sum(int(r["bad"]) for r in rows),
                             sum(int(r["valid"]) for r in rows))
        last_five = Fraction(int(rows[-1]["bad"]), int(rows[-1]["valid"]))
        self.assertEqual(last_hour, Fraction(63, 4000))
        self.assertEqual(last_five, Fraction(3, 50))
        self.assertEqual((last_hour * 1000, last_five * 1000),
                         (Fraction(63, 4), 60))
        self.assertTrue(last_hour > Fraction(144, 10000) and
                        last_five > Fraction(144, 10000))
        self.assertTrue(verify.audit()["page_1h_5m"])

    def test_missing_last_bucket_is_not_zero_bad(self):
        with (HERE / "five_minute.csv").open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))
        visible = rows[:-1]
        self.assertEqual(sum(int(r["bad"]) for r in visible), 129)
        self.assertNotEqual(sum(int(r["bad"]) for r in visible),
                            verify.audit()["error_1h"] * 12_000)


if __name__ == "__main__":
    unittest.main()
