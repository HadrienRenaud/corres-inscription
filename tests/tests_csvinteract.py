import unittest

import csvinteract


class CSVExtractTest(unittest.TestCase):

    def test_with_just_some_text(self):
        csv_file = open("./base_test.csv", "r")
        csv_extracted = csvinteract.extract(csv_file)
        self.assertEqual(csv_extracted, [['a', 'b'], ['c', 'd']])
