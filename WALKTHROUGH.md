# Reproducing the Hiring Stall Alerter Demo (Windows)

This guide provides a repeatable local demonstration of the application and its reference results. The application runs locally; it is not hosted on a public server.

## 1. Prepare the environment

Install Python 3.11 or newer; the recorded local verification used Python 3.13 on Windows. Download or clone this repository and open the project directory.

Launch **`start_windows.bat`**. On first run, the launcher creates a virtual environment named `.venv` and installs the dependencies in `requirements.txt`.

To start manually in PowerShell from the project directory:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

The Streamlit interface will usually open automatically. Otherwise, visit `http://localhost:8501` and keep the application terminal open.

## 2. Reproduce the reference result

1. Select **Try example data**.
2. Set **Analyze as of** to **2026-11-17**.
3. Set **Flag after this many days** to **7**.
4. Compare the dashboard with the reference values below.

| Dashboard metric | Reference result |
|---|---:|
| Valid candidates | 25 |
| Active candidates | 22 |
| Flagged to follow up | 15 |
| Urgent | 6 |

The reference screenshot is stored at `docs/dashboard.png`. The CSV export for the same settings is available in `sample_followup_report.csv`.

## 3. Examine filtering and export

- Change the threshold to **10 days** and verify that fewer candidates are flagged. Restore it to **7 days**.
- Search for **Maria Santos**. Clear the search and use the priority filter.
- Select **Download prioritized follow-up CSV** and inspect the exported rows.

These three functional checks were completed during the initial Windows walkthrough.

## 4. Test an invalid row

Create a copy of `sample_hiring_board.csv` and replace one `last_stage_change` value with `not-a-date`. Choose **Upload a CSV** and select that modified file.

The application is designed to skip the invalid row and show a warning. This is a reproducible test scenario, **not** a claim that this specific upload scenario was manually demonstrated. The automated test suite separately checks invalid-date handling.

## 5. Run the automated tests

From PowerShell in the project directory, with the virtual environment installed:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The included suite covers date parsing, duplicate IDs, missing values, future dates, thresholds, terminal stages, priority ordering, stage-specific actions, and export fields. **21 automated tests passed** in the assistant's project environment during the export-security iteration (14 original + 7 regression tests).

## 6. Verify the spreadsheet export protection

1. Set the analysis date to **2026-11-17**, with a **7-day threshold**.
2. Choose **Upload a CSV** and select `sample_security_check.csv` (fictional, harmless spreadsheet-formula test data).
3. Confirm that formula-like candidate names (for example `=1+1`) are displayed in the application, and that all seven test records are flagged.
4. Download the prioritized follow-up CSV. Inspect the **raw CSV in a text editor**: formula-like fields should have a tab character as a prefix inside quoted CSV cells.
5. If using Excel, also test the **opened file and an Excel save/re-open cycle**. Spreadsheet applications vary, and an automated CSV-content test alone does not prove that a particular Excel import workflow is safe.

This demonstration uses benign formulas only. The application does not evaluate or execute candidate values; the export mitigation is a defense-in-depth measure.

## 7. Trigger the public reviewer checks

Visit [Reviewer verification in GitHub Actions](https://github.com/alvinjohn0417/hiring-stall-alerter/actions/workflows/reviewer-verification.yml) and open an existing run. Repository collaborators with write access can additionally select **Run workflow** on branch `main` to start a new run; public read-only reviewers can inspect previous results.

- A successful run means the syntax check, 21 Python tests, reference metrics, and exported CSV checks passed.
- Open the run's **Summary** tab for the reference scenario results.
- Download the `reviewer-verification-report` artifact to inspect the verification report and generated CSVs.

A manual workflow run is not required to browse the existing public verification results.

## 8. How results are generated


The pipeline follows fixed, inspectable steps:

```text
CSV input → validation → active-stage filtering
→ days-in-stage calculation → priority assignment
→ reason and suggested next action → human review / CSV export
```

No LLM is called when the app analyzes CSV data. ChatGPT assisted with development; the live application relies on Python business rules. The sample candidates are fictional. No candidate messages are sent and no external hiring records are changed.
