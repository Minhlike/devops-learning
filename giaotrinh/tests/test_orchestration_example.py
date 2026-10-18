"""Protect the chapter's false-success and checked-failure evidence."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROBE = ROOT / "examples" / "orchestration_probe.py"
PYTHON = ROOT / "examples" / "orchestrate_python.py"


class OrchestrationExampleTests(unittest.TestCase):
    def test_failure_is_visible_but_bad_policy_reports_success(self):
        with tempfile.TemporaryDirectory(prefix=".qa-orchestrate-", dir=ROOT) as tmp:
            work = Path(tmp)
            (work / ".demo-only").write_text("demo\n", encoding="utf-8")
            bad = subprocess.run(
                [sys.executable, PYTHON, "bad", "fail", PROBE, work],
                capture_output=True, text=True, timeout=5,
            )
            self.assertEqual((bad.returncode, bad.stdout.strip()), (0, "DEPLOY_OK"))
            self.assertIn("apply_fail: status=7", bad.stderr)
            self.assertIn("verify: status=8", bad.stderr)
            self.assertEqual((work / "state.txt").read_text(encoding="utf-8"),
                             "partial\n")

            checked = subprocess.run(
                [sys.executable, PYTHON, "checked", "fail", PROBE, work],
                capture_output=True, text=True, timeout=5,
            )
            self.assertEqual(checked.returncode, 1)
            self.assertNotIn("DEPLOY_OK", checked.stdout)
            self.assertIn("apply_fail: status=7", checked.stderr)
            self.assertNotIn("verify:", checked.stderr)

    def test_probe_rejects_unmarked_directory(self):
        with tempfile.TemporaryDirectory(prefix=".qa-orchestrate-", dir=ROOT) as tmp:
            work = Path(tmp)
            result = subprocess.run(
                [sys.executable, PROBE, "apply_ok", work],
                capture_output=True, text=True, timeout=5,
            )
            self.assertEqual(result.returncode, 2)
            self.assertFalse((work / "state.txt").exists())


if __name__ == "__main__":
    unittest.main()
