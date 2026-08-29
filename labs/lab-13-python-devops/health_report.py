import sys
import json
import subprocess

from pathlib import Path

LOG_FILE = Path("logs/app.log")
if not LOG_FILE.exists():
    print(f"ERROR: File {LOG_FILE} khong ton tai")
    sys.exit(1)
content = LOG_FILE.read_text()
ERRORS = content.count("ERROR")
HTTP_500 = content.count("500")
try:
    command = subprocess.run(
        ["df", "-h", "/"],
        capture_output=True,
        text=True
    )
except FileNotFoundError:
    print("ERROR: Command khong ton tai")
    sys.exit(1)

print("RETURN CODE:", command.returncode)

if command.returncode != 0:
    print("COMMAND FAILED:")
    print(command.stderr)
    sys.exit(command.returncode)
report = {
    "log_errors": ERRORS,
    "http_500": HTTP_500,
    "disk_command_status": "COMMAND SUCCESS"
}
with open("health_report.json", "w") as file:
    json.dump(report, file, indent=3)

print("Health report created")
