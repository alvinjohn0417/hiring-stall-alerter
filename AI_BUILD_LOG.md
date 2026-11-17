# AI-first build log — Hiring Stall Alerter (Option C)

## Challenge objective

Build a small tool within five days that reads a hiring-board CSV, finds candidates who have not progressed for a set number of days, and lists whom to follow up first and what to do. The challenge emphasizes a changed working method through effective AI use.

## What happened — verified log

| Date | Step | Result and evidence |
|---|---|---|
| 2026-11-17 | Chose **Option C: Stall Alerter**, and decided to build with **ChatGPT + Python + Streamlit** instead of Claude Code or the familiar n8n-only approach. | Project scope agreed in ChatGPT conversation. |
| 2026-11-17 | Asked ChatGPT to start building immediately and explain the steps. ChatGPT generated a Python application, calculation engine, 25-row fictional CSV, test file, and Windows launcher. | Original code files in this repository. |
| 2026-11-17 | Launched locally with **Python 3.13**. Package installation completed and the Streamlit browser page opened. | Local console screenshot shared during walkthrough. |
| 2026-11-17 | Tested with analysis date **2026-11-17** and **7-day threshold**. | Actual dashboard showed 25 valid, 22 active, 15 stalled, 6 urgent. See `docs/dashboard.png`. |
| 2026-11-17 | Tested threshold change, candidate search/filter, and CSV download/opening on Windows. | **All three manual tests passed.** |
| 2026-11-17 | ChatGPT's project environment executed the automated engine tests. | **14 tests passed** (`python -m unittest discover -s tests -v`). These are separate from the local UI checks. |
| 2026-11-17 | Published the project to GitHub, removed an accidentally duplicated directory, and reviewed the documentation. | [Public repository](https://github.com/alvinjohn0417/hiring-stall-alerter). |

## Follow-up engineering iteration — export security and CI

| 2026-11-17 | Reviewed the CSV export for spreadsheet formula interpretation risk. A harmless candidate value `=1+1` remained formula-like in the original raw pandas CSV output. | Reproduced with a CSV export sample; this establishes an unsafe raw value, not execution in Excel. |
| 2026-11-17 | Used ChatGPT to add a separate CSV export safety module, a seven-test regression suite, and an automated reviewer check. | `csv_export.py`, `tests/test_csv_export.py`, `scripts/reviewer_check.py`. |
| 2026-11-17 | First run of the standalone reviewer check raised `ModuleNotFoundError: No module named 'csv_export'`. The script was adjusted to load the repository root before importing. | After correction, **21 local automated tests passed**, and the scripted reference check passed with 25 valid / 22 active / 15 stalled / 6 urgent. |
| 2026-11-17 | Added a GitHub Actions workflow which can also be triggered manually by reviewers. | `.github/workflows/reviewer-verification.yml`; GitHub-run outcome reported separately. |

The CSV fix applies a tab prefix to formula-like cells only in downloaded spreadsheet CSVs. It does not alter candidates shown in the application or change ranking calculations. This is an Excel-oriented defense-in-depth measure, **not a claim of universal spreadsheet safety**. The automated checks validate raw CSV contents; Excel save-and-reopen behavior remains subject to manual verification.

## How AI changed the workflow

**Before:** My existing portfolio emphasized low-code integrations, APIs/webhooks and visual workflow builders such as n8n.

**For this challenge:** I used conversational instructions with ChatGPT to define the requirements, produce a working Python+Streamlit application and test suite, help with Windows setup, interpret real screenshots, and check the results. Instead of manually writing every line from scratch, I directed the build through natural-language specifications and then validated the output on my machine.

**Important distinction:** This is **AI-assisted software development**, not an LLM-powered candidate analysis engine. The running tool applies deterministic rules, so its results can be checked and explained. Recruiters review suggested next steps before acting.

## Real prompt examples from the conversation

- “can I do that without claude code” — led to evaluation of ways to build using existing tools or ChatGPT-assisted Python.
- “can we do it now and explain the steps to me.” — led to the first executable project with code and beginner-friendly instructions.
- “i have python 3.13” — led to guidance using the already installed Python version.
- Later messages shared the running console and app screenshot and confirmed three functional tests passed.

These are examples of **actual** collaboration with ChatGPT, rather than reconstructed prompts or additional work that did not occur.

## Technical decisions and safeguards

The running application uses Python to validate hiring-board data, calculate days in stage, and rank follow-ups using visible business rules. Streamlit provides the interface for filtering and exporting reports.

AI assisted development but does not analyze candidate records at runtime. Suggested actions are based on hiring stages and require human review. All example candidate records are fictional, and the app neither sends messages nor changes an applicant-tracking system.

## Verification summary

| Check | Result |
|---|---|
| Python 3.13 + Streamlit local startup | Passed |
| Sample data, 2026-11-17, 7-day limit | 25 valid / 22 active / 15 stalled / 6 urgent |
| Manual UI tests | Threshold, search/filter, and CSV export passed |
| Automated tests | 21 passed in the assistant's project environment (14 original + 7 export regression tests) |
| Public GitHub repository | Published, including reviewer-triggerable workflow |

## Reflection

Rather than building another visual automation, I used ChatGPT as a coding assistant to create a Python and Streamlit application. I supplied the objective, ran the application locally, checked the example results, and tested the main interactions. I learned to verify AI-generated software against concrete outputs rather than assuming generated code works. The finished prototype uses auditable rules and keeps hiring decisions with people. During the later review I was also able to use AI to investigate a CSV export risk, check the proposed protection with regression tests, and correct an import-path error revealed by the reviewer verification script.
