import unittest
from unittest import mock
import argparse
import main


class TestArgParser(unittest.TestCase):

    def meta_test(self, inp, out, msg=None):
        real_out = main._get_parser(inp)
        self.assertEqual(real_out, out,
                         msg=msg or f"main._get_parser({inp}) should return "
                                    f"{out} and not {real_out}")

    @mock.patch('main._file_exists')
    def test_basic(self, mock_exists: mock.MagicMock):
        mock_exists.side_effect = lambda x: x
        inp = ['tests.csv', 'tests.jinja']
        out = ('tests.csv', 'tests.jinja', False, False, False)
        self.meta_test(inp, out)

    @mock.patch('main._file_exists')
    def test_file_exists(self, mock_exists: mock.MagicMock):
        mock_exists.side_effect = lambda x: x
        inp = ['tests.csv', 'tests.jinja']
        out = ('tests.csv', 'tests.jinja', False, False, False)
        self.meta_test(inp, out)
        mock_exists.assert_any_call('tests.csv')
        mock_exists.assert_any_call('tests.jinja')


class TestFileExists(unittest.TestCase):

    @mock.patch("main.open")
    def test_case_exists(self, mock_open):
        mock_open.return_value = True
        self.assertEqual(main._file_exists(mock.sentinel.file), mock.sentinel.file)

    @mock.patch("main.open")
    def test_case_not_exists(self, mock_open):
        mock_open.side_effect = FileNotFoundError
        with self.assertRaises(argparse.ArgumentError):
            main._file_exists(mock.sentinel.file)
        mock_open.assert_called_with(mock.sentinel.file, 'r')

    @mock.patch("main.open")
    def test_file_cannot_be_opened(self, mock_open):
        mock_open.side_effect = Exception
        with self.assertRaises(argparse.ArgumentError):
            main._file_exists(mock.sentinel.file)
        mock_open.assert_called_with(mock.sentinel.file, 'r')


if __name__ == '__main__':
    unittest.main()
