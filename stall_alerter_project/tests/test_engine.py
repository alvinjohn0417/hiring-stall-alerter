"""Run from the project folder: python -m unittest discover -s tests -v"""

import unittest
from datetime import date

from engine import assess_candidates, read_candidates, summarize

TODAY = date(2026, 11, 17)
HEADER = "candidate_id,candidate_name,role,stage,last_stage_change,owner\n"


def parse(rows: str):
    return read_candidates((HEADER + rows).encode("utf-8"), TODAY)


class CSVValidationTests(unittest.TestCase):
    def test_utf8_bom(self):
        candidates, issues = read_candidates((HEADER + "1,Ana,Engineer,Interview,2026-11-10,Sam\n").encode("utf-8-sig"), TODAY)
        self.assertEqual((len(candidates), len(issues)), (1, 0))

    def test_missing_required_column_is_error(self):
        with self.assertRaisesRegex(ValueError, "Missing columns"):
            read_candidates(b"candidate_name,stage\nAna,Interview\n", TODAY)

    def test_invalid_date_skipped(self):
        candidates, issues = parse("1,Ana,Engineer,Interview,11/10/2026,Sam\n")
        self.assertEqual(len(candidates), 0)
        self.assertIn("invalid date", issues[0])

    def test_future_date_skipped(self):
        candidates, issues = parse("1,Ana,Engineer,Interview,2026-11-18,Sam\n")
        self.assertEqual(len(candidates), 0)
        self.assertIn("after analysis date", issues[0])

    def test_duplicate_id_skipped(self):
        candidates, issues = parse(
            "1,Ana,Engineer,Interview,2026-11-10,Sam\n"
            "1,Ben,Engineer,Assessment,2026-11-08,Sam\n"
        )
        self.assertEqual(len(candidates), 1)
        self.assertIn("duplicate", issues[0])

    def test_missing_name_skipped(self):
        candidates, issues = parse("1,,Engineer,Interview,2026-11-10,Sam\n")
        self.assertEqual(len(candidates), 0)
        self.assertIn("required", issues[0])


class AlertTests(unittest.TestCase):
    def test_exactly_at_threshold_is_flagged(self):
        candidates, _ = parse("1,Ana,Engineer,Interview,2026-11-10,Sam\n")
        alerts = assess_candidates(candidates, 7, TODAY)
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0].days_beyond_limit, 0)
        self.assertEqual(alerts[0].priority, "Follow up")

    def test_below_threshold_not_flagged(self):
        candidates, _ = parse("1,Ana,Engineer,Interview,2026-11-11,Sam\n")
        self.assertFalse(assess_candidates(candidates, 7, TODAY))

    def test_closed_stage_not_flagged(self):
        candidates, _ = parse("1,Ana,Engineer,Hired,2026-10-01,Sam\n")
        self.assertFalse(assess_candidates(candidates, 7, TODAY))
        self.assertEqual(summarize(candidates)["closed"], 1)

    def test_offer_stage_gets_higher_priority(self):
        candidates, _ = parse(
            "1,Ana,Engineer,Offer,2026-11-10,Sam\n"
            "2,Ben,Engineer,Interview,2026-11-10,Sam\n"
        )
        alerts = assess_candidates(candidates, 7, TODAY)
        self.assertEqual([a.priority for a in alerts], ["High", "Follow up"])
        self.assertEqual(alerts[0].candidate_name, "Ana")

    def test_urgent_overdue_comes_first(self):
        candidates, _ = parse(
            "1,Ana,Engineer,Interview,2026-11-10,Sam\n"
            "2,Ben,Engineer,Screening,2026-10-25,Lee\n"
        )
        alerts = assess_candidates(candidates, 7, TODAY)
        self.assertEqual(alerts[0].candidate_name, "Ben")
        self.assertEqual(alerts[0].priority, "Urgent")

    def test_stage_action_and_one_sentence_explanation(self):
        candidates, _ = parse("1,Ana,Engineer,Assessment,2026-11-08,Sam\n")
        alert = assess_candidates(candidates, 7, TODAY)[0]
        self.assertIn("assessment", alert.next_action.lower())
        self.assertEqual(alert.explanation.count("."), 1)

    def test_invalid_threshold(self):
        with self.assertRaises(ValueError):
            assess_candidates([], 0, TODAY)

    def test_export_fields(self):
        candidates, _ = parse("1,Ana,Engineer,Interview,2026-11-10,Sam\n")
        export = assess_candidates(candidates, 7, TODAY)[0].for_export()
        self.assertEqual(export["Days in stage"], 7)
        self.assertIn("Recommended action", export)


if __name__ == "__main__":
    unittest.main()
