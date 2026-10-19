"""Check a hypothetical load fixture; never produce benchmark claims."""
import csv
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent


def audit():
    with (HERE / "load.csv").open(encoding="utf-8", newline="") as stream:
        rows = {r["phase"]: r for r in csv.DictReader(stream)}
    if set(rows) != {"A", "B", "C"}:
        raise ValueError("need A, B and C")
    result = {}
    for phase, row in rows.items():
        duration, offered, completed, delta = (int(row[k]) for k in ("duration_s", "offered_rps", "completed_rps", "queue_delta"))
        if duration <= 0 or offered < 0 or completed < 0 or row["hidden_drop_timeout_retry"] != "false":
            raise ValueError("fixture conditions violated")
        if (offered - completed) * duration != delta:
            raise ValueError(f"queue accounting failed for {phase}")
        if phase in {"A", "B"}:
            if delta != 0:
                raise ValueError("Little's Law fixture must be stable")
            result[f"L_{phase}"] = Fraction(completed * int(row["mean_latency_ms"]), 1000)
    result["C_queue_growth"] = int(rows["C"]["queue_delta"])
    result["forecast_peak_rps"] = Fraction(int(rows["B"]["offered_rps"])) * Fraction(5, 4)
    result["C_stable"] = int(rows["C"]["queue_delta"]) == 0
    return result


if __name__ == "__main__":
    for key, value in audit().items():
        print(f"{key}={value}")
