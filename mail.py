import smtplib
from email.message import EmailMessage
from typing import Union, List, TypeVar

SMTP_SERVER = "smtp.gmail.com:587"
SMTP_USER = "hadrien.renaud@animath.fr"
SMTP_PASSWORD = "m57kIlxhhqNu"


class SendingError(Exception):
    pass


T = TypeVar('T')
OneOrMany = Union[T, List[T]]


def send(content: str, sender: OneOrMany[str], receivers: OneOrMany[str],
         subject: str = None, **kwargs):
    """Send message."""
    # Message setup
    msg = EmailMessage()
    msg.set_content(content)
    # msg["From"] = _format_mail(sender)
    # msg['To'] = _format_mail(receivers)
    msg["From"] = sender
    msg['To'] = receivers

    if subject is not None:
        msg["Subject"] = subject

    for key, val in kwargs.items():
        msg[key] = val

    # Sending message
    with smtplib.SMTP(SMTP_SERVER) as server:
        server.ehlo()
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)


if __name__ == '__main__':
    message = """Ceci est un message de test ! 
        Le script a l'air de fonctionner."""
    source = "hadrien.renaud@animath.fr"
    target = "hadrien.renaud@animath.fr"
    subject = "Test du script d'envoi de mail"

    send(message, source, target, subject=subject)
