import unittest
from unittest import mock


class SendMailTests(unittest.TestCase):

    @mock.patch("mail.smtplib.SMTP")
    def basic_test_case(self, mock_smtp):
        # Mock configuration
        pass
