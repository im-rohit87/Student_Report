# from dotenv import load_dotenv
# import os

# load_dotenv()

# print("EMAIL_ID =", os.getenv("EMAIL_ID"))
# print("EMAIL_PASSWORD =", os.getenv("EMAIL_PASSWORD"))
# import smtplib
from pathlib import Path
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

from config import *


def send_email(receiver, attachment):

    try:

        msg = MIMEMultipart()

        msg["From"] = EMAIL_ID
        msg["To"] = receiver

        msg["Subject"] = (
            "Training Performance Report"
        )

        body = f"""
Dear Student,

Please find attached your training
performance grade card.

Regards,
Training Team
"""

        msg.attach(
            MIMEText(body, "plain")
        )

        part = MIMEBase(
            "application",
            "octet-stream"
        )

        with open(
            attachment,
            "rb"
        ) as f:

            part.set_payload(
                f.read()
            )

        encoders.encode_base64(part)

        filename = Path(
            attachment
        ).name

        part.add_header(
            "Content-Disposition",
            f"attachment; filename={filename}"
        )

        msg.attach(part)

        server = smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT
        )

        server.starttls()

        server.login(
            EMAIL_ID,
            EMAIL_PASSWORD
        )

        server.send_message(msg)

        server.quit()

        print(
            f"Email sent to {receiver}"
        )

    except Exception as e:

        print(
            f"Email failed for {receiver}: {e}"
        )

