import smtplib
from email.message import EmailMessage
from typing import Union, List, TypeVar
import config


class SendingError(Exception):
    pass


T = TypeVar('T')
OneOrMany = Union[T, List[T]]


def send(send: bool = False, content: str = None, sender: OneOrMany[str] = None,
         receivers: OneOrMany[str] = None, subject: str = None, **kwargs):
    """Send message."""
    # Message setup
    if send:
        print(f"Sending mail :\n"
              f"  from: {sender}\n"
              f"  to: {receivers}\n"
              f"  subject: {subject}\n"
              f"  content: " + content.split('\n')[0] + " ...")

    msg = EmailMessage()
    msg["From"] = sender
    msg['To'] = receivers

    if subject is not None:
        msg["Subject"] = subject

    for key, val in kwargs.items():
        if key != "content":
            msg[key] = val
    msg.set_content(content)

    # Sending message
    if send:
        with smtplib.SMTP(config.SMTP_SERVER) as server:
            server.ehlo()
            server.starttls()
            server.login(config.SMTP_USER, config.SMTP_PASSWORD)
            server.send_message(msg)
            print("Done.")

    else:
        return str(msg)


if __name__ == '__main__':
    message = """Ceci est un message de test ! 
    Le script a l'air de fonctionner. Même si certaines fonctionnalités sont \
    encore à tester. """
    source = "tt247463@gmail.com"
    target = "tt247463@gmail.com"
    subj = "Test du script d'envoi de mail"
    with smtplib.SMTP(config.SMTP_SERVER) as server:
        server.ehlo()
        server.starttls()
        server.login(config.SMTP_USER, config.SMTP_PASSWORD)
        server.sendmail(source, target, message.encode(), ['SMTPUTF8'])
    send(True, message, source, target, subject=subj)
