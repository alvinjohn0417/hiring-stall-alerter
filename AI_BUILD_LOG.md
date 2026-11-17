# AI-first build log — Hiring Stall Alerter (Option C)

> Purpose: accurately document how AI helped produce a working tool. Distinguish verified evidence from suggested next steps; do not invent iterations or claim manual coding that did not happen.

## Challenge objective

Build a small tool within five days that reads a hiring-board CSV, finds candidates who have not progressed for a set number of days, and lists whom to follow up first and what to do. The challenge emphasizes a changed working method through effective AI use.

## What happened — verified log

| Date | Step | Result and evidence |
|---|---|---|
| 2026-11-17 | Chose **Option C: Stall Alerter**, and decided to build with **ChatGPT + Python + Streamlit** instead of Claude Code or the familiar n8n-only approach. | Project scope agreed in ChatGPT conversation. |
| 2026-11-17 | Asked ChatGPT to start building immediately and explain the steps. ChatGPT generated a Python application, calculation engine, 25-row fictional CSV, test file, and Windows launcher. | Original code files in this repository. |
| 2026-11-17 | Launched locally with **Python 3.13**. Package installation completed and the Streamlit browser page opened. | Local console screenshot shared during walkthrough. |
| 2026-11-17 | Tested with analysis date **2026-11-17** and **7-day threshold**. | Actual dashboard showed 25 valid, 22 active, 15 stalled, 6 urgent. See `docs/dashboard.png`. |
| 2026-11-17 | Tested threshold change, candidate search/filter, and CSV download/opening. | User reported **all three manual tests passed**. |
| 2026-11-17 | Re-ran automated unit tests from the project folder. | **14 tests passed** (`python -m unittest discover -s tests -v`). |
| 2026-11-17 | Updated README and build log to reflect verified results rather than placeholder claims. | `README.md` and this file. |

**Not yet verified or completed:** GitHub upload, quest demo Loom, separate career video, final submission; do not list these as accomplished until finished.

## How AI changed the workflow

**Before:** My existing portfolio emphasized low-code integrations, APIs/webhooks and visual workflow builders such as n8n.

**For this challenge:** I used conversational instructions with ChatGPT to define the requirements, produce a working Python+Streamlit application and test suite, help with Windows setup, interpret real screenshots, and check the results. Instead of manually writing every line from scratch, I directed the build through natural-language specifications and then validated the output on my machine.

**Important distinction:** This is **AI-assisted software development**, not an LLM-powered candidate analysis engine. The running tool applies deterministic rules, so its results can be checked and explained. Recruiters review suggested next steps before acting.

## Real prompt examples from the conversation

- “can I do that without claude code” — led to evaluation of ways to build using existing tools or ChatGPT-assisted Python.
- “can we do it now and explain the steps to me.” — led to the first executable project with code and beginner-friendly instructions.
- “i have python 3.13” — led to guidance using the already installed Python version.
- Later messages shared the running console and app screenshot and confirmed three functional tests passed.

These are examples of **actual** collaboration with ChatGPT. For your Loom, open the conversation if you want to demonstrate the real prompt-to-code workflow rather than inventing a prompt history.

## Evidence to keep for submission

- [x] Working dashboard with expected sample metrics: `docs/dashboard.png`.
- [x] User confirmation of three manual UI tests (threshold, search/filter, CSV export).
- [x] Automated engine tests: 14/14 passing in the project workspace.
- [ ] Optional: capture your *own* Windows terminal running the test command.
- [ ] Optional: test and record an invalid-date upload in the UI.
- [ ] Publish the GitHub repository and save its public link.
- [ ] Record tool demo Loom and explain the design, actual AI usage, tests, and limitations.
- [ ] Record separate career path / career leverage / quest connection video (max 5 minutes).

## Reflection you can adapt in your own words

> Rather than building another visual automation, I used ChatGPT as a coding partner to create a Python and Streamlit application. I provided the business objective and tested the result locally. The tool reads fictional CSV data, calculates days in stage, applies clear priorities, and produces a human-reviewed follow-up queue. I learned the importance of checking AI-generated code against concrete expected results instead of assuming the first answer works. This tool runs without a paid AI API because its actual detection logic should be transparent and reproducible.

## Next technical experiments (not yet done)

1. Upload a sample row with an invalid date and confirm the warning is specific and understandable.
2. Ask AI to propose new tests for unusual stage names, extra columns, and threshold boundaries.
3. If time allows, add configurable stall limits by hiring stage, with a new automated test.

Keep future entries factual: write down the prompt, proposed change, any error, whether you accepted it, and the observed test result.
