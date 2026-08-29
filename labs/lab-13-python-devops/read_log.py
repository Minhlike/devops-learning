import sys
import json
from pathlib import Path

LOG_FILE = Path("logs/app.log")

def read_log(path):
    if not path.exists():
        print(f"ERROR: File {path} khong ton tai")
        sys.exit(1)
    if not path.is_file():
        print(f"ERROR: {path} khong phai la file")
        sys.exit(1)
    return path.read_text()
def analyze_all_logs(log_dir):
    for path in log_dir.glob("*.log"):
        content = path.read_text()
        result = {
            "errors": content.count("ERROR"),
            "http_500": content.count("500")
        }
        
        print(
            f"{path.name} -> "
            f"ERROR: {result['errors']}, "
            f"HTTP 500: {result['http_500']}"
        )

def analyze_log(content):
    return {
	"errors": content.count("ERROR"),
	"http_500": content.count("500")
    }

content = read_log(LOG_FILE)
result = analyze_log(content)

with open("report.json", "w") as file:
    json.dump(result, file, indent=2)

print("Da tao report.json")

LOG_DIR = Path("logs")
analyze_all_logs(LOG_DIR)
