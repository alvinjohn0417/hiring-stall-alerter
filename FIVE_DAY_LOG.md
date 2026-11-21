# Five-Day Quest Log — Hiring Stall Alerter (Option C)

**Timeline note:** This is a retrospective log prepared on **November 21, 2026**. The working application, initial tests, GitHub publication, and security/CI improvements were completed on **November 17, 2026**, using an accelerated schedule. The five entries below are **project checkpoints**, not claims of work performed on five separate consecutive calendar days.

## Day 1 — Define the problem and choose the approach
**Actual date: November 17, 2026**

**Goal:** Create a small tool that helps recruiters notice candidates who have spent too long in the same hiring stage.

**What I did:** I selected Option C and defined the input as a hiring-board CSV, with an analysis date and configurable stall threshold. I chose to move beyond familiar visual automation platforms and try ChatGPT-assisted Python and Streamlit, despite having no prior Python development background.

**How I used AI:** I discussed whether Claude Code was necessary and used ChatGPT to compare implementation options and translate the business problem into an application scope.

**Outcome / lesson:** A narrowly defined task was sufficient to start building with an unfamiliar programming language.

**Evidence:** [Project intent](intent.md) · [Initial project files](app.py)

## Day 2 — Build and run the first working version
**Actual date: November 17, 2026 (accelerated)**

**Goal:** Turn the requirements into a usable application.

**What I did:** I asked ChatGPT to build the tool immediately and explain each step. ChatGPT generated the initial Python engine, Streamlit dashboard, fictional candidate CSV, tests, and Windows launcher. I launched it locally using Python 3.13 and checked its output.

**How I used AI:** ChatGPT generated and explained the code; I followed the setup steps and validated the running dashboard.

**Outcome / lesson:** With an analysis date of November 17 and a seven-day threshold, the dashboard showed **25 valid candidates, 22 active, 15 stalled, and 6 urgent**. AI-assisted generation still required real-world verification.

**Evidence:** [Dashboard screenshot](docs/dashboard.png) · [Business logic](engine.py) · [Sample data](sample_hiring_board.csv)

## Day 3 — Validate the behavior and publish the code
**Actual date: November 17, 2026 (accelerated)**

**Goal:** Confirm that the basic features work and make the project reviewable.

**What I did:** I tested the threshold slider, candidate search/filter, and CSV download in the browser; all three manual checks passed. The original **14 engine tests** passed in the development environment. I published the project in a public GitHub repository and corrected an accidental duplicated directory.

**How I used AI:** ChatGPT guided the testing process and prepared the initial README and development documentation. I reviewed the published files and requested corrections when some documentation contained user-facing instructions instead of reviewer-ready evidence.

**Outcome / lesson:** A successful screen is not sufficient; test results, reproducible setup, and accurate documentation also matter.

**Evidence:** [Original engine tests](tests/test_engine.py) · [README](README.md) · [GitHub repository](https://github.com/alvinjohn0417/hiring-stall-alerter)

## Day 4 — Improve security and automate verification
**Actual date: November 17, 2026 (accelerated)**

**Goal:** Demonstrate an engineering improvement beyond the first working version.

**What I did:** During a follow-up review, ChatGPT identified a potential spreadsheet formula-interpretation risk in exported CSV text. I authorized the improvement, and ChatGPT added an export-specific safeguard, **seven regression tests**, and a GitHub Actions reviewer-verification workflow. Some early CI runs failed because the workflow referenced a script that had not yet been committed; that dependency was fixed, and subsequent complete runs passed. An import-path error in the verification script was also corrected.

**How I used AI:** ChatGPT investigated the problem, implemented changes, inspected GitHub Actions errors, and checked the resulting reports. I examined the results and requested another investigation when I noticed failed runs.

**Outcome / lesson:** The suite grew to **21 passing automated tests**. I learned that AI-generated code needs security review, regression tests, and careful interpretation of CI failures. Automated CSV checks do **not** replace manual Excel save-and-reopen verification.

**Evidence:** [CSV export module](csv_export.py) · [Regression tests](tests/test_csv_export.py) · [Successful CI run](https://github.com/alvinjohn0417/hiring-stall-alerter/actions/runs/44113298195)

## Day 5 — Review the final deliverables and reflect
**Actual date: November 21, 2026**

**Goal:** Compare the project against the complete published deliverables and prepare the required written artifacts.

**What I did:** I reviewed the full requirements screenshot and discovered four documentation deliverables that were not included in the initial checklist: `intent.md`, `Final directive.md`, a short five-entry log, and a one-page note on what I unlearned. ChatGPT drafted these from the actual project history and added them to the repository; I continued reviewing the artifacts for reviewer-facing clarity.

**How I used AI:** ChatGPT reconciled the revised checklist with the repository and drafted retrospective documents without inventing five separate workdays.

**Outcome / lesson:** Clear evidence and honest attribution are part of engineering work. The code, README, and written artifacts are available; the two required videos were not yet recorded at this point. Their status is shown in the [README](README.md#video-links).

**Evidence:** [Intent](intent.md) · [Final directive](Final%20directive.md) · [Unlearning reflection](UNLEARNED.md) · [AI build log](AI_BUILD_LOG.md)

---

**Scope of this record:** These entries summarize verified milestones across an accelerated build. They are **not contemporaneous logs from five different calendar days**. The tool applies deterministic Python rules at runtime; ChatGPT supported development, review, debugging, and documentation. All example candidate data is fictional.

## Submission update — November 21, 2026

The tool demonstration Loom was provided after the original log entry and is now linked in the [README's video section](README.md#video-links): [Hiring Stall Alerter tool demo](https://www.loom.com/share/7b299434f9ef4320930fe414faeaf813). The separate career path and career leverage video has not yet been supplied. This update preserves the original Day 5 status as a record of what was known at that time.
