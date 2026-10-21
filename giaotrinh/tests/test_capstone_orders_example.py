"""Run the same local capstone fixture command that the reader is given."""

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CapstoneOrdersExample(unittest.TestCase):
    def test_healthy_http_does_not_hide_data_and_rollback_failure(self):
        run = subprocess.run(
            [sys.executable, str(ROOT / "examples/capstone_orders.py")],
            cwd=ROOT, capture_output=True, text=True, timeout=15, check=True,
        )
        evidence = json.loads(run.stdout)
        events = evidence["events"]
        self.assertEqual(evidence["scope"], "local_fixture_only")
        self.assertEqual(len({event["request_id"] for event in events.values()}), 9)
        self.assertEqual((events["s2_health"]["status"], events["s2_write"]["status"],
                          events["s2_read"]["status"]), (200, 201, 200))
        self.assertEqual((events["s1_read"]["amount_cents"],
                          events["s2_read"]["amount_cents"]), (100, 201))
        self.assertEqual((events["rollback_old"]["status"],
                          events["rollback_new"]["status"]), (200, 409))
        self.assertEqual((events["restored_old"]["status"],
                          events["restored_new"]["status"]), (200, 404))
        self.assertEqual(events["rollback_new"]["error"], "unsupported_record_version")
        self.assertEqual(events["restored_new"]["error"], "order_missing")
        self.assertEqual(len(evidence["script_sha256"]), 64)
        self.assertEqual(len(evidence["backup_sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
