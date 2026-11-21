# Five-day quest log — factual record

The quest asks for a short entry for each of five days. **Development was accelerated:** the documented code-building, local testing, GitHub publication, security improvements, and CI work occurred on **2026-11-17**, rather than on five separate calendar days. The five entries below describe the five work checkpoints retrospectively; they do **not** pretend that one stage was completed on each consecutive date. A final deliverables review took place on **2026-11-21**.

## Day 1 checkpoint — Problem and intended outcome (2026-11-17)

Selected Option C, the Hiring Stall Alerter. Defined the core task as checking active hiring-board records for prolonged time in a stage and prioritizing recruiter follow-up. Chose ChatGPT-assisted Python + Streamlit instead of using only familiar no-code/low-code tools.

**Evidence:** Conversation prompts, `intent.md`, initial repository source.

## Day 2 checkpoint — First working tool (2026-11-17, accelerated)

ChatGPT generated the initial Streamlit dashboard, Python engine, sample CSV, launcher, and tests. The app launched locally on Windows with Python 3.13. With the reference date and threshold it showed 25 valid candidates, 22 active, 15 stalled, and 6 urgent.

**Evidence:** `app.py`, `engine.py`, `sample_hiring_board.csv`, `docs/dashboard.png`.

## Day 3 checkpoint — Manual verification (2026-11-17, accelerated)

Tested threshold adjustment, candidate search/filter, and CSV export on the local dashboard; all three were reported as passing. The original 14 automated engine tests passed in the development environment. Published the project to GitHub and removed an accidental duplicate directory.

**Evidence:** `tests/test_engine.py`, `README.md`, public GitHub history.

## Day 4 checkpoint — Security and CI revision (2026-11-17, accelerated)

Investigated formula-like values in downloaded CSVs. Added an export-specific mitigation and seven regression tests, bringing the suite to 21. Added a reviewer verification script and GitHub Actions. Early CI failures occurred when the workflow was pushed before its script; after completing the files and correcting an import-path error, full verification passed.

**Evidence:** `csv_export.py`, `tests/test_csv_export.py`, `scripts/reviewer_check.py`, `AI_BUILD_LOG.md`, and [passing Actions run](https://github.com/alvinjohn0417/hiring-stall-alerter/actions/runs/44113298195).

## Day 5 checkpoint — Submission-readiness review (2026-11-21)

Rechecked the full deliverables list. Confirmed working code, public README, and automated evidence. Identified additional named requirements—`intent.md`, `Final directive.md`, five-day log, and one-page unlearning reflection—and prepared those documents. The tool and career videos were **not yet recorded** at the time of this entry.

**Evidence:** These files and the repository's revision history.

## What the compressed timeline means

This was **not** five distinct, equally active development days. The activity is organized into five checkpoints for review while preserving the actual dates. If the evaluator requires contemporaneous logs from five separate days, this retrospective log does not substitute for them.
