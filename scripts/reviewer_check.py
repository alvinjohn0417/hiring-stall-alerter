"""Reproducible reference checks for a reviewer-visible CI run."""

from __future__ import annotations

import csv
from datetime import date
from io import StringIO
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from csv_export import export_followups_csv
from engine import assess_candidates, read_candidates, summarize

AS_OF = date(2026, 11, 17)
THRESHOLD = 7


def main() -> None:
    raw = (ROOT / "sample_hiring_board.csv").read_bytes()
    candidates, warnings = read_candidates(raw, AS_OF)
    alerts = assess_candidates(candidates, THRESHOLD, AS_OF)
    metrics = summarize(candidates)
    observed = {
        "valid_candidates": metrics["all"],
        "active_candidates": metrics["active"],
        "stalled_candidates": len(alerts),
        "urgent_followups": sum(a.priority == "Urgent" for a in alerts),
        "input_warnings": len(warnings),
    }
    expected = {
        "valid_candidates": 25, "active_candidates": 22,
        "stalled_candidates": 15, "urgent_followups": 6,
        "input_warnings": 0,
    }
    if observed != expected:
        raise AssertionError(f"Reference dataset mismatch: expected {expected}, got {observed}")

    csv_text = export_followups_csv([alert.for_export() for alert in alerts]).decode("utf-8-sig")
    rows = list(csv.DictReader(StringIO(csv_text)))
    if len(rows) != 15:
        raise AssertionError(f"Expected 15 export rows; found {len(rows)}")

    injected = (
        "candidate_id,candidate_name,role,stage,last_stage_change,owner\n"
        "SEC01,=1+1,Engineer,Interview,2026-11-01,Reviewer\n"
    ).encode("utf-8")
    bad_rows, issues = read_candidates(injected, AS_OF)
    if issues or len(bad_rows) != 1:
        raise AssertionError(f"Security fixture parsing failed: {issues}")
    security_alerts = assess_candidates(bad_rows, THRESHOLD, AS_OF)
    safe_result = export_followups_csv([a.for_export() for a in security_alerts])
    parsed = list(csv.DictReader(StringIO(safe_result.decode("utf-8-sig"))))
    if parsed[0]["Candidate"] != "\t=1+1":
        raise AssertionError("Formula-like candidate field was not neutralized")

    output = ROOT / "reviewer_results"
    output.mkdir(exist_ok=True)
    (output / "reference_followups_safe.csv").write_bytes(csv_text.encode("utf-8-sig"))
    (output / "formula_input_check_safe.csv").write_bytes(safe_result)
    lines = [
        "# Reviewer verification report", "",
        "Generated from the included fictional data by `scripts/reviewer_check.py`.", "",
        "| Check | Expected | Observed |", "|---|---:|---:|",
        *[f"| {name} | {expected[name]} | {observed[name]} |" for name in expected],
        "| Safe exported follow-up rows | 15 | 15 |",
        "| Formula-like input `=1+1` | tab-prefixed in CSV | tab-prefixed in CSV |",
        "", "Note: CI checks CSV contents; it does not execute Microsoft Excel.",
        "Manual Excel save/re-open testing remains necessary for app-specific behavior.",
    ]
    (output / "verification_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("PASS: reference metrics", observed)
    print("PASS: safe CSV export row count", len(rows))
    print("PASS: formula-like input is neutralized in raw exported CSV")
    print("Report generated at reviewer_results/verification_report.md")


if __name__ == '__main__':
    main()
