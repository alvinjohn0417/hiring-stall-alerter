"""Spreadsheet-oriented CSV export with formula-injection risk reduction.

Formula mitigation is applied only when generating a downloadable spreadsheet CSV.
The dashboard and calculation engine retain the original candidate text.

This is a defense-in-depth measure for Excel-oriented CSV viewing, not a
universal sanitizer for all spreadsheet applications and import/export cycles.
"""

from __future__ import annotations

import csv
from io import StringIO
from typing import Mapping, Sequence

EXPORT_COLUMNS = (
    "Candidate ID", "Candidate", "Role", "Stage", "Owner",
    "Last stage change", "Days in stage", "Days beyond limit",
    "Priority", "Why flagged", "Recommended action",
)

# ASCII and full-width formula prefixes. Control/leading whitespace can also
# be stripped or normalized by spreadsheet software before interpretation.
FORMULA_PREFIXES = frozenset("=+-@＝＋－＠")
IGNORED_LEADING = " \t\r\n\v\f\ufeff\u200b\u2028\u2029"


def spreadsheet_safe_cell(value: object) -> str:
    """Prefix risky values with a tab for CSV viewing in Excel.

    This follows OWASP's Excel-oriented mitigation recommendation. The tab is
    intentional CSV data and may be visible in downstream programmatic imports.
    """
    text = "" if value is None else str(value)
    normalized = text.lstrip(IGNORED_LEADING)
    if text.startswith(("\t", "\r", "\n", "\v", "\f", "\u2028", "\u2029")) or (
        normalized and normalized[0] in FORMULA_PREFIXES
    ):
        return "\t" + text
    return text


def export_followups_csv(rows: Sequence[Mapping[str, object]]) -> bytes:
    """Produce quoted, UTF-8 BOM CSV for human spreadsheet review."""
    stream = StringIO(newline="")
    writer = csv.DictWriter(
        stream,
        fieldnames=EXPORT_COLUMNS,
        extrasaction="ignore",
        quoting=csv.QUOTE_ALL,
        lineterminator="\r\n",
    )
    writer.writeheader()
    for row in rows:
        writer.writerow({col: spreadsheet_safe_cell(row.get(col, "")) for col in EXPORT_COLUMNS})
    return stream.getvalue().encode("utf-8-sig")
