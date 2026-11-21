# Final directive — Hiring Stall Alerter

## Purpose

This document records the stable engineering directive for maintaining and extending the completed Option C prototype. It is a handoff specification for subsequent work, including work assisted by AI coding tools—not a claim that the application has production capabilities.

## Primary directive

Maintain a small, explainable tool that transforms a hiring-board CSV into a prioritized **operational follow-up** queue. Preserve human oversight and reproducible business rules.

## Required invariants

1. Do not decide whether a candidate should be hired or rejected. Rank only the urgency of **following up** on stalled pipeline records.
2. Use the user-selected analysis date and configurable stall threshold for date calculations.
3. Keep calculations and priority assignment deterministic, inspectable, and covered by tests.
4. Exclude terminal hiring stages from active follow-up alerts.
5. Reject or warn on malformed CSV rows; do not silently invent missing dates or identities.
6. Keep the dashboard's original text visible; apply spreadsheet formula risk reduction when exporting CSV data.
7. Do not send messages, change ATS records, or expose applicant information without separately designed authorization and human approval.
8. Treat all sample candidate information as fictional.

## Instructions for future AI-assisted changes

- Start with a specific problem, reproduction, and acceptance criteria.
- Make the smallest change that addresses it. Keep UI, analysis logic, and export logic separated.
- Add or update tests for any business-rule or security behavior change.
- Run `python -m unittest discover -s tests -v` and `python scripts/reviewer_check.py`.
- Compare the reference results (2026-11-17 / 7 days): **25 valid, 22 active, 15 stalled, 6 urgent**.
- Review the GitHub Actions result and document observed failures and corrections, not invented debugging stories.
- Confirm any spreadsheet-specific behavior manually if it cannot be verified by Python tests.

## Current verified boundaries

The project runs locally on Python and Streamlit. The repository has automated unit/regression checks and a CI evidence report. CSV export includes an Excel-oriented formula-injection mitigation but does not guarantee safety across every spreadsheet program or save-and-reopen cycle.

## Recommended future extension

For real organizational use, introduce stage-specific policies, stage-change history, authenticated access, secure storage, audit logs, ATS integration, scheduled checks, and human-approved notifications. Deployment, real data protection, and operating costs would need separate engineering and review.
