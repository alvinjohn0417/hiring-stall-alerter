# Step-by-step walkthrough (Windows)

You can follow this even if you have not written Python code before.

## Step 1 — Download and unzip the project

Download `stall_alerter_project.zip` from ChatGPT and right-click it in File Explorer > **Extract All**. Open the extracted `stall_alerter_project` folder.

**What you have:** `app.py` creates the dashboard; `engine.py` contains the detection rules; `sample_hiring_board.csv` is fictional input data; `tests/` checks calculations. See the README for every file.

## Step 2 — Install Python (once per computer)

If Python is already installed, you can skip this. Otherwise install Python 3.11 or newer from https://www.python.org/downloads/. On Windows, select **Add Python to PATH** during setup if prompted. Restart your terminal after installation.

## Step 3 — Launch the app

Double-click `start_windows.bat` in the project folder. On first run, it creates an isolated `.venv` environment and installs Streamlit/Pandas. Internet is needed to install these packages. Keep the black console window open.

If the launcher doesn't work, open Windows Terminal or PowerShell in this folder and paste these commands one at a time:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

If `py` isn't recognized, use `python -m venv .venv` instead. Streamlit should open in your browser at `http://localhost:8501`.

## Step 4 — Run the first experiment

- Keep **Try example data** selected.
- In the sidebar, set **Analyze as of = 2026-11-17**.
- Set **Flag after this many days = 7**.
- Review the four metrics and the ranked follow-up queue. A reference CSV is in `sample_followup_report.csv`.
- Move the slider to 10. The number of alerts should change.
- Move the slider back to 7, use the priority filter, and download the CSV report.

**What just happened:** Each `last_stage_change` date was subtracted from the selected analysis date. Only active candidates at or over the threshold were flagged. A transparent rule assigned each priority and next action.

## Step 5 — Try your own data

Select **Upload a CSV**, then upload `sample_hiring_board.csv` first. It should show the same result. For your own example, copy the sample and change a few dates, stages and names. Save as CSV UTF-8 in Excel.

### Try an intentional error

In a copy of the CSV, change one `last_stage_change` value to `not-a-date`. Upload it. The dashboard should show a warning explaining which row was skipped.

## Step 6 — Check the calculations

Open Windows Terminal/PowerShell inside the same project folder and run:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The included automated tests cover dates, thresholds, closed candidates, priority ordering, duplicate IDs, and bad input. Take a screenshot of the results for your quest.

## Step 7 — Your AI-first learning evidence

As you test, paste your actual errors or proposed improvements into ChatGPT and ask for one change at a time. Record your real prompt, proposed code, test result, and whether you accepted the change. Use `AI_BUILD_LOG.md` as a journal, then record the separate tool Loom and the career-leverage Loom required by the quest.

**Privacy:** Use invented candidate data for the demo. This prototype does not send messages, alter a hiring system, or contact an external AI service.
