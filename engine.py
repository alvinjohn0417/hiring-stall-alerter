"""Pure-Python business rules for a small hiring-pipeline stall detector.

No LLM or internet connection is required. Keep detection and prioritization
reproducible; a reviewer can inspect every rule in this file.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date, datetime
from io import StringIO

REQUIRED_COLUMNS = (
    "candidate_id", "candidate_name", "role", "stage", "last_stage_change", "owner"
)
TERMINAL_STAGES = {"hired", "rejected", "withdrawn", "closed", "declined", "not selected"}
STAGE_WEIGHTS = {
    "offer": 5,
    "final interview": 4,
    "interview": 3,
    "assessment": 2,
    "screening": 1,
    "applied": 0,
}

ACTIONS = {
    "applied": "Ask the recruiter to review this application and confirm the next screening step.",
    "screening": "Ask the recruiter for a screening decision and proposed next step.",
    "assessment": "Check assessment completion and request the reviewer's feedback.",
    "interview": "Request interview feedback and agree on the next interview step.",
    "final interview": "Ask the hiring manager for a decision and update the candidate.",
    "offer": "Confirm offer approval and send the candidate a status update.",
}


@dataclass(frozen=True)
class Candidate:
    candidate_id: str
    candidate_name: str
    role: str
    stage: str
    last_stage_change: date
    owner: str


@dataclass(frozen=True)
class Alert:
    candidate_id: str
    candidate_name: str
    role: str
    stage: str
    owner: str
    last_stage_change: date
    days_in_stage: int
    days_beyond_limit: int
    priority: str
    priority_score: int
    explanation: str
    next_action: str

    def for_export(self) -> dict[str, str | int]:
        return {
            "Candidate ID": self.candidate_id,
            "Candidate": self.candidate_name,
            "Role": self.role,
            "Stage": self.stage,
            "Owner": self.owner,
            "Last stage change": self.last_stage_change.isoformat(),
            "Days in stage": self.days_in_stage,
            "Days beyond limit": self.days_beyond_limit,
            "Priority": self.priority,
            "Why flagged": self.explanation,
            "Recommended action": self.next_action,
        }


def read_candidates(raw_csv: bytes, as_of: date) -> tuple[list[Candidate], list[str]]:
    """Validate a UTF-8 CSV; skip problematic rows with plain-language warnings.

    Raises ValueError for unrecoverable CSV errors (e.g., missing required columns).
    """
    try:
        content = raw_csv.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError("Use a UTF-8 CSV file. In Excel, choose 'CSV UTF-8'.") from exc

    try:
        reader = csv.DictReader(StringIO(content, newline=""))
        if reader.fieldnames is None:
            raise ValueError("The file is empty or has no header row.")
        fields = {name.strip() for name in reader.fieldnames if name is not None}
        missing = set(REQUIRED_COLUMNS) - fields
        if missing:
            raise ValueError("Missing columns: " + ", ".join(sorted(missing)))
        if any(name != name.strip() for name in reader.fieldnames if name is not None):
            raise ValueError("Remove spaces from CSV column headers and upload again.")

        candidates: list[Candidate] = []
        issues: list[str] = []
        seen_ids: set[str] = set()
        for row_num, row in enumerate(reader, start=2):
            if None in row:
                issues.append(f"Row {row_num}: extra fields detected; row skipped.")
                continue
            row = {k: (v or "").strip() for k, v in row.items()}
            if not any(row.values()):
                continue
            candidate_id = row["candidate_id"]
            name = row["candidate_name"]
            stage = row["stage"]
            changed = row["last_stage_change"]
            if not all((candidate_id, name, stage, changed)):
                issues.append(f"Row {row_num}: ID, name, stage and date are required; row skipped.")
                continue
            if candidate_id.casefold() in seen_ids:
                issues.append(f"Row {row_num}: duplicate candidate_id '{candidate_id}'; row skipped.")
                continue
            try:
                moved_on = datetime.strptime(changed, "%Y-%m-%d").date()
                if moved_on.isoformat() != changed:
                    raise ValueError("Noncanonical date format")
            except ValueError:
                issues.append(f"Row {row_num}: invalid date '{changed}'; expected YYYY-MM-DD; row skipped.")
                continue
            if moved_on > as_of:
                issues.append(f"Row {row_num}: stage date is after analysis date; row skipped.")
                continue
            seen_ids.add(candidate_id.casefold())
            candidates.append(Candidate(
                candidate_id=candidate_id,
                candidate_name=name,
                role=row["role"] or "Not specified",
                stage=stage,
                last_stage_change=moved_on,
                owner=row["owner"] or "Unassigned",
            ))
    except csv.Error as exc:
        raise ValueError("Could not parse the CSV. Check file structure and delimiters.") from exc
    return candidates, issues


def summarize(candidates: list[Candidate]) -> dict[str, int]:
    terminal = sum(1 for c in candidates if c.stage.casefold() in TERMINAL_STAGES)
    return {"all": len(candidates), "active": len(candidates) - terminal, "closed": terminal}


def assess_candidates(candidates: list[Candidate], threshold_days: int, as_of: date) -> list[Alert]:
    """Flag active candidates at or above the threshold and rank them.

    Priority rules:
      * Urgent: >=7 days beyond threshold, or late stage >=3 days beyond.
      * High: >=3 days beyond threshold, or late stage already at threshold.
      * Follow up: any other flagged candidate.
    Within each priority, longer overdue first, then later-stage candidates.
    """
    if threshold_days < 1:
        raise ValueError("Threshold must be at least 1 day.")
    alerts: list[Alert] = []
    for candidate in candidates:
        stage_key = candidate.stage.casefold().strip()
        if stage_key in TERMINAL_STAGES:
            continue
        days = (as_of - candidate.last_stage_change).days
        if days < threshold_days or days < 0:
            continue
        overdue = days - threshold_days
        late_stage = stage_key in {"offer", "final interview"}
        if overdue >= 7 or (late_stage and overdue >= 3):
            priority = "Urgent"
            tier = 3
        elif overdue >= 3 or late_stage:
            priority = "High"
            tier = 2
        else:
            priority = "Follow up"
            tier = 1
        weight = STAGE_WEIGHTS.get(stage_key, 0)
        score = tier * 100000 + overdue * 10 + weight
        day_word = "day" if days == 1 else "days"
        explanation = (
            f"{candidate.candidate_name} has been in {candidate.stage} for {days} {day_word}, "
            f"meeting or exceeding the {threshold_days}-day follow-up threshold."
        )
        action = ACTIONS.get(stage_key, "Ask the hiring owner for a stage update and next action.")
        alerts.append(Alert(
            candidate_id=candidate.candidate_id,
            candidate_name=candidate.candidate_name,
            role=candidate.role,
            stage=candidate.stage,
            owner=candidate.owner,
            last_stage_change=candidate.last_stage_change,
            days_in_stage=days,
            days_beyond_limit=overdue,
            priority=priority,
            priority_score=score,
            explanation=explanation,
            next_action=action,
        ))
    return sorted(
        alerts,
        key=lambda a: (-a.priority_score, a.candidate_name.casefold(), a.candidate_id.casefold()),
    )
