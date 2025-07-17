import csv
from pathlib import Path
from datetime import datetime

UTILS_DIR = Path(__file__).resolve().parent
FEEDBACK_FILE = UTILS_DIR / "feedback.csv"
LOG_FILE = UTILS_DIR / "usage_log.csv"


def append_row(path: Path, row: list[str]):
    path.parent.mkdir(parents=True, exist_ok=True)
    new_file = not path.exists()
    with path.open("a", newline="") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["timestamp"] + [f"col{i}" for i in range(1, len(row)+1)])
        writer.writerow([datetime.utcnow().isoformat()] + row)
