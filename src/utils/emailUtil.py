from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import List


conf = ConnectionConfig(
    MAIL_USERNAME="rk848506@gmail.com",
    MAIL_PASSWORD="utpyjxlkhiehsqoj",
    MAIL_FROM="rk848506@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="Lifeopedia"
)


def send_email(subject: str, recipient: List, message: str):
    message = MessageSchema(
        subject=subject,
        recipients=recipient,
        body=message,
        subtype="html"
    )
    print(message)
    fm = FastMail(conf)
    return fm.send_message(message)
