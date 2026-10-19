"""Validate the hypothetical Ch19 trace, log correlation and timing."""

import csv
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRACE_ID = "4bf92f3577b34da6a3ce929d0e0e4736"


def validate_timeline(rows):
    by_alias = {row["alias"]: row for row in rows}
    if len(rows) != len(by_alias) or set(by_alias) != {"G", "A", "D", "U1", "U2"}:
        raise ValueError("missing or duplicate span alias")
    if len({row["span_id"] for row in rows}) != len(rows):
        raise ValueError("duplicate span id")
    for row in rows:
        if not re.fullmatch(r"[0-9a-f]{16}", row["span_id"]) or int(row["span_id"], 16) == 0:
            raise ValueError("invalid span id")
        if row["start_ms"] >= row["end_ms"]:
            raise ValueError("nonpositive span duration")
        if row["parent"] != "-":
            parent = by_alias.get(row["parent"])
            if not parent or not (parent["start_ms"] <= row["start_ms"]
                                  and row["end_ms"] <= parent["end_ms"]):
                raise ValueError("invalid parent interval")
    return by_alias


class TraceExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (ROOT / "examples/trace-ch19.csv").open(encoding="utf-8", newline="") as file:
            cls.rows = [{key: int(value) if key in ("start_ms", "end_ms") else value
                         for key, value in row.items()} for row in csv.DictReader(file)]
        cls.spans = validate_timeline(cls.rows)
        cls.logs = json.loads((ROOT / "examples/logs-ch19.json").read_text(encoding="utf-8"))

    def test_latency_and_retry_are_consistent(self):
        duration = lambda alias: self.spans[alias]["end_ms"] - self.spans[alias]["start_ms"]
        self.assertEqual([duration(alias) for alias in ("G", "A", "D", "U1", "U2")],
                         [420, 393, 250, 50, 40])
        self.assertEqual(sum(duration(alias) for alias in self.spans), 1153)
        self.assertEqual(self.spans["U2"]["start_ms"] - self.spans["U1"]["end_ms"], 10)
        self.assertEqual(self.spans["U2"]["end_ms"] - self.spans["U1"]["start_ms"], 100)
        self.assertEqual(self.spans["U1"]["status"], "ERROR")
        self.assertEqual(self.spans["A"]["status"], "UNSET")

    def test_logs_link_to_existing_spans_and_events(self):
        span_ids = {row["span_id"]: row for row in self.rows}
        self.assertEqual(len(self.logs), 3)
        self.assertEqual({log["request_id"] for log in self.logs}, {"req-17"})
        for log in self.logs:
            self.assertEqual(log["trace_id"], TRACE_ID)
            self.assertIn(log["span_id"], span_ids)
            t = int(log["time"].split(".")[1][:3])
            span = span_ids[log["span_id"]]
            self.assertLessEqual(span["start_ms"], t)
            self.assertLessEqual(t, span["end_ms"])
            self.assertTrue(log["event"])
            self.assertNotIn("token", json.dumps(log).lower())
        self.assertEqual(self.logs[1]["event"], "upstream_timeout")
        self.assertEqual(self.logs[2]["http_status"], 200)

    def test_broken_parent_is_rejected(self):
        rows = [row.copy() for row in self.rows]
        rows[-1]["parent"] = "D"
        with self.assertRaisesRegex(ValueError, "invalid parent interval"):
            validate_timeline(rows)

    def test_traceparent_matches_gateway_span(self):
        chapter = (ROOT / "chapters/19-logs-traces-opentelemetry.md").read_text(encoding="utf-8")
        match = re.search(r'traceparent: ([0-9a-f]{2})-([0-9a-f]{32})-([0-9a-f]{16})-([0-9a-f]{2})', chapter)
        self.assertIsNotNone(match)
        self.assertEqual(match.groups(), ("00", TRACE_ID, self.spans["G"]["span_id"], "01"))


if __name__ == "__main__":
    unittest.main()
