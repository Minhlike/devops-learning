"""Audit fictional incident counts, not a live incident replay."""
import csv
import re
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name, root=HERE):
    with (root / name).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def audit(root=HERE):
    rows = load("observations.csv", root)
    canary = [r for r in rows if r["window"] == "10:00-10:05"]
    if len(canary) != 2 or {r["release"] for r in canary} != {"v1", "v2"}:
        raise ValueError("canary comparison requires both releases in one window")
    for row in rows:
        valid, wrong, errors = (int(row[k]) for k in ("valid", "wrong_amount", "http_5xx"))
        if not 0 <= wrong <= valid or not 0 <= errors <= valid:
            raise ValueError("invalid incident counts")
    by_release = {r["release"]: r for r in canary}
    v1, v2 = by_release["v1"], by_release["v2"]
    samples = load("request_evidence.csv", root)
    if {r["request_id"] for r in samples} != {"K-26", "K-27", "K-28"}:
        raise ValueError("missing request-level evidence")
    timeline = {r["time"]: r for r in load("timeline.csv", root)}
    if timeline["10:16"]["epistemic_status"] != "verification needed":
        raise ValueError("post-mitigation verification has no request-level fixture")
    if timeline["10:22"]["epistemic_status"] != "reconciliation needed":
        raise ValueError("record-level reconciliation has not been performed")
    evidence_text = "\n".join((root / name).read_text(encoding="utf-8")
                              for name in ("timeline.csv", "manuscript.md", "answers.md", "visual.md"))
    prose = "\n".join((root / name).read_text(encoding="utf-8")
                      for name in ("manuscript.md", "answers.md"))
    if re.search(r"10:16[^.\n]{0,180}(?:đã xác (?:minh|nhận)|đã phục hồi|trả số tiền đúng)",
                 prose, flags=re.IGNORECASE):
        raise ValueError("pending 10:16 check cannot be described as verified")
    if re.search(r"\b30\s+(?:bản ghi|order)\b", evidence_text, flags=re.IGNORECASE):
        raise ValueError("30 wrong requests do not establish 30 distinct records")
    return {"v1_wrong_ratio": Fraction(int(v1["wrong_amount"]), int(v1["valid"])),
            "v2_wrong_ratio": Fraction(int(v2["wrong_amount"]), int(v2["valid"])),
            "all_wrong_ratio": Fraction(sum(int(r["wrong_amount"]) for r in canary),
                                        sum(int(r["valid"]) for r in canary)),
            "v2_traffic_share": Fraction(int(v2["valid"]),
                                         sum(int(r["valid"]) for r in canary)),
            "v2_samples_100x_low": all(int(r["input_cents"]) == 100 * int(r["stored_cents"])
                                       for r in samples if r["release"] == "v2"),
            "wrong_v2_requests": int(v2["wrong_amount"]),
            "distinct_affected_records": None,
            "post_mitigation_verified": False}


if __name__ == "__main__":
    for key, value in audit().items():
        print(f"{key}={value}")
