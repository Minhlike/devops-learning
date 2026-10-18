"""Run the same state assertions for Python and an available Go toolchain."""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROBE = ROOT / "examples" / "orchestration_probe.py"
PYTHON = ROOT / "examples" / "orchestrate_python.py"
GO_FILES = [ROOT / "examples" / name for name in
            ("orchestrate_go.go", "orchestrate_go_step.go")]


def check_matrix(test, command, *, go=False):
    cases = [
        ("checked", "ok", 0, "ready\n", [], False),
        ("bad", "ok", 0, "ready\n", [], False),
        ("bad", "fail", 0, "partial\n", ["apply_fail: EXIT 7", "verify: EXIT 8"], True),
        ("checked", "fail", 1, "partial\n", ["apply_fail: EXIT 7"], False),
        ("bad", "slow", 0, "partial\n", ["apply_slow: TIMEOUT", "verify: EXIT 8"], True),
        ("checked", "slow", 1, "partial\n", ["apply_slow: TIMEOUT"], False),
    ]
    for policy, mode, exit_code, state, errors, false_success in cases:
        with test.subTest(policy=policy, mode=mode):
            with tempfile.TemporaryDirectory(prefix=".qa-orchestrate-", dir=ROOT) as tmp:
                work = Path(tmp)
                (work / ".demo-only").write_text("demo\n", encoding="utf-8")
                env = os.environ.copy()
                # Larger than the old 0.3 s whole-process deadline.
                if policy == "checked" and mode == "ok":
                    env["DEMO_STARTUP_DELAY"] = "0.7"
                else:
                    env.pop("DEMO_STARTUP_DELAY", None)
                args = [*command, policy, mode]
                if go:
                    args.append(sys.executable)
                args.extend((PROBE, work))
                result = subprocess.run(
                    args,
                    capture_output=True, text=True, timeout=20, env=env,
                )
                test.assertEqual(result.returncode, exit_code, result.stderr)
                test.assertEqual((work / "state.txt").read_text(encoding="utf-8"), state)
                test.assertEqual(result.stdout.strip() == "DEPLOY_OK", exit_code == 0)
                for error in errors:
                    test.assertIn(error, result.stderr)
                if not false_success and policy == "checked":
                    test.assertNotIn("verify:", result.stderr)


class PythonOrchestrationTests(unittest.TestCase):
    def test_all_branches_and_final_state(self):
        check_matrix(self, [sys.executable, str(PYTHON)])

    def test_probe_rejects_unmarked_directory(self):
        with tempfile.TemporaryDirectory(prefix=".qa-orchestrate-", dir=ROOT) as tmp:
            work = Path(tmp)
            result = subprocess.run(
                [sys.executable, PROBE, "apply_ok", work],
                capture_output=True, text=True, timeout=5,
            )
            self.assertEqual(result.returncode, 2)
            self.assertFalse((work / "state.txt").exists())


class GoOrchestrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        go = os.environ.get("DEVOPS_GO_BIN") or shutil.which("go")
        if not go:
            raise unittest.SkipTest("Go toolchain unavailable")
        cls.scratch = tempfile.TemporaryDirectory(prefix=".qa-go-", dir=ROOT)
        scratch = Path(cls.scratch.name)
        binary = scratch / ("orchestrate.exe" if os.name == "nt" else "orchestrate")
        env = os.environ.copy()
        env.update({"GOCACHE": str(scratch / "cache"),
                    "GOPATH": str(scratch / "gopath"),
                    "GOTMPDIR": str(scratch), "GOTOOLCHAIN": "local",
                    "GOTELEMETRY": "off", "GO111MODULE": "off"})
        result = subprocess.run([go, "build", "-o", binary, *GO_FILES],
                                capture_output=True, text=True, timeout=120, env=env)
        if result.returncode:
            cls.scratch.cleanup()
            raise AssertionError(result.stderr)
        cls.binary = binary

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "scratch"):
            cls.scratch.cleanup()

    def test_all_branches_and_final_state(self):
        check_matrix(self, [str(self.binary)], go=True)


if __name__ == "__main__":
    unittest.main()
