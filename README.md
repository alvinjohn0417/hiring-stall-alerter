# Hiring Stall Alerter

[![Reviewer verification](https://github.com/alvinjohn0417/hiring-stall-alerter/actions/workflows/reviewer-verification.yml/badge.svg)](https://github.com/alvinjohn0417/hiring-stall-alerter/actions/workflows/reviewer-verification.yml)

**A CSV-based hiring pipeline follow-up dashboard, built with ChatGPT-assisted Python and Streamlit.**

The app finds candidates who have stayed in an *active* hiring stage at or beyond a chosen threshold, orders the follow-up queue by clear rules, explains each flag, and recommends a next step for a recruiter to review. It does **not** make hiring decisions or send messages.

![Hiring Stall Alerter dashboard overview](docs/dashboard.png)

*Dashboard overview — sample data, settings, and metrics.*

![Hiring Stall Alerter follow-up queue](docs/dashboard_queue.png)

*Follow-up queue — candidate priorities, explanations, and recommended actions.*

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
2. Confirm the analysis date is `2026-11-17` (the example data opens on this date) and the threshold is **7** days.
3. Check the four reference metrics above.
4. Change the threshold to **10**; the stalled count should decrease. Restore it to **7**.
5. Search for `Maria Santos`, clear the search, and try the priority filter.
6. Download the follow-up CSV and inspect it in a text editor.
7. Optional: open the CSV in Excel, then save and reopen it.
8. Optional: upload a modified sample CSV containing an invalid `last_stage_change` date and check that the app reports a warning.

The reference metrics, threshold change, search/priority filter, and CSV download were checked manually on Windows. Opening the export in Excel (including a save-and-reopen cycle) and the malformed-input upload are suggested follow-up checks that are **not** recorded as completed. Input validation is also covered by the automated tests.

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
| `sample_security_check.csv` | Fictional formula-like names for CSV export testing |
| `tests/test_csv_export.py` | CSV export regression tests |
| `scripts/reviewer_check.py` | Reference scenario verification and report generation |
| `.github/workflows/reviewer-verification.yml` | Automated tests and evidence on GitHub Actions |
| `engine.py` | CSV checks, date calculations, priorities, actions |
| `sample_hiring_board.csv` | Fictional sample hiring board |
| `sample_followup_report.csv` | Reference output for the 2026-11-17 example |
| `tests/test_engine.py` | Automated tests of the core logic |
| `start_windows.bat` | Windows launcher |
| `scripts/check_layout.py` | Checks expected files and local documentation links |
| `docs/dashboard_queue.png` | Follow-up queue screenshot |
| `AI_BUILD_LOG.md` | Actual AI-assisted development and testing record |
| `WALKTHROUGH.md` | Reproducible local demo and test procedure |
| `docs/dashboard.png` | Screenshot of the locally verified dashboard |

## Quest documentation

| Document | Purpose |
|---|---|
| [`intent.md`](intent.md) | Retrospective problem statement, scope, and AI-first intent |
| [`Final directive.md`](Final%20directive.md) | Engineering handoff requirements and safeguards |
| [`FIVE_DAY_LOG.md`](FIVE_DAY_LOG.md) | Five checkpoint log with accurate activity dates |
| [`UNLEARNED.md`](UNLEARNED.md) | One-page reflection on changed working habits |
| [`AI_BUILD_LOG.md`](AI_BUILD_LOG.md) | Detailed AI development and validation record |

### Video links

Both videos have a **five-minute maximum**.

| Video | Link |
|---|---|
| Quest Loom: tool demonstration | [Watch the Hiring Stall Alerter demo](https://www.loom.com/share/7b299434f9ef4320930fe414faeaf813) |
| Career path & career leverage | Recording pending; link will be added once available |

## Run the automated tests

From inside this project directory:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

**21 automated tests passed**, including 14 original engine tests and 7 CSV export regression tests. The GitHub Actions workflow reruns these tests and verifies the reference data. Three manual UI checks were completed on Windows: threshold adjustment, search/filter, and CSV export. Spreadsheet export protection still requires manual Excel save-and-reopen verification.

## AI-first approach

ChatGPT was used to break down the task, generate the first Python/Streamlit codebase and tests, explain local setup, interpret actual screenshots, and plan validation. **AI assisted development; AI does not decide the runtime results.** This was an intentional shift from visual workflow-building toward a standalone, AI-assisted coded application.

The [`AI_BUILD_LOG.md`](AI_BUILD_LOG.md) records the development timeline, the respective roles of ChatGPT and the developer, and the results that were verified.

## Reviewer verification — GitHub Actions

The [verification workflow](https://github.com/alvinjohn0417/hiring-stall-alerter/actions/workflows/reviewer-verification.yml) runs on pushes and pull requests. Its Summary tab shows the reference scenario and its downloadable artifact contains verification files. Public reviewers can inspect past runs; triggering new runs requires collaborator write access.

The fictional `sample_security_check.csv` lets reviewers inspect the exported handling of harmless formula-like values. The dashboard preserves the original input text; the downloadable CSV reduces spreadsheet formula interpretation risk. This does not prove safety in every spreadsheet application or after saving and reopening in Excel.

## Limitations and safety

- CSV import only; no live applicant-tracking-system integration.
- A stage's inactivity is measured solely from `last_stage_change`.
- No emails are drafted/sent, no ATS records are modified, and no hiring decisions are automated.
- Rules are fixed in code and should be reviewed against each organization's recruiting policy.
- Formula-like exported values receive a tab-prefix mitigation; behavior varies across spreadsheet applications and import/export workflows.
- Use invented or authorized candidate records; do not publish private applicant information.

This is an educational prototype for operational follow-up, not a candidate suitability/ranking system.