"""Audit illustrative SLO counts; standard library only, no network or production access."""
from __future__ import annotations

import csv
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLO = Fraction(999, 1000)


def read_counts(name: str) -> list[tuple[int, int]]:
    with (HERE / name).open(encoding="utf-8", newline="") as stream:
        rows = [(int(r["valid"]), int(r["bad"])) for r in csv.DictReader(stream)]
    if not rows or any(valid <= 0 or not 0 <= bad <= valid for valid, bad in rows):
        raise ValueError(f"invalid event counts in {name}")
    return rows


def ratio(rows: list[tuple[int, int]]) -> Fraction:
    return Fraction(sum(bad for _, bad in rows), sum(valid for valid, _ in rows))


def audit() -> dict[str, Fraction | int | bool]:
    five = read_counts("five_minute.csv")
    month = read_counts("monthly.csv")
    if len(five) != 12 or five != [(1000, 1)] * 9 + [(1000, 60)] * 3:
        raise ValueError("unexpected 5-minute fixture")
    if month[-1] != (sum(v for v, _ in five), sum(b for _, b in five)):
        raise ValueError("monthly last hour does not match 5-minute data")
    valid = sum(v for v, _ in month)
    bad = sum(b for _, b in month)
    allowance = valid * (1 - SLO)
    if allowance.denominator != 1:
        raise ValueError("fractional-event budget requires explicit rounding policy")
    hour = ratio(five)
    short = ratio(five[-1:])
    threshold = Fraction(144, 10) * (1 - SLO)
    return {"valid_30d": valid, "bad_30d": bad, "good_30d": valid - bad,
            "sli_30d": 1 - ratio(month), "allowance": int(allowance),
            "remaining": int(allowance) - bad, "error_1h": hour,
            "error_5m": short, "burn_1h": hour / (1 - SLO),
            "burn_5m": short / (1 - SLO),
            "page_1h_5m": hour > threshold and short > threshold}


if __name__ == "__main__":
    for key, value in audit().items():
        print(f"{key}={value}")
