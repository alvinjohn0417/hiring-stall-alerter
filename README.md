# Hiring Stall Alerter

[![Reviewer verification](https://github.com/alvinjohn0417/hiring-stall-alerter/actions/workflows/reviewer-verification.yml/badge.svg)](https://github.com/alvinjohn0417/hiring-stall-alerter/actions/workflows/reviewer-verification.yml)

**A CSV-based hiring pipeline follow-up dashboard, built with ChatGPT-assisted Python and Streamlit.**

The app finds candidates who have stayed in an *active* hiring stage at or beyond a chosen threshold, orders the follow-up queue by clear rules, explains each flag, and recommends a next step for a recruiter to review. It does **not** make hiring decisions or send messages.

![Hiring Stall Alerter dashboard, using fictional candidates](docs/dashboard.png)

*Partial screenshot of the locally verified dashboard (scrolled view).*

## Demo result

With the included fictional data, **Analyze as of = 2026-11-17** and **threshold = 7 days**, the dashboard produces:

| Metric | Result |
|---|---:|
| Valid candidates | 25 |
| Active candidates | 22 |
| Flagged for follow-up | 15 |
| Urgent follow-ups | 6 |

These values were verified on a Windows PC running **Python 3.13** and Streamlit. The screenshot is from the locally running app; it is not a public deployment.

## Features

- Load a ready-to-use 25-candidate fictional CSV or upload another CSV.
- Select an analysis date and a stall threshold of 1–30 days.
- Exclude closed stages: Hired, Rejected, Withdrawn, Closed, Declined, and Not selected.
- Flag stalled candidates, explain *why*, and rank them Urgent / High / Follow up.
- Provide a stage-specific next action for **human review**.
- Search by candidate, role, owner, or stage; filter by priority.
- Download the displayed follow-up queue as spreadsheet-oriented CSV, with formula-like text neutralized in export.
- Warn about malformed input, invalid/future dates, and duplicate candidate IDs.

## Quick start: Windows

You need **Python 3.11 or newer** (Python 3.13 was used in the verified local run).

1. Download or clone this repository.
2. Open the project folder.
3. Double-click **`start_windows.bat`**. On first launch, it creates `.venv` and installs the dependencies.
4. Open **http://localhost:8501** if a browser does not open automatically.
5. Keep the Command Prompt window running while using the app.

### Manual start (PowerShell)

From **inside the project directory**:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

If `py` is unavailable, substitute `python -m venv .venv` in the first command.

## How to test the app

1. Choose **Try example data**.
2. Set the analysis date to `2026-11-17` and the threshold to **7** days.
3. Check the four reference metrics above.
4. Change the threshold to **10**; the stalled count should decrease. Restore it to **7**.
5. Search for `Maria Santos`, clear the search, and try the priority filter.
6. Download the follow-up CSV and open it in Excel.
7. As an extra test, upload a modified sample CSV containing an invalid `last_stage_change` date and check that the app reports a warning.

The first six checks were performed during the project walkthrough; the malformed-input UI example is a suggested follow-up check. Input validation is also covered by the automated tests.

## CSV schema

The file must include these column headers (in any order):

```csv
candidate_id,candidate_name,role,stage,last_stage_change,owner
C001,Alex Torres,Support Specialist,Interview,2026-11-08,Robin Cruz
```

- Dates: `YYYY-MM-DD`.
- Candidate IDs must be unique.
- `candidate_id`, `candidate_name`, `stage`, and `last_stage_change` cannot be blank; `role` and `owner` may be blank.
- Extra columns are ignored. Use CSV UTF-8 when exporting from Excel.

You can use `sample_hiring_board.csv` as your upload template. It contains **fictional data** only.

## How the rules work

```text
CSV data + analysis date + threshold
    ↓
Validate the rows and skip invalid records with warnings
    ↓
Exclude candidates in closed stages
    ↓
Days in stage = analysis date − last stage change
    ↓
Flag candidate if days in stage >= threshold
    ↓
Rank and explain each follow-up
    ↓
Human reviews the result → optional CSV export
```

**Priority rules:**

- **Urgent** — at least **7 days beyond** the threshold, or in Offer/Final Interview at least **3 days beyond** it.
- **High** — at least **3 days beyond** the threshold, or in Offer/Final Interview at the threshold.
- **Follow up** — every other candidate at or beyond the threshold.

Within each priority group, the app orders candidates by days beyond the limit, with hiring-stage precedence used in scoring. Recommendations come from a rule-based lookup by stage, **not from an LLM at runtime**. No email, ATS integration, or external AI API is called.

## Project files

| File | Purpose |
|---|---|
| `app.py` | Streamlit user interface |
| `csv_export.py` | Spreadsheet-oriented CSV export safety boundary |
| `sample_security_check.csv` | Fictional formula-like candidate names for manual export testing |
| `tests/test_csv_export.py` | Export encoding and spreadsheet formula safety regression tests |
| `scripts/reviewer_check.py` | Reference scenario verification and report generation |
| `.github/workflows/reviewer-verification.yml` | GitHub Actions tests and evidence report; manual reruns require write access |
| `engine.py` | CSV checks, date calculations, priorities, actions |
| `sample_hiring_board.csv` | Fictional sample hiring board |
| `sample_followup_report.csv` | Reference output for the 2026-11-17 example |
| `tests/test_engine.py` | Automated tests of the core logic |
| `start_windows.bat` | Windows launcher |
| `AI_BUILD_LOG.md` | Actual AI-assisted development and testing record |
| `WALKTHROUGH.md` | Reproducible local demo and test procedure |
| `docs/dashboard.png` | Screenshot of the locally verified dashboard |

## Quest documentation

The following artifacts accompany the working source code:

| Document | Purpose |
|---|---|
| [`intent.md`](intent.md) | Retrospective statement of problem, scope, success criteria, and AI-first intent |
| [`Final directive.md`](Final%20directive.md) | Current engineering handoff directive and safeguards |
| [`FIVE_DAY_LOG.md`](FIVE_DAY_LOG.md) | Five checkpoint entries with actual activity dates, transparently noting the accelerated build |
| [`UNLEARNED.md`](UNLEARNED.md) | One-page reflection on working-method changes and remaining gaps |
| [`AI_BUILD_LOG.md`](AI_BUILD_LOG.md) | Detailed observed prompts, tests, failures, and corrections |

The challenge also requires two **separate** recordings: a tool demonstration (maximum five minutes) and a career path/career leverage video (maximum five minutes). These are submitted as video links, not part of the executable source.

## Run the automated tests

From inside this project directory:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

**21 automated tests passed in the development environment**: 14 original engine tests plus 7 CSV export regression tests. The reviewer workflow re-runs these tests and verifies the sample data. Three original manual UI checks were completed on Windows: threshold adjustment, search/filter, and CSV export. The updated spreadsheet-safety behavior still requires manual Excel testing.

## AI-first approach

ChatGPT was used to break down the task, generate the first Python/Streamlit codebase and tests, explain local setup, interpret actual screenshots, and plan validation. **AI assisted development; AI does not decide the runtime results.** This was an intentional shift from visual workflow-building toward a standalone, AI-assisted coded application.

The [`AI_BUILD_LOG.md`](AI_BUILD_LOG.md) records the development timeline, the respective roles of ChatGPT and the developer, and the results that were verified.

## Reviewer verification — GitHub Actions

The [Reviewer verification workflow](https://github.com/alvinjohn0417/hiring-stall-alerter/actions/workflows/reviewer-verification.yml) runs on pushes, pull requests, and manual invocation. It executes the Python tests and a reproducible sample-data check. Its **Summary** tab contains the generated reference metrics; the **Artifacts** section contains a reference follow-up CSV, a harmless formula-input export, and a Markdown verification report.

Reviewers can inspect past runs and their public **Summary** results from the workflow link without installing Python. Repository collaborators with **write access** may also choose **Run workflow** on `main` to start a new run. A green status means automated checks passed; it does **not** certify how Microsoft Excel handles cells after a save-and-reopen cycle.

The fictional `sample_security_check.csv` can be uploaded in the application to exercise formula-like names. The dashboard intentionally shows the original text. The **downloaded** CSV neutralizes formula-like cells for Excel-oriented viewing; manual Excel testing is still appropriate.

### AI-assisted engineering iteration

A review of the original CSV export identified a potential spreadsheet formula interpretation issue: values such as `=1+1` passed through the raw export as-is. ChatGPT assisted in moving export formatting into a separately testable `csv_export.py` module and adding seven regression tests. The detection engine and candidate priority rules were left unchanged. A development-time import-path error in `scripts/reviewer_check.py` was corrected, after which 21 tests and the sample-data check passed locally. See `AI_BUILD_LOG.md` for this actual iteration.

## Limitations and safety

- CSV import only; no live applicant-tracking-system integration.
- A stage's inactivity is measured solely from `last_stage_change`.
- No emails are drafted/sent, no ATS records are modified, and no hiring decisions are automated.
- Rules are fixed in code and should be reviewed against each organization's recruiting policy.
- Exported spreadsheet CSVs prefix formula-like text with an embedded tab as a defense-in-depth measure. Spreadsheet importers differ; there is no guarantee against every re-save/re-import interpretation. This mitigation does not replace organizational data-handling controls.
- Use invented or authorized candidate records; do not publish private applicant information.

This is an educational prototype for operational follow-up, not a candidate suitability/ranking system.
