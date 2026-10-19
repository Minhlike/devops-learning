import unittest
import csv
import tempfile
from fractions import Fraction
from pathlib import Path
from verify import audit


class LoadArithmetic(unittest.TestCase):
    def test_fixture_calculations(self):
        with (Path(__file__).parent / "load.csv").open(encoding="utf-8", newline="") as stream:
            points = list(csv.DictReader(stream))
        self.assertEqual([p["phase"] for p in points], ["A", "B", "C"])
        a, b, c = points
        self.assertEqual(Fraction(int(a["completed_rps"]) * int(a["mean_latency_ms"]), 1000), 12)
        self.assertEqual(Fraction(int(b["completed_rps"]) * int(b["mean_latency_ms"]), 1000), 40)
        self.assertEqual((int(c["offered_rps"]) - int(c["completed_rps"])) * int(c["duration_s"]), 2400)
        self.assertEqual(Fraction(int(b["offered_rps"])) * Fraction(125, 100), 200)
        self.assertEqual(audit(), {"L_A": 12, "L_B": 40, "C_outstanding_growth": 2400,
                                   "forecast_peak_rps": 200, "C_stable": False})

    def test_accounting_cannot_be_labeled_queue_only(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            source = (Path(__file__).parent / "load.csv").read_text(encoding="utf-8")
            (root / "load.csv").write_text(source.replace("outstanding_delta", "queue_delta"),
                                           encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "not a queue-only measurement"):
                audit(root)


if __name__ == "__main__":
    unittest.main()
