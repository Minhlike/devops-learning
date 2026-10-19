"""Check the worked Ch18 dataset and its matching exposition snapshot."""

import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIELDS = ("ok", "err", "le_0_1", "le_0_5", "le_1", "le_inf", "cpu_s")


def validate_rows(rows):
    grouped = {instance: sorted((row for row in rows if row["instance"] == instance),
                                key=lambda row: row["t_s"]) for instance in ("a", "b")}
    for instance, series in grouped.items():
        if [row["t_s"] for row in series] != [0, 60, 120, 180]:
            raise ValueError(f"timestamps for {instance}")
        for previous, current in zip(series, series[1:]):
            if any(current[field] < previous[field] for field in FIELDS):
                raise ValueError(f"counter decrease for {instance}")
        for row in series:
            if not (row["le_0_1"] <= row["le_0_5"] <= row["le_1"] <= row["le_inf"]):
                raise ValueError(f"noncumulative bucket for {instance}")
            if row["le_inf"] != row["ok"] + row["err"]:
                raise ValueError(f"count mismatch for {instance}")
    return grouped


class MetricsExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (ROOT / "examples/metrics-ch18.csv").open(encoding="utf-8", newline="") as file:
            cls.rows = [{key: value if key == "instance" else int(value)
                         for key, value in row.items()} for row in csv.DictReader(file)]
        cls.grouped = validate_rows(cls.rows)

    def test_rates_ratio_cpu_and_classic_histogram(self):
        first = [series[1] for series in self.grouped.values()]
        last = [series[-1] for series in self.grouped.values()]
        delta = lambda field: sum(b[field] - a[field] for a, b in zip(first, last))
        self.assertEqual(delta("err"), 24)
        self.assertEqual(delta("le_inf"), 240)
        self.assertAlmostEqual(delta("err") / 120, 0.2)
        self.assertAlmostEqual(delta("err") / delta("le_inf"), 0.1)
        self.assertAlmostEqual(delta("cpu_s") / 120, 0.4)
        self.assertEqual([delta(field) for field in ("le_0_1", "le_0_5", "le_1", "le_inf")],
                         [80, 180, 232, 240])
        p95 = 0.5 + (0.95 * 240 - 180) / (232 - 180) * 0.5
        self.assertAlmostEqual(p95, 0.9615384615384616)

    def test_snapshot_matches_final_counter_values(self):
        snapshot = (ROOT / "examples/metrics-ch18.prom").read_text(encoding="utf-8")
        row = self.grouped["a"][-1]
        for status, field in (("2xx", "ok"), ("5xx", "err")):
            self.assertIn(f'http_requests_total{{status_class="{status}"}} {row[field]}', snapshot)
        for boundary, field in (("0.1", "le_0_1"), ("0.5", "le_0_5"),
                                ("1", "le_1"), ("+Inf", "le_inf")):
            self.assertIn(f'http_request_duration_seconds_bucket{{le="{boundary}"}} {row[field]}', snapshot)
        self.assertIn(f'http_request_duration_seconds_count {row["le_inf"]}', snapshot)
        self.assertIn(f'process_cpu_seconds_total {row["cpu_s"]}', snapshot)
        self.assertNotIn('instance=', snapshot)
        self.assertNotIn('\nup{', snapshot)

    def test_malformed_histogram_is_rejected(self):
        rows = [row.copy() for row in self.rows]
        rows[-1]["le_0_5"] = rows[-1]["le_1"] + 1
        with self.assertRaisesRegex(ValueError, "noncumulative bucket"):
            validate_rows(rows)


if __name__ == "__main__":
    unittest.main()
