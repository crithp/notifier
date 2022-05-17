"""
    Chris Thornton 2022-05-16
"""
import smtplib
import lib.shared_globals as shared_globals
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


# Base class for all senders
class Sender:
    def __init__(self, logger):
        self.name = None
        self.logger = logger

    def execute(self):
        raise NotImplementedError()

    def send_email(self, to: str, subject: str, body: str) -> bool:
        """
            Sending of mails can often go wrong, lots of try...excepts to cater for this
        """
        if not shared_globals.conf.email_enabled:
            return True

        from_address = shared_globals.conf.from_email
        login_mail = shared_globals.conf.login_email

        # Generate HTML attachment
        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        # Get text component for if HTML is disabled
        text = msg.as_string()

        try:
            # Attempt to login to mailbox
            server = smtplib.SMTP(login_mail, shared_globals.conf.login_port)
            server.starttls()
            server.login(login_mail, shared_globals.conf.login_password)
        except Exception as e:
            self.logger.error(f"Failed to connect to mailbox {login_mail} with error {str(e)}")
            return False

        try:
            # Actually send the mail
            server.sendmail(from_address, to, text)
            return True
        except Exception as e:
            self.logger.error(f"Failed to send to mailbox {to} with error {str(e)}")
            return False
        finally:  # If we got this far, we still have an open mailbox that needs closing
            server.quit()
