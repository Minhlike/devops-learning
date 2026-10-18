"""Demo only: 'bad' deliberately ignores a failed step."""
import subprocess
import sys

if len(sys.argv) != 5:
    sys.exit("usage: script.py bad|checked ok|fail|slow probe.py workdir")
policy, mode, probe, work = sys.argv[1:]
if policy not in ("bad", "checked") or mode not in ("ok", "fail", "slow"):
    sys.exit(2)

for action in ("precheck", "apply_" + mode, "verify"):
    try:
        result = subprocess.run(
            [sys.executable, probe, action, work],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            timeout=0.3, check=False,
        )
        status = result.returncode
    except subprocess.TimeoutExpired:
        status = 124  # Nhãn của demo, không phải exit code của con.
    except OSError:
        status = 125  # Không khởi chạy được hoặc lỗi I/O của lời gọi.
    if status != 0:
        print(f"{action}: status={status}", file=sys.stderr)
        if policy == "checked":
            sys.exit(1)
print("DEPLOY_OK")
