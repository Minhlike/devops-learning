import unittest
from pathlib import Path
import csv
from verify import audit


class RecoveryArithmetic(unittest.TestCase):
    def test_objectives_and_orders(self):
        with (Path(__file__).parent / "timeline.csv").open(encoding="utf-8", newline="") as f:
            times = {r["event"]: r["at"] for r in csv.DictReader(f)}
        def minutes(s):
            h, m = map(int, s.split(":"))
            return h * 60 + m
        self.assertEqual(minutes(times["failure"]) - minutes(times["last_recoverable_commit"]), 8)
        self.assertEqual(minutes(times["service_verified"]) - minutes(times["failure"]), 37)
        self.assertEqual(minutes(times["replay_finished"]) - minutes(times["failure"]), 27)
        self.assertEqual(audit()["restored_ids"], ["O-101", "O-102", "O-103"])
        self.assertEqual(audit()["reconcile_ids"], ["O-104", "O-105"])


if __name__ == "__main__":
    unittest.main()
