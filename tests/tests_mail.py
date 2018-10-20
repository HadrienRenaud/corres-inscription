import unittest
from unittest import mock

import mail


def identity(args):
    """Identity function x -> x."""
    return args


class SendMailTests(unittest.TestCase):

    @mock.patch("mail.EmailMessage")
    @mock.patch("mail.smtplib.SMTP")
    def test_basic(self, mock_smtp, mock_email_message):
        # Mock configuration
        mock_smtp.__enter__.return_value = mock_smtp
        mock_msg = mock.MagicMock()
        mock_email_message.return_value = mock_msg

        # Execution
        mail.send(mock.sentinel.content, mock.sentinel.sender,
                  mock.sentinel.receiver)

        # Verification
        mock_smtp.return_value = mock_smtp
        # mock_smtp.__enter__.assert_called_once()
        mock_smtp.assert_called_once()
        mock_email_message.assert_called_once()
        mock_msg.set_content.assert_called_with(mock.sentinel.content)
        mock_msg.__setitem__.assert_any_call("To", mock.sentinel.receiver)
        mock_msg.__setitem__.assert_any_call("From", mock.sentinel.sender)
