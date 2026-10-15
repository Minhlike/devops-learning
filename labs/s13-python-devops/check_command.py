import subprocess
import sys

result = subprocess.run(
    ["ls", "-lh", "logs"],
    capture_output=True,
    text=True
)

print("RETURN CODE:", result.returncode)

if result.returncode != 0:
    print("COMMAND FAILED:")
    print(result.stderr)
    sys.exit(result.returncode)

print("COMMAND SUCCESS:")
print(result.stdout)
