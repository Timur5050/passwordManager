import os
import smtplib
import time
from pathlib import Path

from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class MailLogger:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.port = 587
        self.username = os.getenv("MAIL_USERNAME")
        self.password = os.getenv("MAIL_PASSWORD")

    def send_message(self, email, text):
        try:
            message = MIMEMultipart()
            message["From"] = self.username
            message["To"] = email
            message["Subject"] = "code"

            message.attach(MIMEText(text, "plain"))

            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.sendmail(self.username, email, message.as_string())

        except Exception as e:
            raise RuntimeError(f"Failed to send email: {str(e)}")


def send_mail(email: str, message: str):
    logger = MailLogger()
    logger.send_message(email, message)
