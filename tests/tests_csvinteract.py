import unittest
from unittest import mock

import csvinteract


class IsNumericTest(unittest.TestCase):
    """Test for _isnumeric."""

    def _test_(self, value: str, expected: bool):
        if expected:
            msg = f"'{value}' should be considered as numeric"
            self.assertTrue(csvinteract._isnumeric(value), msg=msg)
        else:
            msg = f"'{value}' should not be considered as numeric"
            self.assertFalse(csvinteract._isnumeric(value), msg=msg)

    def test_int(self):
        self._test_("0", True)
        self._test_("9", True)
        self._test_("-8", True)

    def test_bool(self):
        self._test_("0.8", True)
        self._test_("9987.7632", True)
        # self._test_("inf", True)
        self._test_("-9823.7", True)
        self._test_(".8", True)
        self._test_("4.5e-8", True)
        self._test_("-9e9", True)

    def test_wrong(self):
        self._test_("lsrgjts", False)
        self._test_("", False)
        self._test_("872,45", False)
        self._test_("recu", False)


class ParseCellTest(unittest.TestCase):
    """Test for csvinteract._parse_cell."""

    def _test_(self, value, expected):
        msg = f"'{value}' should be converted to {expected}"
        self.assertEqual(csvinteract._parse_cell(value), expected, msg=msg)

    def test_numeric(self):
        cases = [
            0,
            1,
            -9,
            89.29875,
            45e-75,
        ]
        for case in cases:
            self._test_(str(case), case)

    def test_string(self):
        cases = [
            "test",
            "bonjour",
            "_fsr",
            "-9 = fsrk",
            "ich bin ein Berliner"
        ]
        for case in cases:
            self._test_(case, case)


class CSVExtractTest(unittest.TestCase):
    """Test for csvinteract.extract."""

    @mock.patch("csvinteract.open")
    def meta_test(self, value_called, expected_value, mock_open):
        # Preparation
        mock_open.return_value = mock_open
        mock_open.__enter__.return_value = value_called
        file = mock.sentinel.file_name

        # Execution
        csv_extracted = csvinteract.extract(file)

        # Analyse du résultat
        mock_open.assert_called_with(mock.sentinel.file_name, 'r')
        self.assertEqual(csv_extracted, expected_value)

    def test_with_text(self):
        expected_value = [['a', 'b'], ['c', 'd']]
        value_called = [','.join(row) for row in expected_value]
        self.meta_test(value_called, expected_value)

    def test_with_text_and_int(self):
        expected_value = [[0, 'b'], [1, 'd']]
        value_called = ["0,b", "1,d"]
        self.meta_test(value_called, expected_value)

    def test_with_float(self):
        expected_value = [[0.5, 'b'], [1, 'd']]
        value_called = ["0.5,b", "1,d"]
        self.meta_test(value_called, expected_value)
