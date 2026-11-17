# AI-first build journal — Option C: Hiring Stall Alerter

## Project brief

Build a small tool that reads a CSV hiring board, flags candidates stalled for a selected number of days, ranks follow-up priority, and suggests next actions. Finish within five days and show how AI changed the development workflow.

## Actual starting point

- **2026-11-17:** Used ChatGPT to scope and generate a Python + Streamlit prototype, sample data, deterministic scoring logic, automated tests and local-run instructions.
- **Validation:** The automated test suite is included in `tests/test_engine.py`; run it yourself and capture the terminal output for your evidence.
- **User validation and Loom demo:** To be completed on your own computer. Do not represent them as completed until you actually do them.

## Why this design

- **Python + Streamlit** demonstrates a new AI-assisted coding workflow, rather than another n8n automation.
- **CSV input** is intentionally small and easy to test with fictional records.
- **Transparent, deterministic rules** keep flagging and priority reproducible.
- **Human review** is required before any outreach or hiring decision.

## Prompts you can use in the next iteration

1. "Review my `engine.py` for edge cases. Do not change the business rule without explaining why. Suggest at least 5 new tests."
2. "Add a per-stage stall threshold to my Streamlit app. Preserve current tests and add coverage for special cases."
3. "Explain each function in my `app.py` in plain English and identify which parts are UI versus business logic."
4. "Help me record a 3-minute Loom demo using the sample CSV, a threshold change, one input error and a report download."

## Screenshots / evidence to gather

- The successful Streamlit page with 7-day threshold.
- The prioritized queue and downloaded CSV opened in Excel.
- A run of `python -m unittest discover -s tests -v`.
- One failure you found and the AI-assisted correction (record the *real* before and after).
- Your actual prompts and any edits you accepted or rejected.

## Final review questions

- Can a first-time user follow the README and launch the tool?
- What happens on a malformed CSV?
- Do urgent candidates appear first?
- Does the tool avoid contacting candidates automatically?
- Did AI make prototyping, test writing or debugging faster? What would you do differently?
