# Intent — Hiring Stall Alerter

## Problem

Hiring teams can lose track of candidates who remain in one pipeline stage without a recorded update. Checking a hiring board manually requires repeated date comparisons and prioritization decisions.

## Intended user and job to be done

A recruiter or hiring coordinator needs to identify which **active** candidates have not changed stages within an acceptable period, see who requires follow-up first, and review an appropriate next action.

## Input and output

- **Input:** A CSV hiring board with candidate ID, name, role, stage, last stage-change date, and owner; an analysis date and stall threshold.
- **Output:** Counts of valid, active, stalled, and urgent candidates; a ranked follow-up queue; a reason and suggested action for each flag; and a downloadable CSV.
- **Human checkpoint:** A recruiter reviews alerts and decides whether and how to follow up.

## Definition of success

1. Flag active records when days in stage are **at or above** the chosen threshold.
2. Exclude terminal stages such as Hired, Rejected, and Withdrawn.
3. Rank flagged records using documented, deterministic rules.
4. Handle invalid inputs with meaningful errors or warnings.
5. Reproduce the reference example for **2026-11-17**, threshold **7**: **25 valid, 22 active, 15 stalled, 6 urgent**.
6. Provide a locally runnable project with documented setup and automated verification.

## Deliberate limits

This is a small, local educational prototype. It does not infer candidate quality, make employment decisions, connect to an applicant-tracking system, send messages, or continuously monitor the hiring pipeline. Its data examples are fictional.

## AI-first change in working method

Instead of relying on familiar visual workflow tools, the build used ChatGPT to propose a standalone Python and Streamlit application, then relied on observed local results, automated checks, and engineering review to validate and revise it. The application itself does **not** call an LLM at runtime.

## Evidence

- [Working application and README](README.md)
- [AI-assisted development log](AI_BUILD_LOG.md)
- [Reviewer verification workflow](.github/workflows/reviewer-verification.yml)
