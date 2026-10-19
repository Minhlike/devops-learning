"""Check arithmetic and fixture consistency; never connect to a database."""
import csv
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent


def rows(name):
    with (HERE / name).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def minute(value):
    return datetime.strptime(value, "%H:%M").hour * 60 + datetime.strptime(value, "%H:%M").minute


def audit():
    points = {row["event"]: minute(row["at"]) for row in rows("timeline.csv")}
    required = {"base_backup", "last_recoverable_commit", "failure", "detected", "restore_started", "replay_finished", "service_verified"}
    if set(points) != required or list(points.values()) != sorted(points.values()):
        raise ValueError("missing or unordered recovery events")
    target = points["last_recoverable_commit"]
    orders = rows("orders.csv")
    if len({r["order_id"] for r in orders}) != len(orders):
        raise ValueError("duplicate order ID")
    for row in orders:
        if (minute(row["committed_at"]) <= target) != (row["expected_restored"] == "true"):
            raise ValueError(f"restore expectation inconsistent for {row['order_id']}")
    return {"rpo_minutes": points["failure"] - target,
            "rto_minutes": points["service_verified"] - points["failure"],
            "db_only_minutes": points["replay_finished"] - points["failure"],
            "restored_ids": [r["order_id"] for r in orders if r["expected_restored"] == "true"],
            "reconcile_ids": [r["order_id"] for r in orders if r["expected_restored"] == "false"]}


if __name__ == "__main__":
    for key, value in audit().items():
        print(f"{key}={value}")
