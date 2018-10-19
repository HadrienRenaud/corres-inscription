import unittest
from unittest import mock

import csvinteract


class CSVExtractTest(unittest.TestCase):

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
