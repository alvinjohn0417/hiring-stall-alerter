"""Pre-recording check: expected files exist with exact names, README links resolve,
and no TODO-LINK placeholders are left. Run from the repo root:

    .\\.venv\\Scripts\\python.exe scripts\\check_layout.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]

EXPECTED = [
    "app.py", "engine.py", "csv_export.py", "requirements.txt", "start_windows.bat",
    "sample_hiring_board.csv", "sample_followup_report.csv", "sample_security_check.csv",
    "tests/test_engine.py", "tests/test_csv_export.py", "scripts/reviewer_check.py",
    ".github/workflows/reviewer-verification.yml", "docs/dashboard.png", "docs/dashboard_queue.png",
    "README.md", "WALKTHROUGH.md", "AI_BUILD_LOG.md", "FIVE_DAY_LOG.md",
    "intent.md", "Final directive.md", "UNLEARNED.md",
]
DOCS = ["README.md", "WALKTHROUGH.md", "AI_BUILD_LOG.md", "FIVE_DAY_LOG.md",
        "intent.md", "Final directive.md", "UNLEARNED.md"]


def main() -> int:
    problems: list[str] = []
    for rel in EXPECTED:
        if not (ROOT / rel).exists():
            problems.append(f"missing file: {rel}")
    for doc in DOCS:
        path = ROOT / doc
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", text):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            if not (ROOT / unquote(target)).exists():
                problems.append(f"{doc}: broken link -> {target}")
        if "TODO-LINK" in text:
            problems.append(f"{doc}: still contains TODO-LINK placeholder")
    if problems:
        print("CHECK FAILED:")
        for p in problems:
            print(" -", p)
        return 1
    print("OK: expected files present, relative links resolve, no placeholders left.")
    return 0


if __name__ == "__main__":
    sys.exit(main())