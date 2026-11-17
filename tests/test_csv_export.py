"""Tests for spreadsheet CSV exports, including formula-like input."""

import csv
from io import StringIO
import unittest

from csv_export import EXPORT_COLUMNS, export_followups_csv, spreadsheet_safe_cell


class FormulaSafetyTests(unittest.TestCase):
    def test_prefixes_are_neutralized(self):
        for value in ("=1+1", "+1+1", "-1+1", "@SUM(1,1)",
                      "＝1+1", "＋1+1", "－1+1", "＠SUM(1,1)"):
            with self.subTest(value=value):
                self.assertEqual(spreadsheet_safe_cell(value), "\t" + value)

    def test_whitespace_and_control_prefixes(self):
        for value in ("  =1+1", "\t=1+1", "\r=1+1", "\n=1+1",
                      "\u200b=1+1", "\ufeff=1+1", "\u2028=1+1"):
            with self.subTest(value=repr(value)):
                self.assertEqual(spreadsheet_safe_cell(value), "\t" + value)

    def test_normal_fields_remain_unchanged(self):
        for value in ("Maria Santos", "A+B", "14", "Interview", "", "O'Connor"):
            with self.subTest(value=value):
                self.assertEqual(spreadsheet_safe_cell(value), value)

    def test_export_safeguards_every_column(self):
        value = '=1+1'
        row = {column: value for column in EXPORT_COLUMNS}
        decoded = export_followups_csv([row]).decode('utf-8-sig')
        reader = csv.DictReader(StringIO(decoded))
        out = list(reader)
        self.assertEqual(len(out), 1)
        self.assertEqual(list(out[0]), list(EXPORT_COLUMNS))
        self.assertTrue(all(v == '\t=1+1' for v in out[0].values()))
        self.assertTrue(decoded.startswith('"Candidate ID","Candidate"'))

    def test_delimiters_quotes_and_line_breaks_are_kept_in_one_cell(self):
        dangerous = '=1+1",=1+1\nother'  # harmless test payload
        result = export_followups_csv([{'Candidate': dangerous, 'Candidate ID': 'X01'}])
        parsed = list(csv.DictReader(StringIO(result.decode('utf-8-sig'))))
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]['Candidate'], '\t' + dangerous)
        self.assertEqual(parsed[0]['Candidate ID'], 'X01')

    def test_utf8_bom_empty_export_and_no_extraneous_fields(self):
        data = export_followups_csv([])
        self.assertTrue(data.startswith(b'\xef\xbb\xbf'))
        reader = csv.DictReader(StringIO(data.decode('utf-8-sig')))
        self.assertEqual(list(reader.fieldnames), list(EXPORT_COLUMNS))
        self.assertEqual(list(reader), [])

    def test_harmless_untrusted_csv_value_through_detection_engine(self):
        from datetime import date
        from engine import read_candidates, assess_candidates
        raw = ("candidate_id,candidate_name,role,stage,last_stage_change,owner\n"
               "S01,=1+1,Engineer,Interview,2026-11-01,Tester\n").encode('utf-8')
        candidates, problems = read_candidates(raw, date(2026, 11, 17))
        self.assertEqual(problems, [])
        result = assess_candidates(candidates, 7, date(2026, 11, 17))
        self.assertEqual(result[0].candidate_name, '=1+1')
        exported = export_followups_csv([result[0].for_export()])
        parsed = list(csv.DictReader(StringIO(exported.decode('utf-8-sig'))))
        self.assertEqual(parsed[0]['Candidate'], '\t=1+1')


if __name__ == '__main__':
    unittest.main()
